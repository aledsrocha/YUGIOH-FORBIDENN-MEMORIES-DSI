# Lote 17.1 (revisado) - Titulo e menus principais fieis ao PS1

Baseado no codigo do jogo (MainMenu_UpdateFrontendMenu) e nos videos enviados.

## Fluxo (como no PS1)
1. Titulo: parede de hieroglifos + logo + (c) 1996 KAZUKI TAKAHASHI + "PUSH START BUTTON" pulsante (so START avanca).
2. START: a parede e o logo escurecem (B - F ate 0x80, 16 passos) e os botoes do menu inicial deslizam por 16 passos, lados alternados, com rastros.
3. Menu inicial: NEW GAME, LOAD, 2P DUEL, TRADE, OPTION. B no menu inicial nao faz nada.
4. LOAD: "LOAD? YES NO" -> "ACCESSING MEMORY CARD..." -> "LOADING..." -> "LOAD COMPLETE!" -> os botoes saem e o menu com jogo carregado entra (cursor em CAMPAIGN).
5. Menu com jogo carregado: CAMPAIGN, FREE DUEL, BUILD DECK, LIBRARY, PASSWORD, SAVE. **B volta ao menu inicial com o cursor em LOAD** (corrige o erro apontado).
6. Voltar de Build Deck/Library/Password/Free Duel reabre o menu com o cursor na entrada de onde saiu; sair da loja ("Return to Title") reabre o menu carregado.

## Tecnico
- `tools/su_sprites.py` / `tools/extract_menu.py` -> `menu.dat` (fundo, 22 botoes, logo, copyright, PUSH START), escala 0.8.
- `source/duel/MainMenu.cpp` (+ `include/duel/MainMenu.h`): maquina de estados do titulo/menu, 30 passos/s, rastros aditivos (B + F), escurecimento por paleta.
- `FrontEnd` delega o menu principal ao MainMenu; `FrontEnd::tick()` roda a cada quadro.
- O jogo agora abre sem carregar o save: LOAD le o save do SD.
- Tela de baixo fora do duelo: a parede escurecida do menu.

## Ainda fora do original (proximos)
- Janela de cartao de memoria: desenhada proceduralmente (listras amarelas); a arte exata entra depois.
- 2P DUEL / TRADE: "MEMORY CARD REQUIRED!"; OPTION: aviso provisorio (som no lote de audio).
- 17.2: nome (teclado), Free Duel, Build Deck, Library, Password. 17.3: caixa de dialogo de pedra, mapa 3D, cenas modos 1/2.

## Revisao 2 (video melonDS de 29/10)
- Piscar: o menu/campanha/telas do front-end agora sao desenhados num quadro de tras (PixelText_BeginBuffered/Present) e copiados de uma vez para a tela.
- O logo e o copyright so aparecem no titulo (PUSH START/fade); o menu desliza sobre a parede, como no PS1.
- Campanha em branco apos o nome: causa ainda nao reproduzida no PC (fluxo NEW GAME -> nome -> campanha passa limpo). Esta build escreve marcadores amarelos no canto da tela de cima (C1, C2, D1..D4, D9) para mostrar ate onde o jogo chega.

## Revisao 2 (video melonDS de 29/10) - correcoes finais
- Causa da campanha parar: `DuelFieldMode` era variavel local em `main()` e ocupava a pilha do ARM9 (16 KB). Com o `MainMenu` dentro do `FrontEnd` a pilha chegava a ~11 KB so ao desenhar a cena; fopen/snprintf estouravam e apagavam a estrutura da thread (data abort em __syscall_getreent). Agora o objeto e estatico.
- `defaultExceptionHandler()` ativo: se o ARM9 cair, aparece a tela de registradores em vez de congelar.
- Piscar: desenho em quadro de tras (PixelText_BeginBuffered/Present). Logo so no titulo.
- Logo/copyright voltam a ficar atras dos botoes do menu (como no PS1; confirmado nos videos).

## Lote 17.2a - dialogo fiel ao PS1
- Janela de pedra (faixa de glifos, miolo azul-escuro, faixa de baixo) montada a partir da folha de UI da campanha: `tools/extract_dialog.py` -> `dialog.dat`.
- Bustos dos personagens (registros de efeito de exibicao do WA_MRG, 64 personagens x ate 4 expressoes): `tools/extract_busts.py` -> `busts.dat`. Posicao: ancora esquerda x=0x68, direita x=0xD8 (x0.8), base logo abaixo do topo da janela.
- Comandos: opcode 9 do roteiro (SHOW_MENU: id + bit 7 = lado) e F6 id flags (0x80 sai, 0x40 expressao, senao entra no lado flags&1).
- Texto em fonte pequena e espacada (6.6 px de avanco) com seta laranja de pagina; escolhas com seta laranja.
- Pendente: animacao de entrada/saida, boca/piscar, imagens de historia (modos 1/2), demais telas.

## Lote 17.2b
- Loja: lista preta (SAVE / BUILD DECK / RETURN TO TITLE / LEAVE SHOP) com seta laranja, caixa NO/YES, janela de pedra e busto do lojista; faixa listrada amarela para avisos de gravacao.

## Lote 17.2c
- Save no DSi real (nds-bootstrap): tenta gravar ao lado da ROM (argv[0]), depois sd:/, fat:/, sd:/_nds/, fat:/_nds/; o caminho que funcionou e reutilizado no LOAD. Falha mostra "SD SAVE FAILED (ERRNO n)".

