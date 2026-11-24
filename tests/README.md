# Browser-Tests

Automatische Tests mit Playwright (Python) und Chrome. Sie laufen ohne Handy; echte Geräte ersetzen sie nicht (siehe `docs/QUALITAET.md`).

| Datei | Was geprüft wird |
|---|---|
| `test_gesamt.py` | Start, Profil, Tutorial bis zur ersten Lieferung, Spiel bis Level 6, Geschenke, Demo-Werbung, Shop, Neustart, keine Konsolenfehler (23 Prüfungen) |
| `test_plattform.py` | Einwilligung vor Werbung und Messung, Widerruf, Store-Preise, Kauf, Sperre bei unvollständigen Rechtstexten, Browser-Variante (mit nachgebauten Plugins, 46 Prüfungen) |
| `test_katze.py` | Katze Mocha: Sprung, Landung, Streicheln, Rückkehr, Sonderfälle |

Aufruf aus dem Projektordner: `python3 -I tests/test_gesamt.py 390 844` (zweite Größe z. B. `360 640`), `python3 -I tests/test_plattform.py`, `python3 -I tests/test_katze.py`.
Voraussetzung: `pip install playwright` und ein installiertes Chrome (Pfad per Umgebungsvariable `CHROME`, Standard `/usr/bin/google-chrome`).
`state.json` ist ein Spielstand auf Level 12 (Paris), den die Tests einspielen.
