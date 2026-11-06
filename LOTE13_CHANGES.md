# Lote 13 - deck inicial, baú, Build Deck, Password e Library

Fonte das regras: a decompilacao que voce mandou (notes/research/the-game.md, cap. 4, e o codigo `NameEntry_BuildStarterDeck` / `card_list_sort.c`).

## Regras implementadas (todas testadas no PC)
- **Deck inicial**: 40 cartas das 7 piscinas de `WA_MRG.MRG` 0xF92BD4 (16 monstros ATK+DEF < 1100, 16 de 1100-1599, 4 de 1600-2099, 1 de 2100+, depois 1 magia (Raigeki ou Dark Hole, 50/50), 1 terreno e 1 equip). Sorteio `(rand & 0x7FF) + 1` sobre pesos de 2048; quarta copia repete o sorteio. As cartas do deck inicial ja contam como vistas.
- **Baú**: copias por carta, maximo 250 (o valor 99 que usei no lote 12 estava errado; corrigido).
- **Build Deck**: so 40 cartas valem para duelar; no maximo 3 copias de uma carta e 1 de cada peca do Exodia; cartas vao do baú para o deck e voltam. Ordens do jogo: numero, nome, mais forte (maior stat, depois o outro), ATK, DEF, tipo e a especial (baú: **New** = mais recentes primeiro, historico de 16; deck: **Shuffle**). Stats em ordem decrescente, empate pelo nome.
- **Password**: 8 digitos; cada carta so pode ser comprada **uma vez**; custo em star chips (10 a 999.999, dados do disco ja estavam em cards.dat); a carta vai para o baú, entra no historico New e vira "vista". As 698 senhas numericas do banco sao todas unicas (testado).
- **Library**: cartas vistas mostram dados; as demais "?????". Ter a carta tambem conta como vista.
- Mensagem original ao tentar duelar sem 40 cartas: **YOUR DECK ISN'T READY!**

## Telas (tela de cima)
Menu principal: FREE DUEL, BUILD DECK, PASSWORD, LIBRARY, NEW GAME (sorteia outro deck inicial e zera o perfil).
- Build Deck: CIMA/BAIXO move, L/R pula 10, ESQ/DIR troca de painel (baú/deck), A move uma copia, Y mostra a carta, START/SELECT troca a ordem, B sai.
- Password: CIMA/BAIXO muda o digito, ESQ/DIR move, A procura (depois A compra, B cancela).
- Library: CIMA/BAIXO, L/R = 10, ESQ/DIR = 100.
- No menu de duelistas, B volta ao menu principal; o deck "MY DECK" (tecla Y) e o padrao.

## Arquivos
`include/GameData.h`, `source/GameData.cpp` (carrega `starter.dat`), `include/Profile.h`, `source/Profile.cpp`, `include/duel/FrontEnd.h`, `source/duel/FrontEnd.cpp` (novos), `DuelFieldMode`, `DuelOverlays`, `tests/*`, `tools/extract_starter.py` (gera o `starter.dat`), `data/bin/starter.dat` e `nitrofiles/data/starter.dat` (**novo arquivo de dados: precisa estar na pasta nitrofiles para o .nds**).

## Limites conhecidos
- Perfil so em memoria: ao fechar, perde tudo (salvamento = lote 14).
- A Library ainda nao marca como vista a carta que aparece so no duelo (resultado de fusao/ritual); entra no lote 14.
- A ordem Shuffle do deck refaz o embaralhamento depois de cada troca de carta.
- Telas desenhadas so com a fonte de pixels (sem arte de cartas ainda; arte nos lotes 17-18).
- Nao compilei para ARM; testei regras no PC (96.776 verificacoes, 0 falhas) e a sintaxe da interface.
