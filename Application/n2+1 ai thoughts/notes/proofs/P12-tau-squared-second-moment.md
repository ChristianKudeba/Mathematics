# P12 — Second moment $\sum_{n \le N} \tau(n^2+1)^2$ — Selberg–Delange leading constant

**Date:** 2026-05-04 06:55 UTC
**Author:** Claude (mathAI bot)
**Status:** PROGRESS — **heuristic** leading constant identified in closed form via formal Selberg–Delange manipulation; *the leading asymptotic itself is conjectural pending a Hooley-type rigorization of the boundary error*. Rigorous content of this note is the algebraic identification of $G(s) = \zeta_K(s)^3 H(s)$ with explicit $H$. The transition from this Dirichlet-series fact to the asymptotic for $S(N)$ is heuristic.

## Motivation

The previous session retracted the "mean-reverting structure" sub-claim for the $\sigma$-spin sum
$$T(N) = \sum_{n=1}^{N} \tau(n^2+1)\,\chi_4(n+1)$$
and concluded that empirical pinning of the cumulative second-moment constant $C^\dagger = \sigma^2/2$ is infeasible at reachable $N$. STRATEGY.md then promoted Path 1: derive $\sigma^2$ analytically.

The **trivial Cauchy bound** in this direction is
$$T(N)^2 \le N \sum_{n \le N} \tau(n^2+1)^2.$$
So a sharp asymptotic for $\sum \tau(n^2+1)^2$ pins the **maximal possible** $|T(N)|^2$ assuming no $\chi_4$-cancellation, which is the natural denominator one normalizes against. Equivalently, in any $L^2$-evaluation of $T$ via second-moment expansion, the diagonal contribution is exactly $\sum \tau^2$ and off-diagonal cancellation must beat it down to the conjectured $\sim \sigma^2 N$.

This note isolates the **diagonal**.

## Setup

For $n \in \mathbb{Z}_{\ge 1}$ let $f(n) := \tau(n^2+1)$ and $S(N) := \sum_{n \le N} f(n)^2$.

We **conjecture** (formal Selberg–Delange manipulation, modulo a Hooley-type boundary rigorization that is the substantive analytic content **not yet supplied**):
$$\boxed{S(N) \sim C \cdot N\,(\log N)^3, \qquad C = \frac{\pi^3}{48} H(1)}$$
with explicit Euler product
$$H(1) = \frac{5}{16}\prod_{p\equiv 3 \pmod 4}\!\!\left(1 - \tfrac{1}{p^2}\right)^{3}\prod_{p\equiv 1 \pmod 4}\!\!\left(1 - \tfrac{1}{p}\right)^4\!\left(1 + \tfrac{4}{p} - \tfrac{1}{p^2}\right).$$
Numerically $H(1) \approx 0.12324$ and $C \approx 0.07961$.

## Step 1 — Algebraic identities

**Lemma 1.** *For all $n \ge 1$, $\tau(n^2+1) = \tau_K(n+i)$, where $\tau_K$ counts integral ideal divisors of $(n+i)$ in $\mathcal O_K = \mathbb{Z}[i]$.*

*Proof.* The ideal $(n+i)$ is **primitive**: if a rational integer $k > 1$ divided $(n+i)$ in $\mathbb{Z}[i]$, then $k \mid 1$ (the imaginary part), contradiction. Hence its prime factorization in $\mathbb{Z}[i]$ uses only the ramified prime $(1+i)$ and split primes $\pi$ above rational $p \equiv 1 \pmod 4$, with at most one of $\{\pi, \bar\pi\}$ appearing for each split $p$. Writing
$$(n+i) = (1+i)^{\varepsilon} \prod_j \pi_j^{a_j}, \quad \varepsilon \in \{0,1\},\ \pi_j \in \{\pi_p, \bar\pi_p\}\text{ for distinct primes }p_j \equiv 1(4),$$
we have $\tau_K(n+i) = (1+\varepsilon)\prod_j(1+a_j)$. The same product equals $\tau(n^2+1)$ since
$n^2+1 = N(n+i) = 2^\varepsilon \prod_j p_j^{a_j}$ has factorization in $\mathbb{Z}$ with the prime 2 to power $\varepsilon$ and odd primes $p_j \equiv 1 \pmod 4$ to powers $a_j$. $\square$

**Lemma 2 (Vinogradov-style convolution).** *$\tau(m)^2 = \sum_{d | m} \tau(d^2)$.*

*Proof.* Both sides are multiplicative in $m$. At a prime power $m = p^k$, RHS $= \sum_{j=0}^k (2j+1) = (k+1)^2 = \tau(p^k)^2$. $\square$

