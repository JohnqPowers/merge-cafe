# Kunst-Briefing Merge Café

**Stand 24.11. (v1.5.2): Alle 49 Bilder (22 Teile, 3 Automaten, 12 Figuren, 12 Gäste) sind geliefert und im Spiel.** Dieses Dokument bleibt die Vorlage für Neues (weitere Gäste und Figuren, Katze, Stadt-Hintergründe, Brett-Rahmen). Die Reihenfolge unten ist damit erledigt.

Ziel: Die 22 Teile und 3 Automaten, die heute noch Emoji sind, sowie die **Spielerfiguren und Café-Gäste** durch eigene Bilder im Candy-Look ersetzen. Reihenfolge der Wichtigkeit (Stand 24.11.): **1. Teile Kette 1, 2. Gäste (12), 3. Spielerfiguren (12), 4. Kette 2 und 3**, danach Brett-Rahmen, Stadt-Hintergründe, Katze/Logo.

## Entscheidung 23.11.: Teile stehen frei, ohne Platte („Variante B“)
- Die Teile stehen direkt auf dem dunkelvioletten Brett, es gibt keine Platte mehr (nur die Automaten behalten ihre goldene Platte). Darum: **Körper hell und satt**, keine großen schwarzen oder sehr dunklen Flächen; die dunklere Kontur bleibt.
- **Hintergrund transparent** (wie bei der Kaffeebohne). Kann dein Tool das nicht: einfarbig Magenta #FF00FF, bei rosa/magentafarbenen Motiven (Bubble Tea, Mocktail) stattdessen reines Grün #00FF00.
- Rand um das Motiv ca. 8–12 % (die Bohne hat ca. 11 %, das passt).
- ~~Etappe 1: nur Kette 1~~ (erledigt, alle Ketten und Automaten sind im Spiel). Neue Bilder weiter als ZIP schicken, ich prüfe sie als Reihe im Testbrett.
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

Teile gesamt: 22 Teile + 3 Automaten = 25 Bilder.

## Figuren und Gäste (neu, 24.11.)
Die Spielerfiguren (Auswahl am Anfang, Profilbild oben links) und die Café-Gäste am Tresen wirken heute zu gleichförmig. Mit eigenen Bildern bekommt jeder Gast und jede Figur ein Gesicht. **Auch einzelne Bilder helfen**: Das Spiel nimmt, was da ist, und zeichnet den Rest selbst.

