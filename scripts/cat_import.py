#!/usr/bin/env python3
"""Katzen-Import fuer Noa's Bean Trail (Mocha, die Café-Katze).

Nimmt das Integrationspaket (ZIP oder entpackter Ordner) und erzeugt daraus alles, was das Spiel braucht:
  www/art/cat/c01.webp ...   die Bilder (identische Frames werden nur einmal gespeichert), alle gleich zugeschnitten
  www/art/cat/h1..h3.webp    Herz-Partikel
  www/art/cat/purr.wav       Schnurr-Schleife (mittlerer, gleichmaessiger Teil, nahtlos ueberblendet, normalisiert)
und schreibt die Tabelle `const CAT` (Frames, Zustaende, Zeiten, Trefferflaeche) in www/index.html zwischen die
Marken /*CAT_DATA*/ und /*END_CAT_DATA*/.

Erwartete Dateien im Paket (wie von Perfekt geliefert, Stand 24.11.2026):
  sprites/cat_01_idle.png ... cat_24_return.png   (512x512, RGBA, alle Frames gleiche Leinwand)
  effects/heart_1.png ... heart_3.png
  audio/purr_*.wav                                (Platzhalter; spaeter durch eine lizenzierte Aufnahme ersetzbar)
  docs/animation_manifest.json                    (Zustaende, Frame-Nummern, Zeiten)

Aufbereitung: Staubpunkte entfernen (Alpha < 10), fast deckende Flaechen ganz deckend machen (Alpha 250 -> 255),
alle Frames mit demselben Rahmen zuschneiden (Frames duerfen sich bewegen, der Rahmen bleibt gleich), mit
vormultipliziertem Alpha verkleinern (keine dunklen Raender), als kleines WebP speichern.

Aufruf:  python3 -I scripts/cat_import.py <ZIP-oder-Ordner> [--width 320] [--quality 80]
Ohne die Dateien in www/art/cat/ bleibt im Spiel die gezeichnete Katze (SVG) mit dem alten Verhalten.
"""
import argparse, hashlib, io, json, re, sys, wave, zipfile
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'www' / 'art' / 'cat'
HTML = ROOT / 'www' / 'index.html'
HEART_PX = 96                                   # Herz-Sprites (im Spiel hoechstens ~36 CSS-Pixel gross)
LOOP_FROM, LOOP_TO, XFADE = 0.20, 1.80, 0.12    # Schnurr-Schleife: Ausschnitt in s und Ueberblendung in s


def open_source(path):
    """Gibt ein Objekt mit names() und read(name) zurueck, fuer ZIP und Ordner gleichermassen."""
    p = Path(path)
    if p.is_dir():
        base = p
        class D:
            def names(self): return [str(f.relative_to(base)).replace('\\', '/') for f in base.rglob('*') if f.is_file()]
            def read(self, n): return (base / n).read_bytes()
        return D()
    z = zipfile.ZipFile(p)
    class Z:
        def names(self): return [n for n in z.namelist() if not n.endswith('/')]
        def read(self, n): return z.read(n)
    return Z()


def find(names, pattern):
    rx = re.compile(pattern)
    return sorted([n for n in names if rx.search(n)], key=lambda n: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', n)])


def clean(rgba):
    """RGBA (uint8) -> sauber: Staub weg, fast deckend -> deckend."""
    a = rgba[..., 3].astype(np.float32)
    a = np.clip(a * 255.0 / 250.0, 0, 255)       # die Katze ist mit Alpha ~250 freigestellt: ganz deckend machen
    a[a < 10] = 0                                  # Staubpunkte (Alpha 1-4) und Raender entfernen
    out = rgba.copy(); out[..., 3] = np.round(a).astype(np.uint8)
    return out


def resize_premult(rgba, w, h):
    """Verkleinern mit vormultipliziertem Alpha (sonst entstehen dunkle Saeume um die Figur)."""
    f = rgba.astype(np.float32) / 255.0
    f[..., :3] *= f[..., 3:4]
    f = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA)
    al = f[..., 3:4]
    rgb = np.where(al > 1e-4, f[..., :3] / np.maximum(al, 1e-4), 0)
    return np.clip(np.concatenate([rgb, al], axis=2) * 255.0 + 0.5, 0, 255).astype(np.uint8)


def save_webp(arr, path, quality):
    Image.fromarray(arr, 'RGBA').save(path, 'WEBP', quality=quality, alpha_quality=100, method=6)


