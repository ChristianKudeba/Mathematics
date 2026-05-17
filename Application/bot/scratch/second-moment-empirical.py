"""
Empirical second-moment scaling of T(M) over dyadic windows [N, 2N].

We have sparse samples T(M_k) at stride ~1000 in M up to N_max = 5e7.
Approximate sum_{M in [N,2N]} T(M)^2 by (stride) * sum_k T(M_k)^2 over
sparse sample points in [N, 2N]. This is accurate to leading order
because T(M)^2 changes slowly on scale << sqrt(M).

Goal: see whether sum_M T(M)^2 ~ C * N^2 (clean) or N^2 log^c N
(needs polylog correction). Conjecture C' predicts ~ N^2.
"""

import math
import pickle

def main():
    with open('/home/user/mathAI/bot/scratch/Tcum.pkl', 'rb') as f:
        sparse = pickle.load(f)
    # sparse is list of (N, T(N)).
    Ms = [n for n, _ in sparse]
    Ts = [t for _, t in sparse]
    if Ms[0] == 0:
        Ms = Ms[1:]; Ts = Ts[1:]
    stride = Ms[1] - Ms[0]
    Nmax = Ms[-1]
    print(f"# sparse samples: {len(Ms)}, stride={stride}, Nmax={Nmax}")

    print()
    print(f"{'N':>10}  {'samples':>8}  {'sum T^2':>14}  {'~int T^2':>14}  {'/N^2':>8}  {'/(N^2 logN)':>12}  {'/(N^2 log^2 N)':>15}")

    # dyadic windows
    Ns = [10**k for k in range(3, 8)] + [3 * 10**k for k in range(3, 8)]
    Ns = sorted(N for N in Ns if 2*N <= Nmax)

    for N in Ns:
        # collect samples in (N, 2N]
        S2 = 0
        cnt = 0
        for M, T in zip(Ms, Ts):
            if N < M <= 2*N:
                S2 += T * T
                cnt += 1
        if cnt < 5:
            continue
        approx_int = S2 * stride  # discrete approx of sum_M T(M)^2
        N2 = N * N
        logN = math.log(N)
        print(f"{N:>10}  {cnt:>8}  {S2:>14}  {approx_int:>14}  {approx_int/N2:>8.4f}  {approx_int/(N2*logN):>12.4f}  {approx_int/(N2*logN*logN):>15.4f}")

    print()
    print("Also: full-range second moment / N_max^2:")
    full = sum(t*t for t in Ts)
    full_int = full * stride
    print(f"  sum over [0, {Nmax}] of T^2: {full} (sparse), ~{full_int} integrated, /N_max^2 = {full_int/(Nmax*Nmax):.4f}, /(N_max^2 log N_max) = {full_int/(Nmax*Nmax*math.log(Nmax)):.4f}")

if __name__ == '__main__':
    main()
