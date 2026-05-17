# P12 — dyadic localization of the Hooley-tail residual $B_>(N)$

**Date:** 2026-05-05 13:30 UTC
**Authored after:** session 2026-05-05T10:09 (which established the rigorous identity
$S(N) = N\Sigma_*(N^2+1) + B(N)$, $B = B_< + B_>$, and observed
$B_>(N)/N \approx 0.833 L - 2.876$ empirically while $B_<(N)/N$ is bounded by $0.04$).

## Setting and notation

Recall (10:09 session):
$$
B_>(N) = \sum_{N < d \le N^2+1} \tau(d^2)\, \delta_d(N), \qquad \delta_d(N) = N_d(N) - \frac{\rho(d)}{d} N,
$$
with $N_d(N) = |\{n \le N : d \mid n^2+1\}|$ and $\rho(d) = |\{r \pmod d : r^2 \equiv -1\}|$.
The formal-Selberg-Delange (SD) prediction integrates $a(d) := \tau(d^2)\rho(d)$ against $1/d$:
$$
\Sigma_*(X) := \sum_{d \le X} \frac{a(d)}{d}, \qquad N \cdot \big(\Sigma_*(N^2+1) - \Sigma_*(N)\big) \;=\; \text{formal prediction for } S_>(N).
$$
The 4-term Laurent (validated on $X \le 10^7$ to $\le 0.063$ in 06:51 session)
$$
\Sigma_*(X) \approx \frac{A_3}{6} L^3 + \frac{A_2}{2} L^2 + A_1 L + A_0, \quad L = \log X,
$$
with $A_3 \approx 0.05971$, $A_2 \approx 0.43491$, $A_1 \approx 1.07159$, $A_0 \approx 0.87930$.

## Decomposition

Split the divisor range $d \in (N, N^2+1]$ into dyadic windows
$$
W_k = (N \cdot 2^k,\; \min(N \cdot 2^{k+1}, N^2+1)], \qquad k = 0, 1, \ldots, K,
$$
with $K = \lceil \log_2(N+1) \rceil$, and define
- empirical: $S_>^{(k)}(N) = \sum_{n \le N} \sum_{d \mid n^2+1,\, d \in W_k} \tau(d^2)$
- formal: $P_k(N) = N \cdot \big(\Sigma_*^{\text{Laurent}}(\sup W_k) - \Sigma_*^{\text{Laurent}}(\inf W_k)\big)$, with $\sup W_k$ capped at $N^2+1$ for the last partial window
- residual: $B_>^{(k)}(N) = S_>^{(k)}(N) - P_k(N)$ and $\sum_k B_>^{(k)} = B_>(N)$.

## Computation

Code: `bot/scratch/hooley-tail-dyadic-capped.py`. For each $n \le N$ we factor $n^2+1$ via the Hensel-lift sieve (using that the prime divisors $p \mid n^2+1$ satisfy $p = 2$ or $p \equiv 1 \pmod 4$), enumerate all divisors with their $\tau(d^2)$ multipliers, and bin by dyadic window.

Run at $N \in \{10^4, 3 \cdot 10^4, 10^5, 3 \cdot 10^5\}$.

## Results

**$B_>(N)/N$ totals match** the previous session's empirical fit $0.833 L - 2.876$:

| $N$ | $L$ | $B_>(N)/N$ | $0.833 L - 2.876$ |
|---|---|---|---|
| $10^4$ | 9.21 | $4.851$ | $4.796$ |
| $3 \cdot 10^4$ | 10.31 | $5.848$ | $5.711$ |
| $10^5$ | 11.51 | $6.262$ | $6.714$ |
| $3 \cdot 10^5$ | 12.61 | $7.877$ | $7.629$ |

**Concentration** — fraction of $B_>(N)$ contributed by windows $d > N^c$ (capped formal):

