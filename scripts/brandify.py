"""Brand image treatments for the JOP site, in the JOP brown palette.

Commands
  python3 scripts/brandify.py scene in.jpg brown|navy|umber out.jpg
      Photo -> halftone tritone (espresso -> tone -> paper). Used for the
      selected-assignment photos.
  python3 scripts/brandify.py portrait in.png brown|navy|umber out.jpg
      Cut-out (RGBA) or black-background portrait -> 4:5 card image on
      espresso with the navy/brown terrain behind.
  python3 scripts/brandify.py placeholder brown|navy|umber out.jpg
      Silhouette portrait for people without a photograph.
  python3 scripts/brandify.py retone in.jpg out.jpg [illustration|portrait]
      Re-colour an existing illustration from the old wine/slate/ochre
      palette into brown/navy/caramel, warming neutrals to espresso and paper.
  python3 scripts/brandify.py monotone in.jpg out.jpg
      Any image -> dark brown monochrome (used for the home hero aerial).
"""
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter, ImageChops
import math, sys

def hx(s):
    s = s.lstrip('#'); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))

# ---- JOP palette (mirrors src/styles/global.css) ---------------------------
ESPRESSO   = hx('#292221')
ESPRESSO_2 = hx('#211B1A')
BROWN      = hx('#A67970')   # JOP brand brown, from the original joripbd.com
BROWN_DEEP = hx('#795149')
BROWN_DARK = hx('#563934')
NAVY       = hx('#3D506D')   # JOP's second colour, from the original site
PAPER      = hx('#E9E1E0')
PAPER_2    = hx('#F6F2F1')
TONES = {'brown': BROWN_DEEP, 'navy': NAVY, 'umber': BROWN_DARK}

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---- core treatments --------------------------------------------------------
def tritone(gray, tone, cell=6, dot=0.55, mid=0.55):
    g = ImageEnhance.Contrast(gray).enhance(1.2); g = ImageOps.autocontrast(g, cutoff=1)
    lut = [(lerp(ESPRESSO, tone, (v / 255) / mid) if v / 255 < mid else lerp(tone, PAPER, ((v / 255) - mid) / (1 - mid))) for v in range(256)]
    tri = Image.merge('RGB', [g.point([c[i] for c in lut]) for i in range(3)])
    small = g.resize((max(1, g.size[0] // cell), max(1, g.size[1] // cell)), Image.BOX)
    screen = Image.new('L', g.size, 255); d = ImageDraw.Draw(screen); sp = small.load()
    for j in range(small.size[1]):
        for i in range(small.size[0]):
            dark = 1 - sp[i, j] / 255; r = (cell * 0.62) * math.sqrt(dark)
            if r > 0.6:
                cx = i * cell + cell / 2 + (cell / 2 if j % 2 else 0); cy = j * cell + cell / 2
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)
    screen = screen.filter(ImageFilter.GaussianBlur(0.4))
    return Image.composite(tri, Image.blend(tri, Image.new('RGB', g.size, ESPRESSO), dot), screen)

def grain(img, amt=0.06):
    noise = Image.effect_noise(img.size, 28).convert('L')
    return Image.blend(img, Image.merge('RGB', (noise, noise, noise)), amt)

def ridges(canvas, W, H, base_y):
    """Navy back ridge, JOP-brown front ridge, both hatched, with a levelling line."""
    def ridge(points, color, hatch_alpha):
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(layer).polygon(points, fill=color + (255,))
        hl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
        for k in range(-H, W + H, 6): hd.line([(k, 0), (k + H, H)], fill=(255, 255, 255, hatch_alpha), width=1)
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(points, fill=255)
        hl.putalpha(ImageChops.multiply(hl.getchannel('A'), m))
        return Image.alpha_composite(canvas, Image.alpha_composite(layer, hl))
    y = base_y
    canvas = ridge([(0, y + 70), (W * 0.13, y), (W * 0.28, y + 40), (W * 0.45, y - 40), (W * 0.63, y + 30), (W * 0.8, y - 20), (W, y + 20), (W, H), (0, H)], NAVY, 36)
    y2 = base_y + 130
    canvas = ridge([(0, y2 + 60), (W * 0.16, y2), (W * 0.33, y2 + 40), (W * 0.52, y2 - 30), (W * 0.7, y2 + 30), (W * 0.87, y2 - 10), (W, y2 + 20), (W, H), (0, H)], BROWN, 34)
    td = ImageDraw.Draw(canvas); pts = [(W * 0.16, y2), (W * 0.52, y2 - 30), (W * 0.87, y2 - 10)]
    for a, b in zip(pts, pts[1:]):
        n = int(math.dist(a, b) / 14)
        for k in range(0, n, 2):
            t0 = k / n; t1 = min((k + 1) / n, 1)
            td.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=(255, 255, 255, 150), width=2)
    for x, yy in pts: td.ellipse((x - 6, yy - 6, x + 6, yy + 6), fill=ESPRESSO, outline=(255, 255, 255), width=2)
    return canvas

def subject_mask(rgba_or_rgb, pw, ph):
    """Alpha from RGBA; else flood-fill the near-black background."""
    if rgba_or_rgb.mode == 'RGBA':
        return rgba_or_rgb.getchannel('A').resize((pw, ph), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    raw = ImageOps.grayscale(rgba_or_rgb.resize((pw, ph), Image.LANCZOS))
    binm = raw.point(lambda v: 255 if v <= 16 else 0).filter(ImageFilter.MinFilter(3))
    for c in [(1, 1), (pw - 2, 1), (1, ph // 2), (pw - 2, ph // 2)]:
        ImageDraw.floodfill(binm, c, 128, thresh=0)
    return binm.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))

def portrait(src, tone_name, out, width_frac=0.66, W=1200, H=1500, bottom_pad=16):
    src = Image.open(src) if isinstance(src, str) else src
    pw = int(W * width_frac); ph = int(pw * src.size[1] / src.size[0])
    rgb = src.convert('RGB').resize((pw, ph), Image.LANCZOS)
    mask = subject_mask(src, pw, ph)
    edge = Image.new('L', (pw, ph), 255); ed = ImageDraw.Draw(edge)
    for k in range(28):
        v = int(255 * k / 28); ed.line((k, 0, k, ph), fill=v); ed.line((pw - 1 - k, 0, pw - 1 - k, ph), fill=v)
    mask = ImageChops.multiply(mask, edge)
    tri = tritone(ImageOps.grayscale(rgb), BROWN)
    canvas = ridges(Image.new('RGBA', (W, H), ESPRESSO + (255,)), W, H, int(H * 0.58)).convert('RGB')
    canvas.paste(tri, ((W - pw) // 2, H - ph + bottom_pad), mask)
    grain(canvas).save(out, quality=86, optimize=True, progressive=True)

def placeholder(tone_name, out, W=1200, H=1500):
    tone = TONES[tone_name]
    canvas = ridges(Image.new('RGBA', (W, H), ESPRESSO + (255,)), W, H, int(H * 0.58))
    sil = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sil)
    cx = W // 2; hr = int(W * 0.145); hy = int(H * 0.50)
    sd.ellipse((cx - hr, hy - hr, cx + hr, hy + hr), fill=PAPER + (255,))
    sd.rounded_rectangle((cx - int(W * 0.38), hy + hr + 50, cx + int(W * 0.38), H + 400), radius=int(W * 0.24), fill=PAPER + (255,))
    sd.rectangle((cx - int(W * 0.05), hy + hr - 30, cx + int(W * 0.05), hy + hr + 60), fill=PAPER + (255,))
    hl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    for k in range(-H, W + H, 7): hd.line([(k, 0), (k + H, H)], fill=tone + (120,), width=2)
    hl.putalpha(ImageChops.multiply(hl.getchannel('A'), sil.getchannel('A')))
    canvas = Image.alpha_composite(Image.alpha_composite(canvas, sil), hl).convert('RGB')
    grain(canvas).save(out, quality=86, optimize=True, progressive=True)

def scene(src, tone_name, out, width=1200):
    im = Image.open(src).convert('RGB')
    im = im.resize((width, int(im.size[1] * width / im.size[0])), Image.LANCZOS)
    tri = tritone(ImageOps.grayscale(im), TONES[tone_name], cell=7, dot=0.42, mid=0.42)
    grain(tri, 0.07).save(out, quality=84, optimize=True, progressive=True)

# ---- palette remap for existing illustrations ------------------------------
def _band(deg, lo0, lo1, hi1, hi0):
    """1 inside [lo1, hi1], cosine ramps to 0 at lo0 and hi0 (degrees, may wrap)."""
    def inside(d, a, b): return (a <= d <= b) if a <= b else (d >= a or d <= b)
    def dist(a, b): return (b - a) % 360
    if inside(deg, lo1, hi1): return 1.0
    if inside(deg, lo0, lo1): t = dist(lo0, deg) / max(1e-6, dist(lo0, lo1)); return 0.5 - 0.5 * math.cos(math.pi * t)
    if inside(deg, hi1, hi0): t = dist(deg, hi0) / max(1e-6, dist(hi1, hi0)); return 0.5 - 0.5 * math.cos(math.pi * t)
    return 0.0

def _circ(a, b):
    """Signed shortest angle from a to b, degrees."""
    return (b - a + 180) % 360 - 180

def retone(src, out, mode='illustration'):
    img = Image.open(src).convert('RGB')
    if mode == 'portrait':
        # treated portraits: slate figure -> sepia brown, wine ridge -> navy
        bands = [((285, 305, 10, 30), 216, 0.80, 0.95),   # red/wine -> navy
                 ((175, 190, 245, 262), 12, 0.75, 1.00),   # blue/slate -> brown
                 ((30, 38, 58, 70), 24, 0.60, 0.95)]       # ochre -> caramel
    else:
        bands = [((285, 305, 12, 28), 10, 0.52, 1.14),    # red/wine -> JOP brown, lighter, softer
                 ((28, 36, 58, 70), 24, 0.62, 0.96),       # ochre/gold -> caramel
                 ((175, 190, 245, 262), 216, 0.80, 0.95)]  # slate/blue -> JOP navy
    lut_h, lut_s, lut_vf, lut_vk = [], [], [], []
    for h in range(256):
        deg = h * 360 / 256; nd = deg; sf = 1.0; vf = 1.0
        for (lo0, lo1, hi1, hi0), tgt, s_fac, v_fac in bands:
            w = _band(deg, lo0, lo1, hi1, hi0)
            if w:
                nd += w * _circ(deg, tgt); sf += w * (s_fac - 1); vf += w * (v_fac - 1)
        lut_h.append(int(round(nd * 256 / 360)) % 256)
        lut_s.append(int(max(0, min(1, sf)) * 255))
        lut_vf.append(int(min(1, vf) * 255)); lut_vk.append(int(max(0, vf - 1) * 255))
    H, S, V = img.convert('HSV').split()
    H2 = H.point(lut_h)
    S2 = ImageChops.multiply(S, H.point(lut_s))
    V2 = ImageChops.add(ImageChops.multiply(V, H.point(lut_vf)), ImageChops.multiply(V, H.point(lut_vk)))
    recon = Image.merge('HSV', (H2, S2, V2)).convert('RGB')
    # neutrals (charcoal grounds, pale papers, whites) -> warm espresso / paper
    # luminance-preserving warm ramp: grey value v comes back at about the same
    # lightness, just warmer (charcoal -> espresso, pale blue -> warm paper)
    sepia = ImageOps.colorize(img.convert('L'), black=hx('#050302'), mid=hx('#8E7872'), white=hx('#FBF6F4'))
    mask = S.point(lambda s: 255 if s < 34 else (0 if s > 82 else int(255 * (82 - s) / 48)))
    Image.composite(sepia, recon, mask).save(out, quality=84, optimize=True, progressive=True)

def monotone(src, out, black='#181312', mid='#5A4743', white='#D9CBC7'):
    img = Image.open(src).convert('L')
    ImageOps.colorize(img, black=black, mid=mid, white=white).save(out, quality=82, optimize=True, progressive=True)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'scene': scene(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'portrait': portrait(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'placeholder': placeholder(sys.argv[2], sys.argv[3])
    elif cmd == 'retone': retone(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else 'illustration')
    elif cmd == 'monotone': monotone(sys.argv[2], sys.argv[3])
