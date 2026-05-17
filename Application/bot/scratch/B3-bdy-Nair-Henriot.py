"""
Cross-validate c_1 = H(1) pi/2 via the Nair-Henriot leading-constant formula
(independent of the hyperbola argument).

For sum_{n <= N} f(F(n)) with F(n) = n^2 + 1 and f multiplicative:
The Selberg-Delange leading constant is

  c = (1/(kappa-1)!) * prod_p E_p,    E_p = (1-1/p)^kappa * sum_{k>=0} f(p^k) rho(p^k) / p^k

where kappa is the order of pole of D_f(s) := sum_d f(d) rho(d) d^{-s} at s=1.

For f = tau (Hooley): kappa = 2, c = 3/pi (well-known).

For f = tau* = 2^omega (squarefree-divisor count): kappa = 2.
Local factors:
  p = 2:   sum_k f(2^k) rho(2^k)/2^k = 1 + 2 * 1/2 + 0 + ... = 2
           E_2 = (1/2)^2 * 2 = 1/2
  p == 1 (mod 4): sum_k f(p^k) rho(p^k)/p^k = 1 + sum_{k>=1} 2 * 2/p^k = 1 + 4/(p-1)
           E_p = (1-1/p)^2 * (1 + 4/(p-1)) = (1-1/p) * (1+3/p) = 1 + 2/p - 3/p^2
  p == 3 (mod 4): sum = 1, E_p = (1-1/p)^2

So c_{tau*} = 1/((2-1)!) * (1/2) * prod_{p==1(4)} (1 + 2/p - 3/p^2) * prod_{p==3(4)} (1 - 1/p)^2
            = (1/2) * prod_{p==1(4)} (1 + 2/p - 3/p^2) * prod_{p==3(4)} (1 - 1/p)^2.

We expect c_{tau*} == H(1) pi/2 = 0.868135 from the other derivation.

Cross-check Hooley's c_tau too (sanity for the formula machinery).
"""
import math


def primes_up_to(M):
    if M < 2: return []
    sieve = bytearray(b"\x01") * (M + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [p for p in range(M+1) if sieve[p]]


def compute_c_tau_star(P_bound=10**6):
    primes = primes_up_to(P_bound)
    log_c = math.log(0.5)  # E_2 contribution
    for p in primes:
        if p == 2: continue
        if p % 4 == 1:
            # E_p = 1 + 2/p - 3/p^2
            log_c += math.log(1.0 + 2.0/p - 3.0/(p*p))
        else:
            # E_p = (1 - 1/p)^2
            log_c += 2 * math.log(1.0 - 1.0/p)
    return math.exp(log_c)


def compute_c_tau_hooley(P_bound=10**6):
    """Sanity: should give 3/pi = 0.9549."""
    primes = primes_up_to(P_bound)
    log_c = math.log(0.5)
    for p in primes:
        if p == 2: continue
        if p % 4 == 1:
            # E_p = 1 + 2/p - 1/p^2
            log_c += math.log(1.0 + 2.0/p - 1.0/(p*p))
        else:
            # E_p = (1 - 1/p)^2
            log_c += 2 * math.log(1.0 - 1.0/p)
    return math.exp(log_c)


def compute_H1(P_bound=10**6):
    """From the SD-zeta_K factorization."""
    primes = primes_up_to(P_bound)
    log_H = math.log(3/4)
    for p in primes:
        if p == 2: continue
        if p % 4 == 1:
            log_H += math.log(1.0 - 3.0/(p*p) + 2.0/(p*p*p))
        else:
            log_H += math.log(1.0 - 1.0/(p*p))
    return math.exp(log_H)


if __name__ == "__main__":
    P = 10**6
    c_NH = compute_c_tau_star(P)
    c_NH_Hooley = compute_c_tau_hooley(P)
    H1 = compute_H1(P)
    c_SD = H1 * math.pi / 2
    print(f"=== Nair-Henriot Halász formula (primes <= {P}) ===")
    print(f"c_tau (Hooley):   {c_NH_Hooley:.10f}  vs  3/pi = {3/math.pi:.10f}")
    print(f"   diff = {c_NH_Hooley - 3/math.pi:.2e}")
    print(f"c_tau*  (NH):     {c_NH:.10f}")
    print(f"c_tau* = H(1) pi/2 (SD via zeta_K H factorization):")
    print(f"   H(1) = {H1:.10f}, pi/2 = {math.pi/2:.10f}")
    print(f"   c_SD = H(1)*pi/2 = {c_SD:.10f}")
    print(f"   diff between two derivations = {c_NH - c_SD:.2e}")
    if abs(c_NH - c_SD) < 1e-6:
        print("*** AGREEMENT: independent derivations give c_1 = H(1)*pi/2 to 6 digits. ***")
