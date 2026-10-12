# Tecnotarô Parallax: plano de integração no app iOS (SwiftUI)

Deck completo: 78 cartas, quatro camadas cada (frame, bg, mid, fg), em `deck/`, com `deck/manifest.json` global.
Viewer de teste (todas as cartas): https://alexandrerangel.github.io/tecnotaro-parallax-test/ (deep link `#NN`).

## 0. Regra de produção: faixas de profundidade (v2, vale para as 78 cartas)

Na v1 a figura flutuava: o chão fazia parte do bg e se movia, a figura não. Regra atual:

| camada | conteúdo | depth | movimento |
|---|---|---|---|
| bg | longe: céu, cidade, tudo acima da linha do chão | -0.025 | o maior, sentido oposto à inclinação |
| mid | figura(s) + faixa de chão sob e ao redor dos pés (largura total, borda superior em degradê) + sombras de contato embutidas | 0 | parado: é a âncora (plano zero) |
| fg | partículas neon esparsas, elementos pequenos de canto | +0.012 | pequeno, a favor da inclinação |
| frame | moldura + título | fixo | nenhum |

- Deslocamento = inclinação (-1..1, com clamp) x depth x largura da janela, nos dois eixos.
- Figura e chão nunca se separam: estão no mesmo arquivo.
- Transição chão/fundo por carta (`ground_edge` no manifest, com `edge_y` em fração da altura da janela):
  - `hard` (21 cartas): corte ao longo de uma borda real da imagem (balaustrada, beirada de plataforma, mureta, meio-fio, horizonte, borda da água). A linha segue, coluna a coluna, o gradiente vertical mais forte a +-35 px de `edge_y`, suavizada; recebe um aro claro de 2 px e uma sombra curta sob o lábio.
  - `fade` (16 cartas): degradê suave (span padrão 9% da altura), para chão sem borda definida (chuva, névoa, vegetação).
  - `none` (41 cartas): pips, Ases e emblemas (e o Enforcado): o emblema ou a mão é o plano mid, céu/nebulosa é o bg.
  - Escolha automática: `hard` se a mediana do gradiente na linha candidata (só colunas sem figura) for > 3x a mediana da faixa; senão `fade`. Sobrescrita manual em `src/overrides.json`.
- Anel de 22 px em volta da figura (pixels originais, alfa decrescente) faz parte do mid: em repouso a composição é igual à carta plana.
- Sombras de contato: elipses suaves sob cada bota/pata, detectadas pela base da máscara, escurecendo só o chão (nunca a figura).
- Limite anti-halo por carta: |depth bg| x largura da janela <= 0.95 x `halo_margin_px`, onde margin = anel (22 px) + tolerância que diminui com o tamanho da área reconstruída (40 px emblemas; 30/22/12 px figuras conforme `hole_frac` < 0.18 / < 0.30 / maior). Resultado: bg entre -0.017 e -0.030; fg = 0.48 x |bg|.
- Cartas sem chão (figura no céu, ex. The Star, The World): mid = figura + nuvem/elemento de apoio; ou figura com depth 0 e bg com amplitude menor.

## 1. Pacote final

```
tecnotaro-parallax/deck/
  manifest.json                 # global: janela, overscan, regra, tabela ground_edges, e cards[] (um card.json por carta)
  00-the-fool/
    frame.webp  frame@2x.webp   # 1120x1920 / 2240x3840, moldura + título, janela transparente, fixa
    bg.webp     bg@2x.webp      # 1041x1700 / 2081x3399 (janela x 1.10), plano de fundo
    mid.webp    mid@2x.webp     # 946x1545 / 1892x3090 (janela), figura/emblema + chão + sombras
    fg.webp     fg@2x.webp      # tamanho da janela, partículas, blend screen
    thumb.webp                  # 200x343 para índice
    card.json                   # id, index, title, suit, kind, ground_edge, edge_y, foot_y, contacts, hole_frac, halo_margin_px, depth{bg,mid,fg,frame}
  ... 77-king-of-coins/
```

