"""
Sign-bias diagnostic on the Hooley-boundary sum

    B_3(N) = sum_{d <= N^2+1} 2^omega(d) * delta_d(N),
    delta_d(N) = N_d(N) - rho(d) N/d,
    N_d(N) = #{n <= N : d | n^2+1},
    rho(d) = #{x mod d : x^2 = -1 mod d}.

Goal: compute the SIGNED per-d contribution
    contrib(d) := 2^omega(d) * delta_d(N)
and bucket by dyadic windows of d to see:
  (a) what fraction of |B_3| lives in each window,
  (b) whether each window's contribution is mostly positive (rounding bias)
      or signed (cancellation),
  (c) whether one or two outlier d's dominate the total.

Only "supported" d (rho(d) > 0) contribute, namely d = 2^a * m with
a in {0,1} and m a product of primes p == 1 mod 4 to any power.
We enumerate them recursively, factorize on the fly (we know the prime
factorization already from the recursion path), and compute exact roots
of x^2 = -1 mod d via CRT + Hensel.

For each supported d we compute delta_d EXACTLY in rational arithmetic
(N_d is an integer; rho(d) N/d is a rational number with denominator
dividing d), then the bucket sums are rational sums.
We run at N in {1000, 3000, 10000} and verify the total against the
prior session's B_3 values.
"""
import math, time, sys
from fractions import Fraction
from collections import defaultdict

def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]

def split_primes_up_to(M):
    return [p for p in primes_up_to(M) if p % 4 == 1]

def tonelli_minus1(p):
    """Find x with x^2 = -1 mod p, p == 1 mod 4."""
    # x = a^((p-1)/4) mod p for any quadratic non-residue a -- easier to use
    # the standard fact: if g is a primitive root, x = g^((p-1)/4).
    # We use random search: pick a, check a^((p-1)/4) squared == -1.
    target = p - 1
    e = (p - 1) // 4
    for a in range(2, p):
        x = pow(a, e, p)
        if (x * x) % p == target:
            return x
    raise RuntimeError(f"no root mod {p}")

def hensel_minus1_pk(p, k, x_p):
    """Lift x_p (a root mod p) to a root mod p^k via Hensel."""
    # Newton: x_{n+1} = x_n - (x_n^2 + 1) * inverse(2 x_n) mod p^{2n}
    pk = p
    x = x_p
    for _ in range(k - 1):
        # double precision
        pk_next = pk * p
        # f(x) = x^2 + 1, f'(x) = 2x. Solve y = x + delta with delta * 2x = -(x^2+1) mod pk_next.
        # Actually Hensel doubles precision each step normally; for p^k specifically we
        # iterate k-1 times raising precision by factor of p each time, which is fine
        # as long as we go to mod pk_next.
        f = (x * x + 1) % pk_next
        fp = (2 * x) % pk_next
        # Need inverse of fp mod pk_next; gcd(fp, p) = 1 because p is odd and x !=0 mod p.
        fp_inv = pow(fp, -1, pk_next)
        x = (x - f * fp_inv) % pk_next
        pk = pk_next
    return x

def crt_combine(r1, m1, r2, m2):
    """CRT for coprime moduli."""
    # r = r1 + m1 * t, t = (r2 - r1) * m1^{-1} mod m2
    inv = pow(m1 % m2, -1, m2)
    t = ((r2 - r1) * inv) % m2
    return (r1 + m1 * t) % (m1 * m2), m1 * m2

def roots_for_d(prime_factors):
    """prime_factors: list of (p, e) with p == 1 mod 4 (and possibly p=2 with e=1).
       Return all roots x mod d = prod p^e of x^2 = -1 mod d."""
    # For p = 2, root mod 2 is x = 1, mod 2 only (e=1 max because 2^2 = 4, x^2=-1 mod 4 has no soln).
    # For p == 1 mod 4, exactly 2 roots mod p^e via Hensel.
    moduli_roots = []  # list of (modulus, [roots])
    for (p, e) in prime_factors:
        if p == 2:
            assert e == 1
            moduli_roots.append((2, [1]))
        else:
            x_p = tonelli_minus1(p)
            x_pk = hensel_minus1_pk(p, e, x_p)
            mod_pk = p ** e
            moduli_roots.append((mod_pk, [x_pk, mod_pk - x_pk]))
    # CRT-combine all moduli to get all roots mod d
    if not moduli_roots:
        return [], 1
    # Start with first
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
    """N_d(N) = sum_{x in roots} #{n <= N, n >= 1, n == x mod d}.
       For root x in [0, d-1], the smallest positive n is x if x >= 1 else x+d=d.
       Then count is floor((N - x_pos) / d) + 1 if x_pos <= N else 0."""
    total = 0
    for x in roots:
        x_pos = x if x >= 1 else d  # if x == 0, smallest positive n is d
        # But x = 0 doesn't satisfy x^2 = -1 mod d for d > 1, so x >= 1 always when d > 1
        if x_pos <= N:
            total += (N - x_pos) // d + 1
    return total

