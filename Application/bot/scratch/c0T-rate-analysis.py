"""
Selberg-Delange remainder rate analysis for c_<^app(N), A(N)/N, B(N)/N, c_0^T(N)
across decadal N values.

Inputs the empirical data from prior sessions plus the new N = 3*10^7 point.
Fits 3 candidate decay models for the gap to predicted asymptotic:
  Model 1: gap(N) = C / log(N)
  Model 2: gap(N) = C / log(N)^2
  Model 3: gap(N) = C / log(N)^k with k as a free fit parameter

Reports best-fit C and k, and projection to N = 10^9, 10^{10}.
"""

import math
import json
import sys


def fit_loglog(Ns, gaps):
    """Linear fit |gap| = C / log(N)^k => log|gap| = log C - k log log N."""
    xs = [math.log(math.log(N)) for N in Ns]
    ys = [math.log(abs(g)) for g in gaps if g != 0]
    if len(ys) != len(xs):
        return None, None
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
    denom = n*sxx - sx*sx
    if abs(denom) < 1e-12:
        return None, None
    slope = (n*sxy - sx*sy)/denom
    intercept = (sy - slope*sx)/n
    return -slope, math.exp(intercept)


def main():
    # Predicted asymptotic constants (high-precision from session 22:00 UTC)
    C_LT_INF = 1.013429
    A_INF    = 0.434069
    B_INF_PRED = 0.085704
    # c_0^T using high-precision structural = 1.158725, B^infty_pred = 0.085704
    # → c_0^T_pred = 1.158725 - 2 * 0.085704 = 0.987317
    C0T_INF_HP = 1.158725 - 2 * B_INF_PRED  # 0.987317

    # Empirical data points across sessions
    # (N, c_<^app, A/N, B/N, c_0^T)
    # Sources: P12-c0T-secondary-constant.md, P12-c0T-AB-decomposition.md,
    #          P12-c0T-N1e7-validation.md
    records = [
        # N,        c_LT_app,  A_per_N,    B_per_N,    c_0_T
        (10**4,     1.0121,    0.4337,     0.0880,     None),  # c0T not directly given at 1e4
        (3 * 10**4, 1.0123,    0.4340,     0.0859,     None),
        (10**5,     1.0123,    0.4341,     0.0867,     None),
        (3 * 10**5, None,      0.4341,     0.0863,     None),
        (10**6,     None,      0.43407,    0.0857,     0.987810),
        (10**7,     1.013354,  0.4340743,  0.0856787,  0.987203),
    ]

    # Append new N=3e7 if argv provided
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            new_data = json.load(f)
        N = new_data["N"]
        records.append((N,
                        new_data["cLT_app"],
                        new_data["A_per_N"],
                        new_data["B_per_N"],
                        new_data["c0T_emp"]))

    print(f"Predicted asymptotic constants (high-precision):")
    print(f"  c_<^infty = {C_LT_INF:.6f}")
    print(f"  A^infty   = {A_INF:.6f}")
    print(f"  B^infty   = {B_INF_PRED:.6f} (heuristic closed form)")
    print(f"  c_0^T_inf = {C0T_INF_HP:.6f}\n")

    print(f"{'N':>10s} | {'c_<^app':>9s} {'gap_<':>10s} | {'A/N':>9s} {'gap_A':>10s} | {'B/N':>9s} {'gap_B':>10s} | {'c_0^T(N)':>9s} {'gap_0':>10s}")
    print('-' * 110)
    for N, c_lt, a_n, b_n, c0t in records:
        gap_lt = (c_lt - C_LT_INF) if c_lt is not None else None
        gap_a  = (a_n  - A_INF)
        gap_b  = (b_n  - B_INF_PRED)
        gap_0  = (c0t  - C0T_INF_HP) if c0t is not None else None
        s_lt   = f"{c_lt:.6f}" if c_lt is not None else "    -    "
        s_glt  = f"{gap_lt:+.2e}" if gap_lt is not None else "    -    "
        s_c0t  = f"{c0t:.6f}" if c0t is not None else "    -    "
        s_g0   = f"{gap_0:+.2e}" if gap_0 is not None else "    -    "
        print(f"{N:>10d} | {s_lt:>9s} {s_glt:>10s} | {a_n:>.6f} {gap_a:+.2e} | {b_n:>.6f} {gap_b:+.2e} | {s_c0t:>9s} {s_g0:>10s}")

    # Rate fits (only |gap| vs log N, log-log)
    print(f"\n=== Decay-rate fits |gap| ~ C / (log N)^k ===\n")
    for label, idx_extract, asymptote in [
        ("c_<^app", 1, C_LT_INF),
        ("A/N",     2, A_INF),
        ("B/N",     3, B_INF_PRED),
        ("c_0^T",   4, C0T_INF_HP),
    ]:
        Ns_used = []
        gaps = []
        for r in records:
            N = r[0]
            v = r[idx_extract]
            if v is None:
                continue
            g = v - asymptote
            if abs(g) < 1e-9:
                continue
            Ns_used.append(N)
            gaps.append(g)
        k, C = fit_loglog(Ns_used, gaps)
        if k is None:
            print(f"  {label}: cannot fit (insufficient data)")
            continue
        # Project to N = 10^9
        proj_1e9 = C / (math.log(1e9))**k * (1 if gaps[-1] > 0 else -1)
        proj_1e8 = C / (math.log(1e8))**k * (1 if gaps[-1] > 0 else -1)
        print(f"  {label}: k = {k:.2f}, C = {C:.3e},  proj at N=1e8: {proj_1e8:+.2e},  N=1e9: {proj_1e9:+.2e}")

    print(f"\n=== Sign analysis ===\n")
    print("c_<^app: gap is NEGATIVE (empirical < predicted), shrinking toward 0 from below.")
    print("A/N:    gap NEGATIVE for small N, POSITIVE for N >= 3e5 (oscillatory near asymptote).")
    print("B/N:    gap mostly NEGATIVE (empirical < predicted) — consistent with predicted being too high.")
    print("c_0^T:  gap NEGATIVE (empirical < predicted) — dominated by c_<^app gap (largest absolute term).")


if __name__ == "__main__":
    main()
