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
fs.writeFileSync(f, s);
