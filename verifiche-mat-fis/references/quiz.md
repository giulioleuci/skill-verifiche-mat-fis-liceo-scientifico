# Quiz a scelta multipla

Flusso per i comandi `quiz` e `correggi-quiz`. Il quiz è una prova a sé: non usa il registro delle evidenze. Gli indicatori ANA/SVI/ARG/COM sono facoltativi (vedi §1 bis). Le risposte possono arrivare da scansioni dei fogli risposte (§4). Lo script è `scripts/quiz.py` (solo `openpyxl`), adattato da <https://github.com/giulioleuci/multiple-choice-randomizer-latex> (GPL-3.0).

## 1. Domande

Le domande arrivano dal file Excel del docente: non scriverle tu. Un foglio è una domanda; ogni riga valida del foglio è una sua versione alternativa, e ogni variante ne estrae una. Colonne:

- obbligatorie: `Testo della domanda`, `Risposta corretta`, almeno una `Alternativa N`;
- facoltative: `Numero Colonne Alternative`, `Punteggio corretta`, `Punteggio non data`, `Punteggio errata` (sovrascrivono i valori predefiniti per quella riga), `Indicatore` (ANA, SVI, ARG o COM), `Alternative fisse` (vuota = si mescola tutto; `tutte` = ordine come scritto nelle colonne; un numero N = le ultime N colonne restano in fondo nell'ordine scritto, le altre si mescolano: `1` per «nessuna delle precedenti», `2` per «tutte le precedenti» seguita da un'altra alternativa fissa). Con questa colonna la risposta corretta deve comparire anche fra le colonne `Alternativa`, altrimenti lo script si ferma.

Testi e alternative sono LaTeX (matematica tra `$...$`, `\um{valore}{unità}`, `\%`).

## 1 bis. Indicatori

`Indicatore` è per riga: versioni diverse della stessa domanda possono avere indicatori diversi. Se la colonna è usata, ogni riga valida deve averlo (errore altrimenti). Senza la colonna il quiz funziona come prima.

- **Vincolo**: in ogni variante la quota di punti massimi per indicatore è identica (stesso peso su 1000). È ciò che fa coincidere sempre il voto dagli indicatori con quello dai punti: `Σ punti_ind / max × 1000` = `punti / max × 1000`. Con `--pesi ANA=250,SVI=400,ARG=200,COM=150` (somma 1000) la quota è imposta; senza, si usa il profilo più frequente tra i candidati della prima variante. Se nessuna combinazione lo rispetta, lo script si ferma e dice quale quota non è raggiungibile.
- **Scelta delle varianti**: tra le combinazioni valide si ruotano le versioni delle domande e si garantisce l'unicità. Solo se il vincolo sugli indicatori non è altrimenti raggiungibile la rotazione viene ignorata (con avviso). È campionamento (200 + 2000 tentativi), non ricerca esaustiva.
- **Punteggio**: `punti_ind = punti_ottenuti_ind / massimo_totale_della_variante × 1000`. Il totale è su 1000 e il voto in decimi usa `correzione.voto` (passo 0,25). `correggi` verifica per ogni studente che il voto dagli indicatori e quello dai punti coincidano.

## 2. Parametri da chiedere

Numero di varianti (predefinito 2), eventuali pesi per indicatore, punti per risposta corretta, non data ed errata (predefiniti 4, 1, 0), punti per risposta **annullata** (due cerchi, `--annullata`; predefinito come non data) ed eventuale **punteggio minimo** del quiz (`--minimo`, predefinito nessuno: con `--errata` negativa evita totali negativi; con gli indicatori il totale è portato al minimo e i punti per indicatore scalano in proporzione, così il voto dagli indicatori coincide ancora con quello dai punti), soglia di sufficienza (predefinita 0,58, ereditata dal progetto originale: vale solo per il flag «sufficiente» delle statistiche; per i voti usa la [griglia ufficiale](griglia_valutazione.md)). Non chiedere dati personali.

## 3. Generazione

```
python scripts/quiz.py genera domande.xlsx --varianti 4 [--corretta 4 --non-data 1 --errata 0 --annullata 0 --minimo 0 --soglia 0.58 --out quiz_out]
```

Produce in `quiz_out/` (nella cartella della prova: `NN_QUIZ/varianti`, vedi [cartelle](cartelle.md)): `quiz_<codice>.tex` e `.pdf` per variante (con foglio risposte), `quiz_chiavi.json` (usato dalla correzione), `quiz_chiavi.xlsx` (chiavi, solo docente) e `risposte_studenti.xlsx` (template). Ordine delle domande e delle alternative cambia a ogni variante; il modello è [quiz_template.tex](../assets/quiz_template.tex), derivato dal modello canonico.

