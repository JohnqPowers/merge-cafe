# Asset- und Lizenzverzeichnis – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.13. Nachweis darüber, woher jedes Bild, jeder Ton, jede Schrift und jede Software-Komponente stammt, unter welchen Bedingungen sie genutzt wird und was noch zu bestätigen ist. Das Repo ist öffentlich: Hier stehen keine persönlichen Angaben und keine Einschätzungen zu fremden Spielen.

## 1. Kurzfassung

| Bereich | Stand |
|---|---|
| Schriften | **belegt.** Zwei Schriften unter SIL OFL 1.1, Originaltexte und Originaldateien im Repo, Lizenzseite im Spiel (Optionen → Lizenzen). |
| Software | **bekannt.** Lizenzen siehe Abschnitt 5; genaue Versionen hält jeder Build im Artefakt `versionen-<Nr>` fest (`docs/TECHNIK.md`). Eine vollständige Liste aller Unterbibliotheken fehlt noch (Abschnitt 5). |
| Töne, Musik | **eigen.** Alles wird im Spiel erzeugt (WebAudio). Seit 1.5.17 gibt es keine Audiodatei mehr (das Katzen-Schnurren, ein synthetischer Platzhalter, ist entfernt). |
| Symbole | **eigen.** 27 SVG-Symbole im Code, im Projekt gezeichnet, keine Fremd-Symbolsätze. |
| Emojis | Systemschrift des Geräts, nicht eingebettet. |
| **Bilder** | **erklärt, nicht lückenlos belegt.** Laut Eigentümer (24.11.2026) überwiegend mit der Bildgenerierung von OpenAI (ChatGPT) nach seinen Briefings erstellt; Verzeichnis mit Prüfsummen und Manifest der ausgelieferten Dateien liegen im Repo (`docs/herkunft/`), 82 von 83 Bild- und Tondateien lassen sich aus den Paketen bitgleich nachstellen. Es fehlen Prompt, Modellversion und Tarif je Bild, und die Rechte am Referenzmaterial sind nicht geprüft (Abschnitt 3, `docs/HERKUNFT_BILDER.md`). Das bleibt der wichtigste offene Punkt dieses Verzeichnisses. |

## 2. Bestand

