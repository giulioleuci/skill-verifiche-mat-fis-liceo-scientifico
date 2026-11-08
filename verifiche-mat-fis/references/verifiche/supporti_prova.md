# Costanti, formule e supporti delle prove

Regola comune a verifiche, recuperi, varianti ordinarie e prove adattate. Proponi sempre l'eventuale inserimento di costanti e formule utili prima della generazione: elenca le voci in un **elenco numerato**, indicando nome, valore o contenuto e pertinenza. Chiedi al docente quali numeri desidera includere, oppure se non desidera alcun supporto, e **attendi conferma esplicita**. La sola approvazione generica della scaletta non vale come scelta dei supporti. Se la scelta è già esplicita e copre le versioni interessate, riusala senza ripetere la domanda.

Nelle proposte e nel testo stampato usa il **nome delle costanti, non il simbolo**: al nome segue il valore con unità. I simboli rimangono ammessi nelle formule generali, dove hanno funzione matematica. Non confondere costanti universali, valori convenzionali e proprietà dei materiali.

## Proposta predefinita per fisica

Presenta sempre queste voci numerate, segnalando quelle non pertinenti agli argomenti, senza inserirle automaticamente:

1. **Accelerazione di gravità**: valore terrestre di riferimento circa \(9{,}81\,\mathrm{m/s^2}\), salvo valore diverso concordato. È un'approssimazione locale, non una costante universale.
2. **Costante di Coulomb**: circa \(8{,}99\times10^9\,\mathrm{N\,m^2/C^2}\), per il vuoto.
3. **Costante dielettrica del vuoto**: circa \(8{,}85\times10^{-12}\,\mathrm{F/m}\).
4. **Costante dielettrica relativa**: proprietà adimensionale del materiale. Chiedi il materiale e il valore da adottare se non già forniti; non inventare un valore universale e non confonderla con quella del vuoto. Riporta il nome del materiale accanto al valore confermato.
5. **Velocità della luce nel vuoto**:  \(3\times10^8\,\mathrm{m/s}\).
6. **Permeabilità magnetica del vuoto**: proponi l'approssimazione scolastica \(4\pi\times10^{-7}\,\mathrm{N/A^2}\), circa \(1{,}26\times10^{-6}\,\mathrm{N/A^2}\). È la costante magnetica del vuoto, non una costante «paramagnetica»; non presentare l'approssimazione come valore esatto del SI.
7. **Tabella dei momenti di inerzia di anello, disco, sfera e sbarretta**: proponi la tabella seguente, specificando geometria e asse. Fai confermare i casi necessari; non usare una formula senza dichiarare l'asse.

| Corpo omogeneo | Asse di rotazione | Momento di inerzia |
|---|---|---|
| Anello sottile di massa \(M\), raggio \(R\) | Passante per il centro e perpendicolare al piano | \(I=MR^2\) |
| Disco pieno di massa \(M\), raggio \(R\) | Passante per il centro e perpendicolare al piano | \(I=\tfrac12 MR^2\) |
| Sfera piena di massa \(M\), raggio \(R\) | Un diametro | \(I=\tfrac25 MR^2\) |
| Sbarretta sottile di massa \(M\), lunghezza \(L\) | Passante per il centro e perpendicolare alla sbarretta | \(I=\tfrac1{12}ML^2\) |
| Sbarretta sottile di massa \(M\), lunghezza \(L\) | Passante per un estremo e perpendicolare alla sbarretta | \(I=\tfrac13 ML^2\) |

Se il testo usa una sfera cava, un anello spesso o un altro asse, adatta e verifica la formula e richiedi conferma del contenuto effettivo. Puoi proporre ulteriori formule pertinenti, sempre come voci numerate soggette alla scelta del docente.

