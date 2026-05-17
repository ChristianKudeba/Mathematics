"""
Decompose B(N) by the maximal squarefull divisor q of n^2+1.

For each n with n^2+1 non-sf, write n^2+1 = q*k with gcd(q,k)=1, q squarefull, k sf.
Then b(n) = #{e sf | n^2+1: sqrt(rad(n^2+1)) < e <= n}.

We bin by q and aggregate:
  B_q^*(N) := sum_{n <= N, max sqfull div of n^2+1 = q} b(n)
  N_q^*(N) := #{n <= N: max sqfull div of n^2+1 = q}

Empirical density: D_q^*(N) = N_q^*(N) / N -> D_q (limit).
Conditional mean:  E_q^*(N) = B_q^*(N) / N_q^*(N) -> E_q.
Contribution:      B_q^*(N)/N -> D_q * E_q.
Total: sum_q D_q E_q = B^infty.

Analytic prediction for D_q (squarefull q with all primes ≡ 1 mod 4):
  D_q = C_0 * prod_{p|q} [ 2(1-1/p) / (p^{v_p(q)} (1 - 2/p^2)) ]
where C_0 := prod_{p ≡ 1 mod 4} (1 - 2/p^2) is Estermann's constant.

Note: a prime ≡ 1 mod 4 contributes; p=2 contributes only with v_2 ∈ {0,1}, never to q.
Inert primes (p ≡ 3 mod 4) contribute density 1 trivially.
"""

import math
import time
import sys

R = math.pi / 4


def primes_up_to(M):
    if M < 2:
        return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]


def factor_n2plus1(n, split_primes_arr):
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
        out.append((m, 1))
    return out


def compute_B_by_q(N, split_primes_arr):
    """Compute B(N) decomposed by max squarefull divisor q.

    Returns dict q -> (count_n, B_q) and total stats.
    """
    by_q = {}     # q (as tuple of (p, v_p) pairs sorted) -> [count_n, B_q]
    total_B = 0
    total_non_sf = 0

    for n in range(1, N+1):
        m = n*n + 1
        factors = factor_n2plus1(n, split_primes_arr)
        rad = 1
        is_sf = True
        for p, e in factors:
            rad *= p
            if e > 1:
                is_sf = False
        if is_sf:
            continue
        total_non_sf += 1

        # max squarefull divisor: product of p^{v_p(m)} over p with v_p >= 2
        q_factors = tuple(sorted([(p, e) for p, e in factors if e >= 2]))

        # Enumerate sf divisors and count those with sqrt(rad) < e <= n
        sf_divs = [1]
        for p, _ in factors:
            sf_divs = sf_divs + [d*p for d in sf_divs]
        bn = 0
        for e in sf_divs:
            if e*e > rad and e <= n:
                bn += 1

        if q_factors not in by_q:
            by_q[q_factors] = [0, 0]
        by_q[q_factors][0] += 1
        by_q[q_factors][1] += bn
        total_B += bn

    return by_q, total_B, total_non_sf


def q_value(q_factors):
    v = 1
    for p, e in q_factors:
        v *= p**e
    return v


def predicted_D_q(q_factors, C0):
    """Analytic prediction D_q = C_0 prod_{p|q} 2(1-1/p)/(p^{v_p}(1 - 2/p^2))."""
    prod = C0
    for p, v in q_factors:
        prod *= 2 * (1 - 1.0/p) / (p**v * (1 - 2.0/(p*p)))
    return prod