| Gruppe | Dateien | Anzahl | Herkunft | Aufbereitung | Ohne Bild im Spiel |
|---|---|---|---|---|---|
| App-Icon (seit 1.5.21) | `assets/src/app-icon-original.png` (Original, Noa blond); abgeleitet: `assets/icon-*.png`, `store/app-icon-512.png`, `www/icons/*` | 1 + 7 | Eigentümer, Chat-Lieferung 28.11.2026 (nicht im Verzeichnis, Prüfsumme in der Paketliste); Erzeugung und Rechte nicht erklärt | `assets/src/build-icon.py` | – |
| App-Icon (bis 1.5.20, Archiv) | `assets/src/app-icon-original-2026-11-24.png` | 1 | Eigentümer, 24.11.2026 (Upload-Datei „Noa_s_Bean_Trail__Caf_zauber.png“; im Verzeichnis `noas_bean_trail_icon_original_1254.png`, gleiche Prüfsumme) | wird nicht mehr gebaut | – |
| Startbild (erste Seite im Spiel, Experiment) | `assets/src/start-original.png` (Original); abgeleitet: `www/art/start.webp` | 1 + 1 | Eigentümer, Chat-Lieferung 28.11.2026 (nicht im Verzeichnis, Prüfsumme in der Paketliste); Erzeugung und Rechte nicht erklärt | `scripts/start_import.py` (Versionsnummer getilgt, unten verlängert, 1220 px) | altes gebautes Startbild |
| Android-Startbild | `assets/splash.png`, `assets/splash-dark.png` (identisch) | 2 | im Projekt seit v1.4.0 (Commit `fb09461`); Erzeugung nicht protokolliert, **Eigentümer bestätigt oder ersetzt** | `capacitor-assets` im Build | – |
| Teile | `www/art/k1_*` bis `k3_*` | 22 (7 Kaffee, 8 Backwaren, 7 Frühstück) | Eigentümer, OpenAI-Bildgenerierung nach `docs/ART_BRIEF.md` (Paket `merge_cafe_alle_25_grafiken.zip`) | `scripts/art_import.py` (Freistellen, Zuschneiden, 256 px, WebP) | Emoji |
| Automaten | `www/art/g1` bis `g3` | 3 | wie Teile | wie Teile | Emoji |
| Spielerfiguren | `www/art/a1` bis `a12` | 12 | wie Teile | `art_import.py` (208 × 208) | Emoji im Farbkreis |
| Gäste | `www/art/c1` bis `c12` | 12 | wie Teile | `art_import.py` (240 × 270) | gezeichnete Typen |
| Hintergründe (Vollbild) | `www/art/b0` bis `b8` | 9 von 9 (seit 1.5.19) | Eigentümer, „Stadtpaket“ vom 25.11.2026 (OpenAI-Bildgenerierung laut Begleittext, Rechte nicht zugesichert) | `art_import.py` (oben auf 9:19,5 ergänzt, 720 × 1560) | gezeichnete Szene mit Boden |
| Böden | `www/art/f0` bis `f3` | 4 von 9 | wie Teile | `art_import.py`, `floor_prep.py` | gebauter Boden; seit 1.5.19 nur noch Rückfall, solange `b<N>` der Welt fehlt |
| Brett-Rahmen | `www/art/frame.webp`, `frame1` bis `frame8` | 1 + 8 (Stadtrahmen seit 1.5.19) | wie Teile; Stadtrahmen aus dem Stadtpaket (Prüfsummen im Verzeichnis des Eigentümers); `frame.webp` ist der Hamburger Rahmen | `art_import.py` (auf 7:8 umgebaut) | CSS-Rahmen / Standardrahmen |
| Möwe (Experiment, nur im Branch `exp/moewe-hamburg`) | `www/art/anim/moewe_hamburg.webp` | 1 Streifen aus 8 Flug-Frames | Eigentümer, Stadtpaket 25.11.2026 (Ordner `07_Animationen_Optional/moewe`); OpenAI-Bildgenerierung laut README, **Rechte nicht zugesichert** | `scripts/gull_import.py` | keine Möwe (nichts wird geladen) |
| Katze Mocha | `www/art/cat/c01` bis `c03` | 3 Ruhebilder (seit 1.5.17; vorher 22 Frames + 3 Herzen) | Eigentümer, Katzen-Paket 24.11.2026; Frames teils abgewandelte Kopien | `scripts/cat_import.py` | gezeichnete SVG-Katze |
| Schnurren | entfernt in 1.5.17 (`www/art/cat/purr.wav` und der Ersatzton im Code) | 0 | war laut Katzen-Paket ein **Platzhalter** (`audio/purr_*.wav`) | – | – |
| Einzugs-Posen, Effekte, Böden 4 bis 8 | `e1` bis `e12`, `fx_*`, `f4` bis `f8` | nicht im Spiel: Posen stehen im Verzeichnis des Eigentümers, sind dem Projekt aber nicht geliefert; `f4` bis `f8` sind Entwürfe im Paket `merge_cafe_8_stadtboeden_entwurf.zip`, nicht eingebaut; `fx_*` nicht geliefert | – | – | Fallbacks im Spiel |

Die Dateinamen sind der Vertrag zwischen Brief, Import-Skript und Spiel (`docs/ART_BRIEF.md`). Das Manifest `const ART` in `www/index.html` führt das Skript selbst nach. Nachweis je ausgelieferte Datei (Pfad, Version, SHA-256, Quelle): `docs/herkunft/ausgelieferte_dateien.csv`.

## 3. Bilder: Herkunft und Nachweis

Stand 24.11.2026. Ausführlich: `docs/HERKUNFT_BILDER.md`; Dateien: `docs/herkunft/`.

**Herkunft (Erklärung des Eigentümers):** Die Spielbilder entstanden überwiegend mit der Bildgenerierung von OpenAI in ChatGPT nach Briefings des Eigentümers (`docs/ART_BRIEF.md`), teils mit hochgeladenem Referenzmaterial, und wurden danach zugeschnitten, freigestellt, skaliert und für die App aufbereitet. Das Verzeichnis nennt die unmittelbare Quelldatei oder das Paket, nicht zwingend die einzelne Generierung oder den Prompt. **Eine lückenlose Kette je Datei gibt es nicht.** Die Originale und Prompts gehören nicht ins öffentliche Repo, sondern in die Bibliothek des Eigentümers.

