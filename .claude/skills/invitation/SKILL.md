---
name: invitation
description: Generate or update the printable wedding invitation (faire-part) — an A5 300-DPI PNG + PDF that mirrors the website's design and content. Use when asked to create/refresh the printable card, or after wedding details change (names, date, times, venues) so the card stays in sync with the site.
---

# Printable invitation (faire-part)

A print-ready **A5 (1748×2480 px @ 300 DPI)** card reusing the site identity: Instrument
Serif names with a sage-green « & », the thin-rule date motif, the hotel illustration, and
a QR code to the site. Output: `assets/print/invitation.png` and `invitation.pdf`.

## Regenerate
```bash
pip install Pillow qrcode    # if not present (PyPI is reachable; browser/CDN are not)
python3 assets/print/generate_invitation.py
```
Then QC by viewing `assets/print/invitation.png` before publishing.

## Keep in sync
Content is defined at the top of `assets/print/generate_invitation.py` and must match
`.claude/memory/wedding-details.md` (names, date, **ceremony/reception times**, venues,
RSVP deadline). When a detail changes on the site, update the script constants and re-run.

## Notes
- Fonts come from the canvas-design skill (`/mnt/skills/.../canvas-fonts/`): Instrument Serif
  (display/italic) + IBM Plex Serif (caps/addresses). Matches the OG share image.
- The QR encodes the live site URL; it keeps working after the custom domain is attached
  (GitHub redirects the old URL). Swap `SITE` to the custom domain once it's live for a
  cleaner target, then regenerate.
- The PDF embeds a 300-DPI raster — fine for home printing and print shops at A5.
- Palette mirrors `styles.css`: ink #2b2b29, sage #5f7d63, soft sage #aebfa3, muted #615c56.
