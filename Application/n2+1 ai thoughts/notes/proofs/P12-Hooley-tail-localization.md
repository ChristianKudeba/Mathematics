# P12 — Empirical localization of the formal-SD residual to the Hooley tail $B_>(N)$

**Date:** 2026-05-05 (continuation of `P12-sigma-star-empirical-validation.md`)
**Author:** Claude (mathAI bot)
**Status:** PROGRESS — clean structural decomposition $S(N) = N\Sigma_*(N) + S_>(N) - E(N)$, plus diagnostic that the empirical $\approx 0.85 NL - 2.2 N$ residual lives entirely in the $d > N$ piece.

## Setup

Recall the elementary identity (for any $m \ge 1$)
$$ \tau(m)^2 = \sum_{d \mid m} \tau(d^2), $$
valid because both sides are multiplicative and $\sum_{j=0}^{e}(2j+1) = (e+1)^2 = \tau(p^e)^2$ at every prime power. Applying with $m = n^2+1$ and switching summation,
$$ S(N) := \sum_{n=1}^N \tau(n^2+1)^2 = \sum_{d \ge 1} \tau(d^2)\, N_d(N), \qquad N_d(N) := |\{n: 1 \le n \le N,\ d \mid n^2+1\}|. $$

For $d \ge 1$ define $\rho(d) := |\{r \pmod d: r^2 \equiv -1 \pmod d\}|$, so $\rho$ is multiplicative with $\rho(2)=1$, $\rho(2^k)=0$ for $k \ge 2$, $\rho(p^k)=2$ for $p \equiv 1 \pmod 4$, and $\rho(p^k) = 0$ for $p \equiv 3 \pmod 4$. Define the **discrepancy**
$$ \delta_d(N) := N_d(N) - \rho(d)\,\tfrac{N}{d}. $$
For $d \le N^2+1$, $|\delta_d(N)| \le \rho(d)$. For $d > N^2+1$, $N_d(N) = 0$.

Set $\Sigma_*(X) := \sum_{d \le X} \tau(d^2)\rho(d)/d$. Since $N_d(N) = 0$ for $d > N^2+1$, both sums truncate at $d \le N^2+1$ and we get the **exact** identity
$$ S(N) \;=\; \sum_{d=1}^{N^2+1} \tau(d^2)\,\rho(d)\tfrac{N}{d} \;+\; \sum_{d=1}^{N^2+1} \tau(d^2)\delta_d(N) \;=\; N\,\Sigma_*(N^2+1) \;+\; B(N), $$
where $B(N) := \sum_{d \le N^2+1} \tau(d^2)\delta_d(N)$. The truncation $d \le N^2+1$ matters: there is no infinite-sum tail being silently dropped.

The formal-SD ansatz $S(N) \approx N\Sigma_*(N^2)$ corresponds to (i) dropping $B(N)$ entirely and (ii) using $\Sigma_*(N^2)$ in place of $\Sigma_*(N^2+1)$. The replacement (ii) is the single term
$$ \Sigma_*(N^2+1) - \Sigma_*(N^2) \;=\; \tfrac{\tau((N^2+1)^2)\,\rho(N^2+1)}{N^2+1}, $$
nonzero only when $N^2+1$ has all prime factors in $\{2\}\cup\{p \equiv 1 \pmod 4\}$, and bounded by $\tau((N^2+1)^2)/(N^2+1) = O(N^{-2+o(1)})$ via the standard $\tau$-bound. Multiplied by $N$ this contributes $O(N^{-1+o(1)})$ — pointwise negligible.

## Empirical localization

Split $B(N) = B_<(N) + B_>(N)$ with
$$ B_<(N) := \sum_{d \le N} \tau(d^2)\delta_d(N), \qquad B_>(N) := \sum_{d > N} \tau(d^2)\delta_d(N). $$

Equivalently, with $S_<(N) := \sum_n \sum_{d \mid n^2+1, d \le N} \tau(d^2)$ and $S_>(N) := \sum_n \sum_{d \mid n^2+1, d > N} \tau(d^2)$:
$$ S_<(N) = N\Sigma_*(N) + B_<(N), \qquad S_>(N) = N\big(\Sigma_*(N^2) - \Sigma_*(N)\big) + B_>(N). $$

