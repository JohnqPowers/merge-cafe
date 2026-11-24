# Unterlagen vor dem Store-Start – Übersicht

Stand: 24.11.2026, Spielversion 1.5.12 (lokal committet, **nichts gepusht, nichts bei Google, Apple oder Almedia eingereicht**). Diese Seite zeigt auf einen Blick die neun Unterlagen, die der Eigentümer am 24.11.2026 vor dem Verkauf verlangt hat, dazu Werbung und Bezahlfunktion. Keine Rechtsberatung: Datenschutz, Impressum und Altersfreigabe sind sorgfältige Entwürfe und sollten vor dem Start einmal fachkundig durchgesehen werden.

## 1. Die neun Unterlagen

| Nr. | Unterlage | Dateien | Stand | Was noch fehlt (wer) |
|---|---|---|---|---|
| 1 | Datenschutzerklärung | `www/privacy.html` (Seite für Spieler), `docs/PRIVACY.md` (Datenflüsse, Entwurf „Datensicherheit“, Pflichten) | Text und Datenflüsse fertig und mit dem Code abgeglichen | Angaben des Verantwortlichen (Platzhalter), Bedingungen der Anbieter annehmen, fachkundige Durchsicht (Eigentümer) |
| 2 | Impressum, Anbieterangaben | `www/impressum.html` | Text fertig | Name, ladungsfähige Anschrift, E-Mail-Adresse (Eigentümer) |
| 3 | Asset- und Lizenzverzeichnis | `docs/ASSETS_LIZENZEN.md`, `www/licenses.html`, `www/ofl/` | fertig: Bestand aller Bilder, Schriften (OFL, Texte liegen bei), Software | Herkunft der Bilder belegen: Werkzeug, dessen Bedingungen für kommerzielle Nutzung, Prompts und Originaldateien ablegen (Eigentümer) |
| 4 | Markenprüfung | `docs/RECHT_UND_NAMEN.md` | Register DPMAregister und TMview am 24.11.2026 durchsucht: kein identisches und kein eng ähnliches Zeichen, Restrisiko gering bis mäßig | **Namensfreigabe** (Abschnitt 5.3 dort); optional WIPO-Abfrage und eigene Wortmarke (Eigentümer) |
| 5 | Altersfreigabe, Jugendschutz | `docs/ALTERSFREIGABE.md` | Entwurf: Zielgruppe 16+, erwartet USK 0 / PEGI 3, Jugendschutz im Spiel beschrieben | Zielgruppe bestätigen, IARC-Fragebogen in der Play Console ausfüllen (Eigentümer) |
| 6 | Store-Texte und Screenshots | `docs/STORE_LISTING.md`, `store/`, `scripts/store_shots.py`, `scripts/store_promo.py`, `tests/test_store.py` | fertig in Deutsch und Englisch: Texte, Alt-Texte, 6 Screenshots je Sprache, 2 Feature-Grafiken, Regelcheck; Test 91/91 | Namensfreigabe; Aussehen auf dem Gerät gegenprüfen |
| 7 | Technische Dokumentation | `docs/TECHNIK.md` | fertig: Aufbau, Build, Signierung, Dienste, Berechtigungen, Risiken, Prüfliste für den ersten echten Build | Prüfliste (Abschnitt 9 dort) abarbeiten, sobald gebaut ist |
| 8 | Test- und Qualitätsbericht | `docs/QUALITAET.md`, `tests/` | fertig für 1.5.12: alle automatischen Tests grün, Leistungswerte, bekannte Mängel, Freigabekriterien | Gerätetest (Abschnitt 8 dort) |
| 9 | Monetarisierungsdokumentation | `docs/MONETARISIERUNG.md` | fertig: Währungen, Käufe, Werbung, Zufallsbelohnungen, Regeln und Stand ihrer Einhaltung | Konten und Schlüssel (Abschnitt 3 unten); Entscheidung zum Euro-Wert (Abschnitt 4) |

## 2. Werbung und Bezahlfunktion (Stand im Code)

- **Werbung:** nur freiwillige Videos mit Belohnung (Google AdMob), kein Banner, kein Zwangsvideo. Einwilligung zuerst (Google-Einwilligungsfenster), Tageslimits im Code (`AD_CAP`), Inhaltsstufe „ParentalGuidance“.
- **Käufe:** Diamanten-Pakete und ein einmaliges Startpaket über Google Play, abgewickelt mit RevenueCat; angezeigt wird der Preis aus dem Store.
- **Sperre:** Solange `www/impressum.html` oder `www/privacy.html` Platzhalter enthalten, bleiben Werbung, Käufe und Messung in der App aus. Die Web-Version hat nie Käufe und nur Demo-Werbung.
- **Test-APK:** zeigt nur Googles Testanzeigen (Version 1.5.11).
- **Nicht geprüft:** echte Anzeigen, echte Käufe, echtes Einwilligungsfenster und AppsFlyer mit echten Konten. Die Plugins sind im Test nachgebaut (`docs/QUALITAET.md`, Abschnitt 2). Das lässt sich erst mit Konten und Gerät klären.
- Der Agent legt keine Konten an, gibt kein Geld aus und reicht nichts ein (`CLAUDE.md`).

