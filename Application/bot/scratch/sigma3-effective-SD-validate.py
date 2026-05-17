"""
Numerical validation of effective Selberg-Delange on
    Sigma_3(X) := sum_{d <= X} 2^omega(d) rho(d) / d
where rho(d) = #{x mod d : x^2 == -1 mod d}.

Selberg-Delange (Tenenbaum II.5.2) applied to the multiplicative
function f(d) = 2^omega(d) rho(d) gives, via T_3(s) = zeta_K(s)^2 H_3(s)
with H_3 analytic on Re s > 1/2 and H_3(1) != 0 (and zeta_K = zeta L(.,chi_4)
so the Vinogradov-Korobov zero-free region transfers), for any A > 0:
    Sigma_3(X) = c_2 (log X)^2/2 + c_1 log X + c_0 + O_A((log X)^{-A}).

Constants from prior session:
  c_2 = R^2 H_3(1)                  approx 0.17133
  c_1 = R^2 H_3'(1) + 2R gamma_K H_3(1)   approx 0.80157
  c_0 = R^2 H_3''(1)/2 + 2R gamma_K H_3'(1) + (gamma_K^2 + 2R beta_K) H_3(1)
                                    approx 0.93878

Compute Sigma_3(X) by direct enumeration of supported d (= 2^a * m, a in {0,1},
m odd composed of primes p == 1 mod 4) up to X.

Then compare the residual r(X) := Sigma_3(X) - 3-term Laurent.
"""
import math, time

# Predictions (recomputed below from clean constants)
H3_1     = 0.27775120
H3_p1    = 0.84240798     # H_3'(1)
H3_pp1   = -0.234         # H_3''(1)
gamma_K  = 0.6462
beta_K   = 0.0915
R        = math.pi/4

c2 = R**2 * H3_1
c1 = R**2 * H3_p1 + 2*R*gamma_K * H3_1
c0 = R**2 * H3_pp1/2 + 2*R*gamma_K*H3_p1 + (gamma_K**2 + 2*R*beta_K)*H3_1

print(f"c_2 = {c2:.6f}")
print(f"c_1 = {c1:.6f}")
print(f"c_0 = {c0:.6f}")
print()

# Compute Sigma_3(X) for various X via direct sieve.
# Strategy: enumerate squarefree-shaped divisors of the right form.
# rho(d) for d in support of rho: d = 2^a * m, a in {0,1}, m squarefree?
# NO -- m can have repeated prime factors as long as p == 1 mod 4.
# Hensel: rho(p^k) = 2 for all k >= 1 if p == 1 mod 4. rho(2) = 1, rho(2^k)=0 for k>=2.
# Hence rho(d) = 0 unless d = 2^a m, a in {0,1}, m = prod p_i^{e_i} with p_i == 1 mod 4.
# In that case rho(d) = 2^{omega(m)} (one factor of 2 per distinct split prime).
# So 2^omega(d) rho(d) = 2^{a + omega(m)} * 2^{omega(m)} = 2^{a + 2 omega(m)}.

# Build sieve of d up to X_MAX, computing the contribution to Sigma_3.
def compute_sigma3(X_MAX):
    """Return (X_list, sigma3_list) at decade values up to X_MAX."""
    # Sieve: for each d <= X_MAX, mark whether in support and compute 2^omega(d) rho(d).
    # Memory: array of length X_MAX+1.
    # Strategy: factor each d by trial sieve over primes <= sqrt(X_MAX).
    # Since X_MAX up to ~10^7, this needs care.

    # Use multiplicative-function sieve (linear sieve modified).
    # Each d has smallest prime factor p; build f(d) recursively.

    f = [0]*(X_MAX+1)  # f(d) = 2^omega(d) * rho(d), integer
    f[1] = 1
    # smallest prime factor
    spf = [0]*(X_MAX+1)
    for i in range(2, X_MAX+1):
        if spf[i] == 0:
            for j in range(i, X_MAX+1, i):
                if spf[j] == 0:
                    spf[j] = i
    # Now compute f
    for d in range(2, X_MAX+1):
        p = spf[d]
        # factor out highest power of p in d
        m = d
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        # m = d / p^e, gcd(m, p) = 1
        # f(d) = f_local(p, e) * f(m)
        if p == 2:
            # f(2) = 2^omega(2) rho(2) = 2 * 1 = 2; f(2^k) = 0 for k >= 2 (since rho(4) = 0)
            if e == 1:
                local = 2
            else:
                local = 0
        elif p % 4 == 1:
            # f(p^e) = 2^omega(p^e) rho(p^e) = 2 * 2 = 4 for any e >= 1
            local = 4
        else:
            # p == 3 mod 4: rho(p^e) = 0
            local = 0
        f[d] = local * f[m]

    # Now Sigma_3(X) = sum_{d <= X} f(d) / d
    # Compute as cumulative.
    targets = [10**k for k in range(3, int(math.log10(X_MAX))+1)]
    if X_MAX > targets[-1] * 3:
        targets.append(3 * targets[-1])
    targets.append(X_MAX)
    targets = sorted(set(t for t in targets if t <= X_MAX))

    out = []
    s = 0.0
    ti = 0
    for d in range(1, X_MAX+1):
        if f[d] != 0:
            s += f[d] / d
        while ti < len(targets) and targets[ti] == d:
            out.append((d, s))
            ti += 1
    return out

print("Running sieve ...")
t0 = time.time()
results = compute_sigma3(10**7)
print(f"Sieve done in {time.time()-t0:.1f}s")
print()

print(f"{'X':>10} {'Sigma_3(X)':>14} {'3-term Laurent':>16} {'residual':>14} {'L^A residual':>30}")
for (X, sigma3) in results:
    L = math.log(X)
    pred = c2 * L**2 / 2 + c1 * L + c0
    resid = sigma3 - pred
    # show residual scaled by L^A for A = 1, 2, 3, 4
    scaled = " ".join(f"L^{A} r={resid * L**A:>8.3f}" for A in (1, 2, 3, 4))
    print(f"{X:>10} {sigma3:>14.6f} {pred:>16.6f} {resid:>14.6f}  {scaled}")
