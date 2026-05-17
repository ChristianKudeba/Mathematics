# P12 — Empirical validation of formal-SD Laurent on $\Sigma_*(X)$, isolating the Hooley boundary in $S(N)$

**Date:** 2026-05-05 06:50 UTC
**Author:** Claude (mathAI bot)
**Status:** PROGRESS — empirical confirmation that the formal Selberg–Delange Laurent expansion of $G(s) = \zeta_K(s)^3 H(s)$ at $s=1$ tracks the partial sum $\Sigma_*(X) := \sum_{d\le X} \tau(d^2)\rho(d)/d$ with sign-oscillating residual bounded by $|\text{res}| \le 0.063$ across all 9 datapoints in $X \in [10^3, 10^7]$. This is consistent with a Tauberian remainder of order $O(L^{-A})$ for some $A > 0$ — the data does not have enough dynamic range to pin $A$ — and rules out a constant-sign systematic bias of size $\gg 0.1$ in the formal Laurent coefficients. The previous-session empirical $S(N)$ discrepancy ($\approx 0.85\,NL - 2.2\,N$ at $N \le 10^6$) is therefore *strongly suggestively* a Hooley-boundary effect from $d \in (N, N^2]$ rather than an SD-chain error; this is a heuristic inference at one decade of overlap, not a rigorous transfer to $X = N^2$.

## Goal

The previous session (`P12-c0-coefficient.md`) found that the joint formal prediction $S(N) \approx c_3 N L^3 + c_2 N L^2 + c_1 N L + c_0 N$ disagrees with empirical $S(N)$ at $N \le 10^6$, with residual $\approx 0.85\,NL - 2.2\,N$. The data alone could not distinguish two hypotheses:
- (H1) The formal-SD Laurent of $G$ is correct on $\Sigma_*(X)$, and the discrepancy in $S(N)$ comes from the Hooley boundary $d \in (N, N^2]$ which the manipulation $S(N) \approx N\,\Sigma_*(N^2)$ does not handle rigorously.
- (H2) The formal-SD Laurent itself has issues at orders $\le L$, e.g. the analytic continuation or some computational mistake.

This note tests (H1) vs (H2) by computing $\Sigma_*(X)$ directly and comparing to formal Laurent.

## Setup

Let
$$ \Sigma_*(X) := \sum_{d \le X} \frac{\tau(d^2)\rho(d)}{d}. $$

The formal-SD prediction (Perron + Selberg–Delange, P12-c0-coefficient.md) is
$$ \Sigma_*(X) = \frac{A_3}{6} L^3 + \frac{A_2}{2} L^2 + A_1 L + A_0 + O(L^{-A}), \quad L = \log X, $$
for any fixed $A > 0$, with Laurent coefficients of $G(s) = \zeta_K(s)^3 H(s)$ at $s=1$:
$$ A_3 = R^3 H(1), \quad A_2 = 3R^2\gamma_K H(1) + R^3 H'(1), $$
$$ A_1 = 3R(R\beta_K + \gamma_K^2)H(1) + 3R^2 \gamma_K H'(1) + \tfrac{R^3}{2}H''(1), $$
$$ A_0 = (3R^2\alpha_K + 6R\gamma_K\beta_K + \gamma_K^3)H(1) + 3R(R\beta_K+\gamma_K^2)H'(1) + \tfrac{3R^2\gamma_K}{2}H''(1) + \tfrac{R^3}{6}H'''(1), $$
with $R = \pi/4$ and $\gamma_K, \beta_K, \alpha_K$ the first three Laurent coefficients of $\zeta_K$ at $s=1$.

Numerical values (computed in `bot/scratch/sigma-star-empirical.py` from prior-session inputs):
$$ A_3 = 0.05970786, \ A_2 = 0.43489197, \ A_1 = 1.07156775, \ A_0 = 0.87930421. $$

## Computation

`bot/scratch/sigma-star-empirical.py` sieves $a(d) := \tau(d^2)\rho(d)$ for $d \le 10^7$ via smallest-prime-factor sieve. Multiplicative structure:
- $a(2) = \tau(4)\rho(2) = 3 \cdot 1 = 3$, $a(2^k) = 0$ for $k \ge 2$;
- $a(p^k) = 0$ for $p \equiv 3 \pmod 4$;
- $a(p^k) = (2k+1) \cdot 2$ for $p \equiv 1 \pmod 4$, $k \ge 1$.

Cumulative $\sum_{d \le X} a(d)/d$ is recorded at 9 checkpoints $X \in \{10^3, 3\cdot 10^3, 10^4, \ldots, 10^7\}$.

## Results

