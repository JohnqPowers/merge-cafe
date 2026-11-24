#!/usr/bin/env python3
"""Bild-Import fuer Noa's Bean Trail.

Nimmt ein ZIP oder einen Ordner mit PNG/WebP-Dateien (Namen wie in docs/ART_BRIEF.md) und erzeugt daraus
einheitliche Sprites in www/art/<key>.webp. Drei Arten, erkannt am Dateinamen:
  - Teile/Automaten  g1_teekanne.png, k1_s2_espresso.png  -> quadratisch 256, Motiv 92 %, Kontaktschatten eingebacken
  - Figuren (Spieler) a1_baristina.png                     -> 208x208, Kachel einheitlich 176 px mit gleich abgerundeten Ecken;
                                                               Huete/Haare, die ueber die Kachel ragen, bleiben erhalten
  - Gaeste           c1_kapitaen_hein.png                  -> 240x270, Halbfigur steht unten buendig (Bildausschnitt bleibt wie gezeichnet)
  - Einzugs-Posen    e1_baristina.png                      -> 576x864, Ganzkoerper-Pose fuer den Einzug (ersetzt dort die Kachel)
  - Boden            f0_hamburg.png                        -> 1024x1024, deckend (Boden unter dem Brett, Stadt 0 = Hamburg ... f8)
  - Hintergrund      b2_paris.png                          -> Vollbild im Hochformat, deckend, Breite 720 (ersetzt gezeichnete Szene und Boden der Welt N = 0 ... 8)
  - Rahmen           frame.png                             -> Magenta (#FF00FF) aussen und im Fenster wird transparent; der Rahmen wird auf
                                                               das Brett-Verhaeltnis umgebaut (Ecken bleiben, Mittelstuecke werden gedehnt) und
                                                               bekommt einen weichen Schatten -> frame.webp. Masse stehen in FR_* und im CSS (#board).
  - Effekte          fx_puff.png, fx_star.png ...          -> 160x160, ohne Schatten (puff, star, drop, flame, leaf, ring, glow, excl)
Fuer alle: Freistellen (echte Transparenz wird uebernommen, sonst wird der einfarbige Hintergrund entfernt),
zuschneiden, einheitlich skalieren, als kleines WebP speichern und das Manifest `const ART = new Set([...])`
in www/index.html aktualisieren.

Aufruf:  python3 -I scripts/art_import.py <ZIP-oder-Ordner> [--size 256] [--fill 0.92]
Das Spiel faellt fuer alles ohne Bild automatisch auf Emoji bzw. die gezeichneten Figuren zurueck.
"""
import argparse, io, math, re, sys, zipfile
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
KEY = re.compile(r'^(g\d|k\d_s\d|[ace]\d{1,2}|[bf]\d|frame\d?|fx_[a-z0-9]+)(?:[_.]|$)')
AV_W = AV_H = 208                                                       # Figuren: Leinwand (Platz fuer Huete ueber der Kachel)
AV_TILE = 176                                                           # Kantenlaenge der Kachel auf der Leinwand
GU_W, GU_H = 240, 270                                                    # Gaeste: Seitenverhaeltnis wie die Vorlage (512x576)
PO_W, PO_H = 576, 864                                                    # Einzugs-Posen (Ganzkoerper, 2:3)
FX_S = 160                                                               # Effekt-Sprites
FLOOR_W = 1024                                                           # Boeden: Breite (quadratisch)
BG_W, BG_H_MAX = 720, 1600                                               # Hintergruende: Breite und hoechste Hoehe (Hochformat, 9:19,5 ergibt 720x1560)
FR_W, FR_T = 1000, 0.068                                                 # Rahmen: Aussenbreite (Referenz) und Dicke als Anteil der Breite
FR_H = round(FR_W * (1 - 2 * FR_T) * 8 / 7 + 2 * FR_W * FR_T)            # Fenster 7:8 -> Aussenhoehe (1123); CSS: aspect-ratio 1000/1123
FR_PAD = (30, 16, 30, 52)                                                # Schattenrand links, oben, rechts, unten (CSS: inset -3% -1.425% -4.63% -3%)


def key_of(name):
    m = KEY.match(Path(name).name.lower())
    return re.sub(r'^([ace])0+(\d)', r'\1\2', m.group(1)) if m else None     # a01 -> a1


