"""
Symbolic match of W_{K-1} via two formal-SD chains.

Goal: compare the prior session's P^(2) (Sigma_* on d-range) against a new
P^(3) (Sigma_3 on n-band) for the topmost dyadic window of B_>(N).

Key correction: W_{K-1} is the partial sum of S_3(N) := sum tau((n^2+1)^2),
NOT of S_2(N) := sum tau(n^2+1)^2.  These have different growth orders
(L^2 vs L^3).

Outputs:
  H_3(1), H_3'(1) via Euler product
  b'_2 = (pi/4)^2 H_3(1), b'_1 = (pi/4)^2 H_3'(1) + 2(pi/4) gamma_K H_3(1)
  Empirical W_{K-1} at N in {10^4, 3e4, 10^5, 3e5}
  Empirical S_3 at N in {3e4, 10^5}
  Comparison table W vs P^(2) vs P^(3)
"""
import math
import time

A3 = (math.pi/4)**3 * 0.12324
A2 = 0.43491036
A1 = 1.07159000
A0 = 0.87930421

def is_prime(n):
    if n<2: return False
    if n<4: return True
    if n%2==0: return False
    for k in range(3, int(n**0.5)+1, 2):
        if n%k==0: return False
    return True

# Compute H_3(1) and H_3'(1) by Euler product, primes up to 10^6.
def compute_H3_constants(P_LIMIT=10**6):
    H3 = 1/2
    log_deriv = 0
    ln2 = math.log(2)
    # p=2 contribution to log H_3':
    # log local at p=2 = log(1+2^(1-s)) + 2 log(1-2^(-s))
    # d/ds at s=1: -ln2/2 (from -(2^(1-s) ln 2)/(1+2^(1-s))|_{s=1} = -ln2/2)
    #            + 2 ln 2  (from 2 * 2^(-s) ln 2 / (1-2^(-s))|_{s=1} = 2*0.5*ln2/0.5 = 2 ln 2)
    log_deriv += -ln2/2 + 2*ln2  # = (3/2) ln 2
    for p in range(3, P_LIMIT, 2):
        if not is_prime(p): continue
        if p%4 == 1:
            H3 *= (1+3.0/p) * (1-1.0/p)**3
            # d/ds log local at s=1:
            # log local = log(1+3 p^(-s)) + 3 log(1-p^(-s))
            # d/ds = -3 p^(-s) ln p / (1+3 p^(-s)) + 3 * p^(-s) ln p / (1-p^(-s))
            log_deriv += -3*math.log(p)/p / (1+3.0/p) + 3*math.log(p)/p / (1-1.0/p)
        else:
            H3 *= (1-1.0/p**2)**2
            # log local = 2 log(1-p^(-2s))
            # d/ds = 2 * 2 p^(-2s) ln p / (1-p^(-2s))
            log_deriv += 4*math.log(p)/p**2 / (1-1.0/p**2)
    H3_prime = log_deriv * H3
    return H3, H3_prime

print("Computing H_3(1) and H_3'(1) via Euler product...")
t0 = time.time()
H3_1, H3_prime_1 = compute_H3_constants()
print(f"  done in {time.time()-t0:.1f}s")
print(f"  H_3(1)  = {H3_1:.6f}")
print(f"  H_3'(1) = {H3_prime_1:.6f}")

r = math.pi/4
gamma_K = 0.6462
b2p = r**2 * H3_1
b1p = r**2 * H3_prime_1 + 2*r*gamma_K*H3_1
print(f"  b'_2 = (pi/4)^2 H_3(1)                            = {b2p:.6f}")
print(f"  b'_1 = (pi/4)^2 H_3'(1) + 2(pi/4) gamma_K H_3(1)  = {b1p:.6f}")

# Sieve-based factorization of n^2+1 for n <= N
def factor_n2plus1_array(N):
    s = bytearray([1])*(N+10)
    s[0] = s[1] = 0
    for i in range(2, int((N+10)**0.5)+1):
        if s[i]:
            for j in range(i*i, N+10, i): s[j] = 0
    primes = [i for i in range(2, N+10) if s[i]]
    vals = [n*n+1 for n in range(N+1)]
    factors = [[] for _ in range(N+1)]
    for p in primes:
        if p == 2: roots = [1]
        elif p%4 == 3: continue
        else:
            r = pow(2, (p-1)//4, p)
            if (r*r+1)%p != 0:
                r = next(x for x in range(1,p) if (x*x+1)%p == 0)
            roots = [r, p-r]
        for r in roots:
            n = r
            if n == 0 or n > N: continue
            while n <= N:
                v = vals[n]; e = 0
                while v%p == 0: v //= p; e += 1
                vals[n] = v
                if e: factors[n].append((p, e))
                n += p
    for n in range(1, N+1):
        if vals[n] > 1: factors[n].append((vals[n], 1))
    return factors

def Sigma_star(X):
    if X<=1: return 0
    L = math.log(X)
    return A3*L**3/6 + A2*L**2/2 + A1*L + A0

def Sigma_3_2term(M):
    if M<=1: return 0
    L = math.log(M)
    return b2p*L**2/2 + b1p*L

# Run comparison at five N (extended 2026-05-06 to N=10^6)
print('\n' + '='*100)
print(f'{"N":>8} {"L":>7} {"|range|":>9} {"W/N":>9} {"P2/N":>9} {"P3/N":>9} {"(W-P2)/N":>11} {"(W-P3)/N":>11} {"S3/pred":>9}')
print('='*100)
for N in [10000, 30000, 100000, 300000, 1000000]:
    t0 = time.time()
    factors = factor_n2plus1_array(N)
    t_factor = time.time() - t0
    K = int(math.ceil(math.log2((N*N+1)/N)))
    inf_edge = N * (1 << (K-1))
    sup_edge = N*N + 1
    n_lo = int(math.floor(math.sqrt(inf_edge - 1)))
    W = 0
    S3 = 0
    for n in range(1, N+1):
        tausq = 1
        for (p, e) in factors[n]: tausq *= (2*e+1)
        S3 += tausq
        v = n*n+1
        if n > n_lo and v > inf_edge and v <= sup_edge:
            W += tausq
    P2 = N * (Sigma_star(sup_edge) - Sigma_star(inf_edge))
    L_N = math.log(N); L_n = math.log(n_lo) if n_lo > 1 else 0
    P3 = (2*b2p*N*L_N**2 + 2*b1p*N*L_N) - (2*b2p*n_lo*L_n**2 + 2*b1p*n_lo*L_n)
    pred_S3 = 2*b2p*N*L_N**2 + 2*b1p*N*L_N
    ratio_S3 = S3 / pred_S3
    print(f'{N:>8} {L_N:>7.3f} {N-n_lo:>9} {W/N:>9.4f} {P2/N:>9.4f} {P3/N:>9.4f} {(W-P2)/N:>11.4f} {(W-P3)/N:>11.4f} {ratio_S3:>9.4f}    [factor {t_factor:.1f}s]')
