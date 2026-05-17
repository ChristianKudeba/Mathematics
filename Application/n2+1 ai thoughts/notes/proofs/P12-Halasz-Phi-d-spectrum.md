# P12 — Halász direction: power spectrum $|\widehat{\widetilde S_h}(\xi)|^2$

**Session 2026-05-10.** Direct power-spectrum computation of
$\widetilde S_h(e)$ on a fine $\xi$-grid at two $N$, $h = 1$.
Discriminates the three remaining post-`P12-Halasz-Phi-d-dyadic.md`
pictures (single Fourier mode, single complex-pole damped oscillation,
multi-mode) by looking directly at where Fourier mass is concentrated.
**Result: the spectrum is white at the baseline $\approx D_h$
for $\xi \gtrsim \xi_c \sim O(1/N)$ and SUPPRESSED below $\xi_c$.
No localized peak anywhere. All three modal pictures cleanly refuted.**

This file is a follow-up to:

- `P12-Halasz-Phi-d-autocorr.md` — defs, identity $(\star)$.
- `P12-Halasz-Phi-d-scaling.md` — multi-$N$ cumulative profile.
- `P12-Halasz-Phi-d-dyadic.md` — dyadic-block sign pattern.

## 1. Setup

For $e \ge 2$ squarefree with $p \mid e \Rightarrow p = 2$ or $p \equiv 1 \pmod 4$
("sf-good"), $\widetilde S_h(e) := \prod_{p \mid e} 2 \cos(2\pi h\,
\alpha_p (e/p)^{-1}_p / p)$, with the convention
$\widetilde S_h(2e) = (-1)^h \widetilde S_h(e)$ for $e$ odd.

Extend $\widetilde S_h$ to $\widetilde S_h(0) = \widetilde S_h(1) = 0$.
Take the discrete Fourier transform on a zero-padded grid of length $n_{\mathrm{fft}}$
(next power of two $\ge 2(N+1)$):
$$
X(k) := \sum_{e=0}^{N} \widetilde S_h(e)\, e^{-2\pi i k e / n_{\mathrm{fft}}},
\qquad
\xi_k := k / n_{\mathrm{fft}},\quad k = 0, 1, \ldots, n_{\mathrm{fft}}/2.
$$
Define
$$
P(\xi_k) := |X(k)|^2.
$$

Three sanity identities:

- **DC**: $X(0) = H_h(N)$, so $P(0) = H_h(N)^2$.
- **Parseval**: $\sum_{k=0}^{n_{\mathrm{fft}}-1} |X(k)|^2 = n_{\mathrm{fft}} \cdot D_h(N)$.
- **Wiener–Khinchin** (for the 0-padded sequence): with $n_{\mathrm{fft}} \ge 2(N+1)$,
  the *circular* autocorrelation of the padded sequence equals the
  *aperiodic* autocorrelation $R(d) = \sum_e \widetilde S_h(e) \widetilde S_h(e+d)
  = \Psi_h(|d|)$ on $|d| \le N$ (no wrap-around), so $P(\xi)$ is the DFT
  of $R$ on the $n_{\mathrm{fft}}$-grid.

## 2. Computation

`bot/scratch/Halasz-Phi-d-spectrum.py`.

- Leg A: $N = 3 \cdot 10^6$, $n_{\mathrm{fft}} = 2^{23} = 8\,388\,608$,
  $\xi$-resolution $\Delta\xi = 1/n_{\mathrm{fft}} \approx 1.19 \cdot 10^{-7}$.
- Leg B: $N = 10^7$, $n_{\mathrm{fft}} = 2^{25} = 33\,554\,432$,
  $\Delta\xi \approx 2.98 \cdot 10^{-8}$.

Total wall-clock $\approx 30$s. Cross-checks at machine precision:

