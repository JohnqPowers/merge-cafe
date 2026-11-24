# Technische Dokumentation – Noa's Bean Trail

Stand: 24.11.2026. Spielversion 1.5.13 (Push auf `main` am 24.11.2026 freigegeben). Der letzte bis zum Push tatsächlich gebaute und geprüfte Android-Build ist Nr. 12 (`versionName 1.0.12`); die Angaben zu Berechtigungen und Bibliotheken stammen aus dessen Manifest. Die Änderungen ab v1.5.8 (Einwilligung, AppsFlyer 7, Store-Preise, Sperre, Hochformat-Sperre, Test-Anzeigen im Debug-Paket) sind in diesem Stand nur im Browser mit nachgebauten Plugins geprüft, **nicht** in einem echten Android-Build.

## 1. Aufbau

| Teil | Inhalt |
|---|---|
| `www/index.html` | das komplette Spiel in einer Datei (HTML, CSS, JavaScript, Schriften als Base64) |
| `www/art/`, `www/icons/` | Bilder (WebP) und Icons |
| `www/privacy.html`, `impressum.html`, `licenses.html`, `ofl/` | Rechtstexte, in Deutsch und Englisch |
| `www/sw.js`, `www/manifest.webmanifest` | Web-Version (Service Worker: Netz zuerst, Cache nur als Reserve; in der App läuft keiner) |
| `capacitor.config.json` | Paket-ID, App-Name, AdMob-Platzhalter |
| `scripts/` | `inject-config.js` (Schlüssel einsetzen, Rechtstext-Schalter), `bundle-af.js` und `af-entry.js` (AppsFlyer-Schnittstelle bündeln), `patch-android.js` (Manifest und Versionsnummer), `art_import.py`, `cat_import.py`, `floor_prep.py` (Bilder), `asset_manifest.py` (Manifest der ausgelieferten Dateien, `docs/herkunft/`), `herkunft_pakete.py` (Dateilisten gelieferter Pakete) |
| `.github/workflows/` | `android.yml` (APK, AAB, Play-Upload), `web.yml` (GitHub Pages), `kpi.yml` (tägliche AppsFlyer-Berichte) |
| `tests/` | Browser-Tests (siehe `docs/QUALITAET.md`) |

Das Spiel läuft im Browser und, mit Capacitor verpackt, als Android-App (WebView). Die nativen Dienste (Werbung, Messung, Käufe) sind Capacitor-Plugins; ohne sie fällt das Spiel auf Demo-Werbung und Browser-Preise zurück. Der Spielstand liegt in `localStorage` (Schlüssel `mergecafe_v1`, **nie ohne Rückfrage ändern**).

## 2. Versionen und Kennungen

| Angabe | Wert | Quelle |
|---|---|---|
| Spielversion | `1.5.13` | `CONFIG.version` in `www/index.html` (bei jeder Änderung erhöhen) |
| Android `versionName` | `1.0.<Build-Nr.>` | `scripts/patch-android.js`, Build-Nr. = Lauf-Nr. von GitHub Actions |
| Android `versionCode` | `<Build-Nr.>` (steigt mit jedem Lauf, wie Google Play es verlangt) | wie oben |
| Paket-ID | `io.github.johnqpowers.beantrail` | `capacitor.config.json`, `.github/workflows/android.yml`, `.github/workflows/kpi.yml`. Vom Eigentümer am 24.11.2026 gewählt (vorher `io.github.johnqpowers.mergecafe`). **Nach dem ersten Upload in Google Play nie mehr änderbar**; sie erscheint in der Store-Adresse. Eine mit der alten ID installierte App wird nicht aktualisiert, sondern bleibt daneben bestehen (eigener Spielstand). |
| App-Name | Noa's Bean Trail | `APP_NAME`, Manifest, `capacitor.config.json` |
| minSdk / targetSdk / compileSdk | 24 (Android 7.0) / 36 / 36 | Build 12. Google Play verlangt seit 31.08.2026 für neue Apps und Updates das Ziel-API-Level 36 (Android 16); erfüllt. Jährlich im August neu prüfen. |
| Play Billing Library | 9.1.0 | Build 12 (über RevenueCat) |

## 3. Android-Paket und Build

Auslöser: Push auf `main` (nur bei Änderungen an `www/`, `capacitor.config.json`, `package.json`, `assets/`, `scripts/` oder dem Workflow) oder manuell (mit Wahl des Play-Tracks, Standard `internal`).

