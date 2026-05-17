"""
Compute forced-prime tiers for the four enumerable polynomials f
(those of Shakov's classification: phi_0, phi_1, psi_2, phi_3).

For each enumerable f, define:
  p_1 < p_2 < ... = the increasing sequence of primes p such that
  p | f(n) for some n in N.

THEOREM (proved below): any n satisfying:
  (a) f(n) < p_{k+1}^2
  (b) p_i does not divide f(n) for i = 1, ..., k
is FORCED to have f(n) prime, since any nontrivial divisor would have to be >= p_{k+1},
forcing a factorization with both factors >= p_{k+1}, hence f(n) >= p_{k+1}^2.

This generalizes B8's lemma (k=0) and P2's second-tier (k=1) to arbitrary tiers.
"""

def isprime(n):
    n = abs(n)
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    i = 3
    while i*i <= n:
        if n % i == 0: return False
        i += 2
    return True

def primes_up_to(N):
    out = []
    for k in range(2, N+1):
        if isprime(k): out.append(k)
    return out

def phi0(n): return n*n + 1
def phi1(n): return n*n + n + 1
def psi2(n): return n*n + 2*n - 1
def phi3(n): return n*n + 3*n + 1

POLYS = [
    ("phi_0", "n^2 + 1",       phi0),
    ("phi_1", "n^2 + n + 1",   phi1),
    ("psi_2", "n^2 + 2n - 1",  psi2),
    ("phi_3", "n^2 + 3n + 1",  phi3),
]

def primes_dividing_f(f, n_bound=2000, p_bound=300):
    """Return sorted list of primes p <= p_bound that divide f(n) for some 1 <= n <= n_bound."""
    seen = set()
    PRIMES = primes_up_to(p_bound)
    for n in range(1, n_bound + 1):
        v = abs(f(n))
        for p in PRIMES:
            if v % p == 0:
                seen.add(p)
    return sorted(seen)

def forced_primes_at_tier(f, primes_list, k, n_max=300):
    """Tier k: n in [1, n_max] s.t. (a) f(n) < primes_list[k]^2, (b) no p in primes_list[:k] divides f(n)."""
    if k >= len(primes_list):
        return []
    p_next = primes_list[k]
    threshold = p_next * p_next
    excluded_primes = primes_list[:k]
    out = []
    for n in range(1, n_max + 1):
        v = abs(f(n))
        if v >= threshold: continue
        if any(v % p == 0 for p in excluded_primes): continue
        out.append(n)
    return out

print("="*78)
print("FORCED-PRIME TIERS FOR THE FOUR ENUMERABLE POLYNOMIALS")
print("="*78)

for name, formula, f in POLYS:
    print(f"\n----- {name}(n) = {formula} -----")
    primes_list = primes_dividing_f(f, n_bound=2000, p_bound=300)
    print(f"  Primes p <= 300 dividing f(n) for some n <= 2000:")
    print(f"    {primes_list}")

    print(f"\n  Tier-by-tier forced primes:")
    cumulative = set()
    for k in range(len(primes_list)):
        ns = forced_primes_at_tier(f, primes_list, k, n_max=500)
        new = sorted(set(ns) - cumulative)
        cumulative |= set(ns)
        if new and k < 12:
            p_next = primes_list[k]
            excluded = primes_list[:k]
            print(f"    Tier {k}: exclude {excluded}, threshold f(n) < {p_next}^2 = {p_next*p_next}")
            print(f"             new forced n: {new}")

    forced = sorted(cumulative)
    print(f"\n  TOTAL forced n with f(n) prime: {forced[:30]}{'...' if len(forced)>30 else ''}")
    print(f"  Count of forced-prime n's (n <= 500): {len(forced)}")

    # Sanity
    bad = [(n, abs(f(n))) for n in forced if not isprime(abs(f(n)))]
    if bad: print(f"  !!! BAD: {bad}")

    # Compare with all primes in [1, max(forced)]
    if forced:
        m = max(forced)
        all_primes_n = [n for n in range(1, m+1) if isprime(abs(f(n)))]
        missed = [n for n in all_primes_n if n not in cumulative]
        print(f"  Actual prime f(n) in [1, {m}]: {len(all_primes_n)} values")
        print(f"  Of these, forced: {len(cumulative & set(all_primes_n))}, NOT-forced (must be checked): {len(missed)}")
        if missed[:10]:
            print(f"  First few not-forced primes: {missed[:10]}")

    # Gap analysis
    if len(forced) >= 2:
        gaps = [forced[i+1] - forced[i] for i in range(len(forced)-1)]
        # Find n_max such that EVERY window [n, n+k-1] contained in [1, n_max+k-1]
        # contains a forced-prime, where k = max gap
        max_gap = max(gaps)
        last_forced = max(forced)
        print(f"  Max gap between forced-prime n's: {max_gap}")
        print(f"  Last forced-prime n: {last_forced}")
        print(f"  ==> THEOREM (this f): every window of {max_gap} consecutive n's in [1, {last_forced}]")
        print(f"      contains at least one n with f(n) FORCED-prime.")
