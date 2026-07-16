#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot N14 — création des 5 folios manquants (mail Bertrand, folios à créer
n°2-6), schémas de principe selon le guide couleur (docs/normes/guide_couleur.md).

66 - Arrêt d'étanchéité DEG sur voussoir        (GT9.C9F1 §6.5, R1F2 III.2.2.1.6)
67 - Détails drainage                            (GT9.R19F1 via C5F1 §5)
68 - Traversées de réseaux courants              (GT9.C10F1 §8)
69 - Tableau de choix DEG/SEL-A/FPM              (RÉSERVE : dépend du statut
     du Cahier 2 = point BLOQUÉ n°1 -> cadre + note d'attente, AUCUN contenu C2)
70 - Réparation/réinjection compartiment DEG     (GT9.R1F2 III.1.5.2.4)

Zones Model libres : bande y=13300-13449, x=9000..10475 (5 x 275 + espaces).
Onglets ajoutés en fin de taborder (après folio 65).

Usage: python3 apply_normes_n14_folios.py FICHIER.dxf RAPPORT.txt
"""
import sys, ezdxf

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

W, H, Y0 = 275.0, 149.0, 13300.0
REGIONS = {66: 9000.0, 67: 9300.0, 68: 9600.0, 69: 9900.0, 70: 10200.0}

TXT = dict(style="txt-moyen", char_height=2.5, layer="Dessin_TEXTES", color=0)

def frame_and_title(x0, title):
    msp.add_lwpolyline([(x0, Y0), (x0+W, Y0), (x0+W, Y0+H), (x0, Y0+H)],
                       close=True, dxfattribs={"layer": "Dessin_Cadres"})
    msp.add_mtext(title, dxfattribs={**TXT, "char_height": 4.0, "width": W-10,
                  "attachment_point": 2, "insert": (x0+W/2, Y0+H-4, 0)})

def label(x, y, body, width=52):
    msp.add_mtext(body, dxfattribs={**TXT, "width": width,
                  "attachment_point": 1, "insert": (x, y, 0)})

def leader(x0y0, x1y1):
    msp.add_line(x0y0, x1y1, dxfattribs={"layer": "Dessin_TEXTES"})

def nota(x, y, body, width=120):
    t = '{\\fArial|b1|i1|c0|p34;\\LNOTA \\l: \\P' + body + '}'
    msp.add_mtext(t, dxfattribs={**TXT, "width": width,
                  "attachment_point": 7, "insert": (x, y, 0)})

# ---------------------------------------------------------------- folio 66
x = REGIONS[66]
frame_and_title(x, "ARRÊT D'ÉTANCHÉITÉ D.E.G. SUR VOUSSOIR")
vx, vy = x+60, Y0+55                       # coin du voussoir
msp.add_lwpolyline([(vx, vy), (vx+120, vy), (vx+120, vy+26), (vx, vy+26)],
                   close=True, dxfattribs={"layer": "Dessin_CONTOURS BETON"})
label(vx+46, vy+17, "VOUSSOIR", 40)
# DEG (rouge) arrivant a gauche, remonte sur la tole colaminee
msp.add_lwpolyline([(x+12, vy-6), (vx+18, vy-6), (vx+18, vy+8)],
                   dxfattribs={"layer": "SYSTEME_DEG_ Geomembrane SYNTHETIQUE"})
# tole colaminee fixee sur la tranche du voussoir
msp.add_line((vx+16, vy+2), (vx+16, vy+22),
             dxfattribs={"layer": "Matériel_Tôle colaminée"})
msp.add_line((vx+16, vy+22), (vx+30, vy+22),
             dxfattribs={"layer": "Matériel_Tôle colaminée"})
# fixations mecaniques (2 croix)
for fy in (vy+7, vy+17):
    msp.add_line((vx+14.6, fy-1.4), (vx+17.4, fy+1.4), dxfattribs={"layer": "Matériel_Fixation mécanique"})
    msp.add_line((vx+14.6, fy+1.4), (vx+17.4, fy-1.4), dxfattribs={"layer": "Matériel_Fixation mécanique"})
label(x+10, Y0+H-16, "Géomembrane D.E.G. soudée sur tôle colaminée", 60)
leader((x+38, Y0+H-18), (vx+10, vy-5))
label(vx+40, vy-14, "Tôle colaminée fixée mécaniquement sur la tranche du voussoir (variante : bride/contre-bride)", 74)
leader((vx+52, vy-6), (vx+17, vy+10))
nota(x+8, Y0+8,
     "Variante S.E.L.A. : anneau sur l'espace annulaire + extension 1 m sur "
     "la paroi moulée + retour 50 cm à l'intrados du voussoir, alvéole V3 "
     "non obturée (visitable) - cf. GT9.C9F1 §6.5 (prépublication). "
     "Distance joint hydrogonflant/extrados : enrobage + 2 cm, jamais < 3 cm "
     "(F67-III §3.1.3.c).", 128)
log.append("folio 66 dessiné")

# ---------------------------------------------------------------- folio 67
x = REGIONS[67]
frame_and_title(x, "DÉTAILS DRAINAGE (selon GT9.R19F1)")
px = x+70                                   # piedroit vertical
msp.add_lwpolyline([(px, Y0+30), (px+16, Y0+30), (px+16, Y0+H-24), (px, Y0+H-24)],
                   close=True, dxfattribs={"layer": "Dessin_CONTOURS BETON"})
label(px+2, Y0+H-30, "PIÉDROIT", 30)
# nappe drainante a excroissances (ligne verte crenelee simplifiee = polyline)
pts = []
yy = Y0+32
while yy < Y0+H-26:
    pts += [(px+18, yy), (px+20, yy+3), (px+18, yy+6)]
    yy += 6
msp.add_lwpolyline(pts, dxfattribs={"layer": "Matériel_Profilé d'arrêt d'eau paroi moulée"})
# cunette en pied + collecteur
msp.add_lwpolyline([(px+16, Y0+30), (px+34, Y0+30), (px+34, Y0+24), (px+44, Y0+24)],
                   dxfattribs={"layer": "Dessin_CONTOURS BETON"})
msp.add_circle((px+39, Y0+29), 4.0, dxfattribs={"layer": "Matériel_Drain-Tube PVC"})
label(x+10, Y0+H-16, "Nappe drainante à excroissances (pas de protection inférieure : contact direct avec l'eau)", 66)
leader((x+40, Y0+H-18), (px+19, Y0+90))
label(px+50, Y0+38, "Collecteur raccordé à la cunette (pente ≥ 5 mm/m, cf. GT9.C10F1 §10.2)", 60)
leader((px+52, Y0+36), (px+42, Y0+29))
nota(x+8, Y0+8,
     "Capacité drainante et anti-colmatage (filtre contre la laitance) selon "
     "GT9.R19F1 ; bétonnage par faibles hauteurs pour ne pas écraser l'âme "
     "drainante (GT9.C5F1 §5, prépublication).", 128)
log.append("folio 67 dessiné")

# ---------------------------------------------------------------- folio 68
x = REGIONS[68]
frame_and_title(x, "TRAVERSÉES DE RÉSEAUX COURANTS (hors bride/contre-bride)")
wx, wy = x+55, Y0+50                        # voile horizontal en coupe
msp.add_lwpolyline([(wx, wy), (wx+150, wy), (wx+150, wy+30), (wx, wy+30)],
                   close=True, dxfattribs={"layer": "Dessin_CONTOURS BETON"})
label(wx+58, wy+19, "VOILE / RADIER", 44)
# fourreau traversant (2 lignes + tube)
msp.add_line((wx+70, wy-14), (wx+70, wy+44), dxfattribs={"layer": "Matériel_Drain-Tube PVC"})
msp.add_line((wx+82, wy-14), (wx+82, wy+44), dxfattribs={"layer": "Matériel_Drain-Tube PVC"})
# joint hydrogonflant autour du fourreau (2 pastilles)
for jx in (wx+68, wx+84):
    msp.add_lwpolyline([(jx-1.6, wy+13), (jx+1.6, wy+13), (jx+1.6, wy+17), (jx-1.6, wy+17)],
                       close=True, dxfattribs={"layer": "Matériel_Joint Hydroexpansif"})
# manchette d'etancheite (resine) sur la face etanchee
msp.add_lwpolyline([(wx+58, wy-6), (wx+94, wy-6)],
                   dxfattribs={"layer": "Matériel_Resine"})
label(x+10, Y0+H-16, "Fourreau scellé au mortier sans retrait, joint hydrogonflant périphérique à mi-épaisseur", 64)
leader((x+42, Y0+H-18), (wx+69, wy+15))
label(wx+98, wy-12, "Manchette d'étanchéité compatible avec le procédé, en adhérence sur le support", 58)
leader((wx+100, wy-10), (wx+90, wy-6))
nota(x+8, Y0+8,
     "Trous de réservation comblés au mortier (F67-III §3.1.7) ; scellement "
     "étanche des traversées selon GT9.C10F1 §8 (publication) ; les "
     "traversées avec bride/contre-bride restent traitées au folio 37.", 128)
log.append("folio 68 dessiné")

# ---------------------------------------------------------------- folio 69
x = REGIONS[69]
frame_and_title(x, "TABLEAU DE CHOIX D.E.G. / S.E.L.-A / F.P.M.")
msp.add_mtext(
    "{\\fArial|b1|i1|c0;FOLIO EN ATTENTE}\\P\\P"
    "Le tableau de choix par partie d'ouvrage et hauteur d'eau s'appuie sur "
    "le Cahier 2 du GTguide (GT9.C2, §4.5 et §8).\\P\\P"
    "Le statut de ce cahier (prépublication sept. 2025) doit être confirmé "
    "avant toute citation contractuelle - décision B. VERRIÈRE en attente "
    "(point à trancher n°1 du mail de reprises v02).\\P\\P"
    "Structure prévue : lignes = parties d'ouvrage (radier / piédroits / "
    "dalle de couverture / raccords) ; colonnes = procédés admis selon la "
    "hauteur d'eau et la classe d'exigence.",
    dxfattribs={**TXT, "width": W-30, "attachment_point": 1,
                "insert": (x+15, Y0+H-20, 0)})
log.append("folio 69 posé (réserve, point bloqué n°1 non tranché)")

# ---------------------------------------------------------------- folio 70
x = REGIONS[70]
frame_and_title(x, "RÉPARATION / RÉINJECTION D'UN COMPARTIMENT D.E.G.")
rx, ry = x+40, Y0+58                        # radier en coupe
msp.add_lwpolyline([(rx, ry), (rx+190, ry), (rx+190, ry+22), (rx, ry+22)],
                   close=True, dxfattribs={"layer": "Dessin_CONTOURS BETON"})
label(rx+80, ry+14, "RADIER", 30)
# DEG sous radier + 2 profils de compartimentage
msp.add_line((rx, ry-4), (rx+190, ry-4), dxfattribs={"layer": "SYSTEME_DEG_ Geomembrane SYNTHETIQUE"})
for cxp in (rx+40, rx+150):
    msp.add_line((cxp, ry-4), (cxp, ry+2), dxfattribs={"layer": "Matériel_Profilé de compartimentage"})
# pipettes remontant dans le radier
for pxp in (rx+60, rx+95, rx+130):
    msp.add_line((pxp, ry-4), (pxp, ry+26), dxfattribs={"layer": "Matériel_Gaine d'injection"})
    msp.add_circle((pxp, ry+27.5), 1.5, dxfattribs={"layer": "Matériel_Gaine d'injection"})
label(x+10, Y0+H-16, "Compartiment D.E.G. délimité par les profilés, ≥ 3 pipettes remontées en boîtier (poteau/refend)", 70)
leader((x+45, Y0+H-18), (rx+95, ry+20))
nota(x+8, Y0+8,
     "Procédure (GT9.R1F2 III.1.5.2.4) : 1. repérage pipettes/compartiment ; "
     "2. essai préalable à l'eau colorée (traceur) : pipettes libres + "
     "compartimentage efficace + calage du temps de prise ; 3. injection en "
     "continu de résine acrylique (ratio indicatif 1 à 1,5 L/m²) jusqu'au "
     "REMPLISSAGE COMPLET ; 4. si rabattement de nappe en cours de travaux : "
     "délai d'observation 5 à 6 semaines après arrêt du pompage.", 128)
log.append("folio 70 dessiné")

# ------------------------------------------------------------- onglets
TITLES = {
    66: "66 - Détail spécifique - Arrêt d'étanchéité DEG sur voussoir",
    67: "67 - Détail spécifique - Détails drainage selon GT9.R19F1",
    68: "68 - Détail spécifique - Traversées de réseaux courants hors bride et contre-bride",
    69: "69 - Détail spécifique - Tableau de choix DEG SELA FPM (en attente statut Cahier 2)",
    70: "70 - Détail spécifique - Réparation et réinjection d'un compartiment DEG",
}
lay64 = None
for nm in doc.layout_names_in_taborder():
    if nm.strip().startswith("64"):
        lay64 = doc.layout(nm); break
for num, name in TITLES.items():
    if name in doc.layout_names_in_taborder():
        log.append(f"onglet {num} déjà présent — ignoré"); continue
    new = doc.layouts.new(name)
    for attr in ("paper_width", "paper_height", "plot_paper_units",
                 "left_margin", "bottom_margin", "right_margin", "top_margin",
                 "plot_rotation", "plot_type", "scale_numerator",
                 "scale_denominator", "paper_size_name"):
        try:
            new.dxf_layout.dxf.set(attr, lay64.dxf_layout.dxf.get(attr))
        except Exception:
            pass
    x0 = REGIONS[num]
    vp = new.add_viewport(center=(243.2, 30.3), size=(385, 209),
                          view_center_point=(x0+W/2, Y0+H/2), view_height=H)
    try:
        vp.dxf.status = 2; vp.dxf.layer = "Defpoints"
    except Exception:
        pass
    new.add_blockref("cart.L6P1", insert=(62.9, -124.8),
                     dxfattribs={"layer": "GEN-_-CARTOUCHE"})
    log.append(f"onglet créé : {name!r}")

doc.saveas(PATH)
doc2 = ezdxf.readfile(PATH)
present = [n for n in doc2.layout_names_in_taborder() if n[:2] in ("66","67","68","69","70")]
log.append(f"[VERIF] onglets 66-70 présents : {len(present)}/5 ; layouts={len(doc2.layouts)} ; re-parse OK")
open(RAP, "w").write("LOT N14 — folios 66-70\n\n" + "\n".join(log) + "\n")
print("\n".join(log))
