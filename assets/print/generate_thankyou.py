#!/usr/bin/env python3
"""Thank-you card placed on the plates at the entrance — A5 portrait (148×210 mm).

Warm, humorous tone (the couple are doctors). Practical info: the arrival concert
programme (songs + original performers, by language) and the two house cocktails.
Wedding identity: IBM Plex Serif, sage accent, double border, sage A·R logo.

Run from repo root:  python3 assets/print/generate_thankyou.py
"""
import os
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image
import fitz

HERE = os.path.dirname(__file__)
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
PLEX, PLEX_IT = FDIR+"IBMPlexSerif-Regular.ttf", FDIR+"IBMPlexSerif-Italic.ttf"
LOGO = os.path.join(HERE, "logo-source.png")
PDF  = os.path.join(HERE, "remerciement.pdf")
PNG  = os.path.join(HERE, "remerciement.png")

INK   = colors.Color(43/255,43/255,41/255)
SAGE  = colors.Color(95/255,125/255,99/255)
SAGES = colors.Color(174/255,191/255,163/255)
MUTED = colors.Color(97/255,92/255,86/255)
LINE2 = colors.Color(228/255,231/255,224/255)
W, H = 148*mm, 210*mm

THANK = ("Merci d’être là ! Ce soir, on raccroche la blouse : ni bip, ni garde, ni urgence — "
         "seulement de la musique, deux cocktails maison et beaucoup d’amour à partager.")

CONCERT_L = [("Oriental",
              [("Qadeyat Am Ahmad", "Omar Khairat"),
               ("Longa Riad", "Riad Al-Sunbati")]),
             ("Libanais",
              [("Kan 3anna Ta7oun", "Fairouz"),
               ("Bint el Chalabiya", "Fairouz")])]
CONCERT_R = [("Anglais",
              [("L.O.V.E.", "Nat King Cole"),
               ("Dream a Little Dream of Me", "Ella Fitzgerald & Louis Armstrong")]),
             ("Français",
              [("L’été indien", "Joe Dassin"),
               ("La vie en rose", "Édith Piaf"),
               ("For me… formidable", "Charles Aznavour")])]

DRINKS = [("Droit au cœur",
           "Le chocolate martini du marié : il visait le but… il a fini droit au cœur."),
          ("Propofolle de lui",
           "À l’araq, pour la mariée : une dose d’amour, sédation garantie — sans anesthésiste.")]


def sage_logo():
    im = Image.open(LOGO).convert("RGB"); a = np.asarray(im).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    alpha = np.clip((255-lum)*1.7, 0, 255).astype(np.uint8)
    out = np.zeros((*lum.shape, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 95, 125, 99
    out[..., 3] = alpha
    img = Image.fromarray(out, "RGBA"); bb = img.split()[3].getbbox()
    return img.crop(bb) if bb else img


def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))
    c = canvas.Canvas(PDF, pagesize=(W, H)); cx = W/2
    def Y(off): return H-off

    def wrap(text, font, size, maxw):
        words = text.split(); lines = []; cur = ""
        for w in words:
            t = (cur+" "+w).strip()
            if c.stringWidth(t, font, size) <= maxw: cur = t
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
        return lines

    def block(text, off, font, size, color, leading, maxw, cxc=None):
        cxc = cx if cxc is None else cxc
        c.setFont(font, size); c.setFillColor(color); y = off
        for ln in wrap(text, font, size, maxw):
            c.drawCentredString(cxc, Y(y), ln); y += leading
        return y

    def spaced(text, off, font, size, tr, color, cxc=None):
        cxc = cx if cxc is None else cxc
        c.setFont(font, size); c.setFillColor(color)
        ws = [c.stringWidth(ch, font, size) for ch in text]
        tot = sum(ws)+tr*(len(text)-1); x = cxc-tot/2
        for ch, w in zip(text, ws): c.drawString(x, Y(off), ch); x += w+tr

    def rule(off, half):
        c.setStrokeColor(SAGES); c.setLineWidth(0.9)
        c.line(cx-half-16, Y(off), cx-half-4, Y(off)); c.line(cx+half+4, Y(off), cx+half+16, Y(off))

    # borders
    c.setStrokeColor(SAGES); c.setLineWidth(1.3); c.rect(15, 15, W-30, H-30)
    c.setStrokeColor(LINE2); c.setLineWidth(0.6); c.rect(18.5, 18.5, W-37, H-37)

    # logo
    lg = sage_logo(); tmp = os.path.join(HERE, "_ty_logo.png"); lg.save(tmp)
    lw = 62; lh = lw*lg.height/lg.width
    c.drawImage(ImageReader(tmp), cx-lw/2, H-(28+lh), width=lw, height=lh, mask="auto"); os.remove(tmp)

    c.setFillColor(INK); c.setFont("Plex", 30); c.drawCentredString(cx, Y(112), "Merci")
    block(THANK, 132, "PlexIt", 10, MUTED, 14.5, W-84)

    # ---- concert ----
    rule(182, 40)
    spaced("LE CONCERT", 200, "Plex", 8.5, 2.2, SAGE)
    block("En attendant de passer à table, laissez-vous porter…", 214, "PlexIt", 8.5, MUTED, 12, W-70)

    def col(groups, cxc, top):
        y = top
        for lang, songs in groups:
            c.setFillColor(SAGE); c.setFont("PlexIt", 9.5); c.drawCentredString(cxc, Y(y), lang); y += 12.5
            for title, perf in songs:
                c.setFillColor(INK); c.setFont("Plex", 8.6); c.drawCentredString(cxc, Y(y), title); y += 9.2
                c.setFillColor(MUTED); c.setFont("PlexIt", 7); c.drawCentredString(cxc, Y(y), perf); y += 11.5
            y += 5
        return y
    col(CONCERT_L, W*0.29, 232)
    col(CONCERT_R, W*0.71, 232)

    # ---- cocktails ----
    rule(360, 52)
    spaced("LES COCKTAILS MAISON", 378, "Plex", 8.5, 2.2, SAGE)
    y = 396
    for name, desc in DRINKS:
        c.setFillColor(INK); c.setFont("Plex", 12); c.drawCentredString(cx, Y(y), name); y += 13
        y = block(desc, y, "PlexIt", 8.6, MUTED, 11.5, W-74) + 8

    # closing
    block("Belle soirée — et rendez-vous sur la piste !", 470, "PlexIt", 9.5, SAGE, 12, W-70)
    spaced("ANDRÉ & RHÉA · 22 AOÛT 2026", 492, "Plex", 7.5, 1.6, MUTED)

    c.showPage(); c.save()
    fitz.open(PDF)[0].get_pixmap(dpi=300).save(PNG)
    print("wrote", PDF, "+", PNG)


if __name__ == "__main__":
    build()