## 3. Reihenfolge bis zum Store-Start (Empfehlung)

1. **Angaben für Impressum und Datenschutz** liefern (Name, ladungsfähige Anschrift, E-Mail). Der Agent trägt sie ein; der Test prüft, dass keine Platzhalter bleiben.
2. **Namen freigeben** (`docs/RECHT_UND_NAMEN.md`, Abschnitt 5.3) oder einen anderen wählen. Ohne Freigabe kein Store-Upload und keine Werbetexte (auch nicht für Almedia).
3. **Push freigeben.** Dann baut die Pipeline die Test-APK und die signierte Store-Datei (Upload nur nach `internal`).
4. **Test-APK auf einem Gerät prüfen:** `docs/TECHNIK.md`, Abschnitt 9, und `docs/QUALITAET.md`, Abschnitt 8.
5. **Konten und Schlüssel** (nur der Eigentümer): Play Console (Produkte `gems_small`, `gems_large`, `starter_pack`), AdMob (App, Belohnungs-Anzeigenblock, Einwilligungsnachricht), RevenueCat, AppsFlyer, Signierschlüssel und Dienstkonto als GitHub-Secrets (`README.md`, `docs/MONETARISIERUNG.md`, Abschnitt 10).
6. **Play Console ausfüllen:** Store-Eintrag (`docs/STORE_LISTING.md`), Zielgruppe und Inhaltseinstufung (`docs/ALTERSFREIGABE.md`), Datensicherheit (`docs/PRIVACY.md`, Abschnitt 3), Datenschutz-URL.
7. **Interner Test** mit Lizenztestern: Testkäufe und Anzeigen mit Testgeräten.
8. **Produktion** löst nur der Eigentümer aus; der Agent veröffentlicht nie auf `production`.

## 4. Entscheidungen beim Eigentümer (mit Empfehlung des Agenten)

| Entscheidung | Empfehlung |
|---|---|
| Name „Noa's Bean Trail“ freigeben | Ja, sofern kein Gegenhinweis: Web, Stores und Register ohne Treffer. Zusätzlich eine eigene Wortmarke anmelden und vor größerem Werbebudget kurz fachkundig beraten lassen. |
| Zielgruppe | 16–17 und 18+ (keine Kinder-Altersgruppen). Gründe und Plan B: `docs/ALTERSFREIGABE.md`. |
| Paket-ID | Vor dem ersten Upload entscheiden, danach nicht mehr änderbar. Heute `io.github.johnqpowers.mergecafe` (trägt den alten Namen). Empfehlung: `io.github.johnqpowers.beantrail`. Änderung betrifft `capacitor.config.json`, `.github/workflows/android.yml`, `.github/workflows/kpi.yml`, `CLAUDE.md`, `README.md` und die Zuordnung in Play, AdMob, RevenueCat und AppsFlyer; der Spielstand-Schlüssel bleibt. Der Agent ändert die ID nicht ohne Auftrag (`CLAUDE.md`). |
| Euro-Wert bei Diamanten-Preisen (EU-Leitsatz 1, nicht bindend) | Anzeigen, z. B. „15 Diamanten ≈ 0,19 bis 0,25 €“, berechnet aus den Store-Preisen (`docs/MONETARISIERUNG.md`, Abschnitt 7). Kleine Code-Änderung, senkt den Umsatz kaum. Wartet auf den Auftrag. |
| Standardsprache der Store-Seite | Deutsch, Englisch als Übersetzung (so vorbereitet). |
| Seite „Käufe“ mit Hinweis zu virtueller Währung und Widerruf | Textvorschlag steht in `docs/MONETARISIERUNG.md`; vor dem Einbau fachkundig prüfen lassen. |

## 5. Bekannte Lücken, die kein Dokument schließt

- Echte Geräte, echte Konten und der CI-Build der Versionen ab 1.5.8 sind noch nicht gelaufen (`docs/QUALITAET.md`, Abschnitt 6).
- Böden der Welten 4 bis 9 und viele Einzugs-Posen fehlen als Bilder; das Spiel zeigt dort gebaute Ersatzgrafik (`CLAUDE.md`, Abschnitt Bilder).
- Das Verdopplungs-Angebot nach einer Lieferung steht 7 Sekunden über der unteren Leiste; im Gerätetest beobachten, ob es versehentlich angetippt wird (`docs/MONETARISIERUNG.md`, Punkt M2).
- Herkunft und Rechte der KI-erzeugten Bilder (Icon, Figuren, Katze, Teile) sind nicht belegt (`docs/ASSETS_LIZENZEN.md`, Abschnitt 3).

## 6. Prüfen und Pflegen

- Alle automatischen Tests: `tests/README.md`. Store-Unterlagen: `python3 -I tests/test_store.py`.
- Nach jeder sichtbaren Änderung an Oberfläche oder Grafik: Store-Bilder neu erzeugen (`docs/STORE_LISTING.md`, Abschnitt 5) und Versionsangaben in den Unterlagen nachziehen.
- Neue Funktionen, die Daten sammeln, Zufall oder Geld betreffen: zuerst `docs/PRIVACY.md`, `docs/MONETARISIERUNG.md` und `docs/ALTERSFREIGABE.md` anpassen, dann bauen.
