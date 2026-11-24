# Monetarisierungsdokumentation – Noa's Bean Trail

Stand: 24.11.2026, Spielversion 1.5.14 (Noa's Pro neu). Alle Zahlen stammen aus `www/index.html`; die Fundstellen stehen in Klammern. Keine Rechtsberatung. **Die Sperre `CONFIG.legalReady` (Werbung, Käufe und Messung) ist seit 24.11.2026 offen, weil Impressum und Datenschutz keine Platzhalter mehr enthalten. Echte Werbung und echte Käufe laufen erst mit Konten und Schlüsseln (GitHub-Secrets); das Test-Paket zeigt nur Googles Testanzeigen.** Es wurde kein Konto angelegt, kein Preis eingestellt und kein Geld ausgegeben.

## 1. Modell in Kürze

Kostenlos spielbar, ohne Zwang. Vier Einnahmequellen:

1. **Freiwillige Belohnungs-Videos** (Google AdMob): Spieler tippt auf ein Angebot und bekommt Energie oder eine Verdopplung. Kein Banner, kein Zwangsvideo.
2. **Diamanten-Pakete** (Echtgeld): 60 oder 400 Diamanten.
3. **Startpaket** (Echtgeld, einmalig): 100 Diamanten + 500 Münzen.
4. **Noa's Pro** (Abo monatlich oder jährlich, oder einmalig als Lifetime; RevenueCat-Entitlement `noa_s_bean_trail_pro`): Belohnungen ohne Video und täglich Diamanten. Abschnitt 3.

Diamanten sparen Zeit (Energie sofort voll, fehlende Zutaten kaufen). Alles im Spiel bleibt auch ohne Echtgeld und ohne Diamanten erreichbar (Text im Spiel: „Spielen kannst du alles auch ohne sie“). **Direkt gegen Echtgeld gibt es nichts Zufälliges.**

## 2. Währungen und Ressourcen

| Ressource | Woher | Wofür | Für Echtgeld? |
|---|---|---|---|
| **Münzen** | Lieferungen (Betrag je Auftrag), Geschenke (40 % der Geschenke), Tagesbonus (Tag 1 und 4), Stadtwechsel-Bonus (150 bis 2000), Verdopplung per Video | Ausbauten (Abschnitt 6) | nur im Startpaket (500) |
| **Diamanten** | Start 10; Level-Aufstieg (3 + 2 je 5 Level); Stadtwechsel (3 bis 15); Tagesbonus (Tag 3, 6, 7); Geschenke (25 %, 2 bis 5); erste Entdeckung einer Zutat ab Stufe 4 (+1, höchste Stufe +3) | Energie auffüllen (15); fehlende Zutaten kaufen (2 bis 45 je Zutat) | **ja** (Pakete, Startpaket) |
| **Energie** | 1 alle 90 Sekunden (`energyRegenMs`), Maximum 100 + 20 je Ausbau „Großer Akku“ (bis 200); +25 je Video; Level-Aufstieg füllt auf; Geschenke (35 %), Tagesbonus (Tag 2, 5) | 1 Energie je Antippen eines Automaten (im Tutorial gratis) | nur indirekt über Diamanten (15 = voll) |
| **XP / Level** | Lieferungen | Fortschritt | nein |

Diamanten gelten nur in diesem Spiel, lassen sich nicht übertragen und nicht auszahlen (Google Play verlangt, dass Spielwährung nur in dem Spiel genutzt wird, für das sie gekauft wurde).

## 3. Echtgeld-Käufe

| Produkt-ID | Inhalt | Preis im Browser (nur Anzeige) | Preis in der App |
|---|---|---|---|
| `gems_small` | 60 Diamanten | 0,99 € | **kommt vom Store** (`priceString`), Vorschlag 0,99 € |
| `gems_large` | 400 Diamanten | 4,99 € | Vorschlag 4,99 € (≈ 80 Diamanten je Euro, bei `gems_small` ≈ 61) |
| `starter_pack` | 100 Diamanten + 500 Münzen, einmalig | 1,99 € | Vorschlag 1,99 € |

- **Technik:** RevenueCat (`getProducts` Typ `inapp`, `purchaseStoreProduct`) über Google Play Billing 9.1.0. Gutschrift im Spiel direkt nach erfolgreichem Kauf (`GRANTS`, `buy()`). Der Preis wird nie im Code festgelegt: Die Knöpfe zeigen den Preis des Stores in der Landeswährung, ohne Store-Preis sind die Knöpfe gesperrt („–“).
- **Typ im Store:** Alle drei als **Verbrauchsgüter** (einmalige Produkte, mehrfach kaufbar). Das Startpaket blendet das Spiel nach dem ersten Kauf aus (`S.starter`). Der Spielstand liegt nur auf dem Gerät: Nach Neuinstallation kann das Startpaket erneut gekauft werden. Das ist bewusst akzeptiert (siehe Abschnitt 9).
- **Weg zum Kauf:** nur über den Shop. Das „+“ neben der Energie öffnet den Shop; das „+“ neben den Diamanten öffnet zuerst das Info-Fenster „Was sind Diamanten?“ mit dem Knopf „Diamanten kaufen“. Kein Pop-up mit Echtgeld-Angebot, keine Kauf-Aufforderung nach einer Niederlage oder bei leerer Energie (das „Keine Energie“-Fenster nennt zuerst Video, Diamanten und Warten).
- **Zahlung, Rechnung, Erstattung, Widerruf:** Google Play. Die Gutschrift erfolgt auf dem Gerät, ohne eigenen Server; eine Erstattung bei Google nimmt die Diamanten nicht zurück (kleiner Schaden, akzeptiert).
- **Messung:** Das Ereignis `purchase` trägt `af_revenue` (Store-Preis) und `af_currency`. Der Umsatz ist brutto (vor Abzug der Store-Gebühr).

### Noa's Pro (Abo und Lifetime, seit v1.5.14)

| Angabe | Wert |
|---|---|
| Entitlement (RevenueCat) | `noa_s_bean_trail_pro` (`CONFIG.revenuecat.entitlement`). Pro ist aktiv, wenn dieses Entitlement in der Kundeninfo aktiv ist. Quelle ist immer RevenueCat, nie der Spielstand: Abfrage beim Start, per Listener bei jeder Änderung und nach der Rückkehr in die App. |
| Produkte | `monthly` (Abo monatlich), `yearly` (Abo jährlich), `lifetime` (einmalig). So heißen sie im RevenueCat **Test Store**. In Google Play: ein Abo mit zwei Basis-Tarifen (monatlich, jährlich) und ein einmaliges Produkt; die Kennungen legt der Eigentümer an. Das Spiel erkennt Pakete nur am Pakettyp (`MONTHLY`, `ANNUAL`, `LIFETIME`), nie an festen Produkt-IDs. |
| Angebot und Paywall | das **aktuelle Angebot** („Current Offering“) mit den drei Paketen; die Paywall wird im RevenueCat-Dashboard gestaltet und dem Angebot zugewiesen. Das Spiel zeigt sie nur, wenn das Entitlement fehlt (`presentPaywallIfNeeded`). |
| Vorteile (Entscheidung des Agenten, **vom Eigentümer zu bestätigen**, bevor echte Produkte live gehen) | 1. **Belohnungen ohne Video:** Zeile „Pro-Bonus“ statt „Werbung ansehen“, gleiche Tageslimits (`AD_CAP`), kein `ad_request`/`ad_rewarded`. 2. **Täglich +5 Diamanten** (`PRO_GEMS`, Tag in `S.proDay`), erst nach dem Tutorial, einmal je Kalendertag. Sonst nichts: kein Vorteil auf dem Brett, keine Zusatz-Energie, keine Chancen-Änderung. |
| Wo im Spiel | Shop (Karte ganz oben) und Optionen (Zeilen „Noa's Pro“ und „Käufe wiederherstellen“). Kein Pop-up, keine Kauf-Aufforderung, keine Zeitgeber. Die Karte erscheint nur, wenn RevenueCat ein Angebot liefert; bis zur Einrichtung ist Pro also nirgends sichtbar. |
| Technik | `Platform.paywall()` (RevenueCat-Paywall; fehlt das UI-Plugin oder wirft es einen Fehler, zeigt das Spiel die eigene Liste `openPaywall()` mit `purchasePackage`), `Platform.manage()` (Customer Center; sonst Hinweis mit Link zu Google Play), `Platform.restore()`. Test: `tests/test_plattform.py`, S12 bis S18. |
| Preisvorschlag (nicht gemessen, Entscheidung des Eigentümers) | monatlich 2,99 €, jährlich 19,99 € (≈ 1,67 € je Monat, ≈ 44 % unter 12 × Monatspreis), Lifetime 39,99 € (zwei Jahre Jahres-Abo). Wegen der überschaubaren Vorteile eher niedrig ansetzen. |
| Test Store | Der **Test-Store-Schlüssel** (`test_…`) steckt nur in der Test-APK (Secret `REVENUECAT_TEST_KEY` → `build.json` im Debug-Paket). Käufe sind dort simuliert (Erfolg, Fehler oder Abbruch wählbar); Test-Abos verlängern sich höchstens 5-mal (monatlich alle 5 Minuten). Im Store-Paket wird ein `test_`-Schlüssel ignoriert, damit die App nicht abstürzt. |
| Messung | `paywall_open`, `pro_start`, `pro_restore`, beim ersten Kauf `purchase` mit Preis des Pakets und `first_purchase` (`docs/EVENTS.md`). Verlängerungen sieht nur das RevenueCat-Dashboard. |

## 4. Werbung

| Platzierung (`placement`) | Angebot | Belohnung | Tageslimit |
|---|---|---|---|
| `shop_energy` | Zeile im Shop und im Fenster „Keine Energie“ | +25 Energie | 6 pro Tag |
| `dbl_order` | kleines Angebot nach einer Lieferung („Münzen verdoppeln“, 7 Sekunden sichtbar) | doppelte Münzen der Lieferung | zusammen mit den zwei folgenden: 8 pro Tag |
| `dbl_gift` | Knopf nach dem Öffnen eines Geschenks | doppelter Geschenk-Inhalt | (siehe oben) |
| `dbl_daily` | Knopf nach dem Abholen des Tagesbonus | doppelter Tagesbonus, einmal am Tag | (siehe oben) |

Höchstens **14 Videos pro Tag** (`AD_CAP` = 6 + 8). Das Verdopplungs-Angebot nach einer Lieferung erscheint nur nach dem Tutorial, ab Level 3, bei mindestens 30 Münzen Belohnung, frühestens 2,5 Minuten nach dem letzten Angebot und nie über einem offenen Fenster (`offerDouble`).

- **Nur freiwillig:** Es läuft nie ein Video ohne Tippen des Spielers. Ablehnen kostet nichts, es gibt keinen Text, der ein schlechtes Gewissen macht.
- **Einwilligung zuerst:** In der App startet AdMob erst nach der Entscheidung im Google-Einwilligungsfenster (UMP). Ohne Einwilligung kein Video, die Knöpfe zeigen „Werbung ist aus“ (Test S2). Widerruf unter Optionen → Werbe-Einstellungen (Test S6).
- **Inhaltsstufe:** `maxAdContentRating: 'ParentalGuidance'`.
- **Belohnung nur, wenn das Plugin sie meldet.** Verhalten bei vorzeitigem Schließen mit dem echten Plugin ist noch nicht geprüft (Gerätetest, `docs/QUALITAET.md`, Abschnitt 8).
- **Test-APK:** zeigt ausschließlich Googles Test-Anzeigen (v1.5.11, `docs/TECHNIK.md`, R1). Die Store-Datei nutzt die echte Kennung aus dem Secret `ADMOB_REWARDED_ANDROID`.
- **Browser-Version:** Demo-Anzeige (Fenster mit Countdown), keine echten Anzeigen, keine Einnahmen.
- **AdMob-Umsatz** erscheint nicht in AppsFlyer; der Werbe-ROAS wird im Wochenbericht aus dem AdMob-Bericht ergänzt.

## 5. Zufallsbelohnungen und Chancen

| Zufall | Auslöser | Ergebnis (Chancen) | Kosten | Im Spiel genannt? |
|---|---|---|---|---|
| **Geschenk** (Geschenk-Fach) | nach dem Tutorial, ab der 2. Lieferung: jede 6. Lieferung oder 6 % Zufall je Lieferung; höchstens 3 im Fach | 40 % Münzen (15 bis 30 + 4 je Level), 35 % Energie (15 bis 30), 25 % Diamanten (2 bis 5) | **gratis**, nicht kaufbar | ja, seit v1.5.12 (Fenster „Was sind Diamanten?“, Abschnitt „Chancen im Spiel“) |
| **Zutat erzeugen** | Antippen eines Automaten | Stufe 2 mit **10 %** (+5 % je Ausbau „Bessere Zutaten“, höchstens 35 %), sonst Stufe 1 (im Tutorial immer Stufe 1) | 1 Energie | ja, seit v1.5.12 (aktueller Wert des Spielers) |

Einordnung: Google Play verlangt die Offenlegung der Chancen, wenn man **zufällige virtuelle Gegenstände durch einen Kauf** erhält („loot boxes“; Payments-Richtlinie, Quelle unten). Das trifft hier nicht zu: Kein Kauf liefert Zufälliges, die Diamanten-Pakete haben feste Mengen. Weil Energie (Zutat erzeugen) indirekt über Diamanten kaufbar ist, werden die Chancen **trotzdem offen genannt**. Das ist die vorsichtige Auslegung und kostet nichts.

Mit Glücksspiel hat das Spiel nichts zu tun: keine Einsätze, keine Gewinne gegen Geld, keine Auszahlung.

## 6. Belohnungs- und Preistabellen

| Posten | Wert | Quelle im Code |
|---|---|---|
| Diamanten je Level-Aufstieg | 3 + 2 × ⌊Level ÷ 5⌋ (Level 5: 5, Level 10: 7, Level 20: 11, Level 50: 23) | `onLevelUp` |
| Stadtwechsel (Münzen / Diamanten) | Wien 150/3, Paris 250/3, Rom 400/5, Istanbul 600/5, Kyoto 800/8, New York 1000/8, Rio 1400/10, Sternecafé 2000/15 (zusammen 6600 Münzen, 57 Diamanten) | `CHAPTERS` |
| Tagesbonus (7-Tage-Reihe) | 50 Münzen · 20 Energie · 5 Diamanten · 120 Münzen · 40 Energie · 10 Diamanten · 25 Diamanten; verpasster Tag: Reihe beginnt bei Tag 1 | `DAILY` |
| Entdeckung einer Zutat (einmal je Zutat) | Stufe 4 bis vorletzte: +1 Diamant; höchste Stufe: +3 | `showDiscovery` |
| Energie auffüllen | 15 Diamanten (auf das Maximum) | `refillRow` |
| Fehlende Zutat kaufen | max(2, ⌈2^Stufe × 0,35⌉) Diamanten je Teil (Stufe 1: 2, Stufe 4: 3, Stufe 6: 12, Stufe 8: 45) | `wishCost` |
| Ausbau „Bessere Zutaten“ | 80 · 2^Stufe Münzen, 5 Stufen (80 bis 1280) | `UPS` |
| Ausbau „Großer Akku“ | 150 · 2^Stufe Münzen, 5 Stufen (150 bis 2400), je +20 Energie | `UPS` |
| Ausbau „Mehr Kundschaft“ | 600 und 2500 Münzen, 2 Stufen, je +1 Auftragsplatz | `UPS` |

## 7. Regeln und Stand der Einhaltung

| Regel | Quelle | Stand |
|---|---|---|
| Digitale Güter nur über Google Play Billing | Google Play Payments-Richtlinie | erfüllt (RevenueCat → Play Billing 9.1.0) |
| Spielwährung nur im eigenen Spiel nutzbar | dieselbe Richtlinie | erfüllt |
| Chancen offenlegen bei Zufallsgegenständen aus Käufen | dieselbe Richtlinie | nicht einschlägig, trotzdem im Spiel genannt |
| Belohnungs-Werbung nur freiwillig, Belohnung vorher erkennbar | AdMob-/Play-Werberichtlinien | erfüllt nach Code; Prüfpunkt: Verdopplungs-Angebot erscheint nach einer Lieferung unten im Bild (Risiko versehentlicher Tipper, Abschnitt 9) |
| Einwilligung (EWR, Großbritannien, Schweiz) vor Werbung und Messung | Google-Richtlinie zur Einwilligung, DSGVO | umgesetzt (UMP), nur mit nachgebauten Plugins getestet |
| Keine Kauf-Aufforderungen an Kinder, keine falschen Zeitgeber | `CLAUDE.md` | erfüllt; Zielgruppe 16+ (`docs/ALTERSFREIGABE.md`); Pro erscheint nur als Karte im Shop und Zeile in den Optionen |
| Abo-Bedingungen vor dem Kauf zeigen (Preis, Laufzeit, automatische Verlängerung, Kündigungsweg) | Google Play, Abo-Richtlinien; EU-Verbraucherrecht | eigene Liste im Spiel: erfüllt (Texte `proTerms`, `perM`, `perY`, `perL`). **RevenueCat-Paywall: Der Eigentümer muss Preis, Laufzeit, automatische Verlängerung und Kündigungshinweis im Paywall-Entwurf im Dashboard zeigen.** Das lässt sich im Spiel nicht prüfen. |
| Abo kündbar und verwaltbar | dieselben | erfüllt: Customer Center, sonst Hinweis mit Link zu Google Play (Shop und Optionen) |
| **EU-Leitsätze zu Spielwährungen** (CPC-Netzwerk, 21.03.2025, nicht bindend, stützen sich auf geltendes EU-Verbraucherrecht) | siehe Quellen | Tabelle unten |

Die sieben Leitsätze und unser Stand:

| Nr. | Leitsatz (sinngemäß) | Stand |
|---|---|---|
| 1 | Echtgeld-Preis klar angeben; Waren, die mit Spielwährung bezahlt werden, auch mit Echtgeld-Preis | **teilweise offen.** Pakete zeigen den Store-Preis. Die Posten in Diamanten (Energie 15, Zutaten 2 bis 45) zeigen **keinen** Euro-Wert. |
| 2 | Preise nicht verschleiern (mehrere Währungen, mehrfaches Umtauschen vermeiden) | **teilweise.** Zwei Währungen (Münzen, Diamanten) plus Energie. Nur Diamanten sind (direkt) kaufbar, nur ein Umtausch (Diamanten → Energie). |
| 3 | Keinen Zwang, mehr Währung zu kaufen als nötig | **teilweise.** Pakete mit festen Mengen (60, 400) lassen Reste. Es gibt keine Posten, die nur über ein größeres Paket erreichbar wären. |
| 4 | Vorvertragliche Informationen beim Angebot | erfüllt über den Google-Play-Kaufdialog (Artikel, Preis); Inhalt steht im Shop („100 Diamanten + 500 Münzen, einmalig“) |
| 5 | Widerrufsrecht erklären | Google Play wickelt Zahlung und Widerruf ab; ein Hinweis im Spiel fehlt (Textvorschlag unten) |
| 6 | Faire, verständliche Bedingungen | keine eigenen Nutzungsbedingungen; Kaufbedingungen sind die von Google Play |
| 7 | Schutz von Kindern und schutzbedürftigen Verbrauchern | Zielgruppe 16+, keine Kauf-Aufforderungen, Käufe nur im Shop; Familienfunktionen von Google Play greifen |

**Empfehlung (Entscheidung beim Eigentümer, Code-Änderung):** Zu Leitsatz 1 neben „15 Diamanten“ und im Diamanten-Fenster einen Richtwert in Euro anzeigen, berechnet aus den Store-Preisen (z. B. „15 Diamanten ≈ 0,19 bis 0,25 €“ nach dem Preis je Diamant des größten und des kleinsten Pakets). Das macht Preise ehrlicher, senkt aber kaum Umsatz, weil Diamanten ohnehin nur Zeit sparen. Nicht gebaut, weil die Leitsätze nicht bindend sind und die Anzeige einen Bezugskurs voraussetzt, den der Eigentümer festlegen sollte. Vor dem ersten Umsatz steht ohnehin eine fachliche Prüfung der rechtlichen und steuerlichen Einordnung an.

Textvorschlag für eine spätere Seite „Käufe“ (vom Eigentümer fachlich prüfen zu lassen, bisher nicht in der App): „Diamanten und Münzen sind virtuelle Spielwährung. Sie haben keinen Geldwert, lassen sich nicht auszahlen oder übertragen und gelten nur in Noa's Bean Trail. Käufe laufen über Google Play; Zahlung, Rechnung, Erstattung und Widerruf richten sich nach den Bedingungen von Google Play.“

## 8. Kennzahlen und Stellschrauben

- **Ziele** (`docs/LAUNCH_PLAN.md`, `CLAUDE.md`): Tutorial ≥ 85 %, D1 ≥ 40 %, D7 ≥ 15 %, Anteil zahlender Nutzer ≥ 2 %, D7-ROAS ≥ 15 %.
- **Ereignisse für die Auswertung** (`docs/EVENTS.md`, nie umbenennen): `purchase`, `first_purchase`, `ad_request`, `ad_rewarded`, `first_ad`, `spend_gems`, `first_gem_spend`, `gift_open`. Annahmequote der Werbung = `ad_rewarded` ÷ `ad_request` (Pro-Spieler erzeugen beides nicht). Pro: `paywall_open`, `pro_start`, `pro_restore`.
- **Stellschrauben** (`CLAUDE.md`: **höchstens eine Änderung pro Woche**): `xpNeed()`, `DAILY`, `energyRegenMs`, Energiekosten, Ausbau-Preise, `AD_CAP`, Chancen (`GIFT_P`, `spawnChance`). Bei Änderungen die Anzeige „Chancen im Spiel“ mitprüfen (sie liest dieselben Werte).
- **Messlücken:** AdMob-Umsatz fehlt in AppsFlyer; die Test-APK sendet nach Einwilligung auch Messdaten (verfälscht die Zahlen); Zahlen pro Nutzer erst mit echten Daten (`reports/appsflyer/` ist bisher leer).

## 9. Risiken und offene Punkte

| Nr. | Punkt | Plan |
|---|---|---|
| M1 | **Euro-Wert der Diamanten-Posten fehlt** (EU-Leitsatz 1, nicht bindend) | Empfehlung in Abschnitt 7; Entscheidung des Eigentümers |
| M2 | Das Verdopplungs-Angebot erscheint 7 Sekunden lang direkt über der unteren Leiste. Wer gerade zieht oder tippt, könnte es versehentlich antippen und ein Video auslösen. Versehentliche Anzeigenklicks sind bei AdMob unerwünscht. | Im Gerätetest beobachten. Mögliche Abhilfe: Angebot erst nach 1 Sekunde Ruhe einblenden oder weiter von der Spielfläche abrücken. |
| M3 | Bei Rückerstattung bei Google bleiben die Diamanten (kein Server). Nach Neuinstallation ist das Startpaket erneut kaufbar. | akzeptiert (kleiner Schaden); mit Cloud-Spielstand lösbar, derzeit nicht geplant |
| M4 | RevenueCat kann Käufe zusätzlich serverseitig an AppsFlyer melden. **Nicht einschalten**, solange das Spiel `purchase` selbst sendet: sonst wird der Umsatz doppelt gezählt. | in `docs/EVENTS.md` vermerkt |
| M5 | Reale Anzeigenerlöse sind unbekannt (Füllrate, Preis je 1000 Ansichten). Es gibt keine Prognose im Repo. | nach den ersten Tagen mit Echtdaten im Wochenbericht ergänzen |
| M6 | AdMob und Play Console prüfen Konten und Apps (Genehmigung, Auszahlungsgrenze, Steuerangaben). Ablauf und Dauer sind hier nicht bekannt. | Eigentümer legt Konten an; Steuer- und Zahlungsangaben nur er |
| M7 | AdMob empfiehlt eine `app-ads.txt` auf der Entwickler-Website (Domain-Wurzel). Mit der Seite unter `johnqpowers.github.io/merge-cafe/` geht das nur über ein Repo `johnqpowers.github.io` oder eine eigene Domain. | prüfen, wenn AdMob eine Warnung zeigt |
| M8 | Echte Käufe und Anzeigen sind auf keinem Gerät gelaufen (der Android-Build 13 vom 24.11.2026 enthält die echten Plugins, ist aber nur im Paket geprüft). | Prüfliste `docs/TECHNIK.md`, Abschnitt 9, und Gerätetest |
| M9 | **Der Nutzen von Pro ist klein:** Videos sind ohnehin freiwillig, +5 Diamanten täglich sind ein Drittel einer Energiefüllung (15). Niedrige Umwandlung ist wahrscheinlich. | Preis niedrig halten; nach 2 bis 4 Wochen Daten (`paywall_open` → `pro_start`) abwarten und erst dann Vorteile ausbauen. Echte Produkte erst anlegen, wenn der Eigentümer die Vorteile bestätigt hat. |
| M10 | Der Test-Store-Schlüssel steckt in der **öffentlichen** Test-APK. Er ist ein öffentlicher SDK-Schlüssel ohne Zugriff auf Geld, Käufe sind simuliert; Fremde könnten aber Testkäufe in deinem Test Store auslösen. | akzeptiert; bei Missbrauch im Dashboard einen neuen Schlüssel erzeugen und das Secret ersetzen |
| M11 | Customer Center ist laut RevenueCat-Dokumentation an einen bezahlten Tarif gebunden (vor dem Einsatz im Dashboard prüfen); der Tarif des Eigentümers ist nicht bekannt. | ohne: Hinweis mit Link zu Google Play (eingebaut) |

## 10. Einrichtung vor dem Start (Eigentümer; der Agent legt keine Konten an und gibt kein Geld aus)

1. Impressum und Datenschutz: erledigt am 24.11.2026 (keine Platzhalter `[[…]]` mehr in `www/privacy.html` und `www/impressum.html`). Damit schaltet der Build Werbung, Käufe und Messung frei, sobald Schlüssel vorhanden sind.
2. **Google Play Console:** App anlegen, drei Produkte mit genau diesen IDs und Typ „einmalig, verbrauchbar“: `gems_small`, `gems_large`, `starter_pack`; Preise festlegen (Vorschläge in Abschnitt 3); Lizenztester eintragen. Für Pro kommen ein Abo und ein einmaliges Produkt dazu (Punkt 3a).
3. **RevenueCat:** Projekt, Android-App mit der Paket-ID, Dienstkonto, die drei Produkte; den öffentlichen Android-Schlüssel als GitHub-Secret `REVENUECAT_ANDROID_KEY` eintragen.
3a. **RevenueCat für Pro:** die Produkte `monthly`, `yearly`, `lifetime` (Test Store) bzw. die Play-Produkte dem **Entitlement `noa_s_bean_trail_pro`** zuweisen; ein **Angebot** mit den Paketen Monatlich, Jährlich und Lifetime anlegen und als „Current“ setzen; die **Paywall** im Paywall-Editor gestalten und dem Angebot zuweisen (mit Preis, Laufzeit, automatischer Verlängerung und Kündigungshinweis); optional das Customer Center einrichten. Zum Testen genügt der Test Store: Secret `REVENUECAT_TEST_KEY` setzen (`gh secret set REVENUECAT_TEST_KEY --repo JohnqPowers/merge-cafe`, fragt den Wert ab). In Google Play dazu später ein Abo (Basis-Tarife monatlich und jährlich) und ein einmaliges Produkt Lifetime.
4. **AdMob:** App und Belohnungs-Anzeigenblock anlegen; Secrets `ADMOB_APP_ID_ANDROID` und `ADMOB_REWARDED_ANDROID`; in der Konsole die **EU-Einwilligungsnachricht (UMP)** einrichten und Testgeräte eintragen.
5. **AppsFlyer:** Dev-Key als Secret `APPSFLYER_DEV_KEY`.
6. Danach (nach der Push-Freigabe) bauen lassen und die Prüfliste in `docs/TECHNIK.md`, Abschnitt 9, abarbeiten, zuerst mit der Test-APK (Test-Anzeigen), dann mit der Store-Datei in `internal`.

## Quellen (Stand 24.11.2026)
- Google Play, Payments-Richtlinie (Spielwährung, Chancen bei Zufallsgegenständen aus Käufen): https://support.google.com/googleplay/android-developer/answer/9858738
- CPC-Netzwerk der EU, „Key Principles on In-game Virtual Currencies“ (21.03.2025), zusammengefasst bei Reed Smith: https://www.reedsmith.com/articles/qas-on-the-eu-consumer-protection-authorities-joint-guidance-paper/
- Weitere Einordnung (Bird & Bird): https://www.twobirds.com/en/insights/2025/global/regulatory-spotlight-virtual-currency-vs-consumer-law-part-2
