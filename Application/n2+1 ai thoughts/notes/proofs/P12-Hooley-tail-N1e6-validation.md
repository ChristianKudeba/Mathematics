# P12 — dyadic localization of $B_>(N)$ at $N = 10^6$ (one-decade extension)

**Date:** 2026-05-05 16:30 UTC
**Continues:** `P12-Hooley-tail-dyadic-localization.md` (2026-05-05 13:30) which ran the
dyadic split at $N \in \{10^4, 3\!\cdot\!10^4, 10^5, 3\!\cdot\!10^5\}$ and documented as
caveat that the concentration percentage $\ge 70\%$ across four data points was
"consistent with both a true asymptotic trend toward $\sim 90\%$ and a fixed-cutoff
artifact". One more decade was the cheapest discriminator.

## Setup

Same as 13:30. Compute
$$B_>(N) = \sum_{N < d \le N^2+1} \tau(d^2)\, \delta_d(N), \qquad \delta_d(N) = N_d(N) - \frac{\rho(d)}{d} N$$
windowed dyadically as $W_k = (N \cdot 2^k, \min(N \cdot 2^{k+1}, N^2+1)]$ for
$k = 0, 1, \ldots, K-1$, with $K = \lceil \log_2((N^2+1)/N) \rceil$. (At $N = 10^6$,
$K = 20$ and the printed top window is $W_{19} = (5.24 \cdot 10^{11}, 10^{12}+1]$;
$W_{20} = (10^{12}+1, 2 \cdot 10^{12}]$ is empty after capping and dropped by the
$\sup W_k \le \inf W_k$ guard.) Subtract the capped formal Selberg-Delange
prediction $P_k = N\big(\Sigma_*(\sup W_k) - \Sigma_*(\inf W_k)\big)$ where
$\Sigma_*(X) \approx \frac{A_3}{6}L^3 + \frac{A_2}{2}L^2 + A_1 L + A_0$, $A_3 \approx 0.05971$,
$A_2 \approx 0.43491$, $A_1 \approx 1.07159$, $A_0 \approx 0.87930$.

Code: `bot/scratch/hooley-tail-dyadic-N1e6.py` (unchanged methodology, single
$N = 10^6$ run, ~3 min wall: 162.5s factorization, 5.6s dyadic binning).
**Note on the script's "COMBINED SUMMARY" table:** the placeholder `cum_to`
values in the prior-N tuples (lines 178-183) are stored as *already-divided-by-N*
floats, but the percentage calculation at line 191 treats them as full-scale,
collapsing every prior-N row to $\sim 100\%$ at every threshold. The hand-built
markdown table in this note is computed correctly from the per-window output
of the four prior runs (archived in 13:30 session); the script's auto-summary
table at the bottom of stdout should be ignored.

## Result at $N = 10^6$

**Total residual.** $B_>(10^6) / 10^6 = 8.8621$. Linear-fit target $0.833 L - 2.876 = 8.632$ at
$L = \log 10^6 = 13.8155$. Overshoot $+0.23 N$.

**Per-window** (full table in `bot/scratch/hooley-tail-dyadic-N1e6.py` output, summary):

| $k$ | window $W_k$ | $W_k$ (empirical) | $P_k$ (formal) | $B_k = W_k - P_k$ | $B_k / N$ |
|---|---|---|---|---|---|
| 0 | $(10^6, 2 \cdot 10^6]$ | $9.16 \cdot 10^6$ | $9.16 \cdot 10^6$ | $-739$ | $-0.001$ |
| ... | ... | ... | ... | ... | $|B_k/N| \le 0.05$ |
| 16 | $(6.55 \cdot 10^{10}, 1.31 \cdot 10^{11}]$ | $2.12 \cdot 10^7$ | $2.16 \cdot 10^7$ | $-3.50 \cdot 10^5$ | $-0.350$ |
| 17 | $(1.31 \cdot 10^{11}, 2.62 \cdot 10^{11}]$ | $2.39 \cdot 10^7$ | $2.25 \cdot 10^7$ | $+1.38 \cdot 10^6$ | $+1.383$ |
| 18 | $(2.62 \cdot 10^{11}, 5.24 \cdot 10^{11}]$ | $2.68 \cdot 10^7$ | $2.35 \cdot 10^7$ | $+3.36 \cdot 10^6$ | $+3.357$ |
| 19 | $(5.24 \cdot 10^{11}, 10^{12}+1]$ (capped) | $2.72 \cdot 10^7$ | $2.27 \cdot 10^7$ | $+4.45 \cdot 10^6$ | $+4.453$ |

Sum of $B_k$ for $k = 17, 18, 19$ (the "deep-tail above $d > N^{1.85}$"): $9.19 N$ — exceeds the
total $8.86 N$ because the bulk $k = 0, \ldots, 16$ residual is slightly negative ($-0.33 N$).

**Concentration.** Cumulative residual through $d \le N^c$, normalized by $N$:

