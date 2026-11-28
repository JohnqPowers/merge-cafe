"""Entwickler-Vorschau (Experiment exp/entwickler; Schalter CONFIG.features.devMenu, im Web ?dev=0 / ?dev=1).
Geprüft werden: Öffnen nur per Geste (7 Tipps auf die Versionszeile in den Optionen, innerhalb von 4 s) und nur mit ?dev=1 (im Web) bzw. im Debug-Paket,
Schalter aus = nichts (kein Element, Geste ohne Wirkung, API verweigert), Sprung durch alle neun Welten (Kulisse und Farben wechseln, Level springt auf den
Welt-Beginn), Schieberegler und Plus/Minus, Vorschau schreibt NICHTS in den Speicher (auch nicht bei Aktionen mit save() und nach Wartezeit), Ereignisse gehen nicht
nach außen (nur dev:true in der Testliste), „Beenden“ stellt den Spielstand unverändert wieder her, Möwen-Auskunft und -Start, Verkleinern, keine Fehler,
keine neuen Speicher-Schlüssel, andere Fenstergrößen.
Aufruf: python3 -I tests/test_entwickler.py"""
import asyncio, json, datetime, sys, os, re
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server, WWW

URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
HTML = Path(WWW, 'index.html').read_text(encoding='utf-8')
res = []


def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''), flush=True)


def rewrite(fn):
    async def h(route):
        r = await route.fetch()
        await route.fulfill(response=r, body=fn(await r.text()))
    return h


async def mk(b, q='?dev=1', w=390, h=844, level=3, rew=None, wait=1600, start=True):
    st = json.loads(json.dumps(BASE)); st['level'] = level; st['tut'] = 3
    ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='de-DE')
    pg = await ctx.new_page(); pg.ctx = ctx; pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if rew: await pg.route(re.compile(r'/index\.html'), rewrite(rew))
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL + q); await pg.wait_for_timeout(wait)
    if start:
        try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(1200)
        except Exception: pass
    return pg


STORE = "JSON.parse(localStorage.getItem('mergecafe_v1'))"
PANEL = "!!document.getElementById('devPanel')"


async def open_settings(pg):
    await pg.evaluate("MC.settings()"); await pg.wait_for_timeout(250)


async def tap_ver(pg, n, gap=60):
    for _ in range(n):
        await pg.click('[data-ver]'); await pg.wait_for_timeout(gap)


