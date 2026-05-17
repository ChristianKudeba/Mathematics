"""
Empirical Sigma_*(X) := sum_{d <= X} tau(d^2) rho(d) / d
vs the formal Laurent prediction at s=1:

    Sigma_*(X) ~ A_3 L^3/6 + A_2 L^2/2 + A_1 L + A_0 + O(L^{-A}),  L = log X,

where A_3, A_2, A_1, A_0 are the Laurent coefficients of G(s) = zeta_K^3 H
at s=1, derived in earlier sessions:

    A_3 = R^3 H(1),
    A_2 = 3 R^2 gamma_K H(1) + R^3 H'(1),
    A_1 = 3 R (R beta_K + gamma_K^2) H(1) + 3 R^2 gamma_K H'(1) + (R^3/2) H''(1),
    A_0 = (3 R^2 alpha_K + 6 R gamma_K beta_K + gamma_K^3) H(1)
        + 3 R (R beta_K + gamma_K^2) H'(1) + (3 R^2 gamma_K / 2) H''(1)
        + (R^3 / 6) H'''(1),

with R = pi/4, and gamma_K, beta_K, alpha_K the Laurent coefficients of zeta_K
at 1, computed in P12-c0-coefficient.md.

This script:
  1. Sieves the smallest prime factor for d <= X.
  2. Computes a(d) = tau(d^2) rho(d) for each d (multiplicative; nonzero only
     if d = 2^eps * prod p_i^k_i with eps in {0,1} and p_i ≡ 1 mod 4).
  3. Forms cumulative T(X) = sum_{d <= X} a(d)/d (running mean).
  4. Compares to the formal Laurent.

Output: residual = Sigma_*(X) - Laurent prediction. If formal-SD is
internally consistent, residual should be small and decreasing in 1/L^A.
"""
import math
import time

# Pre-computed Laurent coefficients (50-digit values from prior session,
# truncated to 12 digits here).
# H Euler-product values from tau-sq-c0-coefficient.py (P_max = 2e5).
H1   =  0.123242891000   # H(1)
H1p  =  0.593437646500   # H'(1)
H1pp =  0.907111888800   # H''(1)
H1ppp = -5.088792573700  # H'''(1)

R = math.pi / 4

# Stieltjes etc.
gamma_E = 0.577215664901
L1     = 0.192901316796912   # L'(1, chi_4)
L2     = -0.154141724429336  # L''(1, chi_4)
L3     = 0.094882859205604   # L'''(1, chi_4)
gamma1 = -0.072815845483676
gamma2 = -0.009690363192872

# Laurent coefficients of zeta_K at s=1: zeta_K = R/u + gamma_K + beta_K u + alpha_K u^2 + ...
# zeta_K = zeta * L(.,chi_4); zeta = 1/u + gamma - gamma_1 u + (gamma_2/2) u^2 + ...
gamma_K = L1 + gamma_E * R
beta_K  = L2/2 + gamma_E * L1 - gamma1 * R   # standard; sign convention zeta = 1/u+gamma-gamma_1 u+gamma_2/2 u^2+...
alpha_K = L3/6 + gamma_E * L2/2 - gamma1 * L1 + (gamma2/2) * R

print("Laurent coefficients of zeta_K at s=1:")
print(f"  R        = {R:.12f}")
print(f"  gamma_K  = {gamma_K:.12f}")
print(f"  beta_K   = {beta_K:.12f}")
print(f"  alpha_K  = {alpha_K:.12f}")

# Laurent coefficients of G(s) = zeta_K(s)^3 H(s) at s=1.
A3 = R**3 * H1
A2 = 3 * R**2 * gamma_K * H1 + R**3 * H1p
A1 = 3 * R * (R * beta_K + gamma_K**2) * H1 + 3 * R**2 * gamma_K * H1p + (R**3 / 2) * H1pp
A0 = (3 * R**2 * alpha_K + 6 * R * gamma_K * beta_K + gamma_K**3) * H1 \
   + 3 * R * (R * beta_K + gamma_K**2) * H1p \
   + (3 * R**2 * gamma_K / 2) * H1pp \
   + (R**3 / 6) * H1ppp

print(f"\nLaurent coefficients of G at s=1:")
print(f"  A_3 = {A3:.12f}")
print(f"  A_2 = {A2:.12f}")
print(f"  A_1 = {A1:.12f}")
print(f"  A_0 = {A0:.12f}")

def laurent_pred(X):
    L = math.log(X)
    return A3 * L**3 / 6 + A2 * L**2 / 2 + A1 * L + A0

def sieve_a(X):
    """Sieve a(d) = tau(d^2) rho(d) for d in [1, X]. Memory: ~X int32."""
    # Smallest prime factor.
    # Use Python list of int; for X = 1e7 this is ~280 MB. Too much.
    # Use array module with int32 (4 bytes).
    from array import array
    spf = array('i', [0]) * (X + 1)  # zero-init, size X+1, 4 bytes each
    for p in range(2, X + 1):
        if spf[p] == 0:
            for k in range(p, X + 1, p):
                if spf[k] == 0:
                    spf[k] = p
    # a(d) = tau(d^2) rho(d).
    # multiplicative; a(p^k):
    #   p = 2, k = 1: 3 ; k >= 2: 0
    #   p ≡ 3 mod 4: 0
    #   p ≡ 1 mod 4: 2 * (2k+1)
    a = array('q', [0]) * (X + 1)  # 8-byte signed
    a[1] = 1
    for d in range(2, X + 1):
        p = spf[d]
        # extract p from d
        m = d
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        # a(p^e):
        if p == 2:
            ap = 3 if e == 1 else 0
        elif p % 4 == 3:
            ap = 0
        else:
            ap = 2 * (2 * e + 1)
        a[d] = a[m] * ap
    return a

def main():
    X_max = 10**7
    print(f"\nSieving smallest prime factor and a(d) for d <= {X_max}...")
    t0 = time.time()
    a = sieve_a(X_max)
    print(f"Sieve done in {time.time()-t0:.1f} s.")
    # Cumulative sum of a(d)/d.
    print(f"\n{'X':>10} {'Sigma_*(X)':>16} {'Laurent':>16} {'residual':>14} {'res*L^2':>12}")
    cumsum = 0.0
    targets = [10**3, 3*10**3, 10**4, 3*10**4, 10**5, 3*10**5, 10**6, 3*10**6, 10**7]
    ti = 0
    for d in range(1, X_max + 1):
        if a[d]:
            cumsum += a[d] / d
        if ti < len(targets) and d == targets[ti]:
            X = d
            L = math.log(X)
            pred = laurent_pred(X)
            res = cumsum - pred
            print(f"{X:>10d} {cumsum:>16.6f} {pred:>16.6f} {res:>14.6f} {res*L*L:>12.4f}")
            ti += 1

if __name__ == "__main__":
    main()
