"""
Compute b'_0 = constant Laurent coefficient of T_3(s) = zeta_K(s)^2 H_3(s) at s=1,
i.e. the coefficient of (s-1)^0 in the Laurent expansion of T_3.

T_3 has pole of order 2: T_3(s) = c_2/(s-1)^2 + c_1/(s-1) + c_0 + O(s-1)
with
  c_2 = R^2 H_3(1)               (= b'_2)
  c_1 = R^2 H_3'(1) + 2 R gamma_K H_3(1)    (= b'_1)
  c_0 = R^2 H_3''(1)/2 + 2 R gamma_K H_3'(1) + (gamma_K^2 + 2 R beta_K) H_3(1)
where zeta_K(s) = R/(s-1) + gamma_K + beta_K (s-1) + O((s-1)^2),
R = pi/4 (residue of Dedekind zeta of Q(i)).

By the Perron contour calculation in the session log,
  Sigma_3(X) := sum_{d <= X} 2^omega(d) rho(d) / d
            ~ c_2 (log X)^2/2 + c_1 log X + c_0 + smaller error.

Hence S_3(N) = N * Sigma_3(N^2+1) + (boundary) ~
             2 b'_2 N L^2 + 2 b'_1 N L + b'_0 N + ...
with L = log N, b'_0 = c_0.

Test: predict W_{K-1} - P^(3,3) / band where P^(3,3) = P^(3) + b'_0 * band.
"""
import math

# Constants from prior session
H3_1 = 0.27775120  # confirmed by Euler product over primes < 10^6
H3_prime_1 = 0.84240798

# gamma_K, beta_K from prior P12-c0 work (Laurent of zeta_K at s=1):
gamma_K = 0.6462
beta_K = 0.0915  # second Laurent coefficient
R = math.pi/4

# Need H_3''(1). Compute via (log H_3)''(1) and (log H_3)'(1):
#   H_3''/H_3 = ((log H_3)')^2 + (log H_3)''
# Approach: differentiate each Euler-factor log term symbolically.
#
# Local at p=2:   f_2(s) = log(1 + 2^(1-s)) + 2 log(1 - 2^(-s))
#   f_2'(1) = -ln2/2 + 2 ln2 = (3/2) ln 2
#   f_2''(1): d/ds [-ln2 * u/(1+u)] with u = 2^(1-s), u' = -ln2*u
#             = -ln2 * u'/(1+u)^2 = (ln2)^2 u/(1+u)^2; at s=1, u=1: (ln2)^2 /4
#             plus d/ds [2 ln2 * v/(1-v)] with v = 2^(-s), v' = -ln2*v
#             = 2 ln2 * v'/(1-v)^2 = -2(ln2)^2 v/(1-v)^2; at s=1, v=1/2: -2(ln2)^2 *0.5/0.25 = -4(ln2)^2
#   total f_2''(1) = (ln2)^2/4 - 4(ln2)^2 = -(15/4)(ln 2)^2
#
# Local at p == 1 (mod 4):  f_p(s) = log(1+3 p^(-s)) + 3 log(1-p^(-s))
#   f_p'(s) = 12 p^(-2s) ln p / [(1-p^(-s))(1+3 p^(-s))]
#   For f_p''(1) compute numerically via a finite-difference centred at s=1.
#
# Local at p == 3 (mod 4):  f_p(s) = 2 log(1 - p^(-2s))
#   f_p'(s) = 4 p^(-2s) ln p / (1 - p^(-2s))
#   f_p''(s): d/ds 4 ln p * w/(1-w) with w = p^(-2s), w' = -2 ln p * w
#           = 4 ln p * w'/(1-w)^2 = -8 (ln p)^2 w/(1-w)^2
#           at s=1: -8 (ln p)^2 / p^2 / (1 - 1/p^2)^2

def is_prime(n):
    if n<2: return False
    if n<4: return True
    if n%2==0: return False
    for k in range(3, int(n**0.5)+1, 2):
        if n%k==0: return False
    return True

