# Altersfreigabe und Jugendschutz – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.13. Entwurf für die Play Console (Abschnitte „Zielgruppe und Inhalt“ und „Inhaltseinstufung“). Keine Rechtsberatung. Verbindlich ist, was der Einstufungs-Fragebogen (IARC) am Ende ergibt; der Wortlaut der Fragen ändert sich, beim Ausfüllen gilt die dann aktuelle Fassung.

## 1. Entscheidung

| Punkt | Entscheidung | Grund |
|---|---|---|
| Zielgruppe in der Play Console | **16–17 Jahre und 18+** (keine Kinder-Altersgruppen) | (1) Für Einwilligungen in Werbung und Messung gilt in Deutschland ein Einwilligungsalter von 16 (DSGVO Art. 8, keine nationale Absenkung). (2) Die Bewerbung über Belohnungs-Plattformen richtet sich an Erwachsene. (3) Es entfallen die Anforderungen des Families-Programms (u. a. nur zertifizierte Werbe-SDKs); bei reinen Kinder-Apps ist die Weitergabe der Werbe-ID untersagt, die AdMob und AppsFlyer nutzen. |
| Inhaltseinstufung (IARC) | erwartet **USK 0 / PEGI 3 / ESRB Everyone** | Keine Gewalt, keine sexuellen Inhalte, keine Sprache, kein Glücksspiel, keine Nutzerkommunikation. |
| Zusatzhinweise (USK) | „In-Game-Käufe“ sicher; „Druck zum Vielspielen“ möglich (Abschnitt 3) | Echtgeld-Käufe für Diamanten; Tagesbonus mit Serie. |
| Aussage im Spiel und in den Texten | „richtet sich an Nutzer ab 16 Jahren“ | passt zu Datenschutzseite und Zielgruppe |

Die Zielgruppe ist eine Empfehlung des Agenten. Der Eigentümer trägt sie in der Play Console ein und kann sie später ändern.

**Risiko:** Google prüft selbst, ob Bildsprache und Wortwahl Kinder ansprechen, unabhängig von der Angabe in der Konsole (siehe Quellen). Die Candy-Optik ist freundlich und bunt. Stuft Google die Zielgruppe als gemischt ein, drohen Auflagen (neutrale Altersabfrage, nur nicht-personalisierte Werbung für Kinder). Plan B steht in Abschnitt 5.

## 2. Inhalte (Fakten aus dem Code, v1.5.13)

| Merkmal | Stand |
|---|---|
| Gewalt, Angst, Horror | keine |
| Sexuelle Inhalte, Nacktheit | keine |
| Schimpfwörter, derbe Sprache | keine; Texte kurz und freundlich (Deutsch, Englisch) |
| Alkohol, Tabak, Drogen | nicht dargestellt. Getränke: Kaffee, Tee, Matcha, Bubble Tea, Frappé, „Mocktail“ (alkoholfrei, Emoji 🍹). Bei Rückfragen des Prüfers das Emoji ersetzen. |
| Glücksspiel | keines. Keine Einsätze, keine Gewinne gegen Geld, keine Wetten. |
| Zufallsbelohnungen | nur **kostenlose** Geschenke (Münzen, Energie oder Diamanten, siehe `docs/MONETARISIERUNG.md`). Nichts Zufälliges ist kaufbar. |
| Chat, Nutzerinhalte, soziale Funktionen | keine |
| Konto, Anmeldung | keine. Spielername (bis 16 Zeichen) und Café-Name (bis 24 Zeichen) bleiben auf dem Gerät. |
| Standort, Kamera, Mikrofon, Kontakte, Dateien | nicht genutzt (Berechtigungen: `docs/TECHNIK.md`) |
| Browser im Spiel, Links nach außen | nur Datenschutz, Impressum, Lizenzen (eigene Seiten) |
| Käufe mit Echtgeld | ja: Diamanten-Pakete und ein einmaliges Startpaket, über Google Play |
| Werbung | ja: nur freiwillige Videos mit Belohnung (kein Banner, kein Zwangsvideo) |
| Zeitdruck | Aufträge laufen nie ab, Kauf-Angebote mit Ablaufzeit gibt es nicht. Es gibt eine Energie, die sich alle 90 Sekunden um 1 füllt. Das kleine Video-Angebot „Münzen verdoppeln“ blendet sich nach 7 Sekunden aus, zeigt keinen Countdown und kostet kein Geld. |
| Benachrichtigungen | keine (keine Push-Mitteilungen) |

## 3. Fragen, bei denen ehrlich „Ja“ oder genau hinzusehen ist

| Frage im Fragebogen (sinngemäß) | Antwort | Anmerkung |
|---|---|---|
| Kann man digitale Güter oder Währung kaufen? | **Ja** | Diamanten (60 und 400) und Startpaket (100 Diamanten + 500 Münzen, einmalig). |
| Gibt es Zufallsgegenstände gegen Geld („Lootboxen“)? | **Nein** | Diamanten kaufen immer feste Mengen; Geschenke sind gratis. |
| Gibt es Werbung? | **Ja** | Belohnte Videos über Google AdMob, Inhaltsstufe auf „ParentalGuidance“ begrenzt. |
| Gibt es tägliche Belohnungen, die zum Wiederkommen drängen? | **Ja, ehrlich angeben** | Tagesbonus über 7 Tage; verpasst man einen Tag, beginnt die Serie wieder bei Tag 1. Daraus kann der Zusatzhinweis „Druck zum Vielspielen“ entstehen. Er ändert die Altersstufe nach unserem Stand nicht, ist aber sichtbar. Eine mildere Regel (Serie pausiert statt zurückzusetzen) wäre eine Balancing-Änderung und wird erst mit KPI-Daten entschieden. |
| Aufdringliche Kaufangebote? | **Nein** | Der Weg zu den Kauf-Knöpfen führt nur über den Shop (auch aus dem Info-Fenster „Was sind Diamanten?“); kein Pop-up mit Echtgeld-Angebot, keine Kauf-Angebote mit Ablaufzeit. |
| Nutzerkommunikation, Nutzerinhalte, Standort? | **Nein** | – |
| Teilen persönlicher Daten mit Dritten? | **Ja (Gerätekennungen)** | Nur nach Einwilligung: AdMob (Werbung), AppsFlyer (Messung). Details: `docs/PRIVACY.md`. |

