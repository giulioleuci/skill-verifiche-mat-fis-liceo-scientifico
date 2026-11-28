#!/usr/bin/env python3
"""Quiz a scelta multipla: varianti randomizzate (genera) e correzione con statistiche (correggi).

Adattato da https://github.com/giulioleuci/multiple-choice-randomizer-latex (GPL-3.0).
Esempio: python scripts/quiz.py genera domande.xlsx --varianti 4
         python scripts/quiz.py correggi
"""
import argparse
from collections import Counter
import json
import random
import statistics as st
import subprocess
import sys
from bisect import bisect_right
from pathlib import Path

import omr
import statistiche
from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "quiz_template.tex"
CODICE_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
INDICATORI = ("ANA", "SVI", "ARG", "COM")


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

def mx_ind(domande):
    """Punti massimi per indicatore di una variante."""
    r = {}
    for q in domande:
        if q.get("ind"):
            r[q["ind"]] = r.get(q["ind"], 0) + q["punti"][0]
    return r


def quote(mx):
    tot = sum(mx.values())
    return tuple(round(mx.get(i, 0) / tot, 9) for i in INDICATORI)


def parse_pesi(txt):
    try:
        pesi = {k.strip().upper(): float(v) for k, v in (x.split("=") for x in txt.split(","))}
    except ValueError:
        sys.exit("--pesi: formato ANA=250,SVI=400,ARG=200,COM=150")
    if not set(pesi) <= set(INDICATORI) or abs(sum(pesi.values()) - 1000) > 1e-9:
        sys.exit(f"--pesi: indicatori ammessi {', '.join(INDICATORI)}, somma esattamente 1000")
    return {k: v for k, v in pesi.items() if v > 0}


def fisse_alternative(v, ordine, ok, dove):
    """Quante alternative, contate dalla fine, restano nell'ordine scritto (None = mescola tutto)."""
    v = s(v).lower()
    if not v:
        return None
    n = len(ordine) if v == "tutte" else int(num(v) or -1)
    if not 1 <= n <= len(ordine) or ok not in ordine:
        sys.exit(f"{dove}: 'Alternative fisse' vuota, 'tutte' o un numero da 1 a {len(ordine)}; la risposta corretta deve comparire fra le colonne 'Alternativa'")
    return n


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
            ordine = list(dict.fromkeys(x for x in (s(r[i]) for i in alt if i < len(r)) if x))
            errate = [x for x in ordine if x != ok]  # testi distinti: chiave dei distrattori
            if not errate:
                sys.exit(f"Foglio {ws.title!r} riga {n}: nessuna alternativa errata")
            fisse = fisse_alternative(get("alternative fisse"), ordine, ok, f"Foglio {ws.title!r} riga {n}")
            fogli.setdefault(ws.title, []).append({
                "foglio": ws.title, "riga": n, "testo": testo, "corretta": ok, "errate": errate, "ordine": ordine, "fisse": fisse,
                "colonne": int(num(get("numero colonne alternative")) or 1),
                "punti": [num(get("punteggio corretta")), num(get("punteggio non data")), num(get("punteggio errata"))],
                "ind": s(get("indicatore")).upper() or None, "arg": s(get("argomento")),
            })
    if not fogli:
        sys.exit("Nessun foglio valido: servono le colonne 'Testo della domanda' e 'Risposta corretta'")
    righe = [q for qs in fogli.values() for q in qs]
    if any(q["ind"] for q in righe):
        for q in righe:
            if q["ind"] not in INDICATORI:
                sys.exit(f"Foglio {q['foglio']!r} riga {q['riga']}: 'Indicatore' deve essere {'/'.join(INDICATORI)} "
                         f"(trovato {q['ind']!r}); se la colonna e' usata serve in ogni riga")
    return fogli


