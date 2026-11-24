"""Entwurf-Böden mit dunklem Rand säubern, bevor sie in `art_import.py` gehen.

Für Lieferungen, die nicht dem Art-Brief entsprechen (abgerundete Ecken, dunkler Rand, Himmel oben):
  1. schneidet das Inhaltsfeld zu (Rand und Himmel gehen weg),
  2. füllt Rest-Ecken des Randes (Inpainting),
  3. lässt die Oberkante weich auslaufen (Alpha), damit der gebaute Boden der Szene durchscheint,
  4. schärft auf Wunsch leicht nach (Entwürfe sind oft hochskaliert und weich).

Aufruf (Maße vorher am Bild ablesen, Zuschnitt möglichst quadratisch):
  python3 -I scripts/floor_prep.py <quelle.png> <x0> <y0> <x1> <y1> <auslauf> <ziel.png> [schaerfe]
  auslauf  = Anteil der Bildhöhe oben, der ausläuft (z. B. 0.13); schaerfe = z. B. 0.6
Beispiele (Stand 24.11.): Paris `40 74 990 1024 0.13 … 0.6`, Rom `9 77 947 1015 0.13 … 0.6`.
Danach `python3 -I scripts/art_import.py <Ordner mit f2_paris.png …>`. Saubere Lieferungen brauchen das nicht."""
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi


def prep(src, box, auslauf, schaerfe=0.0):
    im = Image.open(src).convert('RGB').crop(box)
    a = np.array(im)
    h, w = a.shape[:2]
    dunkel = (a.max(axis=2) < 70) & (a[:, :, 2] >= a[:, :, 0] - 6)          # dunkelblauer Rand der Rundungen
    zone = np.zeros_like(dunkel)
    r = 70
    for ys in (slice(0, r), slice(h - r, h)):
        for xs in (slice(0, r), slice(w - r, w)):
            zone[ys, xs] = True
    lab, n = ndi.label(dunkel & zone)
    ecke = np.zeros_like(dunkel)
    for i in range(1, n + 1):                                               # nur Flecken, die wirklich in einer Bildecke sitzen
        ys, xs = np.where(lab == i)
        if ((ys < 6) | (ys > h - 7)).any() and ((xs < 6) | (xs > w - 7)).any():
            ecke |= lab == i
    maske = ndi.binary_dilation(ecke, iterations=3).astype(np.uint8) * 255
    bgr = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), maske, 7, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    if schaerfe > 0:
        out = out.filter(ImageFilter.UnsharpMask(radius=2.0, percent=int(schaerfe * 100), threshold=2))
    if out.size[0] > 1024:
        out = out.resize((1024, round(out.size[1] * 1024 / out.size[0])), Image.LANCZOS)
    t = np.clip(np.arange(out.size[1], dtype=float) / (out.size[1] * auslauf), 0, 1)
    t = t * t * (3 - 2 * t)                                                 # weicher Auslauf
    alpha = np.tile((t * 255).astype(np.uint8)[:, None], (1, out.size[0]))
    rgba = out.convert('RGBA')
    rgba.putalpha(Image.fromarray(alpha))
    return rgba, int(ecke.sum())


if __name__ == '__main__':
    if len(sys.argv) < 8:
        sys.exit(__doc__)
    quelle, ziel = sys.argv[1], sys.argv[7]
    x0, y0, x1, y1 = map(int, sys.argv[2:6])
    bild, ecken = prep(quelle, (x0, y0, x1, y1), float(sys.argv[6]), float(sys.argv[8]) if len(sys.argv) > 8 else 0.0)
    bild.save(ziel)
    print(f'{ziel}: {bild.size[0]}x{bild.size[1]}, Eckflecken gefüllt: {ecken} px')
