#!/usr/bin/env python3
"""Flusso `correggi` dell'esempio 01: scansioni simulate (a mano) -> correzioni.json -> schede PDF ->
riepilogo Excel, correttore per alunno, fascicolo. Alunni fittizi. Esecuzione: python3 build_correzione.py"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[2]
SKILL = RADICE / "verifiche-mat-fis"
sys.path[:0] = [str(SKILL / "scripts"), str(RADICE / "esempi" / "strumenti"), str(QUI)]
import correzione as C  # noqa: E402
import manoscritto as M  # noqa: E402
from elaborati import ELAB  # noqa: E402

ARGOMENTO, CLASSE, DATA = "Rette e fasci", "3X", "27/11/2026"
NOTE = {
    "A": "- Esempio Anna, Prova Bruno, Demo Elena, Finto Davide e Modello Chiara: versione A confermata da intestazione e dati (A(-2,1), B(4,3)).\n"
         "- Modello Chiara: cancellatura al punto 1c non valutata; asterisco del punto 3 seguito a pagina 2.\n"
         "- Demo Elena: foto in 2 file (`_1`, `_2`); il secondo metodo dell'area ha un errore di segno non individuato dall'alunna.\n"
         "- Prova Bruno: risultato di 1b coerente con l'errore di segno (non trascinato oltre).\n"
         "- Finto Davide: elaborato quasi in bianco; un solo tentativo errato = voto 2.\n"
         "- Nessuna risposta identica o quasi tra alunni diversi.\n",
    "B": "- Campione Franco: file con prefisso `B_` nella consegna del docente. Saggio Gina: file senza prefisso, assegnata alla versione B dai dati (A(-1,-2), B(5,2)); confermato dal docente.\n"
         "- Saggio Gina: nessun risultato giusto con passaggi sbagliati; la foto ha ombra a sinistra ma è leggibile.\n"
         "- Nessuna risposta identica o quasi tra alunni diversi.\n",
}


def pdflatex(tex, cartella):
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(cartella), str(tex)],
                       check=True, capture_output=True)
    for e in ("aux", "log", "out"):
        (cartella / f"{tex.stem}.{e}").unlink(missing_ok=True)


def scansioni(v, dst):
    """Un formato diverso per alunno: PDF scanner, PDF da foto, sottocartella di foto, JPG singolo, JPG numerati."""
    shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
    for n, (nome, e) in enumerate(ELAB[v].items()):
        base = nome.replace(" ", "_")
        pag = [M.pagina(r, 1000 * ord(v) + 10 * n + k, titolo=f"{nome}   {CLASSE}   {DATA}" if k == 0 else None,
                        col=M.BLU if n % 2 == 0 else M.NERO) for k, r in enumerate(e["pagine"])]
        eff = (lambda im, s: M.scanner(im, s, (-1) ** n * 0.8)) if e["effetto"] == "scanner" else M.foto
        img = [eff(p, 7 * n + k) for k, p in enumerate(pag)]
        if e["formato"] == "pdf":
            M.salva_pdf(img, dst / f"{base}.pdf")
        elif e["formato"] == "cartella":
            (dst / base).mkdir()
            for k, i in enumerate(img, 1):
                M.salva_jpg(i, dst / base / f"{k}.jpg")
        elif e["formato"] == "jpg":
            M.salva_jpg(img[0], dst / f"{base}.jpg")
        else:
            for k, i in enumerate(img, 1):
                M.salva_jpg(i, dst / f"{base}_{k}.jpg")


def pt(x):
    return f"{x:.1f}".replace(".", ",").removesuffix(",0")


def scheda(v, nome, e, calc, rows, risultati):
    es = [x for x in calc["per_es"] if x != "Intero elaborato"]
    mx = {k: sum(r["Max"] for r in rows if str(r["Esercizio"]) == k) for k in calc["per_es"]}
    etic = calc["voto"][0].replace("½", r"\ensuremath{\tfrac12}")
    t = (SKILL / "assets" / "scheda_alunno_template.tex").read_text(encoding="utf-8")
    pre, _ = t.split(r"\begin{document}")
    tab = "".join(f"Esercizio {k} & {pt(calc['per_es'][k])} & {mx[k]} \\\\\n" for k in es)
    tab += f"Intero elaborato & {pt(calc['per_es']['Intero elaborato'])} & {mx['Intero elaborato']} \\\\\n"
    body = rf"""\begin{{document}}
{{\Large\bfseries Verifica \textsc{{{ARGOMENTO}}} --- {nome.upper()}}}\\
Classe {CLASSE} \quad Data {DATA} \quad Punteggio massimo 1000

