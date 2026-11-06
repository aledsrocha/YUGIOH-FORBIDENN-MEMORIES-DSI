# Lote 10 - cartas viradas completas + IA dos duelistas

## Cartas viradas (jogador)
- Magia comum: usar na hora OU baixar virada na fileira; a virada pode ser usada depois.
- Equip: equipar direto num monstro do campo OU baixar; o equip virado pode ser usado depois num monstro.
- Ritual baixado pode ser ativado depois (DuelEngine_ActivateSetRitual / ActivateSetEquip).
- Fusao encadeada sobre monstro que ja esta no campo (DuelEngine_FuseChainOntoField).

## IA (nova)
- include/DuelAI.h, source/DuelAI.cpp: VM da IA do PS1 (67 opcodes, 20 registradores).
- source/AiScripts.cpp: scripts dos 39 duelistas + tabela de parametros (extraidos do disco).
- DuelEngine: a CPU antiga foi trocada por RunOpponentAI (mao + campo, ate 40 passos).
- Eventos novos para o jogador ver a CPU: CPU_SPELL, CPU_RITUAL, CPU_EQUIP, CPU_SET.
- Fila de eventos ampliada de 16 para 32.

## Testes
40.796 verificacoes, 0 falhas (inclui os 39 duelistas jogando 40 turnos sem travar).

## Para testar
make clean && make. Verificar: baixar magia/equip virados e usar depois; CPU baixando cartas,
mensagens "OPPONENT ..."; regra de uma jogada por turno; 1o turno sem ataque.

## 10.1
- Virado nao forca mais defesa: posicao e virada sao independentes (X ataque / Y defesa / R vira).
  A IA continua baixando virado em defesa.
- Zona de monstro ocupada agora pode ser escolhida ao jogar da mao: funde (se houver fusao/equip)
  ou substitui o monstro. API: DuelEngine_FuseChainOntoFieldEx.