Ablauf in `android.yml`:
1. `npm install` (Capacitor, AdMob, AppsFlyer, RevenueCat; **ohne Sperrdatei**).
2. `node scripts/inject-config.js`: setzt Schlüssel aus den GitHub-Secrets ein und stellt `CONFIG.legalReady` auf `true`, **nur** wenn `privacy.html` und `impressum.html` keine Platzhalter `[[…]]` mehr enthalten (seit 24.11.2026 der Fall).
3. `node scripts/bundle-af.js`: bündelt die AppsFlyer-Schnittstelle zu `www/af.js` (esbuild); bricht den Build ab, wenn das Paket fehlt oder die Datei zu klein ist.
4. Versionsnachweis: `npm ls` als Artefakt `versionen-<Nr>` und in der Zusammenfassung des Laufs.
5. `npx cap add android`, `capacitor-assets generate` (Icons, Startbild), `node scripts/patch-android.js` (AdMob-App-ID, VIBRATE, Hochformat-Sperre, Testmarkierung `build.json` nur für das Debug-Paket, Versionsnummern, Apostroph im Namen), `npx cap sync android`.
6. Test-APK: `assembleDebug`, als Artefakt und als öffentlich herunterladbare Vorabversion `test-apk` im GitHub-Repo. Sie enthält die Datei `build.json` und zeigt deshalb nur Googles **Test**-Anzeigen (siehe R1).
7. Store-Datei: signierte `.aab` (`npx cap build android … --androidreleasetype AAB`), nur wenn die Signier-Secrets gesetzt sind; Artefakt `noas-bean-trail-store-aab-<Nr>`.
8. Upload nach Google Play (`r0adkll/upload-google-play`), nur wenn Signier- und Play-Secrets gesetzt sind. Track `internal`, Status `draft` (änderbar über die Repository-Variable `PLAY_RELEASE_STATUS`).

Der Agent löst **nie** einen Release auf `production` aus (`CLAUDE.md`).

Google Play erzeugt aus der `.aab` die APKs je Gerät. Mindestens Android 7.0. Das Spiel ist für Handys im Hochformat gestaltet: Web-Manifest `portrait`, in der App zusätzlich `screenOrientation=portrait` am `MainActivity` (`patch-android.js`). Auf Bildschirmen ab 600 dp (Tablets, Faltgeräte) ignoriert Android 16 die Sperre; dort bleibt das Spiel spielbar, das Brett wird im Querformat nur klein (getestet bei 1024×600: Felder 26–32 px). In sehr niedrigen Fenstern zeigt das Spiel selbst den Hinweis „Bitte ins Hochformat drehen“.

## 4. Signierung

- Google Play signiert die ausgelieferten Apps selbst (**Play App Signing**, für neue Apps Pflicht, Schlüssel liegt bei Google). Unsere Pipeline signiert die `.aab` mit dem **Upload-Schlüssel** (RSA, mindestens 2048 Bit, in einer `.jks`-Datei).
- Secrets in GitHub (Namen, keine Werte): `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`, `PLAY_SERVICE_ACCOUNT_JSON`.
- Der Agent liest, nennt und ändert keine Secrets.
- **Sicherung:** Die `.jks`-Datei und die Passwörter gehören zusätzlich in eine private Sicherung des Eigentümers (nicht ins Repo). Geht der Upload-Schlüssel verloren, lässt er sich nur über den Google-Support zurücksetzen.
- Die erste `.aab` lädt der Eigentümer einmal von Hand in der Play Console hoch (danach übernimmt die Pipeline).
- Die Test-APK ist **debug-signiert** (`debuggable=true`) und nur zum Ausprobieren gedacht, nicht für die Store-Veröffentlichung.

## 5. Dienste und Bibliotheken (SDKs)

Lizenzen und Versionen: `docs/ASSETS_LIZENZEN.md`, Abschnitt 5. Datenflüsse im Detail: `docs/PRIVACY.md`.

| Dienst | Zweck | Daten (nach Einwilligung) | Start im Spiel |
|---|---|---|---|
| Google AdMob (Mobile Ads SDK) | belohnte Videos | Werbe-ID, IP, Geräte- und App-Angaben | erst nach Einwilligung, `Platform.initAds()` |
| Google UMP (User Messaging Platform) | Einwilligungsfenster, „Werbe-Einstellungen“ | Einwilligungsstatus | beim Start, vor allem anderen |
| AppsFlyer 7 (Plugin 7.0.4, JS-Kern 7.1.0) | Herkunfts- und Ereignismessung, Berichte für Almedia | Werbe-ID, IP, Geräteangaben, Ereignisse mit Zahlen | erst nach Einwilligung; stoppt beim Widerruf |
| RevenueCat | Käufe, Preise aus dem Store | anonyme Kennung, Kaufbeleg, Produkt, Land | beim Start (nur App, nur wenn `legalReady`) |
| Google Play Billing | Zahlung | (nur Google) | über RevenueCat |

