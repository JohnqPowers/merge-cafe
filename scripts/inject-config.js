// Setzt beim Build die echten Schlüssel aus GitHub-Secrets ein.
// Fehlt ein Secret, bleibt der Platzhalter bzw. die Google-Test-ID stehen.
const fs = require('node:fs');
const f = 'www/index.html';
let s = fs.readFileSync(f, 'utf8');
const map = {
  YOUR_APPSFLYER_DEV_KEY: process.env.APPSFLYER_DEV_KEY,
  YOUR_IOS_APP_ID: process.env.APPSFLYER_IOS_APP_ID,
  YOUR_RC_ANDROID_KEY: process.env.REVENUECAT_ANDROID_KEY,
  YOUR_RC_IOS_KEY: process.env.REVENUECAT_IOS_KEY,
  'ca-app-pub-3940256099942544/5224354917': process.env.ADMOB_REWARDED_ANDROID,
  'ca-app-pub-3940256099942544/1712485313': process.env.ADMOB_REWARDED_IOS
};
for (const [k, v] of Object.entries(map)) if (v) { s = s.split(k).join(v); console.log('gesetzt:', k.slice(0, 22) + '…'); }
// Rechtstexte vollständig? Dann Werbung, Käufe und Messung in der App freischalten (CONFIG.legalReady).
// Platzhalter in den Rechtstexten sind mit [[…]] markiert (www/privacy.html, www/impressum.html).
const legal = ['www/privacy.html', 'www/impressum.html'];
const offen = legal.filter(p => !fs.existsSync(p) || /\[\[/.test(fs.readFileSync(p, 'utf8')));
if (!offen.length) {
  if (!s.includes('legalReady: false')) { console.error('legalReady-Schalter nicht gefunden'); process.exit(1); }
  s = s.replace('legalReady: false', 'legalReady: true');
  console.log('Rechtstexte vollständig: Werbung, Käufe und Messung freigeschaltet');
} else console.log('Platzhalter in ' + offen.join(', ') + ': Werbung, Käufe und Messung bleiben aus (Testversion)');
fs.writeFileSync(f, s);
