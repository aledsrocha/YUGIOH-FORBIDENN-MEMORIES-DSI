# Lote 9 — primeiro turno, cartas viradas, magia/armadilha baixadas e armadilhas (YGOFM_DS)

Aplique SOBRE os lotes 1 a 8.1. Depois `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `40749 verificacoes, 0 falhas`), `bash tests/check_ui_syntax.sh`, `bash tests/preview/run_preview.sh`.

## O que você pediu
1. **Primeiro turno sem ataque.** Cada lado não ataca no seu primeiro turno (o jogador no turno 1, a CPU no primeiro turno dela), então ninguém perde LP na primeira rodada. Selo `1ST TURN` na tela e, se tentar atacar, o aviso `NO ATTACK ON 1ST TURN`.
2. **Monstro virado ou não.** Ao escolher a zona, **R** alterna `FACE DOWN` / `FACE UP` (etiqueta no canto). Virado = defesa escondida; revela quando ataca, é atacado ou por Swords/Dark-piercing Light. Vale para fusão também.
3. **Magia e armadilha: usar na hora ou baixar virada.** Fileira de magia/armadilha com 5 zonas por lado.

## Controles novos
| Ação | Tecla |
|---|---|
| Usar uma Magic na hora | **A** (como antes) |
| Baixar a carta destacada virada para baixo | **UP**: monstro (abre a escolha da zona já virado; **R** desliga), magia/armadilha/equip/ritual (vai para a primeira zona livre da fileira) |
| Armadilha | **A** também só baixa (armadilha não se usa na hora) |
| Alternar virado / para cima | **R**, durante a escolha da zona |
| Ativar uma magia baixada | mova o cursor (**L/R**) até ela e aperte **X** (sobre um monstro, o X continua atacando) |
Armadilhas baixadas disparam sozinhas. Cada jogada (inclusive baixar) gasta a jogada do turno.

## As 10 armadilhas (regras do jogo original)
| Carta | Efeito |
|---|---|
| House of Adhesive Tape, Eatgaboon, Bear Trap, Invisible Wire, Acid Trap Hole | quando o adversário ataca com ATK ≤ 500 / 1000 / 1500 / 2000 / 3000, o atacante é **eliminado** (vale a de menor id se mais de uma serve; também em ataque direto) |
| Widespread Ruin | elimina o atacante, qualquer que seja o ATK |
| Fake Trap | blefe: se nenhuma armadilha real serve, é gasta e **nada acontece** (a batalha segue) |
| Goblin Fan | o dano direto de uma magia do adversário **volta** para ele |
| Bad Reaction to Simochi | a cura de uma magia do adversário vira **dano** nele |
| Reverse Trap | o equip do adversário (mão ou fusão) vira **penalidade** |
Cada armadilha disparada aparece num aviso (verde se é sua, vermelho se a CPU armou contra você).
Harpie's Feather Duster agora destrói a fileira de magia/armadilha do adversário.
**O jogo original não tem efeitos de monstros** (os arquivos que eu havia visto eram do mod de PC), então não há nada a implementar ali.

## Novo deck para testar: `Y: DECK TRAPS`
No menu de duelistas, **Y** agora alterna BASIC → TEST → TRAPS. Ordem fixa do deck TRAPS: mão 1 Baby Dragon, Mystical Elf, House of Adhesive Tape, Bear Trap, Fake Trap · mão 2 Eatgaboon, Invisible Wire, Acid Trap Hole, Widespread Ruin, Time Wizard · mão 3 Raigeki, Dark Hole, Hinotama, Red Medicine, Megamorph · mão 4 Goblin Fan, Bad Reaction, Reverse Trap, Harpie, Stop Defense · o resto são monstros de ATK variados.

## O que dá para testar no jogo agora e o que não
- **Dá:** trava do primeiro turno; monstro virado; baixar magia e armadilha; ativar uma magia baixada com X; a CPU atacando para dentro das suas armadilhas (ataque, Fake Trap).
- **Ainda não:** Goblin Fan, Bad Reaction e Reverse Trap só reagem a magias e equips jogados pelo **adversário**, e a CPU ainda não os usa. Estão no motor e testados, e entram em ação com a IA. Ataques seus contra armadilhas da CPU também dependem da IA baixar cartas.

## Limites e itens não confirmados
- **Regra do primeiro turno:** vem da sua descrição do jogo; não achei trava específica no código do jogo. Implementei como *cada lado não ataca no seu primeiro turno* (você no turno 1 e a CPU no primeiro turno dela).
- Não confirmei no original: fusão baixada virada; ativar magia baixada depois (X sobre ela); armadilha disparar também em ataque direto; equip e ritual baixados não se ativam (só jogados da mão).
- A CPU ainda não baixa cartas nem invoca virada; isso vem com a IA.
- A fileira de magia/armadilha usa as zonas que o campo já tinha; **não vi na tela real** como o renderizador desenha a carta virada nessas zonas.
- Não compilei para ARM; posições dos avisos escolhidas a olho.
