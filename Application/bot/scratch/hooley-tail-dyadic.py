"""
Dyadic decomposition of B_>(N).

Background (from session 2026-05-05T10-09):
  S(N) = N*Sigma_*(N^2+1) + B(N), B = B_< + B_>,
  B_>(N) = sum_{N < d <= N^2+1} tau(d^2) * delta_d(N),
  delta_d(N) = N_d(N) - rho(d) N/d.

This script splits B_>(N) into dyadic windows
  W_k = (N * 2^k, N * 2^(k+1)]   for k = 0, 1, ..., floor(log2(N+1))
and reports per-window:
  S_>^(k)(N)   := sum_{n<=N} sum_{d | n^2+1, d in W_k} tau(d^2)
  P_>^(k)(N)   := N * (Sigma_Laurent(N*2^(k+1)) - Sigma_Laurent(N*2^k))   (formal)
  B_>^(k)(N)   := S_>^(k)(N) - P_>^(k)(N)
  per-N normalized: B_>^(k)/N and as a fraction of empirical 0.85*L-2.876.

We use the closed-form 4-term Laurent (validated session 06:51 to within 0.063
on [10^3, 10^7]; Tauberian budget per session 10:09 is <= 0.5/N for X up to N^2).
The dyadic split brings the subtraction stage to per-window scale, so window-level
formal-SD residuals at most inherit the same overall budget.
"""
import math
from array import array

# ---------- Factorization ----------

