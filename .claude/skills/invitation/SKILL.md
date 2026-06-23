---
name: invitation
description: Generate or update the printable wedding invitation (faire-part) — an A5 300-DPI PNG + PDF that mirrors the website's design and content. Use when asked to create/refresh the printable card, or after wedding details change (names, date, times, venues) so the card stays in sync with the site.
---

# Printable invitation (faire-part)

A print-ready **landscape 178×127 mm (7×5") card, recto/verso**, reusing the site identity.
Output is a **2-page true vector PDF** (`assets/print/invitation.pdf` — crisp text + QR) plus
PNG previews of each page (`invitation.png` = recto, `invitation-verso.png` = verso), rendered
from the same PDF. The hotel illustration is embedded full-resolution (`hotel-source.png`).

- **Recto:** invitation issued by the parents (Elie & Pascale Geha · Manhal & Najwa Nacouzi),
  names, date, illustration, and ceremony/reception in two columns.
- **Verso:** illustration, a discreet "gifts" note with **two bank accounts** (Lebanon/USD and
  abroad/EUR — Bénéficiaire/Banque/IBAN/BIC), and a QR to the site. Bank values are placeholders
  (`‹ à compléter ›`) in the `ACCT_LB` / `ACCT_INTL` constants — fill with real details on request.
- Single typeface throughout: **IBM Plex Serif** (regular + italic).

## Regenerate
```bash
pip install reportlab pymupdf Pillow   # PyPI is reachable; browser/CDN are not
python3 assets/print/generate_invitation.py
```
Then QC by viewing `assets/print/invitation.png` before publishing.

## Keep in sync
Content constants are at the top of `assets/print/generate_invitation.py` and must match
`.claude/memory/wedding-details.md` (names, date, **ceremony/reception times**, venues,
RSVP deadline). When a detail changes on the site, update the constants and re-run.

## Notes
- Built with **reportlab** (vector PDF: embeds Instrument Serif + IBM Plex Serif, draws the
  date rules and a **vector QR** via `reportlab.graphics.barcode.qr`). **PyMuPDF** rasterises
  the PDF to the PNG preview so preview == print. Illustration source: `assets/img/hotel.webp`.
- The QR encodes the live site URL; it keeps working after the custom domain is attached
  (GitHub redirects the old URL). Swap `SITE` to the custom domain once live, then regenerate.
- Palette mirrors `styles.css`: ink #2b2b29, sage #5f7d63, soft sage #aebfa3, muted #615c56.
