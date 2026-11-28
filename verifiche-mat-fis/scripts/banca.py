#!/usr/bin/env python3
"""Banca delle domande dei quiz, con la difficolta' misurata sulle classi.

Uso: banca.py aggiungi NN_QUIZ [--radice DIR]      domande.xlsx + risultati/statistiche_distrattori.csv -> _banca/banca.xlsx
     banca.py componi --out domande.xlsx [--argomento A] [--indicatore ANA] [--difficolta 0.3-0.7] [--n 10] [--radice DIR]
Difficolta' = 1 - quota di risposte corrette; con piu' quiz e' la media pesata sugli alunni. Domande mai somministrate: nessun dato.
"""
import argparse
import csv
import random
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

import domande_xlsx
import quiz

HEAD = ["Testo della domanda", "Risposta corretta", "Alternative errate", "Numero Colonne Alternative", "Indicatore", "Argomento",
        "Difficoltà", "Alunni", "Quiz"]


def leggi(banca):
    return [list(r) for r in load_workbook(banca).active.iter_rows(min_row=2, values_only=True)] if banca.exists() else []


def aggiungi(quiz_dir, radice):
    q = Path(quiz_dir)
    dif = {}  # (foglio, riga) -> (alunni, % corrette)
    f = q / "risultati" / "statistiche_distrattori.csv"
    if f.exists():
        tot = {}
        for r in csv.DictReader(open(f, encoding="utf-8")):
            k = (r["Foglio"], int(r["Riga Excel"]))
            tot[k] = tot.get(k, 0) + int(r["Scelte"])
            if r["Corretta"] == "sì":
                dif[k] = [0, int(r["Scelte"])]
        for k, v in dif.items():
            v[0] = tot[k]
    banca = Path(radice) / "_banca" / "banca.xlsx"
    righe = {(r[0], r[1]): r for r in leggi(banca)}
    for foglio, qs in quiz.leggi_domande(q / "domande.xlsx").items():
        for d in qs:
            n, ok = dif.get((foglio, d["riga"]), (0, 0))
            vecchia = righe.get((d["testo"], d["corretta"]))
            n0, k0 = (vecchia[7], vecchia[7] * (1 - vecchia[6])) if vecchia and vecchia[7] else (0, 0)
            alunni = n0 + n
            righe[(d["testo"], d["corretta"])] = [d["testo"], d["corretta"], " | ".join(d["errate"]), d["colonne"], d["ind"], d["arg"] or None,
                                                  round(1 - (k0 + ok) / alunni, 2) if alunni else None, alunni,
                                                  ", ".join(sorted({*((vecchia[8] or "").split(", ") if vecchia else []), q.name} - {""}))]
    banca.parent.mkdir(exist_ok=True)
    wb = Workbook()
    wb.active.title = "Banca"
    wb.active.append(HEAD)
    for r in righe.values():
        wb.active.append(r)
    wb.save(banca)
    print(f"{len(righe)} domande in {banca}")


def componi(radice, out, argomento, indicatore, difficolta, n):
    lo, hi = (float(x) for x in difficolta.split("-")) if difficolta else (0, 1)
    ok = [r for r in leggi(Path(radice) / "_banca" / "banca.xlsx")
          if (not argomento or (r[5] or "").lower() == argomento.lower()) and (not indicatore or r[4] == indicatore.upper())
          and (not difficolta or (r[6] is not None and lo <= r[6] <= hi))]
    if len(ok) < n:
        sys.exit(f"Nella banca ci sono solo {len(ok)} domande con questi filtri (richieste {n})")
    scelte = random.SystemRandom().sample(ok, n)
    domande_xlsx.scrivi([{"versioni": [{"testo": r[0], "corretta": r[1], "errate": r[2].split(" | "), "colonne": r[3] or 1}],
                          **({"indicatore": r[4]} if r[4] else {}), **({"argomento": r[5]} if r[5] else {})} for r in scelte], out)
    print(f"{n} domande in {out}: " + ", ".join(f"{r[6]}" if r[6] is not None else "n.d." for r in scelte) + " (difficoltà)")


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = a.add_subparsers(dest="cmd", required=True)
    s.add_parser("aggiungi").add_argument("quiz")
    c = s.add_parser("componi")
    c.add_argument("--out", required=True); c.add_argument("--argomento"); c.add_argument("--indicatore")
    c.add_argument("--difficolta"); c.add_argument("--n", type=int, default=10)
    for x in s.choices.values():
        x.add_argument("--radice", default=".")
    x = a.parse_args()
    aggiungi(x.quiz, x.radice) if x.cmd == "aggiungi" else componi(x.radice, x.out, x.argomento, x.indicatore, x.difficolta, x.n)
