# P12 — Halász direction: dyadic-block profile of $\Psi_h(d)$

**Session 2026-05-10.** Dyadic-block decomposition of the autocorrelation
$\Psi_h(d) := \sum_e \widetilde S_h(e)\widetilde S_h(e+d)$ at three $(N, h)$
data points. Confirms across three independent points the
"negative-wave $+$ positive-correction $+$ negative-tail" cumulative
structure that the predecessor session (`P12-Halasz-Phi-d-scaling.md`)
observed at a single $(N, h)$.

This file is a follow-up to:

- `P12-Halasz-Phi-d-autocorr.md` — definitions, identity $(\star)$, single-$N$ FFT.
- `P12-Halasz-Phi-d-scaling.md` — multi-$N$ cumulative profile.

## 1. Setup

For $e \ge 2$ squarefree with $p \mid e \Rightarrow p = 2$ or $p \equiv 1 \pmod 4$
("sf-good"), and $\widetilde S_h(e) := \prod_{p \mid e} 2 \cos(2\pi h\,
\alpha_p (e/p)^{-1}_p / p)$, with the conventional $\widetilde S_h(2e) =
(-1)^h \widetilde S_h(e)$ for $e$ odd.

Define
$$
H_h(N) = \!\!\sum_{2 \le e \le N \atop e \text{ sf-good}}\!\! \widetilde S_h(e),
\qquad
D_h(N) = \!\!\sum_{2 \le e \le N \atop e \text{ sf-good}}\!\! \widetilde S_h(e)^2,
$$
$$
\Psi_h(d) := \!\!\sum_{2 \le e, e+d \le N}\!\! \widetilde S_h(e)\,\widetilde S_h(e+d),
\qquad T_h(N) := \tfrac12\!\left(H_h(N)^2 - D_h(N)\right).
$$
Identity $(\star)$ (proved last session, $d \in [1, N-2]$):
$$
\sum_{d=1}^{N-2} \Psi_h(d) = T_h(N).
$$

For each integer $k \ge 0$, the **dyadic block sum** is
$$
\sigma_h(k) := \!\!\sum_{2^k \le d < \min(2^{k+1}, N-1)}\!\! \Psi_h(d).
$$

Per identity $(\star)$,
$\sum_{k = 0}^{\lfloor \log_2(N-2)\rfloor} \sigma_h(k) = T_h(N)$.

## 2. Computation

`bot/scratch/Halasz-Phi-d-dyadic.py`. Three legs:
- **Leg A**: $N = 3 \cdot 10^6$, $h = 1$.
- **Leg B**: $N = 3 \cdot 10^6$, $h = 5$.
- **Leg C**: $N = 10^7$, $h = 1$.

FFT autocorrelation gives $\Psi_h(d)$ for all $d \in [0, N-1]$ in $O(N \log N)$.
Total wall-clock: $\sim 30$s. Identity $(\star)$ verified to relative error
$\le 5 \cdot 10^{-16}$ at all three points (numerical FFT precision; not new
mathematics).

## 3. Data

### 3.1 Leg A — $N = 3 \cdot 10^6$, $h = 1$

$H_h = -123.3$, $\;D_h = 1\,178\,740.6$, $\;T_h = -581\,773.7$.