def crea_varianti(fogli, n, base, rng, pesi=None):
    uso = {(f, q["riga"]): 0 for f, qs in fogli.items() for q in qs}
    visti, varianti, codici = set(), [], set()
    rif = tuple(round(pesi.get(i, 0) / 1000, 9) for i in INDICATORI) if pesi else None
    for _ in range(n):
        cand = []
        # fase 1: rotazione delle versioni; fase 2 (solo con indicatori e nessun candidato valido): qualunque riga
        for libero, tentativi in ((False, 200), (True, 2000)):
            for _t in range(tentativi):
                scelte = []
                for f, qs in fogli.items():
                    minimo = min(uso[(f, q["riga"])] for q in qs)
                    q = rng.choice([q for q in qs if libero or uso[(f, q["riga"])] == minimo])
                    alt = [q["corretta"]] + q["errate"]
                    if q["fisse"]:  # le ultime N restano in coda nell'ordine scritto, le altre si mescolano
                        alt = q["ordine"][:len(q["ordine"]) - q["fisse"]]
                        rng.shuffle(alt)
                        alt += q["ordine"][len(q["ordine"]) - q["fisse"]:]
                    else:
                        rng.shuffle(alt)
                    scelte.append({**q, "alternative": alt, "corretta": "ABCDEFGHIJ"[alt.index(q["corretta"])],
                                   "punti": [p if p is not None else b for p, b in zip(q["punti"], base)]})
                    for k in ("errate", "ordine", "fisse"):
                        del scelte[-1][k]
                rng.shuffle(scelte)
                firma = tuple((q["foglio"], q["riga"], tuple(q["alternative"])) for q in scelte)
                if firma in visti:
                    continue
                mx = mx_ind(scelte)
                cand.append((quote(mx) if mx else None, firma, scelte))
                if not mx:
                    break  # senza indicatori basta la prima combinazione distinta
            if rif is None and cand and cand[0][0]:  # prima variante senza --pesi: profilo piu' frequente tra i candidati
                rif = Counter(c[0] for c in cand).most_common(1)[0][0]
            cand = [c for c in cand if c[0] == rif] if rif else cand
            if cand:
                if libero:
                    print("Attenzione: per mantenere i profili per indicatore uguali ho ignorato la rotazione delle versioni", file=sys.stderr)
                break
            if not any(q["ind"] for qs in fogli.values() for q in qs):
                break
        if cand:
            _, firma, scelte = rng.choice(cand)
        elif rif:
            sys.exit("Nessuna variante con quote di punti per indicatore identiche a "
                     + ", ".join(f"{i} {100 * r:.1f}%" for i, r in zip(INDICATORI, rif) if r)
                     + ": cambia --pesi, gli indicatori o i punteggi delle righe")
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


def latex_variante(v, base, nota=""):
    c, nd, e = base
    punteggi = f"Punti per risposta corretta: {fmt(c)} $\\cdot$ non data: {fmt(nd)} $\\cdot$ errata: {fmt(e)}"
    if any(q["punti"] != list(base) for q in v["domande"]):
        punteggi += " (salvo diversa indicazione)"
    punteggi += nota
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
            .replace("%%DOMANDE%%", "\n".join(corpo)).replace("%%FOGLIO%%", omr.tikz(v)))


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
    nota = (f" $\\cdot$ risposta annullata: {fmt(a.annullata)}" if a.annullata is not None else "") \
        + (f" $\\cdot$ punteggio minimo: {fmt(a.minimo)}" if a.minimo is not None else "")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pesi = parse_pesi(a.pesi) if a.pesi else None
    varianti = crea_varianti(leggi_domande(a.domande), a.varianti, base, random.SystemRandom(), pesi)
    for v in varianti:
        v["foglio"] = omr.layout([len(q["alternative"]) for q in v["domande"]])
    if mx_ind(varianti[0]["domande"]):
        pesi = {i: round(1000 * q, 4) for i, q in zip(INDICATORI, quote(mx_ind(varianti[0]["domande"]))) if q}
        for v in varianti:
            print(f"{v['codice']}: " + ", ".join(f"{i} {fmt(m)} pt" for i, m in mx_ind(v["domande"]).items()))
        print("Pesi su 1000 (uguali in ogni variante): " + ", ".join(f"{i} {fmt(p)}" for i, p in pesi.items()))
    else:
        pesi = None
    (out / "quiz_chiavi.json").write_text(json.dumps({"base": base, "annullata": a.annullata, "minimo": a.minimo, "soglia": a.soglia, "pesi": pesi, "varianti": varianti},
                                                     ensure_ascii=False, indent=1), encoding="utf-8")
    wb = Workbook()
    ws = wb.active
    ws.title = "Chiavi"
    ws.append(["Codice", "N", "Foglio", "Riga Excel", "Corretta", "Indicatore"])
    for v in varianti:
        for q in v["domande"]:
            ws.append([v["codice"], q["n"], q["foglio"], q["riga"], q["corretta"], q["ind"]])
    wb.save(out / "quiz_chiavi.xlsx")
    wb = Workbook()
    wb.active.append(["ID", "Codice"] + list(range(1, len(varianti[0]["domande"]) + 1)))
    wb.save(out / "risposte_studenti.xlsx")
    for v in varianti:
        tex = out / f"quiz_{v['codice']}.tex"
        tex.write_text(latex_variante(v, base, nota), encoding="utf-8")
        if not a.no_pdf:
            ok = compila(tex)
            pag = int(next((l.split()[1] for l in subprocess.run(["pdfinfo", str(tex.with_suffix(".pdf"))], capture_output=True, text=True).stdout.splitlines()
                            if l.startswith("Pages:")), 0)) if ok else 0
            print(f"{tex.stem}: " + (f"PDF ok, {pag} pagine" + ("" if pag % 2 == 0 else " (DISPARI: controllare)") if ok else "compilazione fallita (vedi .log)"))
    print(f"Codici variante: {', '.join(v['codice'] for v in varianti)}\nOutput in {out}/")


