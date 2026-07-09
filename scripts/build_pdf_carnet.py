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

# fallback pour les onglets dont le viewport pointe vers l'origine ou est absent
ANCHOR_FALLBACK = {
    4:  r'Radier du Puits',
    8:  r'voir détails folios 30 à 33',
    30: r'partie courante avec imperméabilisation',
    31: r"ancré dans parois moulées avec imperméabilisati",
    32: r"partie courante sans imperméabilisation",
    37: r'Détail ancrage par Bride|Système Bride',
    39: r'Soudure manuelle sur tôle colaminée',
}

def ents_in(x0, x1, y0, y1, margin=150):
    out = []
    for e in msp:
        p = None
        for attr in ("insert", "start", "center"):
            try:
                p = getattr(e.dxf, attr)
                break
            except Exception:
                continue
        if p is None:
            try:
                p = e.context.base_point  # MULTILEADER
            except Exception:
                continue
        if x0 - margin <= p.x <= x1 + margin and y0 - margin <= p.y <= y1 + margin:
            out.append(e)
    return out

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
