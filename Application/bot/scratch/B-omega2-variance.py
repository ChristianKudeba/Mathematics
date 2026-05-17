"""
Empirical variance of b(n) restricted to omega(q) = 2 events.

For sampling-noise SE on the omega(q)=2 rate at N = 10^6, 10^7.
Bootstrap-block estimate of SE accounting for AP correlation
(use first-half / second-half split of the n range and look at
disagreement between halves as a proxy for total SE).

Run as: python B-omega2-variance.py 10000000
"""

import math
import sys
import time
import numpy as np

# Re-use sqrt_minus1 and Hensel from B-fast-sieve via small reimpl.
def primes_up_to(M):
    if M < 2:
        return np.array([], dtype=np.int64)
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
        Q //= 2
        S += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    M_ = S
    c = pow(z, Q, p)
    t = pow(a, Q, p)
    R = pow(a, (Q + 1) // 2, p)
    while t != 1:
        i = 0
        temp = t
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
        b = pow(c, 1 << (M_ - i - 1), p)
        M_ = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p
    return R


def hensel_lift(r, pk_old, pk_new, p):
    r = int(r)
    pk_new = int(pk_new)
    f = (r * r + 1) % pk_new
    two_r = (2 * r) % pk_new
    inv = pow(two_r, -1, pk_new)
    return (r - f * inv) % pk_new


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    print(f"N = {N}", flush=True)
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
    is_nsf = np.zeros(N + 1, dtype=bool)

    t0 = time.time()
    for p in split_primes:
        p_int = int(p)
        for r0 in roots_mod_p[p_int]:
            if r0 == 0:
                continue
            idx = np.arange(r0, N + 1, p_int)
            if len(idx) == 0:
                continue
            omega[idx] += 1
            if p_int == 2:
                continue
            pk = p_int
            r_curr = r0
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
                is_nsf[idx_k] = True
                pk = pk_new
                r_curr = r_new

    n_arr = np.arange(0, N + 1, dtype=np.int64)
    residual = n_arr * n_arr + 1
    for p in split_primes:
        p_int = int(p)
        for r0 in roots_mod_p[p_int]:
            if r0 == 0:
                continue
            pk = p_int
            r_curr = r0
            start = r_curr
            if start > N:
                continue
            if p_int == 2:
                idx = np.arange(start, N + 1, pk)
                if len(idx) > 0:
                    residual[idx] //= 2
                continue
            bound = N * N + 1
            while True:
                idx = np.arange(start, N + 1, pk)
                if len(idx) == 0:
                    break
                div_mask = (residual[idx] % p_int == 0)
                if not np.any(div_mask):
                    break
                div_idx = idx[div_mask]
                residual[div_idx] //= p_int
                pk_new = pk * p_int
                if pk_new > bound:
                    break
                r_new = hensel_lift(r_curr, pk, pk_new, p_int)
                if r_new == 0:
                    r_new = pk_new
                if r_new > N:
                    break
                pk = pk_new
                r_curr = r_new
                start = r_new
    has_large = residual > 1
    has_large[0] = False
    omega[has_large] += 1
    print(f"  Sieve: {time.time()-t0:.1f}s", flush=True)

    nsf_indices = np.where(is_nsf)[0]
    omega_nsf = omega[nsf_indices].astype(np.int64)
    total_entries = omega_nsf.sum()
    primes_flat = np.zeros(total_entries, dtype=np.int64)
    exps_flat = np.zeros(total_entries, dtype=np.int8)
    offsets = np.zeros(len(nsf_indices) + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(omega_nsf)
    write_ptr = offsets[:-1].copy()
    nsf_pos = np.full(N + 1, -1, dtype=np.int64)
    nsf_pos[nsf_indices] = np.arange(len(nsf_indices))

    t0 = time.time()
    for p in split_primes:
        p_int = int(p)
        for r0 in roots_mod_p[p_int]:
            if r0 == 0:
                continue
            idx = np.arange(r0, N + 1, p_int)
            if len(idx) == 0:
                continue
            idx_nsf_mask = is_nsf[idx]
            idx_nsf = idx[idx_nsf_mask]
            if len(idx_nsf) == 0:
                continue
            positions = nsf_pos[idx_nsf]
            wp = write_ptr[positions]
            primes_flat[wp] = p_int
            exps_flat[wp] = 1
            write_ptr[positions] += 1
            if p_int == 2:
                continue
            pk = p_int
            r_curr = r0
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
                positions_k = nsf_pos[idx_k]
                wp_k = write_ptr[positions_k] - 1
                exps_flat[wp_k] += 1
                pk = pk_new
                r_curr = r_new
    nsf_with_large = is_nsf & has_large
    idx_large = np.where(nsf_with_large)[0]
    if len(idx_large) > 0:
        positions_large = nsf_pos[idx_large]
        wp_large = write_ptr[positions_large]
        primes_flat[wp_large] = residual[idx_large]
        exps_flat[wp_large] = 1
        write_ptr[positions_large] += 1
    print(f"  Factor list: {time.time()-t0:.1f}s", flush=True)

    # Pass 3: compute b(n) per omega(q) class, retain the b values for omega=2.
    t0 = time.time()
    primes_flat_py = primes_flat.tolist()
    exps_flat_py = exps_flat.tolist()
    offsets_py = offsets.tolist()
    nsf_indices_py = nsf_indices.tolist()

    b_vals_omega2 = []  # list of b(n) for n with omega(q)=2
    n_idx_omega2 = []   # corresponding n indices

    for i in range(len(nsf_indices_py)):
        n = nsf_indices_py[i]
        start = offsets_py[i]
        end = offsets_py[i + 1]
        primes_n = primes_flat_py[start:end]
        exps_n = exps_flat_py[start:end]
        rad = 1
        for p in primes_n:
            rad *= p
        omega_q = sum(1 for e in exps_n if e >= 2)
        if omega_q != 2:
            continue
        divisors = [1]
        for p in primes_n:
            divisors = divisors + [d * p for d in divisors]
        bn = 0
        for e in divisors:
            if e * e > rad and e <= n:
                bn += 1
        b_vals_omega2.append(bn)
        n_idx_omega2.append(n)
    print(f"  Pass 3: {time.time()-t0:.1f}s", flush=True)

    arr = np.array(b_vals_omega2, dtype=np.int64)
    n_arr_o2 = np.array(n_idx_omega2, dtype=np.int64)
    Nf = float(N)
    print()
    print(f"  count of omega(q)=2 events: {len(arr)}")
    print(f"  sum b: {arr.sum()}")
    print(f"  rate (sum b)/N = {arr.sum()/Nf:.7f}")
    print(f"  per-event mean b = {arr.mean():.4f}")
    print(f"  per-event std  b = {arr.std(ddof=1):.4f}")
    print(f"  per-event var  b = {arr.var(ddof=1):.4f}")
    print(f"  max b at omega=2 event = {arr.max()}")
    print()
    # i.i.d. SE of (sum b)/N treating per-event b as i.i.d.
    se_iid = np.sqrt(len(arr) * arr.var(ddof=1)) / Nf
    print(f"  SE on rate via i.i.d. assumption = sqrt(K * var)/N = {se_iid:.7f}")
    # The events are not independent (AP correlation), so this is a lower bound.

    # Half-split estimate: divide n-range in two equal halves, compare half-rates
    half = N // 2
    mask_lo = n_arr_o2 <= half
    rate_lo = arr[mask_lo].sum() / float(half)
    rate_hi = arr[~mask_lo].sum() / float(N - half)
    print(f"  half-split rates: lo={rate_lo:.7f}, hi={rate_hi:.7f}, diff={abs(rate_lo-rate_hi):.7f}")
    # SE on overall rate from half-split: |rate_lo - rate_hi|/2 is a finite-difference
    # standard-error estimate (like a 2-sample bootstrap with k=2).
    # Actually for two independent halves of the same size, SE on the full rate is
    # sqrt(var(lo, hi))/2 ~ |lo-hi|/(2*sqrt(2)).
    se_halfsplit = abs(rate_lo - rate_hi) / (2 * math.sqrt(2))
    print(f"  SE estimate from half-split (lower bound): {se_halfsplit:.7f}")

    # Block-bootstrap: 10 blocks of N/10 each; estimate SE on rate
    n_blocks = 10
    block_size_N = N // n_blocks
    block_rates = []
    for k in range(n_blocks):
        lo = k * block_size_N
        hi = (k + 1) * block_size_N
        mask = (n_arr_o2 > lo) & (n_arr_o2 <= hi)
        block_rates.append(arr[mask].sum() / float(block_size_N))
    block_rates = np.array(block_rates)
    se_blocks = block_rates.std(ddof=1) / math.sqrt(n_blocks)
    print(f"  10-block rates: {[f'{r:.5f}' for r in block_rates]}")
    print(f"  block-bootstrap SE on overall rate: {se_blocks:.7f}")

    # Compare to predictions
    print()
    print(f"  predicted FULL : 0.0075381")
    print(f"  predicted LEAD : 0.0077141")


if __name__ == "__main__":
    main()
