#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot N12 — P50 (mail Bertrand, statut DESSIN) : dispositif anti-intrusion et
entretenabilité sur le détail d'évacuation du folio 50.

Justification normative : GT9.C10F1 §9.3.1 (publication) — les entrées d'eau
des exutoires doivent rester visibles/accessibles pour contrôle et
maintenance ; protection de l'évacuation (fig. 62).

Réalisation (guide couleur docs/normes/guide_couleur.md) :
- nouveau calque « Matériel_Grille anti-intrusion » ACI 50 (convention
  aciers galvanisés), couleurs BYLAYER ;
- grille = 3 barreaux (cordes verticales) sur le cercle de la canalisation
  #169CC + collerette horizontale au-dessus ;
- étiquette MTEXT sur Dessin_TEXTES + amorce de renvoi (LINE).

Usage: python3 apply_normes_n12.py FICHIER.dxf RAPPORT.txt
"""
import sys, math, ezdxf

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

LAYER = "Matériel_Grille anti-intrusion"
if LAYER not in doc.layers:
    doc.layers.add(LAYER, color=50)
    log.append(f"calque créé : {LAYER!r} (ACI 50)")

cx, cy, r = 23527.20, 11594.20, 5.40

# 3 barreaux verticaux (cordes du cercle) espacés de r/2
for dx in (-r/2, 0.0, r/2):
    half = math.sqrt(max(r*r - dx*dx, 0.0)) * 0.92
    msp.add_line((cx+dx, cy-half), (cx+dx, cy+half), dxfattribs={"layer": LAYER})
# collerette : petit trait horizontal au sommet (appui de la grille)
msp.add_line((cx-r*0.75, cy+r*1.05), (cx+r*0.75, cy+r*1.05), dxfattribs={"layer": LAYER})
log.append(f"grille posée sur #169CC : 3 barreaux + collerette @({cx},{cy}) r={r}")

# étiquette + amorce de renvoi
tx, ty = cx + 14, cy + 26
mt = msp.add_mtext(
    "Grille anti-intrusion démontable\\P(contrôle et entretien périodiques\\P- cf. GT9.C10F1 §9.3.1)",
    dxfattribs={"style": "txt-moyen", "char_height": 2.5, "width": 46,
                "layer": "Dessin_TEXTES", "color": 0,
                "attachment_point": 7, "insert": (tx, ty, 0)})
msp.add_line((tx - 1.5, ty + 1.0), (cx + r*0.5, cy + r*0.9),
             dxfattribs={"layer": "Dessin_TEXTES"})
log.append(f"étiquette #{mt.dxf.handle} @({tx},{ty}) + amorce")

doc.saveas(PATH)

# vérification : re-parse + présence des nouveaux objets
doc2 = ezdxf.readfile(PATH)
n = sum(1 for e in doc2.modelspace() if e.dxf.layer == LAYER)
log.append(f"[VERIF] {n} entités sur {LAYER!r} (attendu 4) ; re-parse OK ({len(doc2.layouts)} layouts)")

open(RAP, "w").write("LOT N12 — P50 anti-intrusion\n\n" + "\n".join(log) + "\n")
print("\n".join(log))
