# Jorip O Paridarshan Company Limited — website

Corporate website for JOP, built to the website proposal dated 30 August 2026 (Option A).

- **Framework:** Astro 5 with Tailwind CSS 4. Static output, no server code.
- **Content:** Markdown and JSON in `src/content` and `src/data`. Edited through Pages CMS (`.pages.yml`).
- **Identity:** follows the GY6 Paperless brand system (https://www.gy6.io/work/paperless). Charcoal, paper, wine and slate; grain, hatch, terrain and folder-tab devices.
- **Fonts:** the target face is Gilroy (commercial). Outfit ships as the free stand-in via fontsource for everything, including labels and numbers; Noto Sans Bengali for the Bengali name only. To switch to Gilroy: put the licensed woff2 files in `public/fonts/` and uncomment `src/styles/gilroy.css`. The token in `global.css` already lists Gilroy first.
- **Form:** Web3Forms. Put the access key issued for info@joripbd.com in `src/data/site.json`.
- **Hosting:** Hostinger. `public/.htaccess` carries the redirects from the old WordPress URLs.

## Run locally

```bash
npm install
npm run dev
```

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
- The Board cards use `public/images/portrait-{wine,slate,navy}.jpg` silhouettes until photographs arrive; set `photo:` in the person file to replace one.
- The six assignment photos in `public/assignments/*-toned.jpg` are brand-toned versions of the old site's photos. The treatment script is `scripts/brandify.py` (Pillow); run `python3 scripts/brandify.py scene in.jpg wine out.jpg` or `portrait in.png slate out.jpg`.
- Management and Team portraits are hatched silhouettes by design until JOP supplies photographs.
- The company profile PDF at `/company-profile.pdf` does not exist yet.
- The Web3Forms key in `src/data/site.json` is a placeholder; the form will not deliver until it is replaced.
