# Tecno Tarô 3D 1 - historico de prompts (Grok)

## Identificacao

| Campo | Valor |
|---|---|
| Nome oficial | Tecno Tarô 3D 1 |
| Pasta publicada | `v1/` no repo `tecnotaro-parallax-test` (origem: `deck/` na raiz de tecnotaro-parallax) |
| Ferramenta | Grok GenerateImage |
| Pipeline | Imagens geradas (ou derivadas do baralho estatico Tecno Tarô 1) e separadas em camadas por script |
| Status | Completo, 78 cartas |
| Datas | Base estatica concluida 11/10/2026; parallax 3D 1 em seguida (~11-12/10/2026) |
| Link | https://alexandrerangel.github.io/tecnotaro-parallax-test/v1/ |

Nota: o `manifest.json` desta versao usa `"version": 3` (esquema interno do manifesto, nao a versao do baralho).

## Camadas (3 moveis + frame)

Ordem de tras para frente (fonte: `PLANO-INTEGRACAO.md`):

| Camada | Conteudo | Depth tipico | Movimento |
|---|---|---|---|
| bg | Longe: ceu, cidade, tudo acima da linha do chao | cerca de -0.025 | maior, oposto a inclinacao |
| mid | Figura(s) + faixa de chao sob os pes + sombras de contato | 0 | ancora (plano zero) |
| fg | Particulas neon, elementos pequenos de canto | cerca de +0.012 | pequeno, a favor da inclinacao |
| frame | Moldura + titulo | fixo | nenhum |

Canvas: carta 1120x1920 (@1x) / 2240x3840 (@2x), aspecto 7:12. Janela de arte dentro da moldura.

Regra de producao v1: figura e chao nunca se separam (mesmo arquivo mid). Transicao chao/fundo por carta (`ground_edge`: hard / fade / none).

## Modelo / ferramenta

- Geracao: Grok Bot, GenerateImage.
- Estilo herdado do Tecno Tarô 1 (estatico): cyberpunk Blade Runner com toques steampunk, neon magenta, ciano e ambar, detalhes em latao. Iconografia Tarô de Marselha (Conver, 1760).
- Personagens: generos misturados, etnias variadas.
- Formato de entrega: WebP por camada em `deck/NN-slug/`.

## Prompts por carta

Os prompts textuais por carta desta versao **nao foram arquivados** de forma sistematica (a geracao era imagem unica ou reaproveitamento do estatico, depois fatiada em camadas). O baralho estatico Tecno Tarô 1 (`/workspace/tarot-app/tecnotaro/`) tambem nao possui um arquivo PROMPTS.md completo por carta.

Para prompts detalhados por camada, ver a evolucao em [grok-v2.md](grok-v2.md).

## Evolucao de estilo (contexto)

Ate a 3D 1, o foco era neon cyberpunk/steampunk luminoso, sem o pacote de regras de 12/10 e 13/10 ainda formalizado (sem guerra, corpos esbeltos, etc.). Essas regras entram de forma explicita no historico a partir da 3D 2 / 3D 3 HQ.

## Apêndice: regras de movimento (resumo)

- Deslocamento = inclinacao (-1..1) x depth x largura da janela.
- Anel de ~22 px em volta da figura faz parte do mid.
- Limite anti-halo: |depth bg| limitado pela margem de halo da carta.

## Atualizacoes futuras

Anexar abaixo secoes datadas. Nao apagar o texto acima.

<!-- exemplo:
## 2026-MM-DD - titulo
- mudanca...
-->
