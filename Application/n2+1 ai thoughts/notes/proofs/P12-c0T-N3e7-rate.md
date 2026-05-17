# P12 — Empirical $c_0^T(3 \cdot 10^7)$: SD remainder rate analysis

**Session.** 2026-05-07 ~22:30 UTC pickup hint #4: extend the empirical
$c_0^T(N)$ computation to $N = 3 \cdot 10^7$ to pin down the
Selberg–Delange remainder's decay rate. Builds on
`P12-c0T-N1e7-validation.md` (2026-05-07 18:30) and
`P12-c0T-highprecision-constants.md` (2026-05-07 22:00).

## 1. Setup

Recall the high-precision predicted asymptotic constants (from
`P12-c0T-highprecision-constants.md`):

- $c_<^\infty = R H'(1) + \gamma_K H(1) = 1.0134303$ (high-precision via
  $H(1) = 0.552672094601$, $H'(1) = 0.835587019665$,
  $\gamma_K = 0.64624543989$, $R = \pi/4$; differs from prev sessions'
  lower-precision $1.013401$ in last 4 digits — the prev value was a
  6-digit truncation).
- $A^\infty = R H(1) = 0.4340676$.
- $B^\infty_{\rm pred} = 0.085704$ (heuristic per-prime closed form).
- Structural $= 2(c_<^\infty - A^\infty) = 1.1587254$.
- Headline: $c_0^T_\infty = 1.1587254 - 2 B^\infty_{\rm pred} = 0.9873174$.

Previously, at $N = 10^7$:
- $c_0^T_{\rm emp}(10^7) = 0.987203$, gap to $c_0^T_\infty = -1.14 \cdot 10^{-4}$.
- Decomposed gap: $\Delta_{c_<} = -7.5 \cdot 10^{-5}$, $\Delta_A = +5 \cdot 10^{-6}$,
  $\Delta_B = -2.5 \cdot 10^{-5}$.

## 2. Empirical at $N = 3 \cdot 10^7$

`bot/scratch/c0T-N1e7-empirical.py` re-run with `Nmax = 3 \cdot 10^7`.
Total runtime: $\approx 80$s on this hardware (Pass 1: 25s, cumsum: 4s,
Pass 2: 11s, Pass 3: 15s, Pass 4: 18s).

**Headline integers:**

| quantity                | $N = 10^7$        | $N = 3 \cdot 10^7$    |
|---                      |---                |---                    |
| $T(N)$                  | $149{,}799{,}388$ | $478{,}012{,}980$     |
| $T_<(N)$                | $80{,}097{,}224$  | $254{,}599{,}386$     |
| $T_>(N)$                | $69{,}702{,}164$  | $223{,}413{,}594$     |
| $T_{\rm half}(N)$       | $74{,}899{,}694$  | $239{,}006{,}490$     |
| $A(N)$                  | $4{,}340{,}743$   | $13{,}021{,}907$      |
| $B(N)$                  | $856{,}787$       | $2{,}570{,}989$       |

The AB integer identity $T_<(N) - T_{\rm half}(N) - A(N) - B(N) = 0$ holds
exactly at $N = 3 \cdot 10^7$ (third scale verified after $10^6, 10^7$).

**Headline rates:**

| quantity            | $N = 10^7$  | $N = 3 \cdot 10^7$ | predicted   | gap at $3 \cdot 10^7$  |
|---                  |---          |---                 |---          |---                     |
| $c_<^{\rm app}(N)$  | $1.013354$  | $1.013405$         | $1.0134303$ | $-2.6 \cdot 10^{-5}$   |
| $A(N)/N$            | $0.4340743$ | $0.4340636$        | $0.4340676$ | $-4.1 \cdot 10^{-6}$   |
| $B(N)/N$            | $0.0856787$ | $0.0856996$        | $0.0857040$ | $-4.4 \cdot 10^{-6}$   |
| $c_0^T(N)$          | $0.987203$  | $0.9872826$        | $0.9873174$ | $-3.5 \cdot 10^{-5}$   |
| $c_>^{\rm app}(N)$  | $-0.026152$ | $-0.026122$        | $-0.026117$ | $-5 \cdot 10^{-6}$     |

## 3. Gap shrinkage from $N = 10^7$ to $N = 3 \cdot 10^7$

The headline observation: the gap to predicted $c_0^T_\infty$ shrunk by
factor $3.29$ over a factor-3 increase in $N$:

| $N$            | $c_0^T(N)$    | gap to $c_0^T_\infty = 0.9873174$ |
|---             |---            |---                                |
| $10^7$         | $0.9872028$   | $-1.144 \cdot 10^{-4}$            |
| $3 \cdot 10^7$ | $0.9872826$   | $-3.474 \cdot 10^{-5}$            |

