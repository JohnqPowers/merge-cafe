# Herkunft der Bilder – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.13. Grundlage: die Herkunftserklärung des Eigentümers vom 24.11.2026 (Dokument, Kurzfassung als PDF, Verzeichnis mit 113 Einträgen) und Prüfungen in diesem Repo. Das ist ein Nachweis der Herkunft, **keine Lizenz, kein Exklusivitätszertifikat und keine Rechtsberatung**. Das Repo ist öffentlich: Hier stehen keine Einschätzungen zu fremden Spielen.

## 1. Kurzfassung

| Frage | Antwort |
|---|---|
| Womit sind die Bilder entstanden? | Überwiegend mit der Bildgenerierung von OpenAI in ChatGPT, nach Briefings des Eigentümers (`docs/ART_BRIEF.md`), teils mit hochgeladenem Referenzmaterial. Danach zugeschnitten, freigestellt, skaliert und als WebP für die App aufbereitet (Skripte im Repo). |
| Ist die Kette belegt? | **Teilweise.** Von den 78 Bild- und Tondateien in `www/art` und `www/icons` lassen sich 77 aus den gelieferten Paketen mit den Skripten des Repos **bitgleich nachstellen** (geprüft am 24.11.2026, die 17 Dateien der Lieferung vom 25.11.2026 und der Möwen-Streifen des Experiments `exp/moewe-hamburg` am 25.11.2026). Ausnahme: der vorläufige Boden `f1`. Nicht belegt sind Prompt, Modellversion, Tarif und Tag jeder einzelnen Generierung. |
| Wem gehören die Rechte? | Nach den EU-Nutzungsbedingungen von OpenAI stehen dem Nutzer im Verhältnis zu OpenAI die Rechte am Ergebnis zu, soweit rechtlich zulässig; Ergebnisse können denen anderer Nutzer ähneln. Das klärt keine Rechte Dritter (Abschnitt 3). |
| Was steht noch aus? | Siehe Abschnitt 7: Prompts und Tarif, Rechte am Referenzmaterial, Sichtprüfung gegen bekannte Figuren, ersetzbare Entwürfe, Herkunft des Startbilds. |

## 2. Herkunft laut Eigentümer (sinngemäß)

- **Bilder:** Die Motive und Anforderungen stammen aus Briefings des Eigentümers (u. a. `docs/ART_BRIEF.md`), aus den darauf aufbauenden Gesprächen und teilweise aus hochgeladenen Referenzbildern. PNG-Dateien, Vorschauen, Zuschnitte, Hintergrundausschnitte, Transparenzvarianten und Animationen entstanden aus generierten Bildern durch technische Nachbearbeitung. Die 25 Spielgegenstände mit Automaten stammen aus einem KI-gestützten Original-Set, teils aus Sammelillustrationen aufbereitet.
- **Grenze der Dokumentation:** Das Verzeichnis nennt die unmittelbare Quelldatei oder das Paket, nicht zwingend die einzelne Generierung oder den wörtlichen Prompt. Eine lückenlose, promptgenaue Kette je Datei gibt es nicht. Die Prüfsummen (SHA-256) dienen der technischen Identifizierung.
- **Katze Mocha:** Der Eigentümer zeigte einen Screenshot des eigenen Spiels mit Katze als Referenz (Nutzereingabe, kein generiertes Original). Daraufhin entstanden mehrere Katzenbilder; für eine Prototyp-Animation wurden daraus Frames durch Skalierung, Drehung, Verschiebung und Compositing abgeleitet. Das Paket enthält 24 Frames, ein Spritesheet, eine GIF-Vorschau, Konfigurationsdaten und einen synthetisch erzeugten Schnurrton. Nicht jeder Frame ist eine neu gezeichnete Körperpose. Im Paket sind zwei Paare byte-identisch (Frame 2 und 4, Frame 12 und 21); `scripts/cat_import.py` speichert sie nur einmal (22 Bilder). **Seit 1.5.17** bleiben im Spiel nur die drei Ruhebilder (`c01` bis `c03`); die übrigen Frames, die Herzen und der Schnurrton sind aus dem Spiel entfernt, `cat_import.py` schreibt nur noch den Zustand IDLE.
- **Referenzmaterial:** Hochgeladene Screenshots sind Referenz und werden nicht als generierte Spielgrafik ausgegeben.

