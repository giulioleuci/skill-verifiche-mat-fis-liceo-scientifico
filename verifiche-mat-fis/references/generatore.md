# Generatore di verifiche

Procedura unica per `nuova-verifica` (prova e scaletta), `varianti` (versioni ordinarie derivate), `recupero` (prova mirata con griglia NR/PR/R), prove adattate e revisioni. Leggi questo file, i [criteri disciplinari](criteri_disciplinari.md) e la sola scheda di classe in `schede/`; [supporti della prova](supporti_prova.md) per costanti e formule, [latex](latex.md) quando generi il documento, [progetto](progetto.md) per revisioni e approvazioni. Per progettare una prova non servono i riferimenti del correttore.

## 1. Contesto e parametri

Il docente fornisce materia, anno, argomenti e vincoli già noti. Identifica comando, materia e anno, presenta subito gli argomenti predefiniti della scheda come proposta iniziale e recupera preferenze e fase raggiunta con `stato`. Non ripetere approvazioni della stessa revisione.

Raccogli in un solo gruppo di domande concise soltanto i parametri mancanti: nuclei da verificare o escludere, programma dell’anno già svolto, durata effettiva, difficoltà attesa, struttura e tipi di richieste, strumenti, griglia in calce (competenze, recupero o nessuna). Non proporre un questionario completo quando basta un dato; riusa tutte le risposte già disponibili.

Chiedi se serviranno prove adattate (meno tempo, BES inclusi DSA, esigenze combinate) soltanto se non già chiarito. Annota il bisogno e approfondiscilo dopo l’approvazione dello standard (§7). Non chiedere dati identificativi, diagnosi documentate o nomi degli studenti.

## 2. Scaletta

Usa gli argomenti confermati o personalizzati e associa a ciascuno un ID stabile; non dedurre dall’elenco che il programma sia stato svolto. Adatta argomenti e difficoltà alla classe.

- **Formato di matematica in terza, quarta e quinta** (almeno 100 minuti): usa il formato predefinito di SKILL.md senza chiedere di nuovo la struttura, salvo esigenze diverse del docente.
- **Punti dipendenti**: chiedi se inserire risultati intermedi per permettere di proseguire e attendi la scelta, salvo preferenza già fornita. Registra quali risultati saranno forniti e in quali punti; non inserirli automaticamente.
- **Supporti**: proponi sempre costanti e formule secondo i [supporti della prova](supporti_prova.md) e attendi la scelta esplicita delle voci o il rifiuto; la sola approvazione generica della scaletta non vale come scelta. Registra contenuti, valori e versioni destinatarie; riusa una scelta già espressa per gli stessi contenuti e versioni.

Presenta la scaletta con esercizio e punto, obiettivo/sigla argomento, livello cognitivo, tempo per richiesta e totale, dipendenze, risultati intermedi e supporti confermati. Proponi prima solo gli standard e le varianti ordinarie; recepisci le modifiche e attendi l’approvazione esplicita della revisione identificata, poi registrala nel progetto. Una revisione invariata già approvata non richiede una seconda conferma. La prova completa approvata può essere generata appena esplicitata anche la scelta sui supporti, senza attendere le prove adattate.

## 3. Generazione

Deriva il sorgente completo da [assets/modello_verifica.tex](../assets/modello_verifica.tex), conservando macro e struttura, e applica i vincoli del documento elencati sotto e le regole comuni di [latex](latex.md). La prova contiene solo consegne: nessuna soluzione, svolgimento o risultato, neppure nei commenti. Fanno eccezione i supporti generali esplicitamente confermati e i risultati intermedi scelti dal docente per i punti dipendenti: dichiarali come dati disponibili, senza spiegare il procedimento, e riporta queste scelte nel progetto e nel passaggio al correttore. Inserisci `\supportiprova{...}` dopo `\vfill`, in fondo alle consegne e prima degli identificativi, soltanto se approvato; omettilo se i supporti sono rifiutati. Non precompilare il template con i supporti e non incorporarvi soluzioni.

Prima della consegna risolvi ogni punto e verifica con Python tutti i passaggi quantitativi. Conserva gli script ripetibili accanto alla prova, riferiti alla versione e con controlli leggibili sui risultati. Applica la revisione linguistica di SKILL.md.

Compila con il motore effettivo e controlla PDF, testo, simboli, grafici, numerazione, rimandi e spazio per le risposte. Consegna sorgente e PDF verificato; se mancano dipendenze indica il limite e il comando, senza dichiarare una compilazione non eseguita.

