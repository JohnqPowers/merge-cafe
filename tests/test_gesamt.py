"""Gesamttest: Start, Profil, Tutorial bis zur ersten Lieferung, Spiel bis Level 6, Geschenke, Werbung (Demo), Shop, Neustart, keine Konsolenfehler. Aufruf: python3 -I tests/test_gesamt.py [Breite Höhe]"""
import asyncio, json, sys, re, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, WWW

W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
H = int(sys.argv[2]) if len(sys.argv) > 2 else 844
res = {}
def ok(name, cond, extra=''):
    res[name] = bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))

async def ent_done(pg, ms=9000):
    """Wartet, bis der Einzug der Figur (.ent) vorbei ist."""
    t = 0
    while t < ms:
        if not await pg.query_selector('.ent'): break
        await pg.wait_for_timeout(100); t += 100
    await pg.wait_for_timeout(300)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        pg = await b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2, locale='de-DE')
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
        pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' and 'fonts.g' not in m.text else None)
        await pg.goto('file://' + os.path.join(WWW, 'index.html')); await pg.wait_for_timeout(1500)
        await pg.click('#spPlay', force=True); await pg.wait_for_timeout(700)
        await pg.fill('#onName', 'Test'); await pg.wait_for_timeout(100)
        (await pg.click('#onSug button >> nth=0') if await pg.is_visible('#onSug button') else await pg.fill('#onCafe', 'Café Test')); await pg.click('[data-av="a3"]'); await pg.wait_for_timeout(200)
        await pg.click('#onGo', force=True); await ent_done(pg)
        cells = await pg.query_selector_all('.cell')
        ok('56 Zellen', len(cells) == 56, len(cells))
        for _ in range(2): await cells[52].click(force=True); await pg.wait_for_timeout(500)

        async def drag(a, b_):
            ba = await cells[a].bounding_box(); bb = await cells[b_].bounding_box()
            await pg.mouse.move(ba['x'] + ba['width'] / 2, ba['y'] + ba['height'] / 2); await pg.mouse.down()
            await pg.mouse.move(ba['x'] + ba['width'] / 2 + 15, ba['y'] + ba['height'] / 2, steps=3)
            await pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2, steps=8); await pg.mouse.up()

        st = await pg.evaluate('MC.state()')
        beans = [i for i, it in enumerate(st['b']) if it and it.get('c') == 0 and it.get('t') == 0]
        if len(beans) >= 2: await drag(beans[0], beans[1])
        await pg.wait_for_timeout(500)
        st = await pg.evaluate('MC.state()')
        ok('Tutorial: Merge erkannt', st['tut'] >= 2, 'tut=%s' % st['tut'])
        await pg.click('.order.ready', force=True); await pg.wait_for_timeout(1400)
        st = await pg.evaluate('MC.state()')
        ok('Tutorial: erste Lieferung', st['tut'] >= 3 and st['stats']['orders'] >= 1, 'tut=%s coins=%s lvl=%s' % (st['tut'], st['coins'], st['level']))

        async def handle_ov():
            vis = await pg.evaluate('!document.getElementById("ov").hidden')
            if not vis: return False
            html = await pg.inner_html('#ov')
            if 'gBox' in html and 'ovGo' not in html:
                for _ in range(3): await pg.click('#gBox', force=True); await pg.wait_for_timeout(150)
                await pg.wait_for_timeout(300)
            await pg.wait_for_timeout(700)
            await pg.click('#ovGo', force=True); await pg.wait_for_timeout(300); return True

        blocking = 0
        for it in range(700):
            if await handle_ov(): blocking += 1; continue
            if not await pg.evaluate('document.getElementById("modal").hidden'): await pg.evaluate('MC.close()')
            st = await pg.evaluate('MC.state()')
            if st['level'] >= 6: break
            if st['energy'] < 5: await pg.evaluate('MC.state().energy=100')
            if await pg.evaluate("(()=>{const c=document.querySelector('.order.ready:not(.leaving)');if(c){c.click();return true}return false})()"):
                await pg.wait_for_timeout(500); continue
            pr = await pg.evaluate('''(()=>{const S=MC.state();const m={};for(let i=0;i<S.b.length;i++){const it=S.b[i];if(!it||it.g!==undefined)continue;const k=it.c+':'+it.t;if(m[k]!==undefined)return [m[k],i];m[k]=i}return null})()''')
            if pr: await drag(pr[0], pr[1]); await pg.wait_for_timeout(120); continue
            gens = [i for i, x in enumerate(st['b']) if x and 'g' in x]
            await cells[gens[it % len(gens)]].click(force=True); await pg.wait_for_timeout(120)
        st = await pg.evaluate('MC.state()')
        ok('Level 6 erreicht', st['level'] >= 6, 'lvl=%s orders=%s blockierende Overlays=%s gifts=%s' % (st['level'], st['stats']['orders'], blocking, st.get('gifts')))
        await pg.wait_for_timeout(2000)

        # ---------- Geschenk-Fach
        await pg.evaluate('MC.state().gifts = 2; MC.render && MC.render()'); await pg.evaluate('MC.gift()'); await pg.wait_for_timeout(500)
        g0 = await pg.evaluate('MC.state().gifts')
        vis = await pg.evaluate('!document.getElementById("giftFab").hidden')
        ok('Geschenk-Symbol sichtbar', vis, 'gifts=%s' % g0)
        await pg.click('#giftFab', force=True); await pg.wait_for_timeout(700)
        ok('Geschenk-Overlay offen', await pg.locator('#gBox').count() == 1)
        before = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
        for _ in range(3): await pg.click('#gBox', force=True); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(500)
        g1 = await pg.evaluate('MC.state().gifts')
        after = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
        ok('Geschenk geöffnet: -1 im Fach, Belohnung gutgeschrieben', g1 == g0 - 1 and after > before, 'gifts %s→%s, Summe %s→%s' % (g0, g1, before, after))
        ok('Geschenk: Verdoppeln-Knopf da', await pg.locator('#gDbl').count() == 1)
        await pg.click('#gDbl', force=True); await pg.wait_for_timeout(4200)
        after2 = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
        ok('Geschenk verdoppelt (Demo-Werbung)', after2 > after, '%s→%s' % (after, after2))
        await pg.click('#ovGo', force=True); await pg.wait_for_timeout(400)

        # ---------- Keine Energie: Sheet, Werbung, Diamanten
        await pg.evaluate('MC.state().energy = 0; MC.state().ads = {day:new Date().toISOString().slice(0,10), n:0, d:0}')
        st = await pg.evaluate('MC.state()')
        gens = [i for i, x in enumerate(st['b']) if x and 'g' in x]
        await cells[gens[0]].click(force=True); await pg.wait_for_timeout(500)
        kind = await pg.evaluate('document.getElementById("modal").hidden ? "" : document.getElementById("modal").dataset.kind')
        ok('Keine Energie → Sheet "noenergy"', kind == 'noenergy', kind)
        await pg.click('[data-act="ad"]', force=True); await pg.wait_for_timeout(4300)
        st = await pg.evaluate('MC.state()')
        ok('Energie-Werbung: +25 ⚡, Zähler 1', st['energy'] >= 25 and st['ads']['n'] == 1, 'energy=%s ads=%s' % (st['energy'], st['ads']))
        await pg.evaluate('MC.close()')
        await pg.evaluate('MC.state().energy = 0; MC.state().gems = 50'); await pg.evaluate('MC.noEnergy()'); await pg.wait_for_timeout(400)
        await pg.click('[data-act="refill"]', force=True); await pg.wait_for_timeout(600)
        st = await pg.evaluate('MC.state()')
        ok('Auffüllen für 15 💎', st['gems'] == 35 and st['energy'] >= 100, 'gems=%s energy=%s' % (st['gems'], st['energy']))

        # ---------- Auftrag: Zutaten kaufen
        await pg.evaluate('MC.close()')
        info = await pg.evaluate('''(()=>{const S=MC.state();S.gems=500;return S.orders.map((o,i)=>i)})()''')
        bought = False
        for i in info:
            await pg.evaluate('MC.order(%d)' % i); await pg.wait_for_timeout(500)
            if await pg.locator('[data-act="orderbuy"]').count() == 1:
                g_before = await pg.evaluate('MC.state().gems'); n_before = await pg.evaluate('MC.state().b.filter(Boolean).length')
                dis = await pg.evaluate('document.querySelector("[data-act=orderbuy]").disabled')
                await pg.click('[data-act="orderbuy"]', force=True); await pg.wait_for_timeout(1800)
                g_after = await pg.evaluate('MC.state().gems'); n_after = await pg.evaluate('MC.state().b.filter(Boolean).length')
                ready = await pg.evaluate("document.querySelectorAll('.order.ready').length")
                ok('Zutaten kaufen: Diamanten abgebucht, Teile liegen auf dem Brett', (not dis) and g_after < g_before and n_after > n_before, 'gems %s→%s, Teile %s→%s, bereit=%s' % (g_before, g_after, n_before, n_after, ready))
                bought = True; break
            await pg.evaluate('MC.close()')
        if not bought: ok('Zutaten kaufen: Knopf gefunden', False, 'alle Aufträge schon komplett')
        await pg.evaluate('MC.close()')

        # ---------- Bonus: täglich + Verdoppeln
        await pg.evaluate("MC.state().daily.last='2000-01-01'; MC.state().ads={day:new Date().toISOString().slice(0,10), n:0, d:0}")
        await pg.evaluate('MC.daily()'); await pg.wait_for_timeout(400)
        c0 = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
        await pg.click('[data-act="claim"]', force=True); await pg.wait_for_timeout(1200)
        c1 = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
        ok('Täglicher Bonus abgeholt', c1 > c0, '%s→%s' % (c0, c1))
        await pg.evaluate('MC.daily()'); await pg.wait_for_timeout(400)
        has = await pg.locator('[data-act="dailydbl"]').count()
        ok('Täglicher Bonus: Verdoppeln angeboten', has == 1)
        if has:
            await pg.click('[data-act="dailydbl"]', force=True); await pg.wait_for_timeout(4300)
            c2 = await pg.evaluate('(()=>{const s=MC.state();return s.coins+s.energy+s.gems})()')
            ok('Täglicher Bonus verdoppelt', c2 > c1, '%s→%s' % (c1, c2))
        await pg.evaluate('MC.close()')

        # ---------- ×2-Münzen-Chip nach Lieferung
        await pg.evaluate('MC.noLimit()'); await pg.evaluate('MC.dbl({coins:100})'); await pg.wait_for_timeout(900)
        on = await pg.evaluate('document.getElementById("dblChip").classList.contains("on")')
        ok('Münzen-verdoppeln-Chip erscheint', on)
        k0 = await pg.evaluate('MC.state().coins')
        await pg.click('#dblChip', force=True); await pg.wait_for_timeout(4400)
        k1 = await pg.evaluate('MC.state().coins')
        ok('Münzen verdoppelt', k1 >= k0 + 100, '%s→%s' % (k0, k1))

        # ---------- Shop / Diamanten erklärt / Ausbau / Optionen
        await pg.evaluate('MC.shop()'); await pg.wait_for_timeout(400)
        await pg.click('[data-act="gems"]', force=True); await pg.wait_for_timeout(400)
        kind = await pg.evaluate('document.getElementById("modal").dataset.kind')
        ok('Info-Knopf öffnet "Was sind Diamanten?"', kind == 'gems', kind)
        await pg.evaluate('MC.close()')
        await pg.evaluate('MC.state().coins = 9000'); await pg.evaluate('MC.ups()'); await pg.wait_for_timeout(400)
        l0 = await pg.evaluate('JSON.stringify(MC.state().up)')
        await pg.click('[data-up]:not([disabled]) >> nth=0', force=True); await pg.wait_for_timeout(400)
        l1 = await pg.evaluate('JSON.stringify(MC.state().up)')
        ok('Ausbau kaufen', l0 != l1, '%s → %s' % (l0, l1))
        await pg.evaluate('MC.close()')
        await pg.evaluate('MC.settings()'); await pg.wait_for_timeout(300); await pg.evaluate('MC.close()')

        # ---------- Speichern/Neuladen
        await pg.wait_for_timeout(500)
        await pg.reload(); await pg.wait_for_timeout(1400)
        sp = await pg.evaluate('!!document.getElementById("spPlay")')
        ok('Neustart: Splash da', sp)
        await pg.click('#spPlay', force=True); await pg.wait_for_timeout(1500)
        st = await pg.evaluate('MC.state()')
        ok('Neustart: Spielstand erhalten', st['level'] >= 6 and st['stats']['orders'] >= 3, 'lvl=%s' % st['level'])
        ev = await pg.evaluate('MC.events().map(e=>e.name)'); print('EVENTS', sorted(set(ev)))
        print('ERRORS', errs[:10])
        ok('Keine Konsolenfehler', not errs, errs[:3])
        await b.close()
    fails = [k for k, v in res.items() if not v]
    print('\nERGEBNIS: %d/%d bestanden' % (len(res) - len(fails), len(res)), 'FEHLER: ' + ', '.join(fails) if fails else '')
asyncio.run(main())
