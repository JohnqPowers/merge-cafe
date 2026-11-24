# Test- und Qualitätsbericht – Noa's Bean Trail

Stand: 25.11.2026. Spielversion 1.5.18 (Push auf `main` am 25.11.2026). Der Bericht trennt streng zwischen **geprüft** (mit Messwert oder Testprotokoll) und **nicht geprüft**. Wo etwas nicht geprüft ist, steht das da, und im Abschnitt 8 steht, wie es nachgeholt wird.

## 1. Kurzfazit

| Bereich | Stand |
|---|---|
| Automatische Browser-Tests (Chrome, Handy-Fenstergrößen) | **grün**: 24/24 (beide Fenstergrößen), 115/115, 11/11, 20/20, 91/91, 16/16, dazu Katze 11/11, Hintergründe 7/7 und Wortwahl 12/12 (Abschnitt 3) |
| Echter Android-Build ab Version 1.5.8 | **durchgelaufen** am 24.11.2026 (CI, Build 13 bis 18; Build 17 enthielt Pro und Paywall-Plugin (Spielversion 1.5.15), Build 18 (Commit 2855e02, Spielversion 1.5.16) ist ohne Plugin gebaut und kleiner: 34,1 MB statt 47 MB; Build 14 scheiterte an einem Netzwerkfehler von Maven Central, nicht am Code); Paket geprüft, aber **auf keinem Gerät gelaufen** (Abschnitt 6, Punkt Q1) |
| Echte Geräte | Der Eigentümer hat Test-APKs bis Build 12 selbst gespielt (Rückmeldungen stehen in `reports/weekly/`). **Gerätemodell, Android-Version und Build sind nicht dokumentiert**, es gibt kein Gerätetest-Protokoll. Die Lücke ist offen. Build 13 (neue Paket-ID) liegt dem Eigentümer seit dem 24.11.2026 vor, die Rückmeldung steht aus. |
| Abstürze | **Keine Daten.** Im Spiel ist keine Absturzmeldung eingebaut, und die App war nie im Store. Bekannte Fehler stammen aus Tests und Rückmeldungen. |
| Werbung, Käufe, Messung, Einwilligung | nur mit **nachgebauten Plugins** geprüft, nie mit echten Konten (Abschnitt 6, Q3) |
| Leistung | im Browser mit gedrosselter CPU gemessen, **nicht auf echten Handys** (Abschnitt 4) |

Empfehlung: Für den internen Test (`internal`) und einen geschlossenen Test reicht der jetzige Stand, sobald der erste echte Build grün ist. Für die Produktion fehlen die Gerätetests und die Werte aus Android vitals (Abschnitt 7).

## 2. Testumgebung und Methode

- Chrome for Testing 153 (headless) mit Playwright (Python), lokaler Webserver auf `www/`. Fenstergrößen wie Handys: 390×844 und 360×640 (Standard der Tests), dazu 320×568, 412×915, 768×1024, 810×1080, 844×390 (quer), 1024×600 und 1280×800 für Sonderfälle.
- Capacitor-Plugins (AdMob, AppsFlyer, RevenueCat, Einwilligung) sind im Test **nachgebaut** (`tests/test_plattform.py`). Sie prüfen die Reihenfolge und die Aufrufe des Spiels, nicht das Verhalten der echten Bibliotheken.
- Leistungsmessungen mit gedrosselter CPU (4× bis 8×), um ein Einsteiger-Handy nachzustellen. Das ist eine Näherung.
- Der Spielstand `tests/state.json` (Level 12, Paris) wird für Tests ab Level 12 eingespielt.
- Konsolenfehler und fehlende Bilder zählen als Testfehler.

## 3. Automatische Tests (Lauf vom 25.11.2026, Version 1.5.17; zu 1.5.18 nur Icon-Größe, Kurzlauf grün)

