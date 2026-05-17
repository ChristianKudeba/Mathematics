"""
Debug: sum_{e sf, e <= X} rho(e) and rho(e)/e.

The Mellin claim is:
   sum_{e sf, e <= X} rho(e) ~ R H(1) X = 0.4341 X.

Verify directly at large X.
"""
import math, time

GAMMA = 0.5772156649015328606
LPRIME_1_CHI4 = 0.19290131767382030
GAMMA_K = (math.pi/4) * GAMMA + LPRIME_1_CHI4
R = math.pi/4

def rho_sf(d):
    if d == 1: return 1
    n = d
    rho = 1
    if n % 2 == 0:
        if n % 4 == 0: return 0
        n //= 2
        # rho(2) = 1
    p = 3
    while p*p <= n:
        if n % p == 0:
            if n % (p*p) == 0:
                return 0
            n //= p
            if p % 4 == 1:
                rho *= 2
            else:
                return 0
        p += 2
    if n > 1:
        if n % 4 == 1:
            rho *= 2
        elif n % 4 == 3:
            return 0
    return rho


def main():
    print("=== sum_{e sf, e <= X} rho(e) and rho(e)/e ===")
    print(f"{'X':>8} {'sum_rho':>10} {'sum_rho/X':>10} {'sum_rho/e':>12} {'pred':>10}")
    H1 = 0.5526721690
    Hp1 = 0.8355849429
    R = math.pi/4
    pred_density = R * H1
    pred_const = R * Hp1 + GAMMA_K * H1
    print(f"  predicted density = R H(1) = {pred_density:.6f}")
    print(f"  predicted constant = R H'(1) + gamma_K H(1) = {pred_const:.6f}")
    print()
    for X in [100, 1000, 10000, 100000, 1000000]:
        t0 = time.time()
        s_rho = 0
        s_rhoe = 0.0
        for d in range(1, X+1):
            r = rho_sf(d)
            if r > 0:
                s_rho += r
                s_rhoe += r/d
        L = math.log(X)
        pred_rhoe = pred_density * L + pred_const
        print(f"{X:>8} {s_rho:>10} {s_rho/X:>10.6f} {s_rhoe:>12.6f} {pred_rhoe:>10.6f}  diff={s_rhoe-pred_rhoe:.4f}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
