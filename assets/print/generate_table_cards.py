#!/usr/bin/env python3
"""Table cards (noms de tables = les 24 senteurs), two formats, black & white.

Large A5 portrait (148×210 mm) to stand on the table, and a small entrance card
A7 portrait (74×105 mm) = the A5 design at exactly ½ scale (identical design).

Each card: a small number (Nº), a simple B&W line drawing of the scent's plant, the
table name in IBM Plex Serif. Double thin border. Ink only (« en noir et blanc »).

Outputs (assets/print/):
  tables-A5.pdf  — 24 pages, big format
  tables-A7.pdf  — 24 pages, small entrance format
  tables-preview.png — a couple of full cards for review

Run from repo root:  python3 assets/print/generate_table_cards.py
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import fitz
from table_motifs import MOTIFS, INK

HERE = os.path.dirname(__file__)
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
PLEX = FDIR+"IBMPlexSerif-Regular.ttf"
PLEX_IT = FDIR+"IBMPlexSerif-Italic.ttf"
GREY = colors.Color(120/255, 120/255, 116/255)
HAIR = colors.Color(188/255, 188/255, 184/255)
A5 = (148*mm, 210*mm)


def _num_fits(c, name, fs, maxw):
    return c.stringWidth(name, "Plex", fs) <= maxw


def global_name_fs(c, W):
    m = W*0.075; maxw = W - 2*m - W*0.09; base = W*0.083
    fs = base
    for name, _ in MOTIFS:
        while fs > W*0.05 and not _num_fits(c, name, fs, maxw):
            fs -= 0.5
    return fs


def draw_card(c, W, H, number, name, motif, name_fs):
    cx = W/2
    def Y(off): return H - off
    m = W*0.075
    c.setStrokeColor(HAIR); c.setLineWidth(1.1); c.rect(m, m, W-2*m, H-2*m)
    c.setStrokeColor(HAIR); c.setLineWidth(0.5); c.rect(m+3.2, m+3.2, W-2*m-6.4, H-2*m-6.4)

    # number (top, small, letter-spaced)
    num = "Nº %d" % number
    s = W*0.05; tr = s*0.30; c.setFont("Plex", s); c.setFillColor(GREY)
    ws = [c.stringWidth(ch, "Plex", s) for ch in num]
    tot = sum(ws) + tr*(len(num)-1); x = cx - tot/2; y = Y(m+W*0.105)
    for ch, wch in zip(num, ws):
        c.drawString(x, y, ch); x += wch + tr

    # motif (centred, upper-middle)
    motif(c, cx, H*0.455, H*0.15, max(1.0, W*0.0055))

    # name (Plex Serif, uniform size across all cards)
    c.setFillColor(INK); c.setFont("Plex", name_fs)
    c.drawCentredString(cx, Y(H*0.82), name)
    c.setStrokeColor(HAIR); c.setLineWidth(0.8)
    c.line(cx - W*0.11, Y(H*0.855), cx + W*0.11, Y(H*0.855))


def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))
    a5 = os.path.join(HERE, "tables-A5.pdf")
    c = canvas.Canvas(a5, pagesize=A5)
    name_fs = global_name_fs(c, A5[0])
    for i, (name, motif) in enumerate(MOTIFS):
        draw_card(c, A5[0], A5[1], i+1, name, motif, name_fs)
        c.showPage()
    c.save()

    # A7 = A5 at ½ scale, identical design
    a7 = os.path.join(HERE, "tables-A7.pdf")
    src = fitz.open(a5); out = fitz.open()
    for pno in range(src.page_count):
        pg = out.new_page(width=A5[0]/2, height=A5[1]/2)
        pg.show_pdf_page(pg.rect, src, pno)
    out.save(a7); src.close(); out.close()

    from PIL import Image
    d = fitz.open(a5)
    # preview: two full cards side by side
    ims = [Image.frombytes("RGB", (p.width, p.height), p.samples)
           for p in (d[0].get_pixmap(dpi=150), d[11].get_pixmap(dpi=150))]
    gap = 30; Wt = sum(im.width for im in ims)+gap*3; Ht = max(im.height for im in ims)+gap*2
    sheet = Image.new("RGB", (Wt, Ht), (240, 239, 235)); xx = gap
    for im in ims:
        sheet.paste(im, (xx, gap)); xx += im.width+gap
    sheet.save(os.path.join(HERE, "tables-preview.png"))
    # overview: all 24 cards as a grid
    cols, rows = 4, 6
    th = [Image.frombytes("RGB", (p.width, p.height), p.samples)
          for p in (d[i].get_pixmap(dpi=52) for i in range(24))]
    tw, thh = th[0].size; g = 12
    mont = Image.new("RGB", (cols*tw+g*(cols+1), rows*thh+g*(rows+1)), (236, 235, 231))
    for i, im in enumerate(th):
        mont.paste(im, (g+(i % cols)*(tw+g), g+(i//cols)*(thh+g)))
    mont.save(os.path.join(HERE, "tables-overview.png"))
    print("wrote", a5, "(24p),", a7, "(24p), + previews | name_fs=%.1f" % name_fs)


if __name__ == "__main__":
    build()
