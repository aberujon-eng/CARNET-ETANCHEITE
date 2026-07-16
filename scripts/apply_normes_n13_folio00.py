#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot N13 — création du folio 00 « Références et généralités » (mail Bertrand,
folio à créer n°1 ; enrichi du corpus normatif lu — docs/suivi_normes.md).

- Contenu écrit dans une zone LIBRE du Model : (8700-8975, 13300-13449),
  au-dessus du patchwork existant (ymax=12999).
- Nouvel onglet « 00A - Références et généralités », taborder 2 (après la
  page de garde), viewport calqué sur celui du folio 64 (échelle texte
  identique aux autres folios), cartouche partagé cart.L6P1 (FIELDs sur le
  nom d'onglet -> titre correct au REGEN AutoCAD).
- Le Cahier 2 GT9 est mentionné avec « statut à confirmer » (formulation du
  mail de Bertrand) : le point BLOQUÉ n°1 n'est PAS tranché.

Usage: python3 apply_normes_n13_folio00.py FICHIER.dxf RAPPORT.txt
"""
import sys, ezdxf

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

X0, Y0 = 8700.0, 13300.0          # coin bas-gauche de la zone folio 00
W, H = 275.0, 149.0               # même format visible que folio 64

# --- cadre + titre ---------------------------------------------------------
msp.add_lwpolyline([(X0, Y0), (X0+W, Y0), (X0+W, Y0+H), (X0, Y0+H)],
                   close=True, dxfattribs={"layer": "Dessin_Cadres"})
msp.add_mtext("RÉFÉRENCES NORMATIVES ET CONTRÔLES",
              dxfattribs={"style": "txt-moyen", "char_height": 4.5,
                          "width": W-10, "layer": "Dessin_TEXTES", "color": 0,
                          "attachment_point": 2,  # TOP_CENTER
                          "insert": (X0+W/2, Y0+H-4, 0)})

COL_W = (W - 20) / 2

refs = (
    "{\\fArial|b1|i0|c0|p34;RÉFÉRENTIEL APPLICABLE}\\P"
    "- CCTG Fascicule 67 Titre III (arrêté du 28/05/2018) "
    "et version commentée CETU (mars 2019)\\P"
    "- NF DTU 14.1 (travaux de cuvelage)\\P"
    "- AFTES GT9.R19F1 - protections mécaniques et drainage\\P"
    "- AFTES GT9.R1 - traitements d'arrêts d'eau (fiche F3 en vigueur)\\P"
    "- AFTES GT9.R9F1 - joints hydrogonflants des voussoirs\\P"
    "- GTguide GT9.C10F1 (oct. 2023, publication) - structures intégrées\\P"
    "- GTguide GT9.C1F1 (nov. 2023), C3F1, C5F1, C9F1 - prépublications\\P"
    "- GT9.C2 (sept. 2025) : statut de prépublication à confirmer avant "
    "toute citation contractuelle\\P"
    "- NF EN 13491 (géomembranes), NF EN 13256 (géotextiles), "
    "NF EN 1504-3 (mortiers de réparation)\\P"
    "- Avis Techniques CETU des procédés (validité 5 ans)\\P"
    "- Certification ASQUAL des soudeurs"
)
ctrl = (
    "{\\fArial|b1|i0|c0|p34;CONTRÔLES D'EXÉCUTION (GT9.C1F1 p.81 / F67-III)}\\P"
    "- Réception du support = POINT D'ARRÊT "
    "(visite contradictoire + procès-verbal)\\P"
    "- Doubles soudures automatiques : contrôle par gonflage "
    "0,2 MPa maintenu 90 s\\P"
    "- Soudures manuelles : contrôle à la pointe sèche "
    "ou à la cloche à vide (0,04 MPa)\\P"
    "- Essais destructifs de pelage : 1 essai / 500 m²\\P"
    "- Support béton (procédés adhérents) : cohésion superficielle "
    "> 1,5 MPa ; humidité massique < 4,5 % ; âge > 21 jours\\P"
    "- Débits de fuite admissibles : fixés au CCTP "
    "(niveaux AFTES 0 à 6, GT9.R1)\\P\\P"
    "{\\fArial|b1|i1|c0;\\LNOTA \\l:} les prépublications du GTguide sont "
    "citées à titre d'information technique ; leur statut contractuel "
    "est à confirmer par la maîtrise d'oeuvre."
)
msp.add_mtext(refs, dxfattribs={"style": "txt-moyen", "char_height": 2.5,
              "width": COL_W, "layer": "Dessin_TEXTES", "color": 0,
              "attachment_point": 1, "insert": (X0+6, Y0+H-14, 0)})
msp.add_mtext(ctrl, dxfattribs={"style": "txt-moyen", "char_height": 2.5,
              "width": COL_W, "layer": "Dessin_TEXTES", "color": 0,
              "attachment_point": 1, "insert": (X0+14+COL_W, Y0+H-14, 0)})
log.append(f"contenu Model posé en ({X0},{Y0})-({X0+W},{Y0+H})")

# --- nouvel onglet ---------------------------------------------------------
NAME = "00A - Références et généralités"
if NAME in doc.layout_names_in_taborder():
    print("onglet déjà présent, abandon"); sys.exit(1)
lay64 = None
for nm in doc.layout_names_in_taborder():
    if nm.strip().startswith("64"):
        lay64 = doc.layout(nm); break
new = doc.layouts.new(NAME)
# copie de la config papier du folio 64
for attr in ("paper_width", "paper_height", "plot_paper_units",
             "left_margin", "bottom_margin", "right_margin", "top_margin",
             "plot_rotation", "plot_type", "scale_numerator",
             "scale_denominator", "paper_size_name", "plot_configuration_file"):
    try:
        new.dxf_layout.dxf.set(attr, lay64.dxf_layout.dxf.get(attr))
    except Exception:
        pass
# taborder : insérer après la page de garde
try:
    orders = sorted((l.dxf_layout.dxf.taborder, l.name) for l in
                    (doc.layout(n) for n in doc.layout_names_in_taborder())
                    if l.name != NAME)
    for l_n in doc.layout_names_in_taborder():
        if l_n in (NAME, "Model"): continue
        l = doc.layout(l_n)
        t = l.dxf_layout.dxf.taborder
        if t >= 2:
            l.dxf_layout.dxf.taborder = t + 1
    new.dxf_layout.dxf.taborder = 2
    log.append("taborder : folio 00A placé en position 2")
except Exception as ex:
    log.append(f"taborder non ajusté ({ex}) — onglet en fin de liste")

# viewport contenu (mêmes proportions papier que folio 64)
vp = new.add_viewport(center=(243.2, 30.3), size=(385, 209),
                      view_center_point=(X0+W/2, Y0+H/2), view_height=H)
try:
    vp.dxf.status = 2
    vp.dxf.layer = "Defpoints"
except Exception:
    pass
log.append(f"viewport -> view_center=({X0+W/2},{Y0+H/2}) view_height={H}")

# cartouche partagé
new.add_blockref("cart.L6P1", insert=(62.9, -124.8),
                 dxfattribs={"layer": "GEN-_-CARTOUCHE"})
log.append("cartouche cart.L6P1 inséré (FIELDs -> titre au REGEN)")

doc.saveas(PATH)

doc2 = ezdxf.readfile(PATH)
ok = NAME in doc2.layout_names_in_taborder()
n_vp = sum(1 for e in doc2.layout(NAME) if e.dxftype() == "VIEWPORT")
log.append(f"[VERIF] onglet présent={ok}, viewports={n_vp}, layouts={len(doc2.layouts)}")
open(RAP, "w").write("LOT N13 — folio 00\n\n" + "\n".join(log) + "\n")
print("\n".join(log))
