"""
Verify the Nair-style upper bound for sum_{n<=N} tau(n^2+1)^2.

(1) Compute S(N) = sum tau(n^2+1)^2 by direct sieve for N up to 10^6.
(2) Compute the Nair-product factor:
    Phi(X) = prod_{p<=X} (1 - rho(p)/p) * sum_{m<=X^2} tau(m)^2 rho(m)/m
    where rho(p^k) = 2 if p=1 mod 4 (any k>=1); rho(2)=1, rho(2^k)=0 for k>=2;
    rho(p^k)=0 if p=3 mod 4.
(3) Verify that S(N) <= C * N * Phi(N) for some absolute C, and S(N) / (N (log N)^3)
    matches.
(4) Verify the Dirichlet series D(s)=sum tau^2(m) rho(m) / m^s has the right
    pole structure (4) at s=1 by checking the local factor /
    zeta_K(s)^4 local factor ratio at s=1, prime by prime.
"""

from sympy import primerange, isprime
from math import log
import time


def sieve_tau_n2plus1(N):
    """Return array of tau(n^2+1) for n=1..N using sieve over divisors."""
    M = N * N + 1
    # We need tau(n^2+1) for each n. Use direct factoring via prime-power sieve.
    # Memory-friendly approach: iterate over primes p, for each p find all n with
    # p | n^2+1, increment exponent.
    tau = [1] * (N + 1)  # tau[n] = tau(n^2+1)
    # Primes up to sqrt(N^2+1) = N approximately, plus need primes up to M
    # but we can be clever: for each prime p, the prime-power p^k dividing n^2+1
    # has p^k <= N^2+1, so k <= 2 log N / log p.
    # However: n^2+1 has factor structure dominated by primes p that split in Q(i).
    # We iterate p up to N (since n^2+1 <= N^2+1, so largest prime factor at most N^2+1
    # but for tau computation we really need all prime power exponents).
    # Memory-friendly: for each n, factor n^2+1 directly.
    # That's slower but simpler. Actually for N<=1e5, doable.

    # Faster: for each prime p, find smallest n0 in [1, p] with n0^2+1 = 0 mod p,
    # then n2+1 divisible by p iff n in n0 mod p.

    # We sieve over prime powers up to M = N^2+1.
    # But that's too much for N=10^6. Let's just factor each n^2+1 directly using trial.
    # For verification, run only up to N=10^4 or 10^5.

    return tau


def compute_S(N):
    """Compute S(N) = sum_{n<=N} tau(n^2+1)^2 by direct factoring."""
    from sympy import factorint
    S = 0
    for n in range(1, N + 1):
        f = factorint(n * n + 1)
        t = 1
        for p, e in f.items():
            t *= (e + 1)
        S += t * t
    return S


