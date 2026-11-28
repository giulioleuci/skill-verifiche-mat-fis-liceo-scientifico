"""verifica-calcoli: riproduce ogni passaggio quantitativo delle Fila A e B (Fractions, nessuna dipendenza).
Esecuzione: python3 verifica_calcoli.py  (stampa i risultati e fallisce se un controllo non torna)"""
from fractions import Fraction as F
from math import isqrt, sqrt


def retta(p, q):
    """Coefficienti (a, b, c) di ax + by + c = 0 per due punti, normalizzati a interi con a > 0."""
    a, b = q[1] - p[1], p[0] - q[0]
    c = -(a * p[0] + b * p[1])
    return a, b, c


def dist_pr(p, r):
    a, b, c = r
    return abs(a * p[0] + b * p[1] + c), a * a + b * b  # |num| e radicando del denominatore


def problema(A, B, C):
    r = retta(A, B)
    num, rad = dist_pr(C, r)
    ab2 = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2
    area = F(1, 2) * sqrt(ab2) * num / sqrt(rad)
    par = (r[0], r[1], -(r[0] * C[0] + r[1] * C[1]))  # parallela per C
    x_int = F(-par[2], par[0])
    return {"AB": r, "AB^2": ab2, "dist": (num, rad), "area": round(area, 9), "parallela": par, "x_int": x_int}


def quesito2(r_m, s_coef):
    """s: a(k) x + b(k) y + c = 0 con a = pa*k + qa, b = pb*k + qb; cerca k con m_s = -1/r_m."""
    (pa, qa), (pb, qb) = s_coef
    # -a/b = -1/m  =>  a*m = b  =>  (pa*k+qa)*m = pb*k+qb
    return F(qb - qa * r_m, pa * r_m - pb)


def asse(P, Q):
    M = (F(P[0] + Q[0], 2), F(P[1] + Q[1], 2))
    m = F(-(Q[0] - P[0]), Q[1] - P[1])  # perpendicolare a PQ
    a, b, c = m, -1, M[1] - m * M[0]
    return M, (a, b, c)


def fascio(g1, g2, k_pt=None, par_x=False):
    """k*g1 + g2 = 0; centro come intersezione; k per il punto richiesto; k della parallela all'asse x."""
    (a1, b1, c1), (a2, b2, c2) = g1, g2
    det = a1 * b2 - a2 * b1
    cx, cy = F(b1 * c2 - b2 * c1, det), F(c1 * a2 - c2 * a1, det)
    out = {"centro": (cx, cy)}
    if k_pt:
        x, y = k_pt
        out["k_punto"] = F(-(a2 * x + b2 * y + c2), a1 * x + b1 * y + c1)
    if par_x:
        out["k_parallela"] = F(-a2, a1)
    return out


# Fila A
a = problema((-2, 1), (4, 3), (2, -3))
assert a["AB"] == (2, -6, 10) and a["AB^2"] == 40 and a["dist"] == (32, 40) and a["area"] == 16 and a["x_int"] == 11, a
assert quesito2(3, ((1, 0), (1, 1))) == F(1, 2)       # s: kx + (k+1)y - 5 = 0, r: m = 3
M, ax = asse((-1, 4), (5, 0))
assert M == (2, 2) and ax == (F(3, 2), -1, F(-1)), (M, ax)   # y = 3/2 x - 1  <=>  3x - 2y - 2 = 0
f = fascio((2, 1, 1), (-1, 2, -3), k_pt=(3, 0), par_x=True)
assert f == {"centro": (-1, 1), "k_punto": F(6, 7), "k_parallela": F(1, 2)}, f
# Fila B
b = problema((-1, -2), (5, 2), (3, -4))
assert b["AB"] == (4, -6, -8) and b["AB^2"] == 52 and b["dist"] == (28, 52) and b["area"] == 14 and b["x_int"] == 9, b
assert quesito2(-2, ((1, 0), (1, -1))) == F(1, 3)    # s: kx + (k-1)y + 4 = 0, r: m = -2
M, ax = asse((0, 5), (6, -1))
assert M == (3, 2) and ax == (1, -1, F(-1)), (M, ax)    # y = x - 1
f = fascio((2, -1, -5), (1, 3, 1), k_pt=(0, 4), par_x=True)
assert f == {"centro": (2, -1), "k_punto": F(13, 9), "k_parallela": F(-1, 2)}, f
print("ok: Fila A e B verificate")
