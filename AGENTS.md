# Repository Guidelines

## Project Structure & Module Organization

This repository packages the `verifiche-mat-fis` educational skill in two forms. `verifiche-mat-fis/` is the source skill: its `SKILL.md` defines behavior, `references/` contains subject and class materials, `assets/` holds LaTeX templates, and `scripts/` contains Python utilities. `plugin-verifiche-mat-fis/` mirrors that content under the plugin layout and adds `plugin.json`. Root-level ZIP files are distributable archives; `installa-verifiche-mat-fis.sh` supports installation. Keep mirrored skill content aligned when editing either copy.

## Build, Test, and Development Commands

There is no root build system or test suite. Install Python dependencies for the relevant skill with `python -m pip install -r verifiche-mat-fis/requirements.txt`. Run a utility directly with `python verifiche-mat-fis/scripts/progetto.py --help` or `python verifiche-mat-fis/scripts/registro_xlsx.py --help` (when supported). Check installer usage with `bash installa-verifiche-mat-fis.sh --help` if available. Rebuild ZIP distributions only when preparing a release, preserving their expected internal directory structure.

## Coding Style & Naming Conventions

Use UTF-8 text and keep Markdown headings, lists, and Italian terminology consistent with neighboring files. Python files use four-space indentation and descriptive `snake_case` names; preserve existing CLI behavior and document new options. Reference files use descriptive lowercase names, often including subject and class, such as `argomenti_fisica_classe3.md`. LaTeX templates should retain their current naming and compile-oriented formatting.

## Testing Guidelines

No formal framework or coverage threshold is configured. For Python changes, run the affected script's `--help` command and exercise the changed behavior with a small representative input. For content or template changes, inspect the rendered or compiled output where practical. Validate archive contents after repackaging so paths match the plugin structure.

## Commit & Pull Request Guidelines

Git history is not available in this working directory, so no repository-specific commit convention can be confirmed. Use short imperative commit subjects, for example `Aggiorna guida alle varianti`. Pull requests should summarize the affected skill/plugin files, explain user-visible changes, link related issues when applicable, and include sample output or screenshots for document/template changes.

## Security & Configuration

Do not commit credentials, private student data, or generated records containing personal information. Keep dependencies declared in the relevant `requirements.txt`, and avoid changing installer behavior without documenting supported paths and options.
