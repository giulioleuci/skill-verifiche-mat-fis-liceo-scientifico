"""Check di cartelle, statistiche, importa, banca e domande_xlsx: python scripts/test_statistiche.py (alunni fittizi)"""
import csv, json, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import banca, cartelle, correzione as c, domande_xlsx, statistiche
from openpyxl import Workbook, load_workbook

S = Path(__file__).parent
def py(*a, ok=True):
    r = subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True)
    assert r.returncode == 0 or not ok, r.stderr[-1500:]
    return r

# statistiche pure
assert statistiche.affidabilita([[1, 0, 1, 0], [1, 0, 1, 0]])[0] == 1.0
assert statistiche.discriminazione([1, 1, 0, 0], [10, 9, 2, 1]) == 1.0 and statistiche.discriminazione([0, 0, 1, 1], [10, 9, 2, 1]) == -1.0
assert "negativa" in statistiche.segnale(0.5, -0.2) and statistiche.segnale(0.5, 0.3) == ""

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    # cartelle: numerazione unica per prove e quiz, mai rinumerata
    a, b = cartelle.nuova(d, "Verifica rette", "prova"), cartelle.nuova(d, "Quiz cinematica", "quiz")
    assert (a.name, b.name) == ("01_VERIFICA_RETTE", "02_QUIZ_CINEMATICA") and (b / "varianti").is_dir()
    (d / "01_VERIFICA_RETTE").rename(d / "01_X"); (d / "05_ALTRA").mkdir()
    assert cartelle.nuova(d, "terza", "importata").name == "06_TERZA" and len(cartelle.elenco(d)) == 4
    assert "tipo" in py(S / "progetto.py", "stato", b / "progetto.json").stdout

    # prova scritta importata dal correttore Excel con una colonna per alunno (anche con colonna vuota e senza nomi)
    ev = lambda i, mx, liv, ind: {"ID evidenza": f"E{i:02d}", "Esercizio": 1 if i < 4 else 2, "Punto/gruppo": "x", "Indicatore": ind, "Sigla argomento": "a",
                                  "Max": mx, "Descrizione evidenza": "d", "Nome completo argomento": "A", "Livello": liv}
    (d / "r.json").write_text(json.dumps([ev(1, 200, "1", "ANA"), ev(2, 250, "2A", "SVI"), ev(3, 400, "2", "SVI"), ev(4, 100, "3", "ARG"), ev(5, 50, "1", "ANA")]))
    (d / "c.json").write_text(json.dumps({"argomento": "P", "alunni": {"Rossi Fittizio": {"E01": 100, "E02": 100, "E03": 100, "E04": 100, "E05": 100},
                                                                       "Verdi Fittizio": {"E01": 100, "E02": 0}, "Bianchi Fittizio": {}}}))
    py(S / "registro_xlsx.py", "write", d / "r.json", d / "reg.xlsx", "--classe", "medio")
    c.correttore_alunni(d / "reg.xlsx", d / "c.json", d / "ca.xlsx")
    w = load_workbook(d / "ca.xlsx"); w.active.insert_cols(load_workbook(d / "reg.xlsx").active.max_column + 1); w.save(d / "ca.xlsx")  # colonna vuota prima degli alunni
    r = py(S / "importa.py", "prova", d / "reg.xlsx", d / "ca.xlsx", "--out", d / "ris")
    assert "sembrano nomi" in r.stderr and "Rossi" not in r.stdout + r.stderr
    classe = {x["Misura"]: x["Valore"] for x in statistiche.leggi_csv(d / "ris/statistiche_classe.csv")}
    assert classe["Studenti"] == "3" and "meno di 20" in classe["Avviso"]
    assert "Rossi" not in "".join(p.read_text() for p in (d / "ris").glob("*")), "nessun nome nei risultati"
    assert {x["Indicatore"] for x in statistiche.leggi_csv(d / "ris/statistiche_indicatori.csv")} == {"ANA", "SVI", "ARG"}
    # chiudi, report, storico
    (d / "06_TERZA/risultati").rmdir(); (d / "ris").rename(d / "06_TERZA/risultati")
    py(S / "statistiche.py", "chiudi", d / "06_TERZA"); py(S / "statistiche.py", "report", d / "06_TERZA")
    assert (d / "storico.csv").exists() and (d / "storico.xlsx").exists() and (d / "06_TERZA/risultati/report_classe.md").exists()
    assert json.loads((d / "06_TERZA/progetto.json").read_text())["fase"] == "chiusa"

    # domande: write + check, poi quiz generato e importato (con chiavi e lettere; senza chiavi 1/0), banca
    dom = [{"argomento": "Rette", "indicatore": "ANA", "versioni": [{"testo": f"Quanto fa $1+{i}$?", "corretta": str(1 + i), "errate": ["7", "8", "9"]}]} for i in range(3)]
    (d / "d.json").write_text(json.dumps(dom))
    assert py(S / "domande_xlsx.py", "write", d / "d.json", d / "domande.xlsx").returncode == 0
    dom[0]["versioni"][0]["errate"] = ["7", "7", "9"]; (d / "d.json").write_text(json.dumps(dom))
    assert py(S / "domande_xlsx.py", "write", d / "d.json", d / "dup.xlsx", ok=False).returncode == 1  # alternativa ripetuta
    q = d / "02_QUIZ_CINEMATICA"; (d / "domande.xlsx").rename(q / "domande.xlsx")
    py(S / "quiz.py", "genera", q / "domande.xlsx", "--varianti", "2", "--no-pdf", "--out", q / "varianti")
    k = json.loads((q / "varianti/quiz_chiavi.json").read_text())["varianti"]
    wb = Workbook(); ws = wb.active
    ws.append(["Domanda", "x", "y", "z"]); ws.append(["Variante", k[0]["codice"], k[0]["codice"], k[1]["codice"]])
    for n in range(3):
        ws.append([n + 1, k[0]["domande"][n]["corretta"], "Z", None])
    wb.save(q / "p.xlsx")
    py(S / "importa.py", "quiz", q / "p.xlsx", "--chiavi", q / "varianti/quiz_chiavi.json", "--out", q / "risultati")
    dist = statistiche.leggi_csv(q / "risultati/statistiche_domande.csv")
    assert len(dist) == 3 and (q / "risultati/statistiche_distrattori.csv").exists()
    py(S / "banca.py", "aggiungi", q, "--radice", d)
    b = load_workbook(d / "_banca/banca.xlsx").active
    assert b.max_row == 4 and b["G2"].value is not None and b["I2"].value == q.name
    py(S / "banca.py", "componi", "--out", d / "nuovo.xlsx", "--n", "2", "--indicatore", "ANA", "--radice", d)
    assert len(load_workbook(d / "nuovo.xlsx").sheetnames) == 2
    # quiz senza chiavi: 1/0
    wb = Workbook(); ws = wb.active
    ws.append(["Domanda", "x", "y"]); [ws.append([n, 1, 0]) for n in (1, 2)]
    wb.save(d / "u.xlsx")
    py(S / "importa.py", "quiz", d / "u.xlsx", "--out", d / "ris2")
    assert not (d / "ris2/statistiche_distrattori.csv").exists()
print("ok")
