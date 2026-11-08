---
name: verifiche-mat-fis
description: Da usare quando un docente richiede verifiche scritte, compiti in classe, varianti Fila A/B, recuperi, correttori, evidenze, punteggi o griglie di matematica, fisica o laboratorio per la scuola secondaria di secondo grado.
---

# verifiche-mat-fis

Rispondi in italiano, con frasi dirette e concise. Individua prima comando, materia e anno dalla richiesta e dal contesto disponibile; chiedi soltanto i dati mancanti. Riusa preferenze, materiali e approvazioni già acquisiti. Tutti i percorsi sono relativi alla skill; la fonte modificabile è questa cartella, non le esportazioni o gli archivi storici.

## Comandi e letture

| Comando | Procedura da leggere |
|---|---|
| `nuova-verifica`, `recupero` | [Flusso generatore](references/verifiche/flusso_generatore.md); scheda pertinente in `references/verifiche/` |
| `varianti` | Flusso generatore e [regole varianti e prove adattate](references/verifiche/02_guida_varianti.md) |
| `correttore` | [Flusso correttore](references/correttori/flusso_correttore.md), poi soltanto i riferimenti indicati per la fase |
| `genera-correttore`, `rigenera-correttore` | Flusso correttore, registro approvato e [macro e impaginazione](references/correttori/04_template_correttore.md) |
| `stato`, `confronta`, `copertura` | [Progetto, revisioni e matrice di copertura](references/progetto.md) |
| `verifica-calcoli` | Esegui e conserva accanto alla prova gli script Python che riproducono ogni passaggio quantitativo; confronta risultati, unità, domini e ordini di grandezza |
| `compila` | Usa il motore del preambolo; verifica dipendenze e PDF; due passate per correttore e svolgimento |
| `aiuto` | Elenca i comandi pertinenti; guide [generatore](references/verifiche/uso.md) e [correttore](references/correttori/uso.md) |

Non caricare tutte le schede né tutti gli elenchi. Identificate materia e anno, leggi soltanto la scheda del flusso in corso, la base di materia collegata e l'elenco predefinito pertinente in `references/argomenti/argomenti_<materia>_classe<N>.md` (per esempio `argomenti_matematica_classe3.md`). Per prove miste leggi solo gli elenchi delle materie coinvolte. Presenta l'elenco come proposta precompilata e lascia sempre al docente la possibilità di selezionare, rimuovere, aggiungere o rinominare argomenti; una modifica per la singola prova non aggiorna il file predefinito, salvo richiesta esplicita. Se materia o anno non sono noti, chiedi prima di caricare l'elenco. L'elenco predefinito non attesta che gli argomenti siano stati effettivamente svolti: per l'anno in corso usa quanto confermato dal docente e chiedi conferma solo dei punti non attestati; per gli anni precedenti usa i contenuti disponibili salvo dubbi specifici.

## Vincoli essenziali

- LaTeX della prova soltanto dopo l'approvazione esplicita della sua scaletta; LaTeX del correttore soltanto dopo l'approvazione esplicita del suo registro. Collega l'approvazione alla revisione precisa in [progetto](references/progetto.md). Il silenzio non approva. Un'approvazione già acquisita resta valida sulla stessa revisione.
- Prima gli standard e le varianti ordinarie, poi le prove adattate con approvazione distinta. Le prove adattate ereditano le scelte approvate; cambiamenti dello standard richiedono il riallineamento dei derivati interessati.
- Ogni versione ha **da 1 a 40 evidenze complessive**, massimi interi positivi, somma **1000**. Ogni evidenza ha ID stabile, esercizio, punto/gruppo, un indicatore ANA/SVI/ARG/COM e un ID argomento dell'elenco del docente. Calibrazione su prestazione Base concreta facoltativa, mai obbligatoria.
- Per matematica in terza, quarta e quinta, durata **almeno 100 minuti**: formato predefinito di **un problema in 3 o 4 punti e 3 o 4 quesiti singoli senza sottopunti**, modificabile dal docente. Se i punti del problema dipendono fra loro, chiedi se fornire risultati intermedi e attendi la scelta, salvo scelta già acquisita. I risultati intermedi concordati e i supporti generali esplicitamente approvati fanno eccezione al divieto di riportare risultati o formule di aiuto; il correttore non li valuta come scelte autonome.
- Proponi sempre costanti e formule utili con un elenco **numerato** e attendi la conferma esplicita delle voci da inserire; usa i nomi delle costanti, non i simboli. Catalogo fisica, formule di quarta e regole in [supporti della prova](references/verifiche/supporti_prova.md). Inserisci solo i contenuti confermati dopo `\vfill` e prima degli identificativi studente.
- Chiama **prove adattate** le personalizzazioni per BES, inclusi DSA, e per esigenze di tempo. Chiedi se servono un formulario o una mappa concettuale specifica e concordane i contenuti; mantieni sempre difficoltà, argomenti e profondità dello standard.
- Prove senza soluzioni, titolo, materia o fila nel documento, monocromatiche; usa [modello canonico](assets/modello_verifica.tex). I colori ANA/SVI/ARG/COM appartengono al correttore docente.
- Compila di norma con `pdflatex`. OpenDyslexic richiede scelta esplicita per il solo testo dei documenti concordati, font verificato e XeLaTeX/LuaLaTeX con `fontspec`. Nessuna sostituzione silenziosa; se non puoi compilare consegna sorgenti e comando effettivo, indicando il limite.
- Non chiedere dati personali degli studenti. Se una richiesta è ambigua o incoerente, chiarisci solo ciò che impedisce il lavoro.
- Prima della consegna applica `humanizer:humanizer` se disponibile; altrimenti svolgi la stessa revisione manuale: frasi dirette, verbi concreti, niente enfasi, riempitivi o trattini lunghi nella prosa. Conserva formule, dati, criteri, unità e vincoli. Controlla anche il testo estratto dal PDF.
