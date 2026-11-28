"""Startbild (Experiment exp/startbild; Schalter CONFIG.features.startImg, im Web-Test ?startimg=0 / ?startimg=1).
Geprüft werden: Bilddatei und Tabelle START (Maße, eingebrannte Versionsnummer getilgt, Zierlinien erhalten, Verlängerung unten ohne Zierlinien-Geister,
Knopf deckt den gemalten Knopf), Einbau in vielen Fenstergrößen (Bild deckt das Fenster oder füllt die Höhe mit verwischtem Rand, Knopf und Versionszeile
im Bild, Satz „Dein eigenes Café wartet auf dich!“ nicht am Rand abgeschnitten, Knopf liegt pixelgenau über dem gemalten Knopf), Knopf startet das Spiel
und ein Tipp auf den Titel nicht, echte Versionsnummer, Willkommenszeile (kurzer und sehr langer Name), Drehen des Fensters, Schalter aus (URL und
CONFIG: kein Element, keine Datei), andere Sprache, fehlende Datei, sehr früher Fingerdruck bei langsamem Bild, nichts Neues im Speicher, bitgleiche
Nachstellung durch scripts/start_import.py.
Aufruf: python3 -I tests/test_startbild.py"""
import asyncio, json, datetime, sys, os, re, io, subprocess, tempfile, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server, WWW

URL = server()
ROOT = Path(WWW).parent
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
HTML = Path(WWW, 'index.html').read_text(encoding='utf-8')
START = json.loads(re.search(r'/\*START_DATA\*/(.*?)/\*END_START_DATA\*/', HTML, re.S).group(1))
VERSION = re.search(r"^\s*version:\s*'(\d+\.\d+\.\d+)'", HTML, re.M).group(1)
W, H, ART = START['w'], START['h'], START['art']
ARTI = int(round(ART))                          # Höhe des eigentlichen Bildes als ganze Zahl (Zeilenindex)
SRC_W, SRC_H = 941, 1672                       # Maße des Originals (assets/src/start-original.png)
SX, SY = W / SRC_W, ART / SRC_H                # Original -> Ausgabe
res = []


def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''), flush=True)


def rewrite(fn):
    async def h(route):
        r = await route.fetch()
        await route.fulfill(response=r, body=fn(await r.text()))
    return h


async def mk(b, q='?startimg=1', w=390, h=844, done=True, name=None, locale='de-DE', abort=None, rew=None, slow=0, dpr=2, wait=1300, commit=False):
    st = json.loads(json.dumps(BASE)); st['level'] = 3; st['tut'] = 3
    if not done: st['profile'] = {'done': False}
    elif name: st['profile'] = dict(st.get('profile') or {}, name=name, done=True)
    ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dpr, locale=locale)
    pg = await ctx.new_page(); pg.ctx = ctx; pg.errs = []; pg.reqs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    pg.on('request', lambda r: pg.reqs.append(r.url) if '/art/start' in r.url else None)
    if abort: await pg.route(abort, lambda r: r.abort())
    if slow:
        async def sl(route):
            await asyncio.sleep(slow); await route.continue_()
        await pg.route(re.compile(r'/art/start\.webp'), sl)
    if rew: await pg.route(re.compile(r'/index\.html'), rewrite(rew))
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL + q, wait_until='commit' if commit else 'load'); await pg.wait_for_timeout(wait)      # commit: nicht auf das Bild warten (ein ladendes Bild hält das load-Ereignis auf)
    return pg


GEO = """() => { const q = s => document.querySelector(s), sp = q('#splash'), st = q('.sp-stage'), pb = q('#spPlay'), v = q('#spVer');
  const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  return { cls: sp ? sp.className : null, stage: r(st), btn: r(pb), ver: r(v), vw: innerWidth, vh: innerHeight, blur: sp ? getComputedStyle(sp, '::before').display : null } }"""
GONE = "!document.getElementById('splash') || document.getElementById('splash').classList.contains('out')"


def lum(a): return a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114