| Datei | Ergebnis | Inhalt |
|---|---|---|
| `tests/test_gesamt.py` | **24/24** bei 390×844 und bei 360×640 | Start, Profil, Tutorial bis zur ersten Lieferung (inkl. Merge), Spiel bis Level 6 (dabei Stadtwechsel Hamburg → Wien bei Level 5), Geschenk-Fach, Verdoppeln per Demo-Werbung, „Keine Energie“-Fenster, Energie-Werbung (Zähler), Auffüllen mit Diamanten, fehlende Artikel kaufen, Tagesbonus, Münzen-Verdoppeln-Chip, Erklär-Fenster „Diamanten“, Ausbau kaufen, Neustart mit erhaltenem Spielstand, Chancen-Anzeige im Diamanten-Fenster, keine Konsolenfehler |
| `tests/test_plattform.py` | **115/115** | Einwilligung vor Werbung und Messung, Ablehnen/Zustimmen/Widerruf, Werbe-Einstellungen, Ereignis-Warteschlange (verwerfen oder senden), Store-Preise statt Platzhalter, Kauf und Gutschrift, Kauf abgebrochen, Browser-Variante ohne Plugins, **Sperre bei unvollständigen Rechtstexten** (S9), **Debug-Paket mit Test-Anzeigenblock** (S10), **Store-Paket ohne Testmarkierung** (S11), **Noa's Pro** (S12 bis S18: Paywall und Kauf, Pro schon beim Start, Kundeninfo-Meldung in beiden Formen, Tagesgeschenk einmal je Tag, eigene Paketliste, Abbruch auch als Fehlercode, Wiederherstellen, Customer Center und Ausweich-Hinweis, Schlüsselregeln für `test_`-Schlüssel, Fehlerfälle; die Pro-Tests laufen mit eingeschaltetem Schalter), **Auslieferungszustand** (S19: Pro ausgeschaltet, im Shop und in den Optionen ist nichts davon sichtbar, Käufe laufen weiter) |
| `tests/test_ausrichtung.py` | **11/11** | Dreh-Hinweis nur bei Querformat und sehr niedrigen Fenstern (844×390, 700×520), nicht bei Handy hochkant und nicht bei Tablets (1024×600, 1280×800, 810×1080); Deutsch und Englisch; Hinweis deckt alles ab und liegt oben |
| `tests/test_spielstand.py` | **20/20** | Update-Sicherheit des Spielstands: alter, unvollständiger Spielstand lädt (neue Felder bekommen Standardwerte, alte Emoji-Figur wird auf die neue Kennung umgestellt), Zusatzfelder bleiben, kaputter Text, fremde Version, falsche Brettgröße, leeres Profil und unbekannte Figur starten ein neues Spiel bzw. Ersatzwerte ohne Absturz, Level-12-Stand lädt bei 360×640 |
| `tests/test_store.py` | **91/91** | Store-Unterlagen ohne Browser: Titel höchstens 30, Kurzbeschreibung 80, Beschreibung 4000 Zeichen, Alt-Texte höchstens 140; keine Werbewörter, Emojis oder Fremdnamen im Titel; Zahlen im Text (22 Leckereien, 3 Ketten, 9 Welten, 12 Figuren, 7 Bonus-Tage, Automaten, Städte) stimmen mit `www/index.html`; Icon 512×512 mit Alpha, Feature-Grafiken 1024×500 ohne Alpha, 6 Screenshots je Sprache 1080×1920 ohne Alpha, deutsche und englische Fassung verschieden, keine Reste mit altem Namen in `store/`. Mit absichtlich falschem Text geprüft: schlägt dann fehl. |
| `tests/test_herkunft.py` | **16/16** | Herkunftsnachweise ohne Browser: Manifest der ausgelieferten Dateien (`docs/herkunft/ausgelieferte_dateien.csv`) ist aktuell und stimmt mit den Dateien überein (Pfad, Größe, SHA-256), jedes Spielbild hat eine Quelle, Verzeichnis des Eigentümers und Paketlisten sind stimmig, keine Namen anderer Spiele in den Herkunftsdateien |
| `tests/test_katze.py` | **11/11** | Katze Mocha (ab 1.5.17 nur Ruhebild): Bild geladen, nur `c01` bis `c03` im Netz, keine Flug-Ebene, Antippen, fehlende Bilder (gezeichnete Katze bleibt), 360×640, 5 Gästeplätze (Katze ausgeblendet), Dateien in `www/art/cat`. |
| `tests/test_hintergrund.py` | **7/7** | Vollbild-Hintergrund je Welt (`art/b<N>.webp`): mit Bild ersetzt er Szene und Boden, ohne Bild bleibt alles wie zuvor, andere Welten unberührt. |
| `tests/test_wortwahl.py` | **12/12** | Wortwahl und Anzeige ab 1.5.17: „Take-away“ mit Take-away-Symbol statt „Verkaufen“ und Mülltonne, „Bessere Artikel“ mit Chance in Prozent (10 % → 15 % bis 35 %), Hinweis „Stufe 2!“ beim Glückstreffer und keiner ohne, Stufe 1 ohne Zahl auf dem Teil; Deutsch und Englisch, keine Konsolenfehler. |

