# Kunst-Briefing Noa's Bean Trail

**Stand 24.11. (v1.5.4): Alle 49 Bilder (22 Teile, 3 Automaten, 12 Figuren, 12 Gäste) sind im Spiel, dazu Brett-Rahmen und die Böden Hamburg, Wien, Paris, Rom (Wien, Paris, Rom vorläufig aus Entwürfen). Offen: Etappe 2 unten (Böden Istanbul, Kyoto, New York, Rio, Sternecafé, Wien/Paris/Rom im Hamburg-Stil, 12 Einzugs-Posen, Effekte).** Dieses Dokument bleibt die Vorlage für Neues (weitere Gäste und Figuren, Katze, Stadt-Hintergründe, Brett-Rahmen). Die Reihenfolge unten ist damit erledigt.

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

## Etappe 2 (24.11.): Brett-Rahmen, Böden, Einzugs-Posen, Effekte
**Status:** `frame.png` (Gold-Holz-Rahmen) und `f0_hamburg.png` sind eingebaut (v1.5.3) und sehen auf dem Handy gut aus; in v1.5.4 kamen Wien, Paris und Rom als vorläufige Böden dazu (siehe Böden). Alles Folgende ist optional, das Spiel hat für jedes Bild einen gebauten Ersatz.

### Brett-Rahmen (`frame.png`)
- Wie der erste Entwurf: quadratisch, **außen und im Fenster reines Magenta #FF00FF**, keine Schatten im Bild (den Schatten baut der Import).
- **Das Rahmenband bitte höchstens so dick wie im Entwurf (ca. 9–10 % der Bildbreite)**, lieber dünner: Im Spiel wird es auf 6,8 % der Brettbreite verkleinert, damit die Felder groß genug bleiben.
- Der Import formt das Quadrat auf das Brett (7×8) um: **Ecken bleiben unverändert, die glatten Mittelstücke werden gestreckt, die kleinen Mittelbeschläge bleiben unverzerrt.** Darum: Ecken mit Beschlag, dazwischen schlichtes Holz ohne Muster, das sich dehnen lässt.
- Der Rahmen gilt für alle Städte, solange keine eigenen geliefert sind; die Farbe des Bretts im Fenster kommt pro Stadt aus dem Spiel (Hamburg blau, Wien braun, Kyoto rosa …).
- **Eigener Rahmen je Stadt (`frame<N>_<name>.png`, N = Weltnummer wie bei den Böden):** `frame0_hamburg`, `frame1_wien`, `frame2_paris`, `frame3_rom`, `frame4_istanbul`, `frame5_kyoto`, `frame6_newyork`, `frame7_rio`, `frame8_sternecafe`. Gleiche Vorlage und gleiche Regeln wie `frame.png` (Form, Dicke, Eckbeschläge und Mittelbeschläge an denselben Stellen, dazwischen schlichtes Material, außen und im Fenster reines Magenta, kein Schatten, kein Text); nur Material und Look ändern. Ein gelieferter Rahmen gilt nur in seiner Welt, jede Welt ohne eigenen Rahmen behält `frame.png` (der Import baut jeden Rahmen auf das Brett um, das Spiel lädt ihn beim Weltwechsel und die nächste Welt im Leerlauf vor). Einzeln liefern geht.
- **Vorlage-Text für das Bild-Tool (`frame.png` als Referenz mitgeben):** „Gleicher Bilderrahmen wie die Referenz: gleiche Form, gleiche Rahmendicke, Eckbeschläge und kleine Mittelbeschläge an denselben Stellen, dazwischen schlichtes Material ohne Muster. Außen und im Fenster reines Magenta #FF00FF, kein Schatten, kein Text. Nur Material und Look ändern: <Material>.“ Material je Stadt: Wien dunkles Mahagoni mit Messingbeschlägen; Paris Schmiedeeisen im Art-Nouveau-Stil mit Silberbeschlägen; Rom heller Travertin-Marmor mit Goldbeschlägen; Istanbul blau-türkise Fliesen mit Goldbeschlägen; Kyoto schwarzer Lack mit roten Kanten und Bambusbeschlägen; New York gebürsteter Stahl mit Nieten; Rio tropisches Grün mit Gold; Sternecafé Mitternachtsblau mit Goldsternen. Zur Orientierung: Eine reine Umfärbung des Gold-Rahmens (Holz und Metall getrennt) sah in Wien (Mahagoni), Paris (Silber-Lavendel), Rom (Travertin), Istanbul (Kobalt), Kyoto (roter Lack), New York (Stahl) und Sternecafé (Nachtblau) brauchbar aus, wurde aber nicht eingebaut, weil der Eigentümer die Rahmen selbst liefert.

