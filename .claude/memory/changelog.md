# Changelog

Dated log of what changed each session. Newest at top.

## 2026-06-22 — Invitation upgraded to a vector PDF
- Rebuilt the faire-part as a **true vector PDF** (reportlab: embedded fonts, vector QR) for
  crisp print quality — the previous PDF was a 300-DPI raster. Illustration embedded full
  colour from `hotel.webp`. PNG preview rendered from the same PDF via PyMuPDF (preview==print).
- Fixed the over-wide line: ceremony/reception now show « role · heure » then the venue on its
  own line. Rebalanced the lower section so the QR + caption sit cleanly above the border.
- Updated the `invitation` skill (now reportlab + pymupdf).

## 2026-06-22 — Printable invitation (faire-part)
- Created a print-ready **A5 300-DPI** invitation matching the site: Instrument Serif names
  (sage « & »), thin-rule date motif, hotel illustration, QR to the site.
- Outputs `assets/print/invitation.png` + `invitation.pdf`; generator script
  `assets/print/generate_invitation.py` + new **`invitation` skill** to regenerate/keep in
  sync with `wedding-details.md` (content constants at top of the script).

## 2026-06-22 — Ceremony time corrected to 16 h 45
- Religious ceremony moved 17 h 00 → **16 h 45** everywhere: Le jour J card, Programme
  timeline, the `.ics` (DTSTART 16:45), and `wedding-details.md`. Reception stays 18 h 30.

## 2026-06-22 — On-site RSVP confirmation panel
- Client confirmed Web3Forms emails arrive. Replaced the small success status line with an
  elegant **confirmation panel** (sage check + « Merci ! » + message) that appears in place
  of the form after a successful submit, scrolls into view, gentle pop animation
  (disabled under prefers-reduced-motion).

## 2026-06-22 — Activated RSVP + acted on thorough review (subagent)
- Set the **Web3Forms access key** → online RSVP form is live (emails André per submit).
- Ran a senior code/UX review via a subagent; applied the high-value fixes:
  - Compressed the PNG **fallback** 575 KB → **130 KB** (downscaled 1000px + 256-colour quantize).
  - **Body font-weight 300 → 400** and darkened `--muted` to `#615c56` (mobile legibility).
  - Sticky nav: added **`-webkit-backdrop-filter`** + bumped opacity to 0.95 (iOS see-through fix).
  - RSVP no-JS fallback: added Web3Forms **`redirect`** hidden input.
  - Guest field names use a **monotonic counter** (no collisions after add/remove).
  - `.ics` **DTSTAMP** set to a real value.
  - Removed **dead CSS** (`.faq*`, `.illustration-placeholder`) + stale comment.
- Deferred (noted, low value): self-hosting fonts; collapsing the form on success; canonical tag.

## 2026-06-22 — RSVP section recoloured to the light theme
- Moved the whole RSVP block from the dark charcoal panel into the **same light tone as the
  rest of the site**; removed the distinct coloured frame on the "mariés" contact card.
- Fixed invisible unselected pills/inputs (darker 1.5px borders); form is now a subtle sand
  card with white fields. Disclosure button uses the standard `btn--ghost`.
- Removed a **stale duplicated dark-theme RSVP CSS block** that was overriding the new styles
  (leftover from a merge).

## 2026-06-22 — RSVP redesign + venue-inspired favicon (client feedback)
- New **favicon**: the hotel's **arched window** (lancet) in the drawing's sampled blue on a
  cream disc — replaces the "&" icon. Regenerated .ico / 16 / 32 / 512 / apple-touch.
- **RSVP contacts** restructured into two cards; **"Auprès des mariés — André & Rhéa"**
  emphasized so it's not buried in text.
- **Online form redesigned** as a modern white card: présent/absent **pill toggles**,
  full-width guest rows with inline ✕ remove, dashed "+ Ajouter un invité", **centered submit**.
- Removed the "régime alimentaire" placeholder from the message field.
- Verified assets serve (200); no orphaned CSS classes.

## 2026-06-22 — Online RSVP + favicon + share image
- Reworked RSVP copy: confirm directly with the **mariés OR their parents** (not only parents).
- Added an **optional online RSVP form** (disclosure button → form) posting to **Web3Forms**:
  attendance radio, add/remove multiple guest names, optional message; honeypot + XSS-safe JS
  (`assets/js/rsvp.js`). Works as a plain POST without JS too. Awaiting André's access key
  (`PLACEHOLDER_ACCESS_KEY`); JS shows a graceful message until then.