Stil, Regeln, Hintergrund (transparent oder Magenta #FF00FF; bei rosa/pinken Motiven Grün #00FF00), Dateiformat und Vorgehen sind **wie bei den Teilen** (Kaffeebohne als Stil-Referenz, alle Bilder wie von einer Hand). Zusätzlich:
- **Gesicht groß und freundlich**, große Augen, lächelnd; Gäste dürfen „hungrig/neugierig“ schauen.
- **Klare Silhouette durch ein Erkennungsmerkmal** (Hut, Haar, Brille, Bart, Schal, Tier-Ohren). Gezeigt wird nur ca. 60 px hoch.
- Frontal, ohne Hände im Bild, ohne Text, ohne Schatten im Bild.
- Helle, satte Farben (das Café ist hell, aber der Hintergrund der Figuren-Kachel ist farbig).

### Spielerfiguren (12)
Bildausschnitt: **Kopf und Schultern**, füllt das Bild, rund zuschneidbar. Jede Figur trägt etwas „Café“ (Kochmütze, Schürze, Fliege …). Dateiname `a<Nr>_<name>.png`, quadratisch, mind. 512×512.

Prompt-Vorlage (Englisch):
```
glossy 3D cartoon game avatar, head and shoulders portrait of {MOTIV}, candy-like gummy look,
thick soft outline, saturated vivid colors, big white specular highlight top-left, big friendly
eyes, smiling, front view, isolated on plain solid magenta (#FF00FF) background, no text,
no cast shadow, mobile game character asset
```

| Datei | Motiv (EN) | Name im Spiel |
|---|---|---|
| `a1_baristina.png` | young woman barista with small white chef hat, curly brown hair | Baristina |
| `a2_barista_ben.png` | young man barista with chef hat and apron, dark skin, short beard | Barista Ben |
| `a3_fuchs_felix.png` | orange fox wearing a chef hat | Fuchs Felix |
| `a4_baer_bruno.png` | brown bear with apron and wooden spoon | Bär Bruno |
| `a5_katze_mimi.png` | ginger cat with bow tie and barista apron | Katze Mimi |
| `a6_panda_pina.png` | panda holding a bamboo cup | Panda Pina |
| `a7_einhorn_luna.png` | unicorn with rainbow mane and tiny chef hat (use green background) | Einhorn Luna |
| `a8_drache_drago.png` | little green dragon holding an espresso cup | Drache Drago |
| `a9_otter_otto.png` | otter with a milk foam moustache | Otter Otto |
| `a10_waschbaer_rocky.png` | raccoon with coffee bean sack | Waschbär Rocky |
| `a11_pinguin_pablo.png` | penguin waiter with bow tie | Pinguin Pablo |
| `a12_robo_barista.png` | cute robot barista with chef hat | Robo-Barista |

### Gäste (12)
Bildausschnitt: **Halbfigur bis zur Hüfte** (unten darf der Körper einfach abgeschnitten sein, der Tresen verdeckt ihn), hochkant (z. B. 3:4), mind. 768 px hoch. Dateiname `c<Nr>_<name>.png`. Thema ist Hamburg/Hafen.

Prompt-Vorlage (Englisch):
```
glossy 3D cartoon game character, half-body (waist up) of {MOTIV}, standing, looking at the viewer,
friendly hungry expression, candy-like gummy look, thick soft outline, saturated vivid colors,
big white specular highlight top-left, front view, isolated on plain solid green (#00FF00) background,
no text, no cast shadow, mobile game character asset
```

| Datei | Motiv (EN) | Name im Spiel |
|---|---|---|
| `c1_kapitaen_hein.png` | sea captain with white beard and captain cap | Käpt'n Hein |
| `c2_hafenarbeiterin_jule.png` | dock worker woman, yellow hard hat, orange hi-vis vest | Hafenarbeiterin Jule |
| `c3_touristin_tina.png` | tourist woman with big sun hat, camera around neck, Hawaiian shirt | Touristin Tina |
| `c4_oma_hilde.png` | grandma with grey bun, round glasses, knitted cardigan | Oma Hilde |
| `c5_matrose_jan.png` | sailor with sailor cap and blue-white striped shirt | Matrose Jan |
| `c6_musikerin_mara.png` | musician with curly hair holding a violin | Musikerin Mara |
| `c7_punk_ronja.png` | punk girl with colorful mohawk and studded jacket | Punk Ronja |
| `c8_geschaeftsmann_max.png` | business man in suit and tie with briefcase | Geschäftsmann Max |
| `c9_student_leo.png` | student with beanie, big beard, headphones | Student Leo |
| `c10_moewe_molly.png` | seagull wearing sunglasses and a sailor scarf | Möwe Molly |
| `c11_fischverkaeufer_knut.png` | fish seller with yellow sou'wester hat, big moustache, apron | Fischverkäufer Knut |
| `c12_malerin_frida.png` | painter with beret, paint splashes, brush behind ear | Malerin Frida |

Ab 6 Gast-Bildern zeigt das Spiel nur noch Bild-Gäste (einheitlicher Look), vorher mischt es sie mit den gezeichneten Gästen (20 Typen mit eigener Kleidung, `ROLE` in `www/index.html`). Bei den Figuren erscheinen die Bild-Figuren zuerst in der Auswahl.

Was das Importskript aus den gelieferten Figuren und Gästen macht: **Figuren** sind Kacheln mit Hintergrundfarbe und abgerundeten Ecken, die Kochmütze darf oben herausragen. Das Skript erkennt die Kachel, rundet alle vier Ecken gleich (die Vorlagen sind teils seitlich angeschnitten) und bringt alle Kacheln auf dieselbe Größe (208×208 mit Platz für die Mütze). **Gäste** behalten den gezeichneten Ausschnitt (240×270, Unterkante bündig, der Tresen deckt sie ab).

Gesamt: 22 Teile + 3 Automaten + 12 Figuren + 12 Gäste = 49 Bilder.

## Was ich damit mache
Ansehen und Rückmeldung zu Stil/Lesbarkeit, Freistellen, Zuschneiden und Vereinheitlichen, Umwandeln in kleine WebP-Dateien, Einbau statt Emoji (Fallback auf Emoji, falls ein Bild fehlt), Glanz/Rand/Leuchten/Effekte im Code, danach Messung (Ruckeln, App-Größe), Veröffentlichung und neue APK.

## Hinweis
Prüfe in den Nutzungsbedingungen deines Tools, dass kommerzielle Nutzung erlaubt ist, und hebe Prompts/Belege auf (kein Rechtsrat).
