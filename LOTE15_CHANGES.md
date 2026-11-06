# Lote 15 - dados da historia (roteiro de eventos + textos de dialogo)

Nada novo aparece na tela neste lote: e a base da campanha (lote 16). Tudo e logica pura, testada no PC.

## Extraido do disco original (`tools/extract_story.py original_iso data/bin`)
- `story_events.dat`: roteiro de eventos (WA_MRG 0xF34000, 0x1000 bytes): tabela de 199 eventos + fluxos de bytes.
- `story_text.dat`: tabela de glifos (0x5C, ja em ASCII), tabela de ids (0x000-0x0FF e 0x500-0x5F9) e o banco de 64 KB de dialogos (bytecode do jogo). Textos em ingles originais.
- Copiados para `data/bin/` e `nitrofiles/data/`.

## Interpretador de texto (`include/Story.h`, `source/Story.cpp`)
`TextReader_Begin/Next/Choose/Jump`. Implementa o bytecode do jogo: glifos, F6 (retrato), F7 (estados, com operandos), F8 (comandos secundarios, com contagem de operandos de cada um), F9 (flag: escrita 0x4000 ou teste + salto; bit 0x8000 = inverte/limpa), FA (pagina), FB (preparo de escolha e tabela de saltos), FC (chamada, ate 8 niveis), FD (salto), FE (linha), FF (fim/retorno). A contagem de opcoes persiste entre strings, como no jogo.
- F8 19 (desbloquear duelista) ja aplica as flags 0x1F+id e 0x6E0+id no perfil.
- F8 0D (descritor de duelo da campanha: oponente, terreno, som) via `Story_ParseDuelDescriptor`.
- Buffers de execucao (nomes de carta etc.) saem como `TEXT_BUFFER` para a interface preencher.

## VM de eventos (`ScriptVM`, `Script_Begin/Next`)
Os 23 opcodes com os operandos lidos do codigo original; fluxo (saltos, testes de flag, escrita de flag, "baralho incompleto") e resolvido dentro da VM; a VM devolve passos observaveis (cena, dialogo, mapa, menu, som, duelo, game over, creditos...). A campanha (lote 16) so precisa executar cada passo.

## Testes (`tests/test_story.cpp`, entra em `tests/run_tests.sh`)
- Percorre os 199 eventos 120 vezes cada com flags aleatorias: todos terminam, opcodes validos, todo dialogo existe.
- Percorre todos os ~360 textos (0x000-0x0FF, 0x500-0x5F9) com flags e escolhas aleatorias: todos terminam sem comando desconhecido; 38 oponentes de campanha (ids 1-39) e 38 desbloqueios encontrados.
- Resultado: 123.722 verificacoes na historia + 96.807 do motor, 0 falhas. Nao compilei para ARM.

## Observacoes
- Dialogo de id 0 e texto vazio (aparece nos eventos de loja/mapa).
- Semantica visual dos F8 (sons, camera) e das imagens fica para os lotes 16-17.