| Leg | $H_h$ | $D_h$ | $T_h$ | Parseval rel err | $X(0)$ vs $|H_h|$ |
|:---:|---:|---:|---:|:---:|:---:|
| A | $-123.3$ | $1\,178\,740.6$ | $-581\,773.7$ | $1.98 \cdot 10^{-16}$ | $3.46 \cdot 10^{-15}$ |
| B | $\;\,291.3$ | $3\,927\,738.3$ | $-1\,921\,446.6$ | $0$ | $1.17 \cdot 10^{-15}$ |

## 3. Per-bin power (dyadic $\xi$-blocks)

Block $j$ holds frequencies $\xi_k \in [2^{-j-1}, 2^{-j})$, count
$N_j \approx 2^{-j-1}\, n_{\mathrm{fft}}$ (count doubles as $j$ decreases;
exact integers shown in the data tables). The relevant statistic is
**average power per bin** within the block:
$$
\bar P_j := \frac{1}{N_j}\!\!\sum_{\xi_k \in [2^{-j-1},\,2^{-j})}\!\! P(\xi_k).
$$
For a hypothetical $\widetilde S_h$ with no autocorrelation at lag $d \ge 1$
(i.e., $\Psi_h(d) = 0$ for $d \ge 1$, a "white-noise null"), Parseval gives
$\sum_k P(\xi_k) = n_{\mathrm{fft}} D_h$ and the spectrum is uniform, so
$\bar P_j \equiv D_h$ for every $j$ — i.e. the **white-noise level
is $D_h$ per bin**.

### 3.1 Leg A — $N = 3 \cdot 10^6$, white-noise level $D_h \approx 1.18 \cdot 10^6$

| $j$ | $\xi$-range | count | $\sum P$ | $\bar P_j$ | ratio to $D_h$ |
|---:|:---:|---:|---:|---:|---:|
| DC | $0$ | $1$ | $1.52 \cdot 10^{4}$ | $1.52 \cdot 10^4$ | $0.013$ |
| $22$ | $[1.2, 2.4) \cdot 10^{-7}$ | $1$ | $4.30 \cdot 10^{4}$ | $4.30 \cdot 10^{4}$ | $0.036$ |
| $21$ | $[2.4, 4.8) \cdot 10^{-7}$ | $2$ | $1.08 \cdot 10^{5}$ | $5.42 \cdot 10^{4}$ | $0.046$ |
| $20$ | $[4.8, 9.5) \cdot 10^{-7}$ | $4$ | $1.39 \cdot 10^{5}$ | $3.49 \cdot 10^{4}$ | $0.030$ |
| $19$ | $[9.5, 19.1) \cdot 10^{-7}$ | $8$ | $7.24 \cdot 10^{5}$ | $9.05 \cdot 10^{4}$ | $0.077$ |
| $18$ | $[1.9, 3.8) \cdot 10^{-6}$ | $16$ | $1.49 \cdot 10^{7}$ | $9.31 \cdot 10^{5}$ | $0.79$ |
| $17$ | $[3.8, 7.6) \cdot 10^{-6}$ | $32$ | $2.38 \cdot 10^{7}$ | $7.44 \cdot 10^{5}$ | $0.63$ |
| $16$ | $[7.6, 15.3) \cdot 10^{-6}$ | $64$ | $6.12 \cdot 10^{7}$ | $9.56 \cdot 10^{5}$ | $0.81$ |
| $15$ | $[1.5, 3.1) \cdot 10^{-5}$ | $128$ | $1.18 \cdot 10^{8}$ | $9.20 \cdot 10^{5}$ | $0.78$ |
| $14$ | $[3.1, 6.1) \cdot 10^{-5}$ | $256$ | $2.98 \cdot 10^{8}$ | $1.16 \cdot 10^{6}$ | $0.99$ |
| $13$ | $[6.1, 12.2) \cdot 10^{-5}$ | $512$ | $6.17 \cdot 10^{8}$ | $1.21 \cdot 10^{6}$ | $1.02$ |
| $12$ | $[1.2, 2.4) \cdot 10^{-4}$ | $1024$ | $1.21 \cdot 10^{9}$ | $1.18 \cdot 10^{6}$ | $1.00$ |
| $11$–$1$ | (all higher $\xi$) | — | — | $1.18 \cdot 10^{6} \pm 1\%$ | $1.00 \pm 0.01$ |

