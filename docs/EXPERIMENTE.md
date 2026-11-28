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
| `exp/moewe-hamburg` | Möwe fliegt im sichtbaren Hintergrund von Hamburg (Welt 1) | `CONFIG.features.gull`, `?gull=0` | Version 1.5.20 im Branch fertig und getestet (28.11.2026), **nicht zusammengeführt**, Vorschau als privater Link |
| `exp/lieferbonus` | freiwilliger Lieferbonus nach drei erledigten Bestellungen | offen | **nicht begonnen** (Auftrag vom 25.11.2026: noch nicht umsetzen) |

### Möwe über Hamburg: Ergebnis (28.11.2026)
Version 1.5.20 im Branch `exp/moewe-hamburg`, Schalter `CONFIG.features.gull` (im Branch auf `true`, damit man sie sieht), Web-Test `?gull=0` / `?gull=1`. Nur hinzugefügt (+129 / −1 Zeilen in `www/index.html`, die eine entfernte Zeile ist die Versionszeile), neue Datei `www/art/anim/moewe_hamburg.webp` mit Herkunft in `docs/HERKUNFT_BILDER.md`.

| Test | Vorher (Referenz 0c1bd88) | Nachher (Branch) | Bewertung |
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

**Vor dem Zusammenführen offen:** (1) Blick auf einem echten Handy (Akku, Bildrate, Android-WebView); (2) Entscheidung des Eigentümers, ob der Standard im Build `true` oder `false` ist (im Android-Build gibt es keinen Adressparameter, abschalten heißt eine Zeile in `CONFIG.features` und einen neuen Build); (3) Zusammenführen nur auf ausdrücklichen Auftrag (Regel 7), danach Version neu vergeben und alle Tests erneut. Der Wächter gilt nur für die laufende Sitzung und speichert nichts.

### Lieferbonus: was vor dem Start geklärt sein muss
Berührt Belohnungen und, je nach Ausführung, Werbung (Monetarisierung): vor dem ersten Code Freigabe des Eigentümers.
- Was ist der Bonus (Münzen, Diamanten, Energie, ein Teil) und wie hoch?
- „Freiwillig“: Abholen per Tipp ohne Gegenleistung, oder optional verdoppeln per Werbung (dann nur bei `legalReady`, nie für Kinder beworben)?
- Zählung: drei Bestellungen in Folge, pro Tag oder insgesamt? Was passiert beim Abbrechen?
- Messung: Anteil, der den Bonus abholt, und D1/D7 gegenüber dem Referenzstand.
