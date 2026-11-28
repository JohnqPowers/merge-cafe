# Experimente: kontrollierte Weiterentwicklung

Stand 28.11.2026. Grundlage sind die sieben Entwicklungsregeln des Eigentümers (`CLAUDE.md`, Abschnitt „Entwicklungsregeln“). Ziel: die laufende App nicht durch viele gleichzeitige Änderungen verschlechtern. Weiterentwickeln, nicht neu bauen.

## Ablauf je Experiment
1. **Branch von `main`:** `git switch -c exp/<kurzname>`. Auf `main` landen Experimente nie von selbst.
2. **Schalter:** `CONFIG.features.<name>` (true/false) in `www/index.html`. Aus heißt: keine Elemente, keine Timer, keine Netzzugriffe. Für Web-Tests zusätzlich der Adressparameter `?<name>=0` oder `?<name>=1`.
3. **Nur hinzufügen:** neuer Block, neue Datei, einzelne Aufrufzeilen. Bestehende Zeilen nur ändern, wenn es nicht anders geht, und im Bericht einzeln nennen. Prüfung: `git diff --numstat 0c1bd88 -- www/index.html` (zweite Zahl = entfernte Zeilen).
4. **Version:** nächste freie Nummer in `CONFIG.version`, rein numerisch `x.y.z` (sonst bricht `scripts/asset_manifest.py`). Beim späteren Zusammenführen wird neu vergeben.
5. **Neue Bilder und Töne:** Quelle und Lizenz in `docs/HERKUNFT_BILDER.md` notieren, danach `python3 -I scripts/asset_manifest.py`.
6. **Tests:** eigener Test `tests/test_<name>.py` (läuft in `run_alle.py` automatisch mit), dann Vorher-Nachher (unten).
7. **Vorführen ohne `main` anzufassen:** Video, Bilder oder eine Vorschau außerhalb der Web-Veröffentlichung. Auf dem Branch niemals `web.yml` oder `android.yml` starten (Pages und Release `test-apk` gehören `main`).
8. **Bericht** an den Eigentümer mit der Vorher-Nachher-Tabelle. Zusammengeführt wird nur auf dessen ausdrücklichen Auftrag.

## Vorher-Nachher (Regel 6)
```
git worktree add --detach /tmp/ref 0c1bd88                              # Referenzstand 1.5.19
python3 -I tests/run_alle.py --wurzel /tmp/ref --json /tmp/vorher.json  # alle Tests auf dem Referenzstand
python3 -I tests/run_alle.py --json /tmp/nachher.json                   # alle Tests im Branch
python3 -I tests/run_alle.py --vergleich /tmp/vorher.json /tmp/nachher.json
```
Neue Tests erscheinen in der Tabelle als „neu“. Jeder „Rückschritt“ muss vor dem Zusammenführen behoben sein.

Referenz ist der Commit `0c1bd88`, kein Tag: Das Pushen von `v1.5.19` hat die Agenten-Sitzung am 25.11.2026 mit HTTP 403 abgelehnt (Repo-Regeln gibt es nicht, es liegt an der Sitzung; umgangen wurde das nicht). Wer den Tag trotzdem möchte, legt ihn am eigenen Rechner an: `git tag -a v1.5.19 0c1bd88 -m "Referenzstand 1.5.19" && git push origin v1.5.19`.

## Zusammenführen (nur auf Auftrag)
`git switch main && git merge --no-ff exp/<kurzname>`, Version neu vergeben, alle Tests erneut, dann pushen. Der Push auf `main` löst Android-Build und Web-Veröffentlichung aus. Rückgängig: der Schalter (ohne neuen Code) oder `git revert` des Merge-Commits.