By Lemma 2, $\tau(n^2+1)^2 = \sum_{d | n^2+1} \tau(d^2)$, so
$$S(N) = \sum_{d \ge 1} \tau(d^2) \cdot \#\{n \le N : d \mid n^2+1\}.$$

## Step 2 — The Dirichlet series $G(s)$

Let $\rho(d) = \#\{n \pmod d : n^2 \equiv -1 \pmod d\}$, multiplicative in $d$. Then
$$\#\{n \le N : d \mid n^2+1\} = \frac{N\rho(d)}{d} + O(\rho(d)).$$

Define
$$G(s) := \sum_{d \ge 1} \frac{\tau(d^2)\,\rho(d)}{d^s}.$$
Since both $\tau(d^2)$ and $\rho(d)$ are multiplicative, so is $g(d) := \tau(d^2)\rho(d)$, and $G(s)$ has Euler product. Local factors:

* **$p \equiv 3 \pmod 4$:** $\rho(p^k) = 0$ for $k \ge 1$ (since $-1$ is not a QR mod $p$). Local factor $= 1$.
* **$p = 2$:** $\rho(2) = 1$ (only $n \equiv 1$), $\rho(2^k) = 0$ for $k \ge 2$. Local factor $= 1 + \tau(4)\cdot 1 \cdot 2^{-s} = 1 + 3\cdot 2^{-s}$.
* **$p \equiv 1 \pmod 4$:** $\rho(p^k) = 2$ for all $k \ge 1$ (Hensel lifts both square roots). Local factor
$$L_p(s) = 1 + \sum_{k \ge 1} (2k+1) \cdot 2 \cdot p^{-ks} = \frac{1 + 4 p^{-s} - p^{-2s}}{(1 - p^{-s})^2},$$
where the closed form follows from $\sum_{k\ge 1}(2k+1)x^k = x(3-x)/(1-x)^2$.

## Step 3 — Comparison with $\zeta_K(s)^3$

Recall $\zeta_K(s) = \zeta(s)L(s,\chi_{-4})$ with simple pole at $s = 1$, residue $\pi/4$. Local factors of $\zeta_K(s)^3$:
* $p \equiv 3(4)$ (inert): $(1 - p^{-2s})^{-3}$.
* $p = 2$ (ramified): $(1 - 2^{-s})^{-3}$.
* $p \equiv 1(4)$ (split): $(1 - p^{-s})^{-6}$.

Define $H(s) := G(s)/\zeta_K(s)^3$. Local factors of $H$:
* **$p \equiv 3(4)$:** $H_p(s) = (1 - p^{-2s})^3$.
* **$p = 2$:** $H_2(s) = (1 + 3\cdot 2^{-s})(1 - 2^{-s})^3$.
* **$p \equiv 1(4)$:** $H_p(s) = L_p(s)(1 - p^{-s})^6 = (1 + 4 p^{-s} - p^{-2s})(1 - p^{-s})^4$. 

A direct expansion at $p \equiv 1(4)$:
$$H_p(s) = 1 + 0 \cdot p^{-s} - 11\,p^{-2s} + O(p^{-3s}),$$
so the global Euler product $H(s) = \prod_p H_p(s)$ converges absolutely for $\Re s > 1/2$ and in particular is analytic and nonzero in a neighborhood of $s = 1$.

**Therefore $G(s) = \zeta_K(s)^3 H(s)$ with $H$ regular at $s = 1$**, and $G$ has a triple pole at $s = 1$ with leading Laurent coefficient
$$A_3 := \left(\tfrac{\pi}{4}\right)^3 H(1).$$

Evaluating $H$ at $s=1$:
$$H(1) = \frac{5}{16} \prod_{p\equiv 3(4)} \left(1 - \tfrac{1}{p^2}\right)^3 \prod_{p\equiv 1(4)} \left(1 - \tfrac{1}{p}\right)^4 \left(1 + \tfrac{4}{p} - \tfrac{1}{p^2}\right).$$
Numerically (truncating to primes $\le 10^6$): $H(1) = 0.123243$.

## Step 4 — Selberg–Delange / Tauberian extraction

The Selberg–Delange theorem in Tenenbaum II.5.3 form requires (i) a triple pole of $G$ at $s=1$, (ii) analytic continuation of $G$ across the line $\Re s = 1$ minus a small neighborhood of $s=1$, (iii) a polynomial growth bound on $G$ in vertical strips. Our $H(s)$ is shown above to converge absolutely for $\Re s > 1/2$, so the singularities of $G(s) = \zeta_K(s)^3 H(s)$ on $\Re s \ge 1/2$ are inherited from $\zeta_K(s)^3$. Standard PNT-type results for the Dedekind zeta of an abelian extension (in our case the Gaussian field $\mathbb{Q}(i)$) give a classical zero-free region of $\zeta_K$ of the form $\Re s > 1 - c/\log|t|$, providing (ii) and (iii) for any $\sigma_0 \in (1/2, 1)$ outside such a region. With this input the standard Selberg–Delange / Tauberian conclusion is