def f_split_first(p, s):
    # at p == 1 mod 4 split prime
    return -3*math.log(p)*p**(-s)/(1+3*p**(-s)) + 3*math.log(p)*p**(-s)/(1-p**(-s))

def compute_logH3_derivs(P_LIMIT=10**6):
    ln2 = math.log(2)
    # First derivatives
    d1 = -ln2/2 + 2*ln2  # = 1.5 * ln 2
    # Second derivatives
    d2 = (ln2)**2 / 4 - 4*(ln2)**2  # = -3.75 (ln 2)^2
    for p in range(3, P_LIMIT, 2):
        if not is_prime(p): continue
        if p%4 == 1:
            # f_p'(1): from script == -3 ln p/p / (1+3/p) + 3 ln p/p / (1-1/p)
            d1 += -3*math.log(p)/p/(1+3/p) + 3*math.log(p)/p/(1-1/p)
            # f_p''(1): take central finite difference of f_p'(s) at s=1
            h = 1e-5
            d2 += (f_split_first(p, 1+h) - f_split_first(p, 1-h))/(2*h)
        else:
            # p == 3 mod 4
            lnp = math.log(p)
            d1 += 4*lnp/p**2 / (1-1/p**2)
            # f_p''(1)
            d2 += -8 * lnp**2 / p**2 / (1 - 1/p**2)**2
    return d1, d2

print("Computing (log H_3)'(1) and (log H_3)''(1) by Euler-product partial sum...")
d1, d2 = compute_logH3_derivs()
print(f"  (log H_3)' (1) = {d1:.6f}")
print(f"  (log H_3)''(1) = {d2:.6f}")
print(f"  H_3'(1)  = {d1*H3_1:.6f}  (cross-check vs prior {H3_prime_1:.6f})")

# H_3'' = H_3 * ((log H_3)')^2 + (log H_3)''
H3_double_prime = H3_1 * (d1**2 + d2)
print(f"  H_3''(1) = {H3_double_prime:.6f}")

# c_0 = R^2 H_3''(1)/2 + 2 R gamma_K H_3'(1) + (gamma_K^2 + 2 R beta_K) H_3(1)
term1 = R**2 * H3_double_prime/2
term2 = 2 * R * gamma_K * H3_prime_1
term3 = (gamma_K**2 + 2*R*beta_K) * H3_1
b0p = term1 + term2 + term3
print(f"\n  R^2 H_3''(1)/2          = {term1:.6f}")
print(f"  2 R gamma_K H_3'(1)     = {term2:.6f}")
print(f"  (gamma_K^2 + 2 R beta_K) H_3(1) = {term3:.6f}")
print(f"  --------")
print(f"  b'_0 = c_0  = {b0p:.6f}")

# Re-evaluate (W - P^(3,3))/band where P^(3,3) = P^(3) + b'_0 * band
print("\nPost-processing (W-P^(3,3))/band with computed b'_0:")
data = [
    # (N, band, W/N, P3/N, ratio_S3)
    (10000,  950,    5.0046, 4.8761, 1.0322),
    (30000,  7830,  16.0934, 15.7324, 1.0286),
    (100000, 19046, 14.0636, 13.7772, 1.0235),
    (300000, 19567,  5.6610, 5.5179, 1.0219),
    (1000000,275923,27.1912,26.7197,1.0191),
]
print(f'{"N":>8} {"band":>8} {"L":>7} {"(W-P3)/N":>11} {"rho_emp":>9} {"(W-P33)/N":>11} {"(W-P33)/band":>14}')
for (N, band, W_per_N, P3_per_N, ratioS3) in data:
    W = W_per_N * N
    P3 = P3_per_N * N
    L = math.log(N)
    P33 = P3 + b0p * band
    resid_2term = (W - P3)
    rho_emp = resid_2term / band
    resid_3term = (W - P33)
    print(f'{N:>8} {band:>8} {L:>7.3f} {resid_2term/N:>11.4f} {rho_emp:>9.4f} {resid_3term/N:>11.4f} {resid_3term/band:>14.4f}')