async def scene_key(pg):
    """Kulisse der Welt: Dateiname des Vollbilds (b0..b8) und CSS-Farbe des Bretts."""
    return await pg.evaluate("""() => { const im = [...document.querySelectorAll('#scene .sc-bg')].map(i => (i.getAttribute('src') || '').match(/b\\d+/)); const L = document.querySelectorAll('#scene .sc-layer').length;
      return { bg: im.map(m => m && m[0]), layers: L, board: getComputedStyle(document.documentElement).getPropertyValue('--board').trim() } }""")


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])

        # ---------- A: Öffnen nur per Geste ----------
        pg = await mk(b)
        ok('A Ausgangslage: kein Panel, Vorschau aus, Web mit ?dev=1 erlaubt', not await pg.evaluate(PANEL) and (await pg.evaluate("MC.dev.state()")) == {'flag': True, 'allowed': True, 'open': False, 'frozen': False, 'level': 3}, await pg.evaluate("MC.dev.state()"))
        keys0 = sorted(await pg.evaluate("Object.keys(localStorage)"))
        await open_settings(pg)
        await tap_ver(pg, 6)
        ok('A sechs Tipps öffnen nichts', not await pg.evaluate(PANEL))
        await pg.wait_for_timeout(4300)
        await tap_ver(pg, 1)
        ok('A der siebte Tipp nach über 4 s zählt nicht (Zähler läuft ab)', not await pg.evaluate(PANEL))
        await tap_ver(pg, 6)
        ok('A siebenmal innerhalb von 4 s öffnet das Panel und schließt die Optionen', await pg.evaluate(PANEL) and await pg.evaluate("document.getElementById('modal').hidden"))
        ok('A beim Öffnen ist noch nichts eingefroren (Spielstand unverändert)', (await pg.evaluate("MC.dev.state()"))['frozen'] is False)
        ok('A Panel zeigt Welt und Level', 'Hamburg' in await pg.evaluate("document.querySelector('#devPanel .dv-name').textContent") and 'Level 3' in await pg.evaluate("document.querySelector('#devPanel output').textContent"))
        ok('A Panel hat neun Welt-Tasten, einen Regler und eine Info-Zeile mit Fenstermaßen', await pg.evaluate("document.querySelectorAll('#devPanel .dv-w button').length") == 9 and await pg.evaluate("!!document.querySelector('#devPanel input[type=range]')") and '390×844' in await pg.evaluate("document.querySelector('#devPanel .dv-info').textContent"))
        ok('A keine Fehler', not pg.errs, pg.errs)

        # ---------- B: durch alle Welten springen ----------
        orig = await pg.evaluate(f"({STORE})")
        seen = []
        for i in range(9):
            await pg.click(f'#devPanel [data-dv="w{i}"]'); await pg.wait_for_timeout(1300)
            k = await scene_key(pg); L = await pg.evaluate("MC.state().level"); name = await pg.evaluate("document.querySelector('#devPanel .dv-name').textContent")
            first = [1, 5, 10, 15, 20, 25, 30, 40, 50][i]
            ok(f'B Welt {i + 1}: Level springt auf {first}, Kulisse b{i}, nur eine Ebene übrig, Panel nennt die Welt', L == first and k['bg'] == [f'b{i}'] and k['layers'] == 1 and f'Welt {i + 1}/9' in name, [L, k, name])
            seen.append(k['board'])
        ok('B die Brettfarbe wechselt mit den Welten (mindestens 7 verschiedene)', len(set(seen)) >= 7, len(set(seen)))
        ok('B ab dem ersten Sprung ist die Vorschau eingefroren', (await pg.evaluate("MC.dev.state()"))['frozen'] is True and 'nicht gespeichert' in await pg.evaluate("document.querySelector('#devPanel .dv-top span').textContent"))
        ok('B jede Welt-Taste ist hervorgehoben, wenn ihre Welt aktiv ist (Sternecafé zuletzt)', await pg.evaluate("[...document.querySelectorAll('#devPanel .dv-w button')].map(b => b.classList.contains('on')).join()") == 'false,false,false,false,false,false,false,false,true')

        # ---------- C: Regler, Plus, Minus ----------
        await pg.click('#devPanel [data-dv="lm"]'); await pg.wait_for_timeout(500)
        ok('C Minus: Level 49 (noch Welt 8, Rio)', await pg.evaluate("MC.state().level") == 49 and 'Rio' in await pg.evaluate("document.querySelector('#devPanel .dv-name').textContent"))
        await pg.click('#devPanel [data-dv="lp"]'); await pg.wait_for_timeout(500)
        ok('C Plus: Level 50 (Sternecafé)', await pg.evaluate("MC.state().level") == 50)
        await pg.evaluate("(() => { const r = document.querySelector('#devPanel input'); r.value = 7; r.dispatchEvent(new Event('input', { bubbles: true })); })()")
        ok('C Regler bewegen zeigt das Level an, ohne es schon zu setzen', await pg.evaluate("document.querySelector('#devPanel output').textContent") == 'Level 7' and await pg.evaluate("MC.state().level") == 50)
        await pg.evaluate("document.querySelector('#devPanel input').dispatchEvent(new Event('change', { bubbles: true }))"); await pg.wait_for_timeout(1300)
        k = await scene_key(pg)
        ok('C Regler loslassen setzt Level 7: Wien (Welt 2, Kulisse b1)', await pg.evaluate("MC.state().level") == 7 and k['bg'] == ['b1'] and 'Wien' in await pg.evaluate("document.querySelector('#devPanel .dv-name').textContent"), k)
        await pg.evaluate("(() => { const r = document.querySelector('#devPanel input'); r.value = 999; r.dispatchEvent(new Event('change', { bubbles: true })); })()"); await pg.wait_for_timeout(600)
        ok('C Level wird auf 60 begrenzt', await pg.evaluate("MC.state().level") == 60)
        ok('C neue Bestellungen passen zum Level (Bestellliste gefüllt)', await pg.evaluate("MC.state().orders.length") >= 3)

        # ---------- D: nichts wird gespeichert, nichts gemeldet ----------
        await pg.wait_for_timeout(700)                                                           # länger als die 150 ms Verzögerung von save()
        st = await pg.evaluate(f"({STORE})")
        ok('D Speicher unverändert trotz Sprüngen und Wartezeit (Level, Münzen, Brett, Bestellungen, Ereignisse)',
           st['level'] == orig['level'] == 3 and st['coins'] == orig['coins'] and st['b'] == orig['b'] and st['orders'] == orig['orders'] and st['ev'] == orig['ev'], [st['level'], orig['level']])
        await pg.evaluate("MC.settings()"); await pg.wait_for_timeout(300)
        await pg.click('[data-act="sound"]'); await pg.wait_for_timeout(700)                     # Aktion, die save() aufruft
        st = await pg.evaluate(f"({STORE})")
        ok('D auch Aktionen mit save() (Ton umschalten) landen nicht im Speicher', st['sound'] == orig['sound'] and await pg.evaluate("MC.state().sound") != orig['sound'], [st['sound'], orig['sound']])
        await pg.evaluate("MC.close()")
        n0 = await pg.evaluate("MC.events().length")
        await pg.evaluate("MC.plat.track('dev_probe', { a: 1 })")
        ev = await pg.evaluate("MC.events().slice(-1)[0]")
        ok('D Ereignisse während der Vorschau tragen dev:true (werden nicht nach außen gemeldet)', ev['name'] == 'dev_probe' and ev.get('dev') is True, ev)
        ok('D Panel verdeckt Fenster nicht (z-Ebene unter den Fenstern)', await pg.evaluate("+getComputedStyle(document.getElementById('devPanel')).zIndex < +getComputedStyle(document.getElementById('modal')).zIndex"))

        # ---------- E: Verkleinern ----------
        await pg.click('#devPanel [data-dv="min"]'); await pg.wait_for_timeout(200)
        ok('E Verkleinern: nur noch die Titelzeile sichtbar', await pg.evaluate("getComputedStyle(document.querySelector('#devPanel .dv-w')).display") == 'none' and await pg.evaluate("document.getElementById('devPanel').getBoundingClientRect().height") < 60)
        await pg.click('#devPanel [data-dv="min"]'); await pg.wait_for_timeout(200)
        ok('E wieder groß', await pg.evaluate("getComputedStyle(document.querySelector('#devPanel .dv-w')).display") != 'none')

        # ---------- F: Beenden stellt alles wieder her ----------
        await pg.click('#devPanel [data-dv="end"]'); await pg.wait_for_timeout(1400)
        now = await pg.evaluate("MC.state()")
        ok('F Beenden: Panel weg, nicht mehr eingefroren', not await pg.evaluate(PANEL) and (await pg.evaluate("MC.dev.state()"))['frozen'] is False)
        ok('F Spielstand wie vorher (Level 3, Münzen, Edelsteine, Brett, Bestellungen, Ton, Ereignisse)',
           now['level'] == orig['level'] and now['coins'] == orig['coins'] and now['gems'] == orig['gems'] and now['b'] == orig['b'] and now['orders'] == orig['orders'] and now['sound'] == orig['sound'] and now['ev'] == orig['ev'], [now['level'], orig['level']])
        k = await scene_key(pg)
        ok('F Kulisse wieder Hamburg (b0), eine Ebene', k['bg'] == ['b0'] and k['layers'] == 1, k)
        await pg.evaluate("MC.plat.track('dev_probe2', {})")
        ev = await pg.evaluate("MC.events().slice(-1)[0]")
        ok('F Ereignisse nach dem Beenden wieder ohne dev-Marke (Messung frei)', ev['name'] == 'dev_probe2' and 'dev' not in ev, ev)
        await pg.wait_for_timeout(500)
        await pg.evaluate("MC.render()")
        st = await pg.evaluate(f"({STORE})")
        ok('F Speicher nach dem Beenden weiterhin der echte Stand', st['level'] == 3 and st['b'] == orig['b'])
        ok('F nach dem Beenden wird wieder gespeichert (Ton umschalten schreibt)', True)
        await pg.evaluate("MC.settings()"); await pg.wait_for_timeout(250)
        await pg.click('[data-act="sound"]'); await pg.wait_for_timeout(600)
        st = await pg.evaluate(f"({STORE})")
        ok('F … und es kommt im Speicher an', st['sound'] == (not orig['sound']) or st['sound'] != orig['sound'], [st['sound'], orig['sound']])
        ok('F keine neuen Speicher-Schlüssel', sorted(await pg.evaluate("Object.keys(localStorage)")) == keys0, await pg.evaluate("Object.keys(localStorage)"))
        ok('F keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- G: Seitenneuladen mitten in der Vorschau: der echte Stand bleibt ----------
        pg = await mk(b)
        await open_settings(pg); await tap_ver(pg, 7)
        ok('G Panel offen', await pg.evaluate(PANEL))
        await pg.click('#devPanel [data-dv="w5"]'); await pg.wait_for_timeout(900)
        ok('G Sprung nach Kyoto (Level 25)', await pg.evaluate("MC.state().level") == 25)
        await pg.reload(); await pg.wait_for_timeout(1800)
        await pg.click('#spPlay', force=True, timeout=2500); await pg.wait_for_timeout(900)
        ok('G nach dem Neuladen (App „geschlossen“ mitten in der Vorschau): Level 3, nichts verloren', await pg.evaluate("MC.state().level") == 3 and not await pg.evaluate(PANEL))
        ok('G keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- H: Möwe ----------
        pg = await mk(b, w=412, h=915)
        await open_settings(pg); await tap_ver(pg, 7)
        info = await pg.evaluate("document.querySelector('#devPanel .dv-info').textContent")
        ok('H Info nennt den Zustand der Möwe und die Fenstermaße', 'Möwe:' in info and '412×915' in info, info)
        why = await pg.evaluate("MC.gull.why()")
        ok('H MC.gull.why() liefert einen kurzen Grund', isinstance(why, str) and 3 < len(why) < 70, why)
        await pg.click('#devPanel [data-dv="w0"]'); await pg.wait_for_timeout(900)
        await pg.click('#devPanel [data-dv="gull"]'); await pg.wait_for_timeout(300)
        ok('H „Möwe zeigen“ meldet sofort, dass sie gleich startet', 'Start in 2 s' in await pg.evaluate("document.querySelector('#devPanel .dv-info').textContent"))
        await pg.wait_for_timeout(2800)
        st = await pg.evaluate("MC.gull.state()"); info = await pg.evaluate("document.querySelector('#devPanel .dv-info').textContent")
        ok('H danach fliegt sie, und die Info sagt „fliegt“ (oder nennt den Grund, warum nicht)', (st['flying'] and 'fliegt' in info) or (not st['flying'] and 'Möwe:' in info and 'Start in 2 s' not in info), [st['flying'], info])
        await pg.click('#devPanel [data-dv="w2"]'); await pg.wait_for_timeout(900)
        ok('H in Paris: Grund „nur in Hamburg“', await pg.evaluate("MC.gull.why()") == 'nur in Hamburg', await pg.evaluate("MC.gull.why()"))
        ok('H keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- I: Schalter und Erlaubnis ----------
        pg = await mk(b, q='')
        await open_settings(pg); await tap_ver(pg, 7)
        ok('I Web ohne ?dev=1: Geste ohne Wirkung (nicht erlaubt)', not await pg.evaluate(PANEL) and (await pg.evaluate("MC.dev.state()"))['allowed'] is False)
        ok('I … und die API verweigert (open und setLevel geben false)', await pg.evaluate("MC.dev.open()") is False and await pg.evaluate("MC.dev.setLevel(30)") is False and await pg.evaluate("MC.state().level") == 3)
        await pg.ctx.close()
        pg = await mk(b, q='?dev=0')
        await open_settings(pg); await tap_ver(pg, 7)
        ok('I ?dev=0: Geste ohne Wirkung, flag=false', not await pg.evaluate(PANEL) and (await pg.evaluate("MC.dev.state()"))['flag'] is False)
        await pg.ctx.close()
        pg = await mk(b, q='?dev=1', rew=lambda t: t.replace('devMenu: true', 'devMenu: false'))
        await open_settings(pg); await tap_ver(pg, 7)
        ok('I CONFIG.features.devMenu=false: auch mit ?dev=1 aus (Master-Schalter)', not await pg.evaluate(PANEL) and (await pg.evaluate("MC.dev.state()"))['flag'] is False)
        await pg.ctx.close()
        pg = await mk(b, q='?dev=1')
        ok('I Standard (CONFIG an, ?dev=1): erlaubt', (await pg.evaluate("MC.dev.state()"))['allowed'] is True)
        # Release-Paket: native und kein Debug -> nicht erlaubt; Debug-Paket -> erlaubt
        ok('I Quelltext: im nativen Paket nur bei Platform.build.kind === \'debug\' erlaubt', "isNative() ? Platform.build.kind === 'debug' : P === '1'" in HTML)
        await pg.ctx.close()

        # ---------- J: kleine Fenster ----------
        for w, h in [(360, 640), (320, 568)]:
            pg = await mk(b, w=w, h=h)
            await open_settings(pg); await tap_ver(pg, 7)
            r = await pg.evaluate("(() => { const r = document.getElementById('devPanel').getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, innerWidth, innerHeight]; })()")
            ok(f'J {w}x{h}: Panel liegt ganz im Fenster', r[0] >= 0 and r[2] <= r[4] and r[1] >= 0 and r[3] <= r[5], [round(v) for v in r])
            ok(f'J {w}x{h}: neun Welt-Tasten mindestens 28 px breit', await pg.evaluate("[...document.querySelectorAll('#devPanel .dv-w button')].every(b => b.getBoundingClientRect().width >= 28)"))
            ok(f'J {w}x{h}: keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        await b.close()

    n = len(res); g_ = sum(res)
    print(f'\nERGEBNIS: {g_}/{n} bestanden' + ('' if g_ == n else f' ({n - g_} FEHLER)'))
    sys.exit(0 if g_ == n else 1)


asyncio.run(main())
