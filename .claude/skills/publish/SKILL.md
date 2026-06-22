---
name: publish
description: Publish/deploy the wedding website to GitHub Pages. Use when asked to deploy, publish, ship, or push the site live, or to verify the live deploy. Covers the GitHub Pages + Actions workflow and pre-deploy checks.
---

# Publish the Wedding Website

The site is a static site hosted on **GitHub Pages**, deployed by GitHub Actions
(`.github/workflows/deploy.yml`) on every push to `main`.

## Pre-deploy checklist
1. Content matches `.claude/memory/wedding-details.md` (no leftover `TODO` placeholders for confirmed details).
2. Preview locally and sanity-check mobile layout:
   ```bash
   python3 -m http.server 8000   # open http://localhost:8000
   ```
3. Update memory: `changelog.md` (what changed) and `tasks.md` (what's next).

## Deploy
Deployment is triggered by getting changes onto `main`:
- Work is done on the assigned branch (`claude/phone-assistant-setup-sm66ba`).
- To go live, the branch must be merged into `main` (open a PR only if the client asks;
  otherwise follow the client's instruction on how `main` gets updated).
- On push to `main`, the workflow builds and deploys automatically.

## One-time setup (client action, only once)
Repo → **Settings → Pages → Source = "GitHub Actions"**. Until this is done, the workflow
will run but Pages won't serve. I cannot toggle this via tools — confirm with the client.

## Verify the deploy
- Check the Actions run for the "Deploy to GitHub Pages" workflow (green).
- Open the published URL (shown in the workflow's `deploy` job output, typically
  `https://<owner>.github.io/<repo>/`).

## Notes
- The whole repo root is published as the site (`path: '.'`). Keep non-site files
  (memory, workflows) out of the way; they're harmless but not linked from the page.