| Bildgruppe | Werkzeug und Version | Tarif / Konto-Art | Datum der Erstellung | Nutzungsbedingungen geprüft | Originale und Prompts aufbewahrt (wo?) |
|---|---|---|---|---|---|
| App-Icon | OpenAI-Bildgenerierung (ChatGPT); Modellversion nicht festgehalten | nicht festgehalten | bis 24.11.2026, Tag nicht festgehalten | Eigentümer, 24.11.2026 (EU-Nutzungsbedingungen von OpenAI: Rechte am Ergebnis beim Nutzer, soweit rechtlich zulässig) | Original im Repo (`assets/src/app-icon-original.png`); Prompt nicht festgehalten |
| Teile und Automaten | wie App-Icon | wie App-Icon | wie App-Icon | wie App-Icon | Paket in der Bibliothek des Eigentümers, Prüfsummen im Repo; Prompt je Bild nicht festgehalten (Briefing: `docs/ART_BRIEF.md`) |
| Figuren und Gäste | wie App-Icon | wie App-Icon | wie App-Icon | wie App-Icon | wie Teile |
| Böden und Rahmen | wie App-Icon | wie App-Icon | wie App-Icon | wie App-Icon | wie Teile; Böden `f1` bis `f3` sind Entwürfe |
| Stadtkulissen (Vollbild) | OpenAI-Bildgenerierung laut Begleittext des Stadtpakets; Modellversion nicht angegeben | nicht angegeben | 25.11.2026 | für diese Lieferung nicht erneut bestätigt (Eigentümer, 24.11.2026 für die früheren Bilder); **Rechte nicht zugesichert** (Begleittext) | Stadtpaket (ZIP) in der Bibliothek des Eigentümers, Dateiliste mit Prüfsummen im Repo; Prompts nicht mitgeliefert |
| Katze (Frames, Herzen) | OpenAI-Bildgenerierung nach einem Screenshot des eigenen Spiels als Referenz; Frames daraus abgeleitet (Skalierung, Drehung, Verschiebung, Compositing) | nicht festgehalten | bis 24.11.2026, Tag nicht festgehalten | wie App-Icon | Katzenpaket in der Bibliothek des Eigentümers; Dateiliste mit Prüfsummen im Repo |
| Schnurr-Datei | synthetisch erzeugt (Katzenpaket), Platzhalter | – | bis 24.11.2026 | – (kein Fremdmaterial laut Eigentümer) | Katzenpaket |

