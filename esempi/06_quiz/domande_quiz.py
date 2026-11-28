"""Banche di domande per gli esempi di quiz (LaTeX nei testi). Ogni voce = un foglio Excel = una domanda;
ogni riga della lista = una versione alternativa. Riga: (testo, corretta, [alternative], extra) con extra opzionale
{'colonne': n, 'corretta': p, 'non_data': p, 'errata': p, 'ind': 'ANA'}."""

RETTE = [
 [(r"Qual è il coefficiente angolare della retta per $A(1,2)$ e $B(5,4)$?", r"$\frac12$", [r"$2$", r"$-\frac12$", r"$\frac32$"], {"colonne": 2}),
  (r"Qual è il coefficiente angolare della retta per $A(0,1)$ e $B(3,7)$?", r"$2$", [r"$\frac12$", r"$-2$", r"$3$"], {"colonne": 2})],
 [(r"Quale equazione rappresenta la retta per $P(0,3)$ con coefficiente angolare $-2$?", r"$y=-2x+3$", [r"$y=2x+3$", r"$y=-2x-3$", r"$y=3x-2$"], {})],
 [(r"La distanza fra $A(-1,2)$ e $B(2,6)$ è:", r"$5$", [r"$7$", r"$\sqrt{7}$", r"$25$"], {"colonne": 2})],
 [(r"Due rette di coefficienti angolari $m_1$ e $m_2$ sono perpendicolari se:", r"$m_1m_2=-1$", [r"$m_1m_2=-1$", r"$m_1=m_2$", r"$m_1m_2=1$", "nessuna delle precedenti"], {"fisse": 1})],
 [(r"La retta $2x-3y+6=0$ interseca l'asse $y$ nel punto:", r"$(0,2)$", [r"$(0,-2)$", r"$(3,0)$", r"$(-3,0)$"], {"colonne": 2}),
  (r"La retta $3x-2y+8=0$ interseca l'asse $y$ nel punto:", r"$(0,4)$", [r"$(0,-4)$", r"$(\!-\frac83,0)$", r"$(\frac83,0)$"], {"colonne": 2})],
 [(r"Il punto medio del segmento di estremi $(2,-4)$ e $(6,2)$ è:", r"$(4,-1)$", [r"$(4,-3)$", r"$(2,3)$", r"$(8,-2)$"], {"colonne": 2})],
 [(r"La distanza del punto $(0,0)$ dalla retta $3x+4y-10=0$ è:", r"$2$", [r"$10$", r"$\frac{10}{7}$", r"$\frac{7}{5}$"], {"colonne": 2, "corretta": 6})],
 [(r"Quale retta è parallela a $y=3x-1$?", r"$6x-2y+5=0$", [r"$x+3y=0$", r"$3x+y-1=0$", r"$y=-\frac13x$"], {})],
 [(r"Il centro del fascio $k(x+y)+(x-y-2)=0$ è:", r"$(1,-1)$", [r"$(-1,1)$", r"$(2,0)$", r"$(0,-2)$"], {"colonne": 2})],
 [(r"L'asse del segmento di estremi $(0,0)$ e $(4,0)$ è:", r"$x=2$", [r"$y=2$", r"$x=4$", r"$y=0$"], {"colonne": 2})],
]

URTI = [
 [(r"In un urto completamente anelastico fra due corpi su un piano liscio si conserva:", r"la quantità di moto totale", [r"l'energia cinetica totale", r"la velocità di ciascun corpo", r"la quantità di moto di ciascun corpo"], {"ind": "ANA"}),
  (r"In un urto elastico si conserva, oltre alla quantità di moto:", r"l'energia cinetica totale", [r"la massa di ciascun corpo", r"la velocità del centro di massa e basta", r"nulla"], {"ind": "SVI"})],
 [(r"Un carrello di $\um{2}{kg}$ a $\um{3}{m/s}$ si aggancia a uno fermo di $\um{1}{kg}$. La velocità finale è:", r"$\um{2}{m/s}$", [r"$\um{3}{m/s}$", r"$\um{1}{m/s}$", r"$\um{1.5}{m/s}$"], {"ind": "SVI", "colonne": 2}),
  (r"Un carrello di $\um{3}{kg}$ a $\um{4}{m/s}$ si aggancia a uno fermo di $\um{1}{kg}$. La velocità finale è:", r"$\um{3}{m/s}$", [r"$\um{4}{m/s}$", r"$\um{1}{m/s}$", r"$\um{2}{m/s}$"], {"ind": "ANA", "colonne": 2})],
 [(r"L'energia cinetica dissipata nell'urto completamente anelastico precedente è sempre:", r"positiva o nulla", [r"negativa", r"uguale all'energia finale", r"sempre nulla"], {"ind": "ANA"})],
 [(r"Un proiettile di $\um{10}{g}$ a $\um{300}{m/s}$ si conficca in un blocco fermo di $\um{2.99}{kg}$. La velocità subito dopo è:", r"$\um{1}{m/s}$", [r"$\um{300}{m/s}$", r"$\um{0.1}{m/s}$", r"$\um{10}{m/s}$"], {"ind": "SVI", "colonne": 2})],
 [(r"Un corpo $m$ urta elasticamente un corpo fermo di massa uguale. Dopo l'urto:", r"il primo si ferma e il secondo prende la sua velocità", [r"i due procedono uniti", r"il primo rimbalza con la stessa velocità", r"entrambi si fermano"], {"ind": "ARG"})],
 [(r"Nel pendolo balistico l'energia meccanica si conserva:", r"solo dopo l'urto", [r"durante l'urto", r"prima dell'urto soltanto", r"mai"], {"ind": "ANA"})],
 [(r"Quale grandezza ha le stesse dimensioni della quantità di moto?", r"l'impulso", [r"l'energia", r"la potenza", r"la forza"], {"ind": "COM"})],
 [(r"Dopo un urto elastico in una dimensione fra masse diverse, la velocità relativa dei due corpi:", r"cambia segno e mantiene il modulo", [r"si dimezza", r"resta uguale", r"si annulla"], {"ind": "ARG"})],
]
