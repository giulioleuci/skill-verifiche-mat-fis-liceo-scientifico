# Esempi della skill `verifiche-mat-fis`

Un flusso completo per ogni comando e opzione della skill, con i file che la skill produce, quelli che il docente fornisce o modifica e le scansioni (scritte a mano, simulate) degli alunni. Tutti i dati sono fittizi (vedi [LIMITI.md](LIMITI.md)).

**Rigenerare**: dalla radice del repository, `python3 esempi/genera_esempi.py`. Esegue gli script reali della skill e ricompila i sorgenti; si ferma se un comando di `verifiche-mat-fis/SKILL.md` non compare in questa pagina. **Aggiornare** (obbligatorio a ogni modifica della skill): vedi la sezione omonima in `CLAUDE.md`.

## Mappa comando → esempio

| Comando | Cartella e file |
|---|---|
| `nuova-verifica` | `01_matematica_rette/`: `scalette/scaletta_A.md`, `prove/prova_A.tex/.pdf`, `prove/prova_A_testo_estratto.txt`, `calcoli/`; fisica in `03_fisica_urti/prove/` (con supporto concordato); laboratorio in `04_laboratorio_pendolo/traccia_laboratorio.*` |
| `varianti` | `01_matematica_rette/prove/prova_B.*` (assenti, `scalette/scaletta_B.md`); `prove/prova_adattata_tempo.*` (tempo ridotto + formulario); `prove/prova_adattata_DSA_opendyslexic.tex` (solo sorgente, vedi LIMITI) |
| `recupero` | `02_recupero_matematica/recupero_rette.*` (`\grigliarecupero`) |
| `correttore` | `01_matematica_rette/registri/` (`evidenze_*.json` → `registro_*.xlsx`, `check_*.txt`, nota del docente su E05, `registro_A_flat.xlsx` con `--layout flat`, `update_A.txt`); `03_fisica_urti/registri/`; griglie d'esame in `05_griglie_esame/*/registro_evidenze.xlsx` |
| `genera-correttore` | `01_matematica_rette/correttori/correttore_A.*`; `03_fisica_urti/correttori/correttore_fisica.*` (con descrizione dei livelli su richiesta); `05_griglie_esame/*/correttore.*` (`boxind`/`boxdat`, `\tabpuntiesame`); `04_laboratorio_pendolo/griglia_laboratorio.*` (griglia autonoma a cinque voci); `01_matematica_rette/svolgimento/svolgimento_studenti_A.*` (solo su richiesta) |
| `rigenera-correttore` | `01_matematica_rette/registri/evidenze_A_rev1.json` → `evidenze_A.json` (revisione 2: E07 e E18, nota su E05) e `correttori/correttore_A.tex` aggiornato; esito in `confronta_A_rev1_rev2.txt` |
| `stato`, `confronta`, `copertura` | `01_matematica_rette/progetto.json`, `progetto_stato_prima.txt`, `progetto_stato.txt`, `progetto_approvazioni.txt` (approvazioni con `approva`), `registri/confronta_*.txt` (inclusa `--derivazioni` e lettura dei due layout), `progetto/matrice_copertura_A.json`, `progetto/copertura_esito.txt` |
| `verifica-calcoli` | `01_matematica_rette/calcoli/verifica_calcoli.py`, `03_fisica_urti/calcoli/`, `04_laboratorio_pendolo/analisi_pendolo.py`, `05_griglie_esame/calcoli_esami.py` (ognuno con il proprio `esito`) |
| `quiz` | `06_quiz/01_quiz_matematica_scansioni/` (4 varianti, righe alternative, punteggio personalizzato); `06_quiz/02_quiz_fisica_indicatori/` (colonna `Indicatore` e `--pesi`, con scansioni) |
| `correggi-quiz` | `06_quiz/01_quiz_matematica_scansioni/`: `scansioni/` simulate (PDF singoli, PDF fronte-retro, JPG da foto, foglio capovolto, foto ritagliata), letture da rivedere (`proposta` per gomma più nuova risposta e per segno debole, `annullata` con `*`), `quiz_out/risposte_scansioni.xlsx`, `letture/` (immagini raddrizzate e `letture.json`; la revisione fatta in `quiz.py rivedi` è simulata dallo script con le stesse funzioni del server), `anomalie_lettura.txt` (prima della revisione), `--errata -1 --annullata 0 --minimo 0`, colonna `Alternative fisse` (domanda D04), `quiz_risultati.xlsx`, `valutazioni.md` (risposta letta, chiave ed esito per ogni foglio), `quiz_out/statistiche.md` e `quiz_out/statistiche_*.csv` (scritti da `quiz.py correggi`: classe con affidabilità, domande, distrattori); `02_quiz_fisica_indicatori/`: fogli a mano in `scansioni/`, riga aggiunta a mano per un alunno senza scansione, `--soglia`, `valutazioni.md`, `quiz_out/statistiche*` (con `statistiche_indicatori.csv`) |
| `correggi` | `01_matematica_rette/correzione/{A,B}/`: `scansioni/` (scritte a mano, PDF, foto, cartella di foto, JPG numerati), `risultati/` (`correzioni.json`, schede PDF, `riepilogo_voti.xlsx`, `correttore_alunni.xlsx`, `copertina.pdf`, `Schede_complete*.pdf`, `note_correzione.md`) |
| `cartelle` | `08_organizzazione_statistiche/radice/`: cartelle `NN_NOME` create da `cartelle.py nuova` (tipi prova, quiz, importata, sequenza unica), `elenco_cartelle.json`, `02_QUIZ_CINEMATICA/progetto_stato.txt` (`stato` di un quiz) |
| `quiz-domande` | `08_organizzazione_statistiche/domande_cinematica.json` (esito dell'intervista) → `08_organizzazione_statistiche/radice/02_QUIZ_CINEMATICA/domande.xlsx` e `controllo_domande.txt` (`domande_xlsx.py`), varianti in `02_QUIZ_CINEMATICA/varianti/` |
| `statistiche` | `08_organizzazione_statistiche/radice/01_VERIFICA_RETTE/risultati/statistiche*` (prova scritta: evidenze, indicatori, livelli, argomenti, affidabilità), `08_organizzazione_statistiche/radice/03_QUIZ_CINEMATICA_IMPORTATO/risultati/statistiche*` (quiz con distrattori); anche `01_matematica_rette/correzione/*/risultati/statistiche*` e `06_quiz/*/quiz_out/statistiche*` |
| `importa-punteggi` | `08_organizzazione_statistiche/radice/05_VERIFICA_RETTE_IMPORTATA/dati/punteggi_prova.xlsx` (colonne del registro, colonna vuota, una colonna per alunno senza nomi), `03_QUIZ_CINEMATICA_IMPORTATO/dati/` (lettere + riga «Variante» con `--chiavi`), `04_QUIZ_ESITI/dati/` (solo 1/0, senza chiavi: nessun distrattore) |
| `chiudi-prova`, `report-classe` | `08_organizzazione_statistiche/radice/storico.csv`, `storico.xlsx` (con grafico), `*/risultati/chiusura.txt`, `*/risultati/report_classe.md` |
| `banca-domande` | `08_organizzazione_statistiche/radice/_banca/banca.xlsx` (difficoltà misurata) e `06_QUIZ_DALLA_BANCA/domande.xlsx` (`banca.py componi`) |
| `compila` | `genera_esempi.py` (`compila()`: due passate di `pdflatex`, pulizia, testo estratto); sorgente non compilabile e comando effettivo in `LIMITI.md` |
| `aiuto` | `07_aiuto_sintesi_flusso/sintesi_flusso.*` (sintesi stampabile di una pagina) |

## Mappa opzione → esempio

| Opzione | Dove |
|---|---|
| Livelli 1/2/2A/3 e `--classe` | tutti i registri; `check_*.txt` mostra il controllo |
| Griglie d'esame `--griglia matematica\|fisica\|mista` | `05_griglie_esame/{matematica,fisica,mista}/` |
| Laboratorio di fisica (cinque voci) | `04_laboratorio_pendolo/` |
| Prove adattate: tempo, formulario, derivazioni | `01_matematica_rette/` (`scaletta_adattata.md`, `derivazioni_adattata.json`) |
| Quiz con indicatori, `--pesi`, `--soglia` | `06_quiz/02_quiz_fisica_indicatori/` |
| Cartelle numerate, scelta della radice | `08_organizzazione_statistiche/radice/` |
| Importazione dei punteggi: prova (`--formato`), quiz con chiavi, quiz 1/0 | `08_organizzazione_statistiche/radice/{03,04,05}_*/` |
| Più versioni nella correzione | `correzione/A/` e `correzione/B/` (assegnazione descritta in `note_correzione.md`) |

## Ciclo di lavoro dei file

Lo `strumenti/manoscritto.py` (solo per gli esempi) simula la scrittura a mano. I testi delle prove, le evidenze, i correttori e i dati degli alunni fittizi (`correzione/elaborati.py`) sono sorgenti da mantenere; registri, PDF, Excel, scansioni ed esiti dei controlli si riscrivono con `genera_esempi.py`.