Exemplo de `card.json`:

```json
{"id":"19-the-sun","index":19,"title":"THE SUN","suit":"major","kind":"figure","ground_edge":"hard","edge_y":0.6104,
 "halo_margin_px":52,"depth":{"bg":-0.025,"mid":0.0,"fg":0.012,"frame":0.0}}
```

- No app: copiar `deck/` como folder reference (WebP é suportado nativamente por UIImage desde iOS 14), ou converter para HEIC em um Asset Catalog por carta. Peso total: @1x cerca de 53 MB, @1x+@2x cerca de 200 MB; usar On-Demand Resources por naipe (tags `major`, `wands`, `cups`, `swords`, `coins`) ou baixar @2x sob demanda.
- `manifest.json` global decodificado com `Codable` (`cards[]` traz as profundidades de cada carta; não há valores fixos no código).
- Profundidade = fração da janela que a camada percorre com inclinação máxima. Negativo = sentido oposto (bg). Valores por carta em `card.json`/`manifest.json`.

## 2. Movimento: CoreMotion

```swift
import CoreMotion, SwiftUI

@MainActor final class Tilt: ObservableObject {
    @Published var x: Double = 0, y: Double = 0          // -1...1, suavizado
    private let mm = CMMotionManager()
    private var ref: CMAttitude?
    private var tx = 0.0, ty = 0.0
    let maxRad = 22.0 * .pi / 180, lerp = 0.12

    func start() {
        guard mm.isDeviceMotionAvailable else { return }
        mm.deviceMotionUpdateInterval = 1.0 / 60
        mm.startDeviceMotionUpdates(using: .xArbitraryZVertical, to: .main) { [weak self] m, _ in
            guard let self, let a = m?.attitude.copy() as? CMAttitude else { return }
            if self.ref == nil { self.ref = a }                 // recentra na primeira leitura
            a.multiply(byInverseOf: self.ref!)
            self.tx = max(-1, min(1, a.roll  / self.maxRad))
            self.ty = max(-1, min(1, a.pitch / self.maxRad))
            self.x += (self.tx - self.x) * self.lerp
            self.y += (self.ty - self.y) * self.lerp
        }
    }
    func recenter() { ref = nil }
    func stop() { mm.stopDeviceMotionUpdates() }
}
```

- Não precisa de permissão no iOS para device motion (diferente da web). Não exige `NSMotionUsageDescription` para attitude.
- Recentrar ao abrir a carta e num toque duplo. Opcional: deriva lenta de volta ao centro (`ref` interpolado) para quem segura o telefone em ângulos diferentes.

## 3. View em camadas

```swift
struct ParallaxCard: View {
    let m: CardManifest            // decodificado do manifest.json
    @StateObject var tilt = Tilt()
    @Environment(\.accessibilityReduceMotion) var reduceMotion

    var body: some View {
        GeometryReader { g in
            let s = g.size.width / m.canvas.w          // escala canvas -> pontos
            let win = m.window.rect.scaled(s)
            let x = reduceMotion ? 0 : tilt.x, y = reduceMotion ? 0 : tilt.y
            ZStack(alignment: .topLeading) {
                ZStack {
                    Image(m.asset("bg")).resizable()
                        .frame(width: win.width * 1.10, height: win.height * 1.10)
                        .offset(x: x * m.depth.bg * win.width, y: y * m.depth.bg * win.width)
                    Image(m.asset("mid")).resizable()            // âncora: sem offset
                    Image(m.asset("fg")).resizable()
                        .blendMode(.screen)
                        .offset(x: x * m.depth.fg * win.width, y: y * m.depth.fg * win.width)
                }
                .frame(width: win.width, height: win.height)
                .clipShape(RoundedRectangle(cornerRadius: win.width * 0.04))
                .offset(x: win.minX, y: win.minY)
                Image(m.asset("frame")).resizable()           // fixa
            }
            .aspectRatio(7/12, contentMode: .fit)
            .rotation3DEffect(.degrees(reduceMotion ? 0 : y * -4), axis: (1, 0, 0), perspective: 0.4)
            .rotation3DEffect(.degrees(reduceMotion ? 0 : x *  4), axis: (0, 1, 0), perspective: 0.4)
            .drawingGroup()                                    // compõe no Metal, um único layer
        }
        .onAppear { if !reduceMotion { tilt.start() } }
        .onDisappear { tilt.stop() }
        .onTapGesture(count: 2) { tilt.recenter() }
    }
}
```

