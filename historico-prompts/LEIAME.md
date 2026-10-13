# Historico de prompts e modelos: Tecnotarô (parallax)

Indice versionado dos prompts, modelos e regras de estilo usados nos baralhos Tecnotarô 3D de Alexandre Rangel.

**Regra permanente:** qualquer mudanca futura de prompt, modelo, sampler, negativo ou regra de estilo global deve ser **anexada** neste historico (nova secao datada no arquivo da versao correspondente e nova linha na tabela de changelog abaixo). Nao sobrescrever prompts antigos: registrar a evolucao.

Ortografia: portugues (pt-BR). Evitar travessoes tipograficos: usar virgula ou hifen curto.

## Arquivos

| Arquivo | Baralho | Pasta / destino | Ferramenta |
|---|---|---|---|
| [grok-v1.md](grok-v1.md) | Tecno Tarô 3D 1 | repo `deck/` (publicado em `v1/`), box `/workspace/tarot-app/tecnotaro-parallax/deck` | Grok GenerateImage + separacao em camadas |
| [grok-v2.md](grok-v2.md) | Tecno Tarô 3D 2 | repo `v2/`, box `/workspace/tarot-app/tecnotaro-parallax/v2` | Grok GenerateImage + `proc.py` / `look.py` / `fin.py` / `finish.sh` |
| [comfy-v3.md](comfy-v3.md) | Tecno Tarô 3D 3 (ComfyUI HQ) | repo `v3/`, box scripts + PC Blackwell `C:\\tecno_v3hq\\` | ComfyUI, Juggernaut XL Ragnarok SDXL, `gen_hq.py` |

Referencia de versoes de baralho: `/workspace/tarot-app/midia/decks/LEIAME-versoes.md` e Dropbox `/tarot-app/midia/decks/`.

## Estrutura de camadas (resumo)

| Versao | Camadas moveis (tras -> frente) | Moldura | Observacao |
|---|---|---|---|
| 3D 1 (v1) | bg, mid (figura + faixa de chao), fg | frame fixa | 3 moveis + frame |
| 3D 2 (v2) | bg, mid, figure, fg | frame fixa | 4 moveis + frame (muitas cartas com mid vazio, aura do fin.py) |
| 3D 3 (v3 HQ) | bg, mid, figure, energy | frame fixa | 4 moveis + frame; mid = objetos destacados atras do personagem |

## Changelog (por data)

| Data (America/Sao_Paulo) | Versao | Mudanca |
|---|---|---|
| 11/10/2026 | Tecno Tarô 1 (estatico) | Baralho estatico completo 78/78 com Grok GenerateImage. Base iconografica Marselha Conver. |
| ~11-12/10/2026 | 3D 1 | Parallax a partir das imagens Grok: moldura fixa, fundo, figura com chao, energia frontal. 78 cartas. |
| 12/10/2026 | 3D 2 | Pipeline Grok por camada (figure em chroma verde, fg em preto, bg crop). Publicacao progressiva 00-35. `fin.py` reforca fg_final e aura em mid. `look.py` + `finish.sh` com opcoes por carta. |
| 12/10/2026 | estilo global | Regras: sem guerra/militar, corpos esbeltos, mulheres de cabelo curto, temas transhumanismo, cultivation, meditacao, musica, artes. Neon magenta/ciano/ambar, latão. |
| 12/10/2026 | 3D 3 (Comfy, leve) | Primeira passagem ComfyUI no Blackwell (Juggernaut XL Ragnarok). Cartas 00-01 modo pesado; a partir da 02 modo leve (sem upscale 4x GPU). So O Louco publicado no GitHub na epoca. Pausado por BSOD. |
| 13/10/2026 | 3D 3 HQ | Pipeline HQ `gen_hq.py` + `cards_hq.json` em `C:\\tecno_v3hq\\` e espelho em `v3/src/`. Renders verticais 1024x1664 -> upscale 4xNomos -> hires 1600x2600. mid = objetos destacados atras do personagem, renderizados a parte em chroma/cinza. Roupas humildes (exceto Imperador, Imperatriz, Mago). Homens modernos, alguns com cabelo azul/rosa, poucas barbas. Mais tech/neon, geometria sagrada, arquitetura, Blade Runner techno-noir. |
| 13/10/2026 | historico-prompts/ | Criacao desta pasta no repo `tecnotaro-parallax-test` e copia para Dropbox `/tarot-app/midia/decks/historico-prompts/`. |

## Fontes consultadas

- `/workspace/tarot-app/midia/decks/LEIAME-versoes.md`
- `/workspace/tarot-app/tecnotaro-parallax/v2/PROMPTS.md`, `SPEC.md`, `finish.sh`, `look.py`, `fin.py`, `proc.py`
- `/workspace/tarot-app/tecnotaro-parallax/v3/PROMPTS.md`, `work/gen.py`
- `/workspace/tecnotaro-parallax-test/v2/PROMPTS.md`, `v2/SPEC.md`, `v3/SPEC.md`, `v3/src/gen_hq.py`, `v3/src/cards_hq.json`, `v3/src/v3_build_hq.py`
- PC Blackwell (somente leitura): `C:\\tecno_v3hq\\gen_hq.py`, `C:\\tecno_v3hq\\cards_hq.json` (nao interromper renders em andamento)
- `/workspace/tarot-app/tecnotaro/LEIAME.md` (baralho estatico 1)
- `/workspace/tarot-app/tecnotaro-parallax/PLANO-INTEGRACAO.md` (camadas v1)

## Como atualizar

1. Editar o arquivo da versao (`grok-v1.md`, `grok-v2.md` ou `comfy-v3.md`).
2. Acrescentar secao datada `## YYYY-MM-DD - descricao` com o diff de prompt/modelo/regra.
3. Acrescentar linha na tabela de changelog deste LEIAME.md.
4. Commit so de `historico-prompts/` no repo; espelhar no Dropbox.