### Böden (`f<Stadt>_<name>.png`)
- Nummern: f0 Hamburg ✅, f1 Wien, f2 Paris, f3 Rom, f4 Istanbul, f5 Kyoto, f6 New York, f7 Rio, f8 Sternecafé. Quadratisch (1024×1024), deckend, gleiche Machart wie `f0_hamburg.png`.
- **Wo man den Boden sieht:** Er liegt unten bündig am Bildschirm, so breit wie der Schirm. Das Brett mit Rahmen deckt die Mitte (ca. 90 % der Breite). Sichtbar bleiben ein **Streifen links und rechts (ca. 5–8 %, auf kleinen Handys bis 15 % der Breite)**, ein schmaler Streifen oben unter der Szene und unten zwischen den Knöpfen. **Requisiten also an den Rändern und in den Ecken, die Mitte ruhig und leer** (wie bei Hamburg).
- Oberkante: darf eine Kante/ein Balken sein (Hamburg: Balken mit Eisenbändern), sie ist meist hinter dem Rahmen.
- Städte-Thema: Wien Kaffeehaus-Parkett/Karo mit Café-Requisiten, Paris Pflaster mit Bistro-Stühlen und Blumenkästen, Rom Terrakotta mit Zitronentöpfen, Istanbul Fliesen mit Teegläsern und Teppichkante, Kyoto Holzdielen/Tatami mit Steinlaterne und Kirschblüten, New York Asphalt/Gehweg mit Hydrant und Taxi-Kante, Rio Wellenpflaster mit Palmen und Surfbrett, Sternecafé dunkler Marmor mit Gold und Sternen.
- Ohne Bild bleibt der gebaute Boden aus der Szene (Planken, Kacheln, Licht, kleine Requisiten).
- **Ab 1.5.17 gibt es zusätzlich Vollbild-Hintergründe je Welt (Etappe 3, `b<N>`).** Sie ersetzen Szene und Boden zusammen und lösen den Stilbruch zwischen gezeichneter Szene und Bildern; wer sie liefert, braucht den Boden dieser Welt nicht mehr. Die Böden bleiben als Rückfall.
- **Die Nummer bestimmt die Stadt, nicht der Dateiname.** Genau diese neun Städte, nicht mehr und nicht weniger; ein Bild pro Nummer. Bitte nicht umsortieren oder andere Städte nehmen (die Spielwelten, Szenen und Texte hängen daran).
- **Lieferstand 24.11. (erste Entwurfsrunde, 8 Dateien):** `f1_berlin` ist das Vorbild für alle weiteren: gleiche Machart wie Hamburg, deckend, randlos, Requisiten nur an den Rändern, ruhige Mitte. Berlin ist aber keine Spielwelt, darum steht es **vorläufig als Boden von Wien** im Spiel (Berliner Bär am Poller übermalt). `f2_paris` und `f3_rom` passen zur Welt, sind aber hochskalierte Ausschnitte mit dunkel-blauem Rand, runden Ecken und Himmel/Skyline oben; sie sind mit `scripts/floor_prep.py` gesäubert und als Platzhalter eingebaut. `f4`…`f8` zeigen andere Städte als ihr Name (Park Güell/Barcelona, Lissabon, Athen, Amsterdam, Kopenhagen; Istanbul fehlt) und sind **nicht** eingebaut.
- **Bitte so (aus der Entwurfsrunde gelernt):** quadratisch 1024×1024 in echter Auflösung (nicht hochskaliert); **kein** Himmel, keine Skyline, kein Horizont, keine Gebäude; **keine** dunklen Ränder oder runden Ecken, das Bild läuft bis an alle vier Kanten; keine Menschen, kein Text, keine zweite Szene im Bild; Mitte ruhig und gleichmäßig, Requisiten nur an den Rändern.
- **Vorlage-Text für das Bild-Tool (Stadt und Requisiten einsetzen):** „Bodenfläche einer Café-Terrasse in <Stadt>, Blick von oben leicht schräg von vorn, Candy-Cartoon-Stil wie f1_berlin, kräftige weiche Farben, quadratisch, randlos bis an alle Kanten, Mitte ruhiger gleichmäßiger Boden, Requisiten nur am linken und rechten Rand und in den unteren Ecken: <Requisiten>. Kein Himmel, kein Horizont, keine Gebäude, keine Menschen, kein Text, keine dunklen Ränder, keine runden Ecken.“ Requisiten je Welt: Wien Schachbrett-Parkett, Thonet-Stühle, Marmortisch mit Melange und Sachertorte; Istanbul türkis-weiße Fliesen mit Teppichkante, Teegläser auf Messingtablett, Kupferkanne, Mosaiklampe; Kyoto Holzdielen mit Tatami-Kante, Steinlaterne, Kirschblütenblätter, Teeschale; New York Gehwegplatten, Hydrant, Gullydeckel mit Dampf, Zeitungsständer; Rio Wellenpflaster schwarz-weiß, Palme, Surfbrett, Kokosnuss; Sternecafé dunkler Marmor mit Goldadern, Sterne-Intarsien, goldene Kerzenständer.
- **Weicher Auslauf oben ist erlaubt:** Hat die Datei Transparenz (z. B. oben 6–13 % auslaufend), behält der Import sie, und der gebaute Boden der Szene scheint durch. Das verdeckt harte Schnittkanten an den Rändern.

