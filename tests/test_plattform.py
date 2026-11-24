"""Plattformtest mit nachgebauten Plugins (AdMob/UMP, AppsFlyer 7, RevenueCat): Einwilligung vor Werbung und Messung, Widerruf, Store-Preise, Kauf, Sperre bei unvollständigen Rechtstexten, Browser-Variante. Aufruf: python3 -I tests/test_plattform.py"""
import asyncio, json, datetime, sys, os
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server
URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []
def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''))
AF_MOCK = """
(function(){const L=(s)=>window.__log.push(s);
window.AFPlugin={
 enableTCFDataCollection:async o=>{L('AF.enableTCFDataCollection '+JSON.stringify(o))},
 init:async o=>{L('AF.init '+JSON.stringify(Object.keys(o).sort()))},
 registerSessionReadyListener:async cb=>{L('AF.registerSessionReadyListener');setTimeout(()=>cb(),30)},
 start:async()=>{L('AF.start')},
 stop:async o=>{L('AF.stop '+JSON.stringify(o))},
 logEvent:async o=>{L('AF.logEvent '+o.eventName+' '+JSON.stringify(o.eventValues||{}))}
};})();
"""
def native_mock(cfg):
    return """
window.__log=[]; window.__cfg=%s;
const L=s=>window.__log.push(s); const wait=ms=>new Promise(r=>setTimeout(r,ms));
window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',Plugins:{
 AdMob:{
  requestConsentInfo:async()=>{L('AdMob.requestConsentInfo');return window.__cfg.info},
  showConsentForm:async()=>{L('AdMob.showConsentForm');await wait(250);window.__cfg.info=window.__cfg.afterForm;return window.__cfg.afterForm},
  showPrivacyOptionsForm:async()=>{L('AdMob.showPrivacyOptionsForm');if(window.__cfg.afterPrivacy)window.__cfg.info=window.__cfg.afterPrivacy},
  initialize:async o=>{L('AdMob.initialize '+JSON.stringify(o))},
  prepareRewardVideoAd:async()=>{L('AdMob.prepareRewardVideoAd')},
  showRewardVideoAd:async()=>{L('AdMob.showRewardVideoAd');return {type:'coin',amount:1}}
 },
 Purchases:{
  configure:async o=>{L('RC.configure '+JSON.stringify(Object.keys(o)))},
  getProducts:async o=>{L('RC.getProducts '+JSON.stringify(o));return {products:window.__cfg.noProducts?[]:[
    {identifier:'starter_pack',price:1.99,priceString:'1,99 €',currencyCode:'EUR'},
    {identifier:'gems_small',price:0.99,priceString:'0,99 €',currencyCode:'EUR'},
    {identifier:'gems_large',price:4.99,priceString:'4,99 €',currencyCode:'EUR'}]}},
  purchaseStoreProduct:async o=>{L('RC.purchaseStoreProduct '+o.product.identifier);return {}}
 }}};
""" % json.dumps(cfg)
async def mk(b, cfg=None, native=True, af=True, legal=True):
    pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1, locale='de-DE')
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if legal:
        async def fix(route):
            r = await route.fetch(); body = (await r.text()).replace('legalReady: false', 'legalReady: true', 1)
            await route.fulfill(response=r, body=body)
        await pg.route('**/index.html', fix)
    if native:
        await pg.add_init_script(native_mock(cfg))
        if af: await pg.route('**/af.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body=AF_MOCK))
    st = json.dumps(BASE).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % st)
    await pg.goto(URL); await pg.wait_for_timeout(1200)
    try: await pg.click('#spPlay', force=True, timeout=1500); await pg.wait_for_timeout(600)
    except Exception: pass
    await pg.wait_for_timeout(1500)
    return pg
