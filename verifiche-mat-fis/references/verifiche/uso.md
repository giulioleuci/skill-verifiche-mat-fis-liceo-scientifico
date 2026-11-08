# Uso del generatore

`nuova-verifica` progetta la prova e la sua scaletta; `varianti` deriva versioni ordinarie; `recupero` prepara una prova mirata con griglia NR/PR/R. Segui il [flusso generatore](flusso_generatore.md), disponibile anche in [LaTeX](flusso_generatore.tex).

Il docente fornisce materia, anno, argomenti e vincoli già noti. L'assistente chiede solo ciò che manca, propone la scaletta e attende la sua approvazione esplicita prima del LaTeX. Le prove adattate vengono progettate dopo lo standard approvato e richiedono una conferma distinta.

Per matematica in terza, quarta e quinta di almeno 100 minuti il formato predefinito è un problema di 3 o 4 punti e 3 o 4 quesiti singoli. Per punti dipendenti il docente sceglie se fornire risultati intermedi; la scelta è attesa e registrata.

La prova pronta per la stampa è monocromatica, senza soluzioni, titolo, materia o fila. Fanno eccezione i risultati intermedi concordati e i supporti generali esplicitamente confermati. Usa il [modello canonico](../../assets/modello_verifica.tex). Il motore ordinario è `pdflatex`; OpenDyslexic richiede scelta esplicita e motore compatibile. La consegna comprende sorgente e PDF compilato e controllato oppure la dichiarazione del limite. `stato` riprende il lavoro dalla revisione raggiunta secondo il [progetto](../progetto.md).

Prima del LaTeX l’assistente propone sempre costanti e formule in elenco numerato e attende la scelta esplicita. Le sole voci confermate compaiono dopo `\vfill`, prima dei dati studente. Per le prove adattate, destinate anche a BES e DSA, chiede se occorrono formulario o mappa concettuale specifici; restano invariati argomenti, difficoltà e profondità. Dettagli nei [supporti della prova](supporti_prova.md).
