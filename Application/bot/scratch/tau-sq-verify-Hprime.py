"""
Cross-check H'(1) via finite difference of log H(s) at s = 1 +/- eps,
and extend the asymptotic to c_1 (third Laurent coefficient A_1).
"""
import math
from sympy import primerange

PMAX = 10**6  # smaller for finite-difference cross-check
primes = list(primerange(2, PMAX+1))

def H_at(s):
    """Truncated H(s) Euler product."""
    val = 1.0
    for p in primes:
        if p == 2:
            val *= (1 + 3 * 2**(-s)) * (1 - 2**(-s))**3
        elif p % 4 == 3:
            val *= (1 - p**(-2*s))**3
        else:  # p % 4 == 1
            x = p**(-s)
            val *= (1 + 4*x - x*x) * (1 - x)**4
    return val

eps = 1e-5
H_minus = H_at(1 - eps)
H_at1   = H_at(1.0)
H_plus  = H_at(1 + eps)
Hprime_fd = (H_plus - H_minus) / (2*eps)
print(f"H(1) (Euler product up to 10^6): {H_at1:.10f}")
print(f"H'(1) via central FD:            {Hprime_fd:.6f}")
print(f"H'(1)/H(1) via FD:               {Hprime_fd/H_at1:.6f}")

# Compare to analytic computation
def dlog_H_factor(p):
    lp = math.log(p)
    if p == 2:
        return 2.4 * lp
    if p % 4 == 3:
        return 6 * lp / (p*p - 1)
    if p % 4 == 1:
        return lp * (22*p - 6) / ((p-1) * (p*p + 4*p - 1))
    raise ValueError

dlogH = sum(dlog_H_factor(p) for p in primes)
print(f"sum_p H'_p/H_p (analytic):       {dlogH:.6f}")
print(f"H'(1) analytic = H(1) * sum:     {H_at1 * dlogH:.6f}")
print()

# Tail estimate beyond PMAX
# For split p (~half of all p): term ~ 22 log p / p^2
# Sum over p > PMAX, p ≡ 1 (4): ~ integral 22 log x / x^2 / (2 ln x) dx from PMAX
#   = 11 / PMAX  approximately
# Plus inert: 6 log p / p^2, similar.
# Total tail ~ 11/PMAX + 3/PMAX = 14/PMAX, e.g. 1.4e-5 at PMAX=10^6.
# So H'(1) is precise to ~5 decimals at PMAX=10^7.

# ---------- Compute c_1 prediction ----------
# c_1 = 2 A_1
# A_1 = 3R(R beta_K + gamma_K^2) H_0 + 3 R^2 gamma_K H_1 + R^3 H_2
# beta_K = L''(1, chi_4)/2 + gamma * L'(1, chi_4) - gamma_1 * L(1, chi_4)
# where gamma_1 is the first Stieltjes constant (~ -0.07282)
# H_2 = H''(1)/2

import mpmath as mp
mp.mp.dps = 30

R = math.pi / 4
gamma_E = 0.5772156649015329
gamma_1_stieltjes = -0.07281584548367672  # first Stieltjes constant

# L'(1, chi_4) and L''(1, chi_4) via mpmath
L_chi4 = lambda s: mp.dirichlet(s, [0, 1, 0, -1])
Lp = float(mp.diff(L_chi4, 1, 1))  # first derivative
Lpp = float(mp.diff(L_chi4, 1, 2))  # second derivative
L1 = float(L_chi4(1))
print(f"L(1, chi_4)  = {L1:.10f}  (should be pi/4 = {math.pi/4:.10f})")
print(f"L'(1, chi_4) = {Lp:.10f}")
print(f"L''(1, chi_4)= {Lpp:.10f}")

gamma_K = Lp + gamma_E * R
beta_K = Lpp / 2 + gamma_E * Lp - gamma_1_stieltjes * R
print(f"gamma_K = {gamma_K:.10f}")
print(f"beta_K  = {beta_K:.10f}")

# H_2 = H''(1)/2 -- compute via finite difference
H_2nd_fd = (H_plus - 2*H_at1 + H_minus) / eps**2
H2 = H_2nd_fd / 2
print(f"H''(1)/2 ≈ {H2:.6f}  (via FD)")

# H_1 from analytic
H1 = H_at1
H1prime = H1 * dlogH
print(f"H(1) = {H1:.10f}")
print(f"H'(1) = {H1prime:.10f}")
print(f"H_2 = {H2:.10f}")

# A_1 components
A1_a = 3 * R * (R * beta_K + gamma_K**2) * H1
A1_b = 3 * R**2 * gamma_K * H1prime
A1_c = R**3 * H2
A1 = A1_a + A1_b + A1_c
print(f"A_1 contributions: a={A1_a:.6f}, b={A1_b:.6f}, c={A1_c:.6f}")
print(f"A_1 = {A1:.6f}")
print(f"c_1 = 2 A_1 = {2*A1:.6f}")
print()

# Now redo full fit with predicted c_3, c_2, c_1
A3 = R**3 * H1
A2 = 3 * R**2 * gamma_K * H1 + R**3 * H1prime
c3 = 4*A3/3
c2 = 2*A2
c1 = 2*A1

# Empirical S(N) data
empirical = [
    (10**3,       86384),
    (10**4,     1614068),
    (10**5,    26859868),
    (3*10**5, 100153656),
    (10**6,   415319768),
]

import numpy as np
xs = np.array([math.log(N) for N, _ in empirical])
ys = np.array([S/(N*math.log(N)**3) for N, S in empirical])

print("Predicted c_3, c_2, c_1:")
print(f"  c_3 = {c3:.6f}")
print(f"  c_2 = {c2:.6f}")
print(f"  c_1 = {c1:.6f}")
print()

# Fit y = c3 + a/x + b/x^2 + c/x^3 with c_3 fixed at predicted
ys_resid = ys - c3
A_mat = np.column_stack([1/xs, 1/xs**2, 1/xs**3])
coefs, *_ = np.linalg.lstsq(A_mat, ys_resid, rcond=None)
print(f"With c_3 fixed at {c3:.6f}: empirical fit:")
print(f"  c_2 = {coefs[0]:.6f}  (predicted {c2:.6f}, ratio {coefs[0]/c2:.4f})")
print(f"  c_1 = {coefs[1]:.6f}  (predicted {c1:.6f}, ratio {coefs[1]/c1:.4f})")
print(f"  c_0 = {coefs[2]:.6f}  (no closed-form prediction here)")
print()

# Show residuals from full prediction
print("Full prediction comparison:")
print(f"{'N':>10} {'S(N)':>15} {'pred(c3+c2/L+c1/L^2)':>22} {'ratio':>10}")
for N, S in empirical:
    L = math.log(N)
    pred = N * (c3 * L**3 + c2 * L**2 + c1 * L)
    print(f"{N:>10} {S:>15} {pred:>22.0f} {S/pred:>10.6f}")
