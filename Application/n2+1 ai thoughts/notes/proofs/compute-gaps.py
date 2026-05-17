"""
Push the tier mechanism much further and examine how the maximum gap
G_f(N) grows with N (the forced range).
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
    if N < 2: return []
    sieve = [True] * (N+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5)+1):
        if sieve[i]:
            for j in range(i*i, N+1, i):
                sieve[j] = False
    return [i for i in range(N+1) if sieve[i]]

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

def primes_dividing_f(f, n_bound, p_bound):
    seen = set()
    PRIMES = primes_up_to(p_bound)
    for n in range(1, n_bound + 1):
        v = abs(f(n))
        for p in PRIMES:
            if p*p > v: break
            if v % p == 0:
                seen.add(p)
                # also any p that equals v itself
        if isprime(v) and v <= p_bound:
            seen.add(v)
    return sorted(seen)

def forced_prime_range(f, primes_list, n_max):
    """Return sorted list of n in [1, n_max] that are forced-prime by the tier mechanism."""
    forced = set()
    for k in range(len(primes_list)):
        p_next = primes_list[k]
        threshold = p_next * p_next
        excluded = primes_list[:k]
        for n in range(1, n_max + 1):
            v = abs(f(n))
            if v >= threshold: continue
            if any(v % p == 0 for p in excluded): continue
            forced.add(n)
    return sorted(forced)

# Push much further
print("Computing forced-prime sets up to large N for each enumerable polynomial.")
print("="*78)

for name, formula, f in POLYS:
    print(f"\n----- {name}(n) = {formula} -----")
    # compute primes dividing f up to a large bound
    PMAX = 5000
    NMAX_SEARCH = 10000
    primes_list = primes_dividing_f(f, n_bound=NMAX_SEARCH, p_bound=PMAX)
    print(f"  Primes p <= {PMAX} dividing f(n) for some n <= {NMAX_SEARCH}: {len(primes_list)} primes")

    # Forced-prime: must have f(n) < primes_list[-1]^2 to be in any tier
    n_limit = int((primes_list[-1] ** 2) ** 0.5)  # crude: f(n) ~ n^2, so n ~ p_max
    print(f"  Crude n-limit from largest prime considered: {n_limit}")

    forced = forced_prime_range(f, primes_list, n_max=n_limit)
    if not forced:
        continue

    # Gap analysis with rolling-max-gap
    gaps = [forced[i+1] - forced[i] for i in range(len(forced)-1)]
    rolling_max_gap = []
    cur_max = 0
    for g in gaps:
        cur_max = max(cur_max, g)
        rolling_max_gap.append(cur_max)

    last_n = forced[-1]
    print(f"  Last forced-prime n: {last_n}")
    print(f"  Total forced-prime count: {len(forced)}")
    print(f"  Max gap overall: {max(gaps) if gaps else 0}")

    # Sample of gap growth
    print(f"  Rolling max gap at various positions:")
    for thresh in [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]:
        idx = max(i for i in range(len(forced)) if forced[i] <= thresh) if any(n <= thresh for n in forced) else -1
        if idx >= 1:
            mg = max(forced[i+1]-forced[i] for i in range(idx))
            print(f"    n <= {thresh:5d}: max gap = {mg:3d}, count = {idx+1}, n_last = {forced[idx]}")

    # Sanity: are ALL primes-of-f in [1, last_n] forced?
    all_primes_in_range = [n for n in range(1, last_n+1) if isprime(abs(f(n)))]
    forced_set = set(forced)
    missed = [n for n in all_primes_in_range if n not in forced_set]
    if missed:
        print(f"  !!! MISSED primes (not forced by tier mechanism): {missed[:20]}")
        print(f"  Note: these are real primes, but the tier mechanism does not 'force' them")
    else:
        print(f"  All actual prime-f(n) in [1, {last_n}] are forced-prime by the tier mechanism.")