### Vincoli del documento

1. **Zero soluzioni**: vietato inserire soluzioni, svolgimenti o risultati numerici nel testo o nei commenti; il documento è pronto da fotocopiare. Fanno eccezione i supporti generali esplicitamente confermati ([supporti](supporti_prova.md)) e i risultati intermedi concordati per i punti dipendenti, senza procedimento.
2. **Nessuna intestazione o metadato superfluo**: mai materia, titolo della verifica o fila, né in intestazione né nel corpo né nel piè di pagina. I comandi di testata restano vuoti: `\firstpageheader{}{}{}` e `\runningheader{}{}{}`.
3. **Identificativi studente** (`Cognome e Nome`, `Classe`, `Data`) su riga aperta con `\hrulefill`, **senza box o riquadri**.
4. **Tipografia**: Palatino con `newpxtext` e `newpxmath`; OpenDyslexic solo per la versione concordata, secondo [latex](latex.md#compilazione). Tabelle ariose in stile `booktabs`, senza righe verticali; badge compatto `\badgeQ` per la numerazione degli esercizi; sottopunti con lettere in grassetto `\alph{partno})`; box consegne a sfondo tenue (`gray!6`) senza intestazione «Istruzioni». Il box di istruzioni iniziale del modello resta invariato salvo richiesta esplicita.
5. **Solo bianco, nero e grigi** (`gray!30`, `black!75`, `black`…): nessun colore, per una resa omogenea in fotocopia.
6. **Griglie in calce**: in `\grigliacompetenze` la legenda dei giudizi (N, Q, S, D, B, O) sta a destra della tabella, per risparmiare spazio verticale, e la colonna della sufficienza S ha fondo grigio chiaro, come nel modello; in `\grigliarecupero` la legenda è nascosta. Sostituisci o ometti la griglia secondo il tipo di prova concordato.
7. **Grafici TikZ** vettoriali puliti: assi orientati, etichette chiare, griglia di sfondo sottile `gray!30`, curve in nero pieno o tratteggio nero/grigio scuro (`line width=1.2pt`).
8. **Supporti in fondo**: dopo le consegne e fuori da `questions`, `\vfill`, poi `\supportiprova{...}` con il solo contenuto approvato, infine gli identificativi. Blocco monocromatico, non flottante e leggibile; nomi delle costanti, non simboli. Se il docente rifiuta i supporti, ometti il blocco e conserva `\vfill`. Dettagli e catalogo nei [supporti](supporti_prova.md#inserimento-e-allineamento).

## 4. Revisioni

A ogni modifica riepiloga l’impatto su calcoli, scaletta, registro, livelli, correttore, svolgimento e versioni derivate. Esegui i controlli interessati, aggiorna confronto e copertura e segnala i derivati da riallineare. Se cambia la revisione approvata della scaletta o dei suoi supporti, mostra le modifiche e registra la conferma esplicita della nuova revisione prima del TeX interessato. Per i materiali già approvati e invariati prosegui senza chiedere una conferma ripetuta.

## 5. Varianti ordinarie

Valgono anche, per i criteri di derivazione, nel [correttore](correttore.md#7-standard-varianti-e-prove-adattate); le due approvazioni riguardano oggetti distinti: scaletta della prova e registro del correttore.

Prima di proporre la variante, se la finalità non è già chiara, chiedi al docente quale obiettivo ha: per assenti, ridotta per esigenze di tempo, entrambe le cose o un'altra esigenza da specificare. Riusa quanto già esplicitato e chiarisci solo i vincoli mancanti. La finalità guida l'entità delle modifiche e la strategia, che va concordata con il docente.

- **Per assenti**: proponi la massima variazione compatibile con gli stessi obiettivi, argomenti, processi cognitivi, difficoltà e profondità, per rendere la prova distinta dall'originale. Cambia per quanto possibile impostazione, contesti, dati e formulazione dei quesiti, usando anche quesiti equivalenti; non limitarti a sostituire i numeri. Mantieni comparabile la durata, salvo esigenze diverse concordate.
- **Ridotta**: concorda il tempo disponibile e applica i criteri per le prove adattate (§7), limitando le modifiche a quelle necessarie per ridurre il carico e mantenere copertura e profondità.
- **Per assenti e ridotta**: combina la massima variazione didatticamente compatibile con la riduzione del carico e la durata concordata; applica anche il flusso e l'approvazione distinta delle prove adattate (§7).
- **Altra finalità**: concorda il grado di variazione e i vincoli pertinenti in funzione dello scopo.

Per le varianti ordinarie conserva tempi comparabili. Proponi, secondo la finalità, variazione numerica, contesto isomorfo, inversione di dati e incognite, quesiti equivalenti o una combinazione per esercizio. Non presumere che cambiare numeri garantisca equipollenza: risolvi i punti e confronta onere dei calcoli, dipendenze e tempi.

Verifica con Python dati, domini, unità e risultati di ogni versione e conserva gli script accanto alle prove. Usa file e cartelle distinti con identificativi neutri; fila, materia e titolo non compaiono nelle prove stampate. I risultati intermedi seguono l’eccezione concordata. Riusa le scelte sui supporti già confermate per le versioni coperte; per aggiunte o modifiche mostra il nuovo elenco e attendi conferma. Aggiorna valori e risultati in tutte le versioni pertinenti e conserva le associazioni tra punti originari e derivati. Registra standard di riferimento, durata, font e revisione nel progetto.

## 6. Recupero

Seleziona con il docente i nuclei da recuperare e isola i passaggi che rendono osservabili le lacune. Usa la macro canonica `\grigliarecupero` con una `\linearecupero` per argomento; esiti NR/PR/R e legenda nascosta. Nessuna griglia di contenuto precompilata nel template.

## 7. Prove adattate

Chiama **prove adattate** le personalizzazioni per BES, inclusi DSA, e per esigenze di tempo. Prima completa revisione e approvazione degli standard; solo dopo approfondisci i bisogni mancanti e proponi le prove adattate dalla rispettiva versione approvata, ereditandone metodi, preferenze, stile, criteri e scelte pertinenti. La loro scaletta richiede una conferma distinta; lo standard può già essere generato.

- **Meno tempo**: acquisisci la durata effettiva. Se manca, proponi 15 minuti in meno; con durata ordinaria di 15 minuti o meno chiedi il tempo disponibile.
- **BES, inclusi DSA**: concorda durata, carico, bisogni operativi di lettura, scrittura e calcolo, strumenti e adattamenti indicati dal docente. Non applicare automaticamente la riduzione temporale.
- **Formulario e mappa**: chiedi esplicitamente se servono un formulario specifico, una mappa concettuale specifica, entrambi o nessuno; concorda contenuto e formato secondo i [supporti](supporti_prova.md#prove-adattate) e attendi la conferma esplicita.
- **Dislessia dichiarata**: chiedi esplicitamente se usare OpenDyslexic per il testo e attendi la scelta; applicalo solo al testo delle versioni concordate, con font e motore verificati, senza sostituzioni silenziose. Non dedurre diagnosi dal testo né richiedere documentazione personale.
- **Esigenze combinate**: chiarisci le versioni effettivamente necessarie e lo standard da cui derivarle, senza sommare automaticamente gli adattamenti.

Conserva sempre argomenti verificati, difficoltà e profondità dello standard. Preferisci eliminare pochi sottopunti ripetitivi o ridurre lettura, scrittura e calcoli accessori, mantenendo testi e struttura dove possibile. Non rimuovere l’unica richiesta di un obiettivo. Controlla che i punti rimasti non dipendano da richieste eliminate e aggiorna numerazione e rimandi. Se tempo e obiettivi sono incompatibili, segnala il conflitto e concorda una soluzione prima di generare.

La scaletta della prova adattata specifica versione di origine, durata, richieste mantenute/modificate/eliminate, tempo risparmiato, copertura, font e supporti confermati. Conserva la corrispondenza dei punti e degli ID evidenza fra standard e derivati nel progetto. Usa `confronta` per verificare richieste e pesi e motiva l’equivalenza didattica con il docente: il confronto automatico non la certifica. Quando cambia lo standard segnala i derivati da riallineare e sottoponi di nuovo soltanto le revisioni sostanziali interessate. Non scrivere diagnosi o motivazioni personali nei file per gli studenti.

## Sintesi stampabile

Se il docente chiede il flusso su carta, compila una sintesi LaTeX di una pagina (`article`, A4, 11 pt, `babel` italiano) con i passi: contesto e parametri; standard e formato; supporti numerati; approvazione della scaletta; generazione monocromatica dall’asset; prove adattate con approvazione distinta; calcoli Python, revisione e compilazione; revisioni e riallineamenti.
