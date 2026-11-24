// Ergänzt das generierte Android-Projekt um Pflichteinträge:
// - AdMob APPLICATION_ID (ohne diesen Eintrag stürzt die App beim Start ab)
// - versionCode / versionName aus der Build-Nummer
const fs = require('node:fs');
const manifest = 'android/app/src/main/AndroidManifest.xml';
const gradle = 'android/app/build.gradle';
const admobAppId = process.env.ADMOB_APP_ID_ANDROID || 'ca-app-pub-3940256099942544~3347511713'; // Google-Test-ID
const build = Number(process.env.BUILD_NUMBER || '1');

let m = fs.readFileSync(manifest, 'utf8');
if (!m.includes('com.google.android.gms.ads.APPLICATION_ID')) {
  m = m.replace(/<application([^>]*)>/, `<application$1>\n        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="${admobAppId}"/>`);
  fs.writeFileSync(manifest, m);
  console.log('AdMob APPLICATION_ID eingetragen');
}
let g = fs.readFileSync(gradle, 'utf8');
g = g.replace(/versionCode\s+\d+/, `versionCode ${build}`).replace(/versionName\s+"[^"]*"/, `versionName "1.0.${build}"`);
fs.writeFileSync(gradle, g);
console.log(`Version 1.0.${build} (Code ${build})`);

// App-Name mit Apostroph ("Noa's Bean Trail"): In Android-Ressourcen muss er als \' stehen, sonst bricht aapt2 den
// Build ab ("unescaped apostrophe in string"). Schon maskierte Apostrophe bleiben unverändert (läuft also gefahrlos
// auch dann, wenn Capacitor selbst maskiert).
const strings = 'android/app/src/main/res/values/strings.xml';
if (fs.existsSync(strings)) {
  const x = fs.readFileSync(strings, 'utf8');
  const y = x.replace(/(<string\b[^>]*>)([^<]*)(<\/string>)/g, (_, a, body, c) => a + body.replace(/(?<!\\)'/g, "\\'") + c);
  if (y !== x) { fs.writeFileSync(strings, y); console.log('Apostrophe in strings.xml maskiert'); }
}
