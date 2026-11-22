"""Check end-to-end di quiz.py: python scripts/test_quiz.py (richiede pdflatex per la parte PDF)."""
import json, subprocess, sys, tempfile
from pathlib import Path
from openpyxl import Workbook, load_workbook

Q = Path(__file__).with_name("quiz.py")
run = lambda *a: subprocess.run([sys.executable, str(Q), *a], check=True, capture_output=True, text=True)

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    wb = Workbook(); wb.remove(wb.active)
    for i in range(3):
        ws = wb.create_sheet(f"q{i}")
        ws.append(["Testo della domanda", "Risposta corretta", "Alternativa 1", "Alternativa 2", "Alternativa 3", "Punteggio corretta"])
        ws.append([f"Quanto fa $1+{i}$?", str(1 + i), "7", "8", "9", 6 if i == 2 else None])
    wb.save(d / "d.xlsx")
    run("genera", str(d / "d.xlsx"), "--varianti", "3", "--out", str(d / "o"))
    assert len(list((d / "o").glob("quiz_*.pdf"))) == 3, "PDF mancanti"
    k = json.loads((d / "o/quiz_chiavi.json").read_text())["varianti"]
    wb = load_workbook(d / "o/risposte_studenti.xlsx"); ws = wb.active
    ws.append(["a", k[0]["codice"], *(q["corretta"] for q in k[0]["domande"])])  # tutte giuste: 4+4+6=14
    ws.append(["b", k[1]["codice"]])                                              # tutte non date: 3
    ws.append(["c", k[2]["codice"], *("Z" for _ in k[2]["domande"])])             # tutte errate: 0
    wb.save(d / "o/risposte_studenti.xlsx")
    run("correggi", "--out", str(d / "o"))
    rows = {r[0]: r for r in load_workbook(d / "o/quiz_risultati.xlsx")["Studenti"].iter_rows(min_row=2, values_only=True)}
    assert rows["a"][5] == 14 and rows["b"][5] == 3 and rows["c"][5] == 0, rows
    assert rows["a"][6] == 14 and rows["a"][7] == 100, rows["a"]
    dis = list(load_workbook(d / "o/quiz_risultati.xlsx")["Distrattori"].iter_rows(min_row=2, values_only=True))
    assert sum(r[4] for r in dis) == 9, "ogni risposta (anche non data) conta una volta"
    assert sum(r[4] for r in dis if r[3] == "sì") == 3, "solo lo studente 'a' ha scelto le corrette"
    assert all(r[2] != "Z" for r in dis), "lettere non valide non sono alternative"
print("ok")