| $k$ | $[\,2^k,\,2^{k+1})$ | $\sigma_h(k)$ | $\sigma/T_h$ | $\mathrm{cum}/T_h$ | sign |
|---:|:---:|---:|---:|---:|:---:|
|  0 | $[1, 2)$ | $-241.3$ | $0.000$ | $0.000$ | $-$ |
|  1 | $[2, 4)$ | $-2412.9$ | $0.004$ | $0.005$ | $-$ |
|  2 | $[4, 8)$ | $662.9$ | $-0.001$ | $0.003$ | $+$ |
|  3 | $[8, 16)$ | $-1481.0$ | $0.003$ | $0.006$ | $-$ |
|  4 | $[16, 32)$ | $-2604.9$ | $0.004$ | $0.010$ | $-$ |
|  5 | $[32, 64)$ | $9005.9$ | $-0.015$ | $-0.005$ | $+$ |
|  6 | $[64, 128)$ | $1288.5$ | $-0.002$ | $-0.007$ | $+$ |
|  7 | $[128, 256)$ | $-9333.2$ | $0.016$ | $0.009$ | $-$ |
|  8 | $[256, 512)$ | $-4296.8$ | $0.007$ | $0.016$ | $-$ |
|  9 | $[512, 1024)$ | $12584.5$ | $-0.022$ | $-0.005$ | $+$ |
| 10 | $[1024, 2048)$ | $-70488.8$ | $0.121$ | $0.116$ | $-$ |
| 11 | $[2048, 4096)$ | $-16763.4$ | $0.029$ | $0.144$ | $-$ |
| 12 | $[4096, 8192)$ | $-57154.1$ | $0.098$ | $0.243$ | $-$ |
| 13 | $[8192, 16384)$ | $-123572.2$ | $0.212$ | $0.455$ | $-$ |
| 14 | $[16384, 32768)$ | $32063.0$ | $-0.055$ | $0.400$ | $+$ |
| 15 | $[32768, 65536)$ | $-164380.3$ | $0.283$ | $0.683$ | $-$ |
| 16 | $[65536, 131072)$ | $-36481.0$ | $0.063$ | $0.745$ | $-$ |
| 17 | $[131072, 262144)$ | $-253577.5$ | $\mathbf{0.436}$ | $\mathbf{1.181}$ | $-$ |
| 18 | $[262144, 524288)$ | $161820.4$ | $-0.278$ | $0.903$ | $+$ |
| 19 | $[524288, 1048576)$ | $17282.0$ | $-0.030$ | $0.873$ | $+$ |
| 20 | $[1048576, 2097152)$ | $-44363.4$ | $0.076$ | $0.950$ | $-$ |
| 21 | $[2097152, 2999999)$ | $-29330.1$ | $0.050$ | $1.000$ | $-$ |

**Peak overshoot**: $\mathrm{cum}/T_h = \mathbf{1.181}$ at end of $k = 17$.
**Positive correction**: $k = 18, 19$ (sum $+179\,102$).
**Tail**: $k = 20, 21$ negative.

### 3.2 Leg B — $N = 3 \cdot 10^6$, $h = 5$

$H_h = -353.9$, $\;D_h = 1\,628\,491.4$, $\;T_h = -751\,613.5$.

Sign pattern $\sigma_h(k)$ for $k = 0,\dots,21$:
$$
+,-,+,-,-,+,-,+,+,-,-,-,-,-,-,-,-,-,-,+,+,-.
$$

Highlights:
- Largest single block: $k = 14$, $\sigma = -267\,172.7$ ($\sigma/T_h = 0.355$).
- Cumulative crosses $1$ inside $k = 17$.
- **Peak overshoot**: $\mathrm{cum}/T_h = \mathbf{1.027}$ at end of $k = 18$.
- **Positive correction**: $k = 19, 20$ (sum $+119\,128$).
- Tail: $k = 21$ negative.

### 3.3 Leg C — $N = 10^7$, $h = 1$

$H_h = +291.3$, $\;D_h = 3\,927\,738.3$, $\;T_h = -1\,921\,446.6$.

Sign pattern $\sigma_h(k)$ for $k = 0,\dots,23$:
$$
+,-,-,-,+,+,-,+,+,+,-,-,-,-,-,-,+,-,-,-,-,-,+,-.
$$

Highlights:
- Largest single block: $k = 18$, $\sigma = -538\,398.5$ ($\sigma/T_h = 0.280$).
- Cumulative crosses $1$ inside $k = 21$.
- **Peak overshoot**: $\mathrm{cum}/T_h = \mathbf{1.071}$ at end of $k = 21$.
- **Positive correction**: $k = 22$ (sum $+245\,011$).
- Tail: $k = 23$ negative.

## 4. Findings

### 4.1 Cumulative overshoot is structural across $(N, h)$

| $N$ | $h$ | peak $\mathrm{cum}/T_h$ | block $k$ at peak | $d$-range at peak |
|---:|---:|---:|---:|---:|
| $3 \cdot 10^6$ | $1$ | $1.181$ | $17$ | $[1.31, 2.62] \cdot 10^5$ |
| $3 \cdot 10^6$ | $5$ | $1.027$ | $18$ | $[2.62, 5.24] \cdot 10^5$ |
| $10^7$         | $1$ | $1.071$ | $21$ | $[2.10, 4.19] \cdot 10^6$ |

