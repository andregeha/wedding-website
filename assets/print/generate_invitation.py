#!/usr/bin/env python3
"""Printable wedding invitation (faire-part) — official landscape card, single page.

Format: 178 × 127 mm landscape (7×5", standard wedding-invitation size).
One page: the complete invitation — parents, names, date, the illustration,
          cérémonie/réception, the two gift accounts, and a QR to the site.

True VECTOR PDF (crisp text + QR) via reportlab; illustration embedded at full resolution.
A PNG preview is rendered from the same PDF via PyMuPDF (preview == print).
Single typeface throughout: IBM Plex Serif (regular + italic).

Run from repo root:  python3 assets/print/generate_invitation.py
Requires: reportlab, pymupdf, Pillow
Content mirrors .claude/memory/wedding-details.md — keep in sync.
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from PIL import Image
import numpy as np
import fitz


def visible_bbox(im, thr=20, dens=0.02, pad=8):
    """Bounding box of the *visible* artwork (ignores faint near-white margins).

    A row/column counts as content only if >`dens` of its pixels differ from
    white by more than `thr` — so the large faint lawn fade at the bottom of the
    illustration is treated as background, and the crop centres the real drawing.
    """
    a = np.asarray(im.convert("RGB")).astype(int)
    d = (255 - a).max(axis=2)
    m = d > thr
    rows = np.where(m.mean(axis=1) > dens)[0]
    cols = np.where(m.mean(axis=0) > dens)[0]
    if not len(rows) or not len(cols):
        return None
    l, t = int(cols[0]) - pad, int(rows[0]) - pad
    r, b = int(cols[-1]) + 1 + pad, int(rows[-1]) + 1 + pad
    return (max(0, l), max(0, t), min(im.width, r), min(im.height, b))

HERE = os.path.dirname(__file__)
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
PLEX, PLEX_IT = FDIR+"IBMPlexSerif-Regular.ttf", FDIR+"IBMPlexSerif-Italic.ttf"
ILLUS = os.path.join(HERE, "hotel-source.png")
PDF   = os.path.join(HERE, "invitation.pdf")
PNG_R = os.path.join(HERE, "invitation.png")        # single-page preview
PDF_B5 = os.path.join(HERE, "invitation-b5.pdf")    # B5 landscape (250×176 mm) version
PNG_B5 = os.path.join(HERE, "invitation-b5.png")
PDF_NOQR = os.path.join(HERE, "invitation-no-qr.pdf")  # 178×127 mm, same design, no QR
PNG_NOQR = os.path.join(HERE, "invitation-no-qr.png")

# --- content (keep in sync with wedding-details.md) ---
PARENTS = ("Elie & Pascale Geha", "Manhal & Najwa Nacouzi")
INVITE  = "ont la joie de vous convier au mariage de leurs enfants"
NAMES   = ("André ", "&", " Rhéa")
DATE    = "SAMEDI 22 AOÛT 2026"
CEREMONY  = ("CÉRÉMONIE · 17 h 00", "Église Notre-Dame de l'Annonciation", "Achrafieh, Beyrouth")
RECEPTION = ("RÉCEPTION · 18 h 30", "Hôtel Al Bustan", "Beit Mery, Mont-Liban")
# Recto footer — discreet gift/bank note (two accounts: Liban/USD + France/EUR)
GIFT_TITLE = "LISTE DE MARIAGE"
GIFT_LB = "Liban · USD   —   André Geha &/ou Rhéa Nacouzi   ·   BIC BLOMLBBX   ·   LB90 0014 0000 2102 6732 6609 4314"
GIFT_FR = "France · EUR   —   André Geha   ·   BIC REVOFRP2   ·   FR76 2823 3000 0144 2006 8520 030"
# Site URL encoded by the recto QR (client keeps the GitHub Pages link)
SITE = "https://andregeha.github.io/wedding-website/"

INK   = colors.Color(43/255, 43/255, 41/255)
SAGE  = colors.Color(95/255, 125/255, 99/255)
SAGES = colors.Color(174/255, 191/255, 163/255)
MUTED = colors.Color(97/255, 92/255, 86/255)
LINE2 = colors.Color(228/255, 231/255, 224/255)
W, H = 178*mm, 127*mm

def render_card(path, png, qr_on=True):
    """Draw the single-page 178×127 card. qr_on toggles the QR next to the RSVP line."""
    c = canvas.Canvas(path, pagesize=(W, H))
    cx = W/2
    def Y(off): return H - off

    def border():
        c.setStrokeColor(SAGES); c.setLineWidth(1.5); c.rect(20, 20, W-40, H-40)
        c.setStrokeColor(LINE2); c.setLineWidth(0.7); c.rect(24, 24, W-48, H-48)

    def spaced(text, cxc, off, font, size, tracking, color):
        c.setFont(font, size); c.setFillColor(color)
        ws = [c.stringWidth(ch, font, size) for ch in text]
        total = sum(ws) + tracking*(len(text)-1); x = cxc - total/2; y = Y(off)
        for ch, w in zip(text, ws):
            c.drawString(x, y, ch); x += w + tracking
        return total

    def center(text, cxc, off, font, size, color):
        c.setFont(font, size); c.setFillColor(color); c.drawCentredString(cxc, Y(off), text)

    def rules(cxc, off, half, color=SAGES):
        y = Y(off); c.setStrokeColor(color); c.setLineWidth(1)
        c.line(cxc-half-20, y, cxc-half-5, y); c.line(cxc+half+5, y, cxc+half+20, y)

    # Crop the illustration to its visible artwork (drops the faint lawn/white margins,
    # esp. at the bottom) so it can be placed tight and centred.
    img = Image.open(ILLUS).convert("RGB")
    vb = visible_bbox(img); art = img.crop(vb) if vb else img

    border()
    # Parents on either side of the card
    center(PARENTS[0], cx-128, 58, "Plex", 11, INK)
    center(PARENTS[1], cx+128, 58, "Plex", 11, INK)
    center(INVITE, cx, 84, "PlexIt", 9.5, MUTED)

    # Names, with a smaller ampersand sitting on the SAME baseline as the names
    a, amp, r = NAMES[0].strip(), NAMES[1], NAMES[2].strip()
    fs = 24; ampfs = 15; pad = 9
    wa = c.stringWidth(a, "Plex", fs); wr = c.stringWidth(r, "Plex", fs)
    wamp = c.stringWidth(amp, "Plex", ampfs)
    total = wa + pad + wamp + pad + wr; x = cx - total/2; yb = Y(120)
    c.setFont("Plex", fs); c.setFillColor(INK); c.drawString(x, yb, a)
    c.setFont("Plex", ampfs); c.setFillColor(SAGE); c.drawString(x+wa+pad, yb, amp)
    c.setFont("Plex", fs); c.setFillColor(INK); c.drawString(x+wa+pad+wamp+pad, yb, r)

    dw = spaced(DATE, cx, 146, "Plex", 9.5, 2.0, INK); rules(cx, 143, dw/2)

    # the hand-drawn illustration (cropped tight), lowered to give the top half air
    iw = 122; ih = iw*art.height/art.width
    c.drawImage(ImageReader(art), cx-iw/2, H-(158+ih), width=iw, height=ih)

    # ceremony / reception two columns
    def vblock(role, venue, addr, cxc, top):
        spaced(role, cxc, top, "Plex", 7.5, 2.0, SAGE)
        center(venue, cxc, top+12, "Plex", 9.2, INK)
        center(addr, cxc, top+22, "Plex", 7.2, MUTED)
    vy = 158 + ih + 13
    vblock(*CEREMONY, cx-118, vy)
    vblock(*RECEPTION, cx+118, vy)

    # RSVP — one compact line (with the QR beside it when qr_on), above the gift block
    rsvp = "Réponse souhaitée avant le 21 juillet 2026 — auprès des mariés, de leurs parents, ou en ligne"
    ry_top = vy + 22 + 11
    if qr_on:
        qw = qr.QrCodeWidget(SITE); qw.barFillColor = INK
        b = qw.getBounds(); bw, bh = b[2]-b[0], b[3]-b[1]; qs = 26
        c.setFont("PlexIt", 6.2); rw = c.stringWidth(rsvp, "PlexIt", 6.2)
        gap = 9; gx = cx - (rw + gap + qs)/2
        c.setFillColor(MUTED); c.drawString(gx, Y(ry_top + qs/2 + 2.2), rsvp)
        dwg = Drawing(qs, qs, transform=[qs/bw, 0, 0, qs/bh, 0, 0]); dwg.add(qw)
        renderPDF.draw(dwg, c, gx + rw + gap, H-(ry_top+qs))
        gy = ry_top + qs + 13
    else:
        center(rsvp, cx, ry_top + 15, "PlexIt", 6.2, MUTED)
        gy = ry_top + 39

    # discreet gift footer — small title, one compact line per account
    c.setStrokeColor(LINE2); c.setLineWidth(0.7); c.line(cx-84, Y(gy), cx+84, Y(gy))
    spaced(GIFT_TITLE, cx, gy+9, "Plex", 6.2, 1.6, SAGE)
    center(GIFT_LB, cx, gy+18, "Plex", 5.9, MUTED)
    center(GIFT_FR, cx, gy+26, "Plex", 5.9, MUTED)
    c.showPage(); c.save()
    fitz.open(path)[0].get_pixmap(dpi=200).save(png)
    print("wrote", path, "+ preview")


def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))

    # Version 1: 178×127 mm with QR ; Version 3: same, without QR
    render_card(PDF, PNG_R, qr_on=True)
    render_card(PDF_NOQR, PNG_NOQR, qr_on=False)

    # Version 2: B5 landscape (250 × 176 mm) — the with-QR design scaled to fill a B5
    # sheet (aspect 1.42 ≈ the card's 1.40), vector-preserved so text + QR stay crisp.
    B5W, B5H = 250*mm, 176*mm
    src = fitz.open(PDF); out = fitz.open()
    page = out.new_page(width=B5W, height=B5H)
    s = min(B5W/W, B5H/H); tw, th = W*s, H*s
    x0, y0 = (B5W-tw)/2, (B5H-th)/2
    page.show_pdf_page(fitz.Rect(x0, y0, x0+tw, y0+th), src, 0)
    out.save(PDF_B5)
    fitz.open(PDF_B5)[0].get_pixmap(dpi=200).save(PNG_B5)
    src.close(); out.close()
    print("wrote", PDF_B5, "+ preview")

if __name__ == "__main__":
    build()