# -------------------------------------------------------------- correggi

def voto(tot):
    import correzione  # voto in decimi dalla scala 1000, come le altre verifiche
    return correzione.voto(tot)


def correggi_studenti(chiavi, path):
    per_codice = {v["codice"]: v for v in chiavi["varianti"]}
    righe = list(load_workbook(path, data_only=True).active.iter_rows(values_only=True))
    col = {s(h).lower(): i for i, h in enumerate(righe[0]) if s(h)}  # colonne per intestazione: 'Nome' e' facoltativa
    if not {"id", "codice"} <= col.keys():
        sys.exit("Intestazione senza 'ID' e 'Codice'")
    cella = lambda r, k: r[col[k]] if k in col and col[k] < len(r) else None
    studenti, visti = [], set()
    for n, r in enumerate(righe[1:], start=2):
        if not any(s(x) for x in r):
            continue
        sid, codice, nome = s(cella(r, "id")), s(cella(r, "codice")).upper(), s(cella(r, "nome"))
        if not sid or sid in visti:
            sys.exit(f"Riga {n}: ID mancante o duplicato ({sid!r})")
        visti.add(sid)
        if codice not in per_codice:
            sys.exit(f"Riga {n}: codice variante {codice!r} sconosciuto")
        esiti, scelte, pt, mx = [], [], 0.0, 0.0
        pi, mi = {}, {}
        for q in per_codice[codice]["domande"]:
            risp = s(cella(r, str(q["n"]))).upper()
            c, nd, e = q["punti"]
            mx += c
            if not risp or risp == "*":  # '*' = annullata (due cerchi, o confermata dal docente): non data, punti --annullata
                stato, p = "n", nd if not risp or chiavi.get("annullata") is None else chiavi["annullata"]
            elif risp == q["corretta"]:
                stato, p = "c", c
            else:
                stato, p = "e", e
                if risp not in "ABCDEFGHIJ"[:len(q["alternative"])]:
                    print(f"Riga {n}, domanda {q['n']}: risposta {risp!r} non valida, contata errata", file=sys.stderr)
            pt += p
            if q.get("ind"):
                pi[q["ind"]], mi[q["ind"]] = pi.get(q["ind"], 0) + p, mi.get(q["ind"], 0) + c
            esiti.append((q["foglio"], stato))
            scelte.append((q["foglio"], q["riga"], q["alternative"]["ABCDEFGHIJ".index(risp)] if risp and risp in "ABCDEFGHIJ"[:len(q["alternative"])] else None))
        if chiavi.get("minimo") is not None and pt < chiavi["minimo"] and mx:  # minimo sul totale; gli indicatori scalano in proporzione
            pt, pi = chiavi["minimo"], {i: chiavi["minimo"] * m / mx for i, m in mi.items()}
        studenti.append({"id": sid, "nome": nome, "codice": codice, "esiti": esiti, "scelte": scelte, "punti": pt, "max": mx,
                         "perc": round(pt / mx * 100, 2) if mx else 0.0,
                         "ind": {i: pi[i] / mx * 1000 for i in pi} if chiavi.get("pesi") and mx else None})
    if not studenti:
        sys.exit("Nessuno studente nel file risposte")
    return studenti


