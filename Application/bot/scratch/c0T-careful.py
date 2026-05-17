"""
Careful derivation of c_0^T via Mellin-Perron.

Approach: use the IDENTITY (no heuristic doubling)
   T(N) = sum_{n <= N} tau*(n^2+1)
        = sum_{e sf} #{n <= N: e | n^2+1}
        = sum_{e sf, e <= N^2+1} rho(e) * (N/e + boundary).

The Hooley split says:
   T(N) = T_<=(N) + T_>(N)
   T_<=(N) := sum_{e sf, e <= N} rho(e) * #{n in [1,N]: e | n^2+1}
   T_>(N)  := sum_{e sf, N < e <= N^2+1} rho(e) * #{n in [1,N]: e | n^2+1}

For T_<= we have an EXACT closed form (up to o(N)):
   T_<=(N) = sum_{e sf, e <= N} rho(e) * (rho(e) lfloor N/e rfloor + O(rho(e)))
   wait no -- I keep confusing myself. Let me re-derive.

   #{n in [1,N]: e | n^2+1} = rho(e) * lfloor N/e rfloor + O(rho(e))
   (rho(e) residue classes, each contributing lfloor N/e rfloor + O(1))

So T_<=(N) = sum_{e sf, e <= N} (rho(e) * lfloor N/e rfloor + O(rho(e)))

That's just one rho factor, NOT rho^2. The "extra" rho factor I was confusing
with comes from when we ALSO sum over e of #{e | n^2+1} -- but that's
already implicit in summing over e.

Verify by Mellin-Perron:
   sum_{e sf, e <= N} rho(e) lfloor N/e rfloor = sum_{m <= N} A(m)
   where A(m) = sum_{d sf, d | m} rho(d).
   Multiplicative: A(p^k) = 1 + rho(p) for k >= 1.
   D_A(s) = prod_p (1 + (1+rho(p)) p^{-s}/(1 - p^{-s}))
          = prod_p (1 - p^{-s} + (1+rho(p)) p^{-s}) / (1 - p^{-s})
          = prod_p (1 + rho(p) p^{-s}) / (1 - p^{-s})
          = zeta(s) * G(s)
          = zeta(s) * zeta_K(s) * H(s).

This has DOUBLE pole at s=1. Mellin-Perron (residue at s=1 of D_A(s) N^s/s):
   sum_{m <= N} A(m) = N(phi(1) log N + phi'(1) - phi(1)) + o(N)
   where phi(s) = (s-1)^2 * D_A(s).

   phi(s) = [(s-1) zeta(s)] [(s-1) zeta_K(s)] H(s)
   (s-1) zeta(s) = 1 + gamma(s-1) + gamma_1(s-1)^2 + ...
   (s-1) zeta_K(s) = R + gamma_K(s-1) + beta_K(s-1)^2 + ...,  R = pi/4

   phi(1)  = R * H(1)
   phi'(1) = R * H'(1) + gamma_K * H(1) + R * gamma * H(1)

So T_<=(N) = N * [R H(1) log N + R H'(1) + gamma_K H(1) + R gamma H(1) - R H(1)] + o(N).

   leading coefficient of N log N: R H(1) = pi H(1)/4 (HALF of c_1 = pi H(1)/2).

Now for T_>:
   T_>(N) = sum_{e sf, N < e <= N^2+1} rho(e) * #{n in [1,N]: e | n^2+1}.

The NAIVE expectation (Hooley): T_>(N) ~= T_<=(N) by symmetry.
   leading: R H(1) N log N
   total T = T_< + T_> ~= 2 T_<= leading = (pi H(1)/2) N log N.   GOOD.

Question: what's the secondary of T_>?

T_>(N) is harder because for e > N, #{n <= N: e | n^2+1} is small. Specifically,
for each e in (N, N^2+1], #{n: e | n^2+1, n <= N} <= rho(e), in fact often 0.

Sum: for fixed e, the residue classes are r in [0, e-1]. For e > N, at most
rho(e) of these intersect [1, N]; if r > N then 0 contribution.

So T_>(N) = sum_{e sf, N < e} rho(e) * #{r: r^2 ≡ -1 (e), 1 <= r <= N}.

Reorder by setting m = n^2+1 = e * k (k = m/e). For each n <= N, n^2+1 has
divisors e with N < e <= n^2+1; complementary k = (n^2+1)/e satisfies
1 <= k < (n^2+1)/N.  The squarefree-divisor relation transfers: e sf ⇔ k = m/e
with squarefree-essence ... not clean.

CLEAN PATH: use the formal Hooley argument
   tau*(m) = 2 * #{e sf | m: e^2 <= rad(m)}    (exact, modulo m=1 diagonal).
            = 2 * #{e sf | m: e <= sqrt(rad(m))}

For 'most' n (those with n^2+1 sf): rad(n^2+1) = n^2+1 ≈ n^2, so sqrt(rad) ≈ n.
For non-sf n^2+1 (density 1 - C_0 where C_0 = prod_{p≡1(4)}(1 - 2/p^2)):
sqrt(rad) < n.

This script computes:
  (a) the candidate c_0^T from the "doubled T_<=" formula (heuristic):
      c_0^T_heur = 2 * (R H'(1) + gamma_K H(1) + R gamma H(1) - R H(1))
                 - sum (Hooley non-sf correction).
  (b) numerical T_<=(N) and T_>(N) at small N to validate.

Comparison empirical c_0^T ≈ 0.99.
"""

