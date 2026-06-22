# Changelog

Dated log of what changed each session. Newest at top.

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
