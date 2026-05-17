"""
Compute the secondary-term decomposition for B_3^bdy(N).

Identity (exact, no asymptotics):

  B_3^bdy(N) = sum_{n<=N} 2^{omega(d_n)} (N_{d_n}(N) - rho(d_n) N / d_n)
             = T(N) + P(N) - N * K_N

where d_n = n^2+1,
  T(N) = sum_{n<=N} 2^{omega(d_n)}     (the diagonal: m=n always counts)
  P(N) = sum_{n<=N} 2^{omega(d_n)} (N_{d_n}(N) - 1)   (off-diagonal pairs, n != m)
  K_N  = sum_{n<=N} 2^{omega(d_n)} rho(d_n) / d_n     (analytic correction)

Goal: confirm c_1 = H(1)*pi/2 = 0.8681 for B_3^bdy by checking that the
secondary residual
  resid_bdy(N) := (B_3^bdy - c_1 N log N) / N
matches  (T - c_1 N log N)/N + P/N - K_N
where (T - c_1 N log N)/N -> c_0 ~= 0.99 (stable from prior empirical),
P/N -> off-diag-pair density, K_N -> K_inf finite constant.

Compute T, P, K at the same N as the prior B_3-boundary run.
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

def factor_n2plus1(n, split_primes):
    """Return (omega, rho) for n^2+1.
       split_primes: primes <= n with p % 4 == 1 (and we handle p=2)."""
    m = n * n + 1
    omega = 0
    rho_count = 1
    if m % 2 == 0:
        omega += 1
        # rho(2) = 1, no change to rho_count
        while m % 2 == 0:
            m //= 2
    for p in split_primes:
        if p * p > m:
            break
        if m % p == 0:
            omega += 1
            rho_count *= 2
            while m % p == 0:
                m //= p
    if m > 1:
        omega += 1
        rho_count *= 2  # m is a prime > sqrt(orig m), so m | n^2+1 means m == 1 mod 4 (since n^2 != -1 mod p for p == 3)
    return omega, rho_count

def tonelli_minus1(p):
    e = (p - 1) // 4
    for a in range(2, p):
        x = pow(a, e, p)
        if (x * x) % p == p - 1:
            return x
    raise RuntimeError(f"no root mod {p}")

def hensel_lift(p, k, x):
    pk = p
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

def all_roots_d(d, factorization):
    """factorization: list of (p, e). Returns list of roots x mod d of x^2 = -1."""
    if not factorization:
        return [0], 1
    moduli_roots = []
    for (p, e) in factorization:
        if p == 2:
            assert e == 1
            moduli_roots.append((2, [1]))
        else:
            x = tonelli_minus1(p)
            x = hensel_lift(p, e, x) if e > 1 else x
            pe = p**e
            moduli_roots.append((pe, [x, pe - x]))
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

def factor_full(n, split_primes):
    """Full factorization of n^2+1 as list of (p, e)."""
    m = n * n + 1
    facs = []
    e = 0
    while m % 2 == 0:
        m //= 2
        e += 1
    if e:
        facs.append((2, e))
    for p in split_primes:
        if p * p > m:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            facs.append((p, e))
    if m > 1:
        facs.append((m, 1))
    return facs

def compute_decomposition(N):
    """For all n <= N, compute T, P, K_N pieces."""
    primes = primes_up_to(N)
    split_primes = [p for p in primes if p % 4 == 1]
    T = 0
    P = 0   # off-diag pairs
    K_sum = 0.0  # K_N = sum 2^om * rho / d_n
    # cache roots per (p, e) implicitly through factor_full
    for n in range(1, N+1):
        facs = factor_full(n, split_primes)
        d = n * n + 1
        omega = len(facs)
        rho = 1
        for (p, e) in facs:
            if p == 2: rho *= 1
            else: rho *= 2
        two_om = 1 << omega
        T += two_om
        K_sum += two_om * rho / d
        # Compute N_d(N) (number of m <= N with d | m^2+1)
        roots, mod = all_roots_d(d, facs)
        Nd = 0
        for x in roots:
            x_pos = x if x >= 1 else d
            if x_pos <= N:
                Nd += (N - x_pos) // d + 1
        # off-diag: P contribution from this n
        P += two_om * (Nd - 1)
    return T, P, K_sum

if __name__ == "__main__":
    # H(1) constant precomputed: 0.55267217 (10^6 prime cap, error <2e-7)
    H1 = 0.5526721690
    c1 = H1 * math.pi / 2
    Ns = [500, 1000, 2000, 3000, 5000, 10000]
    expected_B3_bdy = {500: 2831, 1000: 6393, 2000: 14190, 3000: 22617, 5000: 40325, 10000: 87322}
    print(f"c_1 = H(1) pi/2 = {c1:.6f}")
    print(f"{'N':>6} {'T(N)':>10} {'P(N)':>8} {'K_N':>9} {'B3_bdy_pred':>13} {'B3_bdy_emp':>11} {'(T-c1NL)/N':>11} {'(B3-c1NL)/N':>12}")
    for N in Ns:
        t0 = time.time()
        T, P, K_N = compute_decomposition(N)
        dt = time.time() - t0
        L = math.log(N)
        B3_pred = T + P - N * K_N
        B3_emp = expected_B3_bdy.get(N, float('nan'))
        T_resid = (T - c1 * N * L) / N
        B3_resid = (B3_pred - c1 * N * L) / N
        match = "ok" if abs(B3_pred - B3_emp) < 1.5 else "DIFF"
        print(f"{N:>6} {T:>10} {P:>8} {K_N:>9.4f} {B3_pred:>13.2f} {B3_emp:>11} {T_resid:>11.4f} {B3_resid:>12.4f}  [{match}, {dt:.1f}s]")
