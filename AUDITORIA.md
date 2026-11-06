# Auditoria dos dados do YGOFM_DS contra o jogo original

**Método.** Rodei o decodificador do próprio `extract_tables.py` do projeto sobre o seu `WA_MRG.MRG`
(fusões, equips, pools dos duelistas) e li a tabela de stats do `SLUS_014.11` (722 palavras de
32 bits em `0x1C4A44`). Comparei tudo com `data/bin/*.dat`. A ferramenta é reutilizável:
`python3 tools/audit/audit_data.py --mrg original_iso/WA_MRG.MRG --exe original_iso/SLUS_014.11 --data data/bin`

## Resultado
| Arquivo | Estado | Detalhe |
|---|---|---|
| `fusions.dat` | **ERRADO** | 25.131 registros. O 2º material e o resultado estão **1 abaixo** do correto; o 1º material está certo |
| `equips.dat` | **ERRADO** | 4.041 pares. O monstro compatível está **1 abaixo** do correto; o equip está certo |
| `cards.dat` | **ERRADO (estrelas)** | ATK, DEF e tipo batem 722/722. As estrelas 1 e 2 estão **trocadas** em 621 cartas |
| `duelists.dat` | OK | os 4 pools (deck, pow, bcd, tec) batem 156/156 |

Tamanhos dos arquivos não mudam; os registros errados têm o mesmo formato.

## Provas independentes (não dependem só do decodificador)
- **Thousand Dragon** (id 69) = Baby Dragon (4) + Time Wizard (16), fusão conhecida do jogo. No original decodificado existe; no `.dat` antigo não.
- **Salamandra** equipa exatamente 31 monstros, **todos de estrela 1 = Marte**, e o único monstro de estrela 1 = Marte que fica de fora é o Thousand Dragon. É exatamente o que a wiki descreve. Isso confirma ao mesmo tempo a correção dos equips e a ordem das estrelas.
- **Sintoma real:** com os `.dat` antigos, a fusão (2, 8) devolvia a carta 469 em vez da 638, e (2, 10) não devolvia nada.

## Impacto
Fusões e compatibilidade de equips estavam todas erradas (nenhuma estava exposta no jogo ainda, por isso passou despercebido). A estrela "padrão", a que a CPU sempre usa e a que aparece marcada primeiro no seu painel, era a segunda estrela do jogo original.

## O que o código decompilado confirmou no motor
- Resolução de batalha (ataque x ataque, ataque x defesa, empate, dano ao atacante contra defesa mais forte): **o motor já estava certo**.
- Bônus de estrela: no original é **assinado (+500/−500) e aplicado só ao atacante**; o defensor usa o valor cru. O resultado é o mesmo do que eu tinha feito no lote 1 (defensor +500), mas agora a aritmética é a exata.
- Equip e terreno somam em **ATK e DEF**, e o resultado é limitado a **0..9999**. O motor não limitava.
- Tabela de **terrenos** por tipo de carta (Forest, Wasteland, Mountain, Sogen, Umi, Yami), que estava pendente.

## Ainda não auditado
- Nível e atributo das cartas, nomes e descrições. (Nomes de duelistas só diferem em espaço: "Villager1" x "Villager 1".)
- Valor do bônus de cada equip (o motor assume +500 para todos; o original tem exceções, como o Megamorph).
- Como o terreno é ativado (cartas de campo, terreno inicial), regras de fusão em cadeia, regra de "uma carta por turno", defensor virado para baixo, magias, armadilhas, rituais e IA. O código decompilado tem tudo isso (`fusion.c`, `ai_*`, `duel_effects.c`); é o próximo passo.

## Nota sobre o material usado
O `fontes_extrator.zip` contém código decompilado do jogo da Konami. Usei-o só para extrair regras e tabelas; o que entrou no projeto é uma tabela de dados (terrenos) e a aritmética do confronto de estrelas. Não distribua esses fontes decompilados junto com o projeto.