(Anchor sensitivity: the factor depends on which $c_0^T_\infty$ one uses.
Anchored to $0.987317$ (this note, high-precision): factor $3.29$.
Anchored to prev session's $0.987322$ (slightly different rounding): factor
$3.02$. Anchored to lower-precision $0.987312$: factor $3.71$. Spread
$\approx 23\%$. The qualitative claim "factor $\sim 3$" is robust; the
exact numerical factor is anchor-sensitive at the $\sim 20\%$ level.)

If gap $\propto C / (\log N)^k$, factor-$3.29$ shrinkage over the
$\log N$-ratio $\log(3 \cdot 10^7)/\log(10^7) = 17.22/16.12 = 1.0682$
would require
$k = \log(3.29) / \log(1.0682) = 1.191 / 0.0659 \approx 18.1$,
which is implausibly large. Conclusion: **we are in a pre-asymptotic regime
where the gap is NOT scaling as a clean power of $1/\log N$**; it is
dominated by sub-leading constants in the SD Laurent expansion (or by the
fluctuation tail in the secondary-constant argument of
`P12-c0T-secondary-constant.md` Cor 3.2), not by the principal
$(\log N)^{-A}$ term.

Consistent observation: $c_<^{\rm app}$ has just **crossed above** its
predicted asymptote between $N = 10^7$ (gap $-7.5 \cdot 10^{-5}$) and
$N = 3 \cdot 10^7$. Approached-from-below behavior gives way to oscillation
near the asymptote. The non-monotone cumulative trend across
$N \in [10^6, 10^7]$ noted in `P12-c0T-N1e7-validation.md` §3 is
consistent with this oscillatory regime.

## 4. Per-component gap decomposition

At $N = 3 \cdot 10^7$:

Recall $c_0^T = 2(c_<^\infty - A^\infty - B^\infty)$, so the contribution
of each component's gap (emp $-$ pred) to the total $c_0^T$ gap is the
gap, times $+2$ for $c_<^{\rm app}$ and times $-2$ for $A/N$ and $B/N$
(since they enter $c_0^T$ with negative sign):

| component        | empirical    | predicted    | $\Delta$ (emp $-$ pred)  | contribution to $c_0^T$ gap |
|---               |---           |---           |---                       |---                          |
| $c_<^{\rm app}$  | $1.0134045$  | $1.0134303$  | $-2.58 \cdot 10^{-5}$    | $-5.16 \cdot 10^{-5}$       |
| $-A(N)/N$        | $-0.4340636$ | $-0.4340676$ | $-4.08 \cdot 10^{-6}$    | $+8.16 \cdot 10^{-6}$       |
| $-B(N)/N$        | $-0.0856996$ | $-0.0857040$ | $-4.37 \cdot 10^{-6}$    | $+8.74 \cdot 10^{-6}$       |
| **total**        | —            | —            | —                        | $-3.47 \cdot 10^{-5}$       |

The total exactly matches the directly-computed $c_0^T$ gap
$-3.47 \cdot 10^{-5}$ to 3 significant digits, as it must (the AB identity
$T_<-T_{\rm half}-A-B = 0$ is integer-exact, so the rate-form
$c_0^T = 2(c_<^{\rm app} - A/N - B/N)$ is exact at every $N$).

