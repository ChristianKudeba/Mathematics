"""
Test the AP-decomposition diagonal estimate for T(N).

Decomposition (P12 Thm C step 4):
  T(M) = 2 * sum_{d in L_odd, d<=M} c_d(M)
  c_d(M) = sum_{n_0 mod d, n_0^2 ≡ -1 (d)}  S_{M,d}(n_0)
  S_{M,d}(n_0) = sum_{n ≡ n_0 (d), d <= n <= M} chi_4(n+1)

Step 4 proved |S_{M,d}(n_0)| <= 1, so |c_d(M)| <= rho(d) = 2^omega(d).

Test 1: Diagonal of second moment.
  D(N) := 4 * sum_{d in L_odd, d<=2N} sum_{M=N+1..2N} c_d(M)^2
  Hypothesis: D(N) >= sum_M T(M)^2 (with off-diag potentially negative).
  Trivial upper bound: D(N) <= 4 N * sum_{d<=2N, L_odd} rho(d)^2 ~ N^2 log N.
  Plausible estimate: D(N) ~ 2 N * sum_{d<=2N, L_odd} rho(d) ~ 4 N^2.

Test 2: Same on n_0=n_0' "true diagonal" only:
  TD(N) := 4 * sum_{d in L_odd, d<=2N} sum_{n_0} sum_M S_{M,d}(n_0)^2
        ~ 4 * (N/2) * sum_{d<=2N, L_odd} rho(d) = 2 N * sum 2^omega ~ 4 c N^2.

We compute these for moderate N (5e3, 1e4, 5e4, 1e5) directly, no Tonelli.
"""

import math
import time
import sys

def chi4(n):
    n = n & 3
    if n == 1: return 1
    if n == 3: return -1
    return 0

