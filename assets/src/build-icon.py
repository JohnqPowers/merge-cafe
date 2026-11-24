#!/usr/bin/env python3
"""Baut alle App-Icons aus dem Original `assets/src/app-icon-original.png`.

Aufruf aus dem Repo-Stamm:  python3 -I assets/src/build-icon.py
Benötigt: numpy, opencv-python, scipy.

Das Original ist ein abgerundetes Quadrat (Eckenradius ≈ 20 %) ohne Alpha; die Ecken (und ein schmaler Streifen
unten) sind einfarbig (Magenta oder Weiß). Die Außenfarbe wird an den Bildecken erkannt und der Außenbereich
mit einem weichen Farbverlauf gefüllt (vollflächige Fassung F),
damit Android, Apple und Google Play die Form selbst zuschneiden können. Daraus entstehen:

  assets/icon-only.png               1024  F vollflächig (Altgeräte, capacitor-assets)
  assets/icon-foreground.png         1024  F als 690-px-Quadrat mittig, Rest durchsichtig (adaptives Icon)
  assets/icon-background.png         1024  F mittig, Rand weich fortgesetzt (adaptives Icon)
  store/app-icon-512.png              512  vollflächig (Google Play rundet selbst)
  www/icons/icon-192.png / -512.png         vollflächig (Favicon, Apple-Touch-Icon, Web-Manifest)
  www/icons/icon-maskable-512.png     512  Kunst 84 %, Rand weich fortgesetzt (Sicherheitszone für Masken)

Maße für das adaptive Icon: capacitor-assets packt beide Ebenen mit 16,7 % Rand (`<inset>`, gelesen in
`res/mipmap-anydpi-v26/ic_launcher.xml` des Pakets, Build 19) in die 108-dp-Ebene. Das ganze 1024-px-Bild landet damit im 72-dp-Fenster,
das die Launcher zeigen; abgeschnitten wird nur an den Ecken durch die Maske. Mit 690 px Kunst (67 %) wirkte das Motiv auf dem Handy des
Eigentümers (Xiaomi HyperOS) zu klein, und der Rand war verwaschen (Rückmeldung 24.11.2026). 1.5.17: 810 px (79 %), Rest der Ebene ein
Goldverlauf in den Farben des Rahmens. 1.5.18: 930 px (91 %), gewählt nach einem Vergleich im Homescreen-Screenshot des Eigentümers
(810, 880, 930, 980 nebeneinander): Gesicht, Katze und Schriftzug sind größer, der goldene Rand der Kunst bleibt sichtbar.
Bei einer Kreismaske fallen nur die äußersten Ecken weg; Figuren, Katze, Tasse und Schriftzug bleiben ganz.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np
import cv2
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'assets' / 'src' / 'app-icon-original.png'
ADAPTIVE_ART = 930      # px der Kunst auf der 1024-px-Ebene (690 war zu klein, 810 in 1.5.17 noch zu klein; die Ebene fuellt auf dem Handy die ganze Kachel)
MASKABLE_ART = 0.84     # Anteil der Kunst auf der maskierbaren Leinwand


def load_rgb(p):
    return cv2.imread(str(p), cv2.IMREAD_COLOR)[:, :, ::-1].copy()


def save(rgb_or_rgba, rel, alpha=False):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    a = rgb_or_rgba
    if a.shape[2] == 3 and alpha:
        a = np.concatenate([a, np.full(a.shape[:2] + (1,), 255, np.uint8)], 2)
    code = cv2.COLOR_RGBA2BGRA if a.shape[2] == 4 else cv2.COLOR_RGB2BGR
    cv2.imwrite(str(p), cv2.cvtColor(a, code), [cv2.IMWRITE_PNG_COMPRESSION, 9])
    print('geschrieben', rel, a.shape[1], 'x', a.shape[0])


def resize(im, s):
    return cv2.resize(im, (s, s), interpolation=cv2.INTER_AREA if s < im.shape[0] else cv2.INTER_LANCZOS4)


def outside_mask(im):
    """Außenbereich: Pixel in der Farbe der Bildecken, die mit einer Bildecke zusammenhängen."""
    h, w = im.shape[:2]
    k = 6
    ref = np.median(np.concatenate([im[:k, :k].reshape(-1, 3), im[:k, -k:].reshape(-1, 3),
                                    im[-k:, :k].reshape(-1, 3), im[-k:, -k:].reshape(-1, 3)]), axis=0)
    near = np.abs(im.astype(int) - ref).max(axis=2) <= 32
    lab, _ = ndi.label(near)
    ids = {lab[0, 0], lab[0, w - 1], lab[h - 1, 0], lab[h - 1, w - 1]} - {0}
    return np.isin(lab, list(ids))


def fill_corners(im):
    """Außenbereich samt Anti-Aliasing-Saum durch einen weichen Farbverlauf aus dem Rand der Kunst ersetzen."""
    out = outside_mask(im)
    bad = cv2.dilate(out.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))) > 0
    good_in = cv2.erode((~bad).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
    _, (iy, ix) = ndi.distance_transform_edt(~good_in, return_indices=True)
    ext = cv2.GaussianBlur(im[iy, ix], (0, 0), 24)
    m = cv2.GaussianBlur(bad.astype(np.float32), (0, 0), 2.0)[..., None]
    res = (im * (1 - m) + ext * m).round().astype(np.uint8)
    res[bad] = ext[bad]
    return res


def frame_corners(F):
    """Mittlere Farbe des Rahmens nahe den vier Ecken der Kunst (oben links, oben rechts, unten links, unten rechts)."""
    h, k, o = F.shape[0], 18, 28
    med = lambda y, x: np.median(F[y:y + k, x:x + k].reshape(-1, 3), axis=0)
    return med(o, o), med(o, h - o - k), med(h - o - k, o), med(h - o - k, h - o - k)


def extended(F, canvas, art_px):
    """Kunst mittig auf der Leinwand, außen ein weicher Goldverlauf in den Farben des Rahmens (kein verwaschenes Spiegelbild der Szene)."""
    tl, tr, bl, br = frame_corners(F)
    u = np.linspace(0, 1, canvas)[None, :, None]
    v = np.linspace(0, 1, canvas)[:, None, None]
    grad = tl * (1 - u) * (1 - v) + tr * u * (1 - v) + bl * (1 - u) * v + br * u * v
    feather = max(4, canvas // 90)
    art = resize(F, art_px)
    pad = (canvas - art_px) // 2
    m = np.zeros((canvas, canvas), np.float32)
    m[pad:pad + art_px, pad:pad + art_px] = 1
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((feather, feather), np.uint8)), (0, 0), feather / 2)[..., None]
    full = np.zeros((canvas, canvas, 3), np.float32)
    full[pad:pad + art_px, pad:pad + art_px] = art
    return (full * m + grad * (1 - m)).round().astype(np.uint8)


def foreground(F, canvas, art_px):
    pad = (canvas - art_px) // 2
    out = np.zeros((canvas, canvas, 4), np.uint8)
    out[pad:pad + art_px, pad:pad + art_px, :3] = resize(F, art_px)
    out[pad:pad + art_px, pad:pad + art_px, 3] = 255
    return out


def main():
    F = fill_corners(load_rgb(SRC))
    save(resize(F, 1024), 'assets/icon-only.png')
    save(foreground(F, 1024, ADAPTIVE_ART), 'assets/icon-foreground.png', alpha=True)
    save(extended(F, 1024, ADAPTIVE_ART), 'assets/icon-background.png')
    save(resize(F, 512), 'store/app-icon-512.png', alpha=True)
    save(resize(F, 192), 'www/icons/icon-192.png', alpha=True)
    save(resize(F, 512), 'www/icons/icon-512.png', alpha=True)
    save(extended(F, 512, int(round(512 * MASKABLE_ART))), 'www/icons/icon-maskable-512.png', alpha=True)


if __name__ == '__main__':
    main()
