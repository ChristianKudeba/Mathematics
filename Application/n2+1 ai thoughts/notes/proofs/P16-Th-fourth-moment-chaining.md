# P16. $T_h$ fourth-moment / additive-energy chaining route

## Goal

Open Route C' (per `P12-Th-chokepoint-status.md` §4) — the CLT / diagonal-second-moment route to the per-$h$ uniform bound on $T_h(N)$ — by laying out the analytic skeleton: present $T_h$ as a trigonometric polynomial of $K = K(N) \asymp N$ frequencies, expand the second moment (analogous to but distinct from Theorem F.2 of the $H_h$ thread), expand the fourth moment as the additive energy of the frequency set, and identify the **two** named sub-tasks that remain: (i) the additive-energy bound HE-4 on the frequency set, (ii) effective small-$H$ moment estimates (i.e., effective at $H = \log^{O(1)} N$ where Vaaler truncation lives, not just at $H \gg N^c$).

**Honest framing of the route's reach.** Conditional on HE-4 + sin-sum cancellation effective down to small $H$, the chaining argument delivers $|T_h(N)|^2 \ll N \log^{O(1)} N$ for $h$ outside a sparse density-$o(1)$ set — an $L^p$-density version strictly stronger than Theorem F.2's Cesaro mean. The fully uniform-in-$h$ bound (Lemma 3.4) requires HE-$2k$ for higher $k$ + sub-Gaussian moment growth + small-$H$ effectiveness; this is a strictly harder additive-energy problem than HE-4 alone.

**This route as sketched does not crack the chokepoint in one session.** Its value is in *converting the single black-box "Lemma 3.4" into a chain of named, separately-attackable sub-tasks*, each of which has standard analytic-NT precedent (Type-I/II divisor sums for HE-4; sub-Gaussian chaining for HE-$2k$ growth).

