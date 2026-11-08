#!/usr/bin/env bash
set -euo pipefail

skill_source="$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")/verifiche-mat-fis"
exec python3 - "$skill_source" "$@" <<'PY'
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

parser = argparse.ArgumentParser(
    description="Senza argomenti installa o aggiorna verifiche-mat-fis nelle cartelle standard di Claude, Codex, OpenCode e .agents sotto la home. Gli aggiornamenti sostituiscono l'intero contenuto della skill.",
    epilog="--dest permette di scegliere cartelle diverse da quelle standard.",
)
parser.add_argument("mode", choices=("auto", "install", "update"), nargs="?", default="auto")
parser.add_argument("--dest", action="append", metavar="CARTELLA")
parser.add_argument("--plugin", action="store_true",
                    help="genera o aggiorna il pacchetto plugin e il relativo ZIP, senza installare la skill")
args = parser.parse_args(sys.argv[2:])
source = Path(sys.argv[1]).resolve()


def recognized(path):
    skill = path / "SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        return False
    lines = skill.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    names = [line.split(":", 1)[1].strip().strip("\"'")
             for line in lines[1:end] if line.startswith("name:")]
    return names == ["verifiche-mat-fis"]


def checked_path(raw):
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Collegamento simbolico non ammesso: {current}")
    return path.resolve()


try:
    if not recognized(source):
        raise ValueError(f"Sorgente della skill non riconosciuta: {source}")
    if any(path.is_symlink() for path in source.rglob("*")):
        raise ValueError("La sorgente contiene collegamenti simbolici")
    if args.plugin:
        root = source.parent
        plugin_name = "plugin-verifiche-mat-fis"
        plugin_dir = root / plugin_name
        plugin_skill = plugin_dir / "skills" / "verifiche-mat-fis"
        metadata = plugin_dir / "plugin.json"
        if not metadata.is_file():
            raise ValueError(f"Metadati plugin mancanti: {metadata}")
        with metadata.open(encoding="utf-8") as stream:
            json.load(stream)
        plugin_dir.mkdir(parents=True, exist_ok=True)
        plugin_skill.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".verifiche-plugin-", dir=root) as temporary:
            stage = Path(temporary) / "plugin"
            shutil.copytree(source, stage / "skills" / "verifiche-mat-fis")
            shutil.copy2(metadata, stage / "plugin.json")
            if plugin_dir.exists():
                shutil.rmtree(plugin_dir)
            stage.rename(plugin_dir)
        archive = root / f"{plugin_name}.zip"
        with tempfile.NamedTemporaryFile(prefix=f".{plugin_name}-", suffix=".zip", dir=root, delete=False) as temporary_zip:
            archive_stage = Path(temporary_zip.name)
        try:
            with zipfile.ZipFile(archive_stage, "w", zipfile.ZIP_DEFLATED) as bundle:
                for item in sorted(plugin_dir.rglob("*")):
                    if item.is_file():
                        bundle.write(item, item.relative_to(root))
            archive_stage.replace(archive)
        finally:
            archive_stage.unlink(missing_ok=True)
        print(f"Pacchetto plugin aggiornato: {plugin_dir}")
        print(f"Archivio plugin creato: {archive}")
        raise SystemExit(0)
    destinations = args.dest or [Path.home() / directory / "verifiche-mat-fis"
                                 for directory in (".claude/skills", ".codex/skills", ".config/opencode/skills", ".agents/skills")]
    targets = [checked_path(raw) for raw in destinations]
    for i, target in enumerate(targets):
        if target == source or target in source.parents or source in target.parents:
            raise ValueError(f"Destinazione sovrapposta alla sorgente: {target}")
        if any(target == other or target in other.parents or other in target.parents
               for other in targets[:i]):
            raise ValueError(f"Destinazioni sovrapposte: {target}")
        if target.exists() and not target.is_dir():
            raise ValueError(f"La destinazione non è una cartella: {target}")
        if args.mode == "install" and target.exists() and any(target.iterdir()):
            raise ValueError(f"Destinazione non vuota; usare update per una skill già installata: {target}")
        if args.mode == "update" and not recognized(target):
            raise ValueError(f"Installazione verifiche-mat-fis non riconosciuta: {target}")
        if args.mode == "auto" and target.exists() and any(target.iterdir()) and not recognized(target):
            raise ValueError(f"Installazione verifiche-mat-fis non riconosciuta: {target}")
        if target.exists() and any(path.is_symlink() for path in target.rglob("*")):
            raise ValueError(f"La destinazione contiene collegamenti simbolici: {target}")

    # Tutte le destinazioni sono validate e tutte le copie preparate prima delle sostituzioni.
    with ExitStack() as stack:
        staged = []
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            stage = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix=".verifiche-mat-fis-", dir=target.parent)))
            shutil.copytree(source, stage / "skill")
            staged.append((target, stage))
        replaced = []
        try:
            for target, stage in staged:
                existed = target.exists()
                if existed:
                    target.rename(stage / "previous")
                replaced.append((target, stage, existed))
                (stage / "skill").rename(target)
        except OSError:
            for target, stage, existed in reversed(replaced):
                if target.exists():
                    shutil.rmtree(target)
                if existed:
                    (stage / "previous").rename(target)
            raise
    for target, stage, existed in replaced:
        print(f"Skill {'aggiornata' if existed else 'installata'}: {target}")
except (OSError, ValueError) as error:
    parser.exit(1, f"Errore: {error}\n")
PY
