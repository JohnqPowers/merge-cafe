#!/usr/bin/env python3
"""Startbild (erste Seite) für Noa's Bean Trail.

Nimmt das Bild des Eigentümers (Chat-Lieferung 28.11.2026, 941x1672, im Repo als assets/src/start-original.png) und baut daraus
  www/art/start.webp        (1220 px breit, ohne die eingebackene Versionsnummer, mit Lanczos vergrößert und leicht nachgeschärft)
und schreibt die Tabelle `const START` in www/index.html zwischen die Marken /*START_DATA*/ und /*END_START_DATA*/:
Dateiname, Bildmaße, Höhe des eigentlichen Bildes ohne Verlängerung, Lage des „Spielen“-Knopfs (Anteile des Bildes in Prozent), Lage der Versionszeile
und der Willkommenszeile (Bildpunkte der Ausgabe).

Warum die Versionsnummer weg muss: Im Bild steht „v1.5.21“ fest eingebrannt. Sie würde bei jedem Update falsch. Das Skript füllt die Stelle
mit dem Farbverlauf der Umgebung (je Spalte zwischen der Zeile darüber und der darunter, mit gleichem Bildkorn); die beiden Zierlinien links
und rechts bleiben stehen. Die echte Nummer setzt das Spiel als Text darüber (www/index.html, Startbild-Einbau).

Verlängerung unten: An sehr hohen Handys (9:20 und höher) würde das Bild links und rechts so stark beschnitten, dass der Satz „Dein eigenes Café
wartet auf dich!“ am Rand abgeschnitten wäre. Darum bekommt das Bild unten EXT Zeilen dazu (die untersten Zeilen gespiegelt, nach unten zunehmend
verwischt, die Zierlinien in der Spiegelung getilgt). Das Spiel richtet das Bild oben aus und beschneidet bei breiteren Fenstern unten wieder, dann
ist es genau das Originalbild.

Das Startbild ist ein Experiment (Branch exp/startbild, Schalter CONFIG.features.startImg); ohne die Datei zeigt das Spiel das alte Startbild.

Aufruf:  python3 -I scripts/start_import.py [QUELLE.png] [--root PFAD] [--quality 88]
         Standard-Quelle: assets/src/start-original.png.  --root: anderes Arbeitsverzeichnis (z. B. eine Kopie des Repos,
         um die Datei bitgleich nachzustellen)
"""
import argparse, json, re, sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
QUELLE_MASS = (941, 1672)
AUSGABE = 'start.webp'
W_OUT = 1220                               # Breite der Ausgabe (wie die Kulissen, scripts/art_import.py BG_W)
SCHARF = dict(radius=1.4, percent=60, threshold=2)
# Lagen im Original (Bildpunkte, x0 y0 x1 y1 ohne die letzte Zeile/Spalte)
KNOPF = (140, 1287, 797, 1486)            # „Spielen“-Knopf: Außenkante der hellen Umrandung bis Unterkante des dunklen Randes
EXT = 170                                 # Verlängerung unten (Zeilen im Original)
ZIERLINIEN = [(284, 1574, 404, 1595), (538, 1574, 658, 1595)]   # die beiden Zierlinien neben der Versionszeile (x0 y0 x1 y1), in der Spiegelung zu tilgen
VERSION_TILGEN = (410, 1560, 531, 1606)   # eingebrannte „v1.5.21“ samt Schatten (Ziffern x 423..517, y 1569..1596); die Zierlinien enden bei x 397 und beginnen bei x 544
VERSION_MITTE_X = 470.5                   # Mitte der Versionszeile
VERSION_GRUNDLINIE = 1594                 # Unterkante der Ziffern
VERSION_ZIFFERN = 24                      # Höhe der Ziffern
WILLKOMMEN = (470.5, 1540, 28, 560)       # Zeile für wiederkehrende Spieler: Mitte x, Grundlinie y, Schrifthöhe, größte Breite (alles im Original)


def tilgen(a, box):
    """Füllt die Fläche `box` (x0, y0, x1, y1) mit dem Verlauf der Umgebung: je Spalte linear zwischen drei Zeilen darüber und drei darunter
    (waagerecht leicht geglättet), dazu Bildkorn mit der Streuung der Umgebung (feste Saat, damit das Ergebnis bitgleich bleibt)."""
    x0, y0, x1, y1 = box
    f = a.astype(np.float32)
    def ref(zeilen):
        m = np.median(f[zeilen[0]:zeilen[1], x0 - 6:x1 + 6], axis=0)
        return cv2.blur(m[None], (9, 1))[0][6:-6]
    oben, unten = ref((y0 - 4, y0 - 1)), ref((y1 + 1, y1 + 4))
    h = y1 - y0
    t = ((np.arange(h, dtype=np.float32) + 0.5 + 2.5) / (h + 5.0))[:, None, None]       # Lage zwischen den Bezugszeilen (die liegen 2,5 Zeilen außerhalb)
    fuell = oben[None] * (1 - t) + unten[None] * t
    streifen = f[y0 - 16:y0 - 3, x0:x1]
    sigma = (streifen - cv2.GaussianBlur(streifen, (0, 0), 1.5)).reshape(-1, 3).std(axis=0)
    fuell = fuell + np.random.default_rng(7).normal(0.0, 1.0, fuell.shape).astype(np.float32) * sigma
    # weicher Rand (3 Bildpunkte), damit keine Kante entsteht
    w = x1 - x0
    dx = np.minimum(np.arange(w) + 1, w - np.arange(w))[None, :]
    dy = np.minimum(np.arange(h) + 1, h - np.arange(h))[:, None]
    al = np.clip(np.minimum(dx, dy) / 3.0, 0, 1)[:, :, None].astype(np.float32)
    f[y0:y1, x0:x1] = fuell * al + f[y0:y1, x0:x1] * (1 - al)
    return np.clip(f + 0.5, 0, 255).astype(np.uint8)


