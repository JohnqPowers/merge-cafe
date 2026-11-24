// Bündelt die AppsFlyer-Schnittstelle (Version 7) zu www/af.js, die das Spiel in der App nachlädt (window.AFPlugin).
// Läuft im Android-Build nach "npm install" und vor "cap sync". Die erzeugte Datei steht in .gitignore und wird nicht eingecheckt.
// Fehlt etwas, bricht der Build mit klarer Meldung ab, damit nicht still ohne Messung ausgeliefert wird.
const fs = require('node:fs');
let esbuild;
try { esbuild = require('esbuild'); } catch (e) { console.error('esbuild fehlt – zuerst "npm install" ausführen.'); process.exit(1); }
for (const pkg of ['appsflyer-capacitor-plugin', '@appsflyer-sdk/js-core-plugin', '@capacitor/core']) {
  try { require.resolve(pkg + '/package.json'); } catch (e) { console.error(`Paket fehlt: ${pkg} – "npm install" ausführen.`); process.exit(1); }
}
try {
  esbuild.buildSync({ entryPoints: ['scripts/af-entry.js'], bundle: true, format: 'iife', platform: 'browser', target: ['chrome80'], minify: true, legalComments: 'none', outfile: 'www/af.js', logLevel: 'warning' });
} catch (e) { console.error('Bündeln fehlgeschlagen:', e.message); process.exit(1); }
const kb = Math.round(fs.statSync('www/af.js').size / 1024);
if (kb < 5) { console.error(`www/af.js ist mit ${kb} KB verdächtig klein.`); process.exit(1); }
const ver = p => { try { return require(p + '/package.json').version; } catch (e) { return '?'; } };
console.log(`www/af.js gebündelt (${kb} KB): appsflyer-capacitor-plugin ${ver('appsflyer-capacitor-plugin')}, js-core-plugin ${ver('@appsflyer-sdk/js-core-plugin')}, @capacitor/core ${ver('@capacitor/core')}`);
