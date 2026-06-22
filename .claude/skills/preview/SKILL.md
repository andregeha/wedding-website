---
name: preview
description: Preview the wedding site locally and capture responsive screenshots at mobile and desktop widths before deploying. Use to visually verify layout, spacing, and the French content render across breakpoints.
---

# Preview & responsive verification

The site is static, so previewing is just serving the folder.

## Local server
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Responsive screenshots
Capture the target widths to confirm the layout holds. Test matrix: **360, 390, 768, 1280 px**.

If a headless browser is available (Chromium/Chrome), e.g.:
```bash
for w in 360 390 768 1280; do
  chromium --headless --disable-gpu --hide-scrollbars \
    --window-size=${w},1400 \
    --screenshot=scratch/shot-${w}.png \
    http://localhost:8000 ;
done
```
(Adjust the binary name: `chromium`, `chromium-browser`, `google-chrome`, or use
Playwright/`npx playwright screenshot` if installed.) Save shots to a scratch dir, not the repo.

## What to check
- Hero: names + date legible; illustration sits well at all widths.
- Nav wraps cleanly on narrow screens; tap targets ≥ 44px.
- Cards stack to 1 column on mobile, 2 columns ≥ 640px.
- WhatsApp buttons stack on mobile, sit inline on desktop.
- No horizontal scroll at 360px.
- French typography correct (guillemets, narrow NBSP, « 15 h 00 »).

## Then
- Note anything fixed in `.claude/memory/changelog.md`.
- When happy, deploy with the `publish` skill.
