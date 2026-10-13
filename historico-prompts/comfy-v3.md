# Tecno Tarô 3D 3 (ComfyUI HQ) - historico de prompts e modelos

## Identificacao

| Campo | Valor |
|---|---|
| Nome oficial | Tecno Tarô 3D 3 (ComfyUI) |
| Pasta | repo `v3/`, box `/workspace/tarot-app/tecnotaro-parallax/v3`, HQ em `v3/src/` |
| Maquina | PC Blackwell (RTX 5090), machineId ac1fa0af-39bc-449a-a711-8f7bea449d4a |
| Scripts HQ | `C:\tecno_v3hq\gen_hq.py` + `cards_hq.json` (espelho: `v3/src/`) |
| Saida raw HQ | `C:\Dropbox\tarot-app\midia\decks\tecnotaro-parallax-3\raw_hq\` |
| Build | `v3/src/v3_build_hq.py NN RAWDIR` |
| Status | HQ em geracao no Blackwell (nao interromper renders); versao leve anterior pausada por BSOD (so O Louco publicado no GitHub na epoca) |
| Datas | 12/10/2026 modo leve/pesado inicial; 13/10/2026 pipeline HQ 4 camadas |
| Link | https://alexandrerangel.github.io/tecnotaro-parallax-test/v3/ |

## Camadas (4 moveis + frame)

Schema `tecnotaro-parallax-v3`:

| Ordem | Camada | Conteudo | Depth tipico |
|---|---|---|---|
| 1 | bg | Ceu + skyline distante, opaco, render vertical | -0.040 |
| 2 | mid | Arquitetura/objetos cerca de 50 cm atras do personagem, cada peca renderizada isolada e keyada | -0.018 |
| 3 | figure | Personagem + chao/objetos anexos, ancora na base da carta | 0 |
| 4 | energy | Energia frontal (luma key), atenuada sobre o corpo, recortada nos rostos | +0.040 |
| 5 | frame | Moldura fixa | fixo |

Tamanho final das camadas moveis: 2120x3460 @2x.

## Modelos e pipeline HQ (13/10/2026, gen_hq.py)

Confirmado por leitura somente-leitura em `C:\tecno_v3hq\gen_hq.py` (identico ao espelho do repo na data desta anotacao).

| Etapa | Detalhe |
|---|---|
| Checkpoint | `_SDXL_1_0\Juggernaut_XL\juggernautXL_ragnarokBy.safetensors` (Juggernaut XL Ragnarok SDXL) |
| Base txt2img | 1024x1664, 40 steps, CFG 4.5, sampler `dpmpp_2m_sde`, scheduler `karras`, denoise 1.0 |
| Upscaler | `4xNomos8k_atd_jpg.safetensors` (ImageUpscaleWithModel) |
| Resize | lanczos para 1600x2600 (hires) |
| Hires img2img | 28 steps, CFG 4.5, denoise 0.34, seed+1, mesmo sampler/scheduler |
| Detailer rosto | YOLO `face_yolov8m.pt`, crop ~2.0x, img2img 1024 px, denoise 0.36, mascara elipse suave |
| Detailer maos | YOLO `hand_yolov8s.pt`, scale 2.2, denoise 0.32 |
| Recorte figura/mid | rembg **BiRefNet** (`birefnet-general`, CPU), threshold, choke 1 px, descontaminacao de cor, defringe |
| mid alternativo | chroma key verde #00FF00 com despill (greenkey) quando aplicavel |
| energy | luma key (preto vira transparente), mascara central + exclusao de rostos + atenuacao sobre corpo |
| Guard GPU | pausa se temp > 80 C; aborta se > 85 C; 3 s entre jobs; 30 s entre cartas |
| Seed base | `5000 + n*100` por carta; offsets por camada (mid +21/+26, figure +41, energy +61) |
| ComfyUI | `http://127.0.0.1:8188` (VAE em fp32 recomendado: `--fp32-vae`) |

### Modo leve anterior (12/10, work/gen.py)

Documentado em `v3/PROMPTS.md`: txt2img nativo 832x1216, sem upscale 4x GPU, upscale CPU Lanczos para 1408x2296, 1 job GPU por vez, limite potencia 450 W. Cartas 00-01 modo pesado: ~896x1536, 32 steps, CFG 4.5, hires 4xNomos denoise 0.32. FaceDetailer do Impact Pack descartado (imagens pretas); detalhe via YOLO + img2img no script.

## Templates de prompt (HQ)

### STYLE (sufixo positivo global)

