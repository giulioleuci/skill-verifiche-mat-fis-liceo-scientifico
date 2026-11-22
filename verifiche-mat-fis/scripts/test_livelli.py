"""Check di registro_xlsx.py sui livelli: python scripts/test_livelli.py"""
import json, subprocess, sys, tempfile
from pathlib import Path

R = Path(__file__).with_name("registro_xlsx.py")
run = lambda *a: subprocess.run([sys.executable, str(R), *a], capture_output=True, text=True)

def ev(i, es, mx, liv):
    return {"ID evidenza": f"E{i:02d}", "Esercizio": es, "Punto/gruppo": "intero", "Indicatore": "SVI",
            "Sigla argomento": "a", "Max": mx, "Descrizione evidenza": "d", "Nome completo argomento": "A", "Livello": liv}

# classe medio: L1 200, L2 650 (di cui 2A 250 = 38%), L3 150
base = [ev(1, 1, 200, "1"), ev(2, 1, 250, "2A"), ev(3, 1, 400, "2"), ev(4, 2, 150, "3")]
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    def prova(nome, rows, classe="medio"):
        (d / f"{nome}.json").write_text(json.dumps(rows))
        return run("write", str(d / f"{nome}.json"), str(d / f"{nome}.xlsx"), "--classe", classe)
    # esercizio 2 solo L3: manca 1/2A
    assert "esercizio 2" in prova("e", base).stderr
    ok = base[:3] + [ev(4, 2, 100, "3"), ev(5, 2, 50, "1")]
    r = prova("ok", ok); assert r.returncode == 0, r.stderr
    c = run("check", str(d / "ok.xlsx"), "--classe", "medio"); assert c.returncode == 0 and "L1=25%" in c.stdout, c
    # L1 oltre 25%
    assert "L1 deve valere" in prova("l1", [ev(1, 1, 300, "1"), ev(2, 1, 250, "2A"), ev(3, 2, 350, "2"), ev(4, 2, 100, "3")]).stderr
    # accessi < 30% di L2: 100 su 650
    assert "accesso" in prova("acc", [ev(1, 1, 200, "1"), ev(2, 1, 100, "2A"), ev(3, 1, 550, "2"), ev(4, 2, 150, "3")]).stderr
print("ok")
