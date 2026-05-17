"""Dyadic-block profile of Psi_h(d) at N = 3*10^6 and (optionally) N = 10^7.

For each dyadic block [2^k, 2^{k+1}) compute
    sigma_h(k) := sum_{d in [2^k, 2^{k+1}) and d < N-1} Psi_h(d)
where Psi_h(d) := sum_e S_h(e) S_h(e+d).  Output:
  - per-block sigma_h(k), running cumulative, and the ratio sigma_h(k)/T_h.
  - sign pattern across k.
This is pickup hint #1 from session 2026-05-09T18-30-00Z: discriminates
"negative-wave + positive-correction" structure (signed alternation
across blocks) from a monotone all-negative profile.

Identity (*) cross-check carried over: sum_d Psi_h(d) = (|H_h|^2 - D_h)/2
to numerical precision.
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


def compute_S_array(N, h_list, spf, root_cache):
    H = len(h_list)
    S = np.zeros((H, N + 1), dtype=np.float64)
    h_arr = np.array(h_list, dtype=np.float64)
    parity_h = ((-1.0) ** h_arr).astype(np.float64)
    for e in range(2, N + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
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
    return S


def autocorrelation_fft(x):
    n = len(x)
    nfft = 1
    while nfft < 2 * n:
        nfft *= 2
    X = np.fft.rfft(x, nfft)
    R = np.fft.irfft(X * np.conj(X), nfft).real[:n]
    return R


def dyadic_blocks(R, N):
    """Returns list of (k, lo, hi, sigma_k, count) where the block is
    d in [lo, hi) intersected with [1, N-2]; sigma_k = sum of R over that range."""
    out = []
    k = 0
    while (1 << k) <= N - 2:
        lo = 1 << k
        hi = min(1 << (k + 1), N - 1)
        sigma_k = float(np.sum(R[lo:hi]))
        count = hi - lo
        out.append((k, lo, hi, sigma_k, count))
        k += 1
    return out


def run_one(N, h_list):
    print(f"\n############# N = {N}, h_list = {h_list} #############", file=sys.stderr)
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
    S = compute_S_array(N, h_list, spf, root_cache)
    print(f"# S array build in {time.time()-t2:.1f}s", file=sys.stderr)

    results = []
    for k_idx, h in enumerate(h_list):
        x = S[k_idx]
        t3 = time.time()
        R = autocorrelation_fft(x)
        print(f"# N={N}, h={h}: autocorr FFT in {time.time()-t3:.1f}s", file=sys.stderr)

        Hh = float(np.sum(x))
        Dh = float(R[0])
        offdiag = Hh * Hh - Dh
        target = offdiag / 2.0   # = T_h

        # Cross-check identity (*) over d in [1, N-2]
        sum_Psi_to_Nm2 = float(np.sum(R[1:N - 1]))
        rel_err = abs(2 * sum_Psi_to_Nm2 - offdiag) / max(abs(offdiag), 1)

        # Dyadic blocks
        blocks = dyadic_blocks(R, N)

        # Total off-diagonal recovered by blocks (= sum_Psi_to_Nm2 modulo
        # the boundary pad; we cap hi at N-1 inside dyadic_blocks).
        block_sum = sum(b[3] for b in blocks)
        block_rel_err = abs(block_sum - sum_Psi_to_Nm2) / max(abs(sum_Psi_to_Nm2), 1)

        results.append({
            "N": N, "h": h,
            "Hh": Hh, "Dh": Dh, "T_h": target, "rel_err": rel_err,
            "block_rel_err": block_rel_err,
            "blocks": blocks,
        })
    return results


def print_results(results):
    for r in results:
        print(f"\n##### N = {r['N']}, h = {r['h']} #####")
        print(f"  H_h = {r['Hh']:.1f}")
        print(f"  D_h = {r['Dh']:.1f}")
        print(f"  T_h = (H_h^2 - D_h)/2 = {r['T_h']:.1f}")
        print(f"  rel err of identity (*): {r['rel_err']:.2e}")
        print(f"  rel err of block coverage vs identity (*): {r['block_rel_err']:.2e}")
        print()
        T = r["T_h"]
        cum = 0.0
        print(f"  {'k':>3} {'lo':>10} {'hi':>10} {'count':>10} {'sigma_h(k)':>16} {'sigma/T_h':>12} {'cum':>16} {'cum/T_h':>10} {'sign':>5}")
        for (k, lo, hi, sigma_k, count) in r["blocks"]:
            cum += sigma_k
            ratio = sigma_k / T if T != 0 else float("nan")
            cum_ratio = cum / T if T != 0 else float("nan")
            sign = "+" if sigma_k > 0 else ("-" if sigma_k < 0 else "0")
            print(f"  {k:>3} {lo:>10} {hi:>10} {count:>10} {sigma_k:>16.1f} {ratio:>12.5f} {cum:>16.1f} {cum_ratio:>10.5f} {sign:>5}")


if __name__ == "__main__":
    # Primary leg: N = 3e6, h in {1, 5}. Carries forward overshoot at (3e6, 1).
    h_list_main = [1, 5]
    Ns_main = [int(3e6)]
    all_results = []
    for N in Ns_main:
        results = run_one(N, h_list_main)
        all_results.extend(results)

    # Secondary leg: N = 1e7, h = 1 only (memory + time).
    if len(sys.argv) > 1 and sys.argv[1] == "--big":
        results_big = run_one(int(1e7), [1])
        all_results.extend(results_big)

    print_results(all_results)
