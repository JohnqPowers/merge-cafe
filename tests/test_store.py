"""Store-Unterlagen: Zeichenlängen und Regeln der Texte (docs/STORE_LISTING.md), Bildformate in store/, Zahlen im Text gegen den Code.
Braucht keinen Browser. Die Grenzen stammen aus den Play-Hilfeseiten (Quellen im Dokument): Titel 30, Kurzbeschreibung 80, Beschreibung 4000,
Alt-Text 140 Zeichen; Icon 512x512 32-Bit-PNG bis 1024 KB; Feature-Grafik 1024x500 ohne Alpha; Screenshots 2 bis 8, 320 bis 3840 px je Seite,
lange Seite höchstens 2,3-mal die kurze, höchstens 8 MB, ohne Alpha.
Die Negativliste für Fremdnamen ist bewusst klein und ersetzt die Sichtprüfung nicht.
Aufruf: python3 -I tests/test_store.py"""
import filecmp, os, re, sys
from PIL import Image, ImageChops, ImageStat

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
WWW, STORE = os.path.join(ROOT, 'www'), os.path.join(ROOT, 'store')
FAILS = []


def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (f' | {info}' if info != '' else ''))
    if not cond:
        FAILS.append(name)


doc = open(os.path.join(ROOT, 'docs', 'STORE_LISTING.md'), encoding='utf-8').read()
src = open(os.path.join(WWW, 'index.html'), encoding='utf-8').read()

# ---------------------------------------------------------------- Texte lesen
def section(titel_teil):
    m = re.search(r'^## [^\n]*' + titel_teil + r'[^\n]*\n(.*?)(?=^## |\Z)', doc, re.S | re.M)
    return m.group(1) if m else ''

def feld(text, label):
    m = re.search(r'\*\*' + label + r'[^*]*\*\*\s*(.+)', text)
    return m.group(1).strip() if m else ''

def block(text):
    m = re.search(r'```text\n(.*?)```', text, re.S)
    return m.group(1).strip() if m else ''

TEXT = {
    'de': {'titel': feld(section('Texte Deutsch'), 'App-Name'), 'kurz': feld(section('Texte Deutsch'), 'Kurzbeschreibung'),
           'lang': block(section('Texte Deutsch')), 'neu': feld(section('Was ist neu'), 'Deutsch:')},
    'en': {'titel': feld(section('Texte Englisch'), 'App name'), 'kurz': feld(section('Texte Englisch'), 'Short description'),
           'lang': block(section('Texte Englisch')), 'neu': feld(section('Was ist neu'), 'English:')},
}

# ---------------------------------------------------------------- Zahlen und Namen aus dem Code
chains = src[src.index('const CHAINS = ['):src.index('const CHAPTERS')]
n_items = sum(len(re.findall(r"'[^']*'", m)) for m in re.findall(r"items:\[([^\]]*)\]", chains))
n_ketten = chains.count("gen:'")
gens = re.findall(r"genName:\{de:'([^']*)',en:'([^']*)'\}", chains)
chap = src[src.index('const CHAPTERS = ['):src.index('const RANKS')]
n_welten = len(re.findall(r'\{ lv:', chap))
welt_de = re.findall(r"de:'([^']*)', st:", chap)
welt_en = re.findall(r"en:'([^']*)', co:", chap)
n_figuren = len([f for f in os.listdir(os.path.join(WWW, 'art')) if re.fullmatch(r'a\d+\.webp', f)])
n_tage = re.search(r'const DAILY = \[(.*?)\];', src).group(1).count('{')
app_name = re.search(r'const APP_NAME = "([^"]+)"', src).group(1)
version = re.search(r"version:\s*'([^']+)'", src).group(1)
print(f'Code: {n_items} Teile in {n_ketten} Ketten, {n_welten} Welten, {n_figuren} Figuren, {n_tage} Bonus-Tage, Name "{app_name}", Version {version}')

PROMO = re.compile(r'\b(kostenlos|gratis|free|beste[rsn]?|best|top|neu|new|sale|rabatt|discount|million\w*)\b|#\s*1\b|nr\.\s*1', re.I)
FREMD = ['gardenscapes', 'homescapes', 'merge mansion', 'merge dragons', 'candy crush', 'cooking diary', 'cooking fever', 'cafeland', 'coffee craze',
         'tasty town', 'hay day', 'township', 'playrix', 'zynga', 'supercell', 'king.com', 'wooga', 'starbucks', 'nespresso', 'lavazza', 'mcdonald',
         'disney', 'nintendo', 'pokemon', 'pokémon', 'coca-cola', 'red bull',
         'merge café', 'merge cafe', 'coffeeshop', 'coffee shop']        # letzte Zeile: alte eigene Namen, nicht mehr verwenden
EMOJI = lambda s: sum(1 for c in s if 0x1F000 <= ord(c) <= 0x1FFFF or c == '☕')

