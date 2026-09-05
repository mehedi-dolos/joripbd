// Rewrites root-absolute URLs in the built site so it can be served from a
// sub-path (GitHub project pages). Astro prefixes its own assets when `base`
// is set; this covers the literal "/images/…", "/clients/…", "/about/" links
// written in the pages. Usage: node scripts/prefix-base.mjs /joripbd
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const base = (process.argv[2] || '').replace(/\/$/, '');
if (!base) { console.log('no base given, nothing to do'); process.exit(0); }
const root = 'dist';
const esc = base.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

function walk(dir, out = []) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}
let n = 0;
for (const file of walk(root)) {
  if (!/\.(html|css|xml|txt)$/.test(file)) continue;
  let s = readFileSync(file, 'utf8');
  const before = s;
  // attributes: href/src/srcset/content/action/poster="/…"  (skip already-prefixed and protocol-relative)
  s = s.replace(new RegExp(`\\b(href|src|content|action|poster)="/(?!/|${esc.slice(1)}/)`, 'g'), `$1="${base}/`);
  // srcset lists: "/a.jpg 900w, /b.jpg 1800w"
  s = s.replace(/\bsrcset="([^"]+)"/g, (m, list) => 'srcset="' + list.replace(new RegExp(`(^|,\\s*)/(?!/|${esc.slice(1)}/)`, 'g'), `$1${base}/`) + '"');
  // css url("/…") and url(/…)
  s = s.replace(new RegExp(`url\\((['"]?)/(?!/|${esc.slice(1)}/)`, 'g'), `url($1${base}/`);
  if (s !== before) { writeFileSync(file, s); n++; }
}
console.log(`prefixed ${n} files with ${base}`);
