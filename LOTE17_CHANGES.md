# Lote 17 - Graficos fora do duelo

## Novo
- `tools/extract_art.py` (Pillow): extrai do disco original `portraits.dat` (65 retratos: 25 dialogo + 40 duelistas), `scenes.dat` (50 cenas de fundo, modo 0) e `title.dat` (tela de titulo).
- `include/Art.h`, `source/Art.cpp`: carregamento sob demanda (sem ler o arquivo todo).
- `PixelText_Blit` para desenhar imagens indexadas.
- Tela de titulo (PRESS START -> menu principal).
- Campanha: fundo da cena (256x128), retrato 48x48 nos dialogos, caixa de texto, mapa como grafo de locais (Egito / cidade), game over e creditos.
- Menu de duelistas do Free Duel mostra o retrato do duelista selecionado.
- `tests/test_art.cpp`: 65 retratos, 50 cenas, titulo validados (0 falhas).
- ROM cresce ~1,9 MB (NitroFS).

## Limitacoes
- Cenas dos modos 1/2 (busts de personagens e cutscenes: ids 0x133..., 0x201...) ainda usam fundo degradê + "SCENE xx".
- Mapa e um grafo 2D, nao a arte 3D original.
- Arte das cartas ja existia (CardArtRenderer).