## 4. Desempenho

- Ligar CoreMotion só na carta visível (onAppear/onDisappear); parar em background (`scenePhase`).
- 60 Hz é suficiente; em ProMotion, 60 Hz de sensor com interpolação na view basta.
- `drawingGroup()` ou um `TimelineView(.animation)` lendo o estado evita recomputar o layout inteiro a cada amostra. Alternativa mais leve: `CALayer` por camada com `transform` atualizado em `CADisplayLink` (sem SwiftUI diff).
- Memória: 4 camadas 2240x3840 RGBA ocupam cerca de 34 MB cada decodificadas. Em tela de iPhone usar 1120x1920 (@2x) ou downsample com `ImageIO` (`kCGImageSourceThumbnailMaxPixelSize`) ao tamanho real em pixels. Manter só a carta atual e as vizinhas em cache.
- `fg` e `frame` são majoritariamente transparentes: recortar ao bounding box e posicionar pelo manifest reduz memória e overdraw.
- Na grade/lista de cartas usar o PNG achatado (carta final), nunca as camadas.

## 5. Acessibilidade

- `accessibilityReduceMotion` = verdadeiro: não iniciar CoreMotion, offsets 0, sem rotação 3D (mostra a carta montada, idêntica à versão plana).
- Ajuste no app: "Efeito de profundidade" liga/desliga, independente do sistema.
- `accessibilityLabel` com o nome da carta na view inteira; camadas marcadas `.accessibilityHidden(true)`.
- Sem flashes: partículas do fg são estáticas na imagem; se animar no futuro, manter lento e de baixo contraste.

## 6. Pipeline de produção (implementado)

Scripts em `src/` (rodar com o venv que tem rembg: `/workspace/.venv-rembg/bin/python`):

1. `build_card.py 0-77` : para cada carta de `tecnotaro/cartas/en` (somente leitura): frame com alfa da moldura; máscara rembg isnet-general-use (passadas extras em caixas de `overrides.json` para corrigir recortes ruins, `drop_boxes`/`keep_boxes` para limpar); detecção do chão (`hard`/`fade`/`none`); sombras de contato; bg com remoção da figura, inpaint multi-escala e textura emprestada, overscan 10%; fg com paleta por naipe (maiores magenta/ciano/âmbar, paus âmbar/laranja, copas ciano/magenta/violeta, espadas ciano/branco, ouros dourado/verde/rosa), nunca sobre a figura; clamp de amplitude; webp @1x/@2x; `card.json`; jpgs de QA. Retoma de onde parou (pula cartas com `card.json`; `--force` refaz).
2. `sheets.py AA BB` : contact sheets `qa/sheet-mid-AA-BB.jpg` (mid sobre xadrez) e `qa/sheet-comp-AA-BB.jpg` (inclinação -1 | repouso | +1). `qa/sheet-hard-edges.jpg` mostra as bordas `hard`.
3. `make_manifest.py` : `deck/manifest.json` global e miniaturas.
4. Revisão visual de cada lote; corrigir em `overrides.json` e refazer só as cartas afetadas.
5. Com GenerateImage disponível: substituir o bg reconstruído por uma placa gerada sem personagens (mesma composição), o que permite subir a amplitude do bg para cerca de -0.035.
