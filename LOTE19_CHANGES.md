# Lote 19 - Sons (SE + BGM)

## Formatos decodificados
- SD_SE.DAT: 18 links; setor 1 = tabela (u16 off, pad, u32 size); dados SPU-ADPCM em 2+off; bloco SDSeq em start+ceil(size/2048): count, keys[u16] em +8, SDNote[8 bytes] em +0x1A0 (vol, timer, pitch, addr*16). Link 0 residente, 1 = duelo, 2 = menus/mapa, 3-17 = bancos de cenas.
- SD_BGM.DAT: 57 VAB + 60 SEQ. pacote=(cmd&0xFF0)>>4, seq=cmd&15 (base 0x7000 removida).
- Ferramentas: tools/sound/extract_sound.py original_iso/DATA <saida> [--wav DIR] [--only-se|--only-bgm]
  Gera nitrofiles/data/audio/ (se_NN.dat, se_index.dat, bgmPPS.dat). Musica vira IMA-ADPCM 22050 Hz estereo (sintese offline aproximada do SEQ+VAB).

## Motor (DS)
- AudioMixer: mixa musica IMA-ADPCM + ate 8 vozes de SE, fila de comandos (seguro em IRQ).
- Audio: saida por stream do maxmod (22050 Hz, timer 0). Makefile: -lmm9. Carga da musica progressiva (8 KB/frame em Audio_Pump).
- Trilhas grandes (creditos ~4 MB) precisam da RAM do DSi.

## Ganchos
SE: 6 cursor, 7 confirma, 8 cancela, 9 recusa, 30 troca de painel, 0x2F ordenar, 11 virar/alternar, 10 colocar carta, 0x10-0x12/0x1D impacto.
BGM: 0x7310 titulo/menu, 0x70E0 Build Deck, 0x72D0 Library/Password, 0x71D0 free duel, campanha usa o campo sound do duelista, 0x72F0 vitoria, 0x72E0 derrota, 0x7300 game over, 0x7330 creditos. Campanha: SCRIPT_SOUND/FADE_BGM via fila Campaign_PopSound.

## Limites
- Nao compilado para ARM aqui (init do maxmod / ARM7 padrao a validar no hardware).
- Sintese aproximada, nao ouvida; mapa de BGM por tela parcialmente presumido.
- Faltam SEs de compra de carta, fusao, magia/armadilha, LP, mudanca de fase.

## Lote 19.1 - fidelidade da musica (render2.py)
Regras reproduzidas do driver decompilado (ext/): tempo do jogo (passos = BPM*100/115, 738,3 chamadas/s, deltas /4 -> a musica toca ~25% mais rapida que o tempo nominal do SEQ), volume = CC7*CC11*prog*tom*velocidade ao vivo, pan linear (prog+tom+CC10-128), pitch bend so MSB, reverb por voz (CC91 / bit 4 do tom) com modo CC98=15 e profundidade CC98=16, ADSR cru do VAB, interpolacao cubica a 44100 Hz e decimacao com FIR (sem aliasing). IMA com busca em feixe (+~2 dB). O reverb e' aproximado (Schroeder por modo), nao o do SPU.
Saida do DS: sem maxmod (ring de 2 canais PCM16 + timers 2/3 do ARM9) - ver Audio.cpp.

## Lote 19.2 - causa raiz do som errado (conferido contra gravacao do PS1)
- Os VAGs (amostras) de cada pacote de SD_BGM.DAT ficam ANTES do cabecalho pBAV (logo apos os SEQs do pacote anterior, alinhados ao setor; pacote 0 comeca no setor 1). A leitura anterior pegava os bytes depois do cabecalho: o "primeiro instrumento" era o proprio SEQ. Corrigido em psx_audio.bgm_layout / parse_vab(vag_base).
- Andamento: medido contra o video do PS1 (fator 1,000 +-0,004): o jogo toca no tempo nominal do SEQ (a conta de 738 chamadas/s dava 25% mais rapido; usa-se 590,6).
- EQ de -3 dB (<400 Hz) e +3 dB (>1 kHz) medido contra o original (sobra <2 dB por banda).
- Musicas por tela (codigo decompilado): titulo/menu 0x7000, nome 0x7010, Free Duel 0x72C0, Build Deck 0x70E0, Password/Library 0x72D0, mapa 0x70A0 (0x70B0 apos o torneio), loja/opcoes 0x7350.

## Lote 19.3 - musicas conferidas contra a gameplay completa do PS1 + banner