def streu(img, box):
    """Streuung der Helligkeit ohne Verlauf: Bildausschnitt minus seine Verwischung (Bildkorn bleibt klein, Schrift/Linien schlagen aus)."""
    a = np.asarray(img.convert('RGB').crop(box)).astype(np.float32)
    b = np.asarray(img.convert('RGB').crop(box).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    return float(np.std(lum(a) - lum(b)))


def gruen(a):
    return (a[..., 1] > 150) & (a[..., 1] > a[..., 0].astype(int) + 30) & (a[..., 1] > a[..., 2].astype(int) + 60)


def box_dicht(m, f=.25):
    """Umriss der dichten grünen Fläche (Zeilen/Spalten mit mindestens 25 % der stärksten); vereinzelte grüne Blätter in den Ecken zählen nicht."""
    r = m.sum(axis=1)
    ys = np.where(r >= f * r.max())[0]                                   # erst die Zeilen des Knopfs, dann darin die Spalten
    c = m[ys.min():ys.max() + 1].sum(axis=0)
    xs = np.where(c >= f * c.max())[0]
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


async def main():
    # ---------- A: Bilddatei und Tabelle (ohne Browser) ----------
    p = Path(WWW, 'art', 'start.webp'); orig = Path(ROOT, 'assets', 'src', 'start-original.png')
    ok('A Datei www/art/start.webp und Original assets/src/start-original.png vorhanden', p.is_file() and orig.is_file())
    im = Image.open(p).convert('RGB'); io_ = Image.open(orig).convert('RGB')
    ok('A Tabelle START: Datei und Maße stimmen mit dem Bild überein', START['file'] == 'art/start.webp' and im.size == (W, H), [START['file'], im.size, (W, H)])
    ok('A Original hat 941x1672', io_.size == (SRC_W, SRC_H), io_.size)
    ok('A Größe unter 600 KB (Ladezeit im Spiel, Größe der App)', p.stat().st_size < 600_000, p.stat().st_size)
    ok('A Verlängerung unten: Gesamthöhe größer als das eigentliche Bild, mindestens 10 %', H - ART >= .10 * ART, [H, ART])
    x0, y0, x1, y1 = (int(v) for v in (423 * SX, 1566 * SY, 520 * SX, 1599 * SY))                 # Fläche der eingebrannten Versionsnummer
    ok('A Messverfahren: im Original schlägt die Versionsnummer deutlich aus (Streuung > 15)', streu(io_.resize((W, round(SRC_H * SY))), (x0, y0, x1, y1)) > 15, round(streu(io_.resize((W, round(SRC_H * SY))), (x0, y0, x1, y1)), 1))
    ok('A Versionsnummer im Bild getilgt (Streuung < 4)', streu(im, (x0, y0, x1, y1)) < 4, round(streu(im, (x0, y0, x1, y1)), 1))
    zl = np.asarray(im.crop((int(300 * SX), int(1578 * SY), int(392 * SX), int(1591 * SY)))).astype(int)
    ok('A Zierlinie links neben der Versionszeile bleibt erhalten (helle Punkte vorhanden)', int((lum(zl) > 200).sum()) > 150, int((lum(zl) > 200).sum()))
    gs = 1.0 * (H - ART)                                                                      # Verlängerung: Zeilen der Ausgabe unter dem eigentlichen Bild
    zi = (int(ARTI + (SRC_H - 1595) * SY), int(ARTI + (SRC_H - 1574) * SY))                     # dort liegen die gespiegelten Zierlinien
    ok('A Verlängerung: keine gespiegelten Zierlinien (Streuung < 4)', streu(im, (int(284 * SX), zi[0], int(404 * SX), zi[1])) < 4 and streu(im, (int(538 * SX), zi[0], int(658 * SX), zi[1])) < 4,
       [round(streu(im, (int(284 * SX), zi[0], int(404 * SX), zi[1])), 1), round(streu(im, (int(538 * SX), zi[0], int(658 * SX), zi[1])), 1)])
    a = np.asarray(im).astype(int)
    ok('A Übergang zur Verlängerung ohne Kante (mittlerer Unterschied der Nachbarzeilen < 10)', float(np.abs(a[ARTI - 2] - a[ARTI + 1]).mean()) < 10, round(float(np.abs(a[ARTI - 2] - a[ARTI + 1]).mean()), 2))
    gx0, gy0, gx1, gy1 = box_dicht(gruen(a[int(.55 * ARTI):ARTI])); gy0 += int(.55 * ARTI); gy1 += int(.55 * ARTI)
    bl, bt, bw, bh = START['btn'][0] / 100 * W, START['btn'][1] / 100 * H, START['btn'][2] / 100 * W, START['btn'][3] / 100 * H
    ok('A Knopffläche in START umschließt den gemalten Knopf (grüne Fläche liegt innen)', bl - 2 <= gx0 and gx1 <= bl + bw + 2 and bt - 2 <= gy0 and gy1 <= bt + bh + 2, [(gx0, gy0, gx1, gy1), (round(bl), round(bt), round(bl + bw), round(bt + bh))])
    ok('A … und ist nicht größer als nötig (höchstens 16 Punkte Rand je Seite)', gx0 - bl <= 16 and bl + bw - gx1 <= 16 and gy0 - bt <= 16 and bt + bh - gy1 <= 16, [round(gx0 - bl), round(bl + bw - gx1), round(gy0 - bt), round(bt + bh - gy1)])
    ok('A Quelltext: Schalter startImg in CONFIG.features und Prüfung auf deutsche Sprache', bool(re.search(r'features:\s*\{[^}]*\bstartImg:\s*true', HTML)) and "LANG === 'de' && !!START.file" in HTML)

    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])

        # ---------- B: Einbau in vielen Fenstergrößen ----------
        ART_A = W / ART
        for w, h in [(390, 844), (412, 915), (393, 873), (360, 640), (375, 667), (360, 780), (320, 568), (1280, 800), (800, 1000), (844, 390)]:
            pg = await mk(b, w=w, h=h, dpr=2 if w < 900 else 1)
            g = await pg.evaluate(GEO); a_ = w / h
            tag = f'B {w}x{h}'
            ok(f'{tag}: Startbild aktiv (sp-img, nicht mehr sp-pre), Bühne sichtbar', g['cls'] and 'sp-img' in g['cls'] and 'sp-pre' not in g['cls'] and g['stage'] is not None, g['cls'])
            sx0, sy0, sx1, sy1 = g['stage']; sw = sx1 - sx0
            if a_ <= ART_A:
                ok(f'{tag}: Bild deckt das ganze Fenster, oben ausgerichtet', sx0 <= .6 and sx1 >= w - .6 and sy0 <= .6 and sy1 >= h - .6, [round(v, 1) for v in g['stage']])
                ok(f'{tag}: kein verwischter Rand nötig (::before aus)', g['blur'] == 'none', g['blur'])
            else:
                ok(f'{tag}: das eigentliche Bild füllt die Höhe, mittig' + (', verwischter Rand an' if a_ > .566 else ' (Fenster nur einen Hauch breiter als das Bild: Rand unter 1 px)'),
                   abs((sy1 - sy0) * ART / H - h) <= 1.5 and abs((sx0 + sx1) / 2 - w / 2) <= 1 and (a_ <= .566 or g['blur'] == 'block'), [round(v, 1) for v in g['stage']] + [g['blur']])
            bx0, by0, bx1, by1 = g['btn']
            ok(f'{tag}: Knopf liegt ganz im Fenster', bx0 >= 0 and bx1 <= w and by0 >= 0 and by1 <= h, [round(v) for v in g['btn']])
            if a_ < 1: ok(f'{tag}: Knopf mindestens 44 px hoch (Fingerfläche)', by1 - by0 >= 44, round(by1 - by0))
            vx0, vy0, vx1, vy1 = g['ver']
            ok(f'{tag}: Versionszeile ganz im Fenster, mittig im Bild', vy1 <= h - 3 and vx0 >= 0 and vx1 <= w and abs((vx0 + vx1) / 2 - (sx0 + sw / 2)) <= 2.5, [round(v, 1) for v in g['ver']])
            if .44 <= a_ <= ART_A:
                t0 = sx0 + 78 / SRC_W * sw; t1 = sx0 + 862 / SRC_W * sw                              # Satz „Dein eigenes Café wartet auf dich!“ im Original von x 78 bis 862
                ok(f'{tag}: Satz „Dein eigenes Café wartet auf dich!“ am Rand nicht abgeschnitten (mindestens 6 px Luft)', t0 >= 6 and t1 <= w - 6, [round(t0, 1), round(t1, 1), w])
            # Pixelvergleich: der Knopf liegt auf dem gemalten Knopf
            if a_ < 1:
                png = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); sc = png.width / w
                arr = np.asarray(png).astype(int); y_lo = int(h * .55 * sc)
                gx0, gy0, gx1, gy1 = box_dicht(gruen(arr[y_lo:]))
                gx0, gx1, gy0, gy1 = gx0 / sc, (gx1 + 1) / sc, (gy0 + y_lo) / sc, (gy1 + 1 + y_lo) / sc
                ok(f'{tag}: Knopf umschließt den gemalten grünen Knopf (Pixel im Bildschirmfoto)', bx0 - 2 <= gx0 and gx1 <= bx1 + 2 and by0 - 2 <= gy0 and gy1 <= by1 + 2, [[round(gx0), round(gy0), round(gx1), round(gy1)], [round(v) for v in g['btn']]])
                ok(f'{tag}: … und mittig darauf (Abweichung der Mitten höchstens 4 px)', abs((gx0 + gx1) / 2 - (bx0 + bx1) / 2) <= 4 and abs((gy0 + gy1) / 2 - (by0 + by1) / 2) <= 6, [round((gx0 + gx1) / 2 - (bx0 + bx1) / 2, 1), round((gy0 + gy1) / 2 - (by0 + by1) / 2, 1)])
            ok(f'{tag}: keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- C: Bedienung ----------
        pg = await mk(b)
        ok('C alte Inhalte entfernt (kein Logo, Titel, Funkeln, Blasen, Fahnen, Begrüßung), Knopf liegt in der Bühne',
           await pg.evaluate("!document.querySelector('#splash .sp-logo,#splash #spTitle,#splash .rays,#splash .bk,#splash #spFlags,#splash #spWelcome') && !!document.querySelector('.sp-stage #spPlay')"))
        ok('C Bild ist geladen und entschlüsselt', await pg.evaluate("(() => { const i = document.querySelector('.sp-stage > img'); return !!i && i.complete && i.naturalWidth === %d && i.naturalHeight === %d; })()" % (W, H)))
        ok('C Knopf hat eine Beschriftung für Vorlesehilfen (aria-label) und ist ein button', await pg.evaluate("(() => { const b = document.getElementById('spPlay'); return b.tagName === 'BUTTON' && b.getAttribute('aria-label') === 'Spielen'; })()"))
        ok('C echte Versionsnummer als Text (v' + VERSION + ')', await pg.evaluate("document.getElementById('spVer').textContent") == 'v' + VERSION)
        ok('C wiederkehrender Spieler: Willkommenszeile mit Namen', (await pg.evaluate("(document.querySelector('.sp-w')||{}).textContent||''")).startswith('Willkommen zurück, '), await pg.evaluate("(document.querySelector('.sp-w')||{}).textContent||''"))
        keys_an = sorted(await pg.evaluate("Object.keys(localStorage)"))
        g = await pg.evaluate(GEO); bx0, by0, bx1, by1 = g['btn']; sx0, sy0, sx1, sy1 = g['stage']
        await pg.mouse.click((sx0 + sx1) / 2, sy0 + (sy1 - sy0) * .30)                                   # Tipp mitten auf den Titel
        await pg.wait_for_timeout(700)
        ok('C Tipp auf den Titel startet das Spiel nicht', not await pg.evaluate(GONE))
        await pg.mouse.click((bx0 + bx1) / 2, (by0 + by1) / 2)
        await pg.wait_for_timeout(120)
        ok('C Tipp auf den Knopf: Startbild blendet aus, Spiel läuft los', await pg.evaluate("document.getElementById('splash').classList.contains('out') && !document.body.classList.contains('splashing')"))
        await pg.wait_for_timeout(1500)
        ok('C danach ist das Startbild samt Bühne aus dem DOM entfernt', await pg.evaluate("!document.getElementById('splash') && !document.querySelector('.sp-stage')"))
        ok('C Spiel ist bedienbar (Brett vorhanden, Zustand lesbar)', await pg.evaluate("!!document.getElementById('board') && MC.state().level >= 1"))
        ok('C keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # Tastatur: Knopf ist fokussierbar und löst mit Enter aus
        pg = await mk(b)
        await pg.focus('#spPlay'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        ok('C Tastatur: Enter auf dem fokussierten Knopf startet das Spiel', await pg.evaluate(GONE)); await pg.ctx.close()

        # ---------- D: Willkommenszeile ----------
        pg = await mk(b, done=False)
        ok('D neuer Spieler: keine Willkommenszeile (der Satz im Bild genügt)', await pg.evaluate("!document.querySelector('.sp-w')") and await pg.evaluate("!!document.querySelector('.sp-stage.rdy')"))
        await pg.ctx.close()
        for nm in ['WWWWWWWWWWWWWWWW', 'Nils', 'Wolfgang Amadeus']:
            pg = await mk(b, name=nm)
            bb = await pg.evaluate("(() => { const t = document.querySelector('.sp-w'); const b = t.getBBox(); return [b.width, t.textContent]; })()")
            ok(f'D Name „{nm}“: Zeile passt in die Breite ({START["wel"][3]:.0f} Einheiten)', bb[0] <= START['wel'][3] + 3 and nm in bb[1], [round(bb[0]), bb[1]])
            ok(f'D Name „{nm}“: Name steht in der Zeile, keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- E: Fenster drehen ----------
        pg = await mk(b)
        g1 = await pg.evaluate(GEO)
        await pg.set_viewport_size({'width': 844, 'height': 390}); await pg.wait_for_timeout(300)
        g2 = await pg.evaluate(GEO)
        ok('E Drehen ins Querformat: Bühne wird neu berechnet (Bild füllt die Höhe, verwischter Rand)', g2['stage'] and abs((g2['stage'][3] - g2['stage'][1]) * ART / H - 390) <= 1.5 and g2['blur'] == 'block', [g2['stage'], g2['blur']])
        await pg.set_viewport_size({'width': 390, 'height': 844}); await pg.wait_for_timeout(300)
        g3 = await pg.evaluate(GEO)
        ok('E zurück ins Hochformat: wieder wie vorher', all(abs(a - b_) <= 1 for a, b_ in zip(g1['stage'], g3['stage'])) and all(abs(a - b_) <= 1 for a, b_ in zip(g1['btn'], g3['btn'])), [g1['stage'], g3['stage']])
        ok('E keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- F: Schalter aus ----------
        pg = await mk(b, q='?startimg=0')
        ok('F ?startimg=0: kein Startbild-Element, keine Klasse, kein Hintergrundbild', await pg.evaluate("!document.querySelector('.sp-stage,.sp-ov') && !/sp-img|sp-pre/.test(document.getElementById('splash').className) && !document.getElementById('splash').style.getPropertyValue('--spbg')"))
        ok('F … das alte Startbild steht (Logo, Titel, Bohnenreihe, Willkommen) und der Knopf ist sichtbar', await pg.evaluate("!!document.querySelector('#splash .sp-logo') && !!document.querySelector('#spTitle span') && !!document.querySelector('#spFlags i') && getComputedStyle(document.getElementById('spPlay')).opacity === '1' && document.getElementById('spVer').textContent === 'v%s'" % VERSION))
        ok('F … und es wird keine Startbild-Datei angefordert', not pg.reqs, pg.reqs)
        keys_aus = sorted(await pg.evaluate("Object.keys(localStorage)"))
        ok('F Speicher-Schlüssel mit und ohne Startbild gleich (nichts Neues geschrieben)', keys_aus == keys_an, [keys_an, keys_aus])
        await pg.click('#spPlay'); await pg.wait_for_timeout(900)
        ok('F altes Startbild startet das Spiel wie bisher', await pg.evaluate(GONE)); ok('F keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        pg = await mk(b, q='', rew=lambda t: t.replace('startImg: true', 'startImg: false'))
        ok('F CONFIG.features.startImg=false: altes Startbild, keine Datei angefordert', await pg.evaluate("!document.querySelector('.sp-stage') && !!document.querySelector('#splash .sp-logo')") and not pg.reqs, pg.reqs); await pg.ctx.close()
        pg = await mk(b, q='?startimg=1', rew=lambda t: t.replace('startImg: true', 'startImg: false'))
        ok('F URL ?startimg=1 schlägt CONFIG=false (Web-Test)', await pg.evaluate("!!document.querySelector('.sp-stage.rdy')")); await pg.ctx.close()
        pg = await mk(b, q='')
        ok('F Standard (CONFIG.features.startImg=true, ohne URL-Angabe): Startbild an', await pg.evaluate("!!document.querySelector('.sp-stage.rdy')") and len(pg.reqs) == 1, pg.reqs); await pg.ctx.close()

        # ---------- G: andere Sprache, fehlende Datei, früher Fingerdruck ----------
        pg = await mk(b, locale='en-US')
        ok('G englische Sprache: altes (übersetztes) Startbild, keine Datei angefordert (das Bild trägt deutschen Text)',
           await pg.evaluate("!document.querySelector('.sp-stage') && document.getElementById('spPlay').textContent === 'Play'") and not pg.reqs, pg.reqs)
        await pg.click('#spPlay'); await pg.wait_for_timeout(900); ok('G … und es startet', await pg.evaluate(GONE)); await pg.ctx.close()

        pg = await mk(b, abort=re.compile(r'/art/start\.webp'))
        ok('G Datei fehlt: das alte Startbild bleibt sichtbar', await pg.evaluate("!document.querySelector('.sp-stage') && !/sp-pre|sp-img/.test(document.getElementById('splash').className) && !!document.querySelector('#splash .sp-logo') && getComputedStyle(document.getElementById('spPlay')).opacity === '1'"))
        await pg.click('#spPlay'); await pg.wait_for_timeout(900)
        ok('G … und startet das Spiel; keine Fehler', await pg.evaluate(GONE) and not pg.errs, pg.errs); await pg.ctx.close()

        pg = await mk(b, slow=1.2, wait=300, commit=True)
        ok('G langsames Bild: bis es da ist, sind die alten Inhalte verborgen (nichts blitzt auf)', await pg.evaluate("getComputedStyle(document.querySelector('#splash .sp-logo')).visibility === 'hidden' && !document.querySelector('.sp-stage')"))
        await pg.click('#spPlay', force=True); await pg.wait_for_timeout(2600)
        ok('G sehr früher Tipp (Bild noch nicht da): Spiel startet, danach kein Startbild-Rest', await pg.evaluate("!document.getElementById('splash') && !document.querySelector('.sp-stage')") and await pg.evaluate("!!MC.state()"), pg.errs)
        ok('G … ohne Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        await b.close()

    # ---------- H: bitgleiche Nachstellung (Skript in einer Kopie des Repos) ----------
    tmp = Path(tempfile.mkdtemp(prefix='start_nachbau_'))
    try:
        (tmp / 'www').mkdir(); (tmp / 'assets' / 'src').mkdir(parents=True)
        shutil.copy(Path(WWW, 'index.html'), tmp / 'www' / 'index.html'); shutil.copy(orig, tmp / 'assets' / 'src' / 'start-original.png')
        r = subprocess.run([sys.executable, '-I', str(ROOT / 'scripts' / 'start_import.py'), '--root', str(tmp)], capture_output=True, text=True)
        neu = tmp / 'www' / 'art' / 'start.webp'
        ok('H Nachbau mit scripts/start_import.py läuft durch', r.returncode == 0 and neu.is_file(), (r.stdout + r.stderr).strip()[-160:])
        ok('H … und ist Byte für Byte gleich der ausgelieferten Datei', neu.is_file() and neu.read_bytes() == p.read_bytes())
        ok('H … die Tabelle START in index.html bleibt dabei unverändert', (tmp / 'www' / 'index.html').read_text(encoding='utf-8') == HTML)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n = len(res); g_ = sum(res)
    print(f'\nERGEBNIS: {g_}/{n} bestanden' + ('' if g_ == n else f' ({n - g_} FEHLER)'))
    sys.exit(0 if g_ == n else 1)


asyncio.run(main())
