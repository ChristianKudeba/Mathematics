"""
Fast computation of T(N) = sum_{n=1..N} tau(n^2+1) * chi_4(n+1)
across many sample points up to N ~ 10^8.

Strategy: do a single full sieve up to N_max, then compute T at any
intermediate N by partial summing the precomputed contributions.

Memory: arrays of size N_max ~ 10^8 of int64 -> ~800 MB. We will use
N_max = 5 * 10^7 to stay under memory budget but still extend the
empirical regime by ~5x past N=10^7.
"""
import math
import time
import sys

def chi4(n):
    n = n & 3
    if n == 1: return 1
    if n == 3: return -1
    return 0

def primes_up_to(B):
    sieve = bytearray([1]) * (B+1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(B**0.5)+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00' * len(sieve[i*i::i])
    return [i for i in range(B+1) if sieve[i]]

def sqrt_minus1_mod_p(p):
    """For prime p == 1 mod 4, find x with x^2 ≡ -1 mod p."""
    for z in range(2, p):
        if pow(z, (p-1)//2, p) == p-1:
            return pow(z, (p-1)//4, p)
    return None

def compute_T_array(N_max):
    """Compute c[n] = tau(n^2+1) * chi_4(n+1) for n=1..N_max, plus
    cumulative T[n] = sum_{k=1..n} c[k]. Skip multiplications when
    chi_4(n+1)=0 (n odd), since then c[n]=0."""
    print(f"Sieving up to N_max={N_max}", flush=True)
    t0 = time.time()

    # We only need tau(n^2+1) for n EVEN (since n odd ⇒ chi_4(n+1)=0).
    # For n odd we set tau=0 implicitly.

    # Use exponent-vector approach: maintain R[n] = residual of n^2+1 after
    # dividing out small primes; tau[n] = product of (e_p+1) so far.
    # Allocate only over even n for memory; index by k = n/2, n = 2k.

    # n = 2k, k=1..N_max/2.  n^2+1 = 4k^2+1 (always odd, so 2 never divides).

    K = N_max // 2
    print(f"  even slots: K={K}", flush=True)
    tau = [1] * (K+1)   # tau[k] = tau(4k^2+1) running
    # R[k] uses Python ints; can be large up to (2K)^2+1 ~ 4*K^2
    # That is ~ 4 * (5e7)^2 = 1e16 -> fits in int64
    R = [4*k*k + 1 for k in range(K+1)]
    R[0] = 1  # ignore k=0
    tau[0] = 0

    print(f"  R[] init done ({time.time()-t0:.1f}s)", flush=True)

    # Sieve primes up to 2*K = N_max
    primes = primes_up_to(N_max)
    print(f"  sieved {len(primes)} primes up to {N_max} ({time.time()-t0:.1f}s)", flush=True)

    # For each prime p ≡ 1 mod 4: solve 4k^2 + 1 ≡ 0 mod p, i.e., k^2 ≡ -1/4 mod p
    # Equivalently, (2k)^2 ≡ -1 mod p. Let m_0 = sqrt(-1) mod p, then 2k ≡ ±m_0 mod p.
    # If p odd, 2 invertible mod p, so k ≡ ±m_0/2 mod p.
    skipped = 0
    for p in primes:
        if p % 4 != 1:
            continue
        m0 = sqrt_minus1_mod_p(p)
        if m0 is None:
            skipped += 1
            continue
        inv2 = pow(2, p-2, p)
        k0 = (m0 * inv2) % p
        # The two roots are k0 and (p - k0) mod p
        roots = {k0, (p - k0) % p}
        for r in roots:
            k = r if r >= 1 else r + p
            while k <= K:
                # divide out all powers of p
                if R[k] % p == 0:
                    e = 0
                    while R[k] % p == 0:
                        R[k] //= p
                        e += 1
                    tau[k] *= (e + 1)
                k += p

    print(f"  prime sieve done ({time.time()-t0:.1f}s)", flush=True)

    # For each k, the residual R[k] > 1 is a single remaining large prime.
    # Justification: (i) only primes p ≡ 1 mod 4 with p ≤ N_max have been
    # divided out (we skip p ≡ 3 mod 4 because they never divide n^2+1, and
    # 4k^2+1 is odd so p=2 never divides). (ii) Any remaining prime factor
    # q of 4k^2+1 must therefore satisfy q ≡ 1 mod 4 (since 4k^2+1's prime
    # factors are exactly {2 if 2|m} ∪ {p ≡ 1 mod 4}, and 2 is excluded for
    # m=4k^2+1 odd) and q > N_max. (iii) Two such q1, q2 would force
    # R[k] ≥ q1·q2 ≥ (N_max+1)(N_max+2) > N_max^2 + 1 ≥ 4K^2+1 = max possible,
    # contradiction. (iv) q^2 with q > N_max gives R[k] ≥ (N_max+1)^2 >
    # 4K^2+1, contradiction. So if R[k] > 1, R[k] is a single prime ≡ 1 mod 4
    # with multiplicity 1 in 4k^2+1, contributing factor 2 to tau.
    for k in range(1, K+1):
        if R[k] > 1:
            tau[k] *= 2

    print(f"  residuals done ({time.time()-t0:.1f}s)", flush=True)

    # T(N) for N=2k_max even: sum_{k=1..k_max} (-1)^k * tau(4k^2+1)
    # because chi_4(2k+1) = +1 if k even, -1 if k odd (i.e., (-1)^k):
    #   2k+1 ≡ 1 (mod 4) iff k even ⇒ chi_4 = +1
    #   2k+1 ≡ 3 (mod 4) iff k odd  ⇒ chi_4 = -1
    # So contribution at n=2k is (-1)^k * tau(4k^2+1).
    # For n=2k+1 odd, contribution is 0.
    # T(N) for general N: T(N) = T(2*floor(N/2)).

    print(f"  computing cumulative T[] ...", flush=True)
    Tcum = [0] * (K+1)
    s = 0
    for k in range(1, K+1):
        s += (-1 if (k & 1) else 1) * tau[k]
        Tcum[k] = s

    print(f"  done in {time.time()-t0:.1f}s total", flush=True)
    return tau, Tcum  # Tcum[k] = T(2k)

def main():
    N_max = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000
    tau, Tcum = compute_T_array(N_max)

    K = N_max // 2

    # Print T at logarithmically spaced sample points
    print()
    print("N            T(N)              T/sqrt(N)    T/(sqrt(N) log N)")
    samples = []
    for exp in range(3, 9):
        for c in [1, 2, 3, 5, 7]:
            N = c * 10**exp
            if N <= N_max:
                samples.append(N)
    samples.append(N_max)
    samples = sorted(set(samples))

    for N in samples:
        k = N // 2
        if k < 1 or k > K:
            continue
        T = Tcum[k]
        sN = math.sqrt(N)
        lnN = math.log(N)
        print(f"{N:>11d}  {T:>14d}    {T/sN:>+10.4f}    {T/(sN*lnN):>+10.4f}")

    # Save Tcum to disk for further analysis
    import pickle
    out = '/home/user/mathAI/bot/scratch/Tcum.pkl'
    # Only save sparsely (every 100k) to keep file small
    sparse = [(2*k, Tcum[k]) for k in range(0, K+1, max(1, K // 50000))]
    with open(out, 'wb') as f:
        pickle.dump(sparse, f)
    print(f"\nSaved {len(sparse)} sparse samples to {out}")

if __name__ == '__main__':
    main()
