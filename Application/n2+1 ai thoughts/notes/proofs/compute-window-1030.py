"""
Concretely: for each enumerable polynomial f, list the f-primes in window [10, 30]
and compare with the non-enumerable comparison polynomial g(n) = n^2 + 3.
Also: what's the smallest window length k such that every window of k consecutive
integers in [1, 30] contains an f-prime?
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

POLYS = [
    ("phi_0",    "n^2 + 1",    lambda n: n*n + 1),
    ("phi_1",    "n^2 + n + 1", lambda n: n*n + n + 1),
    ("psi_2",    "n^2 + 2n - 1", lambda n: n*n + 2*n - 1),
    ("phi_3",    "n^2 + 3n + 1", lambda n: n*n + 3*n + 1),
    ("g (n^2+3)","n^2 + 3 (NOT enumerable)", lambda n: n*n + 3),
    ("h (n^2+5)","n^2 + 5 (NOT enumerable)", lambda n: n*n + 5),
]

print("PRIMES IN WINDOW [10, 30] FOR EACH POLYNOMIAL")
print("=" * 70)
for name, formula, f in POLYS:
    print(f"\n  {name}: {formula}")
    primes_in_window = []
    for n in range(10, 31):
        v = abs(f(n))
        if isprime(v):
            primes_in_window.append((n, v))
    print(f"    Primes in [10, 30]: {primes_in_window}")
    print(f"    Count: {len(primes_in_window)}")

print("\n\nLARGEST CONSECUTIVE-COMPOSITE RUN IN [1, 100]")
print("=" * 70)
for name, formula, f in POLYS:
    print(f"\n  {name}: {formula}")
    composite_runs = []
    cur_run = 0
    cur_start = None
    for n in range(1, 101):
        v = abs(f(n))
        if isprime(v):
            if cur_run > 0:
                composite_runs.append((cur_start, cur_start + cur_run - 1, cur_run))
            cur_run = 0
            cur_start = None
        else:
            if cur_run == 0:
                cur_start = n
            cur_run += 1
    if cur_run > 0:
        composite_runs.append((cur_start, cur_start + cur_run - 1, cur_run))
    if composite_runs:
        max_run = max(composite_runs, key=lambda x: x[2])
        print(f"    Longest composite run: n in [{max_run[0]}, {max_run[1]}], length {max_run[2]}")
        print(f"    Implies: any window of length {max_run[2]+1} in [1, 100] contains a prime.")
        print(f"    Cannot improve (the composite run has length {max_run[2]}).")

print("\n\nSMALLEST WINDOW LENGTH k SUCH THAT EVERY [a, a+k-1] in [1, 100] HAS A PRIME")
print("=" * 70)
for name, formula, f in POLYS:
    primes = [n for n in range(1, 101) if isprime(abs(f(n)))]
    if len(primes) < 2:
        print(f"  {name}: not enough primes")
        continue
    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
    # also include initial gap
    if primes[0] > 1:
        gaps = [primes[0]] + gaps  # gap from 1 to first prime
    max_gap = max(gaps)
    print(f"  {name}: smallest k = {max_gap} (from gap structure)")
