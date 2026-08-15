#!/usr/bin/env python3
"""24 minimalist B&W line motifs (one per scent/table) + a contact-sheet renderer.

Each motif: f(c, cx, cy, R, lw) — drawn centred on (cx, cy), roughly within a box of
half-size R, single ink stroke of width lw. Kept deliberately simple/elegant.
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import fitz

INK = colors.Color(38/255, 38/255, 36/255)


def _setup(c, lw):
    c.setStrokeColor(INK); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1); c.setFillColor(INK)


def leaf(c, bx, by, tx, ty, wid, midrib=True):
    dx, dy = tx-bx, ty-by; L = math.hypot(dx, dy) or 1
    ux, uy = dx/L, dy/L; px, py = -uy, ux
    p = c.beginPath(); p.moveTo(bx, by)
    p.curveTo(bx+ux*L*0.30+px*wid, by+uy*L*0.30+py*wid,
              bx+ux*L*0.70+px*wid, by+uy*L*0.70+py*wid, tx, ty)
    p.curveTo(bx+ux*L*0.70-px*wid, by+uy*L*0.70-py*wid,
              bx+ux*L*0.30-px*wid, by+uy*L*0.30-py*wid, bx, by)
    c.drawPath(p, stroke=1, fill=0)
    if midrib:
        c.line(bx, by, bx+ux*L*0.82, by+uy*L*0.82)


def petal(c, cx, cy, ang, length, wid):
    a = ang; ux, uy = math.cos(a), math.sin(a); px, py = -uy, ux
    tx, ty = cx+ux*length, cy+uy*length
    p = c.beginPath(); p.moveTo(cx, cy)
    p.curveTo(cx+ux*length*0.25+px*wid, cy+uy*length*0.25+py*wid,
              cx+ux*length*0.85+px*wid*0.7, cy+uy*length*0.85+py*wid*0.7, tx, ty)
    p.curveTo(cx+ux*length*0.85-px*wid*0.7, cy+uy*length*0.85-py*wid*0.7,
              cx+ux*length*0.25-px*wid, cy+uy*length*0.25-py*wid, cx, cy)
    c.drawPath(p, stroke=1, fill=0)


def blossom(c, cx, cy, R, n=5, pw=0.62, core=True, phase=0.5):
    for k in range(n):
        a = math.pi*phase + 2*math.pi*k/n
        petal(c, cx, cy, a, R, R*pw)
    if core:
        c.circle(cx, cy, R*0.13, stroke=1, fill=0)


def circle_fruit(c, cx, cy, r, leaves=1):
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.line(cx, cy+r, cx, cy+r*1.28)                       # stem
    for i in range(leaves):
        s = 1 if i % 2 == 0 else -1
        leaf(c, cx, cy+r*1.22, cx+s*r*0.85, cy+r*1.75, r*0.28)


# ---- flowers -------------------------------------------------------------
def jasmin(c, cx, cy, R, lw):
    _setup(c, lw)
    leaf(c, cx, cy-R*0.2, cx-R*0.75, cy-R*0.95, R*0.16)
    leaf(c, cx, cy-R*0.2, cx+R*0.75, cy-R*0.95, R*0.16)
    blossom(c, cx-R*0.34, cy+R*0.28, R*0.42, n=5, pw=0.5)
    blossom(c, cx+R*0.4, cy+R*0.5, R*0.34, n=5, pw=0.5)
    c.line(cx-R*0.34, cy+R*0.28, cx, cy-R*0.2)
    c.line(cx+R*0.4, cy+R*0.5, cx, cy-R*0.2)


def fleur_oranger(c, cx, cy, R, lw):
    _setup(c, lw)
    leaf(c, cx-R*0.1, cy-R*0.1, cx-R*0.9, cy+R*0.15, R*0.22)
    leaf(c, cx+R*0.1, cy-R*0.1, cx+R*0.9, cy+R*0.15, R*0.22)
    blossom(c, cx, cy+R*0.28, R*0.62, n=5, pw=0.6)


def rose(c, cx, cy, R, lw):
    _setup(c, lw)
    by = cy + R*0.35                                       # bloom centre
    # bloom outline (rounded, slightly egg-shaped, opening upward)
    p = c.beginPath(); p.moveTo(cx, by+R*0.65)
    p.curveTo(cx+R*0.62, by+R*0.55, cx+R*0.6, by-R*0.5, cx, by-R*0.6)
    p.curveTo(cx-R*0.6, by-R*0.5, cx-R*0.62, by+R*0.55, cx, by+R*0.65)
    c.drawPath(p, stroke=1, fill=0)
    # furled inner petals — a couple of smooth swirling curves
    c.setLineWidth(lw*0.85)
    p = c.beginPath(); p.moveTo(cx-R*0.3, by+R*0.15)
    p.curveTo(cx+R*0.1, by+R*0.4, cx+R*0.34, by-R*0.05, cx+R*0.05, by-R*0.22)
    c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath(); p.moveTo(cx-R*0.02, by-R*0.28)
    p.curveTo(cx-R*0.3, by-R*0.12, cx-R*0.22, by+R*0.28, cx+R*0.08, by+R*0.25)
    c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(lw)
    c.line(cx, by-R*0.6, cx, cy-R*1.0)                     # stem
    leaf(c, cx, cy-R*0.72, cx+R*0.62, cy-R*0.5, R*0.2)


def pivoine(c, cx, cy, R, lw):
    _setup(c, lw)
    blossom(c, cx, cy, R*0.98, n=7, pw=0.4, core=False, phase=0.5)
    blossom(c, cx, cy, R*0.52, n=6, pw=0.4, core=False, phase=0.64)
    c.circle(cx, cy, R*0.1, stroke=1, fill=0)


def magnolia(c, cx, cy, R, lw):
    _setup(c, lw)
    blossom(c, cx, cy+R*0.05, R*0.95, n=6, pw=0.42, core=False, phase=0.5)
    for a in (1.15, 1.37, 1.6, 1.83):                      # short stamens in the centre
        c.line(cx, cy+R*0.05, cx+math.cos(a)*R*0.22, cy+R*0.05+math.sin(a)*R*0.22)
    leaf(c, cx+R*0.55, cy-R*0.7, cx+R*1.02, cy-R*0.18, R*0.16)


def iris(c, cx, cy, R, lw):
    _setup(c, lw)
    # three upright standards
    petal(c, cx, cy, math.pi*0.5, R*0.95, R*0.3)
    petal(c, cx, cy, math.pi*0.5-0.5, R*0.8, R*0.26)
    petal(c, cx, cy, math.pi*0.5+0.5, R*0.8, R*0.26)
    # three drooping falls
    petal(c, cx, cy, math.pi*1.5, R*0.9, R*0.34)
    petal(c, cx, cy, math.pi*1.5-0.55, R*0.85, R*0.3)
    petal(c, cx, cy, math.pi*1.5+0.55, R*0.85, R*0.3)
    c.line(cx, cy-R*0.9, cx, cy-R*1.15)


def musc(c, cx, cy, R, lw):
    # cotton boll — three fluffy lobes over a pointed star calyx + short stem
    _setup(c, lw)
    for dx, dy in ((0, 0.45), (-0.42, -0.02), (0.42, -0.02)):
        c.circle(cx+R*dx, cy+R*dy, R*0.44, stroke=1, fill=0)
    basey = cy - R*0.35
    for a in (-0.5, 0.0, 0.5):                             # calyx sepal points
        c.line(cx, basey, cx+math.sin(a)*R*0.85, basey-R*0.7)
    c.line(cx, basey, cx, cy-R*1.0)                        # stem


def miel(c, cx, cy, R, lw):
    # honeycomb cluster + a drop
    _setup(c, lw)
    def hexagon(hx, hy, s):
        p = c.beginPath()
        for i in range(6):
            a = math.pi/6 + i*math.pi/3
            x, y = hx+math.cos(a)*s, hy+math.sin(a)*s
            (p.moveTo if i == 0 else p.lineTo)(x, y)
        p.close(); c.drawPath(p, stroke=1, fill=0)
    s = R*0.42; dx = s*math.cos(math.pi/6)*2
    hexagon(cx-dx*0.5, cy+R*0.35, s); hexagon(cx+dx*0.5, cy+R*0.35, s)
    hexagon(cx, cy+R*0.35+s*1.5, s)
    # honey drop
    p = c.beginPath(); p.moveTo(cx, cy-R*0.55)
    p.curveTo(cx+R*0.28, cy-R*0.2, cx+R*0.22, cy+R*0.1, cx, cy+R*0.1)
    p.curveTo(cx-R*0.22, cy+R*0.1, cx-R*0.28, cy-R*0.2, cx, cy-R*0.55)
    c.drawPath(p, stroke=1, fill=0)


# ---- citrus --------------------------------------------------------------
def citron(c, cx, cy, R, lw):
    _setup(c, lw); circle_fruit(c, cx, cy-R*0.1, R*0.66, leaves=1)


def bergamote(c, cx, cy, R, lw):
    _setup(c, lw)
    circle_fruit(c, cx-R*0.15, cy-R*0.1, R*0.6, leaves=0)
    c.line(cx-R*0.15, cy-R*0.7, cx-R*0.15, cy-R*0.95)
    leaf(c, cx+R*0.2, cy+R*0.3, cx+R*0.95, cy+R*0.55, R*0.22)


def pamplemousse(c, cx, cy, R, lw):
    # citrus half — segments
    _setup(c, lw)
    r = R*0.8
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.circle(cx, cy, r*0.86, stroke=1, fill=0)
    for k in range(8):
        a = math.pi/8 + k*math.pi/4
        c.line(cx+math.cos(a)*r*0.06, cy+math.sin(a)*r*0.06,
               cx+math.cos(a)*r*0.84, cy+math.sin(a)*r*0.84)


# ---- herbs / leaves ------------------------------------------------------
def menthe(c, cx, cy, R, lw):
    _setup(c, lw)
    c.line(cx, cy-R*0.95, cx, cy+R*0.9)
    for k, yy in enumerate((-0.5, 0.05, 0.55)):
        s = R*(0.9-0.18*k)
        leaf(c, cx, cy+R*yy, cx-s, cy+R*yy+R*0.42, R*0.2)
        leaf(c, cx, cy+R*yy, cx+s, cy+R*yy+R*0.42, R*0.2)


def verveine(c, cx, cy, R, lw):
    _setup(c, lw)
    c.line(cx, cy-R*1.0, cx, cy+R*0.95)
    for yy in (-0.7, -0.3, 0.1, 0.5):
        leaf(c, cx, cy+R*yy, cx-R*0.8, cy+R*yy-R*0.12, R*0.11)
        leaf(c, cx, cy+R*yy, cx+R*0.8, cy+R*yy-R*0.12, R*0.11)
    for a in (1.2, 1.5, 1.8):                              # tiny flower spike
        c.circle(cx+math.cos(a)*R*0.12, cy+R*0.9+math.sin(a)*R*0.12, R*0.07, stroke=1, fill=0)


def patchouli(c, cx, cy, R, lw):
    _setup(c, lw)
    c.line(cx, cy-R*0.95, cx, cy+R*0.5)
    leaf(c, cx, cy+R*0.1, cx-R*0.6, cy+R*0.95, R*0.34)
    leaf(c, cx, cy+R*0.1, cx+R*0.6, cy+R*0.95, R*0.34)
    leaf(c, cx, cy-R*0.4, cx-R*0.45, cy-R*0.95, R*0.24)
    leaf(c, cx, cy-R*0.4, cx+R*0.45, cy-R*0.95, R*0.24)


def the_noir(c, cx, cy, R, lw):
    # two leaves and a bud
    _setup(c, lw)
    c.line(cx, cy-R*0.9, cx, cy+R*0.2)
    leaf(c, cx, cy-R*0.1, cx-R*0.85, cy+R*0.5, R*0.26)
    leaf(c, cx, cy-R*0.1, cx+R*0.85, cy+R*0.5, R*0.26)
    leaf(c, cx, cy+R*0.2, cx, cy+R*0.95, R*0.16)           # central bud/leaf


# ---- trees / wood --------------------------------------------------------
def cedre(c, cx, cy, R, lw):
    # Lebanon cedar — broad, flat-topped, layered foliage masses
    _setup(c, lw)
    c.line(cx, cy-R*1.0, cx, cy-R*0.35)                    # short trunk
    # flattened foliage tiers (widest in the middle), drawn as low lens shapes
    for yy, ww, hh in [(-0.25, 0.55, 0.16), (0.12, 0.95, 0.2),
                       (0.5, 0.78, 0.17), (0.85, 0.45, 0.14)]:
        y = cy + R*yy
        p = c.beginPath(); p.moveTo(cx-R*ww, y)
        p.curveTo(cx-R*ww*0.5, y+R*hh, cx+R*ww*0.5, y+R*hh, cx+R*ww, y)   # flat-ish top
        p.curveTo(cx+R*ww*0.5, y-R*hh*0.7, cx-R*ww*0.5, y-R*hh*0.7, cx-R*ww, y)  # underside
        c.drawPath(p, stroke=1, fill=0)


def cypres(c, cx, cy, R, lw):
    _setup(c, lw)
    yb = cy - R*0.85; h = R*1.75; w = R*0.9
    p = c.beginPath(); p.moveTo(cx-w*0.5, yb)
    p.curveTo(cx-w*0.52, yb+h*0.45, cx-w*0.22, yb+h*0.8, cx, yb+h)
    p.curveTo(cx+w*0.22, yb+h*0.8, cx+w*0.52, yb+h*0.45, cx+w*0.5, yb)
    p.curveTo(cx+w*0.28, yb-h*0.03, cx-w*0.28, yb-h*0.03, cx-w*0.5, yb)
    c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(lw*0.7); c.line(cx, yb+h*0.05, cx, yb+h*0.9)
    for t in (0.3, 0.5, 0.7):
        yy = yb+h*t; ww = w*0.42*(1-t)
        c.line(cx, yy, cx-ww, yy-h*0.05); c.line(cx, yy, cx+ww, yy-h*0.05)
    c.setLineWidth(lw); c.line(cx, yb, cx, yb-R*0.18)


def santal(c, cx, cy, R, lw):
    # leafy branch (sandalwood)
    _setup(c, lw)
    p = c.beginPath(); p.moveTo(cx-R*0.7, cy-R*0.9)
    p.curveTo(cx-R*0.2, cy-R*0.3, cx+R*0.1, cy+R*0.3, cx+R*0.55, cy+R*0.95)
    c.drawPath(p, stroke=1, fill=0)
    pts = [(-0.45, -0.55, -1, 0), (-0.05, -0.05, 1, 0.2), (0.2, 0.4, -1, 0.35)]
    for bx, by, s, _ in pts:
        leaf(c, cx+R*bx, cy+R*by, cx+R*bx+s*R*0.7, cy+R*by+R*0.2, R*0.2)


def oud(c, cx, cy, R, lw):
    # piece of agarwood — a horizontal log, cut end showing rings + bark
    _setup(c, lw)
    w, h = R*0.95, R*0.5                                   # half-length, half-height
    c.line(cx-w, cy-h, cx+w*0.75, cy-h)                    # top & bottom edges
    c.line(cx-w, cy+h, cx+w*0.75, cy+h)
    c.ellipse(cx-w-R*0.24, cy-h, cx-w+R*0.24, cy+h, stroke=1, fill=0)      # left cut end
    c.ellipse(cx-w-R*0.10, cy-h*0.5, cx-w+R*0.10, cy+h*0.5, stroke=1, fill=0)  # inner ring
    c.ellipse(cx+w*0.75-R*0.2, cy-h, cx+w*0.75+R*0.2, cy+h, stroke=1, fill=0)  # right end
    for gx in (-0.35, 0.1, 0.5):                           # bark grain
        c.line(cx+w*gx, cy-h*0.7, cx+w*gx, cy+h*0.7)


# ---- spices / pods -------------------------------------------------------
def cardamome(c, cx, cy, R, lw):
    _setup(c, lw)
    for dx, ang in ((-0.5, 0.25), (0.15, -0.1), (0.6, 0.2)):
        px, py = cx+R*dx, cy
        a = ang
        # small oval pod, pointed top
        p = c.beginPath(); p.moveTo(px, py-R*0.7)
        p.curveTo(px+R*0.3, py-R*0.3, px+R*0.28, py+R*0.5, px, py+R*0.62)
        p.curveTo(px-R*0.28, py+R*0.5, px-R*0.3, py-R*0.3, px, py-R*0.7)
        c.drawPath(p, stroke=1, fill=0)
        c.line(px, py-R*0.62, px, py+R*0.5)
        c.line(px, py-R*0.7, px, py-R*0.92)


def cannelle(c, cx, cy, R, lw):
    # two cinnamon quills
    _setup(c, lw)
    for dx in (-0.32, 0.32):
        x = cx+R*dx
        c.roundRect(x-R*0.16, cy-R*0.95, R*0.32, R*1.9, R*0.14, stroke=1, fill=0)
        # rolled end (spiral) at top
        c.ellipse(x-R*0.16, cy+R*0.7, x+R*0.16, cy+R*0.95, stroke=1, fill=0)
        c.line(x-R*0.05, cy-R*0.9, x-R*0.05, cy+R*0.75)


def vanille(c, cx, cy, R, lw):
    # two long slender pods + a small bloom
    _setup(c, lw)
    for dx in (-0.22, 0.14):
        x = cx+R*dx
        p = c.beginPath(); p.moveTo(x, cy-R*0.95)
        p.curveTo(x+R*0.12, cy-R*0.3, x+R*0.12, cy+R*0.5, x+R*0.05, cy+R*0.95)
        c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath(); p.moveTo(x+R*0.14, cy-R*0.9)
        p.curveTo(x+R*0.26, cy-R*0.3, x+R*0.26, cy+R*0.5, x+R*0.19, cy+R*0.92)
        c.drawPath(p, stroke=1, fill=0)
        c.line(x, cy-R*0.95, x+R*0.14, cy-R*0.9)
        c.line(x+R*0.05, cy+R*0.95, x+R*0.19, cy+R*0.92)
    blossom(c, cx+R*0.55, cy-R*0.5, R*0.32, n=5, pw=0.5)


def feve_tonka(c, cx, cy, R, lw):
    _setup(c, lw)
    def bean(bx, by, s, rot):
        p = c.beginPath()
        pts = []
        for i in range(0, 361, 20):
            a = math.radians(i)
            rr = s*(1.0 + 0.12*math.cos(a*2))
            x = bx + math.cos(a)*rr*1.35
            y = by + math.sin(a)*rr*0.8
            # rotate
            xr = bx + (x-bx)*math.cos(rot) - (y-by)*math.sin(rot)
            yr = by + (x-bx)*math.sin(rot) + (y-by)*math.cos(rot)
            pts.append((xr, yr))
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close(); c.drawPath(p, stroke=1, fill=0)
        # seam
        c.line(bx-s*1.0, by, bx+s*1.0, by)
    bean(cx-R*0.28, cy+R*0.2, R*0.5, 0.5)
    bean(cx+R*0.35, cy-R*0.25, R*0.42, 0.7)


def chocolat(c, cx, cy, R, lw):
    # cacao pod — ridged elongated pod
    _setup(c, lw)
    w, h = R*0.6, R*1.5
    p = c.beginPath(); p.moveTo(cx, cy-h*0.5)
    p.curveTo(cx+w, cy-h*0.3, cx+w, cy+h*0.3, cx, cy+h*0.5)
    p.curveTo(cx-w, cy+h*0.3, cx-w, cy-h*0.3, cx, cy-h*0.5)
    c.drawPath(p, stroke=1, fill=0)
    for gx in (-0.55, 0.0, 0.55):
        p = c.beginPath(); p.moveTo(cx+w*gx*0.6, cy-h*0.42)
        p.curveTo(cx+w*gx, cy-h*0.15, cx+w*gx, cy+h*0.15, cx+w*gx*0.6, cy+h*0.42)
        c.drawPath(p, stroke=1, fill=0)
    c.line(cx, cy-h*0.5, cx, cy-h*0.62)


MOTIFS = [
    ("Jasmin d’Orient", jasmin), ("Fleur d’Oranger", fleur_oranger), ("Rose de Mai", rose),
    ("Pivoine Blanche", pivoine), ("Magnolia de Méditerranée", magnolia), ("Iris Poudré", iris),
    ("Citron Vert", citron), ("Bergamote", bergamote), ("Pamplemousse", pamplemousse),
    ("Verveine", verveine), ("Menthe Fraîche", menthe), ("Cèdre du Liban", cedre),
    ("Santal Boisé", santal), ("Bois d’Oud", oud), ("Cyprès de Montagne", cypres),
    ("Vanille Bourbon", vanille), ("Fève Tonka", feve_tonka), ("Miel de Fleurs", miel),
    ("Cardamome", cardamome), ("Patchouli Tropical", patchouli), ("Cannelle", cannelle),
    ("Chocolat des Îles", chocolat), ("Musc Blanc", musc), ("Thé Noir", the_noir),
]


def contact_sheet(path_pdf, path_png):
    cols, rows = 4, 6
    cw, ch = 150, 175
    W, H = cols*cw, rows*ch
    c = canvas.Canvas(path_pdf, pagesize=(W, H))
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
    pdfmetrics.registerFont(TTFont("Plex", FDIR+"IBMPlexSerif-Regular.ttf"))
    for i, (name, fn) in enumerate(MOTIFS):
        col = i % cols; row = i // cols
        cx = col*cw + cw/2; cy = H - (row*ch + ch*0.46)
        fn(c, cx, cy, 44, 1.4)
        c.setFillColor(INK); c.setFont("Plex", 9)
        c.drawCentredString(cx, H-(row*ch+ch*0.92), "%d · %s" % (i+1, name))
        c.setStrokeColor(colors.Color(0.85,0.85,0.83)); c.setLineWidth(0.4)
        c.rect(col*cw+6, H-(row*ch+ch)+6, cw-12, ch-12, stroke=1, fill=0)
    c.showPage(); c.save()
    fitz.open(path_pdf)[0].get_pixmap(dpi=200).save(path_png)
    print("wrote", path_png)


if __name__ == "__main__":
    import os
    HERE = os.path.dirname(__file__)
    contact_sheet(os.path.join(HERE, "_contact.pdf"), os.path.join(HERE, "_contact.png"))
