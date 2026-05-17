"""
Compute the constant Laurent coefficient c_0 in the formal SD asymptotic
   S(N) = sum_{n<=N} tau(n^2+1)^2
        ~ c_3 N (log N)^3 + c_2 N (log N)^2 + c_1 N log N + c_0 N + ...
where (formally) c_j = 2 A_j for j=1,2 and c_0 = A_0, with A_j the Laurent
coefficients of G(s) = zeta_K(s)^3 H(s) at s=1.

A_0 = (3 R^2 alpha_K + 6 R gamma_K beta_K + gamma_K^3) H(1)
    + 3 R (R beta_K + gamma_K^2) H'(1)
    + (3/2) R^2 gamma_K H''(1)
    + (1/6) R^3 H'''(1)

with R = pi/4 and:
    gamma_K = L'(1, chi_4) + gamma R                       (already verified)
    beta_K  = L''(1, chi_4)/2 + gamma L'(1, chi_4) - gamma_1 R   (already verified)
    alpha_K = L'''(1, chi_4)/6 + gamma L''(1, chi_4)/2
              - gamma_1 L'(1, chi_4) + (gamma_2/2) R
                    (derived this session, see proof file)

H(s) = prod H_p(s) with H_p as in P12-tau-squared-secondary-coefficient.md.
Compute H', H'', H''' via finite differences of log H(s), then
H'''/H = (log H)''' + 3 (log H)' (log H)'' + (log H)'^3.
Cross-check H'(1), H''(1) against previous-session values.
"""
import math
from mpmath import mp, mpf, stieltjes, nsum, inf, log, diff, exp

mp.dps = 50  # 50-digit precision

# --- L(s, chi_4) via alternating-series representation -----------------
#   L(s, chi_4) = sum_{n=0}^infty (-1)^n / (2n+1)^s  (Dirichlet beta)
# Use mpmath.diff with this representation; nsum handles alternating
# series acceleration well at s=1.

def Lchi4(s):
    return nsum(lambda n: (-1)**n / (2*n+1)**s, [0, inf])

print("=== L(s, chi_4) and derivatives at s=1 ===")
L0 = Lchi4(mpf(1))
L1 = diff(Lchi4, mpf(1), 1)
L2 = diff(Lchi4, mpf(1), 2)
L3 = diff(Lchi4, mpf(1), 3)
print(f"L(1,chi_4)        = {float(L0):.15f}    (pi/4 = {float(mp.pi/4):.15f})")
print(f"L'(1,chi_4)       = {float(L1):.15f}")
print(f"L''(1,chi_4)      = {float(L2):.15f}")
print(f"L'''(1,chi_4)     = {float(L3):.15f}")

# --- Stieltjes constants -----------------------------------------------
gamma  = stieltjes(0)
gamma1 = stieltjes(1)
gamma2 = stieltjes(2)
print("\n=== Stieltjes constants ===")
print(f"gamma     = {float(gamma):.10f}")
print(f"gamma_1   = {float(gamma1):.10f}")
print(f"gamma_2   = {float(gamma2):.10f}")

# --- Laurent coefficients of zeta_K = zeta * L --------------------------
R = mp.pi / 4
gamma_K = L1 + gamma * R
# beta_K with the sign convention used in the previous proof file:
#   zeta(s) = 1/u + gamma + e_1 u + e_2 u^2 + ..., with e_1 = -gamma_1,
#   e_2 = gamma_2 / 2 (where gamma_n is standard Stieltjes:
#        zeta(s) = 1/u + gamma + sum_{n>=1} (-1)^n gamma_n u^n / n!)
beta_K  = L2/2 + gamma*L1 - gamma1*R
alpha_K = L3/6 + gamma*L2/2 - gamma1*L1 + (gamma2/2)*R

print("\n=== zeta_K Laurent coefs at s=1 ===")
print(f"R       = pi/4    = {float(R):.10f}")
print(f"gamma_K           = {float(gamma_K):.10f}")
print(f"beta_K            = {float(beta_K):.10f}")
print(f"alpha_K           = {float(alpha_K):.10f}")
# Cross-check vs previous session values:
print(f"  (prev session: gamma_K ~ 0.6462, beta_K ~ 0.0915)")

