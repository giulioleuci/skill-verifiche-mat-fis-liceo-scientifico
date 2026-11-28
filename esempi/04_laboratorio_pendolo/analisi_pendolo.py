"""Analisi dei dati del pendolo semplice: T^2 = (4 pi^2 / g) L, g da regressione lineare con errore.
Esecuzione: python3 analisi_pendolo.py  (stampa i risultati e fallisce se un controllo non torna)"""
import csv
from math import pi, sqrt
from pathlib import Path

import numpy as np

righe = list(csv.DictReader(open(Path(__file__).with_name("dati_pendolo.csv"))))
L = np.array([float(r["L_m"]) for r in righe])
T = np.array([float(r["t10_s"]) for r in righe]) / 10     # periodo da 10 oscillazioni
sT = 0.2 / 10                                             # errore sul tempo: 0,2 s su 10 oscillazioni
T2, sT2 = T**2, 2 * T * sT                                # propagazione: s(T^2) = 2 T s(T)
(a, b), cov = np.polyfit(L, T2, 1, cov=True)              # T^2 = a L + b
g = 4 * pi**2 / a
sg = g * sqrt(cov[0, 0]) / a                              # s(g) = g * s(a) / a
print(f"T^2 = ({a:.3f} ± {sqrt(cov[0, 0]):.3f}) s^2/m * L + ({b:.3f} ± {sqrt(cov[1, 1]):.3f}) s^2")
print(f"g = {g:.2f} ± {sg:.2f} m/s^2; periodi: {np.round(T, 3).tolist()}; s(T^2): {np.round(sT2, 3).tolist()}")
assert abs(g - 9.81) < 3 * sg, "g compatibile con 9,81 entro 3 sigma"
assert abs(b) < 3 * sqrt(cov[1, 1]), "intercetta compatibile con zero"
