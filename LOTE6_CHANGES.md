# Lote 6 — interface: fusão em cadeia, equip e terreno (YGOFM_DS)

Aplique SOBRE os lotes 1 a 5. Depois `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `39327 verificacoes, 0 falhas`), `bash tests/check_ui_syntax.sh`
e `bash tests/preview/run_preview.sh` (gera PNGs dos painéis em `build_tests/preview/`).

## Controles novos (com uma carta da mão destacada, fora de invocação/ataque)
| Tecla | Efeito |
|---|---|
| **Y** | marca/desmarca a carta para fusão (a ordem de marcação é a ordem da fusão) |
| **BAIXO** ou **B** | limpa as marcações |
| **A** com cartas marcadas | começa a invocação do **resultado da fusão**: escolha a zona (ESQ/DIR), X ataque / Y defesa, A confirma; CIMA/BAIXO troca a estrela |
| **A** sobre carta de terreno (Forest, Wasteland, Mountain, Sogen, Umi, Yami) | joga na hora e ativa o terreno |
| **A** sobre carta de equip | escolhe o monstro em campo: ESQ/DIR troca o alvo, A equipa, B cancela |

Os outros controles não mudaram.

## Painéis (tela de cima, só quando relevantes)
- **Fusão:** `FUSE 1>2>3` (posições da mão na ordem marcada; vira `FAIL` se algum passo não funde), nome do resultado (17 letras) e ATK/DEF com equips e terreno. `NOT A MONSTER` se o resultado não for monstro (não dá para jogar).
- **Equip:** nome do equip, monstro-alvo e ATK/DEF antes e depois.
- **Selo do terreno:** sempre que há terreno ativo, no vão entre o LP da CPU e o painel de estrelas.

## Mudanças no motor
`DuelEngine_PreviewFuseChain`: simula a cadeia sem alterar nada. A jogada real usa a mesma avaliação, então o painel sempre concorda com o resultado. Mais 4 símbolos na fonte (`'`, `#`, `,`, `!`).

## Limites
- **Não compilei para ARM; não vi a tela real.** Os painéis estão em posições escolhidas a olho (constantes em `source/duel/DuelOverlays.cpp`: `kInfoPanelX/Y`, `kBadgeX/Y`, `kStarPanelX/Y`); se cobrirem algo importante, me diga onde.
- A regra "uma jogada por turno" (`cardPlayedThisTurn_`, que já existia) vale também para fusão, terreno e equip. **Não consegui confirmá-la no código do jogo**; se o original permitir mais de uma jogada, é só mudar essa regra.
- Nomes longos aparecem cortados nos painéis (a fonte é larga).
- Não verifiquei se o `FieldCardRenderer` mostra os bônus de equip nas cartas do campo; o ATK/DEF certo aparece no painel e vale no combate.
