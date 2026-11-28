#!/usr/bin/env python3
"""Esempio 08: cartelle numerate NN_NOME, domande del quiz, importazione di punteggi anonimi, statistiche, storico,
report di classe e banca delle domande. Alunni fittizi e anonimi. Eseguito da genera_esempi.py."""
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

QUI = Path(__file__).resolve().parent
SK = QUI.parents[1] / "verifiche-mat-fis" / "scripts"
R = QUI / "radice"
E1 = QUI.parent / "01_matematica_rette" / "correzione" / "A"


def run(script, *a, out=None):
    r = subprocess.run([sys.executable, SK / script, *map(str, a)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ERRORE {script} {a}\n{r.stdout[-600:]}{r.stderr[-1200:]}")
    if out:
        Path(out).write_text(r.stdout + r.stderr, encoding="utf-8")
    return r.stdout.strip()


def nuova(nome, tipo):
    return Path(run("cartelle.py", "nuova", nome, "--tipo", tipo, "--radice", R))


def main():
    shutil.rmtree(R, ignore_errors=True); R.mkdir()
    rng = random.Random(8)
    # 01 prova scritta: registro approvato e correzioni fittizie dell'esempio 01, poi statistiche con correzione.py
    p1 = nuova("verifica rette", "prova")
    shutil.copy(E1 / "registro_evidenze.xlsx", p1 / "registri/registro_A.xlsx")
    shutil.copy(E1 / "risultati/correzioni.json", p1 / "risultati/correzioni.json")
    run("correzione.py", p1 / "registri/registro_A.xlsx", p1 / "risultati/correzioni.json", p1 / "risultati/riepilogo_voti.xlsx")
    # 02 quiz: intervista (qui il sorgente JSON) -> domande.xlsx controllato -> varianti -> punteggi importati
    q = nuova("quiz cinematica", "quiz")
    shutil.copy(QUI / "domande_cinematica.json", q / "domande_cinematica.json")
    run("domande_xlsx.py", "write", q / "domande_cinematica.json", q / "domande.xlsx", out=q / "controllo_domande.txt")
    run("quiz.py", "genera", q / "domande.xlsx", "--varianti", 3, "--out", q / "varianti")
    ch = json.loads((q / "varianti/quiz_chiavi.json").read_text(encoding="utf-8"))["varianti"]
    # 04 quiz già corretto dal docente: lettere + riga «Variante», una colonna per alunno (anonimo)
    q4 = nuova("quiz cinematica importato", "importata")
    wb = Workbook(); ws = wb.active
    alunni = [(ch[i % 3], rng.random() * 0.5 + 0.4) for i in range(24)]
    ws.append(["Domanda"] + [None] * len(alunni))
    ws.append(["Variante"] + [v["codice"] for v, _ in alunni])
    for n in range(len(ch[0]["domande"])):
        ws.append([n + 1] + [(v["domande"][n]["corretta"] if rng.random() < abil - 0.1 * n / 6 else rng.choice("ABCD")) if rng.random() > 0.05 else None
                             for v, abil in alunni])
    wb.save(q4 / "dati/punteggi_quiz.xlsx")
    run("importa.py", "quiz", q4 / "dati/punteggi_quiz.xlsx", "--chiavi", q / "varianti/quiz_chiavi.json", "--out", q4 / "risultati")
    # 05 quiz con solo esiti 1/0 (nessuna chiave): niente distrattori
    q5 = nuova("quiz esiti", "importata")
    wb = Workbook(); ws = wb.active
    ws.append(["Domanda", "x", "y", "z", "w", "v"])
    for n in range(1, 7):
        ws.append([n] + [int(rng.random() < 0.7) if rng.random() > 0.1 else None for _ in range(5)])
    wb.save(q5 / "dati/esiti.xlsx")
    run("importa.py", "quiz", q5 / "dati/esiti.xlsx", "--out", q5 / "risultati")
    # 03 prova scritta corretta a mano: colonne del registro, colonna vuota, una colonna per alunno (senza nomi, intestazione vuota o sigla)
    p3 = nuova("verifica rette importata", "importata")
    reg = load_workbook(E1 / "registro_evidenze.xlsx"); w = reg.active
    ncol = w.max_column
    w.insert_cols(ncol + 1)  # colonna vuota di separazione
    for k in range(18):
        for r in range(2, w.max_row + 1):
            if w.cell(r, 1).value:
                w.cell(r, ncol + 2 + k, rng.choice([100, 100, 100, 75, 50, 20, 10, 0]) if k % 5 else rng.choice([100, 100, 75]))
        w.cell(1, ncol + 2 + k, f"S{k + 1:02d}" if k % 2 else None)
    reg.save(p3 / "dati/punteggi_prova.xlsx")
    run("importa.py", "prova", E1 / "registro_evidenze.xlsx", p3 / "dati/punteggi_prova.xlsx", "--out", p3 / "risultati")
    # chiusura: storico, report, banca
    for c in (p1, q4, p3):
        run("statistiche.py", "chiudi", c, out=c / "risultati/chiusura.txt")
        run("statistiche.py", "report", c)
    shutil.copy(q / "domande.xlsx", q4 / "domande.xlsx")  # il docente fornisce anche le domande: servono alla banca
    run("banca.py", "aggiungi", q4, "--radice", R)
    q6 = nuova("quiz dalla banca", "quiz")
    run("banca.py", "componi", "--out", q6 / "domande.xlsx", "--indicatore", "SVI", "--n", 2, "--radice", R)
    (R / "elenco_cartelle.json").write_text(run("cartelle.py", "elenco", "--radice", R) + "\n", encoding="utf-8")
    run("progetto.py", "stato", q / "progetto.json", out=q / "progetto_stato.txt")
    print("08 ok:", len(list(R.glob("[0-9][0-9]_*"))), "cartelle")


if __name__ == "__main__":
    main()