def calcola_statistiche(studenti, soglia):
    perc = sorted(x["perc"] for x in studenti)
    media, dev = st.fmean(perc), st.pstdev(perc)
    bounds = [statistiche.percentile(perc, p) for p in (4, 11, 23, 40, 60, 77, 89, 96)]
    for x in studenti:
        x["z"] = round((x["perc"] - media) / dev, 2) if dev else 0.0
        x["percentile"] = round((sum(p < x["perc"] for p in perc) + sum(p <= x["perc"] for p in perc)) / 2 / len(perc) * 100, 2)
        x["stanine"] = bisect_right(bounds, x["perc"]) + 1
        x["sufficiente"] = x["perc"] >= soglia * 100
    perc_ordine = [x["perc"] for x in studenti]
    domande = {}
    for x in studenti:
        for f, stato in x["esiti"]:
            domande.setdefault(f, {"c": 0, "e": 0, "n": 0})[stato] += 1
    for f, d in domande.items():
        tot = d["c"] + d["e"] + d["n"]
        d.update({"tot": tot, "difficolta": round(1 - d["c"] / tot, 2),
                  "discriminazione": statistiche.discriminazione([dict(x["esiti"])[f] == "c" for x in studenti], perc_ordine)})
    classe = statistiche.descrittive(perc) + [("Soglia sufficienza %", soglia * 100),
                                              ("Sufficienti %", round(100 * sum(x["sufficiente"] for x in studenti) / len(studenti), 2))]
    M = [[dict(x["esiti"])[f] == "c" for x in studenti] for f in domande]  # item 0/1: alpha = KR-20
    classe += statistiche.affidabilita_righe(M, len(studenti), "domande corrette")
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
    correggi(chiavi, a.risposte or out / "risposte_studenti.xlsx", a.soglia, Path(a.risultati or out))


