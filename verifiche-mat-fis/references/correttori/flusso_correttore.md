# Flusso del correttore

Procedura per `correttore`, `genera-correttore` e `rigenera-correttore`. [01](01_griglia_valutazione.md) contiene griglia e conversioni ufficiali; [02](02_criteri_assegnazione_punteggi.md) costruzione e pesatura; [04](04_template_correttore.md) macro e impaginazione. Il [progetto](../progetto.md) conserva revisioni, approvazioni e collegamenti fra materiali.

## 1. Contesto e risoluzione

Identifica comando, materia e anno dal contesto prima di caricare riferimenti. Leggi [02](02_criteri_assegnazione_punteggi.md), la base di materia, la sola scheda di classe pertinente in questa cartella e l'elenco predefinito corrispondente in `../argomenti/argomenti_<materia>_classe<N>.md`; consulta [03](03_calibrazione_contesto_classe.md) per contesto o taratura da chiarire. Leggi 01 per fasce e conversioni, 04 quando devi generare il documento, non per porre le prime domande. Per prove miste usa soltanto le basi e gli elenchi delle materie coinvolte.

Presenta l'elenco predefinito pertinente come proposta per identificare gli argomenti della verifica; il docente può confermare, selezionare, rimuovere, aggiungere o rinominare voci senza modificare il file predefinito, salvo richiesta esplicita. Acquisisci testo completo della verifica, argomenti con nomi sintetici forniti o confermati dal docente, programma effettivamente svolto, standard di riferimento e preferenze mancanti. L'elenco predefinito non attesta il programma effettivamente svolto: non inventare argomenti né attribuire al docente contenuti non confermati. Accetta testo, PDF o foto; chiarisci subito parti illeggibili, dati incoerenti o richieste ambigue. Riusa metodi e soluzioni del docente. Non richiedere di nuovo preferenze o programma già confermati e non inventare argomenti.

Risolvi ogni punto con metodi consentiti per quella classe. Riproduci tutti i passaggi quantitativi con Python, confrontali con la soluzione e conserva gli script accanto alla prova/versione. Acquisisci anche le costanti, formule, formulari e mappe concettuali effettivamente disponibili secondo i [supporti della prova](../verifiche/supporti_prova.md). Non premiare il richiamo autonomo di ciò che è già fornito e non penalizzare l’uso dei supporti consentiti; valuta le azioni ancora richieste. I risultati intermedi già forniti nel testo sono dati disponibili: non valutarli come scelte autonome. Segui [02](02_criteri_assegnazione_punteggi.md) per uso successivo, confini ANA/SVI/ARG/COM, errori trascinati e descrittori.

## 2. Registro prima del LaTeX

Costruisci le evidenze dalla soluzione reale, con da 1 a 40 evidenze per versione e totale 1000. Mostra la proposta e i riepiloghi per esercizio, indicatore e ID argomento. Offri la calibrazione Base concreta solo come controllo facoltativo.

Genera inizialmente soltanto `registro_evidenze.xlsx`, con le colonne nell'ordine seguente:

`ID evidenza`, `Esercizio`, `Punto/gruppo`, `Indicatore`, `ID Argomento`, `Max`, `Descrizione evidenza`, `Nome completo argomento`, `Note utente`.

Un'unica riga per evidenza; `Note utente` inizialmente vuota. ID evidenza stabile rispetto a ordine, peso e descrizione; ID argomento distinto dal nome esteso e associato univocamente all'elenco del docente. Accorpamenti e separazioni restano registrati come derivazioni fra ID nel progetto. Dettagli dati e controlli in [progetto](../progetto.md).

Dalla radice della skill, usa `python scripts/registro_xlsx.py write evidenze.json percorso/registro_evidenze.xlsx` per creare il registro, `python scripts/registro_xlsx.py check percorso/registro_evidenze.xlsx` per verificarlo e `python scripts/registro_xlsx.py update evidenze.json percorso/registro_evidenze.xlsx` soltanto per aggiornarlo esplicitamente. Lo script richiede `openpyxl`. `write` rifiuta file esistenti; `update` conserva le note per ID e rifiuta eliminazioni di evidenze annotate. Gli input sono validati prima della sostituzione atomica del file; uno schema vecchio è rifiutato esplicitamente. Non aggirare gli errori riscrivendo il registro a mano.

Attendi revisione e conferma esplicita del docente sulla revisione precisa. Il docente può modificare campi e `Note utente`; dopo la sua conferma rileggi il file e usa `check`, non la proposta originaria. Errori, campi mancanti, associazioni incoerenti, massimi non interi/positivi, totale diverso da 1000 o conteggio fuori 1–40 impediscono il LaTeX. Proponi correzioni, aggiorna esplicitamente conservando note e richiedi approvazione della nuova revisione; poi rileggi e controlla. Non chiedere una seconda approvazione di un registro invariato già approvato. Registra l'approvazione con l'impronta del file in [progetto](../progetto.md).

