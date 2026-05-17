"""
Monte Carlo: simulate Gaussian RWs and compute the WITHIN-PATH std of
V(N)/N^2 across N (matching the empirical statistic).

This is the RIGHT null comparison.  The previous derivation gave
ENSEMBLE std at fixed N, which is conceptually different.

For each path:
  - simulate epsilon_1, ..., epsilon_K iid N(0, sigma^2)
  - T_M = cumsum(epsilon)
  - V_M = cumsum(T_M^2)
  - sample V(N)/N^2 at N in [K/2, K] dense
  - compute within-path std

Average within-path std across paths gives the "typical within-path std" for
a single RW realization.

Run: choose sigma^2 = 0.4 (matching the empirical V/N^2 ~ 0.2 mean).
"""

import numpy as np
import time
import math

def simulate_one(K, sigma2, rng):
    eps = rng.normal(0.0, math.sqrt(sigma2), size=K).astype(np.float64)
    T = np.cumsum(eps)
    V = np.cumsum(T*T)
    return T, V

def main():
    sigma2 = 0.4   # to match empirical V/N^2 ~ 0.2 = sigma^2/2
    K = 1_000_000  # path length
    nP = 50        # number of paths
    print(f"=== RW null: sigma^2 = {sigma2}, K = {K}, nP = {nP} ===")

    rng = np.random.default_rng(seed=42)
    within_stds = []
    within_means = []
    final_VK = []
    t0 = time.time()
    for ip in range(nP):
        T, V = simulate_one(K, sigma2, rng)
        # Sample V(N)/N^2 at 100 equally-spaced N in [K/2, K].
        Ns = np.linspace(K // 2, K, 100, dtype=int)
        ratios = V[Ns - 1] / (Ns.astype(np.float64))**2
        within_stds.append(ratios.std())
        within_means.append(ratios.mean())
        final_VK.append(V[K-1] / (K*K))
        if (ip+1) % 10 == 0:
            print(f"  path {ip+1}/{nP} done, t={time.time()-t0:.1f}s", flush=True)

    within_stds = np.array(within_stds)
    within_means = np.array(within_means)
    final_VK = np.array(final_VK)

    print(f"\nResults across {nP} paths (each K={K}):")
    print(f"  V(K)/K^2: mean = {final_VK.mean():.5f}, std = {final_VK.std():.5f}")
    print(f"    [theoretical: mean = sigma^2/2 = {sigma2/2:.5f}, std = sigma^2/sqrt(3) = {sigma2/math.sqrt(3):.5f}]")
    print(f"  Within-path mean of V(N)/N^2 over [K/2,K]: avg = {within_means.mean():.5f}")
    print(f"  Within-path STD of V(N)/N^2 over [K/2,K]: avg = {within_stds.mean():.5f}, std = {within_stds.std():.5f}")
    print(f"  Within-path REL STD/MEAN: avg = {(within_stds/within_means).mean():.4f}, std = {(within_stds/within_means).std():.4f}")
    print(f"\n  *** EMPIRICAL (T sieve, single 'path' over N in [5e6,1e7]) ***")
    print(f"  rel std/mean = 0.205")

    # Also compute at K = 5_000_000 (matches empirical N range)
    print(f"\n--- Repeating at K = 5_000_000 with 10 paths (slow) ---")
    K2 = 5_000_000
    within_stds2 = []
    within_means2 = []
    nP2 = 10
    rng2 = np.random.default_rng(seed=43)
    for ip in range(nP2):
        T, V = simulate_one(K2, sigma2, rng2)
        Ns = np.linspace(K2 // 2, K2, 100, dtype=int)
        ratios = V[Ns - 1] / (Ns.astype(np.float64))**2
        within_stds2.append(ratios.std())
        within_means2.append(ratios.mean())
        if (ip+1) % 2 == 0:
            print(f"  path {ip+1}/{nP2} done, t={time.time()-t0:.1f}s", flush=True)
    within_stds2 = np.array(within_stds2)
    within_means2 = np.array(within_means2)
    print(f"\n  K={K2}: within-path REL STD/MEAN: avg = {(within_stds2/within_means2).mean():.4f}, std = {(within_stds2/within_means2).std():.4f}")

if __name__ == '__main__':
    main()