def correggi(chiavi, risposte, soglia, dest):
    """Scrive in dest quiz_risultati.xlsx, statistiche_*.csv e statistiche.md."""
    dest.mkdir(parents=True, exist_ok=True)
    soglia = soglia if soglia is not None else chiavi["soglia"]
    studenti = correggi_studenti(chiavi, risposte)
    domande, classe, perc = calcola_statistiche(studenti, soglia)
    wb = Workbook()
    ws = wb.active
    ws.title = "Studenti"
    pesi = chiavi.get("pesi") or {}
    nomi = any(x["nome"] for x in studenti)  # la colonna Nome compare solo se compilata (scansioni)
    ws.append((["ID", "Nome"] if nomi else ["ID"]) + ["Codice", "Corrette", "Non date", "Errate", "Punteggio", "Massimo", "%", "Sufficiente", "z", "Percentile", "Stanine"]
              + [f"{i} (max {fmt(p)})" for i, p in pesi.items()] + ["Totale su 1000", "Voto"])
    for x in studenti:
        cnt = [sum(s_ == k for _, s_ in x["esiti"]) for k in "cne"]
        tot = round(sum(x["ind"].values()), 6) if pesi else round(x["punti"] / x["max"] * 1000, 6)
        if pesi:  # per costruzione (quote uguali in ogni variante) il voto dagli indicatori e dai punti coincide
            assert voto(tot) == voto(round(x["punti"] / x["max"] * 1000, 6)), f"{x['id']}: voti diversi, chiavi non coerenti"
        ws.append([x["id"]] + ([x["nome"]] if nomi else []) + [x["codice"], *cnt, x["punti"], x["max"], x["perc"], "sì" if x["sufficiente"] else "no",
                   x["z"], x["percentile"], x["stanine"]] + [round(x["ind"].get(i, 0), 2) for i in pesi] + [round(tot, 2), voto(tot)[0]])
    wd = wb.create_sheet("Domande")
    wd.append(["Foglio", "Corrette", "Errate", "Non date", "% corrette", "% errate", "% non date", "Difficoltà (1-%corrette)", "Discriminazione", "Nota"])
    for f, d in domande.items():
        wd.append([f, d["c"], d["e"], d["n"], *(round(100 * d[k] / d["tot"], 2) for k in "cen"), d["difficolta"], d["discriminazione"],
                   statistiche.segnale(d["c"] / d["tot"], d["discriminazione"])])
    wx = wb.create_sheet("Distrattori")
    wx.append(["Foglio", "Riga Excel", "Alternativa", "Corretta", "Scelte", "% sugli studenti", "Nota", "Indicatore"])
    ind_riga = {(q["foglio"], q["riga"]): q["ind"] for v in chiavi["varianti"] for q in v["domande"]}
    for (f, riga), d in ({} if chiavi.get("senza_distrattori") else distrattori(chiavi, studenti)).items():
        for alt, n in d["conta"].items():
            ok = alt == d["giusta"]
            nota = "" if ok else ("mai scelto: poco plausibile" if n == 0 else "più scelto della corretta" if n > d["conta"][d["giusta"]] else "")
            wx.append([f, riga, alt, "sì" if ok else "", n, round(100 * n / d["tot"], 2), nota, ind_riga[(f, riga)]])
        wx.append([f, riga, "(non data)", "", d["non_data"], round(100 * d["non_data"] / d["tot"], 2), ""])
    wc = wb.create_sheet("Classe")
    ind_tab = []
    if pesi:
        medie = {i: st.fmean(x["ind"].get(i, 0) for x in studenti) for i in pesi}
        classe += [(f"Media {i} su {fmt(p)}", round(medie[i], 2)) for i, p in pesi.items()]
        classe.append(("Media totale su 1000", round(st.fmean(sum(x["ind"].values()) for x in studenti), 2)))
        ind_tab = [[i, "", p, round(medie[i], 2), round(100 * medie[i] / p, 1), "debole" if 100 * medie[i] / p < statistiche.DEBOLE else ""] for i, p in pesi.items()]
    for r in classe:
        wc.append(list(r))
    wc.append([])
    wc.append(["Fascia %", "Studenti"])
    base = wc.max_row
    for r in statistiche.fasce(perc):
        wc.append(r)
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
    wb.save(dest / "quiz_risultati.xlsx")
    tab = {"classe": (["Misura", "Valore"], classe),
           "domande": ([c.value for c in wd[1]], [list(r) for r in wd.iter_rows(min_row=2, values_only=True)])}
    if wx.max_row > 1:
        tab["distrattori"] = ([c.value for c in wx[1]], [list(r) for r in wx.iter_rows(min_row=2, values_only=True)])
    if ind_tab:
        tab["indicatori"] = (["Indicatore", "Evidenze", "Max", "Media punti", "Media %", "Nota"], ind_tab)
    tab["distribuzione"] = (["Fascia %", "Studenti"], statistiche.fasce(perc))
    statistiche.scrivi(dest, tab, "Statistiche del quiz")
    print(f"{len(studenti)} studenti corretti, media {classe[1][1]}%. Risultati in {dest / 'quiz_risultati.xlsx'}")


def scrivi_letture(dest, L):
    """letture.json e' la fonte; risposte_scansioni.xlsx (risposte + Anomalie ancora da rivedere) ne e' derivato."""
    (dest / "letture" / "letture.json").write_text(json.dumps(L, ensure_ascii=False), encoding="utf-8")
    wb = Workbook()
    ws, wa = wb.active, wb.create_sheet("Anomalie")
    ws.append(["ID", "Nome", "Codice"] + list(range(1, L["nq"] + 1)))
    wa.append(["ID", "File", "Domanda", "Stato", "Riempimento per alternativa"])
    for f in L["fogli"]:
        r = {d["n"]: d["risposta"] or None for d in f["domande"]}
        ws.append([f["id"], f["nome"], f["codice"]] + [r.get(i) for i in range(1, L["nq"] + 1)])
        for d in sorted(f["domande"], key=lambda d: d["conf"]):  # prima i dubbi maggiori
            if d["stato"] in ("proposta", "annullata") and not d["rivista"]:
                wa.append([f["id"], f["file"], d["n"], d["stato"], " ".join(f"{l}={v}" for l, v in zip(omr.LETTERE, d["fill"]))])
    for e in L["errori"]:
        wa.append([e["id"], e["file"], "", e["messaggio"], ""])
    wb.save(dest / "risposte_scansioni.xlsx")


