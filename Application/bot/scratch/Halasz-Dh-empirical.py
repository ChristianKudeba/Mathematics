"""Compute the diagonal second moment

    D_h(N) := sum_{e <= N, sf, good} |\widetilde S_h(e)|^2
            = sum_{e}     prod_{p|e} 4 cos^2(2 pi h alpha_p (e/p)^{-1} / p)

alongside the prev session's

    H_h(N) := sum_{e <= N, sf, good} \widetilde S_h(e).

The point: prev session showed |H_h|/sqrt(N) bounded by ~1.36 across 23 (N,h)
points -- empirically a CLT/sqrt(N) rate, much faster than Halasz's
~N exp(-c log log N).  The natural framework that DOES give sqrt(N) is the
diagonal / Cauchy-Schwarz / second-moment one:

    |H_h(N)|^2 <= (count_sfg) * D_h(N)               (Cauchy-Schwarz)
    |H_h(N)|^2 ~ D_h(N)                              (if no off-diagonal cancellation)

This session pins which regime we are in by computing D_h directly.

Analytic approximation (averaging over (e/p)^{-1} mod p):
    E_k[(2 cos(2 pi h alpha_p k / p))^2] = 2 - 2/(p-1)
       (since 4 cos^2(theta) = 2 + 2 cos(2 theta), and sum over k!=0 of cos(...) = -1)
so heuristically
    D_h(N) ~ sum_{e <= N, sf good} prod_{p|e} 2(p-2)/(p-1) =: D_h^heur(N).
The Dirichlet series for the heuristic sum factors as G_h(s) = zeta_K(s) * H_h(s)
with H_h holomorphic and nonzero at s=1, hence
    D_h^heur(N) ~ (pi/4) H_h(1) * N      (NO log factor; kappa=1).
See `P12-Halasz-Dh-diagonal.md` for the full derivation.
"""
import math
import sys
import time

import numpy as np


def smallest_prime_factor(N):
    spf = np.zeros(N + 1, dtype=np.int64)
    for i in range(2, N + 1):
        if spf[i] == 0:
            for j in range(i, N + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf


def find_root_mod_p(p):
    if p == 2:
        return 1
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            break
    return pow(z, (p - 1) // 4, p)


def factor_sf_good(e, spf):
    pf = []
    n = e
    while n > 1:
        p = int(spf[n])
        n //= p
        if n % p == 0:
            return None
        if p != 2 and p % 4 == 3:
            return None
        pf.append(p)
    return pf


def factor_for_h(pf, root_cache, h, e):
    """Return (S, S2) where S = \widetilde S_h(e) (real), S2 = |S|^2 = S*S."""
    two_pi = 2.0 * math.pi
    S = 1.0
    for p in pf:
        ep = e // p
        if p == 2:
            sign = (-1) ** h
            S *= sign
        else:
            ep_inv = pow(int(ep), -1, p)
            ap = (root_cache[p] * ep_inv) % p
            angle = two_pi * h * ap / p
            S *= 2.0 * math.cos(angle)
    return S, S * S


def compute_HhDh(N_target, spf, root_cache, h_list):
    """Compute (H_h, D_h, count_sfg) for sf good e <= N_target."""
    H = {h: 0.0 for h in h_list}
    D = {h: 0.0 for h in h_list}
    count_sfg = 0
    for e in range(2, N_target + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        count_sfg += 1
        for h in h_list:
            S, S2 = factor_for_h(pf, root_cache, h, e)
            H[h] += S
            D[h] += S2
    return H, D, count_sfg


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e5)
    h_list = [1, 2, 5, 100]
    if len(sys.argv) > 2:
        h_list = [int(x) for x in sys.argv[2:]]

    t0 = time.time()
    spf = smallest_prime_factor(N)
    print(f"# SPF sieve to {N} in {time.time()-t0:.1f}s", file=sys.stderr)

    t1 = time.time()
    root_cache = {}
    is_prime = (spf == np.arange(N + 1, dtype=np.int64))
    for p in range(2, N + 1):
        if is_prime[p] and (p == 2 or p % 4 == 1):
            root_cache[p] = find_root_mod_p(p)
    print(f"# Root cache for {len(root_cache)} primes in {time.time()-t1:.1f}s", file=sys.stderr)

    t2 = time.time()
    H, D, count_sfg = compute_HhDh(N, spf, root_cache, h_list)
    print(f"# Sum loop in {time.time()-t2:.1f}s, sf good count = {count_sfg}", file=sys.stderr)

    sqrtN = math.sqrt(N)
    logN = math.log(N)
    NlogN = N * logN
    print(f"\n# N = {N}, sqrt(N) = {sqrtN:.2f}, log N = {logN:.3f}")
    print(f"# sf good count = {count_sfg} (= {count_sfg/N:.4f} * N)")
    print(f"{'h':>5} | {'H_h':>14} | {'|H_h|/sqrtN':>12} | {'D_h':>16} | {'D_h/(N log N)':>14} | {'|H_h|^2/D_h':>12} | {'|H_h|^2/(D_h*sf)':>16}")
    print("-" * 120)
    for h in h_list:
        Hv = H[h]
        Dv = D[h]
        ratio_HsqN = abs(Hv) / sqrtN
        ratio_DNlogN = Dv / NlogN
        ratio_H2D = (Hv * Hv) / Dv if Dv > 0 else 0.0
        # CS upper bound: |H|^2 <= count_sfg * D, so |H|^2 / (count_sfg D) <= 1
        ratio_H2_count_D = (Hv * Hv) / (count_sfg * Dv) if Dv > 0 else 0.0
        print(f"{h:>5} | {Hv:>14.2f} | {ratio_HsqN:>12.4f} | {Dv:>16.2f} | {ratio_DNlogN:>14.4f} | {ratio_H2D:>12.4f} | {ratio_H2_count_D:>16.5f}")
