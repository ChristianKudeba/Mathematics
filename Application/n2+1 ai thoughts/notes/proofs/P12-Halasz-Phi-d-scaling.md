# P12 Halász: cumulative autocorrelation profile under $N$-scaling

**Status:** Empirical (single-session scan). Three $N$ values, two $h$ values.

## 0. Setup recap

Continuing from `P12-Halasz-Phi-d-autocorr.md`. We work with the
multiplicative root-weight sum on squarefree-good integers:
$$
\widetilde S_h(e) := \mathbb 1[e \text{ sf-good}] \prod_{p \mid e} 2\cos\!\Big(\tfrac{2\pi h\,
\alpha_p (e/p)^{-1}_p}{p}\Big),
$$
with $\alpha_p$ a fixed root of $x^2 \equiv -1 \pmod p$ at split $p$, and
$\widetilde S_h(2^a) = (-1)^h \cdot \mathbb 1[a = 1]$.  Cumulative
auto-correlation:
$$
\Psi_h(d) := \sum_{e=2}^{N-d} \widetilde S_h(e)\,\widetilde S_h(e+d),
\qquad
C_h(D) := \sum_{d=1}^{D} \Psi_h(d).
$$
Identity $(\star)$ from prev session: $|H_h(N)|^2 - D_h(N) = 2 \sum_{d=1}^{N-2}
\Psi_h(d) =: 2 T_h(N)$.

This session asks: **does the off-diagonal mass $T_h$ live on a fixed
absolute $d$-scale, or scale with $N$?**

## 1. Setup of the scan

Compute $\Psi_h(d)$ via FFT autocorrelation (full $d$-spectrum at
$O(N \log N)$ cost), then $C_h(D)$ at the cumulative grid
$D \in \{10, 10^2, 10^3, 10^4, 10^5, N/100, N/10, N/3, N-2\}$ for
$N \in \{10^5, 10^6, 3 \cdot 10^6\}$ and $h \in \{1, 5\}$.  Total compute
$\sim 10$ s.

For each $(N, h)$: $D^*_q(N, h) := $ smallest $D \ge 1$ such that
$|C_h(D)/T_h| \ge q$, $q \in \{0.25, 0.50, 0.75\}$.

Identity $(\star)$ verified: $|2 \sum_{d=1}^{N-2} \Psi_h(d) - (|H_h|^2 -
D_h)| / \max(\cdot, 1) \le 5 \cdot 10^{-16}$ at all 6 data points
(numerical FFT precision).

Code: `bot/scratch/Halasz-Phi-d-scaling.py`.

## 2. Threshold table

| $N$ | $h$ | $H_h$ | $D_h$ | $T_h$ | $D^*_{25}$ | $D^*_{50}$ | $D^*_{75}$ | $D^*_{50}/N$ |
|---|---|---|---|---|---|---|---|---|
| $10^5$ | $1$ | $4.5$ | $39\,324$ | $-19\,652$ | $755$ | $2\,701$ | $3\,828$ | $0.0270$ |
| $10^5$ | $5$ | $-112.8$ | $54\,005$ | $-20\,637$ | $1\,176$ | $1\,376$ | $1\,888$ | $0.0138$ |
| $10^6$ | $1$ | $-53.3$ | $394\,170$ | $-195\,666$ | $2\,007$ | $12\,928$ | $33\,629$ | $0.01293$ |
| $10^6$ | $5$ | $-26.4$ | $543\,912$ | $-271\,607$ | $1\,569$ | $11\,215$ | $17\,071$ | $0.01121$ |
| $3 \cdot 10^6$ | $1$ | $-123.3$ | $1.179 \cdot 10^6$ | $-581\,774$ | $5\,896$ | $39\,295$ | $61\,075$ | $0.01310$ |
| $3 \cdot 10^6$ | $5$ | $-353.9$ | $1.628 \cdot 10^6$ | $-751\,614$ | $8\,247$ | $21\,680$ | $31\,989$ | $0.00723$ |

