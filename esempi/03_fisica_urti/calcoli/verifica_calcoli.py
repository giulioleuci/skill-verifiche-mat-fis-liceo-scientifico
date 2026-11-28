"""verifica-calcoli: riproduce i passaggi quantitativi della prova di fisica (SI, g = 9,81 m/s²).
Esecuzione: python3 verifica_calcoli.py (fallisce se un controllo non torna)"""
from math import isclose, sqrt

g = 9.81
# Es. 1: urto completamente anelastico
m1, v1, m2 = 0.50, 4.0, 1.5
V = m1 * v1 / (m1 + m2)
Ki, Kf = 0.5 * m1 * v1**2, 0.5 * (m1 + m2) * V**2
assert isclose(V, 1.0) and isclose(Ki, 4.0) and isclose(Kf, 1.0) and isclose(Ki - Kf, 3.0)
# Es. 2: urto elastico unidimensionale
m1, v1, m2 = 2.0, 4.0, 3.0
u1, u2 = (m1 - m2) / (m1 + m2) * v1, 2 * m1 / (m1 + m2) * v1
assert isclose(u1, -0.8) and isclose(u2, 3.2)
assert isclose(m1 * v1, m1 * u1 + m2 * u2) and isclose(0.5 * m1 * v1**2, 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2)  # 16 J
# Es. 3: pendolo balistico
m, M, h = 0.020, 1.980, 0.100
Vb = sqrt(2 * g * h)
v = (m + M) / m * Vb
assert isclose(Vb, 1.4007, abs_tol=1e-4) and isclose(v, 140.07, abs_tol=0.01)
print(f"ok: V' = {V:.2f} m/s, dK = {Ki - Kf:.1f} J; u1 = {u1:.2f}, u2 = {u2:.2f} m/s; V = {Vb:.3f} m/s, v = {v:.0f} m/s")
