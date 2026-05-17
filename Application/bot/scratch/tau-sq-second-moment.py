"""
Numerical verification of the conjectured asymptotic
    sum_{n<=N} tau(n^2+1)^2  ~  C * N * (log N)^3
where C = pi^3 * H(1) / 48 and H(1) is an explicit Euler product:
    H(1) = (5/16)
         * prod_{p=3 mod 4} (1 - p^{-2})^3
         * prod_{p=1 mod 4} (1 - p^{-1})^4 * (1 + 4/p - 1/p^2)

We compute S(N) by sieve-factoring n^2+1 for n<=N, summing tau(n^2+1)^2.
"""
import math

def primerange(a, b):
    """Primes p with a <= p < b. Simple sieve."""
    if b <= 2: return
    sieve_arr = bytearray([1]) * b
    sieve_arr[0] = sieve_arr[1] = 0
    for i in range(2, int(b**0.5) + 1):
        if sieve_arr[i]:
            for j in range(i*i, b, i):
                sieve_arr[j] = 0
    for i in range(max(a, 2), b):
        if sieve_arr[i]:
            yield i

class _Sieve:
    def primerange(self, a, b):
        return primerange(a, b)
sieve = _Sieve()

def compute_both(N):
    """Returns (sum_{n<=N} tau(n^2+1)^2, sum_{n<=N} tau(n^2+1))."""
    from array import array
    vals = [n*n + 1 for n in range(N + 1)]
    tau = array('q', [1] * (N + 1))
    p_bound = N + 5
    primes = list(sieve.primerange(2, p_bound + 1))
    for p in primes:
        if p == 2:
            roots = [1]
        elif p % 4 == 3:
            continue
        else:
            r = None
            for x in range(1, p):
                if (x*x + 1) % p == 0:
                    r = x
                    break
            roots = [r, p - r]
        for r in roots:
            n = r if r <= N else None
            if n is None:
                continue
            while n <= N:
                v = vals[n]
                e = 0
                while v % p == 0:
                    v //= p
                    e += 1
                vals[n] = v
                tau[n] *= (e + 1)
                n += p
    for n in range(1, N + 1):
        if vals[n] > 1:
            tau[n] *= 2
    S2 = 0
    S1 = 0
    for n in range(1, N + 1):
        t = tau[n]
        S2 += t * t
        S1 += t
    return S2, S1

def compute_S(N):
    # tau(m) for m = n^2+1, n=1..N.
    # Strategy: sieve n^2+1 over primes p<=N^2+1 with rho(p)>0.
    # Use vals[n] = n^2+1 (mutable), and tau-counter per n.
    from array import array
    vals = [n*n + 1 for n in range(N + 1)]
    tau = array('q', [1] * (N + 1))
    # sieve primes up to sqrt(N^2+1) ~ N (only need primes up to N for residual extraction;
    # any leftover val[n] > 1 after sieving is itself prime).
    p_bound = N + 5
    primes = list(sieve.primerange(2, p_bound + 1))
    for p in primes:
        if p == 2:
            roots = [1]
        elif p % 4 == 3:
            continue  # rho(p) = 0
        else:
            # find one root of x^2 = -1 mod p
            r = None
            for x in range(1, p):
                if (x*x + 1) % p == 0:
                    r = x
                    break
            roots = [r, p - r]
        for r in roots:
            # n with n ≡ r mod p, n <= N
            n = r if r <= N else None
            if n is None:
                continue
            while n <= N:
                v = vals[n]
                # extract all powers of p
                e = 0
                while v % p == 0:
                    v //= p
                    e += 1
                vals[n] = v
                tau[n] *= (e + 1)
                n += p
    # any remaining vals[n] > 1 is a single prime (since n^2+1 < (N+1)^2 and
    # we sieved primes up to ~N, any prime factor > N appears exactly once).
    for n in range(1, N + 1):
        if vals[n] > 1:
            tau[n] *= 2
    S = 0
    for n in range(1, N + 1):
        S += tau[n] * tau[n]
    return S

def H_at_1(P):
    """Euler product H(1) truncated to primes p <= P."""
    H = 5.0 / 16.0
    for p in sieve.primerange(3, P + 1):
        if p % 4 == 3:
            H *= (1.0 - 1.0/(p*p)) ** 3
        elif p % 4 == 1:
            H *= (1.0 - 1.0/p) ** 4 * (1.0 + 4.0/p - 1.0/(p*p))
    return H

def main():
    # Constant
    P_max = 10**6
    H1 = H_at_1(P_max)
    print(f"H(1) truncated to primes <= {P_max}:  {H1:.10f}")
    C = math.pi**3 * H1 / 48.0
    print(f"Predicted C = pi^3 * H(1) / 48 = {C:.10f}\n")

    Ns = [10**3, 3*10**3, 10**4, 3*10**4, 10**5, 3*10**5, 10**6]
    Ctau = 3.0/math.pi
    print(f"Ctau = 3/pi = {Ctau:.6f}\n")
    print(f"{'N':>10} {'S(tau^2)':>15} {'S/(N log^3)':>15} {'ratio C':>10} | {'S(tau)':>14} {'S/(N log)':>14} {'ratio Ctau':>10}")
    for N in Ns:
        S2, S1 = compute_both(N)
        denom2 = N * math.log(N)**3
        denom1 = N * math.log(N)
        emp2 = S2 / denom2
        emp1 = S1 / denom1
        r2 = emp2 / C
        r1 = emp1 / Ctau
        print(f"{N:>10} {S2:>15} {emp2:>15.6f} {r2:>10.4f} | {S1:>14} {emp1:>14.6f} {r1:>10.4f}")

if __name__ == "__main__":
    main()
