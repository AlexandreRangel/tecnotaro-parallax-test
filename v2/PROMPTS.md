# Tecno Tarot Parallax 2: prompts por carta e camada

Gerador: GenerateImage do Grok Bot (cerca de 1024x576). Processo: `proc.py SRC NN-slug camada modo [frac]`, depois `fin.py NN-slug` (abre o rosto na camada de energia) e `comp.py NN-slug` (gera a prévia em qa/). A publicação é feita com `publish_batch.sh NN`.
Regras gerais: figura com 85 a 95% da altura e proporção adulta real; energia saindo dos objetos, nunca sobre o rosto; mid em fundo verde #00FF00, fg em fundo preto #000000.

## 00 O Louco
- figure (modo fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. A mature weathered traveler (the Fool tarot card), grey beard, blue hooded jester coat with brass gear ornaments, holding a tall brass staff with a glowing cyan orb, an amber lantern at his hip, boots, standing on a small patch of cobblestones. Realistic adult body proportions, about 7.5 heads tall, long legs, head not oversized. Beside his boots a small fluffy shih tzu dog with a little brass collar, looking up at him. Highly detailed face, cyberpunk steampunk illustration, bright neon magenta cyan amber rim light. Figure fills the full height of the image, centered.
- fg (modo r): Pure solid black #000000 background, no people. Abundant large glowing foreground energy: thick neon magenta and cyan plasma ribbons, amber sparks and floating light motes surging up both left and right sides and across the bottom, big swirls curling toward the viewer, a few large out-of-focus brass gears and neon butterflies in the corners. Only a central oval area in the upper middle (where a face would be) stays black and empty. Luminous cyberpunk steampunk tarot style.
- bg e mid: versões anteriores mantidas (os prompts não foram registrados).

(Novas cartas entram aqui conforme forem geradas.)

## 01 O Mago
- figure (fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Magician tarot card: a mature charismatic man of Middle Eastern descent, short dark beard with grey, wide brimmed brass-trimmed hat, crimson and black long coat with brass gears and cables, right hand raising a brass wand with a glowing cyan crystal tip, left hand pointing down. Realistic adult proportions about 7.5 heads tall, head not oversized, highly detailed expressive face with a knowing smile. Cyberpunk steampunk illustration, bright neon magenta cyan amber rim light. Figure fills the full height of the image, centered.
- mid (center): On a flat pure chroma green #00FF00 background, nothing else: a single wide ornate brass and dark wood alchemist table seen from the front, occupying the bottom third of the image, on it a glowing golden cup, a short sword, a brass pentacle disc and a small staff, neon cyan and magenta glints. No people, no shelves, nothing above the table. Cyberpunk steampunk illustration.
- fg (top): Pure solid black #000000 background, no people, no objects. Vertical composition. In the upper left corner a brilliant cyan-white starburst (the tip of a magic wand), from it huge thick spiraling ribbons of glowing cyan, magenta and amber plasma rush forward toward the viewer and pour down the whole left side and sweep across the entire bottom of the image, dense sparks, glowing infinity symbols and lightning arcs. The right upper half and the center stay empty black. Very bright, luminous, cyberpunk steampunk tarot style.
- bg: versão anterior mantida.

## 02 A Sacerdotisa
- figure (fig 0.9): Full body seated-on-throne figure on a flat pure chroma green #00FF00 background, nothing else in the background. The High Priestess tarot card: a serene mature woman of Persian descent in her forties, deep blue and silver hooded robe with brass filigree, a glowing crescent moon crown, holding an open glowing book (scroll of TORA) on her lap that emits soft cyan light, sitting on a simple brass throne. Realistic adult proportions, head not oversized, highly detailed calm wise face. Cyberpunk steampunk illustration, bright neon cyan magenta amber rim light. Figure fills the full height of the image, centered.
- mid (top): On a flat pure chroma green #00FF00 background, nothing else: two tall ancient stepped temple pyramids with glowing neon cyan and magenta edges and brass details, one on the far left and one on the far right edge, symmetrical, like temple pillars, and a low veil of glowing pomegranate pattern cloth hanging between them at the bottom. No people, no chimneys, no pipes, center empty green.
- fg (center): Pure solid black #000000 background, no people. Abundant glowing cyan and silver energy streams with floating luminous glyphs, letters of light and pages rising from the lower center and spiraling outward toward the viewer along both sides and across the bottom, magenta moon crescents and amber sparks. The upper center stays empty black. Luminous cyberpunk mystical tarot style.

## 03 A Imperatriz
- figure (fig 0.88): Seated figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Empress tarot card: a radiant mature Afro-Brazilian woman in her forties, warm smile, a simple elegant brass crown with twelve small glowing stars, flowing emerald and magenta gown with a few brass details, holding a brass scepter topped with a glowing orb, a heart-shaped brass shield with a Venus symbol beside her, seated on a simple throne. Clean and elegant, not busy. Realistic adult proportions, head not oversized, highly detailed expressive face. Cyberpunk steampunk illustration, bright neon rim light. Figure fills the full height of the image, centered.
- bg (crop): fundo anterior mantido (asset b3885291).
- mid: vazio (de propósito, para limpar a carta).
- fg (bottom): Pure solid black #000000 background, no people. Glowing foreground energy of fertility and nature: luminous emerald and magenta vines, glowing wheat stalks, neon flower petals and golden pollen sparks swirling up from the bottom and along the left and right edges toward the viewer, a few small glowing stars. The upper center stays empty black. Luminous cyberpunk steampunk tarot style.

## 04 O Imperador
- figure (fig 0.88): Seated figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Emperor tarot card: a powerful mature man of Indigenous South American descent in his fifties, grey streaked long hair and short beard, stern but kind face, a clean brass crown, dark red and brass armored robe, simple design not busy, holding a brass scepter with an ankh top glowing amber, seated on a stone and brass throne with ram head ornaments. Realistic adult proportions, head not oversized, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Figure fills the full height of the image, centered.
- bg (crop): fundo anterior mantido (asset c01afe7c).
- mid: vazio.
- fg (center): Pure solid black #000000 background, no people. Glowing foreground energy of power: from the upper left a golden ankh-shaped light flare, thick amber and crimson plasma streams with fiery sparks and floating geometric brass sigils pour down the left side and sweep across the bottom toward the viewer, cyan electric arcs. The upper center and right stay empty black. Luminous cyberpunk steampunk tarot style.

## 06 Os Enamorados
- figure (fig 0.9): Full body standing figures on a flat pure chroma green #00FF00 background, nothing else in the background. The Lovers tarot card: three mature adults standing close together, a smiling Latin man in his forties in the center, a Black woman and a Middle Eastern woman leaning close to his face on each side, elegant cyberpunk steampunk gowns and coat with brass filigree in violet, teal and gold. Realistic adult proportions, head not oversized, highly detailed expressive faces. Cyberpunk steampunk illustration, bright neon rim light. Feet at the bottom of the image, centered. (asset afffacd2)
- bg (r): steampunk city towers with a radiant sun in a magenta and cyan sky (asset 4a173df1).
- mid (split): brass lanterns and fairy lights at the top, golden balustrade with glowing hearts and roses at the bottom, on green #00FF00 (asset aa4c29a9).
- fg (bottom): Pure solid black #000000 background, no people. Pink and gold silk ribbons of light with rose petals sweeping in from the left and right edges, center empty black (asset 29de50cb).

## 07 O Carro
- figure (fig 0.9): Full body figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Chariot tarot card: a confident mature woman in brass and black armor standing in an ornate steampunk chariot, holding a glowing magenta staff, the chariot pulled by two seated robot cats, one dark bronze and one silver, neon cyan and magenta lights. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset b8743faf)
- bg (crop): night steampunk avenue of towers with neon reflections on wet stone (asset 375f7e6d).
- mid: vazio.
- fg (bottom): Pure solid black #000000 background, no people. Magenta, cyan and amber speed streaks of energy and sparks rushing along the bottom toward the viewer, upper area empty black (asset e22fde89).

## 08 A Justiça
- figure (fig 0.9): Seated figure on a flat pure chroma green #00FF00 background, nothing else in the background. Justice tarot card: a stern but fair mature man with short dark hair and a trimmed beard, crimson and black velvet robe with brass filigree, holding a glowing cyan sword upright in one hand and brass scales in the other, seated on an ornate brass throne with a gear motif. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset c25db402)
- bg (crop): grand steampunk hall of justice with brass columns, cyan lights and a round window onto a night city (asset cb6e9433).
- mid: vazio.
- fg (bottom): Pure solid black #000000 background, no people. Sharp cyan and amber crystal blades of light rising from the bottom corners toward the viewer, center empty black (asset d0a8fd97).

## 09 O Eremita
- figure (fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Hermit tarot card: an old wise man with a long white beard in a hooded tattered grey cloak with brass gear details, raising a glowing brass lantern with a six-pointed star inside, holding a tall brass staff. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset 2c216a5f)
- bg (crop): snowy mountain peak under aurora lights with a steampunk observatory and a glowing city below (asset f75a3bae).
- mid: vazio.
- fg (bottom): Pure solid black #000000 background, no people. Drifting cyan and gold bokeh sparks and snow of light rising along the bottom and sides, upper center empty black (asset ff036286).

## 10 A Roda da Fortuna
- figure (fig 0.85, KEY_STRICT=1): Object on a flat pure chroma green #00FF00 background, nothing else in the background. Wheel of Fortune tarot card: a large ornate brass wheel of gears and spokes with neon cyan and magenta rings and glowing alchemical symbols, a golden sphinx seated on top, a glowing golden serpent coiling on the right side, on a brass pedestal. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset bfdcd376)
- bg (crop): cosmic sky with constellation figures of the eagle, lion, bull and angel around a floating steampunk city (asset 54f3ce8b).
- mid: vazio.
- fg (center): Pure solid black #000000 background, no people. Concentric rings of magenta, cyan and gold light with small brass gears orbiting, center open (asset 6f2b4156).

## 11 A Força
- figure (fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. Strength tarot card: a serene mature woman with long dark hair in a flowing white and gold gown, a glowing infinity symbol above her head, gently resting her hand on a large seated brass mechanical lion. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset 05c27c6f)
- bg (crop): sunset steampunk garden palace with glass domes and flowering arches (asset 7708343b).
- mid: vazio.
- fg (bottom): Pure solid black #000000 background, no people. Amber and magenta petals and sparks curving along the bottom with a glowing golden infinity ribbon, upper area empty black (asset 153e35fa).

## 12 O Enforcado
- figure (fig 0.9, FIG_ANCHOR=top, KEY_STRICT=1, fin FIN_HEAD=bottom): Full body figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Hanged Man tarot card: a calm man with a long dark beard hanging upside down by one foot from a brass pipe beam at the top of the image, the other leg crossed, dark leather steampunk suit with cyan lights, a glowing golden halo ring around his head. Realistic adult proportions, highly detailed serene face. Cyberpunk steampunk illustration, bright neon rim light. Beam at the top edge, centered. (asset 58256c50)
- bg (crop): misty forest of giant brass pipe trees with glowing teal canopies and sunlight (asset 2f45669b).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (top): Pure solid black #000000 background, no people. Golden and cyan leaves of light and falling sparks, center empty black (asset df07b265).

## 13 A Morte
- figure (fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. Death tarot card: an armored skeletal knight in black and brass plate armor holding a scythe with a glowing magenta blade and a black banner with a white rose. Cyberpunk steampunk illustration, bright neon rim light. Centered. (asset 57bf92e6)
- bg (crop): river at sunrise between tall spired towers and glowing gardens, a new dawn (asset bb71d5a4).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. A swirling ring of magenta and violet petals and energy shards, open center (asset 18405a3a).

## 14 A Temperança
- figure (fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. Temperance tarot card: a serene Black woman angel with an updo, white and gold robe, very wide brass mechanical wings with cyan light, pouring a glowing cyan stream of water between two hands, one foot on a rock and one in water at the bottom. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Feet in water at the bottom, centered. (asset 622d17e7)
- bg (crop): calm mountain lake at sunrise with a radiant sun, a path and purple irises (asset a5f2a7c6).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): Pure solid black #000000 background, no people. A cyan wave of light from the left meeting a golden wave from the right over reflective water, center empty (asset 61759077).

Nota: a partir de 12/10 o fin.py gera fg_final mais forte (sem 10% de transparência global, corpo atenuado 15%, brilho e saturação 1.3x) e uma aura do fg atrás da figura, gravada em mid.png sobre mid_base.png.

## 15 O Diabo
- figure (fig 0.9, KEY_STRICT=1): Full body figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Devil tarot card: a horned armored devil with wide bat wings seated on a brass throne under a glowing inverted pentagram, two chained horned figures, a man and a woman, kneeling at his sides. Cyberpunk steampunk illustration, bright neon rim light. Centered, wide. (asset 5b5e0680)
- bg (crop): infernal steampunk foundry with red furnaces, pipes and pink smoke (asset ca253040).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Crimson, orange and magenta flames framing the edges, center empty (asset cff646ac).

## 16 A Torre
- figure (fig 0.9, KEY_STRICT=1): Object on a flat pure chroma green #00FF00 background, nothing else in the background. The Tower tarot card: a tall ornate brass and copper steampunk tower struck by violet lightning, its top exploding in fire and debris, two small figures falling. Base cropped at the bottom edge. Cyberpunk steampunk illustration, bright neon rim light. (asset f13c8bb8)
- bg (crop): violet and cyan lightning storm over a night megacity (asset 0730cd1b).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Cyan lightning bolts and orange sparks around the edges, center empty (asset b41d635a).

## 17 A Estrela
- figure (fig 0.9, KEY_STRICT=1): Figure on a flat pure chroma green #00FF00 background, nothing else in the background. The Star tarot card: a graceful mature woman with silver hair and a jeweled headpiece in a pale blue and gold gown, kneeling in a glowing pool, pouring glowing cyan water from two brass jugs. Realistic adult proportions, highly detailed face. Cyberpunk steampunk illustration, bright neon rim light. Pool at the bottom, centered. (asset 0b4c5dfd)
- bg (crop): violet night with a great eight-pointed star over a reflective lake, a city and a golden tree with a bird (asset 06528bfd).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Swirling cyan water and light splashes framing the sides, center empty (asset 2fa0e010).

Nota (12/10, tarde): look.py gera figure.png a partir de figure_key.png (neon semitransparente com bloom, rim light colorido pelo bg esquerdo/direito, grade de 12% para os tons do bg). finish.sh NN-slug roda look.py, fin.py e comp.py com as opções por carta (12: FIN_HEAD=bottom, FG_EXTEND=1300; 13: BLOOM=60, WATER=1, FG_DIFFUSE=50).

## 18 A Lua
- figure (fig 0.9, KEY_STRICT=1, FIG_ANCHOR=base, look RECOLOR_GREEN=1): Object group on a flat pure chroma green #00FF00 background, nothing else in the background. The Moon tarot card: two ornate brass steampunk towers, a mechanical wolf howling and a mechanical dog between them, a brass crayfish emerging from a glowing pool at the bottom. Cyberpunk steampunk illustration, neon rim light. Base flush with the bottom edge. (asset d7a5f83d) Nota: o lago e as luzes verdes da fonte conflitam com o chroma; o key estrito remove o verde de fundo e o look.py recolore os brilhos verdes restantes para ciano.
- bg (crop): great pale moon with a serene face radiating light over misty violet mountains (asset 7497d153).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Silver and violet mist with falling dew drops framing the edges, center empty (asset 033150fa).

## 19 O Sol
- figure (fig 0.9): Full body figures on a flat pure chroma green #00FF00 background, nothing else in the background. The Sun tarot card: a joyful Black man in a cream linen steampunk outfit and a joyful Latin woman in a flowing cream dress dancing barefoot hand in hand, laughing. Realistic adult proportions, highly detailed faces. Cyberpunk steampunk illustration, warm rim light. Feet at the bottom, centered. (asset 25c946d7)
- bg (crop): golden mechanical sun over a garden wall of sunflowers and neon (asset c8372d96).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Golden sun rays from the upper corners and magenta and amber flower petals at the sides, center empty (asset 47e2300d).

## 20 O Julgamento
- figure (fig 0.9, KEY_STRICT=1, FIG_ANCHOR=base): Figures on a flat pure chroma green #00FF00 background, nothing else in the background. Judgement tarot card: a winged angel in brass armor with wide mechanical wings blowing a brass trumpet at the top, three adults with raised arms rising from brass capsules at the bottom. Cyberpunk steampunk illustration, neon rim light. Capsules flush with the bottom edge. (asset c0901e2b)
- bg (crop): radiant sky with sunbeams over sea and mountain islands (asset 555b34eb).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Golden and cyan arcs of light like sound waves framing the edges, center empty (asset 91fa8097).

## 21 O Mundo
- figure (fig 0.92, width cap binds): Figure on a flat pure chroma green #00FF00 background, nothing else in the background. The World tarot card: a joyful Black woman dancer in bronze and violet steampunk costume with flowing violet silk, dancing inside an oval brass laurel wreath with neon cyan and magenta accents; the wreath interior is open (green). Cyberpunk steampunk illustration, neon rim light. Centered. (asset 15f7a3f4)
- bg (crop): cosmic sky with a glowing planet and constellation figures of the eagle, lion, bull and angel (asset dc1b4f61).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (center): Pure solid black #000000 background, no people. Magenta, amber and cyan nebula ribbons framing the edges, center empty (asset fe6eed44).

## 22 Ás de Paus
- figure (fig 0.85, FIG_ANCHOR=base, look DEFRINGE=2): On flat pure chroma green #00FF00, nothing else. Ace of Wands: the hand of a mature dark-skinned Black woman with a brass cuff rising from the bottom edge, gripping one large ornate brass wand with glowing magenta, cyan and amber glass sections and a jeweled crown tip, glowing neon leaves sprouting along it. Cyberpunk steampunk illustration, neon rim light. Large, fills about 85% of the height. (asset f3c3d81f)
- bg (crop): steampunk fantasy city of brass towers and neon banners over green hills, golden sun sigil in a sunset sky (asset 2dbb78f1).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (r): Pure solid black #000000, amber fire and cyan magenta plasma plumes rising with sparks (asset 6ba7549a, rotated).

## 23 Dois de Paus
- figure (fig 0.9, FIG_MAXW=2100): On flat pure chroma green #00FF00, nothing else. Two of Wands: a mature man with dark swept hair and a short grey beard in a long black and brass steampunk coat, holding a glowing cosmic globe in one hand and a tall glowing brass staff in the other, a second staff standing beside him. Realistic adult proportions, highly detailed face. Feet at the bottom. (asset 6074a2d3)
- bg (crop): brass balcony with banners overlooking a sunset harbor city and airships (asset fcf0126e).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored horizontally.

## 24 Três de Paus
- figure (fig 0.9, FIG_MAXW=2100): On flat pure chroma green #00FF00, nothing else. Three of Wands: a woman with short dark hair seen from behind in a long ornate black and brass coat, holding one of three tall brass lantern staffs, looking out to sea. Feet at the bottom. (asset 4da4857a)
- bg (crop): sunset sea with ships and airships from a cliff; the three staffs on the cliff at the left of the source fall outside the portrait center crop (asset 979b2413).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (top): reuse of asset 6ba7549a, flipped vertically.

## 25 Quatro de Paus
- figure (fig 0.9, FIG_MAXW=2100): On flat pure chroma green #00FF00, nothing else. Four of Wands: a joyful couple celebrating, a Latin woman in a golden ball gown and a smiling man in a brown brass coat, each raising a glowing neon flower bouquet. Realistic adult proportions, highly detailed faces. Feet at the bottom. (asset fc2fde34)
- bg (crop): flowered brass arch of four pillars before a glowing steampunk castle at dusk (asset 8fdcd104).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, hue shifted +40 degrees.

## 26 Cinco de Paus
- figure (fig 0.9): On flat pure chroma green #00FF00, nothing else. Five of Wands: five diverse adults in steampunk coats sparring with long glowing brass staffs crossed overhead. Feet at the bottom. (asset 13a00dac)
- bg (crop): neon industrial canyon of brass machinery and glowing screens with wet reflective ground (asset 76a8ee1c).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored and hue shifted -50 degrees.

## 27 Seis de Paus
- figure (fig 0.9, FIG_MAXW=2100): On flat pure chroma green #00FF00, nothing else. Six of Wands: a triumphant mature Black man with a grey beard and a brass top hat riding a mechanical brass horse, holding a staff crowned with a glowing laurel wreath. Highly detailed face. (asset 26026bdc)
- bg (crop): golden avenue of brass arches and towers at sunset with a sparkling sky (asset 70ae8c78).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (top): reuse of asset 6ba7549a, flipped both ways and hue shifted +90 degrees.


## 28 Sete de Paus
- figure (fig, FIG_FIT=753,2206,1647 KEY_STRICT=1: woman large and shifted left, top staff head inside the card, lower staff tips cropped): On flat pure chroma green #00FF00, nothing else. Seven of Wands: a grey-braided older woman in a patterned steampunk cloak standing on a dark rock, gripping a glowing brass staff, six brass staff tips with glowing orbs rising from below. (asset 5c5712b4)
- bg (crop): neon steampunk city of brass spires on a rocky ridge under a violet sky with airships and lightning (asset 5a722f12).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored horizontally and hue shifted +150 degrees.
- finish: DEFRINGE=2.

## 29 Oito de Paus
- figure (fig, FIG_FIT=1080,1920,1900): On flat pure chroma green #00FF00, nothing else. Eight of Wands: eight brass staffs flying diagonally with cyan, magenta and amber energy trails, no people. Scaled large to fill the frame. (asset e3850dd6)
- bg (crop): steampunk city beside a glowing turquoise river through green valleys under a swirling neon sky (asset 59e8e619).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (top): reuse of asset 6ba7549a, rotated 180 degrees and hue shifted -120 degrees.
- finish: DEFRINGE=2.

## 30 Nove de Paus
- figure (fig 0.9, FIG_MAXW=2160, KEY_STRICT=1: large centered, staff tops not cropped): On flat pure chroma green #00FF00, nothing else. Nine of Wands: a bearded man in teal and magenta robes meditating on a mossy mound, nine brass staffs with glowing crystal tips around him. (asset d816808c)
- bg (crop): fortified brass gate and wall with neon towers, misty mountains and a wet reflective plaza (asset 1c02569d).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (top): reuse of asset 6ba7549a, flipped vertically and hue shifted -25 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5.

## 31 Dez de Paus
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=4200, KEY_STRICT=1: man kept large, staff ends cropped): On flat pure chroma green #00FF00, nothing else. Ten of Wands: a muscular tattooed man with a topknot in steampunk armor straining under a bundle of ten brass staffs with glowing neon tubes. (asset d92d51b0)
- bg (crop): golden-hour road of cobblestones winding up to a hilltop steampunk city of windmills and neon (asset 4066608e).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, hue shifted -80 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5.

## 32 Pajem de Paus
- figure (fig 0.9, FIG_ANCHOR=base, KEY_STRICT=1): On flat pure chroma green #00FF00, nothing else. Page of Wands: a smiling curly-haired woman with goggles in a brass-trimmed leather coat holding a staff that sprouts glowing leaves. (asset b732d47c)
- bg (crop): desert of glowing neon dunes with pyramids and constellation salamanders in a starry sky (asset 2fc3d31e).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways and hue shifted +60 degrees.
- finish: DEFRINGE=2 RECOLOR_GREEN=1 RECOLOR_TO=amber (yellow-green leaves -> amber).

## 33 Cavaleiro de Paus
- figure (fig 0.9, FIG_ANCHOR=base, KEY_STRICT=1): On flat pure chroma green #00FF00, nothing else. Knight of Wands: a rider in a turban and brass armor on a rearing mechanical brass horse with a flaming mane and tail, raising a staff topped by a glowing orb. (asset d0806d1f)
- bg (crop): fiery orange desert canyon with brass refinery towers and cyan light streaks in the sky (asset 79268e90).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored and hue shifted -160 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5.

## Edge clean (all cards, look.py, from 28-33 on)
- White fringe cause: rim light added on the outermost contour pixels (brighter than the bg), edge pixels carrying unpremultiplied bright screen/spill color, and leftover screen-green rims. look.py now always chokes the key alpha by EDGE_CHOKE=3 px, replaces contour pixels that are brighter than the interior (halo) or much darker (despill line) with the nearest interior color, brightness-caps thin parts, keeps the rim light strictly inside (5 px from the contour) and no brighter than the bg, drops leftover screen-green rims, and fills transparent pixels with interior color so resizing can't bleed bright colors.

## 34 Rainha de Paus
- figure (fig 0.9, FIG_ANCHOR=base, KEY_STRICT=1): On flat pure chroma green #00FF00, nothing else. Queen of Wands: a regal smiling woman with sunflowers in her hair on a brass lion throne, a black mechanical cat at her feet, holding a staff with a green flame. (asset 3da28dea)
- bg (crop): brass and stained-glass palace hall opening onto a golden steampunk city (asset 50969ae0).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically and hue shifted +110 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (green flame -> amber).

## 35 Rei de Paus
- figure (fig 0.9, FIG_ANCHOR=base, KEY_STRICT=1): On flat pure chroma green #00FF00, nothing else. King of Wands: a grey-bearded king in a red brocade coat on a brass salamander throne holding a staff topped by a glowing magenta orb. (asset 5535c431)
- bg (crop): ornate brass arch framing a sunset sky and neon city spires (asset 6a33ac58).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, rotated 180 degrees, mirrored and hue shifted -140 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5.

## 36 Ás de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: forearm flush to bottom, chalice fully visible): On flat pure chroma green #00FF00, nothing else. Ace of Cups (Marseille numbering): a metallic hand and forearm rising from the bottom edge, holding a large ornate brass chalice overflowing with glowing cyan and magenta liquid, four watery streams pouring down, small green leaves and pink blossoms around it. Cyberpunk steampunk illustration, neon rim light. Large. (asset 3248e803)
- bg (crop): luminous neon lagoon city with cyan water reflections, magenta bridge arches and a Flower of Life sigil in the sky (asset 8fd3b1cd).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways and hue shifted +175 degrees (watery cyan/magenta).
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (small green leaves -> amber).

## 37 Dois de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: both figures fully visible, width-bound as large as possible): On flat pure chroma green #00FF00, nothing else. Two of Cups (Marseille numbering): a woman in a white cyan-piped steampunk suit and a pink-haired man in a white magenta-piped suit facing each other, each holding a glowing chalice, a holographic caduceus between them on a mossy mound. Realistic adult proportions, highly detailed faces. Cyberpunk steampunk illustration, neon rim light. Feet at the bottom. (asset 8223bbd4)
- bg (crop): luminous neon lagoon city with cyan water reflections and magenta sky (asset c5d1bc2e).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored horizontally and hue shifted +155 degrees (watery cyan/magenta).
- finish: DEFRINGE=4 EDGE_CHOKE=5 FIN_HEADBOX=420,1200,230+1750,1170,230 (energy carved off both faces).

## 38 Três de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: width-bound, cups at top fully inside the card): On flat pure chroma green #00FF00, nothing else. Three of Cups (Marseille numbering): three joyful women toasting with raised ornate brass chalices, standing on a harvest of grapes and pumpkins with green leaves. Realistic adult proportions, highly detailed faces. Cyberpunk steampunk illustration, neon rim light. Base flush with the bottom edge. (asset 3f8392cb)
- bg (crop): luminous neon lagoon city / harvest night scene (asset e844db8a).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically and hue shifted -170 degrees (watery cyan/magenta).
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (green leaves under harvest -> amber) FIN_HEADBOX=750,2160,210+1100,2200,230+1620,2160,200 (energy carved off all three faces).

## 39 Quatro de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): blue-haired man meditating cross-legged under a golden bonsai on a mossy mound, three brass cups before him and a holographic hand offering a fourth cup (asset 9a92bb07).
- bg (crop): neon city skyline at dusk over a stone terrace with a glowing sigil circle (asset 0313b841).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways and hue shifted +165 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (moss / green holo hand -> amber).

## 40 Cinco de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): pink-haired woman in a grey tattered coat looking down at spilled cups glowing magenta, two cups standing behind her (asset b64118e6; grey backdrop flood-replaced with chroma green before keying, spilled cups kept in figure layer).
- bg (crop): rainy neon canal city with a sacred-geometry spire (asset b97d7520, cropped inside the baked ornamental border, excluding the title, left plaque and bottom emblem).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored horizontally and hue shifted -160 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5.

## 41 Seis de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): blue-haired man kneeling, giving a glowing flower cup to a child, five cups on a mossy ground patch (asset 79c4236f).
- bg (crop): overgrown sunlit courtyard with crystal lotus flowers and a glowing mandala floor (asset 2f6bcef2).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically and hue shifted +135 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (moss -> amber, kept in figure) FG_BOOST=0.6 FG_BODY=0.8 (softer energy, cleared over the figures).

## 42 Sete de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): woman seen from behind reaching up to seven floating holographic cups in an arc (cups in figure layer) (asset 132db018).
- bg (crop): cosmic sky with floating castle islands and sacred-geometry circles (asset ff67e7f1).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways and hue shifted -120 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 43 Oito de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): pink-haired man walking away with a glowing staff, eight stacked cups at left (in figure layer) (asset 585537f7).
- bg (crop): misty mountain path under a sacred-geometry moon (asset 6507a4bb).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored and hue shifted +95 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 44 Nove de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: width-bound): joyful woman seated on a bench before a shelf of nine cups (asset 0ea80d2b).
- bg (crop): sunset neon city seen from a domed pavilion with a geometric glass ceiling (asset 5150422a).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, hue shifted -90 degrees.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 45 Dez de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: width-bound): joyful family of four under an arc of ten rainbow cups on a grassy ground patch (asset 9398c9d6).
- bg (crop): golden sunrise valley under a Flower of Life sky (asset 59c1ca55).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically, hue +20 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (grass -> amber) FG_BOOST=0.6 FG_BODY=0.8.

