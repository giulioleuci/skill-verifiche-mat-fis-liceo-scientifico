# Stato, confronto e copertura del progetto

Comandi `stato`, `approva`, `confronta` e `copertura` di `scripts/progetto.py`, da eseguire dalla radice della skill. Lavorano sui materiali della prova, fuori dalla cartella installata della skill. Non sostituiscono la revisione didattica né il consenso del docente. Dipendenza Python: `openpyxl`, dichiarata in [requirements.txt](../requirements.txt). Installarla con `python -m pip install -r requirements.txt` dalla cartella della skill.

## File di progetto

Conservare `progetto.json` accanto alle cartelle delle versioni. Crearlo quando si identificano le versioni; aggiornarlo con le preferenze effettivamente concordate, senza inventare parametri. Schema JSON:

| Campo | Tipo e significato |
|---|---|
| `preferenze` | Oggetto con materia, classe, argomenti, impostazioni concordate, eventuali risultati intermedi, adattamenti e supporti comuni esplicitamente confermati. Non inserire dati personali. |
| `versioni` | Oggetto indicizzato dagli identificativi delle versioni. |
| `versioni.<ID>.standard` | ID della versione da cui deriva; assente o null per uno standard indipendente. Niente cicli. |
| `versioni.<ID>.durata_minuti` | Intero positivo: durata effettiva concordata. |
| `versioni.<ID>.font` | Stringa non vuota: font concordato. |
| `versioni.<ID>.fase` | Stringa non vuota: fase di lavoro raggiunta. |
| `versioni.<ID>.scaletta` | Percorso della scaletta effettiva, se presente. |
| `versioni.<ID>.registro` | Percorso del registro Excel, se presente. |
| `versioni.<ID>.approvazioni` | Oggetto scritto dal comando `approva`: revisione SHA-256 del file, contesto e riferimento standard al momento dell'approvazione. Non compilarlo a mano. |

I percorsi relativi si risolvono dalla cartella di `progetto.json`. Registrare nelle preferenze anche standard di riferimento, criteri particolari e scelta del font quando coinvolgono più versioni. Le proprietà aggiuntive della singola versione vengono conservate: usare `revisioni` per annotare motivo, accorpamenti e separazioni di evidenze, con ID precedenti e successivi. Se cambiano le preferenze o i metadati della versione, l'approvazione precedente non copre il nuovo contesto. Conservare in `versioni.<ID>.supporti` i contenuti e le conferme specifici di formulario, mappa, costanti o formule della singola prova adattata, senza dati personali. Le scelte condivise stanno nelle preferenze comuni. La sola fase di lavoro può avanzare senza invalidarla; aggiungere il percorso del registro non invalida la scaletta già approvata. L’approvazione del registro dipende anche dal contenuto della scaletta, quando presente.

`python scripts/progetto.py stato percorso/progetto.json` mostra per ogni versione standard, durata, font, fase e stato distinto di scaletta e registro:

- `mancante`: documento non indicato o non trovato;
- `da revisionare`: nessuna approvazione oppure file o contesto cambiati;
- `approvato`: revisione corrente uguale a quella confermata;
- `da riallineare`: derivata approvata rispetto a uno standard successivamente cambiato o non più approvato.

Dopo la conferma esplicita del docente, registrarla con `python scripts/progetto.py approva percorso/progetto.json ID scaletta` oppure `... ID registro`. Il comando non chiede il consenso e non può ricavarlo dal contenuto del file: l'agente lo esegue soltanto dopo averlo ricevuto per la revisione precisa mostrata. Per il registro esegue anche la validazione completa. Per una derivata richiede prima l'approvazione del documento corrispondente dello standard. Salvare in modo atomico il piccolo file di progetto; non sovrascrivere manualmente le impronte delle approvazioni.

Prima di generare o rigenerare, usare `stato`, rileggere il documento confermato e controllare che sia ancora approvato. Dopo un aggiornamento sostanziale ripetere revisione e consenso; non approvare automaticamente le derivate. Riepilogare l'impatto su calcoli, registro, livelli, correttore, svolgimento e versioni derivate. Conservare gli script quantitativi accanto alla prova e rieseguire quelli interessati.

