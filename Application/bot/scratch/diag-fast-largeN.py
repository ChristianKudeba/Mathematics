"""
Efficient computation of D_0(N), D(N), and sum_{M in (N,2N]} T(M)^2 at large N
using the period-4d closed form from P12-D0-rigorous.md (Lemma 2).

Key facts (Lemma 2):
  For each (d, n_0) with d in L_odd, n_0^2 = -1 (d), 1 <= n_0 <= d:
    S_{M,d}(n_0) takes the cyclic-shift-(0,1,0,-1) pattern at jump points
    a_k = n_0 + k*d.  S^2 is 4d-periodic on M >= n_0; in each 4d-period
    S^2 = 1 on exactly 2d consecutive integers (in 2 consecutive d-blocks).

Algorithm for D_0(N):
  For each (d, n_0):
    - Determine the starting d-block index of the "S^2 = 1 region" within the
      4d-period (from n_0 mod 4).
    - Count integers M in (N, 2N] that are in S^2 = 1 positions.
  Sum * 4 to get D_0(N).

Algorithm for D(N):
  For each d, build c_d(M) as a piecewise-constant function on each 4d-period,
  with at most rho(d) = 2^omega(d) jumps per d-block.  Then integrate c_d^2 over
  M in (N, 2N].  Cost per d: O(d) to walk through the 4d-period * (N/(4d))
  periods => O(N) per d. Total: O(N * #L_odd) = O(N * N/sqrt(log N)) — too slow.

  Better: compute c_d(M) as a step function with O(rho(d)) jumps per 4d-period.
  Pattern-period is 4d; integrating c_d^2 over the window (N, 2N] costs
  O(rho(d)) per period * #periods = O(rho(d) * N/d).
  Total: O(N * sum_{d, L_odd} rho(d)/d) = O(N * log(N)/pi) = O(N log N).

Algorithm for sum T^2:
  Compute T(M) directly via tau(n^2+1) sieve (as in diag-vs-second-moment.py),
  then sum T(M)^2 for M in (N, 2N].
"""

import math
import time
import sys
from collections import defaultdict

def chi4(n):
    n = n & 3
    if n == 1: return 1
    if n == 3: return -1
    return 0