## 46 Valete de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): teal-bob young woman holding a cup with a holographic fish (asset 7947ba37).
- bg (crop): neon seaside promenade at dusk (asset 7df1f337).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways, hue -40 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 47 Cavaleiro de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: width-bound): pink-haired rider in a white suit on a white robot horse, holding a glowing cup (asset f8086743).
- bg (crop): pastel dreamscape with an aqueduct and crystal spires (asset 26900c85).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored, hue +60 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 48 Rainha de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): Black queen in a blue circuit gown on a pearl shell throne holding an ornate glowing cup (asset 8e79bef7).
- bg (crop): pastel coastal sky with crystal rocks (asset ed9a1918).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically, hue -70 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 49 Rei de Copas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): blue-haired king in a blue embroidered coat on a glass and coral throne, holding a sceptre and a glowing cup (asset d88ca424).
- bg (crop): night sea under a sacred-geometry star sigil (asset 4522ce81).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways, hue +110 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 50 Ás de Espadas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1): hand rising from a cloud holding a crystal sword crowned by a golden laurel halo (asset 406fe1dd).
- bg (crop): blue sky over snowy mountain peaks (asset e9461f10).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, hue -15 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (green spill on the gold laurel -> gold) FG_BOOST=0.6 FG_BODY=0.8.

