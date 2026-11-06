# Roteiro do YGOFM_DS (estado após o lote 8)

## O que "100% fiel" significa neste projeto
- **Regras, dados e comportamento do duelo:** o alvo é 100%. Tudo é conferido contra o jogo original (tabelas do disco, constantes e textos do executável) e protegido por testes. A ferramenta `tools/audit/audit_data.py` re-audita os dados.
- **Imagem, som e vídeo:** não dá para ser idêntico bit a bit. O DS tem tela de 256×192 (o PS1 usa 320×240), pouca RAM e nenhum decodificador dos vídeos do PS1. Aqui o alvo é **mesmo conteúdo e mesmo comportamento, apresentação adaptada**.

## Feito (lotes 1 a 9)
Dados corrigidos e auditados · estrelas guardiãs · terrenos · fusão em cadeia · equips · as 33 magias · 24 rituais · Exodia · as 10 armadilhas · cartas viradas · fileira de magia/armadilha · trava do primeiro turno · menu de duelistas · painéis · 3 decks de teste.

## Falta
| Fase | Conteúdo | Lotes (estimativa) |
|---|---|---|
| Regras restantes | (o jogo original não tem efeitos de monstros) | concluído no lote 9 |
| IA | scripts de IA de cada duelista (o código decompilado tem a máquina de scripts), a CPU usando magias, equips, armadilhas e cartas viradas | 10–11 |
| Fluxo do jogo | recompensas do duelo (pools já nos dados), star chips, biblioteca de cartas, montagem de deck e seu custo, salvamento | 12–14 |
| Campanha e história | ordem dos duelistas, progressão, diálogos e cenas adaptadas para o DS | 15–16 |
| Gráficos fora do duelo | telas de título e menus, retratos dos duelistas, visualizador de cartas, animações | 16–18 |
| Áudio | converter trilhas e efeitos (`SD_BGM.DAT`, `SD_SE.DAT`, `MASTER.XA`) dentro dos limites do DS | 19–20 |
| Hardware | testes no DSi/DS real, memória e desempenho (contínuo) | todos |

Total estimado: **cerca de 11 lotes** além deste. É uma estimativa: depende dos testes e dos erros de compilação que você me trouxer, e a parte de história/áudio/vídeo é a mais incerta.

## Pontos em aberto (precisam de decisão ou de fonte)
- **Vídeos do PS1** (`MOVIE.STR`, 35 MB): sem decodificador no DS. Opções: cenas estáticas com texto, ou converter para um formato de vídeo do DS (pesado).
- **Modelos 3D** (`MODEL.MRG`, 351 MB): usados nas cenas do PS1; no DS viram imagens 2D.
- **Regra de "uma jogada por turno"**: ainda não confirmada no original.

## Lote 10 - concluido (aguardando teste no melonDS)
- 10.1: monstro virado pode ficar em ataque ou defesa (X ataque, Y defesa, R vira); da mao sobre monstro do campo: funde ou substitui.
Cartas viradas completas e IA dos 39 duelistas. Proximos: 11 refino/ajustes de duelo, 12-14 fluxo do jogo
(recompensas, biblioteca, deck builder, save), 15-16 campanha/historia, 16-18 graficos fora do duelo,
19-20 audio, teste em hardware continuo.

## Lote 11 - concluido (aguardando teste no melonDS)
Menu da mao fiel ao PS1 (face com setas, monstro vira em ataque, equip em qualquer monstro). Ver LOTE11_AUDITORIA.md.

## Lote 12 - concluido (aguardando teste no melonDS)
Correcao do cursor na fileira de magia/armadilha (L/R percorrem as 10 zonas proprias), rank do duelo (10 contadores e tabela original), star chips, sorteio da carta com os pesos do duelista e tela de resultado. Perfil em memoria (star chips, bau). Ver LOTE12_CHANGES.md.
Proximos: 13 biblioteca/bau e montagem de deck (custo), 14 salvamento (SRAM/SD) e ordem dos duelistas, 15-16 campanha/historia.

## Lote 13 - concluido (aguardando teste no melonDS)
Menu principal, deck inicial real (7 piscinas do disco), baú, Build Deck (3 copias, 1 de cada peca do Exodia, 40 cartas, 6 ordens + New/Shuffle), Password (compra unica, custo em star chips) e Library. O duelo usa o deck montado. Ver LOTE13_CHANGES.md.
Correcao do plano: o jogo original NAO tem "custo de deck"; as regras do Build Deck sao so 40 cartas, 3 copias e 1 peca de cada Exodia.

## Plano revisado dos lotes 14-20 (com o codigo decompilado que voce mandou)
- 14: salvar/carregar (arquivo no cartao SD via libfat, bloco duplicado com checksum como o original), registros VITORIAS/DERROTAS por duelista, desbloqueio do Free Duel, cartas vistas no duelo (fusao/ritual).
- 15: dados da historia: extrair do disco o script de eventos (199 eventos, 23 opcodes) e os textos de dialogo (160 KB, tabela de caracteres) para .dat; mecanismo de flags (array de flags do save).
- 16: campanha jogavel: dialogos, mapa de locais, duelos forcados/opcionais, loja de cartas (Save/Build Deck/Return/Leave), game over, derrota obrigatoria do Heishin, finais.
- 17: graficos fora do duelo: titulo, mapas, retratos, fundos de cenas (ferramentas de TIM do projeto), cartas no Build Deck/Library.
- 18: refinamento visual e de interface (animacoes, telas de resultado, menus) e desempenho no DS.
- 19: audio: conversao de trilhas e efeitos (SD_BGM.DAT, SD_SE.DAT) para o DS.
- 20: teste em hardware (DSi/DS), correcoes e pacote final.

## Lote 14 - concluido (aguardando teste no melonDS)
Salvamento em arquivo (cartao SD), array de flags do original, registros VITORIAS/DERROTAS por duelista, Free Duel com duelistas liberados e cartas vistas no duelo. Ver LOTE14_CHANGES.md.

- Lote 15 concluido: dados da historia extraidos + interpretador de texto + VM de eventos (ver LOTE15_CHANGES.md). Proximo: 16 campanha jogavel.
- Lote 16 concluido: campanha jogavel em texto (ver LOTE16_CHANGES.md). Proximo: 17 graficos fora do duelo.


Lote 17 concluido (graficos fora do duelo: titulo, cenas, retratos, mapa). Proximo: 18 (refino visual/UI e desempenho).

Lote 17.1 concluido (menu principal fiel). Pendentes de fidelidade visual: 17.2 (nome, Free Duel, Build Deck, Library, Password), 17.3 (dialogo, mapa real, cenas modos 1/2). Depois: 18.
