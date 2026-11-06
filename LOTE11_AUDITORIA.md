# Auditoria das regras de jogar cartas — Forbidden Memories (PS1)

Fonte: código descompilado do jogo (`duel_scene_hand_actions.c`, `duel_scene_field_actions.c`,
`duel_scene_card_placement.c`, `func_8001B938.c`, `func_8001D240.c`, `duel_selected_card_checks.c`).
**[C]** = lido direto no código. **[I]** = inferido; confirmar com vídeo/emulador.

Botões do PS1 citados: L2/R2 (bits 0x1/0x2), L1/R1 (0x4/0x8), Triângulo, Círculo, X, Quadrado,
Start, Cima/Baixo/Esquerda/Direita.

## 1. Fase da mão (jogador)
| Entrada | O que faz |
|---|---|
| Esquerda / Direita | move o destaque na mão (5 cartas) [C] |
| Triângulo | ver a carta [C] |
| Cima | **marca** a carta para combinação (guarda a ORDEM de marcação) [C] |
| Círculo ou Baixo | desmarca a última marcada [C] |
| L2 / R2 (segurar) | passa o cursor para olhar o campo [C] |
| X ou Quadrado | confirma. 0 marcadas = carta única (seção 2). **Exatamente 1 marcada = ignora.** 2 ou mais = vai direto escolher a zona (seção 4) [C] |

## 2. Carta única (nenhuma marcada)
A carta vai para o centro da tela, com dois ícones (virada para cima / para baixo).
- **Esquerda/Direita** alterna a face. [C]
- **Começa virada para baixo** se for monstro ou armadilha; começa virada para cima se for magia, equip ou ritual. [C — conferir no vídeo]
- **Círculo** cancela e a carta volta para a mão. [C]
- **X/Quadrado** confirma a face escolhida. [C]
- **Não existe escolha de ataque/defesa na invocação.** Monstro entra em ATAQUE, virado ou não. A posição só muda depois, no campo. [C]

## 3. Para onde vai a carta única (linhas do campo: 2 = monstros, 3 = magia/armadilha)
| Carta | Face | Resultado |
|---|---|---|
| Monstro | cima ou baixo | cursor só na linha de monstros: zona vazia, ou zona ocupada (funde/substitui) [C] |
| Magia comum (tipo 20) | para cima | **usada na hora**, sem escolher zona [C] |
| Ritual (tipo 22) | para cima | **usado na hora** [C] |
| Magia ou Ritual | para baixo | cursor só na fileira de magia/armadilha; fica baixada [C] |
| Equip (23) | para cima | cursor na linha de monstros. Zona vazia é **recusada**. Zona ocupada: qualquer monstro seu serve; se o equip não encaixar, a combinação falha (equip descartado, monstro fica) [C] |
| Equip | para baixo | vai para a fileira de magia/armadilha [C] |
| Armadilha (21) | qualquer | sempre fileira de magia/armadilha [C] |

## 4. Combinação (2 ou mais marcadas)
- Cursor na linha de monstros. Se a zona estiver ocupada, **o monstro do campo entra como primeira carta da cadeia**. [C]
- Cada passo tenta fusão, depois equip nas duas direções. Falhou com monstro + não-monstro: monstro fica. Outros casos: a primeira é descartada. [C — igual ao nosso `ChainStep`]
- Não há escolha de face na cadeia (o código pula a etapa). [I]

## 5. Fase do campo (jogador)
| Entrada | O que faz |
|---|---|
| Cursor | percorre as 4 linhas (oponente: 0 e 1; suas: 2 monstros, 3 magia/armadilha) [C] |
| L1 / R1 sobre monstro seu, ocupado e não usado | **gira a posição** (ataque ⇄ defesa). Não marca como usado, pode repetir. **Não desvira** o monstro. [C] |
| X/Quadrado em monstro seu | só vale se ocupado, **não usado e NÃO em defesa**. Depois escolhe o alvo na linha 1 (monstros do oponente). Linha vazia = ataque direto [C] |
| Quadrado (em vez de X) no alvo | mostra a batalha na arena 3D (não se aplica ao DS) [C] |
| X/Quadrado em carta da fileira de magia/armadilha | abre confirmação (sim/não) e usa a carta. Se for equip, escolhe depois um monstro seu ocupado [C] |
| X em carta do oponente | erro (som) [C] |
| Start | termina o turno [C] |

## 6. Diferenças em relação ao nosso projeto (a corrigir no lote 11)
1. **Invocação não escolhe ataque/defesa** (hoje X/Y escolhem). Deve entrar sempre em ataque. [alto]
2. **Face da carta única**: começa virada para baixo (monstro/armadilha) ou para cima (magia/equip/ritual), alternada com Esquerda/Direita. Hoje é R e começa para cima. [alto]
3. **Um único menu no X/A** para carta única, sem a tecla Cima (que passa a marcar para combinação, como no original). [alto]
4. **Uma só marcada é ignorada**; 2+ vão para a zona. [médio]
5. **Magia comum e ritual para cima = uso imediato** (já é assim); virados vão para a fileira (já é assim). **Equip para cima em zona vazia deve ser recusado** e hoje nós abrimos seleção de monstro com filtro de compatibilidade; o original deixa escolher qualquer monstro. [alto]
6. **Girar posição não revela o monstro virado**. Nosso `DuelEngine_ChangePosition` revela ao virar para ataque. [alto]
7. **Girar posição não marca como usado**; só `hasAttacked` bloqueia. O engine já bloqueia só pelo ataque. [ok]
8. **Ataque**: monstro em defesa não ataca (ok). Ataque direto só com a linha do oponente vazia (ok).
9. Fileira de magia/armadilha: **usar carta baixada pede confirmação**. [baixo]
10. Armadilha baixada pode ser **selecionada manualmente** no original (mesmo caminho das magias). Precisa de teste. [I]

## 7. O que ainda preciso ver em vídeo
- Se monstro e armadilha realmente começam virados para baixo na carta única.
- O que acontece ao usar à mão uma armadilha baixada.
- A cadeia de 2+ cartas: se a face pode ser escolhida.
- A confirmação (sim/não) ao usar carta baixada.

## 8. Confirmado no vídeo (gravação do jogo no emulador)
- Monstro da mão chega ao centro **virado para baixo** e foi baixado em **ataque**; na batalha usou ATK 2800 contra 2700 e sobreviveu. [confirmado]
- Equip da mão chega **virado para cima** com setas ← → (alternam a face). Face para cima: cursor na linha de monstros, para em qualquer monstro (inclusive um que não aceita o equip). Face para baixo: vai para a fileira de magia/armadilha. [confirmado]
- Cartas marcadas mostram o número da ordem (1, 2, 3). [confirmado]
- Dúvida aberta: a combinação Sorcerer of Dark Magic + Ritual Weapon + Mage Power chegou a +2500, e pelo código do PS1 seria +1000. Verificar se a gravação usa o disco original.

## 9. Lote 11 — o que foi feito
- Carta única: A abre o centro; ← → / L / R alternam a face; A confirma; B cancela.
  - Monstro: começa virado, entra sempre em ATAQUE. X/Y de posição foram removidos.
  - Magia e Ritual: para cima = usa na hora; para baixo = baixa na fileira.
  - Equip: para cima = escolhe qualquer monstro seu (se não servir, o equip é descartado, "NO EFFECT"); para baixo = baixa na fileira.
  - Armadilha: sempre baixada.
- Cima marca/desmarca a carta para combinação (como no original). Y continua marcando.
- Girar posição não desvira o monstro. Equip sobre o mesmo monstro não o desvira.
- Equip baixado também vale em qualquer monstro.
