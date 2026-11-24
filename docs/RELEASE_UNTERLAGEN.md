# Unterlagen vor dem Store-Start – Übersicht

Stand: 24.11.2026, Spielversion 1.5.13 (Push auf `main` vom Eigentümer am 24.11.2026 freigegeben; **nichts bei Google, Apple oder Almedia eingereicht**). Diese Seite zeigt auf einen Blick die neun Unterlagen, die der Eigentümer am 24.11.2026 vor dem Verkauf verlangt hat, dazu Werbung und Bezahlfunktion. Keine Rechtsberatung: Datenschutz, Impressum und Altersfreigabe sind sorgfältige Entwürfe und sollten vor dem Start einmal fachkundig durchgesehen werden.

## 1. Die neun Unterlagen

| Nr. | Unterlage | Dateien | Stand | Was noch fehlt (wer) |
|---|---|---|---|---|
| 1 | Datenschutzerklärung | `www/privacy.html` (Seite für Spieler), `docs/PRIVACY.md` (Datenflüsse, Entwurf „Datensicherheit“, Pflichten) | Text und Datenflüsse fertig und mit dem Code abgeglichen; Angaben des Verantwortlichen am 24.11.2026 eingetragen | Bedingungen der Anbieter annehmen, fachkundige Durchsicht (Eigentümer) |
| 2 | Impressum, Anbieterangaben | `www/impressum.html` | fertig: Name, Anschrift und E-Mail am 24.11.2026 eingetragen, keine Platzhalter mehr | fachkundige Durchsicht empfohlen; die Anschrift steht damit öffentlich im Netz (Eigentümer) |
| 3 | Asset- und Lizenzverzeichnis | `docs/ASSETS_LIZENZEN.md`, `docs/HERKUNFT_BILDER.md`, `docs/herkunft/`, `scripts/asset_manifest.py`, `www/licenses.html`, `www/ofl/` | fertig: Bestand aller Bilder, Schriften (OFL, Texte liegen bei), Software; Herkunft der Bilder erklärt (Eigentümer, 24.11.2026), Verzeichnis mit 113 Einträgen und Prüfsummen im Repo, Manifest aller ausgelieferten Dateien | Tarif, Modellversion und Prompt je Bild fehlen (keine lückenlose Kette); Rechte an Referenzmaterial und Ähnlichkeit zu bekannten Figuren prüfen; fachkundige Einordnung der OpenAI-Bedingungen empfohlen (Eigentümer) |
| 4 | Markenprüfung | `docs/RECHT_UND_NAMEN.md` | Register DPMAregister und TMview am 24.11.2026 durchsucht: kein identisches und kein eng ähnliches Zeichen, Restrisiko gering bis mäßig; **Name „Noa's Bean Trail“ vom Eigentümer am 24.11.2026 freigegeben** | optional WIPO-Abfrage und eigene Wortmarke (Eigentümer) |
| 5 | Altersfreigabe, Jugendschutz | `docs/ALTERSFREIGABE.md` | Entwurf: Zielgruppe 16+, erwartet USK 0 / PEGI 3, Jugendschutz im Spiel beschrieben | Zielgruppe bestätigen, IARC-Fragebogen in der Play Console ausfüllen (Eigentümer; Weg und vorbereitete Antworten: `docs/ALTERSFREIGABE.md`, Abschnitt 3) |
| 6 | Store-Texte und Screenshots | `docs/STORE_LISTING.md`, `store/`, `scripts/store_shots.py`, `scripts/store_promo.py`, `tests/test_store.py` | fertig in Deutsch und Englisch: Texte, Alt-Texte, 6 Screenshots je Sprache, 2 Feature-Grafiken, Regelcheck; Test 91/91 | Aussehen auf dem Gerät gegenprüfen |
| 7 | Technische Dokumentation | `docs/TECHNIK.md` | fertig: Aufbau, Build, Signierung, Dienste, Berechtigungen, Risiken, Prüfliste für den ersten echten Build | Prüfliste (Abschnitt 9 dort) abarbeiten, sobald gebaut ist |
| 8 | Test- und Qualitätsbericht | `docs/QUALITAET.md`, `tests/` | fertig für 1.5.13: alle automatischen Tests grün, Leistungswerte, bekannte Mängel, Freigabekriterien | Gerätetest (Abschnitt 8 dort) |
| 9 | Monetarisierungsdokumentation | `docs/MONETARISIERUNG.md` | fertig: Währungen, Käufe, Werbung, Zufallsbelohnungen, Regeln und Stand ihrer Einhaltung | Konten und Schlüssel (Abschnitt 3 unten); Entscheidung zum Euro-Wert (Abschnitt 4) |