def run(N, X_max=None, primes_cap=None):
    """Compute B_3(N) and its dyadic decomposition signed by (positive, negative)
       contributions per dyadic window of d."""
    if X_max is None:
        X_max = N * N + 1
    if primes_cap is None:
        primes_cap = X_max
    print(f"\n=== N = {N}, X_max = {X_max} ===")
    t0 = time.time()
    sp = split_primes_up_to(primes_cap)
    print(f"  split primes <= {primes_cap}: {len(sp)} ({time.time()-t0:.1f}s)", flush=True)

    # Caches: tonelli for each split prime; that's once per p.
    # We'll compute roots on demand inside the recursion; cache (p, e) -> root mod p^e.
    root_cache = {}  # (p, e) -> root mod p^e
    def get_pk_root(p, e):
        if (p, e) in root_cache:
            return root_cache[(p, e)]
        if e == 1:
            x = tonelli_minus1(p)
        else:
            x_p = tonelli_minus1(p) if (p, 1) not in root_cache else root_cache[(p, 1)]
            root_cache[(p, 1)] = x_p
            x = hensel_minus1_pk(p, e, x_p)
        root_cache[(p, e)] = x
        return x

    # Enumeration: pick subset of split primes with multiplicities.
    # For each visited m, we can produce d = m or d = 2m.
    # Track running prime_factors stack so we can compute roots.
    sys.setrecursionlimit(10**6)

    # Bucket: dyadic windows of d, indexed by floor(log2(d))
    # B_3 = sum of contrib(d) over all supported d
    # contrib(d) = 2^omega(d) * (N_d(N) - rho(d) * N / d)
    pos_bucket = defaultdict(Fraction)  # window -> sum of positive contributions
    neg_bucket = defaultdict(Fraction)  # window -> sum of negative contributions (signed, negative)
    count_bucket_pos = defaultdict(int)
    count_bucket_neg = defaultdict(int)
    count_bucket_zero = defaultdict(int)

    # Track top contributors (largest |contrib|)
    top_contributors = []  # heap of (|contrib|, d, contrib)

    total = Fraction(0)
    visited = [0]

    def process(d, prime_factors, fw, omega):
        """d: divisor; fw = 4^|odd_factors| (= 2^omega for d odd); omega = number of distinct prime factors;
           contrib = 2^omega * delta_d.
           Note 2^omega(d) for d = 2 * m_odd is 2^(1 + omega(m_odd)).
           fw passed in is 2^omega(d).  (caller passes 1 for d=1, 2 for d=p in split, etc.)"""
        if d > X_max:
            return
        roots, mod = roots_for_d(prime_factors) if prime_factors else ([], 1)
        if mod != d:
            # something off
            raise RuntimeError(f"d={d}, mod={mod}, factors={prime_factors}")
        rho = len(roots) if d > 1 else 1  # rho(1) = 1
        if d == 1:
            # delta_1 = N_1 - 1*N/1 = N - N = 0
            visited[0] += 1
            return
        Nd = Nd_from_roots(roots, d, N)
        delta = Fraction(Nd) - Fraction(rho) * Fraction(N, d)
        contrib = Fraction(fw) * delta
        nonlocal total
        total += contrib

        window = int(math.log2(d))  # floor(log2(d))
        if contrib > 0:
            pos_bucket[window] += contrib
            count_bucket_pos[window] += 1
        elif contrib < 0:
            neg_bucket[window] += contrib
            count_bucket_neg[window] += 1
        else:
            count_bucket_zero[window] += 1

        # track top 30 contributors by |contrib|
        c_abs = abs(contrib)
        if len(top_contributors) < 30:
            top_contributors.append((c_abs, d, contrib))
        else:
            mn_idx = min(range(len(top_contributors)), key=lambda i: top_contributors[i][0])
            if c_abs > top_contributors[mn_idx][0]:
                top_contributors[mn_idx] = (c_abs, d, contrib)

        visited[0] += 1
        if visited[0] % 200000 == 0:
            print(f"    visited {visited[0]} d, total so far {float(total):.4f} ({time.time()-t0:.1f}s)", flush=True)

    # DFS: choose split primes from sp, with multiplicities; for each m, also d=2m.
    def recurse(idx, m, prime_factors, omega_m):
        # process d = m (a in {0})
        process(m, prime_factors, 1 << omega_m, omega_m)
        # process d = 2m (a in {1})  — only when 2m <= X_max
        if 2 * m <= X_max:
            new_factors = [(2, 1)] + prime_factors
            process(2 * m, new_factors, 1 << (omega_m + 1), omega_m + 1)
        # extend with next split prime
        for j in range(idx, len(sp)):
            p = sp[j]
            if p * m > X_max:
                break
            mp = m * p
            e = 1
            while mp <= X_max:
                pf2 = prime_factors + [(p, e)]
                recurse(j + 1, mp, pf2, omega_m + 1)
                mp *= p
                e += 1
                if mp > X_max:
                    break

    print(f"  starting recursion ...", flush=True)
    recurse(0, 1, [], 0)
    print(f"  DONE: visited {visited[0]} supported d; B_3 = {float(total):.6f}; total time {time.time()-t0:.1f}s", flush=True)

    return {
        "N": N,
        "X_max": X_max,
        "B3_total": float(total),
        "B3_total_frac": total,
        "pos_bucket": {k: float(v) for k, v in pos_bucket.items()},
        "neg_bucket": {k: float(v) for k, v in neg_bucket.items()},
        "count_pos": dict(count_bucket_pos),
        "count_neg": dict(count_bucket_neg),
        "count_zero": dict(count_bucket_zero),
        "top_contributors": sorted([(float(c[0]), c[1], float(c[2])) for c in top_contributors],
                                    reverse=True),
        "visited": visited[0],
    }