def compute(Ns):
    Nmax = max(Ns)
    print(f"Direct AP decomposition test up to Nmax={Nmax}", flush=True)
    t0 = time.time()

    # Find all (d, n_0) with d in L_odd, d <= 2*Nmax, n_0^2 ≡ -1 (mod d).
    # We also need T(M) for verification, so we'll factor n^2+1 directly.
    # Memory budget: bookkeep per-d arrays of c_d(M) at sample M's.

    # Easier: for each (d, n_0) pair, simulate S_{M,d}(n_0) over M=1..2*Nmax
    # and accumulate squared partial sums into the appropriate dyadic windows.

    # Generate all (d, n_0) pairs. We need d odd, all primes ≡ 1 mod 4, d <= 2*Nmax.
    # For efficiency: enumerate d using a sieve.

    # Sieve primes up to 2*Nmax
    B = 2*Nmax
    sieve = bytearray([1])*(B+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(B))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    primes_1mod4 = [p for p in range(B+1) if sieve[p] and p%4==1]
    print(f"  {len(primes_1mod4)} primes ≡ 1 (mod 4) up to {B}", flush=True)

    # Enumerate squarefree-ish d in L_odd up to B (d = product of distinct primes ≡ 1 mod 4
    # is squarefree; L_odd also includes prime powers p^k for p≡1 mod 4)
    # For simplicity: enumerate all d in L_odd via recursive multiplication, then for each find the n_0's.
    # This may be heavy memory; cap d at a reasonable threshold.

    # We'll compute the diagonal by enumerating (d, n_0) directly.

    # tonelli-shanks for sqrt(-1) mod p
    def sqrt_m1(p):
        for z in range(2, p):
            if pow(z, (p-1)//2, p) == p-1:
                return pow(z, (p-1)//4, p)
        return None

    # For each d in L_odd, n_0 with n_0^2 ≡ -1 (d): enumerate via CRT over prime power factors.
    # For simplicity, restrict to d up to a cap because enumerating all d in L_odd up to B is expensive.

    # Strategy: enumerate primes p_1, p_2, ... ≡ 1 (mod 4), use BFS to multiply,
    # store list of (d, root) where root is a sqrt(-1) mod d.
    # We only need ROOTS UP TO d <= B. But there can be MANY such d's.

    # For sanity: do this only for d up to some threshold per N (we test smaller N).

    # PLAN B (simpler, and what the diagonal really tests):
    # Compute sum_M T(M)^2 directly for our chosen N's, then SEPARATELY compute
    # the AP-diagonal sum_d sum_M c_d(M)^2 by iterating over d in L_odd up to 2N.

    # For each test N, work as follows:
    test_results = []

    # We need T(M) for M=1..2*Nmax. Sieve a[n] = tau(n^2+1)*chi_4(n+1).
    print(f"  computing a[n] for n=1..{2*Nmax}", flush=True)
    Nbig = 2*Nmax
    tau = [1]*(Nbig+1)  # tau(n^2+1) for n>=1
    R = [n*n+1 for n in range(Nbig+1)]
    R[0] = 1; tau[0] = 0
    # 2-power
    for n in range(2, Nbig+1, 2):
        # n even: n^2+1 odd; no factor of 2.
        pass
    for n in range(1, Nbig+1, 2):
        # n odd: n^2+1 even, n^2+1 ≡ 2 (mod 4) (since n odd => n^2 ≡ 1 (mod 8) actually for odd n n^2≡1 mod 8, so n^2+1 ≡ 2 (mod 8), so v_2=1 only).
        # divide out single 2
        if R[n] % 2 == 0:
            R[n] //= 2
            tau[n] *= 2
    # Now sieve odd primes p ≡ 1 mod 4 and p ≡ 3 mod 4 — but only p ≡ 1 mod 4 divide some n^2+1.
    for p in primes_1mod4:
        if p > Nbig + 1:
            break
        m0 = sqrt_m1(p)
        roots = {m0, p - m0}
        # find smallest n with n^2 ≡ -1 (mod p) in [1, Nbig], then step by p
        for r in roots:
            n = r if r >= 1 else r + p
            while n <= Nbig:
                if R[n] % p == 0:
                    e = 0
                    while R[n] % p == 0:
                        R[n] //= p; e += 1
                    tau[n] *= (e+1)
                n += p
    # residual single large prime
    for n in range(1, Nbig+1):
        if R[n] > 1:
            tau[n] *= 2
    a = [0]*(Nbig+1)
    for n in range(1, Nbig+1):
        c4 = chi4(n+1)
        a[n] = tau[n]*c4 if c4 else 0
    Tcum = [0]*(Nbig+1)
    for n in range(1, Nbig+1):
        Tcum[n] = Tcum[n-1] + a[n]

    print(f"  T(Nmax)={Tcum[Nmax]}, T(2Nmax)={Tcum[2*Nmax]}, time={time.time()-t0:.1f}s", flush=True)

    # Now the actual work: compute diagonal of AP decomp.
    # For each d in L_odd, d <= 2Nmax, and each n_0 with n_0^2 ≡ -1 (mod d):
    #   Compute S_{M,d}(n_0) for M=1..2Nmax, accumulate into per-N second moment.

    # We compute a global per-d sum_{M=N+1..2N} c_d(M)^2 = (sum_{n_0} S_{M,d}(n_0))^2

    # To enumerate (d, n_0) pairs efficiently, do prime-power CRT building:
    # Start with d=1, root=0 (S_{M,1}(0) = sum_{n=1..M} chi_4(n+1)).
    # For each prime p ≡ 1 mod 4, multiply each existing (d, n0) by p^k to get
    # new (d * p^k, new_n0) via CRT.

    # Memory cost: number of (d, n_0) pairs up to B is sum_{d in L_odd} rho(d)
    # which is ~ B (Selberg-Delange with kappa=1). At B=2e5 (Nmax=1e5), that's
    # ~2e5 pairs. Each pair needs walks of length ~Nbig. That's 2e5 * 2e5 = 4e10 operations.
    # Too slow.

    # Smarter: bookkeep only THE REQUIRED N's (e.g. N=5e3, 1e4, 5e4, 1e5) and
    # for each (d, n_0) walk just enough.
    # Alternative: use the precomputed Tcum to get sum_M T^2 directly, and
    # validate the diagonal at small N with d up to some cap.

    # For 18-min session: just compute sum_M T(M)^2 for several windows from Tcum.
    print(f"\n  Tcum-based second moment over [N+1, 2N]:")
    print(f"  {'N':>10}  {'sum T^2':>14}  {'/N^2':>8}")
    for N in Ns:
        if 2*N > Nbig:
            continue
        s = 0
        for M in range(N+1, 2*N+1):
            s += Tcum[M] * Tcum[M]
        print(f"  {N:>10}  {s:>14}  {s/(N*N):>8.4f}")

    # Now: for ONE small N (say 5000), compute the diagonal sum_d sum_M c_d(M)^2.
    # We'll enumerate (d, n_0) up to d <= 2N.
    print()
    N_diag_list = [1000, 2000, 5000, 10000]
    Nbig_diag = 2 * max(N_diag_list)
    # Enumerate (d, n_0) pairs:
    # Start: list of (d, n_0) = [(1, 0)]
    pairs = [(1, 0)]
    # For each prime p ≡ 1 mod 4 up to Nbig_diag:
    for p in primes_1mod4:
        if p > Nbig_diag:
            break
        # find sqrt(-1) mod p
        m0 = sqrt_m1(p)
        new_pairs = []
        # For existing (d, n_0): for each k>=0, (d * p^k, lift_n_0_to_d*p^k).
        # We append new pairs, but only with d*p^k <= Nbig_diag.
        # The new pair lifts n_0 mod d to mod d*p^k via CRT with the n_0' mod p^k that
        # solves (n_0')^2 ≡ -1 (mod p^k). For p^k with k>=1, there are exactly 2 solutions
        # mod p^k (Hensel). m0 mod p, lifts uniquely as k grows.

        # For p^1: roots are {m0, p - m0}.
        # For p^2 etc.: Hensel lift. We'll just handle k=1 to keep it simple; k>=2
        # contributions are sparse and won't change the asymptotics.

        roots_pk_list = []  # list of (p^k, [roots mod p^k])
        pk = p
        m_pk = [m0, p - m0]
        while pk <= Nbig_diag:
            roots_pk_list.append((pk, list(set(m_pk))))
            # Hensel lift to p^(k+1):
            # if r^2 + 1 ≡ 0 (mod p^k), look for r' = r + t*p^k with t such that
            # 2 r t * p^k ≡ -(r^2 + 1) (mod p^(k+1))
            new_m_pk = []
            pk_next = pk * p
            for r in m_pk:
                # need t s.t. (r + t pk)^2 ≡ -1 (mod pk_next)
                # r^2 + 2 r t pk + (t pk)^2 = r^2 + 2rt pk + O(p^(k+2))
                # so r^2 + 2rt pk ≡ -1 (mod pk_next)
                # 2rt pk ≡ -1 - r^2 (mod pk_next)
                # let delta = (-1 - r^2)/pk (integer divide; this is exactly the residual)
                # delta = (-1 - r^2) // pk (when pk | -1-r^2)
                if (r*r + 1) % pk_next == 0:
                    new_m_pk.append(r)
                    continue
                # Otherwise lift
                resid = (-1 - r*r) // pk
                resid_mod = resid % p
                inv2r = pow(2 * r, -1, p)  # inverse of 2r mod p
                t = (resid_mod * inv2r) % p
                rprime = (r + t * pk) % pk_next
                new_m_pk.append(rprime)
            m_pk = new_m_pk
            pk = pk_next

        # Now for each (d, n0) and each (pk, roots): combine.
        for (d, n0) in pairs:
            for (pk, rs) in roots_pk_list:
                if d * pk > Nbig_diag:
                    break
                for r in rs:
                    # CRT: find x mod d*pk with x ≡ n0 (d), x ≡ r (pk).
                    # We use: x = n0 * pk * (pk inv mod d) + r * d * (d inv mod pk).
                    if d == 1:
                        x = r % pk
                    else:
                        inv_pk = pow(pk, -1, d)
                        inv_d = pow(d, -1, pk)
                        x = (n0 * pk * inv_pk + r * d * inv_d) % (d * pk)
                    new_pairs.append((d * pk, x))
        # add the new ones to pairs (NOT to be re-multiplied this round; multiplication is
        # over distinct primes via this BFS layer)
        pairs.extend(new_pairs)
    print(f"  enumerated {len(pairs)} (d, n_0) pairs with d <= {Nbig_diag}", flush=True)

    # Compute the AP-diagonal: for each d, sum_M c_d(M)^2 with c_d(M) = sum_{n_0} S_{M,d}(n_0)
    # But pairs is a flat list; group by d.
    from collections import defaultdict
    by_d = defaultdict(list)
    for (d, n0) in pairs:
        by_d[d].append(n0)

    print(f"  {len(by_d)} distinct d's", flush=True)

    # For diagonal at N=N_diag: sum over d <= 2N_diag of sum_M c_d(M)^2 over M in [N+1..2N].
    # We need S_{M,d}(n_0) for each (d, n_0) and M in [N+1..2N_diag].
    # Compute S incrementally: S grows as M increases by chi_4(M+1) when M ≡ n_0 (mod d) and M >= d.

    print(f"  {'N':>8}  {'direct':>12}  {'AP-diag':>12}  {'true-diag':>12}  {'/N^2 dir':>10}  {'/N^2 AP':>10}  {'/N^2 TD':>10}")
    for N_diag in N_diag_list:
        # We need d <= 2*N_diag.
        diag_sum = 0
        diag_TD = 0
        for d, n0_list in by_d.items():
            if d > 2*N_diag:
                continue
            S_per_n0 = {n0: 0 for n0 in n0_list}
            sum_c2 = 0
            sum_S2 = 0
            for M in range(1, 2*N_diag+1):
                for n0 in n0_list:
                    if M >= d and (M - n0) % d == 0:
                        S_per_n0[n0] += chi4(M+1)
                if N_diag < M <= 2*N_diag:
                    c = sum(S_per_n0.values())
                    sum_c2 += c*c
                    sum_S2 += sum(s*s for s in S_per_n0.values())
            diag_sum += sum_c2
            diag_TD += sum_S2
        diag_sum *= 4
        diag_TD *= 4
        s_direct = sum(Tcum[M]*Tcum[M] for M in range(N_diag+1, 2*N_diag+1))
        print(f"  {N_diag:>8}  {s_direct:>12}  {diag_sum:>12}  {diag_TD:>12}  {s_direct/(N_diag**2):>10.4f}  {diag_sum/(N_diag**2):>10.4f}  {diag_TD/(N_diag**2):>10.4f}")

if __name__ == '__main__':
    compute([1000, 5000, 10000, 50000])
