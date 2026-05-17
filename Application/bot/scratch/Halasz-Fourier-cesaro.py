"""Test whether R(N, H) := sum_h |H_h|^2 / sum_h D_h converges to 1 as H -> infty.

Theoretical claim (this session):
   For fixed N, R(N, H) -> 1 as H -> infty.
   Reason: \widetilde S_h(e) = sum_eps e^{2 pi i h \tilde\alpha_eps(e)}.
   For e_1 != e_2 sf-good, all beta = \tilde\alpha_{eps_1}(e_1) + \tilde\alpha_{eps_2}(e_2)
   are nonzero mod 1 (Lemma F.1). Hence by orthogonality
       (1/H) sum_{h=1}^H e^{2 pi i h beta} -> 0,
   so off-diagonal vanishes Cesaro and R -> 1.

Test: small N (so lcm of primes is small and convergence is observable).
"""
import math
import sys
import time

import numpy as np


def factor_sf_good(e):
    """Return list of primes if e is squarefree and all primes are 2 or ==1 mod 4; else None."""
    n = e
    primes = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return None
            if p > 2 and p % 4 == 3:
                return None
            primes.append(p)
        else:
            p += 1
    if n > 1:
        if n > 2 and n % 4 == 3:
            return None
        primes.append(n)
    return primes


def find_root_mod_p(p):
    """Find sqrt(-1) mod p, p == 1 mod 4 or p = 2."""
    if p == 2:
        return 1
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            return pow(z, (p - 1) // 4, p)


def precompute_e_data(N):
    """Return list of (e, [(p, ap)]) for sf-good e in [2, N]."""
    out = []
    for e in range(2, N + 1):
        primes = factor_sf_good(e)
        if primes is None:
            continue
        prime_data = []
        for p in primes:
            if p == 2:
                # We'll handle p=2 specially: contributes (-1)^h
                prime_data.append((2, None))
            else:
                ep = e // p
                ep_inv = pow(ep, -1, p)
                ip = find_root_mod_p(p)
                ap = (ip * ep_inv) % p
                prime_data.append((p, ap))
        out.append((e, prime_data))
    return out


def compute_R_chunked(e_data, H, chunk=10000):
    """Compute R(N, H) = (sum_{h=1}^H |H_h|^2) / (sum_{h=1}^H D_h) by chunking over h."""
    sum_H2 = 0.0
    sum_D = 0.0
    h_low = 1
    while h_low <= H:
        h_high = min(h_low + chunk - 1, H)
        sz = h_high - h_low + 1
        h_arr = np.arange(h_low, h_high + 1, dtype=np.float64)
        Hh = np.zeros(sz, dtype=np.float64)
        Dh = np.zeros(sz, dtype=np.float64)
        for e, prime_data in e_data:
            S = np.ones(sz, dtype=np.float64)
            for (p, ap) in prime_data:
                if p == 2:
                    S *= ((-1.0) ** h_arr)
                else:
                    angle = 2.0 * math.pi * h_arr * (ap / p)
                    S *= 2.0 * np.cos(angle)
            Hh += S
            Dh += S * S
        sum_H2 += float(np.sum(Hh * Hh))
        sum_D += float(np.sum(Dh))
        h_low = h_high + 1
    return sum_H2, sum_D


if __name__ == "__main__":
    Ns = [10, 20, 50, 100]
    Hs = [100, 1000, 10000, 100000, 1000000]

    for N in Ns:
        e_data = precompute_e_data(N)
        es = [e for e, _ in e_data]
        # lcm of all primes appearing
        all_primes = set()
        for _, pd in e_data:
            for (p, _) in pd:
                all_primes.add(p)
        lcm = 1
        for p in sorted(all_primes):
            lcm *= p

        print(f"# N = {N}, sf-good count = {len(e_data)}, primes = {sorted(all_primes)}, lcm = {lcm}")
        print(f"# es: {es[:25]}{'...' if len(es)>25 else ''}")

        for H in Hs:
            t0 = time.time()
            sum_H2, sum_D = compute_R_chunked(e_data, H)
            R = sum_H2 / sum_D if sum_D > 0 else float('nan')
            dt = time.time() - t0
            print(f"  H = {H:>8}: R = {R:.6f}    (sum |H|^2 = {sum_H2:.4e}, sum D = {sum_D:.4e}, t = {dt:.1f}s)")
        print()