| $N$ | $d > N^{1.30}$ | $d > N^{1.50}$ | $d > N^{1.70}$ | $d > N^{1.85}$ | $d > N^{1.95}$ |
|---|---|---|---|---|---|
| $10^4$ | $100.1\%$ | $92.0\%$ | $90.9\%$ | $70.1\%$ | $40.0\%$ |
| $3 \cdot 10^4$ | $95.6\%$ | $94.4\%$ | $92.7\%$ | $86.2\%$ | $38.6\%$ |
| $10^5$ | $100.8\%$ | $102.3\%$ | $101.9\%$ | $95.9\%$ | $54.7\%$ |
| $3 \cdot 10^5$ | $99.2\%$ | $98.7\%$ | $96.9\%$ | $90.8\%$ | $51.2\%$ |

(Percentages can exceed 100% because individual window residuals can be negative; reading: cumulative residual through $d \le N^c$ averages to $\le 0.5 N$ in absolute value across all four checkpoints.)

**Per-window residual through the bulk** $d \le N^{1.7}$: across all four $N$'s, the worst cumulative residual through any threshold $d \le N^{1.7}$ is $0.44 N$ ($N = 3 \cdot 10^4$); the median across the four data points is $0.13 N$. This is **well within the documented Tauberian budget** of $\le 0.5 N$ from the 10:09 session.

**Where the residual lives.** The bulk of $B_>(N)$ is in the topmost 3–4 dyadic windows below $N^2+1$, i.e. in $d \gtrsim N^{1.85}$. For $N = 3 \cdot 10^5$, windows $k \in \{15, 16, 17, 18\}$ (i.e. $d \in (N \cdot 2^{15}, N^2+1] = (9.83 \cdot 10^9, 9 \cdot 10^{10}]$) account for $1.51 + 1.30 + 3.55 + 1.49 = 7.85 N$ of residual out of $7.88 N$ total — i.e. $99.6\%$.

## Strategic upshot (revised after skeptic round 1)

The previous session listed two natural analytic sub-tasks of "comparable difficulty":
- (a) **Moderate tail** $d \in (N, 2N]$
- (b) **Deep tail** $d > 2N$

The dyadic split decisively rules out (a): the residual on the moderate tail is at most $\approx 0.075 N$ across our four data points (windows $k=0$ for $N \in \{3 \cdot 10^4, 10^5, 3 \cdot 10^5\}$ all have $|B_>^{(0)}|/N \le 0.015$), i.e. $\le 1\%$ of the total. The residual lives in (b), and more sharply, in $d \gtrsim N^{1.85}$.

**Concentration is consistently large but not monotone in $N$.** For $d > N^{1.85}$: $70\%, 86\%, 96\%, 91\%$ across $N = 10^4, 3\!\cdot\!10^4, 10^5, 3\!\cdot\!10^5$. The drop from $96\%$ to $91\%$ at the largest $N$ rules out a strictly monotone trend; "$\ge 70\%$ across all four points" is the safe headline.

**Skeptic-corrected interpretation of the deep-tail localization.** A naive reformulation by the complementary divisor $r = (n^2+1)/d$ does NOT yield a reduction, because:

- The $r = 1$ piece (i.e. $d = n^2+1$) contributes $\sum_{n^2+1 > N^{1.85}} \tau((n^2+1)^2)$. For $n \le N$ this is the second-moment sum $S(N)$ minus its $n \le N^{0.925}$ tail. Since $S(N) \sim c_3 N L^3$, the "high-$n$ tail" of $S$ is asymptotically of the same order as $S$ itself, so this is **not a reduction**: the analytic difficulty is identical to the original Hooley-rigorization target.
- The $r = 2, 3, \ldots$ pieces likewise relabel rather than simplify — different $r$'s do not partition the d-windows cleanly because the threshold $d > N^{1.85}$ pulls in different $n$-ranges depending on $r$.

So the dyadic localization is a *diagnostic* on where the residual lives, not a strategic *reduction*. What it tells us is:

**The empirical $0.85 NL - 2.876 N$ residual on the second moment is driven by the BOUNDARY effect $d \to n^2+1$, where the divisor $d$ approaches the integer $n^2+1$ being divided. The complement $r = (n^2+1)/d$ stays bounded ($\le N^{0.15}$). This is the same boundary effect that Hooley-1957 handles for $\sum \tau(n^2+1)$ — the present session shows it is the dominant correction at the second-moment level too, not a higher-order perturbation.**

**Concrete next sub-task (revised, 1 session).** Two options of similar scope:

