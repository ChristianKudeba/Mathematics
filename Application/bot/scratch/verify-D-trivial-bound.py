"""
Verify the trivial bound D(N) <= 4 N * sum_{d <= 2N, L_odd} 4^omega(d).

Compute sum_{d <= x, L_odd} 4^omega(d) for x = 1e3, 1e4, 1e5, 1e6 and check:
1. the leading asymptotic C * x * log(x) with C = pi^2/16 * G(1).
2. the resulting upper bound on D(N) is loose by a factor of log(N).
"""

import math

def main():
    Xs = [1000, 10000, 100000, 1000000]
    Xmax = max(Xs)
    sieve = bytearray([1])*(Xmax+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(Xmax))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    primes = [p for p in range(Xmax+1) if sieve[p]]
    primes_1mod4 = [p for p in primes if p%4 == 1]

    # omega(d) for d in L_odd: count distinct prime factors of d (all ≡ 1 mod 4).
    # Also need to check d is in L_odd.
    in_L = [False]*(Xmax+1)
    omega = [0]*(Xmax+1)
    in_L[1] = True
    for p in primes_1mod4:
        pk = p
        while pk <= Xmax:
            for d in range(pk, Xmax+1, pk):
                if d == pk:
                    # First time we hit d = pk, increment omega and mark.
                    pass  # handled below
            pk *= p
    # Simpler: factorize each d up to Xmax.
    # For each d, factorize.
    omega = [0]*(Xmax+1)
    in_L = [True]*(Xmax+1); in_L[0] = False
    for p in primes:
        for d in range(p, Xmax+1, p):
            omega[d] += 1
            if p % 4 != 1:
                in_L[d] = False

    # Sum 4^omega(d) over d <= x, d in L_odd.
    cum = 0
    print(f"  {'x':>10}  {'sum':>14}  {'/x log x':>12}  {'/(x (log x)^k)':>10}")
    pow4 = [4**k for k in range(30)]
    for x in Xs:
        # Recompute by sweep.
        s = 0
        for d in range(1, x+1):
            if in_L[d]:
                s += pow4[omega[d]]
        s_normalized = s / (x * math.log(x))
        print(f"  {x:>10}  {s:>14}  {s_normalized:>12.6f}")

    # Compute G(1) numerically via Euler product up to large prime.
    # G(s) = (1 - 2^{-s})^2 * prod_{p≡3(4)}(1-p^{-2s})^2 * prod_{p≡1(4)}(1+3p^{-s})(1-p^{-s})^3
    # At s = 1:
    G1 = (1 - 0.5)**2  # p=2 factor
    for p in primes:
        if p == 2:
            continue
        if p % 4 == 3:
            G1 *= (1 - 1/p**2)**2
        elif p % 4 == 1:
            G1 *= (1 + 3/p) * (1 - 1/p)**3
        else:
            assert False
        if p > 100000:
            break
    C = (math.pi**2) * G1 / 16
    print(f"\n  Estimated G(1) = {G1:.4f}")
    print(f"  Estimated C    = pi^2 G(1)/16 = {C:.4f}")
    print(f"  Predicted leading term:  sum/(x log x) -> {C:.4f}")

if __name__ == '__main__':
    main()
