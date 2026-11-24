"""Wortwahl und Anzeige ab 1.5.17: „Take-away“ statt „Verkaufen“ (mit Take-away-Symbol statt Mülltonne), „Bessere Artikel“ mit Chance in Prozent,
Glückstreffer „Stufe 2!“ beim Erzeugen, Stufe 1 ohne Zahl auf dem Teil. Deutsch und Englisch. Aufruf: python3 -I tests/test_wortwahl.py"""
import asyncio, json, datetime, sys, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []
def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))
async def mk(b, locale='de-DE'):
    pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, locale=locale)
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    st = json.dumps(BASE).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % st)
    await pg.goto(URL); await pg.wait_for_timeout(1300)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(600)
    except Exception: pass
    await pg.wait_for_timeout(1500)
    return pg
async def modal(pg): return await pg.evaluate("document.getElementById('modalBody').innerText.replace(/\\s+/g,' ')")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = await mk(b)
        tr = await pg.evaluate("document.querySelector('#trash').innerText.trim()")
        ok('DE Ablage heißt „Take-away“ mit Take-away-Symbol (keine Mülltonne)', tr == 'Take-away' and await pg.evaluate("document.querySelector('#trash use').getAttribute('href')") == '#i-togo' and not await pg.evaluate("!!document.getElementById('i-bin')"), tr)
        ok('DE „Verkaufen“ und „Mülleimer“ kommen im Spiel nicht mehr vor', not await pg.evaluate("/Verkaufen|Mülleimer|Mülltonne/.test(document.body.innerText)"))
        await pg.evaluate("MC.state().up.gen=0; MC.ups()"); await pg.wait_for_timeout(400)
        tt = await modal(pg)
        ok('DE Ausbau: „Bessere Artikel“, Chance 10 % → 15 %', 'Bessere Artikel' in tt and 'Chance auf Stufe 2 beim Erzeugen: 10 % → 15 %' in tt and 'Zutaten' not in tt, tt[:160])
        await pg.evaluate("MC.close(); MC.state().up.gen=3; MC.ups()"); await pg.wait_for_timeout(300)
        ok('DE Ausbau Stufe 3: 25 % → 30 %', '25 % → 30 %' in await modal(pg))
        await pg.evaluate("MC.close(); MC.state().up.gen=5; MC.ups()"); await pg.wait_for_timeout(300)
        tt = await modal(pg)
        ok('DE Ausbau am Ende: nur 35 %, kein Pfeil', 'Erzeugen: 35 %' in tt and '→' not in tt.split('Großer Akku')[0], tt[:160])
        await pg.evaluate("MC.close()")
        # Glückstreffer: Zufall erzwingen
        await pg.evaluate("MC.state().tut=3; MC.state().energy=90; MC.render()")
        gi = await pg.evaluate("MC.state().b.findIndex(x=>x&&x.g!==undefined)")
        n0 = await pg.evaluate("MC.state().b.filter(x=>x&&x.g===undefined).length")
        await pg.evaluate("Math.random=()=>0"); await pg.click(f'#board .cell:nth-child({gi + 1})', force=True); await pg.wait_for_timeout(1100)
        fl = await pg.evaluate("[...document.querySelectorAll('.float')].map(e=>e.textContent)")
        ok('DE Treffer (Zufall 0): neues Teil Stufe 2, Hinweis „Stufe 2!“', await pg.evaluate("MC.state().b.filter(x=>x&&x.g===undefined).length") == n0 + 1 and 'Stufe 2!' in fl, fl)
        await pg.evaluate("Math.random=()=>.99"); await pg.wait_for_timeout(1500)
        await pg.click(f'#board .cell:nth-child({gi + 1})', force=True); await pg.wait_for_timeout(1100)
        fl = await pg.evaluate("[...document.querySelectorAll('.float')].map(e=>e.textContent)")
        ok('DE ohne Treffer (Zufall .99): kein Hinweis', 'Stufe 2!' not in fl, fl)
        r = await pg.evaluate("(()=>{const b=MC.state().b;const hi=b.filter(x=>x&&x.g===undefined&&x.t>0).length;const badges=[...document.querySelectorAll('#board .cell .tier')].map(e=>e.textContent);return [hi,badges.length,badges.includes('1')]})()")
        ok('Stufe 1 ohne Zahl: nur Teile ab Stufe 2 tragen eine Zahl', r[0] == r[1] and not r[2], r)
        ok('DE keine Fehler', not pg.errs, pg.errs); await pg.close()
        # Englisch
        pg = await mk(b, 'en-US')
        ok('EN Ablage heißt „Take-away“', await pg.evaluate("document.querySelector('#trash').innerText.trim()") == 'Take-away')
        await pg.evaluate("MC.state().up.gen=0; MC.ups()"); await pg.wait_for_timeout(400)
        tt = await modal(pg)
        ok('EN Ausbau: „Better Items“, Chance 10% → 15%', 'Better Items' in tt and 'Chance of tier 2 when producing: 10% → 15%' in tt and 'Ingredient' not in tt, tt[:160])
        ok('EN keine Fehler', not pg.errs, pg.errs); await pg.close()
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
    sys.exit(0 if all(res) else 1)
asyncio.run(main())
