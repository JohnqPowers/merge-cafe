#!/usr/bin/env python3
"""Manifest der ausgelieferten Bild-, Ton- und Schriftdateien: Pfad, Spielversion, SHA-256 und Quelle laut Verzeichnis.

Schreibt docs/herkunft/ausgelieferte_dateien.csv. Erfasst werden www/art, www/icons, www/ofl und assets/ (Icons, Startbild,
Schrift-Originale und ihre Lizenztexte). Quellen kommen aus
  docs/herkunft/bibliothek_113_dateien.csv      Verzeichnis des Eigentuemers (Stand 24.11.2026)
  docs/herkunft/pakete_dateiliste_sha256.csv    Inhalt der gelieferten Pakete (scripts/herkunft_pakete.py)
und, fuer die Katze, aus der Frame-Zuordnung `const CAT` in www/index.html.

Aufruf:  python3 -I scripts/asset_manifest.py             schreibt die Datei neu
         python3 -I scripts/asset_manifest.py --pruefen   vergleicht nur (Ausgang 1, wenn die Datei veraltet ist)
Nach jeder Aenderung an www/art, www/icons, www/ofl oder assets/ ausfuehren und die CSV mitcommitten.
Das Manifest ist ein technischer Nachweis (welche Datei, welche Pruefsumme, welche Quelle). Es ist keine Lizenz;
Einordnung und offene Punkte: docs/HERKUNFT_BILDER.md.
"""
import csv, hashlib, io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERK = ROOT / 'docs' / 'herkunft'
OUT = HERK / 'ausgelieferte_dateien.csv'
LIB = HERK / 'bibliothek_113_dateien.csv'
PAK = HERK / 'pakete_dateiliste_sha256.csv'
INDEX = ROOT / 'www' / 'index.html'
BEREICHE = ['www/art', 'www/icons', 'www/ofl', 'assets']
ENDUNGEN = {'.webp', '.png', '.wav', '.ttf', '.txt'}
SPALTEN = ['pfad', 'gruppe', 'bytes', 'sha256', 'pixel', 'version', 'herkunft', 'quelle', 'quelle_paket', 'quelle_sha256',
           'quelle_status', 'nachweis']
KATZENPAKET = 'Noas_Bean_Trail_Katze_Claude_Paket.zip'
KATZE_PRAEFIX = 'Noas_Bean_Trail_Cat_Integration/'
STADTPAKET = 'Noas_Bean_Trail_Stadtpaket_mit_Animationen_Claude.zip'      # Lieferung vom 25.11.2026: Kulissen b0..b8, Stadtrahmen frame1..frame8
STADT = ['hamburg', 'wien', 'paris', 'rom', 'istanbul', 'kyoto', 'new_york', 'rio', 'sternecafe']   # Welt 0..8 (Hamburg nutzt den Standardrahmen `frame`)

