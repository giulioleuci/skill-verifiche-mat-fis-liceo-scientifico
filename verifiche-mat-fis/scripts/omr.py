"""Foglio risposte a cerchi da annerire: geometria, TikZ e lettura da scansione (OpenCV, poppler).

Layout in mm, origine in alto a sinistra, y verso il basso. Quattro quadrati neri agli angoli (il
primo, in alto a sinistra, e' piu' grande) permettono di raddrizzare la scansione; il QR code
contiene il codice della variante. La geometria e' salvata in quiz_chiavi.json: stampa e lettura
usano gli stessi numeri.
"""
import math
import subprocess
import tempfile
from pathlib import Path

W, H = 210, 297
MARKER = {"TL": (12, 12, 10), "TR": (198, 12, 6), "BR": (198, 285, 6), "BL": (12, 285, 6)}  # centro x, y, lato
R, DX, DY = 2.3, 8, 8          # raggio cerchio, passo fra cerchi, passo fra righe
X0, XMAX, Y0, YMAX = 16, 194, 84, 270
PX = 8                          # pixel per mm nell'immagine raddrizzata
PIENO, TRACCIA = 0.5, 0.15      # frazione di pixel scuri: cerchio annerito / traccia di correzione
MARGINE = 2.5                   # cerchio annerito vale risposta se supera di 2,5 volte il secondo segno (gomma + nuova risposta); da tarare su scansioni reali
LETTERE = "ABCDEFGHIJ"
NOME, QR = [20, 33, 138, 45], [150, 18, 190, 58]  # caselle del nome e del QR, mm


