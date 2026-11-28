"""Check end-to-end di quiz.py: python scripts/test_quiz.py (richiede pdflatex per la parte PDF)."""
import json, re, subprocess, sys, tempfile, urllib.error, urllib.request
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
    assert rows["a"][8] == "sì" and rows["a"][9] is not None  # voto sempre presente anche senza indicatori
    assert rows["a"][12:14] == (1000, "10"), rows["a"]
    # da scansioni: colonna Nome facoltativa, colonne lette per intestazione
    wb = load_workbook(d / "o/risposte_studenti.xlsx"); ws = wb.active
    ws.delete_rows(2, ws.max_row)
    ws.insert_cols(2); ws["B1"] = "Nome"
    ws.append(["a", "Rossi Mario", k[0]["codice"], *(q["corretta"] for q in k[0]["domande"])])
    wb.save(d / "o/scan.xlsx")
    run("correggi", "--out", str(d / "o"), "--risposte", str(d / "o/scan.xlsx"))
    r = list(load_workbook(d / "o/quiz_risultati.xlsx")["Studenti"].iter_rows(min_row=2, values_only=True))[0]
    assert r[:3] == ("a", "Rossi Mario", k[0]["codice"]) and r[6] == 14, r
    # foglio risposte: PDF reale con segni sintetici, scansione storta; pagine pari per il fronte-retro
    import cv2, omr
    for v in k:
        pg = omr.pagine(d / f"o/quiz_{v['codice']}.pdf")
        assert len(pg) % 2 == 0, f"pagine dispari: {len(pg)}"
    g, B, mm = pg[-1], k[2]["foglio"]["bolle"], 200 / 25.4
    k2 = k[2]
    for n, j in ((0, 1), (1, 0), (1, 2), (2, 2)):  # 1: B ok; 2: due cerchi = annullata; 3: C ok
        cv2.circle(g, (int(B[n][j][0] * mm), int(B[n][j][1] * mm)), int(omr.R * mm), 0, -1)
    cv2.circle(g, (int(B[2][0][0] * mm), int(B[2][0][1] * mm)), int(omr.R * mm * .35), 0, -1)  # + traccia: correzione
    g = cv2.warpAffine(g, cv2.getRotationMatrix2D((g.shape[1] / 2, g.shape[0] / 2), 1.5, .97), g.shape[::-1], borderValue=255)
    (d / "o/scan").mkdir(); cv2.imwrite(str(d / "o/scan/Verdi_Anna.png"), cv2.rotate(g, cv2.ROTATE_180))
    run("leggi", str(d / "o/scan"), "--out", str(d / "o"))
    xl = lambda: list(load_workbook(d / "o/risposte_scansioni.xlsx").active.iter_rows(min_row=2, values_only=True))[0]
    anomalie = lambda: {x[2]: x[3] for x in load_workbook(d / "o/risposte_scansioni.xlsx")["Anomalie"].iter_rows(min_row=2, values_only=True)}
    r = xl()
    assert r[:3] == ("S01", "Verdi Anna", k2["codice"]) and r[3:6] == ("B", "*", "C"), r  # B ok; due cerchi = annullata; C con traccia = proposta
    assert anomalie() == {2: "annullata", 3: "proposta"}, anomalie()
    # editor: server locale, solo con il token; modifiche validate; xlsx riscritto
    srv = subprocess.Popen([sys.executable, str(Q), "rivedi", "--out", str(d / "o"), "--no-browser"], stdout=subprocess.PIPE, text=True)
    try:
        url = re.search(r"http://\S+/", srv.stdout.readline())[0]
        web = urllib.request.build_opener(urllib.request.ProxyHandler({})).open
        token = re.search(r'name="token" content="([^"]+)"', web(url).read().decode())[1]
        assert json.loads(web(url + "letture.json").read())["fogli"][0]["id"] == "S01" and web(url + "img/S01.png").status == 200
        for tok, risp, code in (("x", "C", 403), (token, "Z", 400), (token, "A", 204)):
            req = urllib.request.Request(url + "salva", json.dumps({"fogli": [{"id": "S01", "nome": "Verdi Anna", "domande": [{"n": 3, "risposta": risp, "rivista": True}]}]}).encode(), {"X-Token": tok})
            try:
                c = web(req).status
            except urllib.error.HTTPError as e:
                c = e.code
            assert c == code, (tok, risp, c)
    finally:
        srv.terminate()
    assert xl()[3:6] == ("B", "*", "A") and anomalie() == {2: "annullata"}, (xl(), anomalie())
    # classificazione dei riempimenti: gomma + nuova risposta e segno debole sono proposte, non risposte perse
    for fill, atteso in (([0, 0, 0], ("vuota", None)), ([.9, 0, 0], ("ok", 0)), ([.9, .25, 0], ("proposta", 0)), ([0, .3, 0], ("proposta", 1)),
                         ([.9, .8, 0], ("annullata", None)), ([.3, .2, 0], ("annullata", None)), ([.6, .3, 0], ("annullata", None))):
        assert omr.classifica(fill)[:2] == atteso, (fill, omr.classifica(fill))

