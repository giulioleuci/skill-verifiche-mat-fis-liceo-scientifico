# Flusso del generatore

Procedura per `nuova-verifica`, `varianti`, `recupero` e revisioni. La versione stampabile del flusso è [flusso_generatore.tex](flusso_generatore.tex). Le regole comuni sono in [SKILL.md](../../SKILL.md); le responsabilità tipografiche in [regole_agente](regole_agente.md). Non è necessario leggere i riferimenti del correttore per progettare una prova.

## 1. Contesto e scaletta

Identifica comando, materia e anno; leggi solo la scheda corrispondente in questa cartella, la base di materia che essa collega e l'elenco predefinito della materia e classe in `../argomenti/argomenti_<materia>_classe<N>.md`. Per una prova mista leggi soltanto gli elenchi delle materie coinvolte. Presenta subito gli argomenti predefiniti come proposta iniziale, consentendo al docente di confermare, selezionare, rimuovere, aggiungere o rinominare voci; non modificare il file predefinito senza richiesta esplicita. Se materia o anno non sono noti, chiedi prima di caricare l'elenco. Recupera preferenze e fase raggiunta con [stato](../progetto.md). Raccogli solo i parametri mancanti secondo [brainstorming](01_guida_brainstorming.md). Non ripetere approvazioni della stessa revisione.

Usa gli argomenti confermati o personalizzati per costruire la scaletta e associa a ciascuno un ID stabile; non dedurre dall'elenco che il programma sia stato svolto. Per l'anno in corso considera svolti solo gli argomenti attestati dal docente e chiarisci quelli non confermati. Per matematica in terza, quarta e quinta di almeno 100 minuti, proponi di default un problema articolato in 3 o 4 punti e 3 o 4 quesiti singoli senza sottopunti. Adatta argomenti e difficoltà alla classe; il docente può richiedere un'altra struttura. Se i punti del problema dipendono fra loro, chiedi se inserire risultati intermedi per permettere di proseguire e attendi la scelta, salvo preferenza già fornita. Registra quali risultati saranno forniti e in quali punti; non inserirli automaticamente.

Proponi sempre costanti e formule tramite un elenco numerato e chiedi conferma esplicita di quali inserire, secondo i [supporti della prova](supporti_prova.md). In fisica usa il catalogo predefinito completo, con nomi delle costanti; in matematica quarta proponi i valori e le formule trigonometriche pertinenti. Registra contenuti, valori e versioni destinatarie; non ripetere una scelta già esplicita.

Presenta una scaletta con esercizio e punto, obiettivo/ID argomento, livello cognitivo, tempo per richiesta e totale, dipendenze, risultati intermedi e supporti confermati. Proponi prima solo gli standard e le varianti ordinarie; recepisci le modifiche e attendi l'approvazione esplicita della revisione identificata. La prova completa approvata può già essere generata una volta esplicitata anche la scelta sui supporti, senza attendere le prove adattate. Progetta poi le prove adattate richieste secondo [varianti](02_guida_varianti.md), con approvazione distinta.

## 2. Generazione

Deriva il sorgente completo dall'[asset canonico](../../assets/modello_verifica.tex), conservando macro e struttura. Applica i vincoli di [impaginazione](regole_agente.md). La prova contiene solo consegne: nessuna soluzione, svolgimento o risultato anche nei commenti. Fanno eccezione i supporti generali esplicitamente confermati e i risultati intermedi scelti dal docente per i punti dipendenti del problema nel formato precedente; dichiarali come dati disponibili, senza spiegare il procedimento. Riporta queste scelte nel progetto e nel passaggio al correttore. Inserisci il blocco `\supportiprova{...}` dopo `\vfill`, in fondo alle consegne e prima degli identificativi, soltanto se approvato. Per i supporti segui il riferimento dedicato, senza precompilare il template.

Prima della consegna risolvi ogni punto e verifica con Python tutti i passaggi quantitativi. Conserva gli script ripetibili accanto alla prova, riferiti alla versione e con controlli leggibili sui risultati. Non incorporare soluzioni della prova nei supporti; inserisci solo i risultati intermedi concordati. Applica la revisione linguistica di SKILL.md.

Compila con il motore effettivo, controlla PDF, testo, simboli, grafici, numerazione, rimandi e spazio per le risposte. Consegna sorgente e PDF verificato; se mancano dipendenze indica il limite e il comando, senza dichiarare una compilazione non eseguita.

## 3. Varianti e revisione

Per BES, inclusi DSA, e per esigenze di tempo usa la denominazione **prove adattate**. Chiedi se occorrono formulario o mappa concettuale specifici e concordane i contenuti dopo lo standard approvato. Conserva sempre difficoltà, argomenti e profondità.

Per le varianti usa le [regole comuni](02_guida_varianti.md), senza un secondo flusso duplicato. Conserva associazioni tra punti originari e derivati. Registra standard di riferimento, durata, font e revisione in [progetto](../progetto.md).

A ogni modifica riepiloga l'impatto su calcoli, scaletta, registro, livelli, correttore, svolgimento e versioni derivate. Esegui i controlli interessati, aggiorna il confronto e segnala i derivati da riallineare. Se cambia la revisione approvata della scaletta o dei suoi supporti, mostra le modifiche e registra la conferma esplicita della nuova revisione prima del TeX interessato. Per i materiali già approvati e invariati prosegui senza richiedere una conferma ripetuta.