| $c$ | $\text{cum} / N$ | fraction of $B_>$ above $d > N^c$ |
|---|---|---|
| $1.30$ | $-0.050$ | $100.6\%$ |
| $1.50$ | $-0.112$ | $101.3\%$ |
| $1.70$ | $-0.120$ | $101.4\%$ |
| **$1.85$** | $-0.311$ | **$103.5\%$** |
| $1.95$ | $+4.190$ | $52.7\%$ |

## Combined evidence — five data points

Hand-computed $\text{cum}_{1.85} / N$ from the five runs (the prior four are extracted from
`bot/scratch/hooley-tail-dyadic-capped.py` output, archived in 13:30 session):

| $N$ | $L$ | $B_>(N)/N$ | $\text{cum}_{d \le N^{1.85}} / N$ | fraction $d > N^{1.85}$ |
|---|---|---|---|---|
| $10^4$ | $9.21$ | $4.85$ | $+1.45$ | $70\%$ |
| $3 \cdot 10^4$ | $10.31$ | $5.85$ | $+0.81$ | $86\%$ |
| $10^5$ | $11.51$ | $6.26$ | $+0.26$ | $96\%$ |
| $3 \cdot 10^5$ | $12.61$ | $7.88$ | $+0.72$ | $91\%$ |
| $10^6$ | $13.82$ | $8.86$ | $-0.31$ | $103\%$ |

The bulk-region cumulative residual $\text{cum}_{d \le N^{1.85}} / N$ goes
$1.45 \to 0.81 \to 0.26 \to 0.72 \to -0.31$ across the five $N$. Differences
are $-0.64, -0.55, +0.46, -1.03$: **net decrease with one local upward step at
$N = 3 \cdot 10^5$**, not a strictly monotone trajectory. The deep-tail fraction
sits at or above $90\%$ at the three highest $N$.

This **modestly strengthens** the previous session's localization claim:

- *Net direction.* The five-point sequence shows a clear net decrease in
  $\text{cum}_{d \le N^{1.85}} / N$, from $+1.45$ to $-0.31$.
- *Largest-decade evidence.* At the largest data point $N = 10^6$, the bulk
  region's contribution to $B_>(N)$ is slightly *negative*; the entire
  positive residual lives in the deep tail $d > N^{1.85}$ and overshoots
  by $3.5\%$.
- *Non-monotonicity.* The bump at $N = 3 \cdot 10^5$ remains. From five data
  points one cannot distinguish "true asymptotic with bounded fluctuation"
  from "a slowly drifting non-monotone artifact".

Re. the worry that $N^{1.85}$ may sit in a similarly favorable position within
the dyadic windowing across all five $N$ (a structural fixed-cutoff worry from
13:30): in $N \cdot 2^k$ coordinates, $N^{1.85} = N \cdot 2^{(0.85) \log_2 N}$
hits dyadic indices $11.3, 12.6, 14.1, 15.5, 16.9$ at the five $N$, with
fractional parts $\{.3, .6, .1, .5, .9\}$ — i.e. $N^{1.85}$ does *not* sit in a
fixed position relative to the nearest dyadic edge. The number of windows above
$N^{1.85}$ is approximately $0.15 \log_2 N$ at every $N$ (roughly $2$-$3$ windows
in our range), so the *count* of "above-threshold windows" is similar across
$N$ — a modest residual structural concern, partially mitigated by the differing
fractional offset.

The "$N = 10^5$ anomaly" (skeptic-flagged in 13:30) is one local bump in a
five-point sequence with net downward direction; not a systematic counterexample,
but not eliminated either.

## Structural observation: top window $= r = 1$ partial sum of $S_2(N)$

At $N = 10^6$, the topmost printed dyadic window $W_{19} = (5.24 \cdot 10^{11}, 10^{12}+1]$
captures *exactly* the $r = 1$ contribution: any $d \mid n^2+1$ with $d > N^2/2$ forces
$r = (n^2+1)/d \le (10^{12}+1)/(5.24 \cdot 10^{11}) < 1.91$, so $r = 1$ (positive integer).
Hence
$$W_{19} \;=\; \sum_{n: n^2+1 \in (5.24 \cdot 10^{11}, 10^{12}+1]} \tau\big((n^2+1)^2\big)
\;=\; \sum_{\sqrt{5.24 \cdot 10^{11} - 1} < n \le 10^6} \tau\big((n^2+1)^2\big)
\;=\; \sum_{724078 < n \le 10^6} \tau\big((n^2+1)^2\big),$$
a partial sum of the Hooley second moment $S_2(N) := \sum_{n \le N} \tau(n^2+1)^2$
restricted to a high-$n$ interval. Empirically $W_{19} = 2.72 \cdot 10^7$,
formal SD prediction $P_{19} = 2.27 \cdot 10^7$, residual $B_{19} = 4.45 \cdot 10^6 \approx 4.45 N$.

**This is a renaming, not yet a reduction.** The partial $S_2$ sum over $n \in (724078, 10^6]$
contains $\approx 276{,}000$ terms each of typical size $\tau((n^2+1)^2) \sim L^3$, so
its absolute size is comparable to a constant fraction of $S_2(10^6)$ itself. The Nair
bound (2026-05-04 13:18) gives an *upper* order of magnitude $\ll N L^3$, but no
asymptotic — and no asymptotic is needed for the SUBTRACTION $W_{19} - P_{19}$ to be
"small". The structural observation is that *the calculation we already need to do for
the second-moment problem is the same calculation that controls the topmost dyadic
window of $B_>(N)$*. So progress on either feeds the other; this is a consistency
constraint, not a route around the underlying Hooley boundary.

