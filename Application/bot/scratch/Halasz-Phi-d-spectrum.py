"""Power-spectrum |X(xi)|^2 of widetilde S_h(e) on linear xi-grid.

Pickup hint #1 from session 2026-05-10T00-49-59Z: discriminate
single-mode (sharp peak), single-complex-pole damped oscillation
(Lorentzian-shaped peak at xi*), multi-mode (multiple peaks).

For each (N, h):
  1. Build S array on sf-good e in [2, N].
  2. FFT (zero-padded to 2*N) -> X(k) for k = 0..nfft-1.
  3. P(xi) := |X(xi)|^2 with xi = k/nfft, restricted to xi in [0, 1/2].
  4. Bin P into log-spaced xi-decades and into dyadic xi-blocks.
  5. Cross-checks:
     - sum_k |X(k)|^2 / nfft = sum_e S(e)^2 = D_h  (Parseval).
     - X(0) = sum_e S(e) = H_h.
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


def compute_S_array(N, h, spf, root_cache):
    S = np.zeros(N + 1, dtype=np.float64)
    parity_h = (-1.0) ** h
    for e in range(2, N + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        v = 1.0
        for p in pf:
            if p == 2:
                v *= parity_h
            else:
                ep = e // p
                ep_inv = pow(int(ep), -1, p)
                ap = (root_cache[p] * ep_inv) % p
                angle = 2.0 * math.pi * h * (ap / p)
                v *= 2.0 * math.cos(angle)
        S[e] = v
    return S


def power_spectrum(S, nfft):
    """Return P[k] = |X(k)|^2 for k = 0..nfft//2 (one-sided), where X = rfft(S, nfft)."""
    X = np.fft.rfft(S, nfft)
    return (X * np.conj(X)).real


def decade_bins(xi_min=1e-9, xi_max=0.5, n_per_decade=2):
    """Log-spaced bin edges from xi_min up to xi_max, with n_per_decade per decade."""
    log10_min = math.log10(xi_min)
    log10_max = math.log10(xi_max)
    n_bins = int(round((log10_max - log10_min) * n_per_decade))
    edges = np.logspace(log10_min, log10_max, n_bins + 1)
    return edges


def bin_power_log(P, nfft, edges):
    """Sum P[k] over k such that xi = k/nfft falls in each [edges[i], edges[i+1])."""
    n_one_sided = len(P)  # = nfft//2 + 1
    k = np.arange(n_one_sided)
    xi = k / nfft
    # For k=0, xi=0; treat the DC mode (H_h^2) separately.
    out = []
    dc_power = float(P[0])
    out.append(("DC (xi=0)", 0.0, 0.0, dc_power, 1))
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        mask = (xi >= lo) & (xi < hi)
        bin_sum = float(np.sum(P[mask]))
        bin_count = int(np.sum(mask))
        out.append((f"[{lo:.2e}, {hi:.2e})", lo, hi, bin_sum, bin_count))
    return out


def bin_power_dyadic(P, nfft):
    """Bin power into dyadic xi-blocks 2^{-j-1} <= xi < 2^{-j} for j = 1, 2, ..."""
    n_one_sided = len(P)
    k = np.arange(n_one_sided)
    xi = k / nfft
    # j_max so that 2^{-j_max} > 1/nfft
    j_max = int(math.log2(nfft)) - 1
    out = []
    dc_power = float(P[0])
    out.append((-1, 0.0, 0.0, dc_power, 1))  # j = -1 means DC
    for j in range(j_max, 0, -1):
        lo = 2.0 ** (-(j + 1))
        hi = 2.0 ** (-j)
        if hi > 0.5:
            hi = 0.5
        if lo >= 0.5:
            continue
        mask = (xi >= lo) & (xi < hi)
        bin_sum = float(np.sum(P[mask]))
        bin_count = int(np.sum(mask))
        out.append((j, lo, hi, bin_sum, bin_count))
    return out


