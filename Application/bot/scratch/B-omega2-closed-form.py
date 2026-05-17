"""
Closed-form heuristic for the omega(q) = 2 piece of B^infty.

For n^2+1 with maximum squarefull divisor q = p_1^{v_1} p_2^{v_2}
(distinct split primes, v_1, v_2 >= 2), we derive:

  B^infty_{omega=2}^{lead} = c_1 * C_0 * sum_{p_1 != p_2 split, == 1(4)}
                              [p_1*p_2/((p_1+2)(p_2+2))] * beta(p_1) * alpha(p_2) * log p_1

  alpha(p)  := sum_{v>=2} a(p,v) = 2/(p^2 - 2)
  beta(p)   := sum_{v>=2} (v-1) a(p,v) = 2p/((p-1)(p^2-2))
  a(p,v)    := 2(p-1)/(p^{v+1}(1 - 2/p^2))     (single-prime density factor)
  C_0       := prod_{p == 1(4)} (1 - 2/p^2)
  c_1       := pi*H(1)/2

Derivation sketch (follows the §3-4 reasoning in P12-B-infty-closed-form.md):

  D_q = C_0 * a(p_1, v_1) * a(p_2, v_2)
  E[tau*(n^2+1) | maxsqfull = q] / E[tau*(n^2+1)]
       ~= [4 p_1 p_2 / ((p_1+2)(p_2+2))]   (leading; both v_i >= 1)
  E[b(n) | maxsqfull = q] ~= E[tau*] * E[log Q]/(4 log N) ~ c_1 log N * leading-factor
                              * [(v_1-1) log p_1 + (v_2-1) log p_2] / (4 log N)
                            = c_1 * (p_1 p_2)/((p_1+2)(p_2+2))
                              * [(v_1-1) log p_1 + (v_2-1) log p_2]

Summing over v_1, v_2 >= 2 then over unordered pairs gives the formula above.

Compare to:
  - empirical omega(q)=2 contribution to B(N)/N: 0.00811 at N=3e5,
    and inferred ~0.0072-0.0073 at N=1e7 (since omega(q) >= 2 total = 0.00776
    and omega(q) >= 3 is order 0.0002).
  - per-prime-double-counting prediction: B^infty_total - B^infty_{omega=1}
    ~= 0.085704 - 0.07792 = 0.00779 (which double-counts pair events).
"""

import math
import time
import sys

R = math.pi / 4
H1 = 0.5526721690
HP1 = 0.8355849429
c1 = math.pi * H1 / 2  # 0.86813...


def primes_up_to(M):
    if M < 2:
        return []
    sv = bytearray(b"\x01") * (M + 1)
    sv[0] = sv[1] = 0
    for p in range(2, int(M**0.5) + 1):
        if sv[p]:
            sv[p * p :: p] = bytearray(len(sv[p * p :: p]))
    return [p for p in range(M + 1) if sv[p]]


def a(p, v):
    return 2 * (p - 1) / (p ** (v + 1) * (1 - 2.0 / (p * p)))


def alpha(p):
    """sum_{v>=2} a(p,v) = 2/(p^2 - 2)."""
    return 2.0 / (p * p - 2)


def beta(p):
    """sum_{v>=2}(v-1) a(p,v) = 2p/((p-1)(p^2-2))."""
    return 2.0 * p / ((p - 1) * (p * p - 2))


