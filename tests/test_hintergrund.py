"""Vollbild-Hintergrund je Welt (Dateien art/b0.webp bis b8.webp, Lieferung vom 25.11.2026, im Spiel ab 1.5.19) und Stadtrahmen (frame1 bis frame8).
Mit Bild ersetzt der Hintergrund gezeichnete Szene und Boden, ohne Bild bleibt alles wie zuvor. Geprüft werden die Aufbereitung (scripts/art_import.py, oben auf
9:19,5 ergänzt), die ausgelieferten Dateien, alle neun Welten im Browser (390x844), das breite Fenster der Web-Version und der Rückfall ohne Bild.
Aufruf: python3 -I tests/test_hintergrund.py"""
import asyncio, json, datetime, sys, os, re, io
from pathlib import Path
import numpy as np
from playwright.async_api import async_playwright
from PIL import Image
HIER = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(HIER.parent / 'scripts'))
from _helfer import CHROME, STATE, server
import art_import
URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []
def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))
LEVELS = [1, 5, 10, 15, 20, 25, 30, 40, 50]                       # Beginn der neun Welten (CHAPTERS)

def testbild(w, h):
    a = np.zeros((h, w, 3), np.uint8)
    for y in range(h): a[y, :, 0] = 40 + 160 * y // h; a[y, :, 1] = 120; a[y, :, 2] = 230 - 150 * y // h      # Verlauf von oben nach unten
    a[:, : w // 6, 1] = 200                                          # Streifen am linken Rand (wie Laub am Bildrand)
    return Image.fromarray(a, 'RGB')

def aufbereitung():
    # 9:16 (wie geliefert 941x1672) -> 720x1560, oben ergänzt; 9:19,5 bleibt unverändert; Querformat wird abgelehnt
    im = testbild(941, 1672)
    out = art_import.bg_asset(im)
    ok('Aufbereitung: 941x1672 (9:16) wird 720x1560 (9:19,5)', out.size == (720, 1560), out.size)
    pad = round(art_import.BG_ASPECT * 941 - 1672)
    k = 720 / 941
    a = np.asarray(out, dtype=np.float32)
    n = round(pad * k)
    sprung = float(np.abs(a[n - 1] - a[n + 1]).mean())
    ok('Aufbereitung: kein sichtbarer Sprung an der Naht (mittlerer Unterschied < 6)', sprung < 6, round(sprung, 2))
    unten = np.asarray(im.resize((720, round(1672 * k)), Image.LANCZOS), dtype=np.float32)
    ok('Aufbereitung: der Bildkörper unterhalb des Übergangs bleibt unverändert (Abweichung < 3)', float(np.abs(a[-300:] - unten[-300:]).mean()) < 3,
       round(float(np.abs(a[-300:] - unten[-300:]).mean()), 2))
    spalte_oben = a[2, :, 1].mean(); spalte_links = a[2, : 720 // 7, 1].mean(); spalte_rechts = a[2, -720 // 7:, 1].mean()
    ok('Aufbereitung: der angesetzte Rand übernimmt die Farben der obersten Zeilen (linker Streifen bleibt heller)', spalte_links > spalte_rechts + 20, (round(spalte_links), round(spalte_rechts)))
    hoch = art_import.bg_asset(testbild(1080, 2340))
    ok('Aufbereitung: 1080x2340 (schon 9:19,5) wird nur verkleinert, nichts angesetzt', hoch.size == (720, 1560), hoch.size)
    try:
        art_import.bg_asset(testbild(1600, 1000)); querformat = False
    except ValueError:
        querformat = True
    ok('Aufbereitung: Querformat wird abgelehnt', querformat)

def dateien():
    html = (HIER.parent / 'www' / 'index.html').read_text(encoding='utf8')
    art = set(re.findall(r"'([^']+)'", re.search(r'const ART = new Set\(\[([^\]]*)\]\);', html).group(1)))
    fehlt, maße = [], set()
    for i in range(9):
        f = HIER.parent / 'www' / 'art' / f'b{i}.webp'
        if f'b{i}' not in art or not f.exists(): fehlt.append(f'b{i}'); continue
        maße.add(Image.open(f).size)
    ok('Dateien: b0 bis b8 liegen vor und stehen im Manifest ART', not fehlt, fehlt)
    ok('Dateien: alle neun Hintergründe sind 720x1560', maße == {(720, 1560)}, maße)
    rahmen = [i for i in range(1, 9) if f'frame{i}' in art and (HIER.parent / 'www' / 'art' / f'frame{i}.webp').exists()]
    ok('Dateien: Stadtrahmen frame1 bis frame8 liegen vor, Hamburg nutzt den Standardrahmen (kein frame0)', rahmen == list(range(1, 9)) and 'frame0' not in art, rahmen)
    gesamt = sum((HIER.parent / 'www' / 'art' / f'b{i}.webp').stat().st_size for i in range(9))
    ok('Dateien: die neun Hintergründe wiegen zusammen unter 2,2 MB', gesamt < 2.2 * 1024 * 1024, f'{gesamt // 1024} KB')

async def mk(b, w=390, h=844, ohne_b2=False):
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='de-DE')
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if ohne_b2:
        async def fix(route):
            r = await route.fetch(); body = await r.text()
            body, n = re.subn(r"'b2', ", "", body, count=1)
            await route.fulfill(response=r, body=body)
        await pg.route('**/index.html', fix)
    st = json.dumps(BASE).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % st)
    await pg.goto(URL); await pg.wait_for_timeout(1300)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(600)
    except Exception: pass
    await pg.wait_for_timeout(1200)
    return pg
