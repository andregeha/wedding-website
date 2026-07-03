# Wedding Details — Source of Truth

> Canonical content for the site. Update here first, then reflect in `index.html`.

## The couple
- Partner 1: **André Geha**
- Partner 2: **Rhéa Nacouzi**
- Display as: **André & Rhéa**

## Date & time
- Wedding date: **samedi 22 août 2026**
- Ceremony: **17 h 00**
- Reception / verre d'accueil: **18 h 30**

## Cérémonie (religieuse)
- Type: religieuse (rite grec-orthodoxe).
- Heure: **17 h 00**
- Lieu: **Église Notre-Dame de l'Annonciation**, Achrafieh, Beyrouth.
- Parking: **gratuit, à 50 m après l'église sur la droite de la route.**
- Carte: https://maps.app.goo.gl/grQqHbBrcDq7Jx4i6
- Recherche (mémoire): église paroissiale grec-orthodoxe d'Achrafieh, consacrée en 1927
  (terrain donné par la famille Fernainé). Façade à portique et grand portail, parapet
  flanqué de deux coupoles en rosace contenant quatre cloches. Riche collection d'icônes
  (icônes russes du XIXe, œuvres de Habib Srour, rare icône sur toile du XVIIe).

## Réception
- Heure: **18 h 30** (verre d'accueil).
- Lieu: **Hôtel Al Bustan**, Beit Mery (Mont-Liban).
- Parking: **gratuit sur place.**
- Carte: https://maps.app.goo.gl/j3J1pSzMC57UrrDx9
- Recherche (mémoire): institution emblématique ouverte en 1967, perchée sur la colline
  de Beit Mery surplombant Beyrouth et la Méditerranée, à ~20 min de Beyrouth. Chapelle
  intime, jardins et "crystal garden" pour les réceptions, spa, deux restaurants, terrasse
  panoramique. Hôte du festival international Al Bustan. Site: hotelalbustan.com

## Programme / déroulé
- **17 h 00** — Cérémonie religieuse
- **18 h 30** — Verre d'accueil
- **20 h 00** — Dîner  *(⚠️ client a écrit « 8h diner » → interprété comme 20 h ; à confirmer)*
- **02 h 00** — Fin de la célébration

## Dress code
- Non précisé (à ne pas afficher).

## Accès / parking / transport
- Parking gratuit à l'église (50 m après, à droite) et à l'hôtel (sur place).

## Hébergement
- Non précisé (à ne pas afficher).

## Enfants
- Non précisé (à ne pas afficher).

## Cadeaux / Liste de mariage
**Deux comptes publiés** (site + faire-part) : un au Liban (USD), un en France (EUR).
Participation **par virement** uniquement (pas de dépôt en espèces affiché — décision 2026-06-30).

### Compte Liban — USD (BLOM Bank)
**Banque : BLOM Bank S.A.L.** (بنك لبنان والمهجر), Beyrouth, Liban — **BIC/SWIFT : `BLOMLBBX`**.
Compte au nom de **ANDRE NOEL GEHA &/OR RHEA NACOUZI** (n° client 2660943). Ouvert juin 2026.

| Devise | N° de compte | IBAN | Publié ? |
|--------|--------------|------|----------|
| **USD** | 021 02 673 2660943 1 4 | `LB90 0014 0000 2102 6732 6609 4314` | ✅ site + faire-part |
| LBP | 021 01 673 2660943 1 5 | `LB55 0014 0000 2101 6732 6609 4315` | ❌ mémoire seulement |

### Compte France — EUR (Revolut) — ajouté 2026-06-30
- Bénéficiaire : **André Geha** (seul) · Banque : **Revolut** · **BIC : `REVOFRP2`**
- **IBAN : `FR76 2823 3000 0144 2006 8520 030`** · Devise : EUR · ✅ site + faire-part

## Faire-part imprimé
- Format **paysage 178 × 127 mm** (7×5", standard), **une seule page**, vectoriel.
- **Émis par les parents** : « Elie & Pascale Geha · Manhal & Najwa Nacouzi — ont la joie de
  vous convier au mariage de leurs enfants André & Rhéa ».
- **Une seule page** (décision 2026-06-30 (8) : plus de verso) : parents, prénoms, date,
  **l'illustration** (recadrée au contenu visible via `visible_bbox()`), cérémonie/réception
  (2 colonnes), les **deux comptes** « Liste de mariage » (Liban/USD + France/EUR, une ligne
  compacte chacun), et un **petit QR** + légende « Infos, programme & confirmation en ligne »
  en bas. PDF 1 page + `invitation.png`. Généré par `assets/print/`.

## RSVP
- **Date limite: 21 juillet 2026.**
- Pas de numéros affichés (les invités les connaissent). Contacter les parents:
  - **Elie & Pascale Geha**
  - **Manhal & Najwa Nacouzi**

## Mot d'accueil / histoire
- Aucun (on s'en passe).

## Assets (from the client)
- **Hotel illustration**: provided in chat (hand-drawn watercolor of Al Bustan), but **not
  yet on disk / in repo**. NEEDED at `assets/img/hotel.png` (transparent or white bg).
  The page references it with a graceful fallback until the file is added.
- **Faire-part**: seen in chat (style/color reference only — no file needed).

## Design (from faire-part)
- Aesthetic confirmed: near-monochrome, **charcoal text on white**, the colourful hand-drawn
  illustration provides all the colour — exactly the faire-part look.
- Accent: **soft sage green** (drawn from the foliage/garden in the illustration), used
  sparingly (rules, links, button). Faire-part uses a thin-rule date motif — echoed in the hero.
- Fonts: client said no need to match the faire-part font. Keep Inter (sans) for body,
  a refined serif (Cormorant) for names/headings. **Exception (2026-06-30): the hero
  ampersand `& ` uses IBM Plex Serif** (same as the card) — the Cormorant `&` was unloved.
- **Site section order (2026-06-30)**: Le jour J → Merci de confirmer votre présence →
  Programme → Liste de mariage. Backgrounds alternate grey/white/grey/white (`section--alt`
  on Le jour J + Programme; RSVP + Liste de mariage are white).

---
*Last confirmed: full content provided 2026-06-22. Pending: hotel illustration file;
confirm dinner time (20 h?); bank details for gifts later.*
