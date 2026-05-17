"""Compare empirical |U_h(N)| (unweighted phase sum) vs |T_h(N)| (rooted).

U_h(N) := sum over sf, "good" e <= N of e^{2 pi i h N / e}
   (one phase per e, no root expansion)

T_h(N) := sum over sf, "good" e <= N of sum over roots r_i of (n^2+1) mod e
            of e^{2 pi i h (N - r_i) / e}
   (rho(e) phases per e)

If both are O(sqrt N), then the cancellation lives in the e-direction
(B-process / van der Corput territory). If U_h is bigger than T_h, then
the root sum / multiplicative weight is essential.
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
    if p == 2:
        return 1
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            break
    return pow(z, (p - 1) // 4, p)


def factor_sf_good(e, spf):
    pf = []
    n = e
    while n > 1:
        p = int(spf[n])
        n //= p
        if n % p == 0:
            return None
        if p != 2 and p % 4 == 3:
            return None
        pf.append(p)
    return pf


def crt_roots(pf, root_cache):
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


def compute_Uh_Th(N_target, spf, root_cache, h_list):
    """Compute both U_h and T_h in one pass."""
    U = {h: 0.0 + 0.0j for h in h_list}
    T = {h: 0.0 + 0.0j for h in h_list}
    two_pi = 2.0 * math.pi
    for e in range(2, N_target + 1):
        pf = factor_sf_good(e, spf)
        if pf is None:
            continue
        # U_h: single phase e^{2 pi i h N / e}
        for h in h_list:
            phase_U = two_pi * h * (N_target % e) / e   # h N mod e for accuracy
            U[h] += complex(math.cos(phase_U), math.sin(phase_U))
        # T_h: phase per root
        roots = crt_roots(pf, root_cache)
        for r in roots:
            y = (N_target - r) % e
            for h in h_list:
                phase = two_pi * h * y / e
                T[h] += complex(math.cos(phase), math.sin(phase))
    return U, T


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e6)
    h_list = [1, 2, 5, 10, 100]

    t0 = time.time()
    spf = smallest_prime_factor(N)
    print(f"# SPF sieve to {N} in {time.time()-t0:.1f}s", file=sys.stderr)

    t1 = time.time()
    root_cache = {}
    is_prime = (spf == np.arange(N + 1, dtype=np.int64))
    for p in range(2, N + 1):
        if is_prime[p] and (p == 2 or p % 4 == 1):
            root_cache[p] = find_root_mod_p(p)
    print(f"# Root cache for {len(root_cache)} primes in {time.time()-t1:.1f}s", file=sys.stderr)

    t2 = time.time()
    U, T = compute_Uh_Th(N, spf, root_cache, h_list)
    print(f"# Sum loop in {time.time()-t2:.1f}s", file=sys.stderr)

    sqrtN = math.sqrt(N)
    print(f"\n# N = {N}, sqrt(N) = {sqrtN:.2f}")
    print(f"{'h':>5} | {'|U_h|':>12} | {'|U_h|/sqrtN':>12} | {'|T_h|':>12} | {'|T_h|/sqrtN':>12} | ratio")
    print("-" * 78)
    for h in h_list:
        rU = abs(U[h]) / sqrtN
        rT = abs(T[h]) / sqrtN
        print(f"{h:>5} | {abs(U[h]):>12.2f} | {rU:>12.4f} | {abs(T[h]):>12.2f} | {rT:>12.4f} | {abs(U[h])/abs(T[h]):>6.3f}")
