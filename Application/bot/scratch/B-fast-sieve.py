"""
Fast vectorized sieve for B(N) := sum_{n <= N, n^2+1 non-sf} b(n),
where b(n) = #{e sf divisor of n^2+1 : sqrt(rad(n^2+1)) < e <= n}.

Pushes N from 10^6 (prev session, ~196s) to N = 10^7 (target).

Algorithm (two-pass):
1. SIEVE PASS. For each split prime p <= N, mark n in arithmetic progressions
   n = r mod p^k (r = Hensel lift of sqrt(-1) mod p^k). Track:
     - omega[n] = number of distinct split primes p with p | n^2+1
     - is_nsf[n] = whether n^2+1 has some v_p >= 2
     - residual[n] = n^2+1 stripped of all small primes; if > 1 at end, that's
       a single large prime > sqrt(N^2+1) factor.

2. FACTOR PASS for non-sf only. Build flat arrays primes_flat, exps_flat
   of total length sum_{nsf n} omega(n^2+1). Iterate split primes again;
   for each, write the prime + valuation into the per-n slot.

3. B(N) computation. For each non-sf n, enumerate 2^omega sf divisors; count
   those e with sqrt(rad) < e <= n.

Validation: matches B(N)/N from prev session at N = 10^4, 10^5, 10^6.
"""

import math
import time
import sys

import numpy as np


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
    """Return r with r^2 ≡ -1 mod p, p ≡ 1 mod 4."""
    if p == 2:
        return 1
    a = p - 1  # = -1 mod p
    # Tonelli–Shanks
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
    """Given r with r^2 + 1 ≡ 0 mod pk_old, find r_new with same mod pk_new (= pk_old * p).

    Newton: r_new = r - (r^2+1) / (2r) mod pk_new.
    """
    r = int(r)
    pk_new = int(pk_new)
    f = (r * r + 1) % pk_new
    two_r = (2 * r) % pk_new
    inv = pow(two_r, -1, pk_new)
    return (r - f * inv) % pk_new


