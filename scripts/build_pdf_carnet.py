#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere un PDF multi-pages du carnet v02 (un folio par page), a partir de la
source DXF. Corrige le bug de rendu identifie : sans ColorPolicy.BLACK, les
entites de couleur ACI 7 / ByLayer (traits, hachures) sont resolues en blanc
et invisibles sur fond blanc -> seul le texte appara^it.

Methode de recadrage par folio : fenetre du viewport papier "far-field" quand
disponible (evite les onglets dont le viewport pointe vers l'origine), sinon
fenetre par ancre textuelle (fallback deja valide pour les folios 04/08/32).

Usage: python3 build_pdf_carnet.py DXF_IN PDF_OUT
"""
import sys, re
import ezdxf
import ezdxf.bbox
import matplotlib
matplotlib.use("Agg")
# Type 3 (defaut matplotlib) n'est pas fiable dans beaucoup de lecteurs PDF
# legers (mobile, apercu navigateur) -> pages qui semblent vides. TrueType
# (42) est le format le plus largement supporte.
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy

DXF_IN, PDF_OUT = sys.argv[1], sys.argv[2]

doc = ezdxf.readfile(DXF_IN)
msp = doc.modelspace()
CFG = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
ctx = RenderContext(doc)

# au-dela de cette taille, une entite ne peut pas etre le contenu legitime
# d'un seul folio (le plus grand folio reel fait ~2500 unites de large) ->
# ce sont des blocs orphelins hors champ (ex. reperes/rosaces a x~300000,
# deja identifies en debut de session) dont la bbox massive "empoisonnerait"
# tout test de recoupement fenetre/entite si on les gardait.
MAX_ENTITY_SPAN = 5000

# Le carnet contient plusieurs categories de TEXT/entites de service AutoCAD
# NON destinees a l'impression, mais qui contaminent le rendu si elles sont
# rasterisees :
#
#  (a) reperes "n°1".."n°65" (calque Dessin_TEXTES, h=10) : navigation manuelle
#      dans le model. S'affichent comme d'enormes chiffres parasites et
#      gonflent anchor_window (cluster 30-33/37/39 -> contamination croisee).
#
#  (b) titres macro de navigation (calque Dessin_TEXTES, h=60/100/300) : "FPM",
#      "DEG", "Partie courante en radier (structure en PM)", "Detail 1/2/3",
#      "Jonction Tunnel ..." — decoupent la matrice du model en zones, pas
#      destines a l'imprime. Le "PM)" geant vu sur folio 30/31 vient d'ici.
#
#  (c) calque 'Remarques - Prise en compte' (252 entites) : commentaires de
#      travail internes (annotations Bertrand/Alexandre), a ne jamais imprimer.
#
# Le texte d'annotation legitime du carnet plafonne a h=5.0 (77 TEXT). Tout
# TEXT h>15 est necessairement un titre de navigation ou un artefact de la
# matrice de travail hors champ.
NOTES_LAYER = "Remarques - Prise en compte"
MAX_LEGITIMATE_TEXT_HEIGHT = 15.0
LOCATOR_RX = re.compile(r"^\s*n°\s*\d+\s*$")

# calques dont la propriete AutoCAD 'Plot' est desactivee (traits de
# construction, Defpoints, calques _NON_IMPRIMABLE_) : par convention
# jamais rasterises. Ces LINE peuvent etre geantes (une ligne verticale
# de 3773 u sur Defpoints etendrait la fenetre d'un folio a x8 sa taille).
NON_PLOTTABLE_LAYERS = {l.dxf.name for l in doc.layers if not l.dxf.plot}
print(f"  {len(NON_PLOTTABLE_LAYERS)} calques non-imprimables (plot=0) : "
      f"{sorted(NON_PLOTTABLE_LAYERS)[:8]}{'...' if len(NON_PLOTTABLE_LAYERS) > 8 else ''}",
      file=sys.stderr)

def is_locator_label(e):
    if e.dxftype() != "TEXT":
        return False
    try:
        if e.dxf.layer != "Dessin_TEXTES":
            return False
        if abs(e.dxf.height - 10.0) > 0.01:
            return False
        return bool(LOCATOR_RX.match(e.dxf.text))
    except Exception:
        return False

def is_oversized_text(e):
    if e.dxftype() != "TEXT":
        return False
    try:
        return e.dxf.height > MAX_LEGITIMATE_TEXT_HEIGHT
    except Exception:
        return False

def is_internal_note(e):
    try:
        return e.dxf.layer == NOTES_LAYER
    except Exception:
        return False

def is_non_plottable(e):
    try:
        return e.dxf.layer in NON_PLOTTABLE_LAYERS
    except Exception:
        return False

print("Calcul des boites englobantes de toutes les entites du Model...", file=sys.stderr)
_BBOX_CACHE = []
skipped_huge = 0
skipped_locator = 0
skipped_titles = 0
skipped_notes = 0
skipped_nonplot = 0
for e in msp:
    if is_non_plottable(e):
        skipped_nonplot += 1
        continue
    if is_internal_note(e):
        skipped_notes += 1
        continue
    if is_locator_label(e):
        skipped_locator += 1
        continue
    if is_oversized_text(e):
        skipped_titles += 1
        continue
    try:
        ext = ezdxf.bbox.extents([e], fast=True)
    except Exception:
        continue
    if not ext.has_data:
        continue
    w, h = ext.extmax.x - ext.extmin.x, ext.extmax.y - ext.extmin.y
    if w > MAX_ENTITY_SPAN or h > MAX_ENTITY_SPAN:
        skipped_huge += 1
        continue
    _BBOX_CACHE.append((e, ext.extmin.x, ext.extmax.x, ext.extmin.y, ext.extmax.y))
print(f"  {len(_BBOX_CACHE)}/{len(msp)} entites avec bbox valide "
      f"(exclusions : {skipped_nonplot} calques plot=0, "
      f"{skipped_huge} bbox > {MAX_ENTITY_SPAN}u, "
      f"{skipped_locator} reperes 'n°NN', "
      f"{skipped_titles} TEXT h>{MAX_LEGITIMATE_TEXT_HEIGHT} (titres macro), "
      f"{skipped_notes} calque '{NOTES_LAYER}')",
      file=sys.stderr)

def ents_in(x0, x1, y0, y1, margin=150):
    """Renvoie les entites dont la boite englobante recoupe la fenetre
    (elargie de margin), quel que soit leur type (LWPOLYLINE, HATCH,
    SPLINE, INSERT... inclus, contrairement a un simple test de point
    d'ancrage)."""
    wx0, wx1, wy0, wy1 = x0 - margin, x1 + margin, y0 - margin, y1 + margin
    out = []
    for e, ex0, ex1, ey0, ey1 in _BBOX_CACHE:
        if ex1 < wx0 or ex0 > wx1 or ey1 < wy0 or ey0 > wy1:
            continue
        out.append(e)
    return out

def far_viewport_window(layout_name):
    best = None
    for v in doc.layout(layout_name):
        if v.dxftype() != "VIEWPORT":
            continue
        vx, vy = v.dxf.view_center_point.x, v.dxf.view_center_point.y
        if vx * vx + vy * vy < 1e6:
            continue
        vh = v.dxf.view_height
        vw = vh * (v.dxf.width / v.dxf.height)
        best = (vx - vw * .55, vx + vw * .55, vy - vh * .55, vy + vh * .55)
    return best

def anchor_window(pattern, probe_radius=180, min_half=90):
    """Localise un point d'ancrage par texte, puis calcule la vraie boite
    englobante des entites presentes dans un large rayon autour (plutot
    qu'une fenetre fixe qui peut couper une partie du dessin)."""
    rx = re.compile(pattern)
    anchor = None
    for e in msp:
        t = e.dxftype()
        if t == "MTEXT":
            raw, p = e.text, e.dxf.insert
        elif t == "TEXT":
            raw, p = e.dxf.text, e.dxf.insert
        elif t == "MULTILEADER":
            try:
                raw = e.context.mtext.default_content
                p = e.context.base_point
            except Exception:
                continue
        else:
            continue
        if raw and rx.search(raw):
            anchor = p
            break
    if anchor is None:
        return None
    ax, ay = anchor.x, anchor.y
    nearby = ents_in(ax - probe_radius, ax + probe_radius, ay - probe_radius, ay + probe_radius, margin=0)
    xs0, xs1, ys0, ys1 = [], [], [], []
    for e in nearby:
        try:
            ext = ezdxf.bbox.extents([e], fast=True)
            if ext.has_data:
                xs0.append(ext.extmin.x); xs1.append(ext.extmax.x)
                ys0.append(ext.extmin.y); ys1.append(ext.extmax.y)
        except Exception:
            pass
    if not xs0:
        return (ax - min_half, ax + min_half, ay - min_half, ay + min_half)
    x0, x1, y0, y1 = min(xs0), max(xs1), min(ys0), max(ys1)
    mx, my = max((x1 - x0) * .08, 5), max((y1 - y0) * .08, 5)
    return (x0 - mx, x1 + mx, y0 - my, y1 + my)

# --- Fenetrage par repere "n°NN" + Voronoi ---
# Meme si excluses du rendu, les etiquettes "n°1".."n°65" (calque
# Dessin_TEXTES, h=10) restent le seul point d'ancrage garanti unique par
# folio dans le model. On les retrouve ici pour calculer, pour chaque folio,
# une fenetre dont les bordures sont limitees par le mid-point vers chaque
# repere voisin proche (Voronoi tronquee) : ca evite mecaniquement la
# contamination des folios voisins pour les clusters 30-33 / 37-39.
def _collect_locator_positions():
    pat = re.compile(r"^\s*n°\s*(\d+)\s*$")
    out = {}
    for e in msp:
        if e.dxftype() != "TEXT":
            continue
        try:
            if e.dxf.layer != "Dessin_TEXTES":
                continue
            if abs(e.dxf.height - 10.0) > 0.01:
                continue
            m = pat.match(e.dxf.text)
            if not m:
                continue
            out[int(m.group(1))] = (e.dxf.insert.x, e.dxf.insert.y)
        except Exception:
            pass
    return out

_LOCATORS = _collect_locator_positions()
print(f"  {len(_LOCATORS)} reperes 'n°NN' localises dans le model", file=sys.stderr)

def locator_window(folio_num, default_half=400, neighbor_radius=900):
    """Fenetre du folio, ancree sur son repere 'n°NN' :
    - point de depart : carre 2*default_half x 2*default_half autour du repere
    - pour chaque repere voisin dans un rayon `neighbor_radius`, la bordure
      la plus proche est rabattue au mid-point selon l'axe dominant du
      vecteur voisin (evite d'englober des quadrants adjacents)."""
    p = _LOCATORS.get(folio_num)
    if p is None:
        return None
    ax, ay = p
    x0, x1 = ax - default_half, ax + default_half
    y0, y1 = ay - default_half, ay + default_half
    for other, q in _LOCATORS.items():
        if other == folio_num:
            continue
        dx, dy = q[0] - ax, q[1] - ay
        d2 = dx * dx + dy * dy
        if d2 > neighbor_radius * neighbor_radius:
            continue
        if abs(dx) >= abs(dy):
            mid_x = (ax + q[0]) / 2
            if dx > 0:
                x1 = min(x1, mid_x)
            else:
                x0 = max(x0, mid_x)
        else:
            mid_y = (ay + q[1]) / 2
            if dy > 0:
                y1 = min(y1, mid_y)
            else:
                y0 = max(y0, mid_y)
    if x1 <= x0 or y1 <= y0:
        return None
    return (x0, x1, y0, y1)

# Fallback textuel : conserve pour les onglets sans repere 'n°NN' localise
ANCHOR_FALLBACK = {
    4:  r'Radier du Puits',
    8:  r'voir détails folios 30 à 33',
    30: r'partie courante avec imperméabilisation',
    31: r"ancré dans parois moulées avec imperméabilisati",
    32: r"partie courante sans imperméabilisation",
    37: r'Détail ancrage par Bride|Système Bride',
    39: r'Soudure manuelle sur tôle colaminée',
}

layouts = []
for name in doc.layout_names_in_taborder():
    if name.lower() == "model":
        continue
    m = re.match(r"\s*(\d+)", name)
    num = int(m.group(1)) if m else None
    layouts.append((num, name))
layouts.sort(key=lambda t: (t[0] is None, t[0]))

report = []
with PdfPages(PDF_OUT) as pdf:
    # page de garde : rendu direct de l'espace papier (fonctionne bien, deja valide)
    fig0 = plt.figure(figsize=(11.7, 16.5))
    ax0 = fig0.add_axes([0, 0, 1, 1])
    ax0.axis("off")
    Frontend(ctx, MatplotlibBackend(ax0), config=CFG).draw_layout(
        doc.layout("00 - Page de garde"), finalize=True
    )
    pdf.savefig(fig0)
    plt.close(fig0)
    report.append((0, "page de garde", "OK (draw_layout)"))

    for num, name in layouts:
        if num == 0:
            continue
        win = far_viewport_window(name)
        method = "viewport far-field"
        if win is None:
            win = locator_window(num)
            if win is not None:
                method = "repere n°NN + Voronoi"
        if win is None and num in ANCHOR_FALLBACK:
            win = anchor_window(ANCHOR_FALLBACK[num])
            method = "ancre texte (fallback)"
        if win is None:
            title = name.split(" - ", 1)[1] if " - " in name else name
            fig = plt.figure(figsize=(16.5, 10))
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")
            ax.text(0.5, 0.55, f"Folio {num:02d} — {title}", ha="center", va="center",
                     fontsize=13, wrap=True, transform=ax.transAxes)
            ax.text(0.5, 0.42,
                     "Rendu indisponible : le viewport papier de cet onglet pointe vers\n"
                     "l'origine du Model dans le fichier source (anomalie preexistante,\n"
                     "non introduite par les reprises v02 — cf. NOTES.md).\n"
                     "A verifier/recadrer manuellement dans AutoCAD.",
                     ha="center", va="center", fontsize=10, color="0.3",
                     transform=ax.transAxes)
            pdf.savefig(fig)
            plt.close(fig)
            report.append((num, name, "PAGE DE REPLI (anomalie viewport source)"))
            continue
        x0, x1, y0, y1 = win
        w, h = x1 - x0, y1 - y0
        fig = plt.figure(figsize=(16.5, max(6, 16.5 * h / w)))
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.90])
        ax.axis("off")
        entities = ents_in(x0, x1, y0, y1)
        Frontend(ctx, MatplotlibBackend(ax), config=CFG).draw_entities(entities)
        # ezdxf force aspect='equal' avec adjustable='datalim' -> etend les axes
        # pour englober toutes les entites (y compris parties qui debordent
        # notre fenetre voulue). On repasse en 'box' pour clipper strictement.
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        title = name.split(" - ", 1)[1] if " - " in name else name
        fig.suptitle(f"Folio {num:02d} — {title}", fontsize=11, y=0.98)
        pdf.savefig(fig)
        plt.close(fig)
        report.append((num, name, f"OK ({method}, {len(entities)} entites)"))

    d = pdf.infodict()
    d["Title"] = "Carnet de détails étanchéité OS — v02 (MAJ F67-III / AFTES GT9)"
    d["Author"] = "Egis"

print(f"PDF genere : {PDF_OUT}")
ok = sum(1 for _, _, s in report if s.startswith("OK"))
ko = [r for r in report if not r[2].startswith("OK")]
print(f"Pages OK : {ok}/{len(report)}")
for num, name, s in report:
    print(f"  [{num if num is not None else '?':>2}] {s:55} {name[:60]}")
if ko:
    print("\n!!! ECHECS:")
    for num, name, s in ko:
        print(f"  [{num}] {name}: {s}")
