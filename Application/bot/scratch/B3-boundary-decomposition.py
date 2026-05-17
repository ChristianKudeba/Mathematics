"""
Compute the "diagonal" contribution to B_3(N):

  B_3^bdy(N) = sum_{n <= N} 2^omega(n^2+1) * delta_{n^2+1}(N)

where delta_d(N) = N_d(N) - rho(d) N/d.

For d = n^2+1, count N_d(N) = number of n' <= N with d | (n')^2 + 1.
n itself is one such; we look for any others (typically there are none for moderate-to-large n).

Then B_3^off(N) = B_3(N) - B_3^bdy(N).

Run at the same Ns as B3-direct-sieve.py for comparison.
"""
import math, sys, time

def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]

def factor_n2plus1(n, primes_le_n):
    """Return prime factorization of n^2+1 as list of (p, e), via trial division.
       Uses that n^2+1 has only primes 2 and p == 1 mod 4 (which we pass in)."""
    m = n * n + 1
    factors = []
    # 2
    e = 0
    while m % 2 == 0:
        m //= 2
        e += 1
    if e:
        factors.append((2, e))
    for p in primes_le_n:
        if p > n:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            factors.append((p, e))
    if m > 1:
        # m is a prime > n (must be prime since m < (n+1)^2 and m has no factor <= n)
        factors.append((m, 1))
    return factors

def tonelli_minus1(p):
    """Find x with x^2 = -1 mod p, p == 1 mod 4, using random search."""
    target = p - 1
    e = (p - 1) // 4
    for a in range(2, p):
        x = pow(a, e, p)
        if (x * x) % p == target:
            return x
    raise RuntimeError(f"no root mod {p}")

def hensel_minus1_pk(p, k, x_p):
    pk = p
    x = x_p
    for _ in range(k - 1):
        pk_next = pk * p
        f = (x * x + 1) % pk_next
        fp = (2 * x) % pk_next
        fp_inv = pow(fp, -1, pk_next)
        x = (x - f * fp_inv) % pk_next
        pk = pk_next
    return x

def crt_combine(r1, m1, r2, m2):
    inv = pow(m1 % m2, -1, m2)
    t = ((r2 - r1) * inv) % m2
    return (r1 + m1 * t) % (m1 * m2), m1 * m2

def all_roots_for_factorization(factors, root_cache):
    """factors: list of (p, e) with p == 1 mod 4 (or p=2 with e=1).
       Return all roots x mod d = prod p^e of x^2 = -1 mod d."""
    moduli_roots = []
    for (p, e) in factors:
        if p == 2:
            if e != 1:
                # n^2+1 has 2-adic valuation at most 1 (for n odd) or 0 (n even)
                raise RuntimeError(f"unexpected e={e} for p=2")
            moduli_roots.append((2, [1]))
        else:
            key = (p, e)
            if key in root_cache:
                x_pk = root_cache[key]
            else:
                if (p, 1) in root_cache:
                    x_p = root_cache[(p, 1)]
                else:
                    x_p = tonelli_minus1(p)
                    root_cache[(p, 1)] = x_p
                x_pk = hensel_minus1_pk(p, e, x_p) if e > 1 else x_p
                root_cache[key] = x_pk
            mod_pk = p ** e
            moduli_roots.append((mod_pk, [x_pk, mod_pk - x_pk]))
    if not moduli_roots:
        return [], 1
    cur_mod = moduli_roots[0][0]
    cur_roots = list(moduli_roots[0][1])
    for (m, rs) in moduli_roots[1:]:
        new_roots = []
        for cr in cur_roots:
            for r in rs:
                combined, _ = crt_combine(cr, cur_mod, r, m)
                new_roots.append(combined)
        cur_mod *= m
        cur_roots = new_roots
    return cur_roots, cur_mod

def Nd_from_roots(roots, d, N):
    total = 0
    for x in roots:
        x_pos = x if x >= 1 else d
        if x_pos <= N:
            total += (N - x_pos) // d + 1
    return total

def compute_boundary(N):
    primes = [2] + [p for p in primes_up_to(N) if p % 4 == 1]
    split_primes_le_N = [p for p in primes_up_to(N) if p % 4 == 1]
    root_cache = {}
    B3_bdy = 0.0
    extra_roots_count = 0  # count of n where N_d > 1
    sum_omega = 0  # sum of 2^omega(n^2+1)
    sum_2omega = 0
    for n in range(1, N+1):
        factors = factor_n2plus1(n, split_primes_le_N)
        d = n * n + 1
        omega = len(factors)
        rho = 1
        for (p, e) in factors:
            if p == 2:
                rho *= 1
            else:
                rho *= 2
        # All roots
        roots, mod = all_roots_for_factorization(factors, root_cache)
        assert mod == d, f"n={n}, d={d}, mod={mod}"
        Nd = Nd_from_roots(roots, d, N)
        if Nd > 1:
            extra_roots_count += 1
        delta = Nd - rho * N / d
        contrib = (1 << omega) * delta
        B3_bdy += contrib
        sum_2omega += 1 << omega
    return B3_bdy, sum_2omega, extra_roots_count

if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [1000, 3000]
    expected_B3 = {500: 333.71, 1000: 336.00, 2000: 879.43, 3000: 1556.66, 5000: 2469.61, 7000: 3602.04, 10000: 4740.21, 15000: 6259.95, 20000: 11832.35, 30000: 17207.82}
    print(f"{'N':>6} {'B_3':>12} {'B_3_bdy':>12} {'B_3_off (=B_3 - bdy)':>22} {'sum 2^om':>10} {'B_3/N':>10} {'B_bdy/N':>10}")
    for N in Ns:
        t0 = time.time()
        bdy, s2om, extras = compute_boundary(N)
        B3 = expected_B3.get(N, float('nan'))
        off = B3 - bdy
        print(f"{N:>6} {B3:>12.4f} {bdy:>12.4f} {off:>22.4f} {s2om:>10} {B3/N:>10.4f} {bdy/N:>10.4f}  ({time.time()-t0:.1f}s, extras={extras})")
