# YGOFM_DS — Yu-Gi-Oh! Forbidden Memories para Nintendo DS / DSi

Port **não oficial** e fiel de *Yu-Gi-Oh! Forbidden Memories* (PS1) para Nintendo DS/DSi, escrito do zero em C++ (devkitARM + libnds).
Testado em melonDS (modo DSi) e em um DSi XL real via nds-bootstrap.

> Unofficial fan port. English summary at the bottom.

## Status
Em desenvolvimento, entregue em "lotes". Já funcionam: campanha completa, duelos, fusões, equipamentos, loja, Build Deck fiel ao PS1 e cenas da história. Em andamento: Free Duel, Password, tela de nome, mapa 3D, memory card, Library, OPTION, 2P/Trade, áudio.
O histórico de cada lote está em [`docs/`](docs/).

## Importante: sem conteúdo do jogo neste repositório
Este repositório contém **apenas código e ferramentas**. Nenhuma ROM, ISO, arte, áudio ou dado do jogo é distribuído (veja `.gitignore`).
Você precisa da **sua própria cópia legal** do jogo (imagem do disco do PS1) para gerar os dados.

## Como compilar
Requisitos: [devkitPro](https://devkitpro.org/) com devkitARM, libnds e calico; Python 3.
1. Coloque sua imagem do jogo extraída em `original_iso/` (arquivos `WA_MRG.MRG`, `SLUS_014.11`, `DATA/*`).
2. Rode as ferramentas de `tools/` para gerar `data/bin/` e `nitrofiles/data/` (ex.: `python3 tools/extract_deckui.py original_iso data/bin`; veja os `LOTE*_CHANGES.md` para as demais).
3. `make` gera `YGOFM_DS.nds`.
4. Testes unitários no PC: `bash tests/run_tests.sh`.

## Controles (Build Deck)
D-pad move · L/R pagina · Y+L/R salta 50 · START/SELECT ordena · A move carta · B sai · X info · ←/→ troca de painel.

## Apoie o projeto
Se quiser ajudar a manter o desenvolvimento:

**[☕ Doar via PayPal](PAYPAL_LINK_AQUI)**

Doações são voluntárias e não dão direito a nada além da minha gratidão.

## Aviso legal
Yu-Gi-Oh! e Forbidden Memories são marcas e propriedade de Konami / Kazuki Takahashi / Shueisha. Projeto sem fins comerciais, sem afiliação ou endosso da Konami. Código sob licença MIT; o conteúdo do jogo continua sendo propriedade de seus donos.

## English
Unofficial fan port of Yu-Gi-Oh! Forbidden Memories (PS1) to Nintendo DS/DSi. Code and tools only — you must supply your own legally obtained game image. Build with devkitARM/libnds; see above. Donations: PayPal link above.