def kind_of(key):
    if re.fullmatch(r'frame\d?', key):                                     # frame = Standard, frame<N> = eigener Rahmen der Welt N
        return 'frame'
    if key.startswith('fx_'):
        return 'fx'
    return {'a': 'avatar', 'b': 'bg', 'c': 'guest', 'e': 'pose', 'f': 'floor'}.get(key[0], 'item')


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


def portrait(im, w, h, fill, bottom):
    """Figur/Gast: zuschneiden, in w x h einpassen (ohne Schatten). bottom=True: Unterkante buendig (Tresen deckt sie ab)."""
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 12)
    if not len(xs):
        raise ValueError('Bild ist leer')
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = min(w * fill / crop.size[0], h * fill / crop.size[1])
    crop = crop.resize((max(1, round(crop.size[0] * k)), max(1, round(crop.size[1] * k))), Image.LANCZOS)
    cw, ch = crop.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.alpha_composite(crop, ((w - cw) // 2, h - ch if bottom else (h - ch) // 2))
    return out


def detect_tile(im):
    """Abgerundete Hintergrund-Kachel einer Figur finden: (x0, y0, x1, y1). Huete/Haare ueber dem Rand zaehlen nicht dazu.
    Gemessen wird nur dort, wo die runden Ecken (Radius ~18 %) nicht stoeren."""
    a = np.array(im.convert('RGBA'))[:, :, 3] > 128
    H, W = a.shape
    col = a[int(.30 * H):int(.80 * H)].mean(axis=0)                      # mittleres Band: links/rechts ohne Ecken
    xs = np.where(col > .9)[0]
    x0, x1 = int(xs.min()), int(xs.max())
    w = x1 - x0 + 1
    row = a[:, x0 + int(.2 * w):x1 - int(.2 * w)].mean(axis=1)           # mittlere Spalten: Unterkante ohne Ecken
    y1 = int(np.where(row > .9)[0].max())
    tops = []                                                            # Oberkante aus Streifen neben der Mitte (dort ragt selten ein Hut)
    for s, e in ((x0 + int(.2 * w), x0 + int(.4 * w)), (x1 - int(.4 * w), x1 - int(.2 * w))):
        for x in range(s, e):
            nz = np.where(a[:, x])[0]
            if len(nz):
                tops.append(nz.min())
    return x0, int(np.percentile(tops, 95)), x1, y1


def tile_avatar(im):
    """Figur auf eine einheitliche Kachel bringen: alle vier Ecken gleich rund (auch dort, wo das Bild die Kachel anschneidet),
    alle Kacheln gleich gross; Huete, Haare und Ohren ueber dem Kachelrand bleiben stehen."""
    im = im.convert('RGBA')
    x0, y0, x1, y1 = detect_tile(im)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if min(w, h) < 0.55 * min(im.size) or max(w, h) / min(w, h) > 1.35:
        raise ValueError('Kachel nicht erkannt')
    arr = np.array(im).astype(np.float32)
    H, W = arr.shape[:2]
    r = 0.18 * math.sqrt(w * h)                                          # wie die Ecken der Vorlagen (~18 %)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = xx + .5, yy + .5
    dx = np.maximum(np.maximum(x0 + r - px, px - (x1 + 1 - r)), 0)
    dy = np.maximum(np.maximum(y0 + r - py, py - (y1 + 1 - r)), 0)
    mask = np.clip(.5 - (np.sqrt(dx * dx + dy * dy) - r), 0, 1)
    inside = (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
    arr[:, :, 3] = np.where(inside, arr[:, :, 3] * mask, arr[:, :, 3])
    k = AV_TILE / math.sqrt(w * h)
    big = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((round(W * k), round(H * k)), Image.LANCZOS)
    ox = round(AV_W / 2 - (x0 + x1 + 1) / 2 * k)
    oy = round(AV_H - 4 - (y1 + 1) * k)
    return big.crop((-ox, -oy, AV_W - ox, AV_H - oy))                    # crop ausserhalb der Grenzen = transparent


def guest(im):
    """Gast: Bildausschnitt wie gezeichnet (Unterkante buendig), nur waagerecht mittig, wenn seitlich Luft ist."""
    im = im.convert('RGBA')
    a = np.array(im)[:, :, 3]
    ys, xs = np.where(a > 12)
    if not len(xs):
        raise ValueError('Bild ist leer')
    W, H = im.size
    k = min(GU_W / W, GU_H / H)
    big = im.resize((round(W * k), round(H * k)), Image.LANCZOS)
    left, right = xs.min() * k, (W - 1 - xs.max()) * k
    shift = round((right - left) / 2) if abs(right - left) > 3 else 0       # >0: Figur nach rechts ruecken (rechts ist mehr Luft)
    return big.crop((-shift, big.size[1] - GU_H, GU_W - shift, big.size[1]))


def key_magenta(im):
    """Magenta (#FF00FF) -> Transparenz, mit entmischter Kantenfarbe (kein rosa Saum). Gibt RGBA zurueck."""
    src = np.array(im.convert('RGB')).astype(np.float32)
    R, G, B = src[..., 0], src[..., 1], src[..., 2]
    m = np.clip((np.minimum(R, B) - G) / 255.0, 0, 1)                    # 1 = reines Magenta, <= 0 = Rahmenfarbe
    alpha = np.where(m > .9, 0, np.clip(1.0 - m * 1.12, 0, 1))
    col = np.clip((src - (1 - alpha)[..., None] * np.array([255, 0, 255], np.float32)) / np.maximum(alpha, 1e-3)[..., None], 0, 255)
    edge = (alpha > 0) & (alpha < .98)
    col[..., 2] = np.where(edge, np.minimum(col[..., 2], col[..., 1] + 20), col[..., 2])
    return Image.fromarray(np.dstack([col, alpha * 255]).astype(np.uint8))


def frame_asset(im):
    """Rahmen auf das Brett-Verhaeltnis umbauen: Ecken bleiben unveraendert (nur gleichmaessig skaliert), die glatten Mittelstuecke
    werden gedehnt, die kleinen Mittelbeschlaege bleiben unverzerrt. Dazu ein weicher Schatten. Ergebnis: Rahmen in FR_W x FR_H
    plus Schattenrand FR_PAD (links, oben, rechts, unten)."""
    k = key_magenta(im)
    a = np.array(k)[:, :, 3]
    ys, xs = np.where(a > 128)
    k = k.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    a = np.array(k)[:, :, 3]
    h, w = a.shape
    n, lab = cv2.connectedComponents((a <= 128).astype(np.uint8), connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    win = (a <= 128) & ~np.isin(lab, list(border))
    wy, wx = np.where(win)
    if not len(wx):
        raise ValueError('Rahmen hat kein Fenster (Magenta im Inneren fehlt)')
    t_src = (wx.min() + (w - 1 - wx.max()) + wy.min() + (h - 1 - wy.max())) / 4      # mittlere Dicke des Rahmenbands
    s = FR_W * FR_T / t_src
    S = k.resize((round(w * s), round(h * s)), Image.LANCZOS)
    sw, sh = S.size
    c = round(2.4 * t_src * s)                                          # Eckstueck (Beschlag samt Rand)
    keep = round(.58 * t_src * s)                                       # Mittelbeschlag: so viel bleibt unverzerrt
    out = Image.new('RGBA', (FR_W, FR_H), (0, 0, 0, 0))
    for (sx, sy, ox, oy) in ((0, 0, 0, 0), (sw - c, 0, FR_W - c, 0), (0, sh - c, 0, FR_H - c), (sw - c, sh - c, FR_W - c, FR_H - c)):
        out.alpha_composite(S.crop((sx, sy, sx + c, sy + c)), (ox, oy))
    def strip(box, size, pos):
        out.alpha_composite(S.crop(box).resize(size, Image.LANCZOS), pos)
    la = (FR_W - 2 * c - 2 * keep) // 2                                 # waagerechte Kanten: Planke | Beschlag | Planke
    lb = FR_W - 2 * c - 2 * keep - la
    lv = (FR_H - 2 * c - 2 * keep) // 2                                 # senkrechte Kanten
    lw = FR_H - 2 * c - 2 * keep - lv
    xm, ym = sw // 2, sh // 2
    for y0, y1, oy in ((0, c, 0), (sh - c, sh, FR_H - c)):               # oben, unten
        strip((c, y0, xm - keep, y1), (la, c), (c, oy))
        out.alpha_composite(S.crop((xm - keep, y0, xm + keep, y1)), (c + la, oy))
        strip((xm + keep, y0, sw - c, y1), (lb, c), (c + la + 2 * keep, oy))
    for x0, x1, ox in ((0, c, 0), (sw - c, sw, FR_W - c)):               # links, rechts
        strip((x0, c, x1, ym - keep), (c, lv), (ox, c))
        out.alpha_composite(S.crop((x0, ym - keep, x1, ym + keep)), (ox, c + lv))
        strip((x0, ym + keep, x1, sh - c), (c, lw), (ox, c + lv + 2 * keep))
    pl, pt, pr, pb = FR_PAD
    canvas = Image.new('RGBA', (FR_W + pl + pr, FR_H + pt + pb), (0, 0, 0, 0))
    al = out.getchannel('A')
    for blur, dy, op in ((7, 9, .55), (20, 24, .30)):                    # naher harter + weiter weicher Schatten
        sh_a = Image.new('L', canvas.size, 0)
        sh_a.paste(al, (pl, pt + dy))
        sh_a = sh_a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
        layer = Image.new('RGBA', canvas.size, (24, 8, 30, 0))
        layer.putalpha(sh_a)
        canvas.alpha_composite(layer)
    canvas.alpha_composite(out, (pl, pt))
    return canvas


def floor_asset(im):
    """Boden: auf FLOOR_W Breite (quadratisch wie geliefert). Deckend; nur wenn die Datei selbst Transparenz
    mitbringt (z. B. weich auslaufende Oberkante), bleibt sie erhalten und die gebaute Szene scheint durch."""
    has_a = im.mode in ('RGBA', 'LA', 'PA') and im.convert('RGBA').getchannel('A').getextrema()[0] < 255
    im = im.convert('RGBA' if has_a else 'RGB')
    k = FLOOR_W / im.size[0]
    return im.resize((FLOOR_W, round(im.size[1] * k)), Image.LANCZOS) if k < 1 else im


def bg_asset(im):
    """Vollbild-Hintergrund einer Welt: Hochformat, deckend (kein Alpha), auf BG_W Breite und hoechstens BG_H_MAX Hoehe verkleinert (nie vergroessert).
    Das Spiel legt das Bild mit object-fit: cover und Ausrichtung oben auf den ganzen Schirm."""
    im = im.convert('RGB')
    w, h = im.size
    if h < w * 1.4:
        raise ValueError('Hintergrund muss ein Hochformat sein (mindestens 1:1,4), z. B. 1080x2340')
    k = min(1.0, BG_W / w, BG_H_MAX / h)
    return im.resize((round(w * k), round(h * k)), Image.LANCZOS) if k < 1 else im


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
    global ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument('quelle')
    ap.add_argument('--size', type=int, default=256)
    ap.add_argument("--fill", type=float, default=0.92)
    ap.add_argument('--root', default=str(ROOT), help='nur zum Testen: anderer Projektordner')
    a = ap.parse_args()
    ROOT = Path(a.root)
    out = ROOT / 'www' / 'art'
    out.mkdir(parents=True, exist_ok=True)
    done, total = [], 0
    for key, name, data in sources(a.quelle):
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
            kd = kind_of(key)
            if kd == 'avatar':
                try:
                    sp = tile_avatar(cutout(im))
                except ValueError as e:                                  # ungewohntes Bild: einfach einpassen
                    print('Hinweis', name, '->', e, '(wird eingepasst)')
                    sp = portrait(cutout(im), AV_W, AV_H, 0.96, False)
            elif kd == 'guest':
                sp = guest(cutout(im))
            elif kd == 'pose':
                sp = portrait(cutout(im), PO_W, PO_H, 0.96, False)
            elif kd == 'fx':
                sp = portrait(cutout(im), FX_S, FX_S, 0.96, False)
            elif kd == 'floor':
                sp = floor_asset(im)
            elif kd == 'bg':
                sp = bg_asset(im)
            elif kd == 'frame':
                sp = frame_asset(im)
            else:
                sp = sprite(cutout(im), a.size, a.fill)
        except Exception as e:                                           # ein kaputtes Bild stoppt nicht den Rest
            print('FEHLER', name, '->', e)
            continue
        f = out / (key + '.webp')
        sp.save(f, 'WEBP', quality=84 if kd == 'bg' else 86 if kd in ('floor', 'frame') else 85, alpha_quality=95 if kd == 'frame' else 92, method=6)
        total += f.stat().st_size
        done.append(key)
        print('ok  %-26s -> art/%s.webp (%d KB)' % (name, key, f.stat().st_size // 1024))
    keys = sorted(p.stem for p in out.glob('*.webp'))
    update_manifest(keys)
    print('%d Bilder verarbeitet (%d KB), Manifest: %s' % (len(done), total // 1024, keys))


if __name__ == '__main__':
    main()
