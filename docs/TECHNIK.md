# Technische Dokumentation – Noa's Bean Trail

Stand: 25.11.2026. Spielversion 1.5.19 (Push auf `main` am 25.11.2026). Der Android-Build Nr. 13 (`versionName 1.0.13`, `versionCode 13`) ist am 24.11.2026 im CI durchgelaufen (Lauf 45487193159, Commit 48c1bc7); die Angaben zu Berechtigungen und Bibliotheken stammen aus seinem Manifest. Die Änderungen ab v1.5.8 (Einwilligung, AppsFlyer 7, Store-Preise, Sperre, Hochformat-Sperre, Test-Anzeigen im Debug-Paket) stecken damit erstmals in einem echten Android-Build und sind im Paket nachgewiesen (Paket-ID, Berechtigungen, Hochformat-Sperre, Testmarkierung, Signatur). **Auf einem Gerät oder Emulator ist der Build noch nicht gelaufen.** Noa's Pro gibt es seit v1.5.14 (Abschnitt 5, Risiken R8 bis R11): Build 16 (Lauf 45497813780, Commit 21a6a4b) enthält den Pro-Ablauf, Build 17 (Lauf 45498986208, Commit b89a630, Spielversion 1.5.15) zusätzlich das RevenueCat-Paywall-Plugin. **Seit v1.5.16 ist Pro ausgeschaltet** (Entscheidung 24.11.2026, `docs/MONETARISIERUNG.md`, Abschnitt 11): Schalter `CONFIG.revenuecat.proEnabled: false`, das Paywall-Plugin ist wieder ausgebaut. Build 18 (Commit 2855e02, Spielversion 1.5.16) ist durchgelaufen: Test-APK 34 092 481 Bytes (Build 17 mit Plugin: 47 MB), die Namen `presentPaywallIfNeeded` und `PaywallActivity` stehen nicht mehr im Paket, Berechtigungen unverändert gegenüber Abschnitt 6 (erneut gelesen).

## 1. Aufbau

| Teil | Inhalt |
|---|---|
| `www/index.html` | das komplette Spiel in einer Datei (HTML, CSS, JavaScript, Schriften als Base64) |
| `www/art/`, `www/icons/` | Bilder (WebP) und Icons: Teile, Automaten, Figuren, Gäste, Böden `f*`, Rahmen `frame*`, Vollbild-Hintergründe je Welt `b0` bis `b8` (seit 1.5.19 alle neun, ersetzen gezeichnete Szene und Boden; auf Handys die ganze Breite, im breiten Fenster der Web-Version 520 px mit verwischter Kopie als Rand), Stadtrahmen `frame1` bis `frame8`, Einzugs-Posen, Effekte; Katze Mocha nur noch als Ruhebild `cat/c01` bis `c03` (drei Bilder ≈ 1,6 MB entpackt statt 22 Bildern ≈ 12 MB, deshalb weniger Arbeitsspeicher) |
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
| Spielversion | `1.5.19` | `CONFIG.version` in `www/index.html` (bei jeder Änderung erhöhen) |
| Android `versionName` | `1.0.<Build-Nr.>` | `scripts/patch-android.js`, Build-Nr. = Lauf-Nr. von GitHub Actions |
| Android `versionCode` | `<Build-Nr.>` (steigt mit jedem Lauf, wie Google Play es verlangt) | wie oben |
| Paket-ID | `io.github.johnqpowers.beantrail` | `capacitor.config.json`, `.github/workflows/android.yml`, `.github/workflows/kpi.yml`. Vom Eigentümer am 24.11.2026 gewählt (vorher `io.github.johnqpowers.mergecafe`). **Nach dem ersten Upload in Google Play nie mehr änderbar**; sie erscheint in der Store-Adresse. Eine mit der alten ID installierte App wird nicht aktualisiert, sondern bleibt daneben bestehen (eigener Spielstand). |
| App-Name | Noa's Bean Trail | `APP_NAME`, Manifest, `capacitor.config.json` |
| minSdk / targetSdk / compileSdk | 24 (Android 7.0) / 36 / 36 | Build 13 (minSdk und targetSdk im Manifest gelesen). Google Play verlangt seit 31.08.2026 für neue Apps und Updates das Ziel-API-Level 36 (Android 16); erfüllt. Jährlich im August neu prüfen. |
| Play Billing Library | 9.1.0 | Build 13 (über RevenueCat; im Manifest gelesen) |

