# Rapport de mise à jour du carnet selon le corpus normatif — juillet 2026

Campagne autonome demandée par Alexandre (2026-07-13) : prise en compte des
11 documents normatifs transmis (`docs/normes/`), modifications texte et
graphiques (guide couleur du carnet respecté), production du PDF couleur.
Suivi d'exécution : `docs/suivi_normes.md` (lots N0-N17, tous FAIT).
Extraits de lecture : `docs/normes/extraits_*.md` (6 fichiers).

## 1. Modifications APPLIQUÉES au carnet (avec justification normative)

| # | Folio(s) | Modification | Justification | Norme citée |
|---|----------|--------------|---------------|-------------|
| 1 | 15, 33, 34, 40-43, 46, 48, 51, 61-63 (34 occurrences) | « Béton de protection lourde ép.**5cm** » → « ép.**6cm** » (toutes variantes : 5cm, 5cm mini) | La protection complémentaire normalisée est de 6 cm de béton dans toutes les configurations (radier sur béton de propreté, dalle de couverture, voûte à couverture ≤ 0,50 m) ; cohérent avec les reprises P34/36 (chape DEG 5→6, lot 1) et P47 (« 6 cm conforme ») déjà actées au mail | **GT9.C5F1** (prépublication) tableaux 1-3 |
| 2 | 30 | NOTA : ≥ 3 pipettes par compartiment, regroupées en boîtier dans un poteau/voile de refend (pas en surface de radier) | Prescription d'exécution du raccord scellé sous radier ; un boîtier en surface de radier se remplit d'eau de chantier | **GT9.C10F1 §7.1** (publication) |
| 3 | 32 | NOTA : surface maximale de compartimentage 250 m² sous pression hydrostatique / 350 m² hors pression | Valeurs d'exécution du compartimentage DEG (le carnet n'indiquait que la position du profilé) | **F67-III art. 3.3.1.d** (comm. 84 : seuil 0,3 MPa) |
| 4 | 46 | NOTA : débit d'eau admissible AFTES niveau 0 en dalle de couverture ; retombée d'étanchéité ≥ 20 cm sous la sous-face | Exigence de performance des couvertures + valeur de retombée | **GT9.C10F1 §9** (publication) |
| 5 | 50 | **Graphique** : grille anti-intrusion démontable (3 barreaux + collerette, calque dédié ACI 50) + étiquette « contrôle et entretien périodiques » | Reprise DESSIN P50 du mail ; entrées d'eau des exutoires à garder visibles/accessibles pour contrôle et maintenance | **GT9.C10F1 §9.3.1** (publication) |
| 6 | **00 (créé)** | Folio « Références et généralités » : référentiel applicable + contrôles d'exécution (gonflage 0,2 MPa/90 s, pointe sèche, cloche à vide 0,04 MPa, pelage 1/500 m², réception support = point d'arrêt, cohésion > 1,5 MPa, humidité < 4,5 %, béton > 21 j, niveaux AFTES 0-6) | Folio à créer n°1 du mail, valeurs C1 p.81 du mail + tableau 1 F67-III | mail Bertrand + **GT9.C1F1 p.81** + **F67-III §3.1/3.2** |
| 7 | **66 (créé)** | Arrêt d'étanchéité DEG sur voussoir : tôle colaminée fixée sur la tranche (variante bride/contre-bride) + NOTA variante SEL-A (anneau + extension 1 m paroi moulée + retour 50 cm intrados, alvéole V3 visitable) et distance joint hydrogonflant/extrados (enrobage + 2 cm, jamais < 3 cm) | Folio à créer n°2 du mail | **GT9.C9F1 §6.5** (prépublication), **F67-III §3.1.3.c**, **GT9.R1F2 III.2.2.1.6** |
| 8 | **67 (créé)** | Détails drainage : nappe drainante à excroissances + cunette + collecteur ; NOTA capacité drainante/anti-colmatage, bétonnage par faibles hauteurs, pente ≥ 5 mm/m | Folio à créer n°3 du mail | **GT9.R19F1** (via C5F1 §5, prépublication) + **GT9.C10F1 §10.2** |
| 9 | **68 (créé)** | Traversées de réseaux courants : fourreau scellé + joint hydrogonflant périphérique à mi-épaisseur + manchette ; NOTA scellement étanche et comblement des réservations | Folio à créer n°4 du mail | **GT9.C10F1 §8** (publication), **F67-III §3.1.7** |
| 10 | **69 (créé — RÉSERVE)** | Tableau de choix DEG/SEL-A/FPM : cadre + note d'attente explicite, structure prévue décrite, AUCUN contenu du Cahier 2 | Folio à créer n°5 du mail — dépend du statut du Cahier 2 (**point bloqué n°1**, décision B. Verrière) | (aucune citation C2) |
| 11 | **70 (créé)** | Réparation/réinjection d'un compartiment DEG : coupe radier + profilés + pipettes ; NOTA procédure complète (repérage, essai à l'eau colorée/traceur, résine acrylique 1-1,5 L/m², remplissage complet, délai 5-6 semaines après arrêt de pompage) | Folio à créer n°6 du mail | **GT9.R1F2 III.1.5.2.4** |

