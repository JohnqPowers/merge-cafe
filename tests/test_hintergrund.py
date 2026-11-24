"""Vollbild-Hintergrund je Welt (Datei art/b<N>.webp, ab 1.5.17): mit Bild ersetzt er gezeichnete Szene und Boden, ohne Bild bleibt alles wie zuvor,
Welten ohne Bild sind nicht betroffen. Das Bild wird für den Test erzeugt und über das Netz-Routing eingespielt. Aufruf: python3 -I tests/test_hintergrund.py"""
import asyncio, json, datetime, sys, os, io, re
from playwright.async_api import async_playwright
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []
def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))
def bild():
    im = Image.new('RGB', (720, 1560), (90, 150, 220))
    for y in range(1560): im.paste((90 + y // 12, 150, 220 - y // 14), (0, y, 720, y + 1))
    b = io.BytesIO(); im.save(b, 'WEBP', quality=60); return b.getvalue()
async def mk(b, mit_bild):
    pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, locale='de-DE')
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if mit_bild:
        async def fix(route):
            r = await route.fetch(); body = await r.text()
            body, n = re.subn(r"const ART = new Set\(\[", "const ART = new Set(['b2', ", body, count=1)
            await route.fulfill(response=r, body=body)
        await pg.route('**/index.html', fix)
        await pg.route('**/art/b2.webp', lambda r: r.fulfill(status=200, content_type='image/webp', body=bild()))
    st = json.dumps(BASE).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % st)
    await pg.goto(URL); await pg.wait_for_timeout(1300)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(600)
    except Exception: pass
    await pg.wait_for_timeout(1200)
    return pg
LAYER = "document.querySelector('#scene .sc-layer:last-child')"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = await mk(b, True)
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2200)
        ok('Paris mit Bild: Vollbild-Ebene, keine gezeichnete Szene, kein Boden', await pg.evaluate(f"!!{LAYER}.querySelector('img.sc-bg') && !{LAYER}.querySelector('svg') && !{LAYER}.querySelector('.sc-floor')"))
        r = await pg.evaluate(f"(()=>{{const i={LAYER}.querySelector('img.sc-bg'),b=i.getBoundingClientRect();return [i.naturalWidth,i.naturalHeight,Math.round(b.width),Math.round(b.height),getComputedStyle(i).objectFit,getComputedStyle(i).objectPosition]}})()")
        ok('Paris mit Bild: Bild geladen (720x1560), füllt den Schirm, cover und oben ausgerichtet', r[0] == 720 and r[1] == 1560 and r[2] == 390 and r[3] == 844 and r[4] == 'cover' and r[5].startswith('50% 0'), r)
        await pg.evaluate("MC.world(1)"); await pg.wait_for_timeout(2200)
        ok('Hamburg (ohne Bild) bleibt gezeichnet: Szene und Boden', await pg.evaluate(f"!!{LAYER}.querySelector('svg') && !{LAYER}.querySelector('img.sc-bg')"))
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2200)
        ok('Zurück nach Paris: Vollbild wieder da', await pg.evaluate(f"!!{LAYER}.querySelector('img.sc-bg')"))
        ok('keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mk(b, False)
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2200)
        ok('Paris ohne Bild: gezeichnete Szene mit Boden wie zuvor', await pg.evaluate(f"!!{LAYER}.querySelector('svg') && !!{LAYER}.querySelector('.sc-floor') && !{LAYER}.querySelector('img.sc-bg')"))
        ok('Paris ohne Bild: keine Fehler', not pg.errs, pg.errs); await pg.close()
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
    sys.exit(0 if all(res) else 1)
asyncio.run(main())
