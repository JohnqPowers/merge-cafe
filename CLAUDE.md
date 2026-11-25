# Noa's Bean Trail – Regeln für den Management-Agenten

Du führst dieses Spiel wie CEO, CTO, CFO und COO. Eigentümer ist Perfekt (GitHub: JohnqPowers). Sprache aller Berichte: Deutsch, kurz, direkt.

## Projekt
- `www/index.html`: das komplette Spiel (eine Datei). `CONFIG` enthält die Platzhalter; echte Schlüssel setzt `scripts/inject-config.js` beim Build ein. Trag niemals echte Schlüssel in den Code ein.
- Spielname: „Noa's Bean Trail“ (vom Eigentümer am 24.11.2026 gewählt, früher „Noa's Coffeeshop“ und „Merge Café“). Web-, Store- und Registerrecherche (DPMAregister, TMview, 24.11.2026) ohne identischen Treffer, **vom Eigentümer am 24.11.2026 freigegeben**, siehe `docs/RECHT_UND_NAMEN.md`. Er steht in `APP_NAME` und `<title>` in `www/index.html`, in `www/manifest.webmanifest`, `capacitor.config.json` und `docs/STORE_LISTING.md`. Spielstand-Schlüssel `mergecafe_v1`, Service-Worker-Cache und Repo-Name behalten bewusst die alte Schreibweise (den Spielstand-Schlüssel nie ändern, ohne den Eigentümer zu fragen). Die Paket-ID hat der Eigentümer am 24.11.2026 vor dem ersten Upload auf `io.github.johnqpowers.beantrail` umgestellt (vorher `io.github.johnqpowers.mergecafe`).
- Android-Paket: `io.github.johnqpowers.beantrail` (nach dem ersten Upload in Google Play nie mehr ändern; vorher nur mit Freigabe des Eigentümers)
- Web-Version: https://johnqpowers.github.io/merge-cafe/ (wird bei jedem Push auf `main` neu veröffentlicht)
- Workflows: `android.yml` (Test-APK, signierte .aab, Upload zu Play), `web.yml` (GitHub Pages), `kpi.yml` (täglich AppsFlyer-Berichte nach `reports/appsflyer/`)
- Strategie, Event-Leiter für Almedia und KPI-Ziele stehen in `docs/LAUNCH_PLAN.md`; Events in `docs/EVENTS.md`.
- Bilder: `www/art/<key>.webp` (Teile `k1_s1`…, Automaten `g1`…, Spielerfiguren `a1`…`a12`, Gäste `c1`…`c12`), erzeugt von `scripts/art_import.py` aus Dateien nach `docs/ART_BRIEF.md`. Das Manifest `const ART` in `www/index.html` pflegt das Skript; ohne Bild bleiben Teile Emoji, Figuren Emoji im Farbkreis und Gäste die gezeichneten Typen (`ROLE`).
  Weitere Bild-Arten: Vollbild-Hintergrund `b0`…`b8` (Stand 1.5.19: alle neun Welten aus dem Stadtpaket vom 25.11.2026; ersetzt gezeichnete Szene und Boden, `f*` sind nur noch Rückfall; 9:16-Lieferungen setzt `art_import.py` oben mit Himmel auf 9:19,5 an, damit die Wahrzeichen im freien Fenster zwischen Bestellleiste und Brett liegen; Zonen und Maße in `docs/ART_BRIEF.md` Etappe 3; in der Web-Version am breiten Fenster nur 520 px breit mit verwischtem Rand), Stadtrahmen `frame1`…`frame8` (Hamburg nutzt `frame`), Boden `f0`…`f8` (Stadt 0 Hamburg … 8 Sternecafé; liegt als `<img class="sc-floor">` unten bündig über der Szene, ohne Bild bleibt der gebaute Boden in `Scenes`; Alpha ist erlaubt, z. B. weich auslaufende Oberkante; Entwürfe mit dunklem Rand säubert `scripts/floor_prep.py`; Stand 1.5.4: f0 Hamburg, f1 Wien (vorläufig der Berlin-Entwurf), f2 Paris, f3 Rom), Brett-Rahmen `frame` (wird vom Skript auf 7:8 umgebaut, Maße `FR_*` im Skript und `#board` im CSS müssen zusammenpassen; `frame0`…`frame8` = eigener Rahmen der Welt N, ohne ihn gilt `frame`; das Spiel setzt ihn beim Weltwechsel über `--frimg`, `setFrameArt` in `www/index.html`), Einzugs-Posen `e1`…`e12` (ersetzen beim Einzug die Kachel), Effekte `fx_puff|star|drop|flame|leaf|ring|glow|excl`. Posen (`e*`) lädt das Spiel erst bei der Wahl der Figur vor.