## 51 Dois de Espadas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, KEY_STRICT=1: width-bound, bench and both blades fully inside): blindfolded South Asian woman in a blue silver-embroidered robe seated on a stone bench, arms crossed holding two blue crystal swords (asset ac5e3cdd).
- bg (crop): night sea with islets and a neon skyline (asset d795d5b4).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored, hue -50 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 52 Três de Espadas
- figure (FIG_FIT=1080,1850,990 KEY_STRICT=1: centered vertically, large, pommels inside the card): magenta crystal circuit heart pierced by three blue crystal swords (asset cf4f7406).
- bg (crop): storm clouds and rain over a dark violet city (asset 96902ec6).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped vertically, hue -25 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.6 FG_BODY=0.8.

## 53 Quatro de Espadas
- figure (FIG_FIT=1080,2750,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% card width, tomb base resting on the chapel floor (no floating); three hanging swords kept, their cut tops feathered 40 px): knight in silver tech armor resting on a carved stone tech tomb, a glowing sword below him, three swords hanging above (asset 376132fd).
- bg (crop): cyber chapel, centered on the circuit stained-glass window (asset c1f575b5).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored, hue +150 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.4 FG_BODY=0.85 FIN_HEADBOX=430,2640,220 (calm, light energy).

## 54 Cinco de Espadas
- figure (fig 0.9, FIG_ANCHOR=base, FIG_MAXW=2160, FIG_KEEPALL=1, KEY_STRICT=1: grounded, rock pile at the bottom; swords over the shoulder kept): red-haired man in a black circuit trench coat standing on a pile of dark rocks, three blue crystal swords over his shoulder and two on the ground (asset ca48af3c).
- bg (crop x 440-845 of 1280): stormy coast with two distant walking figures and a neon city at right (asset d4ad7d99).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, flipped both ways, hue -100 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.5 FG_BODY=0.85.

