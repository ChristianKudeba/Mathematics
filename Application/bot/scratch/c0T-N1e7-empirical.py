"""
Fast sieve to compute T(N) = sum_{n <= N} 2^omega(n^2+1) and split it into
  T_<(N) = sum_{n <= N, e sf | n^2+1, e <= N} 1
  T_>(N) = sum_{n <= N, e sf | n^2+1, e > N} 1
  A(N)   = #{(n, e) : e sf | n^2+1, n < e <= N}
  B(N)   = sum_{n: n^2+1 not sf} #{e sf | n^2+1 : sqrt(rad(n^2+1)) < e <= n}
  T_half(N) = sum_{n <= N, e sf | n^2+1, e <= sqrt(rad(n^2+1))}
verifying T_<(N) = T_half(N) + A(N) + B(N) and T(N) = 2 T_half(N).

Targets: N in {10^5, 10^6, 3*10^6, 10^7}.

Output the residuals
  c_0^T(N)  := T(N)/N - c_1 log N
  c_<^app(N) := T_<(N)/N - a_1 log N
  c_>^app(N) := T_>(N)/N - a_1 log N
  A(N)/N
  B(N)/N
where c_1 = pi H(1)/2, a_1 = c_1/2 = pi H(1)/4.

Predicted (from prev sessions' closed forms):
  c_0^T = 1.158730 - 2 B^infty,
  with closed-form B^infty ≈ 0.085704, so c_0^T ≈ 0.987322.
  A^infty = R H(1) = pi/4 * 0.55267 = 0.434068.
  c_<^infty = R H'(1) + gamma_K H(1) = 1.013429.

Numerical inputs (from prev sessions; 6-digit precision):
  H(1) = 0.552674
  H'(1) = 0.83558
  gamma_K = 0.6462
"""

import math
import time
import sys

import numpy as np


# === constants from prev sessions ===
H1     = 0.552674
HP1    = 0.83558
GAMMAK = 0.6462
R      = math.pi / 4.0
C1     = R * 2 * H1     # = pi H(1)/2
A1     = R * H1         # = pi H(1)/4

