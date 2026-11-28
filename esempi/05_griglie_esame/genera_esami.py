#!/usr/bin/env python3
"""Griglie d'esame (matematica, fisica, mista), solo su richiesta del docente: evidenze -> registro con --griglia ->
check -> correttore LaTeX (boxind/boxdat, \\tabpuntiesame) -> PDF, più la prova dello studente.
Esecuzione: python3 genera_esami.py. I testi stanno in questo file; i template si leggono da verifiche-mat-fis/assets."""
import json
import re
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
SKILL = QUI.parents[1] / "verifiche-mat-fis"
NOMI_IND = {"ANA": "ANA", "IND": "IND", "SVI": "SVI", "ARG": "ARG", "DAT": "DAT"}

ESAMI = {
 "matematica": dict(
  classe="Classe quinta, liceo scientifico \\textperiodcentered\\ Prova modellata sulla seconda prova di matematica",
  ordine=("ANA", "IND", "SVI", "ARG"), rinomina=r"\renewcommand{\nomeANA}{Comprendere}\renewcommand{\nomeSVI}{Sviluppare il processo risolutivo}",
  sigle={"FUN": "Studio di funzione", "INT": "Integrali", "TEO": "Teoremi sulle funzioni continue"},
  esercizi={"1": ("Problema", r"Sia $f(x)=x\,e^{-x}$. (a) Determina dominio, limiti agli estremi e asintoti. (b) Studia monotonia ed estremi. (c) Studia concavità e flessi. (d) Calcola l'area della regione fra il grafico, l'asse $x$ e le rette $x=0$ e $x=1$. (e) Commenta la coerenza dei risultati con l'andamento del grafico."),
            "2": ("Quesito", r"Dimostra che l'equazione $x\,e^{-x}=\tfrac14$ ha esattamente due soluzioni reali e localizzale in intervalli di ampiezza $1$.")},
  ev=[
   ("1", "ANA", "FUN", 50, "1", "Individua dominio e limiti da calcolare", [r"La funzione è definita e continua su $\mathbb R$: nessuna condizione di esistenza.", r"I limiti rilevanti sono per $x\to-\infty$ e $x\to+\infty$."]),
   ("1", "SVI", "FUN", 50, "1", "Calcola limiti e asintoto", [r"$\lim_{x\to-\infty}xe^{-x}=-\infty$.", r"$\lim_{x\to+\infty}xe^{-x}=0$ (l'esponenziale prevale): asintoto orizzontale $y=0$."]),
   ("1", "IND", "FUN", 80, "2A", "Sceglie il segno della derivata prima", [r"Monotonia ed estremi si studiano con il segno di $f'$.", r"I punti stazionari si trovano con $f'(x)=0$."]),
   ("1", "SVI", "FUN", 80, "1", "Calcola $f'$ e individua il massimo", [r"$f'(x)=(1-x)e^{-x}$.", r"$f'>0$ per $x<1$ e $f'<0$ per $x>1$.", r"Massimo assoluto in $\left(1,\frac1e\right)$."]),
   ("1", "IND", "FUN", 70, "2", "Sceglie la derivata seconda", [r"Concavità e flessi si studiano con il segno di $f''$."]),
   ("1", "SVI", "FUN", 50, "1", "Calcola $f''$ e il flesso", [r"$f''(x)=(x-2)e^{-x}$.", r"Flesso in $\left(2,\frac2{e^2}\right)$: concavità verso il basso per $x<2$, verso l'alto per $x>2$."]),
   ("1", "ANA", "INT", 100, "2A", "Traduce l'area in un integrale", [r"Su $[0,1]$ è $f\ge0$: l'area è $\int_0^1 xe^{-x}\,dx$."]),
   ("1", "IND", "INT", 70, "2", "Sceglie l'integrazione per parti", [r"Il prodotto $x\cdot e^{-x}$ si integra per parti con $u=x$ e $dv=e^{-x}dx$."]),
   ("1", "SVI", "INT", 70, "2", "Calcola l'integrale", [r"$\int xe^{-x}dx=-xe^{-x}-e^{-x}+c$.", r"$\int_0^1xe^{-x}dx=1-\frac2e\approx0{,}264$."]),
   ("1", "ARG", "FUN", 100, "3", "Commenta la coerenza con il grafico", [r"Il massimo vale $\frac1e\approx0{,}37$: su $[0,1]$ l'area è minore di $0{,}37$, coerente con $0{,}264$.", r"Crescita fino a $x=1$, flesso in $x=2$ e tendenza a $0$ concordano con i segni di $f'$, $f''$ e con l'asintoto."]),
   ("2", "ANA", "TEO", 100, "2A", "Individua le proprietà utili", [r"$f$ cresce su $(-\infty,1]$ da $-\infty$ a $\frac1e$ e decresce su $[1,+\infty)$ da $\frac1e$ a $0$.", r"Per $x\le0$ è $f\le0<\frac14$: le soluzioni sono in $x>0$."]),
   ("2", "IND", "TEO", 80, "2", "Sceglie valori intermedi e monotonia", [r"Su ogni tratto monotono la continuità assicura l'esistenza e la monotonia l'unicità."]),
   ("2", "ARG", "TEO", 100, "3", "Motiva e localizza le due soluzioni", [r"$f(0)=0<\frac14<f(1)=\frac1e$: una soluzione in $(0,1)$, unica per la crescita.", r"$f(2)=\frac2{e^2}\approx0{,}271>\frac14>f(3)=\frac3{e^3}\approx0{,}149$: una soluzione in $(2,3)$, unica per la decrescita.", r"Non ce ne sono altre."]),
  ]),
 "fisica": dict(
  classe="Classe quarta, liceo scientifico \\textperiodcentered\\ Prova modellata sulla seconda prova di fisica",
  ordine=("ANA", "SVI", "DAT", "ARG"), rinomina=r"\renewcommand{\nomeSVI}{Sviluppare il processo risolutivo}\renewcommand{\nomeDAT}{Interpretare criticamente i dati}",
  sigle={"MOL": "Legge di Hooke e dati sperimentali", "OSC": "Oscillatore armonico"},
  esercizi={"1": ("Problema, parte sperimentale", r"Una molla è allungata da forze $F=0{,}5;\,1{,}0;\,1{,}5;\,2{,}0;\,2{,}5\ \si{N}$ (errore $\SI{0.01}{N}$) e si misurano gli allungamenti $x=21;\,40;\,62;\,81;\,101\ \si{mm}$ (errore $\SI{1}{mm}$). (a) Rappresenta i dati $F$--$x$ con le barre di errore. (b) Determina la costante elastica con una regressione lineare e la sua incertezza. (c) Discuti se la legge di Hooke è pertinente ai dati."),
            "2": ("Problema, parte teorica", r"Alla molla è appesa una massa di $\SI{0.500}{kg}$ che oscilla verticalmente con ampiezza $\SI{5.0}{cm}$; trascura gli attriti e usa la costante trovata. Scrivi la legge oraria, determina periodo, velocità massima ed energia meccanica, e verifica la coerenza fra l'energia e il lavoro necessario per allungare la molla di $\SI{5.0}{cm}$.")},
  ev=[
   ("1", "ANA", "MOL", 60, "1", "Riconosce la legge di Hooke come modello", [r"La forza elastica è proporzionale all'allungamento: $F=kx$.", r"I dati vanno confrontati con una retta per l'origine."]),
   ("1", "DAT", "MOL", 80, "1", "Rappresenta i dati con barre di errore", [r"Grafico $F$--$x$ con assi etichettati, unità e scala.", r"Barre di errore $\pm\SI{0.01}{N}$ e $\pm\SI{1}{mm}$."]),
   ("1", "DAT", "MOL", 100, "2A", "Esegue la regressione e ricava $k$ con incertezza", [r"Regressione lineare $F=kx+b$ con il software.", r"$k=(24{,}9\pm0{,}3)\ \si{N/m}$; $b$ compatibile con zero."]),
   ("1", "SVI", "MOL", 60, "1", "Riporta $k$ con unità e cifre corrette", [r"$k$ ha l'unità $\si{N/m}$ e due cifre dopo la virgola dell'incertezza coerenti."]),
   ("1", "ARG", "MOL", 100, "3", "Valuta la pertinenza del modello", [r"L'intercetta è compatibile con zero e i punti stanno entro le barre di errore.", r"Il modello è pertinente nell'intervallo misurato; oltre il limite elastico potrebbe non valere."]),
   ("2", "ANA", "OSC", 90, "2A", "Riconosce il moto armonico", [r"La forza di richiamo $F=-kx$ proporzionale all'allungamento dà un moto armonico semplice."]),
   ("2", "SVI", "OSC", 120, "2A", "Calcola pulsazione e periodo", [r"$\omega=\sqrt{k/m}=\sqrt{\dfrac{\SI{24.9}{N/m}}{\SI{0.500}{kg}}}=\SI{7.06}{rad/s}$.", r"$T=2\pi/\omega=\SI{0.890}{s}$."]),
   ("2", "SVI", "OSC", 120, "2", "Calcola velocità massima ed energia", [r"$v_{\max}=A\omega=\SI{0.353}{m/s}$.", r"$E=\tfrac12kA^2=\SI{0.0311}{J}$."]),
   ("2", "DAT", "OSC", 70, "2", "Confronta energia e lavoro", [r"Il lavoro per allungare la molla di $A$ è $\tfrac12kA^2=\SI{0.0311}{J}$, uguale all'energia $E$."]),
   ("2", "ARG", "OSC", 100, "3", "Giustifica la coerenza dei risultati", [r"In assenza di attriti l'energia meccanica si conserva: l'energia cinetica massima $\tfrac12mv_{\max}^2$ è uguale a $E$.", r"Il valore di $T$ è compatibile con quello atteso per $k$ e $m$ di questo ordine di grandezza."]),
   ("2", "ANA", "OSC", 100, "2", "Imposta la legge oraria", [r"$x(t)=A\cos(\omega t+\varphi)$ con $A=\SI{5.0}{cm}$ e fase iniziale scelta dalle condizioni iniziali."]),
  ]),
 "mista": dict(
  classe="Classe quarta, liceo scientifico \\textperiodcentered\\ Prova mista di matematica e fisica",
  ordine=("ANA", "SVI", "DAT", "ARG"), rinomina=r"\renewcommand{\nomeSVI}{Sviluppare il processo risolutivo}\renewcommand{\nomeDAT}{Interpretare, rappresentare, elaborare i dati}",
  sigle={"VEL": "Velocità limite e dati sperimentali", "SPA": "Spazio percorso"},
  esercizi={"1": ("Problema, parte sperimentale", r"Una sfera di massa $\SI{0.50}{kg}$ cade in un fluido con resistenza $-bv$, $b=\SI{2.0}{kg/s}$. Sono misurate le velocità $v=0{,}81;\,1{,}35;\,1{,}95;\,2{,}23;\,2{,}35\ \si{m/s}$ agli istanti $t=0{,}1;\,0{,}2;\,0{,}4;\,0{,}6;\,0{,}8\ \si{s}$. (a) Determina la velocità limite. (b) Rappresenta i dati $v$--$t$ e individua l'andamento. (c) Confronta i dati con $v(t)=\frac{mg}{b}\left(1-e^{-bt/m}\right)$ e stima la costante di tempo. (d) Discuti la compatibilità fra dati e modello."),
            "2": ("Problema, parte teorica", r"Con $v(t)=\frac{mg}{b}\left(1-e^{-bt/m}\right)$: (a) ricava l'accelerazione $a(t)$ e interpreta $a(0)$; (b) imposta e calcola lo spazio percorso nel primo secondo; (c) rappresenta $s(t)$ e confrontalo con la caduta libera; (d) giustifica il comportamento per $t\to\infty$ e la coerenza fisica.")},
  ev=[
   ("1", "ANA", "VEL", 60, "1", "Riconosce la condizione di velocità limite", [r"A velocità limite l'accelerazione è nulla: la forza peso uguaglia la resistenza, $mg=bv_\ell$."]),
   ("1", "SVI", "VEL", 60, "1", "Calcola la velocità limite", [r"$v_\ell=\dfrac{mg}{b}=\dfrac{\SI{0.50}{kg}\cdot\SI{9.81}{m/s^2}}{\SI{2.0}{kg/s}}=\SI{2.45}{m/s}$."]),
   ("1", "DAT", "VEL", 80, "1", "Rappresenta i dati e individua la saturazione", [r"Grafico $v$--$t$ con assi, unità e scala.", r"I dati crescono sempre più lentamente e tendono a $\SI{2.45}{m/s}$."]),
   ("1", "DAT", "VEL", 100, "2A", "Confronta i dati con il modello e stima $\\tau$", [r"$\tau=m/b=\SI{0.25}{s}$.", r"Per ogni $t$ misurato il modello dà $0{,}81;\,1{,}35;\,1{,}95;\,2{,}23;\,2{,}35\ \si{m/s}$, uguali ai dati entro $\SI{0.01}{m/s}$."]),
   ("1", "ARG", "VEL", 100, "3", "Valuta la compatibilità fra dati e modello", [r"Le differenze sono entro l'incertezza di lettura: dati e modello sono compatibili.", r"Cause di discrepanza: tempo di reazione, resistenza non esattamente lineare."]),
   ("2", "ANA", "SPA", 90, "2A", "Collega accelerazione e derivata di $v$", [r"$a(t)=\dfrac{dv}{dt}$; $a(0)$ è l'accelerazione iniziale quando la resistenza è nulla."]),
   ("2", "SVI", "SPA", 120, "2A", "Calcola $a(t)$ e $a(0)$", [r"$a(t)=g\,e^{-bt/m}$.", r"$a(0)=g=\SI{9.81}{m/s^2}$."]),
   ("2", "SVI", "SPA", 120, "2", "Integra $v(t)$ per lo spazio", [r"$s(t)=\dfrac{mg}{b}\left[t-\tau\left(1-e^{-t/\tau}\right)\right]$.", r"$s(\SI{1}{s})=\SI{2.45}{m/s}\cdot\left[\SI{1}{s}-\SI{0.25}{s}\cdot(1-e^{-4})\right]=\SI{1.85}{m}$."]),
   ("2", "DAT", "SPA", 70, "2", "Rappresenta $s(t)$ e confronta con la caduta libera", [r"Grafico di $s(t)$ crescente e quasi lineare per $t\gg\tau$.", r"In caduta libera si avrebbe $\tfrac12gt^2=\SI{4.9}{m}$: la resistenza riduce molto lo spazio."]),
   ("2", "ARG", "SPA", 100, "3", "Giustifica il limite e la coerenza fisica", [r"Per $t\to\infty$ è $a\to0$ e $v\to v_\ell$: la velocità non supera $\frac{mg}{b}$.", r"Lo spazio nel primo secondo è minore di quello in caduta libera, come atteso."]),
   ("2", "ANA", "SPA", 100, "2", "Imposta lo spazio come integrale", [r"$s(t)=\int_0^tv(t')\,dt'$ con $s(0)=0$."]),
  ]),
}


