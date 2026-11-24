"""Feature-Grafik 1024x500 für Google Play (Deutsch und Englisch), gebaut aus Spielmaterial:
App-Icon (store/app-icon-512.png), Item-Bilder (www/art), die Stadt-Postkarten des Spiels (Scenes.svg über den Debug-Hook MC.scene)
und die im Spiel eingebetteten Schriften (Lilita One, Fredoka; beide OFL, siehe docs/ASSETS_LIZENZEN.md).
Gerendert mit doppelter Pixeldichte und auf 1024x500 verkleinert, RGB ohne Alpha (Play-Vorgabe).
Play-Regeln für Grafiken: keine Handlungsaufforderung („Jetzt laden“), keine Preise, keine Rangangaben („Nr. 1“, „Beste“), keine fremden Marken.

Aufruf (aus dem Repo-Ordner):  python3 -I scripts/store_promo.py
Ergebnis: store/feature-graphic-de-1024x500.png und store/feature-graphic-en-1024x500.png"""
import asyncio, io, os, re, sys, tempfile
from playwright.async_api import async_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tests'))
from _helfer import CHROME, server             # noqa: E402

WWW = os.path.join(ROOT, 'www')
ICON = os.path.join(ROOT, 'store', 'app-icon-512.png')
OUT = os.path.join(ROOT, 'store')

idx = open(os.path.join(WWW, 'index.html'), encoding='utf-8').read()
FONTS = '\n'.join(re.findall(r'@font-face\{font-family:(?:Fredoka|"Lilita One")[^}]*\}', idx)[:2])
assert FONTS.count('@font-face') == 2, 'Schriften in www/index.html nicht gefunden'

TAG = {'de': 'Verschmelzen · Backen · Reisen', 'en': 'Merge · Bake · Travel'}
CARDS = [(0, '🇩🇪', 'Hamburg', -6), (2, '🇫🇷', 'Paris', 2), (5, '🇯🇵', 'Kyoto', -3)]    # Welt-Nummer, Flagge, Name, Neigung

