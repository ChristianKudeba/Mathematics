# P12 — Broad $(N, h)$ scan of $\rho_h(N) := |H_h(N)|^2 / D_h(N)$

**Session:** 2026-05-10 (pickup hint #1 from `2026-05-10T03-52-40Z`).

**Definitions.** Let $\widetilde S_h(e) := \prod_{p \mid e} f_h(p, e)$ on
square-free good $e$ (good $:=$ every prime factor is $2$ or $\equiv 1 \pmod 4$),
where $f_h(2, e) = (-1)^h$ and $f_h(p, e) = 2 \cos(2\pi h \alpha_p (e/p)^{-1}_p / p)$
at split $p$, with $\alpha_p$ the chosen square root of $-1 \pmod p$. Write

$$
H_h(N) := \!\!\sum_{\substack{2 \le e \le N \\ e\ \mathrm{sf,\ good}}}\!\! \widetilde S_h(e),
\qquad
D_h(N) := \!\!\sum_{\substack{2 \le e \le N \\ e\ \mathrm{sf,\ good}}}\!\! \widetilde S_h(e)^2,
\qquad
\rho_h(N) := \frac{H_h(N)^2}{D_h(N)}.
$$

By Cauchy–Schwarz, $\rho_h(N) \le |\{e \le N : \mathrm{sf,\ good}\}| =: M(N)$,
empirically $M(N) \approx 0.115 N$ at $N = 10^7$. The strategic interest is the
much sharper relation

$$
\rho_h(N) = O(1) \text{ uniformly in } (N, h)
\;\iff\;
|H_h(N)| = O(\sqrt{N}) \text{ uniformly},
$$

since $D_h(N) \sim C_h N$ with $C_h \in [0.39, 0.55]$ (proved
in `P12-Halasz-Dh-diagonal.md`, Selberg–Delange $\kappa = 1$).

## 1. Data

42 $(N, h)$ data points computed by `bot/scratch/Halasz-rho-broad.py`.

### 1.1 Horizontal scan: $N = 10^7$, varying $h$

| $h$ | $H_h$ | $|H_h|/\sqrt N$ | $D_h$ | $D_h/N$ | $\rho_h$ |
|---|---|---|---|---|---|
| 1   |   291.28  | 0.092 | $3.928 \cdot 10^6$ | 0.393 | 0.0216 |
| 2   |  -757.57  | 0.240 | $3.919 \cdot 10^6$ | 0.392 | 0.1464 |
| 3   |  -784.43  | 0.248 | $3.919 \cdot 10^6$ | 0.392 | 0.1570 |
| 5   |  -529.27  | 0.167 | $5.426 \cdot 10^6$ | 0.543 | 0.0516 |
| 7   |  -283.07  | 0.090 | $3.925 \cdot 10^6$ | 0.393 | 0.0204 |
| 10  |  -879.66  | 0.278 | $5.429 \cdot 10^6$ | 0.543 | 0.1425 |
| 13  |   122.76  | 0.039 | $4.506 \cdot 10^6$ | 0.451 | 0.0033 |
| 17  |  -168.65  | 0.053 | $4.363 \cdot 10^6$ | 0.436 | 0.0065 |
| 20  |  -316.83  | 0.100 | $5.440 \cdot 10^6$ | 0.544 | 0.0184 |
| 50  |    -2.90  | 0.001 | $5.431 \cdot 10^6$ | 0.543 | $5\cdot 10^{-7}$ |
| 100 | -2151.42  | 0.680 | $5.434 \cdot 10^6$ | 0.543 | 0.8518 |
| 500 | -3278.22  | 1.037 | $5.423 \cdot 10^6$ | 0.542 | 1.9819 |
| 1000| -4288.91  | 1.356 | $5.423 \cdot 10^6$ | 0.542 | 3.3917 |
| 2000| -3276.99  | 1.036 | $5.424 \cdot 10^6$ | 0.542 | 1.9798 |
| 5000|  -565.05  | 0.179 | $5.430 \cdot 10^6$ | 0.543 | 0.0588 |
|10000|  -314.62  | 0.099 | $5.443 \cdot 10^6$ | 0.544 | 0.0182 |

### 1.2 Vertical scans: trajectories at fixed $h$

Trajectory of $\rho_h(N)$ across $N$:

| $h$ | $N=10^6$ | $N=3 \cdot 10^6$ | $N=10^7$ | $N=2 \cdot 10^7$ | $N=3 \cdot 10^7$ |
|---|---|---|---|---|---|
| 1   | 0.0072 | 0.0129 | 0.0216 | 0.0342 | 0.0268 |
| 2   | 0.0039 | 0.0105 | 0.1464 | 0.0171 | 0.0072 |
| 5   | 0.0013 | 0.0769 | 0.0516 | 0.0397 | 0.1399 |
| 100 | 2.1079 | 0.6189 | 0.8518 | 0.0261 | 0.0642 |

Same data as $|H_h(N)|/\sqrt N$:

| $h$ | $10^6$ | $3 \cdot 10^6$ | $10^7$ | $2 \cdot 10^7$ | $3 \cdot 10^7$ |
|---|---|---|---|---|---|
| 1   | 0.053 | 0.071 | 0.092 | 0.116 | 0.103 |
| 2   | 0.039 | 0.064 | 0.240 | 0.082 | 0.053 |
| 5   | 0.026 | 0.204 | 0.167 | 0.147 | 0.276 |
| 100 | 1.067 | 0.579 | 0.680 | 0.119 | 0.187 |

### 1.3 Summary statistics across all 42 points

- $\max_{(N, h)} \rho_h(N) = 3.39$ (at $h=1000, N=10^7$).
- $\max_{(N, h)} |H_h(N)|/\sqrt N = 1.36$ (same point).
- $D_h(N)/N$ matches the closed-form prediction $C_h$ to $< 10^{-3}$ at every
  point, as established in `P12-Halasz-Dh-diagonal.md`.

## 2. Three readings of the data

### 2.1 The pickup-hint question RESOLVED in the "stable/random" direction

The previous-session pickup hint #1 was *a question*, not a hypothesis:
"Test the '$\rho_h$ uniformly small' hypothesis quantitatively: is $\rho_h \to 0$
with $N$, or stable, or random?"

**Answer (resolved by this data):** stable/random, *not* $\to 0$.

- $h=100$ trajectory: $\rho_{100}(N) \in \{2.11, 0.62, 0.85, 0.026, 0.064\}$
  across $N \in \{10^6, 3 \cdot 10^6, 10^7, 2 \cdot 10^7, 3 \cdot 10^7\}$ —
  bounces non-monotonically, no descent toward $0$.
- Horizontal scan at $N = 10^7$: $\rho_h$ ranges from $5 \cdot 10^{-7}$ (at
  $h=50$) to $3.39$ (at $h=1000$); spread $> 6$ orders of magnitude.
- $h=50$ outlier verified as a zero-crossing, not a bug:
  $H_{50}(8\cdot 10^6) = -963$, $H_{50}(9\cdot 10^6) = -581$,
  $H_{50}(10^7) = -2.9$ — the partial sum continuously decays through zero
  near $N = 10^7$. Confirms random-walk-like behavior.

`P12-Halasz-Dh-diagonal.md` §7 already preferred the "CLT-fluctuation, mean 1
with large variance" reading; this session resolves the open
question in that prior preference's favor.

### 2.2 The weaker "$\rho_h = O(1)$ uniformly" hypothesis remains consistent with data

Across 42 tested points, $\rho_h(N) \le 3.4$. No trajectory shows
$\rho_h$ growing with $N$. The $h=100$ trajectory specifically
peaked at the smallest $N$ tested, then dropped by a factor of $\sim 30$.

This is the strategically-relevant hypothesis: **$\rho_h = O(1)$ uniformly
$\iff |H_h(N)| \le C \sqrt{C_h N} \le C' \sqrt{N}$ uniformly, which is the
$\sqrt{N}$ rate the P12 program needs.**

**Caveat (skeptic-flagged):** 1.5 decades of $N$ ($10^6$ to $3 \cdot 10^7$) and
$h$ up to $10^4$ are far too thin to *establish* $\rho_h = O(1)$ uniformly.
A logarithmic drift $\rho_h \asymp \log\log N$ uniform in $h$ would also be
consistent with this data and would correspond to $|H_h| \asymp \sqrt{N \log\log N}$
— i.e., a Halász-type loss. The data merely **fails to refute** $\rho_h = O(1)$.

### 2.3 The empirical mean $\bar\rho < 1$ points to NEGATIVE off-diagonal correlation

Under the iid model "$\widetilde S_h(e)$ has zero mean and per-element variance
$C_h$" we have *exactly* $E[H_h(N)^2] = D_h(N)$, hence $E[\rho_h] = 1$ by
linearity (zero off-diagonal expectation). The 16 horizontal-scan
$\rho_h(10^7)$ values give

$$
\bar\rho_{10^7} = \frac{1}{16}\sum_{h \in \mathrm{grid}} \rho_h(10^7) \approx 0.553,
\qquad
\mathrm{median}(\rho_h(10^7)) \approx 0.056.
$$

If $\rho_h$ were chi-sq(1) (the iid limit), expected mean is $1$, expected
median is $\approx 0.455$. Empirical mean is $\approx 0.55$ of prediction;
empirical median is $\approx 0.12$ of prediction.

**Implication: the iid model under-fits in the direction of *additional*
cancellation, not extra noise.** I.e., on the tested grid the cross-pair
sum $H_h(N)^2 - D_h(N) = \sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde
S_h(e_2)$ is *systematically negative* on average over $h$, by a factor of
roughly $1 - \bar\rho \approx 0.45$ relative to $D_h$.

This is the **same** sign and order of magnitude found in
`P12-Halasz-h-averaged.md` (six exact $R(N, H) := \sum_{h=1}^H |H_h|^2 /
\sum_{h=1}^H D_h$ values, all $< 1$, decreasing in $N$). The new contribution
of this session is to confirm the negative off-diagonal across a denser $h$-grid
at fixed $N$, not just the average over $h \in [1, H]$.

**Cosmetic warning:** the "Rayleigh-square" framing in an earlier draft of
this section was wrong — Rayleigh-square has mean 2, not 1. The correct iid
limit for $\rho_h = H_h^2 / D_h$ when $H_h$ is approximately mean-zero
Gaussian is $\chi^2_1$ (mean 1, median $\approx 0.455$). Section corrected.

## 3. Strategic implications

**On the tested 42-point grid.** $|H_h(N)| \le 1.4 \sqrt N$ across $h \in
\{1, \ldots, 10^4\}$, $N \in \{10^6, \ldots, 3 \cdot 10^7\}$. This extends
prev session's range (23 points up to $h=1000, N=10^7$) to 42 points up to
$h = 10^4, N = 3 \cdot 10^7$. **Not** an asymptotic statement; the data is
consistent with $|H_h| \ll \sqrt{N}$ but does not separate it from
$|H_h| \ll \sqrt{N (\log\log N)^c}$.

**Resolved (in the "stable/random" direction).** Prev-session question
"is $\rho_h \to 0$ with $N$?". The trajectory $h=100$ alone refutes the
$\to 0$ reading: $\rho_{100}(10^6) = 2.11$, then bounces.

**Re-confirmed, not new.** The strategic upshot — that the relevant analytic
target is bounding $\sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde S_h(e_2) = H_h^2 - D_h$
(equivalently the off-diagonal in the second moment) — is already the framework
of `P12-Halasz-Dh-diagonal.md` §7, `P12-Halasz-h-averaged.md`, and the
spectral-no-peak finding of `P12-Halasz-Phi-d-spectrum.md`. This session's
contribution to the strategic picture is the new empirical observation in §2.3
that the cross-pair sum is **negative on average over $h$ at fixed $N$**, with
the same sign and rough magnitude as the $h$-averaged finding.

The cleanest analytic handle remains the $h$-averaged off-diagonal of
`P12-Halasz-h-averaged.md`. The new evidence here points in the same direction.

## 4. Caveats

1. **42 data points, not asymptotic.** The "$\rho_h = O(1)$" reading
   could fail at $N \gg 3 \cdot 10^7$ or $h \gg 10^4$. Computation cost is
   $O(N \log\log N \cdot |h_{\mathrm{list}}|)$ in this Python code (the
   inner $h$-loop multiplies the sieve cost), so $N = 10^8$ at a few $h$ is
   a single-session reach (~5 min compute) but a wide-$h$ scan at $N = 10^9$
   is a separate engineering project.

2. **No rigorous content.** Findings are descriptive of the tested grid.
   The closed form $D_h(N) \sim C_h N$ is rigorous (prev session); the
   $\rho_h$ behavior is not.

3. **$h = 100$ trajectory is suggestive but not proof of bounded oscillation.**
   Five $N$-values is not enough to rule out a slow secular drift such as
   $\rho_h \asymp \log\log N$.

4. **§2.3 inference depends on the iid null model.** "Empirical mean
   $\bar\rho < 1 \implies$ negative off-diagonal" is rigorous *given*
   $\widetilde S_h(e)$ has zero mean and per-element variance $C_h$ — both
   true (the first by the same Weyl-equidistribution input, the second by
   the closed-form $D_h \sim C_h N$). What is not rigorous is the assumption
   that the $h$-grid sample of size 16 is representative of $\rho_h$ as a
   distribution; the median 0.06 vs predicted 0.45 gap is striking but a
   biased $h$-sample (e.g. low-$h$ overrepresented) could explain it.

## 5. Files

- `bot/scratch/Halasz-rho-broad.py` (new): broad $(N, h)$ scan, intermediate-$N$
  snapshots from a single sieve.
- Builds on: `P12-Halasz-Hh-empirical.md` (23-point $H_h$ table; this session
  adds 19 more), `P12-Halasz-Dh-diagonal.md` (closed form $D_h \sim C_h N$),
  `P12-Halasz-h-averaged.md` (off-diagonal $\sum_{h=1}^H |H_h|^2 < \sum_{h=1}^H D_h$),
  `P12-Halasz-Phi-d-spectrum.md` (no spectral peak in $\widetilde S_h$).
