"""Elaborati simulati (alunni fittizi): testo scritto a mano, percentuali per evidenza, testo delle schede.

Dati usati da build_correzione.py. Percentuale 0-100 per evidenza; 0 = tentata e sbagliata; None = non svolta.
Un solo posto da modificare per cambiare esempio: righe, pct e schede restano coerenti."""
N = None
IDS = [f"E{i:02d}" for i in range(1, 19)]


def pct(*v):
    assert len(v) == 18, len(v)
    return dict(zip(IDS, v))


ELAB = {"A": {}, "B": {}}

# ---------------------------------------------------------------- Fila A
ELAB["A"]["Esempio Anna"] = dict(
    formato="pdf", effetto="scanner",
    pagine=[
        ["1a) m = (3 - 1)/(4 + 2) = 2/6 = 1/3", "y - 1 = 1/3 (x + 2)  ⇒  x - 3y + 5 = 0", "|AB| = √(6² + 2²) = √40 = 2√10", None,
         "1b) h = d(C, AB) = |2 - 3(-3) + 5|/√(1 + 9)", "h = 16/√10", "Area = 1/2 · |AB| · h = 1/2 · 2√10 · 16/√10 = 16", None,
         "Verifica con i vertici:", "A = 1/2 |-2(3+3) + 4(-3-1) + 2(1-3)|", "A = 1/2 |-12 - 16 - 4| = 16", "I due metodi danno lo stesso valore.", None,
         "1c) stesso m = 1/3, passa per C(2; -3)", "y + 3 = 1/3 (x - 2)  ⇒  x - 3y - 11 = 0", "y = 0  ⇒  x = 11      P(11; 0)"],
        ["2) m_r = 3  ⇒  m_s = -1/3", "m_s = -k/(k + 1) = -1/3  ⇒  3k = k + 1", "k = 1/2", "Se k = -1, s è x = -5 verticale: non va bene.", None,
         "3) M = (2; 2)    m_PQ = (0 - 4)/(5 + 1) = -2/3", "m = 3/2    y - 2 = 3/2 (x - 2)", "3x - 2y - 2 = 0", "Scelgo X(0; -1): sta sull'asse (0 + 2 - 2 = 0)",
         "XP² = 1 + 25 = 26     XQ² = 25 + 1 = 26", None,
         "4) r1: 2x + y + 1 = 0     r2: -x + 2y - 3 = 0", "centro: y = -2x - 1 ; -5x - 5 = 0  ⇒  C(-1; 1)", "per (3; 0): 7k - 6 = 0 ⇒ k = 6/7 ⇒ x + 4y - 3 = 0",
         "parallela a x: 2k - 1 = 0 ⇒ k = 1/2 ⇒ y = 1", "r1 non si ottiene: servirebbe r2 proporzionale a r1,", "ma le due rette sono incidenti."],
    ],
    pct=pct(100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 80, 90),
    schede={
        "1": (["retta AB, lunghezza e altezza calcolate bene", "area confermata con i vertici", "parallela per C e intersezione con l'asse $x$"], []),
        "2": (["condizione di perpendicolarità e valore $k=\\frac12$", "caso della retta verticale escluso"], []),
        "3": (["asse scritto con punto medio e pendenza", "equidistanza verificata con un punto"], []),
        "4": (["centro $(-1,1)$, retta per $(3,0)$ e $y=1$"], ["la motivazione sulla generatrice è corretta ma breve: indica anche che occorrerebbe $k\\to\\infty$"]),
    },
    aree=["Completa le motivazioni con il caso limite $k\\to\\infty$.", "Scrivi le unità e le conclusioni in una frase finale."],
)

