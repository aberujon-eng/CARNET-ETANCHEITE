# État d'avancement — MAJ carnet détails étanchéité OS (source DXF)

Dernière mise à jour : 2026-07-05, session autonome.

## Fait — passe 1 sur la source DXF (v02)

Support DWG/DXF **validé** : l'export DXF (AC1032/R2018, 46 Mo, 66 onglets,
7181 entités model) se charge, s'édite et se sauvegarde avec `ezdxf` 1.4.4.
Le point « support CAD non confirmé » du CLAUDE.md est levé.

### Corrections appliquées (39 au total) — `scripts/apply_corrections_v02.py`
- Orthographe (portage des corrections déjà actées en passe PDF) :
  - `soutenement par centres HEB` → `soutènement par cintres HEB` (1)
  - `REVETEMENT`/`Revetement` → `REVÊTEMENT`/`Revêtement` (17)
  - `fixation mécanqiue` → `fixation mécanique` (1 multileader — coquille par
    inversion, repérée au rendu de contrôle du folio 29)
- Renvois périmés : `Détail n°18` → `Détail folio 65`
  (2 MTEXT NOTA + 5 MULTILEADER + 1 TEXT isolé)
- Sommaire page de garde : `raccords psur aroi moulée` → `raccords sur paroi
  moulée` (bloc d'affichage `*T232` **et** données de cellules ACAD_TABLE,
  patchées en brut pour survivre à un REGEN)
- Noms d'onglets (donc titres de cartouche via FIELD) :
  - 38 : `étancchéité` → `étanchéité`
  - 53–58 : `impermeabilisation` → `imperméabilisation`

### Vérifications
- Re-scan API ezdxf : 0 résidu sur tous les motifs corrigés
- Grep brut du fichier sauvé (attrape caches FIELD + cellules de table) : 0 résidu
- Re-parse complet : OK, 66 onglets intacts
- Audit calques des entités modifiées : uniquement `Dessin_TEXTES`,
  `Remarques - Prise en compte`, `GEN-_-CARTOUCHE` — contenu textuel modifié
  seulement, **aucune entité déplacée de calque, aucun calque de géométrie touché**
- Rendus de contrôle : `controle/*.png` (10 folios impactés + page de garde
  + zooms). Page de garde : les 2 tables (sommaire + versions 01/02) rendent
  correctement.

### Découvertes de structure (utiles pour la suite)
- Les dessins vivent dans le Model (patchwork), chaque onglet papier = 1
  viewport vers sa région + cartouche partagé `cart.L6P1` dont titre et
  n° de page sont des FIELDs sur le nom d'onglet → renommer l'onglet suffit.
- La table des versions contient déjà la ligne `02 | 06/05/2026 | Deuxième
  version | Alexandre BERUJON | Bertrand VERRIERE` — la source est plus
  fraîche que le PDF v01, rien à ajouter.
- Textes porteurs : MTEXT, TEXT, ATTRIB **et MULTILEADER** (391 — à ne jamais
  oublier dans les scans) + cellules ACAD_TABLE (non exposées par l'API,
  passer par patch brut des groupes 1/302/304).

### Limites connues du pipeline de contrôle
- Le rasteriseur (ezdxf drawing + matplotlib) ne dessine pas les entités TEXT
  en style `Arial` (police absente du conteneur) ni ne rasterise les viewports
  en rendu d'onglet papier. Les corrections sur ces entités sont vérifiées
  textuellement (triple contrôle ci-dessus). Utiliser `BackgroundPolicy.WHITE`
  systématiquement (ACI 7 = blanc sinon → invisible sur fond blanc).
- Les caches de FIELD (titre/page du cartouche) ne se réévaluent qu'à
  l'ouverture dans AutoCAD (REGEN) — comportement normal.

## À faire (dans l'ordre proposé)
1. **Galerie de contrôle des 66 folios** (PNG par folio, committée) — support
   de revue pour Bertrand + détection visuelle d'autres coquilles (méthode qui
   a déjà payé : `mécanqiue`).
2. Reprises folio par folio du mail à Bertrand — **le contenu du mail n'est
   pas dans le repo** : le coller dans `docs/` ou dans la conversation.
3. Portage des 17 encadrés « NOTA MAJ 2026 » (folios 6, 10, 29, 30–33, 35,
   40–44, 46, 47, 50, 64) — **textes exacts requis** (PDF retouché ou mail),
   ne pas réinventer les valeurs GT9.
4. Nouveaux folios (6) : 00 Références, arrêt DEG voussoir, drainage,
   traversées hors bride/contre-bride, tableau de choix, réparation DEG.
   Créables dans la source (onglet + région Model + viewport + cartouche).
5. Harmonisation décimales : la convention source est le **point** (197 occ.)
   — la correction PDF « 1,00m » impliquerait 41 cotes à basculer en virgule.
   **À trancher** (charte Egis) avant toute bascule massive.

## Points bloquants — intacts, décision Bertrand Verrière requise
(cf. CLAUDE.md — aucun n'a été touché dans cette passe)
1. Statut du Cahier 2 GT9 (prépublication) — citable ou non
2. Épaisseur écran supérieur DEG : 19/10e (C1F1) vs 20/10e (carnet v01)
3. Cotes engravures folio 38 (9/6/10/15 cm) vs CMO réel
4. Raccord DEG/FPM folio 45 « à définir » depuis 2022
5. Seuil « hauteur d'eau > 10 m » folio 27 — règle interne ou à sourcer

## Fichiers
- `source/carnet_v02.dxf` — source corrigée (état de cette passe)
- `source/carnet_v01_source_dxf.zip` — export DXF d'origine (intact, zippé)
- `scripts/apply_corrections_v02.py` — passe reproductible v01→v02
- `docs/rapport_corrections_v02.txt` — journal détaillé avant/après
- `docs/inventaire_textes_v01.txt` — inventaire des textes par folio (état v01)
- `controle/*.png` — rendus de contrôle post-modification

## Leçons pipeline (session lot 3)
- **ColorPolicy.BLACK obligatoire** pour les rendus de contrôle : le RenderContext
  résout ACI 7/ByLayer en blanc (convention fond noir model space) même avec
  BackgroundPolicy.WHITE — d'où des textes invisibles sur PNG fond blanc.
- Polices : les styles du carnet pointent segoeui.ttf (absente sous Linux) ;
  mapper une substitution dans ~/.fonts + `fonts.build_system_font_cache()`.
- MULTILEADER : (1) le texte vit dans le contexte ET en copie groupe 304 au
  niveau entité — patcher les deux ; (2) le cache proxy_graphic garde l'ancien
  rendu — purgé sur les 50 ML édités (AutoCAD régénérera).
- NOTA ajoutés (9) : MTEXT style txt-moyen, ch=2.5, calque Dessin_TEXTES,
  couleur ByLayer, placement en rectangle vide (bbox fast) ancré sur la fenêtre
  du folio.
- Anomalie préexistante relevée : viewports des onglets 31/37/39 pointant vers
  l'origine (0,0) — à vérifier dans AutoCAD (affichage onglet possiblement vide).