def seamless_loop(samples, sr):
    """Mittleren Teil ausschneiden und das Ende in den Anfang ueberblenden (gleichmaessige Leistung), dann normalisieren."""
    a, b = int(LOOP_FROM * sr), int(LOOP_TO * sr)
    seg = samples[a:b].astype(np.float64)
    L = int(XFADE * sr)
    t = np.linspace(0, np.pi / 2, L)
    head = seg[:L] * np.sin(t) + seg[-L:] * np.cos(t)
    loop = np.concatenate([head, seg[L:-L]])
    loop -= loop.mean()
    loop *= 0.9 / max(1e-9, np.abs(loop).max())
    return loop


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source'); ap.add_argument('--width', type=int, default=320); ap.add_argument('--quality', type=int, default=80)
    args = ap.parse_args()
    src = open_source(args.source); names = src.names()

    frames_n = find(names, r'sprites/cat_(\d+)_[^/]*\.png$')
    frames_n = [n for n in frames_n if 'spritesheet' not in n]
    if not frames_n: sys.exit('Keine Frames gefunden (erwartet: sprites/cat_01_*.png ...).')
    raw = [clean(np.array(Image.open(io.BytesIO(src.read(n))).convert('RGBA'))) for n in frames_n]
    H0, W0 = raw[0].shape[:2]
    if any(r.shape[:2] != (H0, W0) for r in raw): sys.exit('Alle Frames muessen dieselbe Leinwand haben.')

    # gemeinsamer Zuschnitt: Vereinigung aller sichtbaren Flaechen, kleiner Rand
    ys = np.concatenate([np.where(r[..., 3] > 0)[0] for r in raw]); xs = np.concatenate([np.where(r[..., 3] > 0)[1] for r in raw])
    m = 6
    x0, x1, y0, y1 = max(0, xs.min() - m), min(W0, xs.max() + 1 + m), max(0, ys.min() - m), min(H0, ys.max() + 1 + m)
    cw, ch = x1 - x0, y1 - y0
    W = args.width; H = round(W * ch / cw)
    print(f'{len(raw)} Frames {W0}x{H0} -> Zuschnitt {cw}x{ch} -> {W}x{H}')

    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob('c*.webp'): f.unlink()
    unique, fmap, seen = [], [], {}
    for r in raw:
        a = resize_premult(r[y0:y1, x0:x1], W, H)
        h = hashlib.md5(a.tobytes()).hexdigest()
        if h not in seen:
            seen[h] = len(unique); unique.append(a)
        fmap.append(seen[h])
    total = 0
    for i, a in enumerate(unique):
        p = OUT / f'c{i + 1:02d}.webp'; save_webp(a, p, args.quality); total += p.stat().st_size
    print(f'{len(unique)} verschiedene Bilder, {total / 1024:.0f} KB')

    # Trefferflaeche: sichtbare Katze in den Frames, in denen sie sitzt/gestreichelt wird (Frames 12-20), etwas eingezogen
    hit_rows = [i for i in range(11, min(20, len(raw)))]
    hx = np.concatenate([np.where(unique[fmap[i]][..., 3] > 128)[1] for i in hit_rows]); hy = np.concatenate([np.where(unique[fmap[i]][..., 3] > 128)[0] for i in hit_rows])
    bx0, bx1, by0, by1 = np.percentile(hx, 1), np.percentile(hx, 99), np.percentile(hy, 1), np.percentile(hy, 99)
    hit = [round(float(bx0) / W, 3), round(float(by0) / H, 3), round(float(bx1) / W, 3), round(float(by1) / H, 3)]

    # Herzen
    hearts = []
    for n in find(names, r'effects/heart_(\d+)\.png$'):
        im = clean(np.array(Image.open(io.BytesIO(src.read(n))).convert('RGBA')))
        yy, xx = np.where(im[..., 3] > 0)
        im = im[max(0, yy.min() - 2):yy.max() + 3, max(0, xx.min() - 2):xx.max() + 3]
        hh = HEART_PX; ww = max(1, round(HEART_PX * im.shape[1] / im.shape[0]))
        key = f'h{len(hearts) + 1}'; save_webp(resize_premult(im, ww, hh), OUT / f'{key}.webp', args.quality); hearts.append(key)

    # Schnurren
    wavs = find(names, r'audio/[^/]*\.wav$')
    purr = False
    if wavs:
        w = wave.open(io.BytesIO(src.read(wavs[0])))
        sr, n = w.getframerate(), w.getnframes()
        if w.getsampwidth() == 2 and w.getnchannels() == 1:
            s = np.frombuffer(w.readframes(n), dtype='<i2').astype(np.float64) / 32768.0
            loop = seamless_loop(s, sr)
            with wave.open(str(OUT / 'purr.wav'), 'wb') as o:
                o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
                o.writeframes((np.clip(loop, -1, 1) * 32767).astype('<i2').tobytes())
            purr = True
        else:
            print('Hinweis: WAV ist nicht 16 Bit mono, Schnurren wird nicht umgebaut.')

    # Zustaende aus dem Manifest des Pakets
    states = {}
    man = [n for n in names if n.endswith('animation_manifest.json')]
    if man:
        mj = json.loads(src.read(man[0]).decode('utf-8'))
        for k, v in mj.get('states', {}).items():
            states[k] = {'f': v['frames'], 'ms': v['frameDurationMs'], 'loop': 1 if v.get('loop') else 0}
        inter = mj.get('interaction', {}); aud = mj.get('audio', {})
    else:
        inter, aud = {}, {}
    if not states: sys.exit('animation_manifest.json mit "states" fehlt.')
    cat = {'v': 1, 'w': W, 'h': H, 'files': [f'c{i + 1:02d}' for i in range(len(unique))], 'map': [int(i) for i in fmap],
           'hit': hit, 'hearts': hearts, 'purr': purr, 'states': states,
           'idleReturnMs': int(inter.get('idleReturnMs', 8000)), 'fadeOutMs': int(aud.get('fadeOutMs', 180))}
    data = json.dumps(cat, separators=(',', ':'), ensure_ascii=False)
    html = HTML.read_text(encoding='utf-8')
    new, k = re.subn(r'/\*CAT_DATA\*/.*?/\*END_CAT_DATA\*/', lambda _: '/*CAT_DATA*/' + data + '/*END_CAT_DATA*/', html, flags=re.S)
    if k != 1: sys.exit('Marken /*CAT_DATA*/ ... /*END_CAT_DATA*/ in www/index.html nicht gefunden.')
    HTML.write_text(new, encoding='utf-8')
    print('Manifest eingetragen:', data[:160] + ' ...')


if __name__ == '__main__':
    main()