**Zusatzprüfung zu 1.5.13:** `scripts/inject-config.js` wurde auf einer Kopie von `www/` ausgeführt (Rechtstexte ohne Platzhalter, deshalb `legalReady: true`). Die Seite lädt in Chrome (390×844) ohne Konsolen- oder Seitenfehler, Impressum und Datenschutz zeigen die Anbieterangaben ohne Platzhalter. Das ist die Browser-Schicht des CI-Builds.

**Prüfung des echten Pakets (Build 13, 24.11.2026):** Der CI-Lauf zum Commit 48c1bc7 ist durchgelaufen, die Web-Veröffentlichung auch. Die Test-APK (`noas-bean-trail-test.apk`, 34 085 493 Bytes, SHA-256 `31952a8e163e74d2830cc1807b797740c37264778ea98cc07ca5f14ffca8a01c`) wurde aus dem Release geladen und geöffnet. Sie enthält: Paket-ID `io.github.johnqpowers.beantrail` (die alte kommt nicht vor), `versionName 1.0.13`, `versionCode 13`, minSdk 24, targetSdk 36; `index.html` mit Version 1.5.13 und `legalReady: true`; Impressum und Datenschutz ohne Platzhalter, mit Name und E-Mail-Adresse; `www/af.js` (AppsFlyer) und `build.json` (Testmarkierung, Googles Test-Anzeigenblock); dieselben Berechtigungen wie in `docs/TECHNIK.md`, Abschnitt 6, einschließlich `VIBRATE`; `MainActivity` auf Hochformat gesperrt; Signaturblock vorhanden. Das Manifest wurde mit einem eigenen Leseprogramm aus der Datei gelesen, nicht mit den Android-Werkzeugen. **Nicht geprüft** ist alles, was ein Gerät braucht: Installation neben der alten App, Einwilligungsfenster, AppsFlyer-Start, Test-Anzeigen, Käufe, Zurück-Taste, Drehung (Q1).

Frühere Einzelprüfungen, die **nicht** im Repo liegen (Wegwerf-Skripte, damals bei 390×844 und 360×640 bestanden): Figuren und Gäste 13/13, Level-Chips 18/18, Ablauf Onboarding → Einzug → Tutorial 34/34, Namenstest 12/12, Sie sind in den Wochenberichten belegt, aber nicht wiederholbar, bis sie ins Repo wandern.

Aufruf: siehe `tests/README.md`.

## 4. Leistung (Messwerte, Chrome mit gedrosselter CPU)

| Messung | Ergebnis | Quelle |
|---|---|---|
| Start, CPU 4× | erstes Bild nach ca. 0,4 s (vorher 0,8 s); Startbild im Leerlauf 60 fps | Wochenbericht v1.5.0 |
| Spielfluss (Ziehen, Mergen, Automat, Lieferung), CPU 8× | Frames über 33 ms: 64–71 → 19–23; mittlere Frame-Zeit 25–27 ms → 19–20 ms | v1.5.1 (Endlos-Animationen ruhen beim Spielen, Zieh-Schatten per `transform`) |
| 16 Übergänge × 3 Läufe, CPU 6× | Frames über 33 ms: 185 → 154; mittlerer Spitzen-Frame 86 → 69 ms; Merge und Automat tippen weiter bei 80–120 ms (Rauschen ±30 %) | v1.5.2 |
| Ziehen, CPU 4× | Mittel 16,9 ms, 95 % der Frames bei 16,8 ms | v1.5.3 |
| Katze, CPU 4× | keine Ausreißer über 50 ms (Messung der damaligen Fassung mit Sprung und Streicheln; beides gibt es seit 1.5.17 nicht mehr) | v1.5.7 |