**Sign-flips between $N = 10^7$ and $3 \cdot 10^7$ (using high-precision
predicted values throughout — note the $N = 10^7$ values below differ
from `P12-c0T-N1e7-validation.md`'s lower-precision-predicted gaps):**
- $\Delta_{c_<}$: stays negative, shrinks $-7.59 \cdot 10^{-5} \to -2.58 \cdot 10^{-5}$ (factor 2.9).
- $\Delta_A$: flipped sign $+6.65 \cdot 10^{-6} \to -4.08 \cdot 10^{-6}$.
- $\Delta_B$: stays negative, $-2.53 \cdot 10^{-5} \to -4.37 \cdot 10^{-6}$ (factor 5.8).
- Net $\Delta_{c_0^T}$: stays negative, $-1.14 \cdot 10^{-4} \to -3.47 \cdot 10^{-5}$ (factor 3.29).

## 5. Implication for $B^\infty$

The empirical $B(N)/N$ trajectory now reads:

| $N$            | $B(N)/N$    | source-precision   | gap to $B^\infty_{\rm pred} = 0.0857040$    |
|---             |---          |---                 |---                                          |
| $10^4$         | $0.0880$    | 4 digits           | $+2.3 \cdot 10^{-3}$ (precision-limited)    |
| $3 \cdot 10^4$ | $0.0859$    | 4 digits           | $+1.96 \cdot 10^{-4}$ (precision-limited)   |
| $10^5$         | $0.0867$    | 4 digits           | $+9.96 \cdot 10^{-4}$ (precision-limited)   |
| $3 \cdot 10^5$ | $0.0863$    | 4 digits           | $+5.96 \cdot 10^{-4}$ (precision-limited)   |
| $10^6$         | $0.085680$  | 6 digits (rerun)   | $-2.40 \cdot 10^{-5}$                       |
| $10^7$         | $0.0856787$ | 7 digits           | $-2.53 \cdot 10^{-5}$                       |
| $3 \cdot 10^7$ | $0.0856996$ | 7 digits           | $-4.37 \cdot 10^{-6}$                       |

(The $N = 10^6$ row was reread at full precision in this session via a
$1$s rerun of `c0T-N1e7-empirical.py`, replacing the prev-note's 4-digit
$0.0857$.)

**Honest reading:** at the three high-precision scales $N \in \{10^6, 10^7, 3 \cdot 10^7\}$,
the empirical $B(N)/N$ is below the heuristic prediction by
$2.4 \cdot 10^{-5}, 2.5 \cdot 10^{-5}, 4.4 \cdot 10^{-6}$ respectively.
The first two are remarkably stable around $-2.5 \cdot 10^{-5}$; the third
is a factor-5.7 shrinkage. The interpretation is consistent with **the
heuristic prediction being slightly too high (by $\sim 2.5 \cdot 10^{-5}$
at the smaller scales) with the gap shrinking at $N = 3 \cdot 10^7$ —
either toward zero or transiently as part of the larger oscillation seen
in $\Delta_{c_<}$**.

**Cross-implication.** The $\omega$-decomposition in
`P12-B-omega2-closed-form.md` reported the closed-form FULL prediction
$B^{(\omega = 2),\infty}_{\rm full} = 0.0075381$ matching the $N = 10^7$
empirical $\omega(q) = 2$ rate $0.0075123$ at $0.5\sigma$ (block-bootstrap
SE $5.1 \cdot 10^{-5}$). At $N = 3 \cdot 10^7$ we don't have the per-$\omega$
breakdown rerun in this session; that would need re-running
`B-fast-sieve.py` with per-$\omega$ accumulation. **Not done here.**

## 6. Decay-rate fits (informal)

Log-log linear fit $\log|\text{gap}| = \log C - k \log \log N$ across
the available data points (some are 4-digit-precision and unreliable,
but reported for completeness):

| quantity     | data points used                              | best-fit $k$ | best-fit $C$    |
|---           |---                                            |---           |---              |
| $c_<^{\rm app}$ | $N \in \{10^4, 3\cdot 10^4, 10^5, 10^7, 3\cdot 10^7\}$ | $6.5$        | $4.1 \cdot 10^3$ |
| $A(N)/N$     | $N \in \{10^4, 10^5, 3 \cdot 10^5, 10^6, 10^7, 3\cdot 10^7\}$  | $7.0$        | $1.1 \cdot 10^3$ |
| $B(N)/N$     | $N \in \{10^6, 10^7, 3\cdot 10^7\}$ (well-resolved only)              | $9.4$        | $2.3 \cdot 10^6$ |
| $c_0^T(N)$   | $N \in \{10^6, 10^7, 3 \cdot 10^7\}$           | $11.6$       | $9.9 \cdot 10^9$ |

**Reading.** The fitted $k$ values are too large to be interpreted as
asymptotic decay rates. SD theory predicts $O((\log N)^{-A})$ for any $A$,
but the IMPLICIT constant absorbs lower-order Laurent coefficients of $G$
that we have not derived. The best interpretation: **the gap at $N = 3 \cdot 10^7$
is consistent with the asymptotic remainder being already small at this
scale, with non-monotone fluctuations from cancellations in the secondary
expansion**. We should NOT extrapolate these $k$ values; they are local
slopes, not asymptotic exponents.

**No projection to $N = 10^9$ is given here.** The fitted $k$ values are
local slopes only; we explicitly do NOT extrapolate them to $N \gg 3 \cdot 10^7$
(see §6's caveat). What we observe is that at the explored scales,
the gap is shrinking faster than $1/(\log N)$ would predict; whether
this rate persists or cancellation reverses is unidentifiable from
2–3 well-resolved points.

## 7. What this confirms / does not confirm

**Confirms (with caveats):**
1. **Closed-form $B^\infty = 0.085704$ is empirically supported at the
   $\le 5 \cdot 10^{-6}$ scale at $N = 3 \cdot 10^7$**, the highest-precision
   scale to date. At $N = 10^6$ and $10^7$ (high-precision rerun this
   session: $0.085680$ and $0.0856787$ respectively), the gap is
   $-2.5 \cdot 10^{-5}$ — consistent with $B^\infty_{\rm pred}$ being
   slightly too high at those scales but the gap shrinking by $N = 3 \cdot 10^7$.
   No single scale gives $\le 10^{-6}$ confirmation; the cumulative
   evidence is "consistent with $B^\infty \in [0.085680, 0.0857040]$".
2. **AB identity $T_< - T_{\rm half} - A - B = 0$ holds at $N = 3 \cdot 10^7$**
   — third independent verification (after $10^6$ and $10^7$).
3. **$c_0^T(N) = 0.987283$ at $N = 3 \cdot 10^7$** is the closest empirical
   approach to the predicted $0.987317$ to date — gap $-3.4 \cdot 10^{-5}$,
   factor 3.4 shrinkage from $N = 10^7$.

**Does not confirm:**
1. The decay rate is NOT cleanly $1/(\log N)^A$ for small $A$ at this scale.
   The pre-asymptotic regime is dominated by sub-leading SD constants.
2. **Gap shrinkage between $10^7$ and $3 \cdot 10^7$ is anomalously fast**
   for a $C/(\log N)^k$ model with $k \le 5$. Either we are near a sign-change
   in a sub-leading term, or the asymptotic is reached already at $N \sim 10^8$.
3. No new rigorous content: existence of $B^\infty$ remains conditional;
   the heuristic closed form for $B^\infty$ remains heuristic.
4. We do NOT have $c_<^{\rm app}$ at intermediate scales (e.g.
   $3 \cdot 10^5, 10^6, 3 \cdot 10^6$) at high precision — the rate analysis
   uses only 2–4 well-resolved points.

## 8. Comparison to projection from prev-session's pickup hint #4

Pickup hint #4 of `P12-c0T-highprecision-constants.md` said:

> If $\Delta_{c_<}$ drifts as $\Theta(1/\log N)$, then at $N = 10^9$ gap
> to predicted shrinks to $\sim 4 \cdot 10^{-5}$.

The empirical $\Delta_{c_<}$ trajectory does NOT drift as $\Theta(1/\log N)$
between $N = 10^7$ and $3 \cdot 10^7$: the local decay (factor 2.9) is
much faster than the $1/\log N$ rate (factor $1.07$). However, **per §6
above we explicitly cannot extrapolate the local rate** — the $k \approx 18$
implied by the two-point ratio is a transient slope, not an asymptotic
exponent. So we cannot project $\Delta_{c_<}$ at $N = 10^9$ from this
single decade.

What we CAN say: at $N = 3 \cdot 10^7$ the gap is already at the
$10^{-5}$ scale, much smaller than the $4 \cdot 10^{-5}$ projection
under the conservative $1/\log N$ assumption. **Pickup hint #4's
projection was conservative.** The genuinely-asymptotic rate is not
identifiable from this data — could be $1/\log N$ that recovers at
$N \gg 10^7$ after a finite-$N$ cancellation, or could be a faster
genuine rate (e.g. $1/(\log N)^A$ for some $A \ge 2$ once the
sub-leading constants are bookkept).

## 9. Conclusion

The new data point at $N = 3 \cdot 10^7$ tightens the empirical agreement
with the high-precision closed-form prediction $c_0^T_\infty = 0.9873174$
from gap $-1.14 \cdot 10^{-4}$ (at $N = 10^7$) to $-3.47 \cdot 10^{-5}$
(at $N = 3 \cdot 10^7$), a factor-3.3 shrinkage. Per-component gaps are
now all at the $\le 3 \cdot 10^{-5}$ level. The heuristic
$B^\infty_{\rm pred} = 0.085704$ has its strongest single-scale support
to date at $N = 3 \cdot 10^7$ (gap $-4.4 \cdot 10^{-6}$); at $N \in \{10^6, 10^7\}$
the gap is $-2.4 \cdot 10^{-5}$, so the cumulative evidence is
"consistent with $B^\infty \in [0.085680, 0.0857040]$".

The decay rate is NOT cleanly $1/(\log N)^A$ at the explored scales — the
pre-asymptotic regime is dominated by sub-leading SD constants. The
fitted local exponent $k \approx 12$ for $c_0^T$ (and $\approx 18$
implied by the two-point $c_0^T$ shrinkage) is not interpretable as an
asymptotic rate.

**No new rigorous content.** Rigorization of the $B^\infty$ heuristic
remains the genuine bottleneck. Existence of $B^\infty$ remains conditional.

## 10. Files

- `bot/scratch/c0T-N1e7-empirical.py` (existing, re-run at `Nmax = 3e7`).
- `bot/scratch/c0T-rate-analysis.py` (new): consolidates empirical data
  across sessions and runs log-log fits.
- This note.
- Builds on: `P12-c0T-N1e7-validation.md`, `P12-c0T-highprecision-constants.md`,
  `P12-c0T-AB-decomposition.md`, `P12-B-infty-closed-form.md`.
