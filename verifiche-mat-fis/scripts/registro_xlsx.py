#!/usr/bin/env python3
"""Registro da 1 a 40 evidenze, totale Max 1000; JSON: lista di oggetti COLS.

ID evidenza e Sigla argomento: stringhe non vuote senza spazi esterni. ID evidenza
è assegnato dall'autore; nelle revisioni rinumerate serve una mappa delle azioni.
Esercizio: testo non vuoto o intero positivo; Punto/gruppo: testo non vuoto
("intero" per quesiti singoli). Max: intero positivo. Gli altri campi sono
testi non vuoti; Note utente è una stringa opzionale. Sigla e nome argomento
hanno corrispondenza univoca nella versione.

Livello: 1, 2, 2A (livello 2 di accesso) o 3; --classe basso|medio|alto verifica
L1 20-25%, L3 10-20%, accessi 2A >= 30% di L2, un 1 o 2A per esercizio.

Griglie d'esame (solo su richiesta del docente), --griglia matematica|fisica|mista:
indicatori e massimi per indicatore fissi, uguali in proporzione al quadro
ministeriale (5/6/5/4 su 20, qui x50). Senza --griglia: IND => matematica,
DAT => fisica/mista, altrimenti ordinaria (ANA/SVI/ARG/COM, massimi liberi).

write crea senza sovrascrivere; update conserva note per ID e blocca eliminazioni
di ID annotati o note in conflitto: archiviare e gestire esplicitamente le note
nel registro prima di riprovare. Accorpamenti/separazioni richiedono nuovi ID e
tracciamento esplicito della derivazione nella revisione.
"""
import argparse
from collections import Counter
from io import BytesIO
import json
import os
from pathlib import Path
import sys
import tempfile
from zipfile import BadZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.exceptions import InvalidFileException


COLS = ["ID evidenza", "Esercizio", "Punto/gruppo", "Indicatore", "Sigla argomento", "Max",
        "Descrizione evidenza", "Nome completo argomento", "Livello", "Note utente"]
COLS_OLD = [c for c in COLS if c != "Livello"]  # registri precedenti ai livelli: leggibili, da aggiornare

# Livello 1/2/3 di difficoltà della richiesta; "2A" = livello 2 di accesso (svolgibile anche da chi ha solo le basi).
LIVELLI = ("1", "2", "2A", "3")
# Percentuali bersaglio L1-L2-L3 per livello classe. Intervalli duri: L1 20-25%, L3 10-20%.
BERSAGLIO = {"basso": (25, 65, 10), "medio": (20, 65, 15), "alto": (20, 60, 20)}

# Indicatori ammessi e massimo totale per indicatore (None = libero). Mista = fisica.
GRIGLIE = {
    "ordinaria": dict.fromkeys(("ANA", "SVI", "ARG", "COM")),
    "matematica": {"ANA": 250, "IND": 300, "SVI": 250, "ARG": 200},
    "fisica": {"ANA": 250, "SVI": 300, "DAT": 250, "ARG": 200},
}
GRIGLIE["mista"] = GRIGLIE["fisica"]


def _griglia(rows, griglia):
    if griglia:
        return GRIGLIE[griglia]
    ind = {r.get("Indicatore") for r in rows if isinstance(r, dict)}
    return GRIGLIE["matematica" if "IND" in ind else "fisica" if "DAT" in ind else "ordinaria"]


# Colonne calcolate inserite dopo Max nel foglio Excel (non fanno parte dello schema JSON).
PCT_COLS = ["% esercizio", "% verifica"]
N_PCT = len(PCT_COLS)

# Colonna 1-based di «Descrizione evidenza» nel foglio con le colonne percentuale.
_DESC_COL = 6 + N_PCT + 1  # = 9

CARBON = "1C1C1C"
TEXT = "FFFFFF"
MUTED = "E0E0E0"
GRID = "222222"

