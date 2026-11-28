#!/usr/bin/env python3
"""Importa punteggi anonimi del docente e produce le stesse statistiche di una correzione fatta dalla skill.

Uso: importa.py prova REGISTRO.xlsx PUNTEGGI.xlsx --out risultati [--formato percentuali|punti]
     importa.py quiz PUNTEGGI.xlsx --out risultati [--chiavi quiz_chiavi.json] [--corretta 4 --non-data 1 --errata 0]

prova: PUNTEGGI.xlsx ha le colonne del registro (ID evidenza in colonna A, riga 1 intestazioni), eventuali colonne
vuote, poi una colonna per alunno (intestazione libera o vuota) con la percentuale 0-100 o i punti di ogni evidenza.
quiz: una riga per domanda (colonna A = numero), una colonna per alunno; una riga con A = "Variante" con il codice
della variante di ciascuno. Celle = lettera scelta (con --chiavi) oppure 1/0 (senza chiavi); vuoto = non data.
I nomi delle intestazioni non vengono mai scritti: gli alunni diventano A01, A02...
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

import correzione
import quiz
import registro_xlsx
import statistiche

SIGLA = re.compile(r"^[A-Za-z]{0,3}\d{1,3}$")


def alunni_colonne(ws, prima, righe):
    """Colonne (dopo `prima`) con almeno un valore nelle righe indicate; le intestazioni sospette si contano, non si leggono."""
    cols = [c for c in range(prima + 1, ws.max_column + 1) if any(ws.cell(r, c).value not in (None, "") for r in righe)]
    nomi = sum(1 for c in cols if ws.cell(1, c).value not in (None, "") and not SIGLA.match(str(ws.cell(1, c).value).strip()))
    if nomi:
        print(f"Attenzione: {nomi} intestazioni sembrano nomi: ignorate, gli alunni sono rinominati A01, A02...", file=sys.stderr)
    return cols


def prova(registro, punteggi, dest, formato=None):
    rows = registro_xlsx.read(registro)
    ids = {r["ID evidenza"]: r for r in rows}
    ncol = load_workbook(registro).active.max_column
    ws = load_workbook(punteggi, data_only=True).active
    riga = {ws.cell(r, 1).value: r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value in ids}
    if len(riga) != len(ids):
        sys.exit(f"Evidenze del registro assenti nel file (colonna A): {', '.join(sorted(set(ids) - set(riga)))}")
    cols = alunni_colonne(ws, ncol, riga.values())
    if not cols:
        sys.exit(f"Nessuna colonna alunno dopo la colonna {ncol} (ultima del registro)")
    val = {}
    for k, c in enumerate(cols, 1):
        for i, r in riga.items():
            v = ws.cell(r, c).value
            if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0):
                sys.exit(f"Cella {ws.cell(r, c).coordinate}: serve un numero ≥ 0, trovato {v!r}")
            val[(f"A{k:02d}", i)] = v
    vuote = sum(v is None for v in val.values())
    if vuote:
        print(f"Attenzione: {vuote} celle vuote contate come 0 punti.", file=sys.stderr)
    dati = [(i, v) for (_, i), v in val.items() if v is not None]
    pct_ok = all(v <= 100 for _, v in dati)
    pt_ok = all(v <= ids[i]["Max"] for i, v in dati)
    if formato is None:
        if pct_ok and pt_ok:
            sys.exit("Formato ambiguo (valori validi sia come percentuali sia come punti): indica --formato percentuali|punti")
        if not (pct_ok or pt_ok):
            sys.exit("Valori incompatibili sia con percentuali (≤ 100) sia con punti (≤ massimo dell'evidenza)")
        formato = "percentuali" if pct_ok else "punti"
    elif not (pct_ok if formato == "percentuali" else pt_ok):
        sys.exit(f"Valori fuori scala per --formato {formato}")
    punti = {a: {} for a, _ in val}
    for (a, i), v in val.items():
        punti[a][i] = 0 if v is None else (v / 100 * ids[i]["Max"] if formato == "percentuali" else v)
    tabelle, tot, voti = statistiche.prova(rows, punti)
    statistiche.scrivi(dest, tabelle, "Statistiche della prova importata")
    with open(Path(dest) / "punteggi_anonimi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["alunno", "punti", "voto"])
        for a, t, v in zip(sorted(punti), tot, voti):
            w.writerow([a, round(t, 2), correzione.voto(t * 1000 / sum(r["Max"] for r in rows))[0]])
    print(f"{len(punti)} alunni importati (formato {formato}). Statistiche in {dest}")


def quiz_import(punteggi, dest, chiavi, base):
    ws = load_workbook(punteggi, data_only=True).active
    var = next((r for r in range(1, ws.max_row + 1) if str(ws.cell(r, 1).value or "").strip().lower() == "variante"), None)
    dom = [r for r in range(1, ws.max_row + 1) if isinstance(ws.cell(r, 1).value, (int, float)) and r != var]
    if not dom:
        sys.exit("Nessuna riga di domanda (colonna A = numero della domanda)")
    cols = alunni_colonne(ws, 1, dom)
    if chiavi and var is None:
        sys.exit("Con --chiavi serve una riga con A = «Variante»")
    if chiavi is None:  # chiavi sintetiche: 1 = alternativa A (corretta), 0 = B; i distrattori non sono disponibili
        chiavi = {"base": base, "soglia": 0.58, "pesi": None, "senza_distrattori": True, "varianti": [{"codice": "IMPR", "domande": [
            {"n": int(ws.cell(r, 1).value), "foglio": f"D{int(ws.cell(r, 1).value):02d}", "riga": 2, "alternative": ["corretta", "errata"],
             "corretta": "A", "punti": base, "ind": None} for r in dom]}]}
    wb = Workbook()
    out = wb.active
    out.append(["ID", "Codice"] + [int(ws.cell(r, 1).value) for r in dom])
    for k, c in enumerate(cols, 1):
        cod = str(ws.cell(var, c).value).strip().upper() if var else "IMPR"
        def cella(r):
            v = ws.cell(r, c).value
            if var:
                return str(v or "").strip().upper()
            if v not in (None, "", 0, 1):
                sys.exit(f"Cella {ws.cell(r, c).coordinate}: senza chiavi servono 1, 0 o vuoto")
            return {1: "A", 0: "B"}.get(v, "")
        out.append([f"A{k:02d}", cod] + [cella(r) for r in dom])
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    wb.save(dest / "risposte_studenti.xlsx")
    quiz.correggi(chiavi, dest / "risposte_studenti.xlsx", None, dest)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("prova")
    a.add_argument("registro"); a.add_argument("punteggi"); a.add_argument("--out", required=True)
    a.add_argument("--formato", choices=("percentuali", "punti"))
    b = s.add_parser("quiz")
    b.add_argument("punteggi"); b.add_argument("--out", required=True); b.add_argument("--chiavi")
    for k, d in (("corretta", 4), ("non-data", 1), ("errata", 0)):
        b.add_argument(f"--{k}", type=float, default=d)
    x = p.parse_args()
    if x.cmd == "prova":
        prova(x.registro, x.punteggi, x.out, x.formato)
    else:
        quiz_import(x.punteggi, x.out, json.loads(Path(x.chiavi).read_text(encoding="utf-8")) if x.chiavi else None, [x.corretta, x.non_data, x.errata])
