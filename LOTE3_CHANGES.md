# Lote 3 — jogabilidade: menu de duelistas e escolha de estrela (YGOFM_DS)

Aplique SOBRE os lotes 1 e 2. Depois: `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `38182 verificacoes, 0 falhas`),
`bash tests/check_ui_syntax.sh` e, para ver o resultado, `bash tests/preview/run_preview.sh`
(gera PNGs em `build_tests/preview/`).

**Correção do lote 2:** o `LOTE2_CHANGES.md` dizia que não havia tela de vitória/derrota. Havia:
o `DuelLifePointRenderer` já desenha YOU WIN / YOU LOSE. Este zip traz o texto corrigido.

## O que entrou
1. **Menu de duelistas** (39 duelistas reais), exibido ao abrir o jogo.
2. **Escolha da estrela guardiã** ao invocar, com painel mostrando o confronto com o campo do adversário.
3. **Fonte 3x5 completa** (A–Z, 0–9 e alguns símbolos) em módulo próprio, base para qualquer texto novo.

## Controles
| Situação | Tecla | Efeito |
|---|---|---|
| Menu | CIMA / BAIXO | duelista anterior / próximo (dá a volta) |
| Menu | L / R | pula 8 |
| Menu | A ou START | inicia o duelo |
| Duelo | SELECT | volta ao menu, já no duelista atual (A = revanche) |
| Duelo terminado | START | abre o menu |
| Invocando (escolhendo zona ou confirmando) | CIMA / BAIXO | alterna a estrela da carta (só se ela tiver duas diferentes) |

O resto (A, B, X, Y, L, R, START para passar o turno) continua como no lote 2.

## Painel de estrelas
Canto superior direito, só durante a invocação. `>` marca a estrela escolhida; a linha `VS +n -m` diz contra quantos monstros **visíveis** do adversário ela vence (+) e perde (−). A escolha vira definitiva ao confirmar a invocação (`DuelEngine_SetGuardianStar`). A CPU sempre usa a primeira estrela.

## Arquivos
Novos: `include/duel/{PixelFont,PixelText,ListMenu,DuelOverlays}.h`, `source/duel/{PixelFont,PixelText,DuelOverlays}.cpp` (o `Makefile` já compila tudo de `source/duel`).
Alterados: `DuelEngine.h/.cpp` (`DuelEngine_GuardianStarName`, `DuelEngine_CountStarMatchups`), `DuelFieldMode.h/.cpp`.
Testes: fonte (todos os glifos distintos; todos os nomes de duelista têm glifo), navegação do menu (a janela sempre contém o item) e confrontos de estrela.

## Limites (o que eu não consegui verificar)
- **Não compilei para ARM.** A sintaxe e os tipos de todos os arquivos de interface passam num stub da libnds, mas o teste real é o seu `make` + melonDS.
- **Não vi a tela real do campo.** O painel de estrelas está em (152, 4), espelhando o painel de LP da CPU em (4, 4). Se sobrepor algo importante, ajuste `kStarPanelX/Y` em `source/duel/DuelOverlays.cpp`. As imagens de prévia usam um fundo verde provisório.
- As estrelas **não aparecem sobre as cartas no campo**: isso depende da geometria do `FieldCardRenderer`, que não alterei.
- O deck do jogador continua provisório (cartas 1 a 40). Falta tela de montagem de deck.
- A tabela de estrelas e o bônus de +500 seguem a documentação da comunidade e ainda precisam ser confirmados no executável original.
