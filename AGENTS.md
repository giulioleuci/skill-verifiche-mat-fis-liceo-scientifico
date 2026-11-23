# Repository Guidelines

## Panoramica del Progetto

Questo repository sviluppa e distribuisce la skill educativa **`verifiche-mat-fis`**, progettata per supportare docenti della scuola secondaria di secondo grado (in particolare del liceo scientifico) nella progettazione, stesura, compilazione e correzione di:
- Verifiche scritte di matematica, fisica e laboratorio di fisica (classi 1ª–5ª);
- Varianti ordinarie equivalenti (Fila A/B) e prove per assenti;
- Prove di recupero mirate con griglia di recupero (NR/PR/R);
- Prove adattate per studenti con BES/DSA e tempi ridotti (stessa difficoltà concettuale, supporti concordati);
- Correttori per docenti con evidenze, punteggi su scala 1000 e indicatori ANA/SVI/ARG/COM;
- Quiz a scelta multipla randomizzati con fogli di risposta e correttore statistico con openpyxl.

## Struttura della Directory

- `verifiche-mat-fis/`: sorgente unica e modificabile della skill.
  - `SKILL.md`: punto di ingresso della skill, vincoli operativi, flussi e tabella comandi per l'agente.
  - `references/`: guide operative e criteri disciplinari:
    - `criteri_disciplinari.md`: macro-aree, pesi per anno, livelli di difficoltà (1/2/3) e relative soglie.
    - `griglia_valutazione.md`: indicatori ANA/SVI/ARG/COM con fasce di livello e, solo su richiesta, griglie d'esame di matematica, fisica e prova mista (ANA/IND/SVI/ARG, ANA/SVI/DAT/ARG) su 1000.
    - `generatore.md`: flusso di generazione prove, scaletta, varianti e recuperi.
    - `correttore.md`: estrazione evidenze, validazione del registro e correttore LaTeX.
    - `progetto.py` / `progetto.md`: ciclo di vita del progetto, tracciamento versioni e matrici di copertura.
    - `quiz.md`: generazione e correzione dei quiz a scelta multipla con analisi dei distrattori.
    - `latex.md`: preambolo canonico, convenzioni tipografiche e regole di compilazione.
    - `supporti_prova.md`: formule, costanti e formulari ammessi.
    - `schede/`: schede tematiche per materia e classe (`matematica_classe*.md`, `fisica_classe*.md`).
  - `assets/`: template LaTeX canonici:
    - `modello_verifica.tex`: layout della prova per lo studente (senza soluzioni né intestazioni di fila).
    - `correttore_template.tex`: layout del correttore docente (a colori, con riquadri evidenze).
    - `svolgimento_studenti_template.tex`: risoluzione per gli studenti (solo su richiesta esplicita).
    - `quiz_template.tex`: foglio quiz anonimo con griglia risposte.
  - `scripts/`: utility Python a supporto:
    - `registro_xlsx.py`: generazione, formattazione dark `#1C1C1C`, validazione (`check`) e aggiornamento (`update`) del registro evidenze.
    - `progetto.py`: gestione stati, log revisioni, approvazioni e matrice di copertura.
    - `quiz.py`: creazione varianti (`genera`) e reportistica statistica (`correggi`).
    - `test_quiz.py`, `test_livelli.py`: test di regressione delle utility.
    - `requirements.txt`: dipendenze Python (`openpyxl`).
- `installa-verifiche-mat-fis.sh`: script bash/python per installare o aggiornare la skill nei path utente standard (`~/.claude/skills`, `~/.codex/skills`, `~/.config/opencode/skills`, `~/.agents/skills`) o creare il pacchetto `--plugin`.
- `README.md`: documentazione utente e panoramica della skill.

## Ambiente e Comandi di Sviluppo

- **Installazione dipendenze Python**:
  ```bash
  python3 -m pip install -r verifiche-mat-fis/requirements.txt
  ```
- **Esecuzione test**:
  ```bash
  python3 verifiche-mat-fis/scripts/test_livelli.py
  python3 verifiche-mat-fis/scripts/test_quiz.py
  ```
- **Validazione registri Excel**:
  ```bash
  python3 verifiche-mat-fis/scripts/registro_xlsx.py check percorso/registro_evidenze.xlsx
  ```
- **Compilazione LaTeX**:
  - Motore predefinito: `pdflatex` (due passate per riferimenti e paginazione).
  - OpenDyslexic / font dedicati: `xelatex` o `lualatex` con `fontspec`.
  - Pacchetti richiesti: `exam`, `newpxtext`, `newpxmath`, `siunitx`, `physics`, `tcolorbox`, `tikz`.

## Convenzioni di Codice e Contenuto

- **Lingua**: la documentazione, i messaggi di commit, le guide e le interazioni con i docenti sono rigorosamente in lingua italiana, chiari, diretti e privi di riempitivi.
- **Python**: conformità a PEP 8, rientri a 4 spazi, nomi in `snake_case`, commenti essenziali. Dipendenze minime: privilegiare la libreria standard e `openpyxl`.
- **LaTeX**: seguire il layout definito nei template in `assets/`. Prove studenti rigorosamente anonime (nessuna indicazione di fila o soluzioni), monocromatiche; evidenze colorate e barre punteggio riservate esclusivamente al correttore docente.
- **Evidenze e punteggi**:
  - Tra 1 e 40 evidenze positive con somma totale esattamente uguale a 1000.
  - Livelli di difficoltà obbligatori: 1 (base, 20–25%), 2 (intermedio, con accesso 2A ≥ 30% di L2), 3 (avanzato, 10–20%).
- **Calcoli quantitativi**: ogni passaggio numerico o algebrico deve essere convalidato tramite script Python autonomo prima di essere integrato in tracce o correttori.

## Gestione Git e Privacy

- **Messaggi di commit**: in italiano, in forma imperativa breve (es. `Aggiungi supporto a ...`, `Correggi validazione ...`).
- **Privacy e Dati Personali**: mai versionare né registrare dati sensibili o nomi reali di studenti.
- **Sorgente unica**: modificare sempre i file all'interno di `verifiche-mat-fis/`. Eventuali pacchetti plugin o zip distributivi devono essere generati solo tramite `installa-verifiche-mat-fis.sh --plugin`.
