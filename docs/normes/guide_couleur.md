# Guide couleur du carnet (relevé des calques de la source DXF)

Relevé exhaustif des calques porteurs de géométrie dans le Model de
`source/carnet_v02.dxf` (lot N10, 2026-07-14). **Règle pour toute
modification graphique : dessiner sur le calque sémantique existant — la
couleur, le type de trait et le comportement d'impression suivent
automatiquement (couleurs en BYLAYER).**

## Systèmes d'étanchéité (calques `SYSTEME_*`)
| Calque | ACI | Couleur | Usage |
|---|---|---|---|
| SYSTEME_DEG_ Geomembrane SYNTHETIQUE | 1 | rouge | géomembrane PVC du DEG |
| SYSTEME_DEG_Protection superieure | 5 | bleu | écran de protection sup. |
| SYSTEME_DEG_Protection inferieure | 3 | vert | géotextile inférieur |
| SYSTEME_DEG_Complexe complet | 4 | cyan | complexe DEG symbolisé |
| SYSTEME_FPM_Feuille Bitume + enduit d'imperméabilisation | 4 | cyan | feuille FPM |
| SYSTEME_FPM_GEOTEXTILE de protection | 3 | vert | protection FPM |
| SYSTEME_FPM_Enduit EIF | 6 | magenta | enduit d'imprégnation |
| SYSTEME_FPM_Géotextile de filtration thermosoudé | 210 | violet | filtration |
| SYSTEME_S.E.L.A | 210 | violet/magenta | SEL armé (le « rose » des rendus) |
| SYSTEME_S.E.L | 30 | orange | SEL non armé |

## Matériels (calques `Matériel_*`)
| Calque | ACI | Couleur | Usage |
|---|---|---|---|
| Matériel_Joint Hydroexpansif | 140 | bleu clair | joints hydrogonflants (⚠️ calque nommé « Hydroexpansif », textes du carnet = « hydrogonflant » — ne pas renommer sans décision) |
| Matériel_Profilé de compartimentage | 7 | noir/blanc | profilés |
| Matériel_Gaine d'injection | 203 | rose pâle | gaines/pipettes |
| Matériel_Feuillard-Solin | 40 | orange | feuillards, solins |
| Matériel_Bande de pontage | 40 | orange | bandes de pontage |
| Matériel_Profilé PM200 | 40 | orange | profilé PM200.3 |
| Matériel_Bride contre bride | 7 | noir | brides |
| Matériel_Profilé d'arrêt d'eau paroi moulée | 3 | vert | BAE |
| Matériel_Resine | 230 | rose | résines |
| Matériel_Tôle colaminée | 90 | vert foncé | tôles colaminées |
| Matériel_Micropieu | 35 | brun | micropieux |
| Matériel_Prise de terre | 211 | rose clair | prises de terre |
| Matériel_Drain-Tube PVC | 4 | cyan | drains |
| Matériel_Soudure manuelle | 11 | rouge pâle | soudures |
| Matériel_Mastic | 30 | orange | mastics |
| Matériel_Plaque acier galva / Profilé Flagjoint | 50 | jaune | aciers galva |
| Matériel_Fixation mécanique | 7 | noir | fixations |
| Matériel_Bande elastomérique de pontage | 236 | rose foncé | bandes élastomères |
| Matériel_Tole de protection en acier galva ou inox | 102 | vert-jaune | tôles de protection |

## Produits (calques `Produit_*`)
| Calque | ACI | Usage |
|---|---|---|
| Produit_Enduit de protection au feu | 6 (magenta) | enduits feu |
| Produit_Imperméabilisation | 219 (violet-rose) | enduits d'imperméabilisation |
| Produit_ Colle PMMA ALSAN 075 | 240 | colle PMMA |
| Produit_Résine REKU P70 | 190 | résine |

## Fond de plan (calques `Dessin_*` et divers)
| Calque | ACI | Usage |
|---|---|---|
| Dessin_CONTOURS BETON | 7 | contours béton (noir) |
| Dessin_TEXTES | 7 | textes d'annotation (h≈2,5 ; NOTA lots 3-4 posés ici) |
| Dessin_HACHURES | 253 (gris clair) | hachures béton/terrain |
| Dessin_AXE | 8 (gris) | axes |
| Dessin_COTATIONS | 7 | cotes |
| Dessin_Cadres | 7 | cadres des sous-détails |
| GEN-* / XREF-* / PAY-* | divers | gabarit générique (ne pas utiliser) |
| Defpoints / 0-NON_IMPRIMABLE_CONSTRUCTION / GEN-_-FMULT | plot=0 | jamais imprimés (exclus du PDF) |

## Règles d'intervention graphique (lot N12 et créations N13-N14)
1. Nouvel élément d'étanchéité → calque `SYSTEME_*` correspondant.
2. Nouvel accessoire → calque `Matériel_*` correspondant (créer un calque
   `Matériel_<nom>` sur le modèle existant si le matériel n'existe pas).
3. Textes/NOTA → `Dessin_TEXTES`, style txt-moyen, h=2,5, ByLayer.
4. Contours/cadres → `Dessin_CONTOURS BETON` / `Dessin_Cadres`.
5. Couleur toujours **BYLAYER** (jamais de couleur explicite d'entité).
6. Ne jamais dessiner sur les calques plot=0 ni `GEN-*`.
