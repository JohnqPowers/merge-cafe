"""Herkunftsnachweise für Bilder, Töne und Schriften (docs/HERKUNFT_BILDER.md, docs/herkunft/, scripts/asset_manifest.py).
Braucht keinen Browser, nur Pillow. Geprüft wird, dass das Manifest der ausgelieferten Dateien zu den Dateien passt, dass die
Verzeichnisse vollständig und in sich stimmig sind und dass im öffentlichen Repo keine Namen anderer Spiele oder Marken stehen.
Die Negativliste ist bewusst klein und ersetzt die Sichtprüfung nicht.
Aufruf: python3 -I tests/test_herkunft.py"""
import csv, hashlib, os, re, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
HERK = os.path.join(ROOT, 'docs', 'herkunft')
FAILS = []


def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (f' | {info}' if info != '' else ''))
    if not cond:
        FAILS.append(name)


def lesen(name, enc='utf-8'):
    with open(os.path.join(HERK, name), encoding=enc, newline='') as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------ Manifest der ausgelieferten Dateien
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'scripts', 'asset_manifest.py'), '--pruefen'], capture_output=True, text=True, cwd=ROOT)
ok('Manifest ausgelieferte_dateien.csv ist aktuell (scripts/asset_manifest.py --pruefen)', r.returncode == 0, (r.stdout + r.stderr).strip()[:160])
man = lesen('ausgelieferte_dateien.csv')
version = re.search(r"^\s*version:\s*'(\d+\.\d+\.\d+)'", open(os.path.join(ROOT, 'www', 'index.html'), encoding='utf-8').read(), re.M).group(1)
ok('Manifest trägt die aktuelle Spielversion', {z['version'] for z in man} == {version}, version)
ok('jede Datei in www/art und www/icons steht im Manifest',
   all(os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/') in {z['pfad'] for z in man}
       for b in ('www/art', 'www/icons') for d, _, fs in os.walk(os.path.join(ROOT, b)) for f in fs if f.lower().endswith(('.webp', '.png', '.wav'))))
ok('keine Datei ohne Gruppe', not [z['pfad'] for z in man if z['gruppe'] == 'unbekannt'])
ok('SHA-256 im Manifest: 64 Hexzeichen, jeder Pfad nur einmal', all(re.fullmatch(r'[0-9a-f]{64}', z['sha256']) for z in man) and len({z['pfad'] for z in man}) == len(man))
ok('Bytes und Prüfsumme stimmen mit der Datei überein (Stichprobe: alle)',
   all(os.path.getsize(os.path.join(ROOT, z['pfad'])) == int(z['bytes']) and hashlib.sha256(open(os.path.join(ROOT, z['pfad']), 'rb').read()).hexdigest() == z['sha256'] for z in man))
bilder = [z for z in man if z['gruppe'] in ('Teil', 'Automat', 'Spielerfigur', 'Gast', 'Boden', 'Brett-Rahmen', 'Katze (Frame)', 'Katze (Herz)')]
ok('jedes Spielbild hat eine Quelle laut Verzeichnis oder Paket', all(z['quelle'] and z['quelle_sha256'] for z in bilder), len(bilder))
ok('Nachweis: jedes Spielbild außer dem vorläufigen Boden f1 ist als nachgestellt vermerkt',
   all(z['nachweis'].startswith('bitgleich nachgestellt') for z in bilder if not z['pfad'].endswith('/f1.webp')))

# ------------------------------------------------------------ Verzeichnis des Eigentümers und Paketlisten
lib = lesen('bibliothek_113_dateien.csv', 'utf-8-sig')
ok('Verzeichnis des Eigentümers: 113 Einträge, Spalten wie geliefert', len(lib) == 113 and list(lib[0].keys()) == ['Pfad', 'Quelle', 'Status', 'Hinweise', 'Bytes', 'SHA256', 'Pixel', 'Modus'])
ok('Verzeichnis: SHA-256 gültig und eindeutig', all(re.fullmatch(r'[0-9a-f]{64}', z['SHA256']) for z in lib) and len({z['SHA256'] for z in lib}) == 113)
pak = lesen('pakete_dateiliste_sha256.csv')
libh = {z['SHA256'] for z in lib}
ok('Paketlisten: Spalten, gültige SHA-256, „im_verzeichnis“ passt zum Verzeichnis',
   list(pak[0].keys()) == ['paket', 'datei', 'bytes', 'sha256', 'im_verzeichnis', 'eingetragen']
   and all(re.fullmatch(r'[0-9a-f]{64}', z['sha256']) and (z['sha256'] in libh) == (z['im_verzeichnis'] == 'ja') for z in pak), len(pak))
ok('Paketlisten: Katzenpaket mit 33 Dateien erfasst', sum(1 for z in pak if z['paket'] == 'Noas_Bean_Trail_Katze_Claude_Paket.zip') == 33)
ok('altes Icon-Original (24.11.2026, im Spiel bis 1.5.20) hat dieselbe Prüfsumme wie der Verzeichnis-Eintrag',
   hashlib.sha256(open(os.path.join(ROOT, 'assets', 'src', 'app-icon-original-2026-11-24.png'), 'rb').read()).hexdigest() in libh)
icon_neu = hashlib.sha256(open(os.path.join(ROOT, 'assets', 'src', 'app-icon-original.png'), 'rb').read()).hexdigest()
ok('aktuelles Icon-Original (Lieferung 28.11.2026) steht als Einzeldatei in der Paketliste und ist nicht im Verzeichnis',
   icon_neu not in libh and any(z['sha256'] == icon_neu and z['paket'] == 'Einzeldatei (Upload)' and z['im_verzeichnis'] == 'nein' for z in pak))
ok('Erklärung des Eigentümers liegt im Repo', os.path.getsize(os.path.join(HERK, 'Bildherkunft_Erklaerung_2026-11-24.pdf')) > 1000)

# ------------------------------------------------------------ Dokument und öffentliche Dateien
doc = open(os.path.join(ROOT, 'docs', 'HERKUNFT_BILDER.md'), encoding='utf-8').read()
ok('Dokument sagt klar: keine Lizenz, keine lückenlose Kette, nicht behaupten',
   'keine Lizenz' in doc and 'Eine lückenlose' in doc and '**Nicht behaupten**' in doc)
FREMD = ['candy crush', 'gardenscapes', 'homescapes', 'merge mansion', 'merge dragons', 'cooking diary', 'cooking fever', 'cafeland',
         'coffee craze', 'tasty town', 'hay day', 'playrix', 'zynga', 'supercell', 'king.com', 'wooga', 'starbucks', 'nespresso']
texte = {n: open(os.path.join(ROOT, n), encoding='utf-8-sig').read().lower()
         for n in ('docs/HERKUNFT_BILDER.md', 'docs/herkunft/README.md', 'docs/herkunft/bibliothek_113_dateien.csv',
                   'docs/herkunft/pakete_dateiliste_sha256.csv', 'docs/herkunft/ausgelieferte_dateien.csv', 'docs/ASSETS_LIZENZEN.md')}
treffer = [(n, w) for n, t in texte.items() for w in FREMD if w in t]
ok('keine Namen anderer Spiele oder Marken in den Herkunftsdateien', not treffer, treffer)

print(f'\nERGEBNIS: {"ALLE bestanden" if not FAILS else str(len(FAILS)) + " FEHLER: " + ", ".join(FAILS)}')
sys.exit(1 if FAILS else 0)
