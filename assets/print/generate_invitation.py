#!/usr/bin/env python3
"""Generate the printable wedding invitation (A5, 300 DPI) → invitation.png + invitation.pdf.

Reuses the website's identity: Instrument Serif names, sage-green accent, the hotel
illustration, the thin-rule date motif, and a QR code to the site.
Content mirrors .claude/memory/wedding-details.md — update both together.

Run from the repo root:  python3 assets/print/generate_invitation.py
Requires: Pillow, qrcode  (pip install Pillow qrcode)
Fonts: bundled with the canvas-design skill; fall back to any serif if absent.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FDIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"
INSTR    = FDIR + "InstrumentSerif-Regular.ttf"
INSTR_IT = FDIR + "InstrumentSerif-Italic.ttf"
PLEX     = FDIR + "IBMPlexSerif-Regular.ttf"

# --- content (keep in sync with wedding-details.md) ---
NAMES   = ("André ", "&", " Rhéa")
EYEBROW = "NOUS NOUS MARIONS"
DATE    = "SAMEDI 22 AOÛT 2026"
CEREMONY = ("CÉRÉMONIE", "16 h 45  —  Église Notre-Dame de l'Annonciation", "Achrafieh, Beyrouth")
RECEPTION = ("RÉCEPTION", "18 h 30  —  Hôtel Al Bustan", "Beit Mery, Mont-Liban")
RSVP    = "Réponse souhaitée avant le 31 juillet 2026"
SITE    = "https://andregeha.github.io/wedding-website/"
QR_CAPTION = "INFOS & CONFIRMATION EN LIGNE"

INK=(43,43,41); SAGE=(95,125,99); SAGES=(174,191,163); MUTED=(97,92,86); WHITE=(255,255,255)
W, H = 1748, 2480  # A5 @ 300 DPI

def F(p, s): return ImageFont.truetype(p, s)

def build():
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im); cx = W / 2
    d.rectangle([92, 92, W-92, H-92], outline=SAGES, width=3)
    d.rectangle([108, 108, W-108, H-108], outline=(230, 233, 226), width=1)

    def spaced(t, cx, baseline, f, fill, sp):
        ws = [d.textlength(ch, font=f) for ch in t]; total = sum(ws) + sp*(len(t)-1); x = cx - total/2
        for ch, w in zip(t, ws):
            d.text((x, baseline), ch, font=f, fill=fill, anchor="ls"); x += w + sp
        return total

    def center(t, cx, baseline, f, fill):
        d.text((cx, baseline), t, font=f, fill=fill, anchor="ms")

    spaced(EYEBROW, cx, 300, F(PLEX, 40), MUTED, 16)

    fn = F(INSTR, 176)
    a, amp, r = NAMES
    wa, wamp, wr = (d.textlength(s, font=fn) for s in (a, amp, r))
    x = cx - (wa+wamp+wr)/2; bl = 520
    d.text((x, bl), a, font=fn, fill=INK, anchor="ls"); x += wa
    d.text((x, bl), amp, font=fn, fill=SAGE, anchor="ls"); x += wamp
    d.text((x, bl), r, font=fn, fill=INK, anchor="ls")

    fd = F(PLEX, 46); bld = 650
    dw = spaced(DATE, cx, bld, fd, INK, 9)
    ry = bld - 15; gap = dw/2 + 50
    d.line([(cx-gap-90, ry), (cx-gap, ry)], fill=SAGES, width=2)
    d.line([(cx+gap, ry), (cx+gap+90, ry)], fill=SAGES, width=2)

    ill = Image.open(os.path.join(ROOT, "assets/img/hotel.png")).convert("RGBA")
    tw = 860; th = int(tw * ill.height / ill.width); ill = ill.resize((tw, th), Image.LANCZOS)
    iy = 740; im.paste(ill, (int(cx-tw/2), iy), ill)

    oy = iy + th + 70
    d.line([(cx-55, oy), (cx+55, oy)], fill=SAGES, width=2)
    d.ellipse([cx-4, oy-4, cx+4, oy+4], fill=SAGE)

    def block(role, line, addr, y):
        spaced(role, cx, y, F(PLEX, 32), SAGE, 12)
        center(line, cx, y+62, F(INSTR, 52), INK)
        center(addr, cx, y+112, F(PLEX, 34), MUTED)

    block(*CEREMONY, oy+150)
    block(*RECEPTION, oy+360)
    center(RSVP, cx, oy+560, F(INSTR_IT, 44), MUTED)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(SITE); qr.make(fit=True)
    qimg = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
    qs = 210; qimg = qimg.resize((qs, qs), Image.NEAREST); qy = oy + 640
    im.paste(qimg, (int(cx-qs/2), qy))
    spaced(QR_CAPTION, cx, qy+qs+50, F(PLEX, 28), MUTED, 8)

    png = os.path.join(HERE, "invitation.png"); pdf = os.path.join(HERE, "invitation.pdf")
    im.save(png); im.save(pdf, "PDF", resolution=300.0)
    print("wrote", png, "and", pdf)

if __name__ == "__main__":
    build()