### Einzugs-Posen (`e1_baristina.png` … `e12_robo.png`)
- Beim Einzug nach der Wahl der Figur läuft/rollt/fliegt die Figur groß ins Bild (andere Bewegung je Figur, schon im Spiel). Heute ist das noch die Kachel; mit Pose kommt die **ganze Figur** (Beine, Rollschuhe, Flügel).
- **Hochformat 2:3 (z. B. 1024×1536), Ganzkörper in der Pose, Hintergrund Magenta #FF00FF, kein Boden, kein Schatten.** Figur und Stil exakt wie das Kachel-Bild (Kachel-Bild als Referenz mitgeben), Figur ca. 70 % der Bildhöhe, die Unterseite (Füße, Rollschuhe, Schubdüsen) komplett sichtbar. Die Bewegung macht das Spiel, das Bild zeigt nur die Haltung.
- Posen: 1 Baristina auf rosa Rollschuhen im Gleiten, Arme leicht seitlich · 2 Ben im Sprint · 3 Felix im Sprung · 4 Bruno stampfend, Brust raus · 5 Mimi im Sprung auf Pfoten · 6 Pina zusammengerollt wie ein Ball · 7 Luna im Galopp, Regenbogenmähne weht · 8 Drago im Flug, Flügel offen · 9 Otto auf dem Rücken liegend wie auf einer Welle · 10 Rocky halb versteckt, schaut vorsichtig · 11 Pablo auf dem Bauch rutschend · 12 Robo schwebend mit Schubdüsen.

### Effekte (`fx_puff.png`, `fx_star.png`, `fx_drop.png`, `fx_flame.png`, `fx_leaf.png`, `fx_ring.png`, `fx_glow.png`, `fx_excl.png`)
- Kleine Sprites für den Einzug (Staubwolke, Stern, Tropfen, Flamme, Blatt, Ring, Leuchten, „!“). Je 256×256, Hintergrund Magenta, im selben Stil. Optional; ohne Bild zeichnet das Spiel sie selbst.

## Etappe 3 (24.11., v1.5.17): Vollbild-Hintergründe je Welt (`b<N>_<stadt>.png`)
**Warum:** Die gezeichnete Szene oben (Skyline, Wahrzeichen) passt nicht mehr zu den Bildern von Brett, Rahmen und Boden, und vom Boden sieht man am Rand nur Bruchstücke (Rückmeldung des Eigentümers zu Paris, 24.11.). Ein Bild je Welt, das Himmel, Wahrzeichen und Boden **zusammen** malt, löst beides. Es ersetzt Szene **und** Boden dieser Welt; fehlt es, bleibt alles wie bisher. Der Platz im Spiel ist seit 1.5.17 eingebaut (Datei `b<N>.webp`, Import mit `art_import.py`); Bilder fehlen noch. Wer ein Bild für eine Welt liefert, braucht für sie keinen Boden mehr.

