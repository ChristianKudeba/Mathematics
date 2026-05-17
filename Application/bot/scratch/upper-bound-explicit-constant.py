"""
Compute the explicit constants in the upper bound

    S(N) := sum_{n <= N} tau(n^2+1)^2  <=  C_Nair * N * P(N^2) * M(N^2)

from the previous session's Nair-based argument, and compare to the conjectured
leading constant  c_3 = pi^3 * H(1) / 48 .

Components:
1.  H_0(1) for D(s) = zeta_K(s)^4 H_0(s), where
      D(s) = sum_m tau^2(m) rho_F(m) / m^s ,  F = X^2+1 ,  rho_F(p) at split = 2.
    Local factors:
      p ≡ 3 (4):  H_{0,p}(1) = (1 - 1/p^2)^4
      p = 2    :  H_{0,2}(1) = (1 + 4/2) * (1 - 1/2)^4 = 3 * 1/16 = 3/16
      p ≡ 1 (4):  H_{0,p}(1) = D_p(1) * (1 - 1/p)^8, with
                  D_p(1) = 2 * (1+1/p)/(1-1/p)^3 - 1 .

2.  H(1) for G(s) = zeta_K(s)^3 H(s), where
      G(s) = sum_d tau(d^2) rho_F(d) / d^s = sum_d g(d) rho_F(d) / d^s ,
      g(p^k) = 2k+1 .
    Local factors:
      p ≡ 3 (4):  H_p(1) = (1 - 1/p^2)^3
      p = 2    :  H_2(1) = (1 + 1/2 + 1/4) * (1 - 1/2)^3 = (7/4)*(1/8) = 7/32
                  Wait that's wrong: at p=2 ramified, rho_F(2) = 1, rho_F(4) = 0.
                  So G_2(s) = sum_k g(2^k) rho_F(2^k) / 2^{ks}
                            = 1 + g(2)*1/2 + 0 + ...
                            = 1 + 3/2 = 5/2  at s=1.
                  And zeta_K(s) at p=2: factor (1 - 1/2^s)^{-1} (ramified, single prime above with norm 2).
                  So zeta_K^3 local at 2 is (1-1/2)^{-3} = 8.
                  Hence H_2(1) = (5/2) * (1-1/2)^3 = (5/2) * (1/8) = 5/16 .
      p ≡ 1 (4):  G_p(1) = 1 + 2 sum_{k>=1} (2k+1)/p^k
                       = 1 + 2 [3/p / (1-1/p) + 2 * (1/p)/(1-1/p)^2]
                       = 1 + 6/(p-1) + 4 / [p(1-1/p)^2]
                       = use generating function (1+x)/(1-x)^2 = sum (2k+1) x^k for k>=0 (check: k=0 -> 1, k=1 -> 3, k=2 -> 5)
                       Yes. So sum_{k>=0}(2k+1) x^k = (1+x)/(1-x)^2.
                       So sum_{k>=1}(2k+1) x^k = (1+x)/(1-x)^2 - 1 = [(1+x) - (1-x)^2]/(1-x)^2 = [3x - x^2]/(1-x)^2 .
                  Thus G_p(1) at split p = 1 + 2 * [3/p - 1/p^2]/(1-1/p)^2 = 1 + 2(3/p - 1/p^2) p^2/(p-1)^2
                                       = 1 + 2(3p - 1)/(p-1)^2 .
                  H_p(1) = G_p(1) * (1 - 1/p)^6 .

3.  c_P : explicit leading constant in P(Y) ~ c_P / log Y, where
      P(Y) = prod_{p<=Y} (1 - rho_F(p)/p)
           = (1/2) * prod_{p<=Y, p≡1(4)} (1 - 2/p) .
    log(c_P/log Y * log Y) = log P(Y).  Take log P(Y) - log(1/log Y) → log c_P.
    Numerically: take large Y, compute P(Y), multiply by log Y.

4.  Upper-bound constant from the chain:
      S(N) <= C_Nair * N * P(N^2) * M(N^2)
    with
      M(N^2) ~ (H_0(1) * pi^4 / 1536) * (log N^2)^4 / 4 = H_0(1) pi^4/(384) * (log N)^4
        (Wait: SD gives sum_{m<=Y} a_m ~ G_0(1)/Gamma(4) * Y log^3 Y , G_0(1) = (pi/4)^4 H_0(1))
        sum_{m<=Y} a_m ~ (pi/4)^4 * H_0(1) / 6 * Y * log^3 Y
                       = H_0(1) * pi^4 / 1536 * Y * log^3 Y .
        Then sum_{m<=Y} a_m / m ~ (1/4) of leading log^4 (partial summation) :
              sum_{m<=Y} a_m/m ~ H_0(1) * pi^4/1536/4 * log^4 Y
                              = H_0(1) * pi^4 / 6144 * log^4 Y .
        At Y = N^2 : M(N^2) ~ H_0(1) * pi^4 / 6144 * (2 log N)^4 = H_0(1) pi^4 / 384 * log^4 N .
      P(N^2) ~ c_P / (2 log N) .
    Product: P * M ~  H_0(1) pi^4 / 384 * c_P / (2 log N) * log^4 N
                  =  H_0(1) pi^4 c_P / 768 * log^3 N .
    So  S(N) <= C_Nair * H_0(1) pi^4 c_P / 768 * N log^3 N .

5.  Conjectured leading: c_3 = pi^3 H(1) / 48 .

Print and compare.
"""
import math


