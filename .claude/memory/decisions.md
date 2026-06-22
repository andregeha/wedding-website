# Decision Log (ADR-style)

Each entry: what was decided, and why. Newest at top.

## 2026-06-22 — Custom domain: mariage-andre-et-rhea.com (.com, cheap registrar)
- **Decision:** Buy `mariage-andre-et-rhea.com` (fallback `…-2026.com` if taken) at a cheap
  registrar (Porkbun / Cloudflare / OVH, ~10 €/yr, free WHOIS privacy). Point it at GitHub
  Pages; keep the site on GitHub's CDN (speed unchanged by registrar/price).
- **Rejected:** `.lb` (expensive, manual approval, bureaucratic), `.mariage` (does not exist),
  long names like `invitation-mariage-…` (less elegant). Short name = classier.
- **Setup order (avoid breaking the live github.io URL):** buy → set DNS (apex A/AAAA to
  GitHub + `www` CNAME) → THEN add repo `CNAME` file + update absolute URLs (og/twitter/
  canonical/ics) → enable "Enforce HTTPS". Do NOT add the CNAME file before DNS resolves.
- GitHub Pages apex IPs: A 185.199.108-111.153 ; AAAA 2606:50c0:8000-8003::153 ; www CNAME → andregeha.github.io

## 2026-06-22 — Online RSVP via Web3Forms (static-site friendly)
- **Decision:** Keep the direct contacts (mariés OR their parents) AND add an optional
  online RSVP form. The form posts to **Web3Forms** (`api.web3forms.com/submit`).
- **Why:** GitHub Pages is static (no backend, public repo). Web3Forms is free + unlimited,
  emails André on each submission, and stores nothing in the repo. Its **access key is
  public by design** (safe to commit). Alternatives: Formspree (50/mo free cap), Google Forms
  (external page, off-brand).
- **Security:** honeypot field (`botcheck`); HTTPS-only POST to the one trusted endpoint;
  client never writes user input into the DOM as HTML (textContent only → no XSS); inputs
  have maxlength; JS guards against the placeholder key so the live form never errors.
- **Pending:** André's Web3Forms access key to replace `PLACEHOLDER_ACCESS_KEY` in index.html.

## 2026-06-22 — Favicon = the hotel's arched window (revised)
- **Decision:** Favicon is a clean **lancet (pointed) arched window** in the illustration's
  exact blue (sampled #6F9DC4) on a cream disc — inspired by the hotel drawing, recognizable
  at 16px. Replaces the earlier serif "&" (client felt it had nothing to do with the wedding).
- **OG/Twitter share image** (1200×630): "André & Rhéa" + date + the hotel illustration on
  white (Instrument Serif names + IBM Plex Serif caps). Unchanged.
- **Why:** Ties the icon to the venue; classy and clear at small sizes.

## 2026-06-22 — RSVP redesign (clearer contacts + modern form)
- **Decision:** Show two contact cards — **"Auprès des mariés — André & Rhéa"** (emphasized)
  and "ou de leurs parents — …" — so the couple isn't buried in prose. The online form is a
  **modern white card** (pill toggles for présent/absent, full-width guest rows with an inline
  ✕, dashed "+ Ajouter un invité", centered submit). Removed the dietary-suggestion placeholder.
- **Why:** Client feedback: contacts were buried, the dark form was unattractive.

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
