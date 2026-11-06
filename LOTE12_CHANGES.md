# Lote 12 - rank, recompensas e correcao da fileira de magia/armadilha

## 1. Correcao: selecionar cartas da fileira de magia/armadilha
Causa: o cursor do campo so andava na horizontal (a seta CIMA/BAIXO e usada para marcar cartas da mao), entao as zonas de magia/armadilha nunca eram alcancadas.
Agora, fora da escolha de invocacao, **L/R** percorrem as 10 zonas proprias: 5 de monstro e depois 5 de magia/armadilha.
Em cima de uma carta baixada, **X/A** faz o que o original faz: magia e usada; equip pede o monstro alvo; ritual e usado; armadilha avisa que dispara sozinha.
Pendente (anotado): escolher a zona da fileira ao baixar (hoje vai para a primeira livre) e confirmacao sim/nao antes de usar.

## 2. Rank do duelo (fiel ao codigo decompilado)
Nota = 50 + ajuste + soma de 10 regras (tabela `gDuel_awRankScoreChange`, igual para os 39 duelistas):

| Regra | Contador | Quando conta |
|---|---|---|
| Turnos | `turnsTaken` | cada turno iniciado do lado |
| Ataques eficazes | `rank.effectiveAttacks` | ataque que destroi monstro em ataque causando dano |
| Vitorias defensivas | `rank.defensiveWins` | defesa vence o atacante (conta para o defensor) |
| Baixadas viradas | `rank.faceDownPlays` | carta unica baixada virada (monstro, magia, armadilha); fusao nao conta |
| Magias puras | `rank.pureMagicUsed` | magia usada da mao ou da fileira |
| Armadilhas | `rank.trapsTriggered` | armadilha disparada (conta para o dono da armadilha) |
| Cartas usadas | `deck.drawIndex` | cartas compradas do deck |
| LP restante | `lifePoints` | |
| Fusoes | `rank.fusionsInitiated` | passos de fusao da cadeia |
| Equips | `rank.equipsUsed` | passos de equip (cadeia, mao, fileira) |

Ajuste do vencedor: +2 vitoria por LP, +40 Exodia, -40 deck vazio.
Letra: abaixo de 50 e TEC (espelhado em 99 - nota, minimo 0); 50 ou mais e POW; `(nota-50)/10` = D, C, B, A, S.
Exemplo conferido: inicio de duelo com vitoria por LP = 101 = S-POW.

## 3. Recompensa
- So se o jogador vence: **star chips = tier + 1** (D=1 ... S=5).
- Piscina da carta: tier A/S (3,4): SA-POW se POW, SA-TEC se TEC; D/C/B: BCD-POW.
- Sorteio: `(rand() & 2047) + 1` contra a soma acumulada dos 722 pesos do duelista (cada piscina soma 2048 - testado nos 39 duelistas).
- O resultado e fechado uma vez por duelo (`DuelEngine_GetResult`).

## 4. Tela de resultado e perfil em memoria
Ao fim do duelo e dos avisos, aparece o painel: YOU WIN/LOSE, motivo, nota (ex.: S-POW), contadores, star chips ganhos/total, carta ganha e copias no bau. A/B/START fecha; START de novo abre o menu de duelistas.
`Profile` (em memoria): star chips (max 999999), bau (max 99 por carta), vitorias/derrotas, ultimos 8 premios. A gravacao em cartucho/SD fica para o lote 14.

## 5. Arquivos
`include/DuelEngine.h`, `source/DuelEngine.cpp` (contadores, rank, premio), `include/Profile.h`, `source/Profile.cpp` (novo), `include/duel/DuelFieldMode.h`, `source/duel/DuelFieldMode.cpp`, `include/duel/DuelOverlays.h`, `source/duel/DuelOverlays.cpp`, `tests/*`.
Testes no PC: 47.537 verificacoes, 0 falhas. Nao compilei para ARM: se o `make` acusar algo, mande a mensagem.

## 6. O que testar
1. L/R no campo passa pelos monstros e depois pelas cartas baixadas; X em magia baixada usa; em equip pede o monstro.
2. Termine um duelo ganhando: confira o painel (nota, star chips, carta).
3. Perca um duelo: "NO REWARD".
