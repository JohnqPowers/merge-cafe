#!/usr/bin/env python3
"""Bild-Import fuer Merge Café.

Nimmt ein ZIP oder einen Ordner mit PNG/WebP-Dateien (Namen wie in docs/ART_BRIEF.md, z. B.
g1_teekanne.png, k1_s2_espresso.png) und erzeugt daraus einheitliche Sprites in www/art/<key>.webp:
  - Freistellen (echte Transparenz wird uebernommen, sonst wird der einfarbige Hintergrund entfernt)
  - auf die Motivgroesse zuschneiden, einheitlich skalieren und mittig setzen
  - weichen Kontaktschatten ins Bild backen (kostet im Spiel keine Rechenleistung)
  - als kleines WebP speichern und das Manifest `const ART = new Set([...])` in www/index.html aktualisieren

Aufruf:  python3 -I scripts/art_import.py <ZIP-oder-Ordner> [--size 256] [--fill 0.84]
Das Spiel faellt fuer jedes Teil ohne Bild automatisch auf das Emoji zurueck.
"""
import argparse, io, re, sys, zipfile
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
KEY = re.compile(r'^(g\d|k\d_s\d)(?:[_.]|$)')


def key_of(name):
    m = KEY.match(Path(name).name.lower())
    return m.group(1) if m else None


def cutout(im):
    """RGBA mit sauberem Rand. Hat das Bild schon echte Transparenz, bleibt es unveraendert."""
    im = im.convert('RGBA')
    a = np.array(im).astype(np.float32)
    h, w = a.shape[:2]
    if (a[:, :, 3] < 250).mean() > 0.04:
        return im
    rgb = a[:, :, :3]
    m = max(8, min(h, w) // 40)
    ring = np.concatenate([rgb[m:2 * m, w // 4:3 * w // 4].reshape(-1, 3), rgb[h - 2 * m:h - m, w // 4:3 * w // 4].reshape(-1, 3),
                           rgb[h // 4:3 * h // 4, m:2 * m].reshape(-1, 3), rgb[h // 4:3 * h // 4, w - 2 * m:w - m].reshape(-1, 3)])
    bgc = np.median(ring, axis=0)
    near = (np.linalg.norm(rgb - bgc, axis=2) < 60) | (rgb.min(axis=2) > 235)      # Hintergrundfarbe oder Weiss (abgerundete Ecken)
    n, lab = cv2.connectedComponents(near.astype(np.uint8), connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    fg = ~bg
    n2, lab2, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), connectivity=8)
    if n2 < 2:
        return im
    fg = lab2 == (1 + np.argmax(st[1:, cv2.CC_STAT_AREA]))
    dtf = cv2.distanceTransform(fg.astype(np.uint8), cv2.DIST_L2, 5)
    dtb = cv2.distanceTransform((~fg).astype(np.uint8), cv2.DIST_L2, 5)
    sel = (dtf >= 4) & (dtf <= 8)
    edge_col = np.median(rgb[sel], axis=0) if sel.any() else rgb[fg].mean(axis=0)
    zone = ((dtf > 0) & (dtf <= 3)) | ((dtb > 0) & (dtb <= 2))
    v = edge_col - bgc
    vv = float(v @ v)
    al = np.clip(((rgb - bgc) @ v) / vv, 0, 1) if vv > 1 else fg.astype(np.float32)
    alpha = np.where(zone, al, fg.astype(np.float32))
    alpha[dtb > 2] = 0
    col = rgb.copy()
    z = zone & (alpha > .05)
    col[z] = np.clip((rgb[z] - (1 - alpha[z])[:, None] * bgc) / alpha[z][:, None], 0, 255)
    return Image.fromarray(np.dstack([col, alpha * 255]).astype(np.uint8))


def sprite(im, size=256, fill=0.84, lift=0.03):
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 12)
    if not len(xs):
        raise ValueError('Bild ist leer')
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = size * fill / max(crop.size)
    crop = crop.resize((max(1, round(crop.size[0] * k)), max(1, round(crop.size[1] * k))), Image.LANCZOS)
    cw, ch = crop.size
    ox, oy = (size - cw) // 2, round((size - ch) / 2 - size * lift)
    ca = np.array(crop)[:, :, 3]
    rows = ca[int(ch * .82):, :] > 128                                   # Breite des Motivs am Boden
    bottom = int(rows.any(axis=0).sum()) or cw
    sw = min(max(bottom * 1.05, cw * .38), cw * .92)
    sh_h = size * .085
    cy = oy + ch - sh_h * .1
    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([size / 2 - sw / 2, cy - sh_h / 2, size / 2 + sw / 2, cy + sh_h / 2], fill=(14, 4, 48, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * .016))
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(crop, (ox, oy))
    return out


def sources(path):
    p = Path(path)
    if p.is_dir():
        for f in sorted(p.iterdir()):
            if f.suffix.lower() in ('.png', '.webp') and key_of(f.name):
                yield key_of(f.name), f.name, f.read_bytes()
    elif zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as zf:                                   # nur gelesen, nie ausgepackt (keine Pfad-Tricks)
            for info in sorted(zf.infolist(), key=lambda i: i.filename):
                name = Path(info.filename).name
                if info.is_dir() or name.startswith(('.', '_')) or Path(name).suffix.lower() not in ('.png', '.webp') or not key_of(name):
                    continue
                if info.file_size > 40 * 1024 * 1024:
                    print('uebersprungen (zu gross):', name)
                    continue
                yield key_of(name), name, zf.read(info)
    else:
        sys.exit('Weder ZIP noch Ordner: ' + str(p))


def update_manifest(keys):
    f = ROOT / 'www' / 'index.html'
    html = f.read_text(encoding='utf8')
    new, n = re.subn(r'const ART = new Set\(\[[^\]]*\]\);', 'const ART = new Set([%s]);' % ', '.join("'%s'" % k for k in keys), html, count=1)
    if n != 1:
        sys.exit('Manifest-Zeile "const ART = new Set([...]);" in www/index.html nicht gefunden')
    if new != html:
        f.write_text(new, encoding='utf8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('quelle')
    ap.add_argument('--size', type=int, default=256)
    ap.add_argument('--fill', type=float, default=0.84)
    a = ap.parse_args()
    out = ROOT / 'www' / 'art'
    out.mkdir(parents=True, exist_ok=True)
    done, total = [], 0
    for key, name, data in sources(a.quelle):
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
            sp = sprite(cutout(im), a.size, a.fill)
        except Exception as e:                                           # ein kaputtes Bild stoppt nicht den Rest
            print('FEHLER', name, '->', e)
            continue
        f = out / (key + '.webp')
        sp.save(f, 'WEBP', quality=85, alpha_quality=92, method=6)
        total += f.stat().st_size
        done.append(key)
        print('ok  %-26s -> art/%s.webp (%d KB)' % (name, key, f.stat().st_size // 1024))
    keys = sorted(p.stem for p in out.glob('*.webp'))
    update_manifest(keys)
    print('%d Bilder verarbeitet (%d KB), Manifest: %s' % (len(done), total // 1024, keys))


if __name__ == '__main__':
    main()