Direct computation: sieve $n^2+1$ for $n \le N$, enumerate divisors, split on $d \le N$ vs $d > N$; $\Sigma_*(N)$ is computed by sieving $a_d := \tau(d^2)\rho(d)$ directly (so this comparison is **exact**, not Laurent-approximated). The formal-SD prediction for $\Sigma_*(N^2) - \Sigma_*(N)$ uses the four-term Laurent
$$ \Sigma_*(X) = \tfrac{A_3}{6}L^3 + \tfrac{A_2}{2}L^2 + A_1 L + A_0 + O(L^{-A}), \quad L = \log X, $$
with $A_3 = 0.0597$, $A_2 = 0.4349$, $A_1 = 1.0716$, $A_0 = 0.8793$ from prior sessions, validated empirically at $X \le 10^7$ with sign-oscillating residual $\le 0.063$ (`P12-sigma-star-empirical-validation.md`).

**Tauberian-remainder budget for the $S_>$ comparison.** The quantity we compute, `formal_tail`, is $L_X = \log X$-Laurent at $X = N^2$ minus the same at $X = N$. Each carries an independent Tauberian remainder $O(L^{-A})$, so the absolute error in `formal_tail` is at most twice the prev-session-validated bound $\le 0.063$, i.e. $\le 0.13$ per N at $X \le 10^7$. At $X = N^2 \le 9 \cdot 10^{10}$ the per-X remainder is at most comparable (by analyticity of $H$ in $\Re s > 1/2$); we conservatively bound it by $0.2$ per N. This is much smaller than the observed $B_>(N)/N \in [2.85, 7.88]$.

| $N$ | $L$ | $S(N)$ | $S_<(N)$ | $S_>(N)$ | $B_<(N)/N$ | $B_>(N)/N$ |
|---|---|---|---|---|---|---|
| $10^3$ | 6.91 | $86\,384$ | $22\,037$ | $64\,347$ | $+0.037$ | $+2.85$ |
| $3\!\cdot\!10^3$ | 8.01 | $355\,420$ | $85\,530$ | $269\,890$ | $+0.022$ | $+3.81$ |
| $10^4$ | 9.21 | $1\,614\,068$ | $369\,168$ | $1\,244\,900$ | $-0.027$ | $+4.85$ |
| $3\!\cdot\!10^4$ | 10.31 | $6\,254\,896$ | $1\,378\,505$ | $4\,876\,391$ | $+0.002$ | $+5.85$ |
| $10^5$ | 11.51 | $26\,859\,868$ | $5\,722\,346$ | $21\,137\,522$ | $-0.017$ | $+6.26$ |
| $3\!\cdot\!10^5$ | 12.61 | $100\,153\,656$ | $20\,687\,939$ | $79\,465\,717$ | $+0.022$ | $+7.88$ |

**Two findings:**

1. **$B_<(N)/N$ is empirically bounded by $0.04$ in absolute value across all six datapoints**, oscillating in $[-0.03, +0.04]$ with no clear monotone growth or trend. **This is an empirical observation only, on six datapoints over $L \in [6.91, 12.61]$**: a slow $\log\log L$ growth or a sign-oscillating $O(\sqrt L)$ behavior cannot be ruled out at this dynamic range. The Erdős-Hooley-type heuristic in §"Why $B_<$ plausible" gives $O(\sqrt N L) = O(\sqrt N L \ll N L)$ as the natural-looking upper bound; observed $O(1)$ per N is much stronger and unexplained. **What we can claim rigorously from this data:** $|B_<(N)/N| \le 0.05$ at $N \in \{10^3, 3\cdot10^3, 10^4, 3\cdot10^4, 10^5, 3\cdot10^5\}$, hence $B_<(N)$ is **not** the source of the observed $\approx 0.85 NL$ residual on $S(N)$ at any of these six $N$. Whether this extends asymptotically remains open.