## Übersicht
| Branch | Inhalt | Schalter | Stand |
|---|---|---|---|
| `exp/moewe-hamburg` | Möwe fliegt im sichtbaren Hintergrund von Hamburg (Welt 1) | `CONFIG.features.gull`, `?gull=0` | Version 1.5.20 fertig und getestet; **28.11.2026 auf Auftrag des Eigentümers nach `main` zusammengeführt** (Standard `true`) |
| `exp/icon-noa` | neues App-Icon „Noa blond“ (Android, Web, Store-Datei) | kein Schalter (Dateiaustausch; Rückgängig per `git revert`) | Version 1.5.21; 28.11.2026 auf Auftrag zusammen mit der Möwe nach `main` zusammengeführt |
| `exp/hintergrund-scharf` | Kulissen `b0`…`b8` neu aufbereitet: ruhiger Himmelsansatz statt Farbbalken, 1220 px statt 720 px breit | kein Schalter (Dateiaustausch; Rückgängig per `git revert`) | zusammengeführt am 28.11.2026 (Version 1.5.22, Merge `597c468`) |
| `exp/moewe-fenster` | Möwe fliegt auch im schmalen freien Fenster (ab 28 px statt 64 px), Größe folgt der Höhe | `CONFIG.features.gull` (bestehend), `?gull=0` | zusammengeführt am 28.11.2026 (Version 1.5.22, Merge `597c468`) |
| `exp/startbild` | neue erste Seite (Bild des Eigentümers); Version und „Willkommen zurück“ als echter Text, Knopf als unsichtbare Fläche | `CONFIG.features.startImg`, `?startimg=0` / `?startimg=1` | zusammengeführt am 28.11.2026 (Version 1.5.22, Merge `597c468`) |
| `exp/entwickler` | Entwickler-Vorschau: durch alle neun Welten und Level 1 bis 60 springen, ohne zu speichern | `CONFIG.features.devMenu`, `?dev=0` / `?dev=1` | zusammengeführt am 28.11.2026 (Version 1.5.22, Merge `597c468`) |
| `exp/klangmix` | Musik auf dem Handy rund 9 dB lauter, Effekte 3 dB leiser | `CONFIG.features.mix`, `?mix=0` / `?mix=1` | zusammengeführt am 28.11.2026 (Version 1.5.22, Merge `597c468`) |
| `exp/kandidat-1522` | Zusammenführung der fünf Branches oben, Version 1.5.22 (einmal vergeben) | die vier Schalter oben | alle Tests grün (Tabelle unten); zusammengeführt am 28.11.2026 auf Auftrag des Eigentümers (Merge `597c468`) |
| `exp/lieferbonus` | freiwilliger Lieferbonus nach drei erledigten Bestellungen | offen | **nicht begonnen** (Auftrag vom 25.11.2026: noch nicht umsetzen) |

### Möwe über Hamburg: Ergebnis (28.11.2026)
Version 1.5.20 im Branch `exp/moewe-hamburg`, Schalter `CONFIG.features.gull` (im Branch auf `true`, damit man sie sieht), Web-Test `?gull=0` / `?gull=1`. Nur hinzugefügt (+129 / −1 Zeilen in `www/index.html`, die eine entfernte Zeile ist die Versionszeile), neue Datei `www/art/anim/moewe_hamburg.webp` mit Herkunft in `docs/HERKUNFT_BILDER.md`.

| Test | Vorher (Referenz 0c1bd88) | Nachher (Möwe + Icon, 1.5.21) | Bewertung |
|---|---|---|---|
| test_ausrichtung | ALLE | ALLE | gleich |
| test_gesamt 390×844 | 24/24 | 24/24 | gleich |
| test_gesamt 360×640 | 24/24 | 24/24 | gleich |
| test_herkunft | ALLE | ALLE | gleich |
| test_hintergrund | 20/20 | 20/20 | gleich |
| test_katze | 11/11 | 11/11 | gleich |
| test_plattform | 115/115 | 115/115 | gleich |
| test_spielstand | ALLE | ALLE | gleich |
| test_store | ALLE | ALLE | gleich |
| test_wortwahl | 12/12 | 12/12 | gleich |
| test_moewe | – | 86/86 | neu |

**Zusammengeführt am 28.11.2026** auf ausdrücklichen Auftrag des Eigentümers (Regel 7), zusammen mit dem neuen Icon als Version 1.5.21: zuerst `exp/moewe-hamburg`, dann `exp/icon-noa`, je mit `--no-ff` (zwei Merge-Commits, einzeln rückgängig zu machen). Die Tabelle zeigt den Lauf auf dem Kandidaten vor dem Merge (11 Läufe, 10 min 34 s). Standard im Build: `true`; abschalten heißt `features.gull: false` in `CONFIG` und ein neuer Build (im Android-Build gibt es keinen Adressparameter). **Offen:** Blick auf einem echten Handy (Akku, Bildrate, Android-WebView). Der Wächter gilt nur für die laufende Sitzung und speichert nichts.

### Kandidat 1.5.22 (28.11.2026): fünf Rückmeldungen des Eigentümers
Branch `exp/kandidat-1522`, aus `main` (45aa030) mit den fünf Experiment-Branches je per `--no-ff` zusammengeführt, die Version **einmal** vergeben (1.5.21 → 1.5.22). Konflikte gab es nur in Doku, `scripts/asset_manifest.py` (beide Seiten behalten) und in der Schalter-Zeile `CONFIG.features` sowie bei den CSS-Blöcken von Startbild und Entwickler-Leiste (beide behalten). Das Manifest der ausgelieferten Dateien ist neu erzeugt (93 Dateien, 8 ohne Nachweis-Vermerk, unverändert). **Zusammengeführt am 28.11.2026 um 19:20 Uhr auf ausdrücklichen Auftrag des Eigentümers („mergen“, Regel 7)**, Merge-Commit `597c468`; rückgängig: `git revert -m 1 597c468`.

**Anlass (Rückmeldung vom 28.11.2026, 15:15 Uhr):** erste Seite ersetzen („Passt das?“), Hamburg „verschwommen“ und Möwe unsichtbar, ein Weg für den Entwickler durch die Stufen, Musik zu leise und Effekte zu laut.

