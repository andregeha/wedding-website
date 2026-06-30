# Changelog

Dated log of what changed each session. Newest at top.

## 2026-06-30 (5) — Verso drawing enlarged + Cloudflare Pages domain
- **Faire-part verso**: illustration enlarged (iw 340 → 400) and kept centred — the « high »
  look was the faint lawn foreground; bigger fills the page so it reads as a centred hero.
- **Hosting → Cloudflare Pages** (client choice B, free, hides GitHub username). Target URL
  **`https://mariage-andre-rhea-geha.pages.dev`** (note: `.pages.dev`, no `www`, not `.pages.app`).
  Updated all absolute URLs in `index.html` (og:url, og:image, twitter:image, Web3Forms
  `redirect`) and the **card QR** (`SITE`) to the pages.dev address.
- **Web3Forms still works** from any domain (browser POST to api.web3forms.com with the public
  key — host-independent). Client must connect the repo in Cloudflare (project name
  `mariage-andre-rhea-geha`, no build, output dir = root). GitHub Pages can stay as a mirror.
- ⚠️ Don't print the card until the Cloudflare site is confirmed live at that exact URL
  (the QR has no redirect if the URL never existed).

## 2026-06-30 (4) — Faire-part: full content on the recto, big drawing on the verso
- Reworked the card so the **recto holds everything** (parents, names, date, **illustration
  back on the recto**, cérémonie/réception, both gift accounts, and a small QR + « Infos,
  programme & confirmation en ligne » at the bottom). **Verso = just the illustration, very
  large** (centred, no text). Removed the verso RSVP/QR + unused constants. Regenerated PDF/PNGs.
- Updated `invitation` skill + memory to match.

## 2026-06-30 (3) — Liste de mariage intro line reworded
- Replaced the clunky « vous pouvez nous gâter par un virement — au choix… » lead with a
  restrained, classic line: « Votre présence est notre plus beau cadeau. Pour ceux qui le
  souhaitent, par virement : » (leads straight into the two account cards). Site only;
  shipped via PR #25. Set repo git identity to `Claude <noreply@anthropic.com>`.

## 2026-06-30 (2) — Section reorder, EUR account, ampersand font, bigger verso photo
- **Site section order** changed to: Le jour J / Merci de confirmer votre présence /
  Programme / Liste de mariage. Reassigned `section--alt` so backgrounds alternate
  grey/white/grey/white; RSVP webform untouched (still works). Nav reordered to match.
- **Hero ampersand** « & » now in **IBM Plex Serif** (same as the faire-part); loaded the
  font + `.hero__names .amp` rule (was Cormorant italic, client disliked it).
- **Liste de mariage — added the France/EUR account** (André Geha · `REVOFRP2` ·
  `FR76 2823 3000 0144 2006 8520 030`). Site rebuilt as **two compact cards** (Liban·USD /
  France·EUR) in a responsive grid (`.gift-grid`/`.gift-card`), replacing the long `dl`.
- **Faire-part**: recto footer now lists **both accounts** (one compact line each, under a
  small « LISTE DE MARIAGE » title); verso illustration **enlarged** (iw 232 → 260).
  Regenerated `invitation.pdf` / `.png` / `-verso.png`.

## 2026-06-30 — Time fix, gift wording, "Merci de confirmer", faire-part redesign
- Client confirmed the **online RSVP (Web3Forms) works**.
- **Published live**: merged via PR #23 (squash) → `main`; Deploy run #24 = success.
  Direct `git push origin main` is blocked (503 / protected branch) — go-live path is
  **PR + merge** via the GitHub MCP tools. Site live at andregeha.github.io/wedding-website.
- **Cérémonie 16 h 45 → 16 h 30** everywhere: site (carte + programme), `wedding-details.md`,
  and faire-part (`CEREMONY` constant).
- **Liste de mariage**: dropped the **dépôt en espèces / agence-locator** note on the site —
  keep only the virement coordinates (BIC + IBAN). Reworded the lead. EUR (France) account
  still pending. (Faire-part recto footer already wire-only.)
- **RSVP heading** → « **Merci de confirmer** votre présence » (site `<h2>` + faire-part
  `RSVP_TITLE`), instead of « Confirmer… » alone.
- **Faire-part redesign**: moved the hand-drawn illustration **off the recto** (rebalanced
  the recto: larger names, more whitespace) and onto the **verso, much larger**. Removed the
  « déroulé de la journée » from the verso (it lives on the site); verso = big illustration +
  RSVP + QR. Regenerated `invitation.pdf` / `.png` / `-verso.png`.

## 2026-06-25 — Real bank details (BLOM Bank, USD) on site + faire-part
- Client opened a BLOM Bank account (Lebanon), two currencies; **only USD is published**
  per client. Full data saved to `wedding-details.md` (incl. the LBP IBAN, memory-only).
- **Site « Liste de mariage »**: replaced placeholders with a discreet detail list —
  Bénéficiaire / Banque / BIC-SWIFT (`BLOMLBBX`) / IBAN USD / Devise — plus a cash-deposit
  line linking the BLOM branch locator (note: filter on *Branches*, not *ATMs*), and a soft
  note that a EUR account (France) is coming. Added `.gift-accounts` (dl) + `.gift-note` CSS.
