"""Broad (N, h) scan of rho_h(N) := |H_h(N)|^2 / D_h(N).

Pickup hint #1 from session 2026-05-10T03-52-40Z. Existing data at N = 10^7,
h in {1, 2, 5, 100}: rho_h in {0.022, 0.146, 0.052, 0.852} -- highly
non-uniform across h.  This script measures rho_h on a denser h-grid and
at one larger N, to characterize rho_h(N, h) as a function of h.

Optimization vs Halasz-Dh-empirical.py:
  - sieve and root cache built ONCE per N
  - inner loop processes the SAME factorization of e for ALL h values in
    a single Python iteration
  - parity factor (-1)^h precomputed per h
"""
import argparse
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


def scan_one_N(N, h_list, log_N_at=None):
    """Compute H_h, D_h for sf-good e <= N, all h simultaneously.

    log_N_at: optional list of intermediate N values <= N at which to record
              partial H_h, D_h (for free intermediate trajectories).
    """
    print(f"\n#### N = {N}, |h_list| = {len(h_list)} ####", file=sys.stderr)
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

    parity = {h: ((-1) ** h) for h in h_list}
    H = {h: 0.0 for h in h_list}
    D = {h: 0.0 for h in h_list}
    count_sfg = 0
    intermediate = {}
    if log_N_at:
        log_N_at_set = sorted(set(int(x) for x in log_N_at if 0 < int(x) <= N))
    else:
        log_N_at_set = []
    next_log_idx = 0

    t2 = time.time()
    two_pi = 2.0 * math.pi
    for e in range(2, N + 1):
        pf = factor_sf_good(e, spf)
        if pf is not None:
            count_sfg += 1
            # Precompute angle base per prime: a_p_over_p = alpha_p * (e/p)^{-1}_p / p
            # For each prime in pf, store this real number once -- for h-values,
            # we just multiply by h.
            primes_data = []
            for p in pf:
                if p == 2:
                    primes_data.append(("two", None))
                else:
                    ep = e // p
                    ep_inv = pow(int(ep), -1, p)
                    ap = (root_cache[p] * ep_inv) % p
                    primes_data.append(("odd", ap / p))

            for h in h_list:
                v = 1.0
                for kind, base in primes_data:
                    if kind == "two":
                        v *= parity[h]
                    else:
                        v *= 2.0 * math.cos(two_pi * h * base)
                H[h] += v
                D[h] += v * v
        # Record intermediate snapshot if e crossed a logging threshold
        while next_log_idx < len(log_N_at_set) and e == log_N_at_set[next_log_idx]:
            intermediate[e] = (
                {h: H[h] for h in h_list},
                {h: D[h] for h in h_list},
                count_sfg,
            )
            next_log_idx += 1

    print(f"# Sum loop in {time.time()-t2:.1f}s, sf good count = {count_sfg}", file=sys.stderr)
    return H, D, count_sfg, intermediate


def report(N, h_list, H, D, count_sfg):
    sqrtN = math.sqrt(N)
    print(f"\n# N = {N}, sf good count = {count_sfg} (= {count_sfg/N:.4f} N)")
    print(f"{'h':>6} | {'H_h':>14} | {'|H_h|/sqrtN':>12} | {'D_h':>16} | {'D_h/N':>10} | {'rho=|H|^2/D':>12}")
    print("-" * 95)
    for h in h_list:
        absH = abs(H[h])
        rho = (H[h] * H[h]) / D[h] if D[h] > 0 else 0.0
        print(f"{h:>6} | {H[h]:>14.2f} | {absH/sqrtN:>12.4f} | {D[h]:>16.2f} | {D[h]/N:>10.4f} | {rho:>12.5f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--h", type=str, required=True,
                    help="comma-separated list of h values")
    ap.add_argument("--logN", type=str, default="",
                    help="comma-separated list of intermediate N to record")
    args = ap.parse_args()

    h_list = [int(x) for x in args.h.split(",") if x.strip()]
    log_N_at = [int(x) for x in args.logN.split(",") if x.strip()] if args.logN else []

    H, D, count_sfg, intermediate = scan_one_N(args.N, h_list, log_N_at)

    # Intermediate snapshots first
    for Ni in sorted(intermediate.keys()):
        Hi, Di, cnt = intermediate[Ni]
        report(Ni, h_list, Hi, Di, cnt)

    # Final
    report(args.N, h_list, H, D, count_sfg)
