"""Katze Mocha (ab 1.5.17 nur noch Ruhebild im Bestellbereich, kein Sprung und kein Streicheln mehr): Bild geladen, nur die drei Ruhe-Dateien
im Netz, kein Schnurr-Ton, keine Flug-Ebene, Antippen = Miau und Hinweis, fehlende Bilder (gezeichnete Katze), 5 Plätze, 360x640.
Aufruf: python3 -I tests/test_katze.py"""
import asyncio, json, datetime, sys, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server, WWW
URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []
def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))
async def mk(b, over=None, w=390, h=844, route=None):
    st = json.loads(json.dumps(BASE))
    for k, v in (over or {}).items(): st[k] = v
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='de-DE')
    pg.errs = []; pg.reqs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    pg.on('request', lambda r: pg.reqs.append(r.url) if '/art/cat/' in r.url else None)
    if route: await pg.route(route, lambda r: r.abort())
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL); await pg.wait_for_timeout(1400)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(900)
    except Exception: pass
    await pg.wait_for_timeout(2600)
    return pg
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        # A: mit Bildern
        pg = await mk(b)
        ok('A Ruhebild geladen (mode home, Klasse sprite, Bild sichtbar)', await pg.evaluate("MC.cat.mode()") == 'home' and await pg.evaluate("document.querySelector('#cat').classList.contains('sprite')") and await pg.evaluate("(()=>{const i=document.querySelector('#cat .cat-sp');return !!i&&i.naturalWidth>0&&i.getBoundingClientRect().width>20})()"))
        files = sorted({u.rsplit('/', 1)[-1] for u in pg.reqs})
        ok('A nur die drei Ruhe-Dateien werden geladen (kein Schnurr-Ton, keine Herzen, keine Sprung-Bilder)', set(files) <= {'c01.webp', 'c02.webp', 'c03.webp'} and len(files) >= 1, files)
        ok('A keine Flug-Ebene und keine Sprung-Funktion mehr', not await pg.evaluate("!!document.querySelector('#catFly')") and await pg.evaluate("typeof MC.cat.launch") == 'undefined')
        # B: Antippen
        await pg.click('#cat'); await pg.wait_for_timeout(500)
        tt = await pg.evaluate("(document.getElementById('toast')||{}).innerText||''")
        ok('B Antippen: Hinweis „Mocha schnurrt“, Katze bleibt im Bestellbereich, nichts auf dem Brett', 'Mocha' in tt and await pg.evaluate("MC.cat.mode()") == 'home' and not await pg.evaluate("!!document.querySelector('#catFly')"), tt)
        for _ in range(3): await pg.click('#cat'); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(2500)
        r = await pg.evaluate("(()=>{const c=document.querySelector('#cat').getBoundingClientRect(),o=document.querySelector('#orders').getBoundingClientRect();return [c.left>=o.left-2,c.right<=o.right+2,c.top>=o.top-2,c.bottom<=o.bottom+2]})()")
        ok('B nach mehrmaligem Antippen noch an ihrem Platz im Bestellbereich', all(r), r)
        ok('B keine Fehler', not pg.errs, pg.errs); await pg.close()
        # C: Bilder fehlen -> gezeichnete Katze
        pg = await mk(b, None, route='**/art/cat/**')
        ok('C ohne Bilder: mode off, gezeichnete Katze sichtbar', await pg.evaluate("MC.cat.mode()") == 'off' and not await pg.evaluate("document.querySelector('#cat').classList.contains('sprite')") and await pg.evaluate("getComputedStyle(document.querySelector('#cat .cat-svg')).display") != 'none')
        await pg.click('#cat'); await pg.wait_for_timeout(400)
        ok('C ohne Bilder: Antippen ohne Fehler', not pg.errs, pg.errs); await pg.close()
        # D: 360x640
        pg = await mk(b, None, 360, 640)
        r = await pg.evaluate("(()=>{const i=document.querySelector('#cat .cat-sp').getBoundingClientRect();return [Math.round(i.left),Math.round(i.right),Math.round(i.top),Math.round(i.bottom),innerWidth,innerHeight]})()")
        ok('D 360x640: Katze liegt vollständig im Bild', r[0] >= 0 and r[1] <= r[4] and r[2] >= 0 and r[3] <= r[5], r)
        await pg.close()
        # E: 5 Plätze -> Katze weg (kein Platz neben den Gästen)
        pg = await mk(b)
        await pg.evaluate("MC.state().up.slots=2; MC.render()"); await pg.wait_for_timeout(300)
        ok('E 5 Plätze: Katze ausgeblendet, keine Fehler', await pg.evaluate("getComputedStyle(document.querySelector('#cat')).display") == 'none' and not pg.errs, pg.errs); await pg.close()
        # F: ausgelieferte Dateien
        names = sorted(os.listdir(os.path.join(WWW, 'art', 'cat')))
        ok('F www/art/cat enthält nur c01 bis c03 (keine Sprung-Bilder, Herzen, Schnurr-Ton)', names == ['c01.webp', 'c02.webp', 'c03.webp'], names)
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
    sys.exit(0 if all(res) else 1)
asyncio.run(main())
