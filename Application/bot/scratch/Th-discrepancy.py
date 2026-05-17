"""
Empirical computation of E(N) AND T_h(N) for the Lemma 3.4 Fourier reduction.

For sf e in [2, N] with rho(e) >= 1, enumerate roots r_i^{(e)} of x^2 = -1 (mod e).

  E(N)   = F(N) - <F>(N), where F(N) = sum_{e,i} {(N - r_i^{(e)}) / e}
  T_h(N) = sum_{e sf, 2<=e<=N, rho(e)>=1} e^{2*pi*i*h*N/e} * S_h^*(e)
           with S_h^*(e) = sum_i e^{-2*pi*i*h*r_i^{(e)}/e}

For efficiency, we sweep e=2..N_max once, store (roots) per e, and accumulate
prefix sums to evaluate at multiple N targets.

Target run time at N_max = 10^7: a few minutes (pure Python sieve).
"""
import math
import time
import sys
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
    """r with r^2 == -1 mod p, p prime, p == 1 mod 4 or p == 2."""
    if p == 2:
        return 1
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            break
    return pow(z, (p - 1) // 4, p)


def factor_sf_good(e, spf):
    """Return list of distinct primes dividing e if e is sf and all primes in
    {2} ∪ {p ≡ 1 mod 4}; else return None."""
    pf = []
    n = e
    while n > 1:
        p = int(spf[n])
        n //= p
        if n % p == 0:
            return None  # not squarefree
        if p != 2 and p % 4 == 3:
            return None  # rho(e)=0
        pf.append(p)
    return pf


def crt_roots(pf, root_cache):
    """Given prime factors of sf e, return list of rho(e) roots of x^2 = -1 (mod e)."""
    roots = [0]
    modulus = 1
    for p in pf:
        rp = root_cache[p]
        p_roots = [1] if p == 2 else [rp, p - rp]
        new_roots = []
        for r in roots:
            for s in p_roots:
                new_modulus = modulus * p
                diff = (s - r) % p
                inv_modulus = pow(modulus, -1, p)
                k = (diff * inv_modulus) % p
                rp_new = (r + k * modulus) % new_modulus
                new_roots.append(rp_new)
        roots = new_roots
        modulus = modulus * p
    return roots


def compute_E_and_Th(N_target, spf, root_cache, h_list):
    """Single-pass over e=2..N: compute F(N), A(N), Sigma_*(N), T_h(N) for h in h_list.

    Returns dict with keys: F, A, Sigma_star, T (dict h->complex).
    """
    F = 0.0
    A = 0
    Sigma_star = 1.0  # e=1 contributes rho(1)/1 = 1
    T = {h: 0.0 + 0.0j for h in h_list}
    two_pi = 2.0 * math.pi

    for e in range(2, N_target + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        rho_e = 1
        for p in pf:
            rho_e *= 1 if p == 2 else 2

        roots = crt_roots(pf, root_cache)

        # Sum {(N - r) / e} and the twisted-root sum S_h(e)
        # S_h(e) = sum_i e^{2*pi*i*h*(N - r_i)/e}  (note: includes the N-dep phase)
        # We can split: S_h(e) = e^{2*pi*i*h*N/e} * S_h^*(e), S_h^*(e) = sum_i e^{-2*pi*i*h*r_i/e}.
        # Just compute the full thing per-e for cleanliness.
        for r in roots:
            y = (N_target - r) % e
            F += y / e
            for h in h_list:
                # phase = 2*pi*h*y/e  (integer y in [0,e-1])
                phase = two_pi * h * y / e
                T[h] += complex(math.cos(phase), math.sin(phase))
        A += rho_e
        Sigma_star += rho_e / e

    F_mean = 0.5 * A - 0.5 * Sigma_star + 0.5
    E = F - F_mean
    return {"F": F, "F_mean": F_mean, "E": E, "A": A,
            "Sigma_star": Sigma_star, "T": T, "N": N_target}


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [int(1e5), int(3e5), int(1e6), int(3e6), int(1e7)]
    h_list = [1, 2, 3, 5, 10]
    Nmax = max(Ns)
    t0 = time.time()
    spf = smallest_prime_factor(Nmax)
    print(f"# SPF sieve to N_max={Nmax} in {time.time() - t0:.1f}s", file=sys.stderr)

    # Pre-cache roots mod p for split primes p <= Nmax
    t1 = time.time()
    root_cache = {}
    is_prime = (spf == np.arange(Nmax + 1, dtype=np.int64))
    for p in range(2, Nmax + 1):
        if is_prime[p] and (p == 2 or p % 4 == 1):
            root_cache[p] = find_root_mod_p(p)
    print(f"# Root cache for {len(root_cache)} primes in {time.time() - t1:.1f}s", file=sys.stderr)

    print(f"{'N':>10} | {'E(N)':>14} | {'|E|/sqrt(N)':>12} |"
          + " | ".join([f"|T_{h}|/sqrt(N)".rjust(15) for h in h_list]))
    print("-" * 110)
    for N in Ns:
        t2 = time.time()
        out = compute_E_and_Th(N, spf, root_cache, h_list)
        E = out["E"]
        sqrtN = math.sqrt(N)
        Tabs = {h: abs(out["T"][h]) for h in h_list}
        row = f"{N:>10} | {E:>14.4f} | {abs(E)/sqrtN:>12.4f} | " \
              + " | ".join([f"{Tabs[h]/sqrtN:>15.4f}" for h in h_list])
        print(row)
        # Also print absolute |T_h|
        absrow = f"{'':>10} | {'(abs |T_h|)':>14} | {'':>12} | " \
                 + " | ".join([f"{Tabs[h]:>15.2f}" for h in h_list])
        print(absrow)
        print(f"# N={N} computed in {time.time() - t2:.1f}s; total {time.time() - t0:.1f}s",
              file=sys.stderr)