def layout(nalt):
    """Posizione dei cerchi per domanda; nalt = numero di alternative di ciascuna domanda."""
    n, nmax = len(nalt), max(nalt)
    larg = 14 + nmax * DX
    blocchi = max(1, int((XMAX - X0 + 6) // (larg + 6)))
    righe = math.ceil(n / blocchi)
    if righe * DY > YMAX - Y0:
        raise SystemExit(f"{n} domande con {nmax} alternative non entrano nel foglio risposte (max {blocchi * int((YMAX - Y0) // DY)})")
    bolle = []
    for i, k in enumerate(nalt):
        x, y = X0 + (i // righe) * (larg + 6), Y0 + (i % righe) * DY
        bolle.append([[x + 14 + j * DX, y] for j in range(k)])
    return {"righe": righe, "larg": larg, "bolle": bolle, "nome": NOME, "qr": QR}


def tikz(v):
    """Pagina del foglio risposte: ultima e di numero pari (con una pagina bianca prima, se serve), cosi' il totale e' pari."""
    f, t = v["foglio"], []
    for x, y, s in MARKER.values():
        t.append(f"\\fill ({x - s / 2},{y - s / 2}) rectangle ({x + s / 2},{y + s / 2});")
    t.append("\\node[anchor=west] at (24,20) {\\large\\textbf{Foglio risposte}};")
    t.append(f"\\node[anchor=west] at (24,25) {{\\small Codice: \\textbf{{{v['codice']}}}}};")
    x0, y0, x1, y1 = f["nome"]
    t.append(f"\\node[anchor=west] at ({x0},{y0 - 2}) {{\\scriptsize Cognome e Nome (stampatello)}};")
    t.append(f"\\draw[line width=0.5pt] ({x0},{y0}) rectangle ({x1},{y1});")
    t.append(f"\\node[anchor=north west,inner sep=0] at ({f['qr'][0]},{f['qr'][1]}) {{\\qrcode[height=36mm,level=M]{{QZ-{v['codice']}}}}};")
    t.append("\\node[anchor=north west,text width=125mm,align=justify] at (20,49) {\\scriptsize Annerisci completamente il cerchio della risposta "
             "scelta con penna nera o blu. Per annullare una risposta annerisci due o più cerchi della domanda. Le correzioni non sono "
             "ammesse: cerchi cancellati, coperti o anneriti in parte possono rendere la domanda non data. Non fare segni fuori dai cerchi.};")
    nmax = max(len(b) for b in f["bolle"])
    for b in range(math.ceil(len(f["bolle"]) / f["righe"])):
        bx = X0 + b * (f["larg"] + 6)
        for j in range(nmax):
            t.append(f"\\node at ({bx + 14 + j * DX},{Y0 - 7}) {{\\small\\textbf{{{LETTERE[j]}}}}};")
    for i, bolle in enumerate(f["bolle"]):
        x, y = bolle[0][0] - 14, bolle[0][1]
        if (i % f["righe"]) % 2 == 0:  # righe alternate in grigio chiaro, solo per guidare l'occhio
            t.append(f"\\fill[black!7] ({x - 2},{y - DY / 2}) rectangle ({x + f['larg'] - 3},{y + DY / 2});")
        t.append(f"\\node[anchor=east] at ({x + 8},{y}) {{\\small\\textbf{{{i + 1}}}}};")
        t += [f"\\draw[line width=0.5pt] ({bx},{by}) circle ({R}mm);" for bx, by in bolle]
    return ("\\clearpage\\ifodd\\value{page}\\thispagestyle{empty}\\null\\clearpage\\fi\n\\thispagestyle{empty}\\null\n"
            "\\begin{tikzpicture}[remember picture,overlay,shift={(current page.north west)},x=1mm,y=-1mm]\n"
            + "\n".join(t) + "\n\\end{tikzpicture}")


# ------------------------------------------------------------------ lettura

def pagine(path):
    """Immagini in grigio (una per pagina) di un PDF o di un'immagine."""
    import cv2
    path = Path(path)
    if path.suffix.lower() != ".pdf":
        g = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        return [g] if g is not None else []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png", str(path), f"{d}/p"], check=True, capture_output=True)
        return [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for p in sorted(Path(d).glob("p*.png"))]


def _marker(g):
    """Centri dei 4 quadrati (TL, TR, BR, BL) e dimensione, oppure None."""
    import cv2
    h, w = g.shape
    s = min(w / W, h / H)
    _, bn = cv2.threshold(cv2.GaussianBlur(g, (5, 5), 0), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cand = []
    for c in cv2.findContours(bn, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
        x, y, cw, ch = cv2.boundingRect(c)
        if 0.8 <= cw / ch <= 1.25 and cv2.contourArea(c) / (cw * ch) > 0.85 and 4.5 * s <= cw <= 12.5 * s:
            cand.append((x + cw / 2, y + ch / 2, cw))
    out = []
    for cx, cy in ((0, 0), (w, 0), (w, h), (0, h)):
        q = [c for c in cand if (c[0] < w / 2) == (cx == 0) and (c[1] < h / 2) == (cy == 0)]
        if not q:
            return None
        out.append(min(q, key=lambda c: math.hypot(c[0] - cx, c[1] - cy)))
    return out


def _raddrizza(g):
    """Immagine raddrizzata a PX pixel/mm con TL in alto a sinistra, oppure None se non e' un foglio risposte."""
    import cv2
    import numpy as np
    for rot in (None, cv2.ROTATE_180):
        gg = g if rot is None else cv2.rotate(g, rot)
        m = _marker(gg)
        if m and m[0][2] > 1.3 * max(c[2] for c in m[1:]):
            src = np.float32([[c[0], c[1]] for c in m])
            dst = np.float32([[x * PX, y * PX] for x, y, _ in MARKER.values()])
            return cv2.warpPerspective(gg, cv2.getPerspectiveTransform(src, dst), (W * PX, H * PX), borderValue=255), gg
    return None


def _qr(w, box, orig):
    import cv2
    x0, y0, x1, y1 = (int(v * PX) for v in box)
    det = cv2.QRCodeDetector()
    for img in (w[y0:y1, x0:x1], orig):
        for k in (1, 2):
            txt = det.detectAndDecode(cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC))[0]
            if txt.startswith("QZ-"):
                return txt[3:]
    return ""


def _riempimento(w, thr, cx, cy):
    import numpy as np
    r = int(R * PX * 0.7)
    x, y = int(cx * PX), int(cy * PX)
    patch = w[y - r:y + r + 1, x - r:x + r + 1]
    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
    return float((patch[xx * xx + yy * yy <= r * r] < thr).mean())


def classifica(fill):
    """(stato, indice della risposta o None, confidenza 0-1) dai riempimenti dei cerchi di una domanda.
    ok = un solo cerchio pieno; proposta = risposta probabile da confermare (segno unico debole, o cerchio pieno
    con tracce molto piu' deboli); annullata = segni confusi o due cerchi pieni; vuota = nessun segno."""
    o = sorted(range(len(fill)), key=fill.__getitem__, reverse=True)
    m1, m2 = fill[o[0]], (fill[o[1]] if len(fill) > 1 else 0.0)
    if m1 < TRACCIA:
        return "vuota", None, 1.0
    conf = round((1 - m2 / m1) * min(1.0, m1 / PIENO), 2)
    if m2 < TRACCIA:
        return ("ok" if m1 >= PIENO else "proposta"), o[0], conf
    if m1 >= PIENO and m1 >= MARGINE * m2:
        return "proposta", o[0], conf
    return "annullata", None, 0.0


def leggi_pagina(g, per_codice):
    """None se la pagina non e' un foglio risposte; altrimenti dict con codice, domande (stato, riempimenti, confidenza), immagini."""
    import numpy as np
    rr = _raddrizza(g)
    if rr is None:
        return None
    w, orig = rr
    codice = _qr(w, QR, orig)
    res = {"codice": codice, "domande": [], "nome": w[NOME[1] * PX:NOME[3] * PX, NOME[0] * PX:NOME[2] * PX], "img": w}
    if codice not in per_codice:
        res["errore"] = "codice variante non letto" if not codice else f"codice {codice!r} sconosciuto"
        res["codice"] = ""
        return res
    thr = 0.6 * float(np.percentile(w[Y0 * PX:YMAX * PX, X0 * PX:XMAX * PX], 95))
    for n, bolle in enumerate(per_codice[codice]["foglio"]["bolle"], start=1):
        fill = [round(_riempimento(w, thr, x, y), 2) for x, y in bolle]
        stato, k, conf = classifica(fill)
        res["domande"].append({"n": n, "stato": stato, "fill": fill, "conf": conf, "risposta": LETTERE[k] if k is not None else "*" if stato == "annullata" else "", "rivista": False})
    return res
