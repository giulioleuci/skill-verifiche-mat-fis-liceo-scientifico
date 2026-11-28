#!/usr/bin/env python3
"""Esempi di quiz: (1) matematica con scansioni simulate (lettura OpenCV, anomalie, correzione e statistiche);
(2) fisica con indicatori e pesi, risposte inserite a mano dal docente. Alunni fittizi.
Esecuzione: python3 genera_quiz.py"""
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from openpyxl import Workbook, load_workbook
from PIL import Image, ImageDraw

QUI = Path(__file__).resolve().parent
SKILL = QUI.parents[1] / "verifiche-mat-fis"
sys.path[:0] = [str(SKILL / "scripts"), str(QUI), str(QUI.parent / "strumenti")]
import manoscritto as M  # noqa: E402
import omr  # noqa: E402
import quiz as quiz_py  # noqa: E402
from domande_quiz import RETTE, URTI  # noqa: E402

COLONNE = ["Testo della domanda", "Risposta corretta", "Alternativa 1", "Alternativa 2", "Alternativa 3", "Alternativa 4", "Numero Colonne Alternative",
           "Punteggio corretta", "Alternative fisse", "Indicatore"]
MM = 200 / 25.4  # pixel per mm nelle immagini di omr.pagine()
quiz = lambda *a: subprocess.run([sys.executable, str(SKILL / "scripts/quiz.py"), *map(str, a)], check=True, capture_output=True, text=True, cwd=SKILL)


def excel(banca, dst, indicatori):
    wb = Workbook(); wb.remove(wb.active)
    for i, righe in enumerate(banca, 1):
        ws = wb.create_sheet(f"D{i:02d}")
        cols = COLONNE if indicatori else COLONNE[:-1]
        ws.append(cols)
        for t, ok, alt, ex in righe:
            r = [t, ok, *alt, *[None] * (4 - len(alt)), ex.get("colonne"), ex.get("corretta"), ex.get("fisse")]
            if indicatori:
                r.append(ex["ind"])
            ws.append(r)
    wb.save(dst)


# ---------------------------------------------------------------- scansioni simulate
def penna(g, cx, cy, rng, forza=1.0):
    """Cerchio annerito a penna: macchia irregolare con tratti incrociati; forza < 1 = solo una traccia."""
    r = int(omr.R * MM)
    if forza < 1:
        cv2.circle(g, (int(cx + rng.uniform(-3, 3)), int(cy + rng.uniform(-3, 3))), int(r * .42), 55, -1)
        return
    cv2.ellipse(g, (int(cx + rng.uniform(-2, 2)), int(cy + rng.uniform(-2, 2))), (int(r * rng.uniform(1.0, 1.18)), int(r * rng.uniform(.95, 1.12))),
                rng.uniform(0, 180), 0, 360, 50, -1)
    for _ in range(3):  # tratti di penna che escono un poco dal cerchio
        a = rng.uniform(0, 6.28)
        cv2.line(g, (int(cx - r * np.cos(a)), int(cy - r * np.sin(a))), (int(cx + r * 1.15 * np.cos(a)), int(cy + r * 1.15 * np.sin(a))), 60, 3)


def nome_a_mano(g, box, testo, rng):
    x0, y0, x1, y1 = (v * MM for v in box)
    im = Image.fromarray(g).convert("RGB")
    M.riga(im, testo, x0 + 20, (y0 + y1) / 2 + 22, 52, M.BLU, rng)
    return np.asarray(im.convert("L")).copy()


def compila_foglio(pdf, chiavi, risposte, nome, seed):
    """Rasterizza il PDF della variante e annerisce il foglio risposte (ultima pagina) secondo `risposte`.
    risposte[n] = lettera, None (vuota), 'AB' (annullata), 'C+' (C annerita e traccia di gomma su un altro cerchio: proposta),
    'D-' (solo un segno debole su D: proposta)."""
    rng = random.Random(seed)
    pag = omr.pagine(pdf)
    g = pag[-1].copy()
    B = chiavi["foglio"]["bolle"]
    for n, r in enumerate(risposte):
        if r is None:
            continue
        forti = [omr.LETTERE.index(c) for c in r.rstrip("+-")]
        for j in forti:
            penna(g, B[n][j][0] * MM, B[n][j][1] * MM, rng, 0.3 if r.endswith("-") else 1.0)
        if r.endswith("+"):
            j2 = next(j for j in range(len(B[n])) if j not in forti)
            penna(g, B[n][j2][0] * MM, B[n][j2][1] * MM, rng, 0.3)
    g = nome_a_mano(g, chiavi["foglio"]["nome"], nome, rng)
    pag[-1] = g
    return pag


