"""Check di correzione.py: python scripts/test_correzione.py (alunni fittizi, nessun dato reale)"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import correzione as c
from openpyxl import load_workbook

# conversione: esempi del docente, minimo 2, arrotondamento a 25 per eccesso sul mezzo passo
for t, v in [(500, "5"), (525, "5+"), (550, "5½"), (575, "6-"), (600, "6"), (1000, "10"), (975, "10-"),
             (487, "5-"), (488, "5"), (200, "2"), (150, "2"), (0, "2"), (100, "1"), (110, "2"), (120, "2")]:
    assert c.voto(t)[0] == v, (t, v, c.voto(t))
assert c.voto(575)[1] == 5.75
# minimo di partecipazione: non svolta 10% del massimo, tentata 20%, il parziale non scende sotto il 20%
assert (c.punti(50, None), c.punti(50, 0), c.punti(50, 10), c.punti(50, 100)) == (5, 10, 10, 50)

def ev(i, es, mx, liv):
    return {"ID evidenza": f"E{i:02d}", "Esercizio": es, "Punto/gruppo": "intero", "Indicatore": "SVI",
            "Sigla argomento": "a", "Max": mx, "Descrizione evidenza": "d", "Nome completo argomento": "A", "Livello": liv}

reg = [ev(1, 1, 200, "1"), ev(2, 1, 250, "2A"), ev(3, 1, 400, "2"), ev(4, 2, 100, "3"), ev(5, 2, 50, "1")]
corr = {"argomento": "Prova", "alunni": {"Rossi Fittizio": {"E01": 100, "E02": 100, "E03": 50, "E04": 0},
                                         "Verdi Fittizio": {}, "Bianchi Fittizio": {"E01": 0}}}
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "r.json").write_text(json.dumps(reg)); (d / "c.json").write_text(json.dumps(corr))
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("registro_xlsx.py")), "write",
                        str(d / "r.json"), str(d / "reg.xlsx"), "--classe", "medio"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    c.riepilogo(d / "reg.xlsx", d / "c.json", d / "out.xlsx")
    c.correttore_alunni(d / "reg.xlsx", d / "c.json", d / "ca.xlsx")
    w = load_workbook(d / "ca.xlsx").active  # colonne alfabetiche, % assolute con minimi: non svolta 10, tentata 20
    assert [w.cell(1, k).value for k in (16, 17, 18)] == ["Bianchi Fittizio", "Rossi Fittizio", "Verdi Fittizio"]
    assert [w.cell(r, 17).value for r in range(2, 7)] == [100, 100, 50, 20, 10] and w.cell(2, 16).value == 20
    # Rossi: 200+250+200 + E04 0% (20% di 100) + E05 non svolta (10% di 50); Verdi: tutto in bianco = 100 -> 1;
    # Bianchi: un solo tentativo errato e il resto in bianco = 120 -> 2
    atteso = {"Rossi Fittizio": 200 + 250 + 200 + 20 + 5, "Verdi Fittizio": 100, "Bianchi Fittizio": 40 + 25 + 40 + 10 + 5}
    assert [a["voto"][0] for a in c.calcola(d / "reg.xlsx", d / "c.json")[2]] == ["2", "7-", "1"]
    if shutil.which("soffice"):  # ricalcola e confronta le formule con le funzioni Python
        subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", str(d / "ric"), str(d / "out.xlsx")],
                       capture_output=True, check=True)
        ws = load_workbook(d / "ric" / "out.xlsx", data_only=True)["Voti"]
        for riga in (5, 6, 7):
            nome = ws.cell(riga, 1).value
            assert ws.cell(riga, 4).value == atteso[nome], (nome, ws.cell(riga, 4).value)
            assert ws.cell(riga, 5).value == c.voto(atteso[nome])[0], (nome, ws.cell(riga, 5).value)
    if shutil.which("pdflatex") and shutil.which("pdfinfo"):  # fascicolo: schede fittizie da 1 pagina
        import fascicolo as f
        (d / "ris").mkdir()
        for a in atteso:
            (d / "s.tex").write_text(r"\documentclass{article}\begin{document}" + a + r"\end{document}")
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(d), str(d / "s.tex")], capture_output=True, check=True)
            shutil.copy(d / "s.pdf", d / "ris" / f"Prova_{a}.pdf")
        corr["argomento"], corr["classe"], corr["data"] = "Prova", "3X", "01/01/2026"
        (d / "c.json").write_text(json.dumps(corr))
        f.fascicolo(d / "reg.xlsx", d / "c.json", d / "ris")
        for nome, n in (("copertina", 1), ("Schede_complete", 4), ("Schede_complete_fronteretro", 8)):
            assert f.pagine(d / "ris" / f"{nome}.pdf") == n, nome
print("ok")