- **Faire-part**: recto footer now two discreet lines with the USD wire info
  (BLOM Bank · BIC · IBAN · beneficiary). Regenerated `invitation.pdf/png`.
- SWIFT `BLOMLBBX` and the branch-locator URL verified via web search.

## 2026-06-23 — Hand-drawn logo favicon + site « Liste de mariage » bank lines
- New **favicon** from the client's hand-drawn logo (`Logo_AR.pdf`): cropped the blue floral
  sprig (excluding the A./R. script), thickened slightly for small-size legibility →
  favicon.ico / 16 / 32 / 512 / apple-touch. Source render kept reproducible via the PDF.
- **Site gift section** reworded: « Pour ceux qui le souhaitent, une liste de mariage est
  disponible chez : » followed by the two discreet bank lines (Liban USD / International EUR,
  placeholders), matching the card. Added `.gift-accounts` style.

## 2026-06-23 — Gift section term → « Liste de mariage » (client choice)
- Client opted for « Liste de mariage » on both the site (section title + nav) and the card
  recto footer (bank line lead-in), superseding the earlier « Avec gratitude / Si le cœur… ».

## 2026-06-23 — Soften « Cadeaux » wording
- Replaced the explicit « Cadeaux » with a gentler, classier framing:
  - **Site:** section title → « Avec gratitude » (nav « Gratitude »); body softened
    (« …et si le cœur vous en dit, nos coordonnées vous seront communiquées avec plaisir »).
  - **Card recto footer:** bank line now led by « Si le cœur vous en dit · … » instead of « Cadeaux ».

## 2026-06-22 — « Cocktail » → « Verre d'accueil »
- Replaced "Cocktail" with the classier **"Verre d'accueil"** on the site programme,
  the invitation card (verso timeline + generator), and `wedding-details.md`.

## 2026-06-22 — Invitation: balance names + online wording
- Couple's names reduced (30→25 pt) and parents bumped (11.5→12.5 pt) for a harmonious hierarchy.
- Verso RSVP block now says the site has **toutes les informations et le programme détaillé**
  (not just confirmation), keeping the three options (mariés / parents / en ligne) + deadline.

## 2026-06-22 — Invitation: add RSVP options on the verso
- Added a « Confirmer votre présence » block on the verso (under the programme), mirroring the
  site's three options: **auprès des mariés ou de leurs parents — ou en ligne** (QR), plus the
  « Réponse souhaitée avant le 31 juillet 2026 » deadline.

## 2026-06-22 — Invitation polish (client feedback)
- **Names** reduced 34→30 pt (more refined).
- **Bank/gift** info moved off the verso to a **single tiny discreet line on the recto** footer
  (Liban·USD + International·EUR IBANs; rest on request).
- **Verso reimagined as a beautiful page:** « Le déroulé de la journée » — an elegant centre-
  axis timeline (16 h 45 Cérémonie · 18 h 30 Cocktail · 20 h 00 Dîner · 02 h 00 Fin) + QR.

## 2026-06-22 — Invitation rework (client feedback)
- **Recto:** parents now placed on either side (top-left / top-right) — classic faire-part
  layout — with the invitation sentence centred below.
- **Verso:** removed the repeated hotel illustration; made it airy with the « Votre présence
  est notre plus beau cadeau » sentiment as the focus.
- **Bank details now truly discreet:** only the IBAN per account on a small single line each
  (Liban·USD, International·EUR) + « Bénéficiaire et BIC/SWIFT sur demande » footnote.

## 2026-06-22 — Invitation redesigned: landscape, parents-issued, recto/verso + bank
- New **landscape 178×127 mm (7×5") recto/verso** card (2-page vector PDF + recto/verso PNGs).
- **Recto:** issued by the parents (Elie & Pascale Geha · Manhal & Najwa Nacouzi) — « ont la joie
  de vous convier au mariage de leurs enfants André & Rhéa » — date, illustration, and
  cérémonie/réception in two columns.
- **Verso:** illustration + discreet « cadeaux » note with **two bank accounts** (Liban/USD,
  étranger/EUR; Bénéficiaire/Banque/IBAN/BIC, placeholders `‹ à compléter ›`) + QR.
- Still uniform IBM Plex Serif. Pending: real bank details from André to replace placeholders.

## 2026-06-22 — Invitation: uniform typography + max-quality illustration
- Unified the faire-part on a **single typeface, IBM Plex Serif** (regular + italic) —
  names and the RSVP line were the last Instrument Serif holdouts (the tall/narrow font that
  looked stretched). Now fully consistent.
- Embedded the illustration at **original lossless 2000px** (`assets/print/hotel-source.png`)
  instead of the WebP, for maximum print quality. PDF stays vector (text + QR).
- Quality note for client: vector PDF = resolution-independent; CMYK + bleed/crop marks can be
  added on request for a professional printer.

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
