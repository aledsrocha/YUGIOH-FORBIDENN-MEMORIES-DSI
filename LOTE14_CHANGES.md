# Lote 14 - salvamento, flags, registros e cartas vistas

## Salvamento
- Arquivo `fat:/ygofm_ds.sav` no cartao SD (libfat; o `-lfat` ja estava no Makefile). No melonDS precisa de cartao SD/DLDI configurado, ou o DSi com SD; sem isso o jogo avisa "NO SD CARD" e segue sem salvar.
- Como no original: dois blocos identicos no arquivo; vale o primeiro bloco valido. Cada bloco tem assinatura `YGOFMDS1`, versao, tamanho e CRC32.
- Conteudo: star chips, vitorias/derrotas totais, deck de 40, baú (722 bytes), 16 cartas recentes, **array de 2048 flags** (256 bytes, MSB primeiro, mesma numeracao do jogo: 0x120+carta = vista, 0x400+carta = senha usada, 0x6E0+id = Free Duel liberado, 0x1F+id = duelista derrotado) e a grade de registros (40 x vitorias/derrotas).
- Dados invalidos sao recusados mesmo com CRC certo (carta 999 no deck, baú acima de 250...); numa carga recusada o perfil em memoria nao muda.
- Ao abrir o jogo ele carrega o arquivo se existir; senao comeca um jogo novo. **Nao ha salvamento automatico** (como no original): use SAVE no menu principal. NEW GAME pede A duas vezes e nao apaga o arquivo ate voce salvar.

## Registros e Free Duel
- Cada duelo concluido soma vitoria/derrota ao duelista (maximo 999) e aparece como `W n L n` no menu de duelistas.
- Duelistas bloqueados aparecem como `?????` e recusam o duelo ("NOT UNLOCKED YET"). **Enquanto nao houver campanha (lote 16) o jogo novo libera todos os 39**; a campanha passara a liberar um a um (os flags ja existem).

## Library
Cartas que aparecem no duelo ficam "vistas": as que voce baixa/funde/ritualiza e as reveladas em batalha (as viradas da CPU so depois de aparecerem). Entram na Library ao fim do duelo.

## Arquivos
`include/DuelEngine.h`, `source/DuelEngine.cpp`, `include/Profile.h`, `source/Profile.cpp`, `include/SaveStorage.h`, `source/SaveStorage.cpp` (novo), `include/duel/FrontEnd.h`, `source/duel/FrontEnd.cpp`, `source/duel/DuelFieldMode.cpp`, `source/duel/DuelOverlays.cpp`, `tests/*`.

## Limites conhecidos
- Nome do jogador e codigo do duelista (tela de nome) entram com a campanha.
- Duvida de fidelidade: se a carta virada da CPU revelada so por efeito (magia) tambem conta como vista; deixei so por batalha.
- Testado no PC: 96.807 verificacoes, 0 falhas (inclui gravar/ler arquivo, corromper um e os dois blocos). Nao compilei para ARM.

## 14.1 - correcao: o save nao gravava
Causa provavel: o emulador/console nao tinha cartao SD (DLDI) e o jogo so tinha o caminho do SD; antes ele so dizia "NO SD CARD" se voce notasse a mensagem.
Agora:
- Se nao ha SD, o jogo tenta a **memoria de save do cartucho** (EEPROM/FLASH) e so diz "SAVED" depois de ler de volta e conferir.
- A frase de status mostra exatamente o que aconteceu: GAME SAVED TO SD CARD / TO CARTRIDGE / NO SD CARD (ENABLE DLDI) / SD CARD IS READ-ONLY OR FULL. Ao abrir o jogo a mesma linha aparece no menu principal (SAVED GAME LOADED FROM SD, NEW GAME...).
- No melonDS: Config > Emu settings > DLDI > marque "Enable DLDI (for homebrew)" e use uma imagem SD ou uma pasta sincronizada (sem "read only"). No DSi/DS real use um cartao SD no flashcart.
