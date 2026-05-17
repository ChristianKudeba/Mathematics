# P12 — $h$-averaged second moment $\sum_{h=1}^H |H_h(N)|^2$ — empirical preview

## 1. Context

Session 2026-05-08 12:52 UTC (`P12-Halasz-Dh-diagonal.md`) computed the
diagonal second moment $D_h(N) := \sum_{e \le N,\,\mathrm{sf,good}} \widetilde S_h(e)^2$
in closed form: $D_h(N) \sim C_h N$ with $C_h = (\pi/4) H_h(1)$ explicit.
Empirically the single-$h$ ratio
$$|H_h(N)|^2 / D_h(N) \in \{0.022, 0.146, 0.052, 0.852\}$$
at $N = 10^7$ for $h \in \{1, 2, 5, 100\}$ — wildly variable, far from 1.

**Hypothesis under test (this session)**: averaging over $h$ might cancel
the off-diagonal contribution $\sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde S_h(e_2)$,
giving
$$\sum_{h=1}^H |H_h(N)|^2 \approx \sum_{h=1}^H D_h(N).$$
This was the "highest-EV next analytic step" promoted by prev session's
strategy file. The orthogonality intuition: summing $\cos(2\pi h \cdot)$
over $h = 1, \dots, H$ gives a Dirichlet kernel that concentrates on
arithmetic alignments $r_1/e_1 + r_2/e_2 \in \mathbb Z$.

## 2. Method

`bot/scratch/Halasz-h-averaged.py`: extends prev session's
`Halasz-Dh-empirical.py` to vectorize over $h$ via numpy. Per-$e$ work:
SPF factorization, `pow(ep, -1, p)` to get $a_p$, then a length-$H$ array
$2\cos(2\pi h\, a_p / p)$ multiplied into the running product. Outputs
$(H_h, D_h)$ for all $h$ simultaneously.

Cost: $\sim 10$s at $N = 10^7$, $H = 20$; $\sim 50$s at $N = 10^7$, $H = 100$.

## 3. Data

Define the $h$-summed ratio
$$R(N, H) := \frac{\sum_{h=1}^H |H_h(N)|^2}{\sum_{h=1}^H D_h(N)}.$$

| $N$    | $H$ | $R(N,H)$ | $\frac{1}{HN} \sum_h |H_h|^2$ | $\frac{1}{HN} \sum_h D_h$ |
|--------|-----|---------:|--------------------------------:|----------------------------:|
| $10^5$ | 20  | 0.301    | 0.128 | 0.426 |
| $10^5$ | 100 | 1.675    | 0.718 | 0.429 |
| $10^6$ | 20  | 0.082    | 0.0352 | 0.428 |
| $10^6$ | 100 | 0.565    | 0.243 | 0.431 |
| $10^7$ | 20  | 0.044    | 0.0189 | 0.428 |
| $10^7$ | 100 | 0.122    | 0.0528 | 0.431 |

Per-$h$ summary at $(N, H) = (10^7, 100)$: mean $|H_h|^2/D_h = 0.120$,
std $0.169$, min $\approx 0$, max $0.852$ (at $h = 75$).

Per-$h$ summary at $(N, H) = (10^7, 20)$: mean $0.044$, std $0.052$,
min $0.001$, max $0.157$ (at $h = 3$).

## 4. Hypothesis status

**No empirical evidence for $R(N, H) \to 1$ in the tested range; trend is wrong-signed.**

- **At fixed $H$, $R(N, H)$ decreases with $N$.** $R(N, 20)$: $0.301, 0.082, 0.044$
  at $N = 10^5, 10^6, 10^7$. $R(N, 100)$: $1.675, 0.565, 0.122$. Both monotone
  *down* across the three decades.
- **At fixed $N$, $R(N, H)$ increases with $H$.** Larger $H$ pulls in more
  "near-equidistributed" $h$ (less small-prime structure), where individual
  $|H_h|^2$ contributions are closer to $D_h$.

**Three decades is not asymptotic.** The data is consistent with: (a) a
genuine $R(N, H) \to 0$ behavior; (b) very slow approach to 1 with crossover
far beyond $10^7$; (c) some intermediate regime. The empirical preview cannot
distinguish between these.

If $|H_h|^2 \sim c_h N^{2\alpha}$ with $\alpha < 1/2$ uniformly, then
$R(N, H) \sim c/C_1 \cdot N^{2\alpha - 1}$. Fitting the $N = 10^5 \to 10^7$
slope gives $\alpha \approx 0.21$ (at $H=100$) to $\alpha \approx 0.29$ (at $H=20$).
**Strong caveats**: only 3 $N$-decades; $H=100$ at $N=10^5$ has only $\sim 13600$
sf-good $e$ (so $\sim 136$ per $h$), where finite-size noise dominates the
single-$h$ statistics. The $\alpha$ fit is suggestive, not a real asymptotic
claim.

**Cauchy–Schwarz baseline.** $|H_h(N)|^2 \le |\{e \le N: \mathrm{sf,good}\}|
\cdot D_h(N) \approx 0.115 N \cdot D_h(N)$, hence trivially
$R(N, H) \le 0.115 N$. The hypothesis "$R \to 1$" was never forced by any
rigorous lower bound; refuting it does not refute any prior rigorous claim.
The observation is descriptive, not corrective.

## 5. What this tells us