All three points show the same **mid-to-upper-$k$** profile (skeptic-flagged
clarification):
$$
\boxed{\text{neg-dominated mid-$k$ bulk} \;\to\; \text{overshoot to } \mathrm{cum}/T_h > 1
       \;\to\; \text{positive correction wave} \;\to\; \text{small negative tail to settle at } 1.000.}
$$
**Caveat.** At small $k$ (typically $k \lesssim 9$ in Legs A and C),
$\sigma_h(k)$ has noisy mixed signs — e.g. Leg A has positive blocks at
$k = 2, 5, 6, 9$. The magnitudes there are $|\sigma_h(k)| \le 13\,000$,
all $\le 2.2\%$ of $|T_h|$, so the small-$k$ contribution is below the
noise floor of the bulk; the structural pattern is in the mid-to-upper $k$.
The boxed slogan describes the dominant trend, not every block.

The overshoot magnitudes also differ meaningfully across legs (excess
over 1 of $0.181$ vs $0.027$ vs $0.071$ — almost an order of magnitude
spread); the *qualitative* shape is consistent, the magnitudes are not.

### 4.2 Mass concentration vs cancellation

For Leg A, the four blocks with largest $|\sigma_h(k)|$ are $k \in \{17, 15, 18, 13\}$
(non-contiguous, with $k=18$ of opposite sign to $k=15, 17$). Their unsigned
total is $|\sigma_{17}| + |\sigma_{15}| + |\sigma_{18}| + |\sigma_{13}| =
253577 + 164380 + 161820 + 123572 = 703\,349 \approx 1.21 \cdot |T_h|$;
their algebraic sum is $-379\,710 \approx 0.65 \cdot |T_h|$. The proper reading
(skeptic-flagged): **cancellation between large blocks of opposite sign is
what makes $|T_h|$ smaller than the unsigned-block budget**, not "spread
mass" alone.

What is correctly claimed:

- **No single dyadic block carries more than $44\%$ of $|T_h|$ in any leg**
  ($k=17$ in Leg A: $0.436$; $k=14$ in Leg B: $0.355$; $k=18$ in Leg C: $0.280$).
  The "single dominant block" picture is **not** ruled out by this alone — $44\%$
  is large — but the existence of a comparable opposite-sign block (e.g.
  $k=18$ at $-0.278 \cdot T_h$ in Leg A) means a single Fourier mode would
  not reproduce the data.

- **Multiple non-trivial blocks contribute $\ge 10\%$ of $|T_h|$ in each leg**:
  in Leg A, $\{k = 10, 12, 13, 15, 17, 18\}$ each have $|\sigma/T_h| \ge 0.098$.
  This is the correct sense of "spread."

What is **not** ruled out: a single-mode picture with a *long* impulse-response
tail (a damped oscillation generated by a single complex pole) would show
exactly this kind of multi-block alternating-sign pattern.

### 4.3 The "spectral peak at a fixed absolute $\xi$" picture is in tension with the two-point trajectory

If $|\widehat{\widetilde S_h}(\xi)|^2$ had a peak at a *fixed absolute* frequency
$\xi^*$ independent of $N$, the dyadic block holding the bulk of off-diagonal
mass would be at a $d$-scale $\sim 1/\xi^*$ independent of $N$. Comparing
Legs A and C (both $h=1$): peak block moved from $k = 17$ ($d \approx 2 \cdot 10^5$)
to $k = 21$ ($d \approx 3 \cdot 10^6$). With only two points and integer-block
peak resolution this is suggestive but not a refutation; see §6 (iv) for the
quantitative discussion.

## 5. Caveats

- Three $(N, h)$ data points only: $(3 \cdot 10^6, 1)$, $(3 \cdot 10^6, 5)$, $(10^7, 1)$.
- Two $h$ values, two $N$ values; cannot independently estimate $N$- and $h$-trends.
- Overshoot magnitude varies from $1.027$ to $1.181$ — almost an order of
  magnitude in *excess* over $1$ ($0.027$ vs $0.181$); the qualitative shape
  is consistent, the magnitudes are not.
- The trend in $N$ for $h=1$ overshoot is non-monotone in this small sample
  ($1.181$ at $N = 3 \cdot 10^6$, $1.071$ at $N = 10^7$).
- Small-$k$ blocks ($k \lesssim 9$) have noisy mixed signs; the structural
  pattern is a mid-to-upper-$k$ statement.
- The §6 (iv) shift estimate $\Delta k = 4$ is an integer measurement on
  two points; honest uncertainty is $\Delta k \in \{3,4,5\}$, $c \in [1.7, 2.9]$.
