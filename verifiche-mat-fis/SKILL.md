---
name: verifiche-mat-fis
description: Progetta e corregge prove scritte di matematica, fisica e laboratorio di fisica per la scuola secondaria di secondo grado (classi 1ª–5ª). Usala quando un docente chiede una verifica o un compito in classe, varianti Fila A/B, un recupero, prove adattate per BES, DSA o tempi ridotti, un correttore con evidenze e punteggi su 1000, griglie ANA/SVI/ARG/COM (o, su richiesta esplicita, le griglie della seconda prova d'esame di matematica, fisica o mista), il registro Excel delle evidenze, lo svolgimento per gli studenti, la compilazione LaTeX/PDF, un quiz a scelta multipla con varianti e correzione statistica, la correzione di elaborati scansionati o fotografati con scheda per alunno, voto in decimi, riepilogo Excel, correttore Excel con colonna per alunno e fascicolo stampabile, la scrittura delle domande di un quiz (file Excel) e la banca delle domande, statistiche oggettive (per evidenza, domanda, distrattore, indicatore, argomento, affidabilità), l'importazione di punteggi anonimi, lo storico e il report di classe, la cartella numerata di ogni prova, oppure lo stato, il confronto o la copertura di versioni già prodotte.
---

# verifiche-mat-fis

Rispondi in italiano, con frasi dirette e concise. Ricava comando, materia e anno dalla richiesta e dal contesto; chiedi soltanto i dati mancanti e riusa preferenze, materiali e approvazioni già acquisiti. I percorsi sono relativi a questa cartella, che è la fonte modificabile (non le esportazioni o gli ZIP). Gli script si eseguono dalla radice della skill e richiedono `openpyxl` (`python -m pip install -r requirements.txt`).

## Comandi

| Comando | Cosa fa | Leggi |
|---|---|---|
| `nuova-verifica` | Scaletta, approvazione, LaTeX e PDF della prova standard | [generatore](references/generatore.md) |
| `varianti` | Versioni derivate, anche per assenti o con esigenze combinate | [generatore §5](references/generatore.md#5-varianti-ordinarie) |
| `recupero` | Prova mirata con griglia NR/PR/R | [generatore §6](references/generatore.md#6-recupero) |
| `correttore` | Evidenze e registro Excel della prova fornita, fino all’approvazione | [correttore](references/correttore.md) |
| `genera-correttore` | Correttore docente dalla revisione approvata; svolgimento studenti solo se richiesto esplicitamente | [correttore §8](references/correttore.md#8-generazione-e-consegna), [latex](references/latex.md) |
| `rigenera-correttore` | Applica modifiche del registro e note del docente | [correttore §9](references/correttore.md#9-rigenerazione) |
| `stato`, `confronta`, `copertura` | Stato delle revisioni, confronto fra registri, matrice di copertura (`scripts/progetto.py`) | [progetto](references/progetto.md) |
| `verifica-calcoli` | Esegue e conserva accanto alla prova script Python che riproducono ogni passaggio quantitativo; confronta risultati, unità, domini e ordini di grandezza | — |
| `cartelle` | Crea la cartella numerata `NN_NOME` di una prova o quiz (sequenza unica, scelta dal docente, default radice) ed elenca la radice (`scripts/cartelle.py`) | [cartelle](references/cartelle.md) |
| `quiz-domande` | Intervista al docente, scaletta approvata e `domande.xlsx` validato per i quiz (`scripts/domande_xlsx.py`) | [quiz_domande](references/quiz_domande.md) |
| `quiz` | Quiz a scelta multipla da Excel: varianti randomizzate con griglia sul foglio, chiavi e PDF | [quiz](references/quiz.md) |
| `correggi-quiz` | Corregge i quiz: fase opzionale di lettura automatica (OpenCV) dei fogli risposte scansionati (variante da QR, risposte proposte con confidenza, nome dal ritaglio), revisione nel browser con `quiz.py rivedi`, poi voti, statistiche per studente, domanda, distrattori e classe | [quiz §4–5](references/quiz.md#4-acquisizione-da-scansioni-facoltativa) |
| `correggi` | Corregge gli elaborati scansionati con il registro approvato: taratura sul primo alunno, scheda PDF per alunno, voti in decimi, riepilogo Excel, fascicolo stampabile (`scripts/correzione.py`, `scripts/fascicolo.py`) | [correzione](references/correzione.md) |
| `statistiche` | Legge e commenta le statistiche di una prova: per evidenza o domanda, distrattore, indicatore, livello, argomento, affidabilità, segnalazioni (`scripts/statistiche.py`) | [statistiche](references/statistiche.md) |
| `importa-punteggi` | Statistiche da punteggi anonimi forniti dal docente (prove: colonna per alunno; quiz: lettere o 1/0) (`scripts/importa.py`) | [statistiche §2](references/statistiche.md#2-importa-punteggi) |
| `chiudi-prova` | Aggiorna `storico.csv/xlsx` e propone le revisioni delle evidenze o domande segnalate | [statistiche §3](references/statistiche.md#3-chiudi-prova-e-report-classe) |
| `report-classe` | Sintesi anonima di classe: indicatori e argomenti deboli, segnalazioni, andamento | [statistiche §3](references/statistiche.md#3-chiudi-prova-e-report-classe) |
| `banca-domande` | Banca delle domande dei quiz con difficoltà misurata; compone un nuovo `domande.xlsx` (`scripts/banca.py`) | [quiz_domande §5](references/quiz_domande.md#5-banca-delle-domande) |
| `compila` | Compila con il motore del preambolo in due passate, verifica dipendenze, PDF e testo estratto | [latex §Compilazione](references/latex.md#compilazione) |
| `aiuto` | Elenca i comandi pertinenti alla richiesta; su domanda produce una sintesi stampabile del flusso | questo file |

## Cartelle

Ogni prova o quiz sta in una cartella `NN_NOME` (`01_VERIFICA_RETTE`, `02_QUIZ_CINEMATICA`...), numerata in progressione sulla radice scelta. **Prima di scrivere qualunque file chiedi al docente in quale cartella lavorare** (default: la radice, cioè la cartella corrente) e creala con `cartelle.py nuova`; i file vanno nelle sue sottocartelle, mai nella cartella della skill. Struttura e privacy in [cartelle](references/cartelle.md).

## Cosa caricare

Non caricare tutti i riferimenti. Identificati materia e anno (se non noti, chiedili prima), leggi soltanto: il file del flusso in corso, [criteri disciplinari](references/criteri_disciplinari.md) e la scheda `references/schede/<materia>_classe<N>.md` (per esempio `matematica_classe3.md`; per il laboratorio la scheda di fisica). Per prove miste leggi solo le schede delle materie coinvolte. La [griglia](references/griglia_valutazione.md) serve per indicatori e fasce, e contiene le griglie d'esame di matematica, fisica e prova mista da usare solo su esplicita richiesta, [latex](references/latex.md) solo per generare o compilare, [cartelle](references/cartelle.md) quando crei o cerchi file, [statistiche](references/statistiche.md) per risultati, importazioni e storico, [supporti](references/supporti_prova.md) quando proponi costanti, formule, formulari o mappe.

Ogni scheda contiene l’elenco predefinito degli argomenti: presentalo come proposta precompilata e lascia al docente la possibilità di selezionare, rimuovere, aggiungere o rinominare voci; una modifica per la singola prova non aggiorna la scheda, salvo richiesta esplicita. L’elenco non attesta che gli argomenti siano stati svolti: per l’anno in corso usa quanto confermato dal docente e chiedi conferma solo dei punti non attestati; per gli anni precedenti usa i contenuti disponibili salvo dubbi specifici.

## Vincoli essenziali

- LaTeX della prova soltanto dopo l’approvazione esplicita della sua scaletta; LaTeX del correttore soltanto dopo l’approvazione esplicita del suo registro. Collega l’approvazione alla revisione precisa nel [progetto](references/progetto.md) con `progetto.py approva`. Il silenzio non approva. Un’approvazione già acquisita resta valida sulla stessa revisione.
- Prima gli standard e le varianti ordinarie, poi le prove adattate con approvazione distinta. Le prove adattate ereditano le scelte approvate; i cambiamenti dello standard richiedono il riallineamento dei derivati interessati.
- Ogni versione ha **da 1 a 40 evidenze complessive**, massimi interi positivi, somma **1000**. Proponi di norma fino a 40 evidenze, senza forzare il massimo. Prima di costruire il registro chiedi la granularità: alta (default per tutta la prova), media o bassa, personalizzabile per esercizio; deroga soltanto se mancano azioni osservabili sufficienti e spiega dove e perché. Ogni evidenza ha un ID progressivo da E01 nell’ordine del registro, esercizio o ambito «Intero elaborato», punto/gruppo, un indicatore ANA/SVI/ARG/COM e una sigla argomento. Le evidenze complessive vanno in fondo; proponi COM complessiva solo dopo aver chiesto al docente e ARG complessiva solo per una ragione specifica, spiegandola. Calibrazione su prestazione Base concreta facoltativa, mai obbligatoria.
- **Griglie d'esame** (matematica, fisica, prova mista) solo su esplicita richiesta del docente, mai per iniziativa dell'agente: indicatori ANA/IND/SVI/ARG o ANA/SVI/DAT/ARG, massimi fissi per indicatore su 1000, `--griglia` in `registro_xlsx.py`, nessun COM. Dettagli in [griglia](references/griglia_valutazione.md#griglie-dellesame-di-stato-solo-su-richiesta-esplicita).
- Ogni evidenza ha un **livello di difficoltà 1/2/3** (`2A` = livello 2 di accesso) e il peso per livello dipende dal livello della classe (basso, medio, alto), da chiedere sempre: L1 20–25%, L3 10–20%, accessi almeno 30% di L2. Regole e tabella nei [criteri disciplinari](references/criteri_disciplinari.md#livelli-di-difficoltà-della-richiesta); non valgono per recupero e quiz.
- Per matematica in terza, quarta e quinta, durata **almeno 100 minuti**: formato predefinito di **un problema in 3 o 4 punti e 3 o 4 quesiti singoli senza sottopunti**, modificabile dal docente. Se i punti del problema dipendono fra loro, chiedi se fornire risultati intermedi e attendi la scelta, salvo scelta già acquisita. I risultati intermedi concordati e i supporti generali esplicitamente approvati sono le sole eccezioni al divieto di riportare risultati o formule di aiuto; il correttore non li valuta come scelte autonome.
- Proponi sempre costanti e formule utili con un elenco **numerato** e attendi la conferma esplicita delle voci da inserire; usa i nomi delle costanti, non i simboli. Inserisci solo i contenuti confermati dopo `\vfill` e prima degli identificativi studente.
- Chiama **prove adattate** le personalizzazioni per BES, inclusi DSA, e per esigenze di tempo. Chiedi se servono un formulario o una mappa concettuale specifica e concordane i contenuti; mantieni sempre difficoltà, argomenti e profondità dello standard.
- Prove senza soluzioni, titolo, materia o fila nel documento (deroga ai soli quiz: codice variante anonimo, vedi [quiz](references/quiz.md)), monocromatiche, derivate dal [modello canonico](assets/modello_verifica.tex). I colori ANA/SVI/ARG/COM appartengono al correttore docente.
- Compila di norma con `pdflatex`. OpenDyslexic richiede scelta esplicita per il solo testo dei documenti concordati, font verificato e XeLaTeX/LuaLaTeX con `fontspec`. Nessuna sostituzione silenziosa; se non puoi compilare consegna sorgenti e comando effettivo, indicando il limite.
- Non chiedere dati personali degli studenti, salvo i nomi per la correzione di elaborati: restano nella cartella locale del docente, mai nel repository, nei log o nei test. Se una richiesta è ambigua o incoerente, chiarisci solo ciò che impedisce il lavoro.
- Prima della consegna applica `humanizer:humanizer` se disponibile; altrimenti svolgi la stessa revisione manuale: frasi dirette, verbi concreti, niente enfasi, riempitivi o trattini lunghi nella prosa. Conserva formule, dati, criteri, unità e vincoli. Controlla anche il testo estratto dal PDF.
