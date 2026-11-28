# Cartelle di lavoro

Valgono per ogni comando che scrive file: `nuova-verifica`, `varianti`, `recupero`, `correttore`, `genera-correttore`, `quiz`, `quiz-domande`, `correggi`, `correggi-quiz`, `importa-punteggi`.

## 1. Regola

- Una cartella per prova o quiz, chiamata `NN_NOME` (`01_VERIFICA_RETTE`, `02_QUIZ_CINEMATICA`, `03_...`). La numerazione è unica e progressiva per verifiche e quiz insieme. Il numero successivo è il massimo esistente più uno: non riusa i buchi e non rinumera.
- **Prima di scrivere qualunque file chiedi al docente in quale cartella lavorare** (default: la radice, cioè la cartella di lavoro corrente). Non scrivere mai nella cartella della skill.
- Crea la cartella con `python scripts/cartelle.py nuova NOME --tipo prova|quiz|importata [--radice DIR]`: stampa il percorso, crea le sottocartelle, `progetto.json` e un `.gitignore` per i dati con i nomi. `cartelle.py elenco [--radice DIR]` mostra tipo, fase e numero di file dei risultati di ogni cartella; `progetto.py stato NN_NOME/progetto.json` lo mostra per una sola.
- Una prova già esistente, chiamata diversamente, resta com'è: proponi la numerazione solo per le nuove.

## 2. Struttura

```
radice/
  01_VERIFICA_RETTE/        tipo prova
    progetto.json           preferenze, versioni, approvazioni (vedi progetto.md)
    scalette/  prove/  registri/  calcoli/  correttori/
    consegne/               elaborati scansionati con i nomi (esclusa da git)
    risultati/              schede, riepilogo_voti.xlsx, correttore_alunni.xlsx, statistiche_*.csv, report_classe.md
  02_QUIZ_CINEMATICA/       tipo quiz
    progetto.json  domande.xlsx
    varianti/               PDF, quiz_chiavi.json (da conservare), risposte_studenti.xlsx
    scansioni/              fogli risposte con i nomi (esclusa da git)
    risultati/              quiz_risultati.xlsx, statistiche_*.csv, valutazioni
  03_TERZA_A/               tipo importata (punteggi anonimi del docente)
    dati/  risultati/
  storico.csv  storico.xlsx   aggiornati da `chiudi-prova`
  _banca/banca.xlsx           banca delle domande dei quiz
```

Comandi con le cartelle: `quiz.py genera domande.xlsx --out NN/varianti`, `quiz.py correggi --out NN/varianti --risultati NN/risultati`, `correzione.py NN/registri/registro.xlsx NN/risultati/correzioni.json NN/risultati/riepilogo_voti.xlsx`, `importa.py ... --out NN/risultati`.

## 3. Privacy

I nomi stanno solo in `consegne/`, `scansioni/` e `dati/`, che il `.gitignore` della cartella esclude. Le statistiche, lo storico e il report sono anonimi: alunni indicati come A01, A02... Non copiare nomi in `risultati/` salvo schede e riepilogo voti, che il docente consegna agli alunni.
