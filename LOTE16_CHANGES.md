# Lote 16 - campanha jogavel (texto)

A historia inteira roda, do inicio ao fim, usando o roteiro e os dialogos do disco original. A arte
(cenas, retratos, mapa 3D, creditos) vem no lote 17: aqui as cenas aparecem como texto.

## Como o jogo original liga as pecas (lido do codigo do original)
- Jogo novo comeca no evento 0x30. O evento e um roteiro: cena, dialogo, mapa, loja, duelo...
- No mapa (16 locais, tabela extraida do disco): setas andam pelas saidas (algumas so com flag da historia),
  A entra no local = evento (local + 32), B volta ao local 0 nos locais 10-15 depois do torneio (flag 0x47).
- O duelo comeca dentro do dialogo (comando F8 0D: oponente, terreno, cena de vitoria, cena de derrota).
  Depois do duelo o jogo vai para a cena de vitoria ou de derrota (dados do proprio descritor).
- Derrota = cena de game over (A tenta o mesmo duelo, B volta ao titulo). A excecao e Heishin (id 8): a derrota e
  obrigatoria e o roteiro cuida disso.
- Loja de cartas (SAVE / BUILD DECK / RETURN TO TITLE / LEAVE SHOP): exige 40 cartas; a cena da loja e a que
  volta ao carregar o save ou sair do Build Deck.
- Desbloqueio de duelistas acontece nas falas de vitoria (F8 19), como no original.

## O que entrou
- `tools/extract_story.py`: agora tambem extrai a tabela do mapa (`story_map.dat`).
- `include/Campaign.h`, `source/Campaign.cpp`: maquina de estados da campanha (logica pura, testada no PC).
- `include/duel/CampaignScreen.h`, `source/duel/CampaignScreen.cpp`: tela de cima (dialogo, escolhas, mapa em texto, loja).
- Menu principal: **CAMPAIGN** (continua a campanha salva), **NEW GAME** agora pede o nome do principe e comeca a
  campanha com baralho inicial e **nenhum duelista liberado** no Free Duel (a historia libera um a um).
- Perfil/save versao 2: guarda a cena da campanha, se ha campanha e o nome. Saves do lote 14 continuam validos.
- Fonte ganhou `? < " ( ) & * % $` (os dialogos usam).
- Duelo da campanha usa o mesmo motor, premios e registros do Free Duel; SELECT/START nao abrem o menu de duelistas nele.

## Testes (PC)
- Jogador automatico percorre a campanha inteira (escolhas e mapa aleatorios, ganhando todos os duelos e perdendo
  a primeira vez de cada um): 12 de 12 chegam aos creditos, 30 de 30 no modo aleatorio, 38 oponentes diferentes,
  35+ duelistas liberados no fim, derrota obrigatoria de Heishin respeitada, maior pagina de dialogo 5 linhas.
- Save v2 ida e volta, nome invalido, CRC. Resultado: 96.807 (motor) + 123.722 (historia) + 187 (campanha), 0 falhas.
- Nao compilei para ARM; a interface foi so checada de sintaxe.

## Limites conhecidos (proximos lotes)
- Sem imagens de cena/retrato/mapa, sem musica, sem animacoes de camera; creditos so mostram "THE END".
- A tela de resultado de torneio / banners (opcode 17) e os efeitos de F7/F8 visuais sao ignorados.
- A escolha de terreno/regras de campo especiais dos Mages (resetar terreno) segue o motor do duelo atual.
