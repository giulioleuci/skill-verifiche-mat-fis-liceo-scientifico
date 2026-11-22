# Quiz a scelta multipla

Flusso per i comandi `quiz` e `correggi-quiz`. Il quiz è una prova a sé: non usa il registro a 1000 punti né gli indicatori ANA/SVI/ARG/COM. Lo script è `scripts/quiz.py` (solo `openpyxl`), adattato da <https://github.com/giulioleuci/multiple-choice-randomizer-latex> (GPL-3.0).

## 1. Domande

Le domande arrivano dal file Excel del docente: non scriverle tu. Un foglio è una domanda; ogni riga valida del foglio è una sua versione alternativa, e ogni variante ne estrae una. Colonne:

- obbligatorie: `Testo della domanda`, `Risposta corretta`, almeno una `Alternativa N`;
- facoltative: `Numero Colonne Alternative`, `Punteggio corretta`, `Punteggio non data`, `Punteggio errata` (sovrascrivono i valori predefiniti per quella riga).

Testi e alternative sono LaTeX (matematica tra `$...$`, `\um{valore}{unità}`, `\%`).

## 2. Parametri da chiedere

Numero di varianti (predefinito 2), punti per risposta corretta, non data ed errata (predefiniti 4, 1, 0), soglia di sufficienza (predefinita 0,58, ereditata dal progetto originale: vale solo per il flag «sufficiente» delle statistiche; per i voti usa la [griglia ufficiale](griglia_valutazione.md)). Non chiedere dati personali.

## 3. Generazione

```
python scripts/quiz.py genera domande.xlsx --varianti 4 [--corretta 4 --non-data 1 --errata 0 --soglia 0.58 --out quiz_out]
```

Produce in `quiz_out/`: `quiz_<codice>.tex` e `.pdf` per variante, `quiz_chiavi.json` (usato dalla correzione), `quiz_chiavi.xlsx` (chiavi, solo docente) e `risposte_studenti.xlsx` (template). Ordine delle domande e delle alternative cambia a ogni variante; il modello è [quiz_template.tex](../assets/quiz_template.tex), derivato dal modello canonico.

Regole del foglio studente:

- niente titolo, materia o fila; in intestazione, su ogni pagina, i punteggi per risposta corretta, non data ed errata;
- **deroga ai soli quiz**: la variante è identificata da un codice anonimo di 4 caratteri (per esempio `K7Q2`) in intestazione a destra. Non rivela l'ordine né la fila;
- la griglia delle risposte è sul foglio: lo studente segna una croce nella casella della lettera scelta;
- compilazione in due passate con `pdflatex` (la numerazione `Pagina x di y` lo richiede). Con `--no-pdf` scrive solo i `.tex`.

Prima della consegna controlla il testo estratto dal PDF e consegna i PDF più il file delle chiavi al docente.

## 4. Correzione e statistiche

Il docente compila `risposte_studenti.xlsx`: colonne `ID` (anonimo, deciso dal docente), `Codice` (quello sul foglio) e una colonna per domanda (1, 2, ...) con la lettera segnata. Cella vuota = non data. Poi:

```
python scripts/quiz.py correggi [--out quiz_out] [--risposte file.xlsx] [--soglia 0.58]
```

Produce `quiz_risultati.xlsx`:

- `Studenti`: corrette, non date, errate, punteggio, massimo, %, sufficienza, z-score, percentile e stanine (1-9) calcolati sulla percentuale;
- `Domande`: esiti, % corrette/errate/non date, difficoltà (1 − % corrette), discriminazione (gruppo alto e basso al 27%) e nota «rivedere» se negativa; grafico a barre impilate;
- `Distrattori`: per ogni versione di domanda (foglio e riga Excel) quante volte è stata scelta ciascuna alternativa e la non data; segnala i distrattori mai scelti (poco plausibili) e quelli più scelti della risposta corretta (possibile ambiguità o chiave da controllare). Le alternative sono identificate per testo, letto da `quiz_chiavi.json` che le salva già nell'ordine stampato in ogni variante: non serve una mappa separata. Alternative con testo identico nella stessa riga sono unificate;
- `Classe`: media, mediana, deviazione standard, quartili, minimo, massimo, % sufficienti e istogramma dei punteggi.

Lo script si ferma se un ID è duplicato o un codice è sconosciuto, e avvisa se una lettera non esiste tra le alternative (contata errata). Con meno di 2 studenti la discriminazione non è calcolata; con classi piccole (meno di 20-30 studenti) discriminazione e «mai scelto» sono poco affidabili. Non rigenerare le varianti dopo aver stampato i quiz: il file delle chiavi va conservato.

## 5. Verifica

`python scripts/test_quiz.py` esegue generazione, compilazione PDF e correzione su dati di prova e controlla i punteggi.
