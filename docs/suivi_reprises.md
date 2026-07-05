# Suivi des reprises v02 — source DXF

Référence : `docs/mail_bertrand_reprises_v02.txt`. Statuts :
**FAIT** / **À FAIRE** (lot suivant) / **DESSIN** (nécessite entités graphiques,
lot dédié) / **BLOQUÉ** (décision Bertrand, cf. CLAUDE.md) / **QUESTION**
(ambiguïté à lever par Alexandre).

## Pré-passe (avant réception du mail) — FAIT
Orthographe (soutènement/cintres HEB, 17× REVÊTEMENT, mécanique),
renvois « Détail n°18 » → « Détail folio 65 » (8), sommaire « sur paroi »,
onglets 38 + 53-58 renommés. Commit `c503e4c`.

## Transverses
| Item | Statut | Note |
|---|---|---|
| T1 Folio 00 références | À FAIRE (création) | avec valeurs C1 p.81 données au mail |
| T2 Légende complexe DEG harmonisée | À FAIRE partiellement | épaisseur écran sup = **BLOQUÉ** (19/10 vs 20/10) ; le reste (géotextile inf / PVC-P translucide 2 mm mini / écran sup) harmonisable |
| T3 Mortiers R3/R4 → NF EN 1504-3 | **FAIT** (lot 1) | 27 occurrences « NF EN 1504-3 » en fichier |
| T4 hydrogonflant partout | **FAIT** (lot 1) | 41 occ., 0 résidu hydro(-)expansif |
| T5 Enduit feu : renvoi référentiel exploitant + PV feu | À FAIRE | ~19 occ. « Enduit de protection au feu » ; formulation renvoi à ajouter |

