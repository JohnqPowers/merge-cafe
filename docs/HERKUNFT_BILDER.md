# Herkunft der Bilder – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.13. Grundlage: die Herkunftserklärung des Eigentümers vom 24.11.2026 (Dokument, Kurzfassung als PDF, Verzeichnis mit 113 Einträgen) und Prüfungen in diesem Repo. Das ist ein Nachweis der Herkunft, **keine Lizenz, kein Exklusivitätszertifikat und keine Rechtsberatung**. Das Repo ist öffentlich: Hier stehen keine Einschätzungen zu fremden Spielen.

## 1. Kurzfassung

| Frage | Antwort |
|---|---|
| Womit sind die Bilder entstanden? | Überwiegend mit der Bildgenerierung von OpenAI in ChatGPT, nach Briefings des Eigentümers (`docs/ART_BRIEF.md`), teils mit hochgeladenem Referenzmaterial. Danach zugeschnitten, freigestellt, skaliert und als WebP für die App aufbereitet (Skripte im Repo). |
| Ist die Kette belegt? | **Teilweise.** Von den 83 Bild- und Tondateien in `www/art` und `www/icons` lassen sich 82 aus den gelieferten Paketen mit den Skripten des Repos **bitgleich nachstellen** (geprüft am 24.11.2026). Ausnahme: der vorläufige Boden `f1`. Nicht belegt sind Prompt, Modellversion, Tarif und Tag jeder einzelnen Generierung. |
| Wem gehören die Rechte? | Nach den EU-Nutzungsbedingungen von OpenAI stehen dem Nutzer im Verhältnis zu OpenAI die Rechte am Ergebnis zu, soweit rechtlich zulässig; Ergebnisse können denen anderer Nutzer ähneln. Das klärt keine Rechte Dritter (Abschnitt 3). |
| Was steht noch aus? | Siehe Abschnitt 7: Prompts und Tarif, Rechte am Referenzmaterial, Sichtprüfung gegen bekannte Figuren, ersetzbare Entwürfe, Herkunft des Startbilds. |

## 2. Herkunft laut Eigentümer (sinngemäß)

- **Bilder:** Die Motive und Anforderungen stammen aus Briefings des Eigentümers (u. a. `docs/ART_BRIEF.md`), aus den darauf aufbauenden Gesprächen und teilweise aus hochgeladenen Referenzbildern. PNG-Dateien, Vorschauen, Zuschnitte, Hintergrundausschnitte, Transparenzvarianten und Animationen entstanden aus generierten Bildern durch technische Nachbearbeitung. Die 25 Spielgegenstände mit Automaten stammen aus einem KI-gestützten Original-Set, teils aus Sammelillustrationen aufbereitet.
- **Grenze der Dokumentation:** Das Verzeichnis nennt die unmittelbare Quelldatei oder das Paket, nicht zwingend die einzelne Generierung oder den wörtlichen Prompt. Eine lückenlose, promptgenaue Kette je Datei gibt es nicht. Die Prüfsummen (SHA-256) dienen der technischen Identifizierung.
- **Katze Mocha:** Der Eigentümer zeigte einen Screenshot des eigenen Spiels mit Katze als Referenz (Nutzereingabe, kein generiertes Original). Daraufhin entstanden mehrere Katzenbilder; für eine Prototyp-Animation wurden daraus Frames durch Skalierung, Drehung, Verschiebung und Compositing abgeleitet. Das Paket enthält 24 Frames, ein Spritesheet, eine GIF-Vorschau, Konfigurationsdaten und einen synthetisch erzeugten Schnurrton. Nicht jeder Frame ist eine neu gezeichnete Körperpose. Im Paket sind zwei Paare byte-identisch (Frame 2 und 4, Frame 12 und 21); `scripts/cat_import.py` speichert sie nur einmal (22 Bilder).
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
   - Katze, 22 Frames, 3 Herzen und Schnurr-Datei: gleich (`scripts/cat_import.py`),
   - Web- und Android-Icons: gleich aus dem Icon-Original (`assets/src/build-icon.py`); das Original im Repo hat dieselbe Prüfsumme wie der Verzeichnis-Eintrag `noas_bean_trail_icon_original_1254.png`,
   - **nicht nachstellbar:** `f1` (vorläufiger Boden, Platzhalter für Wien). Die Quelle `f1_berlin.png` steht im Entwurfspaket und im Verzeichnis, die ausgelieferte Datei entstand aber anders oder aus einer anderen Fassung.
3. **Grenze dieser Prüfung:** Sie belegt „Paket → Skript → Spieldatei“. Sie belegt nicht, wie die Pakete selbst entstanden sind. Bitgleichheit gilt für die Bibliotheksversionen vom 24.11.2026 (Pillow, OpenCV, NumPy); andere Versionen können abweichende Bytes liefern, ohne dass die Quelle falsch wäre. Nachstellen immer in einer Kopie des Repos: Die Skripte überschreiben `www/art` und das Bildmanifest in `www/index.html`.

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
| Nutzungsbedingungen von OpenAI: Stand des Abrufs sichern (Kopie mit Datum) und fachkundig einordnen lassen | Eigentümer |
| Rechte am hochgeladenen Referenzmaterial (Screenshots, Referenzbilder) prüfen | Eigentümer |
| Figuren, Gäste und Teile einmal gegen bekannte Figuren und Logos ansehen (zufällige Ähnlichkeit) | Eigentümer, optional mit fachkundiger Hilfe |
| Entwürfe ersetzen: Böden `f1` bis `f3` (Verzeichnis: für die finale App einzeln neu erzeugen), Böden 4 bis 8, zwei Stadtrahmen | Eigentümer |
| Einzugs-Posen und Stadtrahmen liegen im Verzeichnis, aber nicht im Projekt: als ZIP liefern, dann importiert und nachgestellt der Agent | Eigentümer, dann Agent |
| Startbild (`assets/splash*.png`): Herkunft nicht protokolliert und nicht im Verzeichnis; bestätigen oder ersetzen | Eigentümer |
| Schnurr-Datei: synthetischer Platzhalter, durch eine eigene oder lizenzierte Aufnahme ersetzen | Eigentümer |
| Transparenzkanten und Darstellung kleiner Spielfiguren auf dem Gerät prüfen | Eigentümer, beim Gerätetest |
| Ob die Stores eine Kennzeichnung KI-erzeugter Bilder verlangen, vor dem Upload in den dann gültigen Richtlinien nachlesen | Eigentümer |
