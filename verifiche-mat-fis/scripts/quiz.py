#!/usr/bin/env python3
"""Quiz a scelta multipla: varianti randomizzate (genera) e correzione con statistiche (correggi).

Adattato da https://github.com/giulioleuci/multiple-choice-randomizer-latex (GPL-3.0).
Esempio: python scripts/quiz.py genera domande.xlsx --varianti 4
         python scripts/quiz.py correggi
"""
import argparse
import json
import random
import statistics as st
import subprocess
import sys
from bisect import bisect_right
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "quiz_template.tex"
CODICE_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def s(v):
    if v is None:
        return ""
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v).strip()


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None


def fmt(x):
    return (str(int(x)) if float(x).is_integer() else f"{x:g}").replace(".", ",")


# ---------------------------------------------------------------- genera

def leggi_domande(path):
    """Un foglio = una domanda; ogni riga valida del foglio e' una sua versione."""
    fogli = {}
    for ws in load_workbook(path, data_only=True).worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        col = {s(h).lower(): i for i, h in enumerate(rows[0]) if s(h)}
        if "testo della domanda" not in col or "risposta corretta" not in col:
            continue
        alt = [i for h, i in col.items() if h.startswith("alternativa")]
        for n, r in enumerate(rows[1:], start=2):
            get = lambda k: r[col[k]] if k in col and col[k] < len(r) else None
            testo, ok = s(get("testo della domanda")), s(get("risposta corretta"))
            if not testo or not ok:
                continue
            errate = list(dict.fromkeys(x for x in (s(r[i]) for i in alt if i < len(r)) if x and x != ok))  # testi distinti: chiave dei distrattori
            if not errate:
                sys.exit(f"Foglio {ws.title!r} riga {n}: nessuna alternativa errata")
            fogli.setdefault(ws.title, []).append({
                "foglio": ws.title, "riga": n, "testo": testo, "corretta": ok, "errate": errate,
                "colonne": int(num(get("numero colonne alternative")) or 1),
                "punti": [num(get("punteggio corretta")), num(get("punteggio non data")), num(get("punteggio errata"))],
            })
    if not fogli:
        sys.exit("Nessun foglio valido: servono le colonne 'Testo della domanda' e 'Risposta corretta'")
    return fogli


def crea_varianti(fogli, n, base, rng):
    uso = {(f, q["riga"]): 0 for f, qs in fogli.items() for q in qs}
    visti, varianti, codici = set(), [], set()
    for _ in range(n):
        for tentativo in range(200):
            scelte = []
            for f, qs in fogli.items():
                minimo = min(uso[(f, q["riga"])] for q in qs)
                q = rng.choice([q for q in qs if uso[(f, q["riga"])] == minimo])
                alt = [q["corretta"]] + q["errate"]
                rng.shuffle(alt)
                scelte.append({**q, "alternative": alt, "corretta": "ABCDEFGHIJ"[alt.index(q["corretta"])],
                               "punti": [p if p is not None else b for p, b in zip(q["punti"], base)]})
                del scelte[-1]["errate"]
            rng.shuffle(scelte)
            firma = tuple((q["foglio"], q["riga"], tuple(q["alternative"])) for q in scelte)
            if firma not in visti:
                break
        else:
            print("Attenzione: varianti non tutte distinte (poche domande o alternative)", file=sys.stderr)
        visti.add(firma)
        for q in scelte:
            uso[(q["foglio"], q["riga"])] += 1
        while (codice := "".join(rng.choices(CODICE_ALFABETO, k=4))) in codici:
            pass
        codici.add(codice)
        varianti.append({"codice": codice, "domande": [{"n": i, **q} for i, q in enumerate(scelte, 1)]})
    return varianti


