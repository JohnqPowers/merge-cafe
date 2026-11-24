# Asset- und Lizenzverzeichnis – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.12. Nachweis darüber, woher jedes Bild, jeder Ton, jede Schrift und jede Software-Komponente stammt, unter welchen Bedingungen sie genutzt wird und was noch zu bestätigen ist. Das Repo ist öffentlich: Hier stehen keine persönlichen Angaben und keine Einschätzungen zu fremden Spielen.

## 1. Kurzfassung

| Bereich | Stand |
|---|---|
| Schriften | **belegt.** Zwei Schriften unter SIL OFL 1.1, Originaltexte und Originaldateien im Repo, Lizenzseite im Spiel (Optionen → Lizenzen). |
| Software | **bekannt.** Lizenzen siehe Abschnitt 5; genaue Versionen hält jeder Build im Artefakt `versionen-<Nr>` fest (`docs/TECHNIK.md`). Eine vollständige Liste aller Unterbibliotheken fehlt noch (Abschnitt 5). |
| Töne, Musik | **eigen.** Alles wird im Spiel erzeugt (WebAudio). Einzige Audiodatei: das Katzen-Schnurren, vom Eigentümer geliefert (Platzhalter). |
| Symbole | **eigen.** 27 SVG-Symbole im Code, im Projekt gezeichnet, keine Fremd-Symbolsätze. |
| Emojis | Systemschrift des Geräts, nicht eingebettet. |
| **Bilder** | **Lücke.** KI-gestützt erstellt, vom Eigentümer geliefert. Werkzeug, Tarif, Datum und Nutzungsbedingungen sind nicht belegt (Abschnitt 3). Das ist der wichtigste offene Punkt dieses Verzeichnisses. |

## 2. Bestand

| Gruppe | Dateien | Anzahl | Herkunft | Aufbereitung | Ohne Bild im Spiel |
|---|---|---|---|---|---|
| App-Icon | `assets/src/app-icon-original.png` (Original); abgeleitet: `assets/icon-*.png`, `store/app-icon-512.png`, `www/icons/*` | 1 + 7 | Eigentümer, 24.11.2026 (Datei „Noa_s_Bean_Trail__Caf_zauber.png“) | `assets/src/build-icon.py` | – |
| Android-Startbild | `assets/splash.png`, `assets/splash-dark.png` (identisch) | 2 | im Projekt seit v1.4.0 (Commit `fb09461`); Erzeugung nicht protokolliert, **Eigentümer bestätigt oder ersetzt** | `capacitor-assets` im Build | – |
| Teile | `www/art/k1_*` bis `k3_*` | 22 (7 Kaffee, 8 Backwaren, 7 Frühstück) | Eigentümer, KI-Werkzeug nach `docs/ART_BRIEF.md` | `scripts/art_import.py` (Freistellen, Zuschneiden, 256 px, WebP) | Emoji |
| Automaten | `www/art/g1` bis `g3` | 3 | wie Teile | wie Teile | Emoji |
| Spielerfiguren | `www/art/a1` bis `a12` | 12 | wie Teile | `art_import.py` (208 × 208) | Emoji im Farbkreis |
| Gäste | `www/art/c1` bis `c12` | 12 | wie Teile | `art_import.py` (240 × 270) | gezeichnete Typen |
| Böden | `www/art/f0` bis `f3` | 4 von 9 | wie Teile | `art_import.py`, `floor_prep.py` | gebauter Boden |
| Brett-Rahmen | `www/art/frame.webp` | 1 | wie Teile | `art_import.py` (auf 7:8 umgebaut) | CSS-Rahmen |
| Katze Mocha | `www/art/cat/c01` bis `c22`, `h1` bis `h3` | 22 Frames + 3 Herzen | Eigentümer, Katzen-Paket 24.11.2026; Frames teils abgewandelte Kopien | `scripts/cat_import.py` | gezeichnete SVG-Katze |
| Schnurren | `www/art/cat/purr.wav` | 1 | Katzen-Paket, laut Paket **Platzhalter** (`audio/purr_*.wav`); Schleife nahtlos geschnitten | `cat_import.py` | synthetischer Ersatzton im Code |
| Einzugs-Posen, Effekte, Böden 4 bis 8, Rahmen je Welt | `e1` bis `e12`, `fx_*`, `f4` bis `f8`, `frame0` bis `frame8` | noch nicht geliefert | – | – | Fallbacks im Spiel |

Die Dateinamen sind der Vertrag zwischen Brief, Import-Skript und Spiel (`docs/ART_BRIEF.md`). Das Manifest `const ART` in `www/index.html` führt das Skript selbst nach.

## 3. Bilder: Nachweis, der noch fehlt

