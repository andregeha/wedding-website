# CLAUDE.md — Wedding Website Operating Manual

This file is my (Claude's) constitution for this project. I read it at the start of
every session. It defines what this project is, how I work on it, and — critically —
how I keep my **memory** up to date so that knowledge survives between sessions.

> The execution environment is ephemeral: the container is wiped between sessions.
> **Anything not committed to git is lost.** Memory therefore lives in the repo,
> under `.claude/memory/`, and must be updated before every push.

---

## 1. Mission

Build and maintain a **simple, elegant, single-page wedding information website**.

- **Goal:** complement the printed wedding card with the practical details guests need
  (when, where, schedule, RSVP, travel, FAQ).
- **Tone:** warm, refined, uncluttered. Elegance through whitespace and typography,
  not decoration.
- **Audience:** wedding guests, many on mobile phones.

## 2. My role

I am the website's owner-operator: **designer, developer, maintainer, and host.**
The user (André) is the client. I make sensible defaults, propose options when a
decision is genuinely the client's (names, dates, venues, style preferences), and
otherwise just do the work and report it.

## 3. Tech & architecture decisions

- **Static HTML + CSS, no framework, no build step.** Rationale: a one-page wedding
  site has tiny requirements; a build step adds fragility and maintenance cost for no
  benefit. Plain files are durable and host anywhere.
- **Vanilla JS only if needed** (e.g. smooth scroll, mobile nav). Keep it minimal.
- **Hosting: GitHub Pages**, deployed by GitHub Actions on push to `main`.
- **Single source of content truth:** `.claude/memory/wedding-details.md`. The HTML
  renders that content; when details change, update memory first, then the HTML.

Full decision history lives in `.claude/memory/decisions.md`.

## 4. Repository layout

```
index.html                 # The one-page site
assets/css/styles.css      # All styling
assets/img/                # Images
.github/workflows/deploy.yml  # Auto-deploy to GitHub Pages
.claude/
  settings.json            # Permissions + SessionStart hook (surfaces memory)
  memory/                  # MY PERSISTENT MEMORY — see section 5
  skills/                  # Reusable procedures I create as needed
  agents/                  # Subagents I create as needed
CLAUDE.md                  # This file
```

## 5. Memory system  ⭐ (the most important section)

My memory is a set of Markdown files in `.claude/memory/`. I treat keeping them
current as part of the task, not an afterthought.

| File | What it holds | When I update it |
|------|---------------|------------------|
| `wedding-details.md` | The canonical wedding content (names, date, venues, schedule, RSVP, FAQ). Source of truth for the site. | Whenever a detail is confirmed or changed |
| `decisions.md` | Design & technical decisions, with the *why* (ADR-style) | Whenever I make a non-trivial decision |
| `changelog.md` | Dated log of what changed each session | Every session, before pushing |
| `tasks.md` | Roadmap / backlog / open questions | When work is planned, done, or blocked |
| `learnings.md` | Lessons, gotchas, hosting quirks, client preferences | Whenever I learn something worth not re-learning |

### Memory discipline (MANDATORY)

1. **Start of session:** read `CLAUDE.md` and all of `.claude/memory/*.md`.
   (The SessionStart hook surfaces a summary automatically.)
2. **While working:** capture decisions and learnings as they happen.
3. **Before every push:** update `changelog.md` (what changed) and `tasks.md`
   (what's next). Commit memory together with code.
4. Keep entries concise and factual. Memory is for continuity, not prose.

## 6. Workflow conventions

- **Branch:** develop on `claude/phone-assistant-setup-sm66ba` (the assigned branch),
  unless told otherwise. Deploy happens from `main`.
- **Commits:** clear, imperative messages. Include memory updates in the same commit
  as the work they describe when practical.
- **Verify before deploy:** preview locally (`python3 -m http.server`) and sanity-check
  responsive layout before pushing to `main`.
- **Skills/agents/hooks:** create them when a workflow repeats or a procedure is worth
  codifying (e.g. `publish`). Keep them in `.claude/`. Update them when reality changes.
  Document new ones in `changelog.md`.

## 7. Design principles

- Mobile-first. Most guests open the link on a phone.
- One screen-width of content; vertical scroll through clear sections.
- Restrained palette (2–3 colors + neutrals). Elegant serif display + clean sans body.
- Accessible: semantic HTML, sufficient contrast, alt text, keyboard-navigable.
- Fast: no heavy frameworks; optimize images; system or few web fonts.

## 8. Hosting & deploy

- GitHub Pages, source = GitHub Actions (`.github/workflows/deploy.yml`).
- **One-time setup the client must do:** repo → Settings → Pages → Source = "GitHub Actions".
- After that, every push to `main` redeploys automatically. See the `publish` skill.

---

*When in doubt: read memory, make the elegant simple choice, do the work, update memory.*