Chiedi esplicitamente se il docente vuole inserire nel correttore la descrizione scritta dei livelli osservabili. Per impostazione predefinita non inserirla; aggiungila solo se il docente la richiede e registra la scelta per la versione. La scelta riguarda la presenza dei livelli nel documento, non i criteri interni usati per costruire le evidenze.

## 3. Standard, varianti e prove adattate

Anche se ricevi tutte le versioni insieme, revisiona e fai approvare prima i registri standard e delle varianti ordinarie. Solo dopo approfondisci gli adattamenti e prepara i registri delle prove adattate dalla revisione approvata, ereditando metodi, criteri, preferenze e stile pertinenti. I registri delle prove adattate richiedono una conferma successiva distinta. Una conferma può coprire più registri identificati della stessa fase; non standard e prove adattate insieme. Lo standard può già essere generato senza attendere le prove adattate.

Applica i [criteri comuni per varianti e prove adattate](../verifiche/02_guida_varianti.md). Segui il testo ricevuto senza riscriverlo autonomamente: mantieni sempre gli stessi argomenti verificati, difficoltà e profondità dello standard; se il testo ricevuto non li rispetta, segnala il conflitto e chiedi come riallinearli prima di procedere. Confronta punti mantenuti/modificati/assenti, escludi evidenze di richieste eliminate e ricalibra a 1000 per ogni versione. Non penalizzare misure dispensative o attività non richieste; segnala l'effetto degli strumenti compensativi sulle azioni osservabili. Il confronto automatico non certifica l'equivalenza didattica.

Usa cartelle distinte per versione, ciascuna con registro, correttore e svolgimento, senza sovrascrivere altre versioni. Mantieni gli ID delle evidenze corrispondenti, registra accorpamenti/separazioni e conserva l'associazione fra punti. Per BES, inclusi DSA, usa la denominazione prove adattate e chiedi se sono richiesti un formulario o una mappa concettuale specifici; concorda i contenuti senza modificare difficoltà, argomenti e profondità. Per dislessia dichiarata chiedi, se non già deciso, la scelta di OpenDyslexic per il solo testo dello svolgimento studenti; attendi la risposta e verifica motore/font. Il correttore docente conserva il motore ordinario.

## 4. Generazione e consegna

Per le sole revisioni approvate, rileggi e valida il registro. Applica note, pesi e criteri a tutte le sezioni del correttore e dello svolgimento; inserisci la descrizione scritta dei livelli nel correttore solo se esplicitamente richiesta, altrimenti omettila. Non modificare silenziosamente la revisione approvata. Genera dai [template canonici](04_template_correttore.md) `correttore.tex` e `svolgimento_studenti.tex`, quindi i rispettivi PDF. Correttore completo e versione studenti coprono ogni richiesta valutata; gli studenti non ricevono metadati valutativi, livelli o errori tipici.

IMPORTANTE: genera lo `svolgimento_studenti.tex` solo se esplicitamente richiesto dall'utente; ricorda all'utente di chiedere di generarlo, ma di default NON verrà generato.

Allinea la [matrice di copertura](../progetto.md): ogni richiesta si collega alle evidenze pertinenti e ai passaggi che la spiegano. Risolvi richieste senza valutazione, evidenze senza richiesta e valutazioni non coperte dallo svolgimento. Il controllo dei riferimenti non sostituisce la verifica didattica del contenuto.

Applica la revisione linguistica comune in [SKILL.md](../../SKILL.md), esegui la [checklist](02_criteri_assegnazione_punteggi.md), compila due volte e controlla PDF e testo estratto. In assenza di motore o font consegna i sorgenti e il comando effettivo, indicando il limite. In chat basta il riepilogo dei file, dei totali per indicatore, delle preferenze applicate e degli eventuali punti aperti. Altri formati soltanto se richiesti.

## 5. Rigenerazione

Rileggi il registro aggiornato dal docente, controlla la revisione e applica le note. Riepiloga documenti e controlli interessati: calcoli, registro, descrittori, correttore, svolgimento, copertura e versioni derivate. Ricalcola tutte le quadrature e ripeti solo i controlli pertinenti alle modifiche. Se cambia lo standard, il progetto segnala i derivati da riallineare; propaga le modifiche pertinenti e fai approvare i cambiamenti sostanziali dei loro registri prima dei rispettivi documenti. Non riusare un'approvazione riferita a un'impronta precedente.