```
Tecnotaro tarot art by Alexandre Rangel, playful energetic fluid mood, transhumanist cyberpunk steampunk world, polished brass and copper, glowing neon magenta, cyan and amber, magic and technology, sacred geometry as glowing neon line-work and holograms (Flower of Life, Metatron cube, golden spirals, mandala grids), neon LED circuitry, holographic interfaces, cybernetic accents, very bright luminous high-key lighting, vivid saturated colors, painterly digital illustration, crisp fine details, sharp focus, masterpiece
```

### NEG (negativo global)

```
text, letters, words, caption, watermark, signature, logo, border, frame, card frame, margin, young, teenager, child, kid, childlike, youthful face, east asian, asian, war, military, soldier, army, armor, armour, helmet, bandana, gun, rifle, weapon, combat, fighting pose, violence, blood, gore, muscular, bodybuilder, bulky, heavy layered drapery, cape, heavy boots, deformed, distorted face, bad anatomy, extra limbs, extra legs, extra arms, extra fingers, missing fingers, fused fingers, mutated hands, photo, photorealistic, blurry, soft focus, lowres, jpeg artifacts, dark, murky, underexposed, muddy, grainy, cropped head
```

### NOFIG (extra em camadas sem pessoa)

```
pedestrians, signage, neon text, shop signs, person, people, human, man, woman, figure, character, face, animal, creature, silhouette, crowd
```

### Montagem por camada (gen_hq.py)

- **bg:** `vertical portrait composition, far distant background only, nobody, {bg}, Blade Runner techno-noir neon megacity with arches, colonnades, futuristic temple-like towers, misty atmosphere, rain glow, holographic signs without readable text, bright and playful not dystopian, luminous sky with glowing nebula clouds of {energy} light, distant holographic billboards without text, LED lit towers, floating drones and data streams far away, soft atmospheric depth` + STYLE / NEG+NOFIG
- **mid:** por lado, `vertical portrait composition, one single tall isolated element: {midobj}, complete and fully visible from top to bottom, centered, no text, flat solid pure green #00FF00 chroma key background` + STYLE (depois BiRefNet e posicao esquerda/direita)
- **figure (major/court/ace):** `{fig}, vertical portrait, full body from head to feet standing on a small ground mound, the character fills the entire frame height, large and close, realistic adult proportions, normal head size, slim body, simple humble clothing` + fundo cinza de estudio + STYLE; detailers face/hand ligados
- **figure (pip):** um unico `{obj}` em product shot no cinza; o script repete no arranjo Marselha com contagem exata
- **energy:** `large swirling neon energy ribbons and luminous light streaks of {energy}, flowing in from the edges around an empty center, glowing sparks, musical light waves and particles, on a pure black background` + STYLE

Fundo de estudio: `isolated on a plain flat solid medium grey studio background`.

## Evolucao de estilo

### 12/10/2026

- Sem guerra, militar, armas, violencia (no NEG HQ).
- Corpos esbeltos; evitar capa pesada, botas pesadas, armor (salvo necessidade da carta).
- Mulheres de cabelo curto.
- Temas: transhumanismo, cultivation, meditacao, musica, artes (props near: instrumentos, tigelas, pinceis, etc.).

### 13/10/2026 (HQ)

- Renders **verticais** (sem crop wide).
- **mid** = objetos destacados atras do personagem, renderizados separadamente.
- Roupas **humildes/simples**, exceto Imperador, Imperatriz e Mago (roupas opulentas).
- Homens modernos: alguns com cabelo azul ou rosa; poucas barbas (muitos clean shaven / stubble leve).
- Mais tech/neon, circuitos LED, hologramas.
- Geometria sagrada como line-work neon / holograma (Flower of Life, cubo de Metatron, espirais aureas, mandalas).
- Arquitetura e atmosfera Blade Runner techno-noir (claro e brincalhao, nao distopico).
- Humor: `playful energetic fluid mood`.

## Prompts por carta (cards_hq.json, 78 cartas)

Campos: `fig` ou `obj`, `bg`, `mid`, `midobj`, `energy`, `near`, `prop`, `ground` (+ `suit`/`count` em pips). Fonte: `v3/src/cards_hq.json` = `C:\tecno_v3hq\cards_hq.json` (56006 bytes em 13/10/2026 ~00:21 America/Sao_Paulo).

