# LaTeX: regole comuni e compilazione

Leggi questo file solo quando generi o compili i documenti; i vincoli specifici stanno nel [generatore](generatore.md#vincoli-del-documento) per la prova e nel [correttore](correttore.md#documenti-latex) per correttore e svolgimento. Le fonti canoniche sono gli asset: [modello_verifica.tex](../assets/modello_verifica.tex), [correttore_template.tex](../assets/correttore_template.tex) e [svolgimento_studenti_template.tex](../assets/svolgimento_studenti_template.tex). Deriva sempre il codice da questi file, senza riprodurne qui il preambolo.

## Regole comuni

- Numeri e unità con `siunitx` e virgola decimale (`\SI`, `\si`, `\num`; nella prova anche `\um{valore}{unità}`); nelle formule una virgola letterale richiede graffe. Unità al termine dell’espressione, non su ogni fattore.
- Notazioni per classe (funzioni inverse, versori, modulo con `\norma{F}`, sistemi per componente) secondo i [criteri disciplinari](criteri_disciplinari.md#progressione-e-notazioni).
- Argomenti degli operatori sempre scritti; pedici testuali con `\pedice` o `\text`; simboli matematici in modalità matematica. Proteggi i caratteri speciali; un `\item` non inizia con una parentesi quadra non protetta. Formule lunghe in un ambiente su riga propria.
- Figure fisiche o geometriche con TikZ; grafici cartesiani con pgfplots, con assi orientati, scale, etichette e virgola decimale.
- Codice completo di preambolo e `\end{document}`, compilabile con `pdflatex` senza dipendenze esterne non standard, salvo la scelta esplicita di OpenDyslexic (§Compilazione).

## Compilazione

- Motore ordinario `pdflatex`, con due passate per correttore e svolgimento e anche per la prova, perché la classe `exam` risolve `\numpages` e i totali dei punti solo alla seconda passata.
- OpenDyslexic solo dopo scelta esplicita, per il solo testo dei documenti concordati: dichiara font e motore richiesti, verifica che il font sia installato e usa `fontspec` con XeLaTeX o LuaLaTeX. Il correttore docente conserva la configurazione ordinaria. Nessuna sostituzione silenziosa del font.
- Dopo la compilazione controlla PDF e testo estratto: formule, accenti, simboli, riferimenti, numerazione, pagine, grafici e spazio per le risposte; nella prova verifica che supporti e identificativi stiano insieme sul fondo dell’ultima pagina utile.
- Se mancano motore, pacchetti o font consegna i sorgenti e il comando effettivo, indicando il limite, senza dichiarare una compilazione non eseguita.