C_LT_INF = R * HP1 + GAMMAK * H1   # 1.013429
A_INF    = R * H1                  # 0.434068
B_INF_PRED = 0.085704              # from per-prime closed form (prev session)
C0_T_PRED  = 1.158730 - 2 * B_INF_PRED  # = 0.987322


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
    Rr = pow(a, (Q + 1) // 2, p)
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
        Rr = (Rr * b) % p
    return Rr


def hensel_lift(r, pk_old, pk_new, p):
    r = int(r)
    pk_new = int(pk_new)
    f = (r * r + 1) % pk_new
    two_r = (2 * r) % pk_new
    inv = pow(two_r, -1, pk_new)
    return (r - f * inv) % pk_new


def main():
    args = sys.argv[1:]
    if not args:
        Nmax = 10**7
    else:
        Nmax = int(args[0])
    print(f"Sieving primes up to {Nmax}...", flush=True)
    t0 = time.time()
    primes = primes_up_to(Nmax)
    print(f"  {len(primes)} primes ({time.time()-t0:.1f}s)", flush=True)

    mask = (primes == 2) | (primes % 4 == 1)
    split_primes = primes[mask].astype(int)
    print(f"  {len(split_primes)} split primes (incl 2)", flush=True)

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

    N = Nmax

    # === Pass 1: omega + is_nsf + residual ===
    print(f"\n=== N = {N}: Pass 1 (omega + is_nsf) ===", flush=True)
    omega   = np.zeros(N + 1, dtype=np.int32)
    is_nsf  = np.zeros(N + 1, dtype=bool)
    n_arr = np.arange(0, N + 1, dtype=np.int64)
    residual = n_arr * n_arr + 1

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
            # divide residual once per Hensel level; track higher levels too
            residual[idx] //= p_int
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
                residual[idx_k] //= p_int
                pk = pk_new
                r_curr = r_new
    print(f"  Pass 1: {time.time()-t0:.1f}s", flush=True)

    # Add 1 to omega for n with residual > 1 (single large prime)
    has_large = residual > 1
    has_large[0] = False
    omega[has_large] += 1

    # Validation
    if N >= 7:
        print(f"  omega[2]=1?  {omega[2]==1}", flush=True)
        print(f"  omega[7]=2?  {omega[7]==2}", flush=True)
        print(f"  is_nsf[7]=True? {is_nsf[7]}", flush=True)
        print(f"  is_nsf[2]=False? {not is_nsf[2]}", flush=True)
        # residual[2] should be 5 (since 2^2+1=5, no small split prime divides
        # via the AP r=1 mod 2 — wait, residual is 5 only if we never divided
        # by 5. Since 5 = N when N>=5, we'd divide it out only if 5 in split_primes
        # AND r0 such that 2 ≡ r0 mod 5. r0=2 (since 2^2+1=5). So we divided
        # residual[2] //= 5. So residual[2] = 1 here, not 5.
        # As a more robust check:
        # T_check = sum_{n=1..7} 2^omega(n^2+1):
        #   n=1: 2 = 2^1, omega=1
        #   n=2: 5 = 5, omega=1
        #   n=3: 10 = 2·5, omega=2
        #   n=4: 17, omega=1
        #   n=5: 26 = 2·13, omega=2
        #   n=6: 37, omega=1
        #   n=7: 50 = 2·5^2, omega=2
        # T_check = 2+2+4+2+4+2+4 = 20
        T_check = (1 << omega[1:8]).sum()
        print(f"  T(7) = {T_check} (expected 20)", flush=True)

    # === T(N) at decadal points + T_<, T_>, T_half, A, B at N=Nmax ===
    print(f"\n=== Aggregate stats ===", flush=True)
    t0 = time.time()
    pow2_omega = np.zeros(N + 1, dtype=np.int64)
    pow2_omega[1:] = (1 << omega[1:].astype(np.int64))
    cum_T = np.cumsum(pow2_omega.astype(np.int64))
    print(f"  T(N) cumsum: {time.time()-t0:.1f}s", flush=True)

    decadal_Ns = [10**5, 10**6, 3 * 10**6, 10**7]
    decadal_Ns = [n for n in decadal_Ns if n <= N]

    print(f"\n=== T(N) and c_0^T residuals (predicted c_0^T = {C0_T_PRED:.6f}) ===", flush=True)
    print(f"  c_1 = pi H(1)/2 = {C1:.6f}", flush=True)
    print(f"  Format: N | T(N) | T(N)/N | c_1 log N | c_0^T(N) = T(N)/N - c_1 log N", flush=True)
    for n_target in decadal_Ns:
        T_n = int(cum_T[n_target])
        per_n = T_n / n_target
        c1_logN = C1 * math.log(n_target)
        c0T_emp = per_n - c1_logN
        print(f"  N={n_target:>10d}  T={T_n:>14d}  T/N={per_n:.6f}  c_1*logN={c1_logN:.6f}  c_0^T(N)={c0T_emp:+.6f}",
              flush=True)

    # === Now: T_<, T_>, A, B at N = Nmax ===
    # T_< = sum over (n,e): n<=N, e sf | n^2+1, e <= N  (i.e., counts pairs where the sf divisor is <= N)
    # T_> = sum_{n<=N} 2^omega(n^2+1) - T_< (by Hooley, the sf divisors of n^2+1 are 2^omega total)
    # A   = #{(n,e): e sf | n^2+1, n < e <= N}
    # B   = #{(n,e): n^2+1 not sf, sqrt(rad(n^2+1)) < e <= n, e sf | n^2+1}
    # T_half = T_< - A - B
    # We must enumerate sf divisors of each n^2+1. For n^2+1 squarefree, all divisors
    # of n^2+1 are sf; for non-sf, sf divisors come from the radical (#divisors = 2^omega).

    # Strategy: for non-sf n we need actual prime list. For sf n, we just need omega.
    # Total #{sf divisors} = 2^omega for both.
    # The pairs (n,e) with e <= N split as e <= n, e in (n, N] (i.e., n < e <= N = A).

    print(f"\n=== Pass 2: factorization (non-sf only) for A, B, T_<, T_> at N={N} ===", flush=True)
    t0 = time.time()
    nsf_indices = np.where(is_nsf)[0]
    omega_nsf = omega[nsf_indices].astype(np.int64)
    total_entries = int(omega_nsf.sum())
    print(f"  non-sf count: {len(nsf_indices)} ({len(nsf_indices)/N:.6f})", flush=True)
    print(f"  total prime-events for non-sf: {total_entries}", flush=True)

    primes_flat = np.zeros(total_entries, dtype=np.int64)
    exps_flat   = np.zeros(total_entries, dtype=np.int8)
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

    # large prime > N
    nsf_with_large = is_nsf & has_large
    idx_large = np.where(nsf_with_large)[0]
    if len(idx_large) > 0:
        positions_large = nsf_pos[idx_large]
        wp_large = write_ptr[positions_large]
        primes_flat[wp_large] = residual[idx_large]
        exps_flat[wp_large] = 1
        write_ptr[positions_large] += 1
    assert np.all(write_ptr == offsets[1:]), "Write pointer mismatch"
    print(f"  Pass 2: {time.time()-t0:.1f}s", flush=True)

    # === Pass 3: enumerate sf divisors and compute B (non-sf only) ===
    print(f"\n=== Pass 3: B(N) compute (non-sf only) ===", flush=True)
    t0 = time.time()
    primes_flat_py = primes_flat.tolist()
    exps_flat_py = exps_flat.tolist()
    offsets_py = offsets.tolist()
    nsf_indices_py = nsf_indices.tolist()
    total_B = 0
    # For non-sf n, we ALSO need to know how many sf divisors of n^2+1 are in (n, N].
    # Call this A_nsf(n). Total A = A_sf + A_nsf where A_sf is from sf n.
    # Easier: compute A directly by enumerating sf divisors at all n. But for sf n,
    # we don't have prime lists. Use Lemma 2 from the AB-decomposition note instead:
    #   A(N) = sum_{e sf, 2 <= e <= N} rho(e)
    # which is independent of n.
    A_nsf_sum = 0
    for i in range(len(nsf_indices_py)):
        n = nsf_indices_py[i]
        start = offsets_py[i]
        end = offsets_py[i + 1]
        primes_n = primes_flat_py[start:end]
        rad = 1
        for p in primes_n:
            rad *= p
        # Enumerate sf divisors of n^2+1 = subsets of primes_n
        divisors = [1]
        for p in primes_n:
            divisors = divisors + [d * p for d in divisors]
        # B: count e with sqrt(rad) < e <= n
        bn = 0
        an = 0
        for e in divisors:
            if e * e > rad and e <= n:
                bn += 1
            if n < e <= N:
                an += 1
        total_B += bn
        A_nsf_sum += an
    print(f"  Pass 3 (B compute): {time.time()-t0:.1f}s", flush=True)

    # === Now compute A directly via Lemma 2 ===
    # A(N) = #{e sf in [2, N] with rho(e) >= 1}, weighted by rho(e).
    # Equivalently, sum over sf e in [2,N] of #{x in [1, e-1]: x^2 + 1 ≡ 0 mod e}.
    # We can compute this via a sieve over sf e using the same prime structure.
    # But there's a simpler identity: A(N) = #{(n, e) : 1 <= n < e <= N, e sf, n^2+1 ≡ 0 mod e}.
    # Using e = product of distinct split primes <= N:
    # For each sf e in [2, N] composed only of split primes,
    # rho(e) = product over primes p|e of rho(p) = 2^omega(e) (with rho(2)=1).
    # The sum of rho(e) for e sf in [2,N] is sum_{e sf <= N} rho(e).
    # We compute this by direct formula:  A_total(N) = sum_{e sf, e <= N, e>=2} rho(e).
    # For checking purposes, we count it via a sieve: enumerate sf "Gaussian-divisor"
    # multiplicities by inclusion.
    # SIMPLER: A(N) = (# pairs (n, e) with 1 <= n <= N, e sf | n^2+1, n < e <= N)
    # Looping over all e is O(N), per-e inner work is rho(e) — cheap.
    print(f"\n=== Pass 4: A(N) via direct enumeration over sf e ===", flush=True)
    t0 = time.time()
    # For each sf e in [2,N], find all roots r with r^2+1 ≡ 0 mod e using CRT.
    # A_total = sum_{e sf, 2<=e<=N} rho(e)
    # Sieve sf-ness: e is sf iff no p^2 | e
    is_sf = np.ones(N + 1, dtype=bool)
    is_sf[0] = False
    is_sf[1] = False
    for p in primes:
        p_int = int(p)
        p2 = p_int * p_int
        if p2 > N:
            break
        is_sf[p2::p2] = False
    sf_indices = np.where(is_sf)[0]
    # rho(e) = 0 unless every prime factor of e is split.
    # We'll compute rho via a multiplicative-sieve. rho(p) = 2 for split p ≡ 1 mod 4,
    # rho(2) = 1, rho(p) = 0 for inert.
    rho = np.zeros(N + 1, dtype=np.int32)
    rho[1] = 1
    # multiplicative sieve
    smallest_prime = np.zeros(N + 1, dtype=np.int64)
    for p in primes:
        p_int = int(p)
        idx = np.arange(p_int, N + 1, p_int)
        sp_zero = (smallest_prime[idx] == 0)
        smallest_prime[idx[sp_zero]] = p_int
    # rho is multiplicative; for sf e:
    for e in sf_indices:
        e = int(e)
        m = e
        rho_e = 1
        valid = True
        while m > 1:
            p = int(smallest_prime[m])
            # for sf e we just divide once
            m //= p
            if p == 2:
                rho_e *= 1
            elif p % 4 == 1:
                rho_e *= 2
            else:
                rho_e = 0
                valid = False
                break
        if valid:
            rho[e] = rho_e
    A_total = int(rho[2:N+1].sum())
    print(f"  Pass 4: {time.time()-t0:.1f}s", flush=True)

    # === Compute T_<, T_>, T_half ===
    # T_<(N) = #{(n, e) : 1 <= n <= N, e sf | n^2+1, e <= N}
    # We have T_<(N) = T_half(N) + A(N) + B(N), and T(N) = 2 T_half(N).
    # So T_half(N) = T(N) / 2, T_<(N) = T(N)/2 + A(N) + B(N), T_>(N) = T(N) - T_<(N).
    T_N = int(cum_T[N])
    T_half_N = T_N // 2
    A_N = A_total  # by Lemma 2
    B_N = int(total_B)
    T_lt_N = T_half_N + A_N + B_N
    T_gt_N = T_N - T_lt_N

    # Sanity: T - 2 T_half = 0 (always true if T even)
    parity_T_check = (T_N % 2 == 0)
    print(f"\n=== Sanity checks at N = {N} ===", flush=True)
    print(f"  T(N) parity even? {parity_T_check}  (T - 2 T_half = {T_N - 2*T_half_N})", flush=True)
    print(f"  A_nsf_sum (via factor list) vs A_total (via direct sf enum):", flush=True)
    print(f"    A_nsf_sum = {A_nsf_sum}", flush=True)
    print(f"    A_total   = {A_total}", flush=True)
    print(f"    diff      = {A_total - A_nsf_sum} (must be A_sf, the contribution from sf n)", flush=True)

    # === Final residuals ===
    print(f"\n=== Final residuals at N = {N} ===", flush=True)
    logN = math.log(N)
    Nf = float(N)

    c0T_emp = T_N / Nf - C1 * logN
    cLT_app = T_lt_N / Nf - A1 * logN
    cGT_app = T_gt_N / Nf - A1 * logN
    A_per_N = A_N / Nf
    B_per_N = B_N / Nf

    print(f"  T(N)        = {T_N}", flush=True)
    print(f"  T_<(N)      = {T_lt_N}", flush=True)
    print(f"  T_>(N)      = {T_gt_N}", flush=True)
    print(f"  T_half(N)   = {T_half_N}", flush=True)
    print(f"  A(N)        = {A_N}", flush=True)
    print(f"  B(N)        = {B_N}", flush=True)
    print(f"  Identity T_<(N) - T_half(N) - A(N) - B(N) = {T_lt_N - T_half_N - A_N - B_N}", flush=True)
    print(f"  c_0^T(N) = T(N)/N - c_1 log N = {c0T_emp:+.6f}   (predicted {C0_T_PRED:+.6f})", flush=True)
    print(f"  c_<^app(N) = T_<(N)/N - a_1 log N = {cLT_app:+.6f}   (predicted c_<^infty = {C_LT_INF:+.6f})", flush=True)
    print(f"  c_>^app(N) = T_>(N)/N - a_1 log N = {cGT_app:+.6f}   (predicted c_>^infty = {C0_T_PRED - C_LT_INF:+.6f})", flush=True)
    print(f"  A(N)/N = {A_per_N:.6f}   (predicted {A_INF:.6f})", flush=True)
    print(f"  B(N)/N = {B_per_N:.6f}   (predicted {B_INF_PRED:.6f})", flush=True)

    # Save
    import json
    out = {
        "N": N,
        "T_N": T_N,
        "T_lt_N": T_lt_N,
        "T_gt_N": T_gt_N,
        "T_half_N": T_half_N,
        "A_N": A_N,
        "B_N": B_N,
        "c0T_emp": c0T_emp,
        "cLT_app": cLT_app,
        "cGT_app": cGT_app,
        "A_per_N": A_per_N,
        "B_per_N": B_per_N,
        "decadal": [
            {"N": int(n_target), "T_N": int(cum_T[n_target]),
             "c0T_emp": cum_T[n_target] / float(n_target) - C1 * math.log(n_target)}
            for n_target in decadal_Ns
        ],
    }
    print(f"\n=== JSON SUMMARY ===", flush=True)
    print(json.dumps(out, indent=2), flush=True)


if __name__ == "__main__":
    main()
