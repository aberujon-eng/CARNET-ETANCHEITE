# Intégration du corpus normatif — plan de travail autonome (trigger 4h)

Demande Alexandre (2026-07-13) : mettre à jour le carnet (DXF source + PDF
couleurs) en prenant en compte **toutes les normes transmises**, modifications
graphiques autorisées **en suivant le guide couleur du carnet DXF**, et rendre
un **résumé justifié modification par modification avec la norme citée**.
Travail continu jour et nuit via trigger 4h, sur plusieurs jours.

## Corpus (docs/normes/) — 9 documents

| # | Fichier | Référence | Date | Statut normatif |
|---|---------|-----------|------|-----------------|
| 1 | STRRES_FAEQ2_2009_entretien_reparation_etancheites.pdf | Guide STRRES FAEQ2 « Étanchéités » | déc. 2009 | guide métier entretien/réparation (93 p.) |
| 2 | GT9_C3F1_prepub_mise_hors_deau.pdf | AFTES GT9.C3F1 — Cahier 3 mise hors d'eau provisoire | mai 2024 | **PRÉPUBLICATION** (30 p.) |
| 3 | GT9_C5F1_prepub_protections_mecaniques.pdf | AFTES GT9.C5F1 — Cahier 5 protections mécaniques | mai 2024 | **PRÉPUBLICATION** (36 p.) |
| 4 | GT9_C9F1_prepub_mixte_raccordement_existants.pdf | AFTES GT9.C9F1 — Cahier 9 étanchéité mixte + raccordements aux existants | janv. 2024 | **PRÉPUBLICATION** (64 p.) |
| 5 | AFTES_GT9R1F2_TOS194-195_2006_arrets_deau.pdf | GT9.R1F2 — traitement d'arrêts d'eau | 2006 | en vigueur (46 p.) |
| 6 | AFTES_GT9R9F1_TOS151_1999_voussoirs_hydrogonflants.pdf | GT9.R9F1 — voussoirs, joints hydrogonflants | 1999 | en vigueur (18 p.) |
| 7 | AFTES_GT9R10F1_TOS159_2000_...pdf | GT9.R10F1 — étanchéité et drainage OS | 2000 | **REMPLACÉE par GT9.R19F1** (24 p., historique) |
| 8 | AFTES_TOS168_2001_...pdf | TOS 168 — étanchéité OS, informations/recommandations | 2001 | article 2 **REMPLACÉ par GT9.R19F1** |
| 9 | AFTES_GT9R15F1_TOS183_2004_ecrans_protection_DEG_...pdf | GT9.R15F1 — dimensionnement écrans de protection DEG | 2004 | **REMPLACÉE par GT9.R19F1** (14 p., historique) |
| 10 | F67_TitreIII_commente_CETU_2019.pdf | **Fascicule 67 Titre III version commentée** (CCTG étanchéité OS) | mars 2019 | référence de base du carnet (84 p.) — reçu 2026-07-13 |
| 11 | GT9_C10F1_publication_structures_integrees.pdf | AFTES GT9.C10F1 — Cahier 10 étanchement des structures intégrées | oct. 2023 | **PUBLICATION** (96 p.) — reçu 2026-07-13 |

Non fournis en PDF : GT9.C1F1 (valeurs p.81 connues via mail Bertrand),
Cahier 2 (statut = point bloqué n°1), GT9.R19F1.
⚠️ Alexandre annonçait « 4 nouveaux documents » dont « GT9C6F1 » le
2026-07-13 au soir : seuls 2 fichiers sont arrivés (F67-III commenté +
C10F1). **Le C6F1 n'a PAS été reçu** → à redemander au prochain jalon.

## Lots de travail (un ou plusieurs lots par réveil 4h)