def sqrt_m1(p):
    # Tonelli for p ≡ 1 (mod 4): find r with r^2 ≡ -1 (mod p)
    for z in range(2, p):
        if pow(z, (p-1)//2, p) == p-1:
            return pow(z, (p-1)//4, p)
    return None

def hensel_lift_roots(p, m0):
    """Iteratively Hensel-lift sqrt(-1) mod p to mod p^k for k=1, 2, ...
    Returns dict pk -> sorted list of roots mod pk."""
    out = {}
    pk = p
    roots = sorted({m0, p - m0})
    out[pk] = list(roots)
    while True:
        pk_next = pk * p
        new_roots = []
        for r in roots:
            # find r' = r + t*pk with (r')^2 ≡ -1 (mod pk_next)
            # 2 r t pk ≡ -(r^2+1) (mod pk_next)
            if (r*r + 1) % pk_next == 0:
                new_roots.append(r)
                continue
            resid = ((-1 - r*r) // pk) % p
            inv2r = pow(2*r % p, -1, p)
            t = (resid * inv2r) % p
            rp = (r + t * pk) % pk_next
            new_roots.append(rp)
        new_roots = sorted(set(new_roots))
        out[pk_next] = new_roots
        pk = pk_next
        roots = new_roots
        if pk_next > 1 << 50:  # safety
            break
        # stop when pk_next exceeds our budget (caller decides via cap)
        if pk_next > CAP_DEFAULT:
            break
    return out

CAP_DEFAULT = 10**9  # raised by main()

def enumerate_pairs(B):
    """Enumerate (d, n_0) with d in L_odd, d <= B, n_0^2 ≡ -1 (mod d), 1 <= n_0 <= d.
    Returns dict d -> list of n_0's (sorted)."""
    global CAP_DEFAULT
    CAP_DEFAULT = B
    # Sieve primes up to B
    sieve = bytearray([1])*(B+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(B))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    primes_1mod4 = [p for p in range(B+1) if sieve[p] and p%4==1]
    print(f"  {len(primes_1mod4)} primes ≡ 1 (mod 4) up to {B}", flush=True)

    # For each prime p, build dict of pk -> roots
    pk_root_map = {}  # p -> {pk: [roots]}
    for p in primes_1mod4:
        m0 = sqrt_m1(p)
        # Iteratively lift only as needed
        roots_dict = {}
        pk = p
        roots = sorted({m0, p - m0})
        while pk <= B:
            roots_dict[pk] = roots
            pk_next = pk * p
            if pk_next > B:
                break
            new_roots = []
            for r in roots:
                if (r*r + 1) % pk_next == 0:
                    new_roots.append(r)
                else:
                    resid = ((-1 - r*r) // pk) % p
                    inv2r = pow(2*r % p, -1, p)
                    t = (resid * inv2r) % p
                    new_roots.append((r + t * pk) % pk_next)
            roots = sorted(set(new_roots))
            pk = pk_next
        pk_root_map[p] = roots_dict

    # BFS over primes: build all (d, n_0) pairs
    # Start: pairs[1] = [0]
    by_d = defaultdict(list)
    by_d[1] = [0]
    for p in primes_1mod4:
        # For each existing d in by_d, multiply by p^k for k=1,2,...
        new_pairs = []
        for d, n0_list in list(by_d.items()):
            for pk, rs in pk_root_map[p].items():
                if d * pk > B:
                    continue
                if d % p == 0:  # avoid double-multiplying by p
                    continue
                inv_pk = pow(pk, -1, d) if d > 1 else 0
                inv_d = pow(d, -1, pk)
                d_new = d * pk
                for n0 in n0_list:
                    for r in rs:
                        if d == 1:
                            x = r % pk
                        else:
                            x = (n0 * pk * inv_pk + r * d * inv_d) % d_new
                        new_pairs.append((d_new, x))
        for d_new, x in new_pairs:
            by_d[d_new].append(x)
    # Sort each list (keep d=1 with n_0=0; rho(1) = 1).
    for d in by_d:
        by_d[d].sort()
    return by_d

def D0_window(d, n0, N):
    """Count of M in (N, 2N] with S_{M,d}(n_0)^2 = 1.
    By Lemma 2, S^2 is 4d-periodic on M >= n_0, with S^2 = 1 on 2 consecutive
    d-blocks per 4d-period.
    Determine the starting d-block index k_start in {0, 1, 2, 3} (relative to
    a_0 = n_0).  S^2 takes value 1 on M in [a_{k_start}, a_{k_start + 2}) within
    each 4d-period.

    From Lemma 2(c): the partial-sum pattern over k=0,1,2,3 takes values
    (s_0, s_1, s_2, s_3) — one of {(1,1,0,0), (0,-1,-1,0), (-1,-1,0,0), (0,1,1,0)}
    depending on phase. The "S^2 = 1" indices in {0,1,2,3} are:
      (1,1,0,0): k in {0, 1}
      (0,-1,-1,0): k in {1, 2}
      (-1,-1,0,0): k in {0, 1}
      (0,1,1,0): k in {1, 2}
    Phase determined by (n_0 + 1) mod 4:
      n_0+1 = 1 mod 4 (n_0 = 0 mod 4): chi_4 pattern (1, 0, -1, 0). Partial sums
        from start: 1, 1, 0, 0.  k_start = 0.
      n_0+1 = 2 mod 4 (n_0 = 1 mod 4): pattern (0, -1, 0, 1). Sums: 0, -1, -1, 0.
        k_start = 1.
      n_0+1 = 3 mod 4 (n_0 = 2 mod 4): pattern (-1, 0, 1, 0). Sums: -1, -1, 0, 0.
        k_start = 0.
      n_0+1 = 0 mod 4 (n_0 = 3 mod 4): pattern (0, 1, 0, -1). Sums: 0, 1, 1, 0.
        k_start = 1.

    But wait: the chi_4(a_k+1) pattern depends on (a_k + 1) mod 4. With
    a_k = n_0 + k*d, (a_k+1) mod 4 = (n_0 + 1 + k*d) mod 4.  Since d is odd
    (d in L_odd), d mod 4 ∈ {1, 3}.  So d=1mod4: (n_0+1+k) mod 4 cycles k+offset.
    d=3mod4: (n_0+1-k) mod 4 cycles k+offset reversed.

    Carefully: For d ≡ 1 (4): pattern over k=0..3 of chi_4(a_k+1) is
    (chi_4(n_0+1), chi_4(n_0+2), chi_4(n_0+3), chi_4(n_0+4)) which is the 4-cycle
    of chi_4 starting at (n_0+1) mod 4.

    For d ≡ 3 (4): pattern over k=0..3 of chi_4(a_k+1) is reversed cycle:
    (chi_4(n_0+1), chi_4(n_0+1-1), chi_4(n_0+1-2), chi_4(n_0+1-3)) = chi_4 starting
    at n_0+1 going backwards.

    So determine k_start (start of S^2=1 region) by computing the partial sums
    for the actual chi_4 sequence.
    """
    # The jump points are a_k = n_0 + k*d for k >= 1 (NOT k=0; the n=n_0
    # case is excluded by the d <= n constraint in S's definition).
    # Increments: b_j := chi_4(a_{j+1} + 1) = chi_4(n_0 + 1 + (j+1)*d) for j=0,1,2,3.
    # Partial sums T_k := sum_{j<k} b_j for k=0,1,2,3 (T_0 = 0 always).
    # S(M) = T_k for M in [a_k, a_{k+1}), which is M - n_0 in [k*d, (k+1)*d).
    seq = [chi4(n0 + 1 + (j+1)*d) for j in range(4)]  # b_0..b_3
    psum = [0]
    s = 0
    for v in seq[:3]:
        s += v
        psum.append(s)
    # T_k for k=0,1,2,3
    one_idx = [k for k in range(4) if psum[k] != 0]
    if len(one_idx) != 2:
        raise ValueError(f"Unexpected one_idx={one_idx} for d={d}, n0={n0}, seq={seq}")
    a, b = sorted(one_idx)
    if b - a != 1:
        raise ValueError(f"Non-consecutive S^2=1 idxs {one_idx} for d={d}, n0={n0}")
    k_start = a
    # k_start is in {1, 2} (since T_0 = 0 always).
    # S^2 = 1 region in period [n_0 + 4dj, n_0 + 4d(j+1)) is M - n_0 in
    # [k_start * d, (k_start + 2) * d).
    # The S^2 = 1 region in the period [n_0 + 0*d, n_0 + 4d) is M in
    # [a_{k_start}, a_{k_start + 2}).  Wraparound: if k_start = 3, region is
    # [a_3, a_5) = [a_3, a_4) ∪ [a_4, a_5) — but a_4 = n_0 + 4d wraps to next period.
    # Equivalently, in each 4d-period starting at a_{4j} = n_0 + 4jd, S^2 = 1 on
    # M in [a_{4j+k_start}, a_{4j+k_start+2}) ∩ [n_0, ∞).
    # For counting purposes over M in (N, 2N]:
    # Treat S^2 as a 4d-periodic indicator function (zero on M < n_0).

    L = 4 * d
    # For each j with 4j*d + n_0 <= 2N, the period [n_0 + 4jd, n_0 + (4j+4)d) intersects
    # the window.  In that period, S^2=1 on M in [n_0 + (4j+k_start)*d, n_0 + (4j+k_start+2)*d).
    # Count integers in this region intersected with (N, 2N], summing over relevant j.

    # Parameterize: relative position in period u = (M - n_0) mod 4d, M >= n_0.
    # Then S^2 = 1 iff u in [k_start * d, (k_start + 2) * d) (mod 4d, but no wrap
    # since k_start <= 3 and k_start+2 <= 5 implies wrap only if k_start = 3 or 2).
    # For k_start in {0, 1, 2}: S^2 = 1 iff u in [k_start*d, (k_start+2)*d).
    # For k_start = 3: u in [3d, 5d) mod 4d = [3d, 4d) ∪ [0, d).

    # k_start is 1 or 2; never 0 (T_0=0) or 3 (would need T_4 != 0 but T_4=T_0=0).
    good_intervals = [(k_start * d, (k_start + 2) * d)]

    # Now count integers M in (N, 2N] with M >= n_0 and (M - n_0) mod 4d in good_intervals.
    # Equivalently: u = (M - n_0) mod 4d, where M ranges in (max(N, n_0-1), 2N].
    M_lo = max(N + 1, n0)  # M >= n_0 for S to be nonzero (M = n_0 - 1 gives S=0)
    M_hi = 2 * N
    if M_lo > M_hi:
        return 0
    # Count u in good_intervals over M in [M_lo, M_hi].
    # u = (M - n_0) mod 4d.
    # Use: count integers M in [M_lo, M_hi] with u in [a, b) (mod 4d).
    count = 0
    for (a, b) in good_intervals:
        # Count M in [M_lo, M_hi] with (M - n_0) mod 4d in [a, b).
        # Transform: x = M - n_0, x in [M_lo - n_0, M_hi - n_0]. x mod 4d in [a, b).
        x_lo = M_lo - n0
        x_hi = M_hi - n0
        # Number of x in [x_lo, x_hi] with x mod L in [a, b) (where L = 4d, b > a):
        # = floor((x_hi - a)/L) - floor((x_lo - 1 - a)/L) ... need to be careful with [a, b).
        # Easier: # = sum_{j} (overlap of [a + j*L, b + j*L) with [x_lo, x_hi]).
        # Compute via: # = #{x in [x_lo, x_hi] : (x - a) mod L < b - a}.
        # Use formula: count_in_residues.
        width = b - a
        # Count integers x in [x_lo, x_hi] with (x - a) mod L < width.
        # Equivalently, t = (x - a) mod L, t in [0, width-1] (integer).
        # Total integers in [x_lo, x_hi] = x_hi - x_lo + 1.
        # In each full period L there are width integers satisfying.
        n_full = (x_hi - x_lo + 1) // L
        rem = (x_hi - x_lo + 1) - n_full * L
        c = n_full * width
        # Partial period: integers x in [x_lo + n_full * L, x_hi].
        # Equivalent to integers x in [x_lo, x_lo + rem - 1] (residues mod L).
        # Count those with (x - a) mod L < width.
        # Compute by iterating only if rem is small; else use direct:
        # Let s0 = (x_lo - a) mod L. The residues in the partial are s0, s0+1, ..., s0+rem-1 mod L.
        # Count those < width.
        if rem > 0:
            s0 = (x_lo - a) % L
            # residues are s0, s0+1, ..., s0+rem-1 (mod L). Count those in [0, width-1].
            # Equivalently: count integers t in [s0, s0+rem-1] with t mod L < width.
            # = (# of t in [s0, s0+rem-1] with t < width) + (# with t-L in [0, width-1]) etc.
            # If s0 + rem - 1 < L: residues are just [s0, s0+rem-1].
            # Count those < width = max(0, min(rem, width - s0)).
            if s0 + rem - 1 < L:
                c += max(0, min(rem, width - s0))
            else:
                # Wraparound: [s0, L-1] then [0, s0+rem-1-L]
                c += max(0, width - s0)  # from [s0, L-1] intersect [0, width-1]
                rem2 = s0 + rem - L  # in [0, ...]
                c += min(rem2, width)
        count += c
    return count

def integrate_cd_squared(d, n0_list, N):
    """Compute sum_{M in (N, 2N]} c_d(M)^2 where c_d(M) = sum_{n_0} S_{M,d}(n_0).

    Direct event-driven walk: compute c_d(N+1) explicitly, then walk through
    jumps in (N+1, 2N], summing c^2 piecewise.

    Cost per d: O(rho(d) * (N/d + 1)) events.  Total over d: O(N log N).
    """
    # Compute b_seqs and T_seqs, plus c_d(N+1).
    b_seqs = {}
    T_seqs = {}
    c = 0
    for n0 in n0_list:
        b = [chi4(n0 + 1 + (j+1)*d) for j in range(4)]
        T = [0]
        s = 0
        for v in b[:3]:
            s += v
            T.append(s)
        b_seqs[n0] = b
        T_seqs[n0] = T
        # Number of jumps for n_0 with M = N+1: K = max(0, floor((N+1 - n_0)/d))
        # but only count k >= 1 (k=0 is no jump).
        if N + 1 < n0 + d:
            S_n0 = 0
        else:
            K = (N + 1 - n0) // d  # >= 1 here
            S_n0 = T[K % 4]
        c += S_n0

    # Collect events in (N+1, 2N]: jumps at M = n_0 + k*d for k >= 1, M > N+1, M <= 2N.
    # A jump at M = N+1 itself is already absorbed in c (= c_d(N+1)).
    events = []
    for n0 in n0_list:
        b = b_seqs[n0]
        # M_jump = n_0 + k*d > N+1 => k > (N+1 - n_0)/d
        #                          => k >= floor((N+1 - n_0)/d) + 1  (since k integer)
        k_lo_lower = max(1, (N + 1 - n0) // d + 1)
        k_hi = (2 * N - n0) // d
        if k_hi < k_lo_lower:
            continue
        for k in range(k_lo_lower, k_hi + 1):
            M_jump = n0 + k * d
            delta = b[(k - 1) % 4]
            if delta != 0:
                events.append((M_jump, delta))
    events.sort()

    total = 0
    M_cur = N + 1
    for M_jump, delta in events:
        if M_jump > M_cur:
            total += (M_jump - M_cur) * c * c
        c += delta
        M_cur = M_jump
    if 2*N >= M_cur:
        total += (2*N - M_cur + 1) * c * c
    return total

def integrate_cd_squared_OLD(d, n0_list, N):
    """OLD VERSION — buggy for d > N/5 (warm-up handling).  Kept for reference."""
    rho = len(n0_list)
    L = 4 * d
    # In one full 4d-period of M starting after warm-up, c_d takes values determined by
    # the jump pattern.  Specifically: for each n_0, S(n_0) jumps at M = n_0 + k*d for
    # k = ..., 0, 1, 2, 3 mod 4 (but k goes through all integers; mod 4 determines value).

    # For computational efficiency: precompute the value of c_d on M ranging over one
    # 4d-period.  Use the steady-state period [warm_up, warm_up + 4d) where warm_up
    # is past the last n_0.

    max_n0 = max(n0_list)
    warm_up_start = max_n0 + 4*d  # any M past this is in steady state

    # Precompute c_d(M) for M in [warm_up_start, warm_up_start + 4d).
    # First compute S(n_0) at M = warm_up_start for each n_0.
    S_init = {}
    for n0 in n0_list:
        # Jumps at n = n_0 + k*d for k >= 1 (NOT k=0, since n >= d required).
        # Increments b_j = chi_4(n_0 + 1 + (j+1)*d) for j = 0,1,2,3 (4-periodic).
        # After K = floor((M - n_0)/d) jumps, S(M) = T_{K mod 4} where
        # T_0=0, T_r = sum_{j<r} b_j.
        b_seq = [chi4(n0 + 1 + (j+1)*d) for j in range(4)]
        T = [0]
        s = 0
        for v in b_seq[:3]:
            s += v
            T.append(s)
        # T = [T_0, T_1, T_2, T_3]
        if warm_up_start - 1 < n0 + d:
            S_init[n0] = 0
        else:
            K = (warm_up_start - 1 - n0) // d
            S_init[n0] = T[K % 4]

    # Now walk the 4d-period and record c_d values per integer.
    # But that's 4d integers — too slow if d is large.  Instead, find the jump events
    # (M, delta_c) in this period, and integrate piecewise.

    events = []  # list of (M_jump, delta_c) — at integer M, c_d changes by delta_c.
    for n0 in n0_list:
        # In [warm_up_start, warm_up_start + 4d), the jumps for this n_0 are at
        # M = n_0 + k*d for k such that warm_up_start <= n_0 + k*d < warm_up_start + 4d.
        # k_lo = ceil((warm_up_start - n_0) / d), k_hi = ceil((warm_up_start + 4d - n_0)/d) - 1.
        k_lo = -(-(warm_up_start - n0) // d)  # ceil
        k_hi = -(-(warm_up_start + 4*d - n0) // d) - 1
        for k in range(k_lo, k_hi + 1):
            M_jump = n0 + k * d
            delta = chi4(n0 + 1 + k*d)  # chi_4(M_jump + 1)
            events.append((M_jump, delta))

    events.sort()
    # Now walk: c_d at M = warm_up_start - 1 is sum S_init.
    # Wait — c_d(M) is sum of S(M, n_0) which counts up to and including M.
    # S(warm_up_start - 1, n_0) = S_init (defined as M = warm_up_start - 1 partial sum).
    # At M = warm_up_start, if any n_0 has a_k = warm_up_start, then S jumps by chi_4(M+1).
    # Then c_d(M) at M = warm_up_start = previous c_d + sum of deltas at M = warm_up_start.

    # Actually c_d(M) is defined as sum_{n_0} S(M, n_0).  S(M, n_0) = sum_{n <= M, n ≡ n_0, n >= d} chi_4(n+1).
    # So as M increases by 1, S(M, n_0) gains chi_4(M+1) iff M >= d and M ≡ n_0 (mod d).

    # Sum across all M in [warm_up_start, warm_up_start + 4d):
    # We have piecewise-constant c_d(M) on intervals between jumps.
    # Compute sum c_d(M)^2 over this 4d-period.

    # Initial c_d at M = warm_up_start - 1:
    c_prev = sum(S_init.values())
    sum_c2_period = 0
    M_cur = warm_up_start
    # Process events sorted by M_jump.
    for M_jump, delta in events:
        # On [M_cur, M_jump): c_d = c_prev. Length: M_jump - M_cur integers.
        if M_jump > M_cur:
            sum_c2_period += (M_jump - M_cur) * c_prev * c_prev
        # At M = M_jump: c_d updates to c_prev + delta.
        c_prev = c_prev + delta
        M_cur = M_jump
    # Tail: from M_cur to warm_up_start + 4d - 1.
    tail_end = warm_up_start + 4*d
    if tail_end > M_cur:
        sum_c2_period += (tail_end - M_cur) * c_prev * c_prev

    # Sanity: c_prev after one full period should equal initial sum (returns to start).
    # (Because chi_4 over 4 jumps per n_0 sums to 0.)

    # Now we want sum over M in (N, 2N].  This window has length N.
    # Number of complete 4d-periods: q = N // (4d).  Remainder: r = N - q * 4d.

    q = N // (4 * d)
    r = N - q * (4 * d)

    sum_total = q * sum_c2_period

    # Remainder: sum c_d(M)^2 over M in (N, N + r].  These M's correspond to some
    # offset in the 4d-period.  Compute by walking r integers from a specific phase.

    # First, c_d(M) at M = N is determined by the period starting at warm_up_start.
    # Let phase = (N + 1 - warm_up_start) mod (4d).  Then M = N + 1 has the same c_d
    # value as M' = warm_up_start + phase.  But our period values were sampled at
    # warm_up_start, so we need to figure out c_d at M' = warm_up_start + phase.

    if r > 0:
        # Compute c_d on [warm_up_start, warm_up_start + 4d) — already have events.
        # Replay walk to find c_d at each integer position in [phase_start, phase_start + r].
        phase_start = (N + 1 - warm_up_start) % (4 * d)
        phase_end_excl = phase_start + r  # might exceed 4d
        # c_d values on the 4d-period: walk events again.
        # Build a list (M_jump_rel, delta) where M_jump_rel = M_jump - warm_up_start in [0, 4d).
        rel_events = sorted([(ev[0] - warm_up_start, ev[1]) for ev in events])
        # Initial c at M_rel = 0 is sum(S_init.values()) before any jumps at M = warm_up_start.
        # If there's a jump at rel = 0, c_d at M = warm_up_start = c_init + delta.
        c_init = sum(S_init.values())
        # Walk through (phase_start, phase_end_excl) and accumulate c_d^2.
        # phase_end_excl can be > 4d; handle wraparound.
        # Simpler: split into [phase_start, min(4d, phase_end_excl)) and (if needed)
        # [0, phase_end_excl - 4d).
        def walk_and_sum(lo, hi):
            # sum c_d(M_rel)^2 for M_rel in [lo, hi).
            if lo >= hi:
                return 0
            c = c_init
            sub = 0
            cur = 0
            # Apply jumps and accumulate.
            for M_jump_rel, delta in rel_events:
                if M_jump_rel < cur:
                    continue
                # Interval [cur, min(M_jump_rel, hi)) at value c.
                seg_lo = max(cur, lo)
                seg_hi = min(M_jump_rel, hi)
                if seg_hi > seg_lo:
                    sub += (seg_hi - seg_lo) * c * c
                if M_jump_rel >= hi:
                    return sub
                # Apply the jump at M_jump_rel.
                c = c + delta
                cur = M_jump_rel
                # Note: at M_jump_rel itself, c_d takes the new value.
            # Tail from cur to hi.
            seg_lo = max(cur, lo)
            seg_hi = hi
            if seg_hi > seg_lo:
                sub += (seg_hi - seg_lo) * c * c
            return sub

        if phase_end_excl <= 4 * d:
            sum_total += walk_and_sum(phase_start, phase_end_excl)
        else:
            sum_total += walk_and_sum(phase_start, 4 * d)
            sum_total += walk_and_sum(0, phase_end_excl - 4 * d)

    return sum_total

def compute_T_cumulative(Bmax):
    """Compute T(M) for M = 0..Bmax via tau(n^2+1) sieve."""
    print(f"  computing T cumulative up to {Bmax}", flush=True)
    t0 = time.time()
    sieve = bytearray([1])*(Bmax+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(Bmax))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    primes_1mod4 = [p for p in range(Bmax+1) if sieve[p] and p%4==1]
    R = list(range(Bmax+1))
    R = [n*n+1 for n in range(Bmax+1)]
    R[0] = 1
    tau = [1]*(Bmax+1); tau[0] = 0
    for n in range(1, Bmax+1, 2):
        if R[n] % 2 == 0:
            R[n] //= 2
            tau[n] *= 2
    for p in primes_1mod4:
        if p > Bmax + 1:
            break
        m0 = sqrt_m1(p)
        roots = {m0, p - m0}
        for r in roots:
            n = r if r >= 1 else r + p
            while n <= Bmax:
                if R[n] % p == 0:
                    e = 0
                    while R[n] % p == 0:
                        R[n] //= p; e += 1
                    tau[n] *= (e+1)
                n += p
    for n in range(1, Bmax+1):
        if R[n] > 1:
            tau[n] *= 2
    Tcum = [0]*(Bmax+1)
    for n in range(1, Bmax+1):
        c4 = chi4(n+1)
        if c4:
            Tcum[n] = Tcum[n-1] + tau[n]*c4
        else:
            Tcum[n] = Tcum[n-1]
    print(f"  done T cumulative, time={time.time()-t0:.1f}s", flush=True)
    return Tcum

def main():
    import os
    if 'NS' in os.environ:
        Ns = [int(x) for x in os.environ['NS'].split(',')]
    else:
        Ns = [10000, 20000, 50000, 100000, 200000, 500000]
    Bmax = 2 * max(Ns)

    print(f"=== large-N D_0, D, sum T^2 computation ===")
    print(f"  Ns = {Ns}, Bmax = {Bmax}", flush=True)

    # T cumulative (for sum T^2).
    Tcum = compute_T_cumulative(Bmax)

    # Enumerate (d, n_0) pairs.
    print(f"  enumerating (d, n_0) pairs with d <= {Bmax}", flush=True)
    t0 = time.time()
    by_d = enumerate_pairs(Bmax)
    n_pairs = sum(len(v) for v in by_d.values())
    print(f"  enumerated {n_pairs} pairs over {len(by_d)} d's, time={time.time()-t0:.1f}s", flush=True)

    # Compute D_0(N) and D(N) for each N.
    print(f"\n  {'N':>8}  {'sum T^2':>14}  {'D':>14}  {'D_0':>14}  "
          f"{'sumT/N^2':>10}  {'D/N^2':>10}  {'D_0/N^2':>10}  {'O/N^2':>10}")
    for N in Ns:
        t0 = time.time()
        D0 = 0
        D = 0
        # Iterate d <= 2N.
        for d, n0_list in by_d.items():
            if d > 2 * N:
                continue
            for n0 in n0_list:
                D0 += D0_window(d, n0, N)
            # D: sum c_d(M)^2 over M in (N, 2N], times 4 at the end.
            D += integrate_cd_squared(d, n0_list, N)
        D0 *= 4
        D *= 4
        sT2 = sum(Tcum[M]*Tcum[M] for M in range(N+1, 2*N+1))
        O = sT2 - D
        print(f"  {N:>8}  {sT2:>14}  {D:>14}  {D0:>14}  "
              f"{sT2/(N*N):>10.4f}  {D/(N*N):>10.4f}  {D0/(N*N):>10.4f}  {O/(N*N):>10.4f}",
              flush=True)
        print(f"    [time {time.time()-t0:.1f}s]", flush=True)

if __name__ == '__main__':
    main()