def print_decomp(res):
    N = res["N"]
    print(f"\n--- N = {N} decomposition ---")
    print(f"B_3(N) = {res['B3_total']:.6f}")
    print(f"B_3(N)/N = {res['B3_total']/N:.6f}")
    windows = sorted(set(res["pos_bucket"]) | set(res["neg_bucket"]))
    print(f"\n  window k: d in [2^k, 2^(k+1))")
    print(f"{'k':>4} {'2^k':>14} {'pos sum':>14} {'neg sum':>14} {'net':>14} {'#pos':>8} {'#neg':>8} {'#zero':>8}")
    cum_net = 0.0
    cum_pos = 0.0
    cum_abs = 0.0
    for k in windows:
        pos = res["pos_bucket"].get(k, 0.0)
        neg = res["neg_bucket"].get(k, 0.0)
        net = pos + neg
        cum_net += net
        cum_pos += pos
        cum_abs += pos - neg  # pos - neg, since neg < 0
        cp = res["count_pos"].get(k, 0)
        cn = res["count_neg"].get(k, 0)
        cz = res["count_zero"].get(k, 0)
        print(f"{k:>4} {1<<k:>14} {pos:>14.4f} {neg:>14.4f} {net:>14.4f} {cp:>8} {cn:>8} {cz:>8}")
    print(f"\n  totals: pos sum = {cum_pos:.4f}, sum_abs = {cum_abs:.4f}, net = {cum_net:.4f}")
    print(f"  cancellation ratio: net / pos = {cum_net / cum_pos if cum_pos else 0:.4f}")
    print(f"  (1.0 means all contributions positive; 0.0 means perfect cancellation)")

    # Top contributors
    print(f"\n  Top 30 |contrib(d)|:")
    print(f"{'|contrib|':>14} {'d':>14} {'contrib':>14}")
    for (ac, d, c) in res["top_contributors"][:30]:
        print(f"{ac:>14.4f} {d:>14} {c:>+14.4f}")
    sum_top = sum(c for (_, _, c) in res["top_contributors"][:30])
    sum_top10 = sum(c for (_, _, c) in res["top_contributors"][:10])
    sum_top3 = sum(c for (_, _, c) in res["top_contributors"][:3])
    print(f"  net of top 30: {sum_top:+.4f} (frac of B_3: {sum_top/res['B3_total']:.4f})")
    print(f"  net of top 10: {sum_top10:+.4f} (frac of B_3: {sum_top10/res['B3_total']:.4f})")
    print(f"  net of top  3: {sum_top3:+.4f} (frac of B_3: {sum_top3/res['B3_total']:.4f})")


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [1000, 3000, 10000]
    expected_B3 = {1000: 336.00, 3000: 1556.66, 10000: 4740.21}
    results = {}
    for N in Ns:
        res = run(N)
        # Sanity check
        diff = res["B3_total"] - expected_B3[N]
        print(f"  >>> expected B_3({N}) = {expected_B3[N]:.4f}, got {res['B3_total']:.4f}, diff = {diff:.4f}")
        if abs(diff) > 0.01:
            print(f"  *** SANITY CHECK FAILED for N={N} ***")
        results[N] = res
        print_decomp(res)
