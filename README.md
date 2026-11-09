# Jorip O Paridarshan Company Limited — website

Corporate website for JOP, built to the website proposal dated 30 August 2026 (Option A).

**Preview:** https://mehedi-dolos.github.io/joripbd/ (GitHub Pages, rebuilt on every push to `main`). Production goes to Hostinger at joripbd.com.

- **Framework:** Astro 5 with Tailwind CSS 4. Static output, no server code.
- **Content:** Markdown and JSON in `src/content` and `src/data`. Edited through Pages CMS (`.pages.yml`).
- **Palette:** built on JOP's own brown `#A67970` (the original joripbd.com navigation bar and logo square), with the original site's navy `#3D506D` as the counterpoint. Espresso `#292221` for dark sections, warm paper `#E9E1E0` for light ones, brown-deep `#795149` for buttons. Tokens live in `src/styles/global.css`. Devices: grain, hatch, terrain ridges (brown in front, navy behind), folder-tab cards.
- **Fonts:** headings and the wordmark in Times New Roman, as in JOP's official correspondence (installed on Macs and Windows; Tinos, its metric-compatible twin, is self-hosted for everything else). Body, labels and figures in Outfit as the stand-in for Gilroy (commercial). Noto Sans Bengali for the Bengali name only.
- **Form:** Web3Forms. Put the access key issued for info@joripbd.com in `src/data/site.json`.
- **Hosting:** Hostinger. `public/.htaccess` carries the redirects from the old WordPress URLs.

## Run locally

```bash
npm install
npm run dev
```

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`: it builds with `SITE_BASE=/joripbd`, prefixes root-absolute links with `scripts/prefix-base.mjs`, and publishes `dist/` to the `gh-pages` branch, which GitHub Pages serves. For Hostinger, run a plain `npm run build` (no base) and upload `dist/`.

## Build

```bash
npm run build
```

Output goes to `dist/`. Upload that folder to Hostinger's `public_html`, or wire GitHub Actions to do it on every push.

## Where things live

| What | Where |
|---|---|
| Design tokens (colours, fonts) | `src/styles/global.css` |
| Site-wide facts (address, phones, stats, licence numbers) | `src/data/site.json` |
| Services (one file each) | `src/content/services/` |
| People (one file each) | `src/content/people/` |
| Client logos | `src/data/clients.json` and `public/clients/` |
| Selected assignments | `src/data/assignments.json` and `public/assignments/` |
| Pages | `src/pages/` |

## Dummy content awaiting JOP

The pages read as finished, so the placeholders are deliberate copy rather than bracketed notes. Replace these when JOP supplies the facts:

- Chairperson and Managing Director: `src/content/people/chairperson.md` and `managing-director.md` carry role names and generic bios (`placeholder: true` shows "Profile to follow").
- Founding decade on the About timeline is written as "1980s", inferred from "about 30 years" on the 2017 site.
- Turnaround times on each service page are indicative and unconfirmed.
- Loss classes on the Loss Assessment page are the standard classes, unconfirmed.
- Insurer count is 5 (from the proposal); the old site showed 7 insurer logos.
- Two client logos are `confirmed: false` in `src/data/clients.json` (Habib Bank, Janata Bank guesses; one unnamed "SB" mark).
- IDRA licence number and company registration number are not shown anywhere yet.
- All illustrations in `public/images/` (home collage, ten page heroes, three About tiles) are AI-generated in the brand style; replace with photography if JOP prefers.
- `public/images/ataur-rahman.jpg` and `public/images/abul-hayat.jpg` are derived from public-domain Press Information Department photographs on Wikimedia Commons, treated as halftone tritones. Both sources are around 500px wide, so keep them at card size.
- Jamaluddin Hossain (adviser, died October 2024) has no free-licence photograph; his card uses the silhouette placeholder until JOP supplies one.
- The Board cards use `public/images/portrait-{brown,navy,umber}.jpg` silhouettes until photographs arrive; set `photo:` in the person file to replace one.
- The six assignment photos in `public/assignments/*-toned.jpg` are brand-toned versions of the old site's photos. All image treatments are in `scripts/brandify.py` (Pillow): `scene` tones a photo, `portrait` builds a portrait card image, `placeholder` a silhouette, `retone` moves an illustration onto the brown palette, `monotone` makes a brown monochrome. Tone names are `brown`, `navy` and `umber`.
- Management and Team portraits are hatched silhouettes by design until JOP supplies photographs.
- The company profile PDF at `/company-profile.pdf` does not exist yet.
- The Web3Forms key in `src/data/site.json` is a placeholder; the form will not deliver until it is replaced.
