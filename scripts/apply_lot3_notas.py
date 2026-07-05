#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot 3 — ajout des NOTA du mail (P9, P29, P31, P33, P34, P37, P39, P44, P49).

Style calibré sur les NOTA existants (#6651/#13653) : calque Dessin_TEXTES,
style txt-moyen, char_height 2.5, Arial gras-italique, « NOTA » souligné.
Placement : recherche de rectangle vide (bbox réelles ezdxf.bbox, fast=True)
dans la fenêtre du folio, préférence pour le bas de la vue.

Usage: python3 apply_lot3_notas.py FICHIER.dxf RAPPORT.txt
"""
import sys, re, ezdxf
from ezdxf import bbox as ezbbox

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

def fmt(body):
    return '{\\fArial|b1|i1|c0|p34;\\LNOTA \\l: \\P' + body + '}'

NOTAS = {
    9:  ("Préparation du support voussoir avant application du S.E.L.A. : surfaçage des épaufrures et traitement des joints de voussoirs (cf. GT9.C1F1 §6.4).", 80),
    29: ("Système bride / contre-bride : entraxe des fixations et couple de serrage selon note de calcul ; nature des joints compressibles selon avis technique du procédé ; résine de protection à préciser.", 85),
    31: ("L'enduit d'imperméabilisation sera continué jusqu'au trait de scie (continuité avec l'étanchéité). Phasage de mise en œuvre à préciser.", 80),
    33: ("L'enduit d'imperméabilisation sera continué jusqu'au trait de scie (continuité avec l'étanchéité). Phasage de mise en œuvre à préciser.", 80),
    34: ("Phasage : 1. recépage de la tête de pieu ; 2. coffrage ; 3. bétonnage (béton hydrofuge) ; 4. pose des profilés ; 5. injection.", 80),
    37: ("Système bride / contre-bride : entraxe des fixations et couple de serrage selon note de calcul ; nature des joints compressibles selon avis technique du procédé ; résine de protection à préciser.", 85),
    39: ("Soudure manuelle sur tôle colaminée : contrôle à la pointe sèche ou à la cloche à vide (cf. GT9.C1F1 p.81).", 80),
    44: ("Préparation de la paroi berlinoise : désaffleurements ≤ 5 cm ; chanfrein à 45° sur les arêtes ; remplissage des ondes par produit résistant à 90 kPa.", 85),
    49: ("Au droit du joint de dilatation : prévoir un soufflet de la feuille F.P.M. et une non-adhérence locale de la feuille (largeur non collée de part et d'autre du joint).", 85),
}

# fenêtres : viewport far-field si sain, sinon ancre textuelle
def far_viewport(folio):
    for nm in doc.layout_names_in_taborder():
        m = re.match(r'\s*(\d+)\s*-', nm)
        if not m or int(m.group(1)) != folio:
            continue
        best = None
        for v in doc.layout(nm):
            if v.dxftype() != "VIEWPORT":
                continue
            vx, vy = v.dxf.view_center_point.x, v.dxf.view_center_point.y
            if vx * vx + vy * vy < 1e6:
                continue
            vh = v.dxf.view_height
            vw = vh * (v.dxf.width / v.dxf.height)
            best = (vx - vw * .5, vx + vw * .5, vy - vh * .5, vy + vh * .5)
        return best
    return None

def anchor_window(pattern, half_w=140, half_h=80):
    rx = re.compile(pattern)
    for e in msp:
        t = e.dxftype()
        raw = e.text if t == "MTEXT" else (e.dxf.text if t == "TEXT" else None)
        if raw and rx.search(raw):
            p = e.dxf.insert
            return (p.x - half_w, p.x + half_w, p.y - half_h, p.y + half_h)
    return None

WINDOWS = {}
for f in NOTAS:
    WINDOWS[f] = far_viewport(f)
WINDOWS[31] = WINDOWS[31] or anchor_window(r'ancré dans parois moulées avec imperméabilisati')
WINDOWS[37] = WINDOWS[37] or anchor_window(r'[Tt]raversée.{0,40}bride|bride et contre-bride')
WINDOWS[39] = WINDOWS[39] or anchor_window(r'Soudure manuelle sur tôle colaminée')

# occupation : bbox réelles des entités dont un point tombe près de la fenêtre
def entity_boxes(win):
    x0, x1, y0, y1 = win
    mx, my = (x1 - x0) * .3, (y1 - y0) * .3
    boxes = []
    for e in msp:
        p = None
        for attr in ('insert', 'start', 'center', 'defpoint'):
            try:
                p = getattr(e.dxf, attr)
                break
            except Exception:
                continue
        if p is None:
            try:
                p = e.context.base_point  # multileader
            except Exception:
                continue
        if not (x0 - mx <= p.x <= x1 + mx and y0 - my <= p.y <= y1 + my):
            continue
        try:
            ext = ezbbox.extents([e], fast=True)
            if ext.has_data:
                boxes.append((ext.extmin.x, ext.extmax.x, ext.extmin.y, ext.extmax.y))
        except Exception:
            boxes.append((p.x - 3, p.x + 3, p.y - 3, p.y + 3))
    return boxes

def free_rect(win, W, H, margin=4):
    x0, x1, y0, y1 = win
    boxes = entity_boxes(win)
    def clash(rx0, ry0):
        rx1, ry1 = rx0 + W, ry0 + H
        for bx0, bx1, by0, by1 in boxes:
            if rx0 - margin < bx1 and rx1 + margin > bx0 and ry0 - margin < by1 and ry1 + margin > by0:
                return True
        return False
    cands = []
    step = 8
    yy = y0 + 2
    while yy + H <= y1 - 2:
        xx = x0 + 2
        while xx + W <= x1 - 2:
            cands.append((yy, xx))          # tri : bas de vue d'abord
            xx += step
        yy += step
    for yy, xx in sorted(cands):
        if not clash(xx, yy):
            return xx, yy, len(boxes)
    return None

created = []
for folio, (body, W) in NOTAS.items():
    win = WINDOWS.get(folio)
    if not win:
        log.append(f"[F{folio}] ECHEC : fenêtre introuvable — NOTA non posé")
        continue
    text = fmt(body)
    approx_lines = max(2, int(len(body) / (W / (2.5 * .72))) + 2)
    H = approx_lines * 2.5 * 1.66
    spot = free_rect(win, W, H)
    if not spot:
        spot = free_rect(win, W * .8, H * 1.2)
        W = W * .8
    if not spot:
        log.append(f"[F{folio}] ECHEC : pas de zone vide {W:.0f}x{H:.0f} — NOTA non posé")
        continue
    x, y, nb = spot
    mt = msp.add_mtext(text, dxfattribs={
        'style': 'txt-moyen', 'char_height': 2.5, 'width': W,
        'layer': 'Dessin_TEXTES', 'color': 0,
        'attachment_point': 7,  # BOTTOM_LEFT : insert = coin bas-gauche
        'insert': (x, y, 0),
    })
    created.append((folio, mt.dxf.handle, x, y))
    log.append(f"[F{folio}] NOTA posé #{mt.dxf.handle} @({x:.0f},{y:.0f}) W={W:.0f} H~{H:.0f} (fenêtre {win[0]:.0f}..{win[1]:.0f} / {win[2]:.0f}..{win[3]:.0f}, {nb} boxes)")

doc.saveas(PATH)
open(RAP, "w").write("LOT 3 — NOTA ajoutés\n\n" + "\n".join(log) + "\n")
for l in log:
    print(l)