### 00 O Louco (`00-the-fool`, kind=major)
- **figure:** a slim playful Black man in his fifties, clean shaven, short bright blue hair, laughing, simple cyan hoodie with glowing LED trim and a small jester hood with two tiny light bells, plain trousers, sneakers, small backpack with a holographic map, holding a light walking stick with a glowing crystal tip, light dancing step, a small robot dog leaping at his feet, standing on a small mound of glowing earth, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** rainy neon megacity canyon street at night lit bright, glowing magenta and cyan skyscraper signs fading into luminous haze
- **mid (legado):** tall brass and glass cyberpunk tenement buildings with neon windows
- **midobj (HQ):** a tall slim brass lamp post with glowing neon arrow shapes and floating holographic crystals
- **energy:** cyan and magenta
- **near:** glowing neon mushrooms and brass flowers
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 01 O Mago (`01-the-magician`, kind=major)
- **figure:** a slim confident Mediterranean woman in her forties with a short dark pixie haircut, sly smile, opulent magenta and gold coat with glowing circuitry embroidery, neon lemniscate hologram above her head, standing behind a brass and glass tech workbench, raising a glowing wand, on the table a cup, a coin, a small blade and holographic dice, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** bright neon alchemist laboratory city skyline with floating holograms and cyan nebula sky
- **mid (legado):** brass shelves with glowing flasks and copper pipes, cogs
- **midobj (HQ):** tall brass stands holding floating holographic screens and glowing alchemical flasks, left and right
- **energy:** magenta and cyan
- **near:** brass gears and glowing crystals
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 02 A Sacerdotisa (`02-the-high-priestess`, kind=major)
- **figure:** a serene slim Indian woman in her sixties with short silver hair, eyes half closed in meditation, simple blue tunic with glowing data lines, thin LED circlet, seated cross legged on a low stone seat, open glowing holographic book on her lap, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** vast luminous library temple with glowing blue veil curtains and starry cyan nebula
- **mid (legado):** tall brass bookshelves and gothic arches
- **midobj (HQ):** two tall pillars, one dark and one light, with glowing neon glyph rings, and a translucent veil of light between them, left and right
- **energy:** cyan and violet
- **near:** potted bioluminescent plants in brass pots
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 03 A Imperatriz (`03-the-empress`, kind=major)
- **figure:** a joyful Afro-Brazilian woman in her forties with short natural hair, opulent magenta and gold gown with LED embroidery, seated on an ornate tech throne with amber holographic wings, holding a sceptre with a glowing orb, ripe glowing wheat around her feet, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** radiant garden palace under bright magenta and gold nebula sky
- **mid (legado):** ornate brass greenhouse arches with glowing flowers
- **midobj (HQ):** tall stalks of glowing bioluminescent wheat and hydroponic towers with neon grow lights, left and right
- **energy:** amber and magenta
- **near:** a brass gramophone horn and glowing musical notes
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 04 O Imperador (`04-the-emperor`, kind=major)
- **figure:** a calm slim Scandinavian man in his sixties, clean shaven, short silver hair, opulent purple and brass jacket with glowing circuitry, simple LED crown, seated on a brass cube throne, holding a sceptre with a holographic globe, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** imperial neon citadel skyline with brass towers under bright blue and amber sky
- **mid (legado):** massive brass fortress walls and columns
- **midobj (HQ):** four tall brass columns with glowing blueprint holograms floating between them, left and right
- **energy:** amber and cyan
- **near:** paint brushes and glowing color jars
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 05 O Papa (`05-the-pope`, kind=major)
- **figure:** a gentle Middle Eastern man in his seventies with a short white goatee, red and gold robe with glowing data patterns, LED triple ring crown, seated, raising two fingers in blessing, holding a light staff, two adult students with tablets listening in front of him seen from behind, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** grand neon cathedral interior with stained glass glowing magenta and gold
- **mid (legado):** brass organ pipes and gothic arches
- **midobj (HQ):** two tall stone columns with glowing neon keys and floating hologram scrolls, left and right
- **energy:** amber and magenta
- **near:** brass beehive and glowing bees
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 06 Os Enamorados (`06-the-lovers`, kind=major)
- **figure:** a slim Latino man in his forties with short pink hair, simple shirt with glowing LED piping, standing between two women, a Black woman in her forties with a short natural haircut and a white redhead woman in her fifties with a short bob, simple modern clothes, tender smiles, holding hands, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** bright radiant sun halo over a neon city boulevard with pink clouds
- **mid (legado):** ornate brass arches with neon hearts and filigree
- **midobj (HQ):** a winged cupid drone of light hovering high above, and two flowering trees with neon blossoms, left and right
- **energy:** magenta and amber
- **near:** a small brass synthesizer with glowing keys
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 07 O Carro (`07-the-chariot`, kind=major)
- **figure:** a joyful slim Polynesian woman in her forties with short curly hair, simple cyan jumpsuit with glowing crescent moon LED panels, standing in a small square hover chariot of brass and glass, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** neon highway megacity under bright cyan sky with light trails
- **mid (legado):** brass gates and towers along an avenue
- **midobj (HQ):** two mechanical horse automatons, one magenta and one cyan, with glowing circuitry, standing apart left and right
- **energy:** cyan and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 08 A Justica (`08-justice`, kind=major)
- **figure:** a composed slim South African woman in her fifties with short cropped grey hair, simple blue tunic with glowing LED trim, seated frontally on a plain stone seat, holding a glowing cyan blade upright in her right hand and holographic scales in her left, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** luminous neon courthouse hall with tall windows of cyan light
- **mid (legado):** two great brass columns and arches
- **midobj (HQ):** two tall pillars with glowing balance symbols and floating data streams, left and right
- **energy:** cyan and amber
- **near:** glowing neon mushrooms and brass flowers
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 09 O Eremita (`09-the-hermit`, kind=major)
- **figure:** a slim Native American man in his seventies, clean shaven, long grey hair, simple dark hooded cloak with glowing LED seams, walking with a light staff, holding up a lantern with a glowing star inside, peaceful smile, standing on a small rocky mound, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** rainy neon alley city at night lit brightly, cyan haze and magenta signs
- **mid (legado):** old brass street lamps and dripping pipes and buildings
- **midobj (HQ):** tall glowing crystal formations and a thin LED lamp post, left and right
- **energy:** amber and cyan
- **near:** brass gears and glowing crystals
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 10 A Roda da Fortuna (`10-wheel-of-fortune`, kind=major)
- **figure:** a giant ornate brass cogwheel of fortune with glowing neon spokes and holographic symbols, a playful monkey android climbing one side, a dog android sliding down the other, a small brass sphinx automaton on top, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** swirling cosmic neon nebula over a futuristic city
- **mid (legado):** floating brass gears and clockwork machinery
- **midobj (HQ):** floating clouds with tech glyphs and four small holographic creature emblems, left and right
- **energy:** magenta and cyan
- **near:** potted bioluminescent plants in brass pots
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 11 A Forca (`11-strength`, kind=major)
- **figure:** a slim Irish woman in her fifties with short red hair, calm smile, simple black and magenta dress with glowing circuitry, lemniscate hologram over her head, gently stroking the head of a friendly mechanical lion with glowing cyan eyes, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** bright neon jungle garden city with cyan and pink sky
- **mid (legado):** brass greenhouse ruins with overgrown glowing vines
- **midobj (HQ):** flowering vines with neon blossoms on tall slender trellises, left and right
- **energy:** amber and magenta
- **near:** a brass gramophone horn and glowing musical notes
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 12 O Enforcado (`12-the-hanged-man`, kind=major)
- **figure:** a slim Arab man in his forties, clean shaven, short blue hair, simple white clothes with glowing LED lines, hanging upside down by one ankle from a light beam like an acrobat, serene smile, glowing coins falling, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** neon city of green data rain and bright cyan sky
- **mid (legado):** two tall brass pillars with gears
- **midobj (HQ):** two tall living trees with glowing circuit bark, left and right
- **energy:** cyan and green
- **near:** paint brushes and glowing color jars
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 13 A Morte (`13-death`, kind=major)
- **figure:** a tall elegant chrome android gardener with glowing magenta joints harvesting glowing flowers with a long curved harvesting blade, new sprouts at its feet, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** ruined neon city skyline under bright violet and cyan sky
- **mid (legado):** broken brass machines and ruined arches
- **midobj (HQ):** tall glowing sunflowers and dandelion seeds of light floating, left and right
- **energy:** magenta and violet
- **near:** brass beehive and glowing bees
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 14 A Temperanca (`14-temperance`, kind=major)
- **figure:** an androgynous angel of Ethiopian descent in their forties with short hair, peaceful gaze, simple white robe with glowing LED lines, holographic feathered wings, pouring glowing cyan liquid from one vessel into another, one foot on a stone, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** heavenly bright sky of pink and cyan clouds over a luminous city
- **mid (legado):** brass aqueduct arches with glowing water
- **midobj (HQ):** tall glowing irises and a small waterfall of light, left and right
- **energy:** cyan and gold
- **near:** a small brass synthesizer with glowing keys
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 15 O Diabo (`15-the-devil`, kind=major)
- **figure:** a slim theatrical Hispanic man in his fifties, clean shaven, short pink hair, small glowing LED horns, holographic bat wings, mischievous grin, simple black outfit with neon lines, standing on a small pedestal holding a glowing torch, two small horned adults loosely tied with glowing ribbons at the base, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** infernal neon city with red and magenta glowing fog
- **mid (legado):** brass furnaces and smokestacks with chains
- **midobj (HQ):** tall neon signs shaped like flames and tangled glowing cables on stands, left and right
- **energy:** red and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 16 A Torre (`16-the-tower`, kind=major)
- **figure:** a tall glass and brass tower struck by neon lightning, its roof flying off in glowing confetti, two adults gliding down with glowing parachute umbrellas, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** stormy bright magenta and cyan sky over a megacity
- **mid (legado):** distant brass skyscrapers and scaffolding
- **midobj (HQ):** jagged glowing lightning rods and falling data fragments, left and right
- **energy:** cyan and magenta
- **near:** glowing neon mushrooms and brass flowers
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 17 A Estrela (`17-the-star`, kind=major)
- **figure:** a graceful slim Black woman in her forties with a short natural haircut, simple translucent cyan tunic with glowing lines, kneeling by a glowing pool on a small mound, pouring water from two jugs, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** starry bright night sky with eight glowing stars and one large central star, cyan and pink nebula
- **mid (legado):** brass garden fountains and a mechanical tree with a small brass bird
- **midobj (HQ):** a big glowing star and small stars of light hanging high, a slim tree with a neon bird, left and right
- **energy:** cyan and pink
- **near:** brass gears and glowing crystals
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 18 A Lua (`18-the-moon`, kind=major)
- **figure:** two mechanical dogs howling up, a crayfish robot emerging from a glowing pool between them, on a small mound, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** large glowing crescent moon with a serene profile face in a cyan and magenta sky with falling droplets
- **mid (legado):** two brass towers on the left and right with neon windows
- **midobj (HQ):** two tall slender towers with glowing windows and a huge holographic moon above, left and right
- **energy:** cyan and violet
- **near:** potted bioluminescent plants in brass pots
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 19 O Sol (`19-the-sun`, kind=major)
- **figure:** a joyful adult man in his forties with short blue hair and a woman in her forties with short hair, different ethnicities, simple bright clothes with glowing LED trim, dancing hand in hand on a small mound, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** a radiant brass sun with a calm face and glowing golden rays in a bright amber and magenta sky
- **mid (legado):** rooftops and brass domes in warm light
- **midobj (HQ):** a low brick wall with neon circuitry and tall glowing sunflowers, left and right
- **energy:** amber and gold
- **near:** a brass gramophone horn and glowing musical notes
- **prop:** lantern
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 20 O Julgamento (`20-judgement`, kind=major)
- **figure:** three mature adults in simple clothes rising from an open glowing tech capsule with arms raised in awe, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** bright clouds of pink and cyan light opening in the sky
- **mid (legado):** ruined brass cathedral arches
- **midobj (HQ):** a winged angel of light blowing a trumpet with a holographic flag high above, and tall glowing antennas, left and right
- **energy:** pink and cyan
- **near:** paint brushes and glowing color jars
- **prop:** cable
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 21 O Mundo (`21-the-world`, kind=major)
- **figure:** a graceful dancing slim woman of mixed race in her forties with short hair, wrapped in a flowing magenta scarf with LED threads, holding two glowing wands, with subtle glowing LED circuit lines and small cybernetic accents
- **bg:** cosmic bright nebula with planets in magenta and cyan
- **mid (legado):** four brass automaton heads of an angel, an eagle, a lion and an ox on brass pedestals at the corners
- **midobj (HQ):** an oval wreath of glowing neon leaves and four holographic emblems in the corners, angel, eagle, bull and lion
- **energy:** magenta and cyan
- **near:** brass beehive and glowing bees
- **prop:** pipe
- **ground:** polished wet brass and stone plaza floor with glowing cyan circuit lines

