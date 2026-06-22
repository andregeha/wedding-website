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

## 2026-06-22 — Recurring PR conflicts (and the fix)
- Because main is updated via **squash-merge**, the working branch keeps its original commits
  and diverges from the squashed commit → every re-PR conflicts on the touched files.
- **Resolution that works:** before opening the next PR, `git merge origin/main` on the branch
  and resolve in favour of the branch: `git checkout --ours -- .` (the branch holds the latest
  desired state), commit, push, then PR + squash-merge.
- Cleaner long-term: reset the branch to `origin/main` after each merge — but `git reset --hard`
  is blocked by the safety classifier here, so the merge/--ours dance is the practical path.
- Deploy is reliable: each merge to main triggers "Deploy to GitHub Pages", green in ~15 s.

## 2026-06-22 — Deploy / git workflow (important)
- **Direct `git push` to `main` is blocked by the environment proxy (HTTP 503).** Pushes
  only succeed to the assigned branch `claude/phone-assistant-setup-sm66ba`. To publish to
  `main`, open a PR (branch → main) and merge it via the GitHub MCP tools. This triggers the
  Pages deploy. (PR #1 and PR #2 followed this path.)
- Binary files (e.g. the illustration) conflict when both `main` and the branch change them;
  resolve on the branch with `git merge origin/main` + `git checkout --ours <file>`, push, then merge the PR.
- Repo is `andregeha/wedding-website` (renamed); MCP scope name `phone-assistant` still works via redirect.
- Live URL: https://andregeha.github.io/wedding-website/

## 2026-06-22 — Tooling
- No local headless browser; `npx`/`npm` work and `playwright` installs, BUT the
  **Chromium binary download is blocked by the network policy** → in-container screenshots
  are not possible. Verify visually on a real device, or rely on careful CSS review.
  `python3 -m http.server` works for serving/HTTP checks.
- **Attachments sent in chat are NOT written to the container filesystem** — I can see
  images but cannot embed them. The client must add image files to the repo (e.g. via
  GitHub web upload to `assets/img/`).

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