Größe: `www/` hat 3,7 MB (davon `index.html` 437 KB mit eingebetteten Schriften, der Rest Bilder und Ton). Die Größe der APK und der `.aab` ist erst nach dem ersten Build bekannt.

Einordnung: Auf einem Einsteiger-Handy können Merge und Automat tippen noch spürbar sein (Spitzen bis 120 ms im gedrosselten Test). Ob das auf echten Geräten stört, zeigt nur der Gerätetest.

## 5. Spielfortschritt

- Aufbau: 9 Städte, Stadtwechsel bei Level 1, 5, 10, 15, 20, 25, 30, 40 und 50 (Hamburg, Wien, Paris, Rom, Istanbul, Kyoto, New York, Rio, Sternecafé), dazu Ränge. Der Spielstand liegt nur auf dem Gerät (`localStorage`, Schlüssel `mergecafe_v1`).
- **Geprüft:** Tutorial bis zur ersten Lieferung; Spielen bis Level 6; ein Spielstand auf Level 12 (Paris) lädt und läuft; Neustart behält den Spielstand; alte, unvollständige und kaputte Spielstände (`tests/test_spielstand.py`).
- **Nicht geprüft:** Durchspielen der Level 13 bis 50, Dauer bis Level 10 oder 20 mit echten Spielern, Balance der Energie über mehrere Tage, Tagesbonus über 7 Tage am Stück (nur ein Abholen und das Verdoppeln). Die KPI-Ziele dafür stehen in `docs/LAUNCH_PLAN.md`; Messwerte gibt es erst mit AppsFlyer-Daten.
- **Grenzen des Spielstands:** Es gibt keinen Cloud-Spielstand. Deinstallieren löscht ihn. Android-Auto-Backup (`allowBackup=true`) kann ihn auf ein neues Gerät mitnehmen, das ist nicht getestet.

## 6. Bekannte Fehler und Einschränkungen