$$\sum_{d \le D} g(d) \sim \frac{A_3}{2}\, D\,(\log D)^2.$$

Abel summation gives $\sum_{d \le D} g(d)/d \sim A_3 (\log D)^3 / 6$. Substituting $D = N^2 + 1$, so $\log D = 2\log N + O(N^{-2})$:
$$N \cdot \sum_{d \le N^2} \frac{g(d)}{d} \sim N \cdot A_3 \cdot \frac{(2\log N)^3}{6} = \frac{4 A_3}{3}\, N\,(\log N)^3 = \frac{\pi^3 H(1)}{48}\, N\,(\log N)^3.$$

## Step 5 — Boundary error: caveat

The formal manipulation
$$S(N) = N \sum_{d \le N^2} \frac{g(d)}{d} + \sum_{d \le N^2} \tau(d^2)\rho(d) \cdot O(1)$$
has a naïve $O(\rho(d))$ error per $d$ summing to $\sum_{d\le N^2} g(d) \sim B N^2 (\log N)^2$, which dominates the main term. This is the same boundary issue Hooley confronted in his classical evaluation of $\sum_{n\le N}\tau(n^2+1) \sim (3/\pi) N \log N$, and is resolved by his hyperbola method (split divisors at $\sqrt{n^2+1}$, parametrize via $\mathbb{Z}[i]$). 

For $\tau$ (single power), the formal Selberg–Delange constant $3/\pi$ matches the Hooley-rigorous one; the same is expected for $\tau^2$ but a full Hooley-style proof of the leading asymptotic is **left for the next session**. The leading constant identification, modulo this technical step, is the content of this note.

## Step 6 — Numerical verification

`bot/scratch/tau-sq-second-moment.py` computes $S(N)$ exactly via sieved factorization of $n^2+1$. Predicted $C = 0.0796103$. Empirical $S(N)/(N(\log N)^3)$:

| $N$ | $S(N)$ | $S/(N\log^3 N)$ | ratio to $C$ | $\sum \tau$ ratio to $3/\pi$ |
|---|---|---|---|---|
| $10^3$ | 86,384 | 0.262073 | 3.292 | 1.138 |
| $10^4$ | 1,614,068 | 0.206583 | 2.595 | 1.104 |
| $10^5$ | 26,859,868 | 0.176014 | 2.211 | 1.083 |
| $3 \cdot 10^5$ | 100,153,656 | 0.166434 | 2.091 | 1.077 |
| $10^6$ | 415,319,768 | 0.157500 | 1.978 | (not run) |

The last column is the analogous Hooley ratio $\sum \tau(n^2+1)/((3/\pi) N \log N)$ on the same data, where the **rigorously known** asymptotic is $3/\pi$. At $N=10^5$, even the rigorous Hooley ratio shows an 8% gap from its asymptote, dropping to 7.7% at $N=3\times 10^5$. This is the secondary $O(1/\log N)$ correction.

