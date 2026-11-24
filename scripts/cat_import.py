#!/usr/bin/env python3
"""Katzen-Import fuer Noa's Bean Trail (Mocha, die Café-Katze).

Nimmt das Integrationspaket (ZIP oder entpackter Ordner) und erzeugt daraus, was das Spiel braucht. Seit 1.5.17 sind das nur die
Ruhebilder (Zustand IDLE): Sprung, Streicheln, Herzen und Schnurr-Ton wurden aus dem Spiel genommen (Speicher, Rueckmeldung des Eigentuemers).
  www/art/cat/c01.webp ...   die Ruhebilder (identische Frames werden nur einmal gespeichert), alle gleich zugeschnitten
und schreibt die Tabelle `const CAT` (Dateien, Frame-Reihenfolge, Zeit) in www/index.html zwischen die Marken
/*CAT_DATA*/ und /*END_CAT_DATA*/.

Erwartete Dateien im Paket (wie von Perfekt geliefert, Stand 24.11.2026):
  sprites/cat_01_idle.png ... cat_24_return.png   (512x512, RGBA, alle Frames gleiche Leinwand)
  docs/animation_manifest.json                    (Zustaende, Frame-Nummern, Zeiten)

Aufbereitung: Staubpunkte entfernen (Alpha < 10), fast deckende Flaechen ganz deckend machen (Alpha 250 -> 255),
alle Frames mit demselben Rahmen zuschneiden (der Rahmen wird aus ALLEN Frames bestimmt, damit die Bilder bitgleich bleiben),
mit vormultipliziertem Alpha verkleinern (keine dunklen Raender), als kleines WebP speichern; geschrieben werden nur die IDLE-Frames.

Aufruf:  python3 -I scripts/cat_import.py <ZIP-oder-Ordner> [--width 320] [--quality 80]
Ohne die Dateien in www/art/cat/ bleibt im Spiel die gezeichnete Katze (SVG).
"""
import argparse, hashlib, io, json, re, sys, zipfile
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'www' / 'art' / 'cat'
HTML = ROOT / 'www' / 'index.html'


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

    # Zustaende aus dem Manifest des Pakets: nur IDLE wird gebraucht
    man = [n for n in names if n.endswith('animation_manifest.json')]
    if not man: sys.exit('animation_manifest.json fehlt.')
    mj = json.loads(src.read(man[0]).decode('utf-8'))
    idle = mj.get('states', {}).get('IDLE')
    if not idle: sys.exit('animation_manifest.json ohne Zustand "IDLE".')
    idle_frames = idle['frames']

    OUT.mkdir(parents=True, exist_ok=True)
    for f in list(OUT.glob('c*.webp')) + list(OUT.glob('h*.webp')) + list(OUT.glob('purr.wav')): f.unlink()
    unique, fmap, seen = [], [], {}
    for r in raw:
        a = resize_premult(r[y0:y1, x0:x1], W, H)
        h = hashlib.md5(a.tobytes()).hexdigest()
        if h not in seen:
            seen[h] = len(unique); unique.append(a)
        fmap.append(seen[h])
    used = sorted({fmap[f - 1] for f in idle_frames})                 # Bilder, die der Zustand IDLE braucht (Namen bleiben c01, c02, ...)
    total = 0
    for i in used:
        p = OUT / f'c{i + 1:02d}.webp'; save_webp(unique[i], p, args.quality); total += p.stat().st_size
    print(f'{len(used)} Ruhebilder, {total / 1024:.0f} KB')

    cat = {'v': 2, 'w': W, 'h': H, 'files': [f'c{i + 1:02d}' for i in used], 'map': [used.index(fmap[f - 1]) for f in idle_frames],
           'states': {'IDLE': {'f': list(range(1, len(idle_frames) + 1)), 'ms': idle['frameDurationMs'], 'loop': 1}}}
    data = json.dumps(cat, separators=(',', ':'), ensure_ascii=False)
    html = HTML.read_text(encoding='utf-8')
    new, k = re.subn(r'/\*CAT_DATA\*/.*?/\*END_CAT_DATA\*/', lambda _: '/*CAT_DATA*/' + data + '/*END_CAT_DATA*/', html, flags=re.S)
    if k != 1: sys.exit('Marken /*CAT_DATA*/ ... /*END_CAT_DATA*/ in www/index.html nicht gefunden.')
    HTML.write_text(new, encoding='utf-8')
    print('Manifest eingetragen:', data[:160] + ' ...')


if __name__ == '__main__':
    main()