The same labeling extends partially to lower windows: $W_{18}$ at $N = 10^6$
captures both $r = 1$ and $r = 2$ contributions (when $n^2+1$ is even, i.e. $n$ odd);
$W_{17}$ captures $r \in \{1, 2, 3\}$; etc. So small-$r$ pieces dominate the deep-tail
residual, consistent with the boundary-effect interpretation in the 13:30 note. The
*cross-window combination* (summing over $r = 1, 2, \ldots, R$ for some growing $R$) is
the same hyperbola-style integration as Hooley-1957 §3 and is not made simpler by this
observation.

## Caveats

1. **Formal-SD extrapolation, $X = N^2+1 = 10^{12}$.** The 06:51 session's empirical
   validation of the Laurent expansion was on $X \le 10^7$; at $N = 10^6$ the topmost
   window's upper edge is $X = 10^{12}$, five decades beyond the validated range.
   Theoretical justification is analyticity of $H$ on $\Re s > 1/2$ and the
   $O(X / (\log X)^A)$ Selberg-Delange remainder, but the constant in that remainder is
   **not effectively tracked at $X = 10^{12}$ in this work**. We have NOT computed an
   explicit Tauberian budget at this $X$; the bound "the residual is much larger than
   any reasonable Tauberian budget" is a *qualitative* claim. Concretely the deep-window
   $B_k / N$ at $N = 10^6$ are $1.38, 3.36, 4.45$, and the empirical residual envelope on
   $\Sigma_*$ within the validated $X \le 10^7$ range was $\le 0.063$; if one accepts a
   *suggestive* extrapolation budget of $\le 0.5$ per window even at $X = 10^{12}$, the
   deep-window signal exceeds it by an order of magnitude. This is the strongest current
   defense; an effective constant would convert it to a hard bound but is not done here.

2. **Single new data point.** The trend across five data points is suggestive but not
   asymptotic. To rule out a pathological non-monotone trajectory, $N = 3 \cdot 10^6$
   (~30 min wall, single session) would be the next compute target. Not done here in
   the interest of finishing one thing. *In particular, "rules out fixed-cutoff
   artifact" was an over-claim from one new data point — the conservative phrasing is
   "consistent with a true asymptotic localization, with one local non-monotone step
   already documented".*

3. **The "$r = 1$ sub-target" remark is interpretive.** It identifies $W_K$ (the
   capped top window) with a partial $S_2$ sum cleanly, but that does not yet supply an
   analytic reduction. The analog of "Hooley-1957 §3" is an **integration over
   $r$-weighted boundary** combining $W_K, W_{K-1}, \ldots$; the present observation
   sharpens the $W_K$ contribution but the cross-window combination is the same task as
   before.

4. **The empirical $B_>/N$ overshoot $+0.23$ at $N = 10^6$.** Linear fit predicted
   $8.63$, observed $8.86$. The fit was based on four data points and the overshoot
   is the largest absolute deviation in the table. Simple two-parameter linear fits do
   not have to extrapolate cleanly; one would expect a $(\log L)$ correction to enter
   eventually. Not currently a priority to refit.

## Conclusion (revised after skeptic round 1)

The cheap empirical-extension diagnostic of the 13:30 session **succeeds, modestly**:
at one more decade ($N = 10^6$), the deep-tail concentration measure $> N^{1.85}$ is
$103\%$, with bulk-region cum residual $-0.31 N$ — consistent with the prior
localization claim, with one local non-monotone step at $N = 3 \cdot 10^5$ unexplained.
"Rules out fixed-cutoff artifact" overstates from one new data point; "consistent with
a true asymptotic localization" is honest.

A structural observation: at each $N$, the topmost dyadic window $W_{K-1}$ (the partial
window capped at $N^2+1$) corresponds exactly to the $r = 1$ contribution from $n$ in
the top range of $[1, N]$, hence equals a partial sum of the Hooley second moment
$S_2(N)$. This is a renaming, not an analytic reduction — the partial $S_2$ sum is
itself a comparable-difficulty open problem (only an order-of-magnitude bound is known,
via Nair 2026-05-04 13:18). It functions as a consistency constraint between the
Hooley-tail residual and the second-moment problem, and tells us that progress on
either feeds the other.

**Next-session candidates** (not chosen this session):
- (i) Compute $W_{19}$ and $P_{19}$ symbolically: write $W_{19}$ as a partial $S_2$
  sum, write $P_{19}$ in closed form via the Laurent of $\Sigma_*$, see if their leading
  $L^3, L^2, L$ terms match (they should, modulo the boundary correction we are after).
- (ii) Run $N = 3 \cdot 10^6$ to add a sixth data point (~30 min compute).
- (iii) Begin the Hooley-1957-§3-style direct boundary integral (likely 2-4 sessions,
  research-y).
