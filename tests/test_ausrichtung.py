"""Ausrichtung: Im Hochformat und auf Tablets bleibt das Spiel frei; im Querformat auf dem Handy (oder in sehr niedrigen Fenstern) deckt der Dreh-Hinweis alles ab, damit niemand vor einem unerreichbaren Start-Knopf sitzt.
Aufruf: python3 -I tests/test_ausrichtung.py"""
import asyncio, json, os, sys, datetime
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
FAILS = []
def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (f' | {info}' if info != '' else '')); 
    if not cond: FAILS.append(name)

async def main():
    st = open(STATE, encoding='utf-8').read().replace('@@TODAY@@', datetime.date.today().isoformat())
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        async def probe(w, h, lang='de-DE'):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, locale=lang)
            pg = await ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            await pg.add_init_script("localStorage.setItem('mergecafe_v1', %s)" % json.dumps(st))
            await pg.goto(URL); await pg.wait_for_timeout(2500)
            r = await pg.evaluate("""(() => { const e = document.getElementById('rotate'), cs = getComputedStyle(e), b = e.getBoundingClientRect();
                const top = document.elementFromPoint(innerWidth / 2, innerHeight / 2);
                return { shown: cs.display !== 'none', cover: Math.round(b.width) === innerWidth && Math.round(b.height) === innerHeight, onTop: e.contains(top), text: document.getElementById('rotT').textContent } })()""")
            await ctx.close(); return r, errs
        r, e = await probe(390, 844); ok('Handy hochkant 390x844: kein Hinweis', not r['shown'], r); ok('  keine Konsolenfehler', not e, e)
        r, e = await probe(360, 640); ok('Handy hochkant 360x640: kein Hinweis', not r['shown'], r)
        r, e = await probe(844, 390); ok('Handy quer 844x390: Hinweis deckt alles ab', r['shown'] and r['cover'] and r['onTop'], r); ok('  Text deutsch', 'Hochformat' in r['text'], r['text']); ok('  keine Konsolenfehler', not e, e)
        r, e = await probe(844, 390, 'en-US'); ok('Handy quer, Englisch: Text englisch', 'portrait' in r['text'], r['text'])
        r, e = await probe(700, 520); ok('Niedriges Fenster 700x520: Hinweis', r['shown'] and r['onTop'], r)
        r, e = await probe(1024, 600); ok('Tablet quer 1024x600: kein Hinweis', not r['shown'], r)
        r, e = await probe(1280, 800); ok('Tablet quer 1280x800: kein Hinweis', not r['shown'], r)
        r, e = await probe(810, 1080); ok('Tablet hochkant 810x1080: kein Hinweis', not r['shown'], r)
        await b.close()
    print(f'\nERGEBNIS: {"ALLE bestanden" if not FAILS else str(len(FAILS)) + " FEHLER: " + ", ".join(FAILS)}')
    sys.exit(1 if FAILS else 0)
asyncio.run(main())
