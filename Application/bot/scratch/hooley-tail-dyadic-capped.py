"""
Capped version: like hooley-tail-dyadic.py, but the formal-SD prediction
P_k is computed over (edges[k], min(edges[k+1], N^2+1)] so that empirical
and formal share the same upper cutoff.  This removes the spurious "cutoff
overshoot" in the very last partial window.
"""
import math
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
    vals = [n*n + 1 for n in range(N + 1)]
    factors = [[] for _ in range(N + 1)]
    primes = primerange(N + 6)
    for p in primes:
        if p == 2: roots = [1]
        elif p % 4 == 3: continue
        else:
            r = next(x for x in range(1, p) if (x*x + 1) % p == 0)
            roots = [r, p - r]
        for r in roots:
            n = r
            if n == 0 or n > N: continue
            while n <= N:
                v = vals[n]; e = 0
                while v % p == 0: v //= p; e += 1
                vals[n] = v
                if e: factors[n].append((p, e))
                n += p
    for n in range(1, N + 1):
        if vals[n] > 1: factors[n].append((vals[n], 1))
    return factors

def dyadic_split(factors, N, K):
    S_lt = 0
    W = [0] * (K + 1)
    log2 = math.log(2)
    for n in range(1, N + 1):
        f = factors[n]
        ds = [(1, 1)]
        for (p, e) in f:
            new_ds = []
            pk = 1
            for k in range(e + 1):
                t = 2*k + 1
                for (d, td2) in ds: new_ds.append((d * pk, td2 * t))
                pk *= p
            ds = new_ds
        for (d, td2) in ds:
            if d <= N: S_lt += td2
            else:
                k = int(math.log(d / N) / log2)
                if N * (1 << k) >= d: k -= 1
                if k > K: W[K] += td2
                else: W[k] += td2
    return S_lt, W

A3, A2, A1, A0 = 0.05971106, 0.43491036, 1.07159000, 0.87930421
def Sig(X):
    L = math.log(X)
    return A3*L**3/6 + A2*L**2/2 + A1*L + A0

def main():
    Ns = [10**4, 3*10**4, 10**5, 3*10**5]
    print(f"{'='*100}")
    print("Capped dyadic decomposition of B_>(N): formal-SD prediction restricted to d <= N^2+1")
    print(f"{'='*100}\n")

    summary = []
    for N in Ns:
        L = math.log(N)
        Ncap = N * N + 1
        K = int(math.ceil(math.log2(Ncap / N)))
        factors = factor_n2plus1(N)
        S_lt, W = dyadic_split(factors, N, K)
        edges = [N * (1 << k) for k in range(K + 2)]

        # capped formal P_k: integrate Sig from max(edges[k], N) to min(edges[k+1], Ncap)
        P_capped = []
        for k in range(K + 1):
            lo = edges[k]
            hi = min(edges[k+1], Ncap)
            if hi <= lo:
                P_capped.append(0.0)
            else:
                P_capped.append(N * (Sig(hi) - Sig(lo)))
        B_per = [W[k] - P_capped[k] for k in range(K + 1)]
        B_total = sum(B_per)

        print(f"N = {N},  L = {L:.4f},  K = {K},  N^2+1 = {Ncap},  B_>(N)/N = {B_total/N:.4f}  (target 0.833 L - 2.876 = {0.833*L - 2.876:.4f})")
        print(f"\n  {'k':>3} | {'window':>30} | {'W_k':>12} | {'P_k(capped)':>14} | {'B_k':>14} | {'B_k/N':>9} | {'cum B/N':>9}")
        print("  " + "-"*105)
        cum = 0.0
        rows = []
        for k in range(K + 1):
            lo = edges[k]
            hi = min(edges[k+1], Ncap)
            if hi <= lo:
                continue
            cum += B_per[k]
            window_str = f"({lo}, {hi}]"
            print(f"  {k:>3} | {window_str:>30} | {W[k]:>12} | {P_capped[k]:>14.2f} | {B_per[k]:>14.2f} | {B_per[k]/N:>9.5f} | {cum/N:>9.5f}")
            rows.append((k, lo, hi, W[k], P_capped[k], B_per[k]))
        print()

        # Concentration: where does B_> live?
        # threshold = d <= N^c for c = 1.5, 1.7, 1.85
        cum_to = {}
        for c in [1.3, 1.5, 1.7, 1.85, 1.95]:
            thresh = int(round(N ** c))
            cum_thresh = 0.0
            for (k, lo, hi, w, p, b) in rows:
                if hi <= thresh:
                    cum_thresh += b
                elif lo < thresh < hi:
                    # partial: split linearly in log-d (rough)
                    # actually just proportionally by W_k contribution to (lo, thresh] vs (lo, hi]
                    frac = (math.log(thresh) - math.log(lo)) / (math.log(hi) - math.log(lo))
                    cum_thresh += b * frac
                # else lo >= thresh: skip (out of region)
            cum_to[c] = cum_thresh
            print(f"    cum residual B_>(N; d <= N^{c:.2f} = {thresh:>14}) / N = {cum_thresh/N:>8.4f}  ({cum_thresh/B_total*100:>5.1f}% of total)")
        print()
        summary.append((N, L, B_total/N, cum_to, B_total))

    print("\n=== SUMMARY: fraction of B_>(N) above d = N^c ===\n")
    header = f"{'N':>8} | {'L':>6} | {'B_>/N':>8} | " + " | ".join(f"d>N^{c:.2f}".rjust(10) for c in [1.3, 1.5, 1.7, 1.85, 1.95])
    print(header)
    print("-" * 90)
    for (N, L, B_per_N, cum_to, B_tot) in summary:
        cells = []
        for c in [1.3, 1.5, 1.7, 1.85, 1.95]:
            frac_above = (B_tot - cum_to[c]) / B_tot if B_tot != 0 else float('nan')
            cells.append(f"{frac_above*100:>9.1f}%")
        print(f"{N:>8} | {L:>6.3f} | {B_per_N:>8.4f} | " + " | ".join(cells))

if __name__ == "__main__":
    main()