def latex_variante(v, base):
    c, nd, e = base
    punteggi = f"Punti per risposta corretta: {fmt(c)} $\\cdot$ non data: {fmt(nd)} $\\cdot$ errata: {fmt(e)}"
    if any(q["punti"] != list(base) for q in v["domande"]):
        punteggi += " (salvo diversa indicazione)"
    n_alt = max(len(q["alternative"]) for q in v["domande"])
    righe = []
    for blocco in range(0, len(v["domande"]), 10):
        qs = v["domande"][blocco:blocco + 10]
        t = "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.3}\n"
        t += "\\begin{tabular}{c|" + "c" * len(qs) + "}\n & " + " & ".join(str(q["n"]) for q in qs) + " \\\\ \\hline\n"
        for k in range(n_alt):
            t += "\\textbf{" + "ABCDEFGHIJ"[k] + "} & " + " & ".join("\\cbox" if k < len(q["alternative"]) else "" for q in qs) + " \\\\\n"
        righe.append(t + "\\end{tabular}\\end{center}")
    corpo = []
    for q in v["domande"]:
        extra = ""
        if q["punti"] != list(base):
            extra = f" \\hfill{{\\footnotesize (corretta {fmt(q['punti'][0])}, non data {fmt(q['punti'][1])}, errata {fmt(q['punti'][2])})}}"
        scelte = "\n".join("\\choice " + a for a in q["alternative"])
        k = q["colonne"]
        blocco = f"\\begin{{choices}}\n{scelte}\n\\end{{choices}}"
        if k > 1:
            blocco = f"\\begin{{multicols}}{{{k}}}\n{blocco}\n\\end{{multicols}}"
        corpo.append(f"\\question {q['testo']}{extra}\n\\vspace{{0.2em}}\n{blocco}\n")
    return (TEMPLATE.read_text(encoding="utf-8").replace("%%PUNTEGGI%%", punteggi).replace("%%CODICE%%", v["codice"])
            .replace("%%GRIGLIA%%", "\n".join(righe)).replace("%%DOMANDE%%", "\n".join(corpo)))


def compila(tex):
    for _ in range(2):  # due passate: \numpages
        subprocess.run(["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", tex.name],
                       cwd=tex.parent, capture_output=True, timeout=120)
    ok = tex.with_suffix(".pdf").exists()
    for ext in ("aux", "out") + (("log",) if ok else ()):
        tex.with_suffix("." + ext).unlink(missing_ok=True)
    return ok


def cmd_genera(a):
    base = [a.corretta, a.non_data, a.errata]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    varianti = crea_varianti(leggi_domande(a.domande), a.varianti, base, random.SystemRandom())
    (out / "quiz_chiavi.json").write_text(json.dumps({"base": base, "soglia": a.soglia, "varianti": varianti},
                                                     ensure_ascii=False, indent=1), encoding="utf-8")
    wb = Workbook()
    ws = wb.active
    ws.title = "Chiavi"
    ws.append(["Codice", "N", "Foglio", "Riga Excel", "Corretta"])
    for v in varianti:
        for q in v["domande"]:
            ws.append([v["codice"], q["n"], q["foglio"], q["riga"], q["corretta"]])
    wb.save(out / "quiz_chiavi.xlsx")
    wb = Workbook()
    wb.active.append(["ID", "Codice"] + list(range(1, len(varianti[0]["domande"]) + 1)))
    wb.save(out / "risposte_studenti.xlsx")
    for v in varianti:
        tex = out / f"quiz_{v['codice']}.tex"
        tex.write_text(latex_variante(v, base), encoding="utf-8")
        if not a.no_pdf:
            print(f"{tex.stem}: {'PDF ok' if compila(tex) else 'compilazione fallita (vedi .log)'}")
    print(f"Codici variante: {', '.join(v['codice'] for v in varianti)}\nOutput in {out}/")


# -------------------------------------------------------------- correggi

