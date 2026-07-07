#!/usr/bin/env python3
"""Envelope seal stickers — round, Ø 25 mm, to cover the brand mark inside the envelope.

Wax-seal aesthetic using the couple's hand-drawn logo (A. · floral · R.), in the wedding's
own colours (edge is NEVER white — the envelope isn't white). Two versions:

  sticker-blue.pdf/.png   — disc in the logo's ink blue (#5359a4), emblem + ring IVORY.
  sticker-green.pdf/.png  — disc in the illustration's light tree green (#c2d8af),
                            emblem + ring in a deep green (tone-on-tone, for contrast).

Each: 29×29 mm artboard = Ø25 mm sticker + 2 mm bleed; the disc colour fills past the cut
line so no white shows. The logo is scaled by a bounding-circle (diagonal) fit so the A and R
never touch the ring. PNG = round die-cut preview.

Run from repo root:  python3 assets/print/generate_sticker.py
Requires: reportlab, pymupdf, Pillow, numpy
"""
import os, math
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import fitz

HERE = os.path.dirname(__file__)
LOGO = os.path.join(HERE, "logo-source.png")

IVORY      = (244, 241, 233)   # #f4f1e9
BLUE       = (83, 89, 164)     # #5359a4 — logo ink
LIGHTGREEN = (194, 216, 175)   # #c2d8af — tree foliage in the illustration
DEEPGREEN  = (70, 96, 63)      # #46603f — deep green, reads on the light-green disc

# version: (disc rgb, emblem/ring rgb, out basename)
VERSIONS = [
    (BLUE,       IVORY,     "sticker-blue"),
    (LIGHTGREEN, DEEPGREEN, "sticker-green"),
]

DIAM   = 25*mm
BLEED  = 2*mm
PAGE   = DIAM + 2*BLEED
R_CUT  = DIAM/2
R_FILL = R_CUT + BLEED


def recolored_logo(rgb):
    """Recolour the blue line-art logo to `rgb` with alpha from darkness; trim to content."""
    im = Image.open(LOGO).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    alpha = np.clip((236 - lum) * 2.4, 0, 255).astype(np.uint8)
    out = np.zeros((*lum.shape, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = alpha
    img = Image.fromarray(out, "RGBA")
    bb = img.split()[3].getbbox()
    return img.crop(bb) if bb else img


def make(disc, emblem, base):
    pdf = os.path.join(HERE, base + ".pdf")
    png = os.path.join(HERE, base + ".png")
    c = canvas.Canvas(pdf, pagesize=(PAGE, PAGE))
    cx = cy = PAGE/2
    disc_c = colors.Color(*[v/255 for v in disc])
    em_c   = colors.Color(*[v/255 for v in emblem])

    # coloured disc, filled past the cut line (bleed) so the edge is never white
    c.setFillColor(disc_c); c.circle(cx, cy, R_FILL, fill=1, stroke=0)

    # fine double ring — the "seal" border
    c.setStrokeColor(em_c)
    c.setLineWidth(0.9); c.circle(cx, cy, R_CUT - 1.5*mm, fill=0, stroke=1)
    c.setLineWidth(0.5); c.circle(cx, cy, R_CUT - 2.3*mm, fill=0, stroke=1)

    # logo, recoloured, scaled by diagonal so its bbox circle clears the inner ring
    logo = recolored_logo(emblem)
    tmp = os.path.join(HERE, "_sticker_logo.png"); logo.save(tmp)
    R_content = R_CUT - 3.4*mm                         # keep A / R off the ring
    rho = logo.width/logo.height
    th = 2*R_content/math.sqrt(rho*rho + 1); tw = th*rho
    c.drawImage(ImageReader(tmp), cx-tw/2, cy-th/2, width=tw, height=th, mask="auto")
    c.showPage(); c.save()
    os.remove(tmp)

    # round die-cut preview on a light backdrop
    pm = fitz.open(pdf)[0].get_pixmap(dpi=600, alpha=True)
    seal = Image.frombytes("RGBA", (pm.width, pm.height), pm.samples)
    cutpx = int(DIAM/PAGE * pm.width); off = (pm.width - cutpx)//2
    seal = seal.crop((off, off, off+cutpx, off+cutpx))
    mask = Image.new("L", (cutpx, cutpx), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, cutpx-1, cutpx-1), fill=255)
    pad = int(cutpx*0.12)
    bg = Image.new("RGB", (cutpx+2*pad, cutpx+2*pad), (238, 236, 231))
    bg.paste(seal.convert("RGB"), (pad, pad), mask)
    bg.save(png)
    print("wrote", pdf, "+", png)


def build():
    for disc, emblem, base in VERSIONS:
        make(disc, emblem, base)


if __name__ == "__main__":
    build()
