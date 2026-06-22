# Wedding Website

A simple, elegant, single-page wedding information website. Its purpose is to
**complement the printed wedding card** with the practical details guests need.

- **Stack:** Static HTML + CSS (no framework, no build step) — fast, durable, trivial to host.
- **Hosting:** GitHub Pages (deployed automatically via GitHub Actions on push to `main`).
- **Managed by:** Claude (design, code, maintenance, and hosting).

## Project layout

```
index.html                 # The one-page site
assets/css/styles.css      # All styling
assets/img/                # Images (photos, icons)
.github/workflows/         # CI/CD — auto-deploy to GitHub Pages
.claude/                   # Claude's "operating system": memory, skills, agents, settings
CLAUDE.md                  # How this project works (read this first)
```

## Local preview

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

> Note: the repository is named `phone-assistant` for now and is being renamed to
> `wedding-website`. GitHub redirects the old URL automatically, so nothing breaks.