## Confronto fra registri

`python scripts/progetto.py confronta prima.xlsx dopo.xlsx` valida entrambi i registri e confronta le evidenze tramite `ID evidenza`, indipendentemente dall'ordine. Se gli ID sono stati rinumerati, il confronto per ID non identifica da solo le azioni corrispondenti: usa la mappa delle revisioni e verifica manualmente i risultati. Restituisce evidenze mantenute, modificate (campi prima/dopo), eliminate e aggiunte; copertura degli argomenti con sigla e nome; pesi per indicatore e argomento nelle due versioni. Le differenze di `Punto/gruppo` sono visibili nelle evidenze modificate.

Legge entrambi i layout del registro (`merged` e `flat`), descritti nel [correttore](correttore.md#6-registro-excel-prima-del-latex).

Per accorpamenti o separazioni, passare `--derivazioni percorso/derivazioni.json`: oggetto con ID del registro successivo come chiavi e liste di ID del registro precedente come valori. Ogni riferimento viene controllato. Conservare questa mappa e la motivazione nelle revisioni di progetto. Rinumera gli ID in ordine di riga dopo inserimenti, eliminazioni o riordini. Registra una mappa completa tra gli ID delle revisioni e le derivazioni, conserva le note sulle azioni corrispondenti e riallinea i riferimenti; un ID può riferirsi ad azioni diverse in revisioni diverse.

Integrare il confronto con un giudizio motivato su richieste, difficoltà, tempi, profondità e obiettivi concordati. Un argomento presente e un totale di 1000 non dimostrano da soli l'equivalenza didattica. Il programma non la certifica.

## Matrice di copertura

Preparare `matrice_copertura.json` per ogni versione di cui si genera lo svolgimento studenti, perché i passaggi verificati sono quelli dello svolgimento. Schema:

| Campo | Tipo e significato |
|---|---|
| `registro` | Percorso del registro Excel, relativo alla cartella della matrice. |
| `richieste` | Lista completa dei sottopunti e dei quesiti singoli della prova. |
| `richieste[].id` | Identificativo univoco del punto della prova. |
| `richieste[].esercizio` | Riferimento all'esercizio nel registro. |
| `richieste[].punto` | Riferimento al sottopunto; `intero` per un quesito singolo. |
| `richieste[].evidenze` | Lista degli ID delle evidenze che valutano la richiesta. |
| `passaggi` | Lista degli ID univoci dei passaggi effettivamente presenti nello svolgimento studenti. |
| `copertura_evidenze` | Oggetto: ogni ID evidenza è associato alla lista dei passaggi che ne spiegano gli elementi valutati. |

Per evidenze comuni a più punti, usare nella colonna `Punto/gruppo` i riferimenti separati da virgole. La corrispondenza deve essere esplicita e limitata allo stesso esercizio. Le evidenze complessive usano `Intero elaborato` nelle colonne `Esercizio` e `Punto/gruppo`, la sigla argomento riservata `TRASVERSALE` e il nome `Competenze trasversali`; si collocano in fondo al registro e non si associano alle singole richieste. Nella matrice non inserirle in `richieste[].evidenze`, ma includerle in `copertura_evidenze` con i passaggi dello svolgimento che permettono di valutarle. Il controllo di copertura non richiede loro una richiesta specifica, ma verifica che i passaggi esistano. I passaggi possono essere condivisi da più evidenze, senza ripeterne il contenuto nello svolgimento.

`python scripts/progetto.py copertura percorso/matrice_copertura.json` segnala richieste prive di valutazione, evidenze senza richiesta, passaggi mancanti e riferimenti inesistenti. Esce con codice 1 se rileva problemi, 0 se la matrice è coerente. La matrice è uno strumento interno: non inserire ID valutativi nello svolgimento studenti. Controllare a mano che l'elenco delle richieste sia completo e che i passaggi indicati spieghino davvero gli aspetti valutati: i collegamenti corretti non verificano il contenuto matematico.

La calibrazione Base facoltativa è descritta nel [correttore](correttore.md#10-calibrazione-base-facoltativa).
