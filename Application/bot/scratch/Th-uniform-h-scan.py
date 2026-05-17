"""Scan |T_h(N)|/sqrt(N) at N=10^7 across many h to test uniformity in h.

Self-contained reimplementation of the same logic (avoids the awkward
hyphenated module name).
"""
import math
import time
import sys
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


def crt_roots(pf, root_cache):
    roots = [0]
    modulus = 1
    for p in pf:
        rp = root_cache[p]
        p_roots = [1] if p == 2 else [rp, p - rp]
        new_roots = []
        for r in roots:
            for s in p_roots:
                new_modulus = modulus * p
                diff = (s - r) % p
                inv_modulus = pow(modulus, -1, p)
                k = (diff * inv_modulus) % p
                rp_new = (r + k * modulus) % new_modulus
                new_roots.append(rp_new)
        roots = new_roots
        modulus = modulus * p
    return roots


def compute_Th_for_h_list(N_target, spf, root_cache, h_list):
    T = {h: 0.0 + 0.0j for h in h_list}
    two_pi = 2.0 * math.pi
    for e in range(2, N_target + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        roots = crt_roots(pf, root_cache)
        for r in roots:
            y = (N_target - r) % e
            for h in h_list:
                phase = two_pi * h * y / e
                T[h] += complex(math.cos(phase), math.sin(phase))
    return T


if __name__ == "__main__":
    # Fix N = 10^7; scan h from 1 to 100, then logarithmic up to 1000.
    N = int(1e7) if len(sys.argv) < 2 else int(sys.argv[1])
    h_list = list(range(1, 21)) + [25, 30, 50, 75, 100, 150, 200, 300, 500, 1000]

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
    T = compute_Th_for_h_list(N, spf, root_cache, h_list)
    print(f"# Sieve + Th for {len(h_list)} h-values in {time.time()-t2:.1f}s", file=sys.stderr)

    sqrtN = math.sqrt(N)
    print(f"\n# N = {N}, sqrt(N) = {sqrtN:.1f}")
    print(f"{'h':>5} | {'|T_h|':>12} | {'|T_h|/sqrt(N)':>14} | {'Re(T_h)/sqrt(N)':>16} | {'Im(T_h)/sqrt(N)':>16}")
    print("-" * 75)
    max_norm = 0.0
    for h in h_list:
        Th = T[h]
        norm = abs(Th) / sqrtN
        max_norm = max(max_norm, norm)
        print(f"{h:>5} | {abs(Th):>12.2f} | {norm:>14.4f} | {Th.real/sqrtN:>16.4f} | {Th.imag/sqrtN:>16.4f}")
    print(f"\n# max |T_h|/sqrt(N) over scanned h: {max_norm:.4f}")
