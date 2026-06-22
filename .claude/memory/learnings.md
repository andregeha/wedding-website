# Learnings

Things worth not re-learning. Newest at top.

## 2026-06-22 — Environment & access
- The remote container is **ephemeral**; only committed-and-pushed files persist.
  Memory must be committed before every push.
- I **cannot rename the GitHub repo** via the available tools (no rename API exposed) —
  the client does it in repo Settings. GitHub auto-redirects the old URL, so the git
  remote keeps working even before/after rename.
- I **cannot toggle GitHub Pages settings** via the available tools — the client enables
  Pages once (Settings → Pages → Source = GitHub Actions); after that, deploys are automatic.

## 2026-06-22 — Tooling
- No local headless browser in the container (`chromium`/`chrome` absent); `npx` exists,
  so responsive screenshots need `npx playwright` (network-dependent). The `preview` skill
  documents both paths. `python3 -m http.server` works for serving.

## 2026-06-22 — Client preferences (confirmed)
- Site language: **French only** (`lang="fr"`, French typography).
- Aesthetic: **minimaliste moderne** (airy, neutral, one accent).
- **No photos**; the signature visual is the **hand-drawn illustration of the hotel** from
  the faire-part. The accent color should be derived from the faire-part.
- RSVP: **WhatsApp only** (no form). Show `wa.me` buttons to the couple and/or parents.
- Mainly opened on **mobile**, also desktop → fully responsive is non-negotiable.
- Repo already renamed to `wedding-website`.

## 2026-06-22 — Client preferences (initial)
- Wants the site **simple and elegant**, one page, complementing the printed card.
- André will primarily interact from his phone.
