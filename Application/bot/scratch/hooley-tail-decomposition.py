"""
Hooley boundary decomposition diagnostic.

Goal: split S(N) = sum_{n<=N} tau(n^2+1)^2 = sum_d tau(d^2) N_d(N) into:
  S_<(N) := sum_{d<=N} tau(d^2) N_d(N)
  S_>(N) := sum_{d>N}  tau(d^2) N_d(N)   "Hooley tail"

and compare:
  S_<(N) vs N*Sigma_*(N) (rigorous identity is S_<(N) - N*Sigma_*(N) = small)
  S_>(N) vs N*(Sigma_*(N^2) - Sigma_*(N)) (formal-SD prediction for tail)

Where Sigma_*(X) := sum_{d<=X} tau(d^2) rho(d) / d.

Run for N in {10^3, 10^4, 10^5, 10^6} and report.
"""
import math
from array import array

def primerange(a, b):
    if b <= 2: return
    sieve_arr = bytearray([1]) * b
    sieve_arr[0] = sieve_arr[1] = 0
    for i in range(2, int(b**0.5) + 1):
        if sieve_arr[i]:
            for j in range(i*i, b, i):
                sieve_arr[j] = 0
    for i in range(max(a, 2), b):
        if sieve_arr[i]:
            yield i

def factor_n2plus1(N):
    """Returns factors[n] = list of (p,e) for n^2+1 = prod p^e, 1<=n<=N."""
    vals = [n*n + 1 for n in range(N + 1)]
    factors = [[] for _ in range(N + 1)]
    p_bound = N + 5
    primes = list(primerange(2, p_bound + 1))
    for p in primes:
        if p == 2:
            roots = [1]
        elif p % 4 == 3:
            continue
        else:
            r = None
            for x in range(1, p):
                if (x*x + 1) % p == 0:
                    r = x; break
            roots = [r, p - r]
        for r in roots:
            n = r
            if n > N or n == 0:
                continue
            while n <= N:
                v = vals[n]
                e = 0
                while v % p == 0:
                    v //= p; e += 1
                vals[n] = v
                if e:
                    factors[n].append((p, e))
                n += p
    for n in range(1, N + 1):
        if vals[n] > 1:
            factors[n].append((vals[n], 1))
    return factors

def split_S(factors, N):
    """Returns (S, S_small, S_large) at threshold N."""
    S_small = 0
    S_large = 0
    for n in range(1, N + 1):
        f = factors[n]
        # build divisors d, tau(d^2) recursively
        ds = [(1, 1)]
        for (p, e) in f:
            new_ds = []
            pk = 1
            for k in range(e + 1):
                t = 2*k + 1
                for (d, td2) in ds:
                    new_ds.append((d * pk, td2 * t))
                pk *= p
            ds = new_ds
        for (d, td2) in ds:
            if d <= N:
                S_small += td2
            else:
                S_large += td2
    return S_small + S_large, S_small, S_large

def sieve_a(X):
    """Returns array a[1..X] with a[d] = tau(d^2)*rho(d), and partial sums.
    a is multiplicative; sieved via smallest-prime-factor."""
    spf = array('i', [0]*(X+1))
    for i in range(2, X+1):
        if spf[i] == 0:
            for j in range(i, X+1, i):
                if spf[j] == 0:
                    spf[j] = i
    a = array('q', [0]*(X+1))
    a[1] = 1
    for d in range(2, X+1):
        p = spf[d]
        m = d; e = 0
        while m % p == 0:
            m //= p; e += 1
        if p == 2:
            local = 3 if e == 1 else 0
        elif p % 4 == 3:
            local = 0
        else:
            local = (2*e + 1) * 2
        a[d] = a[m] * local
    return a

def sigma_star(X, a=None):
    """Sigma_*(X) = sum_{d<=X} a[d]/d."""
    if a is None:
        a = sieve_a(X)
    total = 0.0
    for d in range(1, X + 1):
        if a[d]:
            total += a[d] / d
    return total

def sigma_star_range(D_lo, D_hi, a):
    """sum_{D_lo < d <= D_hi} a[d]/d."""
    total = 0.0
    for d in range(D_lo + 1, D_hi + 1):
        if a[d]:
            total += a[d] / d
    return total

def main():
    Ns = [10**3, 3*10**3, 10**4, 3*10**4, 10**5, 3*10**5]
    # Precompute a[] up to max N^2
    print("Sieving a[d] = tau(d^2)*rho(d) up to max N^2 ...")
    Xmax = max(Ns)**2
    # That's 10^12 — way too big. Just go up to 10^8 and do partial.
    # Actually for the formal-SD prediction we use the closed-form Laurent.
    Xmax = max(Ns)
    print(f"  building a[] up to {Xmax}")
    a = sieve_a(Xmax)

    # Precompute Sigma_*(N) for each N from a[]
    print("Computing Sigma_*(N) for each N ...")
    Sigma_at = {}
    cum = 0.0
    pos = 1
    sorted_Ns = sorted(Ns)
    for d in range(1, Xmax + 1):
        if a[d]:
            cum += a[d] / d
        while pos < len(sorted_Ns) and d == sorted_Ns[pos - 1]:
            Sigma_at[sorted_Ns[pos - 1]] = cum
            pos += 1
            if pos > len(sorted_Ns):
                break
    Sigma_at[sorted_Ns[-1]] = cum  # ensure largest captured

    # Closed-form Laurent inputs from prior sessions:
    A3 = 0.05971106
    A2 = 0.43491036
    A1 = 1.07159000
    A0 = 0.87930421
    def laurent(L):
        return A3 * L**3 / 6 + A2 * L**2 / 2 + A1 * L + A0
    def formal_tail(N):
        """Formal-SD prediction for Sigma_*(N^2) - Sigma_*(N)."""
        L1 = math.log(N)
        L2 = 2 * L1
        return laurent(L2) - laurent(L1)

    print("\nFor each N, compute split and compare.")
    print(f"\n{'N':>8} | {'S(N)':>13} | {'S_small':>13} | {'S_large':>13} | "
          f"{'N*Sigma_*':>13} | {'S_small-NSig':>13} | {'NSig(N^2)-NSig(N)':>17} | "
          f"{'S_large-formal':>14}")
    print("-" * 140)
    for N in Ns:
        print(f"  factoring n^2+1 for n<={N} ...", flush=True)
        factors = factor_n2plus1(N)
        print(f"  splitting divisors ...", flush=True)
        S, S_sm, S_lg = split_S(factors, N)
        Sig = Sigma_at[N]
        N_Sig = N * Sig
        sm_residual = S_sm - N_Sig
        # formal pred for S_>(N) is N * (Sigma_*(N^2) - Sigma_*(N)).
        formal_lg = N * formal_tail(N)
        lg_residual = S_lg - formal_lg
        print(f"{N:>8} | {S:>13} | {S_sm:>13} | {S_lg:>13} | "
              f"{N_Sig:>13.2f} | {sm_residual:>13.2f} | {formal_lg:>17.2f} | {lg_residual:>14.2f}")
        # Also report normalized residuals:
        L = math.log(N)
        print(f"           per-N residuals: (S_small - N*Sigma_*)/N = {sm_residual/N:.4f}, "
              f"(S_large - formal_tail)/N = {lg_residual/N:.4f}")
        print(f"           empirical residual fits 0.85L - 2.2 = {0.85*L - 2.2:.4f}")
        print()

if __name__ == "__main__":
    main()