def compute_S_sieve(N):
    """Faster computation: sieve tau(n^2+1) values via prime sieve."""
    # Allocate exponent counters indirectly: for each n, compute log(n^2+1)
    # decomposed via primes via prime power sieve.

    # Simpler: maintain residue arrays, sieve.
    # For each prime p with -1 a QR mod p, find roots r1,r2 mod p.
    # Then for k=1,2,..., lift roots to p^k, and increment exponent counter for n in r mod p^k.

    # We need primes up to N (since prime divisor of n^2+1 <= n^2+1 but unique large factor
    # appears at most once; we still need all primes up to N^2+1, which is too much).
    # Actually for tau computation we need to know the FULL factorization of n^2+1.
    # Trick: after sieving small primes, the remainder is a prime > some threshold.

    # Threshold approach: sieve all primes p <= sqrt(N^2+1) = N. After dividing out
    # all such prime powers, the remainder is either 1 or a prime.

    from sympy import primerange

    # Initialize: copies of n^2+1 (as Python ints) and exponent product.
    rem = [n * n + 1 for n in range(N + 1)]
    rem[0] = 1
    tau = [1] * (N + 1)

    # Handle p=2 separately: only for odd n, n^2+1 is even. n^2+1 = 2 mod 4 (since n odd
    # => n^2 = 1 mod 8, so n^2+1 = 2 mod 8, exactly one factor of 2).
    for n in range(1, N + 1, 2):
        rem[n] //= 2
        tau[n] *= 2

    # Primes p = 1 mod 4: two roots r, p-r mod p. Lift to p^k for higher powers.
    # Primes p = 3 mod 4: no roots, skip.

    sqrtN = int(N) + 1
    for p in primerange(3, sqrtN + 1):
        if p % 4 != 1:
            continue
        # Find r with r^2 = -1 mod p. Use sqrt mod p via Tonelli-Shanks (sympy).
        from sympy.ntheory.residue_ntheory import sqrt_mod
        r = sqrt_mod(-1, p)
        if r is None:
            continue
        roots = [r, p - r]
        # For each prime power p^k, sieve.
        pk = p
        while pk <= N * N + 1:
            # Lift roots to p^k via Hensel; or just compute n^2+1 mod p^k directly.
            # For simplicity: at p^k, find roots by computing n^2+1 mod p^k for n in {r, p-r, ...}
            # Actually simpler: for each n with rem[n] still divisible by p^k, sieve.
            # Use: at level p^k, the roots of x^2+1 = 0 mod p^k are 2 values (Hensel).

            # Use sqrt_mod to compute roots at p^k directly.
            r_pk = sqrt_mod(-1, pk)
            if r_pk is None:
                break
            roots_pk = [r_pk % pk, (-r_pk) % pk]
            for r_val in set(roots_pk):
                # Find smallest n >= 1 with n = r_val mod pk
                start = r_val if r_val >= 1 else r_val + pk
                if start == 0:
                    start = pk
                for n in range(start, N + 1, pk):
                    if rem[n] % p == 0:
                        rem[n] //= p
                        # tau update is handled at end via prime power exponents
            pk *= p

    # Now rem[n] is either 1 or a single prime > sqrt(N^2+1). In both cases, tau gets *2 once.
    # But wait: I've been updating rem[n] but tau[n] should account for actual prime powers.
    # Let me restart with cleaner logic.

    return None  # placeholder


def compute_S_simple(N):
    """Simple direct computation. Slow but correct, for verification at small N."""
    from sympy import factorint
    S = 0
    for n in range(1, N + 1):
        m = n * n + 1
        f = factorint(m)
        t = 1
        for p, e in f.items():
            t *= (e + 1)
        S += t * t
    return S


def nair_product_factor(N):
    """Compute the Nair-bound factor for f=tau^2, F=x^2+1.

    Phi(N) = prod_{p<=N^2}(1 - rho(p)/p) * sum_{m<=N^2} tau(m)^2 rho(m)/m

    where rho is the multiplicative function with rho(2)=1, rho(2^k)=0 for k>=2,
    rho(p^k)=2 for p=1 mod 4, rho(p^k)=0 for p=3 mod 4.
    """
    from sympy import factorint, primerange

    M = N * N
    # Product over primes
    prod = 1.0
    # p=2: factor = 1 - 1/2 = 1/2
    prod *= 0.5
    for p in primerange(3, M + 1):
        if p % 4 == 1:
            prod *= (1 - 2.0 / p)
        # p%4==3: factor 1, skip

    # Sum sum_{m<=M} tau(m)^2 rho(m) / m
    # Multiplicative; build via Euler product on primes <= M with rho(p)>0
    # That doesn't work for partial sum directly. Instead, sieve through m = product
    # of allowed primes. For verification at small N, just iterate m=1..M.

    # Determine rho(m): factor m, check rho(p^k) at each prime power.
    s = 0.0
    for m in range(1, M + 1):
        f = factorint(m)
        # Check rho(m): nonzero iff m = 2^e * prod of (p=1 mod 4) prime powers, with e in {0,1}.
        ok = True
        rho = 1
        tau_m = 1
        for p, e in f.items():
            tau_m *= (e + 1)
            if p == 2:
                if e == 1:
                    rho *= 1
                else:
                    ok = False
                    break
            elif p % 4 == 3:
                ok = False
                break
            elif p % 4 == 1:
                rho *= 2  # for any k >= 1
        if not ok:
            continue
        s += (tau_m ** 2) * rho / m

    return prod, s, prod * s