Hinweise:
- **Schutz:** Rein KI-erzeugte Bilder sind nach verbreiteter Ansicht kaum urheberrechtlich geschützt (so auch die Einschätzung des US Copyright Office vom Januar 2025); menschliche Auswahl, Gestaltung und Bearbeitung kann geschützt sein. Folge: Dritte könnten die Bilder kopieren. Den Namen und das Gesamtbild des Spiels schützt eher das Markenrecht (Namensprüfung in `docs/RECHT_UND_NAMEN.md`). Keine Rechtsberatung.
- **Beleg der Entstehung:** Die Pakete liegen in der Bibliothek des Eigentümers; das Repo hält die Prüfsummen und die Import-Skripte. Damit lassen sich 77 von 78 Bild- und Tondateien in `www/art` und `www/icons` bitgleich aus den Paketen nachstellen (Ausnahme: der vorläufige Boden `f1`); die 17 Dateien des Stadtpakets (Kulissen `b0` bis `b8`, Rahmen `frame1` bis `frame8`) am 25.11.2026. Prompts je Bild sind nicht lückenlos erhalten; ab jetzt je Lieferung festhalten (`docs/HERKUNFT_BILDER.md`, Abschnitt 6).
- **Nutzungsbedingungen:** Vom Eigentümer am 24.11.2026 geprüft, vom Agenten nicht selbst abgerufen. Den Stand des Abrufs mit Datum aufheben und vor dem Start fachkundig einordnen lassen. Das klärt keine Rechte Dritter.
- **Referenzmaterial:** Hochgeladene Screenshots und Referenzbilder sind Referenz, keine generierten Originale; ihre Nutzungsrechte sind nicht geprüft.
- **Stadtkulissen:** Sie zeigen reale Bauwerke als Illustration im Hintergrund. Vor dem Store-Upload die Bildrechte an Bauwerken (Panoramafreiheit je Land, Sonderfälle wie die nächtliche Beleuchtung des Eiffelturms; die Kulisse zeigt eine Tagesansicht) und die KI-Kennzeichnung fachkundig einordnen lassen. Der Agent hat die neun Bilder am 25.11.2026 auf Schrift, Logos und Marken angesehen: nichts gefunden.
- **Zufällige Ähnlichkeit:** Figuren, Gäste und Teile einmal gegen bekannte Figuren und Logos ansehen (Brief: keine Texte, keine Marken). Die Prüfung gegen das früher untersuchte Referenzspiel ist erledigt (Bericht an den Eigentümer, 24.11.2026); eine Sichtprüfung gegen weitere bekannte Figuren steht aus.
- **Katze:** Frames teils abgeleitet, ein Paar im Paket ist eine Kopie (Frame 2 und 4). Seit 1.5.17 bleiben nur die drei Ruhebilder; Schnurr-Ton, Herzen und die übrigen Frames sind entfernt (Speicher, kein Streicheln mehr). Herkunft der drei Bilder: wie zuvor, siehe `docs/HERKUNFT_BILDER.md`.
- **Startbild:** `assets/splash.png` und `assets/splash-dark.png` stehen nicht im Verzeichnis des Eigentümers, ihre Erzeugung ist nicht protokolliert; bestätigen oder ersetzen.
- **Nicht behaupten:** dass jedes Bild exklusiv urheberrechtlich geschützt, markenrechtlich freigegeben, einzeln extern lizenzgeprüft oder die Herkunft aller Referenzen abschließend geklärt sei.
- **Store-Angaben:** Die Lizenzseite im Spiel nennt die KI-Unterstützung offen. Ob ein Store eine Kennzeichnung von KI-Bildern verlangt, vor dem Upload in den dann gültigen Richtlinien nachlesen.

## 4. Schriften

