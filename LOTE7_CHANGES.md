# Lote 7 — magias (YGOFM_DS)

Aplique SOBRE os lotes 1 a 6. Depois `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `39488 verificacoes, 0 falhas`), `bash tests/check_ui_syntax.sh`
e `bash tests/preview/run_preview.sh` (PNGs dos avisos em `build_tests/preview/`).

## Como jogar uma magia
Destaque a carta Magic na mão e aperte **A**: ela é jogada na hora. Aparece um aviso no meio da tela com o resultado
(`3 DESTROYED`, `YOU RECOVER 500 LP`...); qualquer tecla fecha. Conta como a jogada do turno.

## As 33 cartas Magic do jogo, todas implementadas (`DuelEngine_PlaySpellFromHand`)
| Efeito | Cartas | Regra (valores e textos conferidos no próprio jogo) |
|---|---|---|
| Terrenos | Forest, Wasteland, Mountain, Sogen, Umi, Yami | ativa o terreno (±500 por tipo) |
| Cura | Mooyan Curry, Red Medicine, Goblin's Secret Remedy, Soul of the Pure, Dian Keto | +200 / 500 / 1000 / 2000 / 5000 LP, até o máximo de 8000 |
| Dano direto | Sparks, Hinotama, Final Flame, Ookazi, Tremendous Fire | 50 / 100 / 200 / 500 / 1000 de dano no adversário |
| Dark Hole | | destrói todos os monstros, dos dois lados |
| Raigeki | | destrói todos os monstros do adversário |
| Dragon Capture Jar | | destrói os Dragões do adversário |
| Remoção por tipo | Warrior Elimination, Eternal Rest, Stain Storm, Eradicating Aerosol, Breath of Light, Eternal Draught | destrói os monstros do adversário do tipo (Warrior, Zombie, Machine, Insect, Rock, Fish) |
| Crush Card | | destrói os monstros do adversário com ATK ≥ 1500 (contando equips, penalidades e terreno) |
| Stop Defense | | monstros do adversário em defesa passam a ataque |
| Dark-piercing Light | | revela os monstros virados para baixo |
| Spellbinding Circle / Shadow Spell | | ATK e DEF de todos os monstros do adversário −500 / −1000 (acumula, piso em 0) |
| Swords of Revealing Light | | revela os monstros do adversário e ele **não ataca por 3 turnos** (contador 4, cai 1 no início de cada turno dele) |
| Cursebreaker | | zera os modificadores **negativos** dos seus monstros (equips ficam) |
| Harpie's Feather Duster | | destrói magias/armadilhas do adversário em campo (**ainda não há nenhuma**, então só é consumida) |

Dano direto que zera o LP termina o duelo. Selos na tela: `SWORDS n` (adversário) e `NO ATK n` (você).

## Mudanças no motor
`DuelPlayerState.swordsTurnsRemaining`, `DuelEngine_PlaySpellFromHand`, `DuelEngine_GetSwordsTurns`. O contador de Swords também bloqueia o ataque da CPU e o seu.

## O que eu não consegui confirmar (leia)
- **De que lado cada magia atua.** Usei o texto de cada carta (`cards.dat`, que vem do próprio jogo): "opponent"/"opposing"/"enemy" nas de remoção, Raigeki, Stop Defense, Spellbinding, Shadow Spell e Swords; Dark Hole e Dark-piercing Light nos dois lados. **Eternal Rest** diz só "Eliminates all Zombie creatures": apliquei como as outras (lado do adversário), porque o código do jogo usa a mesma rotina. **Cursebreaker** atua nos seus monstros (é uma cura); o código decompilado não deixa claro o lado.
- A regra "uma jogada por turno" continua sendo a da interface (vale também para magias); não confirmei no original.
- **A CPU ainda não usa magias.** E a IA atual ataca monstros mais fortes, ferindo a si mesma (visto nos testes): fica para o lote da IA.
- Não compilei para ARM; posição do aviso e dos selos escolhida a olho (constantes em `source/duel/DuelOverlays.cpp`). Nomes longos aparecem cortados.
