# YGOFM_DS — Yu-Gi-Oh! Forbidden Memories para Nintendo DS / DSi

Port **não oficial** e fiel de *Yu-Gi-Oh! Forbidden Memories* (PS1) para Nintendo DS/DSi, escrito do zero em C++ (devkitARM + libnds).
Testado no melonDS (modo DSi) e em um DSi XL real via nds-bootstrap.

> Unofficial fan port. English summary at the bottom.

## Objetivo: 100% fiel

- **Regras, dados e comportamento do duelo:** alvo de 100%. Tudo é conferido contra o jogo original (tabelas do disco, constantes e textos do executável) e protegido por testes. A ferramenta `tools/audit/audit_data.py` re-audita os dados.
- **Imagem e som:** não dá para ser idêntico bit a bit. O DS tem tela de 256×192 (o PS1 usa 320×240), pouca RAM e nenhum decodificador dos vídeos do PS1. O alvo é **mesmo conteúdo e mesmo comportamento, com a apresentação adaptada** às duas telas do DS.

## Importante: sem conteúdo do jogo neste repositório

Este repositório contém **apenas código e ferramentas**. Nenhuma ROM, ISO, arte, áudio ou dado do jogo é distribuído. Você precisa da **sua própria cópia legal** do jogo (imagem do disco do PS1) para gerar os dados.

## Estado do projeto

O desenvolvimento é entregue em "lotes"; cada um tem suas notas em `LOTE*_CHANGES.md`.

| Área | Estado |
|---|---|
| Motor de duelo (fusões, equips, magias, rituais, armadilhas, Exodia, estrelas guardiãs, terrenos, cartas viradas) | Feito, com testes |
| IA dos duelistas (scripts do original) | Feito |
| Fluxo: recompensas, star chips, rank, baú, Build Deck, Password, Library, salvamento no cartão SD | Feito |
| História e campanha jogável (eventos, diálogos, mapa, loja, game over, finais) | Feito |
| Gráficos fora do duelo (título, menus, retratos, cenas) | Feito, com itens em aberto |
| Desempenho (60 fps nos menus) | Em ajuste (lote 18) |
| Áudio (lote 19) | Em andamento, ver abaixo |
| Teste em hardware real, pacote final | Lote 20 |

### Áudio (lote 19)

- Efeitos (`SD_SE.DAT`) e músicas (`SD_BGM.DAT`) são convertidos em PC por `tools/sound/extract_sound.py`. O formato dos efeitos e o driver de som do original foram decodificados; o sintetizador das músicas (`tools/sound/render2.py`) segue as regras do driver do jogo (tempo, volume, pan, pitch bend, reverb).
- No DS, `source/AudioMixer.cpp` mixa a música (IMA-ADPCM, 22050 Hz estéreo) e até 8 efeitos; `source/Audio.cpp` envia o resultado a dois canais PCM16 do libnds, sem depender do maxmod.
- **Limites conhecidos:** as músicas são sintetizadas (SEQ+VAB), não gravadas, e o reverb é aproximado, então o timbre pode diferir do PS1. Faixas longas (como os créditos) precisam da RAM do DSi. Os efeitos de fusão, magia/armadilha e mudança de fase no duelo ainda não estão ligados.

### Itens em aberto

- Tela "enigma se mexe" (falha visual), CPU atacando sem a cena de batalha, contagem gradual dos LP, página 2 do RESULTS, imagens originais das placas, arte da janela do memory card.
- Vídeos do PS1 (`MOVIE.STR`) não têm decodificador no DS; os modelos 3D viram imagens 2D.

## Como compilar

Requisitos: [devkitPro](https://devkitpro.org/) com devkitARM e libnds; Python 3 (com `numpy` e `scipy` para as ferramentas de áudio); `gcc` para compilar `tools/sound/ima.c`.

1. Extraia a sua imagem do jogo em `original_iso/` (`WA_MRG.MRG`, `SLUS_014.11`, `DATA/*`).
2. Gere os dados com as ferramentas de `tools/` (`extract_*.py`; os comandos de cada uma estão nas notas dos lotes). Elas escrevem em `data/bin/` e `nitrofiles/data/`.
3. Gere o áudio:
   ```
   gcc -O2 -shared -fPIC -o tools/sound/libima.so tools/sound/ima.c
   python3 tools/sound/extract_sound.py original_iso/DATA nitrofiles/data/audio
   ```
   (`--wav DIR` grava prévias em WAV para ouvir no PC.)
4. `make` gera `YGOFM_DS.nds`. Os arquivos de `nitrofiles/` vão dentro da ROM (NitroFS).
5. Para rodar no DSi real, use nds-bootstrap; no melonDS, ative o modo DSi (a RAM de 16 MB faz diferença).

## Testes (no PC)

```
bash tests/run_tests.sh        # motor, campanha e história
bash tests/check_ui_syntax.sh  # checagem de sintaxe das telas e do áudio
```

Os testes precisam dos `data/bin/*.dat` gerados no passo 2. `tests/audio/` tem um harness que renderiza o mixer no PC; `tests/preview/` gera prévias e medidas de desempenho das telas.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `source/`, `include/` | Motor de duelo, IA, campanha, história, perfil/salvamento, áudio |
| `source/duel/` | Telas e modo de campo: duelo, Build Deck, Free Duel, Password, Library, mapa, menu principal |
| `source/graphics/` | Renderização para as duas telas do DS |
| `tools/` | Extratores de dados do disco, auditoria, conversão de gráficos |
| `tools/sound/` | Conversão de efeitos e músicas |
| `tests/` | Testes de regras, prévias de telas e harness de áudio |
| `LOTE*_CHANGES.md`, `ROTEIRO.md`, `AUDITORIA.md` | Histórico, plano e auditorias |

## Controles (Build Deck)

D-pad move · L/R pagina · Y+L/R salta 50 · START/SELECT ordena · A move carta · B sai · X info · ←/→ troca de painel.

## Apoie o projeto

Se quiser ajudar a manter o desenvolvimento:

**[☕ Doar via PayPal](https://www.paypal.com/donate/?business=ZUFZ9T4PD792W&no_recurring=0&currency_code=USD)**

Doações são voluntárias e não dão direito a nada além da minha gratidão.

## Aviso legal

Yu-Gi-Oh! e Forbidden Memories são marcas e propriedade de Konami / Kazuki Takahashi / Shueisha. Projeto sem fins comerciais, sem afiliação ou endosso da Konami. Código sob licença MIT; o conteúdo do jogo continua sendo propriedade de seus donos.

## English

Unofficial fan port of Yu-Gi-Oh! Forbidden Memories (PS1) to Nintendo DS/DSi, aiming at the original's rules, data and behaviour with the presentation adapted to the DS's two screens. Code and tools only: you must supply your own legally obtained game image and generate the data with the scripts in `tools/`. Build with devkitARM/libnds (`make`); run the PC tests with `bash tests/run_tests.sh`. Audio is converted from the game's own sound data (`tools/sound/`) and played through libnds sound channels. Donations: PayPal link above.
