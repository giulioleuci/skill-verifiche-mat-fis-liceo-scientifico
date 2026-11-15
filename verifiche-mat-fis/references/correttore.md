# Correttore

Procedura unica per `correttore` (evidenze e registro Excel della prova fornita), `genera-correttore` (documenti delle sole revisioni approvate) e `rigenera-correttore` (modifiche del registro e note del docente). Leggi questo file, i [criteri disciplinari](criteri_disciplinari.md) e la sola scheda di classe in `schede/`. Gli altri riferimenti servono solo nella fase indicata: [griglia ufficiale](griglia_valutazione.md) per fasce e conversioni, [latex](latex.md) per regole comuni e compilazione, [progetto](progetto.md) per revisioni, ID, note, approvazioni e collegamenti fra materiali, [supporti della prova](supporti_prova.md) per costanti, formule, formulari e mappe.

## 1. Contesto e risoluzione

Identifica comando, materia e anno dal contesto prima di caricare riferimenti; per prove miste usa soltanto le schede delle materie coinvolte. Riusa preferenze e programma già confermati, senza riproporre il questionario completo delle preferenze.

1. Identifica materia, anno, indirizzo e tipo di prova: scritto o laboratorio.
2. Acquisisci il testo completo della verifica (testo, PDF o foto) e gli argomenti con nomi sintetici forniti o confermati dal docente, partendo dall’elenco predefinito della scheda come proposta. Chiarisci subito parti illeggibili, dati incoerenti o richieste ambigue.
3. Conferma sempre quali contenuti dell’anno in corso sono stati svolti; per gli anni precedenti usali senza nuova conferma, salvo dubbi specifici. L’elenco predefinito non attesta il programma svolto: non inventare argomenti né attribuire al docente contenuti non confermati.
4. Acquisisci standard di riferimento, eventuali pesi imposti, soluzione del docente, metodi richiesti o esclusi, adattamenti concordati pertinenti e preferenze mancanti. Riusa metodi e soluzioni del docente.
5. Chiedi soltanto se necessari durata, livello della classe, strumenti ulteriori rispetto alla calcolatrice sempre disponibile e vincoli della singola prova.

Non fissare durata, livello, programma svolto o percentuali come valori automatici. Riassumi il contesto e prosegui soltanto sulle parti che non dipendono da informazioni ancora da chiarire.

Risolvi ogni punto con metodi consentiti per quella classe. Riproduci tutti i passaggi quantitativi con Python, confrontali con la soluzione e conserva gli script accanto alla prova/versione. Acquisisci costanti, formule, formulari e mappe concettuali effettivamente disponibili: non premiare il richiamo autonomo di ciò che è già fornito e non penalizzare l’uso dei supporti consentiti; valuta le azioni ancora richieste. I risultati intermedi già forniti nel testo sono dati disponibili: non valutarli come scelte autonome.

## 2. Costruzione delle evidenze

Applica la griglia ufficiale alla soluzione concreta, con i confini degli indicatori dei criteri disciplinari. Non imporre i quattro indicatori in ogni punto. Prevedi ANA per scelte autonome osservabili; non assegnarla a formule o risultati intermedi già forniti, né a procedure abituali prive di scelta distinta: il loro uso successivo può essere valutato secondo ciò che lo studente deve effettivamente fare. Motiva l’assenza di ANA quando altrimenti attesa.

Risolvi integralmente ogni richiesta con il programma confermato e i metodi del docente. Ricava passaggi osservabili specifici per ogni punto/gruppo, senza aggiungere richieste.

**Granularità.** Prima di costruire le evidenze chiedi al docente la granularità: alta (default per tutta la prova), media o bassa; accetta personalizzazioni per singolo esercizio. Accorpa solo azioni compatibili dello stesso esercizio, indicatore e argomento, e solo quando la percentuale di completamento del passaggio è facilmente identificabile; nel dubbio lascia separato. Un gruppo specifica esattamente quali punti comprende. Se le azioni osservabili non bastano per applicare la scelta in un esercizio, non inventare azioni né accorpare azioni eterogenee: usa la granularità più vicina applicabile e spiega al docente dove e perché hai derogato.