| Bereich | Befund | Änderung |
|---|---|---|
| Möwe | Auf hohen Handys ist das freie Fenster zwischen Bestellleiste und Brett nur etwa 36 bis 60 px hoch; der Code verlangte 64 px, also blieb die Möwe ganz aus | Untergrenze 28 px, Größe folgt der Fensterhöhe (94 %, höchstens 16 % der Breite) |
| Hintergründe | oben ein Farbbalken aus gedehnten obersten Zeilen (olivgrün links, blau rechts), Bilder nur 720 px breit | ruhiger Himmelsansatz, 1220 px breit, leicht geschärft (4,3 MB statt 1,9 MB für neun) |
| Startbild | Bild 9:16 gegen Handys bis 9:21: Seiten werden etwa 9 % beschnitten, Knopf bleibt ganz | neues Bild als Vollbild; eingebrannte Versionsnummer getilgt und als echter Text gesetzt; altes Startbild bleibt Rückfall (englische Sprache, Ladefehler, Schalter aus) |
| Entwickler | keine Möglichkeit, Stufen zu sehen, ohne sie zu spielen | Vorschau-Leiste; Öffnen: Optionen, siebenmal innerhalb von 4 s auf die Versionszeile tippen |
| Klang | auf einem Handy-Lautsprecher (Hochpass 300 Hz) lag die Musik rund 22 dB unter Zusammenführen und Liefern: die Musik besteht zum größten Teil aus tiefem Bass, den ein Handy kaum spielt | Musik +10 dB, Bass-Stimme zusätzlich −7 dB, Effekte −3 dB; Abstand 21,8 → 9,4 dB; alle lauten Effekte über Musik: Spitze −1,7 → −4,4 dBFS |

**Entwickler-Vorschau:** erlaubt nur im Debug-Paket (Test-APK, `Platform.build.kind === 'debug'`) und im Web mit `?dev=1`; im Play-Paket und bei `devMenu: false` gibt es weder Element noch Wirkung der Geste. Die Leiste hat neun Welt-Tasten, Regler und Plus/Minus, die Möwen-Auskunft (`MC.gull.why()`) und „Möwe zeigen“. Sie speichert nichts: `save()` ist eingefroren, der echte Stand liegt als Abbild bereit, Ereignisse tragen `dev:true` und gehen nicht an die Auswertung. Beenden stellt Stand, Kulisse und Anzeige wieder her; auch Neuladen mitten in der Vorschau lässt den echten Stand unberührt (`tests/test_entwickler.py`, 63 Prüfungen).

**Klang-Schalter:** `CONFIG.features.mix`, Web-Test `?mix=0` (= Stand 1.5.21, bit-gleicher Graph) / `?mix=1`. Die Zahlen stehen an einer Stelle: Konstante `MIX` vor dem Modul `Sound` in `www/index.html` (`sfx`, `mus`, `duck`, `bass`). Gemessen wird mit einem Abgriff hinter dem Verdichter (`tests/test_klangmix.py`, 22 Prüfungen, aus und an im selben Lauf).

| Test | Vorher (Referenz 0c1bd88, 1.5.19) | Nachher (Kandidat 1.5.22, d4ed7cf) | Bewertung |
|---|---|---|---|
| test_ausrichtung | ALLE | ALLE | gleich |
| test_gesamt 390×844 | 24/24 | 24/24 | gleich |
| test_gesamt 360×640 | 24/24 | 24/24 | gleich |
| test_herkunft | ALLE | ALLE | gleich |
| test_hintergrund | 20/20 | 21/21 | geändert: eine Prüfung ergänzt (ruhiger Himmelsansatz statt Farbbalken), eine angepasst; kein Rückschritt |
| test_katze | 11/11 | 11/11 | gleich |
| test_plattform | 115/115 | 115/115 | gleich |
| test_spielstand | ALLE | ALLE | gleich |
| test_store | ALLE | ALLE | gleich |
| test_wortwahl | 12/12 | 12/12 | gleich |
| test_entwickler | – | 63/63 | neu |
| test_klangmix | – | 22/22 | neu |
| test_moewe | – | 107/107 | neu (Stand 1.5.21: 86/86; 21 Prüfungen für das schmale Fenster ergänzt) |
| test_startbild | – | 139/139 | neu |

Alle 14 Läufe grün (`python3 -I tests/run_alle.py --json /tmp/nachher.json` in einer getrennten Arbeitskopie des Kandidaten, rund 20 Minuten). Das Ergebnis gilt für den Commit `d4ed7cf`; spätere Commits im Branch ändern nur Doku.

### Lieferbonus: was vor dem Start geklärt sein muss
Berührt Belohnungen und, je nach Ausführung, Werbung (Monetarisierung): vor dem ersten Code Freigabe des Eigentümers.
- Was ist der Bonus (Münzen, Diamanten, Energie, ein Teil) und wie hoch?
- „Freiwillig“: Abholen per Tipp ohne Gegenleistung, oder optional verdoppeln per Werbung (dann nur bei `legalReady`, nie für Kinder beworben)?
- Zählung: drei Bestellungen in Folge, pro Tag oder insgesamt? Was passiert beim Abbrechen?
- Messung: Anteil, der den Bonus abholt, und D1/D7 gegenüber dem Referenzstand.
