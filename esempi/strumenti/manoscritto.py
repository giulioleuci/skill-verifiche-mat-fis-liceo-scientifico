"""Simulazione di elaborati scritti a mano (solo per gli esempi, non fa parte della skill).

Testo disegnato carattere per carattere con font corsivo (Purisa), disturbi di posizione, inclinazione e
inchiostro, su carta a quadretti; effetto foto (prospettiva, ombra, rumore) e effetto scanner (leggera rotazione).
Dipendenze: Pillow, numpy, opencv. Tutto deterministico dal seed."""
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/usr/share/fonts/opentype/tlwg/Purisa-Oblique.otf"
W, H, Q = 1240, 1754, 30           # A4 a 150 dpi, quadretti da 5 mm
BLU, NERO = (22, 38, 120), (28, 28, 38)


def _font(n):
    return ImageFont.truetype(FONT, n)


def carta(rng, quadretti=True):
    im = Image.new("RGB", (W, H), (251, 250, 246))
    d = ImageDraw.Draw(im)
    if quadretti:
        for x in range(0, W, Q):
            d.line([(x, 0), (x, H)], fill=(196, 214, 228), width=1)
        for y in range(0, H, Q):
            d.line([(0, y), (W, y)], fill=(196, 214, 228), width=1)
    d.line([(95, 0), (95, H)], fill=(225, 150, 150), width=2)  # margine
    return im


def _carattere(im, ch, x, y, dim, col, rng):
    """Disegna un carattere ruotato e disturbato; restituisce l'avanzamento in pixel."""
    f = _font(int(dim * rng.uniform(0.94, 1.08)))
    box = f.getbbox(ch if ch.strip() else "n")
    w = (box[2] - box[0]) if ch.strip() else int(dim * 0.38)
    if ch.strip():
        tile = Image.new("L", (dim * 2, dim * 2), 0)
        ImageDraw.Draw(tile).text((dim // 2, dim // 2), ch, font=f, fill=255)
        tile = tile.rotate(rng.uniform(-5, 5), resample=Image.BICUBIC, center=(dim, dim))
        im.paste(Image.new("RGB", tile.size, col), (int(x - dim / 2), int(y - dim * 0.85 + rng.uniform(-2, 2))), tile)
    return w + rng.uniform(1, 3.5) + (box[0] if ch.strip() else 0)


def _radicale(d, x, y, dim, col):
    d.line([(x, y - dim * .35), (x + dim * .12, y - dim * .22), (x + dim * .3, y + dim * .05), (x + dim * .5, y - dim * .75)], fill=col, width=3)
    return x + dim * .5


def riga(im, testo, x, y, dim=34, col=BLU, rng=None, barrato=False):
    """Scrive una riga di testo con '√' come radicale vero (vinculum sul seguito fino allo spazio)."""
    rng = rng or random.Random(1)
    d = ImageDraw.Draw(im)
    x0, vinc, ybase = x, None, y
    for ch in testo:
        ybase += rng.uniform(-0.5, 0.5)
        if ch == "√":
            vinc = _radicale(d, x, ybase, dim, col)
            x += dim * .55
            continue
        if ch == " " and vinc is not None:
            d.line([(vinc, ybase - dim * .78), (x, ybase - dim * .78)], fill=col, width=3)
            vinc = None
        if ch in "≠⇒→":
            for c2 in {"≠": "=/", "⇒": "=>", "→": "->"}[ch]:
                x += _carattere(im, c2, x, ybase, dim, col, rng)
            continue
        x += _carattere(im, ch, x, ybase, dim, col, rng)
    if vinc is not None:
        d.line([(vinc, ybase - dim * .78), (x, ybase - dim * .78)], fill=col, width=3)
    if barrato:  # cancellatura a tratto ondulato
        pts, xx = [], x0 - 4
        while xx < x + 4:
            pts.append((xx, y - dim * .3 + rng.uniform(-7, 7))); xx += 24
        d.line(pts, fill=col, width=3)
    return x


def macchia(im, x, y, w, h, rng):
    """Chiazza di inchiostro che rende illeggibile il testo."""
    d = ImageDraw.Draw(im)
    for _ in range(26):
        cx, cy, r = x + rng.uniform(0, w), y + rng.uniform(-h, 0), rng.uniform(7, 15)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 40, 90))


def pagina(righe, seed, titolo=None, col=BLU, quadretti=True):
    """righe: lista di str oppure (str, {'x': rientro in quadretti, 'barrato': True, 'macchia': True, 'col': ...}).
    Una riga di testo occupa due quadretti. None = riga vuota."""
    rng = random.Random(seed)
    im = carta(rng, quadretti)
    y = 150
    if titolo:
        riga(im, titolo, 110, y, 30, col, rng); y += 2 * Q + 10
    for r in righe:
        if r is None:
            y += Q * 2; continue
        t, o = (r, {}) if isinstance(r, str) else r
        x = 110 + o.get("x", 0) * Q + rng.uniform(-3, 3)
        if y > H - 110:
            break
        if o.get("macchia"):
            riga(im, t, x, y, 34, o.get("col", col), rng); macchia(im, x - 5, y + 4, 330, 44, rng)
        else:
            riga(im, t, x, y, 34, o.get("col", col), rng, barrato=o.get("barrato", False))
        y += Q * 2
    return im.filter(ImageFilter.GaussianBlur(0.7))


def scanner(im, seed, gradi=0.0):
    """Scansione: leggera rotazione, grana, contrasto."""
    rng = np.random.default_rng(seed)
    a = np.asarray(im).astype(np.float32)
    a = a + rng.normal(0, 4, a.shape)
    m = cv2.getRotationMatrix2D((W / 2, H / 2), gradi, 1.0)
    a = cv2.warpAffine(np.clip(a, 0, 255).astype(np.uint8), m, (W, H), borderValue=(235, 235, 235))
    return Image.fromarray(a)


def foto(im, seed):
    """Foto da telefono: prospettiva, ombra di lato, tono caldo, sfondo scuro visibile."""
    rng = np.random.default_rng(seed)
    a = np.asarray(im).astype(np.float32)
    dx, dy = rng.uniform(25, 60, 4), rng.uniform(20, 55, 4)
    src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    dst = np.float32([[dx[0], dy[0]], [W - dx[1], dy[1] * .6], [W - dx[2] * .5, H - dy[2]], [dx[3] * .4, H - dy[3] * .8]])
    out = cv2.warpPerspective(a, cv2.getPerspectiveTransform(src, dst), (W, H), borderValue=(52, 48, 44))
    grad = np.linspace(1.0, rng.uniform(.68, .82), W)[None, :, None]
    out = out * grad * np.array([1.0, .97, .90])[None, None, :]
    out = out + rng.normal(0, 7, out.shape)
    out = cv2.GaussianBlur(np.clip(out, 0, 255).astype(np.uint8), (3, 3), 0)
    return Image.fromarray(out)


def salva_pdf(pagine, path, qualita=62):
    pagine = [p.convert("L") for p in pagine]
    pagine[0].save(path, "PDF", resolution=150, save_all=True, append_images=pagine[1:], quality=qualita)


def salva_jpg(im, path, qualita=70):
    im.save(path, "JPEG", quality=qualita)