| Granularità | Costruzione e obiettivo descrittivo |
|---|---|
| Alta (default) | Evidenze strette; accoppia al massimo due azioni e soltanto calcoli simili. Descrivi soprattutto se l’azione è stata svolta o non svolta. |
| Media | Accorpa più azioni simili o dello stesso dominio, se omogenee. Descrivi se sono state svolte tutte, parzialmente o non svolte. |
| Bassa | Accorpa più azioni, anche numerose, solo se sufficientemente simili e omogenee. Descrivi se sono state svolte tutte, abbastanza, poco o non svolte. |

Esempi: ad alta granularità si possono accoppiare la risoluzione di due equazioni dello stesso tipo, non la scelta del modello e l’interpretazione del risultato; a media granularità si possono valutare insieme tre calcoli omogenei di cinematica, distinguendo riuscita completa, parziale e assente; a bassa granularità si possono riunire cinque applicazioni dello stesso procedimento, distinguendo tutte, abbastanza (per esempio 3–4), poco (1–2) e nessuna. Adatta le soglie al numero di azioni e alla loro importanza, senza intervalli meccanici. La granularità governa ampiezza e descrizione dell’evidenza, non fasce e percentuali della griglia.

**Strategie alternative.** Quando esistono più strategie valide, individua azioni e risultati equivalenti prima di pesare. Distribuisci criteri e massimi in modo che percorsi diversi, se corretti, ottengano punteggi analoghi; esplicita nel correttore le alternative ammesse e non imporre una sequenza esclusiva.

