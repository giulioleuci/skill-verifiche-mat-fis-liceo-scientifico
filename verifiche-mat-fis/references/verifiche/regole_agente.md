# Impaginazione delle verifiche

La procedura e le approvazioni sono nel [flusso generatore](flusso_generatore.md); qui sono mantenuti soltanto i vincoli del documento.

## Vincoli di consegna e LaTeX

1. **Zero soluzioni**: è categoricamente vietato inserire soluzioni, svolgimenti, risultati numerici nei testi o commenti. Il documento deve essere pronto per essere fotocopiato e consegnato agli studenti. Fanno eccezione i supporti generali esplicitamente confermati secondo i [supporti della prova](supporti_prova.md) e i risultati intermedi esplicitamente concordati per i punti dipendenti del problema, secondo il [flusso generatore](flusso_generatore.md); non includere il procedimento.
2. **DIVIETO ASSOLUTO DI INTESTAZIONI E METADATI SUPERFLUI**:
   - **NON inserire MAI** nel documento (né nell'intestazione, né nel corpo del testo, né nel piè di pagina):
     - La **materia** ;
     - Il **titolo della verifica** ;
     - L'indicazione della **fila** .
   - I comandi di testata devono essere sempre vuoti: `\firstpageheader{}{}{}` e `\runningheader{}{}{}`.
3. **Identificativi studente**: i campi studente (`Cognome e Nome: ... Classe: ... Data: ...`) devono essere formattati su riga aperta pulita con `\hrulefill`, **SENZA alcun box o riquadro** attorno ad essi.
4. **Modello di riferimento e tipografia**: derivare sempre il codice da `modello_verifica.tex`. Utilizzare di default il font Palatino con `newpxtext` e `newpxmath`; se il docente sceglie OpenDyslexic, applicarlo al testo della sola versione concordata seguendo [guida varianti](02_guida_varianti.md). Conservare tabelle ariose in stile `booktabs` (senza gabbie di righe verticali), badge compatto per la numerazione degli esercizi (`\badgeQ`), sottopunti con lettere in grassetto `\alph{partno})`, e box consegne a sfondo tenue (`gray!6`) senza intestazione "Istruzioni".
5. **Cromatismo rigorosamente monocromatico**: è fatto obbligo di utilizzare **esclusivamente toni di bianco, nero e sfumature di grigio** (`gray!30`, `black!75`, `black`). È vietato l'uso di qualsiasi colore primario o secondario (niente blu, rosso, verde, ecc.), garantendo massima resa e omogeneità in fotocopia.
6. **Griglie di valutazione e legenda**:
   - Nella griglia per competenze standard (`\grigliacompetenze`), posizionare la legenda dei giudizi (*N, Q, S, D, B, O*) **a destra della tabella** (affiancata orizzontalmente) per risparmiare spazio verticale, ed evidenziare con fondo grigio chiaro (`>{\columncolor{gray!16}}c`) la colonna della sufficienza (*S*).
   - Nelle verifiche di recupero (`\grigliarecupero`), **nascondere completamente la legenda**.
7. **Grafici TikZ**: tracciare grafici vettoriali puliti con assi orientati, etichette chiare, griglie di sfondo a tratti sottili grigi (`gray!30`) e curve/rette in nero pieno o tratteggio nero/grigio scuro (`line width=1.2pt`), senza alcun colore.
8. **Formattazione numerica e unità**: usare la virgola decimale e il pacchetto `siunitx` (macro `\um{valore}{unità}` o `\SI{valore}{unità}`).
9. **Autonomia del codice**: il codice generato deve essere completo di preambolo ed `\end{document}`, pronto per la compilazione con `pdflatex` senza dipendenze esterne non standard. Fa eccezione la scelta esplicita di OpenDyslexic: dichiarare font e motore richiesti, verificarne la disponibilità e seguire [guida varianti](02_guida_varianti.md).

10. **Supporti confermati in fondo alla prova**: dopo le consegne e fuori da `questions`, usa `\vfill`, quindi `\supportiprova{...}` solo con costanti/formule/supporti approvati e infine gli identificativi studente. Il blocco è monocromatico, non flottante e leggibile; usa il nome delle costanti, non il simbolo. Attendi la scelta esplicita prima di generare; ometti il blocco se il docente rifiuta i supporti. Segui il [catalogo e il flusso di conferma](supporti_prova.md), anche per varianti e prove adattate.
