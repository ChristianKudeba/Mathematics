"""
High-precision computation of H(1), H'(1), gamma_K for the c_0^T closed form.

Conventions (matching prev sessions):
- K = Q(i), R = pi/4
- zeta_K(s) = zeta(s) L(s, chi_4)
- gamma_K := R*gamma + L'(1, chi_4)  [the "scaled" Euler-Kronecker]
- G(s) = sum_{e sf} rho(e) e^{-s} = zeta_K(s) H(s)
- H(s) = (1 - 4^{-s}) prod_{p≡1(4)} (1 - 3 p^{-2s} + 2 p^{-3s})
                    * prod_{p≡3(4)} (1 - p^{-2s})
- c_0^T_inf = 2 (R H'(1) + gamma_K H(1) - R H(1)) - 2 B_inf

Two independent numerical paths:
1. mp 40-digit Euler product at P = 10^7 (~25 s).
2. float64 Euler product at P = 10^8 (~3 min) — independent precision check.
Combine via tail estimate ~4/P.
"""
import math
import time
import mpmath as mp
import numpy as np

mp.mp.dps = 40  # 40 decimal digits of precision throughout


def primes_up_to(N):
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.flatnonzero(sieve)


# === L(1, chi_4) = pi/4, exact ===
R = mp.pi / 4
gamma_E = mp.euler

# === L'(1, chi_4) via Lerch-Kronecker closed form ===
Lprime = R * (gamma_E + 2*mp.log(2) + 3*mp.log(mp.pi) - 4*mp.log(mp.gamma(mp.mpf(1)/4)))
gamma_K = R * gamma_E + Lprime

print("=== Constants ===")
print(f"R = pi/4                = {mp.nstr(R, 25)}")
print(f"gamma                   = {mp.nstr(gamma_E, 25)}")
print(f"L'(1, chi_4)            = {mp.nstr(Lprime, 25)}")
print(f"gamma_K = R*gamma + L'  = {mp.nstr(gamma_K, 25)}")

# Cross-check via mp.diff (lower precision)
def beta(s):
    return mp.dirichlet(s, [0, 1, 0, -1])
Lprime_check = mp.diff(beta, 1)
print(f"L'(1, chi_4) [diff chk] = {mp.nstr(Lprime_check, 12)}")


# === Path 1: mp 40-digit Euler product at P = 10^7 ===
print("\n=== Path 1: mp Euler product at P=10^7 ===")
t0 = time.time()
P1 = 10**7
primes1 = primes_up_to(P1)
log_prod = mp.log(mp.mpf(3) / 4)
HlogD = mp.log(mp.mpf(4)) / 3
for p in primes1[1:]:
    pp = mp.mpf(int(p))
    lp = mp.log(pp)
    if int(p) % 4 == 1:
        factor = 1 - 3/pp**2 + 2/pp**3
        log_prod += mp.log(factor)
        HlogD += 6 * lp * (1/pp**2 - 1/pp**3) / factor
    else:
        factor = 1 - 1/pp**2
        log_prod += mp.log(factor)
        HlogD += 2 * lp / pp**2 / factor
H1_mp = mp.exp(log_prod)
Hp_mp = HlogD * H1_mp
print(f"  time: {time.time()-t0:.1f}s, #primes used: {len(primes1)}")
print(f"  H(1)        = {mp.nstr(H1_mp, 25)}")
print(f"  H'/H        = {mp.nstr(HlogD, 25)}")
print(f"  H'(1)       = {mp.nstr(Hp_mp, 25)}")


# === Path 2: float64 Euler product at P = 10^8 ===
print("\n=== Path 2: float64 Euler product at P=10^8 ===")
t0 = time.time()
P2 = 10**8
primes2 = primes_up_to(P2)
log_prod_f = math.log(0.75)
HlogD_f = math.log(4) / 3
for p in primes2[1:]:
    p = int(p)
    lp = math.log(p)
    if p % 4 == 1:
        factor = 1 - 3/p**2 + 2/p**3
        log_prod_f += math.log(factor)
        HlogD_f += 6 * lp * (1/p**2 - 1/p**3) / factor
    else:
        factor = 1 - 1/p**2
        log_prod_f += math.log(factor)
        HlogD_f += 2 * lp / p**2 / factor
H1_f = math.exp(log_prod_f)
Hp_f = HlogD_f * H1_f
print(f"  time: {time.time()-t0:.1f}s, #primes used: {len(primes2)}")
print(f"  H(1)  [float64]  = {H1_f:.16f}")
print(f"  H'/H  [float64]  = {HlogD_f:.16f}")
print(f"  H'(1) [float64]  = {Hp_f:.16f}")


