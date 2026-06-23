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
# Recto footer — discreet one-line gift/bank note (kept minimal)
BANK_LINE = "Cadeaux  ·  Liban (USD) IBAN ‹ à compléter ›   ·   International (EUR) IBAN ‹ à compléter ›"
# Verso — programme of the day (the beautiful back)
PROG_TITLE = "LE DÉROULÉ DE LA JOURNÉE"
PROGRAMME = [("16 h 45", "Cérémonie religieuse"), ("18 h 30", "Cocktail"),
             ("20 h 00", "Dîner"), ("02 h 00", "Fin de la soirée")]
RSVP_TITLE = "CONFIRMER VOTRE PRÉSENCE"
RSVP_LINE = "Auprès des mariés ou de leurs parents — ou en ligne :"
RSVP_DEADLINE = "Réponse souhaitée avant le 31 juillet 2026"
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
    # Parents on either side of the card
    center(PARENTS[0], cx-128, 56, "Plex", 11.5, INK)
    center(PARENTS[1], cx+128, 56, "Plex", 11.5, INK)
    center(INVITE, cx, 88, "PlexIt", 10.5, MUTED)

    a, amp, r = NAMES; fs = 30
    c.setFont("Plex", fs)
    wa, wamp, wr = (c.stringWidth(s, "Plex", fs) for s in (a, amp, r))
    x = cx - (wa+wamp+wr)/2; yb = Y(124)
    c.setFillColor(INK); c.drawString(x, yb, a)
    c.setFillColor(SAGE); c.drawString(x+wa, yb, amp)
    c.setFillColor(INK); c.drawString(x+wa+wamp, yb, r)

    dw = spaced(DATE, cx, 150, "Plex", 11, 2.2, INK); rules(cx, 147, dw/2)

    img = Image.open(ILLUS).convert("RGB")
    iw = 126; ih = iw*img.height/img.width
    c.drawImage(ImageReader(img), cx-iw/2, H-(164+ih), width=iw, height=ih)

    def vblock(role, venue, addr, cxc, top):
        spaced(role, cxc, top, "Plex", 8, 2.2, SAGE)
        center(venue, cxc, top+13, "Plex", 10, INK)
        center(addr, cxc, top+24, "Plex", 7.8, MUTED)
    vy = 164 + ih + 16
    vblock(*CEREMONY, cx-118, vy)
    vblock(*RECEPTION, cx+118, vy)

    # discreet one-line gift/bank footer
    fy = Y(312); c.setStrokeColor(LINE2); c.setLineWidth(0.8); c.line(cx-66, fy, cx+66, fy)
    center(BANK_LINE, cx, 324, "Plex", 6.6, MUTED)
    c.showPage()

    # ===================== VERSO — programme + RSVP (the beautiful back) =====================
    border()
    spaced(PROG_TITLE, cx, 62, "Plex", 10, 3.2, SAGE)
    oy = Y(82); c.setStrokeColor(SAGES); c.setLineWidth(1)
    c.line(cx-26, oy, cx-6, oy); c.line(cx+6, oy, cx+26, oy)
    c.setFillColor(SAGE); c.circle(cx, oy, 1.3, fill=1, stroke=0)

    def prow(t, label, off):
        y = Y(off); gap = 15
        c.setFont("Plex", 14); c.setFillColor(SAGE); c.drawRightString(cx-gap, y, t)
        c.setFillColor(SAGES); c.circle(cx, y+4, 1.2, fill=1, stroke=0)
        c.setFont("Plex", 12.5); c.setFillColor(INK); c.drawString(cx+gap, y, label)
    py = 114
    for t, label in PROGRAMME:
        prow(t, label, py); py += 30

    # RSVP — confirm with the couple, the parents, or online (QR)
    spaced(RSVP_TITLE, cx, 240, "Plex", 8.5, 2.6, SAGE)
    center(RSVP_LINE, cx, 254, "Plex", 8.6, INK)
    qw = qr.QrCodeWidget(SITE); qw.barFillColor = INK
    b = qw.getBounds(); bw, bh = b[2]-b[0], b[3]-b[1]; qs = 34
    dwg = Drawing(qs, qs, transform=[qs/bw, 0, 0, qs/bh, 0, 0]); dwg.add(qw)
    renderPDF.draw(dwg, c, cx-qs/2, H-(264+qs))
    center(RSVP_DEADLINE, cx, 312, "PlexIt", 7.6, MUTED)
    c.showPage()

    c.save()
    doc = fitz.open(PDF)
    doc[0].get_pixmap(dpi=200).save(PNG_R)
    doc[1].get_pixmap(dpi=200).save(PNG_V)
    doc.close()
    print("wrote", PDF, "+ recto/verso previews")

if __name__ == "__main__":
    build()
