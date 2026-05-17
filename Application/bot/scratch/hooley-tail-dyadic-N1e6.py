"""
Dyadic decomposition of B_>(N) at N=10^6 (and 3*10^6 if time permits) -
extension of hooley-tail-dyadic-capped.py to one more decade.

Goal: test whether the d > N^1.85 concentration percentage stabilizes
near ~90% (robust empirical localization, supports analytic next-step)
or drifts down (fixed-cutoff artifact, would invalidate prev session's
main result).

Memory note: factor_n2plus1 allocates per-n list of (p, e). At N=10^6 the
total number of (p, e) pairs is ~ N log log N ~ 1e7, fine.
"""
import math
import sys
import time
from array import array

def primerange(b):
    if b < 3: return [2] if b >= 2 else []
    s = bytearray([1]) * b
    s[0] = s[1] = 0
    for i in range(2, int(b**0.5) + 1):
        if s[i]:
            for j in range(i*i, b, i): s[j] = 0
    return [i for i in range(2, b) if s[i]]

def factor_n2plus1(N):
    # vals[n] = remaining unfactored part of n^2+1
    # use small-prime sieve up to N+6 (since n^2+1 has at most one prime factor > sqrt(n^2+1) ~ N)
    vals = [n*n + 1 for n in range(N + 1)]
    factors = [[] for _ in range(N + 1)]
    primes = primerange(N + 6)
    for p in primes:
        if p == 2:
            roots = [1]
        elif p % 4 == 3:
            continue
        else:
            # Tonelli-Shanks for sqrt(-1) mod p
            r = pow(2, (p - 1) // 4, p)  # quick if p%8==5
            if (r * r + 1) % p != 0:
                # fallback: linear search (only for small primes)
                r = next(x for x in range(1, p) if (x*x + 1) % p == 0)
            roots = [r, p - r]
        for r in roots:
            n = r
            if n == 0 or n > N: continue
            while n <= N:
                v = vals[n]; e = 0
                while v % p == 0:
                    v //= p; e += 1
                vals[n] = v
                if e: factors[n].append((p, e))
                n += p
    for n in range(1, N + 1):
        if vals[n] > 1:
            factors[n].append((vals[n], 1))
    return factors

def dyadic_split(factors, N, K):
    S_lt = 0
    W = [0] * (K + 1)
    log2 = math.log(2)
    Nf = float(N)
    for n in range(1, N + 1):
        f = factors[n]
        # build divisor list as (d, tau(d^2)) pairs
        ds = [(1, 1)]
        for (p, e) in f:
            new_ds = []
            pk = 1
            for k in range(e + 1):
                t = 2*k + 1  # tau(p^(2k)) = 2k+1
                for (d, td2) in ds:
                    new_ds.append((d * pk, td2 * t))
                pk *= p
            ds = new_ds
        for (d, td2) in ds:
            if d <= N:
                S_lt += td2
            else:
                k = int(math.log(d / Nf) / log2)
                if N * (1 << k) >= d: k -= 1
                if k > K: W[K] += td2
                else: W[k] += td2
    return S_lt, W

# Same Selberg-Delange Laurent for Σ_*(X) := Σ_{d <= X} τ(d²) ρ(d) / d
# (constants from previous session's tau-sq-c0-coefficient.py)
A3, A2, A1, A0 = 0.05971106, 0.43491036, 1.07159000, 0.87930421
def Sig(X):
    if X <= 1: return 0.0
    L = math.log(X)
    return A3*L**3/6 + A2*L**2/2 + A1*L + A0

def run_one_N(N):
    print(f"\n{'='*100}")
    print(f"N = {N}")
    print(f"{'='*100}")
    L = math.log(N)
    Ncap = N * N + 1
    K = int(math.ceil(math.log2(Ncap / N)))
    print(f"  L = {L:.4f},  K = {K},  N^2+1 = {Ncap}")
    sys.stdout.flush()

    t0 = time.time()
    factors = factor_n2plus1(N)
    t1 = time.time()
    print(f"  factor_n2plus1 done in {t1-t0:.1f}s")
    sys.stdout.flush()

    S_lt, W = dyadic_split(factors, N, K)
    t2 = time.time()
    print(f"  dyadic_split done in {t2-t1:.1f}s")
    sys.stdout.flush()

    edges = [N * (1 << k) for k in range(K + 2)]
    P_capped = []
    for k in range(K + 1):
        lo = edges[k]
        hi = min(edges[k+1], Ncap)
        if hi <= lo: P_capped.append(0.0)
        else:        P_capped.append(N * (Sig(hi) - Sig(lo)))
    B_per = [W[k] - P_capped[k] for k in range(K + 1)]
    B_total = sum(B_per)

    # also: S(N) - N*Sigma_*(N) for cross-check vs prev session
    S_total = S_lt + sum(W)
    NSig_at_Ncap = N * Sig(Ncap)
    print(f"  B_>(N)/N = {B_total/N:.4f}  (linear-fit target 0.833 L - 2.876 = {0.833*L - 2.876:.4f})")
    print(f"  S(N) (= sum tau(d^2) over n<=N, d|n^2+1) = {S_total}")
    print(f"  N*Sigma_*(N^2+1) (formal) = {NSig_at_Ncap:.2f}")
    print(f"  S(N) - N*Sigma_*(N^2+1) = {S_total - NSig_at_Ncap:.2f}  (should equal B_total)")
    sys.stdout.flush()

    print(f"\n  {'k':>3} | {'window':>32} | {'W_k':>14} | {'P_k':>14} | {'B_k':>14} | {'B_k/N':>8} | {'cum/N':>8}")
    print("  " + "-"*108)
    cum = 0.0
    rows = []
    for k in range(K + 1):
        lo = edges[k]
        hi = min(edges[k+1], Ncap)
        if hi <= lo: continue
        cum += B_per[k]
        wstr = f"({lo}, {hi}]"
        print(f"  {k:>3} | {wstr:>32} | {W[k]:>14} | {P_capped[k]:>14.2f} | {B_per[k]:>14.2f} | {B_per[k]/N:>8.4f} | {cum/N:>8.4f}")
        rows.append((k, lo, hi, W[k], P_capped[k], B_per[k]))
    sys.stdout.flush()

    cum_to = {}
    for c in [1.3, 1.5, 1.7, 1.85, 1.95]:
        thresh = int(round(N ** c))
        cumc = 0.0
        for (k, lo, hi, w, p, b) in rows:
            if hi <= thresh:
                cumc += b
            elif lo < thresh < hi:
                frac = (math.log(thresh) - math.log(lo)) / (math.log(hi) - math.log(lo))
                cumc += b * frac
        cum_to[c] = cumc
        frac_above = (B_total - cumc) / B_total if B_total else float('nan')
        print(f"    d <= N^{c:.2f} = {thresh:>14}  ->  cum residual / N = {cumc/N:>8.4f}  "
              f"(fraction above = {frac_above*100:>5.1f}% of total)")
    sys.stdout.flush()
    return (N, L, B_total/N, cum_to, B_total, t2-t0)

def main():
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [10**6]
    results = []
    for N in targets:
        try:
            results.append(run_one_N(N))
        except MemoryError:
            print(f"!! MemoryError at N={N}, stopping")
            break

    # combine with prior 4 data points
    prior = [
        (10**4,    9.21,  4.85, {1.30: 0.0, 1.50: 4.85*0.08, 1.70: 4.85*0.09, 1.85: 4.85*0.30, 1.95: 4.85*0.60}, 4.85*10**4),
        (3*10**4, 10.31,  5.85, {1.30: 5.85*0.04, 1.50: 5.85*0.06, 1.70: 5.85*0.07, 1.85: 5.85*0.14, 1.95: 5.85*0.61}, 5.85*3*10**4),
        (10**5,   11.51,  6.26, {1.30: 6.26*-0.01, 1.50: 6.26*-0.02, 1.70: 6.26*-0.02, 1.85: 6.26*0.04, 1.95: 6.26*0.45}, 6.26*10**5),
        (3*10**5, 12.61,  7.88, {1.30: 7.88*0.01, 1.50: 7.88*0.01, 1.70: 7.88*0.03, 1.85: 7.88*0.09, 1.95: 7.88*0.49}, 7.88*3*10**5),
    ]
    print("\n=== COMBINED SUMMARY: fraction of B_>(N) above d = N^c ===\n")
    header = f"{'N':>10} | {'L':>6} | {'B_>/N':>8} | " + " | ".join(f"d>N^{c:.2f}".rjust(10) for c in [1.3, 1.5, 1.7, 1.85, 1.95])
    print(header)
    print("-" * 95)
    for (N, L, B_per_N, cum_to, B_tot, *_) in prior + results:
        cells = []
        for c in [1.3, 1.5, 1.7, 1.85, 1.95]:
            frac_above = (B_tot - cum_to[c]) / B_tot if B_tot else float('nan')
            cells.append(f"{frac_above*100:>9.1f}%")
        print(f"{N:>10} | {L:>6.3f} | {B_per_N:>8.4f} | " + " | ".join(cells))

if __name__ == "__main__":
    main()
