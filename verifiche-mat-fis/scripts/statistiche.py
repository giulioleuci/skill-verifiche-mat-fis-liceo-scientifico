#!/usr/bin/env python3
"""Statistiche comuni a prove scritte e quiz, storico e report di classe (nessun nome di alunno).

Uso: statistiche.py chiudi NN_NOME      aggiorna storico.csv/xlsx nella radice e segna la prova come chiusa
     statistiche.py report NN_NOME      scrive risultati/report_classe.md
Le tabelle (statistiche_*.csv, statistiche.md) le scrivono correzione.py, quiz.py e importa.py con scrivi().
"""
import csv
import json
import statistics as st
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference

N_MIN = 20       # sotto questo numero di alunni discriminazione e affidabilita' sono poco affidabili
DEBOLE = 60      # media % sotto la quale un indicatore o argomento e' segnalato come debole
FASCE = 10


def percentile(v, p):
    """Interpolazione lineare su una lista ordinata (come numpy)."""
    k = (len(v) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def descrittive(perc):
    p = sorted(perc)
    return [("Studenti", len(p)), ("Media %", round(st.fmean(p), 2)), ("Mediana %", round(st.median(p), 2)),
            ("Deviazione standard %", round(st.pstdev(p), 2)), ("Minimo %", round(p[0], 2)), ("Massimo %", round(p[-1], 2)),
            ("Q1 %", round(percentile(p, 25), 2)), ("Q3 %", round(percentile(p, 75), 2))]


def fasce(perc):
    return [[f"{i * FASCE}-{i * FASCE + FASCE - 1 if i < 9 else 100}",
             sum(i * FASCE <= x < i * FASCE + FASCE or (i == 9 and x >= 100) for x in perc)] for i in range(10)]


def discriminazione(frazioni, tot):
    """Media del gruppo alto meno gruppo basso (27% per totale); None con meno di 2 alunni."""
    n = len(tot)
    if n < 2:
        return None
    k = max(1, int(n * 0.27))
    ordine = sorted(range(n), key=lambda i: -tot[i])
    return round(st.fmean(frazioni[i] for i in ordine[:k]) - st.fmean(frazioni[i] for i in ordine[-k:]), 2)


def affidabilita(M):
    """Alpha di Cronbach (KR-20 se gli item valgono 0/1) ed errore standard di misura, in unita' del totale.
    M: una lista di punteggi per item. (None, None) se non calcolabili."""
    k, n = len(M), len(M[0]) if M else 0
    tot = [sum(c) for c in zip(*M)]
    if k < 2 or n < 2 or st.pvariance(tot) == 0:
        return None, None
    a = k / (k - 1) * (1 - sum(st.pvariance(i) for i in M) / st.pvariance(tot))
    return round(a, 2), round(st.pstdev(tot) * max(0, 1 - a) ** 0.5, 2)


def segnale(raggiunta, disc):
    """Nota «rivedere» di un item; raggiunta = quota (0-1) di alunni che l'hanno risolto."""
    note = []
    if disc is not None and disc < 0:
        note.append("rivedere: discriminazione negativa")
    if raggiunta < 0.10:
        note.append("rivedere: raggiunta da meno del 10%")
    elif raggiunta > 0.95:
        note.append("raggiunta da oltre il 95%: poco informativa")
    return "; ".join(note)


def affidabilita_righe(M, n, unita):
    a, sem = affidabilita(M)
    r = [("Affidabilità (alpha di Cronbach / KR-20)", a if a is not None else "n.d."),
         (f"Errore standard di misura ({unita})", sem if sem is not None else "n.d.")]
    if n < N_MIN:
        r.append(("Avviso", f"meno di {N_MIN} alunni: discriminazione e affidabilità poco attendibili"))
    return r


def prova(rows, punti):
    """Tabelle di una prova scritta. rows: righe del registro; punti: {alunno: {ID evidenza: punti}}."""
    import correzione
    alunni = sorted(punti)
    M = [[punti[a].get(r["ID evidenza"], 0) for a in alunni] for r in rows]
    mx = sum(r["Max"] for r in rows)
    tot = [sum(c) for c in zip(*M)]
    perc = [100 * t / mx for t in tot]
    voti = [correzione.voto(t * 1000 / mx)[1] for t in tot]
    classe = descrittive(perc) + [("Media voto (decimi)", round(st.fmean(voti), 2)),
                                  ("Sufficienti % (voto ≥ 6)", round(100 * sum(v >= 6 for v in voti) / len(voti), 2))]
    classe += affidabilita_righe(M, len(alunni), "punti su 1000" if mx == 1000 else "punti")
    evid, gruppi = [], {k: {} for k in ("Indicatore", "Livello", "Sigla argomento")}
    for r, v in zip(rows, M):
        fr = [x / r["Max"] for x in v]
        att = st.fmean(f >= 0.5 for f in fr)
        disc = discriminazione(fr, tot)
        evid.append([r["ID evidenza"], r["Esercizio"], r["Indicatore"], r["Livello"], r["Sigla argomento"], r["Max"],
                     round(100 * st.fmean(fr), 1), round(100 * att, 1), round(1 - st.fmean(fr), 2), disc, segnale(att, disc)])
        for k, g in gruppi.items():
            e = g.setdefault(r[k], [0, 0, 0])
            e[0] += 1; e[1] += r["Max"]; e[2] += st.fmean(v)
    def tab(nome, g):
        return ([nome, "Evidenze", "Max", "Media punti", "Media %", "Nota"],
                [[k, e[0], e[1], round(e[2], 1), round(100 * e[2] / e[1], 1), "debole" if 100 * e[2] / e[1] < DEBOLE else ""] for k, e in sorted(g.items())])
    return {"classe": (["Misura", "Valore"], classe),
            "evidenze": (["ID", "Esercizio", "Indicatore", "Livello", "Argomento", "Max", "Media %", "% alunni ≥50% del max",
                           "Difficoltà (1-media)", "Discriminazione", "Nota"], evid),
            "indicatori": tab("Indicatore", gruppi["Indicatore"]), "livelli": tab("Livello", gruppi["Livello"]),
            "argomenti": tab("Argomento", gruppi["Sigla argomento"]),
            "distribuzione": (["Fascia %", "Studenti"], fasce(perc))}, tot, voti


def scrivi(dest, tabelle, titolo="Statistiche"):
    """statistiche_<nome>.csv per ogni tabella e statistiche.md riassuntivo."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    md = [f"# {titolo}\n"]
    for nome, (head, righe) in tabelle.items():
        with open(dest / f"statistiche_{nome}.csv", "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows([head] + [["" if c is None else c for c in r] for r in righe])
        md.append(f"\n## {nome.capitalize()}\n")
        if nome == "classe":
            md += [f"- {r[0]}: {r[1]}" for r in righe]
        else:
            md += ["| " + " | ".join(map(str, head)) + " |", "|" + "---|" * len(head)]
            md += ["| " + " | ".join("" if c is None else str(c) for c in r) + " |" for r in righe]
    (dest / "statistiche.md").write_text("\n".join(md) + "\n", encoding="utf-8")


# ------------------------------------------------------------ storico, report

def leggi_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cartella(arg):
    c = Path(arg).resolve()
    if not (c / "risultati" / "statistiche_classe.csv").exists():
        sys.exit(f"{c}: manca risultati/statistiche_classe.csv (esegui prima correggi, correggi-quiz o importa-punteggi)")
    return c


def da_rivedere(risultati):
    """[(item, nota)] dalle tabelle evidenze o domande."""
    for nome, col in (("evidenze", "ID"), ("domande", "Foglio")):
        f = risultati / f"statistiche_{nome}.csv"
        if f.exists():
            return [(r[col], r["Nota"]) for r in leggi_csv(f) if r["Nota"].startswith("rivedere")]
    return []


def chiudi(c):
    ris = c / "risultati"
    classe = {r["Misura"]: r["Valore"] for r in leggi_csv(ris / "statistiche_classe.csv")}
    righe = [[c.name, "TOTALE", classe["Studenti"], classe["Media %"]]]
    if (ris / "statistiche_indicatori.csv").exists():
        righe += [[c.name, r["Indicatore"], classe["Studenti"], r["Media %"]] for r in leggi_csv(ris / "statistiche_indicatori.csv")]
    f = c.parent / "storico.csv"
    storico = [r for r in (list(csv.reader(open(f, encoding="utf-8")))[1:] if f.exists() else []) if r[0] != c.name]
    storico = sorted(storico + righe)
    with open(f, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        w.writerow(["prova", "voce", "studenti", "media_perc"])
        w.writerows(storico)
    prove = sorted({r[0] for r in storico})
    voci = sorted({r[1] for r in storico}, key=lambda v: (v != "TOTALE", v))
    wb = Workbook()
    ws = wb.active
    ws.title = "Andamento"
    ws.append(["Prova"] + voci)
    for p in prove:
        ws.append([p] + [next((float(r[3]) for r in storico if r[0] == p and r[1] == v), None) for v in voci])
    g = LineChart()
    g.title, g.y_axis.title = "Media % per prova", "%"
    g.add_data(Reference(ws, min_col=2, max_col=len(voci) + 1, min_row=1, max_row=len(prove) + 1), titles_from_data=True)
    g.set_categories(Reference(ws, min_col=1, min_row=2, max_row=len(prove) + 1))
    ws.add_chart(g, "H2")
    wb.save(c.parent / "storico.xlsx")
    p = c / "progetto.json"
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        d["fase"] = "chiusa"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Storico aggiornato: {f} ({len(prove)} prove). Prova segnata come chiusa.")
    for item, nota in da_rivedere(ris):
        print(f"Da rivedere: {item}: {nota}")


def report(c):
    ris = c / "risultati"
    classe = {r["Misura"]: r["Valore"] for r in leggi_csv(ris / "statistiche_classe.csv")}
    L = [f"# Report di classe: {c.name}\n", "Dati aggregati e anonimi.\n",
         f"- Alunni: {classe['Studenti']} · media {classe['Media %']}% · mediana {classe['Mediana %']}% · deviazione standard {classe['Deviazione standard %']}%"]
    if "Sufficienti %" in classe or "Sufficienti % (voto ≥ 6)" in classe:
        L.append(f"- Sufficienti: {classe.get('Sufficienti %', classe.get('Sufficienti % (voto ≥ 6)'))}%")
    L += [f"- {k}: {v}" for k, v in classe.items() if k.startswith(("Affidabilità", "Avviso"))]
    for nome, titolo in (("indicatori", "Indicatori"), ("argomenti", "Argomenti"), ("livelli", "Livelli di difficoltà")):
        f = ris / f"statistiche_{nome}.csv"
        if f.exists():
            r = sorted(leggi_csv(f), key=lambda x: float(x["Media %"]))
            L += [f"\n## {titolo} (dal più debole)\n"] + [f"- {x[list(x)[0]]}: {x['Media %']}%" + (" · **debole** (candidato al recupero)" if float(x["Media %"]) < DEBOLE else "") for x in r]
    rv = da_rivedere(ris)
    L += ["\n## Da rivedere in una prossima prova\n"] + ([f"- {i}: {n}" for i, n in rv] or ["- nessuna segnalazione"])
    s = c.parent / "storico.csv"
    if s.exists():
        t = [r for r in leggi_csv(s) if r["voce"] == "TOTALE"]
        if len(t) > 1:
            L += ["\n## Andamento (media % totale)\n"] + [f"- {r['prova']}: {r['media_perc']}%" for r in t]
    (ris / "report_classe.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Scritto {ris / 'report_classe.md'}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("chiudi", "report"):
        sys.exit(__doc__)
    {"chiudi": chiudi, "report": report}[sys.argv[1]](cartella(sys.argv[2]))