| Lot | Contenu | Statut |
|-----|---------|--------|
| N0 | Rangement corpus, plan, trigger 4h | **FAIT** (2026-07-13) |
| N1 | Lecture **F67-III commenté** (base du carnet, priorité) → `docs/normes/extraits_F67III.md` | **FAIT** (2026-07-13/14 : chap. 1 terminologie + chap. 2 + chap. 3 intégraux ; ⚠️ R1F3 existe, notre R1F2 est antérieure — à demander à Alexandre) |
| N2 | Lecture GT9.R1F2 arrêts d'eau → `docs/normes/extraits_R1F2.md` (folios 27, 34, 40-43, 65 : injections, arrêts d'eau, hydrogonflants) | **FAIT** (2026-07-14 : niveaux 0-6, réparation compartimentage DEG III.1.5.2.4, bandes de pontage bride/contre-bride, injection joints) |
| N3 | Lecture GT9.R9F1 voussoirs hydrogonflants → extraits (folios 9/10, 22/23, 24 : jonctions tunnel foré, découpe voussoirs) | **FAIT** (2026-07-14 : critères Pf≥3Pe/min 1 bar, Frv≥0,4Fri≥200N, extractible ≤1 %, poses simple/double joint — `extraits_R9F1.md`) |
| N4 | Lecture C3F1 mise hors d'eau → extraits (mise hors d'eau provisoire, pompages — lien NOTA phasage folios 31/33/34) | **FAIT** (2026-07-14 : fig. 3 = base folios 34/36 ; humidité <4,5 % ; NOTA phasage confirmés ; le « cahier 6 » cité = C6F1 manquant, à redemander — `extraits_C3F1.md`) |
| N5 | Lecture C5F1 protections mécaniques → extraits (chapes/écrans : folios 15/33/34/36/40-43/46-48/51 « béton de protection », écran sup DEG) | À FAIRE |
| N6 | Lecture C9F1 mixte + raccordements existants → extraits (folios 45, 61-63 raccords DEG/FPM/SELA ; réparations) | À FAIRE |
| N7 | Lecture **C10F1 structures intégrées (publication)** → extraits (pertinence folios gares/structures : 12-25, 61-64) | À FAIRE |
| N8 | Lecture STRRES FAEQ2 ch. 3/4/5 (diagnostic, réparation, essais) → extraits (folio réparation DEG à créer ; NOTA contrôles) | À FAIRE |
| N9 | Balayage R10F1/R15F1/TOS168 (remplacées) : vérifier que le carnet ne cite aucune référence périmée ; sinon basculer vers R19F1/cahiers | **FAIT** (2026-07-14 : 0 référence périmée dans la source ; actives saines : 42×F67, 37×1504-3, 16×C1F1, 9×GT9, 2×R19F1) |
| N10 | Relevé du guide couleur du carnet (légendes DXF, calques) → `docs/normes/guide_couleur.md` | À FAIRE |
| N11 | Application reprises TEXTE (NOTA, renvois normatifs) issues de N1-N9 — hors 5 points bloqués | À FAIRE |
| N12 | Modifications GRAPHIQUES ciblées (couleurs selon guide_couleur.md) : P50 anti-intrusion + entretenabilité (DESSIN), compléments simples | À FAIRE |
| N13 | Création folio 00 « Références et contrôles » (hiérarchie normative complète + valeurs C1 p.81 du mail) | À FAIRE |
| N14 | Autres folios à créer (arrêt DEG voussoir, drainage R19F1, traversées, tableau de choix, réparation DEG) — selon faisabilité, graphiques sobres | À FAIRE |
| N15 | Régénération PDF couleur + contrôle visuel élargi (pdftoppm, ≥ 12 pages) | À FAIRE |
| N16 | Rapport final `docs/rapport_maj_normes.md` (modif par modif : quoi / folio / justification / norme) + MAJ Excel avancement | À FAIRE |
| N17 | Livraison à Alexandre + désactivation du trigger 4h et arrêt du /loop | À FAIRE |

## Règles permanentes
- **5 points BLOQUÉS intacts** (décision Bertrand Verrière) : statut Cahier 2 ·
  écran sup 19/10 vs 20/10 · engravures folio 38 · raccord DEG/FPM folio 45 ·
  seuil > 10 m folio 27. Les cahiers C3/C5/C9 fournis n'incluent PAS le
  Cahier 2 : le point 1 reste bloqué.
- Les prépublications (C3F1/C5F1/C9F1) sont citées avec la mention
  « (prépublication) » dans le carnet.
- R10F1/R15F1/TOS168-art.2 sont REMPLACÉES : ne jamais les citer comme
  référence active — historique seulement.
- Commit + push à chaque lot terminé (l'environnement est éphémère).
- PDF régénéré seulement après modifications de la source.
- Ne pas déranger Alexandre à chaque réveil : messages seulement aux jalons
  (fin de lecture corpus, fin des reprises, livraison finale) ou si blocage.