Riferimenti per i valori e le convenzioni: [NIST, costanti CODATA](https://physics.nist.gov/cuu/pdf/all.pdf), [NIST, unità SI della velocità della luce](https://www.nist.gov/pml/special-publication-330/sp-330-section-2), [OpenStax, momenti di inerzia](https://openstax.org/books/university-physics-volume-1/pages/10-4-moment-of-inertia-and-rotational-kinetic-energy). I valori sopra sono arrotondamenti per la prova, da usare coerentemente anche nei calcoli e nei correttori.

## Proposta per matematica in quarta

Quando gli argomenti lo rendono necessario, proponi esplicitamente queste voci nell'elenco numerato:

1. Tabella dei valori esatti di seno e coseno degli angoli \(\pi/6\), \(\pi/4\), \(\pi/3\), in radianti.
2. Formule di addizione e sottrazione del seno: \(\sin(\alpha\pm\beta)=\sin\alpha\cos\beta\pm\cos\alpha\sin\beta\).
3. Formule di addizione e sottrazione del coseno: \(\cos(\alpha\pm\beta)=\cos\alpha\cos\beta\mp\sin\alpha\sin\beta\).

| Angolo | Seno | Coseno |
|---|---|---|
| \(\pi/6\) | \(1/2\) | \(\sqrt3/2\) |
| \(\pi/4\) | \(\sqrt2/2\) | \(\sqrt2/2\) |
| \(\pi/3\) | \(\sqrt3/2\) | \(1/2\) |

Anche fuori da questo caso proponi eventuali formule pertinenti, senza aggiungerle d'ufficio. Non inserire valori o formule che risolvano già le richieste della prova.

## Prove adattate per BES

Usa la denominazione **prove adattate**, anche per DSA, altri BES o esigenze di tempo, senza riportare diagnosi nei documenti degli studenti. Chiedi sempre, se non già chiarito, se occorre un **formulario specifico**, una **mappa concettuale specifica**, entrambi oppure nessuno. Concorda argomenti, formule, relazioni concettuali, formato e versioni destinatarie; mostra il contenuto esatto e attendi l'approvazione esplicita prima di inserirlo. Non dedurre questi strumenti dalla sola presenza di un BES e non chiedere dati personali.

Mantieni **gli stessi argomenti verificati, il livello di difficoltà e la profondità** dello standard. Adatta accessibilità e carico accessorio, senza trasformare il supporto nello svolgimento degli esercizi. Un formulario può raccogliere relazioni generali; una mappa collega concetti, condizioni e relazioni pertinenti, senza dati sostituiti o soluzioni della prova. Se uno strumento annulla una prestazione che si intende verificare, segnala il conflitto e concorda un supporto e richieste che conservino obiettivi e difficoltà, senza semplificare silenziosamente.

## Inserimento e allineamento

Nel [modello canonico](../../assets/modello_verifica.tex), dopo l'ultima consegna e fuori da `questions`, mantieni `\vfill`; subito dopo inserisci `\supportiprova{...}` con **soltanto il contenuto confermato**, quindi la riga Cognome e Nome / Classe / Data. Non mettere supporti dopo gli identificativi o nelle intestazioni. Se il docente non li vuole, ometti il blocco e conserva `\vfill`.

Il blocco è monocromatico e non flottante. Usa nomi delle costanti con valori e unità (`siunitx`), tabelle leggibili e formule generali. Non precompilare il template con il catalogo. Controlla lo spazio reale nel PDF: mantieni blocco e identificativi insieme sul fondo dell'ultima pagina utile; se non entrano, ridistribuisci le consegne senza comprimere la leggibilità. Per una mappa estesa concorda un allegato specifico, senza spostarla fuori dal testo di tua iniziativa.

Registra contenuto, valori, rifiuto eventuale, versioni destinatarie e conferma nella scaletta e nel [progetto](../progetto.md): preferenze comuni per i supporti condivisi, metadati della singola versione per quelli specifici. Se i supporti vengono concordati dopo l’approvazione della scaletta, mostra la revisione aggiornata con contenuti e versioni interessate: la conferma esplicita può coprire insieme i supporti e quella revisione, senza una seconda domanda identica. Registra poi l’approvazione del contesto aggiornato; non riutilizzare l’impronta precedente. Lo standard approvato trasmette alle varianti soltanto le scelte pertinenti e confermate; per aggiunte o modifiche mostra il nuovo elenco e attendi conferma. Verifica ogni versione, comprese quelle adattate.

Passa al correttore il testo effettivamente consegnato e i supporti disponibili. Non attribuire credito per ricordare autonomamente una costante, formula o relazione già fornita; valuta le azioni ancora richieste senza duplicare o penalizzare l'uso del supporto consentito. Riesamina evidenze, pesi, confronto e copertura quando il supporto cambia; registra l'approvazione della revisione interessata secondo il flusso ordinario.
