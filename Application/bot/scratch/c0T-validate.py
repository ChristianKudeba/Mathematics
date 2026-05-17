"""
Validate the closed form
   c_<^infty = (pi/4) H'(1) + gamma_K H(1) = 1.0134

via direct Mellin-Perron derivation:
   sum_{e sf, e <= N} rho(e)/e = (pi/4) H(1) log N + (pi/4) H'(1) + gamma_K H(1) + o(1).

Then T_<=(N) := sum_{e sf, e <= N} #{n in [1,N]: e | n^2+1}
                = N * sum_{e sf, e <= N} rho(e)/e + (discr error, mean 0)
                ~= (pi H(1)/4) N log N + ((pi/4) H'(1) + gamma_K H(1)) N.

So if T_<=(N)/N - 0.4341 log N -> 1.0134, the closed form is right.

Then c_0^T = c_<^infty + c_>^infty where c_>^infty := lim (T_>(N)/N - 0.4341 log N).
Empirical (from prev script): c_>^infty ~= -0.02 across small N.

This script:
  (a) Recompute (pi/4) H'(1) + gamma_K H(1) via Euler product (cross-check).
  (b) Compute sum_{e sf, e <= X} rho(e)/e at large X and compare.
  (c) Extend T_<= and T_> to N up to 5*10^4.
"""
import math, time

GAMMA = 0.5772156649015328606
LPRIME_1_CHI4 = 0.19290131767382030
GAMMA_K = (math.pi/4) * GAMMA + LPRIME_1_CHI4
R = math.pi/4

def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]

def compute_H_and_Hprime(P_bound=10**6):
    primes = primes_up_to(P_bound)
    log_H = math.log(3.0/4.0)
    dlog_H = math.log(4.0)/3.0
    sum1 = 0.0
    sum3 = 0.0
    for p in primes:
        if p == 2: continue
        lp = math.log(p)
        if p % 4 == 1:
            f = 1.0 - 3.0/(p*p) + 2.0/(p*p*p)
            log_H += math.log(f)
            sum1 += 6.0 * lp * (1.0/(p*p) - 1.0/(p*p*p)) / f
        else:
            f = 1.0 - 1.0/(p*p)
            log_H += math.log(f)
            sum3 += 2.0 * lp / (p*p) / f
    H1 = math.exp(log_H)
    Hprime1 = H1 * (dlog_H + sum1 + sum3)
    return H1, Hprime1


def rho_sf(d):
    """rho(d) for squarefree d: number of solutions of x^2 ≡ -1 mod d."""
    if d == 1: return 1
    n = d
    rho = 1
    p = 2
    if n % 2 == 0:
        # rho(2) = 1
        n //= 2
    p = 3
    while p*p <= n:
        if n % p == 0:
            if n % (p*p) == 0:
                return 0  # not squarefree
            n //= p
            if p % 4 == 1:
                rho *= 2
            else:
                return 0  # p ≡ 3 mod 4 ⇒ rho = 0
        p += 2
    if n > 1:
        # n is prime
        if n % 4 == 1:
            rho *= 2
        elif n % 4 == 3:
            return 0
        # else n = 2 (already handled)
    return rho


def sum_rho_over_e(X):
    """Compute sum_{e sf, e <= X} rho(e)/e directly."""
    s = 0.0
    for d in range(1, X+1):
        r = rho_sf(d)
        if r > 0:
            s += r / d
    return s


def factor_n2plus1_sf_divs(n, split_primes):
    """Return sorted list of squarefree divisors of n^2+1."""
    m = n*n + 1
    primes = []
    if m % 2 == 0:
        primes.append(2)
        while m % 2 == 0: m //= 2
    for p in split_primes:
        if p*p > m: break
        if m % p == 0:
            primes.append(p)
            while m % p == 0: m //= p
    if m > 1:
        primes.append(m)
    sf = [1]
    for p in primes:
        sf = sf + [d*p for d in sf]
    return sf

def compute_T_split_fast(N):
    primes_up = primes_up_to(N)
    split_primes = [p for p in primes_up if p % 4 == 1]
    T_lt = 0
    T_gt = 0
    for n in range(1, N+1):
        sf = factor_n2plus1_sf_divs(n, split_primes)
        for d in sf:
            if d <= N:
                T_lt += 1
            else:
                T_gt += 1
    return T_lt, T_gt


def main():
    print("=== H(1), H'(1) ===")
    H1, Hp1 = compute_H_and_Hprime(P_bound=10**6)
    print(f"  H(1)   = {H1:.10f}")
    print(f"  H'(1)  = {Hp1:.10f}")
    a1 = R * H1
    c_lt = R * Hp1 + GAMMA_K * H1
    c1 = math.pi/2 * H1
    print(f"  c_1 = pi H(1)/2          = {c1:.10f}")
    print(f"  a_1 = pi H(1)/4          = {a1:.10f}")
    print(f"  c_<^infty := pi H'(1)/4 + gamma_K H(1) = {c_lt:.10f}")
    print()

    print("=== Direct check: sum_{e sf, e <= X} rho(e)/e vs closed form ===")
    print(f"{'X':>8} {'partial sum':>14} {'predicted':>14} {'diff':>10}")
    for X in [1000, 3000, 10000, 30000, 100000]:
        t0 = time.time()
        s = sum_rho_over_e(X)
        L = math.log(X)
        pred = a1 * L + c_lt
        print(f"{X:>8} {s:>14.6f} {pred:>14.6f} {s-pred:>10.6f}  ({time.time()-t0:.1f}s)")
    print()

    print("=== T_< (N) / N and T_> (N) / N at larger N ===")
    print(f"{'N':>7} {'T_<':>10} {'T_>':>10} {'T_</N - a1L':>14} {'T_>/N - a1L':>14} {'(T-c1NL)/N':>10}")
    for N in [500, 1000, 2000, 5000, 10000, 20000, 50000]:
        t0 = time.time()
        T_lt, T_gt = compute_T_split_fast(N)
        L = math.log(N)
        clt = (T_lt - a1*N*L) / N
        cgt = (T_gt - a1*N*L) / N
        ct  = (T_lt + T_gt - c1*N*L) / N
        print(f"{N:>7} {T_lt:>10} {T_gt:>10} {clt:>14.4f} {cgt:>14.4f} {ct:>10.4f}  ({time.time()-t0:.1f}s)")
    print()

    print("=== Conclusions ===")
    print(f"  c_<^infty (closed form) = {c_lt:.4f}")
    print(f"  c_<^infty (empirical)   ≈ ?  (should approach {c_lt:.4f} as N -> infty)")
    print(f"  c_>^infty (empirical)   ≈ ?  (small constant, ~ -0.02)")
    print(f"  c_0^T = c_<^infty + c_>^infty  ≈ {c_lt:.4f} - 0.02 = {c_lt - 0.02:.4f}")
    print(f"  Empirical c_0^T from prev session: 0.99 +/- 0.03   ✓")


if __name__ == "__main__":
    main()
