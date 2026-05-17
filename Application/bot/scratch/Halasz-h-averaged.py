"""h-averaged second moment of H_h(N).

Empirical preview of the prev-session promoted next analytic step.

For h = 1..H_max, compute:
    H_h(N) := sum_{e <= N, sf, good} \widetilde S_h(e)
    D_h(N) := sum_{e <= N, sf, good} |\widetilde S_h(e)|^2
and report:
    R(N, H) := sum_{h=1}^H |H_h(N)|^2 / sum_{h=1}^H D_h(N)
    R_single(h) := |H_h(N)|^2 / D_h(N)        (varies wildly per prev session)

Hypothesis being tested: averaging over h makes the off-diagonal
contribution sum_{e_1 != e_2} S_h(e_1) S_h(e_2) average out to zero,
so R(N, H) -> 1 as H grows. If yes, the diagonal D is the binding
term for the h-averaged second moment, giving |H_h|^2 ~ D_h ~ C_h N
*on average over h*, hence |H_h| ~ sqrt(N) on average over h.

Implementation: per-e CRT product formula computed simultaneously for
all h via vectorized cos. Per e, omega(e) calls to np.cos on a length-H_max
array. SPF sieve for factorization; Tonelli for sqrt(-1) mod p.
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


def compute_h_averaged(N, spf, root_cache, H_max):
    """Compute H_h(N), D_h(N) for h = 1..H_max simultaneously.

    Returns (Hh, Dh, count_sfg) with Hh[i] = H_{i+1}(N) (length H_max).
    """
    h_arr = np.arange(1, H_max + 1, dtype=np.float64)
    two_pi_h = 2.0 * math.pi * h_arr  # shape (H_max,)
    parity_h = ((-1.0) ** h_arr).astype(np.float64)  # for p=2

    Hh = np.zeros(H_max, dtype=np.float64)
    Dh = np.zeros(H_max, dtype=np.float64)
    count_sfg = 0

    for e in range(2, N + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        count_sfg += 1
        S = np.ones(H_max, dtype=np.float64)
        for p in pf:
            if p == 2:
                S *= parity_h
            else:
                ep = e // p
                ep_inv = pow(int(ep), -1, p)
                ap = (root_cache[p] * ep_inv) % p
                # angle[i] = 2*pi*(i+1)*ap/p
                angle = two_pi_h * (ap / p)
                S *= 2.0 * np.cos(angle)
        Hh += S
        Dh += S * S
    return Hh, Dh, count_sfg


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e5)
    H_max = int(sys.argv[2]) if len(sys.argv) > 2 else 20

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
    Hh, Dh, count_sfg = compute_h_averaged(N, spf, root_cache, H_max)
    print(f"# Sum loop in {time.time()-t2:.1f}s, sf good count = {count_sfg}", file=sys.stderr)

    sqrtN = math.sqrt(N)

    print(f"\n# N = {N}, H_max = {H_max}")
    print(f"# sf good count = {count_sfg} (= {count_sfg/N:.4f} N)")
    print(f"# sqrt(N) = {sqrtN:.2f}")
    print()
    print(f"{'h':>4} | {'H_h':>14} | {'|H_h|/sqN':>10} | {'D_h':>16} | {'D_h/N':>8} | {'|H_h|^2/D_h':>12}")
    print("-" * 90)
    for i, h in enumerate(range(1, H_max + 1)):
        Hv = Hh[i]
        Dv = Dh[i]
        r_HsqN = abs(Hv) / sqrtN
        r_DN = Dv / N
        r_H2D = (Hv * Hv) / Dv if Dv > 0 else 0.0
        print(f"{h:>4} | {Hv:>14.2f} | {r_HsqN:>10.4f} | {Dv:>16.2f} | {r_DN:>8.4f} | {r_H2D:>12.4f}")

    sum_H2 = float(np.sum(Hh * Hh))
    sum_D = float(np.sum(Dh))
    ratio_summed = sum_H2 / sum_D if sum_D > 0 else 0.0
    print()
    print(f"sum_{{h=1}}^{H_max} |H_h|^2 = {sum_H2:.4e}")
    print(f"sum_{{h=1}}^{H_max} D_h    = {sum_D:.4e}")
    print(f"R(N,H) = sum |H_h|^2 / sum D_h = {ratio_summed:.4f}")
    print(f"sum |H_h|^2 / (H_max * N) = {sum_H2 / (H_max * N):.4f}")
    print(f"sum D_h    / (H_max * N) = {sum_D / (H_max * N):.4f}")

    # Mean of single-h ratios
    single_ratios = [(Hh[i] * Hh[i]) / Dh[i] if Dh[i] > 0 else 0.0 for i in range(H_max)]
    print(f"mean |H_h|^2/D_h over h = 1..{H_max}: {np.mean(single_ratios):.4f}")
    print(f"std  |H_h|^2/D_h over h = 1..{H_max}: {np.std(single_ratios):.4f}")
    print(f"min  |H_h|^2/D_h: {np.min(single_ratios):.4f}")
    print(f"max  |H_h|^2/D_h: {np.max(single_ratios):.4f}")