**Strutture di evidenze standardizzate.** Applica sempre le preferenze disciplinari consolidate ([criteri disciplinari](criteri_disciplinari.md)):
- *Geometria analitica (intersezioni):* in ARG valuta la descrizione esplicita che «intersezione = sistema», associando ciascuna equazione al rispettivo luogo geometrico.
- *Studio di funzione (tutte le classi):* valuta prioritariamente la coerenza interna tra risultati e grafici. Dominio: impostare TUTTE le condizioni (anche ridondanti) è ANA; calcoli SVI; rappresentazione cartesiana COM; mostrare il risultato come unione di intervalli è COM solo in quinta. Segno e intersezioni assi: impostazione equazioni, disequazioni e sistemi in ANA (peso ridotto); calcoli in SVI; rappresentazione cartesiana in COM. Punti stazionari: derivate e porle $=0$ in ANA; calcoli in SVI. Monotonia: derivate e studio del segno in ANA; calcoli in SVI; grafico con segni $+/- /0$ della derivata prima, frecce e scritte $\max/\min/\text{flesso}$ in ANA. Concavità e flessi: analoghi con derivata seconda (derivata seconda $=0$ per candidati flessi in ANA, calcoli SVI; studio segno derivata seconda in ANA, calcoli SVI; grafico con segni $+/- /0$ della derivata seconda, concavità e scritte flesso in ANA).
- *Problemi fisici con vettori (cinematica, statica, dinamica, quantità di moto, campo elettrico...):* sequenza standard in 7 passi: 1. Rappresentazione situazione in COM (se non fornita); 2. Rappresentazione di tutti i vettori in COM (peso proporzionale a quanti elementi disegnare/forniti); 3. Scelta del sistema di riferimento in ANA (con freccia circolare e segno $+/-$ per rotazioni perpendicolari); 4. Scomposizione grafica dei vettori sugli assi in COM; 5. Scrittura equazioni per asse: ANA per la scelta corretta dei vettori, SVI per i segni algebrici giusti ($+/-$); 6. Risoluzione algebrica in SVI; 7. Eventuale interpretazione del risultato in ARG (es. segno dell'accelerazione).

**Numero, campi e ordine.** Ogni versione ha da 1 a 40 evidenze complessive, massimi interi positivi (qualsiasi granularità), totale 1000. Proponi di norma fino a 40 evidenze, senza raggiungere il tetto se la prova non lo giustifica. Le evidenze riferite agli esercizi conservano l’associazione a esercizio e argomento e vengono prima; le eventuali evidenze complessive vanno in fondo, con `Intero elaborato` in `Esercizio` e `Punto/gruppo`, sigla riservata `TRASVERSALE` e nome `Competenze trasversali`, senza associarle a un punto della prova. Proponi COM complessiva solo dopo aver chiesto al docente se la desidera; ARG complessiva non è proposta di default, ma può esserlo per una ragione specifica da spiegare e sottoporre al docente.

**ID e sigle.** ID consecutivi da `E01` nell’ordine delle righe. Dopo inserimenti, eliminazioni o riordini rinumera l’intero registro; conserva nel [progetto](progetto.md) la mappa dalla revisione precedente alla nuova, comprese le derivazioni di accorpamenti e separazioni. Associa note, riferimenti e varianti alle azioni tramite questa mappa, non al numero riutilizzato. Le sigle sono quelle dell’elenco del docente, con associazione stabile e univoca sigla/nome; riporta entrambe in colonne distinte.

## 3. Pesi

Distribuisci i massimi per importanza, difficoltà e tempo delle azioni effettivamente osservabili. I pesi orientativi dei criteri disciplinari e le priorità della scheda non impongono evidenze mancanti; rispetta i limiti per argomento indicati dalle schede.

- Per ogni esercizio o argomento senza grafici e tabelle, COM non supera il 10% del relativo totale, salvo brainstorming e accordo esplicito con il docente.
- Con grafici, distingui le evidenze grafiche da quelle di sola forma: il grafico pesa nettamente più di notazione, unità e sequenza delle formule dello stesso esercizio; se serve riserva a questi aspetti una piccola parte del COM dell’esercizio, orientativamente il 20%. Ogni grafico riceve un peso motivato dalla sua richiesta; non imporre confronti fra i COM di esercizi diversi, così più esercizi grafici possono coesistere.
- Riduci o rimuovi ARG quando le argomentazioni sono poche, assenti o estremamente banali.
- Il peso di SVI rispetto alla sola traduzione ANA cresce con la difficoltà del calcolo nell’anno (tabella nei criteri disciplinari) e con la complessità del problema. A difficoltà 1–2 il calcolo pesa poco e ANA può pesare quanto SVI, più o molto di più; a 3 SVI pesa più della sola traduzione; a 4 riceve il peso maggiore; a 0 il contenuto non è utilizzabile senza averne chiarito il programma. Considera il metodo realmente svolto: può rendere il calcolo più semplice.
- Una sostituzione numerica in formule già valutate ha peso basso; accorpala alla derivazione quando compatibile. Accorpa derivazioni consecutive della stessa catena, con stesso esercizio, indicatore e argomento; non premiare due volte una derivazione già svolta. Le sole sostituzioni restano con i calcoli del medesimo tipo, distinte dalla soluzione di condizioni nuove.

## 4. Livelli osservabili

Titoli, svolgimenti e livelli descrivono ciò che lo studente scrive, calcola, rappresenta o giustifica, con verbi alla terza persona singolare. Lo svolgimento docente è completo: dati, impostazione, formule, passaggi letterali e numerici, condizioni, unità, deduzioni e risultati; un passaggio per voce numerata.

Ogni evidenza ha da tre a cinque descrizioni concrete: **non raggiunto, base e avanzato obbligatori**; iniziale e intermedio solo per azioni complesse, articolate o composte da più parti, anche separatamente. Mantieni fasce e percentuali assegnabili della griglia: la descrizione binaria o graduata orienta la lettura delle prestazioni, non elimina fasce né impone percentuali; i livelli omessi non modificano fasce o percentuali. Nelle evidenze composte nomina la parte specifica solo quando essenziale, altrimenti descrivi quante parti sono riuscite. I livelli possono richiamare i numeri dei propri passaggi, indicando riuscita ed errori osservati.

Ogni livello è autonomo, senza confronti con il precedente. Sotto l’avanzato descrivi nella stessa frase anche ciò che ancora manca, senza etichette aggiuntive; nell’avanzato soltanto le azioni svolte. Non dedurre aiuti dalla prestazione: citali solo se documentati. La piena riuscita di una consegna semplice vale 100%, senza originalità o prestazioni fuori consegna.

## 5. Valutazione ed errori

Punti ottenuti = massimo × percentuale / 100. Le percentuali delle evidenze sono indipendenti, restano 0–100 e non devono sommare a 100. Aggrega con somma ottenuti / somma massimi, conservando i decimali fino all’arrotondamento finale della griglia. Nessuna quota interna agli indicatori, percentuale negativa o detrazione duplicata.

Penalizza l’errore nell’evidenza in cui nasce. I passaggi successivi coerenti con il dato errato possono ottenere il massimo se plausibili e di difficoltà equivalente. Valuta separatamente nuovi errori indipendenti e controlli richiesti omessi. Se l’errore semplifica il seguito, motiva quale sviluppo resta osservabile. Le disposizioni generali della griglia restano separate.

ARG valuta giustificazioni indispensabili e non banali, senza numero fisso per esercizio o frasi finali di routine. Accetta una frase breve, formula commentata, freccia annotata o disegno con didascalia equivalente. Giustificazione assente: zero nella relativa evidenza ARG, senza ridurre di nuovo ANA/SVI. Controlli di plausibilità soltanto se evidenti e significativi.

COM valuta lo stesso errore ripetuto una volta per evidenza; nessuna detrazione per occorrenza. Richiedi gli argomenti degli operatori anche nei passaggi intermedi. Se un simbolo ambiguo esprime un errore concettuale, assegnalo al contenuto pertinente senza duplicarlo in COM. Formula diretta, derivazione letterale, sostituzione finale e unità seguono i criteri disciplinari.

## 6. Registro Excel prima del LaTeX

Mostra la proposta con i riepiloghi per esercizio, indicatore e sigla argomento; offri la calibrazione Base solo come controllo facoltativo (§10). Genera inizialmente soltanto `registro_evidenze.xlsx`, una riga per evidenza, con questi campi logici:

`ID evidenza`, `Esercizio`, `Punto/gruppo`, `Indicatore`, `Sigla argomento`, `Max`, `% esercizio`, `% verifica`, `Descrizione evidenza`, `Nome completo argomento`, `Note utente`.

Le colonne `% esercizio` e `% verifica` sono calcolate dallo script e non fanno parte dello schema JSON: mostrano, per ogni evidenza, la percentuale del suo `Max` rispetto al totale dell'esercizio e rispetto al totale della verifica (1000), arrotondate all'intero più vicino. Sono puramente indicative: la somma delle percentuali può non fare 100.

`Note utente` è inizialmente vuota. Le due colonne percentuale (`% esercizio`, `% verifica`) sono inserite dallo script tra `Max` e `Descrizione evidenza` e non vanno incluse nel JSON. Il formato predefinito (`merged`) unisce la cella `Descrizione evidenza` su quattro colonne contigue (I:L, dopo lo spostamento delle percentuali) e sposta a destra i campi successivi; non chiedere se applicarlo. Usa `--layout flat` soltanto se il docente chiede esplicitamente un foglio senza celle unite, senza proporgli di scegliere. `check`, `update` e `progetto.py` leggono sia i registri nuovi (con colonne percentuale) sia quelli vecchi (senza); `update` salva nel layout indicato, `merged` per default. Stile applicato dallo script: fondo carbone `#1C1C1C` in tutte le celle, comprese vuote e unite, senza fondo di input perché il registro non contrassegna campi d’inserimento; intestazioni bianche in grassetto, testo `#E0E0E0`, Open Sans 8 pt, Inconsolata 8 pt per `Max` e per le colonne percentuale, linee `#222222`, testo a capo, colonne larghe al massimo 20 caratteri.

Dalla radice della skill (richiede `openpyxl`):

| Comando | Effetto |
|---|---|
| `python scripts/registro_xlsx.py write evidenze.json percorso/registro_evidenze.xlsx` | Crea il registro; rifiuta destinazioni esistenti. |
| `python scripts/registro_xlsx.py check percorso/registro_evidenze.xlsx` | Valida schema, campi e totale e stampa i riepiloghi per esercizio, indicatore e sigla argomento. |
| `python scripts/registro_xlsx.py update evidenze.json percorso/registro_evidenze.xlsx` | Solo per aggiornamenti espliciti: conserva le note per ID e rifiuta eliminazioni di evidenze annotate o note in conflitto. |

Gli input sono validati prima della sostituzione atomica del file; i formati non riconosciuti sono rifiutati. Non aggirare gli errori riscrivendo il registro a mano. Se una rinumerazione cambia il significato di un ID annotato, non usare `update`: conserva il registro precedente, associa le note alle azioni tramite la mappa delle revisioni, crea un nuovo registro con `write` e controlla a mano note e riferimenti.

Attendi revisione e conferma esplicita del docente sulla revisione precisa. Il docente può modificare campi e `Note utente`; dopo la conferma rileggi il file e usa `check`, non la proposta originaria. Errori, campi mancanti, associazioni incoerenti, massimi non interi o non positivi, totale diverso da 1000 o conteggio fuori 1–40 impediscono il LaTeX: proponi correzioni, aggiorna esplicitamente conservando le note, chiedi l’approvazione della nuova revisione, poi rileggi e controlla. Non chiedere una seconda approvazione di un registro invariato già approvato. Registra l’approvazione con l’impronta del file tramite `progetto.py approva` ([progetto](progetto.md)).

Chiedi esplicitamente se il docente vuole nel correttore la descrizione scritta dei livelli osservabili. Per impostazione predefinita non inserirla; aggiungila solo su richiesta e registra la scelta per la versione. La scelta riguarda la presenza dei livelli nel documento, non i criteri interni usati per costruire le evidenze.

## 7. Standard, varianti e prove adattate

Anche se ricevi tutte le versioni insieme, fai revisionare e approvare prima i registri standard e delle varianti ordinarie. Solo dopo approfondisci gli adattamenti e prepara i registri delle prove adattate dalla revisione approvata, ereditando metodi, criteri, preferenze e stile pertinenti; richiedono una conferma successiva distinta. Una conferma può coprire più registri identificati della stessa fase, mai standard e prove adattate insieme. Lo standard può già essere generato senza attendere le prove adattate.

Applica i criteri comuni per [varianti e prove adattate](generatore.md#5-varianti-ordinarie). Segui il testo ricevuto senza riscriverlo: se non mantiene gli stessi argomenti verificati, difficoltà e profondità dello standard, segnala il conflitto e chiedi come riallinearlo prima di procedere. Confronta punti mantenuti, modificati e assenti, escludi le evidenze delle richieste eliminate e ricalibra a 1000 ogni versione. Non penalizzare misure dispensative o attività non richieste; segnala l’effetto degli strumenti compensativi sulle azioni osservabili. Il confronto automatico non certifica l’equivalenza didattica.

Usa cartelle distinte per versione, ciascuna con registro, correttore ed eventuale svolgimento, senza sovrascrivere altre versioni; gli aggiornamenti sono espliciti e non sovrascrivono silenziosamente dati precedenti. Mantieni gli ID delle evidenze corrispondenti, registra accorpamenti e separazioni e conserva l’associazione fra punti. Per BES, inclusi DSA, usa la denominazione prove adattate, acquisisci insieme al testo formulario o mappa concettuale concordati e chiedi se ne servono di specifici, senza modificare difficoltà, argomenti e profondità. Per dislessia dichiarata chiedi, se non già deciso, se usare OpenDyslexic per il solo testo dello svolgimento studenti; attendi la risposta e verifica motore e font. Il correttore docente conserva il motore ordinario.

## 8. Generazione e consegna

Per le sole revisioni approvate rileggi e valida il registro. Applica note, pesi e criteri a tutte le sezioni; inserisci la descrizione dei livelli solo se richiesta. Non modificare silenziosamente la revisione approvata. Genera `correttore.tex` da [assets/correttore_template.tex](../assets/correttore_template.tex) secondo i vincoli sotto e le regole comuni di [latex](latex.md), poi il PDF. Il correttore copre ogni richiesta valutata.

**Svolgimento studenti solo su richiesta esplicita.** Di default non generare `svolgimento_studenti.tex`; ricorda al docente che può chiederlo. Quando richiesto, copre ogni richiesta valutata senza metadati valutativi, livelli o errori tipici, e allinea la [matrice di copertura](progetto.md#matrice-di-copertura): ogni richiesta si collega alle evidenze pertinenti e ai passaggi che la spiegano; risolvi richieste senza valutazione, evidenze senza richiesta e valutazioni non coperte dallo svolgimento. Il controllo dei riferimenti non sostituisce la verifica didattica del contenuto.

Applica la revisione linguistica di SKILL.md, esegui la checklist (§11), compila due volte e controlla PDF e testo estratto. In assenza di motore o font consegna i sorgenti e il comando effettivo, indicando il limite. In chat basta il riepilogo dei file, dei totali per indicatore, delle preferenze applicate e degli eventuali punti aperti. Altri formati soltanto se richiesti.

### Documenti LaTeX

Apri con intestazione sintetica, contesto e legenda dei quattro indicatori, senza una sezione sui parametri di correzione. Riporta il testo della prova nei singoli esercizi. Il registro iniziale raggruppa esercizio e argomento comune, indicando ID evidenza, nome completo dell’azione, punto/gruppo, indicatore e massimo; per gruppi con argomenti diversi esplicita le associazioni. Il nome dell’azione è identico al titolo del suo svolgimento: questa ripetizione è ammessa.

Inserisci soltanto riepiloghi per esercizio, indicatore e argomento, derivati dalle stesse evidenze. Nessun riepilogo per punto/gruppo e nessuna tabella di conversione voto o giudizio, la cui fonte resta la [griglia](griglia_valutazione.md).

Gli esercizi iniziano su una nuova pagina. Ogni evidenza ha una sola intestazione compatta «ID · sigla colorata · azione», passaggi numerati e livelli (solo se richiesti); nel corpo non ripetere esercizio, argomento, massimo o nome completo dell’indicatore. Metadati completi nel sorgente e nel registro, nessun campo per percentuale o punti ottenuti. Alternative, errori e criteri specifici stanno in elenco puntato dopo i livelli dell’evidenza pertinente; ometti la sezione se vuota. Le note condivise stanno dove nasce la scelta o l’errore, con rimandi senza duplicazioni.

| Macro o ambiente | Uso |
|---|---|
| `\evidenza{ID}{esercizio/punto}{indicatore}{argomento}{massimo}` | Registra l’evidenza e l’ID del box successivo; per argomento usa la sigla del registro; specifica i punti del gruppo. |
| `\controllaevidenze` | Conteggio della verifica: da 1 a 40; dalla quarantunesima evidenza produce errore. Non aggirare il controllo. |
| `\livelli{non raggiunto}{iniziale}{base}{intermedio}{avanzato}` | Primo, terzo e quinto argomento obbligatori; secondo e quarto vuoti con `{}` quando non necessari. Le fasce non cambiano. |
| `\sigla{ANA}`, `\indicatore{ANA}` | Colora sigla oppure sigla e nome; analogamente SVI/ARG/COM. Usale per ogni riferimento agli indicatori, anche in tabelle, note e legenda. |
| `boxana`, `boxsvi`, `boxarg`, `boxcom` | Unica intestazione con ID, sigla e azione; all’interno passaggi `enumerate` in terza persona. |
| `\registrogruppo{esercizio}{argomento}{righe}` | Raggruppa metadati comuni, senza perdere l’associazione di ogni evidenza. |
| `\riepiloghi{esercizi/indicatori}{argomenti}` | Affianca i riepiloghi aggregati. |
| `\inizioesercizi`, `\esercizio`, `\punto`, `\tabpunti`, `\sez`, `enun` | Struttura e comandi del template; i massimi rimangono nei riepiloghi. |
| `\criteri{elenco}`, `\nota{testo}` | Note puntate dopo i livelli dell’evidenza interessata. |
| `\ANA{ID}{massimo}` e analoghe | Eventuali chip di riferimento, senza quote interne o detrazioni. |
| `grafico` | Figura nel passaggio pertinente; conserva `figure[h!]` e `\centering`. `[h!]` non garantisce una posizione impossibile: controlla il PDF e adatta dimensioni o pagina. |

I colori rosso/blu/giallo/verde (ANA/SVI/ARG/COM) sono riservati agli indicatori. Nelle figure del correttore usa nero, grigi, arancio o teal. Non introdurre un comando `\arg`, già riservato in LaTeX.

Nella scrittura tecnica parti dalle formule dirette e ricava letteralmente l’incognita, sostituendo i dati alla fine della derivazione pertinente. Una grandezza ormai espressa solo con dati noti si calcola subito con unità e il valore si riusa: vale il massimo. Usa formule composte solo quando più convenienti o richieste. Indica le unità nei risultati intermedi e finali e dichiara la convenzione angolare.

### Svolgimento studenti

Usa [svolgimento_studenti_template.tex](../assets/svolgimento_studenti_template.tex) e organizza esercizi e sottopunti in passi numerati chiari: strategia, formule, condizioni, sviluppi, motivazioni essenziali, grafici, unità e risultati coprono tutto ciò che viene valutato. Un percorso completo lecito basta; non servono tutte le alternative. Gli aspetti condivisi sono spiegati una volta. Nessun punteggio, massimo, percentuale valutativa, indicatore o colore convenzionale, ID evidenza, livello, registro, riepilogo, errore tipico o istruzione al docente.

## 9. Rigenerazione

Rileggi il registro aggiornato dal docente, controlla la revisione e applica le note. Riepiloga documenti e controlli interessati: calcoli, registro, descrittori, correttore, svolgimento, copertura e versioni derivate. Ricalcola tutte le quadrature e ripeti solo i controlli pertinenti alle modifiche. Se cambia lo standard, `stato` segnala i derivati da riallineare: propaga le modifiche pertinenti e fai approvare i cambiamenti sostanziali dei loro registri prima dei rispettivi documenti. Non riusare un’approvazione riferita a un’impronta precedente.

## 10. Calibrazione Base facoltativa

Solo su richiesta, mai come passaggio obbligatorio che blocca il flusso. Simula una prestazione Base concreta e plausibile: quali parti completa, quali errori commette, quali passaggi omette, con percentuali per evidenza coerenti con i descrittori. Calcola la somma ponderata e confrontala con circa 600/1000; annota ipotesi e conseguenze sui pesi e sui livelli. Il 60% uniforme su ogni evidenza produce 600 per costruzione e non dimostra la taratura. La marcatura delle richieste essenziali non impone che i loro massimi sommino al 60%.

## 11. Checklist di consegna

- Testo, contesto e argomenti del docente acquisiti; tutti i punti risolti e calcoli ripetibili conservati.
- Da 1 a 40 evidenze per versione, campi validi, ID consecutivi e mappa delle revisioni, un indicatore e una sigla argomento per evidenza, massimi interi positivi e totale 1000.
- Nessuna duplicazione; riepiloghi per esercizio, indicatore e argomento coerenti; richieste fornite o eliminate escluse dalle scelte autonome valutate.
- Livelli specifici, azioni in terza persona, errore trascinato e alternative pertinenti applicati.
- Se c’è lo svolgimento: matrice di copertura allineata a richieste, evidenze e passaggi; nessuna valutazione o spiegazione mancante.
- Registro della revisione approvata riletto e controllato, note conservate, derivati riallineati e approvazioni distinte rispettate.
- Documenti conformi ai vincoli LaTeX del §8 e di [latex](latex.md), prosa rivista secondo SKILL.md, compilazione e PDF controllati oppure limite dichiarato.
- Calibrazione concreta controllata solo se richiesta.
