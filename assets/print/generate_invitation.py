#!/usr/bin/env python3
"""Generate the printable wedding invitation (faire-part), A5.

Produces a TRUE VECTOR PDF (crisp text + QR at any zoom/print size) via reportlab,
with the hand-drawn hotel illustration embedded at high resolution. Also renders a
PNG preview from the same PDF (via PyMuPDF) so the preview always matches the print file.

Reuses the website identity: Instrument Serif names with a sage « & », thin-rule date
motif, the hotel illustration, sage-green accent, and a QR code to the site.
Content mirrors .claude/memory/wedding-details.md — keep them in sync.

Run from the repo root:  python3 assets/print/generate_invitation.py
Requires: reportlab, pymupdf, Pillow  (pip install reportlab pymupdf Pillow)
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from PIL import Image
import fitz  # PyMuPDF

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
PLEX, PLEX_IT = FDIR+"IBMPlexSerif-Regular.ttf", FDIR+"IBMPlexSerif-Italic.ttf"

# --- content (keep in sync with wedding-details.md) ---
EYEBROW = "NOUS NOUS MARIONS"
NAMES   = ("André ", "&", " Rhéa")
DATE    = "SAMEDI 22 AOÛT 2026"
CEREMONY = ("CÉRÉMONIE · 16 h 45", "Église Notre-Dame de l'Annonciation", "Achrafieh, Beyrouth")
RECEPTION = ("RÉCEPTION · 18 h 30", "Hôtel Al Bustan", "Beit Mery, Mont-Liban")
RSVP    = "Réponse souhaitée avant le 31 juillet 2026"
SITE    = "https://andregeha.github.io/wedding-website/"
QR_CAPTION = "INFOS & CONFIRMATION EN LIGNE"
ILLUS  = os.path.join(HERE, "hotel-source.png")  # original full-res, lossless (2000px)
PDF    = os.path.join(HERE, "invitation.pdf")
PNG    = os.path.join(HERE, "invitation.png")

INK   = colors.Color(43/255, 43/255, 41/255)
SAGE  = colors.Color(95/255, 125/255, 99/255)
SAGES = colors.Color(174/255, 191/255, 163/255)
MUTED = colors.Color(97/255, 92/255, 86/255)
LINE2 = colors.Color(228/255, 231/255, 224/255)

def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))
    W, H = A5
    c = canvas.Canvas(PDF, pagesize=A5)
    cx = W / 2
    def Y(off): return H - off

    # delicate double border
    c.setLineJoin(1)
    c.setStrokeColor(SAGES); c.setLineWidth(1.6); c.rect(22, 22, W-44, H-44)
    c.setStrokeColor(LINE2); c.setLineWidth(0.7); c.rect(26.5, 26.5, W-53, H-53)

    def spaced(text, off, font, size, tracking, color):
        c.setFont(font, size); c.setFillColor(color)
        widths = [c.stringWidth(ch, font, size) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total/2; y = Y(off)
        for ch, w in zip(text, widths):
            c.drawString(x, y, ch); x += w + tracking
        return total

    def center(text, off, font, size, color):
        c.setFont(font, size); c.setFillColor(color); c.drawCentredString(cx, Y(off), text)

    spaced(EYEBROW, 72, "Plex", 9.6, 3.8, MUTED)

    # Names, sage ampersand (same family as the rest)
    a, amp, r = NAMES; fs = 36
    c.setFont("Plex", fs)
    wa, wamp, wr = (c.stringWidth(s, "Plex", fs) for s in (a, amp, r))
    x = cx - (wa + wamp + wr) / 2; yb = Y(124)
    c.setFillColor(INK); c.drawString(x, yb, a)
    c.setFillColor(SAGE); c.drawString(x + wa, yb, amp)
    c.setFillColor(INK); c.drawString(x + wa + wamp, yb, r)

    # Date + side rules
    dw = spaced(DATE, 156, "Plex", 11, 2.2, INK)
    ry = Y(156) + 3.2; gap = dw/2 + 9
    c.setStrokeColor(SAGES); c.setLineWidth(1)
    c.line(cx-gap-24, ry, cx-gap-5, ry); c.line(cx+gap+5, ry, cx+gap+24, ry)

    # Illustration
    img = Image.open(ILLUS).convert("RGB")
    top_illus = 170; iw = 205; ih = iw * img.height / img.width
    c.drawImage(ImageReader(img), cx - iw/2, H - (top_illus + ih), width=iw, height=ih)

    # Ornament
    orn = top_illus + ih + 22
    oy = Y(orn); c.setStrokeColor(SAGES); c.setLineWidth(1)
    c.line(cx-14, oy, cx+14, oy); c.setFillColor(SAGE); c.circle(cx, oy, 1.2, fill=1, stroke=0)

    def block(role, venue, addr, top):
        spaced(role, top, "Plex", 8, 2.4, SAGE)
        center(venue, top + 14, "Plex", 11, INK)
        center(addr, top + 26, "Plex", 8.4, MUTED)

    cer_role = orn + 36
    block(*CEREMONY, cer_role)
    block(*RECEPTION, cer_role + 50)
    center(RSVP, cer_role + 99, "PlexIt", 10.5, MUTED)

    # Vector QR + caption
    qw = qr.QrCodeWidget(SITE); qw.barFillColor = INK
    b = qw.getBounds(); bw, bh = b[2]-b[0], b[3]-b[1]; qs = 50
    qr_top = cer_role + 119
    dwg = Drawing(qs, qs, transform=[qs/bw, 0, 0, qs/bh, 0, 0]); dwg.add(qw)
    renderPDF.draw(dwg, c, cx - qs/2, H - (qr_top + qs))
    spaced(QR_CAPTION, qr_top + qs + 12, "Plex", 6.7, 1.9, MUTED)

    c.showPage(); c.save()

    # PNG preview from the same PDF (keeps preview == print)
    doc = fitz.open(PDF); doc[0].get_pixmap(dpi=200).save(PNG); doc.close()
    print("wrote", PDF, "and", PNG)

if __name__ == "__main__":
    build()
