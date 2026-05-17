"""Analytic verification of D_h(N) ~ C_h * N.

Derivation:
    D_h(N) := sum_{e <= N, sf, good} prod_{p|e} 4 cos^2(2 pi h alpha_p (e/p)^{-1}/p)

Average per-prime factor over (e/p)^{-1} uniform in (Z/p)*:
    p = 2:  1                  (always: factor is (-1)^h, square = 1)
    p ≡ 1(4), p ∤ h:  2(p-2)/(p-1)
    p ≡ 1(4), p | h:  4

Heuristic multiplicative-function approximation:
    D_h(N) ~ sum_{e <= N, sf good} g_h(e),  g_h multiplicative, g_h(p) above

Dirichlet series:
    G_h(s) = (1 + 2^{-s}) prod_{p ≡ 1(4)} (1 + g_h(p)/p^s).

At s=1, log G_h(s) = 2 sum_{p ≡ 1(4)} p^{-s} + O(1) = log zeta_K(s) + O(1),
so G_h(s) ~ C_h/(s-1) near s=1, where (using Wirsing/Selberg-Delange)
    C_h = res_{s=1} G_h(s) = (pi/4) * H_h(1)
with
    H_h(s) := G_h(s) / zeta_K(s) =
        (1 - 4^{-s})
        * prod_{p ≡ 1(4)} (1 + g_h(p)/p^s)(1 - 1/p^s)^2
        * prod_{p ≡ 3(4)} (1 - 1/p^{2s}).

Plugging in:
    H_h(1) = (3/4)
        * prod_{p ≡ 1(4), p ∤ h} (p^2 + p - 4)(p-1)/p^3
        * prod_{p ≡ 1(4), p | h} (p+4)(p-1)^2/p^3
        * prod_{p ≡ 3(4)} (1 - 1/p^2).

We compute these to high precision (truncating at P=10^7) and compare to empirical
C_h := D_h(10^7)/10^7 from `Halasz-Dh-empirical.py`.
"""
import math
import sys

import numpy as np


def primes_to(P):
    sieve = np.ones(P + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(P ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    return np.nonzero(sieve)[0]


def compute_Hh1_via_truncation(P, h):
    """H_h(1) truncated at P."""
    primes = primes_to(P)
    log_factor = 0.0  # log H_h(1)
    log_factor += math.log(3.0 / 4.0)  # p = 2 ramified
    h_split_primes = []
    for p in primes:
        p = int(p)
        if p == 2:
            continue
        if p % 4 == 3:
            # inert
            log_factor += math.log(1.0 - 1.0 / (p * p))
        else:
            # p ≡ 1 mod 4, split
            if h % p == 0:
                # g_h(p) = 4
                f = (p + 4) * (p - 1) ** 2 / p ** 3
                h_split_primes.append(p)
            else:
                # g_h(p) = 2(p-2)/(p-1)
                f = (p * p + p - 4) * (p - 1) / p ** 3
            log_factor += math.log(f)
    return math.exp(log_factor), h_split_primes


def predict_Ch(h, P=10 ** 7):
    Hh1, splits = compute_Hh1_via_truncation(P, h)
    Ch = (math.pi / 4.0) * Hh1
    return Ch, Hh1, splits


if __name__ == "__main__":
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6

    # Empirical from Halasz-Dh-empirical.py at N=10^7:
    empirical = {1: 0.39277, 2: 0.39193, 5: 0.54259, 100: 0.54337}

    print(f"# Truncating Euler products at P = {P}")
    print(f"{'h':>5} | {'predicted C_h':>14} | {'empirical C_h':>14} | {'gap':>10} | {'splits|h':>20}")
    print("-" * 90)
    for h in [1, 2, 5, 100]:
        Ch_pred, Hh1, splits = predict_Ch(h, P)
        Ch_emp = empirical[h]
        gap = Ch_pred - Ch_emp
        print(f"{h:>5} | {Ch_pred:>14.6f} | {Ch_emp:>14.6f} | {gap:>+10.5f} | {str(splits):>20}")
