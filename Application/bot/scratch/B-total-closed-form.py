"""
Refined closed-form heuristic for B^infty (sums all omega(q) contributions).

Derivation: B(N)/N ~ (1/(4 log N)) * E[tau^*(n^2+1) log Q(n^2+1)]

  log Q(m) = sum_p nu_p^+(m) log p, with nu_p^+ = max(v_p-1, 0).

Hence sum_n tau^*(n^2+1) log Q = sum_p log p sum_n tau^*(n^2+1) nu_p^+(n^2+1).

For each fixed split prime p ≡ 1(4):
  sum_n tau^*(n^2+1) (v_p - 1)·1[v_p>=2]
  ~ N · c_1 log N · (2p/(p+2)) · sum_{k>=2} (k-1)(2/p^k)(1-1/p)
  = N · c_1 log N · 4 / ((p+2)(p-1))

(where (2p/(p+2)) = E[tau^*|v_p=k]/E[tau^*] for k>=1, by conditional independence.)

Therefore:
  B^infty ~ c_1 sum_{p ≡ 1 mod 4} log p / ((p+2)(p-1))

This is the TOTAL B^infty heuristic — sums over ALL omega(q) contributions
because nu_p^+ multi-counts in the obvious way (a max-sqfull q with omega=2 is
counted once for each p|q in the per-p sum).

Note: this differs from the per-q decomposition by a "joint vs marginal"
correction. Compare with empirical to see which one is closer.
"""

import math
import sys

R = math.pi / 4
H1 = 0.5526721690
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
    P = 10_000_000
    primes = primes_up_to(P)
    sp1 = [p for p in primes if p % 4 == 1]
    print(f"primes ≡ 1 mod 4 up to {P}: {len(sp1)}")
    print(f"c_1 = pi H(1)/2 = {c1:.10f}")
    print()

    # Sum the §6-style closed form: c_1 sum_p log p / ((p+2)(p-1))
    S = 0.0
    cumsum_table = []
    for p in sp1:
        term = math.log(p) / ((p+2)*(p-1))
        S += term
        cumsum_table.append((p, S))

    print("Cumulative sum of log p/((p+2)(p-1)) over p ≡ 1 mod 4:")
    for cap in [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 200, 1000, 10000, 100000, 1000000, 10000000]:
        for i, (p, total) in enumerate(cumsum_table):
            if p > cap:
                break
        else:
            i = len(cumsum_table)
        if i > 0:
            p_at = cumsum_table[i-1][0]
            print(f"  p ≤ {cap:>7}: S_truncated={cumsum_table[i-1][1]:.7f}, c_1·S = {c1 * cumsum_table[i-1][1]:.7f}")

    print()
    print(f"FINAL §6-style heuristic prediction (p ≤ 10^7): B^infty ≈ {c1 * S:.7f}")
    print()
    print("Empirical B^infty:")
    print(f"  N=10^4:    0.0880")
    print(f"  N=3·10^4: 0.0859")
    print(f"  N=10^5:    0.0867")
    print(f"  N=3·10^5: 0.0863")
    print(f"  N=10^6:    0.0857")
    print()
    print("If §6 closed form > empirical: §6 over-predicts, so the 'uniform-in-log'")
    print("    assumption inside the (1/4 log N) factor over-estimates the divisor count.")
    print("If close: §6 closed form is essentially correct (up to a small correction).")


if __name__ == '__main__':
    main()
