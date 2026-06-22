# Changelog

Dated log of what changed each session. Newest at top.

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
