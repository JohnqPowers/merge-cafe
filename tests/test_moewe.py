"""Möwe über Hamburg (Experiment exp/moewe-hamburg; Schalter CONFIG.features.gull, im Web-Test ?gull=0 / ?gull=1).
Geprüft werden: Schalter aus = nichts (kein Element, kein Timer-Flug, keine Datei), Flug nur im freien Fenster zwischen Bestellungen und Brett
(drei Fenstergrößen; Pixelvergleich: außerhalb des Bands ändert die Möwe keinen Pixel), Pause bei Fingerdruck und beim Ziehen eines Teils,
Ende bei langer Störung, reduzierte Bewegung (am Start und mitten im Flug), Wächter bei langsamen Bildern (und kein falscher Alarm bei kurzen
Rucklern), nur Hamburg und nur nach dem Tutorial, fehlende Datei, nichts gespeichert, keine neuen Berechtigungen im Quelltext, Aufräumen nach
vielen Flügen, Bildstreifen.
Aufruf: python3 -I tests/test_moewe.py"""
import asyncio, json, datetime, sys, os, re, io, time
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server, WWW

URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
HTML = Path(WWW, 'index.html').read_text(encoding='utf-8')
DEFAULT_ON = bool(re.search(r'features:\s*\{[^}]*\bgull:\s*true', HTML))       # Standard aus CONFIG im Quelltext
res = []


def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''), flush=True)


def rewrite(fn):
    """Route-Handler: liefert index.html mit verändertem Quelltext aus (für die CONFIG-Schalterprüfung)."""
    async def h(route):
        r = await route.fetch()
        await route.fulfill(response=r, body=fn(await r.text()))
    return h


async def mk(b, q='?gull=1', w=390, h=844, level=3, tut=3, reduced=False, abort=None, rew=None, wait=2600):
    st = json.loads(json.dumps(BASE)); st['level'] = level; st['tut'] = tut          # Level 1 bis 4 = Hamburg
    ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='de-DE', reduced_motion='reduce' if reduced else 'no-preference')
    pg = await ctx.new_page(); pg.ctx = ctx; pg.errs = []; pg.reqs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    pg.on('request', lambda r: pg.reqs.append(r.url) if '/art/anim/' in r.url else None)
    if abort: await pg.route(abort, lambda r: r.abort())
    if rew: await pg.route(re.compile(r'/index\.html'), rewrite(rew))
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL + q); await pg.wait_for_timeout(1400)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(900)
    except Exception: pass
    await pg.wait_for_timeout(wait)
    return pg


GS = "MC.gull.state()"
TF = "(document.querySelector('.gull')||{style:{}}).style.transform||''"
BAND = "!!document.querySelector('.gull-band')"
SAMPLE = """async n => {
  const sl = ms => new Promise(r => setTimeout(r, ms)), out = [], q = s => document.querySelector(s);
  for (let i = 0; i < n; i++) {
    const band = q('.gull-band'), gull = q('.gull'), o = q('#orders').getBoundingClientRect(), b = q('#board').getBoundingClientRect();
    if (band && gull) {
      const br = band.getBoundingClientRect(), gr = gull.getBoundingClientRect();
      const vl = Math.max(gr.left, br.left), vr = Math.min(gr.right, br.right), vt = Math.max(gr.top, br.top), vb = Math.min(gr.bottom, br.bottom);
      out.push({ band: [br.left, br.top, br.right, br.bottom], gull: [gr.left, gr.top, gr.right, gr.bottom], orders: [o.left, o.top, o.right, o.bottom],
                 board: [b.left, b.top, b.right, b.bottom], vis: vr > vl && vb > vt ? [vl, vt, vr, vb] : null });
    } else out.push(null);
    await sl(150);
  }
  return out;
}"""
SPIN = "(() => { window.__busy = true; const f = () => { if (!window.__busy) return; const t = performance.now(); while (performance.now() - t < 70) {} requestAnimationFrame(f); }; requestAnimationFrame(f); })()"
SPIKES = "(() => { let k = 0; const f = () => { const t = performance.now(); while (performance.now() - t < 150) {} if (++k < 3) setTimeout(f, 400); }; setTimeout(f, 200); })()"