KI = 'KI-Bild (überwiegend OpenAI-Bildgenerierung nach Briefing; Erklärung des Eigentümers 24.11.2026), im Projekt aufbereitet'
KI_STADT = 'KI-Bild (OpenAI-Bildgenerierung laut Lieferung vom 25.11.2026; Rechte nicht zugesichert), im Projekt aufbereitet (oben auf 9:19,5 ergänzt, scripts/art_import.py)'
KI_MOEWE = 'KI-Bild (OpenAI-Bildgenerierung laut Lieferung vom 25.11.2026; Rechte nicht zugesichert), im Projekt aufbereitet (acht Flug-Frames zu einem Streifen, scripts/gull_import.py)'
KATZE = 'KI-Bild (Erklärung des Eigentümers 24.11.2026); Frames im Katzenpaket durch Skalierung, Drehung und Verschiebung abgeleitet, im Projekt aufbereitet'
ICON = 'KI-Bild des Eigentümers (Icon-Original), im Projekt abgeleitet (assets/src/build-icon.py)'
GRUPPEN = [  # (Muster auf den Pfad, Gruppe, Herkunft); die erste passende Zeile gilt
    (r'^www/art/k\d_s\d+\.webp$', 'Teil', KI),
    (r'^www/art/g\d+\.webp$', 'Automat', KI),
    (r'^www/art/a\d+\.webp$', 'Spielerfigur', KI),
    (r'^www/art/c\d+\.webp$', 'Gast', KI),
    (r'^www/art/f\d+\.webp$', 'Boden', KI),
    (r'^www/art/b\d+\.webp$', 'Hintergrund (Vollbild)', KI_STADT),
    (r'^www/art/frame\d*\.webp$', 'Brett-Rahmen', KI),
    (r'^www/art/e\d+\.webp$', 'Einzugs-Pose', KI),
    (r'^www/art/fx_[a-z0-9]+\.webp$', 'Effekt', KI),
    (r'^www/art/anim/moewe_[a-z0-9_]+\.webp$', 'Animation (Möwe)', KI_MOEWE),
    (r'^www/art/cat/c\d+\.webp$', 'Katze (Frame)', KATZE),
    (r'^www/art/cat/h\d+\.webp$', 'Katze (Herz)', KATZE),
    (r'^www/art/cat/purr\.wav$', 'Katze (Ton)', 'synthetischer Platzhalter-Ton aus dem Katzenpaket, im Projekt zur Schleife geschnitten'),
    (r'^www/icons/', 'Icon (Web)', ICON),
    (r'^assets/icon-(only|foreground|background)\.png$', 'Icon (Android)', ICON),
    (r'^assets/src/app-icon-original\.png$', 'Icon-Original', 'KI-Bild des Eigentümers (Verzeichnis: noas_bean_trail_icon_original_1254.png)'),
    (r'^assets/splash(-dark)?\.png$', 'Startbild', 'Herkunft nicht protokolliert (seit v1.4.0); Eigentümer bestätigt oder ersetzt'),
    (r'^assets/fonts/.*\.ttf$', 'Schrift (Original)', 'SIL OFL 1.1, Quelle: assets/fonts/QUELLE.md'),
    (r'-OFL\.txt$', 'Schrift-Lizenztext', 'SIL OFL 1.1'),
]

# Ergebnis der Nachstellung vom 24.11.2026: Die Pakete des Eigentuemers wurden mit den Skripten dieses Repos in einer Kopie
# neu eingelesen und Byte fuer Byte mit den ausgelieferten Dateien verglichen. Nur diese Schluessel gelten als nachgestellt.
# Bei neuen Lieferungen erneut pruefen und hier nachfuehren; alles andere bleibt ohne Nachweis (leer).
ART_NACHGESTELLT = re.compile(r'^(g[1-3]|k1_s[1-7]|k2_s[1-8]|k3_s[1-7]|a([1-9]|1[0-2])|c([1-9]|1[0-2])|f0|frame)$')
BODEN_NACHGESTELLT = re.compile(r'^f[23]$')
NACH_ART = 'bitgleich nachgestellt 24.11.2026 (scripts/art_import.py)'
NACH_BODEN = 'bitgleich nachgestellt 24.11.2026 (scripts/floor_prep.py, scripts/art_import.py)'
NACH_KATZE = 'bitgleich nachgestellt 24.11.2026 (scripts/cat_import.py)'
NACH_STADT = 'bitgleich nachgestellt 25.11.2026 (scripts/art_import.py aus dem ZIP, Kopie des Repos)'
NACH_MOEWE = 'bitgleich nachgestellt 25.11.2026 (scripts/gull_import.py aus dem ZIP, Kopie des Repos)'
NACH_ICON = 'bitgleich nachgestellt 24.11.2026 (assets/src/build-icon.py)'
NACH_F1 = 'Zuordnung nur nach Dateiname; ausgeliefertes f1.webp nicht bitgleich nachstellbar (vorläufiger Boden)'
NACH_HASH = 'Prüfsumme gleich Verzeichnis-Eintrag'

KEY = re.compile(r'^(g\d|k\d_s\d|[ace]\d{1,2}|f\d|frame\d?|fx_[a-z0-9]+)(?:[_.]|$)')   # wie in scripts/art_import.py
LIB_ORDNER = ('01_Game_Items/', '02_Characters/Gaeste/', '02_Characters/Cafe_Figuren/', '03_Backgrounds/', '04_Board_Frames/Original/')


def lesen_csv(pfad, enc='utf-8-sig'):
    with open(pfad, encoding=enc, newline='') as f:
        return list(csv.DictReader(f))


