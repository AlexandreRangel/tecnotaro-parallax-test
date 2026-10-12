# Tecno Tarot Parallax 2: prompts por carta e camada

Gerador: GenerateImage do Grok Bot (cerca de 1024x576). Processo: `proc.py SRC NN-slug camada modo [frac]`, depois `fin.py NN-slug` (abre o rosto na camada de energia) e `comp.py NN-slug` (gera a prévia em qa/). A publicação é feita com `publish_batch.sh NN`.
Regras gerais: figura com 85 a 95% da altura e proporção adulta real; energia saindo dos objetos, nunca sobre o rosto; mid em fundo verde #00FF00, fg em fundo preto #000000.

## 00 O Louco
- figure (modo fig 0.9): Full body standing figure on a flat pure chroma green #00FF00 background, nothing else in the background. A mature weathered traveler (the Fool tarot card), grey beard, blue hooded jester coat with brass gear ornaments, holding a tall brass staff with a glowing cyan orb, an amber lantern at his hip, boots, standing on a small patch of cobblestones. Realistic adult body proportions, about 7.5 heads tall, long legs, head not oversized. Beside his boots a small fluffy shih tzu dog with a little brass collar, looking up at him. Highly detailed face, cyberpunk steampunk illustration, bright neon magenta cyan amber rim light. Figure fills the full height of the image, centered.
- fg (modo r): Pure solid black #000000 background, no people. Abundant large glowing foreground energy: thick neon magenta and cyan plasma ribbons, amber sparks and floating light motes surging up both left and right sides and across the bottom, big swirls curling toward the viewer, a few large out-of-focus brass gears and neon butterflies in the corners. Only a central oval area in the upper middle (where a face would be) stays black and empty. Luminous cyberpunk steampunk tarot style.
- bg e mid: versões anteriores mantidas (os prompts não foram registrados).

(Novas cartas entram aqui conforme forem geradas.)
