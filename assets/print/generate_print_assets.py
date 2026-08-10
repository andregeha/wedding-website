#!/usr/bin/env python3
"""Standalone print assets (both meant for printing):

  logo-black.png / .pdf   — the A·R logo recoloured from blue to BLACK, tight-cropped,
                            transparent background, at the source resolution.
  drawing-cropped.pdf     — the colour garden/hotel drawing (drawing-source.pdf) with the
                            white margins cropped on all four sides, native resolution kept
                            (the PDF cropbox is set to the content box — lossless).
  drawing-cropped.png     — 300-DPI preview of the cropped drawing.

Run from repo root:  python3 assets/print/generate_print_assets.py
Requires: pymupdf, Pillow, numpy, reportlab
"""
import os
import numpy as np
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(__file__)
LOGO_SRC = os.path.join(HERE, "logo-source.png")
DRAW_SRC = os.path.join(HERE, "drawing-source.pdf")


def content_bbox(dark, thr, dens):
    """bbox (l,t,r,b) of rows/cols whose share of pixels darker-than-white > thr exceeds dens."""
    m = dark > thr
    rows = np.where(m.mean(1) > dens)[0]
    cols = np.where(m.mean(0) > dens)[0]
    if not len(rows) or not len(cols):
        return None
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def make_logo_black():
    im = Image.open(LOGO_SRC).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    alpha = np.clip((255 - lum) * 1.7, 0, 255).astype(np.uint8)   # ink -> opaque black
    out = np.zeros((*lum.shape, 4), np.uint8)          # RGB stays 0,0,0 = black
    out[..., 3] = alpha
    img = Image.fromarray(out, "RGBA")                  # keep the full original frame (uncropped)
    png = os.path.join(HERE, "logo-black.png"); img.save(png)
    # PDF at the image's native size (1 px = 1 pt), transparent background
    pdf = os.path.join(HERE, "logo-black.pdf")
    c = canvas.Canvas(pdf, pagesize=(img.width, img.height))
    c.drawImage(ImageReader(png), 0, 0, width=img.width, height=img.height, mask="auto")
    c.showPage(); c.save()
    print("wrote", png, "+", pdf, f"({img.width}x{img.height})")


def make_drawing_cropped():
    d = fitz.open(DRAW_SRC); p = d[0]
    dpi = 200; s = 72.0 / dpi
    pm = p.get_pixmap(dpi=dpi)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[:, :, :3].astype(int)
    dark = (255 - a).max(2)
    bb = content_bbox(dark, thr=40, dens=0.004)
    l, t, r, b = bb
    pad = 3                                             # a few px so anti-aliased edges aren't clipped
    l, t = max(0, l - pad), max(0, t - pad)
    r, b = min(pm.width, r + pad), min(pm.height, b + pad)
    rect = fitz.Rect(l * s, t * s, r * s, b * s) & p.rect
    p.set_cropbox(rect)
    out_pdf = os.path.join(HERE, "drawing-cropped.pdf"); d.save(out_pdf)
    # 300-DPI preview of the cropped page
    out_png = os.path.join(HERE, "drawing-cropped.png")
    fitz.open(out_pdf)[0].get_pixmap(dpi=300).save(out_png)
    print("wrote", out_pdf, "+", out_png, f"(crop {rect.width:.0f}x{rect.height:.0f} pt)")


if __name__ == "__main__":
    make_logo_black()
    make_drawing_cropped()
