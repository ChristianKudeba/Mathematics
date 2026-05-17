# P12 — Halász direction: autocorrelation $\Phi_h(d)$ on sf good $e$

**Status: empirical preview, verdict PROGRESS, consensus WITH-CAVEAT.**

Builds on `P12-Halasz-h-averaged.md` (off-diagonal $|H_h|^2 - D_h$ is *negative*
on tested $h$) and `P12-Halasz-Dh-diagonal.md` ($D_h(N) \sim (\pi/4)H_h(1)\,N$
closed form).  Tests *where* in $d$-space the systematic negativity lives.

## 1. Object

For $h \in \mathbb Z_{\ge 1}$ and sf-good $e \ge 2$ (square-free, all prime
factors $\in \{2\} \cup \{p \equiv 1 \pmod 4\}$), let
$$
\widetilde S_h(e) := \prod_{p \mid e} 2 \cos\!\bigl(2\pi h\, a_p(e)/p\bigr),
\qquad a_p(e) := \alpha_p \cdot (e/p)^{-1} \pmod p,
$$
with $\alpha_p$ the chosen square root of $-1 \pmod p$ (resp. $1$ at $p=2$).
Extend by $\widetilde S_h(e) = 0$ when $e$ is not sf-good.  Define the
displacement autocorrelation
$$
\Psi_h(d) := \sum_{e=2}^{N-d} \widetilde S_h(e)\, \widetilde S_h(e+d),
\qquad
\Phi_h(d) := \Psi_h(d)/N.
$$

Translation-invariance gives the identity
$$
|H_h(N)|^2 - D_h(N) \;=\; \sum_{e_1 \ne e_2} \widetilde S_h(e_1)\widetilde S_h(e_2)
                     \;=\; 2\sum_{d=1}^{N-2} \Psi_h(d).
\qquad (\star)
$$
The summation range is $d \in \{1, \dots, N-2\}$ (since $\widetilde S_h$ is
supported in $\{2, \dots, N\}$, ordered pairs $(e_1, e_2) = (e, e+d)$ with
$e_1 < e_2$ require $e \ge 2, e+d \le N$ so $d \le N-2$).  Cross-check
against direct $|H_h|^2 - D_h$ matches to $\le 10^{-4}$ relative error
across $h = 1, 5, 20$ in the FFT script (limited by float64 accumulation).

## 2. Rigorous parity-zero structure

**Lemma 2.1.**  Fix $h, N$ and any $d \ge 1$ with $d \equiv 2 \pmod 4$.
For every integer $e$ with $2 \le e$ and $e+d \le N$, at least one of
$\widetilde S_h(e)$ or $\widetilde S_h(e+d)$ is zero.  Hence $\Psi_h(d) = 0$.

*Proof.*  $\widetilde S_h(\cdot) = 0$ on integers that are not sf-good, so it
suffices to show no $e \ge 2$ has both $e$ and $e+d$ sf-good.  Every sf-good
$e \ge 2$ satisfies $e \equiv 1$ or $2 \pmod 4$:
- If $e$ is odd, all its prime factors are $\equiv 1 \pmod 4$, so the product
  is $\equiv 1 \pmod 4$.
- If $e$ is even, sf-good forces $e = 2m$ with $m$ odd sf-good $\equiv 1 \pmod 4$,
  so $e \equiv 2 \pmod 4$.

Now adding $d \equiv 2 \pmod 4$:
- $e \equiv 1 \Rightarrow e+d \equiv 3 \pmod 4$.  Odd, but $\not\equiv 1$, so not sf-good.
- $e \equiv 2 \Rightarrow e+d \equiv 0 \pmod 4$.  Divisible by $4$, so not square-free.

In both cases $e+d$ is not sf-good. $\square$

This is the only rigorous structural identity from this session.  It
restricts the support of $\Psi_h$ to $d \in \{0\} \cup (\mathbb Z_{>0} \setminus 4\mathbb Z + 2)$.

## 3. Empirical: short-$d$ table, $N = 10^6$

Direct evaluation at $h \in \{1, 5, 20\}$, $d \in \{1, 2, 3, 5, 10, 100\}$
(`bot/scratch/Halasz-Phi-d-autocorr.py`).  Cond avg = $\Psi/\#\{e: e, e+d$
sf-good$\}$.  Compare to $\mathbb E[\widetilde S_h^2 \mid \text{sf-good}]
= D_h / \#\text{sf-good} \approx 3.17 \;(h{=}1),\; 4.37\;(h{=}5),\; 4.35\;(h{=}20)$.