TPL = '''<!doctype html><html><head><meta charset="utf-8"><style>
%%FONTS%%
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1024px;height:500px;overflow:hidden;background:#000}
.stage{position:relative;width:1024px;height:500px;overflow:hidden;
  background:radial-gradient(ellipse 620px 520px at 790px 250px,#FFD66B 0%,#FFAB4A 42%,#F2686F 78%,#D8466F 100%)}
.rays{position:absolute;inset:0;background:repeating-conic-gradient(from 3deg at 790px 250px,rgba(255,255,255,.20) 0 7.5deg,rgba(255,255,255,0) 7.5deg 15deg);
  -webkit-mask-image:radial-gradient(circle at 790px 250px,#000 0,#000 240px,rgba(0,0,0,0) 640px);mask-image:radial-gradient(circle at 790px 250px,#000 0,#000 240px,rgba(0,0,0,0) 640px)}
.title{position:absolute;left:44px;top:22px;font-family:"Lilita One",Fredoka,sans-serif;color:#FFF3C6;line-height:.9;
  -webkit-text-stroke:12px #7A2E12;paint-order:stroke fill;text-shadow:0 7px 0 #7A2E12,0 16px 22px rgba(90,25,0,.35);letter-spacing:1px}
.t1{font-size:92px;margin-left:6px}
.t2{font-size:124px;margin-top:2px}
.tag{position:absolute;left:46px;top:252px;font-family:Fredoka,sans-serif;font-weight:600;font-size:31px;color:#fff;letter-spacing:.3px;
  background:rgba(110,38,16,.82);border-radius:999px;padding:7px 26px 9px;box-shadow:0 5px 0 rgba(70,20,6,.45)}
.pc{position:absolute;width:166px;padding:6px;border-radius:7px;box-shadow:0 8px 14px rgba(80,20,0,.38);
  background:repeating-linear-gradient(135deg,#E24C4C 0 9px,#fff 9px 18px,#3E78D6 18px 27px,#fff 27px 36px)}
.pc .in{position:relative;background:#fffdf6;border-radius:3px;overflow:hidden}
.pc .pv{height:100px;position:relative;overflow:hidden}.pc .pv svg{position:absolute;inset:0;width:100%;height:100%}
.pc .nm{font-family:"Lilita One",Fredoka,sans-serif;font-size:19px;color:#5A2A12;padding:2px 9px 4px;line-height:1.1}
.pc .st{position:absolute;top:5px;right:5px;width:26px;height:31px;display:grid;place-items:center;font-size:17px;background:#fffdf6;border:2px dashed #C9B79C;border-radius:3px;transform:rotate(4deg)}
.hero{position:absolute;left:598px;top:52px;width:394px;height:394px;border-radius:90px;transform:rotate(2.5deg);
  box-shadow:0 0 0 7px rgba(255,255,255,.55),0 24px 44px rgba(90,25,0,.45),0 0 90px 24px rgba(255,236,150,.55)}
.sp{position:absolute;filter:drop-shadow(0 9px 6px rgba(90,25,0,.38))}
.star{position:absolute;width:30px;height:30px;opacity:.95}
</style></head><body><div class="stage">
<div class="rays"></div>
<div class="title"><div class="t1">Noa's</div><div class="t2">Bean Trail</div></div>
<div class="tag">%%TAG%%</div>
%%CARDS%%
<img class="hero" src="file://%%ICON%%">
<img class="sp" style="left:522px;top:312px;width:128px;transform:rotate(-12deg)" src="file://%%ART%%/k2_s6.webp">
<img class="sp" style="left:545px;top:14px;width:112px;transform:rotate(9deg)" src="file://%%ART%%/k1_s4.webp">
<img class="sp" style="left:896px;top:10px;width:116px;transform:rotate(18deg)" src="file://%%ART%%/k2_s3.webp">
<img class="sp" style="left:912px;top:366px;width:104px;transform:rotate(-14deg)" src="file://%%ART%%/k2_s5.webp">
<svg class="star" style="left:30px;top:6px" viewBox="0 0 24 24"><path fill="#FFF6C8" d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>
<svg class="star" style="left:520px;top:240px;width:24px;height:24px" viewBox="0 0 24 24"><path fill="#FFF6C8" d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>
<svg class="star" style="left:990px;top:230px;width:26px;height:26px" viewBox="0 0 24 24"><path fill="#FFF6C8" d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>
</div></body></html>'''


async def main():
    url = server()
    tmp = tempfile.mkdtemp(prefix='promo-')
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = await browser.new_page(viewport={'width': 360, 'height': 640})
        await pg.goto(url)
        await pg.wait_for_timeout(1200)
        scenes = {}
        for i, *_ in CARDS:
            scenes[i] = await pg.evaluate(f"MC.scene({i}, '0 40 400 300', true)")     # dieselbe Ansicht wie die Postkarten im Spiel
            assert scenes[i].lstrip().startswith('<svg'), scenes[i][:60]
        await pg.close()
        for lang in ('de', 'en'):
            cards = ''
            for k, (i, flag, name, rot) in enumerate(CARDS):
                x, y = 40 + k * 168, 330 + (k % 2) * -6
                cards += (f'<div class="pc" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="in">'
                          f'<div class="pv">{scenes[i]}</div><span class="st">{flag}</span><div class="nm">{name}</div></div></div>\n')
            html = (TPL.replace('%%FONTS%%', FONTS).replace('%%TAG%%', TAG[lang]).replace('%%CARDS%%', cards)
                       .replace('%%ICON%%', ICON).replace('%%ART%%', os.path.join(WWW, 'art')))
            page_file = os.path.join(tmp, f'promo-{lang}.html')
            open(page_file, 'w', encoding='utf-8').write(html)
            ctx = await browser.new_context(viewport={'width': 1024, 'height': 500}, device_scale_factor=2)
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            await pg.goto('file://' + page_file)
            await pg.wait_for_timeout(1500)
            await pg.evaluate('document.fonts.ready')
            im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB').resize((1024, 500), Image.LANCZOS)
            im.save(os.path.join(OUT, f'feature-graphic-{lang}-1024x500.png'), optimize=True)
            print(lang, im.size, im.mode, 'Konsolenfehler:', errs or 'keine')
            await ctx.close()
        await browser.close()


asyncio.run(main())