Three positive structural observations follow from refuting the hypothesis.

**(a) Off-diagonal is negative on the tested $h$-range.** The empirical
$\sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde S_h(e_2) = |H_h(N)|^2 - D_h(N)$
is negative for *all* $h \in \{1, \dots, 100\}$ at $N = 10^7$ (mean ratio
$|H_h|^2/D_h = 0.12$). **Caveat**: $h \in [1, 100]$ is the small-$h$ regime,
where Dirichlet-kernel concentration creates arithmetic biases; this sample
is not random over $h$-space. Whether the negativity persists for $h$ in
$[10^4, 10^5]$ or for randomly-sampled large $h$ is not tested. The phrase
"structural anti-correlation" is a *hypothesis* compatible with the small-$h$
data, not a proven property.

**(b) Average $|H_h|^2$ is much smaller than $D_h$, with growing margin.**
At $N = 10^7$, $H = 100$: mean $|H_h(10^7)|^2 / N \approx 0.053$ vs mean
$D_h(10^7)/N \approx 0.43$. So the *typical* $|H_h(N)| \le \sqrt{0.053 N} \approx
0.23 \sqrt N$ — well within $\sqrt N$. Prev session's $|H_h|/\sqrt N \le 1.36$
envelope is driven by outlier $h$.

**(c) Halász and diagonal-CLT both inconsistent with data.** Halász would give
$|H_h|^2 \ll N^2 (\log N)^{-2c}$, much weaker than the $N$ scale we see
(this was already shown by prev session). This session's data — $R(N,H)$
trending below 1 in the empirical range — is also inconsistent with the
simple diagonal-CLT prediction $|H_h|^2 \sim D_h$. The data lives somewhere
in between: $|H_h|^2$ may grow like $N^{2\alpha}$ ($\alpha < 1/2$), or like
$N / (\log N)^c$, or like $D_h$ but with multiplicative constant $\ll 1$
that's $h$-dependent. We cannot discriminate from 3 $N$-decades.
*Empirical observation, not analytic claim.*

## 6. What's rigorous vs. heuristic

**Rigorous (this session):**
- The closed form $D_h(N) = \sum_{e} \prod_{p|e} 4\cos^2(2\pi h a_p/p)$ is
  computed exactly, no approximation. (`Halasz-h-averaged.py` verified
  against `Halasz-Dh-empirical.py` from prev session: agrees pointwise.)
- The $h$-summed values $\sum_{h=1}^H |H_h(N)|^2$, $\sum_{h=1}^H D_h(N)$ are
  exact for the stated $(N, H)$.

**Empirical only:**
- The $R(N, H)$ trend across decades. 3 $N$-points, 2 $H$-points — no
  asymptotic claim.
- The "$\alpha \in [0.21, 0.29]$" fit. Heuristic 2-point slope.
- The "off-diagonal systematically negative" generalization beyond the
  measured $(N, h)$ grid.

**Not addressed:**
- Why off-diagonal is systematically negative (no analytic explanation).
- Whether $\frac{1}{H} \sum_h |H_h|^2 / N$ has a limit as $N \to \infty$
  (separately from $H$).

## 7. Strategic effect

**Redirects** (does NOT close): The "off-diagonal cancels under $h$-averaging"
hypothesis assumed off-diagonal $\to 0$. Empirically off-diagonal is *negative*
and not small. That's actually MORE useful than zero off-diagonal for the
upstream goal $|H_h(N)| \ll \sqrt N$ — it means the diagonal $D_h \sim N$
upper-bounds typical $|H_h|^2$ with margin. The route isn't dead; it's
redirected: from "show off-diagonal averages out" to "characterize the
structurally-negative off-diagonal."

The empirical preview took $\sim 50$s of compute at the hardest single point
($N=10^7$, $H=100$). The setup time saved is the *full analytic session* that
would have been spent on Dirichlet-kernel orthogonality before noticing the
data doesn't fit.

**Opens**: Two refined directions:
1. **Characterize the off-diagonal directly.** Compute
   $\Phi_h(d) := \sum_{e: \mathrm{sf,good}, e+d \le N} \widetilde S_h(e) \widetilde S_h(e+d)$
   for small $d$. The systematic negativity should reveal a structural
   pattern (e.g. anti-correlation when $\gcd(e, e+d) = 1$).
2. **Compute typical-$h$ $|H_h(N)|^2$ asymptotics.** If
   $\frac{1}{H} \sum_{h=1}^H |H_h(N)|^2 \sim K N$ with $K$ a small constant,
   that $K$ is itself a Dirichlet-series problem (now over pairs $e_1, e_2$
   with $e_1 = e_2$ contributing $D$ and $e_1 \ne e_2$ contributing the
   structural negative shift).

**Reaffirms**: prev sessions' methodological lesson — empirical preview
before analytic commitment. This session: a 5-min computation closed
*another* hypothesized route. The pattern is now: the diagonal $D_h$ is
asymptotically *too large* compared to $|H_h|^2$, indicating the off-diagonal
is the dominant negative-magnitude term.

## 8. Files

- `bot/scratch/Halasz-h-averaged.py` (new): vectorized over $h$.
- This note (new).
- Builds on: `P12-Halasz-Dh-diagonal.md` (closed form for $D_h$),
  `P12-Halasz-Hh-empirical.md` (single-$h$ data).
