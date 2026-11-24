// Ergänzt das generierte Android-Projekt um Pflichteinträge:
// - AdMob APPLICATION_ID (ohne diesen Eintrag stürzt die App beim Start ab)
// - VIBRATE-Berechtigung (Vibration im Spiel)
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
// Vibration (Einstellung „Vibration“ im Spiel): ohne diese Berechtigung ignoriert Android navigator.vibrate() in der App still.
if (!m.includes('android.permission.VIBRATE')) {
  m = m.replace('</manifest>', '    <uses-permission android:name="android.permission.VIBRATE" />\n</manifest>');
  fs.writeFileSync(manifest, m);
  console.log('VIBRATE-Berechtigung eingetragen');
}
// Hochformat sperren: Das Spiel ist fürs Hochformat gebaut; im Querformat wären Start-Knopf und Brett auf Handys nicht erreichbar.
// (Auf Bildschirmen ab 600 dp ignoriert Android 16 die Sperre; dort bleibt das Spiel spielbar, das Brett wird nur kleiner.
// In sehr niedrigen Fenstern zeigt das Spiel selbst einen Dreh-Hinweis.)
if (!/android:screenOrientation=/.test(m)) {
  const y = m.replace(/<activity\b(?=[^>]*android:name="[^"]*MainActivity")/, '<activity android:screenOrientation="portrait"');
  if (y !== m) { m = y; fs.writeFileSync(manifest, m); console.log('Hochformat gesperrt'); }
  else console.warn('WARNUNG: MainActivity im Manifest nicht gefunden, Ausrichtung nicht gesperrt');
}
// Debug-Paket (öffentliche Test-APK): Markierung für Googles Test-Anzeigenblock. Liegt nur in src/debug, also nicht im Store-Paket.
// Das Spiel liest die Datei beim Start (Platform.buildInfo in www/index.html). Der Testblock steht hier, nicht in www/index.html,
// weil inject-config.js dort die Test-Kennung durch die echte ersetzt.
const dbgDir = 'android/app/src/debug/assets/public';
fs.mkdirSync(dbgDir, { recursive: true });
const dbgInfo = { kind: 'debug', admobRewarded: 'ca-app-pub-3940256099942544/5224354917' };
// RevenueCat Test Store: Der test_-Schluessel stuerzt in jedem Release-Paket absichtlich ab (Schutz von RevenueCat). Er darf deshalb nur hier,
// im Debug-Paket, landen – nie in www/index.html und nie in den Store-Paketen. Es werden ausschliesslich test_-Schluessel uebernommen.
const rcTest = (process.env.REVENUECAT_TEST_KEY || '').trim();
if (/^test_[A-Za-z0-9]{8,}$/.test(rcTest)) dbgInfo.rcTest = rcTest;
else if (rcTest) console.warn('WARNUNG: REVENUECAT_TEST_KEY beginnt nicht mit test_ und wird ignoriert');
fs.writeFileSync(dbgDir + '/build.json', JSON.stringify(dbgInfo) + '\n');
console.log('Debug-Paket: Test-Anzeigenblock markiert' + (dbgInfo.rcTest ? ', RevenueCat-Test-Store-Schluessel hinterlegt' : ', ohne RevenueCat-Test-Store-Schluessel'));
// RevenueCat-Oberflaeche (Paywall, Customer Center) braucht mindestens Android 7.0 (API 24). Liegt die Vorgabe des Capacitor-Projekts darunter,
// bricht der Build mit einem Manifest-Konflikt ab; deshalb hier auf 24 anheben (betrifft weniger als 1 % der Geraete).
const vars = 'android/variables.gradle';
if (fs.existsSync(vars)) {
  const v = fs.readFileSync(vars, 'utf8');
  const w = v.replace(/(minSdkVersion\s*=\s*)(\d+)/, (a, p, n) => (Number(n) < 24 ? p + '24' : a));
  if (w !== v) { fs.writeFileSync(vars, w); console.log('minSdkVersion auf 24 angehoben (RevenueCat-Oberflaeche)'); }
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
