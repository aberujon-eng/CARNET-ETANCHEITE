#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot N11 — reprises texte issues du corpus normatif (docs/suivi_normes.md).

A. « Béton de protection lourde ép.5cm » -> 6 cm (34 occ., toutes variantes)
   Justification : GT9.C5F1 (prépublication) tableaux 1-3 : protection
   complémentaire = 6 cm de béton ; cohérent avec P34/36 (chape DEG 5->6,
   lot 1) et P47 (« 6 cm conforme ») du mail Bertrand.
B. NOTA folio 30 : pipettes en boîtier (GT9.C10F1 §7.1, publication).
C. NOTA folio 32 : surfaces maxi de compartimentage (F67-III art. 3.3.1).
D. NOTA folio 46 : dalle de couverture, débit AFTES 0 + retombée >= 20 cm
   (GT9.C10F1 §9).

Points BLOQUÉS (Bertrand Verrière) : AUCUN n'est touché — la bascule 6 cm
ne concerne pas l'écran 19/10-20/10 (autre élément), ni les engravures
folio 38, ni le folio 45, ni le seuil folio 27, ni le statut Cahier 2.

Usage: python3 apply_normes_n11.py FICHIER.dxf RAPPORT.txt
"""
import sys, re, ezdxf
from ezdxf import bbox as ezbbox

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

# ---------------------------------------------------------------- A. 5->6 cm
# "lourde" puis 5cm dans une fenetre de 20 caracteres (couvre : "lourde
# ép.5cm", "lourde: 5cm mini", "lourde (ép. 5cm mini.)", "lourde \Pbéton
# ép.5cm", "lourde ép.5cm"...). Garde-fou : pas de chiffre avant le 5
# (evite 15cm/25cm).
RX_LOURDE = re.compile(r"(lourde[\s\S]{0,20}?[^\d])5(\s?cm)", re.I)

def fix_lourde(raw):
    return RX_LOURDE.sub(r"\g<1>6\g<2>", raw)

edited = 0
ml_purged = 0
for e in msp:
    t = e.dxftype()
    if t == "MTEXT":
        raw = e.text
        new = fix_lourde(raw)
        if new != raw:
            e.text = new; edited += 1
            log.append(f"[A-6cm] #{e.dxf.handle} MTEXT\n    AVANT: {' '.join(raw.split())[:110]}\n    APRES: {' '.join(new.split())[:110]}")
    elif t == "TEXT":
        raw = e.dxf.text
        new = fix_lourde(raw)
        if new != raw:
            e.dxf.text = new; edited += 1
            log.append(f"[A-6cm] #{e.dxf.handle} TEXT\n    AVANT: {raw[:110]}\n    APRES: {new[:110]}")
    elif t == "MULTILEADER":
        try:
            mt = e.context.mtext
            raw = mt.default_content
        except Exception:
            continue
        if not raw:
            continue
        new = fix_lourde(raw)
        if new != raw:
            mt.default_content = new
            e.proxy_graphic = None       # purge du cache de rendu (NOTES.md)
            ml_purged += 1; edited += 1
            log.append(f"[A-6cm] #{e.dxf.handle} MULTILEADER (proxy purgé)\n    AVANT: {' '.join(raw.split())[:110]}\n    APRES: {' '.join(new.split())[:110]}")
log.append(f"[A-6cm] TOTAL {edited} entités modifiées ({ml_purged} MULTILEADER purgés)")

# ------------------------------------------------------------- B/C/D. NOTAs
def fmt(body):
    return '{\\fArial|b1|i1|c0|p34;\\LNOTA \\l: \\P' + body + '}'

NOTAS = {
    30: ("Pipettes d'injection : 3 minimum par compartiment, regroupées en "
         "boîtier dans un poteau ou voile de refend (pas en surface de radier) "
         "- cf. GT9.C10F1 §7.1.", 85,
         r'partie courante avec imperméabilisation'),
    32: ("Surface maximale de compartimentage : 250 m² sous pression "
         "hydrostatique, 350 m² hors pression (F67-III art. 3.3.1).", 80,
         r'partie courante sans imperméabilisation'),
    46: ("Étanchéité de la dalle de couverture : débit d'eau admissible AFTES "
         "niveau 0 ; retombée de l'étanchéité 20 cm minimum sous la sous-face "
         "de dalle (cf. GT9.C10F1 §9).", 85, None),
}

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

def entity_boxes(win):
    x0, x1, y0, y1 = win
    mx, my = (x1 - x0) * .3, (y1 - y0) * .3
    boxes = []
    for e in msp:
        p = None
        for attr in ('insert', 'start', 'center', 'defpoint'):
            try:
                p = getattr(e.dxf, attr); break
            except Exception:
                continue
        if p is None:
            try:
                p = e.context.base_point
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
            cands.append((yy, xx))
            xx += step
        yy += step
    for yy, xx in sorted(cands):
        if not clash(xx, yy):
            return xx, yy
    return None

for folio, (body, W, anchor) in NOTAS.items():
    win = far_viewport(folio)
    if win is None and anchor:
        win = anchor_window(anchor)
    if not win:
        log.append(f"[NOTA F{folio}] ECHEC : fenêtre introuvable — non posé")
        continue
    text = fmt(body)
    approx_lines = max(2, int(len(body) / (W / (2.5 * .72))) + 2)
    H = approx_lines * 2.5 * 1.66
    spot = free_rect(win, W, H)
    if not spot:
        W2 = W * .8
        spot = free_rect(win, W2, H * 1.2)
        if spot:
            W = W2
    if not spot:
        log.append(f"[NOTA F{folio}] ECHEC : pas de zone vide — non posé")
        continue
    x, y = spot
    mt = msp.add_mtext(text, dxfattribs={
        'style': 'txt-moyen', 'char_height': 2.5, 'width': W,
        'layer': 'Dessin_TEXTES', 'color': 0,
        'attachment_point': 7,
        'insert': (x, y, 0),
    })
    log.append(f"[NOTA F{folio}] posé #{mt.dxf.handle} @({x:.0f},{y:.0f}) W={W:.0f}")

doc.saveas(PATH)

# --------------------------------- patch brut (caches 304 des MULTILEADER)
with open(PATH, "r", encoding="utf-8", errors="surrogateescape") as f:
    raw = f.read()
new_raw, n_raw = RX_LOURDE.subn(r"\g<1>6\g<2>", raw)
if n_raw:
    with open(PATH, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(new_raw)
log.append(f"[A-6cm] patch brut post-sauvegarde : {n_raw} occurrence(s) résiduelle(s) corrigée(s) (caches 304)")

# ------------------------------------------------------------- vérification
doc2 = ezdxf.readfile(PATH)
res = 0
for e in doc2.modelspace():
    t = e.dxftype()
    raw2 = None
    if t == "MTEXT": raw2 = e.text
    elif t == "TEXT": raw2 = e.dxf.text
    elif t == "MULTILEADER":
        try: raw2 = e.context.mtext.default_content
        except Exception: pass
    if raw2 and RX_LOURDE.search(raw2):
        res += 1
        log.append(f"[VERIF] RESIDU 5cm : #{e.dxf.handle} {raw2[:80]!r}")
with open(PATH, encoding="utf-8", errors="surrogateescape") as f:
    res_raw = len(RX_LOURDE.findall(f.read()))
log.append(f"[VERIF] résidus API={res}, résidus bruts={res_raw} (attendu 0/0) ; re-parse OK ({len(doc2.layouts)} layouts)")

open(RAP, "w").write(f"LOT N11 — {len(log)} entrées\n\n" + "\n".join(log) + "\n")
print(f"N11 applique -> {PATH}")
for l in log:
    if 'ECHEC' in l or 'RESIDU' in l or 'TOTAL' in l or 'VERIF' in l or 'NOTA' in l:
        print(" ", l.splitlines()[0])