import math, time

GAMMA = 0.5772156649015328606
LPRIME_1_CHI4 = 0.19290131767382030
GAMMA_K = (math.pi/4) * GAMMA + LPRIME_1_CHI4
R = math.pi/4

# H(1), H'(1) from prior calculation
H1 = 0.55267216900
HP1 = 0.83558494285  # actually let's recompute below to be safe

# Empirical T values from prev session (read from B3-bdy-SD-constants.py output:
# N        T(N)         T/(N log N)   resid/N = (T - c1 N L)/N
# 500      4434         1.034         1.05    (approx)
# 1000     8908         1.025         1.03
# ...
# 100000  1148658       0.954         1.01
# Let's recompute T(N) directly here.

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


def factor_n2plus1(n, split_primes):
    m = n*n + 1
    omega = 0
    if m % 2 == 0:
        omega += 1
        while m % 2 == 0:
            m //= 2
    for p in split_primes:
        if p*p > m:
            break
        if m % p == 0:
            omega += 1
            while m % p == 0:
                m //= p
    if m > 1:
        omega += 1
    return omega


def compute_T(N):
    primes_up = primes_up_to(N)
    split_primes = [p for p in primes_up if p % 4 == 1]
    T = 0
    for n in range(1, N+1):
        omega = factor_n2plus1(n, split_primes)
        T += 1 << omega
    return T


def compute_T_split(N):
    """
    Computes T(N) = T_<(N) + T_>(N)
    T_<(N) = sum over (n, e) with e sf, e | n^2+1, e <= N
    T_>(N) = sum over (n, e) with e sf, e | n^2+1, e > N (and e <= n^2+1)
    Returns (T, T_<, T_>).
    """
    # Direct: for each n, factor n^2+1, enumerate squarefree divisors.
    primes_up = primes_up_to(N)
    split_primes = [p for p in primes_up if p % 4 == 1]
    T_lt = 0
    T_gt = 0
    for n in range(1, N+1):
        m = n*n + 1
        # Find prime factorization of m
        factors = []  # list of distinct primes
        if m % 2 == 0:
            factors.append(2)
            while m % 2 == 0: m //= 2
        for p in split_primes:
            if p*p > m: break
            if m % p == 0:
                factors.append(p)
                while m % p == 0: m //= p
        if m > 1:
            factors.append(m)
        # Enumerate all squarefree divisors
        sf_divs = [1]
        for p in factors:
            sf_divs = sf_divs + [d*p for d in sf_divs]
        for d in sf_divs:
            if d <= N:
                T_lt += 1
            else:
                T_gt += 1
    return T_lt + T_gt, T_lt, T_gt


def main():
    print("=== Recompute H(1), H'(1) ===")
    t0 = time.time()
    H1, Hp1 = compute_H_and_Hprime(P_bound=10**6)
    print(f"  H(1)  = {H1:.10f}")
    print(f"  H'(1) = {Hp1:.10f}  ({time.time()-t0:.1f}s)")
    print()

    c1 = H1 * math.pi / 2.0
    print("=== Theoretical predictions ===")
    print(f"  c_1 = H(1) pi/2 = {c1:.6f}")

    # Mellin formula for T_<=(N) = sum_{e sf, e <= N} rho(e) lfloor N/e rfloor
    K1 = R * Hp1 + GAMMA_K * H1 + R * GAMMA * H1 - R * H1
    print(f"  K_1 (constant in T_<=) = R H'(1) + gamma_K H(1) + R gamma H(1) - R H(1)")
    print(f"        = {R*Hp1:.4f} + {GAMMA_K*H1:.4f} + {R*GAMMA*H1:.4f} - {R*H1:.4f}")
    print(f"        = {K1:.6f}")
    # T_<=(N) ~= R H(1) N log N + K_1 N + o(N)
    a1 = R * H1
    print(f"  Predicted T_<= ~= {a1:.4f} * N log N + {K1:.4f} * N")
    print()

    # If T_> ~= T_<= (heuristic doubling):
    #   T(N) ~= 2 R H(1) N log N + 2 K_1 N
    #         = c_1 N log N + 2 K_1 N
    print(f"  Naive doubling: c_0^T (heur) = 2 K_1 = {2*K1:.6f}")
    print()
    # But this is wrong (we saw above gives ~1.66, empirical ~0.99).

    # Let's directly compute T_<=(N) and T_>(N) numerically.
    print("=== Numerical T_<=(N) and T_>(N) ===")
    print(f"{'N':>7} {'T':>10} {'T_<':>10} {'T_>':>10} {'T_<=/N':>10} {'T_>/N':>10}")
    for N in [500, 1000, 2000, 5000, 10000, 20000]:
        t0 = time.time()
        T, T_lt, T_gt = compute_T_split(N)
        L = math.log(N)
        # Subtract leading; constant part:
        clt = (T_lt - a1 * N * L) / N
        cgt = (T_gt - a1 * N * L) / N
        ct  = (T - c1 * N * L) / N
        print(f"{N:>7} {T:>10} {T_lt:>10} {T_gt:>10} {clt:>10.4f} {cgt:>10.4f}  Tres/N={ct:.4f} ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
