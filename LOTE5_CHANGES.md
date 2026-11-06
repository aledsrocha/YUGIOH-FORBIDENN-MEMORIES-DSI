# Lote 5 — cadeia de fusão, equips e terrenos no motor (YGOFM_DS)

Aplique SOBRE os lotes 1 a 4 (copie para a raiz). Depois `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `39303 verificacoes, 0 falhas`).

## O que entrou (tudo em `DuelEngine`, com testes)
| API | O que faz |
|---|---|
| `DuelEngine_FuseChainFromHand(slots, n, campo, posição)` | cadeia de fusão de 1 a 5 cartas da mão, regras de `Fusion_Step` do jogo (fusão, equip, falha) |
| `DuelEngine_GetEquipBonus(id)` | +500; **Megamorph (657) dá +1000** (antes era +500 para todos) |
| `DuelEngine_PlayFieldMagicFromHand(slot)` | jogar Forest, Wasteland, Mountain, Sogen, Umi ou Yami ativa o terreno |
| `DuelEngine_GetCardEffectGroup(id)` | grupo de efeito de cada magia/armadilha/ritual (tabela do original) |

### Regras da cadeia (portadas de `Fusion_Step`)
As cartas escolhidas combinam da esquerda para a direita. Em cada passo: (1) se existe fusão, nasce o monstro novo e ele **perde os bônus de equip anteriores**; (2) senão, um equip compatível se aplica ao monstro; (3) senão a fusão falha e fica a carta nova, exceto quando a nova é magia e a atual é monstro (fica o monstro). Todas as cartas escolhidas saem da mão. O resultado final precisa ser um monstro.

## O que ainda NÃO está ligado à interface
Escolher várias cartas em ordem, jogar equip sobre monstro em campo e jogar carta de terreno **ainda não têm controle na tela**: é o próximo lote (interface). O motor já aceita e está testado.

## Também neste zip
`MAPA_MAGIAS.md`: todas as magias, armadilhas e rituais agrupados por efeito, o roteiro do lote de magias.