def effetto(g, seed, gradi, foto=False, capovolto=False):
    h, w = g.shape
    rng = np.random.default_rng(seed)
    m = cv2.getRotationMatrix2D((w / 2, h / 2), gradi, 0.97)
    out = cv2.warpAffine(g, m, (w, h), borderValue=215)
    if foto:
        src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        dst = np.float32([[16, 12], [w - 8, 22], [w - 22, h - 8], [7, h - 18]])
        out = cv2.warpPerspective(out, cv2.getPerspectiveTransform(src, dst), (w, h), borderValue=175)
        out = (out * np.linspace(1.0, 0.86, w)[None, :]).astype(np.uint8)
    out = np.clip(out.astype(np.float32) + rng.normal(0, 5, out.shape), 0, 255).astype(np.uint8)
    return cv2.rotate(out, cv2.ROTATE_180) if capovolto else out


def risposte_studente(variante, acc, rng, speciali):
    """Lettere per ogni domanda. Errori su una sola alternativa errata per domanda (il distrattore piu' plausibile)."""
    out = []
    for q in variante["domande"]:
        corretta = q["corretta"]
        if rng.random() < acc:
            out.append(corretta)
        else:
            sbagliate = [c for c in "ABCDEFGHIJ"[:len(q["alternative"])] if c != corretta]
            out.append(sbagliate[0] if rng.random() < .7 else rng.choice(sbagliate))
    for n, v in speciali.items():
        out[n - 1] = v
    return out


def scansiona(alunni, V, pdf, scan, rng):
    for n, (nome, iv, acc, sp, fmt) in enumerate(alunni):
        v = V[iv]
        r = risposte_studente(v, acc, rng, sp)
        pag = compila_foglio(pdf(v), v, r, nome, 100 + n)
        base = nome.replace(" ", "_")
        if fmt == "fronteretro":  # PDF intero della variante (domande + foglio), come dalla fotocopiatrice fronte-retro
            ims = [Image.fromarray(effetto(p, 5 + k, .6 * (-1) ** k)).convert("L") for k, p in enumerate(pag)]
            ims[0].save(scan / f"{base}.pdf", "PDF", resolution=200, save_all=True, append_images=ims[1:])
            continue
        g = effetto(pag[-1], n, .9 * (-1) ** n, foto=fmt in ("foto", "ritagliata"), capovolto=fmt == "capovolto")
        if fmt == "ritagliata":  # foto con i quadrati inferiori fuori dall'inquadratura: non leggibile, va rifatta
            g = g[: int(g.shape[0] * .8)]
        if fmt in ("foto", "ritagliata"):
            cv2.imwrite(str(scan / f"{base}.jpg"), g, [cv2.IMWRITE_JPEG_QUALITY, 70])
        else:
            Image.fromarray(g).save(scan / f"{base}.pdf", "PDF", resolution=200)


def report(out, dst):
    """valutazioni.md: per ogni foglio letto, risposta letta, chiave, esito, punteggio e voto (dai file prodotti dalla skill)."""
    ch = {v["codice"]: v for v in json.loads((out / "quiz_chiavi.json").read_text())["varianti"]}
    ris = load_workbook(out / "risposte_scansioni.xlsx" if (out / "risposte_scansioni.xlsx").exists() else out / "risposte_studenti.xlsx").active
    righe = list(ris.iter_rows(values_only=True))
    ST = {r[0]: r for r in load_workbook(out / "quiz_risultati.xlsx")["Studenti"].iter_rows(min_row=2, values_only=True)}
    head = list(load_workbook(out / "quiz_risultati.xlsx")["Studenti"].iter_rows(max_row=1, values_only=True))[0]
    L = ["# Valutazioni automatiche\n", "Lettura (`quiz.py leggi`) e correzione (`quiz.py correggi`); risposta vuota = non data.\n"]
    for r in righe[1:]:
        d = dict(zip(righe[0], r)); v = ch[d["Codice"]]
        s = ST[d["ID"]]; tot = dict(zip(head, s))
        L.append(f"\n## {d['ID']} {d.get('Nome') or ''} (variante {d['Codice']}): {tot['Punteggio']}/{tot['Massimo']}, voto {tot['Voto']}\n")
        L.append("| Domanda | Letta | Chiave | Esito |\n|---:|:-:|:-:|---|")
        for q in v["domande"]:
            x = d.get(q["n"]); esito = "non data" if not x else "annullata" if x == "*" else "corretta" if x == q["corretta"] else "errata"
            L.append(f"| {q['n']} | {x or '-'} | {q['corretta']} | {esito} |")
    Path(dst).write_text("\n".join(L) + "\n", encoding="utf-8")