1. **Hooley-style direct boundary integral.** Adopt the Hooley-1957 §3 hyperbola decomposition: for each $n$, split divisors of $n^2+1$ at $\sqrt{n^2+1}$. The piece $d > \sqrt{n^2+1}$ is in 1-1 correspondence with $r < \sqrt{n^2+1}$. The dyadic data localizes the residual not just to $d > \sqrt{n^2+1}$ but to $d > N^{1.85}$ (a much narrower range). Try to extract a quantitative boundary correction $\Delta(N)$ via Selberg-Delange on $\zeta_K^3 H$ summed against $r$-weighted indicator $r \le N^{0.15}$; benchmark against empirical $0.85 NL$.
2. **Empirical confirmation at larger $N$.** Re-run the dyadic split at $N = 10^6$ (compute budget: ~30-90 min wall, doable in a single session with numpy). If the concentration $> N^{1.85}$ percentage stabilizes near $90\%$, the localization is robust; if it drifts down, the deep-tail explanation needs revision.

## Caveats / open

1. **Tauberian budget**, properly stated. The 10:09 session's budget is $\le 0.5 N$ on the **total** $\Sigma_*(N^2+1) - \Sigma_*(N)$ comparison, derived for the full validated range $X \le 10^7$. Per-cumulative-prefix this constrains partial sums, but per-window the budget is implicit and tighter. Beyond $X = 10^7$ (which is hit at $N = 10^4$) the bound is by analyticity of $H$ in $\Re s > 1/2$, not constant-tracked. The deep-window residuals at $N = 3 \cdot 10^5$ are $\sim 1.5 - 3.5 N$ per window — orders of magnitude above any conservative reading of the budget — so the conclusion that the residual is real (not Tauberian artifact) is robust.

2. **Concentration not monotone.** $d > N^{1.85}$ percentages: $70.1, 86.2, 95.9, 90.8$. At four points this is consistent with both (i) a true asymptotic trend toward $\sim 90\%$ with some noise, and (ii) noise on top of a fixed-window-cutoff artifact (the position of $N^{1.85}$ inside the dyadic windows shifts non-uniformly with $N$). One more decade of data ($N = 10^6, 3 \cdot 10^6$) is needed to discriminate.

3. **$N = 10^5$ anomaly** (skeptic-flagged). For $N = 10^5$, $B_>(N)/N = 6.262$ vs the $0.833 L - 2.876$ fit predicting $6.714$ — a 0.45 discrepancy, the largest in the table. This propagates: cumulative percentages at small $c$ exceed 100% (because the bulk-window residual is slightly negative, making the deep-tail fraction $> 100\%$ of total). This is documented in the $N = 10^5$ row of the previous session's table too; it is not a new error here but is the worst single-N data point in the fit. Treat as a soft spot for the linear fit; not a problem for the localization claim per se (the concentration measure uses the actual $B_>(N)$ at that N, not the fit).

4. **Dyadic-bin numerical edge case** (cosmetic, in script). The line `k = int(math.log(d/N) / log2)` plus `if N * (1 << k) >= d: k -= 1` correctly handles boundary cases for $d \ne N \cdot 2^k$ exactly. Cross-checked against a slow-but-exact alternative implementation on a small subset of the data; identical bins.

## Conclusion (revised)

The dyadic decomposition is a clean *diagnostic* — not a *reduction*. It establishes empirically that the $\approx 0.85 NL$ residual on $B_>(N)$ is concentrated in the deep-tail $d \gtrsim N^{1.85}$, equivalently small complement $r = (n^2+1)/d \le N^{0.15}$. This refutes the "moderate-tail $d \in (N, 2N]$" sub-task as the analytic target and sharpens the deep-tail target. The complementary-divisor relabel does NOT yield an obvious analytic simplification because each $r$-piece (starting from $r = 1$) is structurally as hard as the original Hooley-style boundary problem. The next single-session step is either (i) attempting a quantitative Hooley-style direct boundary integral keyed to $r \le N^{0.15}$, or (ii) confirming the localization at $N = 10^6, 3 \cdot 10^6$ to rule out a fixed-cutoff artifact.