for lang, grenze_namen in (('de', 'Deutsch'), ('en', 'Englisch')):
    T = TEXT[lang]
    ok(f'{lang} Titel, Kurzbeschreibung, Beschreibung, Neuerungen gefunden', all(T.values()), {k: len(v) for k, v in T.items()})
    ok(f'{lang} Titel höchstens 30 Zeichen', 0 < len(T['titel']) <= 30, len(T['titel']))
    ok(f'{lang} Kurzbeschreibung höchstens 80 Zeichen', 0 < len(T['kurz']) <= 80, len(T['kurz']))
    ok(f'{lang} Beschreibung höchstens 4000 Zeichen', 0 < len(T['lang']) <= 4000, len(T['lang']))
    ok(f'{lang} Neuerungen höchstens 500 Zeichen', 0 < len(T['neu']) <= 500, len(T['neu']))
    ok(f'{lang} Titel beginnt mit dem Spielnamen aus dem Code', T['titel'].startswith(app_name), (T['titel'], app_name))
    ok(f'{lang} Titel nur Buchstaben, Leerzeichen, Apostroph, Doppelpunkt, Bindestrich (keine Emojis, keine Sonderzeichen-Ketten)',
       re.fullmatch(r"[A-Za-zÄÖÜäöüß' :\-]+", T['titel']) is not None, T['titel'])
    ok(f'{lang} Titel und Kurzbeschreibung ohne Werbewörter (kostenlos, beste, neu, #1 …)', not PROMO.search(T['titel'] + ' ' + T['kurz']),
       PROMO.search(T['titel'] + ' ' + T['kurz']).group(0) if PROMO.search(T['titel'] + ' ' + T['kurz']) else '')
    ok(f'{lang} Titel und Kurzbeschreibung ohne Wörter in Großbuchstaben',
       not [w for w in re.findall(r'[A-Za-zÄÖÜ]{4,}', T['titel'] + ' ' + T['kurz']) if w.isupper()])
    ok(f'{lang} Beschreibung ohne Platzhalter und mit höchstens 4 Emojis', '[[' not in T['lang'] and EMOJI(T['lang']) <= 4, EMOJI(T['lang']))
    alles = ' '.join(T.values()).lower()
    treffer = [n for n in FREMD if n in alles]
    ok(f'{lang} keine Fremdnamen und keine alten eigenen Namen in den Texten', not treffer, treffer)

de, en = TEXT['de']['lang'], TEXT['en']['lang']
def zahl(muster, text):
    m = re.search(muster, text)
    return tuple(int(x) for x in m.groups()) if m else None

ok('de „N Leckereien in M Ketten“ stimmt mit dem Code', zahl(r'(\d+) Leckereien in (\d+) Ketten', de) == (n_items, n_ketten), zahl(r'(\d+) Leckereien in (\d+) Ketten', de))
ok('en „N treats in M merge chains“ stimmt mit dem Code', zahl(r'(\d+) treats in (\d+) merge chains', en) == (n_items, n_ketten), zahl(r'(\d+) treats in (\d+) merge chains', en))
ok('de „N Welten“ stimmt', zahl(r'(\d+) Welten', de) == (n_welten,), zahl(r'(\d+) Welten', de))
ok('en „N worlds“ stimmt', zahl(r'(\d+) worlds', en) == (n_welten,), zahl(r'(\d+) worlds', en))
ok('de „N Figuren“ stimmt (Dateien a1…)', zahl(r'(\d+) Figuren', de) == (n_figuren,), zahl(r'(\d+) Figuren', de))
ok('en „N characters“ stimmt', zahl(r'(\d+) characters', en) == (n_figuren,), zahl(r'(\d+) characters', en))
ok('de „N-Tage-Serie“ stimmt mit DAILY', zahl(r'(\d+)-Tage-Serie', de) == (n_tage,), zahl(r'(\d+)-Tage-Serie', de))
ok('en „N-day streak“ stimmt mit DAILY', zahl(r'(\d+)-day streak', en) == (n_tage,), zahl(r'(\d+)-day streak', en))
ok('de alle drei Automaten beim Namen genannt', all(g[0].lower() in de.lower() for g in gens), gens)
ok('en alle drei Automaten beim Namen genannt', all(g[1].lower() in en.lower() for g in gens), gens)
ok('de erste und letzte Welt stimmen („von Hamburg … bis ins Sternecafé“)', welt_de[0] in de and welt_de[-1] in de, (welt_de[0], welt_de[-1]))
ok('en erste und letzte Welt stimmen', welt_en[0] in en and welt_en[-1] in en, (welt_en[0], welt_en[-1]))
ok('genannte Städte (Hamburg, Paris, Kyoto) gibt es im Code', all(s in welt_de for s in ('Hamburg', 'Paris', 'Kyoto')), welt_de)
ketten_de = re.findall(r"de:\[([^\]]*)\]", chains)
namen_de = [n for m in ketten_de for n in re.findall(r"'([^']*)'", m)]
ok('de Teile im Text gibt es im Code (Kaffeebohne, Espresso, Matcha, Bubble Tea, Weizen, Festtorte)',
   all(n in namen_de and n in de for n in ('Kaffeebohne', 'Espresso', 'Matcha', 'Bubble Tea', 'Weizen', 'Festtorte')))
