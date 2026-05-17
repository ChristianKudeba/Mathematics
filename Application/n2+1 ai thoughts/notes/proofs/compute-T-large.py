"""
Fast computation of T(N) = sum_{n<=N} tau(n^2+1) * chi_4(n+1).
Uses a sieve approach: for each prime p, mark which n in [1, N] have p | n^2+1.
"""
import math
import time

def chi4(n):
    n = n % 4
    if n == 1: return 1
    if n == 3: return -1
    return 0

def primes_up_to(B):
    """Return primes <= B using sieve of Eratosthenes."""
    sieve = bytearray([1]) * (B+1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(B**0.5)+1):
        if sieve[i]:
            for j in range(i*i, B+1, i):
                sieve[j] = 0
    return [i for i in range(B+1) if sieve[i]]

def tonelli_shanks_minus1(p):
    """Find n such that n^2 ≡ -1 (mod p), for prime p ≡ 1 (mod 4).
    Use Cipolla or simpler: check x^((p-1)/4) for primitive roots..."""
    # Find any quadratic non-residue z, then compute z^((p-1)/4) which is a 4th root of unity != ±1.
    # Then n = z^((p-1)/4) is one solution.
    if p == 2:
        return 1  # 1^2 ≡ 1 ≡ -1 mod 2
    if p % 4 != 1:
        return None
    for z in range(2, p):
        if pow(z, (p-1)//2, p) == p-1:  # quadratic non-residue
            return pow(z, (p-1)//4, p)
    return None

def tau_n2_plus_1_array(N):
    """Returns array of tau(n^2+1) for n = 0, 1, ..., N."""
    # M = n^2 + 1 for n in [1, N], so M in [2, N^2+1]
    # The primes dividing M are: 2, and primes p ≡ 1 mod 4 with p ≤ N^2+1
    # and a prime p divides n^2+1 iff n ≡ ±n_0 (mod p) for n_0 = sqrt(-1 mod p)
    # For each prime p with such an n_0, mark n ≡ ±n_0 (mod p)

    # Approach: maintain residual array R[n] = (n^2+1) / (already-divided primes)
    # For each prime, divide out all powers from R[n] for n in the AP.
    # tau(M) = product of (e_i + 1) where M = prod p_i^{e_i}.

    # But computing tau requires tracking each prime's multiplicity.
    # Easier: precompute all (n^2+1) values, factor each.

    tau = [0] * (N+1)
    R = [0] * (N+1)  # R[n] = remaining factor after dividing out small primes
    # tau will track running tau as primes are processed

    # Initialize R[n] = n^2 + 1
    for n in range(1, N+1):
        R[n] = n*n + 1
    # Initialize tau[n] = 1
    for n in range(1, N+1):
        tau[n] = 1

    # Handle p = 2: 2 | n^2+1 iff n odd. Multiplicity is 1 (since n^2+1 ≡ 2 mod 4 for n odd).
    for n in range(1, N+1, 2):
        R[n] //= 2
        tau[n] *= 2  # exponent 1 → factor (1+1)=2

    # For primes p ≡ 1 mod 4 up to N (since p ≤ n^2+1 and we need p | n^2+1 for some n ≤ N
    # the relevant primes are those ≡ 1 mod 4 with p ≤ N^2+1, but for small primes we sieve fully,
    # then handle large primes p > N differently.

    # Actually each n^2+1 has at most one prime factor > N (since 2 such factors would make n^2+1 > N^2 ≥ n^2+1, contradiction unless n is small).

    # Hmm actually for n^2+1 ≤ N^2+1, prime factors can be up to ~N^2. So a single prime factor could be up to ~N^2. But we can sieve primes up to N to handle small factors, then any remaining R[n] > 1 is either prime or a square of prime. Most likely prime.

    # Sieve primes up to N
    primes = primes_up_to(N)
    for p in primes:
        if p == 2 or p % 4 != 1:
            continue
        n_0 = tonelli_shanks_minus1(p)
        if n_0 is None:
            continue
        # n_0 might be > p/2, take the smaller representative
        if 2*n_0 > p:
            n_0 = p - n_0
        # Now mark n ≡ ±n_0 (mod p)
        for offset in [n_0, p - n_0] if n_0 != 0 else [n_0]:
            n = offset
            while n <= N:
                if n >= 1:
                    # Find multiplicity of p in n^2+1
                    e = 0
                    while R[n] % p == 0:
                        R[n] //= p
                        e += 1
                    if e > 0:
                        tau[n] *= (e + 1)
                n += p

    # For each n with R[n] > 1: R[n] is a remaining prime factor (or product, but rare)
    for n in range(1, N+1):
        if R[n] > 1:
            # Most often R[n] is a single prime > N
            # If R[n] is a square, like p^2 with p > sqrt(R[n])... let's check
            r = R[n]
            sr = int(r**0.5)
            if sr * sr == r:
                # R[n] = p^2 for some prime p
                tau[n] *= 3  # exponent 2 → factor 3
            else:
                tau[n] *= 2  # exponent 1 → factor 2

    return tau

print('N         T(N)        |T(N)|/sqrt(N)   |T(N)|/log(N)')
for N in [1000, 5000, 10000, 50000, 100000, 500000, 1000000]:
    t0 = time.time()
    tau = tau_n2_plus_1_array(N)
    T = 0
    for n in range(1, N+1):
        T += tau[n] * chi4(n+1)
    elapsed = time.time() - t0
    sqrtN = math.sqrt(N)
    print(f'{N:8d}  {T:8d}     {abs(T)/sqrtN:.4f}        {abs(T)/math.log(N):.4f}    [{elapsed:.1f}s]')