ELAB["A"]["Prova Bruno"] = dict(
    formato="pdf", effetto="scanner",
    pagine=[
        ["1a) m = (3 - 1)/(4 + 2) = 1/3", "y - 1 = 1/3 (x + 2)   x - 3y + 5 = 0", "|AB| = √(36 + 4) = √40 = 2√10", None,
         "1b) h = |2 - 9 + 5|/√10 = 2/√10", "Area = 1/2 · 2√10 · 2/√10 = 2", None,
         "1c) m = 1/3   y + 3 = 1/3 (x - 2)", "x - 3y - 11 = 0     y = 0 ⇒ x = 11", None,
         "2) m_r = 3   m_s = -k/(k + 1) = -1/3", "3k = k + 1  ⇒  k = 1/2"],
        ["3) M = (2; 2)   m_PQ = -4/6 = -2/3", "asse: m = 3/2   y - 2 = 3/2 (x - 2)", "3x - 2y - 2 = 0", None,
         "4) r1: 2x + y + 1 = 0    r2: -x + 2y - 3 = 0", "C = r1 ∩ r2 = (-1; 1)", "per (3; 0): 7k - 6 = 0 ⇒ k = 7/6", "parallela a x: 2k - 1 = 0 ⇒ k = 1/2", "y = 1"],
    ],
    pct=pct(100, 100, 100, 100, 30, 100, N, 100, 100, 100, 60, 100, 100, N, 100, 50, N, 60),
    schede={
        "1": (["retta AB e lunghezza corrette", "area coerente con il valore trovato di $h$", "parallela per $C$ e intersezione $(11,0)$"],
              ["nella distanza: $-3\\cdot(-3)=+9$, non $-9$; il numeratore è $|2+9+5|=16$", "manca la verifica dell'area con un secondo metodo"]),
        "2": (["condizione di perpendicolarità e $k=\\frac12$"], ["non è discusso il caso $k=-1$ (retta verticale)"]),
        "3": (["asse scritto correttamente"], ["manca la verifica dell'equidistanza di un punto dell'asse"]),
        "4": (["centro $(-1,1)$ e retta parallela all'asse $x$"], ["da $7k-6=0$ segue $k=\\frac67$, non $\\frac76$", "manca la motivazione sulla prima generatrice"]),
    },
    aree=["Controlla i segni nelle sostituzioni prima di calcolare.", "Verifica sempre il risultato con un secondo metodo o un punto di prova.", "Discuti i casi particolari del parametro."],
)

ELAB["A"]["Modello Chiara"] = dict(
    formato="cartella", effetto="foto",
    pagine=[
        ["1a) m = (3 - 1)/(4 + 2) = 1/3", "y - 1 = 1/3 (x + 2)  ⇒  y = x/3 + 5/3", "|AB| = √(6 + 2) = √8 = 2√2", None,
         "1b) y = x/3 + 5/3 ⇒ a = 1/3, b = 1, c = 5/3", "d = |1/3 · 2 + 1 · (-3) + 5/3|/√(1/9 + 1)", "d = 2/3 · 3/√10 = 2/√10", None,
         "1c) ", ("y + 3 = 3(x - 2)", {"barrato": True}), "y + 3 = 1/3 (x - 2)  ⇒  y = x/3 - 11/3", "y = 0 ⇒ x = 11", None,
         "2) m_r = 3. Perpendicolari ⇒ m_s = m_r = 3", "-k/(k + 1) = 3 ⇒ -k = 3k + 3 ⇒ k = -3/4", None,
         ("3) * vedi ultima pagina", {})],
        ["* M = (2; 2)    m_PQ = (0 - 4)/(5 + 1) = -2/3", "m_asse = 3/2    y - 2 = 3/2 (x - 2)", "3x - 2y - 2 = 0", "X = M(2; 2) è sull'asse ed è equidistante da P e Q."],
    ],
    pct=pct(100, 100, 0, 100, 0, N, N, 100, 100, 0, 70, 100, 100, 100, N, N, N, 70),
    schede={
        "1": (["retta AB e parallela per $C$ corrette", "intersezione con l'asse $x$: $(11,0)$"],
              ["$|AB|=\\sqrt{6^2+2^2}$: i quadrati vanno sui due scarti, non sulla somma", "forma della retta: da $y=\\frac x3+\\frac53$ si ha $b=-1$, non $+1$", "area e secondo metodo non svolti"]),
        "2": (["risoluzione dell'equazione coerente con la condizione scelta"], ["rette perpendicolari: $m_s=-\\frac1{m_r}$, non $m_s=m_r$", "caso $k=-1$ non discusso"]),
        "3": (["asse corretto (continua a pagina 2)", "punto scelto sull'asse, ma $M$ non dimostra molto"], []),
        "4": ([], ["esercizio non svolto"]),
    },
    aree=["Rivedi la condizione di parallelismo e di perpendicolarità.", "Ripassa la formula della distanza fra due punti.", "Gestisci il tempo: non lasciare esercizi in bianco."],
    nota="Cancellatura al punto 1c non valutata. Asterisco del punto 3 seguito a pagina 2.",
)