## 3. Android-Paket und Build

Auslöser: Push auf `main` (nur bei Änderungen an `www/`, `capacitor.config.json`, `package.json`, `assets/`, `scripts/` oder dem Workflow) oder manuell (mit Wahl des Play-Tracks, Standard `internal`).

Ablauf in `android.yml`:
1. `npm install` (Capacitor, AdMob, AppsFlyer, RevenueCat-Kern-Plugin; **ohne Sperrdatei**). Das Paywall-Plugin `@revenuecat/purchases-capacitor-ui` ist seit 1.5.16 nicht mehr dabei (Pro ausgeschaltet).
2. `node scripts/inject-config.js`: setzt Schlüssel aus den GitHub-Secrets ein und stellt `CONFIG.legalReady` auf `true`, **nur** wenn `privacy.html` und `impressum.html` keine Platzhalter `[[…]]` mehr enthalten (seit 24.11.2026 der Fall).
3. `node scripts/bundle-af.js`: bündelt die AppsFlyer-Schnittstelle zu `www/af.js` (esbuild); bricht den Build ab, wenn das Paket fehlt oder die Datei zu klein ist.
4. Versionsnachweis: `npm ls` als Artefakt `versionen-<Nr>` und in der Zusammenfassung des Laufs.
5. `npx cap add android`, `capacitor-assets generate` (Icons, Startbild), `node scripts/patch-android.js` (AdMob-App-ID, VIBRATE, Hochformat-Sperre, Testmarkierung `build.json` nur für das Debug-Paket, dort bei gesetztem Secret `REVENUECAT_TEST_KEY` auch der Test-Store-Schlüssel (R8), minSdk mindestens 24, Versionsnummern, Apostroph im Namen), `npx cap sync android`.
6. Test-APK: `assembleDebug`, als Artefakt und als öffentlich herunterladbare Vorabversion `test-apk` im GitHub-Repo. Sie enthält die Datei `build.json` und zeigt deshalb nur Googles **Test**-Anzeigen (siehe R1) und, mit dem Secret `REVENUECAT_TEST_KEY`, die simulierten Käufe des RevenueCat-Test-Stores (siehe R8). Der Gradle-Aufruf läuft über `scripts/retry-net.sh`: bis zu drei Versuche, aber nur bei Netzwerkfehlern (HTTP 429/5xx, Zeitüberschreitung), nie bei Codefehlern (siehe R11).
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
| RevenueCat (Kern-Plugin) | Käufe und Preise aus dem Store (Diamanten-Pakete, Startpaket); Pro-Abo (Entitlement `noa_s_bean_trail_pro`) ist **ausgeschaltet** | anonyme Kennung, Kaufbeleg, Produkt, Land | beim Start (nur App, nur wenn `legalReady`) |
| Google Play Billing | Zahlung | (nur Google) | über RevenueCat |

Ohne Einwilligung bleiben AdMob und AppsFlyer aus; das Spiel bleibt vollständig spielbar. Ereignisse, die vor der Entscheidung entstehen, werden gemerkt (höchstens 60) und nur bei Zustimmung gesendet, sonst verworfen. Alle Ereignisnamen stehen in `docs/EVENTS.md` und werden nie umbenannt (Almedia rechnet darüber ab).

