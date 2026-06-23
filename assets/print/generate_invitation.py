#!/usr/bin/env python3
"""Printable wedding invitation (faire-part) — official landscape card, recto/verso.

Format: 178 × 127 mm landscape (7×5", standard wedding-invitation size).
Page 1 (recto): formal invitation issued by the parents.
Page 2 (verso): the hotel illustration, a discreet "gifts" note with TWO bank accounts
                (Lebanon/USD and abroad/EUR), and a QR to the site.

True VECTOR PDF (crisp text + QR) via reportlab; illustration embedded at full resolution.
A PNG preview of each page is rendered from the same PDF via PyMuPDF (preview == print).
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
import fitz

HERE = os.path.dirname(__file__)
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
PLEX, PLEX_IT = FDIR+"IBMPlexSerif-Regular.ttf", FDIR+"IBMPlexSerif-Italic.ttf"
ILLUS = os.path.join(HERE, "hotel-source.png")
PDF   = os.path.join(HERE, "invitation.pdf")
PNG_R = os.path.join(HERE, "invitation.png")        # recto preview
PNG_V = os.path.join(HERE, "invitation-verso.png")  # verso preview

# --- content (keep in sync with wedding-details.md) ---
PARENTS = ("Elie & Pascale Geha", "Manhal & Najwa Nacouzi")
INVITE  = "ont la joie de vous convier au mariage de leurs enfants"
NAMES   = ("André ", "&", " Rhéa")
DATE    = "SAMEDI 22 AOÛT 2026"
CEREMONY  = ("CÉRÉMONIE · 16 h 45", "Église Notre-Dame de l'Annonciation", "Achrafieh, Beyrouth")
RECEPTION = ("RÉCEPTION · 18 h 30", "Hôtel Al Bustan", "Beit Mery, Mont-Liban")
# Verso — gifts / bank (placeholders to complete)
GIFT_TITLE = "AVEC TOUTE NOTRE GRATITUDE"
GIFT_1 = "Votre présence est notre plus beau cadeau."
GIFT_2 = "Pour celles et ceux qui souhaitent y contribuer :"
ACCT_LB   = ("AU LIBAN · USD", [("Bénéficiaire", "‹ à compléter ›"), ("Banque", "‹ à compléter ›"),
             ("IBAN", "‹ à compléter ›"), ("BIC / SWIFT", "‹ à compléter ›")])
ACCT_INTL = ("À L'ÉTRANGER · EUR", [("Bénéficiaire", "‹ à compléter ›"), ("Banque", "‹ à compléter ›"),
             ("IBAN", "‹ à compléter ›"), ("BIC / SWIFT", "‹ à compléter ›")])
SITE = "https://andregeha.github.io/wedding-website/"
QR_CAPTION = "INFOS & CONFIRMATION EN LIGNE"

INK   = colors.Color(43/255, 43/255, 41/255)
SAGE  = colors.Color(95/255, 125/255, 99/255)
SAGES = colors.Color(174/255, 191/255, 163/255)
MUTED = colors.Color(97/255, 92/255, 86/255)
LINE2 = colors.Color(228/255, 231/255, 224/255)
W, H = 178*mm, 127*mm

def build():
    pdfmetrics.registerFont(TTFont("Plex", PLEX))
    pdfmetrics.registerFont(TTFont("PlexIt", PLEX_IT))
    c = canvas.Canvas(PDF, pagesize=(W, H))
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

    # ===================== RECTO =====================
    border()
    center(PARENTS[0], cx, 58, "Plex", 12, INK)
    center(PARENTS[1], cx, 76, "Plex", 12, INK)
    center(INVITE, cx, 100, "PlexIt", 10.5, MUTED)

    a, amp, r = NAMES; fs = 34
    c.setFont("Plex", fs)
    wa, wamp, wr = (c.stringWidth(s, "Plex", fs) for s in (a, amp, r))
    x = cx - (wa+wamp+wr)/2; yb = Y(140)
    c.setFillColor(INK); c.drawString(x, yb, a)
    c.setFillColor(SAGE); c.drawString(x+wa, yb, amp)
    c.setFillColor(INK); c.drawString(x+wa+wamp, yb, r)

    dw = spaced(DATE, cx, 166, "Plex", 11, 2.2, INK); rules(cx, 163, dw/2)

    img = Image.open(ILLUS).convert("RGB")
    iw = 132; ih = iw*img.height/img.width
    c.drawImage(ImageReader(img), cx-iw/2, H-(182+ih), width=iw, height=ih)

    def vblock(role, venue, addr, cxc, top):
        spaced(role, cxc, top, "Plex", 8, 2.2, SAGE)
        center(venue, cxc, top+13, "Plex", 10, INK)
        center(addr, cxc, top+24, "Plex", 7.8, MUTED)
    vy = 182 + ih + 22
    vblock(*CEREMONY, cx-118, vy)
    vblock(*RECEPTION, cx+118, vy)
    c.showPage()

    # ===================== VERSO =====================
    border()
    img2 = Image.open(ILLUS).convert("RGB")
    iw2 = 104; ih2 = iw2*img2.height/img2.width
    c.drawImage(ImageReader(img2), cx-iw2/2, H-(30+ih2), width=iw2, height=ih2)
    gy = 30 + ih2 + 18
    spaced(GIFT_TITLE, cx, gy, "Plex", 9, 2.6, SAGE)
    center(GIFT_1, cx, gy+18, "PlexIt", 10, INK)
    center(GIFT_2, cx, gy+33, "Plex", 8.8, MUTED)

    def account(title, fields, cxc, top):
        spaced(title, cxc, top, "Plex", 8.5, 2, SAGE)
        y = top + 16
        for label, val in fields:
            c.setFont("Plex", 6.8); c.setFillColor(MUTED); c.drawCentredString(cxc, Y(y), label.upper())
            c.setFont("Plex", 8.6); c.setFillColor(INK); c.drawCentredString(cxc, Y(y+10), val)
            y += 18
    ay = gy + 56
    account(*ACCT_LB, cx-120, ay)
    account(*ACCT_INTL, cx+120, ay)

    # QR bottom-centre + caption (centre lane, below both columns)
    spaced(QR_CAPTION, cx, 274, "Plex", 6.5, 1.8, MUTED)
    qw = qr.QrCodeWidget(SITE); qw.barFillColor = INK
    b = qw.getBounds(); bw, bh = b[2]-b[0], b[3]-b[1]; qs = 38
    dwg = Drawing(qs, qs, transform=[qs/bw, 0, 0, qs/bh, 0, 0]); dwg.add(qw)
    renderPDF.draw(dwg, c, cx-qs/2, 32)
    c.showPage()

    c.save()
    doc = fitz.open(PDF)
    doc[0].get_pixmap(dpi=200).save(PNG_R)
    doc[1].get_pixmap(dpi=200).save(PNG_V)
    doc.close()
    print("wrote", PDF, "+ recto/verso previews")

if __name__ == "__main__":
    build()