Notation: $T_h := \tfrac{1}{2}(|H_h|^2 - D_h) = \sum_{d=1}^{N-2} \Psi_h(d)$.

## 3. Three findings

### Finding 1 — $D^*$ neither $\Theta(N)$ nor $O(1)$

Empirically on this grid, $D^*_{50}/N$ **decreases** with $N$ but does
**not** decay to 0 fast.  $h=1$ values:
$0.0270 \to 0.01293 \to 0.01310$.
$h=5$ values: $0.0138 \to 0.01121 \to 0.00723$.

Log-log slopes $\log(D^*_{50}(N_2)/D^*_{50}(N_1)) / \log(N_2/N_1)$:

| $h$ | $N_1 \to N_2$ | slope |
|---|---|---|
| $1$ | $10^5 \to 10^6$ | $0.680$ |
| $1$ | $10^6 \to 3 \cdot 10^6$ | $1.013$ |
| $5$ | $10^5 \to 10^6$ | $0.911$ |
| $5$ | $10^6 \to 3 \cdot 10^6$ | $0.601$ |

**Interpretation (cautious).**  Three $N$-points yield two slope
estimates per $h$, and the four estimates $\{0.680, 1.013, 0.911,
0.601\}$ are non-monotone in $h$ and finite-size unstable.  What can
be honestly said:
- (b′) The "fixed absolute $d$-scale" hypothesis $D^*_{50} = O(1)$ as
  $N \to \infty$ is **refuted on this grid**: $D^*_{50}$ grows from
  $\sim 10^3$ at $N = 10^5$ to $\sim 4 \cdot 10^4$ at $N = 3 \cdot 10^6$.
- (a′) The "uniformly spread" hypothesis $D^*_{50}/N \to \mathrm{const}$
  is **NOT refuted**: at $h = 1$, $D^*_{50}/N$ goes
  $0.027 \to 0.013 \to 0.013$, plausibly approaching a constant; at
  $h = 5$, the trend is $0.014 \to 0.011 \to 0.007$, mildly down but
  with only 3 points cannot rule out a small positive limit.

The slope estimates are *consistent with* $D^* \sim N$ up to a slowly
varying factor, but **cannot pin a power**.  More $N$-points needed
(see §9).

### Finding 2 — Cumulative profile overshoots 1 (single strong instance + weaker echoes)

At $N = 3 \cdot 10^6$, $h = 1$: ratio $C_h(D)/T_h$ at $D \in
\{10^5, 3 \cdot 10^5, 10^6, N{-}2\}$ reads:
$$
0.727, \quad 1.241, \quad 0.917, \quad 1.000.
$$
Cumulative reaches $1.241$ near $D \approx N/10$, then descends to $1$
at $D = N - 2$.

If real, this means $\sum_{d \in (3 \cdot 10^5, 10^6]} \Psi_h(d) > 0$
at $(N, h) = (3 \cdot 10^6, 1)$, i.e. *positive*-aggregate
contribution on a particular dyadic-ish block.

Weaker analogues:
- $h = 5$, $N = 3 \cdot 10^6$: ratio $1.042$ at $D = 10^6$.
- $h = 5$, $N = 10^5$: ratio $1.250$ at $D = 10^4$, $1.226$ at $D \approx
  N/3$.

**Caveat (skeptic-flagged).**  Only **one** point overshoots strongly
($24\%$), at the largest $N$ tested.  With $\le 6$ data points and no
randomized-null comparison, this could be finite-size or
small-statistics noise rather than a structural feature.  The §3.2
"sign-pattern wave" hypothesis below is therefore *suggestive* on
this grid; a wider $N$-grid would test whether the overshoot grows,
saturates, or vanishes.

**Suggestive (not established).** *If* the pattern persists,
$T_h$ accumulates from a "negative wave" in $d \in [10^4, N/10]$
followed by a "positive correction wave" in $d \in [N/10, N]$ at the
larger $N$.  Worth probing with dyadic-block sums in a follow-up.

