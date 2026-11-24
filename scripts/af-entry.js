// Einstiegspunkt für www/af.js: macht die AppsFlyer-Schnittstelle (Version 7) dem Spiel als window.AFPlugin zugänglich.
// Das Spiel ist eine einzelne HTML-Datei ohne Bundler; die Schnittstelle liegt als npm-Paket vor, deshalb bündelt der Build sie
// (scripts/bundle-af.js). Im Browser (GitHub Pages) wird diese Datei nie geladen.
import { AppsFlyer } from 'appsflyer-capacitor-plugin';
window.AFPlugin = AppsFlyer;