## Folio par folio
| Folio | Reprise | Statut |
|---|---|---|
| P1 | casse renvois Détail n°1/2/3 vs folios 5/26/28 | À FAIRE (inspection casse) |
| P2 | R4→1504-3 | **FAIT** (lot 1, générique) |
| P2 | retour technique 1,00 m « à adapter selon hauteur d'eau / NDC » | **FAIT** (lot 2, #1FE5F) |
| P4/P20 | solin 3x3 époxy vs polymérique | **QUESTION** : quelle cible ? (P4=époxy, P20=polymérique, mail ne tranche pas) |
| P8 | renvoi explicite folios 30-33 | **FAIT** (lot 2, #12A34) |
| P9 | R4/retrait compensé →1504-3 | **FAIT** (lot 1) |
| P9 | NOTA préparation support voussoir (C1 §6.4) | À FAIRE (ajout MTEXT) |
| P10 | folio dédié arrêt DEG voussoir | À FAIRE (création n°2) |
| P11,16-19 | harmonisation casse/corps libellés | À FAIRE (inspection) |
| P12-14 | légender « Etanchéité par D.E.G. » | À FAIRE |
| P12-14 | cote 0,50 m signification | **QUESTION** (ambiguïté signalée par le mail lui-même) |
| P15 | écran protection sup. non légendé côté gauche | À FAIRE (inspection) |
| P20 | surfaçage époxy/R4 →1504-3 | **FAIT** (lot 1) |
| P21 | cohérence Min 1.00m vs folios 22-25 | À FAIRE (inspection cotes) |
| P22/23 | note découpe voussoir accord MOE GC | **FAIT** (lot 1, 3 occ.) |
| P24 | doublon joint hydrogonflant | **FAIT** (lot 1 : #EB7E supprimé, superposé à 0.00 u) |
| P25 | NOTA joints PM radier → renvoi folios 40-43 | **FAIT** (lot 2, #6651) |
| P27 | seuil hauteur d'eau > 10 m | **BLOQUÉ** (point 5) |
| P27 | tôle galva/inox harmonisation | **FAIT** (lot 2, #FEBB : « tôle (galvanisée ou inox) », + coquille « conformtement » corrigée ; seuil > 10 m intact) |
| P29 | plats galvanisés ou inox | **FAIT** (lot 1, #1637D) |
| P29/37 | entraxe fixations + couple serrage NDC + nature joints compressibles | À FAIRE (ajout de NOTA) |
| P30/32 | géotextile + cunette → renvois GT9.R19F1 | À FAIRE |
| P31/33 | NOTA continuité enduit imperméabilisation + phasage | À FAIRE |
| P34 | NOTA phasage (recépage→injection) | À FAIRE |
| P34/36 | chape protection DEG 5→6 cm | **FAIT** (lot 1, #6030 ; #6071 était déjà à 6) — vérifier folio 36 au lot 2 |
| P37 | idem P29 (entraxes/joints/résine) | À FAIRE |
| P38 | cotes engravures | **BLOQUÉ** (point 3) |
| P39 | NOTA contrôle pointe sèche / cloche à vide (C1 p.81) | À FAIRE |
| P41 | bande pontage : résine époxy + préparation | **FAIT** (lot 2, 4 occ. même objet F41/43/65) |
| P44 | légende exigences berlinoise (≤5 cm, chanfrein 45°, 90 kPa) | À FAIRE |
| P45 | raccord DEG/FPM | **BLOQUÉ** (point 4) |
| P45 | FPM bicouche anti-racine « uniquement si végétalisation » | **FAIT** (lot 2, #1746C) — #13E13 (F63) identique non modifié, voir Q6 |
| P47 | 6 cm conforme | référence — voir QUESTION « Béton de protection lourde 5 cm » ci-dessous |
| P48 | casse/unités | À FAIRE (inspection) |
| P49 | NOTA soufflet JD + non-adhérence locale | À FAIRE |
| P50 | anti-intrusion + entretenabilité sur le dessin | DESSIN |
| P51 | resurfaçage → 1504-3 R3 mini + tolérances | **FAIT** (lot 2, #130D3) |
| P52-54 | resurfaçage →1504-3 | **FAIT** (lot 2, 3 occ.) |
| P52-54 | tableau de choix EB/EH/EE en tête de section | À FAIRE (création) — cite C2 → dépend **BLOQUÉ** point 1 |
| P55/57/59 | NOTA carottages → cf. folio 50 | **FAIT** (lot 1, 3 occ.) |
| P55-60 | resurfaçage R3 →1504-3 | **FAIT** (lot 2, 6 occ.) |
| P56-60 | feuillard matériau + entraxe | **FAIT** (lot 1, 9 occ.) |
| P61 | « SEL-A sous référentiel CETU » | **FAIT** (lot 2 : légende #13DD7 + titre #15685) |
| P61 | recouvrements 20/20/15 vs CMO | **QUESTION** (vérification externe CMO) |
| P65 | engravure 20x220 probablement erronée | **QUESTION** (bonne valeur ?) |
| P65 | « centré 70 mm mini » → débord mini de part et d'autre | **FAIT** (lot 2, 2 occ.) |
| P65 | tôle galva/inox | déjà conforme (« galvanisé ou Inox ») |

## Questions ouvertes pour Alexandre (non bloquantes CLAUDE.md mais ambiguës)
1. **Solin 3×3 cm** : mortier époxy (folio 4) ou polymérique (folio 20) — quelle cible ?
2. **« Béton de protection lourde ép. 5 cm »** (~12 occ., folios 15/33/34/40-43/46/48/51…) :
   P47 valide 6 cm pour le béton de protection des remontées édicules — faut-il
   aussi basculer la « protection lourde » 5 cm → 6 cm, ou est-ce un autre élément
   (protection lourde horizontale) qui reste à 5 cm ?
3. **Cote 0,50 m** folios 12-14 : signification à confirmer avant de légender.
4. **P65 engravure 20×220 mm** : valeur de remplacement ?
5bis. **Anti-racine folio 63** (#13E13, même texte que folio 45) : appliquer la même
   condition « uniquement si végétalisation » ? Et le titre du folio 61 dit
   « D.E.G. - F.P.B » (F.P.B vs F.P.M ailleurs) : coquille à confirmer.
5. **Décimales** : convention source = point (197 occ.) ; la correction PDF
   « 1,00m » implique-t-elle une bascule générale en virgule ? (charte)

## Folios à créer (après reprises texte)
1. Folio 00 références+contrôles (valeurs C1 p.81 fournies) — À FAIRE
2. Arrêt DEG sur voussoir — À FAIRE
3. Drainage selon GT9.R19F1 — À FAIRE
4. Traversées courantes hors bride/contre-bride — À FAIRE
5. Tableau de choix DEG/SEL-A/FPM — dépend statut C2 (**BLOQUÉ** 1)
6. Réparation/réinjection compartiment DEG — À FAIRE

## 5 points BLOQUÉS (décision Bertrand Verrière) — intacts
Statut C2 · écran sup 19/10 vs 20/10 · engravures folio 38 · raccord DEG/FPM
folio 45 · seuil > 10 m folio 27.
