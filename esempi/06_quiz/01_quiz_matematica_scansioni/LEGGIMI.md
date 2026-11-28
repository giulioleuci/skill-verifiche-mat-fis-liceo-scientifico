# Quiz di matematica con scansioni

`domande.xlsx` (10 domande, 2 con versioni alternative) -> `quiz.py genera` (4 varianti) -> fogli compilati a mano simulati in `scansioni/` (PDF singoli, un PDF fronte-retro intero, un JPG da foto, uno capovolto, una foto ritagliata e quindi non leggibile) -> `quiz.py leggi` (`quiz_out/risposte_scansioni.xlsx`, `quiz_out/letture/`) -> `quiz.py correggi` (`quiz_out/quiz_risultati.xlsx`).

Il nome è precompilato dal nome del file; l'agente lo confronta con `letture/Sxx_nome.png`. Anomalie della lettura automatica: `anomalie_lettura.txt` (Gamma Chiara: domanda 3 annullata, 6 proposta C per la gomma, 7 proposta A per un segno debole; Theta Hugo: domanda 8 annullata; la foto di Iota Ilaria non è leggibile perché ritagliata: l'agente chiede al docente una nuova foto e non corregge quel foglio).

`quiz.py rivedi` apre l'editor nel browser: il docente conferma le proposte, lascia annullata la 3 di Gamma Chiara (`*`: 0 punti con `--annullata 0`) e segna a mano B alla 8 di Theta Hugo. L'esempio applica le stesse modifiche dallo script; il risultato è in `quiz_out/letture/letture.json` e `risposte_scansioni.xlsx`. Il quiz è generato con `--errata -1 --annullata 0 --minimo 0` (il totale non scende sotto 0) e la domanda D04 ha `Alternative fisse` = 1: «nessuna delle precedenti» resta sempre in fondo.