Réalisation graphique : calques sémantiques du carnet respectés
(`docs/normes/guide_couleur.md`), couleurs BYLAYER, NOTA en style txt-moyen
h=2,5 sur Dessin_TEXTES (convention des lots précédents).

## 2. Vérifications
- Bascule 6 cm : 0 résidu « lourde…5cm » (contrôle API ezdxf + grep brut du
  fichier, caches proxy des 14 MULTILEADER purgés, patch brut anti-REGEN).
- Re-parse complet après chaque lot (73 layouts, 0 erreur).
- PDF couleur 72/72 pages générées ; contrôle visuel pdftoppm sur 15 pages
  (garde, 00, 14, 16, 30-32, 44, 46, 50, 66-70) ; polices TrueType embarquées.
- Aucune référence périmée (R10F1/R15F1/TOS168) dans la source (lot N9).

## 3. Les 5 points BLOQUÉS — intacts, avec informations recueillies pour B. Verrière
| Point | État carnet (inchangé) | Information du corpus |
|---|---|---|
| 1. Statut Cahier 2 | non cité ; folio 69 en réserve | C2 sept. 2025 toujours prépublication ; C10F1 est passé en publication (oct. 2023) — précédent utile |
| 2. Écran sup DEG 19/10 vs 20/10 | 20/10 conservé | **C5F1 : « écran de protection PVC 1,90 mm mini » partout** (tableaux 1-3) — converge avec C1F1 (19/10) |
| 3. Engravures folio 38 (9/6/10/15 cm) | inchangé | C10F1 §7.1 : trait de scie **5 cm** usuel (enrobage 7,5 cm), engravure 5×1 cm, resurfaçage R4 jusqu'à +15 cm ; carnet folio 31 : 6 cm — divergence à arbitrer avec le CMO |
| 4. Raccord DEG/FPM folio 45 | « à définir » conservé | **C9F1 fig. 2-3 : deux solutions normalisées** (tôle colaminée + géotextile séparateur PVC/bitume, ou bande bi-matière) ; matrice : « pièce de transition, hors nappe » |
| 5. Seuil > 10 m folio 27 | inchangé | **C10F1/DTU 14.1 : seuil normatif = 8 m** pour structures relativement étanches (débits 0,5-1,0-2 l/m²/j) ; le « 10 m » du carnet ne correspond à aucune source du corpus |

## 4. Divergences relevées SANS modification (à arbitrer)
- Mortier de resurfaçage : carnet « R3 mini » (mail lot 2) vs C10F1 « R4 »
  au §7.1 — la règle C10F1 §6.1.3 est : **R3 ou R4 si H ≤ 8 m, R4 si
  H > 8 m** → dépend de la hauteur d'eau du projet.
- Terminologie : F67-III écrit « hydro-expansif », le carnet suit
  « hydrogonflant » (décision T4 du mail — conservée).
- SEL-A intrados : F67-III le réserve aux ouvrages < 300 m — à vérifier
  contre la longueur des gares du projet (question au MOE).

## 5. Manques documentaires (à fournir si possible)
- **GT9.C6F1** « dispositions constructives et points singuliers » — annoncé
  le 13/07 mais jamais reçu ; c'est le cahier le plus cité par les autres
  (raccords aux puits, traversées, fixations, butons).
- **GT9.R1F3** (TES 257) — remplace la R1F2 (2006) fournie.
- PDF de GT9.C1F1, GT9.R19F1, Cahier 2 (cités mais non fournis).

## 6. Imperfections résiduelles connues
- Folio 50 : léger chevauchement de l'étiquette de la grille avec les
  étiquettes existantes (lisible ; à ajuster d'un clic dans AutoCAD).
- Folio 35 : rendu PDF par fenêtre reconstituée (viewport source défaillant,
  anomalie préexistante).
- Folios 66-68/70 : schémas de principe volontairement sobres — à enrichir
  par le projeteur si besoin (les NOTA portent les exigences normatives).
- Masques de fond des étiquettes (bg_fill) désactivés dans le rendu PDF
  uniquement (sinon barres noires) — intacts dans le DXF pour AutoCAD.