def verlaengern(a, ext):
    """Hängt unten `ext` Zeilen an: die untersten Zeilen gespiegelt (Übergang ohne Kante), die Zierlinien der Spiegelung getilgt, nach unten zunehmend verwischt."""
    h = a.shape[0]
    sp = np.ascontiguousarray(a[h - ext:][::-1])
    for x0, y0, x1, y1 in ZIERLINIEN:
        sp = tilgen(sp, (x0, h - y1, x1, h - y0))
    f = sp.astype(np.float32)
    weich = cv2.GaussianBlur(f, (0, 0), 14)
    w = np.linspace(0.0, 0.85, ext, dtype=np.float32)[:, None, None]
    return np.concatenate([a, np.clip(f * (1 - w) + weich * w + 0.5, 0, 255).astype(np.uint8)], axis=0)


def bauen(quelle):
    im = Image.open(quelle).convert('RGB')
    if im.size != QUELLE_MASS:
        sys.exit(f'Das Skript ist für ein Bild von {QUELLE_MASS[0]}x{QUELLE_MASS[1]} gebaut, die Datei hat {im.size[0]}x{im.size[1]}.')
    a = tilgen(np.asarray(im), VERSION_TILGEN)
    w, h = QUELLE_MASS
    a = verlaengern(a, EXT)
    hg = h + EXT                                           # Höhe mit Verlängerung (Original)
    h_out = round(W_OUT * hg / w)
    sx, sy = W_OUT / w, h_out / hg
    gross = Image.fromarray(a).resize((W_OUT, h_out), Image.LANCZOS).filter(ImageFilter.UnsharpMask(**SCHARF))
    x0, y0, x1, y1 = KNOPF
    wx, wy, wsize, wbreit = WILLKOMMEN
    daten = {
        'v': 2, 'file': 'art/' + AUSGABE, 'w': W_OUT, 'h': h_out, 'art': round(h * sy, 1),        # art = Höhe des eigentlichen Bildes ohne die Verlängerung
        'btn': [round(100 * x0 / w, 3), round(100 * y0 / hg, 3), round(100 * (x1 - x0) / w, 3), round(100 * (y1 - y0) / hg, 3)],   # links, oben, Breite, Höhe in % des ganzen Bildes
        'ver': [round(VERSION_MITTE_X * sx, 1), round(VERSION_GRUNDLINIE * sy, 1), round(VERSION_ZIFFERN * sy, 1)],            # Mitte x, Grundlinie y, Ziffernhöhe (Bildpunkte der Ausgabe)
        'wel': [round(wx * sx, 1), round(wy * sy, 1), round(wsize * sy, 1), round(wbreit * sx, 1)],                            # Mitte x, Grundlinie y, Schrifthöhe, größte Breite
    }
    return gross, daten


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('quelle', nargs='?', help='PNG des Startbilds (Standard: assets/src/start-original.png)')
    ap.add_argument('--root', default=str(ROOT), help='Arbeitsverzeichnis (Standard: dieses Repo)')
    ap.add_argument('--quality', type=int, default=88)
    o = ap.parse_args()
    root = Path(o.root)
    quelle = Path(o.quelle) if o.quelle else root / 'assets' / 'src' / 'start-original.png'
    if not quelle.is_file():
        sys.exit(f'Quelle fehlt: {quelle}')
    bild, daten = bauen(quelle)
    ziel = root / 'www' / 'art' / AUSGABE
    ziel.parent.mkdir(parents=True, exist_ok=True)
    bild.save(ziel, 'WEBP', quality=o.quality, method=6)
    idx = root / 'www' / 'index.html'
    s = idx.read_text(encoding='utf-8')
    neu, n = re.subn(r'/\*START_DATA\*/.*?/\*END_START_DATA\*/', lambda m: '/*START_DATA*/' + json.dumps(daten, separators=(',', ':')) + '/*END_START_DATA*/', s, flags=re.S)
    if n != 1:
        sys.exit('Marken /*START_DATA*/ … /*END_START_DATA*/ in www/index.html nicht gefunden (genau einmal erwartet)')
    if neu != s:
        idx.write_text(neu, encoding='utf-8')
    print(f'{ziel.relative_to(root)}: {daten["w"]}x{daten["h"]}, {ziel.stat().st_size // 1024} KB; Knopf {daten["btn"]}; Version {daten["ver"]}')


if __name__ == '__main__':
    main()
