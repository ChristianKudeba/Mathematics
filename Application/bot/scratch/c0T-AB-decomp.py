"""
Decompose T_<(N) and T_>(N) further via the Hooley identity
T(N) = 2 T_half(N), where
  T_half(N) := sum_{n <= N} #{e sf | n^2+1 : e <= sqrt(rad(n^2+1))}.

The identity:
  T_<(N) = T_half(N) + A(N) + B(N)
  T_>(N) = T_half(N) - A(N) - B(N)
where
  A(N) := sum over (n, e) with e sf, e | n^2+1, n < e <= N
        = sum_{e sf, e <= N} rho(e)        (since n in [1, e-1] roots, count=rho(e))
  B(N) := sum_{n: n^2+1 NON-sf} #{e sf | n^2+1: sqrt(rad(n^2+1)) < e <= n}

Then:
  c_<^infty - c_>^infty = 2 (A + B)^infty
  c_0^T = c_<^infty + c_>^infty = 2 c_half^infty
  Where c_<^infty = R H'(1) + gamma_K H(1) (closed form, prev session)
        A^infty = R H(1) (closed form via SD on G(s), simple pole)
        B^infty = empirical (the genuine Hooley-boundary residue)

For each n <= N, factor n^2+1 by trial division on the split-prime list,
enumerate sf divisors, classify each:
  - count toward T_< if e <= N
  - count toward T_> if e > N
  - count toward T_half if e <= sqrt(rad(n^2+1))
  - count toward A if n < e <= N
  - count toward B if rad(n^2+1) < n^2+1 (non-sf) AND sqrt(rad) < e <= n

Verification: A(N) + B(N) == T_<(N) - T_half(N).
"""

import math
import time
import sys

GAMMA = 0.5772156649015328606
LPRIME_1_CHI4 = 0.19290131767382030
GAMMA_K = (math.pi/4) * GAMMA + LPRIME_1_CHI4
R = math.pi/4
H1 = 0.5526721690
HP1 = 0.8355849429


def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]


def factor_n2plus1(n, split_primes_arr):
    """Return list of (prime, exponent) for n^2+1."""
    m = n*n + 1
    out = []
    if m % 2 == 0:
        e = 0
        while m % 2 == 0:
            m //= 2
            e += 1
        out.append((2, e))
    for p in split_primes_arr:
        if p*p > m:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            out.append((p, e))
    if m > 1:
        # m is the remaining prime factor (must be split since n^2+1 only has 2 or split-prime factors)
        out.append((m, 1))
    return out


def compute_full_decomp(N, split_primes_arr):
    """
    Compute T, T_<, T_>, T_half, A, B in one pass.
    Returns dict.
    """
    T_lt = 0
    T_gt = 0
    T_half = 0
    A = 0
    B = 0

    for n in range(1, N+1):
        m = n*n + 1
        factors = factor_n2plus1(n, split_primes_arr)
        # rad(m) = product of distinct primes
        rad = 1
        is_sf = True
        for p, e in factors:
            rad *= p
            if e > 1:
                is_sf = False
        # sqrt(rad) — use integer comparison: sqrt(rad) < e iff rad < e^2
        # For each squarefree divisor e, classify

        # Enumerate sf divisors
        sf_divs = [1]
        for p, e in factors:
            sf_divs = sf_divs + [d*p for d in sf_divs]

        # rad as int — already computed
        for e in sf_divs:
            # T_< / T_>
            if e <= N:
                T_lt += 1
            else:
                T_gt += 1
            # T_half: e <= sqrt(rad) iff e^2 <= rad
            if e*e <= rad:
                T_half += 1
            # A: n < e <= N
            if e <= N and e > n:
                A += 1
            # B: non-sf AND sqrt(rad) < e <= n  (i.e. e^2 > rad and e <= n)
            if not is_sf and e*e > rad and e <= n:
                B += 1

    T = T_lt + T_gt
    return {
        'N': N,
        'T': T, 'T_lt': T_lt, 'T_gt': T_gt,
        'T_half': T_half,
        'A': A, 'B': B,
        # Sanity: T == 2 T_half (Hooley identity)
        'T_minus_2Thalf': T - 2*T_half,
        # Sanity: T_lt - T_half == A + B
        'sanity_AB': (T_lt - T_half) - (A + B),
    }


def main():
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [10000, 30000, 100000]
    # Need split primes up to N (to handle the largest factor of n^2+1 where n <= N)
    Pbound = max(targets)
    print(f"Sieving primes up to {Pbound}...", flush=True)
    t0 = time.time()
    split_primes = [p for p in primes_up_to(Pbound) if p == 2 or p % 4 == 1]
    print(f"  {len(split_primes)} split primes (incl 2). {time.time()-t0:.1f}s", flush=True)

    a1 = R * H1   # = pi H(1)/4
    c_lt_pred = R * HP1 + GAMMA_K * H1   # 1.0134
    A_density_pred = R * H1               # 0.4341

    print()
    print("=== Predictions (closed forms / forecast) ===")
    print(f"  a_1 = R H(1)       = {a1:.6f}     (half of c_1)")
    print(f"  c_<^inf = R H'(1) + gamma_K H(1) = {c_lt_pred:.6f}")
    print(f"  A^inf / N = R H(1) = {A_density_pred:.6f}")
    print(f"  c_0^T (predicted from c_<^inf, prev empirical c_>^inf)")
    print(f"        = c_<^inf + c_>^inf ~= 1.013 + (-0.029) = 0.984")
    print(f"  Heuristic B^inf = (c_<^inf - c_>^inf)/2 - A^inf")
    print(f"                  = (1.013 - (-0.029))/2 - 0.434 = 0.087")
    print()

    print(f"{'N':>8} {'T':>12} {'T_<':>12} {'T_>':>12} {'T_half':>12} {'A':>10} {'B':>8} {'T-2Thalf':>10} {'AB-sanity':>10}", flush=True)
    print("-" * 110)
    for N in targets:
        # Limit primes to those up to N (no need for larger when factoring n^2+1 for n<=N)
        sp_for_N = [p for p in split_primes if p <= N]
        t0 = time.time()
        d = compute_full_decomp(N, sp_for_N)
        elapsed = time.time() - t0
        Lr = math.log(N)
        Nf = float(N)

        cl = (d['T_lt']  - a1 * N * Lr) / N
        cg = (d['T_gt']  - a1 * N * Lr) / N
        ch = (d['T_half'] - a1 * N * Lr) / N
        ct = (d['T']     - 2*a1 * N * Lr) / N
        Ad = d['A'] / Nf
        Bd = d['B'] / Nf

        print(f"{N:>8} {d['T']:>12} {d['T_lt']:>12} {d['T_gt']:>12} {d['T_half']:>12} {d['A']:>10} {d['B']:>8} {d['T_minus_2Thalf']:>10} {d['sanity_AB']:>10}  ({elapsed:.1f}s)", flush=True)
        print(f"   cs:    cl={cl:.4f}    cg={cg:.4f}    ch={ch:.4f}    ct={ct:.4f}    A/N={Ad:.4f}    B/N={Bd:.4f}", flush=True)
        # Sanity checks
        if d['T_minus_2Thalf'] != 0:
            # Hooley identity exact only when m = n^2+1 != 1; for n>=1 m>=2.
            print(f"   WARNING: Hooley identity T = 2 T_half violated by {d['T_minus_2Thalf']}", flush=True)
        if d['sanity_AB'] != 0:
            print(f"   WARNING: T_< - T_half = A + B violated by {d['sanity_AB']}", flush=True)
        print()


if __name__ == '__main__':
    main()
