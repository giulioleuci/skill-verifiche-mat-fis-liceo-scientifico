#!/usr/bin/env python3
"""Registro da 1 a 40 evidenze, totale Max 1000; JSON: lista di oggetti COLS.

ID evidenza e ID Argomento: stringhe non vuote senza spazi esterni. ID evidenza
è assegnato dall'autore e resta invariato per riordini, pesi e descrizioni.
Esercizio: testo non vuoto o intero positivo; Punto/gruppo: testo non vuoto
("intero" per quesiti singoli). Max: intero positivo. Gli altri campi sono
testi non vuoti; Note utente è una stringa opzionale. ID e nome argomento
hanno corrispondenza univoca nella versione. Schemi precedenti sono rifiutati.

write crea senza sovrascrivere; update conserva note per ID e blocca eliminazioni
di ID annotati o note in conflitto: archiviare e gestire esplicitamente le note
nel registro prima di riprovare. Accorpamenti/separazioni richiedono nuovi ID e
tracciamento esplicito della derivazione nella revisione, mai ID riciclati.
"""
import argparse
from io import BytesIO
import json
import os
from pathlib import Path
import sys
import tempfile
from zipfile import BadZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.utils.exceptions import InvalidFileException


COLS = ["ID evidenza", "Esercizio", "Punto/gruppo", "Indicatore", "ID Argomento", "Max",
        "Descrizione evidenza", "Nome completo argomento", "Note utente"]


def _error(row, column, problem):
    raise ValueError(f"riga {row}, colonna '{column}': {problem}")


def validate(rows, row_numbers=None):
    """Valida il JSON o righe Excel; restituisce copie con Note utente presente."""
    if not isinstance(rows, list):
        _error(1, "registro", "attesa una lista di oggetti")
    if not 1 <= len(rows) <= 40:
        _error(1, "ID evidenza", "servono da 1 a 40 evidenze")
    ids, topics, names, result = set(), {}, {}, []
    for number, row in zip(row_numbers or range(2, len(rows) + 2), rows):
        if not isinstance(row, dict):
            _error(number, "registro", "atteso un oggetto con le colonne del registro")
        for column in row.keys() - COLS:
            _error(number, column, "colonna sconosciuta")
        for column in COLS:
            value = row.get(column, "" if column == "Note utente" else None)
            if column == "Max":
                if type(value) is not int or value <= 0:
                    _error(number, column, "deve essere un intero positivo")
            elif column == "Esercizio" and type(value) is int and value > 0:
                continue
            elif not isinstance(value, str) or (column != "Note utente" and not value.strip()):
                _error(number, column, "testo obbligatorio non vuoto" if column != "Note utente" else "attesa una stringa")
            elif len(value) > 32767 or ILLEGAL_CHARACTERS_RE.search(value):
                _error(number, column, "testo non rappresentabile in una cella Excel")
            if column in ("ID evidenza", "ID Argomento") and value != value.strip():
                _error(number, column, "ID senza spazi iniziali o finali")
        if row["Indicatore"] not in ("ANA", "SVI", "ARG", "COM"):
            _error(number, "Indicatore", "ammessi ANA, SVI, ARG, COM")
        eid, tid, name = row["ID evidenza"], row["ID Argomento"], row["Nome completo argomento"].strip()
        if eid in ids:
            _error(number, "ID evidenza", f"ID duplicato: {eid}")
        if tid in topics and topics[tid] != name:
            _error(number, "Nome completo argomento", f"ID Argomento {tid} associato a nomi diversi")
        if name in names and names[name] != tid:
            _error(number, "ID Argomento", f"nome argomento già associato a {names[name]}")
        ids.add(eid)
        topics[tid], names[name] = name, tid
        result.append({**row, "Note utente": row.get("Note utente", "")})
    if sum(row["Max"] for row in result) != 1000:
        _error(1, "Max", "la somma deve essere 1000")
    return result


def read(path):
    """Legge e valida il registro; restituisce list[dict] senza stampare."""
    return _read(path)[0]


def _read(path):
    try:
        wb = load_workbook(path, data_only=False)
    except (BadZipFile, InvalidFileException, KeyError, SyntaxError) as error:
        raise ValueError(f"registro Excel non valido: {error}") from error
    try:
        ws = wb.active
        header = [cell.value for cell in ws[1]]
        if header != COLS:
            _error(1, "intestazioni", f"schema non valido; colonne richieste: {', '.join(COLS)}. Nessuna migrazione automatica")
        rows, numbers = [], []
        for cells in ws.iter_rows(min_row=2):
            if all(cell.value in (None, "") for cell in cells):
                continue
            row = {}
            for column, cell in zip(COLS, cells):
                if cell.data_type in ("f", "e"):
                    _error(cell.row, column, "formule ed errori Excel non ammessi")
                row[column] = "" if column == "Note utente" and cell.value is None else cell.value
            rows.append(row)
            numbers.append(cells[0].row)
        return validate(rows, numbers), numbers
    finally:
        wb.close()


def _source(src):
    with open(src, encoding="utf-8") as source:
        return validate(json.load(source))


def _save(rows, dst, previous=None):
    dst = Path(dst)
    wb = Workbook()
    ws = wb.active
    ws.append(COLS)
    for row in rows:
        ws.append([row[column] for column in COLS])
        for cell in ws[ws.max_row]:
            if isinstance(cell.value, str):
                cell.data_type = "s"  # Le note e i testi sono letterali, anche se iniziano con '='.
    fd, temporary = tempfile.mkstemp(prefix=f".{dst.name}.", suffix=".xlsx", dir=dst.parent)
    os.close(fd)
    try:
        wb.save(temporary)
        read(temporary)
        if previous is None:
            os.link(temporary, dst)  # Pubblicazione atomica senza sovrascrivere, anche in caso di concorrenza.
        else:
            if dst.is_symlink() or dst.read_bytes() != previous:
                raise ValueError("registro cambiato durante l'aggiornamento; rileggere e riprovare")
            os.replace(temporary, dst)
    finally:
        wb.close()
        Path(temporary).unlink(missing_ok=True)


def write(src, dst):
    """Crea un nuovo registro; una destinazione esistente è sempre rifiutata."""
    if os.path.lexists(dst):
        raise FileExistsError(f"destinazione già esistente: {dst}; usare update per aggiornarla")
    _save(_source(src), dst)


def update(src, dst):
    """Aggiorna esplicitamente conservando tutte le note per ID evidenza."""
    dst = Path(dst)
    if dst.is_symlink():
        raise ValueError("update richiede un registro regolare, non un collegamento simbolico")
    previous = dst.read_bytes()
    old_rows, numbers = _read(BytesIO(previous))
    rows = _source(src)
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
    _save(rows, dst, previous)


def check(path):
    rows = read(path)
    print(f"evidenze={len(rows)} (1-40) somma Max=1000 (1000)")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in (("write", "crea un nuovo registro senza sovrascrivere"),
                              ("update", "aggiorna esplicitamente e conserva le note per ID")):
        command = commands.add_parser(name, help=description)
        command.add_argument("src", help="JSON delle evidenze con colonne COLS")
        command.add_argument("dst", help="registro .xlsx")
    command = commands.add_parser("check", help="valida schema, campi, evidenze e totale")
    command.add_argument("path", help="registro .xlsx")
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            check(args.path)
        else:
            {"write": write, "update": update}[args.command](args.src, args.dst)
    except (ValueError, OSError, BadZipFile, InvalidFileException, KeyError) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