## Lote 17.2d
- O texto troca a imagem da cena por dentro do dialogo (F7 05 + u16: id da imagem, BCD; 0x4000/0x8000 sao flags): `Campaign.cpp` agora acompanha isso (antes so a op. 2 do roteiro valia).
- Imagens de historia dos modos 1 e 2 em `scenes.dat` (`tools/extract_story_pics.py`): fundo 320x160 + recortes encaixados nos buracos por correspondencia de silhueta; modo 2 = parte esquerda do quadro largo (a rolagem do viewport fica para depois).
- Conhecido: alguns recortes (ex. 0x104, 0x111, 0x132...) ficam como silhueta escura e o brilho aditivo nao e desenhado.

## Lote 17.2e/f
- Imagens de historia montadas como o jogo: tabelas D_80090BA8 (modo 1) e D_80090C00 (modo 2) dizem quais camadas existem; a camada ocupa o mesmo lugar do quadro (folhas c2/c3 = recorte do modo 1; modo 2: fundo 512x256 + camadas c4/c6 em (x,y)). Substitui a correspondencia de silhueta.
- Pendente: brilho aditivo (camada 2), rolagem do viewport (F7 05 estendido / op 6) do modo 2.

## Lote 17.3 - animacao das cenas e dos bustos (como o jogo)
Lido no codigo do jogo (ScriptImage_RebuildObjects, Script_OpLoadImageScene/ShowImage/UpdateViewportTween, Text_HandleDisplayEffectCommand, DisplayEffect_UpdateMenuRecord).

**Cores corrigidas (causa dos recortes "estranhos")**: a ultima secao de cada imagem de historia traz 4 paletas (linhas 0xF0..0xF3 da VRAM). Fundo = paleta 0, recorte = paleta 1, brilho aditivo = paleta 2. Antes todas usavam a paleta 0.
- `tools/extract_story_v2.py` -> `story.dat` (camadas separadas por cena, cada uma com a sua paleta); `scenes.dat` volta a ter so as cenas do modo 0.
- Imagem larga do modo 2 (410x205) com rolagem; camada de brilho aditiva (nao rola quando a mascara tem o bit 7).

**Animacao de cena** (`Campaign.cpp` logica, `duel/SceneStage.cpp` desenho):
- Op. 1 (LOAD_SCENE): acende do preto (faixas, 8 niveis/quadro); ops. 4/5 e F7 05 no texto: escurece, troca e acende (12 niveis/quadro; flag 0x4000 = nao acende).
- Rolagem do viewport: F7 05 estendido (byte Y + u16 X), op. 6 e F7 0B (X, Y, quadros; Y >= 0x1000 = o texto espera) - interpolacao linear a 30 Hz como Script_UpdateViewportTween.
- Op. 16 (FADE_OUT, bit 7 = espera) e op. 20 (WAIT) agora seguram o roteiro.
- Pulso de brilho (func_8002FED8): angulo +32/quadro, fundo/recorte 1.0..1.19, camada aditiva 1.0..1.37, nas cenas cujo registro tem valor 1.
- O roteiro/texto so continua quando a animacao acaba (`Campaign_Tick`, `Campaign_Busy`).

**Bustos animados** (`tools/extract_busts2.py` -> `busts2.dat`, `duel/BustStage.cpp`):
- Entrada deslizando de fora da tela (16 quadros, desacelera), saida deslizando (acelera) ou em fade, entrada em fade (flag 8), troca de expressao em fade cruzado com deslize de 16 px; saida e troca seguram o texto.
- Piscar: olhos variante 1 (5 quadros) com intervalo aleatorio 60..315 quadros de 30 Hz.
- Boca: forma de cada letra vem da tabela do jogo (0x801D9000); abre/fecha enquanto o texto aparece; F6 0x21 = silencio.
- Texto aparece letra a letra (2 por quadro de 30 Hz); A termina a pagina.

Previa no PC: `tests/preview/build_scene.sh [a_cada_n_quadros] [quadros] [evento]`.
Ainda fora: slide/zoom do retrato pequeno (F6 0x41+), mapa 3D, tela de nome, demais telas do menu.

## 17.4 (parcial)
- Campanha: antes de cada duelo abre o Build Deck (B inicia o duelo; exige baralho com 40 cartas). FrontEnd::openBuildDeckFromCampaign(preDuel), DuelFieldMode::handleCampaignMode/handleFrontEndOutcome.