This route is *mathematically aligned with the empirically observed $\sqrt N$ regime* (per `P12-Th-chokepoint-status.md` route #4 framework analysis); Halász's apparatus delivers $(\log N)^{-c}$-savings, which the empirical data already exceeds.

## Why now

The $T_h$ chokepoint has not advanced for ~30 bot sessions. The previous strategic step-back (`bot/sessions/2026-05-10T15-50-25Z.md`) explicitly recommended Route C' as the highest-EV next bot step. Halász (route #4) was retired; the per-$h$ B-process (route #2) was closed by negative result. Of routes left in the catalog, route C' is the one mathematically aligned with the observed CLT-like rate.

## 1. Setup

Recall (`P12-Lemma-3-4-reduction.md` §4):
$$
T_h(N) \;=\; \sum_{\substack{2 \le e \le N \\ e \,\mathrm{sf,\,good}}} e^{2\pi i h N/e} \, S_h(e), \qquad S_h(e) \;=\; \prod_{p \mid e} S_h^{(p)},
$$
where "$e$ sf good" means $e$ squarefree with all prime divisors $\equiv 1 \pmod 4$ (the $p = 2$ factor we suppress; it contributes only a sign $(-1)^{h_2}$ that we absorb), and for split primes $p \equiv 1 \pmod 4$ with roots $\pm r_p$ of $x^2 + 1 \pmod p$:
$$
S_h^{(p)} \;=\; e^{2\pi i h_p r_p/p} + e^{-2\pi i h_p r_p/p} \;=\; 2 \cos(2\pi h_p r_p/p), \qquad h_p \;:=\; h \cdot (e/p)_p^{-1} \pmod p.
$$

**Frequency expansion.** Expanding the product (suppressing the $p=2$ phase $(-1)^{h_2}$, which is $h$-dependent and would either be folded into the index $h$ or treated as a separate harmonic; for the qualitative count below we restrict to odd $e$ — same asymptotic order):
$$
S_h(e) \;=\; \sum_{\epsilon \in \{\pm 1\}^{\omega(e)}} e^{2\pi i h \alpha_\epsilon(e)}, \qquad \alpha_\epsilon(e) \;:=\; \sum_{p \mid e} \epsilon_p \cdot \frac{r_p}{p} \cdot (e/p)_p^{-1} \pmod 1.
$$

Substituting:
$$
\boxed{T_h(N) \;=\; \sum_{(e, \epsilon)} e^{2\pi i h \beta_{e, \epsilon}}, \qquad \beta_{e, \epsilon} \;:=\; \frac{N}{e} + \alpha_\epsilon(e) \pmod 1.}
$$

So **$T_h$ is a trigonometric polynomial in $h$**, with $K = K(N) := \sum_{e \le N, \mathrm{sf, good}, e \,\mathrm{odd}} 2^{\omega(e)}$ unit-modulus terms (and a parallel even-$e$ stratum with one fewer power of 2 per such $e$, contributing the same order). The empirical table in `P12-Halasz-CN-empirical.md` reports $A(N)/N \approx 0.43$ stably for $N \le 2000$; we take $K \asymp N$. Strictly, Selberg–Delange on $\sum 2^{\omega(e)}$ over sf-good $e \le N$ gives $\sim c N (\log N)^{a}$ for an explicit $a$ depending on the sf-good restriction; the empirical near-linear stability suggests $a$ is small, but the precise scaling has not been derived here.

**Note on relation to the Halász $H_h$ thread.** The $H_h$ object of `P12-Halasz-Fourier-orthogonality.md` is $H_h(N) = \sum_{e} \widetilde S_h(e)$ *without* the $e^{2\pi i h N/e}$ phase factor. The frequencies of $H_h$ as a trig poly in $h$ are $\{\tilde\alpha_\epsilon(e)\}$, while ours are $\{N/e + \alpha_\epsilon(e)\}$ — different sets. Theorem F.2 is therefore a precedent for the technique but not an importable envelope; the $C_{\mathrm{num}}(N)$ measurement of `P12-Halasz-CN-empirical.md` does not directly bound the off-diagonal of the present second moment. A fresh measurement would be required.

## 2. The trigonometric-polynomial picture

The frequency set is
$$
\mathcal{F}(N) \;:=\; \{\beta_{e, \epsilon} : 2 \le e \le N, \, e \,\mathrm{sf,\,good}, \, \epsilon \in \{\pm 1\}^{\omega(e)}\} \;\subset\; \mathbb{R}/\mathbb{Z}.
$$
Counted with multiplicity, $|\mathcal{F}(N)| = K = A(N)$.

**Naive trivial bound.** $|T_h(N)| \le K = A(N) \sim 0.43 N$, attained only when all $K$ phases align.

**Gaussian heuristic.** If the $\beta_{e,\epsilon}$ were i.i.d. uniform on $\mathbb{R}/\mathbb{Z}$, then $T_h(N)$ at any fixed $h$ would be a sum of $K$ independent unit-modulus complex random variables, with $|T_h|^2 / K \xrightarrow{d} \mathrm{Exp}(1)$, hence $|T_h| \asymp \sqrt K \asymp \sqrt N$ in distribution. The empirical data (`P12-Lemma-3-4-empirical-Th.md`) bears this out: $|T_h|/\sqrt N \le 1.222$ across 43 sampled $h \le 7560$ at $N = 10^7$.

**Goal of this route.** Make the Gaussian heuristic rigorous in $L^4$ — i.e., produce a fourth-moment estimate that delivers $|T_h(N)|^2 \ll A(N) (\log H)^{C}$ uniformly in $h \le H$ (or for all $h$ outside an $o(H)$-density bad set).

## 3. Second moment

Squaring and summing:
$$
\sum_{h=1}^{H} |T_h(N)|^2 \;=\; \sum_{(e_1, \epsilon_1), (e_2, \epsilon_2)} \sum_{h=1}^{H} e^{2\pi i h (\beta_1 - \beta_2)}.
$$

**Diagonal $\beta_1 \equiv \beta_2 \pmod 1$:** always includes the $(e_1, \epsilon_1) = (e_2, \epsilon_2)$ pairs (count $= K$). It may include "accidental" coincidences if $\beta_{e_1, \epsilon_1} \equiv \beta_{e_2, \epsilon_2} \pmod 1$ for distinct labels — sub-question P16.3 below. Without that count, only the upper bound $\#\mathrm{diag} \ge K$ is unconditional; equality requires the accidental count to vanish or be controlled.

**Off-diagonal $\beta_1 \not\equiv \beta_2 \pmod 1$:** geometric series in $h$ gives
$$
\Big|\sum_{h=1}^{H} e^{2\pi i h (\beta_1 - \beta_2)}\Big| \;\le\; \min\!\Big(H, \, \frac{1}{|\sin(\pi(\beta_1 - \beta_2))|}\Big).
$$

The off-diagonal sin-sum (analogous to Theorem F.2's $C_{\mathrm{num}}$ but with the additional $N/e_1 - N/e_2$ contribution to $\beta_1 - \beta_2$):
$$
C_{\mathrm{num}}^{(T)}(N) \;:=\; \sum_{\beta_1 \ne \beta_2} \frac{1}{|\sin(\pi(\beta_1 - \beta_2))|}.
$$

**Worst-case bound.** The denominator of $\beta_1 - \beta_2 = N(1/e_1 - 1/e_2) + (\alpha_{\epsilon_1}(e_1) - \alpha_{\epsilon_2}(e_2)) \pmod 1$ divides $\mathrm{lcm}(e_1, e_2) \le e_1 e_2 \le N^2$. By Jordan's inequality, $1/|\sin(\pi/q)| \le q/2 \le N^2/2$ per term; with $K^2 \asymp N^2$ pairs, the trivial worst-case is $C_{\mathrm{num}}^{(T)}(N) \le N^4$. This is much worse than the diagonal $H \cdot K \asymp HN$ at any $H \le N^3$, so the *unconditional* second-moment estimate is dominated by the off-diagonal — useless without further input.

**Conjectured envelope** (parallel to the empirical $C_{\mathrm{num}}$ result): pair-wise denominators $\mathrm{lcm}(e_1, e_2) \asymp e_1 e_2$ on average force $C_{\mathrm{num}}^{(T)}(N) \le N^{2+o(1)}$ — same scaling as $C_{\mathrm{num}}$, by analogous tally-of-pairs reasoning. This is **not yet measured for the $T_h$ object;** numerical confirmation is sub-question P16.6.

**Conditional.** Under the conjectural envelope $C_{\mathrm{num}}^{(T)}(N) \le N^{2+o(1)}$ and (D2)-vanishing for the diagonal:
$$
\sum_{h=1}^{H} |T_h(N)|^2 \;=\; H \cdot K \cdot (1 + O(N^{1+o(1)}/H)),
$$
effective at $H \gg N^{1+o(1)}$. Useless for the per-$h$ uniform problem (where $H = \log^{O(1)} N$).

The mean of $|T_h|^2$ over a long $h$-window is $K \asymp N$. The square root of the mean is the canonical CLT prediction: $\sqrt K \asymp \sqrt N$ — consistent with the empirical $|T_h|/\sqrt N \le 1.222$ across 43 sampled $h \le 7560$ at $N = 10^7$ (`P12-Lemma-3-4-empirical-Th.md`, cited but not re-verified here).

## 4. Fourth moment — the additive energy of $\mathcal{F}(N)$

The next moment is genuinely new content beyond Theorem F.2. Open the fourth power:
$$
\sum_{h=1}^{H} |T_h(N)|^4 \;=\; \sum_{(e_i, \epsilon_i)_{i=1}^{4}} \sum_{h=1}^{H} e^{2\pi i h (\beta_1 + \beta_2 - \beta_3 - \beta_4)}.
$$

**Diagonal** $\beta_1 + \beta_2 \equiv \beta_3 + \beta_4 \pmod 1$. Each diagonal quadruple contributes $H$ to the sum.

**Off-diagonal.** Geometric-series bound: $|\cdot| \le 1/|\sin(\pi \delta)|$ where $\delta := \beta_1 + \beta_2 - \beta_3 - \beta_4 \pmod 1$.

Define the **(restricted) additive energy** of the frequency set:
$$
\mathsf{E}_4(N) \;:=\; \#\big\{ ((e_i, \epsilon_i))_{i=1}^{4} \;:\; \beta_1 + \beta_2 \equiv \beta_3 + \beta_4 \pmod 1 \big\}.
$$

Identifiable strata:

- **(D1) Pairing stratum:** there exists a bijection $\sigma: \{1, 2\} \to \{3, 4\}$ with $(e_i, \epsilon_i) = (e_{\sigma(i)}, \epsilon_{\sigma(i)})$ as labels. Count: at least $2K^2 - K$ (two pair orderings minus diagonal corner), assuming the $\beta_{e,\epsilon}$ for distinct labels are themselves distinct (i.e., no (D2) coincidences). For $K \asymp N$ this contributes $\asymp N^2$.
- **(D2) Frequency coincidences with distinct labels:** $\beta_{e_i, \epsilon_i} \equiv \beta_{e_j, \epsilon_j} \pmod 1$ with $(e_i, \epsilon_i) \ne (e_j, \epsilon_j)$. Whether this is empty is sub-question P16.3.
- **(D3) Genuine non-pairing 4-term coincidences:** $\beta_1 + \beta_2 \equiv \beta_3 + \beta_4 \pmod 1$ with no pairing structure. This is the genuinely arithmetic content.

**Hypothesis HE-4 (additive-energy bound, the open chunk).**
$$
\mathsf{E}_4(N) \;\le\; C \cdot K^2 \cdot \log^B N
$$
for some absolute constants $C, B$ with $B$ as small as possible (ideally $B \le 1$). Equivalently, the strata (D2)+(D3) contribute $O(K^2 \log^B N)$ on top of the trivial (D1).

**Off-diagonal worst-case (corrected).** The denominator of $\delta = \beta_1 + \beta_2 - \beta_3 - \beta_4 \pmod 1$ divides $\mathrm{lcm}(e_1, e_2, e_3, e_4) \le e_1 e_2 e_3 e_4 \le N^4$. By Jordan, $1/|\sin(\pi\delta)| \le N^4/2$ per term. With $K^4 \asymp N^4$ tuples, the trivial worst-case sin-sum is $\le N^8/2$ — vastly larger than the diagonal $H \cdot K^2 \asymp H N^2$ at any $H \ll N^6$. So *unconditionally*, the fourth-moment estimate is dominated by off-diagonal at any reasonable $H$.

**Conjectural envelope** (analogous to second-moment): if the fourth-moment off-diagonal sin-sum scales like $C_{\mathrm{num}}^{(T,4)}(N) \le N^{4+o(1)}$ (as Heath-Brown / divisor-sum heuristics predict — the analogue of the empirical $C_{\mathrm{num}} \le N^{2+o(1)}$), then under HE-4,
$$
\sum_{h=1}^{H} |T_h(N)|^4 \;\le\; H \cdot \mathsf{E}_4(N) \cdot (1 + o(1)) \;\le\; C H \cdot K^2 \log^B N,
$$
effective for $H \gg N^{2+o(1)}$. **Both the conjectural envelope $C^{(T,4)} \le N^{4+o(1)}$ and HE-4 are unproven open chunks.**

**The fourth moment as stated does not crack the small-$H$ regime.** At $H = \log^{O(1)} N$ where Vaaler lives, the off-diagonal — under any envelope, conjectural or trivial — dominates the diagonal $H K^2$. So the fourth moment, like the second, is a long-window estimate.

What does the long-window estimate buy us? Two things:
1. *Rate of growth of the diagonal*: HE-4 with $B \ll 1$ would refine the second moment's $\sqrt K$ CLT-like rate to a fourth-power moment estimate of size $\sqrt[4]{K^2 \log^B} = \sqrt K \log^{B/4}$ — Gaussian-type tail control on $|T_h|$ in the long-window mean.
2. *Identification of the small-$H$ obstacle as a separate, named sub-task* (P16.7 below).

## 5. The chaining / max-inequality transfer — and its limitations

For a unit-modulus trigonometric polynomial $T_h$ of $K$ frequencies, we want to convert moment estimates into a pointwise bound on $|T_h|$. The key honest constraint: §3-4 deliver moment estimates only for $H \gg N^{1+o(1)}$ (resp. $N^{2+o(1)}$ for the fourth moment), conjecturally — not at the small $H = \log^{O(1)} N$ that the Vaaler truncation needs.

### 5.1. Markov on the fourth moment, large-$H$ regime only

For $H \gg N^{2+o(1)}$ where the fourth-moment estimate of §4 is conjecturally effective:
$$
\#\{h \le H : |T_h(N)|^2 > t K\} \;\le\; \frac{1}{t^2 K^2} \sum_{h=1}^{H} |T_h|^4 \;\le\; \frac{C H \log^B N}{t^2}.
$$

Setting $t = \log^{B/2 + \eta} N$ for any $\eta > 0$:
$$
\#\{h \le H : |T_h(N)|^2 > K \log^{B + 2\eta} N\} \;\le\; \frac{C H}{\log^{2 \eta} N} \;=\; o(H).
$$

So **for $1 - o(1)$ of $h \le H$, with $H \ge N^{2+o(1)}$**:
$$
|T_h(N)| \;\le\; \sqrt K \cdot \log^{B/2 + \eta} N \;\ll\; \sqrt N \log^{B/2 + \eta} N.
$$

This is the natural fourth-moment density-form bound. It is strictly stronger than Theorem F.2's Cesaro mean (since the second moment alone gives only $L^2$-mean information, while this gives an $L^4$ density majority $\le \sqrt N \log^{O(1)}$).

**Crucial caveat.** The bound is *only* on density-$1-o(1)$ of $h \le H$ at $H \ge N^{2+o(1)}$. At small $H$ (Vaaler), the Markov-on-fourth-moment argument gives no effective bound on individual $h$.

### 5.2. Why this is not Lemma 3.4

The Lemma 3.4 route via Vaaler (`P12-Lemma-3-4-reduction.md` §5) requires control of $\sum_{h=1}^{H} |T_h|/h$ for $H = H(N) = \log^{O(1)} N$. The bound delivered by §5.1 is:

- Effective only for $H \ge N^{2+o(1)}$.
- Density $1-o(1)$ over that long $h$-window, not uniform.

So §5.1 by itself does *not* close Lemma 3.4. Two separate gaps remain:

**Gap A (small-$H$ effectiveness).** Make the moment estimates of §3-4 effective for $H = \log^{O(1)} N$. This itself is the chokepoint in different guise — at small $H$, the moment expansion's off-diagonal swamps the diagonal, and the "moment method" reduces to the per-$h$ uniform bound problem. **Identifying this Gap A as a named sub-task is one of this session's deliverables.** Sub-question P16.7.

**Gap B (uniform-in-$h$ vs density).** Even granting Gap A, §5.1's "density $1 - o(1)$" is not uniform. The standard upgrade is sub-Gaussian chaining via higher moments (§5.3 below), but it inherits Gap A.

### 5.3. Sub-Gaussian chaining sketch — conditional on Gap A

Conditional on Gap A being solved (small-$H$ moment estimates effective), the standard chaining argument is:

If for each $k = 1, 2, \ldots$
$$
\sum_{h=1}^{H} |T_h(N)|^{2k} \;\le\; C_k H \cdot K^k \log^{B_k} N,
$$
with $C_k = O(c^k k!)$ and $B_k = O(k)$ (sub-Gaussian moment growth), then by union bound + Markov:
$$
\max_{h \le H} |T_h(N)|^2 \;\le\; K \cdot \log^{O(1)}(NH).
$$

This would give $\max_{h \le H} |T_h(N)| \ll \sqrt N \log^{O(1)} N$, sufficient for Lemma 3.4 with $H = \log^{O(1)} N$ in the Vaaler truncation.

**The conditions** are:
- Gap A: small-$H$ effectiveness of all $2k$-moment expansions.
- HE-$2k$ for all $k$ with $C_k = O(c^k k!)$ and $B_k = O(k)$ — sub-Gaussian additive-energy growth on the frequency set.

Both are substantial open problems. HE-$2k$ generalizes HE-4 of §4: it is an additive-combinatorial / Diophantine question on the joint distribution of the frequencies $\{N/e + \alpha_\epsilon(e)\}$. Gap A is the small-$H$ form of the chokepoint itself.

**The genuine open problem set:**
1. **HE-4** (additive energy with $B \le O(1)$). Tractable: divisor-sum + CRT, sub-question P16.1.
2. **HE-$2k$ for $k \ge 3$** with sub-Gaussian growth in $k$. Less tractable; high-moment additive energy of structured frequency sets is a well-developed literature (e.g., Bourgain's restriction estimates, Iosevich–Łaba) but transfer to our specific frequency set is non-trivial.
3. **Gap A**: small-$H$ effectiveness. This is *the* chokepoint in different guise — equivalent to a per-$h$ structural bound on $T_h$, which is the original problem.

### 5.4. What this route actually delivers

Even *fully completing* §5.3 with both HE-$2k$ and Gap A delivers Lemma 3.4 only conditional on those substantial inputs. The contribution of this P# is *not* a self-contained proof, but a **decomposition of the chokepoint into named, separately-attackable sub-tasks**. The route's value is in providing:

- A clean small-$H$ obstacle (Gap A) that previous Halász/Hooley framings hid.
- An additive-combinatorial sub-task (HE-4) with explicit divisor/Diophantine structure.
- A clear conditional path from these to Lemma 3.4 in $L^p$-density form (already strictly more useful than the Cesaro mean of Theorem F.2).

## 6. Structure of HE-4 — what would a proof look like?

The equation $\beta_1 + \beta_2 \equiv \beta_3 + \beta_4 \pmod 1$ unpacks to
$$
N \!\Big( \frac{1}{e_1} + \frac{1}{e_2} - \frac{1}{e_3} - \frac{1}{e_4} \Big) \;+\; \big( \alpha_{\epsilon_1}(e_1) + \alpha_{\epsilon_2}(e_2) - \alpha_{\epsilon_3}(e_3) - \alpha_{\epsilon_4}(e_4) \big) \;\equiv\; 0 \pmod 1.
$$

Two separate pieces. Note:

- The **integer-ratio term** $N(1/e_1 + 1/e_2 - 1/e_3 - 1/e_4) = N \cdot (\text{something with denominator dividing } e_1 e_2 e_3 e_4)$. Generically this is a rational number of small denominator; the equation $\equiv 0 \pmod 1$ becomes a divisibility condition on $N$ vs. the $e_i$.
- The **$\alpha_\epsilon$ term** $\sum \pm r_p/p \cdot (e/p)_p^{-1}$ is a sum of CRT-spread root contributions.

**Strategic decomposition.** Let $L := \mathrm{lcm}(e_1, e_2, e_3, e_4)$. The combined sum is a fraction with denominator dividing $L$:
$$
\beta_1 + \beta_2 - \beta_3 - \beta_4 \;\equiv\; \frac{M}{L} \pmod 1, \qquad M = M(N, e_i, \epsilon_i, r_p) \in \mathbb{Z}.
$$
The equation $\equiv 0 \pmod 1$ becomes $L \mid M$. Counting solutions reduces to counting $(e_1, e_2, e_3, e_4, \epsilon, \mathrm{roots})$-tuples with $L \mid M$ — a Diophantine counting problem amenable, in principle, to standard divisor / lattice-point arguments.

**Heuristic count.** For "generic" choices of $(e_i, \epsilon_i)$, the value $M \pmod L$ is uniformly distributed in $\{0, 1, \ldots, L-1\}$, so the density of solutions is $1/L$. Summing over tuples and weighting by frequency-density:
$$
\mathsf{E}_4^{\text{generic}}(N) \;\approx\; \sum_{e_1, e_2, e_3, e_4 \le N} \frac{2^{\omega(e_1) + \omega(e_2) + \omega(e_3) + \omega(e_4)}}{L(e_1, e_2, e_3, e_4)}.
$$

For a generic 4-tuple with $L \asymp \prod e_i / \mathrm{lcm}$-savings, this density is small; the quadruple-sum collapses heuristically to $O(A(N)^2 \log^{O(1)} N)$ via standard divisor identities.

**The challenge** is making this rigorous without losing more than $\log^B$. Heath-Brown / Iwaniec-style Type-I/II decompositions on the divisor structure are candidates.

This is the natural **next chunk** for this P# (P16.1 below).

## 7. Open sub-questions

- **P16.1.** Prove HE-4 with $B = O(1)$ (any explicit constant). Heuristic argument in §6 suggests $B = 1$ should be achievable.
- **P16.2.** Verify the heuristic numerically: compute $\mathsf{E}_4(N)$ at $N \in \{50, 100, 200, 500, 1000\}$ and fit to $K^2 \log^B N$ to estimate $B$.
- **P16.3.** ~~Establish (D2) self-pair vanishing~~ — **resolved 2026-05-10** in `P16.1-HE4-D2-pairwise-coprime.md` Theorem 2: $(D2)_{\mathrm{ord}}(N) \le 3^{\omega(N^2+1)} \cdot K(N) = N^{1+o(1)}$ via the CRT reformulation $\beta_{e,a} = (N+a)/e$ with $a^2 \equiv -1 \pmod e$. (D2) coincidences are not vanishing but are sub-leading; their contribution to HE-4 is $O(N^{2+o(1)}) = K^2 \cdot N^{o(1)}$.
- **P16.4.** Higher moments HE-$2k$ for $k = 3, 4, \ldots$ — uniform bound with $B_k = O(k)$, $C_k = O(c^k k!)$, suitable for sub-Gaussian chaining.
- **P16.5.** The "for $1 - o(1)$ of $h$" output of §5.1 is *already* sufficient for some downstream applications (e.g., second-moment bounds on the discrepancy $E(N)$ averaged over $N$). What does it give for the AB framework?
- **P16.6.** Measure $C_{\mathrm{num}}^{(T)}(N)$ — the off-diagonal sin-sum for the *$T_h$* second moment — and verify the conjectural $\le N^{2+o(1)}$ envelope. The empirical $C_{\mathrm{num}}$ of `P12-Halasz-CN-empirical.md` is for the $H_h$ object and does not directly apply.
- **P16.7. (Gap A)** Establish small-$H$ effectiveness of the $2k$-moment expansions: i.e., that the off-diagonal sin-sum at fourth-power level is bounded by a quantity strictly smaller than the diagonal $H K^2$ at $H = \log^{O(1)} N$. **This is the original chokepoint in different guise** — without progress on the per-$h$ structure of $T_h$, off-diagonal will dominate. So P16.7 is *not* a separable sub-task; it is the chokepoint itself.

## 8. What this session establishes — and does not

This session does **no new mathematics on the chokepoint**. It opens P16 with a clean analytic skeleton: the trigonometric-polynomial picture, the second-moment expansion, the fourth-moment expansion as an additive energy, a Markov-on-fourth-moment density-form bound, and a sub-Gaussian chaining sketch.

**Honest framing.** The route as sketched does *not* deliver Lemma 3.4 unconditionally — and on close inspection, it *cannot* deliver it without an additional "Gap A" input (small-$H$ effectiveness of the moment expansions) which is essentially equivalent to the original chokepoint. So the route's reach is more limited than initially envisioned:

- **Conditional output 1** (HE-4 + Gap A solved): density-$1-o(1)$ form of Lemma 3.4 at small $H$.
- **Conditional output 2** (HE-$2k$ for all $k$ + Gap A solved): full Lemma 3.4.
- **Unconditional output of this session**: a clean decomposition of the chokepoint into named, separately-investigable sub-tasks (HE-4 = additive combinatorics on the frequency set; Gap A = small-$H$ moment effectiveness), with a clear conditional implication graph.

This is a strategic framework contribution. **It does NOT advance the rigorous bound on $T_h$ this session.** Per the bias profile / concrete-progress check (`PROTOCOL.md` §3), opening a new P# stub for a new direction *does* count as concrete progress — this is what option 1 (Invent) of the Phase 1 rubric provides.

**Caveat for next session.** Sub-question P16.1 (rigorous HE-4) is *the* recommended next chunk, since it is genuinely separable from Gap A and would deliver a publishable additive-combinatorics result independent of whether Gap A is ever closed.

## 9. Files

- This note.
- Inputs:
  - `P12-Th-chokepoint-status.md` — strategic context, route catalog.
  - `P12-Lemma-3-4-reduction.md` — definitions of $T_h, S_h$, the chokepoint statement.
  - `P12-Halasz-Fourier-orthogonality.md` — Theorem F.2 (the second-moment estimate of §3).
  - `P12-Halasz-CN-empirical.md` — empirical $C_{\mathrm{num}}(N) \le N^{2+o(1)}$.
  - `P12-Lemma-3-4-empirical-Th.md` — empirical $|T_h|/\sqrt N \le 1.222$.

## 10. Session log

- 2026-05-10: P16 opened. Skeleton: trig-poly picture, second-moment recap, fourth-moment as additive energy of frequency set, chaining transfer, HE-4 identified as primary open sub-task. Skeptic round 1 raised six CORE issues (conflation of $T_h$ with $H_h$ object; $K^4$/Jordan worst-case error; threshold-algebra error; §5.3 small-$H$ regime gap; (D2) coincidences not unconditionally vanishing; $K$/$A(N)$ definition mismatch). All six addressed in §1, §3, §4, §5 rewrites; §5.4, P16.6, P16.7 added to make the Gap A obstacle explicit. **Next chunk: P16.1 — rigorous bound on HE-4 via divisor-sum + CRT reduction.**

- 2026-05-10 (later session): chip-away on P16.1. Established the CRT reformulation $\beta_{e,\epsilon} = (N + a_\epsilon(e))/e \pmod 1$ where $a_\epsilon(e) \in \{0,\dots,e-1\}$ is the unique square root of $-1 \pmod e$ matching the sign vector $\epsilon$ (Lemma 1 of `P16.1-HE4-D2-pairwise-coprime.md`). Proved Theorem 2: $(D2)_{\mathrm{ord}}(N) \le 3^{\omega(N^2+1)} \cdot K(N) = N^{1+o(1)}$ — resolves sub-question P16.3. Proved Theorem 3: pairwise-coprime (D3) tuples force every $e_i \mid N^2+1$ and $a_i \equiv -N \pmod{e_i}$, hence $(D3)_{\mathrm{pwc}}(N) \le \tau(N^2+1)^4 = N^{o(1)}$. Corollary 5 reduces HE-4 to bounding $(D3)_{\mathrm{hard}}(N)$ — the not-pairwise-coprime (D3) tuples — by $K^2 \log^B N$. **Next chunk: P16.1.a/b/c per `P16.1-HE4-D2-pairwise-coprime.md` §6.**

- 2026-05-11: chunk P16.1.a executed (file `P16.1.a-S3hard-unique-prime-refinement.md`). Proved Theorem 4 (unique-prime refinement: for every prime $p$ with $|S_p((e_i))| = 1$ in a $(D3)$-tuple, $p \mid N^2 + 1$ and the unique $i$ with $p \mid e_i$ has $a_i \equiv -N \pmod p$); Corollary 7 (structural decomposition: every $(D3)$-tuple factors as $e_i = e_i^{(1)} \cdot e_i^{(\ge 2)}$ with pairwise-coprime $(e_i^{(1)})$ dividing $N^2+1$, the shared-prime part $(e_i^{(\ge 2)})$ described by a shared-prime structure $\sigma$); Theorem 5 (per-shared-prime fiber bound $\le 2^{|S_p|-1}$ via a one-line linear-algebra argument); Corollary 8 (count formula for $|S_3^{\mathrm{hard}}|$ given $\sigma$ and $(e_i^{(1)})$). Preliminary bound on the $|\mathfrak{P}_{\ge 2}| = 1$ warm-up sub-case: $N^{1+o(1)}$, sub-leading relative to the $K^2 \approx N^{2+o(1)}$ HE-4 target. **Next chunk: P16.1.b — bound the $|\mathfrak{P}_{\ge 2}| \ge 2$ regime via divisor-sum / $\tau_k$-moment identities.**

- 2026-05-11 (later): chunk P16.1.b.1 executed (file `P16.1.b.1-outer-sum-reformulation.md`). Proved Lemma 9 (canonical bijection between shared-prime structures $\sigma$ and ordered 4-tuples $(F_i)$ of squarefree integers with primes $\equiv 1 \pmod 4$ s.t. every prime in $\bigcup_i \mathrm{supp}(F_i)$ divides $\ge 2$ of the $F_i$); Theorem 6 (outer-sum reformulation $|S_3^{\mathrm{hard}}|(N) \le \mathcal{B}(N) := \sum_{(F_i) \in \mathcal{F}^*,\, F_i \le N} W(F) \tilde\Phi(N; F)$, where $W$ is the multiplicative-over-primes shared-prime weight and $\tilde\Phi$ is the count of pwc 4-tuples of $N^2+1$-divisors with box constraint $d_i \le N/F_i$); Lemma 10 (multiplicative structure of $W$; box envelope: the shared-prime mass satisfies $\prod_{p \in \mathrm{supp}} p \le N^2$). Sanity-checked $|\mathfrak{P}| = 1$ contribution recovers the P16.1.a §6 warm-up bound. Without the box constraint, $\sum_F W(F)$ would diverge as $\prod_p 37$; box constraint is essential. **Next chunk: P16.1.b.2 — prime-by-prime decoupling (dyadic Mellin envelope OR direct dyadic box decomposition).**

- 2026-05-12: chunk P16.1.b.2 executed (file `P16.1.b.2-mellin-decoupling.md`). Implemented Approach A (Mellin envelope). Proved Proposition 11 ($\widehat\Psi$ smoothing — simple pole at $s=0$ residue $1$, rapid decay on verticals via $C^\infty$ + repeated IBP), Theorem 7 (integral representation $\mathcal{B}(N) \le \frac{1}{(2\pi i)^4}\int_{(c)^4} N^{\sum s_i}\prod_i\widehat\Psi(s_i)\,\mathcal{D}_F^*(\vec s)\,\mathcal{D}_d(\vec s)\,d^4 s$ for $c > 1/2$), Lemma 12 (explicit local Euler factors $L_p(\vec s) = 1+\sum_{|S|\ge 2}2^{|S|-1}\prod_{i\in S}p^{-s_i}$ at $p\equiv 1\pmod 4$, $M_p(\vec s) = 1+\sum_i p^{-s_i}$ at $p\mid N^2+1$), Lemma 13 (closed form $L_p = \tfrac12[1+\prod_i(1+2p^{-s_i})]-\sum_i p^{-s_i}$), Theorem 8 (pair-leading-order: $\mathcal{D}_F^{\mathcal{F}}(\vec s) = \prod_{i<j}\zeta_\mathcal{Q}(s_i+s_j)^2 \cdot H(\vec s)$ with $H$ holomorphic in $\min\mathrm{Re}(s_i) > 1/3$). The six critical hyperplanes $\{s_i+s_j=1\}_{i<j}$ all meet at $\vec s = (1/2,1/2,1/2,1/2)$ where $N^{\sum s_i}=N^2$ matches the $K^2$ target scale. **Next chunk: P16.1.b.3.A — compute residue at $s_4=1-s_3$, derive 3-variable integrand.**

- 2026-05-13: chunk P16.1.b.3.A executed (file `P16.1.b.3.A-first-residue.md`). Established Lemma 14 (simple-pole structure of $\zeta_\mathcal{Q}(w)^2$ at $w=1$, residue $\kappa>0$, derived via the factorization $\zeta(w) L(w,\chi_{-4})/(\text{regular factors})$); Theorem 9 (closed-form first-hyperplane residue at $s_4 = 1-s_k$ for any $k\in\{1,2,3\}$); Theorem 10 (contour-shift identity $\mathcal{B}^\sharp(N) = \mathcal{B}^\sharp_{(c,c,c,\delta)}(N) + 3 R^{(4)}(N)$ with $\delta\in(1/3, 1-c)$, factor of 3 from $S_3$-symmetry over three coincident-real-part poles). Corrected two mis-statements in the previous session's b.2 §8 hint: a simple-pole residue gives no $\log N$, and the first $s_4$-shift catches three poles (not one). Discovered the emergent diagonal pole structure $s_1=s_3$, $s_2=s_3$ in the 3-variable residual $G^{(3)}$ — these "new" hyperplanes emerge from the $s_4\to 1-s_3$ substitution and complicate the b.3.B iteration. **Next chunk: P16.1.b.3.B — handle five poles in $s_3$ (two original-type, two diagonal, one from $\widehat\Psi(1-s_3)$ at $s_3=1$), with $s_1, s_2$ contours perturbed to push diagonal poles into the strip.**

- 2026-05-13 (later): chunk P16.1.b.3.B executed (file `P16.1.b.3.B-s3-shift.md`). Established Lemma 15 (contour-lift $s_1, s_2: (c)\to(c+\eta)$ for small $\eta>0$, valid by codim-2 generic-avoidance of the diagonal locus, no residues picked up); the lift pushes the diagonal poles $s_3=s_1, s_3=s_2$ to $\mathrm{Re}=c+\eta$, OUTSIDE the strip $[\delta,c]$ on the right, so only two original-type poles $s_3=1-s_1, s_3=1-s_2$ remain in the strip. Theorem 11 (residue at $s_3=1-s_1$ extracted in closed form: $\mathrm{Res}_{s_3=1-s_1}[\cdot] = \kappa\,\widehat\Psi(1-s_1)\widehat\Psi(s_1)\,\zeta_\mathcal{Q}(s_1+s_2)^4\zeta_\mathcal{Q}(2s_1)^2\zeta_\mathcal{Q}(s_2+1-s_1)^2\cdot H(s_1,s_2,1-s_1,s_1)\cdot\mathcal{D}_d^{(3,1)}(s_1,s_2)$). **Key structural emergence:** the $\zeta_\mathcal{Q}(s_2+1-s_3)^2$ factor collapses onto $\zeta_\mathcal{Q}(s_1+s_2)^2$ at $s_3=1-s_1$, doubling the pre-existing factor to give $\zeta_\mathcal{Q}(s_1+s_2)^4$ — a *double pole* at $s_1+s_2=1$. This realizes the $\log N$-from-coalescence prediction of b.3.A §1: the next contour shift across $s_1+s_2=1$ will produce $\log N$ from the double pole. New simple pole $s_1=1/2$ from $\zeta_\mathcal{Q}(2s_1)^2$ also emerges (inside next strip, will give $N^{1/2}$ residue). New anti-diagonal pole $s_1=s_2$ from $\zeta_\mathcal{Q}(s_2+1-s_1)^2$ handled by another lift trick. Lemma 17 ($S_2$-symmetry $R^{(4,1)} = R^{(4,2)}$ ⇒ factor of 2). Theorem 12 (contour-shift identity $R^{(4)} = R^{(4)}_\delta + 2 R^{(4,*)}$). Combined identity: $\mathcal{B}^\sharp(N) = \mathcal{B}^\sharp_{(c,c,c,\delta)}(N) + 3\,R^{(4)}_\delta(N) + 6\,R^{(4,*)}(N)$ with $6 = 3\cdot 2$ (the $S_3 \to S_2$ symmetry decay through iterative residue extraction). **Next chunk: P16.1.b.3.C — shift $s_1$-contour in $R^{(4,*)}$, extract double-pole $\log N$ residue at $s_1=1-s_2$, simple-pole residue at $s_1=1/2$, with anti-diagonal $s_1=s_2$ handled by lifting $s_2$ to $(c+2\eta)$.**

- 2026-05-13 (b.3.C): chunk P16.1.b.3.C executed (file `P16.1.b.3.C-s1-shift-logN.md`). Lemma 17 (re-stratification of $R^{(4,*)}$ to $(c+\eta)\times(c+\eta+\eta')$, anti-diagonal $s_2=s_1$ off-contour). Theorem 13 ($s_1=1/2$ simple-pole residue: $N^{3/2}$-tier integrand $\zeta_{\mathcal{Q}}(s_2+1/2)^6$). Theorem 14 ($s_1=1-s_2$ double-pole residue extracts FIRST $\log N$ via $\partial_{s_1}N^{s_1+s_2}|_{s_1=1-s_2}=N\log N$; residue $\kappa^2 N J_{\log}(s_2)[\log N+\Xi(s_2)] + 2\kappa\gamma_0 N J_{\log}(s_2)$). Theorem 15 ($R^{(4,*)} = R^{(4,*)}_{\delta'} + R^{(4,*)}_{1/2} + R^{(4,*)}_{\log}$). 5-term decomposition $\mathcal{B}^\sharp = \mathcal{B}^\sharp_{(c,c,c,\delta)} + 3R^{(4)}_\delta + 6R^{(4,*)}_{\delta'} + 6R^{(4,*)}_{1/2} + 6R^{(4,*)}_{\log}$. **Next chunk: P16.1.b.3.D — $s_2$-shift past triple/sextuple poles, extract SECOND $\log N$.**

- 2026-05-13 (b.3.D): chunk P16.1.b.3.D executed (file `P16.1.b.3.D-s2-shift.md`). Lemma 19 ($Q$ even in $u=s_2-1/2$ via $S_4$-symmetry of $H$ ⇒ $\mathrm{Res}_{s_2=1/2}J_{\log}=0$). Theorem 20 ($\Xi$ simple pole at $s_2=1/2$, residue $3/2$). **Theorem 21**: triple-pole residue of $\mathcal{F}_{1/2}=N^{s_2}\widehat\Psi(s_2)\zeta_{\mathcal{Q}}(s_2+1/2)^6 H\mathcal{D}_d^{(2,1)}$ extracts **SECOND $\log N$ at $N^2(\log N)^2$-tier**, coefficient $\frac{\kappa^6}{4}\widehat\Psi(1/2)^4 H(\vec{1/2})\prod_p[1+4p^{-1/2}]$ (strictly positive). Theorem 22 ($\mathcal{J}_0,\mathcal{J}_1$ residues finite constants; $R^{(4,*)}_{\log,\mathrm{Res}}$ has NO $\Lambda^2$ — its integrand lacks $N^{s_2}$). Theorem 23 ($s_2$-shift identity). 7-term decomposition $\mathcal{B}^\sharp = \mathcal{B}^\sharp_{(c,c,c,\delta)} + 3R^{(4)}_\delta + 6R^{(4,*)}_{\delta'} + 6R^{(4,*)}_{1/2,\delta''} + 6R^{(4,*)}_{1/2,\mathrm{Res}} + 6R^{(4,*)}_{\log,\delta''} + 6R^{(4,*)}_{\log,\mathrm{Res}}$. **§9 corrects two errors in b.3.C §8**: second-$\log N$ source is $R^{(4,*)}_{1/2,\mathrm{Res}}$ (not $R^{(4,*)}_{\log,\mathrm{Res}}$); $\zeta_{\mathcal{Q}}^6$ has order-3 pole (not order-6). **§11 central open question for b.3.E**: leading $N^2(\log N)^2$ tier is **$N^2$ above target** $N^{o(1)}(\log N)^B$; gap must close via cancellation among explicit residues (most likely route: sign-cancellation against unextracted $\Lambda^2$-piece in $\mathcal{B}^\sharp_{(c,c,c,\delta)}$). CONSENSUS-WITH-CAVEAT. **Next chunk: P16.1.b.3.E — enumerate residue tree of $\mathcal{B}^\sharp_{(c,c,c,\delta)}$ on partially-shifted contour, look for opposite-sign $\Lambda^2$-pieces.**

- 2026-05-14 (b.3.E.1): chunk P16.1.b.3.E.1 executed (file `P16.1.b.3.E.1-residue-tree.md`). Enumerated residue tree of $\mathcal{B}^\sharp_{(c,c,c,\delta)}(N)$. Three rounds of leftward shifts produce Branches A and B. Branch B's iterated residue substitution gives $\zeta_\mathcal{Q}(1/2+s_4)^6$ — identical to b.3.D's $R^{(4,*)}_{1/2}$ but with $s_4$-contour on LEFT of the triple pole. Rightward $s_4$-shift past $s_4=1/2$ (route a') extracts $\Lambda^2$ piece $-\frac{\kappa^6}{2}\widehat\Psi(1/2)^4 H(\vec{1/2})\prod_p[1+4p^{-1/2}]\cdot N^2\Lambda^2$ = exactly $1/3$ of b.3.D's $+\frac{3\kappa^6}{2}(\ldots)$. **Net $\Lambda^2$ tier $+\kappa^6(\ldots)\cdot N^2\Lambda^2$ survives** — partial cancellation $1/3$. Branch A gives sub-leading $\Lambda^1$-at-$N^2$ only. CONSENSUS-WITH-CAVEAT.

- 2026-05-14 (b.3.E.2.γ): chunk P16.1.b.3.E.2.γ executed (file `P16.1.b.3.E.2-gamma-multiplicity-audit.md`). **Multiplicity audit confirmed factor $6 = 3\times 2$ in $6R^{(4,*)}_{1/2,\mathrm{Res}}$ is structurally correct**: b.3.A factor 3 = literal pole count in $s_4$-strip ($S_3$-symmetry equates residue values, not over-count); b.3.B factor 2 = literal pole count in $s_3$-strip post-lift. b.3.D coefficient $+\frac{3\kappa^6}{2}$ stands. **Audit (γ) does NOT close the gap.** Sharpened diagnosis: the b.3.C 5-term decomposition has TWO unanalyzed-for-$\Lambda^2$ terms — $3 R^{(4)}_\delta$ (singly-residue'd, 3-fold integral, never touched) AND $6 R^{(4,*)}_{\delta'}$ (doubly-residue'd, $s_1$-shifted to $\delta'<1/2$, no $\Lambda^2$ extraction attempted). Conditional prediction: $\Lambda^2[R^{(4)}_\delta] \stackrel{?}{=} -\frac{\kappa^6}{3}\widehat\Psi(1/2)^4 H(\vec{1/2})\prod_p[\ldots]\cdot N^2\Lambda^2$ (conditional on $\Lambda^2[\mathcal{B}^\sharp]=0$ working hypothesis AND $\Lambda^2[R^{(4,*)}_{\delta'}]=0$ AND audit-α completeness; sketch §6 produces $+\kappa^6$ sign — discrepancy noted, requires rigorous derivation). Two skeptic rounds; 5 round-1 CORE issues addressed (target-bound caveat, $R^{(4,*)}_{\delta'}$ honestly marked UNANALYZED, four-question framing, sign discrepancy openly noted, audit scope narrowed). CONSENSUS-WITH-CAVEAT. **Next chunk: P16.1.b.3.E.3 — rigorously compute $\Lambda^2[R^{(4)}_\delta]$.**