ok('Katze Mocha ist im Spiel (CatFx, Bilder in www/art/cat)', 'const CatFx' in src and os.path.isdir(os.path.join(WWW, 'art', 'cat')))
ok('Zielgruppen-Satz „ab 16“ steht in beiden Beschreibungen', 'ab 16 Jahren' in de and 'aged 16 and over' in en)
ok('Beschreibung nennt Käufe, Werbung, Energie und Zufallsgeschenke offen',
   all(w in de for w in ('In-App-Käufe', 'Werbevideos', 'Energie', 'zufällige')) and all(w in en for w in ('in-app purchases', 'reward videos', 'energy', 'random')))
v = re.search(r'Spielversion (\d+\.\d+\.\d+)', doc)
print(f'INFO Dokument sagt Spielversion {v.group(1) if v else "?"}, Code sagt {version}' + ('' if v and v.group(1) == version else '  -> prüfen, ob die Bilder neu erzeugt werden müssen'))

# ---------------------------------------------------------------- Alt-Texte
alt = {}
for zeile in doc.splitlines():
    m = re.match(r'\|\s*(Feature-Grafik|Screenshot \d)\s*\|(.+)\|(.+)\|\s*$', zeile)
    if m:
        alt[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
erwartet = ['Feature-Grafik'] + [f'Screenshot {i}' for i in range(1, 7)]
ok('Alt-Texte für Feature-Grafik und 6 Screenshots vorhanden', sorted(alt) == sorted(erwartet), sorted(alt))
ok('Alt-Texte höchstens 140 Zeichen (de und en)', all(len(t) <= 140 for p in alt.values() for t in p), {k: (len(a), len(b)) for k, (a, b) in alt.items()})
ok('Alt-Texte ohne Fremdnamen', not [n for p in alt.values() for t in p for n in FREMD if n in t.lower()])

# ---------------------------------------------------------------- Bilder
erwartet_dateien = {'app-icon-512.png', 'feature-graphic-de-1024x500.png', 'feature-graphic-en-1024x500.png'} | \
                   {f'screenshot-{n}-{l}.png' for n in range(1, 7) for l in ('de', 'en')}
vorhanden = set(os.listdir(STORE))
ok('store/ enthält genau die erwarteten Dateien (keine Reste mit altem Namen)', vorhanden == erwartet_dateien,
   {'fehlt': sorted(erwartet_dateien - vorhanden), 'überzählig': sorted(vorhanden - erwartet_dateien)})

ic = os.path.join(STORE, 'app-icon-512.png')
im = Image.open(ic)
ok('Icon 512x512, 32-Bit-PNG mit Alpha, höchstens 1024 KB', im.size == (512, 512) and im.mode == 'RGBA' and os.path.getsize(ic) <= 1024 * 1024, (im.size, im.mode, os.path.getsize(ic) // 1024))
ok('Icon im Store-Ordner ist dasselbe wie das Icon der Web-App', filecmp.cmp(ic, os.path.join(WWW, 'icons', 'icon-512.png'), shallow=False))

for l in ('de', 'en'):
    f = os.path.join(STORE, f'feature-graphic-{l}-1024x500.png')
    im = Image.open(f)
    ok(f'Feature-Grafik {l}: 1024x500, 24-Bit ohne Alpha', im.size == (1024, 500) and im.mode == 'RGB', (im.size, im.mode))
    st = ImageStat.Stat(im)
    ok(f'Feature-Grafik {l}: nicht leer, nicht nur Weiß/Schwarz/Dunkelgrau', max(st.stddev) > 30 and 40 < sum(st.mean) / 3 < 215, (round(max(st.stddev)), round(sum(st.mean) / 3)))

for n in range(1, 7):
    paar = []
    for l in ('de', 'en'):
        f = os.path.join(STORE, f'screenshot-{n}-{l}.png')
        im = Image.open(f)
        kurz, lang_ = sorted(im.size)
        gut = im.mode == 'RGB' and 320 <= kurz and lang_ <= 3840 and lang_ <= 2.3 * kurz and os.path.getsize(f) <= 8 * 1024 * 1024
        ok(f'Screenshot {n} {l}: 24-Bit ohne Alpha, 320…3840 px, Seitenverhältnis, höchstens 8 MB', gut, (im.size, im.mode, os.path.getsize(f) // 1024))
        ok(f'Screenshot {n} {l}: 1080x1920 (9:16, Mindestgröße für große Empfehlungsflächen)', im.size == (1080, 1920))
        ok(f'Screenshot {n} {l}: nicht leer', max(ImageStat.Stat(im).stddev) > 25, round(max(ImageStat.Stat(im).stddev)))
        paar.append(im)
    ok(f'Screenshot {n}: deutsche und englische Fassung unterscheiden sich (Oberfläche übersetzt)', ImageChops.difference(paar[0], paar[1]).getbbox() is not None)

print(f'\nERGEBNIS: {"ALLE bestanden" if not FAILS else str(len(FAILS)) + " FEHLER: " + ", ".join(FAILS)}')
sys.exit(1 if FAILS else 0)