- "Same qualitative profile" is a sign-pattern observation, not a quantitative one.
- The dyadic binning is chosen for analytic-side convenience; other binnings
  (decadic, triadic) are not tested.
- No analytic theorem here. All findings are descriptive of the tested grid.

## 6. Strategic implication

Two pictures **disfavored on this grid (3 points each)**:

- (i) **strict single-block dominance** — disfavored: max single block
  contributes only $0.28$–$0.44$ of $|T_h|$; comparable opposite-sign
  blocks coexist (per §4.2). A *single Fourier mode* picture is in tension
  with the data, but a single complex-pole damped oscillation (which
  produces a multi-block alternating-sign autocorrelation) is **not**
  excluded.
- (ii) **monotone all-negative dyadic profile** — refuted on the dominant
  blocks: positive correction blocks are present in every leg (e.g.
  $k=18$ in Leg A with $-0.278 T_h$; $k=19, 20$ in Leg B with sum $\approx
  -0.158 T_h$; $k=22$ in Leg C with $-0.128 T_h$). This is a clean refutation.

Two pictures **still consistent**:

- (iii) **damped-oscillation in $\Psi_h(d)$ on a $d$-scale that grows with $N$**:
  consistent with all three legs.
- (iv) **low-frequency $\xi^* \sim N^{-c}$ spectral peak** for some
  $c \in (0, 1]$: in this picture, the dyadic block holding the peak should
  shift by $\Delta k = c \log_2(N_2/N_1)$ as $N$ scales by $N_2/N_1$. With
  the observed shift $\Delta k = 21 - 17 = 4$ between Legs A and C
  ($\log_2(N_2/N_1) = \log_2(10^7 / (3 \cdot 10^6)) = 1.737$), the implied
  $c \approx 2.30$.
  **Quantization caveat (skeptic-flagged):** $\Delta k$ is an integer and
  is identified by visual peak in $\mathrm{cum}/T_h$ rather than a fitted
  continuous quantity. A reasonable error bar is $\Delta k \in \{3, 4, 5\}$,
  giving $c \in [1.7, 2.9]$. With only **two** $h=1$ data points, this is
  one integer measurement and the apparent inconsistency with $c \le 1$
  is suggestive, not refutation. A third $N$ point ($N = 3 \cdot 10^7$) is
  needed to test it.

The most direct discrimination is **direct FFT of $\widetilde S_h$** to
visualize $|\widehat{\widetilde S_h}(\xi)|^2$ as a function of $\xi$ at
two distinct $N$. This is the natural next step, and is the heart of
predecessor pickup hint #4 (low-frequency large-sieve setup).

## 7. Pickup hints for next session

1. **(½ session, empirical, highest-EV next)**: direct FFT
   $|\widehat{\widetilde S_h}(\xi)|^2$ on the linear $\xi$-grid for
   $\xi \in [0, 1/2]$, at $N = 3 \cdot 10^6$ and $N = 10^7$, $h = 1$.
   Bin into $\xi$-decades; report where the power is concentrated.
   Discriminates picture (iii) vs (iv) directly.

2. **(½ session, empirical, scaling)**: extend dyadic profile to
   $N = 3 \cdot 10^7$ at $h = 1$ to give *three* $h=1$ data points
   for the peak-block trajectory. This pins the $\xi^*(N)$ exponent
   (or refutes the monotone-shift claim).

3. **(½ session, analytic): explain the negative sign of $T_h$.**
   Carry-over from prev session. Candidate mechanism: $p = 2$ contribution.

4. **(1 session, analytic, more ambitious)**: Once (1) is in hand,
   set up the large-sieve / Plancherel inequality on $|\widehat{\widetilde
   S_h}|^2$, using the dyadic mass distribution to set a Cauchy budget.

## 8. Files

- `bot/scratch/Halasz-Phi-d-dyadic.py` (new): three-leg dyadic computation.
- `n2+1 ai thoughts/notes/proofs/P12-Halasz-Phi-d-dyadic.md` (this file).
- Builds on: `P12-Halasz-Phi-d-autocorr.md`, `P12-Halasz-Phi-d-scaling.md`,
  `P12-Halasz-Hh-empirical.md`, `P12-Halasz-Dh-diagonal.md`,
  `P12-Halasz-h-averaged.md`.
