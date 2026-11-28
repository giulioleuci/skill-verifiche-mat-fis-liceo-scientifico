#!/usr/bin/env python3
"""Cartelle numerate delle prove: NN_NOME (01_VERIFICA_RETTE, 02_QUIZ_CINEMATICA...), una sequenza unica per verifiche e quiz.

Uso: cartelle.py nuova NOME --tipo prova|quiz|importata [--radice DIR]   crea la cartella successiva e stampa il percorso
     cartelle.py elenco [--radice DIR]                                   tipo, fase e file dei risultati di ogni cartella
La radice (default: cartella corrente) la sceglie il docente. Non rinumera mai le cartelle esistenti.
"""
import argparse
import json
import re
from pathlib import Path

SOTTO = {"prova": ["scalette", "prove", "registri", "calcoli", "correttori", "consegne", "risultati"],
         "quiz": ["varianti", "scansioni", "risultati"],
         "importata": ["dati", "risultati"]}
RISERVATE = "consegne/\nscansioni/\ndati/\n"  # elaborati e scansioni con i nomi: mai nel repository
NN = re.compile(r"^(\d{2,})_")


def prossima(radice):
    return max((int(m[1]) for d in Path(radice).iterdir() if d.is_dir() and (m := NN.match(d.name))), default=0) + 1


def nuova(radice, nome, tipo):
    slug = re.sub(r"[^A-Z0-9]+", "_", nome.upper()).strip("_")
    if not slug:
        raise SystemExit("Nome vuoto")
    c = Path(radice) / f"{prossima(radice):02d}_{slug}"
    for s in SOTTO[tipo]:
        (c / s).mkdir(parents=True)
    (c / ".gitignore").write_text(RISERVATE, encoding="utf-8")
    (c / "progetto.json").write_text(json.dumps({"tipo": tipo, "nome": slug, "fase": "nuova", "preferenze": {}, "versioni": {}},
                                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return c


def elenco(radice):
    r = []
    for d in sorted(p for p in Path(radice).iterdir() if p.is_dir() and NN.match(p.name)):
        p = json.loads((d / "progetto.json").read_text(encoding="utf-8")) if (d / "progetto.json").exists() else {}
        fasi = sorted({v["fase"] for v in p.get("versioni", {}).values() if "fase" in v}) or [p.get("fase", "?")]
        ris = sorted(f.name for f in (d / "risultati").glob("*") if f.is_file()) if (d / "risultati").is_dir() else []
        r.append({"cartella": d.name, "tipo": p.get("tipo", "prova"), "fase": ", ".join(fasi), "risultati": len(ris)})
    return r


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = a.add_subparsers(dest="cmd", required=True)
    n = s.add_parser("nuova")
    n.add_argument("nome"); n.add_argument("--tipo", choices=SOTTO, required=True)
    s.add_parser("elenco")
    for x in s.choices.values():
        x.add_argument("--radice", default=".")
    x = a.parse_args()
    if x.cmd == "nuova":
        print(nuova(x.radice, x.nome, x.tipo))
    else:
        print(json.dumps(elenco(x.radice), ensure_ascii=False, indent=2))