## 55 Seis de Espadas
- figure (FIG_FIT=1080,2441,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, hull at the water surface below the horizon, lower-middle): hooded ferrywoman with a glowing pole steering a black hover boat carrying a hooded mother and child and six upright blue swords (asset 66a38da2).
- bg (crop): dusk sea with a city on the far shore (asset 96221418), plus a soft contact shadow and faded hull reflection baked under the boat so it sits on the water.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, hue +170 degrees with green hues folded to cyan/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1430,2000,170+990,2410,220.

## 56 Sete de Espadas
- figure (FIG_FIT=1080,2685,1000 FIG_KEEPALL=1 KEY_STRICT=1: dirt patch on the muddy ground near the card bottom, ground swords kept): grinning hooded thief in black neon-trimmed gear sneaking off with five blue crystal swords, two swords left stuck in a dirt patch (asset 2eb35d59).
- bg (crop, centered on the path): night camp with tents and violet banners on muddy ground (asset 5cb21545), plus a soft elliptical contact shadow baked under the dirt patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): reuse of asset 6ba7549a, mirrored, hue -140 degrees with yellow-green..green hues folded to blue/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (grass tufts in the dirt patch) FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=767,1792,230.

## 57 Oito de Espadas
- figure (FIG_FIT=1080,3060,1000 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, puddle on the marsh near the card bottom): blindfolded woman in a silver suit and translucent cape wrapped in violet light ribbons, walking through a dark wet puddle ringed by eight upright swords (asset 119782cb).
- bg (crop x 700-1105 of 1280, keeps the castle): misty marsh with a spired castle-city on a hill (asset 0a8fd54f), plus a soft elliptical contact shadow under the puddle.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): work/nogreen.py, asset 6ba7549a flipped vertically, hue +40 degrees, yellow-green..green folded to blue/magenta.
- finish: DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 (green glints in the puddle -> cyan) FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1077,2470,200.

