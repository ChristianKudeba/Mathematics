"""Compute
    H_h(N) := sum_{e <= N, sf, good} \widetilde S_h(e)
(the unnormalized partial sum; ratios |H_h|/N and |H_h|/sqrtN are reported)
where
    \widetilde S_h(e) := sum over roots r of (n^2+1) mod e of e^{-2 pi i h r / e}
    "good" e := e is sf, and every prime factor of e is 2 or 1 mod 4.

This is the multiplicative-root-weight (in modulus, |\widetilde S_h(e)| <= 2^omega(e))
sum that prev session identified as the binding direction (Halasz mean-value
on the bounded mult function f_h(p) = 2 cos(2 pi h r_p / p) at split p).

Decay rate ~ N exp(-c log log N) is the Halasz prediction (assuming
mean(f_h(p)) over p <= X is small via Weyl/Hooley).

Comparison: at h = 0, f_0(p) = 2 always, and \widetilde S_0(e) = 2^omega(e) >= 0,
so H_0(N) is positive and grows as the trivial sf good count -- sanity check.
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


def sum_phases_via_product(pf, root_cache, h, e):
    """Compute sum_{r: r^2+1 ≡ 0 (e)} exp(-2 pi i h r / e) as a product
    over primes p|e. Uses CRT formula:
        r/e ≡ sum_p r_p * (e/p)^{-1}_p / p  (mod 1)
    so the sum factors as
        prod_p [exp(-2 pi i h alpha_p (e/p)^{-1} / p) + exp(+2 pi i h alpha_p (e/p)^{-1} / p)]
        = prod_p 2 cos(2 pi h alpha_p (e/p)^{-1} / p)
    (At p = 2, only one root, factor = exp(-2 pi i h * 1 * (e/2)^{-1}_2 / 2)
     = exp(-i pi h * (e/2)) which is +/- 1 depending on parity of h*(e/2);
     since e is sf and e is even => e/2 is odd, so this is exp(-i pi h) = (-1)^h.)
    """
    two_pi = 2.0 * math.pi
    prod = 1.0 + 0.0j
    for p in pf:
        ep = e // p
        if p == 2:
            # single root r = 1 mod 2, ep is odd since e sf
            sign = (-1) ** h
            prod *= sign
        else:
            ep_inv = pow(ep, -1, p)
            ap = (root_cache[p] * ep_inv) % p
            angle = two_pi * h * ap / p
            prod *= 2.0 * math.cos(angle)
    return prod


def compute_Hh(N_target, spf, root_cache, h_list):
    """Compute sum_e \widetilde S_h(e) for sf good e <= N_target."""
    H = {h: 0.0 + 0.0j for h in h_list}
    count_sfg = 0
    for e in range(2, N_target + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        count_sfg += 1
        for h in h_list:
            H[h] += sum_phases_via_product(pf, root_cache, h, e)
    return H, count_sfg


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
    H, count_sfg = compute_Hh(N, spf, root_cache, h_list)
    print(f"# Sum loop in {time.time()-t2:.1f}s, sf good count = {count_sfg}", file=sys.stderr)

    sqrtN = math.sqrt(N)
    logN = math.log(N)
    loglogN = math.log(max(logN, 2.0))
    print(f"\n# N = {N}, sqrt(N) = {sqrtN:.2f}, log N = {logN:.3f}, log log N = {loglogN:.3f}")
    print(f"# sf good count = {count_sfg} (~{count_sfg/N:.3f} * N)")
    print(f"{'h':>5} | {'Re(H_h)':>14} | {'Im(H_h)':>14} | {'|H_h|':>14} | {'|H_h|/N':>10} | {'|H_h|/sqrtN':>12} | {'|H_h|/(N*exp(-loglogN))':>22}")
    print("-" * 110)
    for h in h_list:
        absH = abs(H[h])
        ratio_N = absH / N
        ratio_sqN = absH / sqrtN
        # Halasz prediction: ~ N exp(-c log log N) for small c; we report ratio with c=1
        ratio_halasz = absH / (N * math.exp(-loglogN))
        print(f"{h:>5} | {H[h].real:>14.2f} | {H[h].imag:>14.2f} | {absH:>14.2f} | {ratio_N:>10.5f} | {ratio_sqN:>12.4f} | {ratio_halasz:>22.4f}")