- **Nummern wie bei den Böden:** b0 Hamburg, b1 Wien, b2 Paris, b3 Rom, b4 Istanbul, b5 Kyoto, b6 New York, b7 Rio, b8 Sternecafé. Die Nummer bestimmt die Stadt, nicht der Dateiname. Lieferung in Etappen ist in Ordnung (zuerst Paris und Wien, die der Eigentümer gerade spielt).
- **Format:** Hochformat **1080×2340 (9:19,5)**, mindestens 1:1,4, deckend, randlos bis an alle Kanten, keine runden Ecken, kein Text, keine Menschen, keine Oberfläche (keine Knöpfe, kein Brett). Der Import verkleinert auf 720 px Breite und speichert als WebP.
- **Aufteilung von oben nach unten** (Prozent der Bildhöhe; das Spiel legt das Bild oben bündig auf den ganzen Schirm, Maße für ein Handy 390×844):
  - **0–12 %** Himmel, darüber liegt die Kopfleiste: ruhig, wenig Detail.
  - **12–28 %** liegt hinter dem Bestell-Tresen und ist **verdeckt**: Himmel oder Spitze des Wahrzeichens, darf weitergehen, wird nicht gesehen.
  - **28–41 % = das Fenster zur Stadt.** Nur dieser Streifen zwischen Tresen und Brett zeigt die Stadt: **Wahrzeichen und Häuserzeile in voller Pracht**, Wahrzeichen rechts oder mittig, damit es auch mit verdeckter Spitze erkennbar bleibt (Paris: Mittelteil und Bogen des Eiffelturms).
  - **41–88 %** liegt hinter dem Brett und ist **verdeckt**: ruhiger, gleichmäßiger Boden (Pflaster, Planken, Fliesen), wenig Kontrast und keine Motive, damit das Brett nicht unruhig wirkt.
  - **Ränder links und rechts (je ca. 8 % der Breite) und unten (88–100 %, zwischen Brett und Knöpfen):** hier die **Requisiten** der Stadt, wie bei den Böden.
- **Stil:** wie Rahmen und Böden: Candy-Cartoon, kräftige weiche Farben, Licht von oben links, **keine dunkle Vignette** und keine dunklen Ränder. Als Stil-Referenz `frame.png` und `f0_hamburg.png` mitgeben.
- **Vorlage-Text für das Bild-Tool (Stadt, Wahrzeichen, Boden und Requisiten einsetzen):** „Vertikaler Hintergrund für ein Handyspiel, Hochformat 9:19,5, glänzender 3D-Candy-Cartoon-Stil wie die Referenzbilder, kräftige weiche Farben, Licht von oben links, keine dunkle Vignette. Straßencafé-Szene in <Stadt>. Aufbau von oben nach unten: oberste 12 % ruhiger Himmel; zwischen 28 % und 41 % der Höhe eine breite Reihe aus <Wahrzeichen und Häuserzeile>, das Wahrzeichen gut erkennbar; von 41 % bis 88 % eine ruhige, gleichmäßig beleuchtete <Boden> fast ohne Details und Kontrast (ein Spielbrett deckt sie ab); Requisiten nur am linken und rechten Rand und am unteren Rand: <Requisiten>. Keine Menschen, kein Text, keine Oberfläche, kein Rahmen, keine runden Ecken, randlos bis an alle Kanten.“
- **Je Welt:**
  - 0 Hamburg: Speicherstadt-Backsteinhäuser mit Giebeln, Elbphilharmonie, Hafenkräne und Schiffsmasten · Boden Holzplanken · Requisiten Tonnen, Taue, Rettungsring, Laterne, Fischkisten (wie `f0_hamburg`)
  - 1 Wien: Riesenrad, Turm des Stephansdoms, Jugendstil-Fassaden · Boden Kopfsteinpflaster · Requisiten Kaffeehausstühle und -tische, Straßenlaterne, Blumenkübel
  - 2 Paris: Eiffelturm, Häuserzeile mit Balkonen und Mansarddächern, grün-weiße Bistro-Markise · Boden Pflaster · Requisiten Bistrotische und -stühle, Blumenkästen, Kreidetafel, Fahrrad
  - 3 Rom: Kolosseum, Zypressen, Terrakotta-Dächer · Boden helle Steinplatten · Requisiten Säulen, Zitronentöpfe, Amphore
  - 4 Istanbul: Moschee mit Kuppel und Minaretten, Galataturm, Möwen · Boden Fliesen · Requisiten Teegläser auf Tablett, Teppichkante, Laternen
  - 5 Kyoto: fünfstöckige Pagode, rotes Torii, Kirschblüten · Boden Holzdielen oder Tatami · Requisiten Steinlaterne, Bambus, Teekanne
  - 6 New York: Wolkenkratzer-Skyline, Brooklyn-Brücke, gelbes Taxi · Boden Gehweg · Requisiten Hydrant, Feuerleiter, Pappbecher
  - 7 Rio: Zuckerhutberg, Christusstatue, Strand und Palmen · Boden Wellenpflaster · Requisiten Palmen, Surfbrett, Kokosnüsse
  - 8 Sternecafé: Nachthimmel mit Mond und Sternen über Café-Dächern, Gold · Boden dunkler Marmor mit Goldadern · Requisiten Goldsterne, Laternen