def primerange(b):
    if b < 3:
        return [2] if b >= 2 else []
    sieve = bytearray([1]) * b
    sieve[0] = sieve[1] = 0
    for i in range(2, int(b**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, b, i):
                sieve[j] = 0
    return [i for i in range(2, b) if sieve[i]]

def factor_n2plus1(N):
    """factors[n] = list of (p,e) for n^2+1 = prod p^e, 1<=n<=N."""
    vals = [n*n + 1 for n in range(N + 1)]
    factors = [[] for _ in range(N + 1)]
    p_bound = N + 5
    primes = primerange(p_bound + 1)
    for p in primes:
        if p == 2:
            roots = [1]
        elif p % 4 == 3:
            continue
        else:
            r = None
            for x in range(1, p):
                if (x*x + 1) % p == 0:
                    r = x; break
            roots = [r, p - r]
        for r in roots:
            n = r
            if n == 0 or n > N:
                continue
            while n <= N:
                v = vals[n]
                e = 0
                while v % p == 0:
                    v //= p; e += 1
                vals[n] = v
                if e:
                    factors[n].append((p, e))
                n += p
    for n in range(1, N + 1):
        if vals[n] > 1:
            factors[n].append((vals[n], 1))
    return factors

# ---------- Dyadic accumulator ----------

def dyadic_split_large(factors, N, K):
    """Returns S_lt (sum d<=N) and W[0..K-1] dyadic counts of tau(d^2) over
    d in (N*2^k, N*2^(k+1)] for k = 0,...,K-1.  Last window includes the
    remainder past N*2^K (always < N^2+1 < 2*N^2 < N*2^(ceil(log2 N)+1))."""
    S_lt = 0
    W = [0] * (K + 1)   # W[K] = overflow bucket for completeness
    log2 = math.log(2)
    for n in range(1, N + 1):
        f = factors[n]
        ds = [(1, 1)]
        for (p, e) in f:
            new_ds = []
            pk = 1
            for k in range(e + 1):
                t = 2*k + 1
                for (d, td2) in ds:
                    new_ds.append((d * pk, td2 * t))
                pk *= p
            ds = new_ds
        for (d, td2) in ds:
            if d <= N:
                S_lt += td2
            else:
                # k = floor(log2(d/N))
                ratio = d / N
                k = int(math.log(ratio) / log2)  # floor for d/N >= 1
                # safety: ensure d in (N*2^k, N*2^(k+1)]
                lo = N * (1 << k)
                if d <= lo:
                    k -= 1
                if k >= K:
                    W[K] += td2
                else:
                    W[k] += td2
    return S_lt, W

# ---------- Formal Laurent ----------

# Closed-form Laurent for Sigma_*(X) ~ A_3 L^3/6 + A_2 L^2/2 + A_1 L + A_0
# (L = log X), validated session 2026-05-05T06-51 to within 0.063 on [10^3,10^7].
A3 = 0.05971106
A2 = 0.43491036
A1 = 1.07159000
A0 = 0.87930421

def Sigma_Laurent(X):
    L = math.log(X)
    return A3 * L**3 / 6 + A2 * L**2 / 2 + A1 * L + A0

# ---------- Main ----------

def main():
    # Pick N values that fit in budget (factorization is the bottleneck).
    # 3e5 is the scale used in 10:09 session.
    Ns = [10**4, 3*10**4, 10**5, 3*10**5]

    print("Dyadic decomposition of B_>(N), windows W_k = (N*2^k, N*2^(k+1)].")
    print()
    for N in Ns:
        L = math.log(N)
        K = int(math.ceil(math.log2(max(2, N))))  # last edge >= N^2 since N*2^K >= N^2 when K >= log2 N
        print(f"=== N = {N} (L = {L:.4f}, K = {K}, last edge N*2^K = {N*(1<<K)}) ===")
        print(f"  factoring n^2+1 for n<={N} ...", flush=True)
        factors = factor_n2plus1(N)
        print(f"  enumerating divisors and binning ...", flush=True)
        S_lt, W = dyadic_split_large(factors, N, K)
        S_total = S_lt + sum(W)

        # per-window formal-SD prediction
        # k-th window edges:
        edges = [N * (1 << k) for k in range(K + 2)]
        # cap last edge at N^2+1
        edges[-1] = min(edges[-1], N*N + 1)
        # Laurent values at each edge
        Sig_edge = [Sigma_Laurent(e) for e in edges]
        # formal P_>^(k) := N * (Sig(edge[k+1]) - Sig(edge[k]))
        P_per_window = [N * (Sig_edge[k+1] - Sig_edge[k]) for k in range(K + 1)]

        # Empirical S_>^(k) = W[k]
        # Residual B_>^(k) = W[k] - P_>^(k)
        # Total empirical B_> = sum (W - P)
        B_per = [W[k] - P_per_window[k] for k in range(K + 1)]
        B_total = sum(B_per)

        # Empirical fit: 0.85*L - 2.876 (per-N, from 10:09)
        fit_target = (0.833*L - 2.876)

        # Print table
        print(f"  S(N) = {S_total},  S_<(N) = {S_lt} (d<=N),  S_>(N) = {sum(W)} (d>N)")
        print(f"  B_>(N) = {B_total:.2f},  B_>(N)/N = {B_total/N:.4f}  (empirical 10:09 fit: {fit_target:.4f})")
        print()
        print(f"  {'k':>3} | {'window (d range)':>30} | {'W_k':>14} | {'P_k(formal)':>14} | "
              f"{'B_k = W-P':>14} | {'B_k/N':>9} | {'frac(|B_total|)':>14}")
        print("  " + "-" * 115)
        for k in range(K + 1):
            lo = edges[k] + 1
            hi = edges[k+1]
            if hi <= lo:
                continue
            window_str = f"({edges[k]}, {hi}]"
            frac = B_per[k] / B_total if B_total != 0 else float('nan')
            print(f"  {k:>3} | {window_str:>30} | {W[k]:>14} | {P_per_window[k]:>14.2f} | "
                  f"{B_per[k]:>14.2f} | {B_per[k]/N:>9.5f} | {frac:>14.4f}")
        print()
        # cumulative: contribution of d in (N, N*2^K_partial] vs further
        cum_B = 0.0
        print(f"  cumulative B_>^(<=k) / N (running):")
        for k in range(K + 1):
            cum_B += B_per[k]
            if k % max(1, K // 8) == 0 or k == K:
                print(f"    k <= {k:>2}  (d <= {edges[k+1]:>14}):  cum B_>/N = {cum_B/N:>8.4f}")
        print()

if __name__ == "__main__":
    main()
