#!/usr/bin/env python3
"""Rigenera tutti gli esempi della skill eseguendo gli script reali (registro, progetto, correzione, fascicolo,
quiz) e compilando i sorgenti LaTeX. Da lanciare dalla radice del repository dopo ogni modifica alla skill:

    python3 esempi/genera_esempi.py

I sorgenti scritti a mano (testi delle prove, evidenze, correttori, dati degli alunni fittizi) restano nelle
cartelle; i file generati (registri, PDF, Excel, scansioni simulate, esiti dei controlli) si riscrivono.
Se cambiano template, comandi o formati della skill, aggiorna prima i sorgenti dell'esempio interessato e README.md.
Richiede: openpyxl, opencv-python-headless, numpy, Pillow, sympy, pdflatex, pdftoppm, pdfinfo (soffice facoltativo)."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
SKILL = QUI.parent / "verifiche-mat-fis"
PY = sys.executable
E1, E3, E4 = QUI / "01_matematica_rette", QUI / "03_fisica_urti", QUI / "04_laboratorio_pendolo"


def run(*a, cwd=None, out=None, ok=(0,)):
    r = subprocess.run([str(x) for x in a], cwd=cwd, capture_output=True, text=True)
    if r.returncode not in ok:
        sys.exit(f"ERRORE: {' '.join(map(str, a))}\n{r.stdout[-800:]}{r.stderr[-1500:]}")
    if out:
        Path(out).write_text(r.stdout + r.stderr, encoding="utf-8")
    return r


def compila(tex):
    """Due passate di pdflatex; pulizia dei file ausiliari."""
    tex = Path(tex)
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name], cwd=tex.parent, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"ERRORE LaTeX in {tex}\n{r.stdout[-1500:]}")
    for e in ("aux", "log", "out", "toc"):
        tex.with_suffix(f".{e}").unlink(missing_ok=True)


def registro(*args):
    return run(PY, SKILL / "scripts/registro_xlsx.py", *args)


def progetto(*args, out=None, ok=(0,)):
    return run(PY, SKILL / "scripts/progetto.py", *args, out=out, ok=ok)


def nota(xlsx):
    """Modifica del docente: nota utente su E05 (in un file xlsx, come farebbe il docente in Excel)."""
    from openpyxl import load_workbook
    wb = load_workbook(xlsx); ws = wb.active
    col = {c.value: c.column for c in ws[1]}
    for riga in range(2, ws.max_row + 1):
        if ws.cell(riga, 1).value == "E05":
            ws.cell(riga, col["Note utente"]).value = "Ammesso anche il risultato approssimato 5,06 se compare la forma esatta."
    wb.save(xlsx)


def es01():
    r = E1 / "registri"
    for f in r.glob("*.xlsx"):
        f.unlink()
    run(PY, E1 / "calcoli/verifica_calcoli.py", out=E1 / "calcoli/esito.txt")
    # versione A: prima revisione, poi modifica del docente (nota + massimi) con `update`
    registro("write", r / "evidenze_A_rev1.json", r / "registro_A_rev1.xlsx", "--classe", "medio")
    registro("write", r / "evidenze_A_rev1.json", r / "registro_A.xlsx", "--classe", "medio")
    nota(r / "registro_A.xlsx")
    run(PY, SKILL / "scripts/registro_xlsx.py", "update", r / "evidenze_A.json", r / "registro_A.xlsx", "--classe", "medio", out=r / "update_A.txt")
    registro("write", r / "evidenze_B.json", r / "registro_B.xlsx", "--classe", "medio")
    registro("write", r / "evidenze_adattata.json", r / "registro_adattata.xlsx", "--classe", "medio")
    registro("write", r / "evidenze_A.json", r / "registro_A_flat.xlsx", "--classe", "medio", "--layout", "flat")  # solo su richiesta del docente
    nota(r / "registro_A_flat.xlsx")
    for v in ("A", "B", "adattata", "A_flat"):
        run(PY, SKILL / "scripts/registro_xlsx.py", "check", r / f"registro_{v}.xlsx", "--classe", "medio", out=r / f"check_{v}.txt")
    # stato prima dell'approvazione, approvazioni nell'ordine standard -> derivate, stato finale
    progetto("stato", E1 / "progetto.json", out=E1 / "progetto_stato_prima.txt")
    for v in ("A", "B", "R"):
        for d in ("scaletta", "registro"):
            progetto("approva", E1 / "progetto.json", v, d, out=E1 / "progetto_approvazioni.txt" if (v, d) == ("A", "scaletta") else None)
    progetto("stato", E1 / "progetto.json", out=E1 / "progetto_stato.txt")
    progetto("confronta", r / "registro_A_rev1.xlsx", r / "registro_A.xlsx", out=r / "confronta_A_rev1_rev2.txt")
    progetto("confronta", r / "registro_A.xlsx", r / "registro_adattata.xlsx", "--derivazioni", r / "derivazioni_adattata.json", out=r / "confronta_A_adattata.txt")
    progetto("confronta", r / "registro_A.xlsx", r / "registro_A_flat.xlsx", out=r / "confronta_merged_flat.txt")  # legge entrambi i layout
    progetto("copertura", E1 / "progetto/matrice_copertura_A.json", out=E1 / "progetto/copertura_esito.txt")
    for t in sorted((E1 / "prove").glob("*.tex")):
        if "opendyslexic" in t.name:  # font non installato: solo sorgente (vedi LIMITI.md)
            continue
        compila(t)
    compila(E1 / "correttori/correttore_A.tex")
    compila(E1 / "svolgimento/svolgimento_studenti_A.tex")
    run("pdftotext", "-layout", E1 / "prove/prova_A.pdf", E1 / "prove/prova_A_testo_estratto.txt")
    run(PY, E1 / "correzione/build_correzione.py")
    verifica_riepiloghi()


def verifica_riepiloghi():
    """Ricalcola con LibreOffice i riepiloghi e confronta i voti con correzione.voto() (se soffice è installato)."""
    if not shutil.which("soffice"):
        return
    sys.path.insert(0, str(SKILL / "scripts"))
    import correzione as C
    from openpyxl import load_workbook
    for v in ("A", "B"):
        d = E1 / "correzione" / v / "risultati"
        tmp = QUI / ".ricalcolo"; shutil.rmtree(tmp, ignore_errors=True)
        run("soffice", "--headless", "--convert-to", "xlsx", "--outdir", tmp, d / "riepilogo_voti.xlsx")
        ws = load_workbook(tmp / "riepilogo_voti.xlsx", data_only=True)["Voti"]
        atteso = {c["nome"]: c["voto"][0] for c in C.calcola(E1 / "correzione" / v / "registro_evidenze.xlsx", d / "correzioni.json")[2]}
        cv = [c.value for c in ws[4]].index("Voto") + 1
        trovati = {ws.cell(r, 1).value: ws.cell(r, cv).value for r in range(5, 5 + len(atteso))}
        assert trovati == atteso, (v, trovati, atteso)
        shutil.rmtree(tmp)


def es02():
    compila(QUI / "02_recupero_matematica/recupero_rette.tex")


def es03():
    run(PY, E3 / "calcoli/verifica_calcoli.py", out=E3 / "calcoli/esito.txt")
    x = E3 / "registri/registro_fisica.xlsx"; x.unlink(missing_ok=True)
    registro("write", E3 / "registri/evidenze.json", x, "--classe", "medio")
    run(PY, SKILL / "scripts/registro_xlsx.py", "check", x, "--classe", "medio", out=E3 / "registri/check_fisica.txt")
    compila(E3 / "prove/prova_fisica.tex"); compila(E3 / "correttori/correttore_fisica.tex")


def es04():
    run(PY, E4 / "analisi_pendolo.py", out=E4 / "analisi_esito.txt")
    compila(E4 / "traccia_laboratorio.tex"); compila(E4 / "griglia_laboratorio.tex")


def altri():
    run(PY, QUI / "05_griglie_esame/calcoli_esami.py", out=QUI / "05_griglie_esame/calcoli_esito.txt")
    run(PY, QUI / "05_griglie_esame/genera_esami.py")
    run(PY, QUI / "06_quiz/genera_quiz.py")
    run(PY, QUI / "08_organizzazione_statistiche/genera_08.py")  # usa il registro e le correzioni di 01
    compila(QUI / "07_aiuto_sintesi_flusso/sintesi_flusso.tex")


def copertura_comandi():
    """Ogni comando della tabella di SKILL.md deve comparire nella tabella di copertura di esempi/README.md."""
    comandi = set()
    for riga in (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if riga.startswith("| `"):
            comandi |= set(re.findall(r"`([a-z-]+)`", riga.split("|")[1]))
    readme = (QUI / "README.md").read_text(encoding="utf-8")
    mancanti = sorted(c for c in comandi if f"`{c}`" not in readme)
    if mancanti:
        sys.exit(f"Comandi di SKILL.md senza esempio in esempi/README.md: {', '.join(mancanti)}.\n"
                 "Aggiungi un esempio (cartella, sorgenti, riga nella tabella) e rilancia.")
    print(f"copertura comandi: ok ({len(comandi)} comandi)")


if __name__ == "__main__":
    for f in (es01, es02, es03, es04, altri, copertura_comandi):
        f(); print(f.__name__, "ok")
    for p in QUI.rglob("*"):  # file ausiliari LaTeX e cache
        if p.suffix in (".aux", ".log", ".out", ".toc") or p.name == "__pycache__":
            shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink()