async def band_mitte(pg):
    r = await pg.evaluate("(()=>{const r=document.querySelector('.gull-band').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    return r[0] + r[2] / 2, r[1] + r[3] / 2


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])

        # ---------- A: Standardschalter (CONFIG), natürlicher Start ohne MC.gull.fly ----------
        pg = await mk(b, q='')
        st = await pg.evaluate(GS); cfg = await pg.evaluate('!!(CONFIG.features&&CONFIG.features.gull)')
        ok('A Standard ohne Parameter: Schalter = Eintrag CONFIG.features.gull', st['flag'] == cfg == DEFAULT_ON, [st['flag'], cfg, DEFAULT_ON])
        ok('A vor dem ersten Flug: kein Band, keine Möwendatei geladen', not await pg.evaluate(BAND) and not pg.reqs, pg.reqs)
        t0, seen = time.time(), False
        while time.time() - t0 < (25 if DEFAULT_ON else 12):
            if await pg.evaluate(BAND): seen = True; break
            await pg.wait_for_timeout(300)
        ok('A natürlicher Start: bei Standard an fliegt sie nach spätestens ca. 25 s von allein, bei Standard aus nie', seen == DEFAULT_ON, [seen, round(time.time() - t0, 1)])
        if seen:
            await pg.wait_for_timeout(600)
            ok('A beim Flug: genau eine Datei, einmal geladen (art/anim/moewe_hamburg.webp)', [u.rsplit('/', 1)[-1] for u in pg.reqs] == ['moewe_hamburg.webp'], pg.reqs)
        ok('A keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- B: Lage im freien Fenster, drei Fenstergrößen; C: Pixelvergleich und Bedienung ----------
        for w, h in [(390, 844), (360, 800), (412, 915)]:
            pg = await mk(b, w=w, h=h)
            keys0 = await pg.evaluate("Object.keys(localStorage).sort().join()")
            ok(f'B {w}x{h}: fly() startet einen Flug', await pg.evaluate("MC.gull.fly()") is True)
            smp = await pg.evaluate(SAMPLE, 20)
            ok(f'B {w}x{h}: Band war die ganze Zeit da', all(smp), sum(1 for s in smp if not s))
            sm = [s for s in smp if s]
            ok(f'B {w}x{h}: Band liegt zwischen Bestellungen und Brett (oben ≥ Unterkante Bestellungen, unten ≥ 5 px über dem Brett)',
               all(s['band'][1] >= s['orders'][3] and s['band'][3] <= s['board'][1] - 5 for s in sm),
               [(round(s['orders'][3]), round(s['band'][1]), round(s['band'][3]), round(s['board'][1])) for s in sm[:1]])
            ok(f'B {w}x{h}: Möwe senkrecht immer im Band (kein Pixel darüber oder darunter)', all(s['gull'][1] >= s['band'][1] - .5 and s['gull'][3] <= s['band'][3] + .5 for s in sm))
            ok(f'B {w}x{h}: sichtbarer Teil nie über Bestellungen oder Brett',
               all(s['vis'] is None or s['vis'][3] <= s['board'][1] and s['vis'][1] >= s['orders'][3] for s in sm))
            ok(f'B {w}x{h}: sie ist zu sehen und bewegt sich', sum(1 for s in sm if s['vis']) >= 5 and len({round(s['gull'][0]) for s in sm}) >= 8,
               [sum(1 for s in sm if s['vis']), len({round(s['gull'][0]) for s in sm})])
            app_w = await pg.evaluate("document.querySelector('#app').getBoundingClientRect().width")
            ok(f'B {w}x{h}: Band breit wie das Spielfenster', all(abs(s['band'][2] - s['band'][0] - app_w) < 1.5 for s in sm), app_w)
            if (w, h) == (390, 844):
                # C: Eigenschaften, Durchgriff, Pixelvergleich
                a = await pg.evaluate("""(() => { const q = s => document.querySelector(s), b = q('.gull-band'), g = q('.gull'), i = q('.gull-img'), cs = e => getComputedStyle(e);
                    return { aria: b.getAttribute('aria-hidden'), pe: [cs(b).pointerEvents, cs(g).pointerEvents, cs(i).pointerEvents], pos: cs(b).position, z: cs(b).zIndex, zApp: cs(q('#app')).zIndex,
                             ov: cs(b).overflow, next: q('#scene').nextElementSibling === b, alt: i.getAttribute('alt'), img: i.tagName }; })()""")
                ok('C Band: aria-hidden, ohne Zeigerereignisse, fest, Ebene 0 unter dem Spiel (Ebene 1), schneidet Überstehendes ab, direkt hinter #scene',
                   a['aria'] == 'true' and a['pe'] == ['none'] * 3 and a['pos'] == 'fixed' and a['z'] == '0' and a['zApp'] == '1' and a['ov'] == 'hidden' and a['next'], a)
                bx, by = await band_mitte(pg)
                gc = await pg.evaluate("(()=>{const r=document.querySelector('.gull').getBoundingClientRect();return [(Math.max(r.left,0)+Math.min(r.right,innerWidth))/2,(r.top+r.bottom)/2]})()")
                durch = await pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);return !!e&&!e.closest('.gull-band')}", gc)
                ok('C Antippen geht durch die Möwe hindurch (das Element an ihrer Stelle gehört nicht zum Band)', durch, gc)
                await pg.add_style_tag(content='*,*::before,*::after{animation:none!important;transition:none!important} #eTimer,#cat{visibility:hidden!important}')   # die zwei laufenden Anzeigen (Energie-Sekundentakt, Katzenbild) laufen unabhängig von der Möwe und würden den Vergleich stören
                box = await pg.evaluate("(()=>{const r=document.querySelector('.gull-band').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
                await pg.mouse.move(bx, by); await pg.mouse.down(); await pg.wait_for_timeout(600)               # Finger drauf: Möwe steht, Bild ruhig
                img1 = await pg.screenshot()
                await pg.evaluate("document.querySelector('.gull-band').style.visibility='hidden'"); await pg.wait_for_timeout(150)
                img2 = await pg.screenshot()
                await pg.evaluate("document.querySelector('.gull-band').style.visibility=''"); await pg.mouse.up()
                d = np.abs(np.asarray(Image.open(io.BytesIO(img1)).convert('RGB'), dtype=int) - np.asarray(Image.open(io.BytesIO(img2)).convert('RGB'), dtype=int)).sum(axis=2)
                x0, y0, bw, bh = [int(round(v * 2)) for v in box]
                mask = np.ones(d.shape, bool); mask[y0:y0 + bh, x0:x0 + bw] = False
                inn, out = int((d[y0:y0 + bh, x0:x0 + bw] > 60).sum()), int((d[mask] > 60).sum())
                ok('C Pixelvergleich mit und ohne Band: im Band ist die Möwe zu sehen (> 1500 Pixel)', inn > 1500, inn)
                ok('C Pixelvergleich: außerhalb des Bands (Bestellungen, Brett, Kopf, Leiste) ändert sich kein Pixel (≤ 40 von 1,3 Mio.; ohne Energie-Timer und Katze)', out <= 40, out)
            await pg.evaluate("MC.gull.stop()"); await pg.wait_for_timeout(200)
            ok(f'B {w}x{h}: nach stop() kein Band mehr, nichts gespeichert (Schlüssel des Speichers unverändert)',
               not await pg.evaluate(BAND) and await pg.evaluate("Object.keys(localStorage).sort().join()") == keys0 and await pg.evaluate("sessionStorage.length") == 0)
            ok(f'B {w}x{h}: keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- D: Pause bei Fingerdruck und beim Ziehen eines Teils ----------
        pg = await mk(b)
        ok('D fly() startet', await pg.evaluate("MC.gull.fly()") is True)
        await pg.wait_for_timeout(900); t1 = await pg.evaluate(TF); await pg.wait_for_timeout(350); t2 = await pg.evaluate(TF)
        ok('D ohne Berührung bewegt sie sich', t1 != t2 and (await pg.evaluate(GS))['paused'] is False, [t1, t2])
        bx, by = await band_mitte(pg)
        await pg.mouse.move(bx, by); await pg.mouse.down(); await pg.wait_for_timeout(450)
        a1 = await pg.evaluate(TF); s1 = await pg.evaluate(GS); await pg.wait_for_timeout(700); a2 = await pg.evaluate(TF)
        ok('D Finger auf dem Schirm: Möwe steht (Stellung bleibt gleich), Zustand paused', a1 == a2 and s1['paused'] and s1['hold'] and s1['flying'], [a1, a2, s1['paused']])
        await pg.mouse.up(); await pg.wait_for_timeout(700); a3 = await pg.evaluate(TF)
        ok('D 0,7 s nach dem Loslassen: weiter ruhig (Schonzeit 1,5 s)', a3 == a2 and (await pg.evaluate(GS))['hold'], [a2, a3])
        await pg.wait_for_timeout(2200); a4 = await pg.evaluate(TF)
        ok('D nach der Schonzeit fliegt sie weiter', a4 != a3 and not (await pg.evaluate(GS))['hold'] and (await pg.evaluate(GS))['flying'], [a3, a4])
        kinds = await pg.evaluate("[...document.querySelectorAll('.cell')].map(c => c.classList.contains('gen') ? 2 : (c.querySelector('.it') ? 1 : 0))")
        if 1 in kinds and 0 in kinds:
            cells = await pg.query_selector_all('.cell'); i, j = kinds.index(1), kinds.index(0)
            ba, bb = await cells[i].bounding_box(), await cells[j].bounding_box()
            await pg.mouse.move(ba['x'] + ba['width'] / 2, ba['y'] + ba['height'] / 2); await pg.mouse.down()
            await pg.mouse.move(ba['x'] + ba['width'] / 2 + 15, ba['y'] + ba['height'] / 2, steps=3)
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=6); await pg.wait_for_timeout(450)
            d1 = await pg.evaluate(TF); sd = await pg.evaluate(GS); await pg.wait_for_timeout(500); d2 = await pg.evaluate(TF)
            ok('D beim Ziehen eines Teils: Möwe steht', d1 == d2 and sd['paused'] and sd['hold'], [d1, d2])
            await pg.mouse.up(); await pg.wait_for_timeout(2600)
            ok('D nach dem Zug fliegt sie weiter (oder ist angekommen), Brett unverändert bedienbar (56 Zellen)', len(cells) == 56 and ((await pg.evaluate(TF)) != d2 or not (await pg.evaluate(GS))['flying']))
        else:
            ok('D Brett hat Teil und freie Zelle für den Zug', False, kinds)
        ok('D keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- E: lange Störung -> Möwe fliegt weg (nach 5 s) ----------
        pg = await mk(b)
        await pg.evaluate("MC.gull.fly()"); await pg.wait_for_timeout(800)
        bx, by = await band_mitte(pg); await pg.mouse.move(bx, by); await pg.mouse.down(); await pg.wait_for_timeout(6300)
        s = await pg.evaluate(GS)
        ok('E Finger länger als 5 s auf dem Schirm: Flug beendet, Band entfernt, nächster Versuch geplant', not s['flying'] and not await pg.evaluate(BAND) and s['planned'], s)
        await pg.mouse.up(); ok('E keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- F: reduzierte Bewegung am Start (Systemeinstellung) ----------
        pg = await mk(b, reduced=True, wait=13500)
        s = await pg.evaluate(GS)
        ok('F reduzierte Bewegung erkannt, Möwe ruht (hold), fly() gibt false', await pg.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches") and s['hold'] and await pg.evaluate("MC.gull.fly()") is False, s)
        ok('F in über 15 s kein Flug von allein, keine Möwendatei geladen', not await pg.evaluate(BAND) and not pg.reqs, pg.reqs)
        ok('F keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- G: reduzierte Bewegung mitten im Flug ----------
        pg = await mk(b)
        await pg.evaluate("MC.gull.fly()"); await pg.wait_for_timeout(900)
        await pg.emulate_media(reduced_motion='reduce'); await pg.wait_for_timeout(900)
        s = await pg.evaluate(GS)
        ok('G Umschalten auf „Bewegung reduzieren“ beendet den Flug sofort, Band entfernt', not s['flying'] and not await pg.evaluate(BAND), s)
        ok('G keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- H: Wächter schaltet bei langsamen Bildern ab; I: kurze Ruckler lösen keinen Alarm aus ----------
        pg = await mk(b)
        await pg.evaluate("MC.gull.fly()"); await pg.wait_for_timeout(500); await pg.evaluate(SPIN)
        t0, off = time.time(), ''
        while time.time() - t0 < 25 and not off:
            await pg.wait_for_timeout(500); off = (await pg.evaluate(GS))['off']
        await pg.evaluate("window.__busy = false"); await pg.wait_for_timeout(600)
        s = await pg.evaluate(GS)
        ok('H dauerhaft langsame Bilder (70 ms): Wächter schaltet die Möwe für die Sitzung ab (off = perf)', off == 'perf' and s['off'] == 'perf', [off, round(time.time() - t0, 1)])
        ok('H danach: kein Band, kein Flug, kein geplanter Versuch, fly() gibt false', not s['flying'] and not await pg.evaluate(BAND) and not s['planned'] and await pg.evaluate("MC.gull.fly()") is False, s)
        ok('H Spiel läuft weiter (56 Zellen, Zustand lesbar)', await pg.evaluate("document.querySelectorAll('.cell').length") == 56 and await pg.evaluate("MC.state().level") == 3)
        ok('H keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()
        pg = await mk(b)
        await pg.evaluate("MC.gull.fly()"); await pg.wait_for_timeout(500); await pg.evaluate(SPIKES); await pg.wait_for_timeout(2200)
        s = await pg.evaluate(GS)
        ok('I drei kurze Ruckler (150 ms): kein Alarm, Möwe fliegt weiter', s['off'] == '' and s['flying'] and s['watch']['strikes'] == 0, s['watch'])
        ok('I keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- J: nur Hamburg, nur nach dem Tutorial ----------
        pg = await mk(b)
        ok('J Hamburg: Flug möglich', await pg.evaluate("MC.gull.fly()") is True); await pg.wait_for_timeout(500)
        await pg.evaluate("MC.world(5)"); await pg.wait_for_timeout(900)
        ok('J Wechsel nach Wien beendet den Flug, Band entfernt', not (await pg.evaluate(GS))['flying'] and not await pg.evaluate(BAND))
        await pg.wait_for_timeout(1500)
        ok('J Wien: fly() gibt false, keine Möwe', await pg.evaluate("MC.gull.fly()") is False and not await pg.evaluate(BAND))
        await pg.evaluate("MC.world(3)"); await pg.wait_for_timeout(2800)
        ok('J zurück in Hamburg: wieder möglich', await pg.evaluate("MC.gull.fly()") is True); await pg.evaluate("MC.gull.stop()")
        await pg.evaluate("MC.state().tut = 2"); await pg.wait_for_timeout(200)
        ok('J Tutorial noch nicht fertig: fly() gibt false', await pg.evaluate("MC.gull.fly()") is False)
        await pg.evaluate("MC.state().tut = 3")
        ok('J keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- K: kleines Fenster 360x640 (kein freies Fenster): nichts, auch keine Datei ----------
        pg = await mk(b, w=360, h=640)
        s = await pg.evaluate(GS)
        ok('K 360x640: kein freies Fenster (band = null), fly() gibt false, keine Möwendatei geladen', s['band'] is None and await pg.evaluate("MC.gull.fly()") is False and not pg.reqs, [s['band'], pg.reqs])
        ok('K keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- L: Schalter aus = nichts (URL-Parameter, CONFIG false, Eintrag fehlt) ----------
        for name, kw, lang in [('?gull=0', dict(q='?gull=0', wait=13500), True),
                               ('CONFIG gull:false (ohne Parameter)', dict(q='', rew=lambda t: re.sub(r'(features:\s*\{[^}]*\bgull:\s*)true', r'\1false', t)), False),
                               ('CONFIG ohne features-Eintrag', dict(q='', rew=lambda t: re.sub(r'features:\s*\{[^}]*\},[^\n]*\n', '', t, count=1)), False)]:
            pg = await mk(b, **kw)
            s = await pg.evaluate(GS)
            ok(f'L {name}: flag false, off = flag, kein geplanter Flug, fly() gibt false', s['flag'] is False and s['off'] == 'flag' and not s['planned'] and not s['flying'] and await pg.evaluate("MC.gull.fly()") is False, s)
            ok(f'L {name}: kein Element (.gull-band, .gull, .gull-img), keine Datei geladen', not await pg.evaluate("!!document.querySelector('.gull-band,.gull,.gull-img')") and not pg.reqs, pg.reqs)
            if lang: ok(f'L {name}: auch nach über 15 s kein Flug', not await pg.evaluate(BAND) and not pg.reqs)
            ok(f'L {name}: keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- M: Bilddatei fehlt -> aus für die Sitzung, Spiel läuft ----------
        pg = await mk(b, abort='**/art/anim/**')
        ok('M Datei nicht ladbar: fly() gibt false, off = asset, kein Band', await pg.evaluate("MC.gull.fly()") is False and (await pg.evaluate(GS))['off'] == 'asset' and not await pg.evaluate(BAND))
        ok('M Spiel läuft weiter (56 Zellen, keine Fehler)', await pg.evaluate("document.querySelectorAll('.cell').length") == 56 and not pg.errs, pg.errs); await pg.ctx.close()

        # ---------- N: Aufräumen nach vielen Flügen ----------
        pg = await mk(b)
        n0 = await pg.evaluate("document.getElementsByTagName('*').length"); k0 = await pg.evaluate("Object.keys(localStorage).sort().join()")
        gut = 0
        for _ in range(8):
            gut += 1 if await pg.evaluate("MC.gull.fly()") is True else 0
            await pg.wait_for_timeout(350); await pg.evaluate("MC.gull.stop()"); await pg.wait_for_timeout(120)
        n1 = await pg.evaluate("document.getElementsByTagName('*').length")
        ok('N acht Flüge nacheinander gestartet und beendet', gut == 8, gut)
        ok('N danach gleiche Anzahl Elemente, kein Band, Schlüssel des Speichers unverändert, nichts in sessionStorage', n1 == n0 and not await pg.evaluate(BAND) and await pg.evaluate("Object.keys(localStorage).sort().join()") == k0 and await pg.evaluate("sessionStorage.length") == 0, [n0, n1])
        ok('N Datei nur einmal geladen', len(pg.reqs) == 1, pg.reqs)
        ok('N keine Fehler', not pg.errs, pg.errs); await pg.ctx.close()
        await b.close()

    # ---------- P: Quelltext des Möwen-Moduls ----------
    i0, i1 = HTML.index('const GULL = '), HTML.index('/* ---------------- Modals')
    code = HTML[i0:i1]
    bad = [t for t in ['localStorage', 'sessionStorage', 'indexedDB', 'caches.', 'fetch(', 'XMLHttpRequest', 'WebSocket', 'sendBeacon', 'Notification', 'geolocation', 'mediaDevices',
                       'vibrate', 'AudioContext', 'new Audio', 'Sound.', 'Capacitor', 'Platform.', 'import(', 'importScripts', 'navigator.', 'setInterval', 'document.cookie'] if t in code]
    ok('P Möwen-Modul: keine Speicher-, Netz-, Geräte- oder Ton-Zugriffe, kein setInterval (keine neuen Berechtigungen oder Abhängigkeiten)', not bad, bad)
    schreibt = re.findall(r'\bS\.[A-Za-z_][\w.\[\]]*\s*(?:=(?!=)|\+=|-=|\+\+|--)', code) + re.findall(r'\b(?:save|persist|addXP|addCoins|spend)\w*\(', code)
    ok('P Möwen-Modul schreibt nie in den Spielstand (kein S.… =, kein save/addXP/addCoins)', not schreibt, schreibt)
    ok('P bewegt wird nur per transform (kein left/top/width/height in place())', 'style.left' not in code and 'style.top =' not in code and re.search(r'function place\(r\)[\s\S]*?\n  }', code).group(0).count('style.transform') == 2)
    # ---------- Q: Bildstreifen ----------
    tab = json.loads(re.search(r'/\*GULL_DATA\*/(.*?)/\*END_GULL_DATA\*/', HTML, re.S).group(1))
    f = Path(WWW, tab['file']); im = Image.open(f) if f.exists() else None
    ok('Q Bildstreifen vorhanden, Maße = Tabelle GULL (n × w, h), unter 120 KB', f.exists() and im.size == (tab['n'] * tab['w'], tab['h']) and f.stat().st_size < 120000, [tab, im.size if im else None, f.stat().st_size if im else 0])
    ok('Q Bildstreifen hat Alphakanal (frei fliegend, kein Kasten)', im is not None and im.mode in ('RGBA', 'LA') and int(np.asarray(im.convert('RGBA'))[..., 3].min()) == 0, im.mode if im else None)
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
    sys.exit(0 if all(res) else 1)


asyncio.run(main())