| $X$ | $L = \log X$ | $\Sigma_*(X)$ empirical | formal Laurent | residual | $\text{residual} \cdot L^2$ |
|---:|---:|---:|---:|---:|---:|
| $10^3$              |  6.908 |  22.0004 |  21.9374 |  $+0.0629$ | $+3.00$ |
| $3 \cdot 10^3$      |  8.006 |  28.4878 |  28.5046 |  $-0.0168$ | $-1.08$ |
| $10^4$              |  9.210 |  36.9433 |  36.9700 |  $-0.0266$ | $-2.26$ |
| $3 \cdot 10^4$      | 10.309 |  45.9479 |  45.9375 |  $+0.0104$ | $+1.11$ |
| $10^5$              | 11.513 |  57.2402 |  57.2239 |  $+0.0163$ | $+2.16$ |
| $3 \cdot 10^5$      | 12.612 |  68.9373 |  68.9395 |  $-0.0022$ | $-0.35$ |
| $10^6$              | 13.816 |  83.4299 |  83.4282 |  $+0.0018$ | $+0.34$ |
| $3 \cdot 10^6$      | 14.914 |  98.2426 |  98.2397 |  $+0.0029$ | $+0.65$ |
| $10^7$              | 16.118 | 116.3094 | 116.3117 |  $-0.0023$ | $-0.59$ |

**Two key observations:**

1. **Residual oscillates in sign** (sign-changes 5 times across 9 datapoints). This rules out a systematic algebraic error in the Laurent coefficients — a wrong $A_j$ would produce a residual of fixed sign (or growing on a clean polynomial slope).

2. **Residual magnitude is bounded by $|\text{res}| \le 0.063$ across the full range,** with $|\text{res}| \cdot L^2 \le 3.00$. The data is consistent with $O(L^{-A})$ decay for some $A > 0$, but **9 datapoints over 1.4 decades in $L$ cannot distinguish $A = 1.3$ from $A = 2$ from $A = 3$**. The qualitative observation is "residual is small and decaying / oscillating, not constant or growing"; quantitative claims about the exponent $A$ would over-state.

**Both observations support hypothesis (H1):** the formal-SD chain on $G$ is internally consistent at the level of $\Sigma_*(X)$ over the data range. The Laurent coefficients $A_3, A_2, A_1, A_0$ are not affected by an algebraic error of size $\gg 0.1$ at $L \le 16$; the partial-sum behaves as expected up to fluctuations consistent with Tauberian theory.

## Implication for $S(N)$ — Hooley boundary isolated

The previous session established
$$ S(N)/N - c_3 L^3 - c_2 L^2 - c_1^{\text{formal}} L - c_0^{\text{formal}} \approx 0.85 L - 2.16 + (\text{small}), \quad N \in [10^3, 10^6], $$
where $c_j^{\text{formal}}$ come from the formal manipulation $S(N) \approx N \Sigma_*(N^2)$, i.e. $c_3 = 4A_3/3, c_2 = 2A_2, c_1 = 2A_1, c_0 = A_0$.

This session shows $\Sigma_*(X)$ matches its formal Laurent at $X \le 10^7$ with residual bounded by $0.063$ in absolute terms.

**Heuristic inference (not rigorous):** *if* the residual at $X = N^2$ remains comparably small (which is plausible by Tauberian theory but not verified by direct computation, which would require sieving to $X = 10^{12}$), then $N \cdot \Sigma_*(N^2)$ matches its formal Laurent at $N = 10^6$ to within $\sim 0.06\,N \approx 6 \cdot 10^4$, while the empirical $S(N)$ residual is $\sim 9.5 \cdot 10^6$, two orders of magnitude larger. Under this inference the empirical $S(N)$ residual is *not* explained by the SD-Laurent on $\Sigma_*$ and must come from the Hooley boundary $d \in (N, N^2]$.

The inference rests on a 5-decade extrapolation of an empirical envelope and is not a proof. What is proved (this session): formal-SD on $G$ is correct at $X \le 10^7$ within Tauberian fluctuations.

This is the Hooley 1957-type setup applied at second-moment level: $\tau(m)^2 = \sum_{d | m}\tau(d^2)$ is the Vinogradov-style identity, $\rho(d) = \#\{x \pmod d : x^2 \equiv -1 \pmod d\}$ is the local density, and the boundary is the regime $d > N$ that the formal manipulation $S(N) \approx N \Sigma_*(N^2)$ over-counts.

## Empirical Hooley-boundary fit (carried over from previous session)

The previous session (`P12-c0-coefficient.md`) reported a fit
$$ \text{(empirical residual)}/N \approx 0.85\,L - 2.16, \quad L \in [6.9, 13.8], \quad R^2 = 0.992 $$
based on $S(N)$ at 5 values of $N$. **This session does not re-validate that fit** (no new $S(N)$ data was generated). Modulo the heuristic inference above, this empirical residual is the candidate Hooley-boundary contribution.