## 2. Werbung und Bezahlfunktion (Stand im Code)

- **Werbung:** nur freiwillige Videos mit Belohnung (Google AdMob), kein Banner, kein Zwangsvideo. Einwilligung zuerst (Google-Einwilligungsfenster), Tageslimits im Code (`AD_CAP`), Inhaltsstufe „ParentalGuidance“.
- **Käufe:** Diamanten-Pakete und ein einmaliges Startpaket über Google Play, abgewickelt mit RevenueCat; angezeigt wird der Preis aus dem Store. Dazu „Noa's Pro“ als Abo (monatlich, jährlich) oder einmalig (Lifetime): Belohnungen ohne Video und täglich Diamanten.
- **Sperre (`CONFIG.legalReady`):** Enthält `www/impressum.html` oder `www/privacy.html` einen Platzhalter, bleiben Werbung, Käufe und Messung in der App aus. Seit 24.11.2026 steht in beiden Seiten kein Platzhalter mehr; der Build schaltet die Funktionen damit frei. Echte Werbung und echte Käufe laufen trotzdem erst mit Konten und Schlüsseln (GitHub-Secrets). Die Web-Version hat nie Käufe und nur Demo-Werbung.
- **Test-APK:** zeigt nur Googles Testanzeigen (Version 1.5.11).
- **Nicht geprüft:** echte Anzeigen, echte Käufe, echtes Einwilligungsfenster und AppsFlyer mit echten Konten. Die Plugins sind im Test nachgebaut (`docs/QUALITAET.md`, Abschnitt 2). Das lässt sich erst mit Konten und Gerät klären.
- Der Agent legt keine Konten an, gibt kein Geld aus und reicht nichts ein (`CLAUDE.md`).

## 3. Reihenfolge bis zum Store-Start (Empfehlung)

1. **Angaben für Impressum und Datenschutz** (Name, ladungsfähige Anschrift, E-Mail): erledigt am 24.11.2026, eingetragen, keine Platzhalter mehr.
2. **Namen freigeben** (`docs/RECHT_UND_NAMEN.md`, Abschnitt 5.3): erledigt am 24.11.2026 für „Noa's Bean Trail“. Bei einem anderen Namen gilt wieder: ohne Freigabe kein Store-Upload und keine Werbetexte (auch nicht für Almedia).
3. **Push freigeben:** erteilt am 24.11.2026. Die Pipeline baut die Test-APK; die signierte Store-Datei und der Upload (nur nach `internal`) laufen erst, wenn die Secrets für Signierung und Play gesetzt sind.
4. **Test-APK auf einem Gerät prüfen:** `docs/TECHNIK.md`, Abschnitt 9, und `docs/QUALITAET.md`, Abschnitt 8.
5. **Konten und Schlüssel** (nur der Eigentümer): Play Console (Produkte `gems_small`, `gems_large`, `starter_pack`; für Pro ein Abo mit Basis-Tarifen monatlich und jährlich sowie ein einmaliges Produkt Lifetime), AdMob (App, Belohnungs-Anzeigenblock, Einwilligungsnachricht), RevenueCat, AppsFlyer, Signierschlüssel und Dienstkonto als GitHub-Secrets (`README.md`, `docs/MONETARISIERUNG.md`, Abschnitt 10).
6. **Play Console ausfüllen:** Store-Eintrag (`docs/STORE_LISTING.md`), Zielgruppe und Inhaltseinstufung (`docs/ALTERSFREIGABE.md`), Datensicherheit (`docs/PRIVACY.md`, Abschnitt 3), Datenschutz-URL.
7. **Interner Test** mit Lizenztestern: Testkäufe und Anzeigen mit Testgeräten.
8. **Produktion** löst nur der Eigentümer aus; der Agent veröffentlicht nie auf `production`.