def run_one(N, h):
    print(f"\n############# N = {N}, h = {h} #############", file=sys.stderr)
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
    S = compute_S_array(N, h, spf, root_cache)
    print(f"# S array build in {time.time()-t2:.1f}s", file=sys.stderr)

    H_h = float(np.sum(S))
    D_h = float(np.sum(S * S))
    T_h = 0.5 * (H_h * H_h - D_h)

    # Choose nfft as next power of 2 >= 2 * N (so dyadic xi-bins line up cleanly)
    nfft = 1
    while nfft < 2 * (N + 1):
        nfft *= 2

    t3 = time.time()
    P = power_spectrum(S, nfft)
    print(f"# rfft length {nfft} in {time.time()-t3:.1f}s", file=sys.stderr)

    # Parseval: sum_k |X(k)|^2 = nfft * sum_e |S(e)|^2  (numpy convention: rfft is unnormalized)
    parseval_lhs = float(P[0] + 2 * np.sum(P[1:-1]) + P[-1])
    parseval_rhs = nfft * D_h
    parseval_rel_err = abs(parseval_lhs - parseval_rhs) / max(parseval_rhs, 1)

    # X(0) = H_h
    X0_match = abs(math.sqrt(P[0]) - abs(H_h)) / max(abs(H_h), 1e-9)

    # Decade bins
    edges = decade_bins(xi_min=1.0 / nfft, xi_max=0.5, n_per_decade=2)
    decade = bin_power_log(P, nfft, edges)

    # Dyadic xi-bins
    dyadic = bin_power_dyadic(P, nfft)

    return {
        "N": N, "h": h, "nfft": nfft,
        "H_h": H_h, "D_h": D_h, "T_h": T_h,
        "parseval_rel_err": parseval_rel_err,
        "X0_match": X0_match,
        "decade": decade,
        "dyadic": dyadic,
    }


def print_results(r):
    print(f"\n##### N = {r['N']}, h = {r['h']}, nfft = {r['nfft']} #####")
    print(f"  H_h = {r['H_h']:.1f}")
    print(f"  D_h = {r['D_h']:.1f}")
    print(f"  T_h = {r['T_h']:.1f}")
    print(f"  Parseval rel err: {r['parseval_rel_err']:.2e}")
    print(f"  X(0) vs |H_h| rel err: {r['X0_match']:.2e}")

    nfft = r["nfft"]
    print()
    print(f"  --- Decade bins (one-sided P, total power = nfft * D_h) ---")
    print(f"  {'bin':>30} {'count':>10} {'sum P':>20} {'frac of total':>14}")
    total = nfft * r["D_h"]
    cum = 0.0
    for label, lo, hi, bs, bc in r["decade"]:
        cum += bs
        frac = bs / total
        print(f"  {label:>30} {bc:>10} {bs:>20.3e} {frac:>14.4e}")
    print(f"  cumulative sum (decade bins) / total = {cum/total:.4f}")

    print()
    print(f"  --- Dyadic xi-blocks (j: 2^{{-j-1}} <= xi < 2^{{-j}}) ---")
    print(f"  {'j':>5} {'lo':>14} {'hi':>14} {'count':>10} {'sum P':>20} {'frac':>10} {'cum frac':>10}")
    cum_dy = 0.0
    for j, lo, hi, bs, bc in r["dyadic"]:
        cum_dy += bs
        frac = bs / total
        cum_frac = cum_dy / total
        print(f"  {j:>5} {lo:>14.4e} {hi:>14.4e} {bc:>10} {bs:>20.3e} {frac:>10.4e} {cum_frac:>10.4f}")


if __name__ == "__main__":
    do_big = "--big" in sys.argv
    Ns = [int(3e6)] + ([int(1e7)] if do_big else [])
    h = 1
    results = []
    for N in Ns:
        r = run_one(N, h)
        results.append(r)
        print_results(r)