### Finding 3 — Short-$d$ cumulative sign-flips at large $N$

At $N = 3 \cdot 10^6$, $h = 1$:
$$
C_h(10) = -2073, \quad C_h(100) = +1073, \quad C_h(1000) = +5999,
$$
all small in *fraction* of $|T_h| = 581\,774$ ($|C_h(10^3)| / |T_h|
\approx 1.03\%$), and *positive*-cumulative through $d = 1000$.
Then $C_h(10^4) = -140\,683$ — flips sharply negative.

So at large $N$, the very-short-range $d \le 10^3$ contributes a small
*positive* increment ($\sim 1\%$ of $T_h$ in the cumulative); the
dominant negative contributions live in $d \in [10^4, 10^5]$ at
$N = 10^6$ and $d \in [10^4, 3 \cdot 10^5]$ at $N = 3 \cdot 10^6$.

This is consistent with prev session's $h = 20$ "crosses zero twice"
observation, now appearing at generic $h$ at sufficiently large $N$.

## 4. Cross-check with prev session

Prev session at $N = 10^6$ reported (rounded to 3 digits):

| $D$ | $h{=}1$ | $h{=}5$ |
|---:|---:|---:|
| $10$ | $0.010$ | $0.014$ |
| $100$ | $0.024$ | $0.035$ |
| $10^3$ | $0.052$ | $0.148$ |
| $10^4$ | $0.383$ | $0.465$ |
| $10^5$ | $0.770$ | $0.802$ |

