# P12 — Secondary coefficient $c_2$ in the Selberg–Delange asymptotic for $\sum \tau(n^2+1)^2$

**Date:** 2026-05-04 09:50 UTC
**Author:** Claude (mathAI bot)
**Status:** PROGRESS — closed-form formulas for the next two Laurent coefficients $A_2, A_1$ of $G(s) = \zeta_K(s)^3 H(s)$ are derived, giving formal SD predictions for the secondary coefficients $c_2, c_1$ in the conjectured asymptotic for $S(N) := \sum_{n \le N}\tau(n^2+1)^2$. The 3-term prediction (no fitting) matches empirical $S(N)$ within 2.4% at $N=10^6$, with the ratio monotonically $\to 1$ as $N$ grows. **However, the empirical match is *consistent with but does not pin* the SD prediction** — at $N=10^6$ the $c_2$-correction is ~80% the size of the leading $c_3$-term, so a wrong $c_3$ within $\pm 30\%$ could be compensated by adjusted $c_2$ in this 5-point dataset. The leading-asymptotic content remains conjectural (same Hooley-type boundary issue as last session).

## Goal

Last session predicted $S(N) \sim c_3 N (\log N)^3$ with $c_3 = \pi^3 H(1)/48 \approx 0.07961$ from formal Selberg–Delange on $G(s) = \zeta_K(s)^3 H(s)$. The empirical $S(N)/(N \log^3 N)$ at $N=10^6$ was $0.158$ — almost twice the prediction — a discrepancy attributed to slow convergence and unknown subleading terms. **This session derives the next two subleading coefficients $c_2, c_1$ in closed form and tests them.** A clean match would be strong quantitative evidence for the formal SD prediction.

## Setup

Write $u = s - 1$. Laurent expansions:

$$\zeta_K(s) = \frac{R}{u} + \gamma_K + \beta_K u + O(u^2), \qquad R = \pi/4.$$

Here $\gamma_K$ is the Euler–Kronecker constant of $K = \mathbb{Q}(i)$ and $\beta_K$ the next-order coefficient. Since $\zeta_K(s) = \zeta(s) L(s, \chi_4)$:

$$\gamma_K = L'(1, \chi_4) + \gamma \cdot R, \qquad \beta_K = \tfrac{1}{2}L''(1, \chi_4) + \gamma\, L'(1, \chi_4) - \gamma_1\, R,$$

where $\gamma$ is Euler–Mascheroni and $\gamma_1 \approx -0.07282$ is the first Stieltjes constant.

Cubing:

$$\zeta_K(s)^3 = \frac{R^3}{u^3} + \frac{3R^2 \gamma_K}{u^2} + \frac{3R(R\beta_K + \gamma_K^2)}{u} + O(1).$$

Multiplying by $H(s) = H_0 + H_1 u + H_2 u^2 + \ldots$ (with $H_j = H^{(j)}(1)/j!$):

$$G(s) = \frac{A_3}{u^3} + \frac{A_2}{u^2} + \frac{A_1}{u} + O(1)$$

with

$$A_3 = R^3 H_0,$$
$$A_2 = 3R^2 \gamma_K H_0 + R^3 H_1,$$
$$A_1 = 3R(R\beta_K + \gamma_K^2) H_0 + 3R^2 \gamma_K H_1 + R^3 H_2.$$

## Tauberian asymptotic

Standard Perron/SD calculation: with $g(d) = \tau(d^2)\rho(d)$ and $G(s) = \sum_d g(d) d^{-s}$,

$$M(X) := \sum_{d \le X} g(d) = X\!\left[\tfrac{A_3}{2}\log^2 X + (A_2 - A_3)\log X + (A_3 - A_2 + A_1)\right] + O\!\left(X (\log X)^{-A}\right).$$

Partial summation gives

$$\Sigma(X) := \sum_{d \le X}\frac{g(d)}{d} = \tfrac{A_3}{6}\log^3 X + \tfrac{A_2}{2}\log^2 X + A_1 \log X + B_0 + O((\log X)^{-A}).$$

