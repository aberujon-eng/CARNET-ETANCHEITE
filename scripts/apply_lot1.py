#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lot 1 des reprises du mail à Bertrand (docs/mail_bertrand_reprises_v02.txt)
— uniquement les reprises textuelles à formulation explicite dans le mail.

Couvre : T4 (hydrogonflant), T3 (mortiers NF EN 1504-3), P22/23 (note MOE GC
découpe voussoir), P55/57/59 (renvoi carottages folio 50), P56+57-60
(feuillard matériau + entraxe), P29 (plats galvanisés ou inox), P34 (chape
DEG 5->6 cm, cible 6 cm donnée par P47), P24 (doublon hydrogonflant si
superposé).

Usage: python3 apply_lot1.py FICHIER.dxf RAPPORT.txt   (modifie en place)
"""
import sys, re, ezdxf

PATH, RAP = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(PATH)
msp = doc.modelspace()
log = []

RULES = [
    # T4 — harmonisation "joint hydrogonflant"
    (re.compile(r'hydro-?expansif'), 'hydrogonflant'),
    (re.compile(r'Hydro-?expansif'), 'Hydrogonflant'),
    # T3 — mortiers réparation : classe R3/R4 selon NF EN 1504-3
    (re.compile(r'mortier type R([34])\b(?![^\\]*1504)'), r'mortier classe R\1 selon NF EN 1504-3'),
    (re.compile(r'Mortier de ragréage R4\b(?!.*1504)'), 'Mortier de ragréage classe R4 selon NF EN 1504-3'),
    (re.compile(r'Mortier R3 mini\b(?!.*1504)'), 'mortier classe R3 mini selon NF EN 1504-3'),
    (re.compile(r'mortier à retrait compensé(?! selon)'), 'mortier à retrait compensé selon NF EN 1504-3'),
    # P22/23/24 — découpe du voussoir : validation structure
    (re.compile(r'Découpe possible du voussoir(?!\s*\()'), 'Découpe possible du voussoir (accord préalable MOE GC obligatoire)'),
]

# éditions ciblées par handle (formulation du mail)
TARGETED = {
    # P29 — option inox (cohérence folio 65)
    '1637D': (re.compile(r'Plats galvanisés'), 'Plats galvanisés ou inox'),
    # P34 — chape de protection DEG : harmonisation à 6 cm (P47 : 6 cm conforme)
    '6030': (re.compile(r'ép\.5cm mini'), 'ép.6cm mini'),
}

# P55/57/59 — NOTA carottages : renvoi folio 50
CAROTTAGE = {'13653', '136F2', '13991'}
# P56 + P57-60 — feuillard : matériau + entraxe (formulation du mail)
FEUILLARD_FOLIOS_HANDLES = {'135DD','13602','1362E','1367E','136A2','136CE','13921','13942','1396E'}
FEUILLARD_NEW = 'Feuillard métallique (inox ou galvanisé) fixé mécaniquement\\P(FPM verticale : 4 fixations/ml, tous les 3 m)'

def fix(raw):
    new = raw
    for rx, rep in RULES:
        new = rx.sub(rep, new)
    return new

def note(container, h, layer, before, after):
    log.append(f"[{container}] #{h} calque={layer!r}\n    AVANT: {' '.join(before.split())[:110]}\n    APRES: {' '.join(after.split())[:110]}")

seen = set()
def process(container, e):
    h = e.dxf.handle
    if h in seen:
        return
    seen.add(h)
    t = e.dxftype()
    if t == "MTEXT":
        raw = e.text
        new = fix(raw)
        if h in TARGETED:
            rx, rep = TARGETED[h]; new = rx.sub(rep, new)
        if h in CAROTTAGE and 'folio 50' not in new:
            new = new.rstrip() + ' (cf. folio 50)'
        if new != raw:
            e.text = new; note(container, h, e.dxf.layer, raw, new)
    elif t in ("TEXT", "ATTDEF"):
        raw = e.dxf.text
        new = fix(raw)
        if new != raw:
            e.dxf.text = new; note(container, h, e.dxf.layer, raw, new)
    elif t == "MULTILEADER":
        try:
            mt = e.context.mtext
        except Exception:
            return
        if not mt or not mt.default_content:
            return
        raw = mt.default_content
        new = fix(raw)
        if h in TARGETED:
            rx, rep = TARGETED[h]; new = rx.sub(rep, new)
        if h in FEUILLARD_FOLIOS_HANDLES:
            new = FEUILLARD_NEW
        if new != raw:
            mt.default_content = new; note(container, h, e.dxf.layer, raw, new)
    elif t == "INSERT":
        for a in e.attribs:
            raw = a.dxf.text; new = fix(raw)
            if new != raw:
                a.dxf.text = new; note(container, a.dxf.handle, a.dxf.layer, raw, new)

for e in msp:
    process("Model", e)
for name in doc.layout_names_in_taborder():
    if name.lower() != "model":
        for e in doc.layout(name):
            process("PS:" + name[:25], e)
for b in doc.blocks:
    for e in b:
        process("B:" + b.name, e)

# P24 — doublon "Joint hydrogonflant" : suppression uniquement si superposé (<5 u)
try:
    a = doc.entitydb['BA4F']; b = doc.entitydb['EB7E']
    pa, pb = a.dxf.insert, b.dxf.insert
    d = ((pa.x-pb.x)**2 + (pa.y-pb.y)**2) ** .5
    if d < 5.0:
        msp.delete_entity(b)
        log.append(f"[Model] #EB7E doublon 'Joint hydrogonflant' supprimé (distance {d:.2f} u de #BA4F)")
    else:
        log.append(f"[Model] doublon P24 NON supprimé : #BA4F et #EB7E distants de {d:.1f} u — à vérifier visuellement")
except Exception as ex:
    log.append(f"[Model] doublon P24 : vérification impossible ({ex})")

doc.saveas(PATH)
open(RAP, "w").write(f"LOT 1 — {len(log)} modifications\n\n" + "\n".join(log) + "\n")
print(f"{len(log)} modifications -> {PATH}")