### 22 As de Paus (`22-ace-of-wands`, kind=ace)
- **figure:** a single elegant hand of a mature Black woman emerging from a glowing neon cloud, gripping one large knotted glowing tech baton with glowing amber core, leaves falling, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / -
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** two tall slender holographic plant towers with neon leaves, left and right
- **energy:** amber and magenta
- **near:** a small brass synthesizer with glowing keys
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes
- **hand:** True

### 23 Dois de Paus (`23-two-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 2
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 24 Tres de Paus (`24-three-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 3
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** glowing neon mushrooms and brass flowers
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 25 Quatro de Paus (`25-four-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 4
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** brass gears and glowing crystals
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 26 Cinco de Paus (`26-five-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 5
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** potted bioluminescent plants in brass pots
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 27 Seis de Paus (`27-six-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 6
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 28 Sete de Paus (`28-seven-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 7
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** paint brushes and glowing color jars
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 29 Oito de Paus (`29-eight-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 8
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** brass beehive and glowing bees
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 30 Nove de Paus (`30-nine-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 9
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** a small brass synthesizer with glowing keys
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 31 Dez de Paus (`31-ten-of-wands`, kind=pip)
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / 10
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing antenna masts with neon vines, left and right
- **energy:** amber and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 32 Pajem de Paus (`32-page-of-wands`, kind=court)
- **figure:** a slim Native Brazilian man in his thirties, clean shaven, short pink hair, simple blue work jacket with glowing LED trim, holding a tall glowing staff planted in the ground, tending neon vines growing on it, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / -
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing staves planted in the ground with neon vines, left and right
- **energy:** amber and magenta
- **near:** glowing neon mushrooms and brass flowers
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 33 Cavaleiro de Paus (`33-knight-of-wands`, kind=court)
- **figure:** a joyful slim Moroccan woman in her forties with short hair, simple amber jumpsuit with glowing circuitry, riding a prancing mechanical horse, holding a glowing staff aloft like a torch, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / -
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing staves planted in the ground with neon vines, left and right
- **energy:** amber and magenta
- **near:** brass gears and glowing crystals
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 34 Rainha de Paus (`34-queen-of-wands`, kind=court)
- **figure:** a warm Italian woman in her fifties with a short grey bob, simple green and gold dress with LED trim, seated on a plain wooden seat, holding a tall glowing staff, a mechanical cat at her feet, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / -
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing staves planted in the ground with neon vines, left and right
- **energy:** amber and magenta
- **near:** potted bioluminescent plants in brass pots
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 35 Rei de Paus (`35-king-of-wands`, kind=court)
- **figure:** a Nigerian man in his sixties with a short white goatee, simple purple tunic with glowing lines, seated, holding a glowing staff, wise gaze, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** brass baton staff with glowing amber core and mechanical vines
- **suit/count:** wands / -
- **bg:** sunlit neon forest of brass trees and glowing embers, magenta and amber nebula sky
- **mid (legado):** brass trellis towers and wooden scaffolds with glowing vines
- **midobj (HQ):** tall glowing staves planted in the ground with neon vines, left and right
- **energy:** amber and magenta
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** rich farm soil with glowing sprouts and brass irrigation pipes

### 36 As de Copas (`36-ace-of-cups`, kind=ace)
- **figure:** a single large ornate glowing tech goblet shaped like a cathedral overflowing with glowing cyan liquid, resting on a glowing tech pedestal, symmetrical, perfect proportions, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / -
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** two tall slender holographic plant towers with neon leaves, left and right
- **energy:** cyan and magenta
- **near:** paint brushes and glowing color jars
- **ground:** shallow glowing water over brass tiles with lily pads

### 37 Dois de Copas (`37-two-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 2
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** brass beehive and glowing bees
- **ground:** shallow glowing water over brass tiles with lily pads

### 38 Tres de Copas (`38-three-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 3
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** a small brass synthesizer with glowing keys
- **ground:** shallow glowing water over brass tiles with lily pads

### 39 Quatro de Copas (`39-four-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 4
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** shallow glowing water over brass tiles with lily pads

### 40 Cinco de Copas (`40-five-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 5
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** glowing neon mushrooms and brass flowers
- **ground:** shallow glowing water over brass tiles with lily pads

### 41 Seis de Copas (`41-six-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 6
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** brass gears and glowing crystals
- **ground:** shallow glowing water over brass tiles with lily pads

### 42 Sete de Copas (`42-seven-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 7
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** potted bioluminescent plants in brass pots
- **ground:** shallow glowing water over brass tiles with lily pads

### 43 Oito de Copas (`43-eight-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 8
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** shallow glowing water over brass tiles with lily pads

### 44 Nove de Copas (`44-nine-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 9
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** paint brushes and glowing color jars
- **ground:** shallow glowing water over brass tiles with lily pads

### 45 Dez de Copas (`45-ten-of-cups`, kind=pip)
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / 10
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** slender fountains of glowing water on stands, left and right
- **energy:** cyan and magenta
- **near:** brass beehive and glowing bees
- **ground:** shallow glowing water over brass tiles with lily pads

### 46 Pajem de Copas (`46-page-of-cups`, kind=court)
- **figure:** a slim woman of Spanish descent in her forties with a short dark bob, simple long coat with LED piping, standing holding one glowing cup in both hands, dreamy gaze, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / -
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** tall stands holding glowing cups and small fountains of light, left and right
- **energy:** cyan and magenta
- **near:** a small brass synthesizer with glowing keys
- **ground:** shallow glowing water over brass tiles with lily pads

### 47 Cavaleiro de Copas (`47-knight-of-cups`, kind=court)
- **figure:** a romantic Persian man in his forties, clean shaven, short blue hair, simple white shirt with glowing lines, riding a calm mechanical horse, offering a glowing cup, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / -
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** tall stands holding glowing cups and small fountains of light, left and right
- **energy:** cyan and magenta
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** shallow glowing water over brass tiles with lily pads

### 48 Rainha de Copas (`48-queen-of-cups`, kind=court)
- **figure:** an Afro-Caribbean woman in her forties with short red curly hair, simple blue dress with glowing lines, seated, holding a covered glowing cup, tender expression, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / -
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** tall stands holding glowing cups and small fountains of light, left and right
- **energy:** cyan and magenta
- **near:** glowing neon mushrooms and brass flowers
- **ground:** shallow glowing water over brass tiles with lily pads

### 49 Rei de Copas (`49-king-of-cups`, kind=court)
- **figure:** a kind Greek man in his sixties, clean shaven, short white hair, simple blue tunic with LED trim, seated on a stone seat at the water's edge, holding a glowing cup, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** ornate brass goblet chalice glowing with cyan liquid
- **suit/count:** cups / -
- **bg:** luminous neon lagoon city with cyan water reflections, cyan and magenta nebula sky
- **mid (legado):** brass canal bridges and fountain arches
- **midobj (HQ):** tall stands holding glowing cups and small fountains of light, left and right
- **energy:** cyan and magenta
- **near:** brass gears and glowing crystals
- **ground:** shallow glowing water over brass tiles with lily pads

### 50 As de Espadas (`50-ace-of-swords`, kind=ace)
- **figure:** a single elegant hand of a mature Latino man with exactly five fingers emerging from a glowing neon cloud, holding upright one neon-edged glowing tech sword through a glowing tech crown with olive and palm branches, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / -
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** two tall slender holographic plant towers with neon leaves, left and right
- **energy:** cyan and amber
- **near:** potted bioluminescent plants in brass pots
- **ground:** windy pale stone terrace with brass inlays and blowing petals
- **hand:** True

### 51 Dois de Espadas (`51-two-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 2
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 52 Tres de Espadas (`52-three-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 3
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** paint brushes and glowing color jars
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 53 Quatro de Espadas (`53-four-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 4
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** brass beehive and glowing bees
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 54 Cinco de Espadas (`54-five-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 5
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** a small brass synthesizer with glowing keys
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 55 Seis de Espadas (`55-six-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 6
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 56 Sete de Espadas (`56-seven-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 7
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** glowing neon mushrooms and brass flowers
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 57 Oito de Espadas (`57-eight-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 8
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** brass gears and glowing crystals
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 58 Nove de Espadas (`58-nine-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 9
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** potted bioluminescent plants in brass pots
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 59 Dez de Espadas (`59-ten-of-swords`, kind=pip)
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / 10
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades, left and right
- **energy:** cyan and amber
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 60 Pajem de Espadas (`60-page-of-swords`, kind=court)
- **figure:** a sharp-eyed slim Turkish woman in her forties with short silver hair, simple dark coat with glowing seams, holding a glowing cyan blade upright like a conductor's baton, curious, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / -
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades and floating light feathers, left and right
- **energy:** cyan and amber
- **near:** paint brushes and glowing color jars
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 61 Cavaleiro de Espadas (`61-knight-of-swords`, kind=court)
- **figure:** a slim Ukrainian man in his forties, clean shaven, short blue hair, simple windbreaker with LED lines, riding a galloping mechanical horse, holding a glowing blade pointing forward like a compass, joyful, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / -
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades and floating light feathers, left and right
- **energy:** cyan and amber
- **near:** brass beehive and glowing bees
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 62 Rainha de Espadas (`62-queen-of-swords`, kind=court)
- **figure:** an elegant Jamaican woman in her fifties with short silver hair, simple pale blue dress with glowing lines, seated, holding an upright glowing blade, clear gaze, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / -
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades and floating light feathers, left and right
- **energy:** cyan and amber
- **near:** a small brass synthesizer with glowing keys
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 63 Rei de Espadas (`63-king-of-swords`, kind=court)
- **figure:** a lean Egyptian man in his sixties, clean shaven, short grey hair, simple silver tunic with LED trim, seated, holding a glowing blade, thoughtful, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** neon-edged curved brass saber sword with ornate hilt
- **suit/count:** swords / -
- **bg:** high windy neon mountain citadel with cyan sky and flowing amber clouds
- **mid (legado):** brass fortress battlements and wind turbines
- **midobj (HQ):** tall slender wind turbines with glowing blades and floating light feathers, left and right
- **energy:** cyan and amber
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** windy pale stone terrace with brass inlays and blowing petals

### 64 As de Ouros (`64-ace-of-coins`, kind=ace)
- **figure:** one very large ornate glowing tech coin engraved with a glowing magenta pentacle flower circuit, framed by mechanical vines and glowing flowers, symmetrical, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / -
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** two tall slender holographic plant towers with neon leaves, left and right
- **energy:** amber and cyan
- **near:** glowing neon mushrooms and brass flowers
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 65 Dois de Ouros (`65-two-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 2
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** brass gears and glowing crystals
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 66 Tres de Ouros (`66-three-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 3
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** potted bioluminescent plants in brass pots
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 67 Quatro de Ouros (`67-four-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 4
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 68 Cinco de Ouros (`68-five-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 5
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** paint brushes and glowing color jars
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 69 Seis de Ouros (`69-six-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 6
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** brass beehive and glowing bees
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 70 Sete de Ouros (`70-seven-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 7
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** a small brass synthesizer with glowing keys
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 71 Oito de Ouros (`71-eight-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 8
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** meditation singing bowls of brass with incense smoke
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 72 Nove de Ouros (`72-nine-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 9
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** glowing neon mushrooms and brass flowers
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 73 Dez de Ouros (`73-ten-of-coins`, kind=pip)
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / 10
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic towers with glowing leaves and coin shaped fruits, left and right
- **energy:** amber and cyan
- **near:** brass gears and glowing crystals
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 74 Pajem de Ouros (`74-page-of-coins`, kind=court)
- **figure:** a thoughtful Mexican man in his thirties, clean shaven, short pink hair, simple overalls with glowing LED trim, standing in a glowing farm plot, contemplating a glowing coin held up, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / -
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic plant towers with glowing coins growing like fruit, left and right
- **energy:** amber and cyan
- **near:** potted bioluminescent plants in brass pots
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 75 Cavaleiro de Ouros (`75-knight-of-coins`, kind=court)
- **figure:** a calm Ghanaian woman in her forties with short hair, simple work clothes with glowing lines, riding a slow mechanical horse over glowing furrows, holding a coin, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / -
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic plant towers with glowing coins growing like fruit, left and right
- **energy:** amber and cyan
- **near:** a brass gramophone horn and glowing musical notes
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 76 Rainha de Ouros (`76-queen-of-coins`, kind=court)
- **figure:** a warm Portuguese woman in her fifties with a short grey bob, simple green dress with LED trim, seated in a garden, holding a large glowing coin, warm smile, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / -
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic plant towers with glowing coins growing like fruit, left and right
- **energy:** amber and cyan
- **near:** paint brushes and glowing color jars
- **ground:** lush garden ground with moss, flowers and scattered brass gears

### 77 Rei de Ouros (`77-king-of-coins`, kind=court)
- **figure:** a Lebanese man in his sixties with a short white goatee, simple red tunic with glowing lines, seated among grape vines, holding a large glowing coin, content, with subtle glowing LED circuit lines and small cybernetic accents
- **obj:** large ornate brass coin engraved with a glowing magenta pentacle flower circuit
- **suit/count:** coins / -
- **bg:** prosperous neon market city with golden light, amber and cyan nebula sky
- **mid (legado):** brass mint buildings with domes and gears
- **midobj (HQ):** hydroponic plant towers with glowing coins growing like fruit, left and right
- **energy:** amber and cyan
- **near:** brass beehive and glowing bees
- **ground:** lush garden ground with moss, flowers and scattered brass gears

## Nota sobre PROMPTS.md antigo (modo leve)

O arquivo `/workspace/tarot-app/tecnotaro-parallax/v3/PROMPTS.md` documenta a passagem inicial (O Louco completo com seeds e negativos por camada). Mantido como referencia historica do modo pesado/leve pre-HQ. O caminho operacional atual e `gen_hq.py` + `cards_hq.json`.

## Atualizacoes futuras

Anexar secoes datadas abaixo (nova seed, mudanca de checkpoint, novo negativo, etc.). Nao apagar o registro acima. Espelhar mudancas em `cards_hq.json` / `gen_hq.py` e anotar a data aqui.

<!-- ## 2026-MM-DD - titulo -->