# Intestazioni attese per tutti i formati supportati in lettura: (has_pct, span, header).
def _headers(cols):
    return [
        (True,  4, cols[:6] + PCT_COLS + ["Descrizione evidenza", None, None, None] + cols[7:], cols),
        (True,  1, cols[:6] + PCT_COLS + cols[6:], cols),
        (False, 4, cols[:7] + [None, None, None] + cols[7:], cols),
        (False, 1, list(cols), cols),
    ]


_HEADERS = _headers(COLS) + _headers(COLS_OLD)


def _format_sheet(ws, layout):
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A2"
    # Colonne: ID, Esercizio, Punto/gruppo, Indicatore, Sigla, Max, %Es, %Ver, Desc(x4 merged/x1 flat), Nome, Note
    if layout == "merged":
        widths = [12, 12, 20, 12, 16, 8, 8, 8, 15, 15, 15, 15, 20, 8, 18]
    else:
        widths = [12, 12, 20, 12, 16, 8, 8, 8, 20, 20, 8, 18]
    for column, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(column)].width = width
    edge = Side(style="hair", color=GRID)
    pct_col_set = set(range(7, 7 + N_PCT))  # 1-based: {7, 8}
    for row in ws.iter_rows():
        is_header = row[0].row == 1
        for cell in row:
            cell.fill = PatternFill(fill_type="solid", fgColor=CARBON)
            cell.font = Font(name="Open Sans", size=8, bold=is_header,
                             color=TEXT if is_header else MUTED)
            cell.alignment = Alignment(
                horizontal="center" if cell.column in ({1, 2, 4, 6} | pct_col_set) or ws.cell(1, cell.column).value == "Livello" else "left",
                vertical="center",
                wrap_text=True,
            )
            cell.border = Border(bottom=edge)
            if cell.column == 6 and not is_header:
                cell.font = Font(name="Inconsolata", size=8, color=TEXT)
            if cell.column in pct_col_set and not is_header:
                # Valore già moltiplicato per 100; '"%" letterale per non ri-moltiplicare.
                cell.number_format = '0"%"'
        if is_header:
            ws.row_dimensions[1].height = 28
        else:
            desc_width = sum(widths[_DESC_COL - 1: _DESC_COL + 2]) if layout == "merged" else widths[_DESC_COL - 1]
            description = ws.cell(row[0].row, _DESC_COL).value
            lines = max(1, (len(str(description or "")) + desc_width - 1) // desc_width)
            ws.row_dimensions[row[0].row].height = min(60, max(18, lines * 12))


def _error(row, column, problem):
    raise ValueError(f"riga {row}, colonna '{column}': {problem}")


def validate(rows, row_numbers=None, livelli=True, griglia=None):
    """Valida il JSON o righe Excel; restituisce copie con Note utente presente."""
    if not isinstance(rows, list):
        _error(1, "registro", "attesa una lista di oggetti")
    if not 1 <= len(rows) <= 40:
        _error(1, "ID evidenza", "servono da 1 a 40 evidenze")
    ids, topics, names, result = set(), {}, {}, []
    ammessi = _griglia(rows, griglia)
    for number, row in zip(row_numbers or range(2, len(rows) + 2), rows):
        if not isinstance(row, dict):
            _error(number, "registro", "atteso un oggetto con le colonne del registro")
        for column in row.keys() - COLS:
            _error(number, column, "colonna sconosciuta")
        for column in COLS:
            if column == "Livello" and not livelli:
                continue
            value = row.get(column, "" if column == "Note utente" else None)
            if column == "Livello":
                if value not in LIVELLI:
                    _error(number, column, "ammessi 1, 2, 2A, 3 (2A = livello 2 di accesso)")
                continue
            if column == "Max":
                if type(value) is not int or value <= 0:
                    _error(number, column, "deve essere un intero positivo")
            elif column == "Esercizio" and type(value) is int and value > 0:
                continue
            elif not isinstance(value, str) or (column != "Note utente" and not value.strip()):
                _error(number, column, "testo obbligatorio non vuoto" if column != "Note utente" else "attesa una stringa")
            elif len(value) > 32767 or ILLEGAL_CHARACTERS_RE.search(value):
                _error(number, column, "testo non rappresentabile in una cella Excel")
            if column in ("ID evidenza", "Sigla argomento") and value != value.strip():
                _error(number, column, "ID senza spazi iniziali o finali")
        if row["Indicatore"] not in ammessi:
            _error(number, "Indicatore", f"ammessi {', '.join(ammessi)}")
        eid, tid, name = row["ID evidenza"], row["Sigla argomento"], row["Nome completo argomento"].strip()
        if eid in ids:
            _error(number, "ID evidenza", f"ID duplicato: {eid}")
        if tid in topics and topics[tid] != name:
            _error(number, "Nome completo argomento", f"Sigla argomento {tid} associata a nomi diversi")
        if name in names and names[name] != tid:
            _error(number, "Sigla argomento", f"nome argomento già associato a {names[name]}")
        ids.add(eid)
        topics[tid], names[name] = name, tid
        result.append({**row, "Note utente": row.get("Note utente", ""), "Livello": row.get("Livello")})
    if sum(row["Max"] for row in result) != 1000:
        _error(1, "Max", "la somma deve essere 1000")
    for ind, massimo in ammessi.items():
        punti = sum(row["Max"] for row in result if row["Indicatore"] == ind)
        if massimo is not None and punti != massimo:
            _error(1, "Max", f"griglia d'esame: {ind} deve sommare {massimo} (ora {punti})")
    return result


def read(path, griglia=None):
    """Legge e valida il registro; restituisce list[dict] senza stampare."""
    return _read(path, griglia)[0]


def _read(path, griglia=None):
    try:
        wb = load_workbook(path, data_only=False)
    except (BadZipFile, InvalidFileException, KeyError, SyntaxError) as error:
        raise ValueError(f"registro Excel non valido: {error}") from error
    try:
        ws = wb.active
        header = [ws.cell(1, column).value for column in range(1, ws.max_column + 1)]
        # Rileva formato: colonne percentuale presenti e ampiezza merge di Descrizione evidenza.
        match = next(((hp, sp, cols) for hp, sp, h, cols in _HEADERS if header == h), None)
        if match is None:
            _error(1, "intestazioni", f"schema non valido; colonne richieste: {', '.join(COLS)}. Nessuna migrazione automatica")
        has_pct, span, cols = match
        pct_skip = N_PCT if has_pct else 0
        desc_col = 7 + pct_skip          # 1-based, es. 9 (new) o 7 (old)
        last = get_column_letter(desc_col - 1 + span)
        desc_letter = get_column_letter(desc_col)
        rows, numbers = [], []
        expected_merges = {f"{desc_letter}1:{last}1"} if span > 1 else set()
        for number in range(2, ws.max_row + 1):
            cells = [ws.cell(number, column) for column in range(1, ws.max_column + 1)]
            if all(cell.value in (None, "") for cell in cells):
                continue
            if span > 1:
                expected_merges.add(f"{desc_letter}{number}:{last}{number}")
            row = {}
            # Legge le 6 colonne iniziali, salta le colonne percentuale, poi Descrizione (1 logica), poi resto.
            logical_cells = cells[:6] + cells[6 + pct_skip: 7 + pct_skip] + cells[6 + pct_skip + span:]
            for column, cell in zip(cols, logical_cells):
                if cell.data_type in ("f", "e"):
                    _error(cell.row, column, "formule ed errori Excel non ammessi")
                row[column] = "" if column == "Note utente" and cell.value is None else cell.value
            rows.append(row)
            numbers.append(number)
        actual_merges = {str(merged_range) for merged_range in ws.merged_cells.ranges}
        if actual_merges != expected_merges:
            _error(1, "celle unite", "le celle unite non corrispondono al formato previsto")
        return validate(rows, numbers, livelli=cols is COLS, griglia=griglia), numbers
    finally:
        wb.close()


def _source(src, griglia=None):
    with open(src, encoding="utf-8") as source:
        return validate(json.load(source), griglia=griglia)


def _save(rows, dst, previous=None, layout="merged", griglia=None):
    if layout not in ("merged", "flat"):
        raise ValueError(f"layout non supportato: {layout}")
    dst = Path(dst)

    # Totali per esercizio usati per le percentuali indicative.
    exercise_totals: dict = {}
    for row in rows:
        ex = str(row["Esercizio"])
        exercise_totals[ex] = exercise_totals.get(ex, 0) + row["Max"]

    desc_col = _DESC_COL  # = 9 (1-based)
    desc_letter = get_column_letter(desc_col)

    wb = Workbook()
    ws = wb.active
    if layout == "merged":
        ws.append(COLS[:6] + PCT_COLS + ["Descrizione evidenza", None, None, None] + COLS[7:])
        ws.merge_cells(f"{desc_letter}1:{get_column_letter(desc_col + 3)}1")
        for row in rows:
            ex = str(row["Esercizio"])
            pct_ex = round(row["Max"] / exercise_totals[ex] * 100)
            pct_tot = round(row["Max"] / 1000 * 100)
            ws.append([row[column] for column in COLS[:6]] +
                      [pct_ex, pct_tot,
                       row["Descrizione evidenza"], None, None, None,
                       row["Nome completo argomento"], row["Livello"], row["Note utente"]])
            number = ws.max_row
            # Nome, Livello e Note (desc_col+4..+6) sono dopo il merge di 4 celle.
            for column in list(range(1, 7)) + [desc_col] + list(range(desc_col + 4, desc_col + 7)):
                cell = ws.cell(number, column)
                if isinstance(cell.value, str):
                    cell.data_type = "s"
            ws.merge_cells(start_row=number, start_column=desc_col,
                           end_row=number, end_column=desc_col + 3)
    else:
        ws.append(COLS[:6] + PCT_COLS + COLS[6:])
        for row in rows:
            ex = str(row["Esercizio"])
            pct_ex = round(row["Max"] / exercise_totals[ex] * 100)
            pct_tot = round(row["Max"] / 1000 * 100)
            ws.append([row[column] for column in COLS[:6]] +
                      [pct_ex, pct_tot] +
                      [row[column] for column in COLS[6:]])
            for cell in ws[ws.max_row]:
                if isinstance(cell.value, str):
                    cell.data_type = "s"
    _format_sheet(ws, layout)
    fd, temporary = tempfile.mkstemp(prefix=f".{dst.name}.", suffix=".xlsx", dir=dst.parent)
    os.close(fd)
    try:
        wb.save(temporary)
        read(temporary, griglia)
        if previous is None:
            os.link(temporary, dst)  # Pubblicazione atomica senza sovrascrivere, anche in caso di concorrenza.
        else:
            if dst.is_symlink() or dst.read_bytes() != previous:
                raise ValueError("registro cambiato durante l'aggiornamento; rileggere e riprovare")
            os.replace(temporary, dst)
    finally:
        wb.close()
        Path(temporary).unlink(missing_ok=True)


def livelli(rows, classe):
    """Stampa la distribuzione per livello; solleva ValueError se viola gli intervalli duri."""
    if any(row["Livello"] is None for row in rows):
        raise ValueError("registro senza colonna Livello: aggiungerla con update")
    punti = lambda *ls: sum(row["Max"] for row in rows if row["Livello"] in ls)
    l1, l2, acc, l3 = punti("1"), punti("2", "2A"), punti("2A"), punti("3")
    print(f"classe {classe}: " + ", ".join(
        f"L{n}={p / 10:g}% (bersaglio {t}%)" + (" AVVISO scostamento > 2,5 punti" if abs(p / 10 - t) > 2.5 else "")
        for n, p, t in zip((1, 2, 3), (l1, l2, l3), BERSAGLIO[classe])))
    print(f"accesso L2: {acc / 10:g}% del totale = {acc / l2 * 100 if l2 else 0:.0f}% di L2")
    errori = []
    if not 200 <= l1 <= 250:
        errori.append(f"L1 deve valere 20-25% del totale (ora {l1 / 10:g}%)")
    if not 100 <= l3 <= 200:
        errori.append(f"L3 deve valere 10-20% del totale (ora {l3 / 10:g}%)")
    if acc * 10 < l2 * 3:
        errori.append(f"le evidenze di accesso (2A) devono valere almeno il 30% di L2 (ora {acc / l2 * 100 if l2 else 0:.0f}%)")
    for es in sorted({str(row["Esercizio"]) for row in rows}):
        if not any(str(row["Esercizio"]) == es and row["Livello"] in ("1", "2A") for row in rows):
            errori.append(f"esercizio {es}: serve almeno un'evidenza di livello 1 o 2A")
    if errori:
        raise ValueError("; ".join(errori))


def write(src, dst, classe, layout="merged", griglia=None):
    """Crea un nuovo registro; una destinazione esistente è sempre rifiutata."""
    if os.path.lexists(dst):
        raise FileExistsError(f"destinazione già esistente: {dst}; usare update per aggiornarla")
    rows = _source(src, griglia)
    livelli(rows, classe)
    _save(rows, dst, layout=layout, griglia=griglia)


def update(src, dst, classe, layout="merged", griglia=None):
    """Aggiorna esplicitamente conservando tutte le note per ID evidenza."""
    dst = Path(dst)
    if dst.is_symlink():
        raise ValueError("update richiede un registro regolare, non un collegamento simbolico")
    previous = dst.read_bytes()
    old_rows, numbers = _read(BytesIO(previous))
    rows = _source(src, griglia)
    livelli(rows, classe)
    by_id = {row["ID evidenza"]: row for row in rows}
    for number, old in zip(numbers, old_rows):
        note, eid = old["Note utente"], old["ID evidenza"]
        if not note:
            continue
        if eid not in by_id:
            _error(number, "Note utente", f"eliminazione dell'ID {eid} con note: archiviare e gestire esplicitamente le note prima di riprovare")
        if by_id[eid]["Note utente"] not in ("", note):
            _error(number, "Note utente", f"nota in conflitto per ID {eid}; conservare e gestire esplicitamente la nota esistente")
        by_id[eid]["Note utente"] = note
    _save(rows, dst, previous, layout, griglia)


def check(path, classe, griglia=None):
    rows = read(path, griglia)
    print(f"evidenze={len(rows)} (1-40) somma Max=1000 (1000)")
    for field in ("Esercizio", "Indicatore", "Sigla argomento"):
        totals = Counter()
        for row in rows:
            totals[str(row[field])] += row["Max"]
        print(f"{field}: " + ", ".join(f"{key}={value}" for key, value in totals.items()))
    livelli(rows, classe)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in (("write", "crea un nuovo registro senza sovrascrivere"),
                              ("update", "aggiorna esplicitamente e conserva le note per ID")):
        command = commands.add_parser(name, help=description)
        command.add_argument("src", help="JSON delle evidenze con colonne COLS")
        command.add_argument("dst", help="registro .xlsx")
        command.add_argument("--classe", choices=sorted(BERSAGLIO), required=True, help="livello della classe")
        command.add_argument("--layout", choices=("merged", "flat"), default="merged",
                             help="formato Excel (default: merged; flat solo se richiesto)")
    command = commands.add_parser("check", help="valida schema, campi, evidenze, totale e livelli; stampa i riepiloghi per esercizio, indicatore, argomento e livello")
    command.add_argument("path", help="registro .xlsx")
    command.add_argument("--classe", choices=sorted(BERSAGLIO), required=True, help="livello della classe")
    for command in commands.choices.values():
        command.add_argument("--griglia", choices=sorted(GRIGLIE), help="griglia d'esame o ordinaria (default: rilevata dagli indicatori)")
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            check(args.path, args.classe, args.griglia)
        else:
            {"write": write, "update": update}[args.command](args.src, args.dst, args.classe, args.layout, args.griglia)
    except (ValueError, OSError, BadZipFile, InvalidFileException, KeyError) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