def main():
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [100000, 300000]
    Pbound = max(targets)
    print(f"Sieving primes up to {Pbound}...", flush=True)
    t0 = time.time()
    split_primes = [p for p in primes_up_to(Pbound) if p == 2 or p % 4 == 1]
    print(f"  {len(split_primes)} split primes (incl 2). {time.time()-t0:.1f}s", flush=True)

    # Compute Estermann's constant C_0 = prod_{p ≡ 1 mod 4} (1 - 2/p^2)
    # Use high-precision Euler product for convergence
    C0 = 1.0
    for p in split_primes:
        if p % 4 == 1:
            C0 *= (1 - 2.0/(p*p))
    # Tail for p > Pbound: log C_0_tail = sum_{p > P} log(1 - 2/p^2) ~ -2 sum_{p > P, p ≡ 1 mod 4} 1/p^2
    # ~ -2 * (1/2) * 1/(Pbound log Pbound) by PNT, very small
    print(f"C_0 (truncated to p <= {Pbound}) = {C0:.10f}", flush=True)
    print()

    for N in targets:
        sp_for_N = [p for p in split_primes if p <= N]
        t0 = time.time()
        by_q, total_B, total_non_sf = compute_B_by_q(N, sp_for_N)
        elapsed = time.time() - t0
        Nf = float(N)

        # Sort by descending B_q contribution
        items = sorted(by_q.items(), key=lambda kv: -kv[1][1])
        print(f"=== N = {N}  (took {elapsed:.1f}s) ===", flush=True)
        print(f"  total B(N) = {total_B}, B/N = {total_B/Nf:.6f}", flush=True)
        print(f"  total non-sf count = {total_non_sf}, density = {total_non_sf/Nf:.6f}", flush=True)
        print(f"  predicted non-sf density = 1 - C_0 = {1-C0:.6f}", flush=True)
        print()
        print(f"  {'q':>15} {'count_n':>10} {'B_q':>8} {'B_q/N':>10} {'count/N (D_q)':>14} {'pred D_q':>10} {'B_q/count':>10}", flush=True)
        # Print top 20 by contribution
        agg_B_simple_p2 = 0
        agg_count_simple_p2 = 0
        for q_factors, (count, B_q) in items[:20]:
            qv = q_value(q_factors)
            Dq_emp = count / Nf
            Dq_pred = predicted_D_q(q_factors, C0)
            E_q_emp = B_q / count if count > 0 else 0
            B_q_over_N = B_q / Nf
            q_label = "*".join(f"{p}^{e}" for p, e in q_factors) if q_factors else "1"
            print(f"  {q_label:>15} {count:>10} {B_q:>8} {B_q_over_N:>10.6f} {Dq_emp:>14.6f} {Dq_pred:>10.6f} {E_q_emp:>10.4f}", flush=True)
            # Track simple p^2 patterns (single prime, exponent 2)
            if len(q_factors) == 1 and q_factors[0][1] == 2:
                agg_B_simple_p2 += B_q
                agg_count_simple_p2 += count

        # Aggregate stats
        print()
        # Aggregate by omega(q)
        by_omega = {}
        for q_factors, (count, B_q) in by_q.items():
            w = len(q_factors)
            if w not in by_omega:
                by_omega[w] = [0, 0]
            by_omega[w][0] += count
            by_omega[w][1] += B_q
        print(f"  Aggregate by omega(q):", flush=True)
        for w in sorted(by_omega.keys()):
            count, B_q = by_omega[w]
            print(f"    omega(q) = {w}: count = {count} ({count/Nf:.5f} density), B = {B_q} ({B_q/Nf:.6f} contrib to B/N)", flush=True)

        # Aggregate by max exponent
        by_maxexp = {}
        for q_factors, (count, B_q) in by_q.items():
            mx = max(e for p, e in q_factors)
            if mx not in by_maxexp:
                by_maxexp[mx] = [0, 0]
            by_maxexp[mx][0] += count
            by_maxexp[mx][1] += B_q
        print(f"  Aggregate by max exp v_max(q):", flush=True)
        for mx in sorted(by_maxexp.keys()):
            count, B_q = by_maxexp[mx]
            print(f"    v_max = {mx}: count = {count} ({count/Nf:.5f}), B = {B_q} ({B_q/Nf:.6f})", flush=True)

        # Simple p^2 (single prime squared) aggregate
        print(f"  Simple p^2 (single prime, exp=2): count={agg_count_simple_p2}, B={agg_B_simple_p2}, contrib B/N = {agg_B_simple_p2/Nf:.6f}", flush=True)
        print()


if __name__ == '__main__':
    main()