def cmd_leggi(a):
    """Legge i fogli risposte scansionati: risposte_scansioni.xlsx + letture/ (immagini e letture.json per `rivedi`)."""
    out = Path(a.out)
    chiavi = json.loads((out / "quiz_chiavi.json").read_text(encoding="utf-8"))
    per_codice = {v["codice"]: v for v in chiavi["varianti"]}
    dest = Path(a.risultati or a.out)  # le chiavi si leggono da --out, i risultati si scrivono in --risultati
    (dest / "letture").mkdir(parents=True, exist_ok=True)
    import cv2
    L = {"nq": len(chiavi["varianti"][0]["domande"]), "geom": {c: v["foglio"]["bolle"] for c, v in per_codice.items()}, "fogli": [], "errori": []}
    for f in sorted(p for p in Path(a.scansioni).rglob("*") if p.suffix.lower() in (".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff")):
        fogli = [r for r in (omr.leggi_pagina(g, per_codice) for g in omr.pagine(f)) if r]
        if not fogli:
            L["errori"].append({"id": "", "file": f.name, "messaggio": "nessun foglio risposte riconosciuto (4 quadrati agli angoli)"})
        for r in fogli:
            sid = f"S{len(L['fogli']) + 1:02d}"
            cv2.imwrite(str(dest / "letture" / f"{sid}_nome.png"), r["nome"])
            cv2.imwrite(str(dest / "letture" / f"{sid}.png"), r["img"])
            if r.get("errore"):
                L["errori"].append({"id": sid, "file": f.name, "messaggio": r["errore"]})
            L["fogli"].append({"id": sid, "file": f.name, "codice": r["codice"], "domande": r["domande"],
                               "nome": f.stem.replace("_", " ") if len(fogli) == 1 else ""})
    scrivi_letture(dest, L)
    da_rivedere = sum(d["stato"] in ("proposta", "annullata") for f in L["fogli"] for d in f["domande"])
    print(f"{len(L['fogli'])} fogli letti, {da_rivedere} domande da rivedere. Controlla e correggi con: quiz.py rivedi --out {a.out}"
          + (f" --risultati {dest}" if a.risultati else "") + f"\nPoi: quiz.py correggi --risposte {dest}/risposte_scansioni.xlsx")


def applica_modifiche(L, m):
    """Riporta in L solo i campi modificabili (nome, risposta, rivista) validandoli: la richiesta arriva dal browser."""
    per_id = {f["id"]: f for f in L["fogli"]}
    for fm in m["fogli"]:
        f = per_id[fm["id"]]
        f["nome"] = str(fm["nome"])[:80]
        dom = {d["n"]: d for d in f["domande"]}
        for dm in fm["domande"]:
            d, r = dom[dm["n"]], str(dm["risposta"])
            if r not in ("", "*", *omr.LETTERE[:len(d["fill"])]):
                raise ValueError(f"risposta {r!r} non valida")
            d["risposta"], d["rivista"] = r, bool(dm["rivista"])


