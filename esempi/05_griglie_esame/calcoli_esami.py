"""verifica-calcoli delle tre prove d'esame (matematica, fisica, mista). Esecuzione: python3 calcoli_esami.py"""
from math import e, exp, isclose, pi, sqrt

import numpy as np
import sympy as sp

# --- Matematica: f(x) = x e^{-x}
x = sp.symbols("x", real=True)
f = x * sp.exp(-x)
assert sp.limit(f, x, sp.oo) == 0 and sp.limit(f, x, -sp.oo) == -sp.oo
d1, d2 = sp.simplify(sp.diff(f, x)), sp.simplify(sp.diff(f, x, 2))
assert sp.simplify(d1 - (1 - x) * sp.exp(-x)) == 0 and sp.simplify(d2 - (x - 2) * sp.exp(-x)) == 0
assert sp.solve(d1, x) == [1] and sp.simplify(f.subs(x, 1) - 1 / sp.E) == 0 and sp.simplify(f.subs(x, 2) - 2 / sp.E**2) == 0
area = sp.integrate(f, (x, 0, 1))
assert sp.simplify(area - (1 - 2 / sp.E)) == 0 and isclose(float(area), 0.26424, abs_tol=1e-5)
r1 = sp.nsolve(f - sp.Rational(1, 4), x, 0.3); r2 = sp.nsolve(f - sp.Rational(1, 4), x, 2.5)
assert 0 < r1 < 1 < 2 < r2 < 3 and f.subs(x, 2) > sp.Rational(1, 4) > f.subs(x, 3)
print(f"matematica: area = {float(area):.4f}; soluzioni di f = 1/4: {float(r1):.4f} e {float(r2):.4f}")

# --- Fisica: molla, F = k x
F = np.array([0.5, 1.0, 1.5, 2.0, 2.5]); X = np.array([0.021, 0.040, 0.062, 0.081, 0.101])
(k, b), cov = np.polyfit(X, F, 1, cov=True)
sk = sqrt(cov[0, 0])
m, A = 0.50, 0.050
T, w = 2 * pi * sqrt(m / k), sqrt(k / m)
vmax, E = A * w, 0.5 * k * A**2
assert isclose(k, 24.9, abs_tol=0.2) and abs(b) < 3 * sqrt(cov[1, 1]) and isclose(T, 0.891, abs_tol=0.01), (k, b, T)
assert isclose(E, 0.5 * m * vmax**2)  # energia meccanica = energia cinetica massima
print(f"fisica: k = {k:.1f} ± {sk:.1f} N/m, T = {T:.3f} s, w = {w:.2f} rad/s, vmax = {vmax:.3f} m/s, E = {E:.4f} J")

# --- Mista: caduta con resistenza viscosa, v(t) = (m g / b)(1 - e^{-b t / m})
m, bb, g = 0.50, 2.0, 9.81
vt, tau = m * g / bb, m / bb
v = lambda t: vt * (1 - exp(-t / tau))
dati = [(0.1, 0.81), (0.2, 1.35), (0.4, 1.95), (0.6, 2.23), (0.8, 2.35)]
assert all(abs(v(t) - y) < 0.01 for t, y in dati) and isclose(vt, 2.4525) and isclose(tau, 0.25)
s1 = vt * (1 - tau * (1 - exp(-1 / tau)))
assert isclose(s1, 1.8506, abs_tol=1e-3) and s1 < 0.5 * g  # meno dei 4,905 m della caduta libera
print(f"mista: vt = {vt:.4f} m/s, tau = {tau} s, s(1 s) = {s1:.4f} m (caduta libera {0.5 * g:.3f} m)")
