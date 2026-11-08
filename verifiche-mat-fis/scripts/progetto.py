#!/usr/bin/env python3
"""Stato, approvazioni esplicite, confronto registri e matrice di copertura.

Uso: progetto.py stato progetto.json
     progetto.py approva progetto.json VERSIONE scaletta|registro
     progetto.py confronta prima.xlsx dopo.xlsx [--derivazioni mappa.json]
     progetto.py copertura matrice.json
Gli schemi sono descritti in references/progetto.md.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from zipfile import BadZipFile

from openpyxl.utils.exceptions import InvalidFileException

from registro_xlsx import read


def leggi_json(path):
    with open(path, encoding='utf-8') as source:
        return json.load(source)


def carica(path):
    data = leggi_json(path)
    if not isinstance(data, dict) or not isinstance(data.get('versioni'), dict) or not data['versioni']:
        raise ValueError('progetto: versioni deve essere un oggetto non vuoto')
    if not isinstance(data.get('preferenze', {}), dict):
        raise ValueError('progetto: preferenze deve essere un oggetto')
    for name, version in data['versioni'].items():
        if not name.strip() or not isinstance(version, dict):
            raise ValueError(f'versione {name}: metadati non validi')
        if type(version.get('durata_minuti')) is not int or version['durata_minuti'] <= 0:
            raise ValueError(f'versione {name}: durata_minuti deve essere un intero positivo')
        for field in ('font', 'fase'):
            if not isinstance(version.get(field), str) or not version[field].strip():
                raise ValueError(f'versione {name}: {field} obbligatorio')
        if not isinstance(version.get('approvazioni', {}), dict) or any(
                not isinstance(value, dict) for value in version.get('approvazioni', {}).values()):
            raise ValueError(f'versione {name}: approvazioni non valide')
        for kind in ('scaletta', 'registro'):
            if kind in version and (not isinstance(version[kind], str) or not version[kind].strip()):
                raise ValueError(f'versione {name}: percorso {kind} non valido')
        standard = version.get('standard')
        if standard is not None and (not isinstance(standard, str) or standard not in data['versioni'] or standard == name):
            raise ValueError(f'versione {name}: standard di riferimento non valido')
    for name in data['versioni']:
        seen = set()
        current = name
        while current is not None:
            if current in seen:
                raise ValueError(f'versione {name}: ciclo nei riferimenti standard')
            seen.add(current)
            current = data['versioni'][current].get('standard')
    return data


def digest(content):
    return hashlib.sha256(content).hexdigest()


def revisione(path, data, name, kind):
    version = data['versioni'][name]
    filename = version.get(kind)
    if not filename:
        return None
    artifact = Path(path).parent / filename
    if not artifact.is_file():
        return None
    context = {'preferenze': data.get('preferenze', {}),
               'versione': {k: v for k, v in version.items()
                           if k not in ('approvazioni', 'fase') and (kind != 'scaletta' or k != 'registro')}}
    if kind == 'registro' and version.get('scaletta'):
        outline = Path(path).parent / version['scaletta']
        context['scaletta_sha256'] = digest(outline.read_bytes()) if outline.is_file() else None
    return {'sha256': digest(artifact.read_bytes()),
            'contesto': digest(json.dumps(context, sort_keys=True, ensure_ascii=False).encode())}


def stato_versione(path, data, name, kind):
    version = data['versioni'][name]
    current = revisione(path, data, name, kind)
    if current is None:
        return 'mancante'
    approval = version.get('approvazioni', {}).get(kind)
    standard = version.get('standard')
    if standard and approval:
        if (stato_versione(path, data, standard, kind) != 'approvato'
                or approval.get('standard') != revisione(path, data, standard, kind)):
            return 'da riallineare'
    if not isinstance(approval, dict) or approval.get('revisione') != current:
        return 'da revisionare'
    return 'approvato'


def stato(path):
    data = carica(path)
    return {name: {'standard': version.get('standard'), 'durata_minuti': version['durata_minuti'],
                   'font': version['font'], 'fase': version['fase'],
                   **{kind: stato_versione(path, data, name, kind) for kind in ('scaletta', 'registro')}}
            for name, version in data['versioni'].items()}


def approva(path, name, kind):
    """Registrare soltanto dopo il consenso esplicito del docente alla revisione."""
    path = Path(path)
    data = carica(path)
    if name not in data['versioni'] or kind not in ('scaletta', 'registro'):
        raise ValueError('versione o tipo di approvazione non valido')
    current = revisione(path, data, name, kind)
    if current is None:
        raise ValueError(f'{name}: {kind} mancante')
    version = data['versioni'][name]
    if kind == 'registro':
        read(path.parent / version[kind])
    approval = {'revisione': current}
    standard = version.get('standard')
    if standard:
        if stato_versione(path, data, standard, kind) != 'approvato':
            raise ValueError(f'{name}: approvare prima {kind} dello standard {standard}')
        approval['standard'] = revisione(path, data, standard, kind)
    version.setdefault('approvazioni', {})[kind] = approval
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.progetto-', suffix='.json', delete=False) as output:
            temporary = Path(output.name)
            json.dump(data, output, ensure_ascii=False, indent=2)
            output.write('\n')
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return approval


def confronta(before, after, derivazioni=None):
    left = {row['ID evidenza']: row for row in read(before)}
    right = {row['ID evidenza']: row for row in read(after)}
    changes = {}
    kept = []
    for evidence in sorted(left.keys() & right.keys()):
        diff = {field: {'prima': left[evidence][field], 'dopo': right[evidence][field]}
                for field in left[evidence] if left[evidence][field] != right[evidence][field]}
        if diff:
            changes[evidence] = diff
        else:
            kept.append(evidence)
    derivazioni = {} if derivazioni is None else derivazioni
    if not isinstance(derivazioni, dict):
        raise ValueError('derivazioni: atteso oggetto ID nuovo -> lista ID precedenti')
    for target, sources in derivazioni.items():
        if target not in right or not isinstance(sources, list) or not sources or any(not isinstance(source, str) or source not in left for source in sources):
            raise ValueError(f'derivazione non valida: {target}')
    result = {'mantenuti': kept, 'modificati': changes,
              'eliminati': sorted(left.keys() - right.keys()), 'aggiunti': sorted(right.keys() - left.keys()),
              'derivazioni': derivazioni}
    for key, field in (('pesi_argomenti', 'ID Argomento'), ('pesi_indicatori', 'Indicatore')):
        totals = []
        for rows in (left.values(), right.values()):
            tally = defaultdict(int)
            for row in rows:
                tally[row[field]] += row['Max']
            totals.append(tally)
        result[key] = {item: {'prima': totals[0][item], 'dopo': totals[1][item]}
                       for item in sorted(totals[0].keys() | totals[1].keys())}
    result['obiettivi'] = {
        label: {row['ID Argomento']: row['Nome completo argomento'] for row in rows.values()}
        for label, rows in (('prima', left), ('dopo', right))}
    result['valutazione'] = 'Il confronto non certifica l’equivalenza didattica: motivarla con il docente.'
    return result


def copertura(path):
    data = leggi_json(path)
    if not isinstance(data, dict) or not isinstance(data.get('registro'), str):
        raise ValueError('matrice: registro obbligatorio')
    requests = data.get('richieste')
    steps = data.get('passaggi')
    coverage = data.get('copertura_evidenze')
    if not isinstance(requests, list) or not requests or not isinstance(steps, list) or not isinstance(coverage, dict):
        raise ValueError('matrice: richieste, passaggi e copertura_evidenze obbligatori')
    if any(not isinstance(step, str) or not step.strip() for step in steps) or len(set(steps)) != len(steps):
        raise ValueError('matrice: ID passaggio vuoto o duplicato')
    rows = {row['ID evidenza']: row for row in read(Path(path).parent / data['registro'])}
    issues = []
    linked = set()
    request_ids = set()
    for request in requests:
        if (not isinstance(request, dict) or not isinstance(request.get('id'), str) or not request['id'].strip()
                or request['id'] in request_ids or not isinstance(request.get('evidenze'), list)
                or not isinstance(request.get('esercizio'), (str, int)) or not str(request['esercizio']).strip()
                or not isinstance(request.get('punto'), str) or not request['punto'].strip()):
            raise ValueError('matrice: richiesta non valida o ID duplicato')
        request_ids.add(request['id'])
        if not request['evidenze']:
            issues.append(f"richiesta {request['id']}: priva di valutazione")
        for evidence in request['evidenze']:
            if not isinstance(evidence, str) or evidence not in rows:
                issues.append(f"richiesta {request['id']}: evidenza sconosciuta {evidence}")
                continue
            linked.add(evidence)
            if str(rows[evidence]['Esercizio']) != str(request['esercizio']):
                issues.append(f"richiesta {request['id']}: esercizio diverso per {evidence}")
            points = [point.strip() for point in rows[evidence]['Punto/gruppo'].split(',')]
            if request['punto'] not in points:
                issues.append(f"richiesta {request['id']}: punto diverso per {evidence}")
    for evidence in rows:
        if evidence not in linked:
            issues.append(f'evidenza {evidence}: priva di richiesta corrispondente')
        links = coverage.get(evidence, [])
        if not isinstance(links, list) or not links:
            issues.append(f'evidenza {evidence}: priva di passaggi nello svolgimento')
        else:
            for step in links:
                if not isinstance(step, str) or step not in steps:
                    issues.append(f'evidenza {evidence}: passaggio sconosciuto {step}')
    for evidence in coverage.keys() - rows.keys():
        issues.append(f'copertura: evidenza sconosciuta {evidence}')
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('stato').add_argument('progetto')
    approve = commands.add_parser('approva')
    approve.add_argument('progetto')
    approve.add_argument('versione')
    approve.add_argument('tipo', choices=['scaletta', 'registro'])
    compare = commands.add_parser('confronta')
    compare.add_argument('prima')
    compare.add_argument('dopo')
    compare.add_argument('--derivazioni')
    commands.add_parser('copertura').add_argument('matrice')
    args = parser.parse_args()
    try:
        if args.command == 'stato':
            result = stato(args.progetto)
        elif args.command == 'approva':
            result = approva(args.progetto, args.versione, args.tipo)
        elif args.command == 'confronta':
            result = confronta(args.prima, args.dopo, leggi_json(args.derivazioni) if args.derivazioni else None)
        else:
            result = copertura(args.matrice)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return int(bool(result))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, BadZipFile, InvalidFileException, KeyError, TypeError) as error:
        print(f'Errore: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
