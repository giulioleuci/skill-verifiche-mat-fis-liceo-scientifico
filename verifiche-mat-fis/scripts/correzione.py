"""Riepilogo di correzione: punti per evidenza, voto in decimi, Excel per la classe.

python scripts/correzione.py registro_evidenze.xlsx correzioni.json riepilogo_voti.xlsx [correttore_alunni.xlsx]

correzioni.json: {"argomento": "Onde", "alunni": {"Cognome Nome": {"E01": 100, "E02": 40, "E03": 0, "E04": null}}}
Scrive anche statistiche_*.csv e statistiche.md (anonime) accanto al riepilogo. "classe" e "data" servono solo a fascicolo.py. Percentuale per evidenza 0-100. 0 = tentata e sbagliata (conta come
SBAGLIATA % del massimo); null o assente = non svolta (conta come NON_SVOLTA % del massimo).
"""
import json
import math
import sys
from copy import copy
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L

import registro_xlsx

NON_SVOLTA, SBAGLIATA = 10, 20  # % del massimo di ogni evidenza: non svolta, tentata (anche tutta sbagliata)
PASSO, VOTO_MIN = 25, 200       # arrotondamento del totale e voto minimo (2), in punti su 1000
BIANCO = 100                    # compito tutto non svolto = 10% di 1000 = voto 1; con un solo tentativo il totale supera 100


def punti(mx, pct):
    """Punti dell'evidenza: percentuale del massimo, con minimo di partecipazione."""
    return mx * (NON_SVOLTA if pct is None else max(pct, SBAGLIATA)) / 100


def voto(totale):
    """(etichetta, decimale) dal totale su 1000: 500=5, 525=5+, 550=5½, 575=6-."""
    r = BIANCO if round(totale, 6) == BIANCO else max(VOTO_MIN, math.floor(totale / PASSO + 0.5) * PASSO)
    v, resto = divmod(r, 100)
    return {0: f"{v}", 25: f"{v}+", 50: f"{v}½", 75: f"{v + 1}-"}[resto], r / 100


def _formula_punti(mx, pct):  # specchio di punti() per il foglio Excel
    return f'=IF({pct}="",{mx}*{NON_SVOLTA}/100,{mx}*MAX({pct},{SBAGLIATA})/100)'


def _formula_voto(dec):  # specchio di voto(): etichetta dal decimale
    q = f"ROUND(MOD({dec},1)*4,0)"
    return f'=IF({q}=3,INT({dec})+1&"-",INT({dec})&CHOOSE({q}+1,"","+","½"))'


def carica(registro, correzioni):
    rows = registro_xlsx.read(registro)
    es = sorted({str(r["Esercizio"]) for r in rows}, key=lambda e: (e == "Intero elaborato", e))
    return rows, es, json.loads(Path(correzioni).read_text(encoding="utf-8"))


def calcola(registro, correzioni):
    """(dati, esercizi, [{nome, per_es, totale, voto: (etichetta, decimale)}]) in ordine alfabetico."""
    rows, es, dati = carica(registro, correzioni)
    out = []
    for nome in sorted(dati["alunni"]):
        per = dict.fromkeys(es, 0)
        for r in rows:
            per[str(r["Esercizio"])] += punti(r["Max"], dati["alunni"][nome].get(r["ID evidenza"]))
        tot = sum(per.values())
        out.append({"nome": nome, "per_es": per, "totale": tot, "voto": voto(tot)})
    return dati, es, out


