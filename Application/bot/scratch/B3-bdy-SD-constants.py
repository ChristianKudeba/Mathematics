"""
Selberg-Delange leading constant for B_3^bdy(N).

Setup. With chi_4 the non-trivial char mod 4, K = Q(i), zeta_K = zeta * L(s, chi_4).

  G(s) := sum_{d sqfree} rho(d) d^{-s}
        = (1 + 2^{-s}) prod_{p == 1 (4)} (1 + 2 p^{-s}).

  G(s) = zeta_K(s) * H(s),
  H(s) = (1 - 4^{-s}) prod_{p == 1 (4)} (1 - 3 p^{-2s} + 2 p^{-3s})
       * prod_{p == 3 (4)} (1 - p^{-2s}).

H(s) is analytic on Re s > 1/2. Residue of zeta_K at s=1 is L(1, chi_4) = pi/4.
Hyperbola (Hooley-style) gives:

  T(N) := sum_{n <= N} 2^{omega(n^2+1)} = sum_{e <= N^2+1, e sf} N_e(N)
        ~ 2 N * (residue of G at s=1) * log N + O(N)
        = 2 * H(1) * pi/4 * N log N + O(N)
        = (H(1) pi / 2) N log N + O(N).

So predicted c_1 = H(1) * pi / 2.

This script:
  (a) Computes H(1) to high precision via sieved primes up to bound P.
  (b) Computes T(N) := sum_{n<=N} 2^{omega(n^2+1)} for N up to 10^5.
  (c) Reports T(N)/(N log N) and the residual T(N) - c_1 N log N for trend.
  (d) Compares to empirical B_3^bdy/(N log N) trend from prior session.
"""

import math, time

def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]


def compute_H1(P_bound=10**7):
    """
    H(1) = (3/4) * prod_{p==1(4), p<=P} (1 - 3/p^2 + 2/p^3)
                * prod_{p==3(4), p<=P} (1 - 1/p^2)
         * (asymptotic tail correction).
    Tail: each missing prime contributes a factor close to 1 - O(1/p^2),
          so tail product is exp(- 3 * sum_{p==1(4), p>P} 1/p^2 + ...).
    Leverage sum_p 1/p^2 = P_2 ~= 0.452247... and split half-half over residues
    by chebotarev, but more accurately compute partial sums and use
    sum_{p>P} 1/p^2 ~ 1/(P log P) (rough).
    Use partial-sum bound: relative error of finite product is
    ~ 3 * sum_{p>P, p==1(4)} 1/p^2 + sum_{p>P, p==3(4)} 1/p^2.
    """
    primes = primes_up_to(P_bound)
    log_H = math.log(3/4)
    s_split_tail_correction = 0.0
    s_inert_tail_correction = 0.0
    for p in primes:
        if p == 2:
            continue
        if p % 4 == 1:
            f = 1.0 - 3.0/(p*p) + 2.0/(p*p*p)
            log_H += math.log(f)
        else:  # p % 4 == 3
            f = 1.0 - 1.0/(p*p)
            log_H += math.log(f)
    H1 = math.exp(log_H)
    return H1, len(primes)


def factor_n2plus1(n, split_primes):
    """Return omega(n^2+1) for n^2+1, via trial division.
       split_primes is the list [2] + primes <= n with p % 4 == 1."""
    m = n * n + 1
    omega = 0
    if m % 2 == 0:
        omega += 1
        while m % 2 == 0:
            m //= 2
    for p in split_primes:
        if p * p > m:
            break
        if m % p == 0:
            omega += 1
            while m % p == 0:
                m //= p
    if m > 1:
        omega += 1
    return omega


def compute_T(N):
    """T(N) = sum_{n<=N} 2^{omega(n^2+1)}, computed by trial-division on n^2+1.
       Only primes p == 1 (mod 4) (and p=2) can divide n^2+1.
       For trial-division we need primes up to sqrt(N^2+1) ~ N.
    """
    primes_up = primes_up_to(N)
    split_primes = [p for p in primes_up if p % 4 == 1]
    T = 0
    for n in range(1, N+1):
        omega = factor_n2plus1(n, split_primes)
        T += 1 << omega
    return T


if __name__ == "__main__":
    print("=== Computing H(1) ===")
    t0 = time.time()
    H1, np = compute_H1(P_bound=10**6)
    dt = time.time() - t0
    c1 = H1 * math.pi / 2
    print(f"H(1) using primes <= 10^6 ({np} primes, {dt:.1f}s):")
    print(f"  H(1)            = {H1:.10f}")
    print(f"  c_1 = H(1)*pi/2 = {c1:.10f}")
    print(f"  3/pi            = {3/math.pi:.10f}  (Hooley constant for tau, NOT for tau*)")
    print()

    # Tail correction estimate
    # sum_{p > 10^6} 1/p^2 < integral_{10^6}^infty dx/(x^2 ln x) ~ 1/(10^6 * 14) ~ 7e-8
    # so log_H error < 3 * 7e-8 = 2e-7
    print("Tail correction estimate: relative error in H(1) is < 2e-7.")
    print()

    print("=== T(N) = sum_{n<=N} 2^{omega(n^2+1)} ===")
    print(f"{'N':>8} {'T(N)':>14} {'T/(N logN)':>12} {'pred c1':>10} {'resid/N':>10}")
    Ns = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    for N in Ns:
        t0 = time.time()
        T = compute_T(N)
        dt = time.time() - t0
        L = math.log(N)
        ratio = T/(N*L)
        resid = (T - c1 * N * L) / N
        print(f"{N:>8} {T:>14} {ratio:>12.6f} {c1:>10.6f} {resid:>10.4f}  ({dt:.1f}s)")
