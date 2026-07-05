#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot 2 des reprises (docs/mail_bertrand_reprises_v02.txt) :
P8 renvoi folios 30-33 ; P25 renvoi folios 40-43 ; P41 résine époxy +
préparation (4 occ. même objet) ; P45 anti-racine si végétalisation ;
P65 débord 70 mm ; P27 coquille "conformtement" + tôle galvanisée/inox
(seuil > 10 m NON touché — point bloqué) ; P51-60 resurfaçage -> NF EN
1504-3 ; P2 retour technique à adapter selon hauteur d'eau / NDC ;
coquille "dupuis" -> "depuis" (3 occ.).

Usage: python3 apply_lot2.py FICHIER.dxf RAPPORT.txt
"""
import sys, re, ezdxf

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
log = []

def edit(h, fn, what):
    e = doc.entitydb[h]
    t = e.dxftype()
    if t == "MTEXT":
        raw = e.text; new = fn(raw)
        if new != raw: e.text = new
    elif t == "MULTILEADER":
        mt = e.context.mtext
        raw = mt.default_content; new = fn(raw)
        if new != raw: mt.default_content = new
    elif t == "TEXT":
        raw = e.dxf.text; new = fn(raw)
        if new != raw: e.dxf.text = new
    else:
        raise TypeError(t)
    if new != raw:
        log.append(f"[{what}] #{h} calque={e.dxf.layer!r}\n    AVANT: {' '.join(raw.split())[:115]}\n    APRES: {' '.join(new.split())[:115]}")
    else:
        log.append(f"[{what}] #{h} : AUCUN CHANGEMENT (motif non trouvé ?)")

# P8 — renvoi explicite
edit('12A34', lambda s: s.replace('(Voir détail de la décomposition)',
     '(voir détails folios 30 à 33)'), 'P8')
# P25 — renvoi explicite
edit('6651', lambda s: s.replace('à prévoir en radier',
     'à prévoir en radier (cf. folios 40 à 43)'), 'P25')
# P41 (+ occurrences identiques F43/F65, même objet)
for h in ('D889', 'D8B5', '12D5D', '12D8C'):
    edit(h, lambda s: s.replace('collée à la résine',
         'collée à la résine époxy\\P(préparation du support selon GT9.C1F1)'), 'P41')
# P45 — bicouche anti-racine : uniquement si végétalisation
edit('1746C', lambda s: s + '\\P(uniquement si végétalisation)', 'P45')
# P65 — clarification débord
for h in ('12D5B', '12D8A'):
    edit(h, lambda s: s.replace('Centré\\P70mm mini',
         'Débord 70mm mini\\Pde part et d\'autre du joint'), 'P65')
# P27 — coquille + matériau tôle (seuil > 10m inchangé)
edit('FEBB', lambda s: s.replace('conformtement \\Ppar tôle si',
     'confortement \\Ppar tôle (galvanisée ou inox) si'), 'P27')
# P51 — resurfaçage PM
edit('130D3', lambda s: s.replace('Resurfaçage de la paroi moulée',
     'Resurfaçage de la paroi moulée au mortier classe R3 mini\\Pselon NF EN 1504-3 (tolérances selon GT9.C1F1)'), 'P51')
# P52-54 — resurfaçage soigné
for h in ('132C4', '132B2', '13267'):
    edit(h, lambda s: s.replace('Resurfaçage soigné',
         'Resurfaçage soigné au mortier\\Pclasse R3 mini selon NF EN 1504-3'), 'P52-54')
# P55/57/59 — type R3 -> + norme
for h in ('135DC', '1367D'):
    edit(h, lambda s: s.replace('type R3', 'type R3 selon NF EN 1504-3'), 'P55/57')
edit('13920', lambda s: s.replace('Resurfaçage soigné',
     'Resurfaçage soigné type R3\\Pselon NF EN 1504-3'), 'P59')
# P56/58/60 — resurfaçage soigné seul
for h in ('13601', '136A1', '13941'):
    edit(h, lambda s: s.replace('Resurfaçage soigné',
         'Resurfaçage soigné au mortier\\Pclasse R3 mini selon NF EN 1504-3'), 'P56-60')
# P2 — retour technique à adapter
edit('1FE5F', lambda s: s.rstrip() +
     "\\PLa longueur du retour technique (1,00 m) est à adapter selon la hauteur d'eau (note de calcul).", 'P2')
# coquille "dupuis"
for h in ('6744', 'C9D1', 'CA4C'):
    edit(h, lambda s: s.replace('dupuis', 'depuis'), 'ortho-dupuis')

doc.saveas(PATH)
open(RAP, "w").write(f"LOT 2 — {len(log)} entrées\n\n" + "\n".join(log) + "\n")
print(f"{len(log)} entrées -> {PATH}")
for l in log:
    if 'AUCUN' in l: print("!!", l)
