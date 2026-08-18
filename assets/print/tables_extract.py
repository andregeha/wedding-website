"""Extraction helpers for the scanned table calligraphy (grey pencil) + drawings (blue pen).
Names -> darkness mask. Drawings -> blueness|darkness mask. No scipy: BFS components on a
downscaled mask. Output can be recoloured to a single ink tone (monochrome cards)."""
import numpy as np
from PIL import Image
from collections import deque
import os
import fitz

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tables-source.pdf')
INK = (43, 43, 41)

_cache = {}
def page_rgb(pno, dpi=300):
    key = (pno, dpi)
    if key not in _cache:
        d = fitz.open(PDF)
        pix = d[pno-1].get_pixmap(dpi=dpi)
        _cache[key] = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        d.close()
    return _cache[key]

def _gray(a):
    return 0.299*a[..., 0] + 0.587*a[..., 1] + 0.114*a[..., 2]

def draw_mask(rgb, blue_thr=12, dark_thr=95):
    a = np.asarray(rgb).astype(np.int16)
    return ((a[..., 2]-a[..., 0]) > blue_thr) | (_gray(a) < dark_thr)

def name_mask(rgb, delta=42):
    a = np.asarray(rgb).astype(np.int16)
    g = _gray(a); paper = np.percentile(g, 90)
    return g < (paper - delta)

def _comps(mask, scale=6):
    h, w = mask.shape; sh, sw = h//scale, w//scale
    small = np.asarray(Image.fromarray(mask.astype(np.uint8)*255).resize((sw, sh), Image.BOX)) > 60
    seen = np.zeros_like(small, bool); out = []
    for i in range(sh):
        for j in range(sw):
            if small[i, j] and not seen[i, j]:
                q = deque([(i, j)]); seen[i, j] = True; pts = []
                while q:
                    y, x = q.popleft(); pts.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < sh and 0 <= nx < sw and small[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                out.append(dict(n=len(pts), y0=min(ys), y1=max(ys)+1, x0=min(xs), x1=max(xs)+1))
    return out, scale

# ---------- names ----------
def name_boxes(pno, dpi=200, mf=0.060):
    rgb = page_rgb(pno, dpi); W, H = rgb.size
    mx, my = int(W*0.06), int(H*0.02)
    sub = rgb.crop((mx, my, W-mx, H-my))
    comps, scale = _comps(name_mask(sub), 6)
    comps = [c for c in comps if c['n'] >= 5]
    comps.sort(key=lambda c: c['y0'])
    merge = (sub.size[1]//6)*mf; lines = []
    for c in comps:
        placed = False
        for L in lines:
            if c['y0'] <= L['y1']+merge and c['y1'] >= L['y0']-merge:
                L['y0'] = min(L['y0'], c['y0']); L['y1'] = max(L['y1'], c['y1'])
                L['x0'] = min(L['x0'], c['x0']); L['x1'] = max(L['x1'], c['x1']); placed = True; break
        if not placed: lines.append(dict(**c))
    lines.sort(key=lambda L: L['y0'])
    return rgb, mx, my, scale, lines

def extract_name(pno, idx, dpi=300, padx=0.03, pady=0.10, mono=True, ink=INK):
    """idx = 0-based line within the page (top->bottom). Returns RGBA."""
    rgb, mx, my, scale, lines = name_boxes(pno, dpi=dpi)
    L = lines[idx]
    x0 = mx + L['x0']*scale; y0 = my + L['y0']*scale
    x1 = mx + L['x1']*scale; y1 = my + L['y1']*scale
    pw = int((x1-x0)*padx); ph = int((y1-y0)*pady)
    x0 = max(0, x0-pw); y0 = max(0, y0-ph); x1 = min(rgb.size[0], x1+pw); y1 = min(rgb.size[1], y1+ph)
    crop = rgb.crop((x0, y0, x1, y1))
    return _mono(crop, 'name', ink) if mono else crop

# ---------- drawings ----------
def extract_drawing(pno, dpi=300, left_crop=0.11, margin=0.02, pad=0.03, mono=True, rotate=0, ink=INK):
    rgb = page_rgb(pno, dpi); W, H = rgb.size
    x0c = int(W*left_crop); mx = int(W*margin); my = int(H*margin)
    sub = rgb.crop((x0c+mx, my, W-mx, H-my))
    comps, scale = _comps(draw_mask(sub), 8)
    if not comps: return None
    comps.sort(key=lambda c: c['n'], reverse=True)
    big = comps[0]['n']; keep = [c for c in comps if c['n'] >= max(1, big*0.02)]
    x0 = min(c['x0'] for c in keep)*scale; y0 = min(c['y0'] for c in keep)*scale
    x1 = max(c['x1'] for c in keep)*scale; y1 = max(c['y1'] for c in keep)*scale
    pw, ph = int((x1-x0)*pad), int((y1-y0)*pad)
    x0 = max(0, x0-pw); y0 = max(0, y0-ph); x1 = min(sub.size[0], x1+pw); y1 = min(sub.size[1], y1+ph)
    crop = sub.crop((x0, y0, x1, y1))
    img = _mono(crop, 'draw', ink) if mono else crop
    if rotate: img = img.rotate(rotate, expand=True, resample=Image.BICUBIC)
    return img

# ---------- recolour to ink ----------
def _mono(rgb, kind, ink=INK):
    """ink = (r,g,b) flat recolour, or None to keep the original scanned colour
    (used for the 'couleur bleue originale' drawings)."""
    a = np.asarray(rgb.convert('RGB')).astype(np.int16)
    g = _gray(a)
    if kind == 'draw':
        blueness = np.clip(a[..., 2]-a[..., 0], 0, 255)
        alpha = np.maximum(np.clip((255-g)*1.15, 0, 255), np.clip(blueness*4.0, 0, 255))
        alpha = (np.clip(alpha, 0, 255)/255.0)**0.85*255.0
        alpha[alpha < 26] = 0
    else:
        paper = np.percentile(g, 92)
        alpha = np.clip((paper-g)*2.4, 0, 255)          # darken the light pencil
        alpha = (np.clip(alpha, 0, 255)/255.0)**0.75*255.0
        alpha[alpha < 22] = 0
    out = np.zeros((*g.shape, 4), np.uint8)
    if ink is None:                                     # keep original blue, punchier
        src = np.asarray(rgb.convert('RGB')).astype(np.float32)
        mean = src.mean(2, keepdims=True)
        src = np.clip(mean + (src-mean)*1.45, 0, 255)   # +saturation so the blue reads
        out[..., :3] = src.astype(np.uint8)
    else:
        out[..., 0], out[..., 1], out[..., 2] = ink
    out[..., 3] = alpha.astype(np.uint8)
    return Image.fromarray(out, 'RGBA')
