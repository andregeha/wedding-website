# Decision Log (ADR-style)

Each entry: what was decided, and why. Newest at top.

## 2026-06-22 — Static HTML/CSS, no framework, no build step
- **Decision:** Build the site as plain `index.html` + `assets/css/styles.css`, vanilla JS only if needed.
- **Why:** A one-page wedding site is tiny. A framework/build step adds fragility and
  maintenance cost for zero guest-facing benefit. Plain files are durable and portable.

## 2026-06-22 — Host on GitHub Pages via GitHub Actions
- **Decision:** Deploy automatically from `main` using `.github/workflows/deploy.yml`.
- **Why:** Free, reliable, zero-ops for a static site, lives in the same repo. The only
  manual step is a one-time toggle (Settings → Pages → Source = GitHub Actions).
- **Alternatives considered:** Netlify/Vercel (great too, but adds an external account
  to manage; Pages keeps everything in one place).

## 2026-06-22 — Single source of content truth in memory
- **Decision:** `.claude/memory/wedding-details.md` is canonical; the HTML renders it.
- **Why:** Avoids the content drifting between "what we agreed" and "what's on the page,"
  and keeps continuity across ephemeral sessions.
