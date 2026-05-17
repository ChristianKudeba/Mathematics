"""
Numerical verification of the rigorous bounds on D_0(N) from P12-D0-rigorous.md.

For each test N, compute:
  A(x) := sum_{d <= x, L_odd} 2^omega(d)
  B(x) := sum_{d <= x, L_odd} d * 2^omega(d)
Then evaluate the Theorem 4, 5, 6 explicit (NOT asymptotic) bounds:
  Thm 4 (clean UB):   D_0(N) <= 4N * A(2N)
  Thm 5 (sharper UB): D_0(N) <= 4 [ (N/2) A(N/4) + 2 B(N/4) + N (A(2N) - A(N/4)) ]
  Thm 6 (LB):         D_0(N) >= 4 [ (N/2) A(N/4) - 2 B(N/4) ]

Compare against the empirical D_0(N) values from P12-second-moment-diagonal.md:
  N=1000  -> D_0 = 745072      / N^2 = 0.7451
  N=2000  -> D_0 = 3012536     / N^2 = 0.7531
  N=5000  -> D_0 = 18685508    / N^2 = 0.7474
  N=10000 -> D_0 = 74754968    / N^2 = 0.7475
"""
import math, sys

def compute_AB(xmax):
    sieve = bytearray([1])*(xmax+1); sieve[0]=sieve[1]=0
    for i in range(2, int(math.isqrt(xmax))+1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00'*len(sieve[i*i::i])
    spf = list(range(xmax+1))
    for p in range(2, xmax+1):
        if sieve[p]:
            for j in range(p, xmax+1, p):
                if spf[j] == j:
                    spf[j] = p
    A = [0]*(xmax+1)
    B = [0]*(xmax+1)
    for d in range(1, xmax+1):
        n = d
        ok = True
        last_p = 0
        w = 0
        while n > 1:
            p = spf[n]
            if p % 4 != 1:
                ok = False; break
            if p != last_p:
                w += 1; last_p = p
            n //= p
        if ok:
            r = (1 << w)
            A[d] = A[d-1] + r
            B[d] = B[d-1] + d*r
        else:
            A[d] = A[d-1]
            B[d] = B[d-1]
    return A, B

def main():
    xmax = 20000
    A, B = compute_AB(xmax)
    emp_D0 = {1000: 745072, 2000: 3012536, 5000: 18685508, 10000: 74754968}
    print(f"{'N':>6}  {'emp D_0':>14}  {'emp/N^2':>9}  {'LB':>14}  {'LB/N^2':>9}  {'Thm5 UB':>14}  {'UB5/N^2':>9}  {'Thm4 UB':>14}  {'UB4/N^2':>9}")
    for N in [1000, 2000, 5000, 10000]:
        if 2*N > xmax:
            continue
        # Thm 4: 4N * A(2N)
        ub4 = 4*N * A[2*N]
        # Thm 5: 4 [(N/2) A(N/4) + 2 B(N/4) + N (A(2N) - A(N/4))]
        d_star = N // 4
        ub5 = 4 * ((N//2)*A[d_star] + 2*B[d_star] + N*(A[2*N] - A[d_star]))
        # Thm 6: 4 [(N/2) A(N/4) - 2 B(N/4)]
        lb = 4 * ((N//2)*A[d_star] - 2*B[d_star])
        emp = emp_D0[N]
        print(f"{N:>6}  {emp:>14}  {emp/(N*N):>9.4f}  {lb:>14}  {lb/(N*N):>9.4f}  {ub5:>14}  {ub5/(N*N):>9.4f}  {ub4:>14}  {ub4/(N*N):>9.4f}")
    print()
    print(f"Asymptotic constants:")
    print(f"  LB asymp:    1/(4*pi) = {1/(4*math.pi):.4f}")
    print(f"  Thm 5 asymp: 31/(4*pi) = {31/(4*math.pi):.4f}")
    print(f"  Thm 4 asymp: 8/pi = {8/math.pi:.4f}")
    print(f"  empirical D_0/N^2 ~ 0.7475")

if __name__ == '__main__':
    main()