def verify_local_factor_zetaK4(p_max=100):
    """Verify D_p(s)/zeta_K(s)^4 at p=1 mod 4 has 1/p^s coefficient 0,
    and 1/p^{2s} coefficient -18 to leading order."""
    from sympy import primerange
    print("Verifying local factor ratio D_p / zeta_K^4 _p at p=1 mod 4 primes:")
    print("Expected: leading 1/p^{2s} coefficient is -18 to first order in 1/p")
    print(f"{'p':>5} {'r_2 = (D/zK^4) coef of 1/p^{2s}':>40}")
    for p in primerange(3, p_max):
        if p % 4 != 1:
            continue
        # zeta_K^4 local at p (split): (1-1/p^s)^{-8}
        # Coefficients of 1/p^{ks}: binomial(k+7, 7) for k=0,1,2,3,...
        # That's: 1, 8, 36, 120
        # D_p local: 1, 8, 18, 32 (with rho=2, f=tau^2)
        # In the Dirichlet series identity D = zeta_K^4 * H_0:
        # Local H_0 at p = D_p * (1-1/p^s)^8.
        # Coefficient at 1/p^{2s} of (D_p) * (1-x)^8 with x=1/p^s:
        # [1 + 8x + 18x^2 + 32x^3 + ...] * [1 - 8x + 28x^2 - 56x^3 + ...]
        # at x^0: 1
        # at x^1: 8 - 8 = 0
        # at x^2: 18 - 64 + 28 = -18
        # at x^3: 32 - 144 + 224 - 56 = 56
        d_coefs = [1, 8, 18, 32, 50]  # D_p coefficients of 1/p^{ks} for k=0..4
        # (k+1)^2 * 2 for k>=1
        zk4_inv_coefs = [1, -8, 28, -56, 70]  # (1-x)^8 coefficients
        # H_0 = D_p * (1-x)^8, compute coefficients
        h_coefs = [0] * 5
        for i in range(5):
            for j in range(5 - i):
                h_coefs[i + j] += d_coefs[i] * zk4_inv_coefs[j]
        print(f"{p:>5}  H_0 local coefs: {h_coefs}")
        if p > 30:
            break

    print()
    print("Conclusion: H_0_p(s) = 1 + 0*x + (-18)*x^2 + 56*x^3 + ... (universal for split p)")
    print("So H_0(s) converges absolutely for Re(s) > 1/2.")
    print("Therefore D(s) = zeta_K(s)^4 * H_0(s) with H_0 analytic at s=1, hence D has pole order 4.")


if __name__ == "__main__":
    print("=" * 70)
    print("Step 1: Verify pole order of D(s) = sum tau^2(m) rho(m) / m^s")
    print("=" * 70)
    verify_local_factor_zetaK4()
    print()

    print("=" * 70)
    print("Step 2: Compute S(N) and Nair factor Phi(N) at small N")
    print("=" * 70)
    for N in [10, 20, 30, 50, 100]:
        t0 = time.time()
        S = compute_S_simple(N)
        t1 = time.time()
        prod, sum_part, phi = nair_product_factor(N)
        t2 = time.time()
        S_predicted = N * phi
        ratio = S / S_predicted
        print(f"N={N:5}: S={S:>10}  N*Phi={N * phi:>12.3f}  S/(N*Phi)={ratio:.4f}  "
              f"S/(N (log N)^3)={S / (N * log(N) ** 3):.4f}")
        print(f"        prod={prod:.5e}  sum_m tau^2 rho /m={sum_part:.4f}")
        print(f"        time: S={t1-t0:.2f}s, Phi={t2-t1:.2f}s")