## 45-55 energy refresh
- fg energy plates of cards 45-55 rebuilt with work/nogreen.py (same flips and hue shifts as listed per card, but the folded range widened to yellow-green..green -> blue/magenta) so no yellow-green energy remains; figure, bg and finish settings unchanged.

## 58 Nove de Espadas
- figure (FIG_FIT=1080,2655,950 FIG_KEEPALL=1 KEY_STRICT=1: bed on the floor near the card bottom, nine stacked swords kept): hooded woman sitting up in a dark circuit-quilt tech bed with her face in her hands, nine blue swords stacked horizontally above (asset f583a91b).
- bg (crop x 600-1005 of 1280: centered on the rainy neon window, the empty bed at left excluded): dark bedroom with a rain-streaked window onto a neon city (asset f40554d9), plus a soft contact shadow under the bed.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): work/nogreen.py, asset 6ba7549a mirrored, hue -60 degrees.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1080,2460,260 (face and hands clear).
- 57 finish now also FIG_DEGREEN=1 (work/degreen.py after look.py), so a rebuild keeps the puddle green cleanup.

## 59 Dez de Espadas
- figure (FIG_FIT=1080,3312,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, ground patch on the shore near the card bottom): chrome android lying face down on a cracked dark ground patch, ten blue crystal swords in its back, red cloak over its legs (asset fda29038).
- bg (crop x 330-735 of 1280: sun glow at left, part of the city at right): black sky, golden dawn over the sea, city on the right, dark shore (asset 1ab8cee8), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored two-tone amber/violet (sparse, dark mood).
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 (green-dominant spill clamped, cyan sword glow pushed back to blue; red cloak untouched) DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.35 FG_BODY=0.9 FIN_HEADBOX=500,3330,230.

