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
    - `cartelle.md`: cartelle numerate `NN_NOME` e privacy; `statistiche.md`: statistiche, importazione, storico, report; `quiz_domande.md`: intervista per `domande.xlsx` e banca.
    - `correttore.md`: estrazione evidenze, validazione del registro e correttore LaTeX.
    - `progetto.py` / `progetto.md`: ciclo di vita del progetto, tracciamento versioni e matrici di copertura.
    - `correzione.md`: correzione di elaborati scansionati, schede per alunno, conversione in decimi e riepilogo.
    - `quiz.md`: generazione e correzione dei quiz a scelta multipla con analisi dei distrattori.
    - `latex.md`: preambolo canonico, convenzioni tipografiche e regole di compilazione.
    - `supporti_prova.md`: formule, costanti e formulari ammessi.
    - `schede/`: schede tematiche per materia e classe (`matematica_classe*.md`, `fisica_classe*.md`).
  - `assets/`: template LaTeX canonici:
    - `modello_verifica.tex`: layout della prova per lo studente (senza soluzioni né intestazioni di fila).
    - `correttore_template.tex`: layout del correttore docente (a colori, con riquadri evidenze).
    - `svolgimento_studenti_template.tex`: risoluzione per gli studenti (solo su richiesta esplicita).
    - `scheda_alunno_template.tex`: scheda di correzione per l'alunno, una pagina (✓ verde e ✗ rosso accesi ammessi solo qui).
    - `quiz_template.tex`: foglio quiz anonimo con griglia risposte.
    - `rivedi/`: editor delle letture dei quiz nel browser (`rivedi.html`, `rivedi.ts` e `rivedi.js` compilato: dopo ogni modifica al `.ts` esegui `npx -p typescript tsc -p verifiche-mat-fis/assets/rivedi` e versiona anche il `.js`; nessuna dipendenza a runtime).
  - `scripts/`: utility Python a supporto:
    - `registro_xlsx.py`: generazione, formattazione dark `#1C1C1C`, validazione (`check`) e aggiornamento (`update`) del registro evidenze.
    - `progetto.py`: gestione stati, log revisioni, approvazioni e matrice di copertura.
    - `correzione.py`: punti per evidenza, voto in decimi (passo 0,25, minimo 2) e riepilogo Excel di classe.
    - `fascicolo.py`: copertina e schede unite in `Schede_complete*.pdf` (anche fronte-retro) con pdflatex e pdfpages.
    - `quiz.py`: creazione varianti con foglio risposte a cerchi (`genera`, con `--annullata`, `--minimo` e colonna `Alternative fisse`), lettura delle scansioni con risposte proposte e confidenza (`leggi`), editor nel browser (`rivedi`, server locale con `assets/rivedi/`) e reportistica statistica (`correggi`).
    - `statistiche.py`: statistiche comuni (descrittive, difficoltà, discriminazione, affidabilità, segnalazioni), storico (`chiudi`) e report di classe (`report`).
    - `importa.py`: punteggi anonimi del docente (una colonna per alunno) per prove scritte e quiz.
    - `cartelle.py`: cartelle numerate `NN_NOME` (`nuova`, `elenco`). `banca.py`: banca delle domande. `domande_xlsx.py`: scrittura e controllo di `domande.xlsx`.
    - `test_statistiche.py`: test di regressione di cartelle, statistiche, importazione, banca e domande.
    - `omr.py`: geometria del foglio risposte, TikZ e lettura OpenCV (quadrati di riferimento, QR, riempimento dei cerchi).
    - `test_quiz.py`, `test_livelli.py`, `test_correzione.py`: test di regressione delle utility.
    - `requirements.txt`: dipendenze Python (`openpyxl`, `opencv-python-headless`, `numpy`).
- `esempi/`: flussi completi di esempio per ogni comando e opzione della skill, con alunni fittizi (non fa parte della skill né del pacchetto plugin).
  - `README.md`: mappa comando → cartella/file e opzione → esempio; `LIMITI.md`: limiti noti (font assenti, scansioni simulate).
  - `genera_esempi.py`: rigenera tutto eseguendo gli script reali della skill e compilando i sorgenti; si ferma se un comando di `SKILL.md` manca nel README degli esempi.
  - `01_matematica_rette/` (verifica standard, Fila B per assenti, prova adattata, registri, revisione, stato/confronta/copertura, correttore, svolgimento, correzione `correggi` con scansioni scritte a mano), `02_recupero_matematica/`, `03_fisica_urti/`, `04_laboratorio_pendolo/`, `05_griglie_esame/` (matematica, fisica, mista), `06_quiz/` (con scansioni, con indicatori), `07_aiuto_sintesi_flusso/`, `08_organizzazione_statistiche/` (cartelle `NN_NOME`, domande del quiz, importazione di punteggi anonimi, statistiche, storico, report, banca), `strumenti/manoscritto.py` (simulazione di scrittura a mano, solo per gli esempi).
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
  python3 verifiche-mat-fis/scripts/test_correzione.py
  python3 verifiche-mat-fis/scripts/test_statistiche.py
  ```
- **Rigenerazione degli esempi** (dalla radice, richiede anche `Pillow`, `sympy`, `pdflatex`, `pdftoppm`, `pdfinfo`; `soffice` facoltativo):
  ```bash
  python3 esempi/genera_esempi.py
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

## Esempi (da aggiornare a ogni modifica della skill)

`esempi/` deve coprire **tutte** le operazioni possibili della skill, comprese quelle del docente (modifiche del registro, approvazioni, note) e le scansioni degli alunni (scritte a mano simulate, con errori). Ogni modifica a `verifiche-mat-fis/` richiede, nello stesso commit:

1. **Nuovo comando, opzione o formato** (SKILL.md, script, template): aggiungi o estendi un esempio in `esempi/`, con sorgenti, file generati e riga nelle tabelle di `esempi/README.md`. `genera_esempi.py` fallisce se un comando della tabella di `SKILL.md` non compare nel README degli esempi.
2. **Modifica di template, preambolo LaTeX, schemi (registro, `progetto.json`, `correzioni.json`, chiavi quiz) o regole di valutazione**: aggiorna i sorgenti degli esempi interessati (prove, correttori, evidenze, dati in `correzione/elaborati.py`) perché seguano i nuovi template e le nuove regole.
3. Esegui `python3 esempi/genera_esempi.py` e fai commit anche dei file rigenerati; controlla a vista almeno un PDF e una scheda per le parti toccate.
4. Rimozione o rinomina di un comando: elimina o rinomina il relativo esempio e la riga del README.
5. Solo dati fittizi: nessun nome reale di alunni negli esempi.

## Gestione Git e Privacy

- **Messaggi di commit**: in italiano, in forma imperativa breve (es. `Aggiungi supporto a ...`, `Correggi validazione ...`).
- **Privacy e Dati Personali**: mai versionare né registrare dati sensibili o nomi reali di studenti; la correzione usa nomi solo nelle cartelle locali del docente, i test usano alunni fittizi.
- **Sorgente unica**: modificare sempre i file all'interno di `verifiche-mat-fis/`. Eventuali pacchetti plugin o zip distributivi devono essere generati solo tramite `installa-verifiche-mat-fis.sh --plugin`.