**Wo steht der Fragebogen?** In der Google Play Console, nicht im Spiel und nicht im Repo. Die App muss dort zuerst angelegt sein. Dann: Play Console › Richtlinie (Bereich „Überwachen und verbessern“, Eintrag „Richtlinie und Programme“) › **App-Inhalte**. Dort liegen zwei Aufgaben: **„Zielgruppe und Inhalt“** (Zielgruppe wählen, Empfehlung: 16–17 und 18+) und die **Inhaltseinstufung** (IARC-Fragebogen, Start, E-Mail-Adresse eintragen, Kategorie „Spiel“ wählen, Fragen nach den Antworten in diesem Abschnitt beantworten, am Ende Einstufung speichern). Die Menüführung kann sich ändern; maßgeblich ist, was die Console zeigt.

## 4. Jugendschutz im Spiel (was schon da ist)

- **Kein Konto, keine Kommunikation, keine fremden Inhalte:** Kinder und Jugendliche können im Spiel nicht angesprochen werden.
- **Keine Kaufaufforderung an Kinder:** Käufe nur im Shop, nur auf Tipp; Preise kommen vom Store (kein versteckter Preis); der Kauf läuft über Google Play und dessen Familienfunktionen (Kaufsperre, Passwort-Abfrage).
- **Werbung freiwillig und begrenzt:** nur auf Tipp des Spielers, das Angebot „Münzen verdoppeln“ nie im Tutorial und erst ab Level 3, höchstens 6 Energie-Videos und 8 Verdopplungen am Tag (`AD_CAP` im Code); Inhaltsstufe „ParentalGuidance“.
- **Einwilligung zuerst:** Bei Start in der App erscheint das Google-Einwilligungsfenster (UMP). Ohne Einwilligung werden weder Werbung angefordert noch Messdaten gesendet. Später widerrufbar unter Optionen → Werbe-Einstellungen.
- **Sperre bei unvollständigen Rechtstexten:** Solange Impressum oder Datenschutz Platzhalter enthalten, bleiben Werbung, Käufe und Messung in der App aus (`CONFIG.legalReady`). Stand 24.11.2026: keine Platzhalter mehr, die Sperre ist offen.
- **Keine Dark Patterns:** keine versteckten Kosten, keine falschen Zeitgeber, keine Schuldzuweisung beim Ablehnen von Werbung, kein Verlust von Spielfortschritt (nur die Serie des Tagesbonus beginnt nach einem verpassten Tag neu, siehe Abschnitt 3).

## 5. Plan B, falls Google die Zielgruppe als gemischt einstuft

1. Neutrale Altersabfrage beim ersten Start (Geburtsjahr, ohne Hinweis auf eine „richtige“ Antwort, ohne Speicherung des Datums, nur Ergebnis „unter 16 / ab 16“).
2. Unter 16: Werbung nur nicht-personalisiert (AdMob-Kennzeichnung „unter dem Einwilligungsalter“), keine Messung (AppsFlyer bleibt aus), Käufe unverändert über Google Play.
3. Eintrag im Test- und Qualitätsbericht und im Datenschutztext ergänzen.

Das ist eine Code-Änderung (neue Version, Tests) und wird nur gebaut, wenn Google es verlangt.

## 6. Noch zu tun vor dem Upload (Eigentümer)

- [ ] Zielgruppe „16–17 und 18+“ in der Play Console eintragen (Entscheidung bestätigen).
- [ ] IARC-Fragebogen nach Abschnitt 3 ausfüllen; das Ergebnis (USK, PEGI, ESRB und Zusatzhinweise) hier eintragen.
- [ ] Spalte „Ergebnis“ nachtragen: Datum, USK-Stufe, Zusatzhinweise, Screenshot der Einstufung ablegen.
- [ ] iOS (später): eigener Altersfragebogen in App Store Connect.

## Quellen (Stand 24.11.2026)
- Google Play Hilfe, „Manage target audience and app content settings“: https://support.google.com/googleplay/android-developer/answer/9867159
- Google Play, „Families Policy Requirements“: https://support.google.com/googleplay/android-developer/answer/9893335
- USK, Altersfreigaben und Zusatzhinweise (u. a. „In-Game-Käufe“, „Druck zum Vielspielen“): https://usk.de/en/the-usk-age-ratings/
- USK, Spiele und Apps im IARC-System: https://usk.de/en/home/age-classification-for-games-and-apps/games-and-apps-in-the-iarc-system/
- Verbraucherzentrale (EVZ), Jugendschutz und Videospiele: https://www.evz.de/einkaufen-internet/gaming/jugendschutz-fuer-videospiele.html