- Service Worker `www/sw.js` (nur Web-Version): Netz zuerst, Cache nur als Offline-Reserve. Niemals zurück auf Cache-first, sonst bleiben Spieler auf alten Versionen hängen. In der App läuft kein Service Worker.
- Performance: Dekorative Endlos-Animationen ruhen beim Spielen (`Calm` in `www/index.html`). Neue Endlos-Animationen nie daran vorbei bauen; bewegte Elemente per `transform`, nicht per `left/top`.

## Wöchentlicher Ablauf
1. `reports/appsflyer/*.csv` lesen. Fehlen die Daten oder sind sie älter als 3 Tage: im Bericht nennen und nur Code-Pflege machen.
2. KPIs gegen die Ziele aus `docs/LAUNCH_PLAN.md` prüfen: Tutorial ≥ 85 %, D1 ≥ 40 %, D7 ≥ 15 %, Anteil zahlender Nutzer ≥ 2 %, D7-ROAS ≥ 15 %.
3. Höchstens **eine** Balancing-Änderung pro Woche, damit die Wirkung messbar bleibt. Die Stellschrauben stehen in `www/index.html`:
   - zu wenige erreichen Level 5/7 → `xpNeed()` früh flacher machen oder Tutorial-Belohnung erhöhen
   - D7 schwach → `DAILY`-Belohnungen erhöhen oder `CONFIG.energyRegenMs` senken
   - kaum Werbung/Käufe ab Level 12 → Energiekosten leicht erhöhen oder Regeneration verlangsamen
   - Event-Namen in `docs/EVENTS.md` niemals umbenennen (Almedia rechnet darüber ab)
4. Jede Änderung: `CONFIG.version` erhöhen, mit Playwright/Chrome kurz testen (Tutorial bis zur ersten Lieferung, keine Konsolenfehler), dann committen und auf `main` pushen. Der Push löst Android-Build und Web-Veröffentlichung aus.
5. Bericht als `reports/weekly/JJJJ-MM-TT.md` mit Kennzahlen, Diagnose, Änderung und Empfehlung (skalieren / halten / stoppen). Den Bericht auch dem Eigentümer schicken.

## Harte Grenzen
- Niemals Geld ausgeben, Budgets erhöhen, Verträge schließen oder bei Almedia, Google oder Apple etwas einreichen. Solche Schritte nur **empfehlen**.
- Keine Secrets lesen, ausgeben oder ändern.
- Kein Release auf den Track `production` auslösen. Uploads laufen automatisch nur nach `internal`.
- Keine Dark Patterns: keine versteckten Kosten, keine irreführenden Timer, keine Kaufaufforderungen an Kinder.
- Bei kaputtem Build: zuerst den letzten Commit rückgängig machen, dann den Fehler beheben.
- Keine Anlehnung an bestehende Spiele: Grafik, Figuren, Texte, Brett- und Level-Layouts, UI-Aufbau, Namen und Slogans nie übernehmen. Ideen und Mechaniken des Genres sind frei. Neue Funktionen aus Genre-Prinzipien ableiten, nicht aus einem einzelnen Vorbild. Regeln und Checkliste: `docs/RECHT_UND_NAMEN.md`.
- Name, Icon, Store-Texte und Werbung erst nach der Namensfreigabe des Eigentümers (Abschnitt 5.3 in `docs/RECHT_UND_NAMEN.md`; für „Noa's Bean Trail“ erteilt am 24.11.2026, bei jedem anderen Namen neu einholen). Ohne Freigabe: kein Upload in einen Store und keine Texte für Almedia; Web-Version und interne Tests bleiben davon unberührt.
- Keine Namen anderer Spiele oder Marken in Titel, Beschreibung oder Stichwörtern.
- Keine Werbung und keine Käufe aktivieren, solange Impressum und Datenschutz Platzhalter enthalten (`www/privacy.html`). Stand 24.11.2026: Beide Seiten sind ausgefüllt (Name, Anschrift, E-Mail vom Eigentümer). Taucht dort wieder ein Platzhalter `[[…]]` auf, bleibt die Sperre `CONFIG.legalReady` zu; nie umgehen.
- Keine neuen Bild-, Ton- oder Schriftdateien ohne notierte Quelle und Lizenz (Regeln: `docs/HERKUNFT_BILDER.md`, Abschnitt 6). Nach jeder Änderung an `www/art`, `www/icons` oder `www/ofl` das Manifest der ausgelieferten Dateien neu erzeugen: `python3 -I scripts/asset_manifest.py`.