Regole del foglio studente:

- niente titolo, materia o fila; in intestazione, su ogni pagina, i punteggi per risposta corretta, non data ed errata;
- **deroga ai soli quiz**: la variante è identificata da un codice anonimo di 4 caratteri (per esempio `K7Q2`) in intestazione a destra e nel QR del foglio risposte. Non rivela l'ordine né la fila;
- **foglio risposte in ogni variante**, in fondo al PDF: per ogni domanda i cerchi A, B, C... (solo le alternative esistenti), quattro quadrati neri agli angoli (guide per il software), QR con il codice, casella per cognome e nome. Lo studente **annerisce** il cerchio scelto; per **annullare** una risposta ne annerisce due o più; **nessuna correzione**: cancellature, bianchetto o cerchi anneriti in parte possono rendere la domanda non data (la lettura propone una risposta quando il segno è chiaro, ma il docente la rivede); Con penna nera o blu;
- **pagine pari**: il PDF di ogni variante ha un numero pari di pagine (domande + foglio risposte, minimo 2, poi 4...) per la stampa fronte-retro: se le pagine delle domande sono pari, si inserisce una pagina bianca prima del foglio risposte, che resta l'ultima pagina. Lo script lo verifica e segnala «DISPARI». Con più di 24 righe per colonna (circa 70 domande a 4 alternative) il foglio non basta e lo script si ferma;
- la geometria dei cerchi è salvata in `quiz_chiavi.json`: stampa e lettura usano gli stessi numeri, quindi non rigenerare le varianti dopo la stampa;
- compilazione in due passate con `pdflatex` (la numerazione `Pagina x di y` lo richiede; pacchetto `qrcode`). Con `--no-pdf` scrive solo i `.tex`.

Prima della consegna controlla il testo estratto dal PDF e consegna i PDF più il file delle chiavi al docente.

## 4. Lettura dei fogli risposte scansionati (facoltativa)

Se il docente fornisce le scansioni o le foto dei fogli risposte (anche i PDF fronte-retro interi: i fogli sono riconosciuti dai quadrati agli angoli), le risposte si leggono con software libero (OpenCV, poppler) e non a occhio. Altrimenti `risposte_studenti.xlsx` lo compila il docente (§5).

```
python scripts/quiz.py leggi cartella_scansioni [--out quiz_out] [--risultati NN/risultati]
```

Dipendenze: `pip install opencv-python-headless numpy`, `pdftoppm` (poppler). Scansioni a 150-300 dpi, pagina intera, anche storta o capovolta; le foto devono inquadrare i quattro quadrati.

1. **Cartelle e privacy**: scansioni in una cartella del docente (`Cognome_Nome.pdf` o immagini). Lo script scrive solo in `--out`. I nomi restano nei file locali del docente: mai nel repository, in log o test (test con alunni fittizi).
2. **Lettura automatica**: per ogni foglio lo script raddrizza l'immagine con i quadrati, legge il codice dal QR (assegna la variante) e misura il riempimento di ogni cerchio. Con `m1` il riempimento maggiore e `m2` il secondo (soglie in `omr.py`, tarate su scansioni simulate):
   - `ok`: `m1 ≥ 50%` e `m2 < 15%`: risposta certa;
   - `proposta`: risposta probabile da confermare, quando il cerchio annerito supera di 2,5 volte il secondo segno (cancellatura più nuova risposta) oppure c'è un solo segno debole (15-50%);
   - `annullata`: due cerchi anneriti o segni confusi; si scrive `*`;
   - `vuota`: nessun segno (< 15%), cella vuota.
   Ogni domanda ha anche una **confidenza** (0-1): l'editor mostra prima i dubbi maggiori. Un `*` vale non data nella statistica, con i punti di `--annullata`.
