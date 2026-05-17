"""
Compute V(N) := sum_{M=1}^{N} T(M)^2  for the spin sum
    T(N) = sum_{n=1..N} tau(n^2+1) * chi_4(n+1).

Key questions:
  (a) Does V(N) / N^2 converge to a limit?  If so, T(M) has true sqrt(M)
      cancellation in mean square, and the limit is ~ C* the asymptotic
      constant.
  (b) Estimate variance of windowed sums sum_{M in (a, b]} T(M)^2 to test
      whether single-window estimators (used in P12-second-moment-empirical-
      extension.md) are dominated by noise.

Reuses the sieve from compute-T-fast.py.  Computes the full T[k] = T(2k)
array (T is 0 on odd M), then:
  - Cumulative V_full[k] = sum_{j=1..k} T(2j)^2 = sum_{M=1..2k} T(M)^2 since
    T(M)=T(M-1) at odd M.
  - Reports V(N)/N^2 at log-spaced N up to N_max.
  - Reports W(a, b) := sum_{M in (a, b]} T(M)^2 / (b - a)^2 over many
    non-overlapping equal-width windows, with mean and stdev.
"""

import math, time, sys, os, pickle

def chi4(n):
    n = n & 3
    if n == 1: return 1
    if n == 3: return -1
    return 0

def primes_up_to(B):
    sieve = bytearray([1]) * (B+1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(B**0.5)+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00' * len(sieve[i*i::i])
    return [i for i in range(B+1) if sieve[i]]

def sqrt_minus1_mod_p(p):
    for z in range(2, p):
        if pow(z, (p-1)//2, p) == p-1:
            return pow(z, (p-1)//4, p)
    return None

def compute_T_full(N_max):
    """Compute Tcum[k] = T(2k) for k=0..K, K = N_max // 2 (must be even)."""
    K = N_max // 2
    print(f"[T] sieving R[k] = 4k^2+1, K={K}", flush=True)
    t0 = time.time()
    tau = [1] * (K+1); tau[0] = 0
    R = [4*k*k + 1 for k in range(K+1)]; R[0] = 1
    primes = primes_up_to(N_max)
    print(f"[T]   {len(primes)} primes up to {N_max} ({time.time()-t0:.1f}s)", flush=True)
    for p in primes:
        if p % 4 != 1:
            continue
        m0 = sqrt_minus1_mod_p(p)
        if m0 is None: continue
        inv2 = pow(2, p-2, p)
        k0 = (m0 * inv2) % p
        roots = {k0, (p - k0) % p}
        for r in roots:
            k = r if r >= 1 else r + p
            while k <= K:
                if R[k] % p == 0:
                    e = 0
                    while R[k] % p == 0:
                        R[k] //= p; e += 1
                    tau[k] *= (e+1)
                k += p
    for k in range(1, K+1):
        if R[k] > 1:
            tau[k] *= 2
    print(f"[T]   sieve done ({time.time()-t0:.1f}s); building Tcum", flush=True)
    Tcum = [0] * (K+1)
    s = 0
    for k in range(1, K+1):
        s += (-1 if (k & 1) else 1) * tau[k]
        Tcum[k] = s
    print(f"[T] total {time.time()-t0:.1f}s", flush=True)
    return Tcum

def compute_V(Tcum):
    """V[k] = sum_{j=1..k} Tcum[j]^2 = sum_{M=1..2k} T(M)^2 (T odd-M = T even-M-1)."""
    K = len(Tcum) - 1
    V = [0] * (K+1)
    s = 0
    # T(2j-1) = T(2j-2) = Tcum[j-1], T(2j) = Tcum[j].
    # sum T(M)^2 for M=1..2k = sum_{j=1..k} (T(2j-1)^2 + T(2j)^2)
    #                        = sum_{j=1..k} (Tcum[j-1]^2 + Tcum[j]^2).
    for k in range(1, K+1):
        s += Tcum[k-1]*Tcum[k-1] + Tcum[k]*Tcum[k]
        V[k] = s
    return V

def V_at(V, N):
    """V at integer N (odd or even). V[k] is sum up to M=2k."""
    # If N=2k, V[k]. If N=2k+1, V[k] + T(2k+1)^2 = V[k] + Tcum[k]^2.
    k = N // 2
    if N & 1:
        # add T(2k+1)^2
        return V[k] + (V[k+1] - V[k] - 0)  # actually we don't store T sep
    return V[k]

def main():
    N_max = int(os.environ.get('NMAX', '10000000'))  # 10^7 default; bigger if mem allows
    print(f"=== V-cumulative at N_max = {N_max} ===")
    Tcum = compute_T_full(N_max)
    K = len(Tcum) - 1

    print(f"\n[V] computing V[k] cumulative sum of T(M)^2 (M=1..2k)", flush=True)
    t0 = time.time()
    V = compute_V(Tcum)
    print(f"[V] done in {time.time()-t0:.1f}s", flush=True)

    # Sanity: V[K] should be O(N_max^2).  Print V/N^2 at samples.
    print()
    print(f"{'N':>10}  {'T(N)':>10}  {'T/sqrt(N)':>10}  {'V(N)':>15}  {'V(N)/N^2':>10}  {'2V(N)/N^2':>10}")
    samples = []
    for exp in range(3, 9):
        for c in [1, 2, 3, 5, 7]:
            N = c * 10**exp
            if N <= N_max:
                samples.append(N)
    samples.append(N_max)
    samples = sorted(set(samples))
    for N in samples:
        k = N // 2
        if k < 1 or k > K: continue
        T = Tcum[k]
        Vn = V[k]
        sN = math.sqrt(N)
        print(f"{N:>10d}  {T:>10d}  {T/sN:>+10.4f}  {Vn:>15d}  {Vn/(N*N):>10.6f}  {2*Vn/(N*N):>10.6f}")

    # Variance of windowed sums.  Pick window widths W and look at non-overlapping
    # windows over the full range.
    print(f"\n[W] non-overlapping window stats: W_w(j) = sum_{{M in ((j-1)w, jw]}} T(M)^2 / w^2")
    print(f"{'w':>10}  {'#wins':>6}  {'mean':>10}  {'stdev':>10}  {'CV':>8}")
    for w in [1000, 5000, 10000, 50000, 100000, 500000, 1000000, 2000000, 5000000]:
        if w > N_max: continue
        nwin = N_max // w
        if nwin < 4: continue
        vals = []
        for j in range(1, nwin+1):
            a = (j-1)*w
            b = j*w
            ka = a // 2
            kb = b // 2
            wsum = V[kb] - V[ka]
            vals.append(wsum / (w*w))
        n = len(vals)
        mean = sum(vals)/n
        var = sum((x-mean)**2 for x in vals)/n
        stdev = math.sqrt(var)
        cv = stdev/mean if mean else float('nan')
        print(f"{w:>10d}  {n:>6d}  {mean:>10.6f}  {stdev:>10.6f}  {cv:>8.4f}")

    # Also: same for D-style (N, 2N] windows at log-spaced N (matches prior session table).
    print(f"\n[U] U(N) := sum_{{M in (N,2N]}} T(M)^2 / N^2 at log-spaced N")
    print(f"{'N':>10}  {'U(N)':>10}")
    for N in samples:
        if 2*N > N_max: continue
        ka = N // 2
        kb = (2*N) // 2
        u = (V[kb] - V[ka]) / (N*N)
        print(f"{N:>10d}  {u:>10.6f}")

if __name__ == '__main__':
    main()