| Nr. | Punkt | Schwere | Stand |
|---|---|---|---|
| Q1 | **Android-Build ab Version 1.5.8: gebaut, aber nie auf einem Gerät gelaufen.** Der erste CI-Lauf am 24.11.2026 (Build 13) ist durchgelaufen; AppsFlyer-Bündel, Testmarkierung `build.json`, Hochformat-Sperre und Berechtigungen sind im Paket nachgewiesen. Einwilligungsfenster, AppsFlyer-Start, Test-Anzeigen und Käufe sind erst auf einem Gerät prüfbar. | mittel (vorher hoch) | offen, Gerätetest durch den Eigentümer mit der Test-APK Build 13 |
| Q2 | Kein eigenes Fehlerprotokoll im Spiel (kein Absturzdienst). Nach dem Start liefert Android vitals in der Play Console die Absturz- und ANR-Raten; Einzelheiten zu Fehlern nur über die Stapelspuren dort. | mittel | akzeptiert (spart ein weiteres SDK und eine weitere Datenschutz-Angabe) |
| Q3 | Echte Werbung, echte Käufe, AppsFlyer-Messung und das echte Einwilligungsfenster sind nie mit echten Konten gelaufen. Konten und Schlüssel fehlen noch. | hoch | wartet auf Konten, Prüfliste in `docs/TECHNIK.md`, Abschnitt 9 |
| Q4 | Tablets und Faltgeräte: Android 16 ignoriert die Hochformat-Sperre ab 600 dp. Im Querformat bei 1024×600 ist das Brett klein (Felder 26–32 px), das Spiel bleibt bedienbar. | mittel | akzeptiert, bei Bedarf Seitenlayout für Querformat |
| Q5 | Handy im Querformat: Start-Knopf und Brett wären nicht erreichbar. Behoben: Sperre im Manifest plus Dreh-Hinweis. | – | behoben in v1.5.10, im echten Build ungeprüft |
| Q6 | Bilder: Böden für Wien, Paris und Rom sind Platzhalter (Wien ist der Berlin-Entwurf), Böden 4 bis 8 fehlen (gebauter Ersatz im Spiel), die zwölf Einzugs-Posen fehlen (Kachel statt Pose). Fünf Teile-Bilder sind am Rand leicht angeschnitten (Donut, Brot, Croissant, Salat, Weizen). | niedrig | offen, braucht neue Bilder des Eigentümers |
| Q7 | Katze Mocha: drei Ruhebilder, teils abgewandelte Kopien (Schnurr-Ton seit 1.5.17 entfernt). Herkunft der Bilder vom Eigentümer erklärt (24.11.2026), aber nicht lückenlos belegt: Prompt, Modellversion und Tarif je Bild fehlen, Rechte am Referenzmaterial sind nicht geprüft (`docs/HERKUNFT_BILDER.md`, `docs/ASSETS_LIZENZEN.md`). | niedrig | offen |
| Q8 | Bedienungshilfen (TalkBack, große Schrift, Farbenblindheit) nicht geprüft. Das Spiel nutzt kaum beschriftete Elemente (7 Stellen mit `aria-label` oder `role`). | mittel | offen, in den Gerätetest aufnehmen |
| Q9 | Sprachen: Deutsch und Englisch. Bei anderen Gerätesprachen zeigt das Spiel Englisch (so festgelegt, nicht in jeder Sprache geprüft). | niedrig | akzeptiert |
| Q10 | Belohnungen werden auf dem Gerät gutgeschrieben, ohne Server (siehe `docs/TECHNIK.md`, R5). | niedrig | akzeptiert |
| Q11 | Ohne vollständige Rechtstexte bleiben Werbung, Käufe und Messung in der App gesperrt (`legalReady`). Seit dem 24.11.2026 sind Impressum und Datenschutz ausgefüllt, und der Android-Build 13 setzt `legalReady` auf true (in der Test-APK nachgewiesen). Ohne Konten und Schlüssel zeigt das Debug-Paket nur Googles Test-Anzeigen, es gibt keine Käufe und keine Messung. | – | erledigt; offen sind Konten und Schlüssel (Q3) |
| Q12 | Ein unlesbarer oder fremder Spielstand (kaputter Text, andere Versionsnummer, falsche Brettgröße) wird nicht repariert, das Spiel startet neu und überschreibt ihn beim nächsten Speichern. Es gibt keine Sicherungskopie. Relevant erst, wenn eine spätere Version das Format ändert (`v` erhöhen) und jemand zur alten Version zurückkehrt. | niedrig | akzeptiert; bei einer Formatänderung vorher eine Sicherungskopie des alten Textes anlegen |
| Q13 | *(ruht: Pro ist seit 1.5.16 ausgeschaltet, gilt beim Wiedereinschalten)* **Noa's Pro (Paywall, Kauf, Wiederherstellen, Abo-Verwaltung) ist nur mit nachgebauten Plugins getestet.** Die echte Paywall-Oberfläche, die Form der Plugin-Antworten (Kundeninfo-Meldung, Paywall-Ergebnis) und der Ablauf mit dem Test Store sind nicht auf einem Gerät gelaufen; im Paket (Build 17) sind nur die Aufrufnamen und die neuen Activities nachgewiesen. Das Spiel liest den Pro-Zustand aus dem Entitlement, nicht aus Ergebnistexten. Dazu: Das RevenueCat-Dashboard (Angebot, Entitlement, Paywall) ist nicht eingerichtet bzw. nicht prüfbar. | – (ruht) | vor dem Wiedereinschalten: Gerätetest (Abschnitt 8, Punkt 6) mit Test-APK und gesetztem Secret `REVENUECAT_TEST_KEY`; Dashboard einrichten (`docs/TECHNIK.md`, R9 und R10) |