**Noa's Pro (seit v1.5.14, ausgeschaltet seit v1.5.16).** Schalter `CONFIG.revenuecat.proEnabled` (`Platform.proOn()`): Bei `false` ist Pro unsichtbar und inaktiv, das Spiel fragt weder Kundeninfo noch Angebote ab, hört keine Änderungsmeldungen, zeigt weder Shop-Karte noch Optionszeilen, gibt keinen Pro-Tagesbonus und sendet keine Pro-Ereignisse; Paywall, Abo-Verwaltung, Wiederherstellen und Paketkauf melden „aus“. Das Paywall-Plugin ist nicht im Paket. Die folgende Beschreibung gilt für den Fall, dass Pro wieder eingeschaltet wird (Bedingungen: `docs/MONETARISIERUNG.md`, Abschnitt 11). Pro ist der Zustand des RevenueCat-Entitlements `noa_s_bean_trail_pro` (`CONFIG.revenuecat.entitlement`). Die Quelle ist immer RevenueCat: Das Spiel fragt beim Start, bei der Rückkehr in die App, nach einer Änderungsmeldung des SDK und nach Paywall oder Wiederherstellen; im Spielstand steht nur der Tag des letzten Tagesgeschenks. Das Angebot kommt aus dem aktuellen Offering. Pakete werden über den Pakettyp (Monat, Jahr, Lifetime) erkannt, nicht über feste Produkt-IDs, und ohne geladenes Offering bleibt die Pro-Karte unsichtbar. Die Paywall zeigt das RevenueCat-UI-Plugin (`presentPaywallIfNeeded`; muss dafür wieder eingebaut werden), die Abo-Verwaltung das Customer Center (`presentCustomerCenter`); fehlt das Plugin oder wirft es einen Fehler, zeigt das Spiel eine eigene Paketliste bzw. einen Link zur Abo-Seite von Google Play. Vorteile (**Vorschlag, vom Eigentümer zu bestätigen**): Belohnungen ohne Video (gleiche Tageslimits) und täglich 5 Diamanten (nach dem Tutorial, einmal je UTC-Tag). Neue Ereignisse: `paywall_open`, `pro_start`, `pro_restore`; der erste Pro-Kauf zählt als `purchase` und `first_purchase`. Einzelheiten: `docs/MONETARISIERUNG.md`, Abschnitt Noa's Pro.

## 6. Berechtigungen (Manifest Build 13, am 24.11.2026 aus der Test-APK gelesen)

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

Nicht angefordert: Standort, Kamera, Mikrofon, Kontakte, Dateien, Benachrichtigungen, Telefon. Weitere Manifest-Fakten: `allowBackup=true` (Android-Geräte-Sicherung kann den Spielstand in das Google-Konto sichern; in der Datenschutzseite genannt), `MainActivity` ist als Start-Aktivität exportiert und auf Hochformat gesperrt (`screenOrientation=portrait`), der Amazon-Empfänger gehört zu RevenueCat und ist bei Google Play ohne Funktion. Ohne Secret trägt das Paket Googles öffentliche Beispiel-App-ID von AdMob (`ca-app-pub-3940256099942544~3347511713`); das Debug-Paket enthält zusätzlich `assets/public/build.json` (siehe R1).

## 7. Updates und Wartung

- **Ablauf je Änderung** (`CLAUDE.md`): Version erhöhen, mit Chrome und Playwright testen (Tutorial bis zur ersten Lieferung, keine Konsolenfehler), committen, nach Freigabe des Eigentümers auf `main` pushen. Der Push baut Web-Version und Android-Pakete.
- **Wege zu den Spielern:** Web-Version sofort; Android: `internal` (Tester) → geschlossener Test → Produktion. Neue Privatkonten bei Google Play brauchen vor der Produktion einen geschlossenen Test mit mindestens 12 Testern über 14 Tage (Stand der Recherche vom 24.11.2026, in der Play Console gegenprüfen). Die Freigabe auf Produktion macht der Eigentümer.
- **Spielstand bleibt kompatibel:** Neue Felder im Spielstand bekommen beim Laden Standardwerte; der Schlüssel `mergecafe_v1` bleibt. Vor Änderungen am Spielstand-Format `MC.state()` und einen alten Stand testen.
- **Rückfall bei kaputtem Build:** zuerst den letzten Commit rückgängig machen, dann den Fehler beheben (`CLAUDE.md`).
- **Jährlich:** Ziel-API-Level anheben (Capacitor-Hauptversion, AndroidX, Play Billing), Richtlinien-Änderungen von Google lesen.
- **Abhängigkeiten festschreiben:** Capacitor und RevenueCat stehen auf `latest`. Nach dem ersten erfolgreichen Build die aufgelösten Versionen aus dem Artefakt `versionen-<Nr>` in `package.json` eintragen und `package-lock.json` einchecken. Wird das Paywall-Plugin (`@revenuecat/purchases-capacitor-ui`) wieder eingebaut, muss es dieselbe Version wie das Kern-Plugin (`@revenuecat/purchases-capacitor`) haben; beide werden gemeinsam festgeschrieben.