LAYER = "document.querySelector('#scene .sc-layer:last-child')"

async def main():
    aufbereitung()
    dateien()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = await mk(b)
        falsch, rahmen_falsch = [], []
        for i, L in enumerate(LEVELS):
            await pg.evaluate(f"MC.world({L})"); await pg.wait_for_timeout(2300)
            r = await pg.evaluate(f"(()=>{{const l={LAYER},im=l.querySelector('img.sc-bg');if(!im)return null;const b=im.getBoundingClientRect();return [im.getAttribute('src'),im.naturalWidth,im.naturalHeight,Math.round(b.left),Math.round(b.width),Math.round(b.height),getComputedStyle(im).objectFit,!!l.querySelector('svg'),!!l.querySelector('.sc-floor')]}})()")
            gut = r and r[0] == f'art/b{i}.webp' and r[1:3] == [720, 1560] and r[3:6] == [0, 390, 844] and r[6] == 'cover' and not r[7] and not r[8]
            if not gut: falsch.append((i, r))
            fr = await pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--frimg').trim()")
            if i == 0: gut_fr = fr in ('', 'url(art/frame.webp)')
            else: gut_fr = fr == f'url(art/frame{i}.webp)'
            if not gut_fr: rahmen_falsch.append((i, fr))
        ok('Alle neun Welten: Vollbild-Ebene mit der richtigen Datei (720x1560, füllt 390x844, cover), keine gezeichnete Szene, kein Boden', not falsch, falsch)
        ok('Alle neun Welten: Rahmen der Welt (Hamburg Standard, sonst frame1 bis frame8)', not rahmen_falsch, rahmen_falsch)
        # Kulisse und Brett: das Brett bleibt, wo es war (Geometrie unverändert), Kulisse liegt dahinter
        g = await pg.evaluate("(()=>{const q=s=>{const r=document.querySelector(s).getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]};return {board:q('#board'),orders:q('#orders'),z:getComputedStyle(document.querySelector('#scene')).zIndex}})()")
        ok('Geometrie 390x844 unverändert: Brett 353x397 ab y=343, Bestellleiste 370x130 ab y=104, Szene hinter allem (z-index 0)', g['board'] == [18, 343, 353, 397] and g['orders'] == [10, 104, 370, 130] and g['z'] == '0', g)
        ok('keine Fehler (neun Welten)', not pg.errs, pg.errs); await pg.close()

        # breites Fenster (Web am Desktop): Kulisse so breit wie die App-Spalte, verwischte Kopie als Rand
        pg = await mk(b, 1280, 800)
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2300)
        r = await pg.evaluate(f"(()=>{{const l={LAYER},im=l.querySelector('img.sc-bg'),b=im.getBoundingClientRect();return [Math.round(b.left),Math.round(b.width),Math.round(b.height),l.classList.contains('sc-hasbg'),getComputedStyle(l,'::before').content,getComputedStyle(l,'::before').filter]}})()")
        ok('Breites Fenster 1280x800: Kulisse 520 px breit und mittig, dahinter verwischte Kopie als Füllung', r[0] == 380 and r[1] == 520 and r[2] == 800 and r[3] and r[4] == '""' and 'blur' in r[5], r)
        ok('Breites Fenster: keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mk(b)
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2300)
        r = await pg.evaluate(f"getComputedStyle({LAYER},'::before').content")
        ok('Handy 390x844: keine verwischte Füllung (Pseudo-Element leer)', r in ('none', 'normal'), r); await pg.close()

        # Rückfall: ohne Datei b2 im Manifest bleibt Paris gezeichnet, mit Boden, wie vor 1.5.19
        pg = await mk(b, ohne_b2=True)
        await pg.evaluate("MC.world(10)"); await pg.wait_for_timeout(2300)
        ok('Paris ohne Bild: gezeichnete Szene mit Boden wie zuvor', await pg.evaluate(f"!!{LAYER}.querySelector('svg') && !!{LAYER}.querySelector('.sc-floor') && !{LAYER}.querySelector('img.sc-bg')"))
        await pg.evaluate("MC.world(5)"); await pg.wait_for_timeout(2300)
        ok('Wien (mit Bild) bleibt Vollbild, auch wenn Paris ohne Bild ist', await pg.evaluate(f"!!{LAYER}.querySelector('img.sc-bg') && !{LAYER}.querySelector('svg')"))
        ok('Paris ohne Bild: keine Fehler', not pg.errs, pg.errs); await pg.close()
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
    sys.exit(0 if all(res) else 1)
asyncio.run(main())