# === Tail bound past P (via PNT-AP partial summation) ===
# sum_{p>P} log p / p^2 ~ 1/P; weighted by 6 (split, with density 1/2) and
# 2 (inert, density 1/2) gives total ~ 4/P for H'/H.
# H tail: sum_{p>P} (3 or 1)/p^2 ~ 2/(P log P).
print("\n=== Tail bounds ===")
print(f"H tail past P=10^7   ~ 2/(P log P) = {2/(P1*math.log(P1)):.2e}")
print(f"H' tail past P=10^7  ~ 4/P * H(1)  = {4/P1 * float(H1_mp):.2e}")
print(f"H tail past P=10^8   ~ 2/(P log P) = {2/(P2*math.log(P2)):.2e}")
print(f"H' tail past P=10^8  ~ 4/P * H(1)  = {4/P2 * float(H1_mp):.2e}")
print(f"Empirical Δ(H,  10^7→10^8) = {float(H1_mp) - H1_f:.3e}")
print(f"Empirical Δ(H', 10^7→10^8) = {float(Hp_mp) - Hp_f:.3e}")


# === Best estimates: use mp at 10^7 plus the float64-derived 10^7→10^8 increment ===
# (float64 has ~13-digit precision; 5.7M sums have rounding ~5.7M * eps ~ 1.3e-9 worst case,
# but variance-sum error ~ sqrt(N)*eps ~ 5e-13.)
H1_best = H1_mp + mp.mpf(H1_f - float(H1_mp))
Hp_best = Hp_mp + mp.mpf(Hp_f - float(Hp_mp))
H1_uncertainty = mp.mpf(2 / (P2 * math.log(P2)))  # ~ 1e-9
Hp_uncertainty = 4 / mp.mpf(P2) * H1_best  # ~ 2e-9

print("\n=== Best estimates (mp@10^7 + float64-derived increment) ===")
print(f"H(1)  best  = {mp.nstr(H1_best, 18)}  ± {mp.nstr(H1_uncertainty, 4)}")
print(f"H'(1) best  = {mp.nstr(Hp_best, 18)}  ± {mp.nstr(Hp_uncertainty, 4)}")


# === Final assembly ===
print("\n=== c_0^T closed form (high-precision) ===")
A_inf = R * H1_best
c_lt_inf = R * Hp_best + gamma_K * H1_best
struct = 2 * (c_lt_inf - A_inf)
print(f"R H(1) = A^inf    = {mp.nstr(A_inf, 18)}")
print(f"R H'(1)            = {mp.nstr(R * Hp_best, 18)}")
print(f"gamma_K H(1)       = {mp.nstr(gamma_K * H1_best, 18)}")
print(f"c_<^inf            = {mp.nstr(c_lt_inf, 18)}")
print(f"structural         = {mp.nstr(struct, 18)}")

B_heur = mp.mpf("0.085704")
B_emp = mp.mpf("0.0856787")
print(f"\nc_0^T_inf with B_heur=0.085704         : {mp.nstr(struct - 2*B_heur, 12)}")
print(f"c_0^T_inf with B(10^7)/10^7=0.0856787  : {mp.nstr(struct - 2*B_emp, 12)}")
print(f"empirical c_0^T(10^7)                  : 0.987203")
print(f"gap (heuristic - emp)                  : {mp.nstr(struct - 2*B_heur - mp.mpf('0.987203'), 6)}")
print(f"gap (B@1e7 - emp)                      : {mp.nstr(struct - 2*B_emp - mp.mpf('0.987203'), 6)}")


# === Decompose the gap ===
print("\n=== Gap decomposition (predicted - empirical at N=10^7) ===")
# Empirical at N=10^7 from prev session's c0T-N1e7-empirical.py:
c_lt_app_1e7 = mp.mpf("1.013354")
A_per_N_1e7 = mp.mpf("0.4340743")
B_per_N_1e7 = mp.mpf("0.0856787")
c0T_emp_1e7 = mp.mpf("0.987203")

# Algebraic identity: c_0^T(N) = 2 (c_<^app(N) - A(N)/N - B(N)/N) (exact)
c0T_alg = 2 * (c_lt_app_1e7 - A_per_N_1e7 - B_per_N_1e7)
print(f"c_0^T(10^7) via 2(c_<^app - A/N - B/N): {mp.nstr(c0T_alg, 10)}  (vs emp 0.987203)")

# Predicted (with heuristic B^inf):
c0T_pred = struct - 2 * B_heur
print(f"c_0^T_inf predicted (with B_heur)     : {mp.nstr(c0T_pred, 10)}")

# Decomposition:
delta_c_lt = c_lt_inf - c_lt_app_1e7
delta_A = A_inf - A_per_N_1e7
delta_B = B_heur - B_per_N_1e7
print(f"  Δ c_<: c_<^inf - c_<^app(10^7) = {mp.nstr(delta_c_lt, 6)}")
print(f"  Δ A:   A^inf - A(10^7)/10^7    = {mp.nstr(delta_A, 6)}")
print(f"  Δ B:   B_heur - B(10^7)/10^7   = {mp.nstr(delta_B, 6)}")
print(f"  predicted - empirical = 2(Δc_< - ΔA - ΔB)")
print(f"    = 2*({mp.nstr(delta_c_lt - delta_A - delta_B, 6)}) = {mp.nstr(2*(delta_c_lt - delta_A - delta_B), 6)}")