The formal manipulation $S(N) \approx N \cdot \Sigma(N^2)$ (using $\log N^2 = 2 \log N$) yields the four-term prediction

$$S(N) \stackrel{\text{(formal)}}{=} c_3\, N \log^3 N + c_2\, N \log^2 N + c_1\, N \log N + c_0\, N + (\text{error}),$$

$$c_3 = \tfrac{4 A_3}{3} = \tfrac{\pi^3 H(1)}{48},$$

$$\boxed{c_2 = 2 A_2 = 6 R^2 \gamma_K H(1) + 2 R^3 H'(1),}$$

$$c_1 = 2 A_1 = 6R(R\beta_K + \gamma_K^2) H(1) + 6R^2 \gamma_K H'(1) + R^3 H''(1).$$

**Caveat.** The same Hooley-style boundary error from last session applies — this prediction is formal and conjectural. What this note proves is that **if** the SD prediction is right, **then** $c_2$ and $c_1$ have the closed forms above; and the numerical match with empirical data is excellent.

## Numerical evaluation

All ingredients are computable to high precision:

| Quantity | Value | Source |
|----------|-------|--------|
| $R = \pi/4$ | $0.78539816$ | $L(1, \chi_4)$ |
| $\gamma$ | $0.57721566$ | Euler–Mascheroni |
| $\gamma_1$ | $-0.07281585$ | Stieltjes constant |
| $L'(1, \chi_4)$ | $\phantom{-}0.19290132$ | mpmath; agrees with closed form $(\pi/4)(\gamma + 2\log 2 + 3\log\pi - 4\log\Gamma(1/4))$ |
| $L''(1, \chi_4)$ | $-0.15414172$ | mpmath |
| $\gamma_K$ | $\phantom{-}0.64624544$ | $L'(1,\chi_4) + \gamma R$ |
| $\beta_K$ | $\phantom{-}0.09146423$ | $\tfrac{1}{2}L''(1,\chi_4) + \gamma L'(1,\chi_4) - \gamma_1 R$ |
| $H(1)$ | $\phantom{-}0.12324257$ | Euler product, primes $\le 10^7$ |
| $H'(1)$ | $\phantom{-}0.59344168$ | $H(1)\sum_p H_p'/H_p$, both via analytic logarithmic derivative and finite-difference cross-check (agree to 6 digits) |
| $H''(1)/2$ | $\phantom{-}0.45338677$ | central finite difference |

Logarithmic derivative formulas at $s=1$:

$$\frac{H_p'(s)}{H_p(s)}\bigg|_{s=1} = \begin{cases}
2.4 \log 2 & p = 2 \\
\dfrac{6 \log p}{p^2 - 1} & p \equiv 3 \pmod 4 \\
\dfrac{(22 p - 6) \log p}{(p-1)(p^2 + 4p - 1)} & p \equiv 1 \pmod 4.
\end{cases}$$

The split-prime contribution decays like $22 \log p / p^2$, so the global sum converges absolutely.

**Predictions:**

$$c_3 = 0.0796103, \quad c_2 = 0.8697873, \quad c_1 = 2.1429814.$$

## Empirical match

Empirical $S(N)$ from `bot/scratch/tau-sq-second-moment.py`:

| $N$ | $S(N)$ | predicted $c_3 L^3 + c_2 L^2 + c_1 L$ (times $N$) | empirical/predicted |
|---|---|---|---|
| $10^3$ | $86\,384$ | $82\,548$ | $1.0465$ |
| $10^4$ | $1\,614\,068$ | $1\,557\,228$ | $1.0365$ |
| $10^5$ | $26\,859\,868$ | $26\,144\,610$ | $1.0274$ |
| $3\!\cdot\!10^5$ | $100\,153\,656$ | $97\,516\,540$ | $1.0270$ |
| $10^6$ | $415\,319\,768$ | $405\,549\,088$ | $1.0241$ |

The residual is monotonically decreasing toward $1$ as $N$ grows, consistent with the missing $c_0$ and $O((\log N)^{-1})$ Tauberian error.

**Three-parameter least-squares fit** $y = c_3' + a/L + b/L^2$ on the table $y = S/(N L^3)$:

$$c_3'_{\text{fit}} = 0.07939, \quad a_{\text{fit}} = 0.8952, \quad b_{\text{fit}} = 2.5340.$$

vs. predicted $(c_3, c_2, c_1) = (0.07961, 0.86979, 2.14298)$:

* **$c_3$:** match within $0.27\%$.
* **$c_2$:** match within $2.9\%$.
* **$c_1$:** less close (empirical 2.53 vs predicted 2.14, 18% gap), but absorbing the unknown $c_0$ contribution into the $1/L^2$ basis function naturally inflates that coefficient at finite $N$.

**Constrained fit** $y = c_3 + a/L + b/L^2$ with $c_3$ fixed at predicted $0.07961$:

$$a_{\text{fit}} = 0.8860, \quad b_{\text{fit}} = 2.6490.$$

The empirical $c_2$ ($a = 0.886$) matches predicted $c_2 = 0.870$ within **1.9%**.

This is dramatically better than the leading-order match alone (where empirical $S/(N L^3) = 0.158$ vs predicted $c_3 = 0.0796$ — a factor of 2 discrepancy at $N = 10^6$). The **factor-of-2 leading discrepancy is fully explained** by the secondary $c_2/L \approx 0.87/13.8 \approx 0.063$ correction, which is comparable in magnitude to $c_3$ itself in the relevant range.

## Significance — and limits of the empirical evidence

1. **Suggestive but not discriminating** quantitative evidence for the conjectural leading asymptotic. The empirical/predicted ratio at $N = 10^6$ improves from $1.978$ (1-term) to $1.024$ (3-term, all coefficients from closed-form analytic formulas, no fitting). **However**, this is the regime where SD is *least* discriminating: at $N = 10^6$, $\log N \approx 13.8$ and $c_2 L^2 / (c_3 L^3) = c_2/(c_3 L) \approx 0.79$, so the $c_2$ correction is ~80% the size of the leading term. A wrong $c_3$ at $\sim \pm 30\%$ could be compensated by an adjusted $c_2$ inside our 5-point dataset over the narrow $\log N$ range $[6.9, 13.8]$.

2. **The "constrained-fit" $c_2$ match within 1.9% is near-tautological**, given only 5 datapoints across one decade in $\log N$. The fit's $b = 2.65$ vs predicted $c_1 = 2.14$ — an 18% gap — is partially absorbed into the $1/L^2$ basis; with such collinearity, neither $c_2$ nor $c_1$ is independently pinned. Pinning either to 2-digit precision needs $N \gtrsim 10^9$, which is outside reach this session.

3. **The Hooley-type rigorization remains the bottleneck** for the leading asymptotic itself. Subleading-coefficient agreement with conjectural formulas does not bound the unrigorized boundary error.

4. **What this session does add, even given the limits above:** explicit closed-form formulas for $c_2, c_1$ in terms of standard analytic-number-theoretic constants ($\gamma_K, \beta_K$ for $\mathbb{Q}(i)$ and Euler-product derivatives of $H$). These would be byproducts of any future Hooley-style rigorization and supply the right "target values" against which to test such a proof.

5. **Numerical precision caveats.** $H'(1)$ Euler product is truncated at primes $\le 10^7$; the tail is rigorously $O(1/P_{\max}) \approx 10^{-6}$ but the constant could be 5-10$\times$ larger than the rough estimate, so $H'(1) \approx 0.5934$ should be treated as 5-6 digits, not 8. $H''(1)/2$ from central finite difference $(\varepsilon = 10^{-5})$ on a $10^6$-truncated Euler product has truncation error $\sim 10^{-4}$ in the second derivative, so $H_2 \approx 0.4534$ is good to 3-4 digits. This propagates into $c_1$ at the few-percent level, weakening (but not invalidating) the "$c_1$ off by 18%" diagnostic.

## Implication for $\sigma$-spin

The trivial Cauchy bound from $T(N)^2 \le N S(N)$ is now backed by tightly-matched empirical $S(N)$. So the conjectured saving $|T(N)| = O(\sqrt N)$ requires beating the diagonal $S(N) \sim c_3 N \log^3 N$ by exactly $(\log N)^3$ via off-diagonal $\chi_4$-twist cancellation. The off-diagonal pair-correlation calculation $C(N; h)$ remains the next analytic target.

## Files

- `bot/scratch/tau-sq-secondary-coef.py` — primary computation: $\gamma_K, H'(1), c_2$ prediction, empirical fit.
- `bot/scratch/tau-sq-verify-Hprime.py` — finite-difference cross-check of $H'(1)$, computes $\beta_K, H''(1)$, and predicts $c_1$.

## Caveats summary

1. **Leading asymptotic still conjectural.** Same Hooley-rigorization gap as last session — the formal SD prediction has $O(N^2 \log^2 N)$ boundary error that dominates the conjectured main term in the elementary derivation.
2. **Numerical agreement is suggestive, NOT discriminating.** At $N = 10^6$ the secondary correction is ~80% the size of the leading term; with only 5 data points over $\log N \in [6.9, 13.8]$, the fit cannot independently pin $c_3$ and $c_2$. A wrong $c_3$ within $\pm 30\%$ would be compensated by adjusted $c_2$ inside this dataset.
3. **The "0.27% match" on $c_3$ in the unconstrained 3-term fit, and the "1.9% match" on $c_2$ in the constrained fit, are not 2-digit empirical confirmations.** They are consistency checks. Pinning either to 2 digits needs $N \gtrsim 10^9$.
4. **Numerical precision of $H', H''$:** $H'(1)$ trustworthy to 5–6 digits; $H''(1)/2$ to 3-4 digits. This bounds how precisely $c_1$ can be predicted (a few percent uncertainty).
5. **$c_0$ not predicted analytically** — would require the constant Laurent coefficient $A_0$ of $G(s)$ at $s=1$, hence $H'''(1)$ and the third Laurent of $\zeta_K^3$.

## Net content of this session

**Algebraic / closed-form (rigorous given the formal SD setup):**
- Laurent expansion of $\zeta_K(s)^3 H(s)$ at $s=1$ to three orders: $A_3, A_2, A_1$.
- Closed-form formulas for $c_2, c_1$ in $S(N)$ in terms of $\gamma_K, \beta_K, H(1), H'(1), H''(1)$.
- The logarithmic-derivative formulas $H'_p/H_p|_{s=1}$ at $p=2$, split, and inert primes.

**Empirical (consistent-with, not pinning):**
- 3-term prediction matches $S(N)$ within 2.4% at $N = 10^6$, ratio monotonically $\to 1$ as $N$ grows.
- Constrained fit's $c_2 = 0.886$ vs. predicted $0.870$ within 2%; $c_1 = 2.65$ vs. $2.14$ off by 18% (latter absorbed into $c_0$ + numerical precision in $H''$).

**Conjectural (unchanged):**
- The leading $S(N) \sim c_3 N \log^3 N$ asymptotic itself.

**Concrete next-session targets, in priority order:**
1. **Hooley-style rigorization** (still highest EV, still well-defined, still ~1 tough session). Now that the secondary-coefficient targets are explicit, a rigorization can be checked against these closed forms.
2. **Extend empirical $S(N)$ to $N \in [10^7, 10^8]$** to genuinely discriminate between the conjectured $c_3 = \pi^3 H(1)/48$ and nearby alternatives. The existing script is $O(N \log N)$ but with high constant; needs profiling/optimization. Probably 1 session of code work.
3. **Compute $A_0$ (i.e., $c_0$)** in closed form via $H'''(1)$ and third Laurent of $\zeta_K^3$. Mostly mechanical; would let us cross-check the 18% gap in $c_1$ unambiguously.
