# verifiche-mat-fis

`verifiche-mat-fis` è una skill per assistere i docenti della scuola secondaria di secondo grado (liceo scientifico) nella progettazione di prove di matematica e fisica. Supporta la creazione di nuove verifiche, prove di recupero, varianti ordinarie e adattate, correttori con evidenze e punteggi, oltre alla gestione dei materiali di progetto.

## Installazione

Occorrono Bash, `python3` e `realpath`. Da un terminale, nella cartella che contiene questo README, esegui:

```bash
./installa-verifiche-mat-fis.sh
```

Lo script installa o aggiorna la skill nelle cartelle standard sotto la home: `.claude/skills`, `.codex/skills`, `.config/opencode/skills` e `.agents/skills`. Un aggiornamento sostituisce l'intero contenuto della skill installata: conserva prima eventuali modifiche locali. Per scegliere una sola destinazione, indicando la cartella finale della skill:

```bash
./installa-verifiche-mat-fis.sh --dest "$HOME/.codex/skills/verifiche-mat-fis"
```

Sono disponibili anche le modalità `install` (solo destinazione vuota) e `update` (solo installazione riconosciuta), ad esempio `./installa-verifiche-mat-fis.sh update`. Per tutte le opzioni: `./installa-verifiche-mat-fis.sh --help`. In alternativa copia l'intera cartella `verifiche-mat-fis/` nella directory delle skill del tuo assistente. Riavvia l'assistente se necessario per rendere disponibile la skill.

## Requisiti per l'uso

- Un assistente compatibile con le skill, con accesso ai file della skill e alla cartella di lavoro.
- Python 3 e `openpyxl` per i registri Excel. Installa la dipendenza nell'ambiente Python usato dall'assistente:

  ```bash
  python3 -m pip install -r verifiche-mat-fis/requirements.txt
  ```

- Per ottenere PDF, una distribuzione LaTeX con `pdflatex` e i pacchetti richiesti dal preambolo, tra cui la classe `exam`, `newpxtext`, `newpxmath`, `siunitx`, `physics`, `tcolorbox` e `tikz`. Le dipendenze esatte dipendono dal documento generato. Se si sceglie esplicitamente OpenDyslexic, servono il font installato, `fontspec` e XeLaTeX o LuaLaTeX. Se la compilazione non è possibile, l'assistente consegna i sorgenti e indica il limite e il comando di compilazione.

## Comandi e fasi di lavoro

Questi sono **comandi da scrivere all'assistente**, anche all'interno di una frase; non sono comandi da eseguire nel terminale. Indica materia, classe, argomenti e vincoli già noti: l'assistente chiederà i dati mancanti.

| Fase | Comando | Cosa fa |
|---|---|---|
| Progettazione | `nuova-verifica` | Prepara la scaletta di una nuova prova. |
| Progettazione | `recupero` | Prepara una prova di recupero mirata. |
| Dopo lo standard | `varianti` | Deriva varianti ordinarie e, con approvazione distinta, prove adattate. |
| Correttore | `correttore` | Prepara evidenze e registro Excel della prova. |
| Dopo l'approvazione del registro | `genera-correttore` | Produce correttore docente e svolgimento studenti. |
| Aggiornamento | `rigenera-correttore` | Applica modifiche al registro e note del docente ai documenti. |
| Durante il progetto | `stato`, `confronta`, `copertura` | Riprendono il lavoro, confrontano revisioni e verificano la copertura. |
| Controllo e consegna | `verifica-calcoli`, `compila` | Verificano i calcoli con script riproducibili e compilano i documenti. |
| In qualsiasi momento | `aiuto` | Mostra i comandi pertinenti. |

Per esempio: «`nuova-verifica`: prepara una verifica di matematica per una terza su equazioni e disequazioni, durata 100 minuti». L'assistente propone una scaletta e attende la tua approvazione esplicita prima di generare il LaTeX. Per il correttore, fornisci la prova con `correttore`, verifica il registro e approvalo esplicitamente prima di chiedere `genera-correttore`. Le approvazioni si riferiscono alla revisione esaminata.

Le guide complete sono in [uso del generatore](verifiche-mat-fis/references/verifiche/uso.md), [uso del correttore](verifiche-mat-fis/references/correttori/uso.md) e [SKILL.md](verifiche-mat-fis/SKILL.md).

## Preferenze dell’autore

La skill è stata costruita a partire dalle preferenze personali dell’autore in materia di valutazione e scrittura dei compiti. Queste preferenze informano, tra l’altro, la struttura delle prove, l’uso di evidenze e punteggi, il processo di approvazione, la preparazione dei correttori e lo stile dei documenti. Vanno intese come impostazioni di lavoro dell’autore, adattabili alle indicazioni del docente che usa la skill.

## Generazione di questo README

Questo README è stato generato da **GPT-6**.