Alle Bilder entstanden mit einem KI-Bildwerkzeug und wurden vom Eigentümer geliefert. Im Repo ist nicht festgehalten, **welches Werkzeug**, **welcher Tarif**, **wann** und **mit welchen Nutzungsbedingungen**. Ohne diese Angaben lässt sich die kommerzielle Nutzung nicht belegen. Der Eigentümer ergänzt die Tabelle (die Originale und Prompts gehören **nicht** ins öffentliche Repo, sondern in einen privaten Ordner):

| Bildgruppe | Werkzeug und Version | Tarif / Konto-Art | Datum der Erstellung | Nutzungsbedingungen geprüft (Datum, kommerzielle Nutzung erlaubt?) | Originale und Prompts aufbewahrt (wo?) |
|---|---|---|---|---|---|
| App-Icon | | | | | |
| Teile und Automaten | | | | | |
| Figuren und Gäste | | | | | |
| Böden und Rahmen | | | | | |
| Katze (Frames, Herzen) | | | | | |
| Schnurr-Datei | | | | | |

Hinweise:
- **Schutz:** Rein KI-erzeugte Bilder sind nach verbreiteter Ansicht kaum urheberrechtlich geschützt (so auch die Einschätzung des US Copyright Office vom Januar 2025); menschliche Auswahl, Gestaltung und Bearbeitung kann geschützt sein. Folge: Dritte könnten die Bilder kopieren. Den Namen und das Gesamtbild des Spiels schützt eher das Markenrecht (Namensprüfung in `docs/RECHT_UND_NAMEN.md`). Keine Rechtsberatung.
- **Beleg der Entstehung:** Originaldateien, Prompts, Zwischenstände und die eigene Nachbearbeitung (die Import-Skripte liegen im Repo) aufheben.
- **Zufällige Ähnlichkeit:** Figuren, Gäste und Teile einmal gegen bekannte Figuren und Logos ansehen (Brief: keine Texte, keine Marken). Die Prüfung gegen das früher untersuchte Referenzspiel ist erledigt (Bericht an den Eigentümer, 24.11.2026); eine Sichtprüfung gegen weitere bekannte Figuren steht aus.
- **Katze:** Frames teils abgewandelte Kopien, Schnurren ist ein Platzhalter. Eine eigene, lizenzierte Aufnahme ersetzt `purr.wav` ohne Codeänderung (gleicher Dateiname); danach Herkunft hier eintragen.
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
| RevenueCat Android SDK, Google Play Billing Library | Billing 9.1.0 im Build 12 | Käufe | MIT (RevenueCat); Billing nach Google-Bedingungen |
| AndroidX, Kotlin-Bibliotheken | von Gradle aufgelöst | Android-Grundlagen | Apache License 2.0 |
| `esbuild` | `^0.25.0` | nur Build-Werkzeug (nicht in der App) | MIT |
| Playwright, Python-Bibliotheken (Pillow, OpenCV, NumPy) | lokal | nur Tests und Bild-Skripte (nicht in der App) | verschiedene freie Lizenzen |

**Offen:**
- `latest` bei Capacitor und RevenueCat bedeutet: jeder Build zieht die aktuelle Version. Nach dem ersten erfolgreichen Build die aufgelöste `package-lock.json` (liegt im Artefakt `versionen-<Nr>` als `npm-tree.txt`, bzw. lokal per `npm install`) festschreiben und `latest` durch feste Versionen ersetzen (`docs/TECHNIK.md`, Abschnitt Updates).
- Eine vollständige Lizenzliste inklusive aller Unterbibliotheken (npm und Gradle) erzeugen und auf der Lizenzseite verlinken (z. B. mit `license-checker` für npm und dem Google-OSS-Licenses-Plugin für Gradle). Das ist ohne Netz nicht prüfbar und wird beim ersten CI-Lauf nachgeholt.

## 6. Pflege

- Neues Bild, neuer Ton, neue Schrift, neue Bibliothek: **zuerst hier eintragen** (Herkunft, Lizenz, Datei), dann einbauen.
- Bilder nur vom Eigentümer oder selbst gebaut (`docs/RECHT_UND_NAMEN.md`, Abschnitt 7).
- Nach jeder Änderung der Lizenzseite `www/licenses.html` und diese Datei gleich halten.

## Quellen
- US Copyright Office, Copyright and Artificial Intelligence, Part 2: Copyrightability (29.01.2025): https://copyright.gov/newsnet/2025/1060.html
- SIL Open Font License 1.1: https://openfontlicense.org (Texte der beiden Schriften: `www/ofl/`)
- Schriftquellen: https://github.com/google/fonts (`ofl/fredoka`, `ofl/lilitaone`)