## 8. Bekannte Risiken und offene Punkte

| Nr. | Punkt | Folge | Plan |
|---|---|---|---|
| R1 | **Test-APK und echte Anzeigen** (behoben in v1.5.11; im Build 13 liegt die Testmarkierung `build.json` in der Test-APK, die Anzeige selbst ist auf einem Gerät noch ungeprüft). Die öffentliche Test-APK hätte dieselbe Konfiguration wie die Store-Datei und damit echte Anzeigen gezeigt, sobald der echte AdMob-Anzeigenblock als Secret gesetzt ist. Eigene Klicks auf echte Anzeigen zählen bei AdMob als ungültiger Verkehr und können das Konto sperren. | Konto-Risiko | `patch-android.js` legt `android/app/src/debug/assets/public/build.json` an (nur Debug-Paket). Das Spiel liest die Datei beim Start (`Platform.buildInfo`) und startet AdMob dann mit `initializeForTesting` und Googles Test-Anzeigenblock `ca-app-pub-3940256099942544/5224354917`; die Optionen zeigen „Test-Paket“. Das Store-Paket enthält die Datei nicht (Prüfpunkt in Abschnitt 9). Test im Browser mit nachgebauten Plugins: `tests/test_plattform.py`, S10 und S11. **Zusatzrisiko:** Die Test-APK sendet trotzdem Messdaten an AppsFlyer (nach Einwilligung) und verfälscht damit die KPIs. Vor dem Start der Werbung die Test-APK nicht an Fremde weitergeben oder im AppsFlyer-Dashboard nach App-Version filtern. |
| R2 | **Der Android-Build ab Version 1.5.8 ist am 24.11.2026 erstmals durchgelaufen (Build 13), aber auf keinem Gerät gelaufen.** AppsFlyer-Bündel (`www/af.js`) und Testmarkierung sind im Paket nachgewiesen; Einwilligungsfenster, AppsFlyer-Start, Test-Anzeigen und Käufe lassen sich nur auf einem Gerät prüfen. | Fehler zeigen sich erst auf dem Gerät | Eigentümer installiert die Test-APK (neue Paket-ID, läuft neben der alten App) und meldet Auffälligkeiten; Ergebnis im Wochenbericht. |
| R3 | `latest` bei Capacitor und RevenueCat | Build ändert sich ohne eigenes Zutun | siehe Abschnitt 7 |
| R4 | Käufe und Anzeigen funktionieren erst mit echten Konten: Play Console (Produkte `starter_pack`, `gems_small`, `gems_large` als Verbrauchsgüter), RevenueCat (Produkte und Android-Schlüssel), AdMob (App und Anzeigenblock, Einwilligungsnachricht), AppsFlyer (Dev-Key) | ohne sie bleibt alles aus oder zeigt Testwerte | Eigentümer legt Konten an und trägt die Secrets ein (Liste in `README.md`) |
| R5 | Belohnungen werden im Spiel auf dem Gerät gutgeschrieben (kein Server). Manipulierte Geräte können sich Diamanten holen. | geringer Schaden bei einem reinen Offline-Spiel | akzeptiert; Käufe prüft RevenueCat serverseitig, die Gutschrift erfolgt trotzdem lokal |
| R6 | AdMob-Umsatz je Anzeige geht nicht an AppsFlyer; der Werbe-ROAS muss aus dem AdMob-Bericht von Hand ergänzt werden | KPI „D7-ROAS“ ist nur teilweise automatisch | im Wochenbericht ergänzen |
| R7 | Pflichtangaben und Konten (Impressum, Datenschutz, Play-Konto) fehlen noch | Werbung, Käufe und Messung bleiben in der App gesperrt (`legalReady`) | Eigentümer liefert Angaben |
| R8 | **RevenueCat-Test-Store-Schlüssel (`test_…`).** Er lässt die App laut RevenueCat in jedem Release-Build (also in jedem Play-Track) beim Start absichtlich abstürzen. Er darf nie in `REVENUECAT_ANDROID_KEY` und nie in die Store-Datei. | Absturz beim Start für alle Spieler, falls doch | Er liegt nur im Secret `REVENUECAT_TEST_KEY` und kommt über `patch-android.js` ausschließlich in `build.json` des Debug-Pakets (öffentliche Test-APK; es ist ein öffentlicher SDK-Schlüssel, Käufe sind nur simuliert). Das Spiel ignoriert `test_`-Schlüssel außerhalb des Debug-Pakets (`tests/test_plattform.py`, S17), `inject-config.js` warnt bei einem `test_`-Schlüssel in `REVENUECAT_ANDROID_KEY`. `REVENUECAT_ANDROID_KEY` muss ein echter `goog_…`-Schlüssel sein. Prüfpunkt in Abschnitt 9. |
| R9 | *(ruht seit 1.5.16, gilt beim Wiedereinschalten von Pro)* **Paywall-Plugin und Pro-Ablauf nur im Paket, nicht auf einem Gerät geprüft.** Build 17 ist durchgelaufen (APK 47 MB statt 34 MB, Jetpack Compose; neue Activities `PaywallActivity` und `CustomerCenterActivity`, keine neuen Berechtigungen; die Namen `presentPaywallIfNeeded` und `presentCustomerCenter` stehen im Paket). Aussehen der Paywall, Form der Ergebnisse und der Kundeninfo-Meldung sind nur aus der Dokumentation bekannt; das Spiel liest den Pro-Zustand deshalb immer aus dem Entitlement und nicht aus Ergebnistexten und hat eine eigene Paketliste als Ausweichlösung. Kern- und Paywall-Plugin stehen beide auf `latest` und können auseinanderlaufen. | Paywall bleibt leer oder zeigt Fehler | Gerätetest mit Test Store (Abschnitt 9); bei Build-Fehler zuerst den Commit mit dem Plugin zurücknehmen (`CLAUDE.md`). |
| R10 | *(ruht seit 1.5.16; die Diamanten-Pakete brauchen weiterhin Produkte und Android-Schlüssel, siehe R4)* **RevenueCat-Dashboard noch nicht eingerichtet** (Stand: unbekannt, nicht vom Agenten prüfbar). Ohne aktuelles Angebot mit Paketen, Entitlement `noa_s_bean_trail_pro` an allen drei Produkten und eine gestaltete Paywall bleibt die Pro-Karte unsichtbar bzw. die Paywall leer. Ob das Customer Center im jetzigen RevenueCat-Tarif nutzbar ist, ist nicht geprüft. | Pro nicht kaufbar | Eigentümer richtet das Dashboard ein (Liste in `docs/MONETARISIERUNG.md`, Noa's Pro; Paywall mit Preis, Laufzeit, automatischer Verlängerung und Kündigungshinweis). Ohne Customer Center zeigt das Spiel den Link zur Abo-Seite von Google Play. |
| R11 | **Zufallsfehler der CI-Umgebung.** Lauf 14 scheiterte an HTTP 429 von Maven Central (Gradle-Bausteine); die GitHub-Pages-Veröffentlichung scheiterte in den Läufen 18 und 20 („Fetching artifact metadata failed“: Artefakt nach dem Hochladen noch nicht abrufbar). Beides war nicht der Code. | roter Lauf ohne Codefehler | Gradle-Aufrufe wiederholen sich bei Netzwerkfehlern selbst (`scripts/retry-net.sh`). Pages: **neuen** Lauf per `workflow_dispatch` von `web.yml` starten; ein Neustart nur des fehlgeschlagenen Jobs scheitert am doppelten Artefakt. Ursache: GitHub listet das Artefakt etwa eine Sekunde nach dem Hochladen noch nicht („Found 0 artifact(s)“, das Hochladen selbst war erfolgreich). Fast alle Push-Läufe scheiterten so (18, 20, 22, 23, 25), die per `workflow_dispatch` gestarteten liefen durch (21, 24). Seit 25.11.2026 baut `web.yml` in zwei Jobs (Bauen, Veröffentlichen) mit 20 Sekunden Wartezeit vor `deploy-pages`; scheitert es trotzdem, bleibt der neue Lauf per `workflow_dispatch` der Weg. Erster Push-Lauf mit dem Umbau: Lauf 26, grün (ein Lauf ist noch kein Beweis). |

## 9. Nach dem ersten echten Build prüfen

- [ ] Lauf grün; Artefakte `noas-bean-trail-test-apk-<Nr>`, `noas-bean-trail-store-aab-<Nr>`, `versionen-<Nr>` vorhanden.
- [ ] Test-APK auf einem echten Gerät: Start, Tutorial bis zur ersten Lieferung, Vibration, Ton, Neustart mit erhaltenem Spielstand.
- [ ] Ohne Rechtstexte: Hinweis „Testversion“ in den Optionen, keine Werbung, keine Käufe.
- [ ] Mit Rechtstexten, Test-APK: Optionen zeigen „Test-Paket“, das Belohnungsvideo ist eine Google-Testanzeige (Aufschrift „Test Ad“); Einwilligungsfenster erscheint (Gerät im EWR), Ablehnen sperrt Werbung und Messung, Zustimmen startet beide.
- [ ] Store-Datei enthält **keine** `build.json`: `unzip -l noas-bean-trail.aab | grep build.json` (bzw. `bundletool`) liefert nichts; in den Optionen der Store-Fassung fehlt „Test-Paket“.
- [ ] Handy im Hochformat gesperrt (Drehen ändert nichts); Tablet im Querformat: Spiel bedienbar.
- [ ] AppsFlyer-Dashboard: Installation und `session_start` erscheinen nur nach Zustimmung.
- [ ] Käufe mit Lizenztester (Play Console): Preis aus dem Store, Kauf, Gutschrift, `purchase` mit Umsatz im Dashboard.
- [ ] *(nur bei eingeschaltetem Pro, Abschnitt 11 der Monetarisierungsdoku)* Noa's Pro, Test-APK mit gesetztem Secret `REVENUECAT_TEST_KEY` und eingerichtetem RevenueCat-Dashboard: Pro-Karte im Shop und Zeile in den Optionen; Paywall öffnet; Kauf im Test Store (simulierter Dialog) schaltet Pro frei (Belohnung ohne Video, +5 Diamanten einmal je Tag); Abbrechen und Fehler zeigen keinen Absturz; „Käufe wiederherstellen“; „Abo verwalten“ (Customer Center oder Link zu Google Play). Optionen zeigen „Test-Paket“.
- [ ] Pro ausgeschaltet (Auslieferungszustand): im Shop keine Pro-Karte, in den Optionen weder „Noa's Pro“ noch „Käufe wiederherstellen“.
- [ ] Die **Store-Datei** enthält keinen RevenueCat-Schlüssel mit `test_` (R8) und `REVENUECAT_ANDROID_KEY` beginnt mit `goog_`.
- [ ] Manifest der `.aab` gegen Abschnitt 6 prüfen (keine zusätzlichen Berechtigungen); Seitengröße 16 KB für native Bibliotheken laut Play-Anforderung prüfen.
- [ ] Hochgeladene Datei in der Play Console: App-Integrität, Signatur, Gerätekatalog.

## Quellen (Stand 25.11.2026)
- Google Play, Anforderungen an das Ziel-API-Level: https://developer.android.com/google/play/requirements/target-sdk
- Google Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Android App Bundle, häufige Fragen: https://developer.android.com/guide/app-bundle/faq