\medskip
\begin{{tabular}}{{@{{}}lrr@{{}}}}\toprule
 & Punti & Massimo\\\midrule
{tab} \midrule \textbf{{Totale}} & \textbf{{{pt(calc['totale'])}}} & 1000\\\bottomrule
\end{{tabular}}
\hfill {{\Large\bfseries Voto: {etic}}}
"""
    for k in es:
        ok, ko = e["schede"][k]
        okt = "".join(f"\\ok {x}\n" for x in ok) or "\\ok ---\n"
        kot = "".join(f"\\ko {x}\n" for x in ko) or "\\ko ---\n"
        body += f"\n\\esercizio{{{k}}}{{{pt(calc['per_es'][k])} / {mx[k]}}}\n\\esito{{{okt}}}{{{kot}}}\n"
    body += "\n\\medskip\\textbf{Aree di miglioramento}\n\\begin{itemize}[label=$\\rightarrow$]\n" + "".join(f" \\item {x}\n" for x in e["aree"]) + "\\end{itemize}\n"
    body += (rf"\medskip{{\small Calcolo: punti {pt(calc['totale'])}, dopo la divisione per 100, arrotondati a 0,25 \(\Rightarrow\) {etic}.}}" "\n\\end{document}\n")
    tex = risultati / f"{ARGOMENTO}_{nome}.tex"
    tex.write_text(pre + body, encoding="utf-8")
    pdflatex(tex, risultati)
    tex.unlink()


def versione(v):
    cart = QUI / v
    cart.mkdir(exist_ok=True)
    reg = cart / "registro_evidenze.xlsx"
    shutil.copy(RADICE / "esempi/01_matematica_rette/registri" / f"registro_{v}.xlsx", reg)  # approvato, invariato
    scansioni(v, cart / "scansioni")
    ris = cart / "risultati"
    shutil.rmtree(ris, ignore_errors=True); ris.mkdir()
    corr = {"argomento": ARGOMENTO, "classe": CLASSE, "data": DATA, "alunni": {n: e["pct"] for n, e in ELAB[v].items()}}
    (ris / "correzioni.json").write_text(json.dumps(corr, ensure_ascii=False, indent=1), encoding="utf-8")
    dati, es, calcs = C.calcola(reg, ris / "correzioni.json")
    rows = C.registro_xlsx.read(reg)
    for c in calcs:
        scheda(v, c["nome"], ELAB[v][c["nome"]], c, rows, ris)
    run = lambda *a: subprocess.run([sys.executable, *map(str, a)], check=True, cwd=SKILL)
    run(SKILL / "scripts/correzione.py", reg, ris / "correzioni.json", ris / "riepilogo_voti.xlsx", ris / "correttore_alunni.xlsx")
    run(SKILL / "scripts/fascicolo.py", reg, ris / "correzioni.json", ris)
    (ris / "note_correzione.md").write_text(f"# Note di correzione, versione {v}\n\n" + NOTE[v], encoding="utf-8")
    print(v, [(c["nome"], c["totale"], c["voto"][0]) for c in calcs])


if __name__ == "__main__":
    for v in ELAB:
        versione(v)
