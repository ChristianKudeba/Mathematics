"""
Verify: sum_{d<=x, L_odd} 2^omega(d) ~ x/pi.
L_odd = positive integers all of whose prime factors are p ≡ 1 (mod 4).
Tests the closed-form constant 1/pi derived from Dedekind zeta of Q(i):
  F(s) = sum_{d in L_odd} 2^omega(d) / d^s
       = zeta_K(s) / (zeta(2s) (1 + 2^{-s}))
  Res_{s=1} F(s) = (pi/4) / ((pi^2/6)(3/2)) = 1/pi.
"""
import math, time, sys

def main(xmax):
    sieve = bytearray([1])*(xmax+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(xmax))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    primes = [p for p in range(xmax+1) if sieve[p]]
    primes_1mod4 = [p for p in primes if p % 4 == 1]
    primes_3mod4 = set(p for p in primes if p % 4 == 3)
    primes_3mod4.add(2)

    # smallest prime factor + omega indicator of L_odd membership
    spf = list(range(xmax+1))
    for p in primes:
        if p > xmax: break
        for j in range(p, xmax+1, p):
            if spf[j] == j:
                spf[j] = p

    # for each d, factor and check (a) all prime factors p ≡ 1 (mod 4), (b) compute omega
    in_Lodd = bytearray(xmax+1)
    omega = [0]*(xmax+1)
    in_Lodd[1] = 1
    for d in range(2, xmax+1):
        n = d
        ok = True
        last_p = 0
        w = 0
        while n > 1:
            p = spf[n]
            if p % 4 != 1:
                ok = False; break
            if p != last_p:
                w += 1; last_p = p
            n //= p
        if ok:
            in_Lodd[d] = 1
            omega[d] = w

    # cumulative sum
    S = 0
    targets = [10**3, 5*10**3, 10**4, 5*10**4, 10**5, 5*10**5, 10**6, 5*10**6]
    targets = [t for t in targets if t <= xmax]
    print(f"{'x':>10} {'sum 2^om(d)':>14} {'sum/x':>10} {'pred 1/pi':>10} {'rel err %':>10}")
    next_t = iter(sorted(targets))
    target = next(next_t, None)
    for d in range(1, xmax+1):
        if in_Lodd[d]:
            S += (1 << omega[d])
        if target is not None and d == target:
            ratio = S / d
            err = (ratio - 1/math.pi) / (1/math.pi) * 100
            print(f"{d:>10} {S:>14} {ratio:>10.6f} {1/math.pi:>10.6f} {err:>+10.3f}")
            target = next(next_t, None)

if __name__ == '__main__':
    xmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
    t0 = time.time()
    main(xmax)
    print(f"time: {time.time()-t0:.1f}s")
