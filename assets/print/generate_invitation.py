#!/usr/bin/env python3
"""Printable wedding invitation (faire-part) — official landscape card, recto/verso.

Format: 178 × 127 mm landscape (7×5", standard wedding-invitation size).
Page 1 (recto): the complete invitation — parents, names, date, the illustration,
                cérémonie/réception, the two gift accounts, and a QR to the site.
Page 2 (verso): just the hotel illustration, very large.

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
CEREMONY  = ("CÉRÉMONIE · 16 h 30", "Église Notre-Dame de l'Annonciation", "Achrafieh, Beyrouth")
RECEPTION = ("RÉCEPTION · 18 h 30", "Hôtel Al Bustan", "Beit Mery, Mont-Liban")
# Recto footer — discreet gift/bank note (two accounts: Liban/USD + France/EUR)
GIFT_TITLE = "LISTE DE MARIAGE"
GIFT_LB = "Liban · USD   —   André Geha &/ou Rhéa Nacouzi   ·   BIC BLOMLBBX   ·   LB90 0014 0000 2102 6732 6609 4314"
GIFT_FR = "France · EUR   —   André Geha   ·   BIC REVOFRP2   ·   FR76 2823 3000 0144 2006 8520 030"
# Site URL encoded by the recto QR (GitHub redirects keep it valid after a custom domain)
SITE = "https://andregeha.github.io/wedding-website/"

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

    img = Image.open(ILLUS).convert("RGB")

    # ===================== RECTO — the complete invitation, incl. the illustration =====================
    border()
    # Parents on either side of the card
    center(PARENTS[0], cx-128, 50, "Plex", 11, INK)
    center(PARENTS[1], cx+128, 50, "Plex", 11, INK)
    center(INVITE, cx, 70, "PlexIt", 9.5, MUTED)

    a, amp, r = NAMES; fs = 23
    c.setFont("Plex", fs)
    wa, wamp, wr = (c.stringWidth(s, "Plex", fs) for s in (a, amp, r))
    x = cx - (wa+wamp+wr)/2; yb = Y(100)
    c.setFillColor(INK); c.drawString(x, yb, a)
    c.setFillColor(SAGE); c.drawString(x+wa, yb, amp)
    c.setFillColor(INK); c.drawString(x+wa+wamp, yb, r)

    dw = spaced(DATE, cx, 122, "Plex", 9.5, 2.0, INK); rules(cx, 119, dw/2)

    # the hand-drawn illustration, modest, between the date and the venues
    iw = 116; ih = iw*img.height/img.width
    c.drawImage(ImageReader(img), cx-iw/2, H-(132+ih), width=iw, height=ih)

    # ceremony / reception two columns
    def vblock(role, venue, addr, cxc, top):
        spaced(role, cxc, top, "Plex", 7.5, 2.0, SAGE)
        center(venue, cxc, top+12, "Plex", 9.2, INK)
        center(addr, cxc, top+22, "Plex", 7.2, MUTED)
    vy = 132 + ih + 13
    vblock(*CEREMONY, cx-118, vy)
    vblock(*RECEPTION, cx+118, vy)

    # discreet gift footer — small title, one compact line per account
    gy = vy + 22 + 16
    c.setStrokeColor(LINE2); c.setLineWidth(0.7); c.line(cx-84, Y(gy), cx+84, Y(gy))
    spaced(GIFT_TITLE, cx, gy+9, "Plex", 6.2, 1.6, SAGE)
    center(GIFT_LB, cx, gy+18, "Plex", 5.9, MUTED)
    center(GIFT_FR, cx, gy+26, "Plex", 5.9, MUTED)

    # QR + caption, inline, centered at the very bottom
    qw = qr.QrCodeWidget(SITE); qw.barFillColor = INK
    b = qw.getBounds(); bw, bh = b[2]-b[0], b[3]-b[1]; qs = 26
    cap = "Infos, programme & confirmation en ligne"
    c.setFont("PlexIt", 7); capw = c.stringWidth(cap, "PlexIt", 7)
    gap = 8; gx = cx - (capw + gap + qs)/2; qy_top = 304
    c.setFillColor(MUTED); c.drawString(gx, Y(qy_top + qs/2 + 2.5), cap)
    dwg = Drawing(qs, qs, transform=[qs/bw, 0, 0, qs/bh, 0, 0]); dwg.add(qw)
    renderPDF.draw(dwg, c, gx + capw + gap, H-(qy_top+qs))
    c.showPage()

    # ===================== VERSO — just the illustration, very large =====================
    border()
    iw = 340; ih = iw*img.height/img.width
    c.drawImage(ImageReader(img), cx-iw/2, (H-ih)/2, width=iw, height=ih)
    c.showPage()

    c.save()
    doc = fitz.open(PDF)
    doc[0].get_pixmap(dpi=200).save(PNG_R)
    doc[1].get_pixmap(dpi=200).save(PNG_V)
    doc.close()
    print("wrote", PDF, "+ recto/verso previews")

if __name__ == "__main__":
    build()