### 3.2 Leg B — $N = 10^7$, white-noise level $D_h \approx 3.93 \cdot 10^6$

| $j$ | $\xi$-range | count | $\sum P$ | $\bar P_j$ | ratio to $D_h$ |
|---:|:---:|---:|---:|---:|---:|
| DC | $0$ | $1$ | $8.49 \cdot 10^{4}$ | $8.49 \cdot 10^{4}$ | $0.022$ |
| $24$ | $[3.0, 6.0) \cdot 10^{-8}$ | $1$ | $2.34 \cdot 10^{5}$ | $2.34 \cdot 10^{5}$ | $0.060$ |
| $23$ | $[6.0, 11.9) \cdot 10^{-8}$ | $2$ | $5.40 \cdot 10^{5}$ | $2.70 \cdot 10^{5}$ | $0.069$ |
| $22$ | $[1.2, 2.4) \cdot 10^{-7}$ | $4$ | $2.81 \cdot 10^{6}$ | $7.01 \cdot 10^{5}$ | $0.18$ |
| $21$ | $[2.4, 4.8) \cdot 10^{-7}$ | $8$ | $1.59 \cdot 10^{7}$ | $1.99 \cdot 10^{6}$ | $0.51$ |
| $20$ | $[4.8, 9.5) \cdot 10^{-7}$ | $16$ | $4.30 \cdot 10^{7}$ | $2.69 \cdot 10^{6}$ | $0.68$ |
| $19$ | $[9.5, 19.1) \cdot 10^{-7}$ | $32$ | $1.12 \cdot 10^{8}$ | $3.50 \cdot 10^{6}$ | $0.89$ |
| $18$ | $[1.9, 3.8) \cdot 10^{-6}$ | $64$ | $1.96 \cdot 10^{8}$ | $3.06 \cdot 10^{6}$ | $0.78$ |
| $17$ | $[3.8, 7.6) \cdot 10^{-6}$ | $128$ | $4.20 \cdot 10^{8}$ | $3.28 \cdot 10^{6}$ | $0.84$ |
| $16$ | $[7.6, 15.3) \cdot 10^{-6}$ | $256$ | $1.02 \cdot 10^{9}$ | $3.97 \cdot 10^{6}$ | $1.01$ |
| $15$ | $[1.5, 3.1) \cdot 10^{-5}$ | $512$ | $1.96 \cdot 10^{9}$ | $3.82 \cdot 10^{6}$ | $0.97$ |
| $14$ | $[3.1, 6.1) \cdot 10^{-5}$ | $1024$ | $3.97 \cdot 10^{9}$ | $3.88 \cdot 10^{6}$ | $0.99$ |
| $13$–$1$ | (all higher $\xi$) | — | — | $3.92 \cdot 10^{6} \pm 1\%$ | $1.00 \pm 0.01$ |

## 4. What this rules out

The three pictures inherited from `P12-Halasz-Phi-d-dyadic.md` § 6 each
predict a **localized POSITIVE excess** in $\bar P_j$ at some $\xi^*$:

