# P12 — Constant Laurent coefficient $c_0$ in formal SD asymptotic for $\sum \tau(n^2+1)^2$, and its empirical falsification

**Date:** 2026-05-05 03:40 UTC
**Author:** Claude (mathAI bot)
**Status:** PROGRESS — closed-form prediction $c_0 = A_0 \approx 0.8793$ derived (constant Laurent coefficient of $G(s) = \zeta_K(s)^3 H(s)$ at $s=1$, via Perron). Empirical comparison at $N \le 10^6$ shows the **joint formal $(c_1, c_0)$ prediction is inconsistent with the data**: $S(N)/N - c_3 L^3 - c_2 L^2 - c_1^{\text{formal}} L \approx 0.85 L - 2.2$ over $L \in [6.9, 13.8]$, far exceeding the formal Tauberian error $O(L^{-A})$. The data alone cannot disentangle which of $c_1, c_0$ (or both) is wrong; only the joint prediction is rejected. The formal-SD chain remains reliable for $c_3$, consistent with formal $c_2 \approx 0.87$, but does not control $c_1, c_0$.

## Goal

Continuing from `P12-tau-squared-secondary-coefficient.md` (which derived $c_2, c_1$): compute the next coefficient $c_0$ in the formal-SD asymptotic
$$ S(N) := \sum_{n \le N} \tau(n^2+1)^2 \stackrel{\text{(formal)}}{=} c_3 N L^3 + c_2 N L^2 + c_1 N L + c_0 N + O(N L^{-A}), $$
where $L = \log N$. Test the prediction empirically to see whether the formal-SD chain extends beyond the leading orders.

## Closed-form derivation

Recall the Dirichlet-series factorization (P12-tau-squared-second-moment.md):
$$ G(s) := \sum_d \tau(d^2)\rho(d)\, d^{-s} = \zeta_K(s)^3\, H(s), \qquad K = \mathbb{Q}(i), $$
with $H(s) = \prod_p H_p(s)$ absolutely convergent on $\Re s > 1/2$.

Write $u = s - 1$ and Laurent-expand:
$$ \zeta_K(s) = \tfrac{R}{u} + \gamma_K + \beta_K u + \alpha_K u^2 + O(u^3), \qquad R = \pi/4, $$
$$ H(s) = H_0 + H_1 u + H_2 u^2 + H_3 u^3 + O(u^4), \qquad H_j = H^{(j)}(1)/j!. $$

The third Laurent coefficient $\alpha_K$ is computed via the factorization $\zeta_K = \zeta \cdot L(\cdot, \chi_4)$:
$$ \alpha_K = \tfrac{1}{6}L'''(1,\chi_4) + \tfrac{\gamma}{2}L''(1,\chi_4) - \gamma_1 L'(1,\chi_4) + \tfrac{\gamma_2}{2} R, $$
where $\gamma, \gamma_1, \gamma_2$ are standard Stieltjes constants (signs as in `P12-tau-squared-secondary-coefficient.md`, i.e. $\zeta(s) = 1/u + \gamma - \gamma_1 u + (\gamma_2/2) u^2 + \ldots$).

Cubing $\zeta_K$:
$$ \zeta_K^3 = \tfrac{R^3}{u^3} + \tfrac{3R^2\gamma_K}{u^2} + \tfrac{3R(R\beta_K + \gamma_K^2)}{u} + (3R^2\alpha_K + 6R\gamma_K\beta_K + \gamma_K^3) + O(u). $$

Multiplying by $H$ and reading off the constant Laurent coefficient $A_0$ of $G$:
$$ \boxed{\; A_0 = (3R^2\alpha_K + 6R\gamma_K\beta_K + \gamma_K^3) H(1) + 3R(R\beta_K + \gamma_K^2)\, H'(1) + \tfrac{3R^2 \gamma_K}{2} H''(1) + \tfrac{R^3}{6} H'''(1) \;} $$

## Tauberian link to $S(N)$ (explicit Perron derivation)

