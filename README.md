# PS1_DSI — emulador de PlayStation para Nintendo DSi

Emulador de PlayStation (PS1) que roda **direto no hardware do Nintendo DSi**,
sem cartuchos com processador extra (como o SuperCard DSTWO).

> **Status: experimental.** *Marvel vs. Capcom* chega à tela de título e *Yu-Gi-Oh!
> Forbidden Memories* ao menu inicial, mas a uns 5–6% da velocidade real.
> Ainda não dá para jogar.

<!-- coloque aqui um print: ![Marvel vs. Capcom no DSi](docs/mvc.png) -->

## O que já funciona

| Parte | Estado |
|---|---|
| CPU R3000A | ✅ recompilador MIPS → ARM (experimental, ~3x mais rápido) + interpretador |
| GPU (desenho em software) | ✅ triângulos, sprites, transferências, frameskip |
| CD-ROM (.cue/.bin, .iso) | ✅ boot de jogos, leitura de dados, XA ignorado |
| GTE (geometria 3D) | ✅ portado do pcsx4all, validado contra o original |
| Controle | ✅ controle digital |
| Pular a intro da BIOS | ✅ |
| Áudio (SPU) e vídeo (MDEC) | ⏳ etapa 6 |
| Recompilador: ligação de blocos, GPU pelo 3D do DS | ⏳ etapa 7 (velocidade) |
| Memory card no SD (slot 1) | ✅ `/psx/mcd001.mcr`, formato padrão (compatível com outros emuladores) |

## Como usar

1. Compile com o [devkitPro](https://devkitpro.org) (devkitARM + libnds + libfat):
   ```sh
   make clean && make
   ```
2. Copie `PS1_DSI.nds` para o cartão SD.
3. Copie **a sua** BIOS do PS1 (`scph1001.bin`, 512 KB) para `/psx/` ou para a raiz do SD.
4. Coloque os jogos (`.cue` + `.bin`, ou `.iso`) em `/games` (ou `/psx/games`, `/psx`, `/`).
5. Abra no DSi em **modo DSi** (16 MB / 133 MHz), por exemplo pelo Unlaunch.

Controles no seletor: **A** abre, **B** volta, **SELECT** liga/desliga pular a
intro da BIOS, **L/R** frameskip, **X** alterna CPU recompilador/interpretador.

Controles no jogo (mesma posicao do controle do PS1):

| DS | PS1 |
|---|---|
| Direcional | Direcional |
| X / A / B / Y | △ / ○ / ✕ / □ |
| L / R | L1 / R1 |
| Toque na metade esquerda / direita da tela de baixo | L2 / R2 |
| START / SELECT | START / SELECT |
| START + SELECT | sai (grava o memory card antes) |

O emulador grava `/psx_log.txt` no cartão (console do PS1, comandos de CD, erros).
Os saves ficam em `/psx/mcd001.mcr` (gravados no SD cerca de 1 s depois de o jogo salvar).

> Este projeto **não** inclui BIOS nem jogos. Use apenas cópias suas.

## Testes no PC

`pc_test/` roda o mesmo núcleo do emulador no PC e salva a tela em imagem:
```sh
cd pc_test && ./build.sh
./psx_pc 60 "/caminho/jogo.cue" fast
```

## Apoie o projeto

O PS1_DSI é livre e gratuito, e vai continuar assim. Se você gosta do projeto
e quer ajudar no desenvolvimento (tempo de trabalho e hardware de teste),
considere uma doação:

[![Doar com PayPal](https://img.shields.io/badge/PayPal-Doar-00457C?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?business=ZUFZ9T4PD792W&no_recurring=0&currency_code=USD)

Obrigado a todos que apoiam!

## Créditos e licença

- Núcleo (CPU, GPU, CD, DMA, timers, front-end do DS): escrito para este projeto,
  com base na documentação [psx-spx](https://psx-spx.consoledev.net/) (Martin Korth / nocash).
- GTE: portado do [pcsx4all](https://github.com/dmitrysmagin/pcsx4all)
  (PCSX / PCSX-Revolution / PCSX-ReARMed), GPL v2+.
- Desenvolvido por Alessandro Rocha com assistência de IA.

Licença: **GNU GPL v3 ou posterior** — veja [COPYING](COPYING) e [CREDITOS.txt](CREDITOS.txt).

---

**English:** experimental PlayStation emulator for the Nintendo DSi (native ARM9,
no add-on hardware). Boots commercial games (e.g. *Marvel vs. Capcom*) at ~6%
speed; a MIPS→ARM dynarec is next. GPL v3+. No BIOS or games included.
Donations: [PayPal](https://www.paypal.com/donate/?business=ZUFZ9T4PD792W&no_recurring=0&currency_code=USD).