Ohne Einwilligung bleiben AdMob und AppsFlyer aus; das Spiel bleibt vollständig spielbar. Ereignisse, die vor der Entscheidung entstehen, werden gemerkt (höchstens 60) und nur bei Zustimmung gesendet, sonst verworfen. Alle Ereignisnamen stehen in `docs/EVENTS.md` und werden nie umbenannt (Almedia rechnet darüber ab).

## 6. Berechtigungen (Manifest Build 12, plus VIBRATE ab v1.5.8)

| Berechtigung | Wofür | Herkunft |
|---|---|---|
| `INTERNET`, `ACCESS_NETWORK_STATE` | Werbung, Messung, Käufe | Werbe-SDK, Capacitor |
| `com.google.android.gms.permission.AD_ID` | Werbe-ID | AdMob, AppsFlyer. In der Play Console „Werbe-ID: ja“ angeben (Zweck: Werbung/Marketing und Analyse). |
| `ACCESS_ADSERVICES_AD_ID`, `_ATTRIBUTION`, `_TOPICS` | Android-Datenschutz-Schnittstellen für Werbung | Google-Werbe-SDK |
| `com.android.vending.BILLING` | In-App-Käufe | Play Billing |
| `WAKE_LOCK`, `FOREGROUND_SERVICE` | Hintergrundaufgaben der Werbe- und Messbibliotheken (WorkManager); das Spiel startet selbst keinen Vordergrunddienst | Bibliotheken |
| `com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE`, `com.samsung.android.mapsagent.permission.READ_APP_INFO`, Abfragen nach Play Store, Meta- und Samsung-Apps | Herkunft der Installation (Install-Referrer) | AppsFlyer |
| `…DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` | Schutz interner Empfänger | AndroidX |
| `VIBRATE` | Vibration (Einstellung im Spiel) | `scripts/patch-android.js` |

Nicht angefordert: Standort, Kamera, Mikrofon, Kontakte, Dateien, Benachrichtigungen, Telefon. Weitere Manifest-Fakten: `allowBackup=true` (Android-Geräte-Sicherung kann den Spielstand in das Google-Konto sichern; in der Datenschutzseite genannt), `MainActivity` ist als Start-Aktivität exportiert, der Amazon-Empfänger gehört zu RevenueCat und ist bei Google Play ohne Funktion.

## 7. Updates und Wartung

- **Ablauf je Änderung** (`CLAUDE.md`): Version erhöhen, mit Chrome und Playwright testen (Tutorial bis zur ersten Lieferung, keine Konsolenfehler), committen, nach Freigabe des Eigentümers auf `main` pushen. Der Push baut Web-Version und Android-Pakete.
- **Wege zu den Spielern:** Web-Version sofort; Android: `internal` (Tester) → geschlossener Test → Produktion. Neue Privatkonten bei Google Play brauchen vor der Produktion einen geschlossenen Test mit mindestens 12 Testern über 14 Tage (Stand der Recherche vom 24.11.2026, in der Play Console gegenprüfen). Die Freigabe auf Produktion macht der Eigentümer.
- **Spielstand bleibt kompatibel:** Neue Felder im Spielstand bekommen beim Laden Standardwerte; der Schlüssel `mergecafe_v1` bleibt. Vor Änderungen am Spielstand-Format `MC.state()` und einen alten Stand testen.
- **Rückfall bei kaputtem Build:** zuerst den letzten Commit rückgängig machen, dann den Fehler beheben (`CLAUDE.md`).
- **Jährlich:** Ziel-API-Level anheben (Capacitor-Hauptversion, AndroidX, Play Billing), Richtlinien-Änderungen von Google lesen.
- **Abhängigkeiten festschreiben:** Capacitor und RevenueCat stehen auf `latest`. Nach dem ersten erfolgreichen Build die aufgelösten Versionen aus dem Artefakt `versionen-<Nr>` in `package.json` eintragen und `package-lock.json` einchecken.

## 8. Bekannte Risiken und offene Punkte