def run(*a, **k):
    return subprocess.run([str(x) for x in a], check=True, capture_output=True, text=True, **k)


def pdflatex(tex):
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name], cwd=tex.parent, capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-1500:])
    for e in ("aux", "log", "out"):
        tex.with_suffix(f".{e}").unlink(missing_ok=True)


def prova(nome, d):
    T = (SKILL / "assets/modello_verifica.tex").read_text(encoding="utf-8")
    head, rest = T.split("% Inserire qui le consegne concordate", 1)
    tail = "\\null" + rest.split("\\null", 1)[1]
    tail = re.sub(r"\n% Inserire qui \\supportiprova.*?% Identificativi studente su riga aperta\.\n", "\n", tail, flags=re.S)
    tail = re.sub(r"\n% Sostituire o omettere questa griglia[^\n]*\n\\grigliacompetenze", "\n", tail)
    q = "".join(f"\\question {t}\n" for _, t in d["esercizi"].values())
    (QUI / nome).mkdir(exist_ok=True)
    f = QUI / nome / "prova.tex"
    f.write_text(head + "\n\\begin{questions}\n" + q + "\\end{questions}\n" + tail, encoding="utf-8")
    pdflatex(f)


def correttore(nome, d, rows):
    T = (SKILL / "assets/correttore_template.tex").read_text(encoding="utf-8")
    ordine = d["ordine"]
    g = {i: sum(r["Max"] for r in rows if r["Indicatore"] == i) for i in ordine}
    chiave = lambda i: f"\\h{i}"
    es = list(d["esercizi"])
    b = [f"\\renewcommand{{\\materia}}{{{nome.capitalize()}}}\n\\renewcommand{{\\classe}}{{{d['classe']}}}\n{d['rinomina']}\n\\begin{{document}}\n"
         "\\begin{center}\n{\\LARGE\\bfseries Correttore\\ \\materia}\\\\[3pt]\n\\classe\n\\end{center}\n\n"
         f"\\legendaesame{{{ordine[0]}}}{{{ordine[1]}}}{{{ordine[2]}}}{{{ordine[3]}}}\n\\sez{{Registro delle evidenze}}\n"]
    for e in es:
        righe = "".join(f"{r['ID evidenza']} & {r['Descrizione evidenza']} & intero & \\sigla{{{r['Indicatore']}}} & {r['Max']}\\\\\n" for r in rows if str(r["Esercizio"]) == e)
        sig = ", ".join(sorted({r['Sigla argomento'] for r in rows if str(r['Esercizio']) == e}))
        b.append(f"\\registrogruppo{{{e}}}{{{sig}}}{{\n{righe}}}\n")
    tr = "".join(f"Esercizio {e} & " + " & ".join(str(sum(r['Max'] for r in rows if str(r['Esercizio']) == e and r['Indicatore'] == i)) for i in ordine)
                 + f" & {sum(r['Max'] for r in rows if str(r['Esercizio']) == e)}\\\\\n" for e in es)
    arg = "".join(f"{s}, {n} & {sum(r['Max'] for r in rows if r['Sigla argomento'] == s)}\\\\\n" for s, n in d["sigle"].items())
    b.append("\\riepiloghi{%\n\\begin{tabular}{@{}lrrrrr@{}}\\toprule\n & " + " & ".join(chiave(i) for i in ordine) + " & Tot\\\\\\midrule\n" + tr
             + "\\midrule\nTotale & " + " & ".join(str(g[i]) for i in ordine) + " & 1000\\\\\\bottomrule\n\\end{tabular}}{%\n\\begin{tabular}{@{}lr@{}}\\toprule\nArgomento & Max\\\\\\midrule\n"
             + arg + "\\midrule\nTotale & 1000\\\\\\bottomrule\n\\end{tabular}}\n\n\\inizioesercizi\n")
    for e in es:
        tit, testo = d["esercizi"][e]
        b.append(f"\\esercizio{{Esercizio {e} -- {tit}}}{{}}{{}}{{}}{{}}{{}}\n\\begin{{enun}}\n{testo}\n\\end{{enun}}\n")
        tot = {i: sum(r['Max'] for r in rows if str(r['Esercizio']) == e and r['Indicatore'] == i) for i in ordine}
        b.append("\\tabpuntiesame{%s}{%s}{%s}{%s}{%s}{%s}{%s}{%s}{%d}\n" % (*ordine, *[tot[i] for i in ordine], sum(tot.values())))
        for r in (r for r in rows if str(r["Esercizio"]) == e):
            ind = r["Indicatore"]
            passi = "\n".join(f"\\item {p}" for p in d["_passi"][r["ID evidenza"]])
            b.append(f"\\evidenza{{{r['ID evidenza']}}}{{{e}}}{{{ind}}}{{{r['Sigla argomento']}}}{{{r['Max']}}}\n"
                     f"\\begin{{box{ind.lower()}}}[{r['Descrizione evidenza']}]\n\\begin{{enumerate}}\n{passi}\n\\end{{enumerate}}\n\\end{{box{ind.lower()}}}\n")
    b.append("\\end{document}\n")
    f = QUI / nome / "correttore.tex"
    f.write_text(T.split("\\begin{document}")[0] + "".join(b), encoding="utf-8")
    pdflatex(f)


