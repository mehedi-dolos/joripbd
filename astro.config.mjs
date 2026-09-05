import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// SITE_URL / SITE_BASE are set by the GitHub Pages workflow (project pages live
// under /<repo>/). Locally and on the final Hostinger domain both stay at root.
const site = process.env.SITE_URL || 'https://joripbd.com';
const base = process.env.SITE_BASE || '/';

// https://astro.build/config
export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  build: { format: 'directory' },
  vite: { plugins: [tailwindcss()] },
});