## 17.5 - Build Deck fiel ao PS1
- Novo renderer `DeckScreen` (arte extraida do disco: `tools/extract_deckui.py` -> `deckui.dat`).
- Linhas, contadores, icones de ordenacao, cursor pulsante e barra de rolagem na geometria do PS1.
- Navegacao portada da decomp: D-pad move; L/R pagina (8); Y+L/R salta 50; START/SELECT ordena; A move carta; B sai; X info; ESQ/DIR troca painel.
- Pendente: dialogo de saida, animacao da carta voando, visor Triangle, pontuacao (. , ' !).

## 17.6 - Free Duel (SELECT OPPONENT!) fiel ao PS1
- `tools/extract_freeduel.py` -> `freeduel.dat` (moldura 320x240, fundo de pedra, cursor ornamentado, barra, 40 retratos 48x48, fonte 8x12 e paletas de texto do pacote WA 0x1E88 / boot).
- `FreeDuelScreen`: grade 5x8 (passo 56x52) com rolagem vertical (janela 0x28..0x90, barra = (y-0x28)*72/364+7), cursor que desliza em 8 passos
  com rastro aditivo (16 quadros, -4/128 por quadro), pulso de escala (16 em 128 quadros), nome + `WIN nnn LOSS nnn` (fonte 8x12 de passo 8, WIN em x+0xA0).
- Logica portada de `FreeDuel_UpdateScreen/UpdateCursorTween/UpdateScrollbar/UpdateSparkle` a 30 Hz; so as celulas liberadas aparecem (Duel Master K sempre).
- Celula 0 abre o Build Deck e B volta ao Free Duel; deck incompleto mostra "YOUR DECK ISN'T READY!". Y (atalho de dev) alterna deck de teste.
- Pendente: tempos da mensagem, sons (lote 19), paginas extras de duelistas.

## 17.7 — Free Duel passa pelo Build Deck antes de cada duelo
- Ao escolher um oponente no Free Duel (deck "Campanha"), o jogo abre o Build Deck antes do duelo, como na campanha.
- B no Build Deck pré-duelo exige exatamente 40 cartas ("DECK NEEDS EXACTLY 40 CARDS"); com deck válido o duelo começa.
- Testes: 187 checks e 150051 checks, 0 falhas.
- Password fiel: em andamento (ver próximo lote).

## 17.8 — Password fiel e detalhe da carta (Triangulo)
- `tools/extract_password.py` → `password.dat` (paineis de pedra, molduras de carta por tipo, verso, estrelas, 24 icones de tipo,
  10 estrelas guardias, aro e setas do cursor, digitos/rotulos ATK/DEF, fonte 16x16 e paletas de texto) e `cardart.dat`
  (arte 102x96 + titulo 96x14 das 722 cartas, lida sob demanda).
- `PasswordScreen`: fundo preto, tres paineis de pedra (STARCHIP, 8 digitos com aro vermelho e setas, mensagem), carta virando em
  torno do eixo vertical, mensagens 226-229 digitadas, escolha EXCHANGE/QUIT, contagem regressiva dos star chips, volta da carta.
  Controles: LEFT/RIGHT movem o cursor (8 quadros), UP/DOWN com repeticao trocam o digito, A consulta/confirma, B sai, X (Triangulo)
  abre o detalhe da carta digitada.
- `CardDetailScreen`: detalhe da carta (Triangulo) no Password, no Build Deck e na Library, com entrada animada.
- `Profile_PasswordCheck` (sem efeitos colaterais) para saber antes de comprar se a senha esta usada / cara / bau cheio.
- Aproximado (nao ha esses pedacos no disco ou nao foram confirmados): orbe de atributo desenhado em codigo, fundo teal do detalhe
  montado com as pedras do painel, verso da carta com a metade de baixo espelhada, velocidade da digitacao.

## 17.9 — Library fiel ao PS1
- `tools/extract_library.py` -> `library.dat` (icone 12x14 da grade + 5 paletas de tipo, direto do pacote da Library em WA_MRG).
- `LibraryScreen` (PasswordScreen.cpp): grade 20x40 em duas secoes 10x10, passo 14x16, so cartas vistas, cinza as que nao estao no bau/deck, cabecalho `<vistas/722>` em letras de 16 px que rola com a grade, cursor em cruz verde pulsante que desliza (6 quadros; Y = 2; L/R = 10 linhas; virar de linha = x4), rolagem mantendo o cursor entre y=64 e 176, A = detalhe da carta, B = sair.
- Aproximacoes: placa inferior e sprite do cursor nao extraidos (preto/cruz procedural); velocidade do pulso estimada; sem modelo 3D do monstro.

## 17.10 — Tela de nome fiel ao PS1
- `tools/extract_name.py` -> `name.dat` (fundo 320x240 do pacote 0x1EDF a 50% de brilho como o sprite 0x404040 do jogo + anel vermelho 32x32).
- `NameEntryScreen` (PasswordScreen.cpp), logica do overlay: grade 15x9 de celulas 20x18, ←→ e END laranja na coluna de comandos (saltos de tabela D_8016AB38/ABC0), quadro verde com cruz que desliza em 8 quadros, START vai ao END, A repete, B apaga (recua o anel), letra pulsa e voa ate o campo (6 letras), letra substituida estilhaca em 16 pedacos, "Input your NAME!" e "Your NAME is ... YES/NO" em caixa que sobe, fade ao confirmar.
- SELECT sai para o menu (conveniencia; o original nao tem saida).
- Aproximacoes: caixa de dialogo em caixa de pedra do Password, cores de brilho/rastro da letra em voo, sem audio.

## Lote 17.11 — mapa 3D da campanha (Egito + cidade)

O mapa em texto (nos de um grafo) foi trocado pelo mapa 3D do PS1: o modelo do terreno girando com a camera em orbita.

**Dados** (`tools/extract_map.py original_iso data/bin` -> `map3d.dat`, 518 KB, copiado para `nitrofiles/data/`):
- pacote do overworld (setor 8153): modelo HMD (733 vertices, 1267 triangulos + 84 quads texturizados, normais), 60 imagens de
  textura/paleta que o overlay sobe na VRAM, banco de sprites (setor 140) e imagem das setas/placa/marcador.
- iluminacao do original (3 luzes planas + ambiente 0,5, brilho = min(2, 2·L)) ja calculada por canto de poligono.
- sprites animados (setas de saida: 10 quadros de 4 ticks; Pedra do Milenio: 16 quadros de 6 ticks; placa de pedra com falcao),
  reduzidos 5->4 como o resto da interface.
- `Story.h` ganhou cameras, posicao do marcador e posicao/variante das setas (`StoryMapLocation` / `StoryMapExit`).

**Codigo** (`include/duel/MapScreen.h`, `source/duel/MapScreen.cpp`, integrado em `CampaignScreen`):
- renderizador por software direto em 256x192 (projecao h=300·0,8, centro (160,120)·0,8; modelo na escala 1365/4096; neblina por
  vertice de 2000 a 2400 ate o preto; ordenacao por tabela de profundidade como o OT do PS1; textura afim 4/8 bits com cor 0 transparente).
- camera: `ViewState_ApplyOrbit` (orbita em torno de (vrx, 0, vrz)); troca de local = transicao linear de 5 canais em `steps` ticks
  de 30 Hz (angulo pelo caminho curto), marcador desliza com cosseno entre locais da cidade; o controle fica travado durante a transicao.
- locais 10-15 (cidade): vinheta de holofote (elipse centrada em (160,144), raio interno 32 / externo 192, x·1,25), marcador e,
  ao vir do mundo, o holofote fecha de 180 ate 32 (7 por tick).
- nome do local (`0x8350 + indice`) em texto 8x12 sobre a placa; setas animadas so quando a camera esta parada.

**Aproximacoes** (sem captura do original para comparar): sombreamento (fator 2,0 maximo) e neblina vem do codigo do GTE;
holofote e sprites sao desenhados na ordem "holofote -> placa -> setas -> marcador" (no original o holofote pode escurecer tambem
os sprites); a saida do mapa nao tem o fade/rotacao final do original; o nome usa a cor branca; velocidade de quadro nao otimizada
(DS: estimativa de ~10-15 quadros/s; ajuste previsto para o lote 18).

Teste no PC: `tests/preview/preview_map.cpp` (gera imagens de todos os locais e das transicoes; 0 falhas).

## Lote 17.12 — tabuleiro 3D do duelo (modulo + extrator; ligacao ao duelo ao vivo no 17.13)

Base: video de um duelo completo no PS1 (campo normal e SEA, mao, cursor, ataque, magia, fusao, resultados).

- `tools/extract_board.py` -> `board3d.dat` (517 KB): modelo HMD do tabuleiro (pacote de terreno, fase 11: 114 vertices, 78 triangulos + 64 quads,
  igual nos 7 terrenos) e, por terreno, as duas paginas de textura de 4 bits + 15 paletas (fase 12). Terrenos: 0 normal (ouro), 1 floresta,
  2 deserto/lava, 3 montanha, 4 pradaria, 5 mar, 6 sombrio.
- `include/duel/Soft3D.h`, `source/duel/Soft3D.cpp`: o renderizador 3D do mapa virou modulo comum (projecao, neblina, OT, triangulos
  texturizados); o mapa da campanha usa o mesmo codigo (saida identica, conferida pixel a pixel).
- `include/duel/DuelBoard.h`, `source/duel/DuelBoard.cpp`: tabuleiro com a camera do original (orbita; projecao h=300, centro (160,108),
  neblina 650..800, tudo x0,8): `viewOverview` (0x258, 0x100, 0x400/0xC00 - mao e panoramica), `viewCursor` (0x14E, 0x3FE, vrz por linha de
  D_800907AC - vista de cima), abertura do duelo (0x4B0/0x358/0x16C0 ate 0x258/0x100/0x400, o tabuleiro surge da neblina), transicao
  linear de camera (func_80022D94) e `project()` para posicionar cartas (17.13).
- `tests/preview/preview_board.cpp`: 7 terrenos x vistas, abertura e transicoes (0 falhas).

Falta (proximos lotes): ligar ao DuelFieldMode, cartas projetadas nos slots, cursor, HUD/painéis, animacao da agua do mar, efeitos.

## Lote 17.13 - tabuleiro 3D ligado ao duelo ao vivo
- `DuelFieldMode` abre o `DuelBoard` com o terreno do duelo (`DuelEngine_GetTerrain()`), troca a textura se o terreno mudar e o fecha ao sair para menus/campanha (libera a memoria que o mapa 3D usa).
- `DuelBoard_FitField`: cada zona logica do campo recebe como retangulo a pegada projetada da carta (56x74 do mundo) na camera atual; cursor, destaque de invocacao e cartas seguem a projecao. Colunas ordenadas pela tela.
- `DuelFieldRenderer` desenha o tabuleiro 3D no lugar do fundo/zonas 2D; `FieldCardRenderer` usa o tamanho projetado (miniaturas ate 40x34; carta em defesa troca largura/profundidade) e, com a camera em movimento, desenha retangulos lisos (sem recarregar a arte a cada quadro).
- Camera: panoramica da mao (`viewOverview(0)`, lado do jogador) e vista de cima na linha do cursor (`viewCursor`) durante invocar/atacar/equipar, transicao de 16 quadros a 30 Hz; so redesenha quando a camera anda.
- `viewOverview(side)` agora: lado 0 = jogador (yaw 0x400), lado 1 = oponente (0xC00), igual ao `viewCursor`.
- Aproximacoes: posicao de baralho/cemiterio/campo estimada; animacao da agua do mar, paineis de pedra, tela de detalhe, resultado e animacoes de ataque/magia/fusao ficam para os proximos lotes; velocidade (10-15 fps estimado) sera ajustada depois.

## Lote 17.14 - controles do original + visual PS1 do duelo
Controles na sua vez (mao):
- Esquerda/Direita: mover na mao. **Cima**: marca/desmarca a carta para fusao (o botao Y foi removido); Baixo ou B: limpa as marcas. A: jogar.
- **R**: ver o campo (cursor livre sobre as 26 zonas, camera de cima acompanha a linha). Antes de jogar uma carta o campo e so leitura (A/X mostra "PLAY A CARD FIRST"); depois de jogar (ou com a mao vazia) A/X ativa a magia baixada ou inicia o ataque. B ou R voltam a mao.
- **L**: mudar a posicao dos monstros (usa `DuelEngine_ChangePosition`: so se ainda nao atacou). Esquerda/Direita escolhem o monstro, A alterna ataque/defesa, B ou L saem, R vai para ver o campo.
- Os antigos L/R (percorrer zonas) e X na mao foram trocados por isso; na escolha de invocacao L/R continuam alternando virada para baixo/cima.
Visual:
- Cursor do campo: moldura vermelha com mira verde (so em ver campo / ataque / equip).
- Verso das cartas: redemoinho laranja/marrom (procedural, nao e a textura exata do PS1). Tarja ATK (e DEF quando a carta e grande) no pe das cartas do campo (valores base da carta).
- Tela de baixo: cartas maiores com ATK/DEF abaixo, a selecionada levantada, faixa de pedra com nome/tipo/atributo/ATK/DEF/LEVEL; sem textos de ajuda.
- HUD: caixa FIELD (terreno ou "-") no canto superior esquerdo; LP / COM / YOU / LP no canto superior direito. Nomes de terreno em ingles (MEADOW, SEA, DARK).
Pendente: baralho/cemiterio/campo em posicao estimada; texturas exatas do PS1 para o verso; paineis/tela de detalhe/resultado/animacoes nos proximos lotes.

## Lote 17.15 - velocidade + composicao do original (uma tela so)
Velocidade (sem som ainda):
- `DuelBoard::render` guarda o ultimo quadro 3D e so renderiza de novo se camera/terreno mudarem (antes re-renderizava 256x192 a cada tecla). Com a camera em movimento renderiza em meia resolucao (4x menos pixels) e amplia 2x2; ao parar faz o quadro completo. No PC: completo 0,21 ms, meia 0,07 ms, reaproveitado 0,002 ms (o DS e dezenas de vezes mais lento, vale a proporcao ~3x e ~100x).
- A camera anda por tempo real (vblank via IRQ, 30 Hz) e nao por iteracao do laco: se um quadro demorar, a transicao nao fica mais lenta, so pula passos.
- Camera em movimento redesenha so a tela de cima (a de baixo nao muda).
- `HandRenderer`: fundo montado uma vez e copiado; arte das cartas da mao em cache (nao le mais o cartucho a cada redesenho); cache de miniaturas do campo subiu para 16.
Fidelidade (composicao de uma tela so, como no PS1):
- Tela de cima: tabuleiro + mao sobre ele (cartas com ATK/DEF, a selecionada levantada, verde quando confirmada) + faixa de pedra no pe com nome, tipo, atributo e ATK/DEF. Nos modos campo/invocar/atacar a mao some e a faixa descreve a carta sob o cursor.
- Tela de baixo: detalhe grande da carta (arte, tipo, atributo, nivel, ATK/DEF), redesenhado so quando a carta muda.
- Corrigidos: barra azul vazia no topo da tela de baixo e moldura quebrada da carta selecionada (a moldura ainda usava a posicao antiga).
Limite: sem medir no hardware (o contador de FPS do melonDS fica na barra de titulo e nao aparece na gravacao).

## Lote 17.16 - zonas, foco no campo, ataques e velocidade do mapa/free duel
- Zonas: pegada da carta agora 66x64 centrada nos centros reais das casas do modelo (colunas -140..140, linhas z = +-94 / +-162, lidos das grades do HMD); moldura do cursor e do alvo de invocacao ficam dentro da casa (antes sobravam 3 px para fora e as casas tinham 74 de fundo). Carta em defesa fica 3/4 da altura. Miniaturas ate 52x48.
- Depois de jogar a carta do turno a mao sai e o foco fica so no campo (B/R nao voltam a mao); a mao volta no turno seguinte. L (posicao) devolve ao campo.
- Ataques: ao entrar no campo e depois de cada ataque o cursor vai direto para o proximo monstro que ainda pode atacar; A num monstro que nao pode mostra "ALREADY ATTACKED" ou "DEFENSE POSITION". O motor ja permitia um ataque por monstro; so o fluxo da interface dificultava.
- Velocidade: `FrameClock` (vblank) conduz a logica do mapa 3D e da camera do duelo em tempo real (30 Hz). Mapa 3D: cena (3D + vinheta + placa + nome) em cache, meia resolucao durante a transicao, desenho so a 30 Hz. Free Duel: camada estatica (fundo, retratos, moldura, textos) montada e reduzida uma vez; so a area do cursor/rastro e refeita e reduzida a cada quadro.

## 17.17 - velocidade 100% e ataque em cadeia

**Ataque em cadeia (bug).** A tecla que fechava o aviso "BATTLE ..." era reprocessada como comando; como o cursor
passa sozinho para o proximo atacante, o mesmo A iniciava outro ataque e assim todos atacavam sem escolha.
Agora a tecla que fecha o aviso e descartada (`pressed = 0`). Cada ataque exige A em um monstro escolhido e A no alvo;
para nao atacar com algum, basta mover o cursor ou apertar START (termina o turno em qualquer ponto).

**Velocidade.**
- Loop do duelo roda a logica em tempo real (contador de vblank, ate 4 passos por desenho): a velocidade do jogo
  nao depende mais do custo do desenho; so o numero de quadros desenhados cai se a tela pesar.
- PixelText (Fill/Blit/BlitLevel/BlitAlpha/BlitWindow/Draw/Present) reescrito com recorte fora do laco: cena ~242 -> ~60-75 us.
- Reducao 320x240 -> 256x192 (Free Duel, Password) separavel, campos de 10 bits: resultado identico bit a bit ao anterior.
  Free Duel 471 -> 237 us, Password 379 -> 257 us (PC -O2).
- Mapa 3D e tabuleiro com cache de quadro e meia resolucao so enquanto a camera se move; Free Duel com camada estatica.
- `tests/preview/build_bench.sh` compila e roda os benchmarks.

**Aproximacoes.** Todos os numeros sao do PC (proxy), nada foi medido no DS/DSi real. Picos de carga (abrir mapa 3D,
CardDetail) ainda existem e ficam para o lote 18.

## 17.18 - ataque escolhido pelo jogador, valores com terreno, clarao de terreno

- **Ataque:** novo teste de fluxo no PC com o codigo real do DuelFieldMode (`tests/preview/build_flow.sh`: joga Umi, ataca, confere flags,
  cursor, B cancela). Nele nenhum monstro ataca sem A no atacante + A no alvo. O cursor pulava sozinho para o proximo atacante
  depois de cada ataque (o PS1 nao faz isso); agora ele fica no monstro que atacou e o jogador escolhe o proximo com Esq/Dir.
- **Tarja ATK/DEF no campo:** passou a mostrar o valor real do duelo (terreno +-500, equips, Megamorph) em vez do valor base;
  verde = bonus, vermelho = penalidade. A tabela de terrenos do motor ja era a do jogo original (confere com a lista de tipos).
- **Troca de terreno:** clarao branco que some em ~30 quadros quando uma carta de campo muda a mesa. E uma aproximacao: precisa de
  video/quadros do original para igualar a animacao exata.
- `tests/stubs/nds_extra.h`, `flow_attack.cpp`, `build_flow.sh` (novos).

## 17.19 - cena de batalha, ataque direto, luz do terreno, YOU WIN! (a partir dos videos do PS1)

Medido nos videos do usuario (Screenrecorder 12-52 e 12-57):
- **Ataque a monstro:** as duas cartas grandes (moldura larga com ATK/DFD de password.dat) entram dos lados (~24 quadros), seguram
  ~40, clarao branco no impacto, fogo na carta destruida (~64), some tudo (~30). O valor que nao vale (DFD do atacante; ATK do
  defensor em ataque, ou o contrario em defesa) aparece apagado. `DuelBattleScene` (novo), `Password_RenderBattleCard`.
- **Ataque direto (oponente sem monstros):** carta do atacante a esquerda e "-N" em vermelho/dourado pulsando a direita.
- **Carta de campo:** a mesa acende em branco com colunas de luz subindo (30 quadros), o terreno troca no pico, a luz desce (60).
- **Vitoria/derrota:** faixa "YOU WIN!" (letras caindo uma a uma, vermelho com contorno dourado) antes do painel de resultado;
  derrota usa "YOU LOSE" (texto e cores PRESUMIDOS: nao ha video da derrota).
- Aproximacoes: fogo e luz sao procedurais (nao ha sprite extraido); letras usam a fonte de 16 px do password.dat ampliada, nao as
  letras originais; ataques da CPU ainda nao usam a cena; contagem gradual dos LP nao feita; tela RESULTS OF DUEL igual ao video
  fica para o proximo lote. `tests/preview/preview_battle.cpp` gera os quadros; `flow_attack.cpp` cobre o fluxo.

## 17.20 - dano legivel, luz do terreno mais rapida, YOU WIN/LOSE e RESULTS OF DUEL (referencias do PS1)

- **Bug de quadro do WIN (video melonDS):** a caixinha antiga "YOU WIN" (DuelLifePointRenderer) ainda era desenhada junto com a faixa nova,
  e a faixa piscava (fade por quadros alternados). Caixa removida, faixa sem piscar (o fundo escurece e a faixa fica ate o painel).
- **YOU WIN / YOU LOSE:** vitoria vermelha, derrota azul (PS1), contorno amarelo, letras caindo; fonte de 16 px ampliada (aproximacao
  das letras altas do original).
- **Dano:** fonte da paleta (amarelo/laranja alternando) com contorno escuro grosso, espacamento de 26 px: "-1300" nao vira "1B00".
- **Luz do terreno:** 90 -> 50 quadros (sobe 14, troca a mesa, desce 36).
- **RESULTS OF DUEL:** titulo azul (vitoria) / vermelho (derrota), barras CARDS USED e REMAINING LP (YOU/COM), WINNER, DUEL SKILL com
  POW/TEC e letra do rank, SPOILS com estrelas de star chip, numero e nome da carta; na derrota, "WINNER <duelista>".
  `DuelResult` ganhou `opponentCardsUsed` e `opponentLife`.
- Aproximacoes: placas "DUEL SKILL"/"SPOILS"/titulo sao texto, nao as imagens originais; a segunda pagina (setas) nao existe ainda.

## 17.21 - YOU WIN sem piscar, fusao e descarte

- Faixa/tela de resultado desenhadas no buffer (BeginBuffered/Present): fim do pisca-pisca.
- Nova `DuelFusionScene` (tela de cima): cartas entram da esquerda, se juntam num clarao e viram a carta nova; no fim de uma cadeia com fusao a carta grande gira sobre fundo estrelado.
- Descarte (carta da mao incompativel com a anterior, ou carta do campo incompativel): a rejeitada escurece/avermelha, treme e cai. Sem filmagem de referencia: e aproximacao.
- `DuelEngine_DescribeChain` descreve cada passo ANTES do commit; ligado em `commitChainSummon` e na invocacao sobre zona ocupada.
- Previa: tests/preview/preview_fusion.cpp.

## 17.22 - carta fora do lugar e ATK/DEF reais na faixa

- `DuelBoard::updateView()` chamado em `prepareBoard` antes de `DuelBoard_FitField`: as zonas eram calculadas com a camera do quadro anterior; no ultimo quadro do movimento da camera (ex.: 1a invocacao) a carta ficava deslocada e nao era redesenhada.
- Faixa de baixo da tela de cima e detalhe da tela de baixo agora mostram ATK/DEF reais do duelo (terreno + equips) para monstros do campo; verde = bonus, vermelho = penalidade. O combate ja usava esses valores (GetFieldPower).

## 17.23 - cartas da mao com bonus do terreno
- Faixa e detalhe da tela de baixo mostram ATK/DEF + bonus do campo ativo tambem para cartas na mao (verde/vermelho).

## 17.24 - derrota
- YOU LOSE: letras azuis com degrade vertical e contorno amarelo, mesa clara por tras (sem escurecer). RESULTS: setas de pagina nos cantos; derrota ja nao mostra POW/TEC, rank nem estrelas.

## 17.25 - tela de nome mais rapida + tela de credito
- Tela de nome: fundo+teclado ficam prontos em cache (copia em vez de reconverter 76 mil pixels e reblitar ~100 glifos por quadro) e a reducao 320x240->256x192 so refaz as linhas que mudaram (saida identica bit a bit, 522 quadros conferidos por hash).
- Nova tela de credito "PORT BY ALEDSROCHA" (300 quadros = 5 s, fade in/out) desenhada por codigo (CreditSplash.cpp), antes do titulo / PUSH START.

## 17.26 - tela de credito PORTATIL LAB
- Nova abertura (5 s): estilo retro-neon, sol com fendas, grade em perspectiva rolando, console de duas telas com halo, logo PORTATIL LAB entrando com falha digital + clarao, linha 'PORT BY ALEDSROCHA' digitando, linhas de varredura e fade.

## 17.27 - passada de velocidade (alvo: 60 fps estaveis)
Medido no PC com callgrind (instrucoes x86, so proxy) numa sessao de duelo roteirizada (tests/preview/prof_session.cpp, build_session.sh): 448 M -> 315 M instrucoes (-30%). Nada medido no ARM; as mudancas tambem tiram divisoes/64 bits, que no ARM9 custam muito mais que no x86.
- Cena de batalha: cartas copiadas por linha (sem teste por pixel; esmaecer por tabela), fogo com calor incremental e soma saturada empacotada, texto do dano montado uma vez, quadros parados (cartas em repouso) nao redesenham. 184 M -> 88 M no trecho.
- Faixa YOU WIN/LOSE: letras prontas (sprites) e fundo guardado; depois da ultima letra nao redesenha ate o painel. Antes: ~12 passadas de fonte por letra por quadro, 150 quadros, mais o campo inteiro.
- Soft3D (tabuleiro e mapa): 1 divisao por vertice (antes 3), 1 divisao de 64 bits por triangulo (antes 6) + 3 de 32 bits; neblina por multiplicacao.
- Terreno: troca de textura do tabuleiro 4->8 bits por tabela de 16 bits; clarao (whiten) por tabela por canal (PixelText_Whiten) em vez de 3 multiplicacoes por pixel.
- Retangulos: FieldCardRenderer/HandRenderer/DuelFieldRenderer sem putPixel por pixel; PixelText_BlitWindow opaco escreve 2 pixels por vez.
- Fusao: mapa de colunas + tabelas por canal (antes uma divisao por pixel).
- Medidor de desempenho: segure L+R+SELECT+START juntos para ligar/desligar "L60 D58 W2" no canto: passos de logica por segundo (deve ser 60), desenhos por segundo e o pior quadro em vblanks (W1 = ok; W2 = um quadro perdido).

## 17.28 - velocidade: modo ARM + clock DSi + DMA
Baseado no video do melonDS (fps 24-42 nas telas 2D: Free Duel, menu/titulo, Build Deck, Library, Password; 50-60 nas demais). Nada medido no ARM aqui.
- Makefile: arquivos de desenho/composicao (PixelText, Soft3D, FreeDuel/Password/Deck/MainMenu/FrontEnd/Campaign/Map, DuelBoard, renderers, cenas, CreditSplash etc.) agora compilados com -marm (32 bits) em vez de Thumb; o resto segue Thumb. Se algo ficar pior (cache de instrucoes de 8 KB), basta esvaziar HOT_ARM.
- main.cpp: no DSi, setCpuClock(true) (134 MHz); no DS normal nao faz nada.
- PixelText_Present: copia do quadro para a VRAM por DMA (DC_FlushRange + dmaCopyWords) em vez de laco da CPU.

## 17.29 - Free Duel: composicao mais barata (lido do medidor do video)
Video 18:06: logica L60 estavel; Free Duel rolando D17 W4, Build Deck/Chest D24-27 W4-W11, menu W3; picos W11/W12/W44/W103 em trocas de tela/carregamentos.
- FreeDuelScreen::composeFull: a moldura (320x240) agora so testa as 4 bordas (a janela central e transparente) em vez de 76 mil pixels; fundo de pedra converte 2 pixels por escrita de 32 bits. Saida identica bit a bit (7 quadros de preview conferidos).

## 17.30 - mapa 3D
Video 20:10 (35 fps): mapa (Card Shop/Town Plaza) rodava L35 D16 com pico W29 ao abrir; duelo com picos isolados W8-W16; entradas de dialogo/duelo W29/W93 (carregamento de arquivos).
- MapScreen: map3d.dat (518 KB) fica em memoria apos a 1a leitura (so no DSi); antes era lido inteiro a cada troca de local.
- Vinheta do holofote: 3 canais por multiplicacao empacotada (bit-exato); ampliacao 2x2 da camera em movimento escreve 32 bits. 15 quadros de preview identicos ao anterior.
- Nao tratado ainda: picos do duelo (render cheio do tabuleiro ao parar a camera) e leituras de bustos/cenas/cardart.

## 17.31 - menus: entradas sem releitura de arquivo (duelo intocado)
Video 20:21 (49 fps): menus em L60 estavel, mas picos W7-W13 ao ENTRAR em Free Duel, Build Deck/Chest, Library, Password, Nome; regime W3-W4.
- include/duel/ResidentAssets.h: Assets_KeepResident() = isDSiMode(). No DSi, FreeDuelScreen::close, DeckScreen_Close e Password_ReleaseAssets deixam freeduel.dat/deckui.dat/password.dat na memoria; a proxima entrada nao le nem analisa o arquivo de novo. No DS comum (4 MB) nada muda.
- Password/Library/Detalhe da carta: reducao 320x240->256x192 incremental (so linhas que mudaram; bit-identico; o cache e invalidado em todo open/close).
- Duelo nao foi alterado. Previews (password 17, library 4, name 9, deck 3 quadros) identicos ao anterior.

## 18.1 - lote 18: carregamentos e menus (duelo intocado)
- Art.cpp: arquivos de arte (busts, busts2, scenes, story, portraits, menu, title, dialog) ficam abertos entre leituras (ArtFopen/ArtFclose; cada uso volta ao inicio). Antes: fopen/fclose do NitroFS a cada busto, cena ou retrato. Saida conferida por hash (746 leituras x2, identica).
- FreeDuelScreen: fundo de pedra convertido uma vez para 16 bits (copia de linhas em vez de 45 mil consultas de paleta por passo de rolagem). Previews identicos.
- Continuam abertos: rolagem do Free Duel recompoe a janela inteira; duelo nao tocado.

## 18.2 - video 16:10 (58/60)
Medidor: L~60 em todos os menus; regime W2-W4; Free Duel/Chest D16-28 W4; pico W11 na 1a entrada no Chest. Duelo (W8-W83) nao tocado.
- DeckScreen: reducao 320x240->256x192 com campos empacotados (mesmo arredondamento; 3 previews identicos).
- DuelFieldMode::run: no DSi, depois da tela de credito, carrega freeduel.dat e deckui.dat (residentes); a 1a entrada no Free Duel/Build Deck nao tem pico.

## 18.3 - redesenho so do que mudou (video 16:23: L60 mas D15-25 W3-5 nos menus)
Causa: a logica roda a 60 mas cada redesenho de tela cheia (copia 98 KB + reducao + copia para a VRAM) custava 3-4 quadros, entao so saiam ~15-25 desenhos/s.
- PixelText_MarkDirtyRows / PixelText_PresentCount: o Present copia so a faixa de linhas marcada (DMA) quando quem desenhou garante que o resto do quadro de tras ja e igual a tela.
- Free Duel: o cursor/rastro restaura so o retangulo anterior a partir da camada estatica e redesenha so o novo; antes copiava a tela inteira a cada quadro. Conferido por hash da VRAM em 3 sequencias aleatorias de teclas (~4300 quadros): identico (tests/preview/equiv_freeduel.cpp).
- Build Deck/Chest: so as linhas refeitas vao para a tela; a caixa de info e a mensagem marcam suas linhas.
- Password/Library/Detalhe/Nome: reducao incremental agora so apresenta as linhas que mudaram, e so reaproveita o quadro anterior se nada foi apresentado entre os dois.
- Previews estaticos (password 17, library 4, name 9, deck 3, freeduel 7) identicos.

## 18.4 - Password e Library (video 16:46)
Medidor: Free Duel D19-26 W3-4, Chest D23 W4, Library D28-30 W2-3, Password D29 W9. Calibracao usada: 1 vblank de W ~ 64 us do desenho no PC (menu principal 70 us = W2, Free Duel 194 us = W3-4).
- Password: a carta era recomposta TODO quadro (incluindo o orbe com sqrt em ponto flutuante por software); agora so quando a carta muda (cache por carta/verso). Fundo de pedra em cache (copia em vez de limpar + converter 76 mil pixels). Girar a carta: 1 divisao por coluna (antes por pixel). Icones OK/END calculados uma vez. PC: 135 -> 63 us por quadro.
- Reducao incremental (Password/Library/Detalhe/Nome): so a faixa de colunas que mudou em cada linha e so copia o trecho alterado para o quadro anterior. Library 126 -> ~40-60 us. Saida da VRAM identica por hash (381 quadros Password+Library).
- Reducao 320x240->256x192 (Free Duel, Build Deck, Password): blocos de 4 colunas com pesos fixos (sem tabelas).
- Free Duel: margem do retangulo do cursor 12 -> 5 px; brilho aditivo do rastro em soma saturada empacotada. Hash da VRAM identico em 5 sequencias aleatorias.
- tests/preview/prof_password.cpp (tempo por quadro, HASH=1 imprime hash) e equiv_freeduel.cpp.

## 18.5 - Chest e rolagem do Free Duel (video 17:09)
Medidor: Library/Password D30 W1 (ok). Free Duel esq/dir D24-30 W2-3; cima/baixo (rolagem) D17-23 W3-4; Chest D17-28 W4. Rolagem = tela inteira refeita a cada passo.
- Build Deck/Chest: fundo dos paineis convertido uma vez (copia de linhas); sprites/texto com recorte por linha e sem teste por pixel. PC 245 -> 189 us por quadro; saida da VRAM identica por hash (3 sequencias aleatorias, 600 quadros cada; tests/preview/prof_chest.cpp).
- Free Duel: quando so a rolagem muda, a reducao 320x240->256x192 refaz so a janela e a barra lateral (antes: tela inteira). Instrucoes na rolagem -13%; hash identico (equiv_freeduel.cpp, VERT=1 para so cima/baixo).
- Limite honesto: um quadro de rolagem/troca de painel ainda refaz ~35-50 mil pixels; para cortar mais seria preciso trocar a reducao 5->4 por outra tecnica (muda a imagem) ou pre-reduzir os retratos.
