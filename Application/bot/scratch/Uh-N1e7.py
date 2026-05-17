"""Confirm |U_1(N)| scales linearly with N for small h."""
import math, time, sys
import numpy as np
sys.path.insert(0, "bot/scratch")
exec(open("bot/scratch/Uh-vs-Th-empirical.py").read().split('if __name__')[0])

N = int(1e7)
t0 = time.time()
spf = smallest_prime_factor(N)
print(f"# SPF sieve in {time.time()-t0:.1f}s", file=sys.stderr)

h_list = [1, 2, 5, 10, 100, 1000]
two_pi = 2*math.pi
U = {h: 0.0+0.0j for h in h_list}
t1 = time.time()
for e in range(2, N+1):
    pf = factor_sf_good(e, spf)
    if pf is None: continue
    Nmod = N % e
    for h in h_list:
        ang = two_pi * (h * Nmod % e) / e
        U[h] += complex(math.cos(ang), math.sin(ang))
print(f"# U sweep over {len(h_list)} h in {time.time()-t1:.1f}s", file=sys.stderr)

sqrtN = math.sqrt(N); print(f"\n# N = {N}, sqrt(N) = {sqrtN:.1f}")
print(f"{'h':>6} | {'|U_h|':>13} | {'|U_h|/N':>10} | {'|U_h|/sqrtN':>12}")
print("-"*60)
for h in h_list:
    aU = abs(U[h])
    print(f"{h:>6} | {aU:>13.2f} | {aU/N:>10.5f} | {aU/sqrtN:>12.4f}")
