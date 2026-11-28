# verifiche-mat-fis

Skill per assistere docenti della scuola secondaria di secondo grado (in particolare del liceo scientifico) nella progettazione, stesura e correzione di verifiche scritte di matematica, fisica e laboratorio di fisica.

Supporta la creazione di verifiche standard, varianti di fila (Fila A/B), prove di recupero con griglia dedicata, prove adattate (BES/DSA e tempi ridotti), correttori con evidenze e punteggi su scala 1000, generazione di sorgenti LaTeX e registri Excel.

## Requisiti

- Un ambiente compatibile con le skill di agenti (Claude, Codex, OpenCode, Antigravity, ecc.).
- Python 3.9+ con il modulo `openpyxl`:
  ```bash
  python3 -m pip install -r verifiche-mat-fis/requirements.txt
  ```
- Una distribuzione LaTeX (come TeX Live) con `pdflatex` (oppure `xelatex`/`lualatex` se si usa OpenDyslexic) e i pacchetti `exam`, `newpxtext`, `newpxmath`, `siunitx`, `physics`, `tcolorbox`, `tikz`.

## Installazione

Esegui lo script dalla radice del repository:

```bash
./installa-verifiche-mat-fis.sh
```

Senza argomenti, lo script installa o aggiorna la skill nei percorsi standard dell'utente (`~/.claude/skills`, `~/.codex/skills`, `~/.config/opencode/skills`, `~/.agents/skills`).

Opzioni disponibili:
- `--dest <cartella>`: specifica una cartella di installazione personalizzata.
- `install`: installa solo se la cartella di destinazione e' vuota.
- `update`: aggiorna solo installazioni gia' presenti.
- `--plugin`: prepara il pacchetto plugin e l'archivio ZIP distributivo.

In alternativa puoi copiare la cartella `verifiche-mat-fis/` direttamente nella directory delle skill del tuo assistente.

## Comandi per l'assistente

I comandi seguenti vanno indicati nelle richieste all'assistente (non sono comandi da eseguire nel terminale):

| Comando | Descrizione | Riferimento |
|---|---|---|
| `nuova-verifica` | Prepara la scaletta e la bozza per una nuova prova | [references/generatore.md](verifiche-mat-fis/references/generatore.md) |
| `varianti` | Crea varianti ordinarie equivalenti (Fila A, B, ecc.) | [references/generatore.md](verifiche-mat-fis/references/generatore.md) |
| `recupero` | Genera una prova mirata con griglia di recupero (NR/PR/R) | [references/generatore.md](verifiche-mat-fis/references/generatore.md) |
| `correttore` | Ricava evidenze e compila il registro Excel della prova | [references/correttore.md](verifiche-mat-fis/references/correttore.md) |
| `genera-correttore` | Compila il correttore docente in LaTeX/PDF e lo svolgimento | [references/correttore.md](verifiche-mat-fis/references/correttore.md) |
| `rigenera-correttore`| Aggiorna il correttore recependo modifiche al registro Excel | [references/correttore.md](verifiche-mat-fis/references/correttore.md) |
| `stato`, `confronta`, `copertura` | Gestisce lo stato delle revisioni e la matrice di copertura | [references/progetto.md](verifiche-mat-fis/references/progetto.md) |
| `verifica-calcoli` | Genera ed esegue script Python per verificare tutti i passaggi numerici | - |
| `quiz` | Quiz a scelta multipla da Excel: varianti randomizzate, griglia sul foglio, chiavi | [references/quiz.md](verifiche-mat-fis/references/quiz.md) |
| `correggi-quiz` | Corregge i quiz e produce statistiche (studenti, domande, distrattori, classe, affidabilità) | [references/quiz.md](verifiche-mat-fis/references/quiz.md) |
| `quiz-domande` | Intervista al docente e `domande.xlsx` validato per i quiz | [references/quiz_domande.md](verifiche-mat-fis/references/quiz_domande.md) |
| `cartelle` | Cartella numerata `NN_NOME` per ogni prova o quiz, scelta dal docente | [references/cartelle.md](verifiche-mat-fis/references/cartelle.md) |
| `statistiche`, `importa-punteggi` | Statistiche oggettive per evidenza, domanda, indicatore, argomento; import di punteggi anonimi (una colonna per alunno) | [references/statistiche.md](verifiche-mat-fis/references/statistiche.md) |
| `chiudi-prova`, `report-classe` | Storico delle prove e sintesi anonima di classe | [references/statistiche.md](verifiche-mat-fis/references/statistiche.md#3-chiudi-prova-e-report-classe) |
| `banca-domande` | Banca delle domande con difficoltà misurata | [references/quiz_domande.md](verifiche-mat-fis/references/quiz_domande.md#5-banca-delle-domande) |
| `compila` | Compila i file LaTeX verificando pacchetti e testo estratto | [references/latex.md](verifiche-mat-fis/references/latex.md) |
| `aiuto` | Mostra i comandi pertinenti al contesto | [SKILL.md](verifiche-mat-fis/SKILL.md) |

## Struttura del repository

- `verifiche-mat-fis/SKILL.md`: definizione delle regole, dei vincoli e dei flussi della skill.
- `verifiche-mat-fis/scripts/registro_xlsx.py`: utility per la creazione e validazione del registro evidenze Excel (foglio .xlsx con sfondo scuro `#1C1C1C`, indicatori ANA/SVI/ARG/COM (o, su richiesta, le griglie d'esame con `--griglia`), punteggio totale 1000 e colonne con percentuali per esercizio e complessive).
- `verifiche-mat-fis/scripts/progetto.py`: utility per il tracciamento del ciclo di vita del progetto, delle approvazioni e delle revisioni.
- `verifiche-mat-fis/scripts/quiz.py`: generazione (`genera`), lettura dei fogli scansionati (`leggi`), revisione nel browser delle letture (`rivedi`) e correzione con statistiche (`correggi`) dei quiz a scelta multipla; `test_quiz.py` ne verifica il flusso. Adattato da [multiple-choice-randomizer-latex](https://github.com/giulioleuci/multiple-choice-randomizer-latex) (GPL-3.0).
- `verifiche-mat-fis/assets/`: modelli LaTeX per le prove, i correttori docenti e gli svolgimenti studenti.
- `verifiche-mat-fis/references/`: criteri disciplinari, schede argomenti per classe (1ª–5ª) e guide operative.
- `esempi/`: flussi completi di esempio per ogni comando (prove, registri, correttori, quiz, scansioni di alunni fittizi scritte a mano e correzioni); si rigenerano con `python3 esempi/genera_esempi.py`, mappa in `esempi/README.md`.

## Regole principali di progettazione

- **Processo in due passaggi**: l'assistente genera il sorgente LaTeX solo dopo l'approvazione esplicita della scaletta (per la prova) o del registro (per il correttore).
- **Evidenze e punteggi**: ogni prova include da 1 a 40 evidenze. I punteggi sono numeri interi positivi con somma totale pari a 1000, con qualsiasi granularita' scelta dal docente (non c'e' alcun vincolo che siano multipli di 5).
- **Registro Excel**: include le colonne calcolate `% esercizio` e `% verifica` per mostrare il peso relativo di ciascuna evidenza.
- **Prove adattate**: derivano sempre dalla prova standard approvata, preservando livello di difficolta' e profondita' concettuale.