## 60 Valete de Espadas
- figure (FIG_FIT=1080,2140,1005 FIG_KEEPALL=1 KEY_STRICT=1: tall, anchored near the bottom, full body incl. sword tip and drone): young Black woman scout in white/blue techwear with long braids, a drone at her shoulder, holding a raised blue crystal sword, standing on a rock base (asset 9fe23510).
- bg (crop x 700-1105 of 1280, centered on the city): windy hilltop under a blue sky with a drone flock, city in the valley (asset 4933d22d), plus a soft contact shadow under the rock base.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped vertically, recolored airy cyan-white / violet (saturation x0.55) for a daytime look.
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.45 FG_BODY=0.85 FIN_HEADBOX=1180,860,260.

## 61 Cavaleiro de Espadas
- figure (FIG_FIT=1080,2703,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, hooves just above the dusty ground in the lower card): knight in silver-blue armor and circuit cape on a galloping silver robot horse, raised blue crystal sword (asset 9dfe251d).
- bg (crop x 230-635 of 1280, keeps the castle towers): stormy plain with wind-bent cypress trees (asset 6f25322b), plus a soft ground shadow ~130 px below the hooves and light dust puffs kicked up at the hind and front hooves.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored two-tone blue / violet (speed streaks).
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.4 FG_BODY=0.85 FIN_HEADBOX=1225,2300,230.