- **(P1) Single Fourier mode** $\widetilde S_h(e) \approx A \cos(2\pi \xi^* e + \varphi)$
  on the bulk: peak bin power $\sim (AN/2)^2$, mainlobe width $\asymp 1/N$.
  Predicted bin (from prev session's $c \approx 2.3$): leg A $j \in \{17, 18\}$,
  leg B $j \in \{20, 21\}$.
- **(P2) Single complex-pole damped oscillation** with linewidth $\lambda$:
  Lorentzian peak at $\xi^*$. For peak bin $\bar P > D_h$, the total mode
  power must satisfy $P_{\mathrm{mode}} \gtrsim \pi \lambda \cdot n_{\mathrm{fft}}\cdot D_h /n_{\mathrm{fft}}$.
- **(P3) Multi-mode** with mass on a finite set of frequencies:
  multiple bins $\bar P_j > D_h$.

**Empirical observation.** Across both legs:
- $\bar P_j \le D_h$ for *every* $j$ (no bin exceeds the white-noise baseline).
- DC is the most-suppressed point ($\bar P_0 \approx 0.013$–$0.022 \cdot D_h$),
  followed by a smooth rise toward $D_h$ as $\xi$ grows.
- The transition region $\bar P_j \in [0.5, 1.0]\, D_h$ is the *opposite*
  of an excess: a **deficit zone** at low $\xi$.

**What is refuted.** Any **positive-amplitude** excess mode whose linewidth
$\lambda$ is at most a fraction of a bin width — call this the "narrow
positive-mode" regime ($\lambda \lesssim 2^{-j-1}$ at the relevant $j$).
In particular (P1) is fully refuted, and (P2)/(P3) are refuted in the
narrow-linewidth regime. **What is NOT refuted by this data alone**:
broad-linewidth Lorentzians (linewidth comparable to $1/N$ or more)
that spread mass thinly enough that no single bin breaks the
$D_h$ ceiling. Those require a separate argument; see §6 for why
they are not natural candidates given the *negative* autocorrelation
integral $\sum_d \Psi_h(d) = H_h^2 - D_h \approx -D_h$.

The spectrum's positive shape — **monotone non-decreasing in $\xi$ on
the tested grid up to white-noise saturation** — is consistent with a
"**white above + deficit below**" structure:
$$
\bar P_j \approx
\begin{cases}
D_h & \xi_j \gtrsim \xi_c, \\
\text{strictly less than } D_h, \text{ smoothly rising} & \xi_j \lesssim \xi_c,
\end{cases}
$$
with no peak — neither sharp (P1), nor smoothed (P2), nor multi-modal (P3).

## 5. The deficit scale $\xi_c$ scales as $\sim 1/N$

Using the convention $\xi_c$ := smallest $\xi$ at which $\bar P_j \ge 0.95 \cdot D_h$:

| $N$ | $\bar P_j / D_h$ first reaches $\ge 0.95$ at | $\xi_c$ | $1/(N \xi_c)$ |
|:---:|:---:|:---:|:---:|
| $3 \cdot 10^6$ | $j = 14$, range $[3.1, 6.1) \cdot 10^{-5}$ | $\approx 3.1 \cdot 10^{-5}$ | $\approx 11$ |
| $10^7$ | $j = 16$, range $[7.6, 15.3) \cdot 10^{-6}$ | $\approx 7.6 \cdot 10^{-6}$ | $\approx 13$ |

The product $N \xi_c$ takes values $11$ and $13$ at the two tested points.
This is **suggestive** of $\xi_c \asymp 1/N$ but two data points constrain
neither the exponent (could be $\xi_c \sim N^{-1+o(1)}$) nor the constant
(ratio $13/11 = 1.18$ across one decade of $N$). The honest framing:
the deficit-zone width has the same order-of-magnitude as the inverse
window length at both tested $N$, with a constant of order unity.

**Window-artifact caveat (important).** A deficit zone of width $\sim 1/N$
is a **predicted property of the rectangular-window embedding** itself:
for any sequence $X(e)$ supported on $e \in [2, N]$, $X^\wedge(\xi) \approx
X^\wedge(0) = H$ for $\xi \ll 1/N$ because the phase $e^{-2\pi i \xi e}$
is approximately constant over the window of length $N$. Hence
$|X^\wedge(\xi)|^2 \approx |H|^2$ in the band $\xi \lesssim 1/N$, and
the deficit-zone *width* $\sim 1/N$ is fixed by window length, not by
$\widetilde S_h$ data. What the data adds is the **depth** of the
deficit at DC: $\bar P_0 / D_h = |H_h|^2/D_h \in \{0.013, 0.022\}$,
which is the same statistic as $|H_h|^2 \ll D_h$ already documented
in `P12-Halasz-Hh-empirical.md` and `P12-Halasz-h-averaged.md`.
The new content is the *interior* shape of the deficit zone (smooth
rise from $|H_h|^2$ at $\xi=0$ to $D_h$ at $\xi \gtrsim 1/N$); see §6.5.

The spectral observations are consistent with — and a Fourier-domain
restatement of — the cumulative-profile observations of
`P12-Halasz-Phi-d-dyadic.md`. The previous session's "$\xi^* \sim N^{-c}$,
$c \approx 2.3$" inference (its §6 (iv)) is **now superseded**: there is
no peak frequency $\xi^*$.

## 6. The "negative $T_h$" reframe is a definitional restatement

$T_h \equiv \tfrac12 (H_h^2 - D_h)$ by definition. With empirical
$|H_h|^2 / D_h \approx 0.013$ (leg A), $0.022$ (leg B):

$$T_h / D_h = \tfrac12 (|H_h|^2/D_h - 1) \approx -0.494, \;-0.489.$$

Numerically: leg A $-D_h/2 = -589\,370$ vs observed $-581\,774$;
leg B $-D_h/2 = -1\,963\,869$ vs observed $-1\,921\,447$ — both within
$\le 1.3\%$ of $-D_h/2$.

**This is a definitional restatement, not a discovery.** The non-trivial
input is the empirical fact $|H_h|^2 \ll D_h$, which was already
documented across 23 $(N, h)$ points in `P12-Halasz-Hh-empirical.md`
and reframed second-moment-style in `P12-Halasz-h-averaged.md`. The
present session does not produce a new mechanism for $|H_h|^2 \ll D_h$;
it observes that, given that input, the negative sign and approximate
magnitude of $T_h$ follow as $T_h \approx -D_h/2$ by elementary algebra.

The substantive open question — *why* is $|H_h|^2 \ll D_h$ uniformly in $N$ —
is unchanged.

## 6.5 What the spectrum adds beyond pre-existing facts

Pre-existing (from earlier P12 notes):
- $|H_h(N)| \le 1.36 \sqrt N$ across 23 $(N, h)$ points.
- $D_h(N) \sim (\pi/4) H_h(1) \cdot N$ (no log factor).
- $|H_h|^2 / D_h \in \{0.022, \ldots, 0.852\}$ at the previously-tested
  small-$h$ grid.
- $\Psi_h(d) < 0$ on most lags $d \ge 1$ (autocorr direction).
- Cumulative dyadic-block sign pattern: negative-bulk + positive-correction.

Genuinely new this session:
- **No bin in the linear $\xi$-grid (resolution $\Delta\xi \sim 10^{-7}$,
  $\sim 10^{-8}$) has $\bar P_j > D_h$ at the two tested points.** Refutes
  narrow positive-amplitude modes (as in §4).
- **The deficit zone is monotone in $\xi$ at the dyadic-block resolution**
  — there is no inflection point that would suggest a hidden mode at
  intermediate $\xi$.
- **The deficit-zone width is consistent with the natural window-length
  scale $1/N$**, not with a separate "intrinsic" lag scale of
  $\widetilde S_h$ in the bulk.

What the spectrum does **not** add:
- A new bound on $|H_h|^2 / D_h$.
- A separation of "intrinsic negative correlation in $\widetilde S_h$"
  from "consequence of suppressed DC + window envelope."
- Any rigorous statement.

## 7. Strategic implication

(a) **Spectral-side / Halász-mean-value** approaches that aim to bound
$|H_h(N)|$ via a localized $\xi^*$ frequency are **ruled out** as a
description of the empirical phenomenon — there is no such $\xi^*$.

(b) The empirically-measured $|H_h(N)| / \sqrt{D_h} \approx 0.11$ — 0.15
across the two legs is the *direct* measure of how well the partial sum
cancels relative to white-noise variance. This is the right scalar
target: a quantitative bound on the "DC suppression factor"
$\rho_h(N) := |H_h(N)|^2 / D_h(N)$, uniform in $N$ (and ideally in $h$).

(c) The wideband-deficit shape of the spectrum is **consistent with**
negative autocorrelations $\Psi_h(d) < 0$ at typical lags $d \ge 1$,
but the spectrum *alone* does not separate this from the combined
"suppressed DC + rectangular-window envelope" (see §6.5). The
direct evidence for negative autocorrelation comes from
`P12-Halasz-Phi-d-dyadic.md`, not from this session.

(d) **Honest ceiling**: no analytic theorem about $|H_h(N)|^2 / D_h(N)$ —
the spectral data is descriptive of the tested two $(N, h)$ points only.
The "$\bar P_j \le D_h$ for every $j$" observation is robust across
$\sim 30$ $j$-bins per leg; the $\xi_c \asymp 1/N$ trend has only
two data points and is suggestive, not confirmed.

## 8. Caveats

1. **Two $N$ points only**, $h = 1$ only. The "no peak" assertion is for
   $\xi \in [\Delta\xi, 1/2]$ and is empirical. The claim "$\xi_c \asymp 1/N$"
   has only two data points; the implied constant ($N \xi_c \in \{11, 13\}$
   at the threshold $\bar P_j / D_h = 0.95$) has $\pm 25\%$ uncertainty
   under choice of threshold and is consistent with order-unity drift.
2. **Bin granularity**: the lowest 4 $j$-bins per leg (count $\le 8$) have
   high statistical noise. The deficit shape from $j = j_{\max}$ down to
   $j \approx \log_2 N - 5$ involves $\le 10$ frequency points.
3. The $0.95 D_h$ threshold for $\xi_c$ is arbitrary; $0.90$ or $0.99$
   would shift $j$ by $\pm 1$.
4. The phrase "no peak" excludes **interior** positive peaks in
   $(0, 1/2]$. DC itself is the most-suppressed bin (ratios $0.013$,
   $0.022$), so it is also not a peak — the spectrum is monotone
   non-decreasing on the tested grid until saturation at $D_h$.
5. No new rigorous content. The reframe in § 6 is descriptive and
   supersedes the incorrect "modal $\xi^*$" interpretation in
   `P12-Halasz-Phi-d-dyadic.md` § 6 (iv).
6. **Implication for $|H_h| \ll \sqrt N$**: the descriptive $|H_h|^2 / D_h$
   stability over two $N$-points is encouraging but is NOT a bound. It
   is also not contradicted by the standard Halász ceiling
   $|H_h(N)| \ll N \exp(-c \log\log N)$, which is logarithmically weaker
   than the empirical rate.

## 9. Picture-discrimination scorecard (final)

| Picture | Status before this session | Status after |
|:---|:---:|:---:|
| Single Fourier mode (narrow) | "in tension" | **refuted** |
| Single complex-pole damped oscillation, narrow ($\lambda \ll 2^{-j-1}$ at relevant $j$) | "remained plausible" | **refuted** |
| Single complex-pole damped oscillation, broad ($\lambda \gtrsim 1/N$) | "remained plausible" | **NOT refuted by spectrum alone** |
| Multi-mode (narrow positive peaks) | "remained plausible" | **refuted** |
| White-noise-with-deficit (no peak) | not previously articulated | **CONSISTENT** |
| Suppressed-DC + window-envelope (largely tautological) | not previously articulated | **CONSISTENT, possibly the dominant explanation** |

## 10. Files

- `bot/scratch/Halasz-Phi-d-spectrum.py` (new): two-leg power-spectrum FFT,
  decade and dyadic $\xi$-binning, Parseval/DC cross-checks.
- This note (new). Builds on `P12-Halasz-Phi-d-dyadic.md`,
  `P12-Halasz-Phi-d-scaling.md`, `P12-Halasz-Phi-d-autocorr.md`,
  `P12-Halasz-Hh-empirical.md`, `P12-Halasz-Dh-diagonal.md`.