def spielversion():
    m = re.search(r"^\s*version:\s*'(\d+\.\d+\.\d+)'", INDEX.read_text(encoding='utf-8'), re.M)
    if not m:
        sys.exit('CONFIG.version in www/index.html nicht gefunden')
    return m.group(1)


def katzen_zuordnung():
    """Frame-Zuordnung der Katze aus `const CAT` (Feld map: Quellframe -> Bild) und Paketliste."""
    s = INDEX.read_text(encoding='utf-8')
    m = re.search(r'/\*CAT_DATA\*/(.*?)/\*END_CAT_DATA\*/', s, re.S)
    if not m:
        return {}
    cat = json.loads(m.group(1))
    paket = [r for r in lesen_csv(PAK, 'utf-8') if r['paket'] == KATZENPAKET]
    frames = sorted((r for r in paket if re.search(r'/sprites/cat_\d\d_[a-z]+\.png$', r['datei'])), key=lambda r: r['datei'])
    out = {}
    for i, name in enumerate(cat['files']):
        quellen = [frames[j] for j, mi in enumerate(cat['map']) if mi == i and j < len(frames)]
        out[f'www/art/cat/{name}.webp'] = quellen
    for n, name in enumerate(cat.get('hearts', []), 1):
        out[f'www/art/cat/{name}.webp'] = [r for r in paket if r['datei'].endswith(f'/effects/heart_{n}.png')]
    out['www/art/cat/purr.wav'] = [r for r in paket if re.search(r'/audio/purr_[^/]*\.wav$', r['datei'])][:1]
    return out


def stadtpaket_zuordnung():
    """Kulissen und Stadtrahmen der Lieferung vom 25.11.2026: Zieldatei -> Zeile der Paketliste (Quelle im ZIP)."""
    paket = {r['datei'].split('/', 1)[1]: r for r in lesen_csv(PAK, 'utf-8') if r['paket'] == STADTPAKET}
    out = {}
    for i, n in enumerate(STADT):
        out[f'www/art/b{i}.webp'] = paket.get(f'01_Neue_Stadtkulissen/PNG_Originale/bg_{n}_portrait.png')
        if i:
            out[f'www/art/frame{i}.webp'] = paket.get(f'02_Bestehende_Rahmen/frame_{n}.png')
    return {k: v for k, v in out.items() if v}


def moewe_zuordnung():
    """Möwen-Flugstreifen (Experiment exp/moewe-hamburg): Zieldatei -> die acht Flug-Frames der Lieferung vom 25.11.2026 (Zeilen der Paketliste)."""
    paket = [r for r in lesen_csv(PAK, 'utf-8') if r['paket'] == STADTPAKET]
    frames = sorted((r for r in paket if re.search(r'/07_Animationen_Optional/moewe/moewe_flug_\d\d\.png$', r['datei'])), key=lambda r: r['datei'])
    return {'www/art/anim/moewe_hamburg.webp': frames} if len(frames) == 8 else {}


def pixelmass(p):
    if p.suffix.lower() not in ('.webp', '.png'):
        return ''
    try:
        from PIL import Image
    except ImportError:
        sys.exit('Pillow fehlt (pip install pillow): Bildmaße lassen sich nicht lesen')
    with Image.open(p) as im:
        return f'{im.size[0]}x{im.size[1]}'


def dateien():
    for b in BEREICHE:
        for p in sorted((ROOT / b).rglob('*')):
            if p.is_file() and p.suffix.lower() in ENDUNGEN:
                yield p