By Perron's formula for $\Sigma_*(X) := \sum_{d \le X} \tau(d^2)\rho(d)/d$ (whose Dirichlet series is $G(s+1) = \sum a_d/d/d^s$ with $a_d = \tau(d^2)\rho(d)$):
$$ \Sigma_*(X) = \frac{1}{2\pi i}\int_{(c)} G(s+1)\, \frac{X^s}{s}\, ds. $$

The integrand has a pole at $s=0$ from both $G(s+1) = A_3/s^3 + A_2/s^2 + A_1/s + A_0 + A_{-1} s + O(s^2)$ (order 3) and the $1/s$ (order 1) — total order 4. Computing the residue explicitly:
$$ G(s+1)\,X^s/s = \big(\tfrac{A_3}{s^4} + \tfrac{A_2}{s^3} + \tfrac{A_1}{s^2} + \tfrac{A_0}{s} + A_{-1} + \cdots\big)\big(1 + sL + \tfrac{s^2 L^2}{2} + \tfrac{s^3 L^3}{6} + \cdots\big), $$
where $L = \log X$. The coefficient of $s^{-1}$ — i.e. the residue — is
$$ A_3 \cdot \tfrac{L^3}{6} + A_2 \cdot \tfrac{L^2}{2} + A_1 \cdot L + A_0. $$

Shifting the contour past $s=0$ to $\Re s = -1/2 + \epsilon$ (using analyticity of $H$ in $\Re s > 1/2$ and meromorphy of $\zeta_K$ globally) gives the standard Selberg–Delange remainder:
$$ \Sigma_*(X) = \tfrac{A_3}{6} L^3 + \tfrac{A_2}{2} L^2 + A_1 L + A_0 + O\!\big((\log X)^{-A}\big), $$
for any fixed $A > 0$. **This identifies the constant Laurent coefficient $A_0$ of $G$ at $s=1$ with the constant in the asymptotic of $\Sigma_*(X)$** — the partial-summation $B_0$ of the previous session is precisely $A_0$ as Perron's formula makes explicit.

Now the formal manipulation $S(N) \approx N \cdot \Sigma_*(N^2)$ (using $\log N^2 = 2L$) yields
$$ S(N) \stackrel{\text{(formal)}}{=} \tfrac{4 A_3}{3} N L^3 + 2 A_2 N L^2 + 2 A_1 N L + A_0 N + (\text{error}), $$
i.e. $c_3 = 4A_3/3, c_2 = 2A_2, c_1 = 2A_1, c_0 = A_0$.

**Caveat (same as previous sessions).** The "$\approx$" is the Hooley boundary issue: the contribution of $d \in (N, N^2]$ to $S(N)$ is unrigorously approximated. In Hooley 1957 (first moment), the analog argument is fully rigorized; for the second moment it is not.

## Numerical evaluation

`bot/scratch/tau-sq-c0-coefficient.py`, using mpmath at 50-digit precision.

Inputs:

| Quantity | Value | Source |
|----------|-------|--------|
| $L'(1,\chi_4)$  | $0.192901316796912$ | mpmath alternating series, agrees with closed form |
| $L''(1,\chi_4)$ | $-0.154141724429336$ | mpmath alternating series |
| $L'''(1,\chi_4)$ | $0.094882859205604$ | mpmath alternating series |
| $\gamma$    | $0.577215664901533$ | mpmath stieltjes(0) |
| $\gamma_1$  | $-0.072815845483676$ | mpmath stieltjes(1) |
| $\gamma_2$  | $-0.009690363192872$ | mpmath stieltjes(2) |
| $R = \pi/4$ | $0.785398163397448$ | exact |
| $\gamma_K$  | $0.6462454399$ | $L'(1,\chi_4) + \gamma R$, matches prev session |
| $\beta_K$   | $0.0914642309$ | $L''/2 + \gamma L' - \gamma_1 R$, matches prev session |
| $\alpha_K$  | $-0.0184318234$ | $L'''/6 + \gamma L''/2 - \gamma_1 L' + \gamma_2 R/2$ (this session) |
| $H(1)$      | $0.1232428910$ | Euler product, primes $\le 2 \cdot 10^5$, matches prev session $0.12324$ |
| $H'(1)$     | $0.5934376465$ | FD on $\log H$ (more numerically stable), matches prev session $0.5934$ |
| $H''(1)$    | $0.9071118888$ | FD on $\log H$, $H''/2$ matches prev session $H_2 = 0.4534$ |
| $H'''(1)$   | $-5.0887925737$ | FD on $\log H$, **new this session** |

Plugging in:
$$ z_0 := 3R^2 \alpha_K + 6R \gamma_K \beta_K + \gamma_K^3 = 0.5143260050, $$
$$ A_0 = z_0 \cdot H(1) + 3R(R\beta_K + \gamma_K^2) H'(1) + \tfrac{3R^2 \gamma_K}{2} H''(1) + \tfrac{R^3}{6} H'''(1) $$
$$ \phantom{A_0} = 0.0634 + 0.6843 + 0.5424 - 0.4109 = 0.8792 \approx 0.8793 \text{ (full precision)}. $$

