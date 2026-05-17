"""
Faster: compute S(N) and the Nair-product factor Phi(N) at larger N
(N=10^3, 10^4) to see the ratio stabilize.
"""

from sympy import factorint, primerange
from sympy.ntheory.residue_ntheory import sqrt_mod
from math import log, isqrt
import time


def compute_S(N):
    """Compute S(N) via efficient sieve. tau(n^2+1) for n=1..N."""
    # Strategy: sieve through prime powers p^k.
    tau = [1] * (N + 1)
    rem = [n * n + 1 for n in range(N + 1)]
    rem[0] = 0

    # p = 2
    for n in range(1, N + 1, 2):  # odd n
        # n^2+1 = 2 mod 4, exactly one factor of 2
        rem[n] //= 2
        tau[n] *= 2

    # p = 1 mod 4 primes
    sqrt_max = int((N * N + 1) ** 0.5) + 1
    # We sieve all primes up to N (since prime divisor of n^2+1 <= n^2+1, can be up to N^2,
    # but those large primes appear at most once and we'll handle separately).
    # Actually, let's iterate all primes p <= N^2+1 with p % 4 == 1, but for tau we only need
    # to know exponents. To be efficient: sieve p <= N (any prime factor <= sqrt(M)).
    # The remaining factor (after dividing all primes <= sqrt(M)) is 1 or a prime p > sqrt(M).

    for p in primerange(3, sqrt_max + 1):
        if p % 4 != 1:
            continue
        try:
            r = sqrt_mod(-1, p)
        except Exception:
            continue
        if r is None:
            continue

        # For each prime power p^k, sieve
        pk = p
        while pk <= N * N + 1:
            try:
                r_pk = sqrt_mod(-1, pk)
            except Exception:
                break
            if r_pk is None:
                break
            roots = list({r_pk % pk, (-r_pk) % pk})
            for r_val in roots:
                start = r_val if r_val >= 1 else r_val + pk
                if start == 0:
                    start = pk
                for n in range(start, N + 1, pk):
                    if rem[n] % p == 0:
                        rem[n] //= p
                        # exponent of p in n^2+1 went up by 1
                        # We'll multiply tau by (e+1)/e at the end... too hard.
                        # Simpler: count exponents per n.
            pk *= p

    # Now rem[n] is either 1 or a prime > sqrt(M). Each such gives one more factor.
    # But we haven't been tracking exponents. Restart with a better approach.
    return None


def compute_S_via_factor(N, max_n=None):
    """Direct factoring approach. Slower but correct."""
    if max_n is None:
        max_n = N
    S = 0
    for n in range(1, max_n + 1):
        f = factorint(n * n + 1)
        t = 1
        for p, e in f.items():
            t *= (e + 1)
        S += t * t
    return S