def primerange(lo, hi):
    """Sieve-of-eratosthenes style primes in [lo, hi)."""
    if hi <= 2:
        return
    sieve = bytearray([1]) * hi
    sieve[0] = sieve[1] = 0
    for i in range(2, int(hi**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, hi, i):
                sieve[j] = 0
    for i in range(max(lo, 2), hi):
        if sieve[i]:
            yield i

# --- step 1: H_0(1) ---
def H0_at_1(P_max=10_000_000):
    """H_0(1) = prod_p H_{0,p}(1)."""
    # p = 2 contribution:
    # D_2(s) = 1 + tau^2(2)*rho(2)/2^s = 1 + 4*1/2^s.
    # zeta_K at 2 (ramified): factor (1 - 1/2^s)^{-1}. zeta_K^4 local: (1-1/2^s)^{-4}.
    # H_{0,2}(s) = D_2(s) * (1 - 1/2^s)^4. At s=1: (1 + 4/2)*(1/2)^4 = 3 * 1/16 = 3/16.
    H = 3.0 / 16.0
    for p in primerange(3, P_max + 1):
        if p % 4 == 3:
            # inert: zeta_K local (1 - 1/p^{2s})^{-1}; zeta_K^4 local (1 - 1/p^{2s})^{-4}.
            # D_p(s) = 1 (no contribution).
            # H_{0,p}(1) = (1 - 1/p^2)^4
            H *= (1 - 1.0/(p*p))**4
        else:  # p ≡ 1 (4), split
            # D_p(1) = 2*(1+1/p)/(1-1/p)^3 - 1
            x = 1.0 / p
            D_p_1 = 2.0 * (1 + x) / (1 - x)**3 - 1.0
            # H_{0,p}(1) = D_p(1) * (1 - 1/p)^8
            H *= D_p_1 * (1 - x)**8
    return H

# --- step 2: H(1) ---
def H_at_1(P_max=10_000_000):
    """H(1) for G(s) = zeta_K(s)^3 H(s)."""
    # p = 2 (ramified): G_2(1) = 1 + g(2)*rho(2)/2 = 1 + 3*1/2 = 5/2.
    # zeta_K at 2: (1-1/2)^{-1} = 2. zeta_K^3 local at 2: 8.
    # H_2(1) = G_2(1) * (1 - 1/2)^3 = (5/2)*(1/8) = 5/16
    H = 5.0 / 16.0
    for p in primerange(3, P_max + 1):
        if p % 4 == 3:
            # inert. H_{p}(1) = (1 - 1/p^2)^3
            H *= (1 - 1.0/(p*p))**3
        else:  # p ≡ 1 (4)
            # G_p(1) = 1 + 2*(3p-1)/(p-1)^2
            G_p_1 = 1 + 2.0 * (3*p - 1) / (p-1)**2
            x = 1.0 / p
            # H_{p}(1) = G_p(1) * (1 - 1/p)^6
            H *= G_p_1 * (1 - x)**6
    return H

# --- step 3: c_P ---
def c_P_compute(Y_max=10**8):
    """Compute log(c_P) = lim_{Y->inf} (log P(Y) + log log Y)."""
    log_P = math.log(0.5)  # contribution of p=2: 1 - 1/2 = 1/2.
    Y_print = []
    log_Y_print = []
    log_P_print = []
    next_check = 10_000
    for p in primerange(3, Y_max + 1):
        if p % 4 == 1:
            log_P += math.log(1 - 2.0/p)
        # Note: p ≡ 3 (4) contributes 1 - 0/p = 1, no contribution.
        if p >= next_check:
            log_Y = math.log(p)
            Y_print.append(p)
            log_Y_print.append(log_Y)
            log_P_print.append(log_P)
            next_check *= 10
    return log_P, Y_print, log_Y_print, log_P_print

# --- main ---
H0 = H0_at_1(P_max=1_000_000)
H1 = H_at_1(P_max=1_000_000)
print(f"H_0(1) ≈ {H0:.6f}     (target: pole-of-order-4 factorization, D(s) = zeta_K^4 H_0)")
print(f"H(1)   ≈ {H1:.6f}     (sanity: previous-session value 0.12324)")

# Step 3: Compute c_P
print("\nMertens for AP — computing c_P (leading constant in P(Y) ~ c_P/log Y) ...")
log_P_final, Y_pts, log_Y_pts, log_P_pts = c_P_compute(Y_max=10**7)
print(f"{'Y':>10s} {'log P(Y)':>14s} {'log P + log log Y':>22s}")
for Y, lY, lP in zip(Y_pts, log_Y_pts, log_P_pts):
    print(f"{Y:10d} {lP:14.6f} {lP + math.log(lY):22.6f}")

# Asymptotic estimate of c_P: log_P + log log Y → log c_P
log_cP_est = log_P_pts[-1] + math.log(log_Y_pts[-1])
cP = math.exp(log_cP_est)
print(f"\nlog c_P ≈ {log_cP_est:.6f}, c_P ≈ {cP:.6f}")

# --- step 4: Compare upper-bound constant to conjectured c_3 ---
pi = math.pi
c3_conj = pi**3 * H1 / 48
C_upper_no_C_Nair = H0 * pi**4 * cP / 768

print()
print("="*60)
print("Putting it together:")
print("="*60)
print(f"Conjectured leading constant:  c_3 = pi^3 H(1)/48 = {c3_conj:.6f}")
print()
print(f"Upper-bound chain: S(N) <= C_Nair * N * P(N^2) * M(N^2)")
print(f"  P(N^2) ~ c_P / (2 log N), c_P ≈ {cP:.6f}")
print(f"  M(N^2) ~ H_0(1)*pi^4/384 * log^4 N, H_0(1) ≈ {H0:.6f}")
print(f"  Product ~ H_0(1)*pi^4*c_P/768 * log^3 N = {C_upper_no_C_Nair:.6f} * log^3 N")
print()
print(f"So the explicit leading constant in the rigorous upper bound is")
print(f"      C_Nair * {C_upper_no_C_Nair:.6f}")
print(f"and the conjectured leading constant is")
print(f"      c_3 = {c3_conj:.6f}")
print()
print(f"Ratio  C_upper / c_3  =  C_Nair * {C_upper_no_C_Nair / c3_conj:.4f}")
print(f"  i.e. the rigorous upper bound is at least C_Nair * {C_upper_no_C_Nair / c3_conj:.2f} times the conjectured asymptotic constant.")
print()

# Sanity: at N = 10^6, predict S(N) using c_3 vs upper bound (with C_Nair=1).
N = 10**6
logN = math.log(N)
S_pred_c3 = c3_conj * N * logN**3
S_upper = C_upper_no_C_Nair * N * logN**3
S_empirical = 415319768  # from previous session writeup
print(f"At N = 10^6:")
print(f"  Empirical S(N)            = {S_empirical:.3e}")
print(f"  Conjectured c_3 N log^3 N = {S_pred_c3:.3e}")
print(f"  Upper bd C_upper N log^3 N (with C_Nair=1) = {S_upper:.3e}")
print(f"  Empirical / c_3 prediction = {S_empirical / S_pred_c3:.3f}  (expect O(1), <= 1 if c_3 is leading)")
print(f"  Empirical / upper bd      = {S_empirical / S_upper:.3f}  (must be <= 1 for the upper bound to be consistent at this N)")
