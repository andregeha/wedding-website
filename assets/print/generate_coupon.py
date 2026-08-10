#!/usr/bin/env python3
"""« Parfum » coupon handed out at the entrance — A6 portrait (105 × 148 mm).

Points guests to choose & collect their perfume at the verre d'accueil. Same identity as the
faire-part: IBM Plex Serif, sage accent, double sage border, the hand-drawn A·R logo (sage).

Run from repo root:  python3 assets/print/generate_coupon.py
Requires: reportlab, pymupdf, Pillow, numpy
Content mirrors the client's approved wording — keep in sync.
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
PDF  = os.path.join(HERE, "coupon.pdf")
PNG  = os.path.join(HERE, "coupon.png")

INK   = colors.Color(43/255, 43/255, 41/255)
SAGE  = colors.Color(95/255, 125/255, 99/255)
SAGES = colors.Color(174/255, 191/255, 163/255)
MUTED = colors.Color(97/255, 92/255, 86/255)

W, H = 105*mm, 148*mm

QUOTE = "« Celui qui maîtrisait les odeurs maîtrisait le cœur de l’humanité. »"
ATTRIB = "— Patrick Süskind, Le Parfum"
BODY = ("Parce que nous aimerions que le souvenir de notre union parfume nos retrouvailles "
        "à venir, allez choisir le vôtre parmi les cinq senteurs que nous avons composées !")
FOOT = "À choisir et à emporter lors du verre d’accueil."


def sage_logo():
    im = Image.open(LOGO).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    alpha = np.clip((255 - lum) * 1.7, 0, 255).astype(np.uint8)
    out = np.zeros((*lum.shape, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 95, 125, 99
    out[..., 3] = alpha
    img = Image.fromarray(out, "RGBA")
    bb = img.split()[3].getbbox()
    return img.crop(bb) if bb else img


def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))
    c = canvas.Canvas(PDF, pagesize=(W, H))
    cx = W/2
    def Y(off): return H - off

    def wrap(text, font, size, maxw):
        words = text.split(); lines = []; cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if c.stringWidth(t, font, size) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def block(text, off, font, size, color, leading, maxw):
        """Draw centred, wrapped text starting at baseline `off`. Returns baseline after last line."""
        c.setFont(font, size); c.setFillColor(color)
        y = off
        for ln in wrap(text, font, size, maxw):
            c.drawCentredString(cx, Y(y), ln); y += leading
        return y - leading

    # double sage border
    c.setStrokeColor(SAGES); c.setLineWidth(1.3); c.rect(15, 15, W-30, H-30)
    c.setStrokeColor(colors.Color(228/255,231/255,224/255)); c.setLineWidth(0.6); c.rect(18.5, 18.5, W-37, H-37)

    # A·R logo (sage), centred near the top
    logo = sage_logo(); tmp = os.path.join(HERE, "_coupon_logo.png"); logo.save(tmp)
    lw = 128; lh = lw*logo.height/logo.width
    top = 56
    c.drawImage(ImageReader(tmp), cx-lw/2, H-(top+lh), width=lw, height=lh, mask="auto")
    os.remove(tmp)

    maxw = W - 58
    # quote (italic) + attribution
    yq = block(QUOTE, top+lh+30, "PlexIt", 11.5, INK, 15.5, maxw)
    block(ATTRIB, yq+20, "PlexIt", 8.5, MUTED, 12, maxw)

    # thin sage divider
    yr = yq + 42; c.setStrokeColor(SAGES); c.setLineWidth(1)
    c.line(cx-26, Y(yr), cx-8, Y(yr)); c.line(cx+8, Y(yr), cx+26, Y(yr))

    # the message
    ym = block(BODY, yr+26, "Plex", 10.5, INK, 15.5, maxw)

    # logistics (italic, sage)
    block(FOOT, ym+30, "PlexIt", 9, SAGE, 13, maxw)

    c.showPage(); c.save()
    fitz.open(PDF)[0].get_pixmap(dpi=300).save(PNG)
    print("wrote", PDF, "+", PNG)


if __name__ == "__main__":
    build()