def nair_factor_fast(N):
    """Fast computation of Nair factor Phi(N).

    Phi(N) = prod_{p<=N^2, rho(p)>0} (1 - rho(p)/p) * sum_{m<=N^2} tau^2(m) rho(m) / m

    The sum factorizes since we're summing over m supported on primes with rho(p)>0,
    but it's a partial sum (m<=N^2), not a full Euler product. We still must enumerate
    the m's directly.

    Faster method: iterate over m of the right form via recursion over primes.
    """
    M = N * N
    # Product part: only p=2 and p=1 mod 4 contribute (1-rho/p), rest=1
    prod = 0.5  # p=2 factor
    for p in primerange(3, M + 1):
        if p % 4 == 1:
            prod *= (1 - 2.0 / p)

    # Sum part: enumerate m <= M with m = 2^e * product of (p=1 mod 4) prime powers, e in {0,1}
    # For each such m, contribution is tau^2(m) * rho(m) / m.
    # rho(m) = 2^omega_+(m) where omega_+(m) = number of distinct primes p=1 mod 4 in m's factorization.
    # tau(m) = 2^[2 in m] * prod (k_i + 1) over p_i^{k_i} prime power parts.

    # Recursion: enumerate over primes p=1 mod 4 sequentially.
    primes_1mod4 = [p for p in primerange(2, M + 1) if p % 4 == 1]

    sum_total = [0.0]

    def recurse(idx, m, tau_m, rho_m):
        # Add contribution for current m
        sum_total[0] += (tau_m ** 2) * rho_m / m
        # Optionally multiply by 2 (include factor 2^1)
        # We'll handle the factor-of-2 case separately at the end.

        # Try adding p_idx, p_idx^2, p_idx^3, ... if m * p_idx^k <= M
        if idx >= len(primes_1mod4):
            return
        p = primes_1mod4[idx]
        if m * p > M:
            # No more primes can fit. Recurse to next.
            # But we still need to enumerate possibilities (skipping p).
            # Actually if m*p > M, no later prime works either since they're larger.
            # Wait, primes are sorted, so p <= subsequent primes. If m*p > M, all
            # subsequent primes also > M/m, so no contribution.
            return
        # Skip p
        recurse(idx + 1, m, tau_m, rho_m)
        # Include p^k for k >= 1
        new_m = m
        new_tau = tau_m
        new_rho = rho_m
        k = 0
        while True:
            new_m *= p
            k += 1
            if new_m > M:
                break
            new_tau_k = tau_m * (k + 1)
            new_rho_k = rho_m * 2  # rho contribution of one more p=1mod4 prime is *2 (only counted once per prime, not per power)
            # Wait: rho is multiplicative. rho(p^k) for p=1mod4, any k>=1, is 2.
            # So rho(m * p^k) / rho(m) = 2 (one new prime introduces factor 2 once,
            # regardless of k).
            sum_total[0] += (new_tau_k ** 2) * new_rho_k / new_m
            # Recurse to consider further primes
            recurse(idx + 1, new_m, new_tau_k, new_rho_k)

    recurse(0, 1, 1, 1)
    s_no2 = sum_total[0]

    # Now include factor 2^1: m = 2 * (m'), with rho(2) = 1, tau(2*m') = 2*tau(m').
    # Contribution: sum over m' <= M/2 of tau^2(2m') rho(2m') / (2m') = sum (4 tau^2(m')) (1*rho(m')) / (2m')
    # = 2 * sum tau^2(m') rho(m') / m', but only over m' with 2m' <= M.
    # We need m' <= M/2 with the same enumeration.
    sum_total[0] = 0.0

    def recurse2(idx, m, tau_m, rho_m, M_eff):
        sum_total[0] += (tau_m ** 2) * rho_m / m
        if idx >= len(primes_1mod4):
            return
        p = primes_1mod4[idx]
        if m * p > M_eff:
            return
        recurse2(idx + 1, m, tau_m, rho_m, M_eff)
        new_m = m
        k = 0
        while True:
            new_m *= p
            k += 1
            if new_m > M_eff:
                break
            new_tau_k = tau_m * (k + 1)
            new_rho_k = rho_m * 2
            sum_total[0] += (new_tau_k ** 2) * new_rho_k / new_m
            recurse2(idx + 1, new_m, new_tau_k, new_rho_k, M_eff)

    recurse2(0, 1, 1, 1, M // 2)
    s_with2 = 2.0 * sum_total[0]  # factor 2 from contribution: tau(2m')^2 rho(2m')/(2m')
                                   # = 4 tau^2(m') * 1 * rho(m') / (2m') = 2 tau^2(m') rho(m')/m'
    s_total = s_no2 + s_with2
    return prod, s_total, prod * s_total


if __name__ == "__main__":
    print("Computing S(N) and Nair factor Phi(N) for moderate N:")
    print(f"{'N':>6} {'S(N)':>14} {'N*Phi(N)':>14} {'S/(N*Phi)':>10} {'S/(N(log N)^3)':>15} {'(log N)^3':>10}")

    for N in [100, 200, 500, 1000, 2000, 5000, 10000]:
        t0 = time.time()
        S = compute_S_via_factor(N)
        t1 = time.time()
        prod, s_part, phi = nair_factor_fast(N)
        t2 = time.time()

        ratio_phi = S / (N * phi)
        ratio_log = S / (N * log(N) ** 3)
        log3 = log(N) ** 3
        print(f"{N:>6} {S:>14} {N*phi:>14.2f} {ratio_phi:>10.4f} {ratio_log:>15.5f} {log3:>10.2f}")
        print(f"        prod={prod:.5e}  sum part={s_part:.4f}   timing: S={t1-t0:.1f}s Phi={t2-t1:.1f}s")

        if t2 - t0 > 60:
            print("Time budget exhausted")
            break
