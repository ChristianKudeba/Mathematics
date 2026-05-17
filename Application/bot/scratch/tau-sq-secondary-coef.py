"""
Compute the secondary coefficient c_2 in the asymptotic
    S(N) = sum_{n<=N} tau(n^2+1)^2 ~ c_3 N log^3 N + c_2 N log^2 N + c_1 N log N + c_0 N

where c_2 = 2 A_2 = 6 R^2 gamma_K H(1) + 2 R^3 H'(1),  R = pi/4.

Then refit empirical S(N) data to test the prediction.
"""
import math
from sympy import primerange

# ---------- L'(1, chi_4) via direct alternating series ----------
# L(s, chi_4) = sum_{n>=0} (-1)^n / (2n+1)^s
# L'(s, chi_4) = -sum_{n>=0} (-1)^n log(2n+1) / (2n+1)^s
# At s=1, n=0 term vanishes.
# Series: log(3)/3 - log(5)/5 + log(7)/7 - log(9)/9 + ...
# Slowly convergent; use Euler / Cesaro accelerated sum or just a long tail.

def L_prime_chi4(N=10**7):
    # Alternating series; use averaging of partial sums for acceleration.
    # Actually use that the Abel summation / convergence is slow, so just sum a lot.
    s = 0.0
    for n in range(1, N+1):
        sign = 1 if n % 2 == 1 else -1
        m = 2*n + 1
        s += sign * math.log(m) / m
    return s

# Better: use closed-form expression.
# Known closed form (Almkvist-Granville, etc):
# L'(1, chi_4) = (pi/4)*(gamma + 2*log(2) + 3*log(pi) - 4*log(Gamma(1/4)))
# This comes from logarithmic derivative of functional equation.
# Let's compute via known formula.

def L_prime_chi4_closed():
    from math import lgamma, log, pi
    # gamma = Euler-Mascheroni
    gamma = 0.5772156649015329
    # Gamma(1/4)
    log_Gamma_1_4 = lgamma(0.25)  # lgamma is log|Gamma(x)|
    val = (pi/4) * (gamma + 2*log(2) + 3*log(pi) - 4*log_Gamma_1_4)
    return val

# Sanity check: there's a famous identity
# L'(1, chi_4) = (pi/4) * (gamma - log(pi/2)) + sum_{m=1}^inf chi_4(m) log(m) ...
# Or: simpler -- use mpmath if available.
try:
    import mpmath as mp
    mp.mp.dps = 30
    def L_prime_chi4_mp():
        # L(s, chi_4) = sum_{n=0}^inf chi_4(2n+1) / (2n+1)^s, but chi_4(2n+1)=(-1)^n
        # mpmath has dirichlet series; just use mp.diff on L(s, chi_4)
        # chi_4 is the unique non-principal Dirichlet character mod 4
        L = lambda s: mp.dirichlet(s, [0, 1, 0, -1])
        return float(mp.diff(L, 1))
    Lp_mp = L_prime_chi4_mp()
except ImportError:
    Lp_mp = None

Lp_closed = L_prime_chi4_closed()
print(f"L'(1, chi_4) via closed form: {Lp_closed:.10f}")
if Lp_mp is not None:
    print(f"L'(1, chi_4) via mpmath:      {Lp_mp:.10f}")
# Use mpmath value if available, otherwise closed form
Lp = Lp_mp if Lp_mp is not None else Lp_closed

# ---------- gamma_K (Euler-Kronecker for Q(i)) ----------
import math
gamma = 0.5772156649015329  # Euler-Mascheroni
R = math.pi / 4
gamma_K = Lp + gamma * R
print(f"gamma_K = L'(1,chi_4) + gamma*R = {gamma_K:.10f}")

# ---------- H(1) via Euler product ----------
# Local factors:
#  p=2:        H_2(1) = (1 + 3/2)(1 - 1/2)^3 = 5/16
#  p=3 mod 4: H_p(1) = (1 - 1/p^2)^3
#  p=1 mod 4: H_p(1) = (1 - 1/p)^4 (1 + 4/p - 1/p^2)
def H_factor(p):
    if p == 2:
        return (1 + 3/2) * (1 - 1/2)**3
    if p % 4 == 3:
        return (1 - 1/p**2)**3
    if p % 4 == 1:
        return (1 - 1/p)**4 * (1 + 4/p - 1/p**2)
    raise ValueError

PMAX = 10**7
print(f"Truncating Euler products at p <= {PMAX}")
primes = list(primerange(2, PMAX+1))
H1 = 1.0
for p in primes:
    H1 *= H_factor(p)
print(f"H(1) ≈ {H1:.10f}")

