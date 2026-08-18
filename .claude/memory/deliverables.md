# Deliverables Inventory

> What exists, where it lives, and which script builds it. Read this first when a session
> needs to touch print or event assets — especially when **multiple sessions run in parallel**.
> Newest context at top of each list.

## ⚠️ PRIVACY POLICY (read before committing anything)

The repo is **public** and hosts the live GitHub Pages site. Therefore:

- **Guest-identifying data is NEVER committed.** The guest list, the nominative seating
  plan, and anything naming individual guests stay **out of git**.
- These live only in the **session scratchpad** (`/tmp/.../scratchpad/`), which is
  **ephemeral and NOT shared between sessions**. They are delivered to the client via
  file upload in chat, never pushed.
- Parents' names (Elie & Pascale Geha · Manhal & Najwa Nacouzi) are already public on the
  faire-part, so they may appear in memory. Individual guest names may not.
- If the client wants these tracked in git, use a **separate private repo** — do not add
  them here while this repo is public. (See decisions.md → "Guest-data privacy".)

## Committed print assets — `assets/print/` (public, safe)

All generated with Python (reportlab + PyMuPDF/fitz + Pillow). Fonts: IBM Plex Serif
(regular + italic). Palette: INK #2b2b29, SAGE #5f7d63, light sage #aebfa3, ivory #f4f1e9.
Each script is the source of truth; re-run from repo root to regenerate.

| Asset | Script | Output |
|-------|--------|--------|
| Faire-part (4 variants) | `generate_invitation.py` | `invitation-a5` (with QR), `-no-qr` (178×127), `-no-deadline`, `-minimal` (.pdf/.png) |
| Thank-you card (on plates) | `generate_thankyou.py` | `remerciement.pdf/.png` (A5) |
| Table cards — 23 scents | `generate_table_cards.py` + `tables_extract.py` + `tables-source.pdf` | `tables-A5.pdf`, `tables-A7.pdf` (23 p each), `tables-overview.png` |
| Envelope seal sticker ×3 | `generate_sticker.py` | `sticker-blue/-sage/-green` (Ø25mm +2mm bleed) |
| Perfume coupon (A6) | `generate_coupon.py` | `coupon.pdf/.png` |
| Logo (black) + garden drawing | `generate_print_assets.py` | `logo-black.pdf/.png`, `drawing-cropped.pdf/.png` |
| Sources (committed) | — | `logo-source.png`, `hotel-source.png`, `drawing-source.pdf` |

Conventions: A7 = A5 at exactly ½ scale (identical design, `show_pdf_page`). Illustrations
auto-cropped to visible content via `visible_bbox()` (numpy density) + CV-verified centering.

### Table cards — the couple's own hand-made scans (2026-08-17)
The 23 table cards now use the couple's **hand scans** (`tables-source.pdf`: pages 1–8 =
calligraphy names, pages 9–31 = the 23 plant/tree drawings). `tables_extract.py` isolates each
name (grey-pencil → darkness mask) and each drawing (blue-pen → blueness mask), removing the
spiral binding + corner labels via BFS connected components, then recolours to one ink tone.
`generate_table_cards.py` composes Nº + name + drawing (A5 & A7); run with `--blue` for a
variant that keeps the drawings' original ballpoint blue. The old procedural motif system
(`table_motifs.py`, `sketch.py`) was **removed**.
- Drawings are matched to names **by content** (the scan order differs from the name order).
- Per-card rotations baked into the `TABLES` list (drawings 1–9 + Cannelle/Chocolat were sideways).
- **Final table numbering** (after the couple's swaps): **Nº 1 = Cèdre du Liban**,
  **Nº 15 = Jasmin d'Orient**, **Nº 13 = Musc Blanc**, **Nº 23 = Verveine Sauvage**; all other
  numbers keep the wedding-details scent order. ⚠️ Keep the seating plan / guest list in sync
  with this numbering.

## PRIVATE deliverables — scratchpad only, NOT in git

| Asset | Script (scratchpad) | Notes |
|-------|--------|-------|
| **Playlist** `Playlist-Rhea-Andy.xlsx` | `build_playlist.py` | Sheets: Déroulé · Party (109) · Ambiance (57) · Dance Before Zaffeh (6, DJ w/ BPM+Key) · Moments clés. No guest data — private mainly to keep the couple's set list unpublished. |
| **Seating plan** `plan-de-salle.pdf/.png` | `generate_seatingplan.py` | Venue-accurate garden layout, 23 tables (1–22 + 24 renumbered → 1–23), coloured by host side. **Nominative → never commit.** |
| **Guest list** `TablesDiffa-Rhea-Andy.xlsx` | (client upload) | Guest names + table assignments. **Never commit.** |

If you regenerate any of these, deliver via file upload; do not push.

## Playlist — open questions / status

- All 166 titles now have title + artist (corrections applied 2026-08-17).
- Still missing **durations** for several Arabic tracks (multiple live/studio versions):
  Hanna El Sakran, El Tannoura, 3am Biza3elni Lello, Al Bosta (~8:56 studio), Bhebbak Ma
  Baaref, Bi Saraha, Batwanes Beek, Habibi Ya Eini — to finalize with the band on the day.
- "Colin Jay Remix" of We Found Love is a DJ bootleg → not on Spotify/Apple Music.
- Spotify/Apple: cannot create a playlist in the client's account (needs their OAuth login).
  Per-track links provided instead; a converter (Soundiiz/TuneMyMusic) can bulk-import a CSV.