# '*', --annullata, --minimo (anche con gli indicatori) e alternative fisse
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    wb = Workbook(); wb.remove(wb.active)
    for i in range(3):
        ws = wb.create_sheet(f"q{i}")
        ws.append(["Testo della domanda", "Risposta corretta", "Alternativa 1", "Alternativa 2", "Alternativa 3", "Alternative fisse", "Indicatore"])
        ws.append([f"Q{i}", "1", "1", "2", "Nessuna delle precedenti", 1 if i == 0 else None, "ANA" if i else "SVI"])
    wb.save(d / "d.xlsx")
    run("genera", str(d / "d.xlsx"), "--varianti", "6", "--errata", "-1", "--annullata", "0", "--minimo", "0", "--out", str(d / "o"), "--no-pdf")
    k = json.loads((d / "o/quiz_chiavi.json").read_text())["varianti"]
    assert all(v["domande"][[q["foglio"] for q in v["domande"]].index("q0")]["alternative"][-1] == "Nessuna delle precedenti" for v in k), "alternativa fissa spostata"
    assert len({tuple(q["alternative"]) for v in k for q in v["domande"] if q["foglio"] == "q1"}) > 1, "le altre non si mescolano"
    wb = load_workbook(d / "o/risposte_studenti.xlsx"); ws = wb.active
    ws.append(["z", k[0]["codice"], *("Z" for _ in k[0]["domande"])])   # tutte errate: -3, minimo 0
    ws.append(["s", k[0]["codice"], *("*" for _ in k[0]["domande"])])   # tutte annullate: 0 punti
    ws.append(["b", k[0]["codice"]])                                     # tutte non date: 3
    wb.save(d / "o/risposte_studenti.xlsx")
    run("correggi", "--out", str(d / "o"))
    rows = {r[0]: r for r in load_workbook(d / "o/quiz_risultati.xlsx")["Studenti"].iter_rows(min_row=2, values_only=True)}
    assert rows["z"][5] == 0 and rows["s"][5] == 0 and rows["b"][5] == 3 and rows["s"][3] == 3, rows  # '*' conta non data, ma punti 0
    assert rows["z"][14] == 0 and rows["z"][15] == "2", rows["z"]                                   # indicatori scalati: totale 0
    wb = load_workbook(d / "d.xlsx"); wb["q0"]["B2"] = "9"; wb.save(d / "x.xlsx")
    r = subprocess.run([sys.executable, str(Q), "genera", str(d / "x.xlsx"), "--out", str(d / "x"), "--no-pdf"], capture_output=True, text=True)
    assert r.returncode and "Alternative fisse" in r.stderr, r  # corretta fuori dalle colonne con ordine fisso

# indicatori per riga: quote uguali in ogni variante, voto da indicatori = voto da punti
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    wb = Workbook(); wb.remove(wb.active)
    for i, inds in enumerate([("ANA", "SVI"), ("SVI", "ANA"), ("ANA", "ANA"), ("SVI", "SVI")]):
        ws = wb.create_sheet(f"q{i}")
        ws.append(["Testo della domanda", "Risposta corretta", "Alternativa 1", "Alternativa 2", "Indicatore"])
        for k, ind in enumerate(inds):
            ws.append([f"Q{i}.{k}", "1", "2", "3", ind])
    wb.save(d / "d.xlsx")
    run("genera", str(d / "d.xlsx"), "--varianti", "4", "--pesi", "ANA=500,SVI=500", "--out", str(d / "o"), "--no-pdf")
    ch = json.loads((d / "o/quiz_chiavi.json").read_text())
    assert ch["pesi"] == {"ANA": 500, "SVI": 500}, ch["pesi"]
    k = ch["varianti"]
    wb = load_workbook(d / "o/risposte_studenti.xlsx"); ws = wb.active
    ws.append(["a", k[0]["codice"], *(q["corretta"] for q in k[0]["domande"])])
    for n, v in enumerate(k[1:], 1):  # parziali diverse: il voto deve coincidere comunque
        ws.append([f"p{n}", v["codice"], *(q["corretta"] if (q["n"] + n) % 2 else "Z" for q in v["domande"])])
    ws.append(["b", k[0]["codice"]])
    wb.save(d / "o/risposte_studenti.xlsx")
    run("correggi", "--out", str(d / "o"))
    rows = {r[0]: r for r in load_workbook(d / "o/quiz_risultati.xlsx")["Studenti"].iter_rows(min_row=2, values_only=True)}
    assert rows["a"][12:15] == (500, 500, 1000) and rows["a"][15] == "10", rows["a"]
    assert rows["b"][12:15] == (125, 125, 250) and rows["b"][15] == "2½", rows["b"]
    for r in rows.values():  # voto dagli indicatori = voto dai punti (percentuale), sempre
        assert abs(r[14] - r[7] * 10) < 0.01, r
    wb = load_workbook(d / "d.xlsx"); wb["q1"]["E3"] = None; wb.save(d / "m.xlsx")
    r = subprocess.run([sys.executable, str(Q), "genera", str(d / "m.xlsx"), "--out", str(d / "m"), "--no-pdf"], capture_output=True, text=True)
    assert r.returncode and "Indicatore" in r.stderr, r
    r = subprocess.run([sys.executable, str(Q), "genera", str(d / "d.xlsx"), "--pesi", "ANA=600,SVI=400", "--out", str(d / "x"), "--no-pdf"], capture_output=True, text=True)
    assert r.returncode and "identiche" in r.stderr, r  # 4 quesiti non possono dare 60/40
print("ok")
