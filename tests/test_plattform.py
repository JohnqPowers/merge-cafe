"""Plattformtest mit nachgebauten Plugins (AdMob/UMP, AppsFlyer 7, RevenueCat): Einwilligung vor Werbung und Messung, Widerruf, Store-Preise, Kauf, Pro (Entitlement, Paywall, Customer Center, Wiederherstellen, Schlüssel-Regeln), Sperre bei unvollständigen Rechtstexten, Browser-Variante. Aufruf: python3 -I tests/test_plattform.py"""
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
window.__rc={pro:!!window.__cfg.proStart,sku:'yearly',cb:null};
const ci=()=>({entitlements:{active:window.__rc.pro?{noa_s_bean_trail_pro:{identifier:'noa_s_bean_trail_pro',isActive:true,productIdentifier:window.__rc.sku}}:{},all:{}},managementURL:'https://play.google.com/store/account/subscriptions?sku=yearly&package=de.test'});
window.__rc.push=wrap=>{const x=ci();window.__rc.cb(wrap?{customerInfo:x}:x)};
const PKG=(id,type,pid,price,ps,title)=>({identifier:id,packageType:type,offeringIdentifier:'default',product:{identifier:pid,price:price,priceString:ps,currencyCode:'EUR',title:title}});
window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',Plugins:{
 AdMob:{
  requestConsentInfo:async()=>{L('AdMob.requestConsentInfo');return window.__cfg.info},
  showConsentForm:async()=>{L('AdMob.showConsentForm');await wait(250);window.__cfg.info=window.__cfg.afterForm;return window.__cfg.afterForm},
  showPrivacyOptionsForm:async()=>{L('AdMob.showPrivacyOptionsForm');if(window.__cfg.afterPrivacy)window.__cfg.info=window.__cfg.afterPrivacy},
  initialize:async o=>{L('AdMob.initialize '+JSON.stringify(o))},
  prepareRewardVideoAd:async o=>{L('AdMob.prepareRewardVideoAd '+JSON.stringify(o||{}))},
  showRewardVideoAd:async()=>{L('AdMob.showRewardVideoAd');return {type:'coin',amount:1}}
 },
 Purchases:{
  setLogLevel:async o=>{L('RC.setLogLevel '+JSON.stringify(o))},
  configure:async o=>{L('RC.configure '+JSON.stringify(o))},
  getProducts:async o=>{L('RC.getProducts '+JSON.stringify(o));return {products:window.__cfg.noProducts?[]:[
    {identifier:'starter_pack',price:1.99,priceString:'1,99 €',currencyCode:'EUR'},
    {identifier:'gems_small',price:0.99,priceString:'0,99 €',currencyCode:'EUR'},
    {identifier:'gems_large',price:4.99,priceString:'4,99 €',currencyCode:'EUR'}]}},
  purchaseStoreProduct:async o=>{L('RC.purchaseStoreProduct '+o.product.identifier);return {}},
  getCustomerInfo:async()=>{L('RC.getCustomerInfo');if(window.__cfg.ciFail)throw new Error('offline');return {customerInfo:ci()}},
  getOfferings:async()=>{L('RC.getOfferings');return {all:{},current:window.__cfg.noOffering?null:{identifier:'default',availablePackages:[PKG('$rc_lifetime','LIFETIME','lifetime',49.99,'49,99 €','Lifetime'),PKG('$rc_annual','ANNUAL','yearly',19.99,'19,99 €','Yearly'),PKG('$rc_monthly','MONTHLY','monthly',2.99,'2,99 €','Monthly')]}}},
  purchasePackage:async o=>{L('RC.purchasePackage '+o.aPackage.identifier);if(window.__cfg.cancelBuy){const e=new Error('Purchase was cancelled.');if(window.__cfg.cancelStyle==='code'){e.code='1'}else{e.userCancelled=true}throw e}if(window.__cfg.failBuy)throw new Error('billing');window.__rc.pro=true;window.__rc.sku=o.aPackage.product.identifier;return {productIdentifier:o.aPackage.product.identifier,customerInfo:ci()}},
  restorePurchases:async()=>{L('RC.restorePurchases');if(window.__cfg.restorable){window.__rc.pro=true}return {customerInfo:ci()}},
  addCustomerInfoUpdateListener:async cb=>{L('RC.addCustomerInfoUpdateListener');window.__rc.cb=cb;return 'id1'}
 }}};
