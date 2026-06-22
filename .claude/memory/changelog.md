# Changelog

Dated log of what changed each session. Newest at top.

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
