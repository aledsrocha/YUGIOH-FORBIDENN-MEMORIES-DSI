# Lote 8 — Exodia, rituais e deck de teste (YGOFM_DS)

Aplique SOBRE os lotes 1 a 7. Depois `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `39796 verificacoes, 0 falhas`), `bash tests/check_ui_syntax.sh`,
`bash tests/preview/run_preview.sh`, e a auditoria: `python3 tools/audit/audit_data.py --mrg original_iso/WA_MRG.MRG --exe original_iso/SLUS_014.11 --data data/bin --source source/DuelEngine.cpp` (esperado: `tudo confere`).

## Para você testar as magias: DECK DE TESTE
No menu de duelistas, **Y** alterna `Y: DECK BASIC` (cartas 1 a 40 embaralhadas, só monstros) e `Y: DECK TEST` (40 cartas de todos os tipos, **em ordem fixa, sem embaralhar**).
A mão inicial e as compras seguem esta ordem (cada jogada compra a próxima carta):
| Mão | Cartas | Para testar |
|---|---|---|
| 1 | Mystical Elf, Mushroom Man, Baby Dragon, Time Wizard, Megamorph | fusão em cadeia (Y nas cartas, depois A), Thousand Dragon, equip |
| 2 | Raigeki, Dark Hole, Swords of Revealing Light, Spellbinding Circle, Crush Card | magias de destruição, Swords, penalidade |
| 3 | Beaver Warrior, Gaia the Fierce Knight, Kuriboh, Black Luster Ritual, Forest | ritual Black Luster, terreno |
| 4 | as 5 peças do Exodia | vitória por Exodia (não jogue as peças) |
| 5 | Dian Keto, Hinotama, Red Medicine, Cursebreaker, Stop Defense | cura, dano, Cursebreaker |
| 6 | Blue-Eyes ×3, Ultimate Dragon (ritual), Salamandra | ritual com 3 Blue-Eyes |
| 7 | Flame Swordsman, Umi, Harpie's Feather Duster, Dragon Capture Jar, Shadow Spell | terreno, Jar, penalidade forte |
| 8 | Dark Magic Ritual, Winged Dragon #1, Dark Magician, Blast Juggler, Mountain | ritual Magician of Black Chaos |
O adversário continua com o deck real do duelista escolhido.

## Novidades
- **Exodia:** quem tiver na mão as 5 peças (cartas 17 a 21) vence na hora, logo após comprar (regra do original). Vale para a CPU também.
- **Rituais (as 24 do jogo):** com a carta de ritual destacada, um painel mostra a receita (`+` tributo em campo, `-` faltando). **A** joga: os 3 monstros saem e o monstro do ritual entra na zona do segundo tributo, virado para cima em ataque. Sem os tributos aparece `NEED THE 3 TRIBUTES` e a carta fica na mão (a jogada não é gasta). A tabela de receitas vem do disco e a auditoria a confere.

## Limites
- **Armadilhas e efeitos de monstros ficam para o lote 9**, junto do que a CPU vai usar; o deck de teste ainda não tem armadilhas.
- A posição do resultado do ritual (zona do segundo tributo, ataque, virado para cima) vem do código decompilado e da lógica de colocação; não confirmei se o original o coloca em ataque ou defesa.
- Não compilei para ARM; posições dos painéis escolhidas a olho.
- `ROTEIRO.md` traz o plano do que falta (gráficos, história, áudio) e o que "100% fiel" significa em cada parte.