if(!window.__cfg.noUI){window.Capacitor.Plugins.RevenueCatUI={
  presentPaywallIfNeeded:async o=>{L('UI.presentPaywallIfNeeded '+JSON.stringify(o));if(window.__rc.pro)return {result:'NOT_PRESENTED'};await wait(120);const r=window.__cfg.paywallResult||'PURCHASED';if(r==='PURCHASED'||r==='RESTORED'){window.__rc.pro=true;window.__rc.sku='yearly'}return {result:r}},
  presentCustomerCenter:async()=>{L('UI.presentCustomerCenter');if(window.__cfg.ccFail)throw new Error('Customer Center nicht verfuegbar')}
}}
""" % json.dumps(cfg)
async def mk(b, cfg=None, native=True, af=True, legal=True, build=None, rckey='goog_testkey1234567890', pro=False):
    pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1, locale='de-DE')
    pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    if legal or rckey or pro:
        async def fix(route):
            r = await route.fetch(); body = await r.text()
            if legal: body = body.replace('legalReady: false', 'legalReady: true', 1)
            if rckey: body = body.replace("android: 'YOUR_RC_ANDROID_KEY'", "android: '%s'" % rckey, 1)
            if pro: body = body.replace('proEnabled: false', 'proEnabled: true', 1)      # Schalter für Noa's Pro; ausgeliefert ist er aus
            await route.fulfill(response=r, body=body)
        await pg.route('**/index.html', fix)
    if build is not None: await pg.route('**/build.json', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(build)))
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
async def mkp(*a, **k): return await mk(*a, pro=True, **k)                       # wie mk, aber mit eingeschaltetem Pro-Schalter (S12 bis S18)
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
        await pg.evaluate("MC.close()"); await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(300)
        ok('S8 Browser: keine Pro-Karte im Shop', not await pg.evaluate("!!document.querySelector('#modalBody .row.pro')"))
        await pg.evaluate("MC.close()"); await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        ok('S8 Browser: keine Pro-/Wiederherstellen-Zeile in den Optionen', not await pg.evaluate("!!document.querySelector('[data-act=pro],[data-act=manage],[data-act=restore]')"))
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
        # S10: Debug-Paket (build.json vorhanden) -> Testanzeigen; S11: Store-Paket (keine Datei) -> Kennung aus CONFIG
        cfg = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}}
        dbg = {'kind': 'debug', 'admobRewarded': 'ca-app-pub-3940256099942544/5224354917'}
        pg = await mk(b, cfg, build=dbg); lg = await log(pg); print('S10 Log:', [l for l in lg if l.startswith('AdMob')])
        ok('S10 Debug: AdMob.initialize mit Testmodus', any(l.startswith('AdMob.initialize') and '"initializeForTesting":true' in l for l in lg), lg)
        ok('S10 Debug: Video mit Test-Anzeigenblock und isTesting', any(l.startswith('AdMob.prepareRewardVideoAd') and '5224354917' in l and '"isTesting":true' in l for l in lg), lg)
        await pg.evaluate("MC.close()"); await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        txt = await pg.evaluate("document.getElementById('modalBody').innerText")
        ok('S10 Debug: Hinweis „Test-Paket“ in den Optionen', 'Test-Paket' in txt, txt[-120:].replace('\n', ' | '))
        ok('S10 keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mk(b, cfg); lg = await log(pg); print('S11 Log:', [l for l in lg if l.startswith('AdMob')])
        ok('S11 Store-Paket: kein Testmodus', any(l.startswith('AdMob.initialize') and '"initializeForTesting":false' in l for l in lg), lg)
        ok('S11 Store-Paket: Video mit Kennung aus CONFIG, isTesting aus', any(l.startswith('AdMob.prepareRewardVideoAd') and '"isTesting":false' in l and '5224354917' in l for l in lg), lg)
        await pg.evaluate("MC.close()"); await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        ok('S11 Store-Paket: kein Test-Hinweis', 'Test-Paket' not in await pg.evaluate("document.getElementById('modalBody').innerText"))
        ok('S11 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # ---------- Pro (RevenueCat-Entitlement noa_s_bean_trail_pro) ----------
        NR = {'info': {'status': 'NOT_REQUIRED', 'isConsentFormAvailable': False, 'canRequestAds': True, 'privacyOptionsRequirementStatus': 'NOT_REQUIRED'}}
        def cf(**kw):
            c = json.loads(json.dumps(NR)); c.update(kw); return c
        async def toast_of(pg): return await pg.evaluate("(document.getElementById('toast')||{}).innerText||''")
        async def evs(pg): return await pg.evaluate("MC.events().map(e=>[e.name,e.params])")
        async def modal_txt(pg): return await pg.evaluate("document.getElementById('modalBody').innerText.replace(/\\s+/g,' ')")
        PRO_ROW = "(() => { const r = document.querySelector('#modalBody .row.pro'); return r ? [r.innerText.replace(/\\s+/g,' '), r.querySelector('button').dataset.act] : null })()"
        # S12: Pro über die RevenueCat-Paywall kaufen, Pro-Bonus ohne Video, Customer Center
        pg = await mkp(b, cf()); lg = await log(pg); print('S12 Log:', [l for l in lg if l.startswith(('RC', 'UI'))])
        ok('S12 RevenueCat: configure → Kundeninfo, Angebote und Listener', 0 <= idx(lg, 'RC.configure') < idx(lg, 'RC.getCustomerInfo') and idx(lg, 'RC.getOfferings') > 0 and idx(lg, 'RC.addCustomerInfoUpdateListener') > 0, lg)
        ok('S12 Pro ist ohne Kauf aus', not await pg.evaluate("MC.plat.pro"))
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        row = await pg.evaluate(PRO_ROW)
        ok('S12 Shop: Pro-Karte mit Knopf „Ansehen“', row and row[1] == 'pro' and "Noa's Pro" in row[0] and 'Ansehen' in row[0], row)
        g0 = await pg.evaluate("MC.state().gems")
        await pg.click('#modalBody .row.pro button', force=True); await pg.wait_for_timeout(900)
        lg = await log(pg)
        ok('S12 Paywall nur bei fehlendem Entitlement (presentPaywallIfNeeded mit noa_s_bean_trail_pro)', 'UI.presentPaywallIfNeeded {"requiredEntitlementIdentifier":"noa_s_bean_trail_pro","displayCloseButton":true}' in lg, [l for l in lg if l.startswith('UI')])
        g1 = await pg.evaluate("MC.state().gems")
        ok('S12 nach dem Kauf: Pro aktiv, Tagesgeschenk +5 Diamanten', await pg.evaluate("MC.plat.pro") and g1 == g0 + 5 and await pg.evaluate("MC.state().proDay") == today, (g0, g1))
        ev = await evs(pg); names = [n for n, _ in ev]
        ok('S12 Ereignisse: paywall_open, purchase mit Umsatz, first_purchase, pro_start', 'paywall_open' in names and 'first_purchase' in names and 'pro_start' in names and any(n == 'purchase' and p.get('sku') == 'yearly' and p.get('af_revenue') == 19.99 and p.get('af_currency') == 'EUR' for n, p in ev), ev[-6:])
        tt = await toast_of(pg)
        ok('S12 Dank-Hinweis mit Tagesgeschenk', 'Willkommen bei Pro' in tt and '+5 Diamanten' in tt, tt)
        row = await pg.evaluate(PRO_ROW)
        ok('S12 Shop zeigt jetzt „aktiv“ und „Verwalten“', row and row[1] == 'manage' and 'aktiv' in row[0] and 'Verwalten' in row[0], row)
        txt = await pg.evaluate("document.querySelector('#modalBody [data-act=ad]').closest('.row').innerText.replace(/\\s+/g,' ')")
        ok('S12 Pro: Zeile „Pro-Bonus“ statt „Werbung ansehen“', 'Pro-Bonus' in txt and 'Werbung ansehen' not in txt, txt)
        en0, n0 = await pg.evaluate("MC.state().energy"), await pg.evaluate("MC.state().ads.n")
        await pg.click('[data-act=ad]', force=True); await pg.wait_for_timeout(500)
        en1, n1 = await pg.evaluate("MC.state().energy"), await pg.evaluate("MC.state().ads.n")
        names = [n for n, _ in await evs(pg)]
        ok('S12 Pro: +25 Energie ohne Video, Tageslimit zählt, kein ad_request/ad_rewarded', idx(await log(pg), 'AdMob.showRewardVideoAd') == -1 and en1 - en0 >= 24 and n1 == n0 + 1 and 'ad_request' not in names and 'ad_rewarded' not in names, (en0, en1, n0, n1))
        await pg.click('#modalBody .row.pro button', force=True); await pg.wait_for_timeout(400)
        ok('S12 „Verwalten“ öffnet das Customer Center', idx(await log(pg), 'UI.presentCustomerCenter') >= 0)
        ok('S12 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S13: Pro beim Start schon aktiv, Listener (beide Datenformen), Rückkehr in die App
        pg = await mkp(b, cf(proStart=True)); await pg.wait_for_timeout(800)
        st = await pg.evaluate("({pro: MC.plat.pro, sku: MC.plat.proSku, gems: MC.state().gems, day: MC.state().proDay})")
        ok('S13 Pro beim Start aktiv, Tagesgeschenk einmal', st['pro'] and st['sku'] == 'yearly' and st['gems'] == BASE['gems'] + 5 and st['day'] == today, st)
        await pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); await pg.wait_for_timeout(300)
        ok('S13 erneutes Öffnen am selben Tag: kein zweites Geschenk', await pg.evaluate("MC.state().gems") == BASE['gems'] + 5)
        await pg.evaluate("window.__rc.pro=false; window.__rc.push(false)"); await pg.wait_for_timeout(200)
        ok('S13 Listener (CustomerInfo direkt): Abo abgelaufen → Pro aus', not await pg.evaluate("MC.plat.pro"))
        await pg.evaluate("window.__rc.pro=true; window.__rc.push(true)"); await pg.wait_for_timeout(200)
        ok('S13 Listener (mit customerInfo-Umhüllung): Pro wieder an, kein weiteres Geschenk', await pg.evaluate("MC.plat.pro") and await pg.evaluate("MC.state().gems") == BASE['gems'] + 5)
        ev = await evs(pg)
        ok('S13 pro_start nur einmal, kein purchase-Ereignis (nur Bestand)', len([1 for n, _ in ev if n == 'pro_start']) == 1 and not any(n == 'purchase' for n, _ in ev), [n for n, _ in ev])
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        row = await pg.evaluate("(() => { const b = document.querySelector('#modalBody [data-act=manage]'); return b ? b.closest('.row').innerText.replace(/\\s+/g,' ') : null })()")
        ok('S13 Optionen: Pro „aktiv“ mit „Verwalten“, Zeile „Käufe wiederherstellen“', row and 'aktiv' in row and 'Käufe wiederherstellen' in await modal_txt(pg), row)
        ok('S13 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S14: ohne RevenueCat-Oberfläche → eigene Paket-Liste (Kauf, Abbruch, Fehler)
        pg = await mkp(b, cf(noUI=True))
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        await pg.click('#modalBody .row.pro button', force=True); await pg.wait_for_timeout(500)
        kind = await pg.evaluate("document.getElementById('modal').dataset.kind")
        rows = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-pkg]')].map(b=>[b.closest('.row').querySelector('.tx').innerText.replace(/\\s+/g,' '), b.textContent.trim()])")
        ok('S14 eigene Paket-Liste mit drei Paketen', kind == 'paywall' and len(rows) == 3, (kind, rows))
        ok('S14 Namen, Laufzeiten und Preise aus dem Angebot', len(rows) == 3 and rows[0][1] == '49,99 €' and 'Lifetime' in rows[0][0] and rows[1][1] == '19,99 €' and 'Jährlich' in rows[1][0] and 'jederzeit kündbar' in rows[1][0] and rows[2][1] == '2,99 €' and 'Monatlich' in rows[2][0], rows)
        txt = await modal_txt(pg)
        ok('S14 Abo-Hinweise sichtbar (automatische Verlängerung, Kündigung in Google Play, Wiederherstellen)', 'verlängern sich automatisch' in txt and 'Google Play' in txt and 'Käufe wiederherstellen' in txt, txt[-260:])
        await pg.evaluate("window.__cfg.cancelBuy=true; document.getElementById('toast').textContent=''"); await pg.click('[data-pkg="1"]', force=True); await pg.wait_for_timeout(400)
        ok('S14 Abbruch durch den Nutzer: kein Fehlerhinweis, Liste bleibt offen', await toast_of(pg) == '' and not await pg.evaluate("MC.plat.pro") and await pg.evaluate("document.getElementById('modal').dataset.kind") == 'paywall', await toast_of(pg))
        await pg.evaluate("window.__cfg.cancelStyle='code'; document.getElementById('toast').textContent=''"); await pg.click('[data-pkg="1"]', force=True); await pg.wait_for_timeout(400)
        ok('S14 Abbruch als Fehlercode 1 (ohne userCancelled): ebenfalls still', await toast_of(pg) == '' and not await pg.evaluate("MC.plat.pro"), await toast_of(pg))
        await pg.evaluate("window.__cfg.cancelBuy=false; window.__cfg.failBuy=true"); await pg.click('[data-pkg="1"]', force=True); await pg.wait_for_timeout(400)
        ok('S14 Fehler beim Kauf: Hinweis, kein Pro', 'abgebrochen' in await toast_of(pg) and not await pg.evaluate("MC.plat.pro"), await toast_of(pg))
        await pg.evaluate("window.__cfg.failBuy=false"); await pg.click('[data-pkg="2"]', force=True); await pg.wait_for_timeout(700)
        ok('S14 Kauf über purchasePackage mit dem Paket aus dem Angebot', 'RC.purchasePackage $rc_monthly' in await log(pg))
        ev = await evs(pg)
        ok('S14 danach Pro aktiv, Liste geschlossen, purchase mit Umsatz', await pg.evaluate("MC.plat.pro") and await pg.evaluate("document.getElementById('modal').hidden") and any(n == 'purchase' and p.get('sku') == 'monthly' and p.get('af_revenue') == 2.99 for n, p in ev), ev[-4:])
        ok('S14 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S15: Käufe wiederherstellen (gefunden / nichts gefunden)
        pg = await mkp(b, cf(restorable=True))
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        await pg.click('[data-act=restore]', force=True); await pg.wait_for_timeout(600)
        ev = await evs(pg)
        ok('S15 Wiederherstellen: restorePurchases, Pro aktiv, Hinweis, pro_restore statt purchase', 'RC.restorePurchases' in await log(pg) and await pg.evaluate("MC.plat.pro") and 'Pro ist wieder aktiv' in await toast_of(pg) and any(n == 'pro_restore' for n, _ in ev) and not any(n == 'purchase' for n, _ in ev), (await toast_of(pg), [n for n, _ in ev]))
        ok('S15 keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mkp(b, cf())
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        await pg.click('[data-act=restore]', force=True); await pg.wait_for_timeout(500)
        ok('S15 nichts zu finden: Hinweis, kein Pro', 'Keine Käufe' in await toast_of(pg) and not await pg.evaluate("MC.plat.pro"), await toast_of(pg))
        ok('S15 keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S16: Customer Center nicht verfügbar → Hinweis mit Link zur Abo-Verwaltung in Google Play
        for tag, extra in (('Customer Center wirft Fehler', dict(proStart=True, ccFail=True)), ('Plugin fehlt', dict(proStart=True, noUI=True))):
            pg = await mkp(b, cf(**extra))
            await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
            await pg.click('#modalBody .row.pro button', force=True); await pg.wait_for_timeout(500)
            kind = await pg.evaluate("document.getElementById('modal').dataset.kind")
            href = await pg.evaluate("(document.querySelector('#modalBody a.btn')||{}).href||''")
            ok('S16 ' + tag + ': Hinweis „Pro verwalten“ mit Link zu Google Play', kind == 'manage' and href.startswith('https://play.google.com/store/account/subscriptions?sku=yearly'), (kind, href))
            ok('S16 ' + tag + ': keine Fehler', not pg.errs, pg.errs); await pg.close()
        # S17: Schlüssel-Regeln (Platzhalter, test_ im Store-Paket, Debug-Paket mit Test-Store-Schlüssel)
        pg = await mkp(b, cf(), rckey=None); lg = await log(pg)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(600)
        btn = await pg.evaluate("[...document.querySelectorAll('#modalBody [data-buy]')].map(b=>[b.textContent.trim(),b.disabled])")
        ok('S17a Platzhalter-Schlüssel (Build ohne Secret): RevenueCat bleibt aus, keine Pro-Karte, Kauf-Knöpfe gesperrt', idx(lg, 'RC.') == -1 and not await pg.evaluate("!!document.querySelector('#modalBody .row.pro')") and btn and all(x == ['–', True] for x in btn), (lg, btn))
        ok('S17a keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mkp(b, cf(), rckey='test_ABCDEFGHIJKLMNOP'); lg = await log(pg)
        ok('S17b test_-Schlüssel im Store-Paket: wird nicht benutzt (kein configure, kein Absturz)', idx(lg, 'RC.') == -1 and not pg.errs, (lg, pg.errs)); await pg.close()
        dbg = {'kind': 'debug', 'admobRewarded': 'ca-app-pub-3940256099942544/5224354917', 'rcTest': 'test_DEBUGKEY1234567'}
        pg = await mkp(b, cf(), build=dbg, rckey=None); lg = await log(pg)
        ok('S17c Debug-Paket: Test-Store-Schlüssel aus build.json, ausführliche Protokolle', 'RC.configure {"apiKey":"test_DEBUGKEY1234567"}' in lg and 'RC.setLogLevel {"level":"DEBUG"}' in lg, [l for l in lg if l.startswith('RC.')])
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(300)
        txt = await modal_txt(pg)
        ok('S17c Debug-Paket: Optionen zeigen RevenueCat-Stand', 'RevenueCat: Test Store · Pakete: 3 · Pro: –' in txt, txt[-140:])
        ok('S17c keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mkp(b, cf(), build={'kind': 'debug', 'admobRewarded': 'ca-app-pub-3940256099942544/5224354917'}); lg = await log(pg)
        ok('S17d Debug-Paket ohne Test-Schlüssel: nimmt den Schlüssel aus CONFIG', 'RC.configure {"apiKey":"goog_testkey1234567890"}' in lg, [l for l in lg if l.startswith('RC.')]); await pg.close()
        pg = await mkp(b, cf(), build=dbg); lg = await log(pg)
        ok('S17e Debug-Paket: Test-Store-Schlüssel hat Vorrang vor dem Produktiv-Schlüssel', 'RC.configure {"apiKey":"test_DEBUGKEY1234567"}' in lg and not any('goog_' in l for l in lg), [l for l in lg if l.startswith('RC.')]); await pg.close()
        # S18: Randfälle (kein Angebot, Kundeninfo nicht ladbar, Paywall-Ergebnisse)
        pg = await mkp(b, cf(noOffering=True))
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        ok('S18 ohne aktuelles Angebot: keine Pro-Karte, Shop sonst normal', not await pg.evaluate("!!document.querySelector('#modalBody .row.pro')") and await pg.evaluate("!!document.querySelector('#modalBody [data-buy]')"))
        ok('S18 keine Fehler', not pg.errs, pg.errs); await pg.close()
        pg = await mkp(b, cf(ciFail=True)); await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        ok('S18 Kundeninfo nicht ladbar: kein Pro, Pro-Karte „Ansehen“, keine Fehler', not await pg.evaluate("MC.plat.pro") and (await pg.evaluate(PRO_ROW) or ['', ''])[1] == 'pro' and not pg.errs, pg.errs); await pg.close()
        for pw, want in (('CANCELLED', ''), ('ERROR', 'nicht verfügbar'), ('RESTORED', 'wieder aktiv')):
            pg = await mkp(b, cf(paywallResult=pw))
            await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
            await pg.evaluate("document.getElementById('toast').textContent=''")
            await pg.click('#modalBody .row.pro button', force=True); await pg.wait_for_timeout(900)
            tt = await toast_of(pg); pro = await pg.evaluate("MC.plat.pro")
            ok('S18 Paywall-Ergebnis ' + pw, (want in tt if want else tt == '') and pro == (pw == 'RESTORED') and not pg.errs, (tt, pro, pg.errs)); await pg.close()
        # S19: Auslieferungszustand (proEnabled: false): von Noa's Pro ist nichts zu sehen, nichts wird abgefragt, Diamanten-Käufe laufen
        pg = await mk(b, cf(proStart=True)); lg = await log(pg); print('S19 Log:', [l for l in lg if l.startswith(('RC', 'UI'))])
        ok('S19 Schalter aus: RevenueCat konfiguriert (Diamanten-Käufe), aber keine Kundeninfo, keine Angebote, kein Listener', idx(lg, 'RC.configure') >= 0 and idx(lg, 'RC.getCustomerInfo') == -1 and idx(lg, 'RC.getOfferings') == -1 and idx(lg, 'RC.addCustomerInfoUpdateListener') == -1, lg)
        ok('S19 Pro bleibt aus, auch wenn das Konto das Entitlement hätte; kein Tagesgeschenk', not await pg.evaluate("MC.plat.pro") and await pg.evaluate("MC.state().gems") == BASE['gems'], await pg.evaluate("MC.state().gems"))
        await pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); await pg.wait_for_timeout(300)
        ok('S19 Rückkehr in die App fragt nichts ab', idx(await log(pg), 'RC.getCustomerInfo') == -1)
        await pg.click('[data-open="shop"]', force=True); await pg.wait_for_timeout(500)
        tt = await modal_txt(pg)
        ok('S19 Shop: keine Pro-Karte, „Werbung ansehen“ und Diamanten-Pakete wie zuvor', not await pg.evaluate("!!document.querySelector('#modalBody .row.pro')") and "Noa's Pro" not in tt and 'Pro-Bonus' not in tt and 'Werbung ansehen' in tt and await pg.evaluate("document.querySelectorAll('#modalBody [data-buy]').length") >= 2, tt[:160])
        await pg.evaluate("MC.close()"); await pg.wait_for_timeout(200)
        await pg.click('[data-open="settings"]', force=True); await pg.wait_for_timeout(400)
        tt = await modal_txt(pg)
        ok('S19 Optionen: keine Zeilen „Noa\'s Pro“ und „Käufe wiederherstellen“', "Noa's Pro" not in tt and 'wiederherstellen' not in tt and 'Datenschutz' in tt, tt[:160])
        rr = await pg.evaluate("Promise.all([MC.plat.paywall('t'), MC.plat.manage(), MC.plat.restore(), MC.plat.purchasePackage({})])")
        ok('S19 Paywall, Customer Center, Wiederherstellen und Paketkauf sind gesperrt', rr == ['off', 'off', 'off', 'off'], rr)
        ev = await evs(pg)
        ok('S19 keine Pro-Ereignisse (paywall_open, pro_start, pro_restore, first_purchase)', not any(n in ('paywall_open', 'pro_start', 'pro_restore', 'first_purchase') for n, _ in ev), [n for n, _ in ev])
        lg = await log(pg)
        ok('S19 kein Aufruf der Paywall-Oberfläche oder des Customer Centers', not any(l.startswith('UI.') for l in lg), lg)
        ok('S19 keine Fehler', not pg.errs, pg.errs); await pg.close()
        await b.close()
    print(f'\nERGEBNIS: {sum(res)}/{len(res)} bestanden')
asyncio.run(main())
