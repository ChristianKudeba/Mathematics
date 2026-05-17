"""Extended d-scan of Phi_h(d) at N = 10^6, h ∈ {1, 5, 20}.

Computes Psi_h(d) := sum_e S_h(e) S_h(e+d) at a wider grid of d, including
both 'parity-killed' even-mod-4 d's (which give 0) and a longer d range
to see whether the off-diagonal localizes anywhere.

Also computes:
  - Per-h cumulative sum sum_{d=1..D} Psi_h(d) at D = 10, 100, 1000, 10000, N-1
    to localize where the bulk of |H_h|^2 - D_h sits.
  - Per-h sum_{d=1..N-1} Psi_h(d) by direct evaluation (vectorized
    numpy convolution-style via single FFT-free pass).

Memory: 3 * (N+1) * 8 = 24 MB for the S array; cumulative Psi via O(N^2) loop
is too slow.  Instead use FFT autocorrelation: Psi_h(d) for ALL d at once
in O(N log N).
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
    """Compute Psi(d) := sum_{i} x[i] * x[i+d] for all d = 0, ..., len(x)-1
    via FFT (not subtracting mean; raw correlation)."""
    n = len(x)
    nfft = 1
    while nfft < 2 * n:
        nfft *= 2
    X = np.fft.rfft(x, nfft)
    R = np.fft.irfft(X * np.conj(X), nfft).real[:n]
    return R


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e6)
    h_list = [1, 5, 20]

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

    print(f"\n# N = {N}, h_list = {h_list}")

    # Compute full autocorrelation Psi_h(d) for d=0..N-1 via FFT.
    for k, h in enumerate(h_list):
        x = S[k]
        t3 = time.time()
        R = autocorrelation_fft(x)  # R[d] = sum_i x[i] x[i+d]
        print(f"# h={h}: autocorr FFT in {time.time()-t3:.1f}s", file=sys.stderr)

        Hh = float(np.sum(x))
        Dh = float(R[0])  # sum x^2
        offdiag = Hh * Hh - Dh
        sum_Psi_pos = float(np.sum(R[1:]))   # sum_{d=1}^{N-1} should equal offdiag/2 modulo boundary
        # check
        print(f"# h={h}: D_h={Dh:.1f}  Hh={Hh:.1f}  H^2-D = {offdiag:.1f}  2*sum_d Psi(d) = {2*sum_Psi_pos:.1f}  rel err = {abs(2*sum_Psi_pos - offdiag)/max(abs(offdiag),1):.4f}")

        # Tabulate Psi at chosen d values
        d_grid = [1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 25, 31, 51, 101, 251, 501, 1001, 5001, 10001, 50001, 100001]
        print(f"\n## h = {h}")
        print(f"{'d':>7} | {'Psi_h(d)':>14} | {'Psi/D_h':>10} | {'Psi/N':>10}")
        print("-" * 55)
        for d in d_grid:
            if d >= N:
                continue
            psi = R[d]
            print(f"{d:>7} | {psi:>14.2f} | {psi/Dh:>10.5f} | {psi/N:>10.5f}")

        # Cumulative sums
        cum_targets = [10, 100, 1000, 10000, 100000, N - 1]
        cum = 0.0
        cum_results = {}
        # We need cumulative through d (sum_{d'=1..d} R[d'])
        prefix = np.cumsum(R)  # prefix[d] = sum_{d'=0..d} R[d']
        print()
        print(f"# Cumulative sum_{{d=1..D}} Psi_h(d) for h={h}:")
        print(f"{'D':>10} | {'cum sum':>14} | {'cum / (off/2)':>16}")
        print("-" * 50)
        for D in cum_targets:
            if D >= N:
                D = N - 1
            cs = float(prefix[D]) - float(R[0])  # subtract d=0
            target = offdiag / 2.0
            print(f"{D:>10} | {cs:>14.2f} | {cs/target if abs(target)>0 else 0:>16.4f}")
        print()
