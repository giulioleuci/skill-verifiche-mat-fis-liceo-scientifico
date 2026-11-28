# Correzione di elaborati scansionati

Procedura per `correggi`: corregge gli elaborati degli alunni (scansioni o foto) con il **registro evidenze approvato** della versione, produce una scheda PDF per alunno e il riepilogo dei voti. Per i quiz vale `correggi-quiz` ([quiz](quiz.md#4-acquisizione-da-scansioni-facoltativa)). Leggi questo file, [correttore](correttore.md#5-valutazione-ed-errori) per errore trascinato e alternative, e [griglia](griglia_valutazione.md) per le fasce.

## 1. Cartelle e privacy

Il docente sceglie la cartella `NN_NOME` della prova ([cartelle](cartelle.md)): `consegne/` per le scansioni, `risultati/` per l'output. Per ogni versione (la fila è la versione), accanto a registro e correttore:

```
<versione>/
  registro_evidenze.xlsx     approvato, invariato
  scansioni/                 Cognome_Nome.pdf, oppure sottocartella Cognome_Nome/ con foto, oppure Cognome_Nome_1.jpg…
  risultati/                 unica cartella in cui scrivi
```

`correzione.py` scrive in `risultati/` anche le statistiche anonime (`statistiche.md` e CSV per evidenza, indicatore, livello, argomento: [statistiche](statistiche.md)). Per chiudere la prova usa `chiudi-prova`; per la sintesi di classe `report-classe`.

- Scrivi solo in `risultati/`. Non modificare, spostare o cancellare altri file; non cancellare nulla senza richiesta esplicita.
- Il nome dell'alunno viene dal nome del file o della sottocartella (`Cognome_Nome`).
- **Privacy**: nomi e correzioni restano nella cartella locale del docente. Mai nel repository della skill, in log, esempi o test (test con alunni fittizi).

## 2. Controllo iniziale

1. Verifica che il registro della versione esista, sia approvato ([progetto](progetto.md)) e superi `registro_xlsx.py check`. Se manca, prima `correttore` con testo e soluzioni; non correggere con una griglia improvvisata.
2. Elenca gli alunni trovati, le pagine di ciascuno, file vuoti, nomi non standard e formati illeggibili.
3. Più versioni: assegna ogni alunno alla sua, in ordine, con la lettera iniziale del file (`A_Rossi_Mario.pdf`), l'intestazione del compito, i dati numerici usati nelle risposte confrontati con i testi. Con indizi mancanti o in contrasto non indovinare: chiedi al docente e annota il caso. Mostra il conteggio per versione e attendi conferma.

## 3. Lettura delle scansioni

- PDF: rasterizza con `pdftoppm -r 150` e guarda le pagine. HEIC: converti in JPG con `pillow-heif` applicando `ImageOps.exif_transpose`.
- Ruota le immagini ruotate o capovolte; ritaglia e ingrandisci le righe piccole; non aumentare il contrasto se peggiora la lettura.
- Le parti cancellate dall'alunno non si valutano; segui asterischi e rimandi nel resto del foglio.
- Parti illeggibili: dillo, non inventare il contenuto.

## 4. Valutazione

Per ogni evidenza del registro assegna una **percentuale 0–100** secondo i descrittori dei livelli e le regole di [correttore §5](correttore.md#5-valutazione-ed-errori) (errore penalizzato dove nasce, seguito coerente valido, alternative ammesse, ARG assente = zero solo in ARG). Stessa severità su errori uguali, anche tra versioni. Confronta i calcoli con gli script conservati accanto alla prova.

Stati speciali, in percentuale del **massimo dell'evidenza**:

- **non svolta** (assente o vuota): **10%**;
- **svolta ma totalmente sbagliata** (tentativo, 0%): **20%**;
- un parziale non scende mai sotto il 20%.

Conseguenze, indipendenti dal numero di evidenze: compito tutto in bianco = 100/1000 = voto **1**; tutto sbagliato = 200/1000 = voto **2**; compito in parte sbagliato e in parte in bianco = almeno 2 (almeno un tentativo).

Nel JSON delle correzioni: numero 0–100, `0` per «tentata e sbagliata», `null` o assente per «non svolta». Con prove adattate usa il registro adattato e non penalizzare misure dispensative.

## 5. Voto in decimi

Totale punti su 1000 → voto = punti / 100, arrotondato a multipli di 25 punti (per eccesso dal mezzo passo), **minimo 2** (solo il compito tutto in bianco vale 1):

| Punti | 500 | 525 | 550 | 575 | 600 | 975 | 1000 |
|---|---|---|---|---|---|---|---|
| Voto | 5 | 5+ | 5½ | 6- | 6 | 10- | 10 |

`+` = +0,25, `½` = +0,5, `-` = −0,25 rispetto al voto successivo. La conversione è in `scripts/correzione.py` (`voto()`), la stessa logica sta nelle formule del file Excel: non riscriverla a mano. Parametri (10%, 20%, 25, minimo 200, bianco 100) in testa allo script.

## 6. Taratura sul primo alunno

1. Correggi **un solo alunno** (il primo in ordine alfabetico, salvo indicazione diversa; uno per versione se sono più di una).
2. Produci la scheda (§7) e mostra: percentuale e punti per evidenza con motivazione breve, totale, voto.
3. **Fermati e attendi l'approvazione.** Se il docente corregge una percentuale, rifai la scheda; se contesta l'evidenza o il peso, è una modifica del registro (`update`, nuova approvazione), non una griglia parallela.
4. Solo dopo passa al resto della classe con gli stessi criteri. Non fermarti a ogni alunno: raccogli i dubbi nelle note.

## 7. Scheda PDF dell'alunno

`risultati/<Argomento>_<Cognome Nome>.pdf`, **una pagina A4**, da [scheda_alunno_template.tex](../assets/scheda_alunno_template.tex), compilata con `pdflatex` in due passate. Contenuto: titolo con alunno, classe, data; tabella punti per esercizio e totale su 1000; voto; per ogni esercizio due elenchi, **Corretto** con ✓ verde acceso e **Errori e mancanze** con ✗ rosso acceso, brevi e concreti (formule e valori giusti dove l'alunno sbaglia); 3–4 aree di miglioramento; nota con il calcolo del voto. Niente indicatori ANA/SVI/ARG/COM né ID evidenza. I colori rosso e verde accesi valgono solo per questi simboli. Se la scheda supera una pagina, accorcia. Applica la revisione linguistica di SKILL.md ai testi.

## 8. Riepilogo della classe

Per ogni versione crea `risultati/correzioni.json` e lancia, dalla radice della skill:

```
python scripts/correzione.py <versione>/registro_evidenze.xlsx <versione>/risultati/correzioni.json <versione>/risultati/riepilogo_voti.xlsx <versione>/risultati/correttore_alunni.xlsx
```

`correttore_alunni.xlsx` è il registro della versione (stesso foglio e formattazione del correttore) con una colonna in più per alunno, in ordine alfabetico, e nelle celle la percentuale 0–100 come numero assoluto per ogni evidenza, già con i minimi del §4 (non svolta 10, tentata o parziale mai sotto 20), quindi uguale ai punti usati per il voto. Non è un registro valido per `check`: non sostituirlo al registro approvato.

Fogli: **Voti** (da mostrare alla classe: punti per esercizio, totale, voto ed equivalente decimale, media e sufficienti, nomi con link alla scheda), **Dettaglio** (solo docente: percentuale per evidenza, unico posto da modificare) e **Punti** (formule). Ricalcola con LibreOffice headless e controlla che i voti coincidano con le schede e che ogni link punti a un file esistente. Più versioni: un riepilogo per versione; nel resoconto confronta le medie e segnala differenze di almeno un voto.

## 8bis. Fascicolo stampabile

Dopo il riepilogo e con tutte le schede in `risultati/`, aggiungi `classe` e `data` a `correzioni.json` e lancia:

```
python scripts/fascicolo.py <versione>/registro_evidenze.xlsx <versione>/risultati/correzioni.json <versione>/risultati/
```

Crea in `risultati/`:
- `copertina.pdf` (una pagina): titolo, classe, data, numero di alunni; tabella alunno, punti per esercizio, totale, voto (giallo); media della classe, nota con la formula e i sufficienti;
- `Schede_complete.pdf`: copertina e schede in ordine alfabetico, con piè di pagina «argomento — classe — data — pag. n di N»;
- `Schede_complete_fronteretro.pdf`: come sopra, con una pagina bianca (senza numero, ma conteggiata in N) dopo la copertina e dopo ogni scheda di pagine dispari, così ogni scheda inizia sul fronte di un foglio.

Richiede `pdflatex` con `pdfpages` e `pdfinfo`. Se la copertina supera una pagina o manca una scheda, lo script si ferma e lo dice. Controlla l'anteprima di copertina e prime pagine. Valori ricalcolati da `correzioni.json` con le stesse funzioni del riepilogo, quindi coincidono. Dopo modifiche a schede o punteggi rigenera: se toccano i voti, rifai prima il riepilogo.

## 9. Note e resoconto

In `risultati/note_correzione.md` annota: esercizi non trovati (foglio mancante), asterischi senza seguito, parti illeggibili, **risposte identiche o quasi tra alunni diversi** (chi e quali esercizi), risultati giusti con passaggi sbagliati.

In chat basta: voti per alunno, media, numero di sufficienti, casi da controllare. Nessun elenco dei passaggi.

## 10. Aggiornamenti

Pagine mancanti o punteggi cambiati: aggiorna `correzioni.json`, riscrivi scheda dell'alunno e riepilogo, aggiorna le note e conferma i nuovi voti.