This session at $N = 10^6$ reports $0.01042, 0.02416, 0.05171,
0.38277, 0.76975$ ($h=1$) and $0.01369, 0.03506, 0.14787, 0.46530,
0.80178$ ($h=5$).  Each pair matches to $\le 5 \cdot 10^{-4}$
(within the rounding of the prev session's display).

## 5. Empirical $|H_h|/\sqrt N$ tracking

| $N$ | $h$ | $|H_h|$ | $|H_h|/\sqrt N$ | $|H_h|^2/D_h$ |
|---|---|---|---|---|
| $10^5$ | $1$ | $4.5$ | $0.014$ | $5 \cdot 10^{-7}$ |
| $10^5$ | $5$ | $112.8$ | $0.357$ | $0.236$ |
| $10^6$ | $1$ | $53.3$ | $0.053$ | $7 \cdot 10^{-3}$ |
| $10^6$ | $5$ | $26.4$ | $0.026$ | $1.3 \cdot 10^{-3}$ |
| $3 \cdot 10^6$ | $1$ | $123.3$ | $0.071$ | $1.3 \cdot 10^{-2}$ |
| $3 \cdot 10^6$ | $5$ | $353.9$ | $0.204$ | $0.077$ |

$|H_h|/\sqrt N$ varies non-monotonically across the 6 points
($0.014, 0.357, 0.053, 0.026, 0.071, 0.204$); $|H_h|^2/D_h$ is $\le
0.236$ across the table, with 4 of 6 points $\le 0.013$ and the
largest value at the smallest-$N$ outlier $(10^5, 5)$.

**Honest reading.** The diagonal-CLT *one-step* prediction $|H_h|^2
\approx D_h$ (i.e. $|H_h|^2/D_h \approx 1$) is **inconsistent with
the data on this 6-point grid** — most points show order-of-magnitude
suppression.  Whether $|H_h|^2/D_h \to 0$ or stabilizes at some small
positive value cannot be decided from 6 points; the trend in $N$ is
non-monotone in either $h$.

## 6. Rigor accounting

**Rigorous (not new — from prev sessions):**
- Lemma 2.1 ($\Psi_h(d) = 0$ for $d \equiv 2 \pmod 4$).
- Identity $(\star)$: $|H_h|^2 - D_h = 2 \sum_{d=1}^{N-2} \Psi_h(d)$
  as a *theorem*.

**Numerical (this session, NOT new mathematics):** the FFT
implementation reproduces both sides of $(\star)$ to relative error
$\le 5 \cdot 10^{-16}$ at all 6 data points — this is a
floating-point sanity check, not a new theorem.

**Empirical (this session):**
- $D^*_{50}$ grows with $N$ (refutes "fixed absolute $d$" on the
  tested grid); $D^*_{50}/N$ trend is non-monotone in $h$ (does NOT
  refute "uniformly spread").
- Single strong cumulative overshoot to $1.241$ at $(N, h) =
  (3 \cdot 10^6, 1)$; weaker echoes elsewhere; return to $1.0$ at
  $D = N-2$.  Statistical robustness of overshoot is open.
- Short-$d$ cumulative sign-flip stable at $N \ge 10^6$.
- $|H_h(N)|^2/D_h \le 0.236$ across 6 points; trend in $N$
  non-monotone.

## 7. Strategic implications

1. **(Heuristic, not finding.)**  *If* $D^*_{50} \sim N^c$ for some
   $c < 1$, the heuristic Fourier-side mass-concentration scale would
   be $\xi \sim 1/D^*_{50} \sim N^{-c}$ — a low-frequency regime.
   This is *suggestive* of a mean-square-on-low-frequencies
   large-sieve setup, but $D^*_{50}$ does not pin Fourier support;
   the inference is heuristic and would need direct
   $|\widehat{\widetilde S_h}(\xi)|^2$ data to confirm (pickup hint
   #2 from prev session).

2. **Signed off-diagonal structure (suggestive, single instance).**
   *If* §3.2's overshoot generalizes, $T_h$ accumulates from a
   "negative wave" then a "positive correction wave" at separated
   $d$-scales.  A one-sided bound would not suffice.  This is one
   data point — needs a wider $N$-grid to test.

3. **Diagonal-CLT one-step prediction is empirically inconsistent
   with data on this grid.**  The simplest model — $H_h$ as a sum of
   independent mean-zero contributions — predicts $|H_h|^2/D_h
   \approx 1$.  Observed $|H_h|^2/D_h \le 0.236$ across 6 points,
   with 4 of 6 $\le 0.013$.  This is order-of-magnitude suppression,
   *not* a "power factor" claim (which would require fitting an
   exponent the data cannot pin).  The mechanism is via the
   negative-aggregate $T_h$ documented in §3.2.

## 8. Caveats

1. **Three $N$-points only.**  The $D^*$ scaling and the overshoot are
   one-decade-and-a-half observations, not asymptotically pinned.

2. **Two $h$-values only.**  $h=1$ and $h=5$.  Larger $h$ untested in
   this session.

3. **Overshoot.**  At $h = 1$, $N = 10^5$, no overshoot — cumulative
   monotone-ish.  At $h = 1$, $N = 3 \cdot 10^6$, overshoot of $24\%$.
   The overshoot magnitude scales with $N$; whether it grows
   unboundedly or saturates is untested.

4. **Sublinear $D^*$ doesn't imply low-frequency dominance** rigorously
   — the median threshold differs from the spectral support.  The §7.1
   inference is a heuristic, not a proof.

## 9. Open follow-up questions

- Does $D^*_{50}(N, h)/N$ continue decreasing past $N = 10^7$?
- Does the overshoot saturate, or does $\max_D |C_h(D)/T_h|$ grow?
- Does $|H_h(N)|^2/D_h$ continue decreasing, suggesting power-saving
  cancellation in $H_h$ itself?
- Per-dyadic-block sign and magnitude of $\sum_{d \in [D, 2D]}
  \Psi_h(d)$ — direct empirical access to the Fourier-side dyadic
  decomposition.

## Files

- `bot/scratch/Halasz-Phi-d-scaling.py` (new): multi-$N$ scaling at
  $N \in \{10^5, 10^6, 3 \cdot 10^6\}$, $h \in \{1, 5\}$.
- Builds on `bot/scratch/Halasz-Phi-d-extended.py`.
- Predecessor proof note: `P12-Halasz-Phi-d-autocorr.md`.