def quiz_scansioni():
    d = QUI / "01_quiz_matematica_scansioni"
    shutil.rmtree(d, ignore_errors=True); d.mkdir()
    excel(RETTE, d / "domande.xlsx", False)
    out = d / "quiz_out"
    quiz("genera", d / "domande.xlsx", "--varianti", 4, "--errata", -1, "--annullata", 0, "--minimo", 0, "--out", out)
    chiavi = json.loads((out / "quiz_chiavi.json").read_text())
    V = chiavi["varianti"]
    pdf = lambda v: out / f"quiz_{v['codice']}.pdf"
    scan = d / "scansioni"; scan.mkdir()
    rng = random.Random(7)
    # (nome, indice variante, accuratezza, risposte speciali per domanda, formato)
    alunni = [("Alfa Anna", 0, .95, {}, "pdf"), ("Beta Bruno", 1, .7, {}, "pdf"), ("Gamma Chiara", 2, .8, {3: "AB", 6: "C+", 7: "A-", 9: None}, "pdf"),
              ("Delta Davide", 3, .4, {2: None, 4: None, 7: None, 10: None}, "foto"), ("Epsilon Elena", 0, .8, {}, "pdf"),
              ("Zeta Franco", 1, .65, {}, "fronteretro"), ("Eta Gina", 2, .9, {}, "capovolto"), ("Theta Hugo", 3, .55, {8: "BC"}, "pdf"), ("Iota Ilaria", 0, .6, {}, "ritagliata")]
    scansiona(alunni, V, pdf, scan, rng)
    quiz("leggi", scan, "--out", out)
    for f in (out / "letture").glob("*.png"):  # solo per ridurre lo spazio nel repository: metà risoluzione, 48 colori
        im = Image.open(f).convert("RGB")
        im.resize((im.width // 2, im.height // 2)).quantize(48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f, optimize=True)
    an = list(load_workbook(out / "risposte_scansioni.xlsx")["Anomalie"].iter_rows(min_row=2, values_only=True))
    (d / "anomalie_lettura.txt").write_text("\n".join(map(str, an)) + "\n", encoding="utf-8")
    # revisione del docente (quello che fa `quiz.py rivedi` nel browser): conferma le proposte e l'annullamento, segna a mano B dove il foglio e' annullato
    L = json.loads((out / "letture/letture.json").read_text())
    for f in L["fogli"]:
        mod = [{"n": x["n"], "risposta": "B" if (f["file"], x["n"]) == ("Theta_Hugo.pdf", 8) else x["risposta"], "rivista": True}
               for x in f["domande"] if x["stato"] in ("proposta", "annullata")]
        quiz_py.applica_modifiche(L, {"fogli": [{"id": f["id"], "nome": f["nome"], "domande": mod}]})
    quiz_py.scrivi_letture(out, L)
    quiz("correggi", "--out", out, "--risposte", out / "risposte_scansioni.xlsx")
    report(out, d / "valutazioni.md")
    (d / "LEGGIMI.md").write_text(
        "# Quiz di matematica con scansioni\n\n`domande.xlsx` (10 domande, 2 con versioni alternative) -> `quiz.py genera` (4 varianti) -> "
        "fogli compilati a mano simulati in `scansioni/` (PDF singoli, un PDF fronte-retro intero, un JPG da foto, uno capovolto, una foto ritagliata e quindi non leggibile) -> "
        "`quiz.py leggi` (`quiz_out/risposte_scansioni.xlsx`, `quiz_out/letture/`) -> `quiz.py correggi` (`quiz_out/quiz_risultati.xlsx`).\n\n"
        "Il nome è precompilato dal nome del file; l'agente lo confronta con `letture/Sxx_nome.png`. Anomalie della lettura automatica: `anomalie_lettura.txt` "
        "(Gamma Chiara: domanda 3 annullata, 6 proposta C per la gomma, 7 proposta A per un segno debole; Theta Hugo: domanda 8 annullata; la foto di Iota Ilaria non è leggibile perché ritagliata: l'agente chiede al docente una nuova foto e non corregge quel foglio).\n\n"
        "`quiz.py rivedi` apre l'editor nel browser: il docente conferma le proposte, lascia annullata la 3 di Gamma Chiara (`*`: 0 punti con `--annullata 0`) e segna a mano B alla 8 di Theta Hugo. "
        "L'esempio applica le stesse modifiche dallo script; il risultato è in `quiz_out/letture/letture.json` e `risposte_scansioni.xlsx`. "
        "Il quiz è generato con `--errata -1 --annullata 0 --minimo 0` (il totale non scende sotto 0) e la domanda D04 ha `Alternative fisse` = 1: «nessuna delle precedenti» resta sempre in fondo.\n", encoding="utf-8")
    print("quiz matematica:", len(an), "anomalie")


def quiz_indicatori():
    d = QUI / "02_quiz_fisica_indicatori"
    shutil.rmtree(d, ignore_errors=True); d.mkdir()
    excel(URTI, d / "domande.xlsx", True)
    out = d / "quiz_out"
    quiz("genera", d / "domande.xlsx", "--varianti", 3, "--pesi", "ANA=375,SVI=250,ARG=250,COM=125", "--corretta", 4, "--non-data", 1, "--errata", 0, "--out", out)
    chiavi = json.loads((out / "quiz_chiavi.json").read_text())
    V = chiavi["varianti"]
    rng = random.Random(11)
    scan = d / "scansioni"; scan.mkdir()
    pdf = lambda v: out / f"quiz_{v['codice']}.pdf"
    alunni = [("Sigma Sara", 0, .9, {}, "pdf"), ("Tau Tommaso", 1, .6, {}, "foto"), ("Upsilon Ugo", 2, .75, {}, "pdf"),
              ("Phi Fabio", 0, .5, {2: None, 5: None}, "pdf"), ("Chi Carla", 1, .85, {4: "AB"}, "capovolto")]
    scansiona(alunni, V, pdf, scan, rng)
    quiz("leggi", scan, "--out", out)
    for f in (out / "letture").glob("*.png"):
        im = Image.open(f).convert("RGB")
        im.resize((im.width // 2, im.height // 2)).quantize(48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f, optimize=True)
    wb = load_workbook(out / "risposte_scansioni.xlsx"); ws = wb.active  # un alunno senza scansione: il docente aggiunge la riga a mano
    ws.append(["S06", "Omega Olga", V[1]["codice"], *risposte_studente(V[1], .7, rng, {})])
    wb.save(out / "risposte_scansioni.xlsx")
    quiz("correggi", "--out", out, "--risposte", out / "risposte_scansioni.xlsx", "--soglia", 0.6)
    report(out, d / "valutazioni.md")
    (d / "LEGGIMI.md").write_text(
        "# Quiz di fisica con indicatori e scansioni\n\nColonna `Indicatore` per riga; `--pesi ANA=375,SVI=250,ARG=250,COM=125` impone la stessa quota di punti per indicatore in ogni variante: voto dagli indicatori = voto dai punti. "
        "Fogli compilati a mano simulati in `scansioni/` (PDF, foto, foglio capovolto) -> `quiz.py leggi` -> riga aggiunta a mano per un alunno senza scansione (S06) -> `quiz.py correggi --soglia 0.6`. Valutazioni per foglio in `valutazioni.md`.\n", encoding="utf-8")
    print("quiz fisica ok")
    return
    quiz("correggi", "--out", out)
    (d / "LEGGIMI.md").write_text(
        "# Quiz di fisica con indicatori\n\nColonna `Indicatore` per riga; `--pesi ANA=375,SVI=250,ARG=250,COM=125` impone la stessa quota di punti "
        "per indicatore in ogni variante, quindi voto dagli indicatori = voto dai punti. Risposte inserite a mano dal docente in "
        "`quiz_out/risposte_studenti.xlsx` (ID anonimi S01..S05, codice variante, lettera per domanda; cella vuota = non data), poi `quiz.py correggi`.\n",
        encoding="utf-8")
    print("quiz fisica ok")


if __name__ == "__main__":
    quiz_scansioni()
    quiz_indicatori()
