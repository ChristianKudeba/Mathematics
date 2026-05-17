"""
*** RETRACTION HEADER (2026-05-04 03:39 UTC) ***
The within-path empirical "rel std/mean = 0.205" computed by this script
should NOT be compared against the ENSEMBLE RW prediction 2/sqrt(3) = 1.155
that this script's docstring originally invoked. They measure different
statistics. The correct comparison is a Monte Carlo of within-path rel
std/mean values, done in V-rw-simulation.py — which gives 0.21-0.22 for
RW, statistically indistinguishable from the empirical 0.205.

See P12-V-cumulative-second-moment.md for the corrected analysis.
*** END RETRACTION ***

Re-run V analysis with dense sampling + theoretical comparison vs. a random-walk
null model.

Theoretical fact (computed by hand): if T were a Gaussian random walk with var
= sigma^2 * M (independent increments), then V(N) := sum_{M=1}^{N} T(M)^2 has
  E[V(N)] = sigma^2 * N(N+1)/2  ~  sigma^2 N^2 / 2
  var(V(N)) ~ sigma^4 * N^4 / 3
  => V(N)/N^2 has mean -> sigma^2/2, std -> sigma^2/sqrt(3).
  => relative std/mean -> 2/sqrt(3) ~ 1.15.

So even a perfect random walk has V/N^2 fluctuating at order of its mean!
This means the empirical-pinning strategy is methodologically obstructed — we
can't pin C* better than O(1) relative precision by examining V(N)/N^2 at any
finite N.

We test this by computing V(N)/N^2 on a dense grid in [N_max/4, N_max] and
reporting (mean, std).  If observed std is comparable to (2/sqrt(3)) * mean,
the random-walk null is consistent and the strategy is dead.  If observed
std is much smaller, T has more structure than a random walk and there's
hope.
"""

import math, time, os, pickle
from V_cumulative import compute_T_full, compute_V

def chi4(n):
    n = n & 3
    if n == 1: return 1
    if n == 3: return -1
    return 0

def main():
    N_max = int(os.environ.get('NMAX', '10000000'))
    print(f"=== V-fluctuation at N_max = {N_max} ===")
    Tcum = compute_T_full(N_max)
    K = len(Tcum) - 1
    V = compute_V(Tcum)
    print(f"V(N_max)/N_max^2 = {V[K]/(N_max*N_max):.6f}", flush=True)

    # Dense grid: N = step, 2*step, ..., N_max with step = N_max // 200.
    step = N_max // 200  # 200 sample points
    print(f"\nDense scan: V(N)/N^2 at N = step k for k=1..200 (step={step})")
    samples = []
    for j in range(1, 201):
        N = j * step
        k = N // 2
        if k <= 0 or k > K: continue
        samples.append((N, V[k]/(N*N)))
    # Print summary stats over the upper half (last 100 points).
    upper = [v for (n, v) in samples[100:]]
    if upper:
        m = sum(upper)/len(upper)
        v = sum((x-m)**2 for x in upper)/len(upper)
        s = math.sqrt(v)
        mn = min(upper); mx = max(upper)
        print(f"upper-half (N in [{samples[100][0]}, {samples[-1][0]}]):")
        print(f"  mean = {m:.5f}, std = {s:.5f}, min = {mn:.5f}, max = {mx:.5f}")
        print(f"  rel std/mean = {s/m:.3f}")
        print(f"  random-walk prediction: rel std/mean = 2/sqrt(3) = {2/math.sqrt(3):.3f}")

    # Show the trajectory at log-spaced N.
    print(f"\nV(N)/N^2 at log-spaced N:")
    for N in [10**3, 10**4, 10**5, 10**6, 10**7]:
        if N > N_max: continue
        k = N // 2
        if k > K: continue
        print(f"  N={N:>10d}: V/N^2 = {V[k]/(N*N):.5f}")

    # Compute a "running average" by averaging V(N)/N^2 over windows of N.
    # This approximates a "smoothed" V/N^2 estimator.
    # smooth(N0) := mean over 100 N values in [N0, 2N0] of V(N)/N^2.
    print(f"\nSmoothed V/N^2 (avg over 100 N-values in [N0, 2N0]):")
    print(f"{'N0':>10}  {'smooth':>10}  {'std':>10}")
    for N0 in [10**4, 5*10**4, 10**5, 5*10**5, 10**6, 2*10**6, 5*10**6]:
        if 2*N0 > N_max: continue
        Ns = [N0 + j*(N0//100) for j in range(100)]
        vals = []
        for N in Ns:
            k = N // 2
            if 1 <= k <= K:
                vals.append(V[k]/(N*N))
        if not vals: continue
        m = sum(vals)/len(vals)
        v = sum((x-m)**2 for x in vals)/len(vals)
        s = math.sqrt(v)
        print(f"{N0:>10d}  {m:>10.5f}  {s:>10.5f}")

    # Pickle a sparse Tcum at N grid for next session.
    out = '/home/user/mathAI/bot/scratch/Tcum-V.pkl'
    sparse = []
    for k in range(0, K+1, max(1, K // 5000)):
        sparse.append((2*k, Tcum[k], V[k]))
    with open(out, 'wb') as f:
        pickle.dump(sparse, f)
    print(f"\nSaved {len(sparse)} sparse (M, T, V) samples to {out}")

if __name__ == '__main__':
    main()
