# Decision Log (ADR-style)

Each entry: what was decided, and why. Newest at top.

## 2026-06-22 — Design direction: minimaliste moderne
- **Decision:** Clean, airy, near-monochrome palette (off-white / charcoal) + **one
  restrained accent** color taken from the faire-part. Primarily a clean sans-serif;
  a refined serif may be used *only* for the couple's names.
- **Why:** Client chose "minimaliste moderne." Replaces the earlier gold-serif scaffold.

## 2026-06-22 — RSVP via WhatsApp, no online form
- **Decision:** No RSVP form. Guests confirm by **WhatsApp** to the couple and/or their
  parents; the site shows `wa.me/<number>` buttons (optionally with a prefilled message)
  + an RSVP deadline.
- **Why:** Client preference; zero backend, familiar channel for guests.

## 2026-06-22 — Imagery: hand-drawn hotel illustration, no photos
- **Decision:** No photographs. The single recurring visual is the **hand-drawn
  illustration of the hotel** from the printed faire-part, placed elegantly (hero +
  optional subtle line-art divider). Client to provide the file (PNG transparent / SVG).
- **Why:** Client preference; keeps the minimalist tone and ties the site to the card.

## 2026-06-22 — URL: start on free GitHub Pages domain, custom domain later
- **Decision:** Launch on `andregeha.github.io/wedding-website`; attach a custom domain
  later if wanted (non-breaking, just add CNAME + DNS).
- **Why:** Client chose "decide later." No reason to block launch on a domain purchase.

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
