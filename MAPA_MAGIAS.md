# Mapa de magias, armadilhas e rituais (do jogo original)

Gerado da tabela `gDuelEffect_abGroupByEffectId` do executável. Ids de carta 301-350 e 651-700 (e 721) apontam para um índice de efeito:
índice = id − 301 (301-350), id − 601 (651-700); a Dark Magic Ritual (721) usa o índice 100. No motor: `DuelEngine_GetCardEffectGroup(cardId)`.

| Grupo | Cartas (id: nome, tipo) | Implementado |
|---|---|---|
| TERRAIN | 330: Forest (Magic); 331: Wasteland (Magic); 332: Mountain (Magic); 333: Sogen (Magic); 334: Umi (Magic); 335: Yami (Magic) | sim (lote 5) |
| LIFE_POINT_RECOVERY | 338: Mooyan Curry (Magic); 339: Red Medicine (Magic); 340: Goblin's Secret Remedy (Magic); 341: Soul of the Pure (Magic); 342: Dian Keto the Cure Master (Magic) | sim (lote 7) |
| DIRECT_DAMAGE | 343: Sparks (Magic); 344: Hinotama (Magic); 345: Final Flame (Magic); 346: Ookazi (Magic); 347: Tremendous Fire (Magic) | sim (lote 7) |
| BOARD_DESTRUCTION | 329: Dragon Capture Jar (Magic); 336: Dark Hole (Magic) | sim (lote 7) |
| RAIGEKI | 337: Raigeki (Magic) | sim (lote 7) |
| MONSTER_REMOVAL | 653: Warrior Elimination (Magic); 656: Eternal Rest (Magic); 660: Stain Storm (Magic); 661: Crush Card (Magic); 662: Eradicating Aerosol (Magic); 663: Breath of Light (Magic); 664: Eternal Draught (Magic) | sim (lote 7) |
| STOP_DEFENSE | 320: Stop Defense (Magic) | sim (lote 7) |
| DARK_PIERCING_LIGHT | 350: Dark-piercing Light (Magic) | sim (lote 7) |
| STAT_PENALTY | 349: Spellbinding Circle (Magic); 669: Shadow Spell (Magic) | sim (lote 7) |
| SWORDS | 348: Swords of Revealing Light (Magic) | sim (lote 7) |
| CURSEBREAKER | 655: Cursebreaker (Magic) | sim (lote 7) |
| HARPIES_FEATHER_DUSTER | 672: Harpie's Feather Duster (Magic) | parcial: sem magias/armadilhas em jogo ainda |
| RITUAL | 665: Curse of Millennium Shield (Ritual); 666: Yamadron Ritual (Ritual); 667: Gate Guardian Ritual (Ritual); 670: Black Luster Ritual (Ritual); 671: Zera Ritual (Ritual); 673: War-lion Ritual (Ritual); 674: Beastry Mirror Ritual (Ritual); 675: Ultimate Dragon (Ritual); 676: Commencement Dance (Ritual); 677: Hamburger Recipe (Ritual); 678: Revival of Sennen Genjin (Ritual); 679: Novox's Prayer (Ritual); 680: Curse of Tri-Horned Dragon (Ritual); 691: Revived of Serpent Night Dragon (Ritual); 692: Turtle Oath (Ritual); 693: Contruct of Mask (Ritual); 694: Resurrection of Chakra (Ritual); 695: Puppet Ritual (Ritual); 696: Javelin Beetle Pact (Ritual); 697: Garma Sword Oath (Ritual); 698: Cosmo Queen's Prayer (Ritual); 699: Revival of Skeleton Rider (Ritual); 700: Fortress Whale's Oath (Ritual); 721: Dark Magic Ritual (Ritual) | não |
| NONE | 44 cartas (equips e cartas sem grupo; equips têm fluxo próprio) | equips: sim (lote 5/6) |

**Armadilhas** (type 21) e **rituais** (type 22) ainda não têm efeito: são o próximo lote.
