"""Spielstand-Kompatibilität: Ein Update darf alte, unvollständige oder kaputte Spielstände nie in einen Absturz verwandeln.
Der Schlüssel `mergecafe_v1` bleibt (siehe docs/TECHNIK.md, Abschnitt 7). Neue Felder bekommen beim Laden Standardwerte.
Aufruf: python3 -I tests/test_spielstand.py"""
import asyncio, json, os, sys, datetime
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
FAILS = []
def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (f' | {info}' if info != '' else ''))
    if not cond: FAILS.append(name)

N = 56   # 7 Spalten × 8 Zeilen

def alt(**extra):
    """Spielstand im Stil einer frühen Version: nur die Grundfelder, alte Emoji-Figur, keine Felder für Geschenke, Welt, Katze usw."""
    b = [None] * N
    b[3 + 7 * 7] = {'g': 0}; b[16] = {'c': 0, 't': 0}; b[17] = {'c': 0, 't': 1}
    s = {'v': 1, 'b': b, 'energy': 40, 'coins': 120, 'gems': 7, 'xp': 5, 'level': 3, 'tut': 3,
         'profile': {'name': 'Alt', 'cafe': 'Altcafé', 'avatar': '🦊', 'done': True}}
    s.update(extra); return s

async def probe(b, raw, w=390, h=844):
    """Spielt `raw` (Text, so wie er im Speicher steht) als Spielstand ein, startet das Spiel und liefert Zustand, Zellenzahl und Fehler."""
    ctx = await b.new_context(viewport={'width': w, 'height': h}, locale='de-DE')
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    await pg.add_init_script("localStorage.setItem('mergecafe_v1', %s)" % json.dumps(raw))
    await pg.goto(URL); await pg.wait_for_timeout(2500)
    st = await pg.evaluate("(() => { const s = MC.state(); return { level: s.level, coins: s.coins, gems: s.gems, gifts: s.gifts, tut: s.tut, avatar: s.profile.avatar, name: s.profile.name, done: s.profile.done, worldPick: s.worldPick, daily: s.daily, ads: s.ads, stats: s.stats, up: s.up, extra: s.zukunft || null } })()")
    cells = await pg.evaluate("document.querySelectorAll('.cell').length")
    await ctx.close(); return st, cells, errs

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])

        st, cells, e = await probe(b, json.dumps(alt()))
        ok('A alter Spielstand: Stufe, Münzen, Diamanten bleiben', (st['level'], st['coins'], st['gems']) == (3, 120, 7), st)
        ok('A alte Emoji-Figur wird auf neue ID umgestellt (🦊 → a3)', st['avatar'] == 'a3', st['avatar'])
        ok('A Name bleibt, Profil gilt als fertig (kein erneutes Onboarding)', st['name'] == 'Alt' and st['done'] is True, st)
        ok('A neue Felder bekommen Standardwerte', st['gifts'] == 0 and st['worldPick'] is None and isinstance(st['daily'], dict) and isinstance(st['ads'], dict) and isinstance(st['stats'], dict) and isinstance(st['up'], dict), st)
        ok('A Brett hat 56 Zellen', cells == N, cells)
        ok('A keine Fehler', not e, e)

        st, cells, e = await probe(b, json.dumps(alt(zukunft={'x': 1}, gifts=2, worldPick=0)))
        ok('B unbekannte Zusatzfelder und vorhandene Felder bleiben erhalten', st['extra'] == {'x': 1} and st['gifts'] == 2 and st['worldPick'] == 0, st)
        ok('B keine Fehler', not e, e)

        st, cells, e = await probe(b, '{kaputt')
        ok('C kaputter Text: neues Spiel, kein Absturz', st['level'] == 1 and st['coins'] == 0 and cells == N, (st, cells))
        ok('C keine Fehler', not e, e)

        st, cells, e = await probe(b, json.dumps(alt(v=2)))
        ok('D fremde Version (v=2): neues Spiel statt Absturz', st['level'] == 1 and cells == N, (st, cells))
        ok('D keine Fehler', not e, e)

        bad = alt(); bad['b'] = [None] * 10
        st, cells, e = await probe(b, json.dumps(bad))
        ok('E falsche Brettgröße: neues Spiel statt Absturz', st['level'] == 1 and cells == N, (st, cells))
        ok('E keine Fehler', not e, e)

        st, cells, e = await probe(b, json.dumps(alt(profile=None)))
        ok('F Profil leer (null): Standardprofil, kein Absturz', st['avatar'] == 'a1' and cells == N, (st, cells))
        ok('F keine Fehler', not e, e)

        st, cells, e = await probe(b, json.dumps(alt(profile={'name': 'X', 'avatar': 'unbekannt', 'done': True})))
        ok('G unbekannte Figur-Kennung: Ersatzfigur a1, kein Absturz', st['avatar'] == 'a1', st)
        ok('G keine Fehler', not e, e)

        real = json.loads(open(STATE, encoding='utf-8').read().replace('@@TODAY@@', datetime.date.today().isoformat()))
        st, cells, e = await probe(b, json.dumps(real), 360, 640)
        ok('H Spielstand Level 12 (Paris) lädt bei 360×640', st['level'] == 12 and cells == N, (st['level'], cells))
        ok('H keine Fehler', not e, e)

        await b.close()
    print(f'\nERGEBNIS: {"ALLE bestanden" if not FAILS else str(len(FAILS)) + " FEHLER: " + ", ".join(FAILS)}')
    sys.exit(1 if FAILS else 0)
asyncio.run(main())