def percentile(sorted_vals, p):  # interpolazione lineare (come numpy)
    k = (len(sorted_vals) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def correggi_studenti(chiavi, path):
    per_codice = {v["codice"]: v for v in chiavi["varianti"]}
    righe = list(load_workbook(path, data_only=True).active.iter_rows(min_row=2, values_only=True))
    studenti, visti = [], set()
    for n, r in enumerate(righe, start=2):
        if not any(s(x) for x in r):
            continue
        sid, codice = s(r[0]), s(r[1]).upper()
        if not sid or sid in visti:
            sys.exit(f"Riga {n}: ID mancante o duplicato ({sid!r})")
        visti.add(sid)
        if codice not in per_codice:
            sys.exit(f"Riga {n}: codice variante {codice!r} sconosciuto")
        esiti, scelte, pt, mx = [], [], 0.0, 0.0
        for q in per_codice[codice]["domande"]:
            risp = s(r[1 + q["n"]] if 1 + q["n"] < len(r) else None).upper()
            c, nd, e = q["punti"]
            mx += c
            if not risp:
                stato, p = "n", nd
            elif risp == q["corretta"]:
                stato, p = "c", c
            else:
                stato, p = "e", e
                if risp not in "ABCDEFGHIJ"[:len(q["alternative"])]:
                    print(f"Riga {n}, domanda {q['n']}: risposta {risp!r} non valida, contata errata", file=sys.stderr)
            pt += p
            esiti.append((q["foglio"], stato))
            scelte.append((q["foglio"], q["riga"], q["alternative"]["ABCDEFGHIJ".index(risp)] if risp and risp in "ABCDEFGHIJ"[:len(q["alternative"])] else None))
        studenti.append({"id": sid, "codice": codice, "esiti": esiti, "scelte": scelte, "punti": pt, "max": mx,
                         "perc": round(pt / mx * 100, 2) if mx else 0.0})
    if not studenti:
        sys.exit("Nessuno studente nel file risposte")
    return studenti


def statistiche(studenti, soglia):
    perc = sorted(x["perc"] for x in studenti)
    media, dev = st.fmean(perc), st.pstdev(perc)
    bounds = [percentile(perc, p) for p in (4, 11, 23, 40, 60, 77, 89, 96)]
    for x in studenti:
        x["z"] = round((x["perc"] - media) / dev, 2) if dev else 0.0
        x["percentile"] = round((sum(p < x["perc"] for p in perc) + sum(p <= x["perc"] for p in perc)) / 2 / len(perc) * 100, 2)
        x["stanine"] = bisect_right(bounds, x["perc"]) + 1
        x["sufficiente"] = x["perc"] >= soglia * 100
    k = max(1, int(len(studenti) * 0.27))
    ordinati = sorted(studenti, key=lambda x: -x["perc"])
    alti, bassi = ordinati[:k], ordinati[-k:]
    domande = {}
    for x in studenti:
        for f, stato in x["esiti"]:
            domande.setdefault(f, {"c": 0, "e": 0, "n": 0})[stato] += 1
    quota = lambda gruppo, f: st.fmean(dict(x["esiti"])[f] == "c" for x in gruppo)
    for f, d in domande.items():
        tot = d["c"] + d["e"] + d["n"]
        d.update({"tot": tot, "difficolta": round(1 - d["c"] / tot, 2),
                  "discriminazione": round(quota(alti, f) - quota(bassi, f), 2) if len(studenti) >= 2 else None})
    classe = [("Studenti", len(studenti)), ("Media %", round(media, 2)), ("Mediana %", round(st.median(perc), 2)),
              ("Deviazione standard %", round(dev, 2)), ("Minimo %", perc[0]), ("Massimo %", perc[-1]),
              ("Q1 %", round(percentile(perc, 25), 2)), ("Q3 %", round(percentile(perc, 75), 2)),
              ("Soglia sufficienza %", soglia * 100), ("Sufficienti %", round(100 * sum(x["sufficiente"] for x in studenti) / len(studenti), 2))]
    return domande, classe, perc


def distrattori(chiavi, studenti):
    """Per ogni versione di domanda (foglio, riga): quante volte e' stata scelta ciascuna alternativa.
    La chiave e' il testo, perche' quiz_chiavi.json salva gia' le alternative nell'ordine stampato."""
    d = {}
    for v in chiavi["varianti"]:
        for q in v["domande"]:
            giusta = q["alternative"]["ABCDEFGHIJ".index(q["corretta"])]
            ris = d.setdefault((q["foglio"], q["riga"]), {"giusta": giusta, "tot": 0, "non_data": 0, "conta": {a: 0 for a in q["alternative"]}})
    for x in studenti:
        for f, riga, testo in x["scelte"]:
            ris = d[(f, riga)]
            ris["tot"] += 1
            if testo is None:
                ris["non_data"] += 1
            else:
                ris["conta"][testo] += 1
    return {k: v for k, v in d.items() if v["tot"]}


def cmd_correggi(a):
    out = Path(a.out)
    chiavi = json.loads((out / "quiz_chiavi.json").read_text(encoding="utf-8"))
    soglia = a.soglia if a.soglia is not None else chiavi["soglia"]
    studenti = correggi_studenti(chiavi, a.risposte or out / "risposte_studenti.xlsx")
    domande, classe, perc = statistiche(studenti, soglia)
    wb = Workbook()
    ws = wb.active
    ws.title = "Studenti"
    ws.append(["ID", "Codice", "Corrette", "Non date", "Errate", "Punteggio", "Massimo", "%", "Sufficiente", "z", "Percentile", "Stanine"])
    for x in studenti:
        cnt = [sum(s_ == k for _, s_ in x["esiti"]) for k in "cne"]
        ws.append([x["id"], x["codice"], *cnt, x["punti"], x["max"], x["perc"], "sì" if x["sufficiente"] else "no",
                   x["z"], x["percentile"], x["stanine"]])
    wd = wb.create_sheet("Domande")
    wd.append(["Foglio", "Corrette", "Errate", "Non date", "% corrette", "% errate", "% non date", "Difficoltà (1-%corrette)", "Discriminazione", "Nota"])
    for f, d in domande.items():
        disc = d["discriminazione"]
        wd.append([f, d["c"], d["e"], d["n"], *(round(100 * d[k] / d["tot"], 2) for k in "cen"), d["difficolta"], disc,
                   "rivedere: discriminazione negativa" if disc is not None and disc < 0 else ""])
    wx = wb.create_sheet("Distrattori")
    wx.append(["Foglio", "Riga Excel", "Alternativa", "Corretta", "Scelte", "% sugli studenti", "Nota"])
    for (f, riga), d in distrattori(chiavi, studenti).items():
        for alt, n in d["conta"].items():
            ok = alt == d["giusta"]
            nota = "" if ok else ("mai scelto: poco plausibile" if n == 0 else "più scelto della corretta" if n > d["conta"][d["giusta"]] else "")
            wx.append([f, riga, alt, "sì" if ok else "", n, round(100 * n / d["tot"], 2), nota])
        wx.append([f, riga, "(non data)", "", d["non_data"], round(100 * d["non_data"] / d["tot"], 2), ""])
    wc = wb.create_sheet("Classe")
    for r in classe:
        wc.append(list(r))
    wc.append([])
    wc.append(["Fascia %", "Studenti"])
    base = wc.max_row
    for i in range(10):
        lo = i * 10
        wc.append([f"{lo}-{lo + 9 if i < 9 else 100}", sum(lo <= p < lo + 10 or (i == 9 and p == 100) for p in perc)])
    ist = BarChart()
    ist.title, ist.legend = "Distribuzione dei punteggi", None
    ist.add_data(Reference(wc, min_col=2, min_row=base, max_row=base + 10), titles_from_data=True)
    ist.set_categories(Reference(wc, min_col=1, min_row=base + 1, max_row=base + 10))
    wc.add_chart(ist, "D2")
    imp = BarChart()
    imp.type, imp.grouping, imp.overlap, imp.title = "col", "stacked", 100, "Esiti per domanda"
    imp.add_data(Reference(wd, min_col=2, max_col=4, min_row=1, max_row=wd.max_row), titles_from_data=True)
    imp.set_categories(Reference(wd, min_col=1, min_row=2, max_row=wd.max_row))
    wd.add_chart(imp, "L2")
    dest = out / "quiz_risultati.xlsx"
    wb.save(dest)
    print(f"{len(studenti)} studenti corretti, media {classe[1][1]}%. Risultati in {dest}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("genera", help="crea PDF delle varianti, chiavi e template risposte")
    g.add_argument("domande", help="xlsx: un foglio per domanda; colonne 'Testo della domanda', 'Risposta corretta', 'Alternativa 1..'; "
                   "facoltative 'Numero Colonne Alternative', 'Punteggio corretta', 'Punteggio non data', 'Punteggio errata'")
    g.add_argument("--varianti", type=int, default=2)
    g.add_argument("--corretta", type=float, default=4, help="punti risposta corretta (default 4)")
    g.add_argument("--non-data", type=float, default=1, help="punti risposta non data (default 1)")
    g.add_argument("--errata", type=float, default=0, help="punti risposta errata (default 0)")
    g.add_argument("--soglia", type=float, default=0.58, help="soglia di sufficienza, frazione (default 0.58)")
    g.add_argument("--out", default="quiz_out")
    g.add_argument("--no-pdf", action="store_true", help="scrive solo i .tex")
    g.set_defaults(f=cmd_genera)
    c = sub.add_parser("correggi", help="corregge risposte_studenti.xlsx e produce quiz_risultati.xlsx")
    c.add_argument("--out", default="quiz_out")
    c.add_argument("--risposte", help="default: <out>/risposte_studenti.xlsx")
    c.add_argument("--soglia", type=float, help="sovrascrive la soglia salvata da genera")
    c.set_defaults(f=cmd_correggi)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
