# Noa's Bean Trail – Launch-Plan (CEO · CTO · CFO · COO)

Stand: 12.11.2026 · Alle Entscheidungen sind getroffen; offene Zahlen sind als **Annahme** markiert und werden nach dem Soft Launch durch echte Daten ersetzt.

---

## 1. CEO – Strategie

**Was funktioniert auf Almedia/Freecash?**
- Almedia nennt Casual-Puzzle- und Wortspiele als Genres mit den höchsten Auszahlungen; Beispiele: *Merge Restaurant*, *Word Farm Adventure*, *Word Collect* (Almedia-Pressemitteilung, Okt. 2026).
- Rewarded UA bezahlt pro erreichtem Meilenstein (Multi-Reward-CPE). Laut Unity haben die meisten dieser Kampagnen 7–10 Stufen.
- Nutzer aus Offerwalls bleiben deutlich länger als andere Nutzer (laut MAF D7-Retention +86 %), **wenn** das Spiel tiefe, gleichmäßige Progression hat.

**Entscheidung:** Merge-2-Spiel mit Aufträgen und Leveln („Noa's Bean Trail“).
- Bewährtes Genre, leicht zu erlernen, endlos skalierbar über Level
- Energie-System = natürliche Monetarisierung (Werbung + Diamanten)
- Level sind perfekte Meilensteine für Almedia (Level 3 … Level 30)

**Plattform-Reihenfolge:** Android → Web-Portale → iOS.
Begründung: Freecash war 2026 zeitweise aus beiden Stores entfernt und ist bisher nur in Google Play zurück (iOS noch offen). Auf iOS gibt es außerdem Einschränkungen für incentivierte Kampagnen. Deshalb zuerst Android.

**Zielmärkte:** DE/AT/CH + USA, UK, CA, AU (Spiel ist zweisprachig DE/EN).

---

## 2. CTO – Technik (fertig gebaut)

| Baustein | Lösung | Status |
|---|---|---|
| Spiel | HTML5, eine Datei, ohne Engine, offline-fähig | ✅ fertig |
| Android/iOS | Capacitor-Wrapper | ✅ konfiguriert |
| Attribution (Pflicht für Almedia) | AppsFlyer-Plugin, Events in `docs/EVENTS.md` | ✅ eingebaut, Dev Key eintragen |
| Werbung | AdMob Rewarded (Energie +25, max. 6/Tag; dazu freiwillige ×2-Angebote nach Lieferung/Geschenk/Tagesbonus, max. 8/Tag; Vorladen + EU-Einwilligung/UMP) | ✅ eingebaut, Test-IDs; GDPR-Nachricht in der AdMob-Konsole noch einzurichten (Eigentümer) |
| Käufe | RevenueCat (Starterpaket 1,99 €, 0,99 €, 4,99 €) | ✅ eingebaut, Produkte anlegen |
| Speicherstand | lokal auf dem Gerät | ✅ |
| Web | PWA + ZIP für Portale | ✅ |

**Progression (simuliert, Median über 50 Durchläufe):**

| Level | ca. Spielzeit (aktiver Spieler) |
|---|---|
| 3 | 3–5 Min. (Tutorial) |
| 5 | ~15 Min. |
| 7 | ~30 Min. |
| 10 | 1–2 Tage |
| 12 | 2–3 Tage |
| 15 | ~1 Woche |
| 20 | 2–3 Wochen |
| 25 | ~4 Wochen |
| 30 | 6–8 Wochen |

Genau diese Kurve (schnelle Erfolge, dann langer Weg) braucht eine Multi-Reward-Kampagne.

**Roadmap (Live-Ops) – Stand 23.11.2026:**
- ✅ v1.5: „Candy-Glanz“-Design (Symbole statt Emoji im Menü, XP-Ring, 3D-Knöpfe), Start-Ruckler behoben, Diamanten-Erklärung + neue Senke „Zutaten kaufen“, Geschenk-Fach statt Zwangs-Popups, Level-Banner statt Vollbild, neue freiwillige Werbe-Angebote
- v1.6: Tages-Aufgaben (3 pro Tag mit Truhe) + Glücksrad (1× gratis, Zusatzdrehung per Werbung)
- v1.7: Sammelalbum (Stadt-Serien, Belohnung pro vollständiger Seite) + Katzen-Garderobe als Diamanten-Senke
- v1.8: Winterzauber-Event ab 1.12. (Event-Namen vorher in `docs/EVENTS.md` festlegen!) + Push „Energie voll“
- v1.9: Cloud-Speicherstand, Remote-Config für A/B-Tests (Energiekosten, Werbe-Angebote)

---

## 3. CFO – Kosten & Wirtschaftlichkeit

**Fixkosten bis zum Launch**

| Posten | Kosten |
|---|---|
| Google Play Konto | 25 USD einmalig |
| Apple Developer (erst Phase 3) | 99 USD/Jahr |
| Domain + Datenschutz-Seite | ~15 €/Jahr |
| AppsFlyer, AdMob, RevenueCat | Einstiegstarife kostenlos bzw. umsatzabhängig – Preise vor Start prüfen |
| **Summe Phase 1** | **< 50 €** |

**UA-Budget Almedia (Annahme, mit Almedia verhandeln):**
- Soft-Launch-Test: **3.000 €** über 3–4 Wochen, nur Android, DACH + 1 Tier-1-Markt
- Nur skalieren, wenn **D7-ROAS ≥ 15 %** und **D30-ROAS ≥ 40 %** (Ziel: Break-even nach 90–120 Tagen)

**Vorgeschlagene Meilenstein-Leiter (Auszahlung pro Nutzer – Annahme, Almedia setzt die Endpreise):**

| # | Event | Anteil am Gesamtbudget je Nutzer |
|---|---|---|
| 1 | `tutorial_complete` | 3 % |
| 2 | `level_5` | 5 % |
| 3 | `level_7` | 7 % |
| 4 | `level_10` | 10 % |
| 5 | `level_12` | 10 % |
| 6 | `level_15` | 15 % |
| 7 | `level_20` | 20 % |
| 8 | `level_25` | 15 % |
| 9 | `level_30` | 15 % |
| + | `first_purchase` | Bonus (eigener Satz) |

Logik: früh kleine Belohnungen (Einstieg), großer Anteil ab Level 15 – dort sind nur noch Nutzer, die wirklich spielen (Werbung schauen, kaufen).

**Einnahmequellen pro Nutzer:** Rewarded Ads (bis 6 pro Tag) + Diamantenkäufe + Starterpaket.
Die Ökonomie ist bewusst so gebaut, dass Offerwall-Spieler ab ~Level 12 an die Energiegrenze stoßen → Werbung/Kauf.

---

## 4. COO – Ablauf (Woche für Woche)

| Woche | Aufgabe | Ergebnis |
|---|---|---|
| 0 | Namens- und Markenrecherche (DPMA, TMview, WIPO, App Stores), Impressum und Datenschutz mit echten Angaben füllen; Checkliste in `docs/RECHT_UND_NAMEN.md` | Name freigegeben (vor Play-Upload und vor dem Almedia-Kontakt) |
| 1 | Konten anlegen (Play Console, AdMob, AppsFlyer, RevenueCat), IDs in `CONFIG` eintragen, `PRIVACY.md` hosten | Release-fähiger Build |
| 1 | `npm install` → Android-Build (README), interner Test mit 5–10 Leuten | Bugfreie .aab |
| 2 | Play-Store-Eintrag (Texte in `STORE_LISTING.md`, Grafiken in `store/`), Closed Testing (bei neuen Privatkonten verlangt Google einen geschlossenen Test mit mehreren Testern über mehrere Tage – frühzeitig starten) | Freigabe |
| 2 | Almedia kontaktieren: almedia.co → „Get started“ / Kontaktformular (Antwort laut Almedia in 2–3 Werktagen; Alternative: partners@almedia.co). Pitch-Text siehe unten | Erstgespräch |
| 3 | AppsFlyer ↔ Almedia verbinden (Almedia als Partner aktivieren), Event-Leiter abstimmen | Tracking live |
| 3–6 | Soft Launch 3.000 €, tägliche Kontrolle: Installs, Tutorial-Rate, D1/D7, ROAS | Daten |
| 6 | Entscheidung: skalieren / Ökonomie anpassen / stoppen | Go/No-Go |
| 7+ | Web-Portale (itch.io, CrazyGames, Poki) für organische Reichweite, iOS-Port | Wachstum |

**KPI-Ziele Soft Launch**

| KPI | Ziel |
|---|---|
| Tutorial abgeschlossen | ≥ 85 % |
| D1-Retention | ≥ 40 % |
| D7-Retention | ≥ 15 % |
| Rewarded Ads / DAU | ≥ 2 |
| Zahlende Nutzer | ≥ 2 % |

### Pitch-Text für das Almedia-Formular
> We are launching **Noa's Bean Trail**, a casual merge-2 game (DE/EN) on Google Play. Deep level progression designed for multi-reward CPE: tutorial → level 5/7/10/12/15/20/25/30 + first purchase, all tracked via AppsFlyer. Monetization: rewarded video + IAP. We'd like to start a soft-launch test (Android, DACH + US/UK) with ~€3k and scale on D7/D30 ROAS. Could you share your recommended event ladder and payout ranges for casual merge titles?

---

## 5. Risiken & Gegenmaßnahmen
- **Plattform-Risiko Freecash (Store-Entfernung 2026):** Nicht 100 % des Budgets in einen Kanal; parallel Tests mit anderen Rewarded-Netzwerken möglich (z. B. Mistplay, Tapjoy/Unity, adjoe).
- **Betrug/Low-Quality-Nutzer:** AppsFlyer Protect360 oder Plausibilitätsprüfung (Level-Zeiten); Spielstand ist lokal – für große Budgets in v1.1 serverseitige Validierung der Meilensteine einbauen.
- **Ökonomie zu streng/zu leicht:** `xpNeed()` und `CONFIG.energyRegenMs` in `index.html` sind die zwei Stellschrauben.
- **Rechtliches:** Datenschutzerklärung, Impressum (DE), Altersfreigabe IARC im Play-Fragebogen ausfüllen; ich bin kein Anwalt – Datenschutztext vor Veröffentlichung prüfen lassen.
- **Namens-/Klon-Vorwurf (geprüft 24.11.2026):** Idee und Mechanik des Genres sind frei, Code/Grafik/Name eigen; Restrisiko liegt beim Namen (Marken- und Titelkollision). Vor Upload und Werbung: Registerrecherche und Freigabe laut `docs/RECHT_UND_NAMEN.md`. Keine Nachbildung bestimmter Spiele.