ELAB["A"]["Finto Davide"] = dict(
    formato="jpg", effetto="foto",
    pagine=[["1a) m = 3 - 1/4 + 2 = 2 3/4", "y = 3x + 1", "AB = 3 + 4 + 1 + 2 = 10", None,
             "scusi prof non ho studiato"]],
    pct=pct(0, 0, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, 0),
    schede={
        "1": ([], ["$m=\\dfrac{y_B-y_A}{x_B-x_A}=\\dfrac{3-1}{4+2}$: i parametri vanno racchiusi fra parentesi", "$y=mx+q$ con $q$ da ricavare dal punto $A$", "$|AB|=\\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}$"]),
        "2": ([], ["esercizio non svolto"]), "3": ([], ["esercizio non svolto"]), "4": ([], ["esercizio non svolto"]),
    },
    aree=["Ripassa il coefficiente angolare e l'equazione della retta per due punti.", "Rivedi con calma la distanza fra due punti.", "Prenota un colloquio per il recupero."],
)

ELAB["A"]["Demo Elena"] = dict(
    formato="jpg_multi", effetto="foto",
    pagine=[
        ["1a) m = (3 - 1)/(4 + 2) = 1/3", "y - 1 = 1/3 (x + 2)  ⇒  x - 3y + 5 = 0", "|AB| = √40 = 6,32", None,
         "1b) h = |2 + 9 + 5|/√10 = 16/√10", "A = 1/2 · AB · h = 1/2 · 2√10 · 16/√10 = 16", None,
         "secondo metodo:", "A = 1/2 |-2(6) + 4(-4) + 2(2)| = 1/2 |-12 - 16 + 4|", "= 12      (non coincide, non so perché)", None,
         "1c) m = 1/3   y + 3 = 1/3 (x - 2)", "x - 3y - 11 = 0   y = 0 ⇒ x = 11"],
        ["2) m_s = -k/(k + 1)   m_r = 3", "-k/(k + 1) = -1/3 ⇒ 3k = k + 1 ⇒ k = 1/2", "k = -1: s verticale, non perpendicolare a r", None,
         "3) M = ((-1 + 5)/2 ; (4 + 0)/2) = (2; 4)", "m_PQ = -2/3 ⇒ m = 3/2", "y - 4 = 3/2 (x - 2)  ⇒  3x - 2y + 2 = 0", "scelgo X(0; 1): sta sull'asse. Equidistante: ok.", None,
         "4) k r1 + r2 = 0   centro: (-1; 1)", "per (3; 0): 7k - 6 = 0 ⇒ k = 6/7 ⇒ x + 4y - 3 = 0", "parallela a x: k = 1/2 ⇒ y = 1", "r1 non si ottiene perché servirebbe k → ∞"],
    ],
    pct=pct(100, 100, 80, 100, 100, 100, 40, 100, 100, 100, 100, 100, 70, 0, 100, 100, 70, 80),
    schede={
        "1": (["retta AB, distanza e area", "parallela per $C$ e intersezione $(11,0)$"],
              ["$|AB|$: lascia $\\sqrt{40}$ approssimato a $6{,}32$; scrivi anche $2\\sqrt{10}$", "secondo metodo: $-2\\cdot6+4\\cdot(-4)+2\\cdot(-2)=-32$, non $-24$; i due risultati devono coincidere"]),
        "2": (["$k=\\frac12$ e discussione del caso verticale"], []),
        "3": (["punto medio e pendenza dell'asse impostati bene"], ["$\\frac{4+0}{2}=2$, non $4$: l'asse è $3x-2y-2=0$", "equidistanza non verificata con il calcolo ($|XP|=|XQ|$)"]),
        "4": (["centro, retta per $(3,0)$ e retta $y=1$"], ["motivazione sintetica: spiega perché $r_2$ non è proporzionale a $r_1$"]),
    },
    aree=["Calcola i punti medi con attenzione, scrivendo i passaggi.", "Quando due metodi non coincidono, cerca l'errore prima di consegnare.", "Mostra sempre i calcoli di una verifica."],
)

