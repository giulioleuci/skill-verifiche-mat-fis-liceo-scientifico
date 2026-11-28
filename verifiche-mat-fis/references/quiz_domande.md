# Domande del quiz: intervista e banca

Procedura per `quiz-domande`: produce `domande.xlsx` per `quiz.py genera` ([quiz](quiz.md)), con la stessa disciplina della prova scritta standard: scaletta, approvazione, contenuti, verifica. Per il comando `banca-domande` vedi §5.

## 1. Intervista

Cartella di lavoro: chiedila e creala ([cartelle](cartelle.md)). Poi, in questo ordine, chiedi solo ciò che manca:
1. Materia, anno e **livello della classe** (basso, medio, alto); durata prevista del quiz.
2. **Argomenti**: proponi l'elenco della scheda (`schede/<materia>_classe<N>.md`) come precompilato; il docente seleziona, toglie, aggiunge o rinomina. Conferma di cosa è stato svolto.
3. **Numero di domande** e di **alternative** (default 4), numero di colonne per le alternative lunghe.
4. **Indicatori**: con o senza ANA/SVI/ARG/COM. Se sì, i pesi su 1000 (`--pesi` di `quiz.py genera`); con i pesi, ogni domanda ha un indicatore e le varianti conservano le stesse quote.
5. **Versioni**: quante versioni equivalenti per domanda, perché le varianti ne estraggano una diversa (default 2 per le domande centrali, 1 per le altre).
6. **Supporti**: formulario o costanti ammessi (numerati: attendi conferma), calcolatrice. Il quiz non riporta formule non concordate.
7. **Punteggi**: corretta, non data, errata (default 4, 1, 0), annullata (default come non data), minimo del quiz (default nessuno), soglia di sufficienza.
7 bis. **Alternative da non mescolare**: «nessuna delle precedenti», «tutte le precedenti» o alternative numeriche in ordine crescente: colonna `Alternative fisse` (vedi [quiz §1](quiz.md)); la corretta compare anche fra le colonne `Alternativa`.
8. Se esiste una banca (`_banca/banca.xlsx`), chiedi se riusare domande: `banca-domande` (§5).

## 2. Scaletta e approvazione

Proponi una tabella: numero, argomento, indicatore (se usato), cosa chiede la domanda, difficoltà attesa (facile/media/difficile), versioni. Controlla la copertura degli argomenti e la distribuzione delle difficoltà. **Non scrivere le domande prima dell'approvazione esplicita** della scaletta; il silenzio non approva.

## 3. Scrittura

- Una sola risposta corretta, formulata in modo non ambiguo. Il testo non suggerisce la risposta e non riporta formule non concordate.
- **Distrattori plausibili**: ognuno corrisponde a un errore tipico (segno, unità, confusione fra grandezze, formula applicata male, risultato intermedio). Non usare «nessuna delle precedenti» né «tutte le precedenti»; alternative di lunghezza simile, senza ripetizioni.
- Le versioni della stessa domanda valutano la stessa abilità con dati diversi.
- Convalida ogni calcolo con uno script Python autonomo (`verifica-calcoli`) prima di inserirlo, anche per i distrattori che derivano da errori tipici.
- LaTeX in matematica con `$...$`, `\SI` per le grandezze fisiche (preambolo in [latex](latex.md)).

## 4. File e controllo

1. Scrivi `domande.json` (schema in `scripts/domande_xlsx.py`): per ogni domanda `argomento`, `indicatore` (facoltativo, ma se c'è serve ovunque), `versioni` con `testo`, `corretta`, `errate`, `colonne`, `punti`.
2. `python scripts/domande_xlsx.py write domande.json NN/domande.xlsx` scrive un foglio per domanda (D01, D02...) e controlla il file: errori (alternative ripetute o uguali alla corretta, indicatore mancante) e avvisi (meno di 4 alternative, versioni con numero diverso di alternative). Esce con 1 se trova errori. `domande_xlsx.py check file.xlsx` controlla un file del docente.
3. Mostra al docente le domande in forma leggibile (testo, alternative, corretta evidenziata) e **attendi la sua approvazione del contenuto**. Registra la modifica nel `progetto.json` della cartella (`fase`).
4. Solo allora `quiz.py genera NN/domande.xlsx --varianti N --out NN/varianti`.

## 5. Banca delle domande

La banca raccoglie le domande dei quiz con la difficoltà misurata sugli alunni, per comporre quiz bilanciati. Sta in `radice/_banca/banca.xlsx`.

```
python scripts/banca.py aggiungi NN_QUIZ [--radice DIR]     # dopo correggi-quiz: unisce domande.xlsx e difficoltà misurata
python scripts/banca.py componi --out NN/domande.xlsx [--argomento A] [--indicatore ANA] [--difficolta 0.3-0.7] [--n 10]
```

Difficoltà = 1 − quota di risposte corrette; con più quiz è la media pesata sugli alunni. Le domande mai somministrate non hanno difficoltà e non passano un filtro di difficoltà. `componi` estrae a caso fra le domande che rispettano i filtri e scrive un `domande.xlsx` pronto per `quiz.py genera` (una versione per domanda). Con classi sotto 20 alunni la difficoltà è indicativa: dillo al docente. Mostra l'elenco estratto e attendi conferma prima di generare.
