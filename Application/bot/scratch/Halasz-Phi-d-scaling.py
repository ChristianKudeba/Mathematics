"""Multi-N scaling of cumulative autocorrelation profile C_h(D)/T_h.

Computes the cumulative off-diagonal profile C_h(D) := sum_{d=1..D} Psi_h(d)
for N in {1e5, 1e6, 3e6}, h in {1, 5}, with Psi_h(d) := sum_e S_h(e) S_h(e+d).
Reports threshold D*(N, h) at which |C_h(D*)/T_h| first reaches 0.5, and
the scaled threshold D*/N.

Tests pickup hint #1 from prev session:
  - If D*/N approx const => off-diagonal "uniformly spread"
  - If D*/N -> 0 (D* sublinear in N) => bulk at fixed absolute d-scale
  - If D*/N -> 1 => bulk at the upper tail of d
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


def find_threshold(prefix, R0, target, frac):
    """Find smallest D >= 1 such that |prefix[D] - R0| / target >= frac.
    prefix is cumsum of R, R0 = R[0]; target = offdiag / 2.
    Returns -1 if never reached.
    """
    if target == 0:
        return -1
    n = len(prefix)
    cs = prefix[1:] - R0
    rel = cs / target
    cond = np.abs(rel) >= frac
    idx = np.argmax(cond)
    if cond[idx]:
        return int(idx + 1)
    return -1


def run_one(N, h_list):
    print(f"\n############# N = {N} #############", file=sys.stderr)
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

    out = []
    for k, h in enumerate(h_list):
        x = S[k]
        t3 = time.time()
        R = autocorrelation_fft(x)
        print(f"# N={N}, h={h}: autocorr FFT in {time.time()-t3:.1f}s", file=sys.stderr)

        Hh = float(np.sum(x))
        Dh = float(R[0])
        offdiag = Hh * Hh - Dh
        target = offdiag / 2.0

        # Cross-check identity (*)
        sum_Psi_to_Nm2 = float(np.sum(R[1:N - 1]))
        rel_err = abs(2 * sum_Psi_to_Nm2 - offdiag) / max(abs(offdiag), 1)

        prefix = np.cumsum(R)
        cum_targets = [10, 100, 1000, 10000, 100000,
                       max(10, N // 100),
                       max(10, N // 10),
                       max(10, N // 3),
                       N - 2]
        cum_targets = sorted(set(cum_targets))

        # Find thresholds at frac = 0.25, 0.5, 0.75 of |target|
        D_25 = find_threshold(prefix, R[0], target, 0.25)
        D_50 = find_threshold(prefix, R[0], target, 0.50)
        D_75 = find_threshold(prefix, R[0], target, 0.75)

        out.append({
            "N": N, "h": h, "Hh": Hh, "Dh": Dh, "offdiag": offdiag, "target": target,
            "rel_err": rel_err,
            "D_25": D_25, "D_50": D_50, "D_75": D_75,
            "cum": [(D, float(prefix[D] - R[0]),
                    float((prefix[D] - R[0]) / target if target else 0.0))
                   for D in cum_targets if D < N],
        })
    return out


if __name__ == "__main__":
    h_list = [1, 5]
    Ns = [int(1e5), int(1e6), int(3e6)]

    all_results = []
    for N in Ns:
        results = run_one(N, h_list)
        all_results.extend(results)

    print("\n\n========== SUMMARY ==========")
    print(f"{'N':>10} {'h':>3} {'H_h':>14} {'D_h':>14} {'T_h=(H^2-D)/2':>16} {'relErr':>10} {'D*_25':>10} {'D*_50':>10} {'D*_75':>10} {'D*_50/N':>10}")
    for r in all_results:
        d50 = r["D_50"]
        d50_over_N = d50 / r["N"] if d50 > 0 else float("nan")
        print(f"{r['N']:>10} {r['h']:>3} {r['Hh']:>14.1f} {r['Dh']:>14.1f} {r['target']:>16.1f} {r['rel_err']:>10.2e} {r['D_25']:>10} {r['D_50']:>10} {r['D_75']:>10} {d50_over_N:>10.5f}")

    print("\n\n========== CUMULATIVE PROFILES ==========")
    for r in all_results:
        print(f"\n# N={r['N']}, h={r['h']}, T_h = {r['target']:.1f}")
        print(f"{'D':>12} {'C_h(D)':>16} {'C_h(D)/T_h':>14}")
        for D, cs, ratio in r["cum"]:
            print(f"{D:>12} {cs:>16.1f} {ratio:>14.5f}")
