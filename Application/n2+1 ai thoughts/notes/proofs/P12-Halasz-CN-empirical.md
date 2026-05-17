# P12 Halász $h$-thread: empirical $C(N)$ envelope for Theorem F.2

**Session:** 2026-05-10 12:50 UTC.
**Predecessor:** `P12-Halasz-Fourier-orthogonality.md` (Theorem F.2 with abstract $C(N)$ constant).
**Question:** Pickup hint #1 from prev session — measure $C(N)$ effectively, test
whether $C(N) = O(N^{2-\delta})$ ("unexpected, would let $H = N$ give a non-trivial bound")
or the expected $C(N) \gg N^2$ from small $\sin(\pi\beta)$ tails.
**Outcome:** $C(N)$ is empirically slow-growing — consistent with both $N \log N$ and
$N^{1.21}$ on 7 data points (cannot discriminate). Either way, much better than the
trivial worst-case $N^3 (\log N)^c$. Theorem F.2 becomes effective at $H$ exceeding this
slow-growing $C(N)$. This is a moderate strategic refinement, not a strategic breakthrough.

## 1. Setup (recap from F.2 note)

Theorem F.2 of `P12-Halasz-Fourier-orthogonality.md` says: for fixed $N$,
$$
R(N, H) := \frac{\sum_{h=1}^H |H_h(N)|^2}{\sum_{h=1}^H D_h(N)}
\xrightarrow[H \to \infty]{} 1, \qquad
|R(N, H) - 1| \le \frac{C(N)}{H},
$$
with $C(N) = 2 C_{\mathrm{num}}(N) / A(N)$ where
$$
C_{\mathrm{num}}(N) = \sum_{e_1, e_2 \,\mathrm{sf,good},\, e_1 \ne e_2}
\sum_{\epsilon_1 \in \{\pm 1\}^{\omega'(e_1)}, \epsilon_2 \in \{\pm 1\}^{\omega'(e_2)}}
\frac{1}{|\sin(\pi \beta(e_1, \epsilon_1, e_2, \epsilon_2))|},
$$
$$
A(N) = \sum_{e \le N,\, \mathrm{sf,good}} 2^{\omega'(e)}, \qquad
\omega'(e) = \omega(e) - [2 \mid e].
$$
Here $\beta = \tilde\alpha_{\epsilon_1}(e_1) + \tilde\alpha_{\epsilon_2}(e_2) \pmod 1$ with
$\tilde\alpha_\epsilon(e) = \sum_{p \mid e,\, p > 2} \epsilon_p a_p^{(e)}/p + [2 \mid e]/2$
and $a_p^{(e)} = \alpha_p \cdot (e/p)^{-1} \pmod p$, $\alpha_p^2 \equiv -1 \pmod p$.

Lemma F.1 guarantees $\beta \not\equiv 0 \pmod 1$ for $e_1 \ne e_2$ sf-good, so each
$1/|\sin(\pi\beta)|$ is finite — but no uniform bound is established.

## 2. Worst-case crude bound

For fixed $(e_1, \epsilon_1), (e_2, \epsilon_2)$ with $e_1 \ne e_2$, $\beta$ is a rational
with denominator $q$ dividing $\mathrm{lcm}(e_1, e_2) \cdot 2 \le 2 e_1 e_2$. Hence
$|\beta - k| \ge 1/q$ for some integer $k$, and by Jordan's inequality
$\sin(\pi/q) \ge 2/q$, so $|\sin(\pi\beta)| \ge 2/q$, i.e.,
$1/|\sin(\pi\beta)| \le q/2 \le e_1 e_2$.

Multiplying by $\le 2^{\omega(e_1) + \omega(e_2)}$ sign-pattern factor and summing:
$$
C_{\mathrm{num}}(N) \le \sum_{e_1, e_2 \le N} 2^{\omega(e_1) + \omega(e_2)} e_1 e_2
\ll N^4 (\log N)^c,
$$
giving $C(N) \ll N^3 (\log N)^c$ in the trivial bound.

This is grossly pessimistic — most $\beta$ values are nowhere near integers.

## 3. Empirical computation

Script `bot/scratch/Halasz-CN-envelope.py`. For each sf-good $e \le N$, factor $e$,
compute $a_p^{(e)}$ for each odd prime $p \mid e$, enumerate the $2^{\omega'(e)}$
sign patterns $\epsilon$ to get the list of $(e, \tilde\alpha_\epsilon(e))$ pairs.
Then for all distinct ordered pairs $((e_1, \epsilon_1), (e_2, \epsilon_2))$ with
$e_1 \ne e_2$, accumulate $1/|\sin(\pi \beta)|$.

Vectorized via numpy outer products. Total wall-clock $\le 10$s for $N = 2000$.

Data table:

| $N$ | $A(N)$ | $C_{\mathrm{num}}(N)$ | $C(N) = C_{\mathrm{num}}/A$ | $C(N)/(N \log N)$ | $C_{\mathrm{num}}/(N^2 \log N)$ |
|---:|---:|---:|---:|---:|---:|
| 20 | 9 | 213 | 23.7 | 0.395 | 0.178 |
| 50 | 19 | 1{,}606 | 84.6 | 0.432 | 0.164 |
| 100 | 43 | 10{,}978 | 255.3 | 0.554 | 0.238 |
| 200 | 89 | 40{,}222 | 451.9 | 0.427 | 0.190 |
| 500 | 217 | 284{,}961 | 1{,}313 | 0.423 | 0.183 |
| 1000 | 429 | 1{,}243{,}919 | 2{,}900 | 0.420 | 0.180 |
| 2000 | 863 | 6{,}450{,}792 | 7{,}475 | 0.492 | 0.212 |

Cross-check: $A(20) = 9$, $A(50) = 19$, $A(100) = 43$ match the F.2 note's
denominator-formula evaluation exactly. So we are computing the same $A(N)$.

## 4. Empirical model fit

**Model A**: $C_{\mathrm{num}}(N) \sim N^p$. Log-log fit over 7 points: $p \approx 2.22$.
Pairwise slopes $\{2.21, 2.77, 1.87, 2.14, 2.13, 2.38\}$ — variable, with no clear
asymptotic value. Means $\approx 2.25$.

**Model B**: $C_{\mathrm{num}}(N) \sim c \cdot N^2 \log N$. The ratio
$C_{\mathrm{num}}/(N^2 \log N)$ takes values $\{0.178, 0.164, 0.238, 0.190, 0.183, 0.180, 0.212\}$.
Mean $\approx 0.19$, std $\approx 0.026$, no monotone trend.

**Model C**: $C(N) \sim c N \log N$. Ratio $C(N)/(N \log N)$:
$\{0.395, 0.432, 0.554, 0.427, 0.423, 0.420, 0.492\}$. Mean $\approx 0.45$,
std $\approx 0.054$, $N = 100$ and $N = 2000$ slightly high. Model B and C
are equivalent only up to $A(N)/N$ — and $A(N)/N$ itself drifts mildly
($\{0.45, 0.38, 0.43, 0.45, 0.43, 0.43, 0.43\}$), so the equivalence is approximate.

**Honest conclusion**: data is consistent with $C_{\mathrm{num}}(N) \asymp N^2 \log N$
**OR** with the pure-power $C_{\mathrm{num}}(N) \sim N^{2.22}$ (script's global log-log fit).
The two models differ by at most a factor 1.6 over $N \in [20, 2000]$ and the data
cannot discriminate. The 7-point pairwise-slope sequence $\{2.21, 2.77, 1.87, 2.14, 2.13, 2.38\}$
has std $\approx 0.27$, comparable to the difference between $\{2.0, 2.21\}$. **Either
model implies the same headline: $C_{\mathrm{num}}$ is at most $N^{2 + o(1)}$, and
$C(N)$ is at most $N^{1 + o(1)}$.**

**Caveats** (essential):
- 7 data points, two-decade range. Cannot rigorously discriminate
  $N^2 \log N$ from $N^{2.05}$ or $N^{2.22}$.
- The rough monotone-up drift in pairwise slope ($1.87 \to 2.38$) is
  consistent with a $\log$ correction OR with a small power slope above 2.
- The ratio $C/(N \log N)$ is non-monotone (peaks at $N = 100$, recovers at
  $N = 2000$), suggesting finite-$N$ artifacts of the same order as the model error.
- Beyond $N = 2000$ the script becomes memory-bound at the pair-matrix step;
  the natural extension is $N = 5000$ via blocked computation, deferred.

## 5. Strategic reading

**The expected outcome held.** Pickup hint #1 was $C(N) \gg N^2$ from small
$\sin(\pi\beta)$ tails. Empirical $C_{\mathrm{num}}(N)$ is at most $N^{2.22}$
(power-fit) or $N^2 \log N$ (log-correction model) — either way, slightly above $N^2$,
not below. Contradicts the hypothetical $O(N^{2-\delta})$ regime in which F.2 would have
given a non-trivial $|R(N, N) - 1| \to 0$ bound at the natural $H = N$.

**The bound is much better than worst-case.** Trivial §2 bound was $C(N) \ll N^3 (\log N)^c$;
measured $C(N) \le N^{1.22}$ (or $N \log N$). Savings: a factor of $N^{1.78}$ to $N^2$
depending on the model. The small-$\sin$ tails contribute, but rarely enough to keep
the average down.

**F.2 with the empirical envelope.** Reading the data conservatively as
$C(N) \le c \cdot N \log N$ with $c \approx 0.5$: $|R(N, H) - 1| \le 0.5 N \log N / H$,
effective at $H \gg N \log N$.

Implications at this $H$ regime (using $A(N) / N \approx 0.43$ from the table):
- Mean over $h$: $\frac{1}{H}\sum_{h=1}^H |H_h(N)|^2 = (1 + o(1)) A(N) \approx 0.43 N$.
  So $L^2$-mean $|H_h| \le \sqrt{A(N)} \le 0.66 \sqrt N$ (Cauchy: Jensen on $|H_h| \le \sqrt{|H_h|^2}$).
- Markov: $\#\{h \in [1, H] : |H_h(N)|^2 \ge K \cdot A(N)\} \le H/K$ for any $K$.
  In particular, 99% of $h \in [1, H]$ have $|H_h(N)|^2 \le 43 N$.

**Strategic gap.** The upstream goal (Lemma 3.4 reduction) needs uniform-in-$h$
$|H_h(N)| \ll \sqrt N \cdot (\log N)^{O(1)}$ for $h \le H(N)$ with $H(N)$ going
to infinity slowly (in $N$). The F.2 framework gives a Cesaro-mean bound at
$H \gg N \log N$ — the wrong direction in the $H \to \infty$ vs $H = O(\log N)$
asymmetry. F.2 is a tool for the AVERAGED question; it does not directly attack
the per-$h$ uniform question.

But it's not vacuous: the Markov density bound (99% of $h$ have $|H_h|^2 \le 100 N$
when averaged over $H \gg N \log N$) is a rigorous statement about the *typical*
$h$, complementing the empirical per-$h$ observations of `P12-Halasz-rho-broad.md`.

## 6. What's vindicated, what's redirected

**Vindicated.** F.2's $C(N)/H$ envelope is empirically sharper than the trivial
worst-case (§2) by a factor of $N^{1.78}$ to $N^2$. The $N^{2 + o(1)}$ scaling of
$C_{\mathrm{num}}$ is consistent with random-phase heuristics for a $\sim N^2$ count
of $\beta$ values uniformly distributed mod 1 (then $\mathbb E[1/|\sin\pi\beta|] = O(\log N)$
under uniform-on-circle assumption).

**Redirected.** F.2 is now a "moderate" tool, not a "strategic" tool. The
right strategic targets remain:
- Per-$h$ rigorization of $|H_h(N)| \ll \sqrt N$ at small $h$. None of the
  Halász, B-process, or Cesaro routes have produced this.
- Fourier-in-$e$ direction (prev pickup hint #2). FFT spectrum data
  (`P12-Halasz-Phi-d-spectrum.md`) showed featureless, no-peak: low EV.
- Multiplicative-character / Dirichlet-series direction (prev pickup hint #3).
  Halász on $\widetilde S_h$ would give only $N (\log N)^{-c}$, weaker than the
  empirical $\sqrt N$. Not the binding mechanism.

The remaining open strategic threads in this branch are:
- Direct exponential-sum bound for $H_h(N)$ at fixed $h$ (Vinogradov-type
  cancellation in $e$-direction with multiplicative weights).
- Step away from this thread entirely; revisit Hooley boundary $\Delta(N)$
  rigorization (the genuine $S(N) = N \Sigma_*$ residual).

## 7. Rigor accounting

**Rigorous (this session).** None — purely empirical. The model fit
$C(N) \asymp N \log N$ has 7 data points and is empirical, not proven.

**Rigorous (carried over).** Theorem F.2 ($R(N, H) \to 1$ as $H \to \infty$)
and Lemma F.1 (no torsion in $\beta$).

**Heuristic (this session).** $C(N) \sim 0.45 N \log N$ as the empirical model.
$C_{\mathrm{num}}(N) \sim 0.19 N^2 \log N$ as the empirical model. Random-phase
intuition for the $\log$ correction.

## 8. Files

- `bot/scratch/Halasz-CN-envelope.py` (new): exact computation of $C_{\mathrm{num}}(N)$
  and $A(N)$ at $N \in \{20, 50, 100, 200, 500, 1000, 2000\}$.
- `bot/scratch/Halasz-CN-envelope-output.txt` (new): raw output table.
- Builds on: `P12-Halasz-Fourier-orthogonality.md` (Theorem F.2; defines $C(N)$).
- Cross-references: `P12-Halasz-rho-broad.md` (per-$h$ data, complements
  Markov density bound), `P12-Halasz-Phi-d-spectrum.md` (FFT-in-$e$ has no peak).
