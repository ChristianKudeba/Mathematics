"""Sweep |U_h(N)| across h to characterize crossover from N-regime to sqrt(N)-regime."""
import math, time, sys
import numpy as np
sys.path.insert(0, "bot/scratch")
exec(open("bot/scratch/Uh-vs-Th-empirical.py").read().split('if __name__')[0])

N = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e6)

t0 = time.time()
spf = smallest_prime_factor(N)
root_cache = {}
is_prime = (spf == np.arange(N + 1, dtype=np.int64))
for p in range(2, N + 1):
    if is_prime[p] and (p == 2 or p % 4 == 1):
        root_cache[p] = find_root_mod_p(p)
print(f"# Setup in {time.time()-t0:.1f}s", file=sys.stderr)

# Sweep h: 1 to 50 to see crossover
h_list = [1,2,3,5,7,10,15,20,30,50,75,100,150,300,500,1000,3000,10000]

# Compute U_h only (faster) — trim T_h calc
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
print(f"{'h':>6} | {'|U_h|':>11} | {'|U_h|/N':>10} | {'|U_h|/sqrtN':>12} | {'|U_h|*sqrt(h)/N':>15} | {'|U_h|/sqrt(N/h)':>16}")
print("-"*94)
for h in h_list:
    aU = abs(U[h])
    print(f"{h:>6} | {aU:>11.2f} | {aU/N:>10.5f} | {aU/sqrtN:>12.4f} | {aU*math.sqrt(h)/N:>15.5f} | {aU/math.sqrt(N/h):>16.4f}")
