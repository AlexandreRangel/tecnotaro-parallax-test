# Tecno Tarô 3D 2 - historico de prompts (Grok)

## Identificacao

| Campo | Valor |
|---|---|
| Nome oficial | Tecno Tarô 3D 2 |
| Pasta | repo `v2/`, box `/workspace/tarot-app/tecnotaro-parallax/v2` |
| Ferramenta | Grok GenerateImage (cerca de 1024x576 por placa) |
| Pipeline | `proc.py SRC NN-slug camada modo [frac]` -> `look.py` / `fin.py` / `comp.py` via `finish.sh NN-slug` -> `publish_batch.sh NN` |
| Status | Em andamento (cartas 00 a 35 documentadas em PROMPTS.md; publicacao progressiva) |
| Datas | Ativo a partir de 12/10/2026 |
| Link | https://alexandrerangel.github.io/tecnotaro-parallax-test/v2/ |
| Fonte primaria de prompts | `v2/PROMPTS.md` (espelhado abaixo) |

## Camadas (4 moveis + frame)

| Ordem | Camada | Conteudo | Alpha | Depth padrao |
|---|---|---|---|---|
| 1 | bg | Fundo distante, ceu, cidade, horizonte. Sem figuras | opaco | -0.030 |
| 2 | mid | Cenario medio (predios, arcos, maquinas) ou aura do fg (fin.py) | transparente | -0.015 |
| 3 | figure | Personagem ou emblema + chao sob os pes | transparente | 0 |
| 4 | fg | Energias, faíscas, fumaca, props frontais | transparente | +0.036 |
| 5 | frame | Moldura com titulo | janela transparente | fixo |

Canvas: frame 2240x3840 @2x. Camadas moveis 2120x3460 @2x (janela x 1.12). Amplitude de tilt 1.15 (15% mais forte que v1).

## Regras gerais de geracao (v2)

- Figura: 85 a 95% da altura, proporcao adulta real (~7.5 cabecas), cabeca nao exagerada.
- Energia (fg) saindo dos objetos, nunca cobrindo o rosto (fin.py abre o rosto).
- mid em fundo verde #00FF00; fg em fundo preto #000000; figure em chroma verde.
- Estilo visual nos prompts: cyberpunk steampunk, neon magenta/ciano/ambar, rim light.

## Evolucao de estilo e pipeline (datas)

### 12/10/2026 - regras globais de conteudo

Formalizadas (e aplicadas tambem no v3 HQ):

- Sem guerra, militar, soldados, armas de fogo, violencia grafica.
- Corpos esbeltos (evitar muscular/bodybuilder).
- Mulheres de cabelo curto preferencialmente.
- Temas: transhumanismo, cultivation, meditacao, musica, artes.
- Continuidade: neon magenta/ciano/ambar, latao e cobre.

### 12/10/2026 - fin.py e look.py

- `fin.py`: fg_final mais forte (sem 10% de transparencia global, corpo atenuado 15%, brilho e saturacao 1.3x); aura do fg atras da figura gravada em mid.png sobre mid_base.png.
- `look.py`: figure.png a partir de figure_key.png (neon semitransparente com bloom, rim light colorido pelo bg, grade de 12% para tons do bg).
- `finish.sh`: orquestra look.py + fin.py + comp.py com flags por carta (ex.: 12 FIN_HEAD=bottom; 13 BLOOM/WATER; 18 RECOLOR_GREEN; 28-35 DEFRINGE/EDGE_CHOKE).

### Edge clean (cartas 28-33 em diante)

`look.py` choke de alpha (EDGE_CHOKE=3), remocao de halo claro/escuro no contorno, rim light so por dentro, remocao de franja verde de chroma.

## Scripts e modos

- `proc.py`: recorte / key das placas Grok.
- `look.py`: pos-processo da figure (neon, rim, defringe).
- `fin.py`: composicao da energia e mid aura.
- `comp.py`: previa em `qa/`.
- `finish.sh NN-slug`: wrapper com export de variaveis por carta.
- Opcoes frequentes: `KEY_STRICT=1`, `FIG_ANCHOR=base|top`, `FIG_MAXW`, `DEFRINGE`, `EDGE_CHOKE`, `RECOLOR_GREEN`, `BLOOM`, `WATER`, `FG_EXTEND`, `FG_DIFFUSE`.

## Prompts por carta (copia de v2/PROMPTS.md)

O bloco a seguir e a fonte operacional usada na geracao. Manter sincronizado: ao mudar PROMPTS.md, anexar a mudanca aqui com data.

---

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


---

## Atualizacoes futuras

Anexar secoes datadas abaixo. Nao apagar prompts antigos.

<!-- ## 2026-MM-DD - titulo -->
