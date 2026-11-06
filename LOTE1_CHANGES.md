# Lote 1 — motor de duelo (YGOFM_DS)

## Como aplicar
1. Faça `git init` + commit do projeto atual (ou mantenha seu backup).
2. Copie o conteúdo deste zip sobre a raiz do projeto (mesmas pastas `include/`, `source/`, `tests/`).
3. `make` como sempre. Nada muda no fluxo do jogo ainda (veja "O que NÃO muda").
4. Testes no PC (shell MSYS2 UCRT64, na pasta do projeto): `bash tests/run_tests.sh`
   Resultado esperado: `33749 verificacoes, 0 falhas`. Precisa de `data/bin/*.dat`.

## O que mudou
| Arquivo | Mudança |
|---|---|
| `source/DuelEngine.cpp` | `BuildDeck` corrigido; estrelas guardiãs na batalha; estrela gravada na invocação |
| `include/DuelEngine.h` | `guardianStar` em `DuelFieldCard`; `DuelEngine_GuardianStarBeats`; `DuelEngine_SetGuardianStar`; ganchos de teste (só com `-DYGOFM_TESTING`) |
| `include/GameData.h` | macro `GAMEDATA_ROOT` (padrão `nitro:/data/`, igual ao atual) |
| `source/GameData.cpp`, `source/EquipEngine.cpp` | usam `GAMEDATA_ROOT`; `GetCardById` com acesso direto (ids são 1..722) |
| `tests/` | 7 grupos de testes do motor, rodando no PC |
| `lote1.patch` | diff completo para revisar/aplicar com `git apply` |

### 1. BuildDeck (bug real, estava latente)
`duelist->deck[]` são **pesos de probabilidade** (soma 2048 nos 39 duelistas, verificado no `duelists.dat`), não quantidades de cópias. O código antigo preenchia o deck com a primeira carta de peso alto (ex.: 40 cópias da mesma). Agora são 40 sorteios independentes ponderados pelos pesos. Fonte: páginas FMR do Yugipedia (chance de cada uma das 40 cartas "out of 2048"). O teste mede a frequência real: carta 393 de Teana, esperado 7,81 cópias/deck, medido 7,88.
Hoje `DuelEngine_Start` não é chamado pela interface (ela monta deck próprio), então o jogo não muda até o lote 2.

### 2. Estrelas guardiãs
Numeração dos .dat: 1 Marte, 2 Júpiter, 3 Saturno, 4 Urano, 5 Plutão, 6 Netuno, 7 Mercúrio, 8 Sol, 9 Lua, 10 Vênus.
Ciclos: Marte>Júpiter>Saturno>Urano>Plutão>Netuno>Marte e Mercúrio>Sol>Lua>Vênus>Mercúrio.
Quem vence a estrela ganha +500 ATK/DEF **naquela batalha** (ataque direto não tem bônus). O jogador escolhe 1 das 2 estrelas ao invocar; a CPU sempre usa a primeira (Yugipedia, "Guardian Star").
Por enquanto a invocação usa a primeira estrela. A interface precisa chamar `DuelEngine_SetGuardianStar(slot, 0 ou 1)` (lote 2).

## O que NÃO muda
`GetFieldAttack/Defense` (valores exibidos na UI) continuam sem o bônus de estrela, que só existe na resolução da batalha.

## Pendências (não implementei de propósito, falta fonte confiável)
- **Tipos por terreno** (Forest, Wasteland, Mountain, Sogen, Umi, Yami): o bônus é ±500, mas não achei a tabela de tipos confiável. Preciso extrair do executável `SLUS_014.11` (Ghidra) ou de uma fonte verificável.
- **Fusão em cadeia** (mais de 2 cartas) e fusão com monstro em campo: regra exata ainda não confirmada.
- **Equip**: o motor soma +500 ATK **e** DEF; uma wiki diz +500 só de ATK (Megamorph +1000). Verificar no original.
- **equips.dat**: a lista de compatibilidade não se correlaciona com a estrela primária, ao contrário do que a wiki descreve (ex.: Salamandra e Marte). Pode ser erro de extração ou de interpretação. Vale conferir contra o jogo original.
- Bônus de estrela com defensor virado para baixo, e limite de cópias nos decks da CPU: marcados `[a confirmar]` no código.