| Schrift | Urheberrechtsvermerk (wörtlich aus der OFL.txt) | Lizenz | Im Spiel | Dateien im Repo |
|---|---|---|---|---|
| Fredoka | Copyright 2016 The Fredoka Project Authors (https://github.com/hafontia/Fredoka-One) | SIL OFL 1.1, kein reservierter Name | Teilmenge der Originaldatei (203 Zeichen, Stärke 400 bis 700, Breite fest), WOFF, Base64 in `www/index.html` | `assets/fonts/Fredoka[wdth,wght].ttf`, `assets/fonts/Fredoka-OFL.txt`, `www/ofl/Fredoka-OFL.txt` |
| Lilita One | Copyright (c) 2011 Juan Montoreano (juan@remolacha.biz), with Reserved Font Name Lilita | SIL OFL 1.1, **reservierter Name** | Originaldatei **unverändert**, Base64 in `www/index.html` (seit v1.5.10; vorher eine Teilmenge unter dem Originalnamen) | `assets/fonts/LilitaOne-Regular.ttf`, `assets/fonts/LilitaOne-OFL.txt`, `www/ofl/LilitaOne-OFL.txt` |

Quelle beider Schriften: `github.com/google/fonts`, Commit `06bfe0d62a98375cb09c942fa18e68bd32cff057` (Details und Prüfsummen: `assets/fonts/QUELLE.md`).

Pflichten der OFL und wie sie erfüllt sind:
1. Urheberrechtsvermerk und Lizenztext müssen bei Weitergabe beiliegen → `www/licenses.html` nennt die Vermerke und verlinkt die vollständigen Texte unter `www/ofl/`; beides liegt auch in der App.
2. Die Schrift darf nicht allein verkauft werden → sie ist Teil des Spiels.
3. Veränderte Fassungen dürfen den reservierten Namen nicht tragen → Lilita One ist unverändert, Fredoka hat keinen reservierten Namen.
4. Abgeleitete Schriftdateien bleiben unter der OFL → die Fredoka-Teilmenge ist nur im Spiel eingebettet und in `www/licenses.html` ausgewiesen.

Prüfung im Vergleich zu vorher: das Startbild unterscheidet sich nach dem Tausch von Lilita One in 558 von 1,3 Mio. Pixeln um höchstens 27 von 255 Stufen (Kantenglättung), sonst gleich.

## 5. Software in der App

| Komponente | Version (Stand `package.json`) | Zweck | Lizenz |
|---|---|---|---|
| Capacitor (`@capacitor/core`, `android`, `ios`, `cli`, `assets`) | `latest` (**nicht festgelegt**) | Gerüst der App | MIT |
| `@capacitor-community/admob` | `^8.0.0` | Werbung (Google AdMob), Einwilligungsfenster (UMP) | MIT |
| Google Mobile Ads SDK, User Messaging Platform | über das AdMob-Plugin | Werbeanzeigen, Einwilligung | Nutzungsbedingungen von Google |
| `appsflyer-capacitor-plugin` | `7.0.4` | Messung (nach Einwilligung) | MIT |
| `@appsflyer-sdk/js-core-plugin` | `7.1.0` | JS-Schnittstelle, per esbuild nach `www/af.js` gebündelt | Lizenzfeld im Paket beim Build prüfen |
| AppsFlyer Android SDK | über das Plugin | Messung | Bedingungen von AppsFlyer |
| `@revenuecat/purchases-capacitor` | `latest` (**nicht festgelegt**) | Käufe | MIT |
| RevenueCat Android SDK, Google Play Billing Library | Billing 9.1.0 im Build 13 | Käufe | MIT (RevenueCat); Billing nach Google-Bedingungen |
| AndroidX, Kotlin-Bibliotheken | von Gradle aufgelöst | Android-Grundlagen | Apache License 2.0 |
| `esbuild` | `^0.25.0` | nur Build-Werkzeug (nicht in der App) | MIT |
| Playwright, Python-Bibliotheken (Pillow, OpenCV, NumPy) | lokal | nur Tests und Bild-Skripte (nicht in der App) | verschiedene freie Lizenzen |

**Offen:**
- `latest` bei Capacitor und dem RevenueCat-Kern-Plugin bedeutet: jeder Build zieht die aktuelle Version. Nach dem ersten erfolgreichen Build die aufgelöste `package-lock.json` (liegt im Artefakt `versionen-<Nr>` als `npm-tree.txt`, bzw. lokal per `npm install`) festschreiben und `latest` durch feste Versionen ersetzen (`docs/TECHNIK.md`, Abschnitt Updates).
- Eine vollständige Lizenzliste inklusive aller Unterbibliotheken (npm und Gradle) erzeugen und auf der Lizenzseite verlinken (z. B. mit `license-checker` für npm und dem Google-OSS-Licenses-Plugin für Gradle). Das ist ohne Netz nicht prüfbar und wird beim ersten CI-Lauf nachgeholt.

## 6. Pflege

- Neues Bild, neuer Ton, neue Schrift, neue Bibliothek: **zuerst hier eintragen** (Herkunft, Lizenz, Datei), dann einbauen.
- Bilder nur vom Eigentümer oder selbst gebaut (`docs/RECHT_UND_NAMEN.md`, Abschnitt 7).
- Nach jeder Änderung der Lizenzseite `www/licenses.html` und diese Datei gleich halten.
- Nach jeder Änderung an Bildern, Tönen oder Schriften das Manifest neu erzeugen (`python3 -I scripts/asset_manifest.py`); `tests/test_herkunft.py` prüft, dass es stimmt. Neue Lieferungen: `scripts/herkunft_pakete.py` (Regeln: `docs/HERKUNFT_BILDER.md`, Abschnitt 6).

## Quellen
- US Copyright Office, Copyright and Artificial Intelligence, Part 2: Copyrightability (29.01.2025): https://copyright.gov/newsnet/2025/1060.html
- SIL Open Font License 1.1: https://openfontlicense.org (Texte der beiden Schriften: `www/ofl/`)
- Schriftquellen: https://github.com/google/fonts (`ofl/fredoka`, `ofl/lilitaone`)

Hinweis 25.11.2026: Das RevenueCat-Paywall-Plugin (`@revenuecat/purchases-capacitor-ui`, MIT laut Anbieter) war nur in v1.5.15 (Build 17) eingebaut und ist seit v1.5.16 nicht mehr im Paket (Pro ausgeschaltet, `docs/MONETARISIERUNG.md`, Abschnitt 11). Wird es wieder eingebaut, kommen die Zeile in diese Tabelle und der Eintrag in `www/licenses.html` zurück.
