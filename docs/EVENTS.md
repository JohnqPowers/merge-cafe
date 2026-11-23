# Event-Katalog (AppsFlyer / Almedia)

Alle Events werden über `Platform.track()` an AppsFlyer (und optional Firebase/gtag) gesendet. Events mit „einmalig“ feuern pro Spieler genau einmal – genau das brauchen Almedia-Meilensteine.

| Event | einmalig | Auslöser | Almedia-Meilenstein |
|---|---|---|---|
| `session_start` | nein | App-Start | – |
| `first_merge` | ja | erstes Verschmelzen | – |
| `tutorial_complete` | ja | erster Auftrag im Tutorial geliefert | **Schritt 1** |
| `first_order` | ja | erster Auftrag | – |
| `level_up` (param `level`) | nein | jedes Level | Analyse |
| `level_2`,`level_3`,`level_5`,`level_7`,`level_10`,`level_12`,`level_15`,`level_20`,`level_25`,`level_30`,`level_40`,`level_50` | ja | Level erreicht | **Schritte 2–10** |
| `orders_10/25/50/100/250/500` | ja | Anzahl gelieferter Aufträge | Alternative Schritte |
| `max_item_chain0/1/2` | ja | Höchststufe einer Kette | Bonus-Schritt |
| `world_unlocked` (params `world`, `level`, `stop`) | nein | neue Stadt der Weltreise freigeschaltet (Postkarte) | Analyse – nicht für Almedia-Abrechnung |
| `first_upgrade` | ja | erstes Upgrade gekauft | – |
| `daily_streak_7` | ja | 7 Tage Login-Bonus in Folge | Retention-Schritt |
| `second_session`, `retained_d1`, `retained_d7` | ja | Rückkehr | Retention |
| `ad_request` (param `placement`) | nein | Spieler tippt ein Werbe-Angebot an (vor der Anzeige) – Annahmequote = `ad_rewarded` ÷ `ad_request` | Analyse |
| `ad_rewarded` (param `placement`: `shop_energy`, `dbl_order`, `dbl_gift`, `dbl_daily`) | nein | Belohnte Werbung angesehen | ROAS (Werbeumsatz) |
| `first_ad` | ja | erste belohnte Werbung | Analyse |
| `spend_gems` (params `what`: `energy`, `order_items`; `amount`) | nein | Diamanten ausgegeben | Analyse |
| `first_gem_spend` | ja | erste Diamanten-Ausgabe | Analyse |
| `gift_open` (param `reward`) | nein | Geschenk aus dem Geschenk-Fach geöffnet | Analyse |
| `purchase` (param `sku`) | nein | In-App-Kauf | ROAS |
| `first_purchase` | ja | erster Kauf | **Kauf-Schritt** |

Hinweis: Für Umsatz-Events in AppsFlyer zusätzlich `af_revenue` + `af_currency` mitsenden (RevenueCat kann Käufe auch serverseitig an AppsFlyer melden – empfohlen).

Hinweis v1.5.0: Bestehende Event-Namen wurden nicht umbenannt; es kamen nur die Zeilen `ad_request`, `first_ad`, `first_gem_spend` (und neue Parameterwerte) hinzu.