- Added **favicon** set (serif "&" on sage disc: .ico, 16/32 png, apple-touch, 512) and a
  **1200×630 OG/Twitter share image** (Pillow + Instrument/IBM Plex Serif). Wired into <head>.
- Verified all assets serve locally (200).

## 2026-06-22 — Illustration integrated + add-to-calendar
- Client uploaded `assets/img/hotel.png` to `main`; pulled it onto the working branch.
- Optimized the illustration: `hotel.webp` (~82 KB) as primary + compressed `hotel.png`
  (~575 KB) fallback via `<picture>`. (Installed Pillow from PyPI — network allows pip.)
- Added an **« Ajouter au calendrier »** button → `assets/wedding.ics` (VEVENT, TZ Asia/Beirut,
  22 Aug 2026 17:00 → 23 Aug 02:00, both venues in the description).
- Dinner time confirmed at 20 h 00. Client confirmed GitHub Pages is enabled.
- Note: `main` currently has only the initial commit + the uploaded image, NOT the site.
  Going live requires getting the branch content onto `main` (pending explicit go-ahead).

## 2026-06-22 — Real content rendered into the site
- Client provided full content. Logged all of it to `wedding-details.md`, including online
  research on the two venues (Église N.-D. de l'Annonciation, Achrafieh — grec-orthodoxe,
  consacrée 1927 ; Hôtel Al Bustan, Beit Mery — landmark de 1967 surplombant Beyrouth).
- Rebuilt `index.html` with real French content: hero (André & Rhéa · samedi 22 août 2026 ·
  Beyrouth & Beit Mery), Le jour J (cérémonie 17 h / réception 18 h 30 + parkings + plans),
  Programme, Cadeaux (coordonnées bancaires à venir), Présence (RSVP avant 31 juillet 2026
  via les parents — pas de numéros). Removed welcome/dress-code/lodging/children sections.
- Design locked to faire-part look: charcoal on white + **sage-green accent** from the
  illustration; faire-part-style thin-rule date motif in the hero. French typography
  (narrow NBSP in « 17 h 00 », etc.).
- Hotel illustration referenced at `assets/img/hotel.png` with a graceful fallback;
  **file still needed from client** (chat attachments don't reach the container).
- Open: confirm **dinner time** (client wrote « 8h » → set to 20 h 00); bank details later.

## 2026-06-22 — Plan approved + scaffold retuned to chosen direction
- Prepared and got approval for the full website plan (saved in plan history).
- Logged client decisions to `decisions.md` and `wedding-details.md`:
  minimaliste moderne · RSVP via WhatsApp (no form) · hotel illustration (no photos) ·
  free GitHub URL for now (custom domain later).
- Retuned the scaffold to match: French (`lang="fr"`) minimalist `index.html`, WhatsApp
  RSVP section + contact numbers, a slot for the hand-drawn hotel illustration; reworked
  `styles.css` tokens to neutral minimalist palette + placeholder accent + sans-serif body.
- Added skills: `content-sync` (map memory → page, French typography) and `preview`
  (local server + responsive screenshots).
- **Still needed from client:** intake answers (names, date, venue(s), programme, WhatsApp
  numbers + deadline), the hotel illustration file, a faire-part photo; enable GitHub Pages.

## 2026-06-22 — Project initialization
- Repurposed the empty `phone-assistant` repo into the wedding website project.
- Replaced the unrelated AL/Business Central `.gitignore` with a web `.gitignore`.
- Wrote `CLAUDE.md` (operating manual + memory discipline).
- Created the memory system under `.claude/memory/`: `README`, `wedding-details`,
  `decisions`, `changelog`, `tasks`, `learnings`.
- Added `.claude/settings.json` with safe permissions and a SessionStart hook that
  surfaces memory at the start of each session.
- Scaffolded the one-page site: `index.html` + `assets/css/styles.css` (elegant template
  with placeholder content tied to `wedding-details.md`).
- Added GitHub Pages auto-deploy workflow `.github/workflows/deploy.yml`.
- Created the `publish` skill documenting the deploy procedure.
- Updated `README.md`.
- **Pending client actions:** rename repo to `wedding-website`; enable GitHub Pages
  (Settings → Pages → Source = GitHub Actions); provide real wedding details.
