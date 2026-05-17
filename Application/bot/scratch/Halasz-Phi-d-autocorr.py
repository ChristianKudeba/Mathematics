"""Autocorrelation Phi_h(d) of \widetilde S_h on sf good e.

Computes
  Psi_h(d) := sum_{e=2}^{N-d}  S_h(e) * S_h(e+d)   (with S_h(e)=0 if e is
                                                    NOT square-free + good)
  Phi_h(d) := Psi_h(d) / N.

The off-diagonal of last session decomposes as
  |H_h|^2 - D_h = sum_{e1 != e2} S_h(e1) S_h(e2)
                = 2 * sum_{d=1}^{N-1} Psi_h(d)
(modulo trivial boundary).  So Psi_h(d) tells us how the *negative*
off-diagonal localizes in displacement d.

Also reports per-(N,h,d) the count of e with e and e+d BOTH sf good,
and the average S(e)S(e+d) on those e (for normalization).

Implementation: sequential Python loop over e in 2..N to compute S_h(e)
into a length-N array (one float per e per h), with S_h=0 if e is not
sf good.  Then for each d, vectorized numpy inner product on the array
(length N-d).  H is small (3 values), so per-h arrays cost 8N bytes
each = 8 MB at N=10^6; fits trivially.
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
    """Return list of distinct prime factors of e if e is square-free
    and all prime factors are 2 or p ≡ 1 (mod 4); else None."""
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


def compute_S_array(N, h_list, spf, root_cache):
    """For each e in 0..N return the array S[k][e] = \widetilde S_{h_list[k]}(e)
    if e is sf-good (and e >= 2), else 0.0."""
    H = len(h_list)
    S = np.zeros((H, N + 1), dtype=np.float64)
    h_arr = np.array(h_list, dtype=np.float64)
    parity_h = ((-1.0) ** h_arr).astype(np.float64)
    count_sfg = 0
    for e in range(2, N + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        count_sfg += 1
        v = np.ones(H, dtype=np.float64)
        for p in pf:
            if p == 2:
                v *= parity_h
            else:
                ep = e // p
                ep_inv = pow(int(ep), -1, p)
                ap = (root_cache[p] * ep_inv) % p
                angle = 2.0 * math.pi * h_arr * (ap / p)
                v *= 2.0 * np.cos(angle)
        S[:, e] = v
    return S, count_sfg


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e5)
    h_list = [1, 5, 20]
    d_list = [1, 2, 3, 5, 10, 100]

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
    S, count_sfg = compute_S_array(N, h_list, spf, root_cache)
    print(f"# S array build in {time.time()-t2:.1f}s, sf good count = {count_sfg}", file=sys.stderr)

    print(f"\n# N = {N}, sf good count = {count_sfg} ({count_sfg/N:.4f} N)")
    print(f"# h_list = {h_list}, d_list = {d_list}")

    # First, sanity-check: verify D_h := sum_e S_h(e)^2 and H_h := sum_e S_h(e),
    # against last session's tabulation at N=10^6, h=1,5,20
    print()
    print(f"{'h':>4} | {'H_h':>14} | {'|H_h|/sqN':>10} | {'D_h':>16} | {'D_h/N':>8}")
    print("-" * 70)
    sqrtN = math.sqrt(N)
    for k, h in enumerate(h_list):
        Hh = float(np.sum(S[k]))
        Dh = float(np.sum(S[k] * S[k]))
        print(f"{h:>4} | {Hh:>14.2f} | {abs(Hh)/sqrtN:>10.4f} | {Dh:>16.2f} | {Dh/N:>8.4f}")

    # Now: Psi_h(d) := sum_{e=2}^{N-d} S_h(e) S_h(e+d)
    # Phi_h(d) := Psi_h(d) / N
    # Conditional mean: avg of S_h(e)*S_h(e+d) over e such that both sf-good.
    print()
    print(f"{'h':>4} {'d':>4} | {'Psi':>16} | {'Psi/N':>10} | {'Psi/D_h':>10} | {'#both sfg':>10} | {'cond avg':>10}")
    print("-" * 90)
    for k, h in enumerate(h_list):
        Sk = S[k]
        Dh = float(np.sum(Sk * Sk))
        sfg_mask = (Sk != 0.0)  # mask of sf good e
        for d in d_list:
            # Inner product S_k[2:N-d+1] . S_k[2+d:N+1]
            left = Sk[2:N + 1 - d]
            right = Sk[2 + d:N + 1]
            psi = float(np.dot(left, right))
            both_sfg = int(np.sum(sfg_mask[2:N + 1 - d] & sfg_mask[2 + d:N + 1]))
            cond_avg = psi / both_sfg if both_sfg > 0 else 0.0
            print(f"{h:>4} {d:>4} | {psi:>16.2f} | {psi/N:>10.4f} | {psi/Dh:>10.4f} | {both_sfg:>10} | {cond_avg:>10.4f}")

    # Cross-check: 2 * sum_{d=1..N-1} Psi_h(d) should equal H_h^2 - D_h.
    # We'll compute the full sum for h = h_list[0] only (cheap, O(N) per d but N-1 d's so O(N^2) -- skip).
    # Instead we can compute via |H_h|^2 - D_h directly.
    print()
    for k, h in enumerate(h_list):
        Hh = float(np.sum(S[k]))
        Dh = float(np.sum(S[k] * S[k]))
        offdiag = Hh * Hh - Dh
        print(f"# h={h}: |H_h|^2 - D_h = {offdiag:.2f} = 2 * sum_{{d>=1}} Psi_h(d) (by translation argument)")
