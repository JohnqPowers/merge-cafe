# Store-Eintrag – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.12. Entwurf für die Google Play Console. Keine Rechtsberatung.

> **Nicht hochladen, solange offen ist:** (1) die Namensfreigabe des Eigentümers (`docs/RECHT_UND_NAMEN.md`, Abschnitt 5.3), (2) die Platzhalter in `www/privacy.html` und `www/impressum.html`. Texte und Bilder sind vorbereitet, es wurde nichts eingereicht und kein Text für Almedia oder andere Werbekanäle erstellt.

Prüfung per Skript: `python3 -I tests/test_store.py` (Zeichenlängen, Bildformate, Alt-Texte, Zahlen im Text gegen den Code, Fremdnamen-Liste).

## 1. Angaben für die Play Console

| Feld | Eintrag | Stand |
|---|---|---|
| App-Name | Deutsch: „Noa's Bean Trail: Merge-Spiel“ (29 Zeichen). Englisch: „Noa's Bean Trail: Merge Puzzle“ (30 Zeichen, Grenze). | Text steht unten |
| Standardsprache | Deutsch; Englisch als zweite Übersetzung | Entscheidung des Agenten |
| Kurzbeschreibung, Beschreibung | Abschnitte 2 und 3 | fertig |
| Was ist neu (erste Version) | Abschnitt 4 | fertig |
| Kategorie | Spiele → Puzzle | Entscheidung des Agenten |
| Tags | In der Console aus der vorgegebenen Liste wählen (passend: Merge, Casual, Puzzle, Kochen, falls vorhanden). Die Liste ändert sich; hier steht keine feste Auswahl. | beim Ausfüllen |
| Preis | kostenlos, mit In-App-Käufen und Werbung („Enthält Werbung“ und „In-App-Käufe“ ankreuzen) | siehe `docs/MONETARISIERUNG.md` |
| Kontakt | E-Mail-Adresse (Pflicht, öffentlich sichtbar), Website optional | **Eigentümer**, gleiche Adresse wie im Impressum |
| Datenschutzerklärung (URL) | `https://johnqpowers.github.io/merge-cafe/privacy.html` | erst nach Ersetzen der Platzhalter |
| Zielgruppe und Inhalt | 16–17 und 18+ (keine Kinder-Altersgruppen) | Empfehlung, siehe `docs/ALTERSFREIGABE.md` |
| Inhaltseinstufung (IARC) | Fragebogen ausfüllen, erwartet USK 0 / PEGI 3 | siehe `docs/ALTERSFREIGABE.md` |
| Datensicherheit | Entwurf der Antworten | siehe `docs/PRIVACY.md` |
| App-Zugriff | Alle Funktionen ohne Anmeldung nutzbar | stimmt (kein Konto im Spiel) |
| Grafiken | Icon, Feature-Grafik, 6 Screenshots je Sprache | Abschnitt 5 |

## 2. Texte Deutsch

**App-Name (max. 30):** Noa's Bean Trail: Merge-Spiel

**Kurzbeschreibung (max. 80):** Verschmelze Kaffee, Gebäck und Frühstück, bediene Gäste und reise um die Welt!

**Beschreibung (max. 4000):**

```text
Willkommen im gemütlichsten Café der Welt! ☕🥐

Tippe auf Teekanne, Brotkorb und Hühnerstall, um Zutaten zu erzeugen. Ziehe zwei gleiche Teile zusammen: Aus der Kaffeebohne wird Espresso, daraus Matcha und Bubble Tea – und aus Weizen am Ende eine Festtorte.

Deine Gäste warten schon mit ihren Bestellungen. Liefere sie aus, verdiene Münzen und steige Level für Level auf. Mit jedem Kapitel zieht dein Café in eine neue Stadt: von Hamburg über Paris und Kyoto bis ins Sternecafé über den Wolken.

★ Einfach zu lernen: ziehen, verschmelzen, liefern
★ 22 Leckereien in 3 Ketten: Kaffee, Backwaren und Frühstück
★ 9 Welten von Hamburg bis ins Sternecafé
★ Dein Café, deine Figur: 12 Figuren zur Auswahl und ein eigener Café-Name
★ Café-Katze Mocha: antippen und streicheln, dann schnurrt sie
★ Täglicher Bonus mit 7-Tage-Serie und kostenlose Geschenke
★ Bestellungen laufen nie ab
★ Kein Konto nötig, dein Spielstand bleibt auf deinem Gerät
★ Auf Deutsch und Englisch

Gut zu wissen
• Kostenlos spielbar. Optional gibt es In-App-Käufe (Diamanten) und freiwillige Werbevideos, für die du eine Belohnung bekommst. Keine Banner, keine Pflicht-Werbung.
• Zutaten erzeugen kostet Energie. Sie füllt sich mit der Zeit von selbst auf; du kannst sie auch mit Diamanten oder einem Werbevideo auffüllen.
• Geschenke enthalten zufällige Belohnungen (Münzen, Energie oder Diamanten). Sie sind gratis; die Chancen siehst du im Spiel im Diamanten-Fenster.
• Wo es vorgeschrieben ist, fragt das Spiel vor Werbung und Messung nach deiner Einwilligung. Du kannst sie jederzeit in den Optionen ändern.
• Für Spieler ab 16 Jahren.

Lade Noa's Bean Trail herunter und mach dein Café zur Legende!
```