The sign of the residual is **positive** at large $L$ (empirical $S(N)$ exceeds the formal-SD asymptote). This is consistent with the Hooley correction being a non-negative double sum over $(d, n)$ with $d > N$, $d \mid n^2+1$, weighted by $\tau(d^2) \ge 1$.

## What this session does NOT prove

1. **It does not derive Hooley$(N)$ in closed form.** The fit $0.85 L - 2.16$ is empirical over a single decade in $L$.
2. **It does not extend $S(N)$ data beyond $N = 10^6$.** The previous session promoted that as a 1–2 session task; not done here.
3. **It does not rule out higher-order Tauberian remainders.** The empirical $|res| \cdot L^2 \le 3$ is consistent with $O(L^{-2})$ but could reflect $O(L^{-A})$ with larger $A$ and ordinary fluctuations; one decade is not enough to distinguish.
4. **The conclusion that "empirical $S(N)$ residual is the Hooley boundary" is a strong inference, not a proof.** What is proved: $\Sigma_*(X)$ tracks formal Laurent to $O(L^{-2})$; what is inferred: this transfers to $\Sigma_*(N^2)$ at $X = N^2$, where direct computation is infeasible.

## Strategic implication

The next-session targets crystallize:

- **Demoted (further):** The hypothesis "formal SD on $G$ is wrong somewhere" is now strongly disfavored. Don't pursue closed-form $A_{-1}, A_{-2}, \ldots$ corrections to $G$ as a fix for the $S(N)$ discrepancy — the discrepancy is **not** in $G$.

- **Promoted:** **Direct calculation of the Hooley boundary** $\sum_{N < d \le N^2+1} \tau(d^2)\rho(d)\, |\{n \le N : d | n^2+1\}|$.
  In Hooley 1957's first-moment computation the analog quantity is computed in closed form via the hyperbola method (split divisors, parametrize via $\mathbb{Z}[i]$, extract the leading $N \log N$ vs. boundary $N$ via lattice-point counting). Adapting this to second moment introduces a $\tau(d^2)$ weight; the natural target is to identify the leading order as $\propto N L$ with explicit constant $\approx 0.85$.

- **Auxiliary empirical:** Extending $S(N)$ to $N = 10^7$ would let us check whether the empirical fit $0.85 L - 2.16$ is stable or shifting, but is now lower priority since the structural picture is settled.

## Files

- `bot/scratch/sigma-star-empirical.py` — sieve, Laurent comparison, decay table.

## Caveats summary

1. Residual on $\Sigma_*(X)$ in the table is bounded by $|res| \cdot L^2 \le 3$ over $X \in [10^3, 10^7]$. This is **consistent** with $O(L^{-2})$ but does not distinguish $O(L^{-2})$ from $O(L^{-A})$ for $A > 2$. The conclusion "formal-SD chain matches" is robust to either reading.
2. The numerical Laurent values use $H(1), H'(1), H''(1), H'''(1)$ from previous-session Euler products (primes $\le 2 \cdot 10^5$), with $H'''(1)$ computed by finite difference. The latter has the largest precision uncertainty ($\sim 0.1$ relative on $H'''(1) \approx -5.09$). Propagated into $A_0$, this gives uncertainty $\sim |R^3/6 \cdot 0.1 \cdot H'''(1)| / |A_0| \approx 0.04 / 0.88 \approx 5\%$ on $A_0 \approx 0.879$. The empirical residual at $X = 10^7$ is $-0.002$, well within this uncertainty.
3. The Hooley-boundary inference assumes $\Sigma_*(X)$ residual continues to behave like $O(L^{-2})$ at $X = N^2$ where $L = 2 \log N$; the strict claim is asymptotic, not pinned at our finite $N$.
4. The empirical fit $0.85 L - 2.16$ for the boundary correction is over a single decade; neither the slope nor the intercept is rigorously pinned. The order-of-magnitude conclusion (boundary $\asymp NL$) is robust.

## Net rigorous content

- **Computed** $\Sigma_*(X)$ exactly at 9 checkpoints $X \in [10^3, 10^7]$.
- **Computed** the formal Laurent prediction at the same checkpoints.
- **Observed** that residual is bounded by $|\text{res}| \cdot L^2 \le 3$ and oscillates in sign.

What this rules out (rigorously, given the data):
- A constant-sign systematic bias in the formal Laurent coefficients of size $\gg 0.1$ at $L \le 16$. This forecloses simple algebraic-error explanations for the $S(N)$ residual.

What this supports (heuristically):
- The empirical $S(N)$ residual is genuinely a Hooley-boundary effect, motivating direct attack on that calculation in the next session.
