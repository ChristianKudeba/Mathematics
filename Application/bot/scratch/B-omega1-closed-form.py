"""
Analytic prediction for the omega(q)=1 contribution to B^infty.

Heuristic derivation (refined §6 with local-factor correction):
  B^infty_{omega=1} = sum_{p ≡ 1 mod 4} sum_{v >= 2} D_{p^v} * E_{p^v}
where
  D_{p^v} = C_0 * 2(p-1)/(p^{v+1}(1 - 2/p^2))  (analytic density of max sqfull = p^v)
  E_{p^v} ~ M_p * c_1 * (v-1) * log p / 4
        where c_1 = pi*H(1)/2 ≈ 0.8681 (leading-order const in T(N)/N log N),
              M_p = E[tau^*(n^2+1) | max sqfull = p^v] / E[tau^*(n^2+1)]
                  = (2/(1+2/p)) * prod_{p' ≡ 1(4), p' ≠ p} (E_p'[tau^*|v<=1] / E_p'[tau^*])

Summation over v: closed form
  sum_{v>=2} D_{p^v} E_{p^v} = (C_0 * c_1 * M_p * p * log p) / (2 (p^2-2)(p-1)).

Total over p:
  B^infty_{omega=1} ~ sum_{p ≡ 1 mod 4} (C_0 c_1 M_p p log p) / (2 (p^2-2)(p-1)).

This script computes this and compares to empirical 0.0779 at N=10^5,3·10^5.
"""

import math

R = math.pi / 4
H1 = 0.5526721690
HP1 = 0.8355849429
c1 = math.pi * H1 / 2  # 0.86813...

def primes_up_to(M):
    if M < 2: return []
    sv = bytearray(b"\x01") * (M+1)
    sv[0] = sv[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sv[p]:
            sv[p*p::p] = bytearray(len(sv[p*p::p]))
    return [p for p in range(M+1) if sv[p]]


def main():
    P = 1_000_000
    primes = primes_up_to(P)
    sp1 = [p for p in primes if p % 4 == 1]
    print(f"primes ≡ 1 mod 4 up to {P}: {len(sp1)}")

    # C_0 = prod_{p ≡ 1 mod 4} (1 - 2/p^2)
    C0 = 1.0
    for p in sp1:
        C0 *= (1 - 2.0/(p*p))
    # Tail correction: log C_0_tail ~ -2 sum_{p > P, p ≡ 1 mod 4} 1/p^2 ~ -1/(P log P)
    tail_C0_log = -2 * 0.5 / (P * math.log(P))
    C0 *= math.exp(tail_C0_log)
    print(f"C_0 = {C0:.10f}")

    # Compute M_p = (2/(1+2/p)) * prod_{p' ≠ p} factor
    # Use approximation: M_p ≈ 2p/(p+2) (leading), with correction
    # For each p, M_p^full = (2/(1+2/p)) * Π_{p' ≡ 1(4), p' ≠ p} g(p')
    # where g(p') = E_{p'}[tau^*|v <=1] / E_{p'}[tau^*] = ((1+2/p'-4/p'^2)/(1-2/p'^2)) / (1+2/p')

    # Precompute G = prod g(p') over all p' ≡ 1 mod 4
    G_full = 1.0
    for p in sp1:
        num = 1 + 2.0/p - 4.0/(p*p)
        den = (1 - 2.0/(p*p)) * (1 + 2.0/p)
        G_full *= num/den
    print(f"G_full (prod_p' g(p')) = {G_full:.10f}")

    print()
    print(f"{'p':>5} {'D_{p^>=2}':>12} {'M_p~':>10} {'(D·E)_{p^>=2}':>16} {'(D·E) leading':>16}")

    total = 0.0
    total_lead = 0.0
    cumsum_table = []
    for p in sp1:
        # Single-prime aggregate density
        D_p_total = 2 * C0 / (p*p - 2)  # = sum_{v >= 2} D_{p^v}
        # M_p exact (relative to leading c_1 log N)
        g_p = ((1 + 2.0/p - 4.0/(p*p)) / (1 - 2.0/(p*p))) / (1 + 2.0/p)
        M_p_full = (2 / (1 + 2.0/p)) * (G_full / g_p)  # remove p's own factor
        # Closed form for sum_v D E:
        # = (C_0 c_1 M_p p log p) / (2 (p^2-2)(p-1))
        DE_full = C0 * c1 * M_p_full * p * math.log(p) / (2 * (p*p - 2) * (p - 1))
        # Leading version (M_p ≈ 2p/(p+2))
        Mp_lead = 2*p / (p+2)
        DE_lead = C0 * c1 * Mp_lead * p * math.log(p) / (2 * (p*p - 2) * (p - 1))
        total += DE_full
        total_lead += DE_lead
        cumsum_table.append((p, total, total_lead))
        if p < 200:
            print(f"{p:>5} {D_p_total:>12.6f} {M_p_full:>10.4f} {DE_full:>16.7f} {DE_lead:>16.7f}")

    print()
    print(f"Total B^infty_{{omega=1}}, full M_p: {total:.6f}")
    print(f"Total B^infty_{{omega=1}}, leading M_p (=2p/(p+2)): {total_lead:.6f}")
    print(f"Empirical at N=10^5:    0.0779")
    print(f"Empirical at N=3·10^5: 0.0779 (stable)")
    print()
    # Also show partial sums
    print("Partial sum vs cumulative cap:")
    print(f"  through p ≤ 5:    full={cumsum_table[0][1]:.6f}")
    for cap in [13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 200, 1000, 10000, 100000]:
        for i, (p, full, lead) in enumerate(cumsum_table):
            if p > cap:
                break
        else:
            i = len(cumsum_table)
        if i > 0:
            print(f"  through p ≤ {cap}: full={cumsum_table[i-1][1]:.6f}  lead={cumsum_table[i-1][2]:.6f}")


if __name__ == '__main__':
    main()