def riepilogo(registro, correzioni, dst):
    rows, es, dati = carica(registro, correzioni)
    ids = [r["ID evidenza"] for r in rows]
    alunni = sorted(dati["alunni"])
    n, ne = len(ids), len(es)
    ultimo = L(n + 1)

    wb = Workbook()
    ws_v, ws_d, ws_p = wb.active, wb.create_sheet("Dettaglio"), wb.create_sheet("Punti")
    ws_v.title = "Voti"
    head = PatternFill("solid", fgColor="1F4E79")
    giallo = PatternFill("solid", fgColor="FFF2CC")

    # Dettaglio (solo docente): % per evidenza, vuoto = non svolta. Punti: formule dei punti.
    for ws, titolo in ((ws_d, "Alunno"), (ws_p, "Alunno")):
        ws.append([titolo] + ids)
        ws.append(["Max"] + [r["Max"] for r in rows])
        ws.append(["Esercizio"] + [str(r["Esercizio"]) for r in rows])
    for i, a in enumerate(alunni):
        ws_d.append([a] + [dati["alunni"][a].get(e) for e in ids])
        riga = 4 + i
        ws_p.append([f"=Dettaglio!A{riga}"] + [
            _formula_punti(f"{L(c)}$2", f"Dettaglio!{L(c)}{riga}") for c in range(2, n + 2)])
    for ws in (ws_d, ws_p):
        for c in ws[1]:
            c.font, c.fill = Font(bold=True, color="FFFFFF"), head
        ws.freeze_panes = "B4"

    # Voti (da mostrare alla classe)
    arg = dati.get("argomento", "")
    ws_v.append([f"Verifica {arg}".strip()])
    ws_v["A1"].font = Font(bold=True, size=14)
    ws_v.append([f"Punteggio su 1000; voto = punti/100 arrotondato a 0,25 (5+ = 5,25 · 5½ = 5,5 · 6- = 5,75), minimo 2 (compito tutto in bianco: 1). "
                 f"Clic sul nome per aprire la scheda."])
    ws_v["A2"].font = Font(italic=True)
    ws_v.append([])
    ws_v.append(["Alunno"] + [f"Esercizio {e}" for e in es] + ["Punti", "Voto", "Voto (decimale)"])
    for c in ws_v[4]:
        c.font, c.fill = Font(bold=True, color="FFFFFF"), head
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    col_tot, col_voto, col_dec = ne + 2, ne + 3, ne + 4
    for i, a in enumerate(alunni):
        riga, rp = 5 + i, 4 + i
        ws_v.cell(riga, 1, a)
        ws_v.cell(riga, 1).hyperlink = f"{arg}_{a}.pdf"
        ws_v.cell(riga, 1).font = Font(color="0563C1", underline="single")
        for j, e in enumerate(es):
            ws_v.cell(riga, 2 + j, f'=SUMIF(Punti!$B$3:${ultimo}$3,"{e}",Punti!$B{rp}:${ultimo}{rp})')
        ws_v.cell(riga, col_tot, f"=SUM({L(2)}{riga}:{L(col_tot - 1)}{riga})")
        ws_v.cell(riga, col_dec, f"=IF(ROUND({L(col_tot)}{riga},6)={BIANCO},{BIANCO / 100:g},"
                f"MAX({VOTO_MIN},FLOOR({L(col_tot)}{riga}/{PASSO}+0.5,1)*{PASSO})/100)")
        ws_v.cell(riga, col_voto, _formula_voto(f"{L(col_dec)}{riga}"))
        ws_v.cell(riga, col_voto).fill = giallo
        ws_v.cell(riga, col_voto).font = Font(bold=True)
        ws_v.cell(riga, col_dec).number_format = "0.00"
        for c in range(2, col_dec + 1):
            ws_v.cell(riga, c).alignment = Alignment(horizontal="center")
    a0, a1 = 5, 4 + len(alunni)
    ws_v.cell(a1 + 2, 1, "Media della classe").font = Font(bold=True)
    ws_v.cell(a1 + 3, 1, "Sufficienti (voto ≥ 6)").font = Font(bold=True)
    for c in list(range(2, col_tot + 1)) + [col_dec]:
        ws_v.cell(a1 + 2, c, f"=AVERAGE({L(c)}{a0}:{L(c)}{a1})").number_format = "0.0" if c != col_dec else "0.00"
        ws_v.cell(a1 + 2, c).alignment = Alignment(horizontal="center")
    ws_v.cell(a1 + 3, col_dec, f'=COUNTIF({L(col_dec)}{a0}:{L(col_dec)}{a1},">=6")')
    ws_v.cell(a1 + 3, col_dec).alignment = Alignment(horizontal="center")
    ws_v.column_dimensions["A"].width = 26
    for c in range(2, col_dec + 1):
        ws_v.column_dimensions[L(c)].width = 14
    ws_v.sheet_view.showGridLines = False
    ws_v.page_setup.orientation = "landscape"
    ws_v.page_setup.fitToWidth, ws_v.page_setup.fitToHeight = 1, 0
    ws_v.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(dst)


def correttore_alunni(registro, correzioni, dst):
    """Copia del registro con una colonna per alunno (ordine alfabetico): % 0-100 per evidenza con i minimi della skill (non svolta 10, tentata 20)."""
    dati = json.loads(Path(correzioni).read_text(encoding="utf-8"))
    wb = load_workbook(registro)
    ws = wb.active
    ultima = ws.max_column
    base = ws.cell(1, ultima)
    for k, a in enumerate(sorted(dati["alunni"]), ultima + 1):
        ws.column_dimensions[L(k)].width = 14
        for r in range(1, ws.max_row + 1):
            c = ws.cell(r, k)
            c._style = copy(ws.cell(r, ultima)._style)
            c.number_format = "0"
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            if r == 1:
                c.value = a
            elif (ev := ws.cell(r, 1).value) is not None:
                c.value = punti(100, dati["alunni"][a].get(str(ev)))
    wb.save(dst)


def statistiche_prova(registro, correzioni, dest):
    """statistiche_*.csv e statistiche.md in dest (per evidenza, indicatore, livello, argomento, classe)."""
    import statistiche
    rows, _, dati = carica(registro, correzioni)
    punti_alunni = {a: {r["ID evidenza"]: punti(r["Max"], dati["alunni"][a].get(r["ID evidenza"])) for r in rows} for a in dati["alunni"]}
    tabelle, _, _ = statistiche.prova(rows, {f"A{k:02d}": p for k, p in enumerate(punti_alunni.values(), 1)})  # nomi mai nelle statistiche
    statistiche.scrivi(dest, tabelle, f"Statistiche della verifica {dati.get('argomento', '')}".strip())


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    riepilogo(*sys.argv[1:4])
    statistiche_prova(sys.argv[1], sys.argv[2], Path(sys.argv[3]).parent)
    if len(sys.argv) == 5:
        correttore_alunni(sys.argv[1], sys.argv[2], sys.argv[4])