def cmd_rivedi(a):
    """Editor delle letture nel browser: server locale (127.0.0.1) con pagina in assets/rivedi/, nessun dato esce dal PC."""
    import re
    import secrets
    import webbrowser
    from http.server import BaseHTTPRequestHandler, HTTPServer
    dest = Path(a.risultati or a.out)
    lett = dest / "letture"
    if not (lett / "letture.json").exists():
        sys.exit(f"Manca {lett}/letture.json: esegui prima quiz.py leggi")
    L = json.loads((lett / "letture.json").read_text(encoding="utf-8"))
    token, pagina = secrets.token_urlsafe(16), TEMPLATE.parent / "rivedi"

    class H(BaseHTTPRequestHandler):
        def invia(self, code, body=b"", tipo="text/plain"):
            self.send_response(code)
            self.send_header("Content-Type", tipo + "; charset=utf-8" if tipo.startswith("text") else tipo)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def host_ok(self):  # contro il DNS rebinding: la pagina vale solo sul nome locale
            return self.headers.get("Host") in (f"127.0.0.1:{srv.server_port}", f"localhost:{srv.server_port}")

        def do_GET(self):
            if not self.host_ok():
                return self.invia(403)
            if self.path == "/":
                return self.invia(200, (pagina / "rivedi.html").read_text(encoding="utf-8").replace("%%TOKEN%%", token).encode(), "text/html")
            if self.path == "/rivedi.js":
                return self.invia(200, (pagina / "rivedi.js").read_bytes(), "text/javascript")
            if self.path == "/letture.json":
                return self.invia(200, json.dumps(L, ensure_ascii=False).encode(), "application/json")
            m = re.fullmatch(r"/img/(S\d+(?:_nome)?\.png)", self.path)
            if m and (lett / m[1]).exists():
                return self.invia(200, (lett / m[1]).read_bytes(), "image/png")
            self.invia(404)

        def do_POST(self):
            if self.path != "/salva" or not self.host_ok() or self.headers.get("X-Token") != token:
                return self.invia(403)
            n = int(self.headers.get("Content-Length") or 0)
            if n > 5_000_000:
                return self.invia(413)
            try:
                applica_modifiche(L, json.loads(self.rfile.read(n)))
            except (ValueError, KeyError, TypeError) as e:
                return self.invia(400, str(e).encode())
            scrivi_letture(dest, L)
            self.invia(204)

        def log_message(self, *_):
            pass

    srv = HTTPServer(("127.0.0.1", 0), H)
    url = f"http://127.0.0.1:{srv.server_port}/"
    print(f"Editor delle letture su {url} (Ctrl+C per chiudere). Le modifiche si salvano da sole in {dest}/risposte_scansioni.xlsx", flush=True)
    if not a.no_browser:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("genera", help="crea PDF delle varianti, chiavi e template risposte")
    g.add_argument("domande", help="xlsx: un foglio per domanda; colonne 'Testo della domanda', 'Risposta corretta', 'Alternativa 1..'; "
                   "facoltative 'Numero Colonne Alternative', 'Alternative fisse' (tutte, o N = le ultime N restano in coda), 'Punteggio corretta', 'Punteggio non data', 'Punteggio errata', 'Indicatore' (ANA/SVI/ARG/COM), 'Argomento'")
    g.add_argument("--varianti", type=int, default=2)
    g.add_argument("--corretta", type=float, default=4, help="punti risposta corretta (default 4)")
    g.add_argument("--non-data", type=float, default=1, help="punti risposta non data (default 1)")
    g.add_argument("--errata", type=float, default=0, help="punti risposta errata (default 0)")
    g.add_argument("--annullata", type=float, help="punti risposta annullata (due cerchi; default: come non data)")
    g.add_argument("--minimo", type=float, help="punteggio minimo del quiz (default: nessuno; con --errata negativa evita totali negativi)")
    g.add_argument("--soglia", type=float, default=0.58, help="soglia di sufficienza, frazione (default 0.58)")
    g.add_argument("--pesi", help="con colonna 'Indicatore': pesi su 1000, es. ANA=250,SVI=400,ARG=200,COM=150 (default: il profilo piu' frequente)")
    g.add_argument("--out", default="quiz_out")
    g.add_argument("--no-pdf", action="store_true", help="scrive solo i .tex")
    g.set_defaults(f=cmd_genera)
    l = sub.add_parser("leggi", help="legge i fogli risposte scansionati (OpenCV) e produce risposte_scansioni.xlsx")
    l.add_argument("scansioni", help="cartella (o file) con PDF/immagini dei fogli risposte")
    l.add_argument("--out", default="quiz_out", help="cartella con quiz_chiavi.json")
    l.add_argument("--risultati", help="dove scrivere risposte_scansioni.xlsx e letture/ (default: --out)")
    l.set_defaults(f=cmd_leggi)
    r = sub.add_parser("rivedi", help="editor nel browser delle letture: conferma le risposte proposte, correggi o segna a mano")
    r.add_argument("--out", default="quiz_out", help="cartella con quiz_chiavi.json")
    r.add_argument("--risultati", help="dove sta letture/ (default: --out)")
    r.add_argument("--no-browser", action="store_true", help="non aprire il browser")
    r.set_defaults(f=cmd_rivedi)
    c = sub.add_parser("correggi", help="corregge risposte_studenti.xlsx e produce quiz_risultati.xlsx")
    c.add_argument("--out", default="quiz_out", help="cartella con quiz_chiavi.json")
    c.add_argument("--risultati", help="dove scrivere quiz_risultati.xlsx e statistiche (default: --out)")
    c.add_argument("--risposte", help="default: <out>/risposte_studenti.xlsx")
    c.add_argument("--soglia", type=float, help="sovrascrive la soglia salvata da genera")
    c.set_defaults(f=cmd_correggi)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