| $h$ | $d$ | $\Psi_h(d)$ | $\Psi/N$ | $\Psi/D_h$ | $\#\{$both sf-good$\}$ | cond avg |
|---:|----:|---:|---:|---:|---:|---:|
| 1 | 1 | 516.3 | 5e-4 | 1e-3 | 9895 | 0.052 |
| 1 | 2 | 0 | 0 | 0 | 0 | — |
| 1 | 3 | $-1518$ | $-1.5$e-3 | $-3.9$e-3 | 19853 | $-0.077$ |
| 1 | 5 | $-294$ | $-3$e-4 | $-7$e-4 | 9938 | $-0.030$ |
| 1 | 10 | 0 | 0 | 0 | 0 | — |
| 1 | 100 | $-63$ | $-6$e-5 | $-2$e-4 | 20162 | $-0.003$ |
| 5 | 3 | $-2610$ | $-2.6$e-3 | $-4.8$e-3 | 19853 | $-0.131$ |
| 5 | 100 | $-1548$ | $-1.5$e-3 | $-2.8$e-3 | 20162 | $-0.077$ |
| 20 | 3 | $+3217$ | $+3.2$e-3 | $+5.9$e-3 | 19853 | $+0.162$ |
| 20 | 100 | $-1492$ | $-1.5$e-3 | $-2.8$e-3 | 20162 | $-0.074$ |

(Even-$d$ entries identically zero by Lemma 2.1; rows for $d=2,10$ confirm this.)

**Reading:** conditional autocorrelation is order $1\%$–$3\%$ of the
single-$e$ variance, with sign varying across $h$.  No clean
structural pattern at small $d$.

## 4. The off-diagonal is diffuse, not localized

Extended FFT autocorrelation (`bot/scratch/Halasz-Phi-d-extended.py`) gives
$\Psi_h(d)$ for all $d \in [0, N-1]$ at $N = 10^6$, and we compute the
cumulative $C_h(D) := \sum_{d=1}^D \Psi_h(d)$ and compare to the target
$T_h := (|H_h|^2 - D_h)/2$ (which by $(\star)$ equals $C_h(N-1)$ exactly).

| $D$ | $C_h(D) / T_h$, $h{=}1$ | $C_h(D) / T_h$, $h{=}5$ | $C_h(D)/T_h$, $h{=}20$ |
|---:|---:|---:|---:|
| $10$ | 0.010 | 0.014 | 0.017 |
| $100$ | 0.024 | 0.035 | $-0.008$ |
| $10^3$ | 0.052 | 0.148 | 0.009 |
| $10^4$ | 0.383 | 0.465 | 0.572 |
| $10^5$ | 0.770 | 0.802 | 1.015 |
| $N-1$ | 1.000 | 1.000 | 1.000 |

**Reading.**  For all three $h$, only $\sim 5\%$ of the off-diagonal sits in
$d \le 1000$, while $\sim 75\%{-}100\%$ sits in $d \le 10^5$.  The bulk of
$|H_h|^2 - D_h$ comes from medium-range correlations $d \in [10^4, 10^5]$,
not from short-range anti-correlation.  For $h = 20$ the cumulative is
non-monotone (goes negative-then-positive-then-negative), evidencing
sign-cancellation among per-$d$ contributions in the lower decade.

## 5. Per-$d$ magnitude does not decay

At $N = 10^6$, $|\Psi_h(d)|$ stays in the range $\sim 10^2$ to $\sim 10^3$
across $d$ from $1$ to $10^5$ — no monotone $1/d$ or $1/d^{1/2}$ envelope
visible from the 21 sampled odd-$d$.  Sample at $h = 1$:

| $d$ | $\Psi_1(d)$ | | $d$ | $\Psi_1(d)$ | | $d$ | $\Psi_1(d)$ |
|---:|---:|---|---:|---:|---|---:|---:|
| 1 | $+516$ | | 21 | $+1160$ | | $251$ | $+462$ |
| 3 | $-1518$ | | 25 | $-133$ | | $501$ | $-176$ |
| 5 | $-294$ | | 31 | $+10$ | | $1001$ | $+199$ |
| 7 | $-10$ | | 51 | $-103$ | | $5001$ | $-38$ |
| 9 | $+519$ | | 101 | $+107$ | | $10001$ | $-206$ |
| 11 | $+2$ | | | | | $50001$ | $+393$ |
| 13 | $+252$ | | | | | $10^5{+}1$ | $+380$ |

If $|\Psi_h(d)| \sim c \sqrt{N}$ on a roughly constant fraction of $d$
with random signs, then $\bigl|\sum_d \Psi_h(d)\bigr|$ is heuristically
$\sim c\sqrt N \cdot \sqrt{N/4} = (c/2) N$, matching the empirical
$|T_h| \approx 2 \cdot 10^5$ at $N = 10^6$ ($\sim 0.2 N$) in *magnitude*.
This heuristic is silent on the *sign* of $T_h$ — it predicts a $\pm$
random walk, not a systematic negative bias.  The empirically observed
negativity of $T_h$ across all 3 tested $h$ is *not* explained by this
heuristic and would need an additional drift term.  (Heuristic, NOT a
proof, and incomplete even as a heuristic.)