## 3. Rechtlicher Rahmen und Grenzen

- **Nutzungsbedingungen:** Der Eigentümer hat die EU-Nutzungsbedingungen von OpenAI am 24.11.2026 geprüft (https://openai.com/policies/eu-terms-of-use/). Sinngemäß: Zwischen Nutzer und OpenAI stehen dem Nutzer die Rechte am Output zu, soweit rechtlich zulässig; ähnliche Ergebnisse bei anderen Nutzern sind möglich. Der Agent hat die Seite nicht selbst abgerufen; die Angabe beruht auf der Prüfung des Eigentümers. Wer sicher sein will, liest die Seite vor dem Start selbst oder lässt sie fachkundig einordnen, und hebt eine Kopie des Stands auf.
- **Schutz:** Rein KI-erzeugte Bilder sind nach verbreiteter Ansicht kaum urheberrechtlich geschützt. Dritte könnten sie also kopieren. Name und Gesamtbild schützt eher das Markenrecht (`docs/RECHT_UND_NAMEN.md`).
- **Nicht geklärt:** Rechte Dritter, insbesondere Marken, geschützte Figuren, Fremdbilder in hochgeladenem Referenzmaterial, Musik, Schriften und Screenshots. Eine Stilbeschreibung gegenüber bekannten Spielen ist keine Lizenz für fremde Bilder oder Marken.
- **Nicht behaupten** (Store-Texte, Werbung, Impressum): dass jedes Bild exklusiv urheberrechtlich geschützt, markenrechtlich freigegeben, einzeln extern lizenzgeprüft oder die Herkunft aller Referenzen abschließend geklärt sei. Die Lizenzseite im Spiel nennt die KI-Unterstützung offen.
- **Store-Grafiken:** Die sieben Entwürfe der Bibliothek mit dem alten Namen (Dateien `ALT_…`) werden nicht verwendet. Icon, Feature-Grafiken und Screenshots in `store/` entstehen neu aus dem Spiel (`scripts/store_shots.py`, `scripts/store_promo.py`); KI-Werbekonzepte werden nie als Spiel-Screenshots ausgegeben.

## 4. Was im Repo liegt (`docs/herkunft/`)

| Datei | Inhalt |
|---|---|
| `bibliothek_113_dateien.csv` | Verzeichnis der Asset-Bibliothek des Eigentümers, unverändert wie geliefert: 113 Einträge mit Pfad, Quelle, Status, Hinweisen, Bytes, SHA-256, Pixeln, Modus. Status: fertig 71, prüfen 13, Entwurf 9, Umbenennung nötig 7, Vorschau 6, Referenz 3, Dokumentation 3, Original 1. |
| `Bildherkunft_Erklaerung_2026-11-24.pdf` | Erklärung des Eigentümers (eine Seite). |
| `pakete_dateiliste_sha256.csv` | Inhalt der gelieferten Pakete (Datei, Größe, SHA-256, „steht im Verzeichnis“). Erzeugt mit `scripts/herkunft_pakete.py`. Die Liste des Katzenpakets hat das Projekt aus dem ZIP selbst erzeugt, die vom Eigentümer erwähnte Datei `katzenpaket_dateiliste_sha256.csv` lag nicht bei. |
| `ausgelieferte_dateien.csv` | Manifest aller ausgelieferten Bild-, Ton- und Schriftdateien: Pfad, Spielversion, SHA-256, Maße, Gruppe, Herkunft, Quelle laut Verzeichnis, Nachweis. Erzeugt mit `scripts/asset_manifest.py`; `tests/test_herkunft.py` prüft, dass es aktuell ist. |

## 5. Prüfungen vom 24.11.2026

1. **Pakete gegen Verzeichnis:** Die Prüfsummen der drei Bildpakete (Teile und Automaten 25, Figuren und Gäste 24, Stadtböden-Entwurf 8 von 9 Dateien; die neunte ist ein Hinweistext) stimmen mit dem Verzeichnis des Eigentümers überein. Zusammen mit vier Einzeldateien (Boden Hamburg, Rahmen, Icon-Original, Vorschau Hamburg mit Rahmen) sind **61 von 113 Verzeichnis-Einträgen** per Prüfsumme in den Lieferungen wiedergefunden. Die übrigen 52 (Einzugs-Posen, Stadtrahmen, Store-Entwürfe mit altem Namen, Vorschauen, Dokumente) lagen dem Projekt nicht vor; Einzugs-Posen und Stadtrahmen sind nicht im Spiel.
2. **Nachstellung:** In einer Kopie des Repos wurden die Pakete mit den Skripten neu eingelesen und die Ergebnisse Byte für Byte mit den ausgelieferten Dateien verglichen:
   - 49 Dateien aus den Paketen für Teile, Automaten, Figuren und Gäste: gleich (`scripts/art_import.py`),
   - Boden Hamburg und Rahmen aus den Einzeldateien: gleich; Böden Paris und Rom: gleich (`scripts/floor_prep.py` mit den dokumentierten Maßen, dann `art_import.py`),
   - Katze, drei Ruhebilder (bis 1.5.16: 22 Frames, 3 Herzen und Schnurr-Datei): gleich (`scripts/cat_import.py`),
   - Web- und Android-Icons: gleich aus dem Icon-Original (`assets/src/build-icon.py`); das Original von damals (heute `assets/src/app-icon-original-2026-11-24.png`) hat dieselbe Prüfsumme wie der Verzeichnis-Eintrag `noas_bean_trail_icon_original_1254.png`,
   - **nicht nachstellbar:** `f1` (vorläufiger Boden, Platzhalter für Wien). Die Quelle `f1_berlin.png` steht im Entwurfspaket und im Verzeichnis, die ausgelieferte Datei entstand aber anders oder aus einer anderen Fassung.
3. **Grenze dieser Prüfung:** Sie belegt „Paket → Skript → Spieldatei“. Sie belegt nicht, wie die Pakete selbst entstanden sind. Bitgleichheit gilt für die Bibliotheksversionen vom 24.11.2026 (Pillow, OpenCV, NumPy); andere Versionen können abweichende Bytes liefern, ohne dass die Quelle falsch wäre. Nachstellen immer in einer Kopie des Repos: Die Skripte überschreiben `www/art` und das Bildmanifest in `www/index.html`.

4. **Lieferung vom 25.11.2026 („Stadtpaket“, `Noas_Bean_Trail_Stadtpaket_mit_Animationen_Claude.zip`, 78 Dateien, 41 MB):**
   - **Herkunft laut Begleittext der Lieferung:** Neun Stadtkulissen und eine überarbeitete Pâtisserie-Theke am 25.11.2026 mit der OpenAI-Bildgenerierung erzeugt; die neun Stadtrahmen und 16 Produktgrafiken stammen aus dem früheren Paket. Prompts, Modellversion und Tarif liegen nicht bei. Der Begleittext gibt **keine Zusicherung exklusiver Rechte** und verlangt, Urheber- und Markenrecht sowie Store-Richtlinien vor dem Release gesondert zu prüfen (Abschnitt 7).
   - **Prüfsummen:** Alle 77 Einträge der Liste des Pakets stimmen mit seinem eigenen Manifest überein. Neun Dateien (die Stadtrahmen) stehen auch im Verzeichnis des Eigentümers; der Rahmen `frame_hamburg.png` ist dieselbe Datei wie der bisherige Standardrahmen `frame.png`.
   - **Im Spiel seit 1.5.19:** Kulissen `b0` bis `b8` (aus `bg_<stadt>_portrait.png`, 941×1672, oben auf 9:19,5 ergänzt, bis 1.5.21 als 720×1560 mit gedehnten obersten Zeilen, **seit 1.5.22 neu aufbereitet** als 1220×2644, siehe Punkt 7) und Stadtrahmen `frame1` bis `frame8` (Hamburg nutzt weiter `frame`). Die Böden `f0` bis `f3` bleiben als Rückfall in den Dateien.
   - **Nachstellung (25.11.2026):** In einer Kopie des Repos aus dem ZIP neu erzeugt, alle 17 Dateien **bitgleich**. Die Dateinamen des Pakets passen nicht zum Importmuster, außerdem würden die Kettendateien `g4`, `g5`, `k4_*`, `k5_*` als Spielteile eingelesen. Darum zuerst umbenennen (Welt N: hamburg 0, wien 1, paris 2, rom 3, istanbul 4, kyoto 5, new_york 6, rio 7, sternecafe 8): `bg_<stadt>_portrait.png` → `b<N>_<stadt>.png`, `frame_<stadt>.png` → `frame<N>_<stadt>.png` (ohne Hamburg), alles in einen leeren Ordner, dann `python3 -I scripts/art_import.py <Ordner> --root <Kopie des Repos>`.
   - **Nicht eingebaut:** die Ketten Schokolade und Pâtisserie (`g4`, `g5`, `k4_s1` bis `k5_s7`; im Spiel gibt es dafür keine Ketten, Balancing und Spielstand-Migration fehlen), die neue Pâtisserie-Theke (Kandidat für das nicht vorhandene `g5`), `city_ambience.*` (Animationen erst nach der Prüfung auf dem Handy), die Möwe nur im Experiment-Branch `exp/moewe-hamburg` (Punkt 5) sowie die 768-px-WebPs (die Pipeline erzeugt aus den PNG-Originalen).
   - **Sichtprüfung durch den Agenten (25.11.2026):** In den neun Kulissen sind keine lesbare Schrift, keine Logos und keine Marken zu sehen. Die Kulissen zeigen reale Bauwerke (Abschnitt 7); das Sternecafé ist erfunden.

5. **Möwe, nur im Experiment-Branch `exp/moewe-hamburg` (aus demselben Stadtpaket, Ordner `07_Animationen_Optional/moewe`):**
   - **Herkunft laut README der Lieferung:** Flügelposen am 25.11.2026 mit der OpenAI-Bildgenerierung erzeugt, PNG/WebP/GIF-Ableitungen mit Pillow. Keine Zusicherung exklusiver Rechte (wie das übrige Paket, Punkt 4).
   - **Im Branch:** `www/art/anim/moewe_hamburg.webp` (Streifen 1536×168 aus den acht Flug-Frames `moewe_flug_00.png` bis `moewe_flug_07.png`, je 192×168, 46 KB), erzeugt von `scripts/gull_import.py`; die Tabelle `const GULL` in `www/index.html` schreibt das Skript. Nicht verwendet: `moewe_fluegelschlag.gif`, `moewe_spritestrip_9x256.*`, `moewe_still_256.*`, die Einzel-WebPs und `city_ambience.*`.
   - **Nachstellung (25.11.2026):** In einer Kopie des Repos aus dem ZIP neu erzeugt (`python3 -I scripts/gull_import.py <ZIP> --root <Kopie>`), **bitgleich** (SHA-256 `183dafbc…4ea3`). Das Manifest führt eine Zeile mit allen acht Quell-Frames und ihren Prüfsummen.
   - **Sichtprüfung durch den Agenten (25.11.2026):** kein Text, kein Logo, keine Marke; im Spiel (390×844, 360×800, 412×915) keine sichtbaren Säume an den Rändern.

6. **Lieferung vom 28.11.2026 (Icon „Noa blond“, Chat-Anhang, 1254×1254, 2 465 814 Bytes, SHA-256 `dcf986e4…f003`):**
   - **Herkunft:** vom Eigentümer im Chat geliefert und zum Einbau beauftragt. Werkzeug, Tag und Prompt hat er nicht genannt; die Optik gleicht den KI-Bildern der übrigen Lieferungen. **Rechte nicht zugesichert** (wie Punkt 4).
   - **Im Repo:** `assets/src/app-icon-original.png` (neu; nicht im Verzeichnis, Zeile „Einzeldatei (Upload)“ in der Paketliste). Das bisherige Original liegt als `assets/src/app-icon-original-2026-11-24.png` (Prüfsumme wie im Verzeichnis). `python3 -I assets/src/build-icon.py` baut daraus `assets/icon-*.png`, `store/app-icon-512.png` und `www/icons/*`.
   - **Nachstellung (28.11.2026):** In einer Kopie des Repos neu gebaut, alle sieben Dateien **bitgleich**.
   - **Sichtprüfung durch den Agenten (28.11.2026):** lesbar ist nur der eigene Schriftzug „Noa's Bean Trail“; dazu ein Kaffeebohnen-Zeichen auf Mütze, Tasse, Schürze und Schild und eine Tasse auf dem Café-Schild. Kein Fremdname und kein bekanntes Logo erkannt (Sichtprüfung, keine Markenrecherche). In der runden, der abgerundeten und der maskierbaren Fassung bleiben Gesicht, Katze, Tasse und Schriftzug ganz.

7. **Neu aufbereitet am 28.11.2026 (Version 1.5.22, Branch `exp/hintergrund-scharf`): dieselben neun Kulissen aus dem Stadtpaket (Punkt 4), nur anders verarbeitet.**
   - **Anlass:** Rückmeldung des Eigentümers vom 28.11.2026 (Handy-Screenshot Hamburg): „alles verschwommen“. Befund: (a) oben (hinter der Statusleiste) ein Farbbalken aus gedehnten obersten Zeilen (olivgrün links, blau rechts), (b) die Bilder waren nur 720 px breit und wurden auf dem Handy (um 1220 px) auf das 1,7-Fache gedehnt.
   - **Änderung nur an der Verarbeitung, nicht an den Quellen:** `scripts/art_import.py` setzt oben ruhigen Himmel an (`sky_pad`, Verlauf aus der Himmelsfarbe, oberste 12 % des Bildes gehen weich über) und rechnet auf 1220 px hoch mit leichtem Schärfen (`BG_W`, `BG_SHARP`). Die Quelldateien sind unverändert (`bg_<stadt>_portrait.png`, 941×1672, Prüfsummen in der Paketliste).
   - **Nachstellung (28.11.2026):** In einer Kopie des Repos aus dem ZIP neu erzeugt (Umbenennen wie in Punkt 4), alle neun Dateien **bitgleich** zu den ausgelieferten. Gewicht: 4,3 MB statt 1,9 MB für alle neun.
   - **Sichtprüfung durch den Agenten (28.11.2026):** Himmelsansatz in allen neun Welten ohne Balken und ohne Naht; in Hamburg bei 407×904 mit Statusleiste geprüft (Vorher/Nachher). Keine neuen Inhalte hinzugefügt: der Ansatz ist ein reiner Farbverlauf mit leichtem Rauschen.

8. **Lieferung vom 28.11.2026 (Startbild, erste Seite, Chat-Anhang, 941×1672, 2 171 301 Bytes, SHA-256 `afca2c50…99c9`):**
   - **Herkunft:** vom Eigentümer im Chat geliefert und als neue erste Seite beauftragt. Werkzeug, Tag und Prompt hat er nicht genannt; die Optik gleicht den KI-Bildern der übrigen Lieferungen. **Rechte nicht zugesichert** (wie Punkt 4 und 6).
   - **Im Repo:** `assets/src/start-original.png` (nicht im Verzeichnis, Zeile „Einzeldatei (Upload)“ in der Paketliste). `python3 -I scripts/start_import.py` baut daraus `www/art/start.webp` (1220×2388) und die Tabelle `START` in `www/index.html`: die eingebrannte Versionsnummer wird mit dem Verlauf der Umgebung getilgt (die echte Nummer setzt das Spiel als Text darüber), das Bild unten um 170 Zeilen verlängert (gespiegelt und zunehmend verwischt, damit der Satz „Dein eigenes Café wartet auf dich!“ an sehr hohen Handys nicht am Rand abgeschnitten wird), auf 1220 px Breite vergrößert und leicht nachgeschärft. Das Spiel zeigt das Bild nur bei deutscher Sprache (der Text im Bild ist deutsch) und nur bei eingeschaltetem `CONFIG.features.startImg`.
   - **Nachstellung (28.11.2026):** In einer Kopie des Repos neu gebaut, **bitgleich** (`tests/test_startbild.py`, Abschnitt H).
   - **Sichtprüfung durch den Agenten (28.11.2026):** lesbar sind „Noa's Bean Trail“, „Dein eigenes Café wartet auf dich!“, „Spielen“ und die Versionsnummer (im Spiel getilgt und durch echten Text ersetzt). Kein Fremdname und kein bekanntes Logo erkannt (Sichtprüfung, keine Markenrecherche). Die acht Bohnen im Bild sind reine Dekoration.

## 6. Regeln für neue Dateien

1. Die Pakete gelten als projektintern erzeugte KI-Bilder. Die Herkunftserklärung ist **keine zusätzliche Lizenz**.
2. **Keine neuen externen Bild-, Ton- oder Schriftdateien** ohne notierte Quelle und Lizenz (zuerst in `docs/ASSETS_LIZENZEN.md` eintragen, dann einbauen).
3. Alle ausgelieferten Dateien stehen im Manifest. Nach jeder Änderung an `www/art`, `www/icons`, `www/ofl` oder `assets/`: `python3 -I scripts/asset_manifest.py` und die CSV mitcommitten.
4. **Neue Lieferung:** Dateiliste mit Prüfsummen eintragen (`python3 -I scripts/herkunft_pakete.py <ZIP-oder-Ordner>`), dazu Datum, Werkzeug und Briefing oder Prompt festhalten. Originale und Prompts gehören in die Bibliothek des Eigentümers, nicht ins öffentliche Repo. Danach nachstellen (Abschnitt 5, Punkt 2) und das Ergebnis in den Mustern `ART_NACHGESTELLT` und `BODEN_NACHGESTELLT` von `scripts/asset_manifest.py` nachführen; ohne Nachstellung bleibt der Nachweis leer.
5. Screenshots und Referenzbilder des Eigentümers nur als Referenz behandeln, nie als generierte Spielgrafik ausgeben.
6. Alte Versionen und Rohdaten aufheben (Bibliothek des Eigentümers).

## 7. Offen

| Punkt | Wer |
|---|---|
| Tarif, Modellversion, Tag und Prompt je Bild nicht festgehalten; ab jetzt je Lieferung festhalten | Eigentümer, laufend |
| Icon „Noa blond“ (28.11.2026): Werkzeug, Tag und Prompt festhalten; ob und wie der Store-Eintrag es als KI-Bild kennzeichnet, entscheidet der Eigentümer | Eigentümer |
| Nutzungsbedingungen von OpenAI: Stand des Abrufs sichern (Kopie mit Datum) und fachkundig einordnen lassen | Eigentümer |
| Rechte am hochgeladenen Referenzmaterial (Screenshots, Referenzbilder) prüfen | Eigentümer |
| Figuren, Gäste und Teile einmal gegen bekannte Figuren und Logos ansehen (zufällige Ähnlichkeit) | Eigentümer, optional mit fachkundiger Hilfe |
| ~~Entwürfe ersetzen: Böden `f1` bis `f3`, Böden 4 bis 8, Stadtrahmen~~ seit 1.5.19 überholt: Die Vollbild-Kulissen `b0` bis `b8` ersetzen die Böden (die Böden `f0` bis `f3` bleiben als Rückfall), die Stadtrahmen `frame1` bis `frame8` sind geliefert und eingebaut | – |
| Einzugs-Posen liegen im Verzeichnis, aber nicht im Projekt: als ZIP liefern, dann importiert und nachgestellt der Agent | Eigentümer, dann Agent |
| Bildrechte an den abgebildeten Bauwerken (Elbphilharmonie, Riesenrad und Stephansdom, Eiffelturm, Kolosseum, Hagia Sophia, Brooklyn Bridge und Freiheitsstatue, Zuckerhut und Christusstatue) und KI-Kennzeichnung im Store vor dem Upload fachkundig einordnen lassen (kein Rechtsrat des Agenten; bekannter Sonderfall: die nächtliche Beleuchtung des Eiffelturms, hier ist es eine Tagesansicht) | Eigentümer |
| Möwe (Experiment `exp/moewe-hamburg`): vor dem Zusammenführen auf einem echten Handy ansehen (Größe, Ränder) und dieselbe Einordnung wie bei den Stadtbildern (Rechte, KI-Kennzeichnung) | Eigentümer, Gerätetest |
| Startbild (`assets/splash*.png`): Herkunft nicht protokolliert und nicht im Verzeichnis; bestätigen oder ersetzen | Eigentümer |
| ~~Schnurr-Datei ersetzen~~ erledigt: Datei seit 1.5.17 entfernt, kein Ton mehr | – |
| Transparenzkanten und Darstellung kleiner Spielfiguren auf dem Gerät prüfen | Eigentümer, beim Gerätetest |
| Ob die Stores eine Kennzeichnung KI-erzeugter Bilder verlangen, vor dem Upload in den dann gültigen Richtlinien nachlesen | Eigentümer |
