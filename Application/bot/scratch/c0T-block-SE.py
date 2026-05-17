"""
Block-bootstrap SE for T(N)/N at N=1e7. Splits [1, 1e7] into 10 blocks of 1e6,
computes T per block, then standard SE of the block-means.

Re-runs the omega sieve (cheap at this scale).
"""
import math
import time
import sys
import numpy as np

sys.path.insert(0, "bot/scratch")
import importlib.util
spec = importlib.util.spec_from_file_location("c0T", "bot/scratch/c0T-N1e7-empirical.py")
mod = importlib.util.module_from_spec(spec)


def primes_up_to(M):
    sieve = np.ones(M + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(M ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = False
    return np.where(sieve)[0].astype(np.int64)


def sqrt_minus1_mod_p(p):
    if p == 2:
        return 1
    a = p - 1
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    Q, S = p - 1, 0
    while Q % 2 == 0:
        Q //= 2; S += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    M_ = S
    c = pow(z, Q, p)
    t = pow(a, Q, p)
    Rr = pow(a, (Q + 1) // 2, p)
    while t != 1:
        i = 0; temp = t
        while temp != 1:
            temp = (temp * temp) % p; i += 1
        b = pow(c, 1 << (M_ - i - 1), p)
        M_ = i; c = (b * b) % p
        t = (t * c) % p; Rr = (Rr * b) % p
    return Rr


def hensel_lift(r, pk_old, pk_new, p):
    r = int(r); pk_new = int(pk_new)
    f = (r * r + 1) % pk_new
    two_r = (2 * r) % pk_new
    inv = pow(two_r, -1, pk_new)
    return (r - f * inv) % pk_new


def main():
    N = 10**7
    print(f"Sieving omega for n <= {N}...", flush=True)
    t0 = time.time()
    primes = primes_up_to(N)
    mask = (primes == 2) | (primes % 4 == 1)
    split_primes = primes[mask].astype(int)
    roots_mod_p = {}
    for p in split_primes:
        if p == 2:
            roots_mod_p[2] = [1]
        else:
            r = sqrt_minus1_mod_p(int(p))
            roots_mod_p[int(p)] = [r, p - r]

    omega = np.zeros(N + 1, dtype=np.int32)
    n_arr = np.arange(0, N + 1, dtype=np.int64)
    residual = n_arr * n_arr + 1
    for p in split_primes:
        p_int = int(p)
        for r0 in roots_mod_p[p_int]:
            if r0 == 0:
                continue
            idx = np.arange(r0, N + 1, p_int)
            if len(idx) == 0:
                continue
            omega[idx] += 1
            residual[idx] //= p_int
            if p_int == 2:
                continue
            pk = p_int; r_curr = r0
            bound = N * N + 1
            while True:
                pk_new = pk * p_int
                if pk_new > bound:
                    break
                r_new = hensel_lift(r_curr, pk, pk_new, p_int)
                if r_new == 0:
                    r_new = pk_new
                if r_new > N:
                    break
                idx_k = np.arange(r_new, N + 1, pk_new)
                if len(idx_k) == 0:
                    break
                residual[idx_k] //= p_int
                pk = pk_new; r_curr = r_new
    omega[residual > 1] += 1
    omega[0] = 0
    print(f"  Sieve: {time.time()-t0:.1f}s", flush=True)

    f = (1 << omega.astype(np.int64))
    f[0] = 0  # exclude n=0

    # Block means: 10 blocks of 1e6, each runs from n in (k*1e6, (k+1)*1e6]
    block_size = 10**6
    n_blocks = 10
    block_T = np.zeros(n_blocks, dtype=np.float64)
    for k in range(n_blocks):
        lo = k * block_size + 1
        hi = (k + 1) * block_size
        block_T[k] = f[lo:hi+1].sum()
    block_means = block_T / block_size

    # Note: each block has different mean (T grows with log N). To assess
    # SE of c_0^T(10^7), we need to be careful — the block means encode the
    # log-scale signal too. Cleanest: compute c_0^T(N_block) per block where
    # N_block = (k+1) * 1e6 (cumulative).
    cum_T = np.cumsum(f)
    H1 = 0.552674
    R = math.pi / 4.0
    C1 = R * 2 * H1
    decade_results = []
    for k in range(n_blocks):
        N_block = (k + 1) * block_size
        T_b = int(cum_T[N_block])
        c0T_b = T_b / float(N_block) - C1 * math.log(N_block)
        decade_results.append((N_block, T_b, c0T_b))

    print(f"\n=== Cumulative c_0^T(N) at decadal-block boundaries (N = k*1e6, k=1..10) ===", flush=True)
    for N_block, T_b, c0T_b in decade_results:
        print(f"  N={N_block:>10d}  T={T_b:>14d}  c_0^T(N) = {c0T_b:+.6f}", flush=True)

    # Block-bootstrap SE: random subsamples of 5 blocks, compute T over union scaled.
    # Cleaner alternative: per-block residual c_0^T_block = T_block / 1e6 - c_1 log(1e6 * (k+0.5)/1)
    # where the log is centered at the block midpoint — captures the "local c_0^T" with reduced
    # log-trend bias. We'll compute SE of these.
    block_c0T = np.zeros(n_blocks)
    for k in range(n_blocks):
        # block_T[k] is the sum over n in (k*1e6, (k+1)*1e6]
        # mean over that range of f(n) ≈ c_1 (log n) + c_0^T at midpoint
        # midpoint log: log((k+0.5) * 1e6)
        n_mid = (k + 0.5) * block_size
        block_c0T[k] = block_means[k] - C1 * math.log(n_mid)

    block_c0T_mean = block_c0T.mean()
    block_c0T_std = block_c0T.std(ddof=1)
    SE_block_mean = block_c0T_std / math.sqrt(n_blocks)
    print(f"\n=== Per-block c_0^T at block midpoint (block size 1e6) ===", flush=True)
    for k, v in enumerate(block_c0T):
        print(f"  Block {k+1}: midpoint N={int((k+0.5)*block_size)}, c_0^T = {v:+.6f}", flush=True)
    print(f"  Mean:    {block_c0T_mean:+.6f}", flush=True)
    print(f"  Std:     {block_c0T_std:.6f}", flush=True)
    print(f"  SE(mean): {SE_block_mean:.6f}", flush=True)

    # Actual c_0^T(1e7) for reference
    c0T_1e7 = cum_T[N] / float(N) - C1 * math.log(N)
    print(f"  Direct c_0^T(1e7) = {c0T_1e7:+.6f}", flush=True)
    print(f"  Predicted: 0.987322", flush=True)
    print(f"  Gap: {c0T_1e7 - 0.987322:+.6f}  ({(c0T_1e7 - 0.987322)/SE_block_mean:+.2f}σ via block SE)", flush=True)


if __name__ == "__main__":
    main()