- **Prüfen:** Das Bild auf 390×844 verkleinern und den Streifen 28–41 % ansehen: Man muss die Stadt noch erkennen. Die Mitte (41–88 %) darf nichts Auffälliges zeigen.
- **Import:** `python3 -I scripts/art_import.py <ZIP-oder-Ordner>` (Dateien `b2_paris.png` usw.); der Import trägt `b2` ins Manifest ein, danach Version erhöhen und testen. Vor der Veröffentlichung Tool, Datum und Nutzungsbedingungen je Bild festhalten (Asset-Verzeichnis).

## Katze Mocha: Ruhebilder austauschen (Stand 1.5.17)
- **Entscheidung 24.11. (Rückmeldung des Eigentümers):** Kein Sprung aufs Brett und kein Streicheln mehr. Mocha blieb auf dem Handy nach dem Streicheln auf dem Brett stehen, und 22 Bilder samt Schnurr-Ton kosteten Arbeitsspeicher. Sie sitzt jetzt klein oben rechts im Bestellbereich (vier Ruhe-Frames im Kreis aus drei Bildern), Antippen: Miau und ein kurzer Hinweis.
- Bilder: `www/art/cat/c01` bis `c03.webp`. Die übrigen Frames, die Herzen und `purr.wav` sind entfernt.
- **Austausch:** neue Ruhe-Frames (Zustand IDLE, gleiche Katze, gleiche Standlinie, Hintergrund Magenta #FF00FF oder echte Transparenz) in ein Paket wie bisher legen (`sprites/cat_01_idle.png` … plus `docs/animation_manifest.json` mit dem Zustand IDLE), dann `python3 -I scripts/cat_import.py <ZIP-oder-Ordner>`. Das Skript schneidet zu (320 px breit, WebP), entfernt doppelte Frames und trägt die Tabelle `CAT` in `www/index.html` ein. Danach Version erhöhen und testen.
- **Rechte:** Der Eigentümer vermerkt zur Herkunft der Bilder, dass sie aus der bisherigen Projektarbeit stammen. Vor der Veröffentlichung Tool, Datum und Nutzungsbedingungen je Bild festhalten (siehe Asset-Verzeichnis).

## Was ich damit mache
Ansehen und Rückmeldung zu Stil/Lesbarkeit, Freistellen, Zuschneiden und Vereinheitlichen, Umwandeln in kleine WebP-Dateien, Einbau statt Emoji (Fallback auf Emoji, falls ein Bild fehlt), Glanz/Rand/Leuchten/Effekte im Code, danach Messung (Ruckeln, App-Größe), Veröffentlichung und neue APK.

## Hinweis
Prüfe in den Nutzungsbedingungen deines Tools, dass kommerzielle Nutzung erlaubt ist, und hebe Prompts/Belege auf (kein Rechtsrat).
