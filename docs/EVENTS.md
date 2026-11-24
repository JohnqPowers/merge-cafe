# Event-Katalog (AppsFlyer / Almedia)

Alle Events werden über `Platform.track()` an AppsFlyer gesendet, und zwar **nur nach Einwilligung** des Spielers (Einwilligungsfenster, `docs/PRIVACY.md`). Ohne Einwilligung oder solange `CONFIG.legalReady` falsch ist, wird nichts gesendet. Firebase oder gtag gibt es im Code nicht. Events mit „einmalig“ feuern pro Spieler genau einmal – genau das brauchen Almedia-Meilensteine.

| Event | einmalig | Auslöser | Almedia-Meilenstein |
|---|---|---|---|
| `session_start` | nein | App-Start | – |
| `onboarding_complete` | nein | Begrüßung abgeschlossen (Name, Café und Figur gewählt, beim ersten Start) | Analyse |
| `first_merge` | ja | erstes Verschmelzen | – |
| `tutorial_complete` | ja | erster Auftrag im Tutorial geliefert | **Schritt 1** |
| `first_order` | ja | erster Auftrag | – |
| `order_complete` (params `level`, `coins`) | nein | jeder gelieferte Auftrag | Analyse |
| `level_up` (param `level`) | nein | jedes Level | Analyse |
| `level_2`,`level_3`,`level_5`,`level_7`,`level_10`,`level_12`,`level_15`,`level_20`,`level_25`,`level_30`,`level_40`,`level_50` | ja | Level erreicht | **Schritte 2–10** |
| `orders_10/25/50/100/250/500` | ja | Anzahl gelieferter Aufträge | Alternative Schritte |
| `max_item_chain0/1/2` | ja | Höchststufe einer Kette | Bonus-Schritt |
| `world_unlocked` (params `world`, `level`, `stop`) | nein | neue Stadt der Weltreise freigeschaltet (Postkarte) | Analyse – nicht für Almedia-Abrechnung |
| `first_upgrade` | ja | erstes Upgrade gekauft | – |
| `daily_claim` (param `streak`) | nein | Tagesbonus abgeholt | Analyse |
| `daily_streak_7` | ja | 7 Tage Login-Bonus in Folge | Retention-Schritt |
| `second_session`, `retained_d1`, `retained_d7` | ja | Rückkehr | Retention |
| `ad_request` (param `placement`) | nein | Spieler tippt ein Werbe-Angebot an (vor der Anzeige) – Annahmequote = `ad_rewarded` ÷ `ad_request` | Analyse |
| `ad_rewarded` (param `placement`: `shop_energy`, `dbl_order`, `dbl_gift`, `dbl_daily`) | nein | Belohnte Werbung angesehen | ROAS (Werbeumsatz) |
| `first_ad` | ja | erste belohnte Werbung | Analyse |
| `spend_gems` (params `what`: `energy`, `order_items`; `amount`) | nein | Diamanten ausgegeben | Analyse |
| `first_gem_spend` | ja | erste Diamanten-Ausgabe | Analyse |
| `gift_open` (param `reward`) | nein | Geschenk aus dem Geschenk-Fach geöffnet | Analyse |
| `purchase` (params `sku`, `af_revenue`, `af_currency`) | nein | In-App-Kauf (Diamanten, Startpaket) oder Pro-Kauf (`sku` = Store-Produkt des gekauften Pakets, z. B. `monthly`, `yearly`, `lifetime`) | ROAS |
| `first_purchase` | ja | erster Kauf (auch der erste Pro-Kauf) | **Kauf-Schritt** |
| `paywall_open` (param `place`: `shop`, `settings`) | nein | Pro-Fenster geöffnet (RevenueCat-Paywall oder eigene Liste); Trichter `paywall_open` → `pro_start` | Analyse |
| `pro_start` (param `sku`) | ja | Pro erstmals aktiv (Kauf oder Wiederherstellung; nach Neuinstallation erneut) | Analyse |
| `pro_restore` (param `sku`) | nein | Pro über „Käufe wiederherstellen“ oder die Paywall zurückgeholt (kein Umsatz) | Analyse |

Hinweis Umsatz: Das Spiel sendet `purchase` selbst, mit `af_revenue` (Preis aus dem Store) und `af_currency`. **Die serverseitige Weitergabe von RevenueCat an AppsFlyer nicht zusätzlich einschalten**, sonst wird derselbe Umsatz doppelt gezählt (`docs/MONETARISIERUNG.md`, Punkt M4).

Hinweis Namen: Bestehende Event-Namen niemals umbenennen, Almedia rechnet darüber ab. Neue Events nur hinzufügen und hier eintragen.

Hinweis 24.11.2026: Die Zeilen `order_complete`, `daily_claim` und `onboarding_complete` fehlten im Katalog, obwohl der Code sie sendet; nachgetragen, Namen unverändert.

Hinweis v1.5.0: Bestehende Event-Namen wurden nicht umbenannt; es kamen nur die Zeilen `ad_request`, `first_ad`, `first_gem_spend` (und neue Parameterwerte) hinzu.

Hinweis v1.5.14 (Noa's Pro): Es kamen nur die Zeilen `paywall_open`, `pro_start`, `pro_restore` hinzu; kein Name wurde geändert. Pro-Spieler holen Belohnungen ohne Video ab und erzeugen deshalb **kein** `ad_request`/`ad_rewarded` (Annahmequote nur über Nicht-Pro-Spieler lesen). Das Spiel sendet `purchase` nur beim **ersten** Kauf eines Pro-Pakets (Preis des Pakets, brutto); Verlängerungen eines Abos sendet es nicht. Abo-Umsatz im Zeitverlauf steht im RevenueCat-Dashboard. Die Weitergabe von RevenueCat an AppsFlyer bleibt aus (sonst Doppelzählung des ersten Kaufs).
