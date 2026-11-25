# Browser-Tests

Automatische Tests mit Playwright (Python) und Chrome. Sie laufen ohne Handy; echte Geräte ersetzen sie nicht (siehe `docs/QUALITAET.md`).

| Datei | Was geprüft wird |
|---|---|
| `test_gesamt.py` | Start, Profil, Tutorial bis zur ersten Lieferung, Spiel bis Level 6, Geschenke, Demo-Werbung, Shop, Neustart, keine Konsolenfehler (24 Prüfungen) |
| `test_plattform.py` | Einwilligung vor Werbung und Messung, Widerruf, Store-Preise, Kauf, Sperre bei unvollständigen Rechtstexten, Debug-Paket mit Test-Anzeigenblock, Browser-Variante (mit nachgebauten Plugins, 54 Prüfungen) |
| `test_ausrichtung.py` | Dreh-Hinweis im Querformat auf dem Handy, keiner bei Tablets und Hochformat (11 Prüfungen) |
| `test_spielstand.py` | alte, unvollständige, kaputte und fremde Spielstände laden ohne Absturz (20 Prüfungen) |
| `test_katze.py` | Katze Mocha: Ruhebild, nur drei Dateien geladen, Antippen, fehlende Bilder, 360×640, 5 Plätze |
| `test_hintergrund.py` | Vollbild-Hintergrund je Welt (`b0` bis `b8`) und Stadtrahmen: Aufbereitung (oben auf 9:19,5 ergänzt), Dateien, alle neun Welten, breites Fenster der Web-Version, Rückfall ohne Bild (20 Prüfungen) |
| `test_wortwahl.py` | Wortwahl und Anzeige ab 1.5.17: „Take-away“ statt „Verkaufen“, „Bessere Artikel“ mit Chance in Prozent, Hinweis „Stufe 2!“ beim Glückstreffer, Stufe 1 ohne Zahl (12 Prüfungen, Deutsch und Englisch) |
| `test_herkunft.py` | Herkunftsnachweise ohne Browser: Manifest der ausgelieferten Dateien (`docs/herkunft/ausgelieferte_dateien.csv`) ist aktuell, Verzeichnis des Eigentümers und Paketlisten stimmig, keine Namen anderer Spiele in den Herkunftsdateien (16 Prüfungen, braucht nur Pillow) |
| `test_store.py` | Store-Unterlagen ohne Browser: Zeichenlängen und Regeln der Texte in `docs/STORE_LISTING.md`, Zahlen im Text gegen den Code, Alt-Texte, Bildformate in `store/` (91 Prüfungen, braucht nur Pillow) |

Aufruf aus dem Projektordner: `python3 -I tests/test_gesamt.py 390 844` (zweite Größe z. B. `360 640`), `python3 -I tests/test_plattform.py`, `python3 -I tests/test_ausrichtung.py`, `python3 -I tests/test_spielstand.py`, `python3 -I tests/test_store.py`, `python3 -I tests/test_herkunft.py`, `python3 -I tests/test_katze.py` (druckt ein Ablaufprotokoll, keine Zählung).
**Alle Tests auf einmal:** `python3 -I tests/run_alle.py` (findet jeden `tests/test_*.py`, zeigt eine Tabelle, Ausgang 1 bei Fehlern; `--json datei` speichert das Ergebnis, `--wurzel /pfad` läuft in einem anderen Arbeitsverzeichnis, z. B. einem `git worktree` des Referenzstands, `--vergleich vorher.json nachher.json` zeigt die Vorher-Nachher-Tabelle). Ablauf für Experimente: `docs/EXPERIMENTE.md`.
Voraussetzung: `pip install playwright` und ein installiertes Chrome (Pfad per Umgebungsvariable `CHROME`, Standard `/usr/bin/google-chrome`).
`state.json` ist ein Spielstand auf Level 12 (Paris), den die Tests einspielen.