2. **$B_>(N)/N$ scales linearly in $L$.** Linear regression (six points, $L \in [6.91, 12.61]$):
   $$ B_>(N)/N \;\approx\; 0.833\, L \;-\; 2.876, \qquad R^2 = 0.982. $$
   This matches the previous-session empirical fit $S(N)/N - c_3 L^3 - c_2 L^2 - c_1^{\text{formal}} L \approx 0.85 L - 2.2$ within the noise of a six-point fit. **Reconciliation arithmetic:** the previous fit was on the residual relative to the **3-term** Laurent. Subtracting the 4-term Laurent instead means subtracting the additional $A_0 = 0.879$, so the 3-term-residual fit $0.85L - 2.2$ becomes the 4-term-residual fit $(0.85 L - 2.2) - 0.879 = 0.85 L - 3.079$. Our regressed intercept $-2.88$ matches this $-3.08$ within $0.2$, comparable to the regression's own slope-times-$L$-range uncertainty.

**Localization claim.** The entire formal-SD-vs-empirical residual on $S(N)$ at orders $NL$ and below resides in $B_>(N) = \sum_{d > N} \tau(d^2)\delta_d(N)$.

## Why this is structurally meaningful

The discrepancy $\delta_d(N) = N_d(N) - \rho(d) N/d$ is, for each $d$, the integer-valued-vs-continuous-approximation gap. It admits the explicit representation, with $r$ ranging over the $\rho(d)$ residues of $x^2 \equiv -1 \pmod d$ in $\{1, \ldots, d-1\}$:
$$ N_d(N) = \sum_{r} \big(\lfloor (N-r)/d \rfloor + 1\big) \cdot \mathbb{1}[r \le N]. $$

For $d > N$: each residue rep $r$ contributes $\mathbb{1}[r \le N]$ (zero or one), so $N_d(N) = |\{r: r \le N\}|$, while $\rho(d)N/d < \rho(d)$ in expectation under uniform spread. Then
$$ B_>(N) = \sum_{d > N} \tau(d^2) \sum_{r^2 \equiv -1 \!\!\pmod d,\ 1 \le r \le d-1} \big(\mathbb{1}[r \le N] - \tfrac{N}{d}\big). $$
Because the $\rho(d)$ reps come in pairs $(r, d-r)$, this can be rewritten using only the small root $r \in (0, d/2)$:
$$ B_>(N) = \sum_{d > N} \tau(d^2) \!\!\sum_{r \in (0, d/2),\ r^2 \equiv -1\,(d)} \Big(\mathbb{1}[r \le N] + \mathbb{1}[d - r \le N] - \tfrac{2N}{d}\Big). $$
For $d > 2N$ the term $\mathbb{1}[d-r \le N]$ vanishes (since $d - r > d/2 > N$), so the relevant pair contribution is $\mathbb{1}[r \le N] - 2N/d$ for $d > 2N$.

This is precisely a **discrepancy sum for the small roots of $x^2 \equiv -1 \pmod d$**, weighted by $\tau(d^2)$. The "expected size" $\rho(d) N/d$ corresponds to the small root $r$ being uniformly distributed in $(0, d/2)$. The empirical $B_>(N)/N \sim 0.83 L - 2.88$ measures the systematic deviation from uniformity, and is the precise quantity the next analytic step must compute or bound.

## Why $B_<(N)/N = O(1)$ is plausible

For $d \le N$, every rep $r \in \{1, \ldots, d-1\}$ satisfies $r \le N$, so the discrepancy comes from the floor-function rounding at the upper end. Writing $N = qd + s$ with $s \in \{0, \ldots, d-1\}$:
$$ \delta_d(N) = |\{r: r \le s\}| - \rho(d)\,s/d. $$
The expectation under $r$-uniformity is zero. Summing $\tau(d^2)\delta_d(N)$ over $d \le N$ gives a bilinear sum in (1) the divisor-weight $\tau(d^2)\rho(d)$ and (2) discrepancies of the small-root distribution in subintervals $[1,s]$ of $[1, d-1]$. Erdős-Hooley-type equidistribution would give $O(\sqrt{\Sigma_{**}(N)}) = O(\sqrt{N} L)$ heuristically; the empirical observation of $O(1)$ per $N$ is much stronger than this and suggests deeper cancellation — but the empirical conclusion is robust to the heuristic.