def main():
    for nome, d in ESAMI.items():
        (QUI / nome).mkdir(exist_ok=True)
        nomi = {s: n for s, n in d["sigle"].items()}
        rows, d["_passi"] = [], {}
        for i, (es, ind, sig, mx, liv, tit, passi) in enumerate(d["ev"], 1):
            rid = f"E{i:02d}"
            rows.append({"ID evidenza": rid, "Esercizio": es, "Punto/gruppo": "intero", "Indicatore": ind, "Sigla argomento": sig, "Max": mx,
                         "Descrizione evidenza": tit, "Nome completo argomento": nomi[sig], "Livello": liv})
            d["_passi"][rid] = passi
        js, xl = QUI / nome / "evidenze.json", QUI / nome / "registro_evidenze.xlsx"
        js.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        xl.unlink(missing_ok=True)
        py = sys.executable
        run(py, SKILL / "scripts/registro_xlsx.py", "write", js, xl, "--classe", "medio", "--griglia", nome)
        chk = run(py, SKILL / "scripts/registro_xlsx.py", "check", xl, "--classe", "medio", "--griglia", nome)
        (QUI / nome / "check_registro.txt").write_text(chk.stdout, encoding="utf-8")
        prova(nome, d)
        correttore(nome, d, rows)
        print(nome, "ok")


if __name__ == "__main__":
    main()