## 3. Texte Englisch

**App name (max 30):** Noa's Bean Trail: Merge Puzzle

**Short description (max 80):** Merge coffee, pastries and breakfast, serve guests and travel the world!

**Description (max 4000):**

```text
Welcome to the coziest café in the world! ☕🥐

Tap the teapot, the bread basket and the hen house to make ingredients. Drag two matching items together: a coffee bean becomes espresso, then matcha and bubble tea – and wheat ends up as a party cake.

Your guests are already waiting with their orders. Serve them, earn coins and level up. With every chapter your café moves to a new city: from Hamburg through Paris and Kyoto all the way to the Star Café above the clouds.

★ Easy to learn: drag, merge, serve
★ 22 treats in 3 merge chains: coffee, bakery and breakfast
★ 9 worlds from Hamburg to the Star Café
★ Your café, your character: 12 characters to choose from and a café name of your own
★ Café cat Mocha: tap her and pet her, and she purrs
★ Daily bonus with a 7-day streak and free gifts
★ Orders never expire
★ No account needed, your progress stays on your device
★ In English and German

Good to know
• Free to play. Optional in-app purchases (gems) and voluntary reward videos are available. No banners, no forced ads.
• Making ingredients costs energy. It refills over time on its own; you can also refill it with gems or by watching a reward video.
• Gifts contain random rewards (coins, energy or gems). They are free; you can see the odds in the game, in the gems window.
• Where required, the game asks for your consent before ads and measurement. You can change it any time in the options.
• For players aged 16 and over.

Download Noa's Bean Trail and turn your café into a legend!
```

## 4. Was ist neu (erste Version, max. 500 Zeichen)

**Deutsch:** Erste Version: Verschmelze Kaffee, Gebäck und Frühstück, bediene deine Gäste und reise von Hamburg bis ins Sternecafé.

**English:** First release: merge coffee, pastries and breakfast, serve your guests and travel from Hamburg to the Star Café.

## 5. Grafiken

Alle Bilder entstehen reproduzierbar aus dem Spiel selbst (Stand 1.5.12). Nach jeder sichtbaren Änderung an Oberfläche oder Grafik neu erzeugen und ansehen:

```
python3 -I scripts/store_shots.py        # 6 Screenshots je Sprache
python3 -I scripts/store_promo.py        # Feature-Grafik de und en
python3 -I tests/test_store.py            # Formate und Texte prüfen
```

