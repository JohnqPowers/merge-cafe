# Kunst-Briefing Merge Café

Ziel: Die 22 Teile und 3 Automaten, die heute noch Emoji sind, durch eigene Bilder im Candy-Look ersetzen. Reihenfolge der Wichtigkeit: **1. Teile + Automaten**, 2. Brett-Rahmen, 3. Stadt-Hintergründe, 4. Kunden/Katze/Logo.

## Entscheidung 23.11.: Teile stehen frei, ohne Platte („Variante B“)
- Die Teile stehen direkt auf dem dunkelvioletten Brett, es gibt keine Platte mehr (nur die Automaten behalten ihre goldene Platte). Darum: **Körper hell und satt**, keine großen schwarzen oder sehr dunklen Flächen; die dunklere Kontur bleibt.
- **Hintergrund transparent** (wie bei der Kaffeebohne). Kann dein Tool das nicht: einfarbig Magenta #FF00FF, bei rosa/magentafarbenen Motiven (Bubble Tea, Mocktail) stattdessen reines Grün #00FF00.
- Rand um das Motiv ca. 8–12 % (die Bohne hat ca. 11 %, das passt).
- **Etappe 1: nur Kette 1.** Die Kaffeebohne (`k1_s1`) liegt schon vor und ist die Stil-Referenz. Es fehlen 7 Bilder: `g1_teekanne` und `k1_s2` bis `k1_s7`. Als ZIP schicken, ich prüfe sie als Reihe im Testbrett. Erst danach Kette 2 und 3.
- Wichtiger als Perfektion im Einzelbild: **alle Bilder wirken wie von einer Hand** (gleiche Kontur, gleicher Glanz, gleicher Blickwinkel leicht von oben).

## Stil (für ALLE Bilder gleich)
- Glänzende 3D-Cartoon-Optik („Gummi/Candy“), kräftige, gesättigte Farben, kein Realismus.
- Weiche, dickere Kontur in einer dunkleren Farbton des Motivs, großer weißer Glanzpunkt oben links, weiche Verläufe.
- Licht immer von oben links. **Kein Schlagschatten im Bild** (den zeichnet das Spiel).
- Motiv mittig, füllt ca. 80 % der Fläche, Vorderansicht, ohne Text, ohne Rahmen, ohne Hände.
- Wird im Spiel nur ca. **40 px** groß gezeigt: klare Silhouette, wenig Details. Test: auf 48 px verkleinern, man muss es noch erkennen.
- Jede Kette soll sichtbar „wachsen“: Stufe 1 einfach und klein wirkend, letzte Stufe festlich und üppig.

## Vorgehen für einheitlichen Stil
1. Erst **nur die Kaffeebohne** erzeugen, bis sie dir gefällt.
2. Alle weiteren Bilder mit der Kaffeebohne als **Stil-Referenz** erzeugen (Midjourney: `--sref <Bild>`; ChatGPT/Leonardo/Ideogram: Bild hochladen und „gleicher Stil wie dieses Bild“).
3. Pro Motiv die beste Version behalten.

## Prompt-Vorlage (Englisch)
```
glossy 3D cartoon game item icon of {MOTIV}, candy-like gummy look, thick soft outline,
saturated vivid colors, big white specular highlight top-left, soft gradients, centered,
front view, isolated on plain solid magenta (#FF00FF) background, no text, no cast shadow,
mobile game asset
```
Für Variante B am Ende zusätzlich anhängen: `bright light main colors, no large black areas, readable on a dark purple background`.

`{MOTIV}` aus der Liste unten einsetzen (englischer Name). Kann dein Tool echte Transparenz, ist das noch besser; sonst bitte einfarbigen magentafarbenen Hintergrund lassen, den stelle ich frei.

## Dateiformat
- PNG, quadratisch, mindestens 512×512 (ideal 1024×1024).
- Dateiname exakt wie in der Liste (kleingeschrieben, ohne Leerzeichen/Umlaute).
- Übergabe: pro Kette ein ZIP im Chat anhängen (Lieferung in Etappen ist in Ordnung; fehlende Bilder bleiben vorerst Emoji).

## Liste

### Kette 1 · Kaffee (Automat: Teekanne)
| Datei | Motiv (EN) | Name im Spiel |
|---|---|---|
| `g1_teekanne.png` | teapot (machine, a bit bigger and special) | Teekanne |
| `k1_s1_kaffeebohne.png` | coffee bean | Kaffeebohne |
| `k1_s2_espresso.png` | espresso cup | Espresso |
| `k1_s3_matcha.png` | matcha tea cup | Matcha |
| `k1_s4_bubbletea.png` | bubble tea with straw | Bubble Tea |
| `k1_s5_frappe.png` | frappé iced coffee drink | Frappé |
| `k1_s6_mocktail.png` | colorful mocktail glass | Mocktail |
| `k1_s7_barista_pokal.png` | golden barista trophy | Barista-Pokal |

### Kette 2 · Backwaren (Automat: Brotkorb)
| Datei | Motiv (EN) | Name im Spiel |
|---|---|---|
| `g2_brotkorb.png` | bread basket (machine, a bit bigger and special) | Brotkorb |
| `k2_s1_weizen.png` | wheat ears | Weizen |
| `k2_s2_brot.png` | loaf of bread | Brot |
| `k2_s3_croissant.png` | croissant | Croissant |
| `k2_s4_brezel.png` | pretzel | Brezel |
| `k2_s5_donut.png` | donut with sprinkles | Donut |
| `k2_s6_cupcake.png` | cupcake | Cupcake |
| `k2_s7_torte.png` | slice of cake | Torte |
| `k2_s8_festtorte.png` | festive party cake with candles | Festtorte |

### Kette 3 · Frühstück (Automat: Hühnerstall)
| Datei | Motiv (EN) | Name im Spiel |
|---|---|---|
| `g3_huehnerstall.png` | hen house with a hen (machine, a bit bigger and special) | Hühnerstall |
| `k3_s1_ei.png` | egg | Ei |
| `k3_s2_spiegelei.png` | fried egg in a pan | Spiegelei |
| `k3_s3_pancakes.png` | pancake stack with butter and syrup | Pancakes |
| `k3_s4_waffeln.png` | waffle | Waffeln |
| `k3_s5_sandwich.png` | sandwich | Sandwich |
| `k3_s6_salat.png` | fresh salad bowl | Salat |
| `k3_s7_brunchbox.png` | brunch box (bento style) | Brunch-Box |

Gesamt: 22 Teile + 3 Automaten = 25 Bilder.

## Was ich damit mache
Ansehen und Rückmeldung zu Stil/Lesbarkeit, Freistellen, Zuschneiden und Vereinheitlichen, Umwandeln in kleine WebP-Dateien, Einbau statt Emoji (Fallback auf Emoji, falls ein Bild fehlt), Glanz/Rand/Leuchten/Effekte im Code, danach Messung (Ruckeln, App-Größe), Veröffentlichung und neue APK.

## Hinweis
Prüfe in den Nutzungsbedingungen deines Tools, dass kommerzielle Nutzung erlaubt ist, und hebe Prompts/Belege auf (kein Rechtsrat).