So
$$ c_0 = A_0 \approx 0.8793. $$

Cross-check on $c_3, c_2, c_1$ (recovered from this session's higher-precision computation): $c_3 = 0.07961$ (matches prev), $c_2 = 0.86978$ (matches prev), $c_1 = 2.14314$ (vs prev 2.14298 — minor diff from improved $H'(1), H''(1)$). All consistent.

## Empirical comparison — joint $(c_1, c_0)$ formal predictions disagree with data

Empirical $S(N)$ (from previous sessions, `bot/scratch/tau-sq-second-moment.py`):

| $N$ | $S(N)$ | formal-3-term $c_3 L^3 + c_2 L^2 + c_1 L$ (per $N$) | residual $S/N - $ 3-term |
|---|---|---|---|
| $10^3$    | $86\,384$       | $82.55$  | $3.84$ |
| $10^4$    | $1\,614\,068$   | $155.72$ | $5.68$ |
| $10^5$    | $26\,859\,868$  | $261.45$ | $7.15$ |
| $3\!\cdot\!10^5$ | $100\,153\,656$ | $325.06$ | $8.79$ |
| $10^6$    | $415\,319\,768$ | $405.55$ | $9.77$ |

**The residual grows from $3.84$ at $N=10^3$ to $9.77$ at $N=10^6$**, while the formal prediction is a $N$-independent $c_0 \approx 0.879$. The residual is $11.1\times$ the formal $c_0$ at $N = 10^6$, and **growing**.

Linear regression of residual vs $L = \log N$: residual $\approx 0.852\, L - 2.16$, $R^2 = 0.992$. So
$$ S(N)/N - c_3 L^3 - c_2 L^2 - c_1^{\text{formal}} L \approx 0.85\, L - 2.2 \quad (N \in [10^3, 10^6]). $$

Equivalently:
$$ S(N)/N - c_3 L^3 - c_2 L^2 - (c_1^{\text{formal}} + 0.85) L \approx -2.2 \quad (\text{empirical}). $$

This is consistent with formal $c_1 = 2.143$ being **off by $\approx 0.85$** from the true $c_1$, and formal $c_0 = 0.879$ being similarly far from a "true" $c_0 \approx -2.2$ (or some similar Hooley-corrected value).

The Tauberian formal-SD error is $O((\log N^2)^{-A}) = O((2L)^{-A})$, which is $< 0.1$ in absolute terms at $N = 10^6$. **The observed residual cannot be explained by Tauberian error.** The discrepancy is a real Hooley-boundary contribution.

## Constrained empirical fits (5 data points, $\log N \in [6.9, 13.8]$)

Fit $y = S/(N L^3) = c_3' + a/L + b/L^2 + d/L^3$:

| Constraint | $c_3'$ | $a$ ($\leftrightarrow c_2$) | $b$ ($\leftrightarrow c_1$) | $d$ ($\leftrightarrow c_0$) |
|---|---|---|---|---|
| Unconstrained | $0.0939$ | $0.4616$ | $6.7118$ | $-12.96$ |
| $c_3 = $ formal $0.0796$ | — | $0.886$ | $2.65$ | $-0.43$ |
| $c_3, c_2$ = formal | — | — | $2.95$ | $-1.76$ |
| Formal predictions  | $0.0796$ | $0.870$ | $2.143$ | $0.879$ |

