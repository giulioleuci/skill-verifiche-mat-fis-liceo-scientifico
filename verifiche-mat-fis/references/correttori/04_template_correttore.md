# Macro e impaginazione dei correttori

Le fonti canoniche sono [corretore_template.tex](../../assets/corretore_template.tex) e [svolgimento_studenti_template.tex](../../assets/svolgimento_studenti_template.tex). Questo riferimento spiega il loro uso, senza riprodurre il preambolo o una prova compilata. La procedura e l'approvazione del registro appartengono al [flusso correttore](flusso_correttore.md); i criteri e livelli a [02](02_criteri_assegnazione_punteggi.md).

## Struttura del correttore docente

Apri con intestazione sintetica, contesto e legenda dei quattro indicatori, senza una sezione sui parametri di correzione. Riporta il testo della prova nei singoli esercizi. Il registro iniziale raggruppa esercizio e argomento comune, indicando ID evidenza, nome completo dell'azione, punto/gruppo, indicatore e massimo; per gruppi con argomenti diversi esplicita le associazioni. Il nome dell'azione è identico al titolo del suo svolgimento: questa ripetizione è ammessa.

Inserisci soltanto riepiloghi per esercizio, indicatore e argomento, derivati dalle stesse evidenze. Nessun riepilogo per punto/gruppo e nessuna tabella di conversione voto o giudizio, la cui fonte resta [01](01_griglia_valutazione.md).

Gli esercizi iniziano su una nuova pagina. Ogni evidenza ha una sola intestazione compatta «ID · sigla colorata · azione», passaggi numerati e livelli; nel corpo non ripetere esercizio, argomento, massimo o nome completo dell'indicatore. Metadati completi nel sorgente e nel registro, nessun campo per percentuale o punti ottenuti. Alternative, errori e criteri specifici stanno in elenco puntato dopo i livelli dell'evidenza pertinente; ometti la sezione se vuota. Le note condivise stanno dove nasce la scelta o l'errore, con rimandi senza duplicazioni.

## Macro canoniche

| Macro o ambiente | Uso |
|---|---|
| `\evidenza{ID}{esercizio/punto}{indicatore}{argomento}{massimo}` | Registra l'evidenza e l'ID del box successivo; per argomento usa l'ID del registro; specifica i punti del gruppo. |
| `\controllaevidenze` | Controlla il conteggio della verifica: da 1 a 40; dalla quarantunesima evidenza produce errore. Non aggirare il controllo. |
| `\livelli{non raggiunto}{iniziale}{base}{intermedio}{avanzato}` | Primo, terzo e quinto argomento obbligatori; secondo e quarto vuoti con `{}` quando non necessari. Le fasce non cambiano. |
| `\sigla{ANA}`, `\indicatore{ANA}` | Colora sigla oppure sigla e nome; analogamente SVI/ARG/COM. Usa le macro per ogni riferimento agli indicatori, anche in tabelle, note e legenda. |
| `boxana`, `boxsvi`, `boxarg`, `boxcom` | Unica intestazione con ID, sigla e azione; all'interno passaggi `enumerate` in terza persona. |
| `\registrogruppo{esercizio}{argomento}{righe}` | Raggruppa metadati comuni, senza perdere l'associazione di ogni evidenza. |
| `\riepiloghi{esercizi/indicatori}{argomenti}` | Affianca i riepiloghi aggregati. |
| `\inizioesercizi`, `\esercizio`, `\punto`, `\tabpunti`, `\sez`, `enun` | Conserva struttura e comandi del template. I massimi rimangono nei riepiloghi. |
| `\criteri{elenco}`, `\nota{testo}` | Note puntate dopo i livelli dell'evidenza interessata. |
| `\ANA{ID}{massimo}` e analoghe | Eventuali chip di riferimento, senza quote interne o detrazioni. |
| `grafico` | Figura nel passaggio pertinente; conserva `figure[h!]` e `\centering`. Verifica il posizionamento nel PDF. |

I colori rosso/blu/giallo/verde sono riservati agli indicatori. Nelle figure del correttore usa nero, grigi, arancio o teal; nella prova per gli studenti soltanto bianco, nero e grigio. Non introdurre un comando `\arg`, già riservato in LaTeX.

## Scrittura tecnica

Usa `siunitx`, `\SI`, `\si` e `\num`, con virgola decimale; nelle formule una virgola letterale richiede graffe. Mantieni gli argomenti degli operatori e i pedici testuali con `\pedice` o `\text`. I simboli matematici vanno in modalità matematica. Proteggi caratteri speciali; un `\item` non inizia con una parentesi quadra non protetta. Per formule lunghe usa un ambiente su riga propria.

Nelle classi prima, seconda e terza usa `\tg^{-1}`, `\sen^{-1}`, `\cos^{-1}` e analoghe, senza funzioni con `arc`. Dalla quarta sono ammesse le notazioni con arc. Non usare versori; nel modulo scrivi solo la lettera, mediante `\norma{F}`, senza freccia interna. Dalla seconda una legge scomposta ha un sistema con una equazione o disequazione per componente.

Parti dalle formule dirette e ricava letteralmente l'incognita; sostituisci i dati alla fine della derivazione pertinente. Una grandezza ormai espressa solo con dati noti si calcola subito con unità e il valore si riusa nei passaggi successivi: vale il massimo. Usa formule composte solo quando più convenienti o richieste. Indica unità nei risultati intermedi e finali, al termine dell'espressione, senza ripeterle su ogni fattore. Dichiara la convenzione angolare e usa gradi/radianti coerenti.

Per figure fisiche o geometriche usa TikZ, per grafici cartesiani pgfplots con assi, scale, etichette e virgola decimale. I grafici stanno nel passaggio pertinente in `grafico`; `[h!]` non garantisce una posizione impossibile: adatta dimensioni o pagina dopo aver controllato il PDF.

## Svolgimento studenti e compilazione

Usa il template studenti e organizza esercizi e sottopunti in passi numerati chiari: strategia, formule, condizioni, sviluppi, motivazioni essenziali, grafici, unità e risultati coprono tutto ciò che viene valutato. Un percorso completo lecito basta; non servono tutte le alternative. Gli aspetti condivisi sono spiegati una volta. Nessun punteggio, massimo, percentuale valutativa, indicatore o colore convenzionale, ID evidenza, livello, registro, riepilogo, errore tipico o istruzione al docente.

Applica la revisione linguistica di [SKILL.md](../../SKILL.md) e compila due volte entrambi i documenti con `pdflatex`. Per il solo testo dei documenti concordati con OpenDyslexic, verifica font e usa `fontspec` con XeLaTeX/LuaLaTeX; il correttore docente conserva la configurazione ordinaria. Controlla formule, accenti, simboli, riferimenti, pagine e testo estratto. Se mancano dipendenze consegna sorgenti e comando effettivo indicando il limite.