## 62 Rainha de Espadas
- figure (FIG_FIT=1080,2765,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, throne platform on the terrace floor at the bottom): silver-haired queen with a blue crystal crown in a blue gown on a carved stone throne with lion armrests, holding an upright blue sword (asset d0d4a0d2).
- bg (crop x 718-1123 of 1280, centered on the city, pillar at right excluded): snowy cliff terrace, mountains and a crystal-spired city under a blue sky (asset 90968248), plus a soft contact shadow under the platform.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped both ways, recolored airy blue-white / violet (saturation x0.55).
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.45 FG_BODY=0.85 FIN_HEADBOX=1083,2340,240.

## 63 Rei de Espadas
- figure (FIG_FIT=1080,2927,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, platform on the polished floor near the bottom): grey-bearded Black king in blue and silver robes and crystal crown on a chrome throne, holding an upright blue crystal sword (asset 4c91e820).
- bg (center crop, the city between the glass columns): glass-column hall open to the sky, city below, polished floor (asset 780ae45d), plus a soft contact shadow and a faint blurred reflection of the throne on the floor.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored airy blue-white / violet (saturation x0.55).
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.45 FG_BODY=0.85 FIN_HEADBOX=1102,2425,240.

## 64 Ás de Ouros
- figure (FIG_FIT=1080,1750,740 FIG_KEEPALL=1 KEY_STRICT=1: centered slightly above the middle, large; cloud floats by design): chrome robotic hand rising from a grey cloud holding a large golden circuit pentagram coin (asset 7e7fbadd).
- bg (center crop on the rose archway and the golden city): rose archway garden at golden hour, golden city through the arch, mountains (asset 77cb6f33).
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped vertically, recolored three-tone amber / gold / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (green spill on gold edges -> amber) FG_BOOST=0.5 FG_BODY=0.85.

