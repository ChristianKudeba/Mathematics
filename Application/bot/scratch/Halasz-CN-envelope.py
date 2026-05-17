"""
Empirical C(N) measurement for Theorem F.2 of session 2026-05-10 09:54.

Theorem F.2 says: |R(N,H) - 1| <= C(N)/H, with C(N) = 2 C_num(N)/A(N), where
    C_num(N) = sum_{e1 != e2, eps1, eps2} 1/|sin(pi * beta)|
    beta = tilde_alpha_eps1(e1) + tilde_alpha_eps2(e2)  (mod 1)
    A(N)  = sum_{e sf-good <= N} 2^omega'(e), omega'(e) = omega(e) - [2|e]
    tilde_alpha_eps(e) = sum_{p|e, p>2} eps_p * a_p^{(e)}/p + [2|e]/2
    a_p^{(e)} = alpha_p * inverse(e/p) mod p, where alpha_p^2 = -1 mod p

Pickup-hint #1 question: is C(N) polynomial in N (specifically O(N^{2-delta}))?
If so, F.2 gives a non-trivial bound at H = N. Expected: C(N) >> N^2 due to
small sin(pi*beta) tails.
"""

import numpy as np
from sympy import sqrt_mod


def main():
    Ns = [20, 50, 100, 200, 500, 1000, 2000]
    Nmax = max(Ns)

    # Smallest-prime-factor sieve for fast factorization
    spf = np.zeros(Nmax + 1, dtype=int)
    for i in range(2, Nmax + 1):
        if spf[i] == 0:
            for j in range(i, Nmax + 1, i):
                if spf[j] == 0:
                    spf[j] = i

    # alpha_p = sqrt(-1) mod p, for p prime, p == 1 mod 4
    alpha = {}
    for p in range(3, Nmax + 1, 2):
        if spf[p] != p:
            continue
        if p % 4 != 1:
            continue
        alpha[p] = int(sqrt_mod(-1, p))

    def factor(n):
        f = []
        while n > 1:
            p = int(spf[n])
            f.append(p)
            n //= p
            if n % p == 0:
                return None  # not squarefree
        return f

    def is_good(factors):
        return all(p == 2 or p % 4 == 1 for p in factors)

    print(f"{'N':>4} {'#(e,eps)':>9} {'A(N)':>6} {'C_num':>14} {'C_num/A':>10} {'C_num/A^2':>11} {'C_num/N':>10} {'C_num/N^2':>11}")

    rows = []
    for N in Ns:
        e_arr = []
        a_arr = []

        for e in range(2, N + 1):
            f = factor(e)
            if f is None or not is_good(f):
                continue
            odd = [p for p in f if p > 2]
            n_odd = len(odd)
            has2 = (2 in f)

            # a_p^{(e)} for each odd p | e
            a_pe = []
            for p in odd:
                ep_mod = (e // p) % p
                ep_inv = pow(int(ep_mod), -1, p)
                a_pe.append((alpha[p] * ep_inv) % p)

            # All 2^n_odd sign patterns
            for mask in range(1 << n_odd):
                val = 0.0
                for i, p in enumerate(odd):
                    eps = 1 if (mask >> i) & 1 == 0 else -1
                    val += eps * a_pe[i] / p
                if has2:
                    val += 0.5
                val = val - np.floor(val)
                e_arr.append(e)
                a_arr.append(val)

        e_np = np.array(e_arr, dtype=np.int64)
        a_np = np.array(a_arr, dtype=np.float64)
        n_pts = len(e_np)

        # Pairwise beta_ij = a_i + a_j mod 1, reduced to [-1/2, 1/2]
        beta = (a_np[:, None] + a_np[None, :]) % 1.0
        beta = np.where(beta > 0.5, beta - 1.0, beta)

        sin_vals = np.abs(np.sin(np.pi * beta))
        # By Lemma F.1, sin > 0 strict where e_i != e_j
        e_diff_mask = e_np[:, None] != e_np[None, :]
        # Where e_i == e_j, set to 0 (we exclude). Where e_i != e_j, sin > 0.
        # Add tiny epsilon to all sin values for safety (only diagonal would be 0)
        inv_sin = np.where(e_diff_mask, 1.0 / np.maximum(sin_vals, 1e-30), 0.0)

        C_num = float(np.sum(inv_sin))
        A = n_pts

        row = (N, n_pts, A, C_num, C_num / A, C_num / A**2, C_num / N, C_num / N**2)
        rows.append(row)
        print(f"{N:4d} {n_pts:9d} {A:6d} {C_num:14.4e} {C_num/A:10.4e} {C_num/A**2:11.4e} {C_num/N:10.4e} {C_num/N**2:11.4e}")

    # Fit C_num ~ N^p
    print()
    print("Power-law fits (log-log slope):")
    Ns_arr = np.array([r[0] for r in rows], dtype=float)
    Cnum_arr = np.array([r[3] for r in rows], dtype=float)
    A_arr = np.array([r[2] for r in rows], dtype=float)
    log_N = np.log(Ns_arr)
    log_C = np.log(Cnum_arr)
    slope_C, intercept_C = np.polyfit(log_N, log_C, 1)
    print(f"  C_num(N) ~ exp({intercept_C:.3f}) * N^{slope_C:.3f}")
    log_A = np.log(A_arr)
    slope_A, intercept_A = np.polyfit(log_N, log_A, 1)
    print(f"  A(N)     ~ exp({intercept_A:.3f}) * N^{slope_A:.3f}")
    log_CA = np.log(Cnum_arr / A_arr)
    slope_CA, intercept_CA = np.polyfit(log_N, log_CA, 1)
    print(f"  C(N)=C_num/A ~ exp({intercept_CA:.3f}) * N^{slope_CA:.3f}")

    # Pairwise slopes (for non-uniform growth detection)
    print()
    print("Pairwise log-log slopes (consecutive Ns):")
    for i in range(1, len(Ns)):
        s_C = np.log(Cnum_arr[i] / Cnum_arr[i-1]) / np.log(Ns_arr[i] / Ns_arr[i-1])
        s_A = np.log(A_arr[i] / A_arr[i-1]) / np.log(Ns_arr[i] / Ns_arr[i-1])
        print(f"  N={Ns[i-1]}->{Ns[i]}: slope_C={s_C:.3f}  slope_A={s_A:.3f}")

    # Test model C(N) ~ c*N*log(N)
    print()
    print("Model C(N) = C_num/A vs c*N*log(N):")
    CA_arr = Cnum_arr / A_arr
    for i in range(len(Ns)):
        ratio = CA_arr[i] / (Ns_arr[i] * np.log(Ns_arr[i]))
        print(f"  N={Ns[i]:5d}: C(N)={CA_arr[i]:10.2f}  N*log(N)={Ns_arr[i]*np.log(Ns_arr[i]):10.2f}  ratio={ratio:.4f}")

    # Test model C_num(N) ~ c*N^2*log(N)
    print()
    print("Model C_num(N) vs c*N^2*log(N):")
    for i in range(len(Ns)):
        ratio = Cnum_arr[i] / (Ns_arr[i]**2 * np.log(Ns_arr[i]))
        print(f"  N={Ns[i]:5d}: C_num={Cnum_arr[i]:12.2f}  N^2*log(N)={Ns_arr[i]**2*np.log(Ns_arr[i]):12.2f}  ratio={ratio:.4f}")


if __name__ == "__main__":
    main()