## 4. Entscheidungen beim Eigentümer (mit Empfehlung des Agenten)

| Entscheidung | Empfehlung |
|---|---|
| Name „Noa's Bean Trail“ freigeben | **Erledigt am 24.11.2026.** Offen und empfohlen: eine eigene Wortmarke anmelden und vor größerem Werbebudget kurz fachkundig beraten lassen. |
| Zielgruppe | 16–17 und 18+ (keine Kinder-Altersgruppen). Gründe und Plan B: `docs/ALTERSFREIGABE.md`. |
| Paket-ID | **Entschieden am 24.11.2026:** `io.github.johnqpowers.beantrail` (vorher `io.github.johnqpowers.mergecafe`). Umgestellt in `capacitor.config.json`, `.github/workflows/android.yml`, `.github/workflows/kpi.yml`, `CLAUDE.md`, `README.md`. In Play, AdMob, RevenueCat und AppsFlyer die neue ID verwenden; der Spielstand-Schlüssel bleibt. Folge: Android behandelt die neue App als eigene App; eine mit der alten ID installierte Test-APK bleibt daneben bestehen, ihr Spielstand wird nicht übernommen. Nach dem ersten Upload in Google Play ist die ID endgültig. |
| Euro-Wert bei Diamanten-Preisen (EU-Leitsatz 1, nicht bindend) | Anzeigen, z. B. „15 Diamanten ≈ 0,19 bis 0,25 €“, berechnet aus den Store-Preisen (`docs/MONETARISIERUNG.md`, Abschnitt 7). Kleine Code-Änderung, senkt den Umsatz kaum. Wartet auf den Auftrag. |
| Standardsprache der Store-Seite | Deutsch, Englisch als Übersetzung (so vorbereitet). |
| Seite „Käufe“ mit Hinweis zu virtueller Währung und Widerruf | Textvorschlag steht in `docs/MONETARISIERUNG.md`; vor dem Einbau fachkundig prüfen lassen. |

## 5. Bekannte Lücken, die kein Dokument schließt

- Echte Geräte und echte Konten fehlen noch. Der CI-Build der Versionen ab 1.5.8 ist mit dem Push vom 24.11.2026 erstmals durchgelaufen (Build 13, Test-APK); auf einem Gerät ist er noch nicht gelaufen (Ergebnis: Wochenbericht und `docs/QUALITAET.md`, Abschnitt 6).
- Böden der Welten 4 bis 9 und viele Einzugs-Posen fehlen als Bilder; das Spiel zeigt dort gebaute Ersatzgrafik (`CLAUDE.md`, Abschnitt Bilder).
- Das Verdopplungs-Angebot nach einer Lieferung steht 7 Sekunden über der unteren Leiste; im Gerätetest beobachten, ob es versehentlich angetippt wird (`docs/MONETARISIERUNG.md`, Punkt M2).
- Herkunft der KI-erzeugten Bilder (Icon, Figuren, Katze, Teile) ist erklärt und im Verzeichnis erfasst, aber nicht lückenlos belegt: kein Prompt je Bild, kein Tarif, keine Modellversion; Rechte an Referenzmaterial sind nicht geprüft (`docs/HERKUNFT_BILDER.md`).

## 6. Prüfen und Pflegen

- Alle automatischen Tests: `tests/README.md`. Store-Unterlagen: `python3 -I tests/test_store.py`.
- Nach jeder sichtbaren Änderung an Oberfläche oder Grafik: Store-Bilder neu erzeugen (`docs/STORE_LISTING.md`, Abschnitt 5) und Versionsangaben in den Unterlagen nachziehen.
- Neue Funktionen, die Daten sammeln, Zufall oder Geld betreffen: zuerst `docs/PRIVACY.md`, `docs/MONETARISIERUNG.md` und `docs/ALTERSFREIGABE.md` anpassen, dann bauen.
