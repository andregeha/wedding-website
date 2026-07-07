#!/usr/bin/env python3
"""Envelope seal sticker — round, Ø 25 mm, to cover the brand mark inside the envelope.

Wax-seal aesthetic in the wedding palette: a solid **sage** disc (edge is NEVER white —
the envelope isn't white) with the couple's hand-drawn logo (A. · floral · R.) recoloured
to **ivory**, tone-on-tone, inside a fine ivory double ring.

Outputs (into assets/print/):
  sticker.pdf  — print file, 29×29 mm artboard = Ø25 mm sticker + 2 mm bleed all around,
                 vector; the sage fills past the cut line so no white shows at the edge.
  sticker.png  — round preview (die-cut result) on a light backdrop.

Run from repo root:  python3 assets/print/generate_sticker.py
Requires: reportlab, pymupdf, Pillow, numpy
"""
import os
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image
import fitz

HERE = os.path.dirname(__file__)
LOGO = os.path.join(HERE, "logo-source.png")
PDF  = os.path.join(HERE, "sticker.pdf")
PNG  = os.path.join(HERE, "sticker.png")

SAGE  = colors.Color(95/255, 125/255, 99/255)     # #5f7d63 — seal colour (matches the site)
IVORY = colors.Color(244/255, 241/255, 233/255)   # #f4f1e9 — emblem / ring, tone-on-tone
IVORY_RGB = (244, 241, 233)

DIAM   = 25*mm          # finished sticker diameter
BLEED  = 2*mm           # extra colour past the cut line
PAGE   = DIAM + 2*BLEED # square artboard
R_CUT  = DIAM/2
R_FILL = R_CUT + BLEED


def ivory_logo():
    """Recolour the blue line-art logo to ivory with alpha from darkness; trim to content."""
    im = Image.open(LOGO).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    alpha = np.clip((236 - lum) * 2.4, 0, 255).astype(np.uint8)   # darker ink -> more opaque
    out = np.zeros((*lum.shape, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = IVORY_RGB
    out[..., 3] = alpha
    img = Image.fromarray(out, "RGBA")
    bb = img.split()[3].getbbox()          # trim to the visible artwork
    return img.crop(bb) if bb else img


def build():
    c = canvas.Canvas(PDF, pagesize=(PAGE, PAGE))
    cx = cy = PAGE/2

    # sage disc, filled past the cut line (bleed) so the edge is never white
    c.setFillColor(SAGE); c.circle(cx, cy, R_FILL, fill=1, stroke=0)

    # fine ivory double ring — the "seal" border
    c.setStrokeColor(IVORY)
    c.setLineWidth(0.9); c.circle(cx, cy, R_CUT - 1.5*mm, fill=0, stroke=1)
    c.setLineWidth(0.5); c.circle(cx, cy, R_CUT - 2.3*mm, fill=0, stroke=1)

    # the logo, recoloured ivory, centred inside the ring
    logo = ivory_logo()
    tmp = os.path.join(HERE, "_sticker_logo.png"); logo.save(tmp)
    target_h = 17*mm; target_w = target_h * logo.width/logo.height
    c.drawImage(ImageReader(tmp), cx-target_w/2, cy-target_h/2,
                width=target_w, height=target_h, mask="auto")
    c.showPage(); c.save()
    os.remove(tmp)

    # --- round preview (die-cut result) on a light backdrop ---
    pg = fitz.open(PDF)[0]
    pm = pg.get_pixmap(dpi=600, alpha=True)
    seal = Image.frombytes("RGBA", (pm.width, pm.height), pm.samples)
    # crop to the cut circle and mask to a clean round sticker
    cutpx = int(DIAM/PAGE * pm.width); off = (pm.width - cutpx)//2
    seal = seal.crop((off, off, off+cutpx, off+cutpx))
    mask = Image.new("L", (cutpx, cutpx), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0, 0, cutpx-1, cutpx-1), fill=255)
    pad = int(cutpx*0.12)
    bg = Image.new("RGB", (cutpx+2*pad, cutpx+2*pad), (238, 236, 231))
    bg.paste(seal.convert("RGB"), (pad, pad), mask)
    bg.save(PNG)
    print("wrote", PDF, "+", PNG)


if __name__ == "__main__":
    build()