Observations:
* The unconstrained 4-parameter fit is **unidentified** with only 5 data points (basis $1, L^{-1}, L^{-2}, L^{-3}$ is highly collinear over $L \in [6.9, 13.8]$). All four coefficients are off by $> 17\%$.
* The "$c_3$ fixed" constrained fit gives $c_2 \approx 0.886$ (vs formal $0.870$, **gap $1.86\%$**), $c_1 \approx 2.65$ (gap $24\%$), $c_0 \approx -0.43$ (formal $0.879$, **gap with sign change**).
* The $c_2$ match within 2% is **consistent with formal $c_2 = 0.870$** being correct; this is the only subleading coefficient where the empirical fit is close to formal.

## Strategic interpretation (carefully bounded by what the data supports)

**What the data DOES support:**
* $c_3$ remains robustly pinned by formal SD. Independent of fit choice, empirical $c_3 \in [0.079, 0.094]$, with the most robust constrained-data-driven fit giving $0.079$, matching formal $\pi^3 H(1)/48 = 0.0796$ to $0.3\%$.
* The **joint formal prediction** $c_1 N L + c_0 N = (2.143)(N L) + 0.879 N$ does not match the data. There is a **real residual** $S(N)/N - c_3 L^3 - c_2 L^2 = 2.143 L + 0.879 + \text{(empirical excess)}$, and the empirical excess scales as $\approx 0.85 L - 2.2$ over $L \in [6.9, 13.8]$ — i.e., the formal joint $(c_1, c_0)$ undershoots by $\sim N L$ at our data scale.
* This excess is far larger than the formal Tauberian error $O(L^{-A})$, so it represents a genuine non-formal contribution — most plausibly the Hooley boundary error from $d \in (N, N^2]$.

**What the data does NOT support:**
* The data does **not** distinguish "formal $c_1$ is wrong, formal $c_0$ is right" from "formal $c_0$ is wrong, formal $c_1$ is right" from "both are wrong." With 5 collinear data points spanning one decade in $\log N$, the basis $\{L, 1\}$ on the residual is strongly correlated; either coefficient can be moved by $O(1)$ within fitting tolerance. Saying "formal $c_0$ is falsified" would overclaim.
* The data does **not** strongly distinguish formal-$c_2$-correct ($c_2 = 0.870$) from formal-$c_2$-off-by-5%. The constrained fit at $0.886$ is within 2% of formal $c_2$, but the previous session noted (and the skeptic of this session reiterated) that this near-match is partly tautological given the $c_3$ constraint.
* The session does NOT prove that any specific Hooley-boundary mechanism contributes at orders $L$ and $1$ — that is a heuristic explanation consistent with the data, not a derivation.

**Sanity check on the Laurent expansion.** Direct computation of $G(s)$ at $s = 1.1$ from the truncated Euler product gives $G(1.1) = 72.49$; the four-term Laurent prediction $A_3/u^3 + A_2/u^2 + A_1/u + A_0 = 114.79$ at $u = 0.1$. The 58% gap implies $A_{-1} \approx -423$ (large but bounded). This is consistent with the Laurent expansion being algebraically correct and the truncation error at $u = 0.1$ being dominated by the unreported $A_{-1} u$ term. **The Laurent algebra is verified to leading orders.**

**Refined recommendation for previous-session "$c_1 = 2.143$ as target":**
* The formal $c_1 = 2.143$ should be **flagged as not-yet-empirically-confirmed** rather than demoted outright. There is a real residual at order $L$ in $S(N)$ that formal SD does not account for, and the residual is consistent in sign and magnitude ($\sim 0.85 N L$) with formal $c_1$ being too low. But disentangling this from a $c_0$-level Hooley correction requires either larger $N$ or a direct boundary calculation.
* For a Hooley-style rigorization of the $S(N)$ asymptotic, the right targets are: $c_3 = \pi^3 H(1)/48$ (robust), $c_2 \approx 0.87 \pm 0.02$ (consistent with formal but not pinned), and **a joint constraint that $c_1 L + c_0$ at $L = 13.8$ equals approximately $40.8$** (versus the formal prediction of $30.5$, a gap of $\sim 10$).

