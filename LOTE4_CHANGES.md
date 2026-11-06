# Lote 4 — auditoria dos dados e fidelidade (YGOFM_DS)

Aplique SOBRE os lotes 1 a 3, copiando o conteúdo do zip para a raiz do projeto.
Depois: `make clean && make` (os `.dat` de `nitrofiles/data` vão dentro da ROM, então precisa recompilar).
No PC: `bash tests/run_tests.sh` (esperado: `39203 verificacoes, 0 falhas`).
Para reconferir os dados a qualquer momento: `python3 tools/audit/audit_data.py --mrg original_iso/WA_MRG.MRG --exe original_iso/SLUS_014.11 --data data/bin` (esperado: `tudo confere`). Precisa de Python 3; no MSYS2: `pacman -S python`.

Leia o `AUDITORIA.md`: ele explica o que estava errado e como foi provado.

## O que mudou
| Arquivo | Mudança |
|---|---|
| `data/bin/{cards,fusions,equips}.dat` e `nitrofiles/data/{cards,fusions,equips}.dat` | **corrigidos** (fusões e equips deslocados em 1; estrelas trocadas). `duelists.dat` já estava certo |
| `source/DuelEngine.cpp`, `include/DuelEngine.h` | bônus de estrela assinado exato (`DuelEngine_GuardianStarMatchup`); terrenos (`DuelEngine_SetTerrain`, `GetTerrainBoost`, campo `DuelState.terrain`); ATK/DEF limitados a 0..9999 |
| `tools/audit/audit_data.py` | auditoria e correção dos `.dat` contra o disco original |
| `tests/test_engine.cpp` | testes de dados contra valores do original, estrelas, terrenos e limites |

## O que você vai notar no jogo
- A estrela "primeira" de cada monstro muda (é a do jogo original): por exemplo, Blue-Eyes passa a mostrar Sol primeiro e Marte depois. O painel de estrelas e a estrela da CPU seguem isso.
- Fusões e equips ainda não aparecem na interface, mas o motor agora devolve os resultados certos.

## Limites
- **Terrenos:** a tabela e o cálculo estão no motor e testados, mas **nada ativa um terreno ainda** (falta implementar as cartas de campo e o terreno inicial). `DuelEngine_SetTerrain` existe para quando isso entrar.
- O bônus dos equips continua +500 para todos (não auditado).
- Não compilei para ARM; a checagem de sintaxe da interface continua passando (`bash tests/check_ui_syntax.sh`).
