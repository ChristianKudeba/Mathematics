"""
Empirical study of E(N) = F(N) - <F(N)>, where
  F(N) = sum_{e sf, 2 <= e <= N} sum_{i=1..rho(e)} {(N - r_i^{(e)}) / e}
  <F(N)> = (1/2) A(N) - (1/2) Sigma_*(N) + 1/2
            with A(N) = sum_{e sf, 2 <= e <= N} rho(e),
                 Sigma_*(N) = sum_{e sf, e <= N} rho(e)/e (incl. e=1).

The rigorous part of P12-B-infty-existence-equivalence (Lemma 3.4) needs
E(N) = o(N).  We empirically test this and look at the apparent rate.

Strategy:
- Sieve squarefree e in [2, N] and compute rho(e) via prime factorization.
- For each e, find the roots r_i of x^2 == -1 (mod e) by CRT from primes p|e.
- Sum {(N - r_i)/e} over (e, i).
"""
import numpy as np
import math
import time
import sys

def mu_sieve(N):
    """Mobius function up to N via sieve."""
    mu = np.ones(N+1, dtype=np.int8)
    mu[0] = 0
    is_prime = np.ones(N+1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, N+1):
        if is_prime[i]:
            for j in range(i, N+1, i):
                if j > i:
                    is_prime[j] = False
                mu[j] = -mu[j]
            i2 = i*i
            for j in range(i2, N+1, i2):
                mu[j] = 0
    return mu

def smallest_prime_factor(N):
    """SPF[k] = smallest prime factor of k for 2 <= k <= N."""
    spf = np.zeros(N+1, dtype=np.int64)
    for i in range(2, N+1):
        if spf[i] == 0:
            for j in range(i, N+1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf

def prime_factors(n, spf):
    """Distinct prime factors of squarefree n (or any n; returns set)."""
    pf = []
    while n > 1:
        p = int(spf[n])
        pf.append(p)
        while n % p == 0:
            n //= p
    return pf

def find_root_mod_p(p):
    """Find r with r^2 == -1 mod p, for p prime, p == 1 mod 4 or p == 2."""
    if p == 2:
        return 1
    # Tonelli-Shanks for sqrt(-1) mod p, p == 1 mod 4
    # Find quadratic non-residue
    for z in range(2, p):
        if pow(z, (p-1)//2, p) == p-1:
            break
    # p-1 = q * 2^s
    q, s = p-1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    # We want sqrt(-1).  Method: r = z^((p-1)/4) since p == 1 mod 4.
    return pow(z, (p-1)//4, p)

def compute_F_and_mean(N, verbose=False):
    """Compute F(N) and <F(N)> = (1/2)A(N) - (1/2)Sigma_*(N) + 1/2.

    Returns (F, F_mean, A, Sigma_star, num_e_sf_with_rho)."""
    t0 = time.time()
    spf = smallest_prime_factor(N)
    if verbose:
        print(f"SPF sieve done at N={N} in {time.time()-t0:.2f}s", file=sys.stderr)

    # Cache root-mod-p for each "good" prime
    root_cache = {}

    F = 0.0
    A = 0
    Sigma_star = 1.0  # e=1 contributes rho(1)/1 = 1
    num_e_with_rho = 1  # e=1

    # For each squarefree e in [2, N] with rho(e) >= 1:
    # rho(e) = prod_{p | e} rho(p), where rho(2) = 1, rho(p) = 2 if p == 1 mod 4, 0 if 3 mod 4
    # squarefree iff all prime factors distinct.
    # We sieve as: iterate e=2..N, factor via spf, check sf and rho>0.

    t1 = time.time()
    for e in range(2, N+1):
        # factor e
        n = e
        pf = []
        sf = True
        while n > 1:
            p = int(spf[n])
            pf.append(p)
            n //= p
            if n % p == 0:
                sf = False
                break
        if not sf:
            continue
        # Check rho > 0: no prime factor == 3 mod 4, and 4 not divides (auto since sf and only one 2)
        bad = False
        rho_e = 1
        for p in pf:
            if p == 2:
                rho_e *= 1
            elif p % 4 == 1:
                rho_e *= 2
            else:  # p % 4 == 3
                bad = True
                break
        if bad:
            continue
        # Compute roots r_i of x^2 == -1 (mod e) via CRT
        # For each prime p in pf: roots are {root_p, p - root_p} for p == 1 mod 4, {1} for p=2
        # CRT product gives rho(e) total roots
        roots = [0]
        modulus = 1
        for p in pf:
            if p not in root_cache:
                root_cache[p] = find_root_mod_p(p)
            rp = root_cache[p]
            if p == 2:
                p_roots = [1]
            else:
                p_roots = [rp, p - rp]
            new_roots = []
            for r in roots:
                for s in p_roots:
                    # combine r mod modulus with s mod p
                    # via Bezout
                    # r' such that r' == r mod modulus, r' == s mod p
                    new_modulus = modulus * p
                    diff = (s - r) % p
                    inv_modulus = pow(modulus, -1, p)
                    k = (diff * inv_modulus) % p
                    rp_new = (r + k * modulus) % new_modulus
                    new_roots.append(rp_new)
            roots = new_roots
            modulus = modulus * p
        # roots are the rho(e) roots in [0, e-1], all in [1, e-1] since 0^2 + 1 != 0
        # Compute sum_i {(N - r_i) / e}
        for r in roots:
            frac = ((N - r) % e) / e
            F += frac
        A += rho_e
        Sigma_star += rho_e / e
        num_e_with_rho += 1

        if verbose and e % 1000000 == 0:
            print(f"e = {e}, elapsed {time.time()-t1:.1f}s", file=sys.stderr)

    F_mean = 0.5 * A - 0.5 * Sigma_star + 0.5
    if verbose:
        print(f"Total compute time: {time.time()-t0:.2f}s", file=sys.stderr)
    return F, F_mean, A, Sigma_star, num_e_with_rho

if __name__ == "__main__":
    Ns = [1000, 3000, 10000, 30000, 100000]
    if len(sys.argv) > 1:
        Ns = [int(x) for x in sys.argv[1:]]
    print(f"{'N':>10} | {'F(N)':>14} | {'<F>(N)':>14} | {'E(N)':>14} | {'E/N':>10} | {'A(N)':>10} | {'Sigma_*(N)':>14}")
    print("-" * 110)
    for N in Ns:
        F, F_mean, A, Sigma_star, num_e = compute_F_and_mean(N, verbose=False)
        E = F - F_mean
        print(f"{N:>10} | {F:>14.4f} | {F_mean:>14.4f} | {E:>14.4f} | {E/N:>10.6f} | {A:>10} | {Sigma_star:>14.6f}")
