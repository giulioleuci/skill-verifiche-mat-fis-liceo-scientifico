#!/usr/bin/env python3
"""Excel delle domande del quiz: scrittura da JSON e controllo.

Uso: domande_xlsx.py write domande.json domande.xlsx
     domande_xlsx.py check domande.xlsx
domande.json: [{"argomento": "Rette", "indicatore": "ANA", "versioni": [
    {"testo": "...", "corretta": "...", "errate": ["...", "...", "..."], "colonne": 2, "punti": [4, 1, 0]}]}]
Una domanda = un foglio (D01, D02...); ogni versione e' una riga, quiz.py ne sceglie una per variante.
"indicatore", "argomento", "colonne" e "punti" (corretta, non data, errata) sono facoltativi.
"""
import json
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

import quiz


def scrivi(domande, dst):
    wb = Workbook()
    wb.remove(wb.active)
    for n, d in enumerate(domande, 1):
        k = max(len(v["errate"]) for v in d["versioni"])
        ws = wb.create_sheet(f"D{n:02d}")
        head = ["Testo della domanda", "Risposta corretta"] + [f"Alternativa {i}" for i in range(1, k + 1)] + ["Numero Colonne Alternative"]
        punti = any(v.get("punti") for v in d["versioni"])
        head += ["Punteggio corretta", "Punteggio non data", "Punteggio errata"] * punti + ["Indicatore"] * ("indicatore" in d) + ["Argomento"] * ("argomento" in d)
        ws.append(head)
        for v in d["versioni"]:
            riga = [v["testo"], v["corretta"]] + v["errate"] + [None] * (k - len(v["errate"])) + [v.get("colonne", 1)]
            riga += list(v.get("punti") or [None] * 3) * punti + [d.get("indicatore")] * ("indicatore" in d) + [d.get("argomento")] * ("argomento" in d)
            ws.append(riga)
    wb.save(dst)


def controlla(path):
    """Ritorna (errori, avvisi, riepilogo)."""
    try:
        fogli = quiz.leggi_domande(path)
    except SystemExit as e:  # leggi_domande segnala gli errori di formato con sys.exit
        return [str(e)], [], ""
    err, avv = [], []
    for ws in load_workbook(path, data_only=True).worksheets:  # alternative ripetute o uguali alla corretta: leggi_domande le scarta in silenzio
        rows = list(ws.iter_rows(values_only=True))
        alt = [i for i, h in enumerate(rows[0]) if quiz.s(h).lower().startswith("alternativa")]
        for n, r in enumerate(rows[1:], 2):
            raw = [quiz.s(r[i]) for i in alt if quiz.s(r[i])]
            if r[0] and len(set(raw) | {quiz.s(r[1])}) < len(raw) + 1:
                err.append(f"{ws.title} riga {n}: alternative ripetute o uguali alla risposta corretta")
    for f, qs in fogli.items():
        if len({len(q["errate"]) for q in qs}) > 1:
            avv.append(f"{f}: le versioni hanno un numero diverso di alternative")
        for q in qs:
            if len(q["errate"]) < 3:
                avv.append(f"{f} riga {q['riga']}: solo {len(q['errate']) + 1} alternative (consigliate almeno 4)")
    n_v = sum(len(q) for q in fogli.values())
    ind = {}
    for q in (q for qs in fogli.values() for q in qs):
        ind[q["ind"] or "-"] = ind.get(q["ind"] or "-", 0) + 1
    return err, avv, f"{len(fogli)} domande, {n_v} versioni; indicatori: " + ", ".join(f"{k} {v}" for k, v in sorted(ind.items()))


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("write", "check"):
        sys.exit(__doc__)
    if sys.argv[1] == "write":
        scrivi(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")), sys.argv[3])
        sys.argv[2:] = [sys.argv[3]]
    e, a, riepilogo = controlla(sys.argv[2])
    print("\n".join(["Errore: " + x for x in e] + ["Avviso: " + x for x in a] + ([riepilogo] if riepilogo else [])))
    sys.exit(1 if e else 0)
