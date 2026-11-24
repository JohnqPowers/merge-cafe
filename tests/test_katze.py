"""Katze Mocha: Tutorial-Sperre, fehlende Bilder, 360x640, 5 Plätze, Schnurren (Datei/Ersatzton), Tippen, Abbruch bei Tab-Wechsel/Drehen, Ton aus. Aufruf: python3 -I tests/test_katze.py (Bilder landen in MC_OUT, Standard /tmp/)"""
import asyncio, json, datetime, sys, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
OUT = os.environ.get('MC_OUT', '/tmp/')
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
PROBE = """window.__au=[];
const S0=AudioBufferSourceNode.prototype.start,P0=AudioBufferSourceNode.prototype.stop;
AudioBufferSourceNode.prototype.start=function(...a){if(this.loop)window.__au.push('start:'+(this.buffer?this.buffer.duration.toFixed(2):'?'));return S0.apply(this,a)};
AudioBufferSourceNode.prototype.stop=function(...a){if(this.loop)window.__au.push('stop');return P0.apply(this,a)};"""
async def mk(b, over=None, w=390, h=844, route=None):
    st = json.loads(json.dumps(BASE)); 
    for k, v in (over or {}).items(): st[k] = v
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='de-DE')
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if route: await pg.route(route, lambda r: r.abort())
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script(PROBE)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL); await pg.wait_for_timeout(1400)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(900)
    except Exception: pass
    await pg.wait_for_timeout(2600)
    return pg
async def hit_center(pg):
    r = await pg.evaluate("(()=>{const r=document.querySelector('.cf-hit').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    return r[0] + r[2] / 2, r[1] + r[3] / 2, r
async def land(pg):
    await pg.click('#cat'); await pg.wait_for_timeout(2000)
    return await pg.evaluate("MC.cat.mode()")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        # A: Tutorial noch nicht fertig -> altes Verhalten, kein Flug
        pg = await mk(b, {'tut': 1})
        await pg.evaluate("document.querySelector('#cat').click()"); await pg.wait_for_timeout(500)
        print('A Tutorial: mode', await pg.evaluate("MC.cat.mode()"), '| catFly vorhanden:', await pg.evaluate("!!document.querySelector('#catFly')"), '| Fehler', pg.errs)
        await pg.close()
        # B: Bilder fehlen -> gezeichnete Katze bleibt
        pg = await mk(b, None, route='**/art/cat/**')
        print('B ohne Bilder: mode', await pg.evaluate("MC.cat.mode()"), '| sprite-Klasse:', await pg.evaluate("document.querySelector('#cat').classList.contains('sprite')"), '| SVG sichtbar:', await pg.evaluate("getComputedStyle(document.querySelector('#cat .cat-svg')).display"))
        await pg.evaluate("document.querySelector('#cat').click()"); await pg.wait_for_timeout(400)
        print('  Klick -> mode', await pg.evaluate("MC.cat.mode()"), '| Fehler', pg.errs); await pg.close()
        # C: kleines Display 360x640
        pg = await mk(b, None, 360, 640)
        print('C 360x640: mode', await pg.evaluate("MC.cat.mode()"), '| nach Landung', await land(pg))
        hx, hy, r = await hit_center(pg)
        box = await pg.evaluate("(()=>{const r=document.querySelector('.cf-box').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom].map(Math.round)})()")
        bd = await pg.evaluate("(()=>{const r=document.querySelector('#board').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom].map(Math.round)})()")
        print('  Katze', box, '| Brett', bd, '| Fenster 360x640 | Treffer', [round(v) for v in r])
        await pg.screenshot(path=OUT + 'cat_360x640_sit.png'); await pg.close()
        # D: 5 Plaetze -> Katze weg
        pg = await mk(b)
        await pg.evaluate("MC.state().up.slots=2; MC.render()"); await pg.wait_for_timeout(300)
        print('D 5 Plaetze: orders-Klasse', await pg.evaluate("document.querySelector('#orders').className"), '| #cat display', await pg.evaluate("getComputedStyle(document.querySelector('#cat')).display"), '| launch ->', await pg.evaluate("MC.cat.launch()"), '| Fehler', pg.errs)
        await pg.close()
        # E: Schnurren (Ton an): erst Ersatzton oder Datei, zweites Streicheln sicher mit Datei
        pg = await mk(b)
        await land(pg)
        hx, hy, _ = await hit_center(pg)
        for rnd in (1, 2):
            await pg.evaluate("window.__au.length=0")
            await pg.mouse.move(hx - 30, hy); await pg.mouse.down()
            for i in range(10): await pg.mouse.move(hx - 30 + (i % 2) * 60, hy + (i % 3) * 6, steps=3); await pg.wait_for_timeout(60)
            mid = await pg.evaluate("MC.cat.mode()"); au1 = await pg.evaluate("window.__au.slice()")
            await pg.mouse.up(); await pg.wait_for_timeout(1000)
            print(f'E Streicheln {rnd}: mode {mid} -> {await pg.evaluate("MC.cat.mode()")} | Audio waehrend:', au1, '| nach Ende:', await pg.evaluate("window.__au.slice()"))
            await pg.wait_for_timeout(600)
        # G: einfaches Tippen = kurzes Streicheln
        await pg.evaluate("window.__au.length=0")
        await pg.mouse.click(hx, hy); await pg.wait_for_timeout(150)
        print('G Tippen: mode', await pg.evaluate("MC.cat.mode()")); await pg.wait_for_timeout(700)
        print('  danach', await pg.evaluate("MC.cat.mode()"), '| Fehler', pg.errs)
        # F: Tab versteckt -> Abbruch; kleine Groessenaenderung bleibt, Drehen bricht ab
        await pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))"); await pg.wait_for_timeout(200)
        print('F Tab versteckt -> mode', await pg.evaluate("MC.cat.mode()"))
        await pg.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true})"); await pg.wait_for_timeout(300)
        print('  neu starten ->', await land(pg))
        await pg.set_viewport_size({'width': 390, 'height': 790}); await pg.wait_for_timeout(300)
        print('  Hoehe -54 (Adressleiste) -> mode', await pg.evaluate("MC.cat.mode()"))
        await pg.set_viewport_size({'width': 844, 'height': 390}); await pg.wait_for_timeout(300)
        print('  Querformat -> mode', await pg.evaluate("MC.cat.mode()"), '| Overlay aus:', not await pg.evaluate("document.querySelector('.cf-box').classList.contains('on')"))
        await pg.close()
        # H: Ton aus -> kein Schnurren
        pg = await mk(b, {'sound': False})
        await land(pg); hx, hy, _ = await hit_center(pg)
        await pg.evaluate("window.__au.length=0")
        await pg.mouse.move(hx - 30, hy); await pg.mouse.down()
        for i in range(8): await pg.mouse.move(hx - 30 + (i % 2) * 60, hy, steps=3); await pg.wait_for_timeout(60)
        print('H Ton aus: mode', await pg.evaluate("MC.cat.mode()"), '| Audio-Starts:', await pg.evaluate("window.__au.filter(x=>x.startsWith('start')).length"))
        await pg.mouse.up(); await pg.close()
        await b.close()
asyncio.run(main())
