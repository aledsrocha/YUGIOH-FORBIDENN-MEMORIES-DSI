# Lote 8.1 — correção dos equips (YGOFM_DS)

Aplique SOBRE o lote 8 e rode `make clean && make`.
No PC: `bash tests/run_tests.sh` (esperado: `40035 verificacoes, 0 falhas`).

## O bug
**O jogo nunca carregava os dados de equip.** `GameData_LoadAll()` carregava cartas, fusões e duelistas, mas só lia o cabeçalho do `equips.dat`; quem carrega as listas de compatibilidade é `EquipEngine_Load()`, e **ninguém a chamava**. Resultado: nenhum equip era compatível com nenhum monstro. Por isso as cartas de equip (as de Megamorph, as de cada tipo de monstro, as de atributo) apareciam na mão e não podiam ser usadas, nem em campo nem dentro de uma fusão.

Meus testes não pegaram porque chamavam `EquipEngine_Load()` à mão, caminho que o jogo não usa. A culpa é minha. O teste agora usa só o caminho real e foi validado ao contrário: reintroduzindo o bug, ele falha na primeira verificação ("carregou 0 equips").

## O que mudou
| Arquivo | Mudança |
|---|---|
| `source/GameData.cpp` | `GameData_LoadAll()` passa a chamar `EquipEngine_Load()` |
| `source/EquipEngine.cpp` | `EquipEngine_Load()` zera a contagem antes de ler (recarregar é seguro) |
| `source/duel/DuelFieldMode.cpp/.h`, `DuelOverlays.cpp/.h` | A em uma carta que não pode ser jogada agora **avisa o motivo**, em vez de não fazer nada: `NO MONSTER CAN USE IT` (equip sem monstro compatível em campo) e `ALREADY PLAYED A CARD` (já gastou a jogada do turno) |
| `tests/test_engine.cpp` | `TestEveryEquip`: os 34 equips, cada um no seu primeiro monstro compatível, recusa de um monstro fora da lista, o bônus certo (Megamorph +1000, os demais +500) e o equip dentro de uma cadeia de fusão |

## Como usar um equip
1. Coloque um monstro compatível em campo (invoque).
2. Destaque o equip na mão e aperte **A**: ESQ/DIR escolhe o monstro (só aparecem os compatíveis), **A** equipa, **B** cancela. O painel mostra ATK e DEF antes e depois.
3. Ou marque o monstro e o equip com **Y** (nessa ordem ou na inversa) e aperte **A**: eles viram um monstro já equipado na zona escolhida.
Lembre: a jogada do turno é uma só (invocar, equipar, jogar magia ou ritual).

## No deck de teste
Mão 1 traz Mystical Elf, Mushroom Man, Baby Dragon, Time Wizard e **Megamorph**: invoque o Time Wizard, depois equipe o Megamorph nele. A Salamandra está na mão 6 e só serve em monstros de estrela 1 = Marte (por exemplo, o Flame Swordsman, que vem na mão 7).