### Behobene Fehler (Auswahl, mit Version)

- v1.5.0: Tutorial ohne Pärchen (die ersten zwei Spawns sind jetzt immer Stufe 1); Startruckler (schwere Arbeit vor dem ersten Bild).
- v1.5.1: Ruckeln im Spielfluss (zu viele Endlos-Animationen auf dem Hauptthread, Zieh-Schatten per `left/top`).
- v1.5.2: **Service Worker lieferte immer die zuerst gespeicherte Seite** (Besucher und Store-Updates blieben auf alten Versionen hängen); Ruckeln bei Fenster-Wechseln (Neuberechnung der ganzen Seite).
- v1.5.6: Apostroph im App-Namen hätte den Android-Build abgebrochen (Maskierung in `patch-android.js`, doppelt ausführbar).
- v1.5.9: Werbung, Käufe und Messung liefen in der App auch bei Platzhalter-Rechtstexten; jetzt gesperrt und getestet.
- v1.5.10: Querformat auf dem Handy (Hochformat-Sperre, Dreh-Hinweis); Schrift „Lilita One“ lag verändert unter dem Originalnamen vor (jetzt unverändert, siehe Lizenzverzeichnis).
- v1.5.12: Das Diamanten-Fenster nannte „+3 bis +7 pro Level“; ab Level 15 gibt es mehr (Formel 3 + 2 je 5 Level). Der Text ist korrigiert, die Chancen (Geschenk, Stufe 2 beim Erzeugen) stehen jetzt im Spiel.
- v1.5.11: Die öffentliche Test-APK hätte mit echter AdMob-Kennung echte Anzeigen gezeigt (Kontosperre bei eigenen Klicks möglich); sie nutzt jetzt Googles Test-Anzeigenblock.
- v1.5.17 (Rückmeldung des Eigentümers vom Handy, 24.11.2026): Die Katze blieb nach dem Streicheln auf dem Brett stehen und verdeckte es; Sprung und Streicheln entfernt (außerdem 22 statt 3 Bilder im Arbeitsspeicher). „Verkaufen“ mit Mülltonne war irreführend, jetzt „Take-away“ mit Take-away-Symbol. „Bessere Zutaten“ war nicht spürbar: Jetzt heißt es „Bessere Artikel“, zeigt die Chance in Prozent und meldet einen Glückstreffer („Stufe 2!“); die Chancen selbst sind unverändert. Das App-Icon wirkte auf dem Handy zu klein: Motiv in der Android-Vordergrundebene von 690 auf 810 px vergrößert, Rand bis an die Ecken gefüllt; nach dem Vergleich im Homescreen-Screenshot des Eigentümers in 1.5.18 weiter auf 930 px (91 % der Ebene). Auf jedem Teil stand eine Zahl, auch bei Stufe 1; jetzt erst ab Stufe 2. Die gezeichnete Szene oben passt in Paris nicht zu den gemalten Bildern: Platz für ein Vollbild-Hintergrundbild je Welt eingebaut (`b<N>`), Bilder fehlen noch (`docs/ART_BRIEF.md`, Etappe 3).

## 7. Freigabekriterien

**Vor dem ersten Upload nach `internal`** (Eigentümer entscheidet, Push erst nach Freigabe):
- [ ] Alle Tests aus Abschnitt 3 grün auf dem Stand, der gebaut wird.
- [ ] Build grün; Artefakte `noas-bean-trail-test-apk-<Nr>`, `noas-bean-trail-store-aab-<Nr>`, `versionen-<Nr>` vorhanden (`docs/TECHNIK.md`, Abschnitt 9).
- [x] Namensfreigabe (`docs/RECHT_UND_NAMEN.md`, 5.3) und vollständige Rechtstexte (beides erledigt am 24.11.2026).

