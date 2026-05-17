"""
Verifies, at small N (up to 3e4):
  1. b(n) = #{e sf | n^2+1 : e <= n} - 2^{omega-1} (pointwise)
  2. B(N) = U(N) - T(N)/2 (cumulative, exact integer identity)
  3. U(N)/N - a_1 log N -> c_<^infty - a_1 = 0.5794 (asymptotic)

a_1 = R H(1), R = pi/4, H(1) = 0.5526721.
c_<^infty = R H'(1) + gamma_K H(1) = 1.013430.
Therefore c_<^infty - a_1 = 0.579362.
"""
import math

def factor(m):
    fs = {}
    d = 2
    while d*d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    return fs

def divisors_of_rad(m):
    fs = factor(m)
    divs = [1]
    for p in fs:
        divs = divs + [d * p for d in divs]
    return divs

def b_pointwise(n):
    """g(n) = #{e | rad(m) : sqrt(rad) < e <= n}, m=n^2+1, with sf m -> 0."""
    m = n*n+1
    fs = factor(m)
    if all(e == 1 for e in fs.values()):
        return 0
    r = 1
    for p in fs:
        r *= p
    sfdivs = divisors_of_rad(m)
    return sum(1 for e in sfdivs if e*e > r and e <= n)

def U_pointwise(n):
    m = n*n+1
    sfdivs = divisors_of_rad(m)
    return sum(1 for e in sfdivs if e <= n)

def T_pointwise(n):
    fs = factor(n*n+1)
    return 1 << len(fs)  # 2^omega

def b_via_identity(n):
    m = n*n+1
    fs = factor(m)
    omega = len(fs)
    return U_pointwise(n) - (1 << (omega-1))

# Pointwise check
mismatches = sum(1 for n in range(1, 5001) if b_pointwise(n) != b_via_identity(n))
assert mismatches == 0, f"Identity failed at {mismatches} positions"
print(f"Pointwise identity b(n) = U_count - 2^(omega-1) verified for n in [1, 5000]")

# Cumulative check
NS = [1000, 3000, 10000, 30000]
B_total = 0; U_total = 0; T_total = 0
a1 = (math.pi/4) * 0.5526720946  # R*H(1)
c_lt_inf_minus_a1 = 0.579362  # c_<^infty - a_1

results = []
for n in range(1, max(NS)+1):
    B_total += b_pointwise(n)
    U_total += U_pointwise(n)
    T_total += T_pointwise(n)
    if n in NS:
        diff = U_total - T_total/2 - B_total
        UN_norm = U_total/n - a1*math.log(n)
        results.append((n, B_total, U_total, T_total, diff, UN_norm))

print(f"\n{'N':>8} {'B(N)':>8} {'U(N)':>10} {'T(N)':>10} {'U-T/2-B':>10} {'U/N-a1*lnN':>12} {'gap':>10}")
for n, B, U, T, d, un in results:
    print(f"{n:>8} {B:>8} {U:>10} {T:>10} {d:>10.1f} {un:>12.6f} {un - c_lt_inf_minus_a1:>+10.4f}")