# ---------- H'(1) via logarithmic derivative ----------
# H'(1)/H(1) = sum_p [d/ds log H_p(s)]_{s=1}
# For p=2:        2.4 * log 2
# For p=3 mod 4:  6 log p / (p^2 - 1)
# For p=1 mod 4:  log p * (22p - 6) / [(p-1)(p^2+4p-1)]
def dlog_H_factor(p):
    lp = math.log(p)
    if p == 2:
        return 2.4 * lp
    if p % 4 == 3:
        return 6 * lp / (p*p - 1)
    if p % 4 == 1:
        return lp * (22*p - 6) / ((p-1) * (p*p + 4*p - 1))
    raise ValueError

dlogH_sum = 0.0
for p in primes:
    dlogH_sum += dlog_H_factor(p)
print(f"sum_p H'_p(1)/H_p(1) = {dlogH_sum:.10f}")

Hprime1 = H1 * dlogH_sum
print(f"H'(1) ≈ {Hprime1:.10f}")

# Tail estimation for H'(1):
# For p large with p ≡ 1 (4), the term is log p * (22p) / (p * p^2) = 22 log p / p^2
# Sum over p > P_max of split primes ~ integral of 22 log x / x^2 / ln x * (1/2) dx from P_max
# = 11/P_max approximately. At P_max = 10^7, this is ~ 1.1e-6. Negligible.
# For p ≡ 3 (4): 6 log p / p^2 in sum, similarly negligible.

# ---------- Predicted constants ----------
A3 = R**3 * H1
A2 = 3 * R**2 * gamma_K * H1 + R**3 * Hprime1

c3 = 4 * A3 / 3
c2 = 2 * A2

print()
print(f"R = pi/4 = {R:.10f}")
print(f"R^3 H(1) = A_3 = {A3:.10f}")
print(f"3 R^2 gamma_K H(1) = {3*R**2*gamma_K*H1:.10f}")
print(f"R^3 H'(1)        = {R**3 * Hprime1:.10f}")
print(f"A_2              = {A2:.10f}")
print()
print(f"PREDICTED c_3 = 4 A_3 / 3 = pi^3 H(1) / 48 = {c3:.10f}")
print(f"PREDICTED c_2 = 2 A_2                       = {c2:.10f}")
print()

# ---------- Empirical S(N) data from last session ----------
# From P12-tau-squared-second-moment.md table:
empirical = [
    (10**3,       86384),
    (10**4,     1614068),
    (10**5,    26859868),
    (3*10**5, 100153656),
    (10**6,   415319768),
]

print("N           S(N)         S/(N log^3 N)   c_3 + c_2/log N (predicted)   residual")
for N, S in empirical:
    L = math.log(N)
    leading = c3 * N * L**3
    secondary = c2 * N * L**2
    pred_total = leading + secondary
    ratio = S / (N * L**3)
    pred_ratio = c3 + c2 / L
    residual = (S - pred_total) / (N * L)  # what's left if we use 2-term model
    print(f"{N:10}  {S:12}  {ratio:.6f}        {pred_ratio:.6f}                {residual:.4f}")

print()
print("If 2-term model is good, residual should be small relative to A_1 / pi factor.")
print()

# Pairwise fit c_3 with two-term model: y = c_3 + c_2/x + a/x^2 (3 unknowns => use 3 pts)
# Or, fix c_3 and c_2 (theoretical), fit only the remaining residual
print("Three-term least-squares fit using y = c_3 + a/x + b/x^2 on full empirical:")
import numpy as np
xs = np.array([math.log(N) for N, _ in empirical])
ys = np.array([S/(N*math.log(N)**3) for N, S in empirical])
# Solve y = c3 + a/x + b/x^2
A_mat = np.column_stack([np.ones_like(xs), 1/xs, 1/xs**2])
coefs, *_ = np.linalg.lstsq(A_mat, ys, rcond=None)
print(f"  c_3 fit = {coefs[0]:.6f}, a = {coefs[1]:.6f}, b = {coefs[2]:.6f}")
print(f"  predicted c_3 = {c3:.6f}, c_2 = {c2:.6f}")
print()

# Constrain c_3 to predicted, fit a (the predicted c_2) and b
ys2 = ys - c3
A_mat2 = np.column_stack([1/xs, 1/xs**2])
coefs2, *_ = np.linalg.lstsq(A_mat2, ys2, rcond=None)
print(f"With c_3 fixed at predicted {c3:.6f}: empirical c_2 fit = {coefs2[0]:.6f}, b = {coefs2[1]:.6f}")
print(f"Predicted c_2 = {c2:.6f}.  Match ratio: {coefs2[0]/c2:.4f}")
