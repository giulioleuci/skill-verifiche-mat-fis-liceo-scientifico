"""Fascicolo stampabile in risultati/: copertina.pdf, Schede_complete.pdf, Schede_complete_fronteretro.pdf.

python scripts/fascicolo.py registro_evidenze.xlsx correzioni.json risultati/

Servono le schede risultati/<argomento>_<Cognome Nome>.pdf di tutti gli alunni e, in correzioni.json,
"argomento", "classe" e "data". Richiede pdflatex (pacchetto pdfpages) e pdfinfo.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from correzione import calcola

SPECIALI = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\~{}", "^": r"\^{}", "\\": r"\textbackslash{}"}
tex = lambda s: "".join(SPECIALI.get(c, c) for c in str(s))
num = lambda x: f"{round(x, 1):g}".replace(".", ",")


def pdflatex(sorgente, cartella, nome):
    (cartella / f"{nome}.tex").write_text(sorgente, encoding="utf-8")
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{nome}.tex"],
                       cwd=cartella, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"pdflatex ha fallito su {nome}:\n" + "\n".join(l for l in r.stdout.splitlines() if l.startswith("!")))
    return cartella / f"{nome}.pdf"


def pagine(pdf):
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))


def copertina(dati, es, alunni):
    n = len(alunni)
    righe = []
    for a in alunni:
        v = a["voto"]
        righe.append(" & ".join([tex(a["nome"])] + [num(a["per_es"][e]) for e in es] + [num(a["totale"]), f"\\cellcolor{{yellow!45}}\\textbf{{{v[0]}}}"]) + r" \\")
    media = lambda f: sum(f(a) for a in alunni) / n
    riga_media = " & ".join(["\\textbf{Media della classe}"] + [num(media(lambda a, e=e: a["per_es"][e])) for e in es]
                            + [num(media(lambda a: a["totale"])), num(media(lambda a: a["voto"][1]))]) + r" \\"
    suff = sum(a["voto"][1] >= 6 for a in alunni)
    return rf"""\documentclass[10pt,a4paper]{{article}}
\usepackage[T1]{{fontenc}}\usepackage[utf8]{{inputenc}}\usepackage[italian]{{babel}}\usepackage{{mathpazo,microtype}}
\usepackage[table]{{xcolor}}\usepackage{{array}}\usepackage[a4paper,margin=1.5cm]{{geometry}}
\pagestyle{{empty}}\setlength{{\parindent}}{{0pt}}
\definecolor{{blu}}{{HTML}}{{1F4E79}}
\begin{{document}}
{{\LARGE\bfseries Verifica {tex(dati["argomento"])}}}\\[2pt]
Classe {tex(dati["classe"])} \quad Data {tex(dati["data"])} \quad Alunni: {n}

\bigskip
\rowcolors{{2}}{{white}}{{gray!12}}\{"footnotesize" if n > 25 else "small"}
\begin{{tabular}}{{l{"r" * len(es)}rc}}
\rowcolor{{blu}}\color{{white}}\bfseries Alunno {"".join(f" & \\color{{white}}\\bfseries Es.\\ {tex(e)}" for e in es)} & \color{{white}}\bfseries Punti & \color{{white}}\bfseries Voto \\
{chr(10).join(righe)}
\hline {riga_media}
\end{{tabular}}

\bigskip
{{\small Punteggio su 1000; voto = punti/100 arrotondato a 0,25 (5+ = 5,25 · 5½ = 5,5 · 6- = 5,75), minimo 2, compito tutto in bianco 1.
Sufficienti (voto $\ge 6$): {suff} su {n}.}}
\end{{document}}
"""


def unisci(pezzi, dispari, piede, totale):
    """Sorgente LaTeX che unisce i PDF (nome, pagine) con piè di pagina; dispari: bianca dopo ogni pezzo con pagine dispari."""
    corpo = []
    for nome, p in pezzi:
        corpo.append(rf"\includepdf[pages=-,pagecommand={{\thispagestyle{{foot}}}}]{{{nome}}}")
        if dispari and p % 2:
            corpo.append(r"\thispagestyle{empty}\null\newpage")
    return rf"""\documentclass[a4paper]{{article}}
\usepackage[a4paper,top=1cm,bottom=1.4cm,footskip=0.7cm]{{geometry}}\usepackage{{pdfpages,fancyhdr,xcolor}}
\fancypagestyle{{foot}}{{\fancyhf{{}}\renewcommand{{\headrulewidth}}{{0pt}}\fancyfoot[C]{{\color{{gray}}\fontsize{{8}}{{10}}\selectfont {piede} --- pag.\ \thepage\ di {totale}}}}}
\begin{{document}}
{chr(10).join(corpo)}
\end{{document}}
"""


def fascicolo(registro, correzioni, dst):
    dst = Path(dst)
    dati, es, alunni = calcola(registro, correzioni)
    arg = dati["argomento"]
    schede = [dst / f"{arg}_{a['nome']}.pdf" for a in alunni]
    mancanti = [s.name for s in schede if not s.exists()]
    if mancanti:
        sys.exit("schede mancanti: " + ", ".join(mancanti))
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        cop = pdflatex(copertina(dati, es, alunni), t, "copertina")
        if pagine(cop) != 1:
            sys.exit("la copertina supera una pagina: troppi alunni")
        pezzi = [("copertina", 1)]
        for i, s in enumerate(schede):
            shutil.copy(s, t / f"s{i:03d}.pdf")  # nomi sicuri per LaTeX (gli originali hanno spazi)
            pezzi.append((f"s{i:03d}", pagine(s)))
        piede = tex(f"{arg} — {dati['classe']} — {dati['data']}")
        for nome, dispari in (("Schede_complete", False), ("Schede_complete_fronteretro", True)):
            totale = sum(p + (dispari and p % 2) for _, p in pezzi)
            shutil.copy(pdflatex(unisci(pezzi, dispari, piede, totale), t, nome), dst / f"{nome}.pdf")
        shutil.copy(cop, dst / "copertina.pdf")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    fascicolo(*sys.argv[1:])
