#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAJ carnet étanchéité OS — passe 1 sur source DXF (portage des corrections
déjà actées dans la passe PDF, cf. CLAUDE.md "Déjà fait").

Périmètre STRICT de cette passe :
  - orthographe : soutenement -> soutènement ; centres HEB -> cintres HEB ;
    REVETEMENT/Revetement -> REVÊTEMENT/Revêtement
  - renvois : "Détail n°18" -> "Détail folio 65"
  - noms d'onglets : 38 étancchéité -> étanchéité ; 53-58 impermeabilisation
    -> imperméabilisation
Hors périmètre (volontairement) :
  - les 5 points bloquants réservés à Bertrand Verrière (cf. CLAUDE.md)
  - harmonisation décimales point/virgule (convention source = point)
  - accentuation générique des capitales non documentée (ex. MOULEE)

Usage: python3 apply_corrections_v02.py IN.dxf OUT.dxf RAPPORT.txt
"""
import sys, re, ezdxf

IN, OUT, RAP = sys.argv[1], sys.argv[2], sys.argv[3]
doc = ezdxf.readfile(IN)
msp = doc.modelspace()
log = []

# ---------------------------------------------------------------- remplacements
RULES = [
    (re.compile(r'soutenement'), 'soutènement'),
    (re.compile(r'Soutenement'), 'Soutènement'),
    (re.compile(r'SOUTENEMENT'), 'SOUTÈNEMENT'),
    (re.compile(r'\bcentres HEB'), 'cintres HEB'),
    (re.compile(r'\bCentres HEB'), 'Cintres HEB'),
    (re.compile(r'\bCENTRES HEB'), 'CINTRES HEB'),
    (re.compile(r'REVETEMENT'), 'REVÊTEMENT'),
    (re.compile(r'Revetement'), 'Revêtement'),
    (re.compile(r'\brevetement'), 'revêtement'),
    (re.compile(r'Détail n°18\b'), 'Détail folio 65'),
    (re.compile(r'Détail N°18\b'), 'Détail folio 65'),
    # coquille sommaire page de garde (bloc table *T232)
    (re.compile(r'psur aroi'), 'sur paroi'),
    # inversion de lettres repérée au rendu de contrôle (folio 29 e.a.)
    (re.compile(r'mécanqiue'), 'mécanique'),
    (re.compile(r'Mécanqiue'), 'Mécanique'),
    (re.compile(r'MECANQIUE'), 'MECANIQUE'),
]

# étiquette de renvoi isolée sur les vues de principe (TEXT seul "n°18")
LONE = {'n°18': 'folio 65'}

def fix(raw):
    if raw.strip() in LONE:
        return raw.replace(raw.strip(), LONE[raw.strip()])
    new = raw
    for rx, rep in RULES:
        new = rx.sub(rep, new)
    return new

seen = set()
def apply_on(container, e, get, set_):
    h = e.dxf.handle
    if h in seen:
        return
    seen.add(h)
    raw = get()
    if not raw:
        return
    new = fix(raw)
    if new != raw:
        set_(new)
        log.append(f"[{container}] {e.dxftype()} #{h}\n    AVANT: {' '.join(raw.split())[:120]}\n    APRES: {' '.join(new.split())[:120]}")

def walk(container, space):
    for e in space:
        t = e.dxftype()
        if t == "MTEXT":
            apply_on(container, e, lambda e=e: e.text, lambda v, e=e: setattr(e, 'text', v))
        elif t == "TEXT":
            apply_on(container, e, lambda e=e: e.dxf.text, lambda v, e=e: e.dxf.__setattr__('text', v))
        elif t == "DIMENSION":
            tx = e.dxf.get("text", "")
            if tx and tx not in ("<>",):
                apply_on(container, e, lambda tx=tx: tx, lambda v, e=e: e.dxf.__setattr__('text', v))
        elif t == "INSERT":
            for a in e.attribs:
                apply_on(container, a, lambda a=a: a.dxf.text, lambda v, a=a: a.dxf.__setattr__('text', v))

walk("Model", msp)
for name in doc.layout_names_in_taborder():
    if name.lower() != "model":
        walk("PS:" + name[:30], doc.layout(name))
for b in doc.blocks:
    for e in b:
        t = e.dxftype()
        if t == "MTEXT":
            apply_on("B:" + b.name, e, lambda e=e: e.text, lambda v, e=e: setattr(e, 'text', v))
        elif t in ("TEXT", "ATTDEF"):
            apply_on("B:" + b.name, e, lambda e=e: e.dxf.text, lambda v, e=e: e.dxf.__setattr__('text', v))

# ------------------------------------------------------- renommage des onglets
RENAMES = []
for name in list(doc.layout_names_in_taborder()):
    new = name.replace('étancchéité', 'étanchéité').replace('impermeabilisation', 'imperméabilisation')
    if new != name:
        RENAMES.append((name, new))
for old, new in RENAMES:
    try:
        doc.layouts.rename(old, new)
        log.append(f"[ONGLET] renommé:\n    AVANT: {old}\n    APRES: {new}")
    except Exception as ex:
        log.append(f"[ONGLET] ECHEC rename {old!r}: {type(ex).__name__}: {ex}")

doc.saveas(OUT)
open(RAP, "w").write(f"{len(log)} modifications\n\n" + "\n".join(log) + "\n")
print(f"{len(log)} modifications appliquées -> {OUT}")
print(f"Rapport: {RAP}")