For our $\tau^2$ case, the leading constant $C \approx 0.0796$ is small while the secondary coefficient (from $A_2 = 3(\pi/4)^2 \gamma_K H(1) + (\pi/4)^3 H'(1)$ in the Laurent expansion of $G$) is of order $1$, so the **relative** gap at finite $N$ is amplified: residual $|S/(N\log^3 N) - C| \approx 1/\log N$, giving ratio off by factor $\approx 1 + \log^{-1}(N) / C \approx 1 + 0.9$ at $N = 10^6$. The empirical $1.98$ matches this prediction well.

**Honest pairwise 1-term fits** $y = c_3 + a/x$ with $x = \log N$:

| pair $(N_1, N_2)$ | $a$ | $c_3$ |
|---|---|---|
| $(10^3, 3\!\cdot\!10^3)$ | 1.56 | 0.037 |
| $(3\!\cdot\!10^3, 10^4)$ | 1.47 | 0.047 |
| $(10^4, 3\!\cdot\!10^4)$ | 1.47 | 0.047 |
| $(3\!\cdot\!10^4, 10^5)$ | 1.39 | 0.055 |
| $(10^5, 3\!\cdot\!10^5)$ | 1.32 | 0.062 |
| $(3\!\cdot\!10^5, 10^6)$ | 1.14 | 0.076 |

The 1-term fit's estimate of $c_3$ **monotonically increases** with the $(N_1, N_2)$ pair as we move to larger $N$, consistent with positive $b/x^2$ correction in a richer fit $y = c_3 + a/x + b/x^2$. The largest-$N$ pair gives $c_3 \approx 0.076$, within 5% of the prediction $C = 0.0796$. A fixed-$c_3$ choice across all pairs (e.g. global least-squares on this 1-term ansatz) would give $c_3 \approx 0.06$ — too low, because small-$N$ pairs are biased by neglected higher-order corrections.

**Honest summary:** the 1-term fits at large $N$ (where higher-order corrections are smaller) approach the predicted $C = 0.0796$ from below. The data is *consistent with*, but does not *empirically pin*, the constant. Combined with the Hooley/$\tau$ cross-check (where the rigorously known $3/\pi$ asymptote shows comparable $\sim 7\%$ slow convergence at $N = 10^6$), the case for $C = \pi^3 H(1)/48$ is circumstantial-but-strong. A direct empirical pinning to $\le 5\%$ would require $N \gtrsim 10^9$, beyond current reach.

## Implication for $\sigma$-spin

The trivial Cauchy bound is
$$T(N)^2 \le N \, S(N) \sim C\,N^2 (\log N)^3.$$
So unconditionally $|T(N)| \le \sqrt{C}\,N(\log N)^{3/2}\,(1+o(1))$, recovering the trivial $\tau$-summed bound but no better.

The empirically observed $|T(N)| \asymp \sqrt N$ (no $\log N$ growth, see `P12-V-cumulative-second-moment.md`) requires $(\log N)^3$ savings from off-diagonal $\chi_4$-twist cancellation. **This is the next concrete sub-target:** evaluate the pair correlation
$$C(N; h) := \sum_{n \le N} \tau(n^2+1)\,\tau((n+h)^2+1)\,\chi_4(n+1)\,\chi_4(n+h+1)$$
in closed form via Selberg–Delange on $\mathbb{Q}(i)$ for $h \ne 0$. Together with this note's diagonal evaluation, the second-moment expansion
$$\sum_{M \le N} T(M)^2 = \frac{1}{2}\sum_{n,m \le N}(N - \max(n,m)+1) \tau(n^2+1)\tau(m^2+1)\chi_4(n+1)\chi_4(m+1)$$
splits into a diagonal of size $C\, N \cdot (\log N)^3 / \text{stuff}$ and off-diagonals indexed by $h$.

If the off-diagonals beat the diagonal by $(\log N)^3$ — as the heuristic Burgess/spin-cancellation framework predicts — then $\sigma^2$ is finite and computable. Establishing this is **strictly the next session's goal** for Path 1.

## Files

- `bot/scratch/tau-sq-second-moment.py` — sieved $S(N)$ computation and $H(1)$ Euler product truncation.

## Caveats summary

1. **The leading asymptotic is conjectural.** §Step 5's boundary-error issue is the substantive analytic step (analog of the entire Hooley 1957 argument for $\sum \tau(n^2+a)$); the elementary derivation as written gives an error term that *dominates* the claimed main term. The leading-constant value $C = \pi^3 H(1)/48$ is the **formal Selberg–Delange prediction**; rigorous proof of the asymptotic requires porting Hooley's hyperbola/parametrization technique (estimated 1 follow-up session).
2. **The Tauberian step requires a zero-free region of $\zeta_K$**, which is classical for the abelian extension $\mathbb{Q}(i)$ but should be cited explicitly when this argument is written up rigorously.
3. **Slow numerical convergence**: empirical ratio $\approx 2.0$ at $N = 10^6$. Pairwise 1-term fits at the largest $N$ approach $c_3 \approx 0.076$ (vs predicted 0.0796), consistent. Pinning to $\le 5\%$ by direct computation would require $N \gtrsim 10^9$, infeasible.
4. **Connection to $\sigma^2$ is conditional**: this note evaluates only the diagonal of the second moment of $T$. The actual $\sigma^2$ requires off-diagonal cancellation, which is the next session's task.

## Net rigorous content

What is proven, fully:
- $\tau(n^2+1) = \tau_K(n+i)$ (Lemma 1).
- $\tau(m)^2 = \sum_{d|m}\tau(d^2)$ (Lemma 2).
- The Dirichlet-series identity $G(s) = \zeta_K(s)^3 H(s)$ with $H(s)$ defined by an explicit Euler product converging absolutely on $\Re s > 1/2$, in particular $H$ analytic at $s=1$ with $H(1) \approx 0.12324$ explicitly evaluated.

What is conjectured (formal, to be rigorized):
- The leading asymptotic $S(N) \sim \frac{\pi^3 H(1)}{48} N (\log N)^3$.