| Nr. | Punkt | Folge | Plan |
|---|---|---|---|
| R1 | **Test-APK und echte Anzeigen** (behoben in v1.5.11, im echten Build noch ungeprüft). Die öffentliche Test-APK hätte dieselbe Konfiguration wie die Store-Datei und damit echte Anzeigen gezeigt, sobald der echte AdMob-Anzeigenblock als Secret gesetzt ist. Eigene Klicks auf echte Anzeigen zählen bei AdMob als ungültiger Verkehr und können das Konto sperren. | Konto-Risiko | `patch-android.js` legt `android/app/src/debug/assets/public/build.json` an (nur Debug-Paket). Das Spiel liest die Datei beim Start (`Platform.buildInfo`) und startet AdMob dann mit `initializeForTesting` und Googles Test-Anzeigenblock `ca-app-pub-3940256099942544/5224354917`; die Optionen zeigen „Test-Paket“. Das Store-Paket enthält die Datei nicht (Prüfpunkt in Abschnitt 9). Test im Browser mit nachgebauten Plugins: `tests/test_plattform.py`, S10 und S11. **Zusatzrisiko:** Die Test-APK sendet trotzdem Messdaten an AppsFlyer (nach Einwilligung) und verfälscht damit die KPIs. Vor dem Start der Werbung die Test-APK nicht an Fremde weitergeben oder im AppsFlyer-Dashboard nach App-Version filtern. |
| R2 | **Der Android-Build mit Version 1.5.8 und später ist nie gelaufen.** AppsFlyer-Bündelung, Einwilligungsfenster und Plugin-Versionen sind nur mit nachgebauten Plugins geprüft. | Build kann beim ersten Lauf scheitern | Erster Lauf nach Freigabe beobachten; Fehlerbild und Korrektur im Wochenbericht. |
| R3 | `latest` bei Capacitor und RevenueCat | Build ändert sich ohne eigenes Zutun | siehe Abschnitt 7 |
| R4 | Käufe und Anzeigen funktionieren erst mit echten Konten: Play Console (Produkte `starter_pack`, `gems_small`, `gems_large` als Verbrauchsgüter), RevenueCat (Produkte und Android-Schlüssel), AdMob (App und Anzeigenblock, Einwilligungsnachricht), AppsFlyer (Dev-Key) | ohne sie bleibt alles aus oder zeigt Testwerte | Eigentümer legt Konten an und trägt die Secrets ein (Liste in `README.md`) |
| R5 | Belohnungen werden im Spiel auf dem Gerät gutgeschrieben (kein Server). Manipulierte Geräte können sich Diamanten holen. | geringer Schaden bei einem reinen Offline-Spiel | akzeptiert; Käufe prüft RevenueCat serverseitig, die Gutschrift erfolgt trotzdem lokal |
| R6 | AdMob-Umsatz je Anzeige geht nicht an AppsFlyer; der Werbe-ROAS muss aus dem AdMob-Bericht von Hand ergänzt werden | KPI „D7-ROAS“ ist nur teilweise automatisch | im Wochenbericht ergänzen |
| R7 | Pflichtangaben und Konten (Impressum, Datenschutz, Play-Konto) fehlen noch | Werbung, Käufe und Messung bleiben in der App gesperrt (`legalReady`) | Eigentümer liefert Angaben |

## 9. Nach dem ersten echten Build prüfen

- [ ] Lauf grün; Artefakte `noas-bean-trail-test-apk-<Nr>`, `noas-bean-trail-store-aab-<Nr>`, `versionen-<Nr>` vorhanden.
- [ ] Test-APK auf einem echten Gerät: Start, Tutorial bis zur ersten Lieferung, Vibration, Ton, Neustart mit erhaltenem Spielstand.
- [ ] Ohne Rechtstexte: Hinweis „Testversion“ in den Optionen, keine Werbung, keine Käufe.
- [ ] Mit Rechtstexten, Test-APK: Optionen zeigen „Test-Paket“, das Belohnungsvideo ist eine Google-Testanzeige (Aufschrift „Test Ad“); Einwilligungsfenster erscheint (Gerät im EWR), Ablehnen sperrt Werbung und Messung, Zustimmen startet beide.
- [ ] Store-Datei enthält **keine** `build.json`: `unzip -l noas-bean-trail.aab | grep build.json` (bzw. `bundletool`) liefert nichts; in den Optionen der Store-Fassung fehlt „Test-Paket“.
- [ ] Handy im Hochformat gesperrt (Drehen ändert nichts); Tablet im Querformat: Spiel bedienbar.
- [ ] AppsFlyer-Dashboard: Installation und `session_start` erscheinen nur nach Zustimmung.
- [ ] Käufe mit Lizenztester (Play Console): Preis aus dem Store, Kauf, Gutschrift, `purchase` mit Umsatz im Dashboard.
- [ ] Manifest der `.aab` gegen Abschnitt 6 prüfen (keine zusätzlichen Berechtigungen); Seitengröße 16 KB für native Bibliotheken laut Play-Anforderung prüfen.
- [ ] Hochgeladene Datei in der Play Console: App-Integrität, Signatur, Gerätekatalog.

## Quellen (Stand 24.11.2026)
- Google Play, Anforderungen an das Ziel-API-Level: https://developer.android.com/google/play/requirements/target-sdk
- Google Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Android App Bundle, häufige Fragen: https://developer.android.com/guide/app-bundle/faq