# ---------------------------------------------------------------- Fila B
ELAB["B"]["Campione Franco"] = dict(
    formato="pdf", effetto="scanner",
    pagine=[
        ["1a) m = (2 + 2)/(5 + 1) = 4/6 = 2/3", "y + 2 = 2/3 (x + 1)  ⇒  2x - 3y - 4 = 0", "|AB| = √(36 + 16) = √52 = 2√13", None,
         "1b) h = |2·3 - 3(-4) - 4|/√13 = 14/√13", "Area = 1/2 · 2√13 · 14/√13 = 14", "con i vertici: 1/2 |-1(2+4) + 5(-4+2) + 3(-2-2)|", "= 1/2 |-6 - 10 - 12| = 14", None,
         "1c) y + 4 = 2/3 (x - 3)  ⇒  2x - 3y - 18 = 0", "y = 0 ⇒ x = 9     P(9; 0)", None,
         "2) m_r = -2 ⇒ m_s = 1/2    -k/(k - 1) = 1/2", "-2k = k - 1 ⇒ k = 1/3.  Se k = 1: s è x = -4,", "verticale: non perpendicolare a r."],
        ["3) M = (3; 2)   m_PQ = (-1 - 5)/(6 - 0) = -1", "asse: m = 1   y - 2 = x - 3  ⇒  x - y - 1 = 0", "X(1; 0): XP² = 1 + 25, XQ² = 25 + 1 ⇒ uguali", None,
         "4) k r1 + r2 = 0: 2x - y - 5 = 0 e x + 3y + 1 = 0", "centro: y = 2x - 5 ⇒ 7x - 14 = 0 ⇒ C(2; -1)", "per (0; 4): -9k + 13 = 0 ⇒ k = 13/9", "parallela a x: 2k + 1 = 0 ⇒ k = -1/2 ⇒ y = -1"],
    ],
    pct=pct(100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, N, 90),
    schede={
        "1": (["retta AB, lunghezza e altezza", "area verificata con i vertici", "parallela per $C$ e intersezione $(9,0)$"], []),
        "2": (["$k=\\frac13$ e caso verticale"], []), "3": (["asse e verifica dell'equidistanza"], []),
        "4": (["centro $(2,-1)$, retta per $(0,4)$ e $y=-1$"], ["manca la motivazione sulla prima generatrice"]),
    },
    aree=["Aggiungi sempre le motivazioni richieste, anche brevi."],
)

ELAB["B"]["Saggio Gina"] = dict(
    formato="pdf", effetto="foto",
    pagine=[
        ["1a) m = (2 + 2)/(5 + 1) = 2/3", "y + 2 = 2/3 (x + 1)  ⇒  y = 2x/3 - 4/3", "AB = √(6² + 4²) = √52 = 2√13", None,
         "1b) h = |3 + 12 - 4|/√13 = 11/√13", "A = 1/2 · 2√13 · 11/√13 = 11", None,
         "1c) m = 2/3  y + 4 = 2/3 (x - 3)", "y = 2x/3 - 6   y = 0 ⇒ x = 9", None,
         "2) m_r = -2   m_s = -1/2", "-k/(k - 1) = -1/2 ⇒ 2k = k - 1 ⇒ k = -1"],
        ["3) M = (3; 2)    m_PQ = -1    asse: m = 1", "y - 2 = x - 3  ⇒  y = x - 1", None,
         "4) centro: 2x - y - 5 = 0, x + 3y + 1 = 0", "x = 1 ; y = -3   C(1; -3)", "(altro non fatto)"],
    ],
    pct=pct(100, 100, 100, 100, 30, 100, N, 100, 100, 100, 20, 100, 100, N, 100, 20, N, 50),
    schede={
        "1": (["retta AB, lunghezza e parallela corrette"], ["distanza: il numeratore è $|6+12-4|=14$, non $11$ ($-3\\cdot(-4)=+12$)", "area coerente con il valore trovato, ma manca il secondo metodo"]),
        "2": (["condizione impostata con $m_s=-\\frac1{m_r}$"], ["$m_s=-\\frac1{-2}=+\\frac12$, non $-\\frac12$", "caso $k=1$ non discusso"]),
        "3": (["punto medio, pendenza ed equazione dell'asse"], ["manca la verifica dell'equidistanza"]),
        "4": (["rette generatrici individuate"], ["sistema: da $y=2x-5$ si ottiene $x=2$, $y=-1$", "retta per $(0,4)$ e parallela all'asse $x$ non svolte"]),
    },
    aree=["Segni e frazioni: ricontrolla le sostituzioni.", "Verifica sempre il risultato con un punto di prova.", "Completa tutti gli esercizi prima di rileggere."],
)