Metodo: o audio do video (2h34) foi comparado com as 60 faixas renderizadas (notas + timbre + ritmo) e com as cenas.
Confirmado no video do PS1:
- Vitoria = 0x72E0 (toca uma vez por duelo ganho, 38 vezes); derrota ("YOU LOSE") = 0x72F0. Estava invertido.
- Password = 0x7350 (a musica da loja de star chips). Library = 0x72D0. Estavam iguais.
- Tela do sacerdote (Save / Build Deck / Return to title / Leave shop) = 0x70F0 (estava 0x7350).
- Ja corretos: titulo 0x7000, nome 0x7010, Build Deck 0x70E0, mapa 0x70A0, creditos 0x7330, musicas de duelo vindas do roteiro.
- shop.c / pack_shop.c / tower_screen.c do codigo decompilado sao do mod do PC, nao do jogo original: nao servem de referencia.
Banner: icone proprio (icon.bmp, 32x32, 16 cores), titulo YGOFM_DS e "by aledsrocha developer" (Makefile).
Nao verificado: efeitos sonoros (SE) por cena; game over (0x7300) e Free Duel (0x72C0) nao aparecem no video.

## Lote 19.4 - musicas do roteiro (causa raiz)

Causa: os comandos de som que ficam DENTRO dos dialogos (F8 0x0E musica, 0x0F musica com flags, 0x10 efeito, 0x11 fade) eram
ignorados pela campanha; so valiam os do roteiro de eventos. Por isso Heishin/Seto/Simon, a Tea, o torneio etc. ficavam com a
musica da cena anterior (ou a da loja). Agora Campaign.cpp executa esses comandos.
Conferido contra o video do PS1: a ordem de musicas 71B0, 7180, 71B0, duelo 7230, derrota 72F0, 71A0, 7050, 7040, 7030, 7090
coincide com o trecho Heishin -> torneio do video.
Tambem:
- a tela da loja (Save / Build Deck / Return to title / Leave shop) nao troca mais de musica: continua a da cena.
- SD_BGMPlay sempre reinicia a sequencia (Audio_RestartBGM nos pedidos da campanha).
- tela RESULTS toca 0x72E1 (vitoria) / 0x72F1 (derrota), como DuelScene_UpdateResultRewards.
- duelo e resultado atualizam "a musica atual" (Campaign_NoteBgm), usada pelos comandos guardar/restaurar do roteiro.
- Efeitos de voz do MASTER.XA (F8 0x10 com 0x8000) continuam sem suporte.

## 19.5 - Final do jogo (Main_RunCredits)
- Ao fim da campanha (SCRIPT_CREDITS): limpa as flags 0x20..0x11F, campanha volta ao evento 0x30, grava o jogo.
- Janela de aviso "ACCESSING MEMORY CARD" -> "SAVE COMPLETE!" (A avanca), tela "SECRET NO. xxxxxxxx" (um dos 5 numeros do executavel, escolhido pelo nome do jogador), e rolagem de creditos com fade por paginas ao som da faixa 0x7330, terminando em "Created by / Konami Computer Entertainment Japan"; A/B saem so depois da ultima pagina.
- `tools/extract_credits.py original_iso nitrofiles/data/credits.txt` gera o texto a partir de SU.MRG (rodar uma vez; o arquivo ja vai no pacote).
- Adaptacao: sem os monstros em wireframe do fundo; o numero secreto usa soma das letras do nome %5 (o original usa o codigo do duelista).
- Testes: ending verificado nos 42 percursos automaticos (flags limpas, cena 0x30, fases).

## 19.6 - Ajustes medidos nos 4 videos de referencia (nome, dialogo, password, fusao)
- Tela de nome (NameEntry_UpdateKeyboard / name_entry_dialog.c): mover cursor SE 47, escolher letra 41, apagar 12 (9 se nao ha o que apagar), setas de tamanho sem efeito 9, END com nome valido 48 (vazio 9), caixas de texto 11, gravar nome 45 + fade da musica.
- Dialogo: confirmar pagina/fim de texto toca SE 11 (func_80039794). Digitacao: 1 letra por quadro de 30 Hz (~30 letras/s; o video mede 27 a 36; antes eram 2 por quadro). Entre paginas a caixa limpa e a proxima so comeca ~0,37 s depois.
- Abertura do jogo (texto 0x546): caixa vazia por ~3,4 s (trecho de voz F8 10 0x8003 de 0x87 = 135 unidades de 1/40 s) antes da 1a imagem; essa pagina espera A com a imagem na tela; entre duas imagens a tela fica preta ~1,06 s (o PS1 le do CD); da tela preta para a 1a imagem nao ha fade-out.
- Password: setas esquerda/direita SE 47; carta encontrada SE 48 (antes 6/7). Subir/descer digito segue 6 (nao deu para confirmar no audio).
- Fusao (duel_scene_card_placement.c): SE 10 quando a carta entra, 24 no clarao da fusao, 25 quando a carta nova aparece grande, 26 na carta rejeitada. Os tempos entre 24 e 25 sao os do port (0,43 s; no video ~0,64 s).
