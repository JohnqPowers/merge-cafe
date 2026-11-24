"""Store-Screenshots aus dem laufenden Spiel (www/): 360x640 CSS-Pixel x 3 = 1080x1920, RGB ohne Alpha (Play-Vorgabe).

Die Bretter sind vorbereitet (gefüllt, damit das Bild etwas zeigt). Oberfläche, Grafik und Texte kommen unverändert aus dem Spiel,
es wird nichts nachträglich eingefügt. Beispieldaten sind frei erfunden (Spielerin „Mia“, Café „Café Sonne“ / „Sunny Café“).
Reihenfolge = Upload-Reihenfolge: 1 Hamburg, 2 Paris, 3 Weltreise, 4 Kyoto, 5 Figurenwahl, 6 Tagesbonus.

Aufruf (aus dem Repo-Ordner):  python3 -I scripts/store_shots.py [de] [en] [nummer ...]
Ergebnis: store/screenshot-<nummer>-<sprache>.png. Ohne Angaben: alle sechs Bilder in beiden Sprachen.
Nach jeder sichtbaren Änderung an Oberfläche oder Grafik neu erzeugen und ansehen (docs/STORE_LISTING.md, Abschnitt Grafiken)."""
import asyncio, datetime, io, json, os, sys
from playwright.async_api import async_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tests'))
from _helfer import CHROME, STATE, server      # noqa: E402  (gemeinsamer Test-Server und Chrome-Pfad)

OUT = os.path.join(ROOT, 'store')
LANGS = [a for a in sys.argv[1:] if a in ('de', 'en')] or ['de', 'en']
ONLY = {int(a) for a in sys.argv[1:] if a.isdigit()}
LOCALE = {'de': 'de-DE', 'en': 'en-US'}
TODAY = datetime.date.today()
YESTERDAY = (TODAY - datetime.timedelta(days=1)).isoformat()


def grid(rows):
    """8 Zeilen à 7 Zellen: '.' leer, 'g0' Automat (0 Teekanne, 1 Brotkorb, 2 Hühnerstall), 'c1t2' Teil (Kette 1, Stufe 2, jeweils ab 0)."""
    b = []
    for r in rows:
        for cell in r.split():
            if cell == '.':
                b.append(None)
            elif cell[0] == 'g':
                b.append({'g': int(cell[1:])})
            else:
                c, t = cell[1:].split('t')
                b.append({'c': int(c), 't': int(t)})
    assert len(b) == 56, len(b)
    return b


def order(i, who, req, coins, xp):
    return {'id': i, 'who': who, 'req': [{'c': c, 't': t} for c, t in req], 'coins': coins, 'xp': xp}


def paris(name, cafe):
    st = json.loads(open(STATE, encoding='utf-8').read().replace('@@TODAY@@', TODAY.isoformat()))
    st['profile'].update(name=name, cafe=cafe, avatar='a3')
    st['gifts'] = 1
    st['b'] = grid(['c0t3 c1t2 . c2t2 c1t4 c0t1 c2t0',
                    'c1t1 c0t2 c2t3 c0t2 . c1t1 c0t0',
                    'c2t1 . c1t3 c1t3 c0t4 c2t1 c2t4',
                    'c0t1 c1t0 . c2t2 c0t1 c1t2 c2t0',
                    '. c0t0 c1t1 c0t3 . c2t2 c1t0',
                    'c2t0 c1t2 c0t2 . c1t5 c0t0 c2t1',
                    'c0t1 . c2t0 c1t0 c2t3 . c0t2',
                    'c1t1 c0t0 g0 g1 g2 c2t1 c1t2'])
    return st                                   # Aufträge aus tests/state.json: alle drei lieferbar


def hamburg(name, cafe):
    st = paris(name, cafe)
    st.update(level=4, xp=31, coins=420, gems=18, energy=100, up={'gen': 0, 'bat': 0, 'slots': 0},
              stats={'merges': 70, 'orders': 11, 'spawns': 110, 'sessions': 3}, daily={'last': TODAY.isoformat(), 'streak': 2})
    st['b'] = grid(['c1t0 . c0t1 c1t2 c1t2 c2t0 c0t0',
                    '. c0t2 c2t1 . c1t1 c0t1 .',
                    'c1t2 c0t0 . c1t3 c2t0 . c0t3',
                    'c2t2 . c0t1 c0t1 . c2t1 c1t0',
                    '. c1t0 c2t0 . c0t2 c1t3 .',
                    'c0t0 c2t1 . c1t1 c1t1 c0t1 c2t2',
                    'c1t1 . c0t0 c2t0 . . c0t2',
                    'c0t0 c1t0 g1 g0 g2 c2t1 c1t2'])
    st['orders'] = [order('a', '👵', [(0, 1), (1, 2)], 60, 9), order('b', '👨‍💼', [(1, 3)], 84, 8),
                    order('c', '👩‍🎓', [(2, 1), (0, 2)], 72, 9)]
    return st