**Vor dem geschlossenen Test mit Testern:**
- [ ] Gerätetest (Abschnitt 8) auf mindestens drei Geräten ohne Absturz in 20 Minuten Spielzeit.
- [ ] Kauf mit Lizenztester, Werbung mit Test-Anzeige, Einwilligungsfenster auf einem Gerät im EWR geprüft.
- [ ] Mindestzahl und Dauer des geschlossenen Tests in der Play Console prüfen (Stand der Recherche vom 24.11.2026: 12 Tester über 14 Tage für neue Privatkonten; die Regel ändert sich, bitte vor Beginn gegenprüfen).

**Vor der Produktion (macht der Eigentümer, nie der Agent):**
- [ ] Android vitals ohne Warnung: nutzerbemerkte Absturzrate unter 1,09 %, nutzerbemerkte ANR-Rate unter 0,47 % (über alle Geräte) und je Handymodell unter 8 % (Schwellen laut Google, Stand 24.11.2026: https://developer.android.com/google/play/vitals).
- [ ] Produkt-KPIs aus `docs/LAUNCH_PLAN.md` im Test erreicht (Tutorial ≥ 85 %, D1 ≥ 40 % …) oder bewusst anders entschieden.
- [ ] Alle offenen Punkte mit Schwere „hoch“ aus Abschnitt 6 erledigt.

## 8. Gerätetest (zu tun, Protokoll)

Mindestens drei Geräte, möglichst: ein Einsteiger-Handy (2 bis 3 GB RAM, Android 8 bis 10), ein Mittelklasse-Handy, ein aktuelles Gerät mit Android 16; zusätzlich, wenn vorhanden, ein Tablet. Jede Zeile mit Gerät, Android-Version und Build-Nummer eintragen.

Ablauf je Gerät (jeweils Test-APK ohne und mit Rechtstexten):
1. Neu installieren, starten (Zeit bis zum ersten Bild schätzen), Figur wählen, Einzug, Tutorial bis zur ersten Lieferung.
2. 10 Minuten durchgehend spielen: Merge-Gefühl, Automaten tippen, Lieferungen, Geschenk-Fach, Tagesbonus; Wärme und Akkuverbrauch notieren.
3. Ton und Musik aus und an, Vibration, Katze antippen (Miau, bleibt oben im Bestellbereich), Icon auf dem Startbildschirm (Größe, Rand).
4. Werbung: Test-Anzeige bis zum Ende (Belohnung kommt), Anzeige vorzeitig schließen (keine Belohnung), ohne Netz (keine Anzeige, kein Absturz).
5. Einwilligung (Gerät im EWR): Fenster erscheint, Ablehnen sperrt Werbung und Messung, „Werbe-Einstellungen“ in den Optionen ändern.
6. Shop: Preis kommt aus dem Store, Kauf mit Lizenztester, Gutschrift, Kauf abbrechen. Im Auslieferungszustand ist von Noa's Pro nichts zu sehen (keine Karte im Shop, keine Zeilen in den Optionen). Nur wenn Pro eingeschaltet ist: Pro-Karte im Shop und Zeile in den Optionen, Paywall öffnet, Kauf im Test Store, Pro aktiv (Belohnung ohne Video, +5 Diamanten einmal je Tag), „Käufe wiederherstellen“, „Abo verwalten“.
7. App in den Hintergrund, Anruf, Bildschirm aus und an; Neustart; Spielstand erhalten; Flugmodus-Start.
8. Systemschrift und Anzeigegröße auf „groß“; Sprache Englisch; Drehen (Handy bleibt hochkant); TalkBack kurz anschalten.

| Gerät / Android | Build | Start | 10 min ohne Absturz | Werbung | Kauf | Einwilligung | Auffälligkeiten |
|---|---|---|---|---|---|---|---|
| (offen) | | | | | | | |

Gefundene Fehler kommen mit Nummer in Abschnitt 6; jeder Fehler bekommt, wenn möglich, einen Test in `tests/`.

## Quellen (Stand 25.11.2026)
- Google, Android vitals und Schwellen für schlechtes Verhalten: https://developer.android.com/google/play/vitals
- Google, Hintergrund zu den Kennzahlen (2022): https://android-developers.googleblog.com/2022/10/raising-bar-on-technical-quality-on-google-play.html