# --- Euler-product H(s) and its derivatives at s=1 ----------------------
# We'll compute H_p(s) for each prime p up to P_max, sum log H_p, and
# differentiate via finite differences applied to *log H(s)*. This avoids
# numerical loss of significance from exponentiating small numbers.

def primes_up_to(P):
    sieve = bytearray([1]) * (P + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(P**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, P+1, i):
                sieve[j] = 0
    return [p for p in range(2, P+1) if sieve[p]]

def Hp_value(p, s):
    """Local factor H_p(s) of H = G/zeta_K^3."""
    x = mpf(p) ** (-s)
    if p == 2:
        # H_2(s) = (1 + 3 * 2^{-s}) (1 - 2^{-s})^3
        return (1 + 3*x) * (1 - x)**3
    if p % 4 == 3:
        # H_p(s) = (1 - p^{-2s})^3
        x2 = mpf(p) ** (-2*s)
        return (1 - x2)**3
    # p ≡ 1 mod 4: H_p(s) = (1 + 4x - x^2)(1-x)^4
    return (1 + 4*x - x*x) * (1 - x)**4

def logH_partial(s, P_max, primes):
    """log H(s) via truncated Euler product over primes <= P_max."""
    total = mpf(0)
    for p in primes:
        if p > P_max:
            break
        v = Hp_value(p, s)
        total += mp.log(v)
    return total

P_max = 200000   # enough for ~8 digits in H(1); more for derivs is overkill
primes = primes_up_to(P_max)
print(f"\n=== H(s) Euler product (primes up to {P_max}) ===")

# Evaluate log H at a stencil of s-values and compute FD derivatives
h = mpf('1e-3')
s_vals = [1 - 2*h, 1 - h, mpf(1), 1 + h, 1 + 2*h]
logH_vals = [logH_partial(s, P_max, primes) for s in s_vals]

# H(1)
logH1 = logH_vals[2]
H1 = mp.exp(logH1)
print(f"H(1)              = {float(H1):.10f}      (prev: 0.12324)")

# (log H)'(1), (log H)''(1), (log H)'''(1) via FD on log H
L_prime  = (logH_vals[3] - logH_vals[1]) / (2*h)
L_double = (logH_vals[3] - 2*logH_vals[2] + logH_vals[1]) / h**2
L_triple = (logH_vals[4] - 2*logH_vals[3] + 2*logH_vals[1] - logH_vals[0]) / (2*h**3)
print(f"(log H)'(1)       = {float(L_prime):.10f}")
print(f"(log H)''(1)      = {float(L_double):.10f}")
print(f"(log H)'''(1)     = {float(L_triple):.10f}")

H1p = L_prime * H1
H2p = (L_double + L_prime**2) * H1
H3p = (L_triple + 3 * L_prime * L_double + L_prime**3) * H1
print(f"H'(1)             = {float(H1p):.10f}      (prev: 0.5934)")
print(f"H''(1)            = {float(H2p):.10f}")
print(f"H'''(1)           = {float(H3p):.10f}")

# Cross-check: H''(1)/2 (this was the H_2 in the file, prev = 0.4534)
print(f"H''(1)/2          = {float(H2p/2):.10f}    (prev: 0.4534)")

# --- Plug into A_3, A_2, A_1, A_0 closed-form formulas ----------------
A3 = R**3 * H1
A2 = 3*R*R*gamma_K*H1 + R**3 * H1p
A1 = 3*R*(R*beta_K + gamma_K**2)*H1 + 3*R*R*gamma_K*H1p + R**3 * H2p / 2
# wait: in the previous file H_2 := H''(1)/2, and z_{-3} H_3 has H_3 := H'''(1)/6.
# Let me re-derive with bare H'(1), H''(1), H'''(1) (no factorials):
# G(s) = sum z_k u^k * sum (H^(j)(1)/j!) u^j
# A_0 = z_0 * H(1) + z_{-1} * H'(1) + z_{-2} * H''(1)/2 + z_{-3} * H'''(1)/6
# A_1 = z_{-1} * H(1) + z_{-2} * H'(1) + z_{-3} * H''(1)/2
# A_2 = z_{-2} * H(1) + z_{-3} * H'(1)
# A_3 = z_{-3} * H(1)
# with z_{-3} = R^3, z_{-2} = 3R^2 gamma_K, z_{-1} = 3R(R beta_K + gamma_K^2),
#      z_0   = 3 R^2 alpha_K + 6 R gamma_K beta_K + gamma_K^3
z_m3 = R**3
z_m2 = 3 * R**2 * gamma_K
z_m1 = 3 * R * (R * beta_K + gamma_K**2)
z_0  = 3 * R**2 * alpha_K + 6 * R * gamma_K * beta_K + gamma_K**3

A3 = z_m3 * H1
A2 = z_m2 * H1 + z_m3 * H1p
A1 = z_m1 * H1 + z_m2 * H1p + z_m3 * H2p / 2
A0 = z_0 * H1 + z_m1 * H1p + z_m2 * H2p / 2 + z_m3 * H3p / 6

print("\n=== Laurent coefs A_j of G = zeta_K^3 H at s=1 ===")
print(f"z_{{-3}} = R^3                 = {float(z_m3):.10f}")
print(f"z_{{-2}} = 3R^2 gamma_K       = {float(z_m2):.10f}")
print(f"z_{{-1}} = 3R(R beta_K + g^2) = {float(z_m1):.10f}")
print(f"z_0    = 3R^2 alpha_K + 6 R gamma_K beta_K + gamma_K^3 = {float(z_0):.10f}")
print(f"A_3 = {float(A3):.10f}")
print(f"A_2 = {float(A2):.10f}")
print(f"A_1 = {float(A1):.10f}")
print(f"A_0 = {float(A0):.10f}")

# c_j coefficients: c_3 = 4 A_3 / 3, c_2 = 2 A_2, c_1 = 2 A_1, c_0 = A_0
c3 = 4 * A3 / 3
c2 = 2 * A2
c1 = 2 * A1
c0 = A0
print("\n=== Predicted c_j in S(N) = sum_{j} c_j N (log N)^j + ... ===")
print(f"c_3 = 4A_3/3 = {float(c3):.10f}    (prev session: 0.07961)")
print(f"c_2 = 2A_2   = {float(c2):.10f}    (prev session: 0.86979)")
print(f"c_1 = 2A_1   = {float(c1):.10f}    (prev session: 2.14298)")
print(f"c_0 =  A_0   = {float(c0):.10f}    (NEW this session)")

# --- Cross-check alpha_K independently via FD on zeta_K(s) ----------
# zeta_K(s) = zeta(s) L(s, chi_4); compute (zeta_K(s) - R/(s-1)) and
# extract Laurent coefficient by FD.  We use the alternating-series form
# for L and mpmath.zeta for zeta.
from mpmath import zeta as mp_zeta

def zetaK(s):
    return mp_zeta(s) * Lchi4(s)

def zetaK_subtracted(s):
    # zeta_K(s) - R/(s-1) is regular at s=1, equals gamma_K + beta_K (s-1) + alpha_K (s-1)^2 + ...
    return zetaK(s) - R/(s-1)

# Estimate gamma_K, beta_K, alpha_K via finite differences of zetaK_subtracted at s=1
# Using small h to avoid catastrophic cancellation
h2 = mpf('1e-3')
f_p2 = zetaK_subtracted(1 + 2*h2)
f_p1 = zetaK_subtracted(1 + h2)
f_m1 = zetaK_subtracted(1 - h2)
f_m2 = zetaK_subtracted(1 - 2*h2)
# value at 1: take a limit. mpmath struggles. Use series: gamma_K + beta_K * 0 + ... = gamma_K
# Instead, use Taylor: f(0) ≈ (4 f(h) - f(2h))/3 - 2*h*beta + ... NO, let's use a different stencil
# centered around symmetric pairs:
gK_fd = (f_p1 + f_m1)/2  # = gamma_K + alpha_K h^2 + O(h^4)  (the beta_K term cancels)
bK_fd = (f_p1 - f_m1)/(2*h2)  # = beta_K + 2 alpha_K * 0 + (1/6) ... beta_K + (1/6) zeta_K''' h^2/3! ...
# alpha_K coefficient:
# f(1+h) = gK + bK h + aK h^2 + delta h^3 + ...
# (f(1+h) + f(1-h))/2 = gK + aK h^2 + O(h^4)  →  aK ≈ ((f+f)/2 - gK)/h^2
# But we don't have gK directly. Use 4-stencil:
# f(1+h)+f(1-h) - 2 gK = 2 aK h^2 + O(h^4)
# Better: use second derivative formula:
# aK ~ f''(1)/2!? No, aK = coefficient of (s-1)^2 in Taylor of f at 1 = f''(1)/2
# f''(1) ≈ (f_p1 - 2 f(1) + f_m1)/h^2 — but we don't have f(1) cleanly.
# Workaround: gK_fd above is already gamma_K to O(h^2); use it as f(1) approximation
gK_approx = gK_fd
aK_fd = (f_p1 - 2*gK_approx + f_m1)/(h2**2)/2  # alpha_K = f''(1)/2
print(f"\n=== Cross-check alpha_K via FD on (zeta_K(s) - R/(s-1)) at s=1 ===")
print(f"gamma_K (FD)  = {float(gK_fd):.10f}    vs analytic {float(gamma_K):.10f}")
print(f"beta_K  (FD)  = {float(bK_fd):.10f}    vs analytic {float(beta_K):.10f}")
print(f"alpha_K (FD)  = {float(aK_fd):.10f}    vs analytic {float(alpha_K):.10f}")

# --- Skeptic-prompted: verify Laurent expansion of G(s) at s=1.1 ----
# G(s) = zeta_K(s)^3 H(s), Laurent A_3/u^3 + A_2/u^2 + A_1/u + A_0 + ...
# Evaluate G(1.1) directly via truncated Euler product, compare to
# Laurent prediction at u=0.1.
def G_via_euler(s, P_max, primes):
    """G(s) = sum_d tau(d^2) rho(d) / d^s via Euler product."""
    val = mpf(1)
    for p in primes:
        if p > P_max:
            break
        if p == 2:
            # local factor: 1 + tau(4)*rho(2)/2^s = 1 + 3 * 2^{-s}
            val *= 1 + 3 * mpf(p)**(-s)
        elif p % 4 == 3:
            val *= mpf(1)  # local factor 1
        else:  # p ≡ 1 mod 4
            x = mpf(p)**(-s)
            val *= (1 + 4*x - x*x) / (1 - x)**2
    return val

print("\n=== Verify Laurent expansion of G(s) numerically ===")
s_test = mpf('1.1')
u_test = s_test - 1
G_direct = G_via_euler(s_test, P_max, primes)
G_Laurent = (z_m3/u_test**3 + z_m2/u_test**2 + z_m1/u_test + z_0) * H1
# More precisely: G = zeta_K^3 H, with Laurent at s=1, error O(u) for the constant truncation
# Using A_3, A_2, A_1, A_0:
G_Laurent_direct = A3/u_test**3 + A2/u_test**2 + A1/u_test + A0
print(f"G(1.1) direct (Euler, primes <= {P_max})   = {float(G_direct):.6f}")
print(f"G(1.1) from Laurent A_3..A_0 (no error)    = {float(G_Laurent_direct):.6f}")
print(f"Relative diff: {float((G_direct - G_Laurent_direct)/G_direct)*100:.3f}%")
# Note: the Laurent only has 4 terms; difference at u=0.1 is O(u) = O(0.1)
# i.e. should be ~10% relative if the next Laurent coef A_{-1} is comparable to A_0.

# --- Empirical comparison from previous data -----------------------
# From the secondary-coefficient file:
#   N           S(N)           predicted c_3 L^3 + c_2 L^2 + c_1 L (times N)
#   10^3        86,384         82,548
#   10^4        1,614,068      1,557,228
#   10^5        26,859,868     26,144,610
#   3·10^5      100,153,656    97,516,540
#   10^6        415,319,768    405,549,088

emp_data = [
    (1000,    86384),
    (10000,   1614068),
    (100000,  26859868),
    (300000,  100153656),
    (1000000, 415319768),
]

print("\n=== Empirical vs 4-term prediction ===")
print(f"{'N':>10} {'S(N)':>14} {'pred 3-term':>14} {'pred 4-term':>14} {'ratio':>8}")
for N, SN in emp_data:
    L = math.log(N)
    pred3 = N * (float(c3)*L**3 + float(c2)*L**2 + float(c1)*L)
    pred4 = pred3 + N * float(c0)
    print(f"{N:>10} {SN:>14} {pred3:>14.0f} {pred4:>14.0f} {SN/pred4:>8.4f}")

# 4-parameter constrained fit: residual = S/N - (c3 L^3 + c2 L^2 + c1 L) ~ c0
print("\n=== Empirical c_0 from residual at each N ===")
print(f"{'N':>10} {'(S - c3 L^3 N - c2 L^2 N - c1 L N)/N':>40}")
for N, SN in emp_data:
    L = math.log(N)
    resid = SN/N - (float(c3)*L**3 + float(c2)*L**2 + float(c1)*L)
    print(f"{N:>10} {resid:>40.4f}    pred c0 = {float(c0):.4f}")

# --- Unconstrained 4-parameter empirical fit ----------------------
# y = S/(N L^3); model y = a + b/L + c/L^2 + d/L^3.
#   a ↔ c_3,  b ↔ c_2,  c ↔ c_1,  d ↔ c_0.
import numpy as np
L_vals = np.array([math.log(N) for N, _ in emp_data])
y_vals = np.array([SN/(N * L**3) for (N, SN), L in zip(emp_data, L_vals)])
basis  = np.column_stack([np.ones_like(L_vals), 1/L_vals, 1/L_vals**2, 1/L_vals**3])
coefs, *_ = np.linalg.lstsq(basis, y_vals, rcond=None)
a, b, c, d = coefs
print("\n=== 4-parameter unconstrained empirical fit (5 data points) ===")
print(f"y = a + b/L + c/L^2 + d/L^3   on   y = S/(N L^3),  L = log N")
print(f"a ↔ c_3 = {a:.5f}    formal = {float(c3):.5f}   gap {(a/float(c3)-1)*100:+.2f}%")
print(f"b ↔ c_2 = {b:.5f}    formal = {float(c2):.5f}   gap {(b/float(c2)-1)*100:+.2f}%")
print(f"c ↔ c_1 = {c:.5f}    formal = {float(c1):.5f}   gap {(c/float(c1)-1)*100:+.2f}%")
print(f"d ↔ c_0 = {d:.5f}    formal = {float(c0):.5f}   gap {(d/float(c0)-1)*100:+.2f}%")

# --- Constrained fit: fix c_3, c_2 at formal; fit c_1, c_0 ---------
# y - c3_formal - c2_formal/L = c_1/L^2 + c_0/L^3
y_red = y_vals - float(c3) - float(c2)/L_vals
basis_red = np.column_stack([1/L_vals**2, 1/L_vals**3])
coefs_red, *_ = np.linalg.lstsq(basis_red, y_red, rcond=None)
print("\n=== Constrained fit: c_3, c_2 fixed at formal; fit (c_1, c_0) ===")
print(f"c_1 (fit) = {coefs_red[0]:.4f}    formal = {float(c1):.4f}   gap {(coefs_red[0]/float(c1)-1)*100:+.2f}%")
print(f"c_0 (fit) = {coefs_red[1]:.4f}    formal = {float(c0):.4f}   gap {(coefs_red[1]/float(c0)-1)*100:+.2f}%")

# --- Constrained fit: fix c_3 only ----------------------------------
y_red2 = y_vals - float(c3)
basis_red2 = np.column_stack([1/L_vals, 1/L_vals**2, 1/L_vals**3])
coefs_red2, *_ = np.linalg.lstsq(basis_red2, y_red2, rcond=None)
print("\n=== Constrained fit: c_3 only fixed; fit (c_2, c_1, c_0) ===")
print(f"c_2 (fit) = {coefs_red2[0]:.4f}    formal = {float(c2):.4f}   gap {(coefs_red2[0]/float(c2)-1)*100:+.2f}%")
print(f"c_1 (fit) = {coefs_red2[1]:.4f}    formal = {float(c1):.4f}   gap {(coefs_red2[1]/float(c1)-1)*100:+.2f}%")
print(f"c_0 (fit) = {coefs_red2[2]:.4f}    formal = {float(c0):.4f}   gap {(coefs_red2[2]/float(c0)-1)*100:+.2f}%")
