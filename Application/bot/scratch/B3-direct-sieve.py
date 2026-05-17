"""
Direct sieve for the Hooley-boundary sum
    B_3(N) := sum_{d <= N^2+1} 2^omega(d) * delta_d(N)
            = S_3(N) - N * Sigma_3(N^2+1)
where
    S_3(N)         := sum_{n <= N} tau((n^2+1)^2)
    Sigma_3(X)     := sum_{d <= X} 2^omega(d) rho(d) / d
    delta_d(N)     := N_d(N) - rho(d) N/d
    N_d(N)         := #{n <= N : d | n^2+1}
    rho(d)         := #{x mod d : x^2 = -1 mod d}

Identity used: tau(m^2) = sum_{d|m} 2^omega(d), so
    S_3(N) = sum_{n <= N} sum_{d | n^2+1} 2^omega(d)
           = sum_{d <= N^2+1} 2^omega(d) * N_d(N).
And N_d(N) = rho(d) N/d + delta_d(N), giving the boundary identity above.

This script computes both S_3 and Sigma_3 by linear sieve up to N_max^2.
Memory: array of int64 of size N_max^2, so ~ 8 N_max^2 bytes.
For N_max = 10^4 this is 800 MB -- too much for a 30 min session in this
sandbox. We instead enumerate supported d recursively (d = 2^a * m,
a in {0,1}, m with only primes p == 1 mod 4 to any power).
"""
import math, time, sys

def primes_up_to(M):
    """Sieve of Eratosthenes."""
    if M < 2:
        return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]

def split_primes_up_to(M):
    """Primes p == 1 (mod 4), p <= M."""
    return [p for p in primes_up_to(M) if p % 4 == 1]

def enumerate_supported_d(X):
    """Yield (d, f(d)) for all d <= X with f(d) > 0,
       where f(d) = 2^omega(d) * rho(d).

       Support: d = 2^a * m, a in {0,1}, m = product of p_i^{e_i} with
       p_i == 1 mod 4. f(2^a * m) = 2^a * 4^omega(m).
    """
    sp = split_primes_up_to(X)
    # Recursively enumerate: pick subset of split primes with multiplicities.
    # We need to be careful: for primes p > sqrt(X), only e=1 contributes.

    # DFS: for each prime in sp (ordered increasing), choose exponent e >= 0.
    # When p > X/m, we've exhausted the subtree.
    results = []  # list of (m, 4^omega(m)) for odd m
    # Recursion via stack:
    def recurse(idx, m, w):
        # m = current odd factor, w = number of distinct split primes used
        results.append((m, 1 << (2*w)))  # 4^w
        for j in range(idx, len(sp)):
            p = sp[j]
            if p * m > X:
                break
            mp = m * p
            new_w = w + 1
            while mp <= X:
                recurse(j + 1, mp, new_w)
                mp *= p
                if mp > X:
                    break
    sys.setrecursionlimit(10**6)
    recurse(0, 1, 0)
    # Now pair with a in {0,1}: d = m, f(d) = 4^w; d = 2m, f(d) = 2 * 4^w.
    out = []
    for (m, fw) in results:
        if m <= X:
            out.append((m, fw))
        if 2 * m <= X:
            out.append((2 * m, 2 * fw))
    return out

def compute_sigma3_at_breakpoints(X_max, breakpoints):
    """Return dict bp -> Sigma_3(bp) for each bp in breakpoints (bp <= X_max).

       Streams supported d through the recursion, accumulating into running
       sums for each breakpoint.  Does NOT materialize the full list, so
       memory is O(#breakpoints + log X_max).
    """
    print(f"Enumerating supported d up to {X_max} ...", flush=True)
    t0 = time.time()
    sp = split_primes_up_to(X_max)
    bps = sorted(breakpoints)
    sums = [0.0] * len(bps)
    count = [0]

    sys.setrecursionlimit(10**6)

    def recurse(idx, m, w):
        # m = current odd factor, w = number of distinct split primes used.
        # Contribution at d = m: f = 4^w; at d = 2m: f = 2 * 4^w.
        fw = 1 << (2 * w)
        # accumulate into all sums with bp >= 2m (and bp >= m)
        # Find smallest bp with bp >= m via linear scan (small list)
        for i in range(len(bps)):
            if bps[i] >= m:
                sums[i] += fw / m
            if bps[i] >= 2*m:
                sums[i] += (2*fw) / (2*m)  # = fw/m, but kept for clarity
        count[0] += 2 if 2*m <= X_max else 1
        for j in range(idx, len(sp)):
            p = sp[j]
            if p * m > X_max:
                break
            mp = m * p
            new_w = w + 1
            while mp <= X_max:
                recurse(j + 1, mp, new_w)
                mp *= p
                if mp > X_max:
                    break

    recurse(0, 1, 0)
    print(f"  visited {count[0]} supported d; {time.time()-t0:.1f}s", flush=True)
    return {bp: sums[i] for i, bp in enumerate(bps)}

