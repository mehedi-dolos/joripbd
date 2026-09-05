"""Brand image treatments for the JOP site.
tritone(img, tone) -> halftone tritone RGB image (charcoal -> tone -> paper)
portrait(src_rgba_or_black_bg, tone, out) -> 4:5 portrait on charcoal with hatched ridges
placeholder(tone, out) -> 4:5 silhouette portrait
scene(src, tone, out, size) -> treated landscape photo
"""
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter, ImageChops
import math, sys

CH=(0x27,0x26,0x24); WINE=(0x8C,0x2B,0x4C); SLATE=(0x5A,0x6F,0x8A); NAVY=(0x3A,0x44,0x68); PAPER=(0xDC,0xE3,0xE8); DEEP=(0x41,0x54,0x69)
TONES={'wine':WINE,'slate':SLATE,'navy':NAVY}

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def tritone(gray, tone, cell=6, dot=0.55, mid=0.55):
    g = ImageEnhance.Contrast(gray).enhance(1.2); g = ImageOps.autocontrast(g, cutoff=1)
    lut=[(lerp(CH,tone,(v/255)/mid) if v/255<mid else lerp(tone,PAPER,((v/255)-mid)/(1-mid))) for v in range(256)]
    tri = Image.new('RGB', g.size); px=g.load(); tp=tri.load()
    for y in range(g.size[1]):
        for x in range(g.size[0]): tp[x,y]=lut[px[x,y]]
    small=g.resize((max(1,g.size[0]//cell), max(1,g.size[1]//cell)), Image.BOX)
    screen=Image.new('L', g.size, 255); d=ImageDraw.Draw(screen); sp=small.load()
    for j in range(small.size[1]):
        for i in range(small.size[0]):
            dark=1-sp[i,j]/255; r=(cell*0.62)*math.sqrt(dark)
            if r>0.6:
                cx=i*cell+cell/2+(cell/2 if j%2 else 0); cy=j*cell+cell/2
                d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=0)
    screen=screen.filter(ImageFilter.GaussianBlur(0.4))
    return Image.composite(tri, Image.blend(tri, Image.new('RGB', g.size, CH), dot), screen)

def grain(img, amt=0.06):
    noise=Image.effect_noise(img.size,28).convert('L')
    return Image.blend(img, Image.merge('RGB',(noise,noise,noise)), amt)

def ridges(canvas, W, H, base_y, tone):
    def ridge(points,color,hatch_alpha):
        layer=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(layer).polygon(points, fill=color+(255,))
        hl=Image.new('RGBA',(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hl)
        for k in range(-H,W+H,6): hd.line([(k,0),(k+H,H)], fill=(255,255,255,hatch_alpha), width=1)
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(points, fill=255)
        hl.putalpha(ImageChops.multiply(hl.getchannel('A'), m))
        return Image.alpha_composite(canvas, Image.alpha_composite(layer, hl))
    y=base_y
    canvas=ridge([(0,y+70),(W*0.13,y),(W*0.28,y+40),(W*0.45,y-40),(W*0.63,y+30),(W*0.8,y-20),(W,y+20),(W,H),(0,H)], DEEP, 36)
    y2=base_y+130
    front = tone if tone!=SLATE else WINE
    canvas=ridge([(0,y2+60),(W*0.16,y2),(W*0.33,y2+40),(W*0.52,y2-30),(W*0.7,y2+30),(W*0.87,y2-10),(W,y2+20),(W,H),(0,H)], front, 42)
    td=ImageDraw.Draw(canvas); pts=[(W*0.16,y2),(W*0.52,y2-30),(W*0.87,y2-10)]
    for a,b in zip(pts,pts[1:]):
        n=int(math.dist(a,b)/14)
        for k in range(0,n,2):
            t0=k/n; t1=min((k+1)/n,1)
            td.line([(a[0]+(b[0]-a[0])*t0,a[1]+(b[1]-a[1])*t0),(a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1)], fill=(255,255,255,150), width=2)
    for x,yy in pts: td.ellipse((x-6,yy-6,x+6,yy+6), fill=CH, outline=(255,255,255), width=2)
    return canvas

def subject_mask(rgba_or_rgb, pw, ph):
    """Alpha from RGBA; else flood-fill the near-black background."""
    if rgba_or_rgb.mode=='RGBA':
        a = rgba_or_rgb.getchannel('A').resize((pw,ph), Image.LANCZOS)
        return a.filter(ImageFilter.GaussianBlur(0.8))
    raw = ImageOps.grayscale(rgba_or_rgb.resize((pw,ph), Image.LANCZOS))
    binm = raw.point(lambda v: 255 if v <= 16 else 0).filter(ImageFilter.MinFilter(3))
    for c in [(1,1),(pw-2,1),(1,ph//2),(pw-2,ph//2)]:
        ImageDraw.floodfill(binm, c, 128, thresh=0)
    return binm.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))

def portrait(src, tone_name, out, width_frac=0.66, W=1200, H=1500, bottom_pad=16):
    tone=TONES[tone_name]
    src = Image.open(src) if isinstance(src,str) else src
    pw = int(W*width_frac); ph = int(pw*src.size[1]/src.size[0])
    rgb = src.convert('RGB').resize((pw,ph), Image.LANCZOS)
    mask = subject_mask(src, pw, ph)
    # side fade
    edge = Image.new('L', (pw,ph), 255); ed = ImageDraw.Draw(edge)
    for k in range(28):
        v=int(255*k/28); ed.line((k,0,k,ph), fill=v); ed.line((pw-1-k,0,pw-1-k,ph), fill=v)
    mask = ImageChops.multiply(mask, edge)
    tri = tritone(ImageOps.grayscale(rgb), SLATE)
    canvas = Image.new('RGBA',(W,H),CH+(255,))
    canvas = ridges(canvas, W, H, int(H*0.58), tone).convert('RGB')
    canvas.paste(tri, ((W-pw)//2, H-ph+bottom_pad), mask)
    canvas = grain(canvas)
    canvas.save(out, quality=86, optimize=True, progressive=True)
    return canvas

def placeholder(tone_name, out, W=1200, H=1500):
    tone=TONES[tone_name]
    canvas = Image.new('RGBA',(W,H),CH+(255,))
    canvas = ridges(canvas, W, H, int(H*0.58), tone)
    # silhouette bust in paper with hatch
    sil = Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sil)
    cx=W//2; hr=int(W*0.145); hy=int(H*0.50)
    sd.ellipse((cx-hr,hy-hr,cx+hr,hy+hr), fill=PAPER+(255,))
    sd.rounded_rectangle((cx-int(W*0.38),hy+hr+50,cx+int(W*0.38),H+400), radius=int(W*0.24), fill=PAPER+(255,))
    sd.rectangle((cx-int(W*0.05),hy+hr-30,cx+int(W*0.05),hy+hr+60), fill=PAPER+(255,))
    hl=Image.new('RGBA',(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hl)
    for k in range(-H,W+H,7): hd.line([(k,0),(k+H,H)], fill=tone+(120,), width=2)
    hl.putalpha(ImageChops.multiply(hl.getchannel('A'), sil.getchannel('A')))
    canvas = Image.alpha_composite(Image.alpha_composite(canvas, sil), hl).convert('RGB')
    canvas = grain(canvas)
    canvas.save(out, quality=86, optimize=True, progressive=True)

def scene(src, tone_name, out, width=1200):
    tone=TONES[tone_name]
    im = Image.open(src).convert('RGB')
    im = im.resize((width, int(im.size[1]*width/im.size[0])), Image.LANCZOS)
    tri = tritone(ImageOps.grayscale(im), tone, cell=7, dot=0.42, mid=0.42)
    grain(tri, 0.07).save(out, quality=84, optimize=True, progressive=True)

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='scene': scene(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd=='portrait': portrait(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd=='placeholder': placeholder(sys.argv[2], sys.argv[3])
