# Statistiche, storico e report di classe

Le statistiche sono oggettive (calcolate, non commentate a occhio) e uguali per prove scritte e quiz. Si producono con `correggi` (`scripts/correzione.py`), `correggi-quiz` (`scripts/quiz.py correggi`) o `importa-punteggi` (`scripts/importa.py`), nella cartella `risultati/` della prova. Il calcolo comune sta in `scripts/statistiche.py`. Dati sempre anonimi.

## 1. Cosa producono

`statistiche.md` (lettura) e un CSV per tabella (`statistiche_<tabella>.csv`):

| Tabella | Contenuto |
|---|---|
| `classe` | alunni, media, mediana, deviazione standard, minimo, massimo, quartili, % sufficienti (prove: voto ≥ 6; quiz: soglia), media dei voti, **affidabilità** (alpha di Cronbach, KR-20 nei quiz), **errore standard di misura**, avviso con meno di 20 alunni |
| `evidenze` (prove) | media % del massimo, % alunni con almeno metà del massimo, difficoltà (1 − media), discriminazione (gruppo alto e basso al 27%), nota |
| `domande`, `distrattori` (quiz) | esiti, difficoltà, discriminazione, scelte per alternativa, distrattori mai scelti o più scelti della corretta |
| `indicatori`, `livelli`, `argomenti` | media punti e media % di ogni gruppo di evidenze (nei quiz solo gli indicatori, se presenti); «debole» sotto il 60% |
| `distribuzione` | alunni per fascia di punteggio (10 fasce) |

**Segnalazioni «rivedere»** nella colonna `Nota`: discriminazione negativa; item raggiunto da meno del 10% degli alunni; item raggiunto da oltre il 95% («poco informativa»). Nelle prove «raggiunta» significa almeno metà del massimo; nei quiz risposta corretta. Sotto 20 alunni discriminazione, affidabilità e «mai scelto» sono poco attendibili: dillo al docente.

Commenta i risultati con numeri (quali indicatori e argomenti sono deboli, quali item rivedere); non dedurre cause didattiche senza il docente.

## 2. `importa-punteggi`

Per le prove corrette dal docente o con altri strumenti. Il docente fornisce un file **anonimo**; l'intestazione degli alunni può essere vuota, una sigla o un nome (non viene mai scritta nei risultati: gli alunni diventano A01, A02...).

```
python scripts/importa.py prova registro_approvato.xlsx punteggi.xlsx --out NN/risultati [--formato percentuali|punti]
python scripts/importa.py quiz punteggi.xlsx --out NN/risultati [--chiavi quiz_chiavi.json] [--corretta 4 --non-data 1 --errata 0]
```

**Prova scritta**: stesso schema del correttore Excel: le colonne del registro (ID evidenza in colonna A, riga 1 intestazioni), eventuali colonne vuote, poi **una colonna per alunno**. Celle: percentuale 0-100 per evidenza (come `correttore_alunni.xlsx`) oppure punti. Il formato si riconosce dai massimi del registro; se i valori sono validi in entrambi i modi lo script si ferma e chiede `--formato`: chiedi al docente. Celle vuote = 0 punti, con avviso. Si ferma se mancano evidenze, se un valore non è un numero o se supera il massimo.

**Quiz**: una riga per domanda (colonna A = numero), **una colonna per alunno**, più una riga con A = «Variante» e il codice della variante di ciascuno. Con `--chiavi` (il `quiz_chiavi.json` della skill) le celle sono lettere e si hanno anche le statistiche sui distrattori. Senza chiavi le celle sono 1 (corretta), 0 (errata) o vuote (non data): niente distrattori.

## 3. `chiudi-prova` e `report-classe`

```
python scripts/statistiche.py chiudi NN_NOME    # storico.csv/xlsx nella radice, fase = chiusa, elenco «da rivedere»
python scripts/statistiche.py report NN_NOME    # risultati/report_classe.md
```

`storico.csv` ha una riga per prova e voce (`TOTALE` più gli indicatori ANA/SVI/ARG/COM): prova, voce, alunni, media %. `storico.xlsx` ha il grafico di andamento. `chiudi` è idempotente: richiamarlo aggiorna le righe della stessa prova. Dopo `chiudi` proponi al docente le revisioni delle evidenze e delle domande segnalate (nuova revisione del registro con `update`, o domande da sostituire nella banca). `report-classe` elenca indicatori e argomenti dal più debole (candidati al recupero), le segnalazioni e, con almeno due prove, l'andamento. Nessun nome.