def compute_S3(N_max):
    """Compute S_3(N) = sum_{n <= N} tau((n^2+1)^2) cumulative for n = 1..N_max.

       Use sieve: for each prime p and each k with p^k | n^2+1 for some n,
       enumerate all such n in [1, N_max].
       Then for each n, build the prime-power decomposition of n^2+1 and
       compute tau((n^2+1)^2) = prod (2 e_i + 1).
    """
    # Approach: for each n, factor n^2+1 by trial division using primes p
    # with p^2 <= n^2+1, i.e. p <= n (or sqrt(n^2+1)). We only need to try
    # primes p == 1 mod 4 (and p = 2 once: 2 | n^2+1 iff n odd).
    # After trial division we have a residue r. r is either 1, a prime > n,
    # or a prime > sqrt(n^2+1) -- but since after dividing out all primes
    # <= n, r > n, hence r is prime (since r <= n^2+1 < (n+1)^2 means r
    # has only one prime factor > n, and r itself, if composite, would be
    # a product of primes > n which is at least n^2+1+ ...) actually if
    # n^2+1 has only one prime factor > n and the rest <= n, then after
    # dividing out all <= n, residue r is the prime factor > n (or 1).
    # Wait but residue could be a prime power r = q^k with q > n. Then
    # q^k <= n^2+1 < (n+1)^2 forces k <= 2 and q <= n. But q > n by
    # assumption -- so k = 1.

    # For p == 1 mod 4, the solutions of x^2 == -1 mod p^k can be
    # generated by Hensel lift. For k = 1 we find x_0 by Tonelli-Shanks
    # or by random search.
    #
    # But simpler: just iterate n from 1 to N_max, factor n^2+1 by trial.

    primes = [2] + split_primes_up_to(N_max)
    # We need primes p == 1 mod 4 up to n_max for trial division (since
    # p == 3 mod 4 never divides n^2+1).
    # Also p = 2.

    S3_cum = [0] * (N_max + 1)
    s = 0
    for n in range(1, N_max + 1):
        m = n*n + 1
        tau_sq = 1
        # Trial divide by 2:
        e = 0
        while m % 2 == 0:
            m //= 2
            e += 1
        # 2 | n^2+1 iff n odd, in which case e = 1 (since n odd => n^2 == 1 mod 8 => n^2+1 == 2 mod 8 => exactly e=1)
        if e:
            tau_sq *= (2*e + 1)
        # Trial divide by primes p == 1 mod 4 with p <= n:
        for p in primes[1:]:
            if p > n:
                break
            if m % p == 0:
                e = 0
                while m % p == 0:
                    m //= p
                    e += 1
                tau_sq *= (2*e + 1)
        # Residue m: if m > 1, m is a prime > n (or = 1).
        if m > 1:
            tau_sq *= 3  # 2*1 + 1 = 3 for one factor of a prime to the first
        s += tau_sq
        S3_cum[n] = s
    return S3_cum

if __name__ == "__main__":
    # Constants from prior session
    H3_1     = 0.27775120
    H3_p1    = 0.84240798
    H3_pp1   = -0.234
    gamma_K  = 0.6462
    beta_K   = 0.0915
    R        = math.pi/4
    c2 = R**2 * H3_1
    c1 = R**2 * H3_p1 + 2*R*gamma_K * H3_1
    c0 = R**2 * H3_pp1/2 + 2*R*gamma_K*H3_p1 + (gamma_K**2 + 2*R*beta_K)*H3_1

    Ns = [500, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 30000]
    N_max = max(Ns)
    X_max = N_max * N_max + 1

    print(f"=== Computing Sigma_3(N^2+1) for N in {Ns}, max X = {X_max} ===")
    print()
    breakpoints = [N*N + 1 for N in Ns]
    sigma3_at = compute_sigma3_at_breakpoints(X_max, breakpoints)
    print("Sigma_3(N^2+1) at breakpoints:")
    for N in Ns:
        print(f"  N={N:>6}, Sigma_3({N*N+1}) = {sigma3_at[N*N+1]:.8f}")
    print()

    print(f"=== Computing S_3(N) for n <= {N_max} ===")
    t0 = time.time()
    S3 = compute_S3(N_max)
    print(f"  done; {time.time()-t0:.1f}s")
    print()
    for N in Ns:
        print(f"  S_3({N}) = {S3[N]}")
    print()

    print("=== B_3(N) and B_3/N ===")
    print(f"{'N':>6} {'S_3(N)':>14} {'N*Sigma_3':>16} {'B_3(N)':>14} {'B_3/N':>10} {'pred(N)':>14} {'S_3-pred':>12} {'(S_3-pred)/N':>13}")
    for N in Ns:
        L = math.log(N)
        sigma3 = sigma3_at[N*N+1]
        nSigma = N * sigma3
        B3 = S3[N] - nSigma
        # 3-term Laurent prediction for S_3(N):
        pred = 2*c2*N*L*L + 2*c1*N*L + c0*N
        diff = S3[N] - pred
        print(f"{N:>6} {S3[N]:>14} {nSigma:>16.4f} {B3:>14.4f} {B3/N:>10.4f} {pred:>14.4f} {diff:>12.4f} {diff/N:>13.4f}")