def kyoto(name, cafe):
    st = paris(name, cafe)
    st.update(level=26, xp=120, coins=5230, gems=64)
    st['b'] = grid(['c0t4 c1t3 c2t2 . c1t5 c0t2 c2t3',
                    'c2t1 c0t3 . c1t4 c0t5 c1t2 .',
                    'c1t2 c2t4 c0t2 c0t2 . c2t2 c1t3',
                    '. c0t1 c1t6 c2t3 c1t1 . c0t3',
                    'c2t5 c1t1 . c0t6 c2t1 c1t4 c0t1',
                    'c0t2 . c1t3 c2t2 . c0t0 c2t1',
                    'c1t1 c2t3 c0t1 . c1t7 c2t2 .',
                    'c0t2 c1t2 g0 g1 g2 c2t6 c0t1'])
    st['orders'] = [order('a', '👵', [(0, 5), (2, 4)], 288, 20), order('b', '👨‍💼', [(1, 6)], 384, 16),
                    order('c', '👩‍🎓', [(2, 5), (0, 6)], 576, 24)]
    return st


def tagesbonus(name, cafe):
    st = paris(name, cafe)
    st['daily'] = {'last': YESTERDAY, 'streak': 2}     # gestern abgeholt: heute ist Tag 3 zum Abholen bereit
    return st


async def main():
    url = server()
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        for lang in LANGS:
            name, cafe = ('Mia', 'Café Sonne') if lang == 'de' else ('Mia', 'Sunny Café')

            async def shot(n, state, action, wait=1800):
                if ONLY and n not in ONLY:
                    return
                ctx = await browser.new_context(viewport={'width': 360, 'height': 640}, device_scale_factor=3, locale=LOCALE[lang])
                pg = await ctx.new_page()
                errs = []
                pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                if state is not None:
                    await pg.add_init_script("localStorage.setItem('mergecafe_v1', %s)" % json.dumps(json.dumps(state)))
                await pg.goto(url)
                await pg.wait_for_timeout(1500)
                await pg.click('#spPlay', force=True)
                await pg.wait_for_timeout(wait)
                await action(pg)
                im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB')
                assert im.size == (1080, 1920), im.size
                im.save(os.path.join(OUT, f'screenshot-{n}-{lang}.png'), optimize=True)
                print(lang, n, 'Konsolenfehler:', errs or 'keine')
                await ctx.close()

            async def ruhig(pg):
                await pg.wait_for_timeout(1200)

            async def weltkarte(pg):
                await pg.click('#bChap', force=True)
                await pg.wait_for_timeout(2200)

            async def warten(pg):
                await pg.wait_for_timeout(2500)

            async def figuren(pg):                   # frischer Start: Begrüßung mit Namens- und Figurenwahl
                await pg.wait_for_timeout(300)
                await pg.fill('#onName', name)
                await pg.wait_for_timeout(150)
                if await pg.is_visible('#onSug button'):
                    await pg.click('#onSug button >> nth=0')
                else:
                    await pg.fill('#onCafe', cafe)
                await pg.click('[data-av="a3"]')
                await pg.wait_for_timeout(600)

            async def bonus(pg):
                await pg.evaluate('MC.daily()')      # Debug-Hook des Spiels: öffnet das Tagesbonus-Fenster
                await pg.wait_for_timeout(1200)

            await shot(1, hamburg(name, cafe), ruhig)
            await shot(2, paris(name, cafe), ruhig)
            await shot(3, paris(name, cafe), weltkarte)
            await shot(4, kyoto(name, cafe), warten, wait=3000)
            await shot(5, None, figuren, wait=900)
            await shot(6, tagesbonus(name, cafe), bonus)
        await browser.close()


asyncio.run(main())