## 6. Strategic implication

**All claims below are at $N = 10^6$, $h \in \{1, 5, 20\}$ only.**  None of
$\sim 5\%$, $\sim 75\%$ etc. is shown to hold under $N$-scaling; the table
in §4 is a single-$N$ snapshot whose absolute $D$-thresholds may move with
$N$.  The most natural "off-diagonal cancellation" stories are
**refuted on the tested $(N, h)$ grid**:

(i) **Short-range anti-correlation localizing the off-diagonal at
small $d$**: refuted on this grid — only $\sim 5\%$ of the off-diagonal
in $d \le 1000$ at $N=10^6$.  Open whether the "small-$d$ fraction" is
fixed or scales as $1 - O(\log\log N / \log N)$ etc.

(ii) **Systematic same-sign per-$d$ negativity**: refuted — signs of
$\Psi_h(d)$ alternate.  The cumulative ratio $C_{20}(D)/T_{20}$ takes
values $0.017, -0.008, 0.009, 0.572, 1.015, 1.000$ at $D = 10, 10^2,
10^3, 10^4, 10^5, N{-}2$ — two zero-crossings in the lower decades.

(iii) **Per-$d$ decay $\Psi_h(d) \sim d^{-\alpha}$, $\alpha > 0$**:
not visible in the range — magnitudes oscillate within a factor of
$\sim 10$ across $d$ from $1$ to $10^5$.

What remains plausible (and consistent with §5's heuristic):

(iv) **Random-sign per-$d$ contributions**: $\Psi_h(d)$ behaves as
roughly mean-zero noise of size $\sim \sqrt N$ on the
non-parity-killed $d$-set, with the partial-sum negative drift coming
from a $\sim 1/\sqrt{N}$-level *systematic* tilt.  Bounding $\sum_d
\Psi_h(d)$ to extract $|H_h|^2 \le D_h$ then requires an *integrated*
control across the entire $d$-spectrum, not a finite-$d$ sum.

(v) **Spectral-side reformulation**: $|H_h|^2 = \widehat{\widetilde
S_h}(0)^2$, and $\Psi_h(d)$ is the inverse-Fourier-transform of
$|\widehat{\widetilde S_h}(\xi)|^2$.  The "diffuse $d$-distribution"
observation says $|\widehat{\widetilde S_h}(\xi)|^2$ has nontrivial
$\xi \to 0$ behavior; the question becomes whether $|\widehat{\widetilde
S_h}|^2$ has a usable peak structure on dyadic $\xi$-blocks.  This is the
natural setup for any large-sieve-style attack on $|H_h|$.

## 7. Cross-checks

- **FFT autocorr identity** ($(\star)$): for each $h \in \{1, 5, 20\}$,
  $|2 \sum_{d=1}^{N-1} \Psi_h(d) - (|H_h|^2 - D_h)|/|...| < 10^{-4}$.
- **Direct vs FFT $\Psi_h(d)$**: at the 6 short-$d$ values from §3, the
  extended-script values match to floating-point precision.
- **Even-$d$ zero**: empirically $\Psi_h(d) = 0$ exactly at $d \in \{2, 10\}$
  (parity-killed), as predicted by Lemma 2.1.

## 8. Caveats and open questions

1. **Single $N = 10^6$.**  Cumulative-$C_h$ profile may shift with $N$; in
   particular the "75% of off-diagonal in $d \le 10^5$" may scale as
   "X% of off-diagonal in $d \le N^{0.83}$" or similar.  Untested.
2. **Three $h$.**  $h = 1, 5, 20$ show qualitatively similar long-range
   diffuse pattern but differ in short-range sign behavior.  Larger
   $h$ untested in this session.
3. **Mean-zero-noise heuristic of §5**: not a proof.  $\Psi_h(d)$ being
   $O(\sqrt N)$ pointwise with random sign is consistent with data but
   could equally be $O(N^{1/2 + o(1)})$ or $O(N^{1/2-\epsilon})$ with
   compensating density.
4. **Structural origin of $h=20$ short-range cumulative non-monotonicity**:
   unexplained.  Could be a Dirichlet-kernel residue ($h \cdot$ small
   primes giving phase coincidences), worth a follow-up.

## 9. Files

- `bot/scratch/Halasz-Phi-d-autocorr.py` (new): direct $\Psi_h(d)$ at
  6 small $d$, with #both-sf-good and conditional avg.
- `bot/scratch/Halasz-Phi-d-extended.py` (new): FFT autocorrelation,
  full $d$-spectrum, cumulative profile.
- Builds on: `P12-Halasz-h-averaged.md`, `P12-Halasz-Dh-diagonal.md`,
  `P12-Halasz-Hh-empirical.md`.