async def log(pg): return await pg.evaluate("window.__log||[]")
def idx(lg, prefix):
    for i, l in enumerate(lg):
        if l.startswith(prefix): return i
    return -1
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        EU = {'info': {'status': 'REQUIRED', 'isConsentFormAvailable': True, 'canRequestAds': False, 'privacyOptionsRequirementStatus': 'REQUIRED'},
              'afterForm': {'status': 'OBTAINED', 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'REQUIRED'}}
        # S1: EU, Einwilligung erteilt
        pg = await mk(b, EU); lg = await log(pg); print('S1 Log:', lg)
        ok('S1 Reihenfolge: Einwilligung vor AdMob', 0 <= idx(lg, 'AdMob.showConsentForm') < idx(lg, 'AdMob.initialize'))
        ok('S1 AdMob.initialize mit Altersfilter', any(l.startswith('AdMob.initialize') and 'ParentalGuidance' in l for l in lg))
        ok('S1 Video wird vorgeladen', idx(lg, 'AdMob.prepareRewardVideoAd') > idx(lg, 'AdMob.initialize') >= 0)
        ok('S1 AppsFlyer: TCF → init → Listener', 0 <= idx(lg, 'AF.enableTCFDataCollection') < idx(lg, 'AF.init') < idx(lg, 'AF.registerSessionReadyListener'))
        ok('S1 AppsFlyer start erst nach Einwilligung', idx(lg, 'AF.start') > idx(lg, 'AdMob.showConsentForm') >= 0)
        ok('S1 AppsFlyer init mit devKey+appId', 'AF.init ["appId","devKey"]' in lg)
        ok('S1 keine Ereignisse vor start', idx(lg, 'AF.logEvent') == -1 or idx(lg, 'AF.logEvent') > idx(lg, 'AF.start'))
        ok('S1 session_start nach start nachgereicht', any(l.startswith('AF.logEvent session_start') for l in lg), [l for l in lg if 'session_start' in l])
        ok('S1 RevenueCat configure', idx(lg, 'RC.configure') >= 0)
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(400)
        ok('S1 Einstellungen: Werbe-Einstellungen-Zeile', await pg.evaluate("!!document.querySelector('[data-act=privopt]')"))
        txt = await pg.evaluate("document.getElementById('modalBody').innerText")
        ok('S1 Einstellungen: Datenschutz, Impressum, Lizenzen', all(w in txt for w in ('Datenschutz', 'Impressum', 'Lizenzen')), txt[:260].replace('\n', ' | '))
        hrefs = await pg.evaluate("[...document.querySelectorAll('#modalBody a')].map(a=>a.getAttribute('href'))")
        ok('S1 Links', hrefs == ['privacy.html', 'impressum.html', 'licenses.html'], hrefs)
        await pg.click('[data-act=privopt]', force=True); await pg.wait_for_timeout(400)
        ok('S1 Werbe-Einstellungen öffnet das Google-Fenster', idx(await log(pg), 'AdMob.showPrivacyOptionsForm') >= 0)
        ok('S1 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S2: EU, Einwilligung abgelehnt
        cfg = json.loads(json.dumps(EU)); cfg['afterForm'] = {'status': 'REQUIRED', 'canRequestAds': False, 'privacyOptionsRequirementStatus': 'REQUIRED'}
        pg = await mk(b, cfg); lg = await log(pg); print('S2 Log:', lg)
        ok('S2 abgelehnt: AdMob nicht gestartet', idx(lg, 'AdMob.initialize') == -1 and idx(lg, 'AdMob.prepareRewardVideoAd') == -1)
        ok('S2 abgelehnt: AppsFlyer sendet nichts (kein start, keine Ereignisse)', idx(lg, 'AF.start') == -1 and idx(lg, 'AF.logEvent') == -1)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(500)
        toast = await pg.evaluate("(document.getElementById('toast')||{}).innerText||''")
        ok('S2 abgelehnt: Werbe-Knopf zeigt Hinweis, kein Video', 'Werbung ist aus' in toast and idx(await log(pg), 'AdMob.showRewardVideoAd') == -1, toast)
        ok('S2 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S3: keine Einwilligung nötig (z. B. USA)
        cfg = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}}
        pg = await mk(b, cfg); lg = await log(pg); print('S3 Log:', lg)
        ok('S3 kein Einwilligungsfenster', idx(lg, 'AdMob.showConsentForm') == -1)
        ok('S3 AdMob + AppsFlyer laufen', idx(lg, 'AdMob.initialize') >= 0 and idx(lg, 'AF.start') >= 0)
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        ok('S3 keine Werbe-Einstellungen-Zeile', not await pg.evaluate("!!document.querySelector('[data-act=privopt]')"))
        await pg.evaluate("MC.close()"); await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(300)
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(900)
        lg = await log(pg)
        ok('S3 Belohnungs-Video wird gezeigt', idx(lg, 'AdMob.showRewardVideoAd') >= 0)
        ok('S3 ad_request/ad_rewarded an AppsFlyer', any(l.startswith('AF.logEvent ad_request') for l in lg) and any(l.startswith('AF.logEvent ad_rewarded') for l in lg))
        ok('S3 keine Fehler', not pg.errs, pg.errs)
        # S4: Käufe mit Store-Preisen (gleiche Seite, Shop öffnen)
        await pg.evaluate("MC.close()"); await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(700)
        lg = await log(pg)
        ok('S4 Produkte als einmalige Käufe angefragt', 'RC.getProducts {"productIdentifiers":["starter_pack","gems_small","gems_large"],"type":"inapp"}' in lg, [l for l in lg if 'getProducts' in l])
        btn = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-buy]')].map(b=>[b.dataset.buy,b.textContent.trim(),b.disabled])")
        ok('S4 Preise aus dem Store, Knöpfe frei', btn == [['starter_pack','1,99 €',False],['gems_small','0,99 €',False],['gems_large','4,99 €',False]], btn)
        g0 = await pg.evaluate("MC.state().gems")
        await pg.click('[data-buy=gems_small]', force=True); await pg.wait_for_timeout(900)
        lg = await log(pg); g1 = await pg.evaluate("MC.state().gems")
        ok('S4 Kauf über RevenueCat, 60 Diamanten gutgeschrieben', 'RC.purchaseStoreProduct gems_small' in lg and g1 == g0 + 60, (g0, g1))
        ok('S4 purchase-Ereignis mit Umsatz an AppsFlyer', any(l.startswith('AF.logEvent purchase') and '"af_revenue": 0.99' in l.replace('"af_revenue":', '"af_revenue": ') and 'EUR' in l for l in lg), [l for l in lg if 'purchase ' in l])
        ok('S4 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S5: Preise nicht ladbar
        cfg = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}, 'noProducts': True}
        pg = await mk(b, cfg)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(800)
        btn = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-buy]')].map(b=>[b.textContent.trim(),b.disabled])")
        ok('S5 ohne Store-Preise: Knöpfe gesperrt mit „–“', btn and all(x == ['–', True] for x in btn), btn)
        ok('S5 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S6: Widerruf über die Werbe-Einstellungen
        cfg = json.loads(json.dumps(EU)); cfg['afterPrivacy'] = {'status': 'REQUIRED', 'canRequestAds': False, 'privacyOptionsRequirementStatus': 'REQUIRED'}
        pg = await mk(b, cfg)
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        await pg.click('[data-act=privopt]', force=True); await pg.wait_for_timeout(600)
        lg = await log(pg)
        ok('S6 Widerruf: AppsFlyer wird gestoppt', 'AF.stop {"shouldStop":true}' in lg, [l for l in lg if 'stop' in l])
        await pg.evaluate("MC.close()"); await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(300)
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(400)
        ok('S6 Widerruf: keine Werbung mehr', idx(await log(pg), 'AdMob.showRewardVideoAd') == -1)
        n0 = len([l for l in lg if l.startswith('AF.logEvent')]); await pg.evaluate("MC.levelUp(13)"); await pg.wait_for_timeout(500)
        n1 = len([l for l in await log(pg) if l.startswith('AF.logEvent')])
        ok('S6 Widerruf: keine weiteren Messereignisse', n1 == n0, (n0, n1))
        ok('S6 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S7: ohne af.js (Datei fehlt) darf nichts brechen
        cfg = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}}
        pg = await mk(b, cfg, af=False); lg = await log(pg)
        ok('S7 ohne af.js: Werbung und Käufe laufen trotzdem', idx(lg, 'AdMob.initialize') >= 0 and idx(lg, 'RC.configure') >= 0 and idx(lg, 'AF.') == -1, lg)
        await pg.evaluate("MC.levelUp(13)"); await pg.wait_for_timeout(300)
        ok('S7 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S8: Browser (kein Capacitor)
        pg = await mk(b, None, native=False)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(400)
        btn = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-buy]')].map(b=>[b.textContent.trim(),b.disabled])")
        ok('S8 Browser: Hinweis-Preise, Knöpfe frei', btn == [['1,99 €', False], ['0,99 €', False], ['4,99 €', False]], btn)
        await pg.click('[data-buy=gems_small]', force=True); await pg.wait_for_timeout(400)
        toast = await pg.evaluate("(document.getElementById('toast')||{}).innerText||''")
        ok('S8 Browser: Kauf zeigt App-Hinweis', 'App-Version' in toast, toast)
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(3600)
        ok('S8 Browser: Demo-Werbung belohnt', await pg.evaluate("MC.state().ads.n") >= 1)
        ok('S8 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S9: Rechtstexte unvollständig (legalReady false) -> alles aus
        cfg = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}}
        pg = await mk(b, cfg, legal=False); lg = await log(pg); print('S9 Log:', lg)
        ok('S9 gesperrt: kein Plugin wird angefasst', lg == [], lg)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(600)
        btn = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-buy]')].map(b=>[b.textContent.trim(),b.disabled])")
        ok('S9 gesperrt: Kauf-Knöpfe aus', btn and all(x == ['–', True] for x in btn), btn)
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(400)
        toast = await pg.evaluate("(document.getElementById('toast')||{}).innerText||''")
        ok('S9 gesperrt: Werbung zeigt Hinweis, kein Video', 'Werbung ist aus' in toast and 'AdMob.showRewardVideoAd' not in await log(pg), toast)
        await pg.evaluate("MC.close()"); await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        txt = await pg.evaluate("document.getElementById('modalBody').innerText")
        ok('S9 gesperrt: Hinweis „Testversion“ in den Optionen, keine Werbe-Einstellungen', 'Testversion' in txt and not await pg.evaluate("!!document.querySelector('[data-act=privopt]')"), txt[-160:].replace('\n', ' | '))
        await pg.evaluate("MC.close()"); await pg.evaluate("MC.levelUp(13)"); await pg.wait_for_timeout(300)
        ok('S9 gesperrt: keine Messereignisse, keine Fehler', await log(pg) == [] and not pg.errs, pg.errs); await pg.close()
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
asyncio.run(main())