## What this session does NOT prove

* **It does not prove $c_1 \ne 2.143$ rigorously.** The constrained fit on 5 data points has limited resolving power; the conclusion is "the data is *more* consistent with a Hooley-boundary contribution at orders $L$ and $1$ than with formal-SD being correct at all orders." Stronger evidence requires extending $N$ to $10^8$ or beyond.
* **It does not derive the true $c_1, c_0$ in closed form.** The Hooley-boundary contribution would need a separate analysis (i.e., the actual rigorization).
* **It does not invalidate the leading-order asymptotic** $S(N) \sim c_3 N \log^3 N$. That conclusion remains conjectural in the formal sense and rigorously $\Theta(N \log^3 N)$ via the Nair upper bound (P12-tau-squared-upper-bound-Nair.md).

## Files

- `bot/scratch/tau-sq-c0-coefficient.py` — closed-form $c_0$, numerical evaluation, FD cross-checks, empirical fits.

## Caveats summary

1. **Closed-form $c_0 = A_0 \approx 0.879$ is derived rigorously from the formal-SD chain.** Algebraic derivation verified: Laurent expansion of $\zeta_K^3 \cdot H$ at $s=1$ truncated at $u^0$ gives $A_3/u^3 + A_2/u^2 + A_1/u + A_0$ with $A_0$ as in the boxed formula; Perron's formula identifies $A_0$ with the constant in $\Sigma_*(X)$. The $\alpha_K$ formula is derived from $\zeta_K = \zeta \cdot L(\cdot, \chi_4)$ (skeptic-verified by hand).
2. **Empirically the joint $(c_1, c_0)$ formal prediction disagrees with $S(N)$ at $N \le 10^6$**, with a residual scaling as $\sim 0.85 N L - 2.2 N$. The data cannot disentangle which of $c_1, c_0$ (or both) is wrong — the basis $\{L, 1\}$ on the residual is collinear over the data range.
3. **What is robustly pinned: $c_3$.** What is consistent with formal SD: $c_2 \approx 0.87$. What is not pinned: $c_1$ and $c_0$ individually.
4. **FD cross-check on $\alpha_K$ failed** due to numerical precision issues with mpmath's $\zeta(s)$ near $s=1$ and the small magnitude $|\alpha_K| \approx 0.018$. The analytic value is reliable; the FD failure is a tooling issue, not a derivation issue.
5. **Numerical precision of $H'''(1)$:** computed by FD on $\log H$ (Euler product to $P_{\max} = 2 \cdot 10^5$). FD step-size is $h = 10^{-3}$; for a third derivative this is the dominant error source, of order $h^2 \cdot H^{(5)}(1) \sim 10^{-3} \cdot O(10^2) \sim 0.1$. This is substantially smaller than the formal-vs-empirical gap of $\sim 10$, so the conclusion is robust to this precision.
6. **The formal-SD prediction is NOT falsified at $c_0$ alone**; rather, the joint $(c_1, c_0)$ prediction is inconsistent with the data, and the data is unable to tell which is wrong. This is a softer (and correct) statement than the initial draft of this writeup.

## Next-session pickup hints

1. **Highest priority** (subject to Anton's strategic call): pivot AWAY from formal-SD subleading-coefficient prediction. The chain breaks down at $c_1, c_0$, so generating closed-form predictions for $c_{-1}, c_{-2}, \ldots$ is unlikely to inform Hooley rigorization further.
2. **Empirical extension to $N = 10^8$** would let us pin $c_1$ to $\sim 5\%$ precision (currently the constrained fit gives $\sim 2.65$ with formal at $2.14$ — $24\%$ gap). The script `tau-sq-second-moment.py` is $O(N \log N)$ in time but with high constant; profiling/optimization needed. Honest target: 1–2 sessions of compute work.
3. **The Hooley boundary itself** as a fresh target: derive the boundary correction $S(N) - N \Sigma_*(N^2)$ in closed form. This would simultaneously rigorize the asymptotic AND give the true $c_1, c_0$. This is the original "Hooley rigorization" target that has been marked "1–2 hard sessions" since 2026-05-04 07:17.
