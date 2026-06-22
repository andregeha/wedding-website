---
name: content-sync
description: Update the wedding site copy from the canonical content in .claude/memory/wedding-details.md. Use whenever wedding details change, when filling placeholders, or to check the page and memory haven't drifted. Covers field-to-HTML mapping and French typography rules.
---

# Sync content from memory → index.html

`.claude/memory/wedding-details.md` is the **source of truth**. The page renders it.
Update memory first, then reflect changes in `index.html`. Never let them drift.

## Field → location map (index.html)
| Memory field | Where in `index.html` |
|---|---|
| Prénoms | `.hero__names`, `.footer__names` (display order matters) |
| Date | `.hero__date` |
| Ville / lieu | `.hero__place` |
| Hotel illustration | `.hero__illustration` — replace the `.illustration-placeholder` with `<img>`/inline SVG |
| Cérémonie (heure/lieu/adresse/carte) | first `.card` in `#jour-j` |
| Réception (heure/lieu/adresse/carte) | second `.card` (remove if single venue) |
| Programme | `.timeline` items in `#programme` |
| Dress code / Accès / Hébergement / Cadeaux | `.faq__item`s in `#infos` |
| RSVP deadline | `.section--rsvp .section__lead` (`[date limite]`) |
| WhatsApp numbers | `.btn--wa` hrefs → `https://wa.me/<international number, no +, no spaces>` |
| Mot d'accueil | `#accueil .section__lead` (remove section if unused) |

## WhatsApp links
- Format: `https://wa.me/212600000000` (country code, digits only, no `+`/spaces).
- Optional prefilled message: append `?text=` + URL-encoded text.

## French typography (apply on every copy change)
- Guillemets : « texte » (with thin spaces inside).
- **Narrow no-break space** before `: ; ! ?` and inside guillemets. Use `&#8239;`
  (narrow NBSP) or `&nbsp;` where a normal NBSP is acceptable.
- Dates en toutes lettres : « samedi 12 septembre 2026 ».
- Heures : « 15 h 00 » (espace insécable autour du « h »).
- Accents on capitals too (À, É, …).

## After syncing
1. Preview (`preview` skill) and check mobile + desktop.
2. Update `.claude/memory/changelog.md`.
3. Commit memory + HTML together.
