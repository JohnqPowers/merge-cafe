#!/usr/bin/env python3
"""Möwen-Flugstreifen (Hamburg) für Noa's Bean Trail.

Nimmt das Stadtpaket vom 25.11.2026 (ZIP oder entpackter Ordner) und baut aus den acht Flug-Frames
  07_Animationen_Optional/moewe/moewe_flug_00.png ... moewe_flug_07.png     (256x256, RGBA, gleiche Leinwand)
einen waagerechten Streifen
  www/art/anim/moewe_hamburg.webp                                          (acht Bilder nebeneinander, alle gleich zugeschnitten)
und schreibt die Tabelle `const GULL` (Datei, Anzahl, Bildmaße) in www/index.html zwischen die Marken /*GULL_DATA*/ und /*END_GULL_DATA*/.

Aufbereitung: gemeinsamer Zuschnitt aus ALLEN Frames (Vereinigung der sichtbaren Flächen plus kleiner Rand, damit die Bilder
deckungsgleich bleiben), Verkleinern mit vormultipliziertem Alpha (keine dunklen Säume), ein WebP mit Alpha.
Die Möwe ist ein Experiment (Branch exp/moewe-hamburg, Schalter CONFIG.features.gull); ohne die Datei zeigt das Spiel einfach keine Möwe.

Aufruf:  python3 -I scripts/gull_import.py <ZIP-oder-Ordner> [--width 192] [--quality 82] [--root PFAD]
         --root: anderes Arbeitsverzeichnis (z. B. eine Kopie des Repos, um die Datei bitgleich nachzustellen)
"""
import argparse, io, json, re, sys, zipfile
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MUSTER = r'07_Animationen_Optional/moewe/moewe_flug_(\d\d)\.png$'
AUSGABE = 'moewe_hamburg.webp'
RAND = 2          # Pixel Rand um die gemeinsame sichtbare Fläche (im Original)
SCHWELLE = 8      # Alpha ab hier gilt als sichtbar (Staubpunkte zählen nicht)


def quelle_oeffnen(pfad):
    """Gibt ein Objekt mit names() und read(name) zurück, für ZIP und Ordner gleichermaßen."""
    p = Path(pfad)
    if p.is_dir():
        class D:
            def names(self): return [f.relative_to(p).as_posix() for f in p.rglob('*') if f.is_file()]
            def read(self, n): return (p / n).read_bytes()
        return D()
    z = zipfile.ZipFile(p)
    class Z:
        def names(self): return [n for n in z.namelist() if not n.endswith('/')]
        def read(self, n): return z.read(n)
    return Z()


def verkleinern(rgba, w, h):
    """Verkleinern mit vormultipliziertem Alpha (sonst entstehen dunkle Säume um die Figur)."""
    f = rgba.astype(np.float32) / 255.0
    f[..., :3] *= f[..., 3:4]
    f = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA)
    al = f[..., 3:4]
    rgb = np.where(al > 1e-4, f[..., :3] / np.maximum(al, 1e-4), 0)
    return np.clip(np.concatenate([rgb, al], axis=2) * 255.0 + 0.5, 0, 255).astype(np.uint8)


def streifen(frames, breite):
    """Acht RGBA-Frames (uint8) -> (Streifen als RGBA-Array, Zellbreite, Zellhöhe, Zuschnittrahmen)."""
    h0, w0 = frames[0].shape[:2]
    if any(f.shape[:2] != (h0, w0) for f in frames):
        sys.exit('Alle Frames müssen dieselbe Leinwand haben.')
    ys = np.concatenate([np.where(f[..., 3] > SCHWELLE)[0] for f in frames])
    xs = np.concatenate([np.where(f[..., 3] > SCHWELLE)[1] for f in frames])
    x0, x1 = max(0, xs.min() - RAND), min(w0, xs.max() + 1 + RAND)
    y0, y1 = max(0, ys.min() - RAND), min(h0, ys.max() + 1 + RAND)
    cw, ch = x1 - x0, y1 - y0
    w, h = breite, round(breite * ch / cw)
    zellen = [verkleinern(f[y0:y1, x0:x1], w, h) for f in frames]
    return np.concatenate(zellen, axis=1), w, h, tuple(int(v) for v in (x0, y0, x1, y1))


def main():
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('quelle'); ap.add_argument('--width', type=int, default=192); ap.add_argument('--quality', type=int, default=82)
    ap.add_argument('--root', default=None)
    a = ap.parse_args()
    if a.root:
        ROOT = Path(a.root).resolve()
    src = quelle_oeffnen(a.quelle)
    namen = sorted((n for n in src.names() if re.search(MUSTER, n)), key=lambda n: int(re.search(MUSTER, n).group(1)))
    if len(namen) != 8:
        sys.exit(f'Erwartet werden acht Flug-Frames ({MUSTER}), gefunden: {len(namen)}')
    frames = [np.array(Image.open(io.BytesIO(src.read(n))).convert('RGBA')) for n in namen]
    bild, w, h, rahmen = streifen(frames, a.width)
    out = ROOT / 'www' / 'art' / 'anim'
    out.mkdir(parents=True, exist_ok=True)
    ziel = out / AUSGABE
    Image.fromarray(bild, 'RGBA').save(ziel, 'WEBP', quality=a.quality, alpha_quality=100, method=6)
    print(f'8 Frames {frames[0].shape[1]}x{frames[0].shape[0]} -> Zuschnitt {rahmen} -> je {w}x{h}, Streifen {8 * w}x{h}, {ziel.stat().st_size / 1024:.0f} KB')

    data = json.dumps({'v': 1, 'file': f'art/anim/{AUSGABE}', 'n': 8, 'w': w, 'h': h}, separators=(',', ':'))
    html_pfad = ROOT / 'www' / 'index.html'
    html = html_pfad.read_text(encoding='utf-8')
    neu, k = re.subn(r'/\*GULL_DATA\*/.*?/\*END_GULL_DATA\*/', lambda _: '/*GULL_DATA*/' + data + '/*END_GULL_DATA*/', html, flags=re.S)
    if k != 1:
        sys.exit('Marken /*GULL_DATA*/ ... /*END_GULL_DATA*/ in www/index.html nicht gefunden.')
    if neu != html:
        html_pfad.write_text(neu, encoding='utf-8')
    print('Tabelle eingetragen:', data)


if __name__ == '__main__':
    main()