def main():
    args = sys.argv[1:]
    if not args:
        targets = [10**6]
    else:
        targets = [int(x) for x in args]

    Nmax = max(targets)
    print(f"Sieving primes up to {Nmax}...", flush=True)
    t0 = time.time()
    primes = primes_up_to(Nmax)
    print(f"  {len(primes)} primes ({time.time()-t0:.1f}s)", flush=True)

    # Split primes (split in Z[i]): p == 2 or p ≡ 1 mod 4
    mask = (primes == 2) | (primes % 4 == 1)
    split_primes = primes[mask].astype(int)
    print(f"  {len(split_primes)} split primes (incl 2)", flush=True)

    # Precompute roots mod p for each split prime
    print(f"Computing roots mod p...", flush=True)
    t0 = time.time()
    roots_mod_p = {}
    for p in split_primes:
        if p == 2:
            roots_mod_p[2] = [1]
        else:
            r = sqrt_minus1_mod_p(int(p))
            roots_mod_p[int(p)] = [r, p - r]
    print(f"  done ({time.time()-t0:.1f}s)", flush=True)

    # ---- Run for each target N ----
    for N in targets:
        print(f"\n========== N = {N} ==========", flush=True)
        t_total = time.time()

        # Allocate state
        omega = np.zeros(N + 1, dtype=np.int32)
        is_nsf = np.zeros(N + 1, dtype=bool)
        # log_rad[n] (for non-sf n we'll compute exactly later via prime list,
        # but useful for diagnostics)

        # Pass 1: sieve omega and is_nsf using only the per-prime APs.
        # We don't need residual here since we only want omega and is_nsf at this stage.
        # Note: large prime > N case (n^2+1 having a single prime factor > N) is NOT
        # captured here — that adds 1 to omega only when residual > 1. We handle below.
        t0 = time.time()
        # First the small-prime sieve (p <= sqrt(N^2+1) = ~N)
        # But we restrict to split primes ≤ N (later: handle p² ≤ N²+1 for higher powers)
        # For omega: any prime p ≤ √(N²+1) ≈ N that divides n²+1 contributes.
        # For is_nsf: need v_p ≥ 2 for some p, i.e., p² | n²+1, p² ≤ n²+1 ≤ N²+1, so p ≤ N.
        for p in split_primes:
            p_int = int(p)
            for r0 in roots_mod_p[p_int]:
                if r0 == 0:
                    continue  # shouldn't happen for split p
                idx = np.arange(r0, N + 1, p_int)
                if len(idx) == 0:
                    continue
                omega[idx] += 1
                # Now lift to p^2 to mark is_nsf. Skip p=2 since v_2(n^2+1) ≤ 1 always.
                if p_int == 2:
                    continue
                pk = p_int
                r_curr = r0
                # Loop while p^k can divide some n^2+1 for n ≤ N (i.e., pk_new ≤ N^2+1).
                bound = N * N + 1
                while True:
                    pk_new = pk * p_int
                    if pk_new > bound:
                        break
                    r_new = hensel_lift(r_curr, pk, pk_new, p_int)
                    if r_new == 0:
                        r_new = pk_new
                    if r_new > N:
                        # No n ≤ N satisfies n ≡ r_new mod pk_new at this level;
                        # but lifting further may yield a smaller root? No,
                        # higher lifts are even larger mod values. Break.
                        break
                    idx_k = np.arange(r_new, N + 1, pk_new)
                    if len(idx_k) == 0:
                        break
                    is_nsf[idx_k] = True
                    pk = pk_new
                    r_curr = r_new
        print(f"  Pass 1 (omega + is_nsf sieve): {time.time()-t0:.1f}s", flush=True)

        # Find n with a single LARGE prime > N as a factor. We use residual approach.
        # residual[n] starts at n^2+1; after dividing out all small split primes
        # (with multiplicity), residual is either 1 or a prime > N (or 2*prime if
        # we missed something? No, we include 2). Actually, after dividing out all
        # small primes for which v_p ≥ 1, residual is a product of primes > N.
        # Since for p > N, p² > N² ≥ n² > n²+1 - 1, so v_p ≤ 1; and at most one
        # such prime can divide n²+1 (since p > N implies p² > n²+1).
        t0 = time.time()
        n_arr = np.arange(0, N + 1, dtype=np.int64)
        residual = n_arr * n_arr + 1  # int64; residual[0] = 1, used as placeholder
        for p in split_primes:
            p_int = int(p)
            for r0 in roots_mod_p[p_int]:
                if r0 == 0:
                    continue
                # Mark n ≡ r0 mod p, divide residual by p as long as p | residual
                pk = p_int
                r_curr = r0
                start = r_curr
                if start > N:
                    continue
                if p_int == 2:
                    # n odd: v_2(n²+1)=1 always; just divide once
                    idx = np.arange(start, N + 1, pk)
                    if len(idx) > 0:
                        residual[idx] //= 2
                    continue
                bound = N * N + 1
                while True:
                    idx = np.arange(start, N + 1, pk)
                    if len(idx) == 0:
                        break
                    # Use a check mask in case some entries already had p stripped
                    # (shouldn't happen since each n has unique r mod p).
                    div_mask = (residual[idx] % p_int == 0)
                    if not np.any(div_mask):
                        break
                    div_idx = idx[div_mask]
                    residual[div_idx] //= p_int
                    # Try to lift
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
        # Loop above stripped one factor of p per Hensel level. But for n with v_p = k,
        # we want to strip k factors. The Hensel-stratification handles that:
        # n ≡ r_p mod p (k times stripped: once at level 1, once at level 2, ..., once at level k).
        # Each level strips ONE factor at the matching index. So n with v_p = k has p stripped k times.
        # CHECK: at level 1, all n ≡ r mod p strip once.
        #        at level 2, all n ≡ r₂ mod p² strip once more.
        # Total v_p stripped = number of levels j such that n ≡ r_j mod p^j ≤ v_p(n²+1).
        # In fact n ≡ r_j mod p^j is equivalent to v_p(n²+1) ≥ j. So strips = v_p(n²+1) exactly.
        print(f"  Residual extraction: {time.time()-t0:.1f}s", flush=True)

        # Add 1 to omega[n] for n where residual > 1 (single large prime)
        has_large = residual > 1
        has_large[0] = False
        omega[has_large] += 1

        # Validation: ω(2²+1=5) should be 1, ω(7²+1=50=2·5²) should be 2
        if N >= 7:
            # Self-check
            print(f"  Self-check: omega[2]=1? {omega[2]==1}, omega[7]=2? {omega[7]==2}", flush=True)
            print(f"             is_nsf[7]=True? {is_nsf[7]}, is_nsf[2]=False? {not is_nsf[2]}", flush=True)
            print(f"             residual[2]=5 (large prime)? {residual[2]==5}", flush=True)

        # Density of non-sf
        nsf_count = is_nsf[1:].sum()
        print(f"  non-sf density = {nsf_count/N:.6f}", flush=True)

        # ---- Pass 2: build flat (prime, exp) lists for non-sf n ----
        t0 = time.time()
        nsf_indices = np.where(is_nsf)[0]
        omega_nsf = omega[nsf_indices].astype(np.int64)
        total_entries = omega_nsf.sum()
        print(f"  total prime-events for non-sf: {total_entries}", flush=True)
        primes_flat = np.zeros(total_entries, dtype=np.int64)
        exps_flat = np.zeros(total_entries, dtype=np.int8)
        offsets = np.zeros(len(nsf_indices) + 1, dtype=np.int64)
        offsets[1:] = np.cumsum(omega_nsf)
        write_ptr = offsets[:-1].copy()

        nsf_pos = np.full(N + 1, -1, dtype=np.int64)
        nsf_pos[nsf_indices] = np.arange(len(nsf_indices))

        for p in split_primes:
            p_int = int(p)
            for r0 in roots_mod_p[p_int]:
                if r0 == 0:
                    continue
                idx = np.arange(r0, N + 1, p_int)
                if len(idx) == 0:
                    continue
                # Restrict to non-sf
                idx_nsf_mask = is_nsf[idx]
                idx_nsf = idx[idx_nsf_mask]
                if len(idx_nsf) == 0:
                    continue
                positions = nsf_pos[idx_nsf]
                wp = write_ptr[positions]
                primes_flat[wp] = p_int
                exps_flat[wp] = 1  # at least v_p ≥ 1
                write_ptr[positions] += 1
                if p_int == 2:
                    continue  # no higher powers
                # Hensel-lift to higher levels and increment exps
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
                    # All n in idx_k are non-sf by definition (v_p ≥ 2 for some k ≥ 2)
                    positions_k = nsf_pos[idx_k]
                    # Find the entry index for prime p at each non-sf n: it's wp - 1
                    # since we just wrote it. wp was advanced, so the entry we wrote
                    # is at write_ptr[positions] - 1 just after the write above.
                    # But we re-look up: for each n in idx_k, the position in primes_flat
                    # corresponding to prime p is the most-recent-written entry, i.e.,
                    # write_ptr[positions_k] - 1 right now (since no other writes for this n
                    # have happened yet for this prime).
                    wp_k = write_ptr[positions_k] - 1
                    exps_flat[wp_k] += 1
                    pk = pk_new
                    r_curr = r_new

        # Add the large prime > N case (residual > 1) for non-sf n
        # Actually for non-sf n with residual > 1, the large prime contributes to omega
        # but does NOT contribute to non-sf-ness (v_large = 1). So we still need to
        # write it into primes_flat for the divisor enumeration.
        nsf_with_large = is_nsf & has_large
        idx_large = np.where(nsf_with_large)[0]
        if len(idx_large) > 0:
            positions_large = nsf_pos[idx_large]
            wp_large = write_ptr[positions_large]
            primes_flat[wp_large] = residual[idx_large]
            exps_flat[wp_large] = 1
            write_ptr[positions_large] += 1
        print(f"  Pass 2 (factor list build): {time.time()-t0:.1f}s", flush=True)

        # Sanity check: write_ptr should equal offsets[1:]
        assert np.all(write_ptr == offsets[1:]), "Write pointer mismatch!"

        # ---- Pass 3: enumerate sf divisors and compute B(N) ----
        t0 = time.time()
        total_B = 0
        log_n = np.log(np.maximum(nsf_indices, 1).astype(np.float64))
        # We'll loop in Python over non-sf n; should be ~10^6 at N=10^7.

        # Convert to Python lists for speed in the inner loop
        primes_flat_py = primes_flat.tolist()
        exps_flat_py = exps_flat.tolist()
        offsets_py = offsets.tolist()
        nsf_indices_py = nsf_indices.tolist()

        # Aggregate by omega(q) = number of distinct primes with v_p ≥ 2
        B_by_omega_q = {}  # omega(q) -> [count_n, sum_b]

        for i in range(len(nsf_indices_py)):
            n = nsf_indices_py[i]
            start = offsets_py[i]
            end = offsets_py[i + 1]
            primes_n = primes_flat_py[start:end]
            exps_n = exps_flat_py[start:end]
            # rad = product of distinct primes
            rad = 1
            for p in primes_n:
                rad *= p
            # Number of distinct primes with v_p ≥ 2 = ω(q) for the max sqfull divisor q
            omega_q = sum(1 for e in exps_n if e >= 2)
            # Enumerate sf divisors of n^2+1 = product of subsets of primes_n
            divisors = [1]
            for p in primes_n:
                divisors = divisors + [d * p for d in divisors]
            # Count sf divisors e with sqrt(rad) < e <= n.
            bn = 0
            for e in divisors:
                if e * e > rad and e <= n:
                    bn += 1
            total_B += bn
            if omega_q not in B_by_omega_q:
                B_by_omega_q[omega_q] = [0, 0]
            B_by_omega_q[omega_q][0] += 1
            B_by_omega_q[omega_q][1] += bn

        print(f"  Pass 3 (B(N) compute): {time.time()-t0:.1f}s", flush=True)

        Nf = float(N)
        print(f"\n  B(N) = {total_B}, B/N = {total_B/Nf:.6f}", flush=True)
        print(f"  ω(q) breakdown:", flush=True)
        for w in sorted(B_by_omega_q.keys()):
            cnt, b = B_by_omega_q[w]
            print(f"    ω(q) = {w}: count_n = {cnt} ({cnt/Nf:.6f}), sum b = {b} ({b/Nf:.6f})", flush=True)
        print(f"  Total time: {time.time()-t_total:.1f}s", flush=True)


if __name__ == "__main__":
    main()