def erzeugen():
    version = spielversion()
    lib = lesen_csv(LIB)
    lib_key = {}
    for r in lib:
        if r['Pfad'].startswith(LIB_ORDNER):
            m = KEY.match(Path(r['Pfad']).name)
            if m:
                lib_key.setdefault(m.group(1), r)
    icon_orig = next((r for r in lib if 'icon_original' in r['Pfad']), None)
    katze = katzen_zuordnung()
    stadt = stadtpaket_zuordnung()
    moewe = moewe_zuordnung()
    zeilen = []
    for p in dateien():
        rel = p.relative_to(ROOT).as_posix()
        daten = p.read_bytes()
        sha = hashlib.sha256(daten).hexdigest()
        gruppe, herkunft = 'unbekannt', 'nicht zugeordnet'
        for muster, g, h in GRUPPEN:
            if re.search(muster, rel):
                gruppe, herkunft = g, h
                break
        quelle = paket = qsha = qstatus = nachweis = ''
        stamm = p.stem
        if rel.startswith('www/art/cat/'):
            qs = katze.get(rel, [])
            if qs:
                quelle = ' + '.join(r['datei'].removeprefix(KATZE_PRAEFIX) for r in qs)
                qsha = ' + '.join(dict.fromkeys(r['sha256'] for r in qs))
                paket, qstatus, nachweis = KATZENPAKET, 'Katzenpaket (nicht im Verzeichnis des Eigentümers)', NACH_KATZE
        elif rel in moewe:
            qs = moewe[rel]
            quelle = ' + '.join(r['datei'].split('/', 1)[1] for r in qs)
            qsha = ' + '.join(dict.fromkeys(r['sha256'] for r in qs))
            paket = STADTPAKET
            qstatus = 'Stadtpaket 25.11.2026 (' + ('Prüfsummen im Verzeichnis des Eigentümers' if all(r['im_verzeichnis'] == 'ja' for r in qs) else 'nicht im Verzeichnis des Eigentümers') + ')'
            nachweis = NACH_MOEWE
        elif rel in stadt:
            r = stadt[rel]
            quelle, paket, qsha = r['datei'], r['paket'], r['sha256']
            qstatus = 'Stadtpaket 25.11.2026 (' + ('Prüfsumme im Verzeichnis des Eigentümers' if r['im_verzeichnis'] == 'ja' else 'nicht im Verzeichnis des Eigentümers') + ')'
            nachweis = NACH_STADT
        elif rel.startswith('www/art/') and stamm in lib_key:
            r = lib_key[stamm]
            quelle, paket, qsha, qstatus = r['Pfad'], r['Quelle'], r['SHA256'], r['Status']
            if stamm == 'f1':
                nachweis = NACH_F1
            elif BODEN_NACHGESTELLT.match(stamm):
                nachweis = NACH_BODEN
            elif ART_NACHGESTELLT.match(stamm):
                nachweis = NACH_ART
        elif gruppe in ('Icon (Web)', 'Icon (Android)', 'Icon-Original') and icon_orig:
            quelle, paket, qsha, qstatus = icon_orig['Pfad'], icon_orig['Quelle'], icon_orig['SHA256'], icon_orig['Status']
            nachweis = NACH_HASH if (gruppe == 'Icon-Original' and sha == qsha) else (NACH_ICON if gruppe != 'Icon-Original' else '')
        zeilen.append([rel, gruppe, len(daten), sha, pixelmass(p), version, herkunft, quelle, paket, qsha, qstatus, nachweis])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(SPALTEN)
    w.writerows(sorted(zeilen, key=lambda z: z[0]))
    return buf.getvalue(), zeilen


def main():
    pruefen = '--pruefen' in sys.argv[1:]
    text, zeilen = erzeugen()
    unbekannt = [z[0] for z in zeilen if z[1] == 'unbekannt']
    if unbekannt:
        print('Nicht zugeordnete Dateien (Gruppe in GRUPPEN ergänzen):', *unbekannt, sep='\n  ')
    if pruefen:
        alt = OUT.read_text(encoding='utf-8') if OUT.exists() else ''
        if alt != text or unbekannt:
            print('VERALTET: docs/herkunft/ausgelieferte_dateien.csv passt nicht zu den Dateien. Neu erzeugen mit: python3 -I scripts/asset_manifest.py')
            sys.exit(1)
        print(f'aktuell: {len(zeilen)} Dateien')
        return
    OUT.write_text(text, encoding='utf-8')
    ohne = sum(1 for z in zeilen if z[11] == '')
    print(f'{OUT.relative_to(ROOT)}: {len(zeilen)} Dateien (Version {zeilen[0][5] if zeilen else "?"}); ohne Nachweis-Vermerk: {ohne}')
    if unbekannt:
        sys.exit(1)


if __name__ == '__main__':
    main()
