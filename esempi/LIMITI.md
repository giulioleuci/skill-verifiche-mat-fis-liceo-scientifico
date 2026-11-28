# Limiti noti degli esempi

- **OpenDyslexic**: il font non è installato in questo ambiente. `01_matematica_rette/prove/prova_adattata_DSA_opendyslexic.tex` è consegnato solo come sorgente (XeLaTeX o LuaLaTeX con `fontspec`, solo il testo; formule in Palatino). Comando effettivo: `xelatex prova_adattata_DSA_opendyslexic.tex` due volte, dopo aver installato il font. Nessun PDF è dichiarato compilato.
- **Scansioni e scrittura a mano**: sono simulate (font corsivo, disturbi, rotazioni, ombre, foto con prospettiva). Servono a esercitare i flussi di lettura e correzione, non a misurare l'accuratezza su grafie reali.
- **Alunni fittizi**: tutti i nomi sono inventati; nessun dato reale entra nel repository.
- **Percentuali di correzione** (`correzione/elaborati.py`): sono scelte dell'esempio per mostrare errori, errore trascinato, parti in bianco e cancellature; non sono una taratura didattica.
- **`riepilogo_voti.xlsx`** contiene formule senza valori memorizzati (come scrive la skill): `genera_esempi.py` li ricalcola con LibreOffice in una cartella temporanea e confronta i voti con `correzione.voto()`.