## Sanity checks

- $S_<(N) + S_>(N) = S(N)$: matches `tau-sq-second-moment.py` output at every $N$.
- $S_<$ at $N=10^3$: 22037, vs $N\Sigma_*(N) \approx 22000$. Direct check on the divisor enumeration at $n=3$ ($m=10$, divisors $\le 1000$ are all of $\{1,2,5,10\}$, $\tau(d^2) \in \{1,3,3,9\}$, sum 16, matches $\tau(10)^2 = 16$). ✓
- Closed-form Laurent-difference $\Sigma_*(N^2) - \Sigma_*(N) = \frac{7A_3}{6}L^3 + \frac{3A_2}{2}L^2 + A_1 L$ at $L = \log N = 6.91$ evaluates to $0.0697 \cdot 329.9 + 0.6524 \cdot 47.75 + 1.0716 \cdot 6.91 = 23.00 + 31.15 + 7.40 = 61.55$. The script reports `formal_tail = 61.493` per N. ✓ within Laurent-rounding.

## Caveats

1. **Six-point regression.** The empirical fit $B_>(N)/N \approx 0.83 L - 2.88$ rests on six data points spanning $L \in [6.9, 12.6]$. The slope and intercept are individually well-determined by least squares ($R^2 = 0.98$), but a slow $\log\log$ correction in either coefficient cannot be ruled out at this dynamic range.

2. **The $N=10^5$ point sits below the fit by $\approx 0.45$.** This is the largest residual of the six and exceeds the others by $\sim 4\times$. It might be statistical fluctuation in the data or might signal genuine sub-linear structure. Adding $N = 10^6, 3 \cdot 10^6$ would discriminate; the script time-budget here capped at $N = 3 \cdot 10^5$.

3. **The formal-SD prediction $\Sigma_*(N^2) - \Sigma_*(N)$ uses the four-term Laurent**, not the actual partial sum. The Laurent-vs-partial-sum error is bounded by $0.063$ at $X \le 10^7$ from the previous session; at $X = N^2 \le 10^{12}$ it is presumed comparable, but is not directly verified. Even pessimistically, this error contributes $O(0.1)$ per N to the comparison — much less than the observed $B_>(N)/N \in [2.85, 7.88]$.

4. **The claim that $B_<(N) = O(N)$ is empirical only over $N \le 3 \cdot 10^5$.** It would be cleaner to derive it rigorously; this is left as a subtask. (A heuristic Erdős-Hooley bound gives $O(\sqrt{N}L)$, which would be $O(N)$ in our range and hence consistent.)

## Files

- `bot/scratch/hooley-tail-decomposition.py` — sieve + divisor-split + $\Sigma_*$ comparison.

## Strategic implication

This session does not advance any rigorous bound on $S(N)$. What it does is **isolate the analytic target**: any rigorization of the second-moment asymptotic must compute or bound
$$ \boxed{\; B_>(N) \;=\; \sum_{d > N} \tau(d^2) \!\!\sum_{r \in (0,d/2),\ r^2 \equiv -1 \!\!\pmod d}\! \Big(\mathbb{1}[r \le N] + \mathbb{1}[d-r \le N] - \tfrac{2N}{d}\Big). \;} $$

The natural attack is via Hooley-style equidistribution of the roots $r$, weighted by $\tau(d^2)$ instead of $1$. This is structurally a $\tau^2$-analog of Hooley (1957) §3-4; the expected difficulty is comparable. The empirical target is $B_>(N) \approx 0.85 NL - 2.9 N$ at the leading $NL$ order with $\approx 5\%$ data-fit uncertainty in both coefficients.

The complementary small-divisor sum $B_<(N)$ is empirically at most $O(N)$ and so does not contribute at order $NL$; rigorizing this is a low-cost auxiliary subtask.