3. **Output**: `risposte_scansioni.xlsx` (`ID` S01, S02..., `Nome`, `Codice`, una colonna per domanda; le proposte sono già scritte) con un foglio `Anomalie` (proposte e annullate ancora da rivedere, dal dubbio maggiore; fogli non riconosciuti, codici non letti), e in `letture/`: `Sxx.png` (foglio raddrizzato), `Sxx_nome.png` (ritaglio del nome) e `letture.json` (riempimenti, stati, confidenza: è la fonte da cui l'xlsx deriva).
4. **Revisione nel browser**: `python scripts/quiz.py rivedi --out quiz_out [--risultati NN/risultati]` avvia un server locale (`127.0.0.1`, porta casuale, token, nessun dato esce dal PC) e apre l'editor (`assets/rivedi/`, TypeScript compilato in `rivedi.js`; il sorgente si ricompila con `npx -p typescript tsc -p assets/rivedi`, per usarlo non serve). A sinistra i fogli, per primi quelli con più dubbi; al centro la scansione con i cerchi sovrapposti (verde = risposta letta o confermata, ambra = proposta, tratteggio = segno rilevato); a destra il ritaglio del nome con il campo di testo e l'elenco delle domande da rivedere, dal dubbio maggiore (o tutte). Un clic su un cerchio, o le lettere `A`-`J`, imposta la risposta; `0` la svuota, `*` la annulla, `Invio` conferma la proposta; le frecce cambiano domanda e `[` `]` foglio. Le modifiche si salvano da sole in `letture.json` e `risposte_scansioni.xlsx`. Il docente può chiudere con Ctrl+C.
5. **Nome**: se il file si chiama `Cognome_Nome` il nome è precompilato: confrontalo con il ritaglio nell'editor e correggilo lì. Nome o codice illeggibile: non indovinare, chiedi al docente (codice vuoto = `correggi` si ferma).
6. **Controllo**: non correggere prima che il docente abbia rivisto le anomalie con `rivedi` (o ne abbia accettato l'elenco); poi esegui `quiz.py correggi --risposte quiz_out/risposte_scansioni.xlsx` (§5) e consegna il report. Se non puoi aprire un browser, mostra al docente il foglio `Anomalie` e chiedi le risposte giuste.

## 5. Correzione e statistiche

Il docente compila `risposte_studenti.xlsx` (oppure lo produce `leggi` dalle scansioni, §4): colonne `ID` (anonimo, deciso dal docente), `Nome` (facoltativa), `Codice` (quello sul foglio) e una colonna per domanda (1, 2, ...) con la lettera segnata. Cella vuota = non data; `*` = annullata (non data, punti `--annullata`). Poi:

```
python scripts/quiz.py correggi [--out quiz_out] [--risultati NN/risultati] [--risposte file.xlsx] [--soglia 0.58]
```

Produce in `--risultati` (default `--out`) `quiz_risultati.xlsx`, più `statistiche.md` e `statistiche_{classe,domande,distrattori,indicatori,distribuzione}.csv` ([statistiche](statistiche.md): affidabilità KR-20, errore standard di misura, segnalazioni «rivedere»). In `quiz_risultati.xlsx`:

- `Studenti`: ID e nome (se presenti), codice, corrette, non date, errate, punteggio, massimo, %, sufficienza, z-score, percentile e stanine (1-9) calcolati sulla percentuale, totale su 1000 e **voto in decimi** (`correzione.voto`, passo 0,25, minimo 2); con gli indicatori anche un punteggio per indicatore;
- `Domande`: esiti, % corrette/errate/non date, difficoltà (1 − % corrette), discriminazione (gruppo alto e basso al 27%) e nota «rivedere» se negativa; grafico a barre impilate;
- `Distrattori`: per ogni versione di domanda (foglio e riga Excel) quante volte è stata scelta ciascuna alternativa e la non data; segnala i distrattori mai scelti (poco plausibili) e quelli più scelti della risposta corretta (possibile ambiguità o chiave da controllare). Le alternative sono identificate per testo, letto da `quiz_chiavi.json` che le salva già nell'ordine stampato in ogni variante: non serve una mappa separata. Alternative con testo identico nella stessa riga sono unificate; con gli indicatori c'è anche una colonna `Indicatore`;
- `Classe` (con gli indicatori anche la media per indicatore e del totale): media, mediana, deviazione standard, quartili, minimo, massimo, % sufficienti e istogramma dei punteggi.

Lo script si ferma se un ID è duplicato o un codice è sconosciuto, e avvisa se una lettera non esiste tra le alternative (contata errata). Con meno di 2 studenti la discriminazione non è calcolata; con classi piccole (meno di 20-30 studenti) discriminazione e «mai scelto» sono poco affidabili. Non rigenerare le varianti dopo aver stampato i quiz: il file delle chiavi va conservato.

Quiz già corretti con altri strumenti: `importa-punteggi` ([statistiche](statistiche.md#2-importa-punteggi)). Le domande si scrivono con `quiz-domande` ([quiz_domande](quiz_domande.md)).

## 6. Verifica

`python scripts/test_quiz.py` esegue generazione, compilazione PDF e correzione su dati di prova e controlla i punteggi.
