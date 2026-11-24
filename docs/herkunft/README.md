# Herkunftsnachweise für die Bilder

Einordnung, Prüfungen und offene Punkte stehen in `docs/HERKUNFT_BILDER.md`. Diese Ablage enthält nur die Dateien.

| Datei | Inhalt | Herkunft |
|---|---|---|
| `bibliothek_113_dateien.csv` | Verzeichnis der Asset-Bibliothek des Eigentümers (113 Einträge: Pfad, Quelle, Status, Hinweise, Bytes, SHA-256, Pixel, Modus). Unverändert wie geliefert: UTF-8 mit BOM, Windows-Zeilenenden. | Eigentümer, 24.11.2026 |
| `Bildherkunft_Erklaerung_2026-11-24.pdf` | Erklärung des Eigentümers zur Herkunft der Grafiken (eine Seite). | Eigentümer, 24.11.2026 |
| `pakete_dateiliste_sha256.csv` | Inhalt der gelieferten ZIP-Pakete und vier Einzeldateien: Datei, Bytes, SHA-256, ob die Prüfsumme im Verzeichnis steht, Eintragsdatum. | `python3 -I scripts/herkunft_pakete.py <ZIP-oder-Ordner>` |
| `ausgelieferte_dateien.csv` | Manifest der ausgelieferten Bild-, Ton- und Schriftdateien mit Spielversion, SHA-256, Quelle laut Verzeichnis und Nachweis. | `python3 -I scripts/asset_manifest.py` (Prüfung: `--pruefen`, Test: `tests/test_herkunft.py`) |

Die vom Eigentümer in der Erklärung erwähnten Begleitdateien `katzenpaket_dateiliste_sha256.csv` und `KURZTEXT_FUER_CLAUDE.txt` lagen nicht bei. Die Dateiliste des Katzenpakets steht deshalb in `pakete_dateiliste_sha256.csv`, aus dem ZIP selbst erzeugt.

Originale, Prompts und Rohdaten gehören nicht in dieses öffentliche Repo, sondern in die Bibliothek des Eigentümers.
