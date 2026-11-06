# Lote 2 — o motor passa a ser dono do estado (YGOFM_DS)

Aplique SOBRE o lote 1. Depois: `make clean && make` e `bash tests/run_tests.sh`
(esperado: `36479 verificacoes, 0 falhas`). Opcional: `bash tests/check_ui_syntax.sh`.

## O que mudou
| Arquivo | Mudança |
|---|---|
| `source/DuelEngine.cpp`, `include/DuelEngine.h` | `DuelEngine_StartWithPlayerDeck`, `DuelEngine_SeedRandom`, `DuelEngine_FindPlayerHandSlotByOrder`; a CPU só invoca monstros; `SummonFromHand` recusa Magic/Trap/Ritual/Equip |
| `source/duel/DuelFieldMode.cpp`, `include/duel/DuelFieldMode.h` | deck e mão agora vêm do motor (a mão visual é espelho); invocação e fim de turno passam pelo motor; some o `playerDeck_` e as 4 funções de compra locais |
| `tests/` | +5 grupos de testes (inclui 60 duelos completos), `check_ui_syntax.sh` e stub da libnds |

## Mudanças de comportamento que você vai ver no jogo
1. **START agora termina o turno de verdade:** o motor completa sua mão, a CPU invoca o monstro de maior ATK e ataca, e o turno volta. Antes, o adversário nunca jogava.
2. **O adversário usa o deck real do duelista 0** (sorteio ponderado por pesos). Seu deck continua provisório (cartas 1 a 40, embaralhadas).
3. **Carta nova entra no lugar do buraco** da mão (slot vazio), não no fim.
4. **Duelo acabado** (LP 0 ou deck vazio): a interface bloqueia invocar e passar turno, e o painel YOU WIN / YOU LOSE (que já existia no `DuelLifePointRenderer`) aparece. SELECT reinicia. *(Correção: a versão anterior deste texto dizia, erradamente, que não havia tela de resultado.)*
5. A semente vem do relógio do DS (`time()`), então o embaralhamento varia.

## Como a interface espelha o motor
Invocar: acha o slot real da mão (`FindPlayerHandSlotByOrder`), pede `SummonFromHand` ao motor e só então redesenha. Se o motor recusar, nada mudou na tela (acabou o código de desfazer).

## Limites e riscos
- **Não compilei para ARM.** `check_ui_syntax.sh` valida sintaxe e tipos da interface com um stub, mas não linka nem roda. O primeiro teste real é o seu `make` + melonDS.
- **Não verifiquei visualmente** se o `FieldCardRenderer` desenha bem as cartas do lado do adversário (o código já sincronizava essas zonas, mas elas nunca tinham carta).
- A regra "uma carta por turno" continua na interface (`cardPlayedThisTurn_`); falta confirmar a regra original antes de movê-la ao motor.
- A escolha da estrela guardiã ao invocar **não tem controle na interface** (usa a primeira). Precisa de um elemento visual, fica para o lote 3.
- `StartExternalField`, `AdvanceExternalTurn`, `RegisterPlayerSummon` e `ClearPlayerFieldSlot` ficam sem uso no motor; removo depois que você confirmar que o jogo roda.