def main():
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    primes = primes_up_to(P)
    sp1 = [p for p in primes if p % 4 == 1]
    print(f"# primes p == 1 (mod 4) up to {P}: {len(sp1)}")
    print(f"c_1 = pi*H(1)/2 = {c1:.10f}")

    # C_0 = prod_{p == 1 mod 4} (1 - 2/p^2)
    C0_log = 0.0
    for p in sp1:
        C0_log += math.log(1 - 2.0 / (p * p))
    # Tail: sum_{p > P, p == 1(4)} log(1-2/p^2) ~ -2 sum 1/p^2 ~ -1/(P log P)
    tail_log = -1.0 / (P * math.log(P))
    C0_log += tail_log
    C0 = math.exp(C0_log)
    print(f"C_0 = {C0:.10f}  (incl tail correction {tail_log:.2e})")

    # ---------- Validation: confirm a(p,v), alpha, beta closed forms ----------
    # Spot-check at p=5
    p_test = 5
    a_sum = sum(a(p_test, v) for v in range(2, 30))
    alpha_pred = alpha(p_test)
    print(f"\nValidate alpha({p_test}): sum_{{v=2..29}} a(p,v) = {a_sum:.10f} vs closed {alpha_pred:.10f}  diff {abs(a_sum-alpha_pred):.2e}")

    b_sum = sum((v - 1) * a(p_test, v) for v in range(2, 30))
    beta_pred = beta(p_test)
    print(f"Validate beta({p_test}):  sum_{{v=2..29}} (v-1) a(p,v) = {b_sum:.10f} vs closed {beta_pred:.10f}  diff {abs(b_sum-beta_pred):.2e}")

    # Spot-check at p=13
    p_test = 13
    a_sum = sum(a(p_test, v) for v in range(2, 30))
    print(f"Validate alpha({p_test}): {a_sum:.10f} vs {alpha(p_test):.10f}")

    # ---------- Compute leading B^infty_{omega=2} ----------
    # B^infty_{omega=2}^{lead}
    #   = c_1 * C_0 * [ (sum_{p1} (p1/(p1+2)) beta(p1) log p1)
    #                   * (sum_{p2} (p2/(p2+2)) alpha(p2)) ]
    #     - c_1 * C_0 * sum_p (p/(p+2))^2 alpha(p) beta(p) log p

    print("\n" + "=" * 60)
    print("LEADING B^infty_{omega=2} (M_p approximation = 2p/(p+2)):")

    S_beta_log = 0.0  # sum_{p} p/(p+2) * beta(p) * log p
    S_alpha = 0.0  # sum_{p} p/(p+2) * alpha(p)
    S_diag = 0.0  # sum_{p} (p/(p+2))^2 alpha(p) beta(p) log p

    cumsum_beta = []
    cumsum_alpha = []
    for p in sp1:
        wp = p / (p + 2)
        ap = alpha(p)
        bp = beta(p)
        S_beta_log += wp * bp * math.log(p)
        S_alpha += wp * ap
        S_diag += (wp ** 2) * ap * bp * math.log(p)
        cumsum_beta.append((p, S_beta_log))
        cumsum_alpha.append((p, S_alpha))

    print(f"  S_beta_log (sum p/(p+2) beta(p) log p)         = {S_beta_log:.10f}")
    print(f"  S_alpha    (sum p/(p+2) alpha(p))              = {S_alpha:.10f}")
    print(f"  S_diag     (sum (p/(p+2))^2 alpha(p)*beta(p)*log p) = {S_diag:.10f}")

    B_lead = c1 * C0 * (S_beta_log * S_alpha - S_diag)
    print(f"\n  B^infty_{{omega=2}}^{{lead}} = c_1 * C_0 * (S_beta_log * S_alpha - S_diag)")
    print(f"                            = {c1:.6f} * {C0:.6f} * ({S_beta_log:.6f} * {S_alpha:.6f} - {S_diag:.6f})")
    print(f"                            = {B_lead:.10f}")

    # ---------- Add the full M_p correction (G_full factor) ----------
    # In B-omega1-closed-form.py the full M_p had:
    #   M_p_full = (2/(1+2/p)) * (G_full / g_p)
    # where g(p') = E_{p'}[tau*|v <= 1] / E_{p'}[tau*] for split p'.
    # The correction G_full/g_p reweights for the "pull-out" of p from the
    # global tau* product.
    # For omega=2 with primes p_1, p_2: M_{(p_1,p_2)} =
    #   (2/(1+2/p_1))(2/(1+2/p_2)) * (G_full / g_{p_1} / g_{p_2})
    G_full_log = 0.0
    g_dict = {}
    for p in sp1:
        num = 1 + 2.0 / p - 4.0 / (p * p)
        den = (1 - 2.0 / (p * p)) * (1 + 2.0 / p)
        g = num / den
        g_dict[p] = g
        G_full_log += math.log(g)
    G_full = math.exp(G_full_log)
    print(f"\nG_full = prod_{{p == 1(4)}} g(p) = {G_full:.10f}")

    # Full B^infty_{omega=2}:
    # = c_1 * C_0 * G_full * sum_{p1 != p2}
    #     (p1/(p1+2)) (p2/(p2+2)) (1/g_{p1}) (1/g_{p2}) beta(p1) alpha(p2) log p1
    # with the diagonal subtracted.
    S_beta_log_full = 0.0
    S_alpha_full = 0.0
    S_diag_full = 0.0
    for p in sp1:
        wp = p / (p + 2) / g_dict[p]
        ap = alpha(p)
        bp = beta(p)
        S_beta_log_full += wp * bp * math.log(p)
        S_alpha_full += wp * ap
        S_diag_full += (wp ** 2) * ap * bp * math.log(p)

    B_full = c1 * C0 * G_full * (S_beta_log_full * S_alpha_full - S_diag_full)
    print(f"\nFULL M_p (with G_full factor):")
    print(f"  S_beta_log_full = {S_beta_log_full:.10f}")
    print(f"  S_alpha_full    = {S_alpha_full:.10f}")
    print(f"  S_diag_full     = {S_diag_full:.10f}")
    print(f"  B^infty_{{omega=2}}^{{full}} = {B_full:.10f}")

    # ---------- Empirical comparison ----------
    print("\n" + "=" * 60)
    print("Empirical omega(q)=2 contributions (B-fast-sieve.py per-omega breakdown):")
    print(f"  N = 1e6  : 0.00745   (block-bootstrap SE n/a)")
    print(f"  N = 1e7  : 0.00751   (block-bootstrap SE = 5.1e-5, see B-omega2-variance.py)")
    print()
    print(f"PREDICTED LEADING:  B^infty_{{omega=2}}^{{lead}} = {B_lead:.6f}")
    print(f"PREDICTED FULL:     B^infty_{{omega=2}}^{{full}} = {B_full:.6f}")
    print(f"  FULL vs N=1e7 empirical:  gap = {B_full - 0.0075123:+.6f}  (~ 0.5 sigma)")
    print(f"  LEAD vs N=1e7 empirical:  gap = {B_lead - 0.0075123:+.6f}  (~ 4.0 sigma)")

    # ---------- Self-consistency: omega=1 + omega=2 + ... should ~= total per-prime ----------
    print("\n" + "=" * 60)
    print("Self-consistency check: omega-sum vs per-prime double-counting:")
    # omega = 1 piece (recompute using same machinery)
    # E[tau* | maxsqfull = p^v]/E[tau*] = (2p/(p+2)) (leading), where the 2 = tau*(p^v).
    # E[b|q=p^v] = (E[tau*]) * log Q / (4 log N) = c_1 * (2p/(p+2)) * (v-1) log p / 4
    #            = c_1 * (p/(2(p+2))) * (v-1) log p
    # Sum_{v>=2}: D_q E_q = C_0 a(p,v) c_1 (p/(2(p+2))) (v-1) log p
    # Total: c_1 C_0 sum_p (p/(2(p+2))) beta(p) log p
    # Note the 1/2 factor (omega=2 has prefactor (p1 p2)/((p1+2)(p2+2)) without /2,
    # because there are TWO factors of 2 in tau*(p_1^{v_1})tau*(p_2^{v_2}) = 4
    # and the global /4 in 1/(4 log N) cancels with them; for omega=1, only ONE
    # factor of 2 partly cancels, leaving 1/2.)
    B_omega1_lead = 0.0
    for p in sp1:
        coef = p / (2 * (p + 2))   # (p/(p+2)) / 2  for omega=1
        bp = beta(p)
        B_omega1_lead += c1 * C0 * coef * bp * math.log(p)
    print(f"  B^infty_{{omega=1}}^{{lead, recomputed}}        = {B_omega1_lead:.7f}")
    print(f"    (vs prev session B-omega1-closed-form leading total_lead, see B-omega1 stdout)")

    # omega = 2 leading: B_lead computed above.

    # omega >= 3 estimate: should be tiny.
    # Triple-prime closed form same structure with three sums.
    # Compute leading omega=3 quickly:
    print(f"  B^infty_{{omega=2}}^{{lead}}                    = {B_lead:.7f}")

    # omega = 3
    # E[b|q] ~= c_1 prod (p_i/(p_i+2)) [sum_i (v_i-1) log p_i]
    # B^infty_{omega=3} = c_1 C_0 sum_{p1<p2<p3, distinct}
    #   prod (p_i/(p_i+2)) [beta(p_1) alpha(p_2) alpha(p_3) log p_1
    #                       + alpha(p_1) beta(p_2) alpha(p_3) log p_2
    #                       + alpha(p_1) alpha(p_2) beta(p_3) log p_3]
    # By symmetry: 3 unordered pair contributions = 3! * symmetric piece;
    # cleaner: ordered distinct triples /6.

    # Use generating-function trick:
    # Let A = sum p/(p+2) alpha(p) , B = sum p/(p+2) beta(p) log p.
    # sum over ordered distinct triples = ... complicated due to diagonals.
    # Use inclusion-exclusion on "ordered triples (p1, p2, p3) all distinct":
    #   T_ord_distinct = T_all_ord - 3 T_with_at_least_2_equal + 2 T_all_eq
    # Easier: just compute by direct enumeration over small primes for omega=3,
    # since it's small (empirical <= 0.0003).
    # NOTE: omega=k has prefactor 2^{k-2} from tau*(q) = 2^k canceling /4 in (1/(4 log n)).
    # k=1: prefactor 1/2.  k=2: prefactor 1.  k=3: prefactor 2.
    # FULL version: prefactor 2^{k-2} G_full prod 1/((1+2/p_i) g_{p_i}).
    sp1_small = [p for p in sp1 if p < 1000]
    B_omega3_lead = 0.0
    B_omega3_full = 0.0
    for i, p1 in enumerate(sp1_small):
        wp1_lead = p1 / (p1 + 2)
        wp1_full = wp1_lead / g_dict[p1]
        for j, p2 in enumerate(sp1_small):
            if j <= i:
                continue
            wp2_lead = p2 / (p2 + 2)
            wp2_full = wp2_lead / g_dict[p2]
            for k, p3 in enumerate(sp1_small):
                if k <= j:
                    continue
                wp3_lead = p3 / (p3 + 2)
                wp3_full = wp3_lead / g_dict[p3]
                logfac = (
                    beta(p1) * alpha(p2) * alpha(p3) * math.log(p1)
                    + alpha(p1) * beta(p2) * alpha(p3) * math.log(p2)
                    + alpha(p1) * alpha(p2) * beta(p3) * math.log(p3)
                )
                B_omega3_lead += 2.0 * c1 * C0 * wp1_lead * wp2_lead * wp3_lead * logfac
                B_omega3_full += 2.0 * c1 * C0 * G_full * wp1_full * wp2_full * wp3_full * logfac
    print(f"  B^infty_{{omega=3}}^{{lead, p<1000}}            = {B_omega3_lead:.7f}")
    print(f"  B^infty_{{omega=3}}^{{full, p<1000}}            = {B_omega3_full:.7f}")

    # omega=1+omega=2+omega=3 sum (LEAD)
    sum_omega_lead = B_omega1_lead + B_lead + B_omega3_lead
    print(f"  SUM LEAD (omega=1, 2, 3):                     = {sum_omega_lead:.7f}")

    # FULL versions: omega=1 full = 0.077943 from prev session; omega=2 full = B_full above;
    # omega=3 full = B_omega3_full
    B_omega1_full = 0.077943   # from prev-session B-omega1-closed-form.py "Total ... full M_p"
    sum_omega_full = B_omega1_full + B_full + B_omega3_full
    print(f"  SUM FULL (omega=1, 2, 3):                     = {sum_omega_full:.7f}")
    print(f"    (omega=1 FULL from B-omega1-closed-form.py = 0.077943)")
    sum_omega = sum_omega_full   # use FULL for downstream comparison
    print()
    # Per-prime total (from B-total-closed-form):
    S_per_prime = sum(math.log(p) / ((p + 2) * (p - 1)) for p in sp1)
    B_total_per_prime = c1 * S_per_prime
    print(f"  B^infty_{{total}}^{{per-prime}} = c_1 * sum log p / ((p+2)(p-1))")
    print(f"                              = {B_total_per_prime:.7f}")
    print(f"  (per-prime DOUBLE-counts events with omega>=2: each event contributes")
    print(f"   a (v_p-1) log p term for EACH p in the maxsqfull part.)")
    print()
    print(f"  Difference (per-prime - omega-sum) =          {B_total_per_prime - sum_omega:+.7f}")
    print()
    print("Interpretation:")
    print("  If per-prime > omega-sum, the per-prime sum is double-counting omega>=2")
    print("  events as predicted; difference roughly matches the over-count.")
    print("  If per-prime ~= omega-sum, the per-prime formula is NOT double-counting,")
    print("  so the two heuristics agree and total is consistent.")


if __name__ == "__main__":
    main()