| Datei | Format | Inhalt |
|---|---|---|
| `store/app-icon-512.png` | 512×512, 32-Bit-PNG mit Alpha, unter 1024 KB | Icon des Eigentümers („Noa's Bean Trail“, Köchin mit Katze), gebaut mit `python3 -I assets/src/build-icon.py` aus `assets/src/app-icon-original.png`. Gleiche Datei wie `www/icons/icon-512.png`. |
| `store/feature-graphic-de-1024x500.png`, `…-en-…` | 1024×500, 24-Bit-PNG ohne Alpha | Icon, Titel, Postkarten von Hamburg, Paris und Kyoto (aus `Scenes`), Gebäck-Bilder aus `www/art`. Text: nur Titel und „Verschmelzen · Backen · Reisen“ / „Merge · Bake · Travel“. |
| `store/screenshot-<1–6>-de.png`, `…-en.png` | 1080×1920 (9:16), 24-Bit-PNG ohne Alpha, je rund 1 bis 2 MB | 1 Hamburg (Start), 2 Paris (volles Brett, drei lieferbare Aufträge), 3 Weltreise (Postkarten), 4 Kyoto (hohe Stufen), 5 Begrüßung mit Figurenwahl, 6 Tagesbonus mit „Abholen“. |

**Alt-Texte** (Play verlangt für jedes Bild einen Alt-Text mit höchstens 140 Zeichen):

| Bild | Deutsch | Englisch |
|---|---|---|
| Feature-Grafik | Noa's Bean Trail: Icon mit Köchin und Katze, Gebäck und Postkarten aus Hamburg, Paris und Kyoto | Noa's Bean Trail: icon with a chef and her cat, pastries and postcards from Hamburg, Paris and Kyoto |
| Screenshot 1 | Spielbrett in Hamburg: gleiche Kaffee-, Back- und Frühstücksteile verschmelzen, oben warten drei Gäste mit Bestellungen | Game board in Hamburg: merge matching coffee, bakery and breakfast items while three guests wait with orders above |
| Screenshot 2 | Spielbrett in Paris mit vielen Teilen und drei Bestellungen, die sich sofort liefern lassen | Game board in Paris with many items and three orders that can be served right away |
| Screenshot 3 | Weltreise: Postkarten von Hamburg, Wien und Paris, weitere Städte werden mit höheren Leveln frei | World trip: postcards of Hamburg, Vienna and Paris, more cities unlock with higher levels |
| Screenshot 4 | Spielbrett in Kyoto auf Level 26 mit Teilen hoher Stufen und neuen Bestellungen | Game board in Kyoto at level 26 with high-tier items and new orders |
| Screenshot 5 | Begrüßung: Namen eingeben, Café benennen und aus zwölf Figuren wählen | Welcome screen: enter a name, name your café and pick one of twelve characters |
| Screenshot 6 | Täglicher Bonus: sieben Tage mit Münzen, Energie und Diamanten, dazu der Knopf „Abholen“ | Daily bonus: seven days of coins, energy and gems, with a Claim button |

**Wie die Screenshots entstanden sind (ehrlich dokumentiert):** Sie sind Aufnahmen der Web-Fassung desselben Codes in Chrome (360×640 Pixel, dreifach vergrößert), nicht vom Telefon. Die Bretter und Aufträge sind vorbereitet, damit das Bild etwas zeigt; Oberfläche, Grafik und Texte kommen unverändert aus dem Spiel, nichts wurde nachträglich eingefügt. Name „Mia“ und Café „Café Sonne“ / „Sunny Café“ sind erfunden. Keine Statusleiste, keine Finger, keine Geräterahmen, keine Werbetexte im Bild. Vor dem Upload mit dem ersten Test-APK gegenprüfen, dass die App auf dem Gerät gleich aussieht; weichen Schriften oder Abstände ab, Screenshots vom Gerät aufnehmen und austauschen.

**Bekannte Lücken in den Bildern:** Wien (Welt 2) zeigt als Boden noch den vorläufigen Entwurf, Böden und Einzugs-Posen der Welten 4 bis 9 fehlen (`CLAUDE.md`, Abschnitt Bilder); die Screenshots zeigen deshalb nur Hamburg, Paris und Kyoto, wo die Boden-Grafik passt oder der gebaute Boden gut aussieht. Kyoto nutzt den gebauten Boden.

## 6. Beleg der Aussagen im Text

Jede Zahl und jede Funktion im Text muss im Spiel stimmen. Die Zahlen prüft `tests/test_store.py` gegen `www/index.html`.

| Aussage | Beleg |
|---|---|
| 22 Leckereien in 3 Ketten | `CHAINS`: 7 Kaffee, 8 Backwaren, 7 Frühstück |
| Kaffeebohne → Espresso → Matcha → Bubble Tea; Weizen → Festtorte | `CHAINS.de`: Kaffeebohne, Espresso, Matcha, Bubble Tea …; Weizen, Brot … Festtorte |
| Teekanne, Brotkorb, Hühnerstall | `CHAINS.genName` |
| 9 Welten von Hamburg bis Sternecafé | `CHAPTERS`: Hamburg, Wien, Paris, Rom, Istanbul, Kyoto, New York, Rio de Janeiro, Sternecafé |
| 12 Figuren, eigener Café-Name | `www/art/a1…a12`; Begrüßung in `showOnboarding` |
| Café-Katze Mocha: antippen, streicheln, schnurrt | `CatFx` (Sprung, Streichen, Herzen; Ton nur bei eingeschaltetem Ton), `tests/test_katze.py` |
| Täglicher Bonus, 7-Tage-Serie | `DAILY` mit 7 Einträgen |
| Geschenke gratis, Zufall, Chancen im Diamanten-Fenster | `GIFT_P`, Fenster „Chancen im Spiel“, `tests/test_gesamt.py` |
| Bestellungen laufen nie ab | Aufträge haben keinen Zeitstempel; neue entstehen nur, wenn ein Platz frei ist (`fillOrders`) |
| Zutaten kosten Energie, füllt sich von selbst auf, mit Diamanten oder Video auffüllbar | `CONFIG.energyRegenMs` (90 s je Punkt), Auffüllen für 15 Diamanten, Video „+25 Energie“ |
| Keine Banner, keine Pflicht-Werbung | nur belohnte Videos auf Tipp (`docs/MONETARISIERUNG.md`) |
| Kein Konto, Spielstand auf dem Gerät | kein Login im Code; Speicherung lokal (`mergecafe_v1`), `docs/PRIVACY.md` |
| Deutsch und Englisch | `STR.de`, `STR.en` |
| Einwilligung „wo vorgeschrieben“ | Google-Einwilligungsfenster (UMP) vor jeder Werbung; ob es erscheint, entscheidet Google nach Region |
| Ab 16 Jahren | Zielgruppen-Empfehlung, `docs/ALTERSFREIGABE.md` (**Eigentümer bestätigt**) |

## 7. Regelcheck (Play-Richtlinien „Metadaten“ und Vorgaben für Grafiken)

| Regel | Stand |
|---|---|
| Titel höchstens 30 Zeichen; keine Emojis, keine wiederholten Sonderzeichen; keine Wörter zu Rang, Preis oder Aktion („Kostenlos“, „Beste“) | erfüllt |
| Kurzbeschreibung höchstens 80, Beschreibung höchstens 4000 Zeichen; ehrlich, passend zum Spiel | erfüllt; Beschreibung nennt Werbung, Käufe, Energie und Zufallsgeschenke offen |
| Keine Namen anderer Spiele oder Marken in Titel, Beschreibung, Stichwörtern (`CLAUDE.md`) | erfüllt; `tests/test_store.py` prüft eine Negativliste, ersetzt aber nicht die Sichtprüfung |
| Keine Preis-, Rang- oder Aktionsangaben und keine Handlungsaufforderung in Bildern („Jetzt laden“) | erfüllt: im Bild nur Titel und Schlagworte |
| Screenshots zeigen das echte Spiel; keine Finger, keine Geräterahmen, keine Statusleiste | erfüllt (Abschnitt 5) |
| Schlagzeilen im Screenshot höchstens 20 % der Bildfläche | erfüllt: keine Schlagzeilen |
| Feature-Grafik: kein reines Weiß, Schwarz oder Dunkelgrau; keine Geräte- oder Store-Symbole; keine fremden Figuren | erfüllt |
| Screenshots 2 bis 8, je Seite 320 bis 3840 px, lange Seite höchstens 2,3-mal die kurze, höchstens 8 MB, 24-Bit-PNG oder JPEG | erfüllt (6 Stück, 1080×1920) |
| Für große Empfehlungsflächen bei Spielen: mindestens 3 Screenshots in 9:16 mit mindestens 1080×1920 | erfüllt |
| Alt-Text höchstens 140 Zeichen je Bild | erfüllt (Abschnitt 5) |
| Bilder spiegeln den aktuellen Stand | Stand 1.5.12; bei sichtbaren Änderungen neu erzeugen |

## 8. Offen (nur der Eigentümer kann das)

1. **Namensfreigabe** eintragen (`docs/RECHT_UND_NAMEN.md`, Abschnitt 5.3). Ohne sie kein Upload und keine Werbetexte.
2. **Impressum und Datenschutz** mit echten Angaben füllen (Platzhalter `[[…]]` in `www/impressum.html`, `www/privacy.html`), dazu die Kontakt-E-Mail der Console. Ohne das bleiben Werbung und Käufe aus.
3. **Zielgruppe „ab 16“** bestätigen oder ändern; danach den Satz „Für Spieler ab 16 Jahren“ anpassen.
4. **Standardsprache, Kategorie und Tags** in der Console bestätigen; Texte erst nach der Freigabe einfügen.
5. **Icon und Spielbilder:** Herkunft und Nutzungsrechte der mit einem Bildwerkzeug erzeugten Bilder (Icon, Figuren, Katze, Teile) bestätigen (`docs/ASSETS_LIZENZEN.md`).
6. **Screenshots vom Gerät** nach dem ersten Test-APK gegenprüfen (Abschnitt 5).

## Quellen

- Play Console Hilfe, Vorschau-Elemente (Icon, Feature-Grafik, Screenshots, Alt-Text): https://support.google.com/googleplay/android-developer/answer/9866151
- Play Console Hilfe, Beste Praxis für den Store-Eintrag (Zeichenlängen, Titel): https://support.google.com/googleplay/android-developer/answer/13393723
- Google Play Richtlinie „Metadaten“: https://support.google.com/googleplay/android-developer/answer/9898842
- Icon-Gestaltung: https://developer.android.com/google-play/resources/icon-design-specifications