## 65 Dois de Ouros
- figure (FIG_FIT=1080,2342,1000 FIG_KEEPALL=1 KEY_STRICT=1: anchored near the bottom, coins and infinity ribbon kept): joyful juggler woman in a purple/orange outfit and top hat dancing on a paving patch, two gold pentacle coins linked by a glowing infinity ribbon (asset 34912aa1).
- bg (crop x 560-965 of 1280: ship at the right, clearly visible beside the juggler): golden-hour harbor quay, ships on rough waves (asset c90c2573), plus a soft contact shadow under the paving patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored two-tone amber / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (grass tufts and gold-edge spill -> amber) FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1060,1342,240.

## 66 Três de Ouros
- figure (FIG_FIT=1080,2995,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, round stone platform on the floor at the bottom; green through the arch opening keyed to background): grey-haired architect holding a blue holographic blueprint, a young woman artisan carving, and a robed monk around a carved stone arch with three glowing gold pentacles on a round stone platform (asset 6cc74fd1).
- bg (default center crop): cathedral under construction with scaffolding and golden light rays (asset 847c3e15), plus a soft contact shadow under the platform.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped vertically, recolored two-tone amber / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=565,2345,200+1050,2435,190+1663,2322,200 (all three faces clear).

## 67 Quatro de Ouros
- figure (FIG_FIT=1080,2548,1050 FIG_KEEPALL=1 KEY_STRICT=1: large, ~65% card height, stone patch on the floor at the bottom): Black woman in black and gold techwear seated on a stone block, a gold pentacle on her crown, one held to her chest and two under her feet, on a stone paving patch (asset 71c196e4).
- bg (crop x 600-1005 of 1280: vault door plus a sliver of city at left): night city and a carved vault door with banners on a stone terrace (asset 45f32cb7), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped both ways, recolored two-tone amber / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1164,1750,230.

## 68 Cinco de Ouros
- figure (FIG_FIT=1080,2844,1200 KEY_STRICT=1: ~48% card height, snowy patch on the ground at the bottom, patch ends run past the card sides; crutch kept, loose snowflakes dropped): hooded young woman with a blue/violet cyber arm and an old bearded man on a crutch, both in ragged snow-covered clothes, walking on a snowy patch (asset f74633ee).
- bg (crop x 718-1123 of 1280, centered on the stained-glass five-pentacle window): snowy neon cathedral street at night (asset c7256996), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored two-tone amber / violet, light (cold scene).
- finish: FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=4 EDGE_CHOKE=5 FG_BOOST=0.35 FG_BODY=0.9 FIN_HEADBOX=830,2066,200+1436,2176,210.

## 69 Seis de Ouros
- figure (FIG_FIT=1080,3152,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, stone patch on the plaza floor at the bottom; floating scale and coins kept): Black merchant in a purple and gold coat holding a glowing golden scale and dropping glowing gold coins to two kneeling beggars, a young woman and an old man, on a stone patch (asset 4ebe7478).
- bg (crop x 400-805 of 1280: central tower, readable tarot banners at right excluded): golden-hour city plaza with a central spire, airships and an inlaid floor circle (asset 6bf65e05), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a, recolored two-tone amber / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (scale/coin glow gold) FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1071,2561,170+551,3009,160+1573,3081,160.

## 70 Sete de Ouros
- figure (FIG_FIT=1080,2997,995 FIG_KEEPALL=1 KEY_STRICT=1: ~92% width, soil patch on the path at the bottom; green screen between the branches keyed, leaves kept): Indigenous farmer in a patterned poncho leaning on a hoe, beside a circuitry bush bearing seven gold pentacle coins, on a soil patch (asset f61dcf54).
- bg (default center crop): sunrise over a misty farm terraces valley with a spired city and the sun on the path (asset 51869b4e), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped vertically, recolored two-tone amber / violet.
- finish: LOOK_KEEPGREEN=1 (new look.py option: skip the green-rim drop so foliage survives) FIG_DEGREEN=1 DEGREEN_CYAN=1 DEFRINGE=2 EDGE_CHOKE=2 (thin twigs kept) RECOLOR_GREEN=1 RECOLOR_TO=amber FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=532,2349,200. Leaves end up dark olive.

## 71 Oito de Ouros
- figure (FIG_FIT=1080,2628,853 FIG_KEEPALL=1 KEY_STRICT=1: ~60% card height, wooden floor patch on the workshop floor at the bottom): goggled craftsman in black leather engraving a gold pentacle at a workbench, a rack of eight gold coins beside him, on a wooden floor patch (asset e071d721).
- bg (default center crop on the window): workshop with a large window onto a spired city at sunset (asset 556c4da4), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a mirrored, recolored two-tone amber / violet.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber FG_BOOST=0.5 FG_BODY=0.85 FIN_HEADBOX=1159,1701,220.

## 72 Nove de Ouros
- figure (FIG_FIT=1080,2515,1050 FIG_KEEPALL=1 KEY_STRICT=1: ~62% card height, width-bound, stone patch on the terrace floor above the bottom edge; green through the trellis keyed): woman in a purple and gold gown with a robotic falcon on her hand, beside a golden trellis with nine gold pentacles and grapes, on a stone patch (asset 02c0b80f).
- bg (crop x 598-1003 of 1280, centered on the spired villa): golden-hour vineyard terrace with a spired villa on a hill (asset 6f08cb25), plus a soft contact shadow under the patch.
- mid: vazio (aura do fg gerada pelo fin.py).
- fg (bottom): asset 6ba7549a flipped vertically, recolored two-tone amber / violet, lighter.
- finish: FIG_DEGREEN=1 DEFRINGE=4 EDGE_CHOKE=5 RECOLOR_GREEN=1 RECOLOR_TO=amber (vine leaves -> amber) FG_BOOST=0.35 FG_BODY=0.85 FIN_HEADBOX=876,1567,220.
