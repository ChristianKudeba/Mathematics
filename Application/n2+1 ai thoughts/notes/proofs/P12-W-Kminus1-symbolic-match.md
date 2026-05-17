# P12 — symbolic match of $W_{K-1}$: corrected identification and $\Sigma_3$ Laurent prediction

**Date:** 2026-05-05 19:30 UTC
**Continues:** `P12-Hooley-tail-N1e6-validation.md` (2026-05-05 16:30) which proposed
"symbolic match of $W_{K-1}$ vs $P_{K-1}$ leading terms" as the highest-EV next thread,
under the heading: "the topmost-window identification with partial $S_2$ sum lets one
write both quantities as Selberg-Delange Laurent expansions in $L = \log N$ and check
whether their leading $L^3, L^2$ coefficients match."

## Headline correction (labeling/interpretation, not computation)

The previous session's writeup (`P12-Hooley-tail-N1e6-validation.md`, line 117)
displayed $W_{19} = \sum_{724078 < n \le 10^6} \tau((n^2+1)^2)$ correctly **but
labeled** that quantity "a partial sum of the Hooley second moment $S_2(N) := \sum \tau(n^2+1)^2$".
The labeling is wrong: $\tau(m^2) \ne \tau(m)^2$ in general (e.g. for $m = pq$ distinct
primes, $\tau(m^2) = 9$ while $\tau(m)^2 = 16$). The displayed quantity is a partial
sum of the **third-power** moment

$$S_3(N) \;:=\; \sum_{n \le N} \tau\big((n^2+1)^2\big), \qquad S_3 \ne S_2.$$

The two moments are linked by the universal identity

$$\sum_{d \mid m} \tau(d^2) \;=\; \tau(m)^2 \quad \text{(yields } S_2 = \sum_d \tau(d^2) N_d \text{)}, \qquad
\tau(m^2) \;=\; \sum_{d \mid m} 2^{\omega(d)} \quad \text{(yields } S_3 = \sum_d 2^{\omega(d)} N_d\text{)}.$$

Their growth orders **differ**:
- $S_2(N) \sim c_3 N L^3$ (Hooley conjectural, $L^3$);
- $S_3(N) \sim 2 b'_2 N L^2$ (this work, $L^2$).

**Important scoping**: this is a *labeling/interpretation* error in the prior session,
NOT a computational error in $P^{(2)}$. The prior session's $P^{(2)} = N(\Sigma_*(\sup)
- \Sigma_*(\inf))$ is built from the $\Sigma_*$ Laurent on the $d$-range, which is its own
formal-SD chain ($\sum_d \tau(d^2)\rho(d)/d$, the "$S_2$-decomposition by $d$"). $P^{(2)}$
is a valid formal prediction for $W_{K-1}$, just not the *natural* one for the $r=1$ regime.
The new $P^{(3)}$ is the natural prediction for the $r=1$ regime. Both predict the same
empirical $W_{K-1}$; they differ in fidelity at finite $N$.

## Analytic structure of $S_3$

Let $T_3(s) := \sum_{d \ge 1} 2^{\omega(d)} \rho(d) d^{-s}$ where $\rho(d) := |\{x \pmod d : x^2 \equiv -1\}|$.
Local factors:

- $p = 2$: $\rho(2) = 1$, $\rho(2^k) = 0$ for $k \ge 2$, $2^{\omega(2)} = 2$. Local factor
  $1 + 2 \cdot 2^{-s} = 1 + 2^{1-s}$.
- $p \equiv 3 \pmod 4$: $\rho = 0$. Local factor $1$.
- $p \equiv 1 \pmod 4$: $\rho(p^k) = 2$, $2^{\omega(p^k)} = 2$ for $k \ge 1$. Local factor
  $1 + \sum_{k \ge 1} 4 p^{-ks} = (1 + 3 p^{-s})/(1 - p^{-s})$.

Hence

$$T_3(s) \;=\; (1 + 2^{1-s}) \prod_{p \equiv 1(4)} \frac{1 + 3 p^{-s}}{1 - p^{-s}}.$$

**Factorization in terms of $\zeta_K$**, $K = \mathbb{Q}(i)$. We have
$\zeta_K(s) = \zeta(s) L(s, \chi_4)$, with local factor $(1 - p^{-s})^{-2}$ at $p \equiv 1(4)$,
$(1 - p^{-2s})^{-1}$ at $p \equiv 3(4)$, $(1 - 2^{-s})^{-1}$ at $p = 2$. Setting

$$T_3(s) = \zeta_K(s)^2 \cdot H_3(s),$$

the local factors of $H_3$ are:

- $p = 2$: $H_3$-local $= (1 + 2^{1-s})(1 - 2^{-s})^2$. At $s = 1$: $2 \cdot (1/2)^2 = 1/2$.
- $p \equiv 1(4)$: $H_3$-local $= (1 + 3 p^{-s})(1 - p^{-s})^3 = 1 - 6 p^{-2s} + 8 p^{-3s} - 3 p^{-4s}$.
  At $s = 1$: $(1 + 3/p)(1 - 1/p)^3 = 1 - 6/p^2 + 8/p^3 - 3/p^4$.
- $p \equiv 3(4)$: $H_3$-local $= (1 - p^{-2s})^2$. At $s = 1$: $(1 - 1/p^2)^2$.

Each local factor at large $p$ is $1 + O(p^{-2})$, so $H_3(s)$ converges absolutely
on $\Re s > 1/2$, hence is **analytic on $\Re s > 1/2$**. Therefore

$$T_3(s) \;=\; \zeta_K(s)^2 \, H_3(s)$$

has a **double pole** at $s = 1$ with leading singular coefficient

$$T_3(s) = \frac{(\pi/4)^2 H_3(1)}{(s-1)^2} + \frac{(\pi/4)^2 H_3'(1) + 2(\pi/4)\gamma_K H_3(1)}{s - 1} + O(1),$$

where $\gamma_K := L'(1, \chi_4) + \gamma L(1, \chi_4) \approx 0.6462$ is the next coefficient
in the Laurent expansion of $\zeta_K$ at $s = 1$ (computed in 2026-05-04 09:57 session).

**Numerical values** (Euler product truncated at $p \le 10^6$; tail bounded by
$\sum_{p > 10^6} O(1/p^2)$ which is $< 10^{-6}$):

$$H_3(1) \approx 0.27775, \qquad H_3'(1) \approx 0.84241.$$

Therefore

$$b'_2 := (\pi/4)^2 H_3(1) \approx 0.17133, \qquad b'_1 := (\pi/4)^2 H_3'(1) + 2(\pi/4)\gamma_K H_3(1) \approx 0.80157.$$

## Selberg–Delange asymptotic for $S_3$

By the standard SD framework with $\kappa = 2$ (analytic prefactor $H_3$ on
$\Re s > 1/2$):

$$\Sigma_3(X) \;:=\; \sum_{d \le X} \frac{2^{\omega(d)} \rho(d)}{d}
\;=\; \frac{b'_2}{2} (\log X)^2 + b'_1 \log X + b'_0 + O\big((\log X)^{-A}\big)$$

for any $A > 0$, with $b'_0$ a third Laurent coefficient (not computed here).
The Hooley-style main-term decomposition

$$S_3(N) \;=\; \sum_d 2^{\omega(d)} N_d(N) \;\approx\; N \, \Sigma_3(N^2 + 1) + B_3(N)$$

(with $B_3$ the analog of the boundary $B$ of $S_2$) yields

$$S_3(N) \;\sim\; 2 b'_2 \cdot N L^2 + 2 b'_1 \cdot N L + O(N) + B_3(N),$$

where $L = \log N$.

**Empirical validation** ($S_3$ computed via direct factorization sieve):

| $N$ | $L$ | $S_3$ | $S_3/(NL^2)$ | $2 b'_2 NL^2 + 2 b'_1 NL$ | ratio |
|---|---|---|---|---|---|
| $3 \cdot 10^4$ | $10.31$ | $1.634 \cdot 10^6$ | $0.5132$ | $1.588 \cdot 10^6$ | $1.029$ |
| $10^5$ | $11.51$ | $6.538 \cdot 10^6$ | $0.4932$ | $6.388 \cdot 10^6$ | $1.024$ |

The two-term Laurent matches empirical $S_3$ to within $2$–$3\%$ in this range —
a non-trivial check of $H_3(1), H_3'(1)$ and the $\zeta_K^2$ structure.

## Application to $W_{K-1}$

Because the topmost dyadic window $W_{K-1} = (\inf, \sup]$ with $\inf = N \cdot 2^{K-1}$,
$\sup = N^2 + 1$, has width $\sup/\inf < 2$, only $r = 1$ contributes (any $d \mid n^2+1$
with $d > N^2/2$ forces $r = (n^2+1)/d = 1$, hence $d = n^2+1$). Therefore

$$W_{K-1} \;=\; \sum_{n_- < n \le N} \tau\big((n^2+1)^2\big), \qquad n_- := \lfloor \sqrt{\inf - 1} \rfloor.$$

The two competing formal predictions:

**(a) $P_{K-1}^{(2)}$ (prior session method) — $\Sigma_*$ Laurent on $d$-range.**

$$P_{K-1}^{(2)} \;=\; N\big(\Sigma_*(\sup) - \Sigma_*(\inf)\big),$$

with $\Sigma_*(X) = A_3 (\log X)^3/6 + A_2 (\log X)^2/2 + A_1 \log X + A_0$. Asymptotically
($\inf \to N^2/2$, $\sup \to N^2$):

$$P_{K-1}^{(2)} \;\sim\; 2 A_3 \log 2 \cdot N L^2 + (2 A_2 \log 2 - A_3 (\log 2)^2) N L + \text{const} \cdot N.$$

Numerically: $2 A_3 \log 2 \approx 0.0828$, leading-$L^2$ coefficient.

**(b) $P_{K-1}^{(3)}$ (this session) — $\Sigma_3$ Laurent on $n$-band.**

$$P_{K-1}^{(3)} \;=\; \big(2 b'_2 N L^2 + 2 b'_1 N L\big) - \big(2 b'_2 n_- (\log n_-)^2 + 2 b'_1 n_- \log n_-\big),$$

obtained as the difference of two-term Laurents of $S_3(N)$ and $S_3(n_-)$. Asymptotically
($n_- \to N/\sqrt 2$):

$$P_{K-1}^{(3)} \;\sim\; 2 b'_2 (1 - 1/\sqrt 2) N L^2 + (2 b'_1 (1 - 1/\sqrt 2) + b'_2 \sqrt 2 \log 2) N L + \text{const} \cdot N.$$

Numerically: $2 b'_2 (1 - 1/\sqrt 2) \approx 0.1003$, leading-$L^2$ coefficient.

**The two leading $L^2$ coefficients differ:**
$0.0828 \,(P^{(2)}) \;\ne\; 0.1003 \,(P^{(3)}).$
This is informative: $P^{(2)}$ formally extends the approximation
$N_d(N) \approx \rho(d) N/d$ uniformly across all $d \in W_{K-1}$, but for $d$ in the
top window each $d$ has $N_d(N) \in \{0, 1\}$ in fact — the average $\rho(d)/d$ is
much smaller than the typical "0 or 1" reality, so $P^{(2)}$ systematically undercounts
in this regime. By contrast $P^{(3)}$ uses the asymptotic of partial $S_3$ on the
exactly-correct $n$-band, which is the natural decomposition for the $r = 1$ piece.

## Empirical comparison at four $N$

Direct computation of $W_{K-1}$ via Hensel-lift sieve, with the dyadic edges
$\inf = N \cdot 2^{K-1}$, $K = \lceil \log_2((N^2+1)/N) \rceil$:

| $N$ | $L$ | $W_{K-1}/N$ | $P^{(2)}/N$ | $P^{(3)}/N$ | $W - P^{(2)}$ per $N$ | $W - P^{(3)}$ per $N$ |
|---|---|---|---|---|---|---|
| $10^4$ | $9.21$ | $5.00$ | $3.80$ | $4.88$ | $+1.20$ | $+0.13$ |
| $3 \cdot 10^4$ | $10.31$ | $16.09$ | $13.45$ | $15.73$ | $+2.65$ | $+0.36$ |
| $10^5$ | $11.51$ | $14.06$ | $11.21$ | $13.78$ | $+2.85$ | $+0.29$ |
| $3 \cdot 10^5$ | $12.61$ | $5.66$ | $4.17$ | $5.52$ | $+1.49$ | $+0.14$ |

(The non-monotone $W/N$ trajectory is the dyadic-edge artifact: $W_{K-1}$ is sensitive
to whether $N$ sits just above or just below a power-of-2 boundary, since $\inf$ jumps
by factor 2 between adjacent decades.)

**Key observation.** The $P^{(3)}$ residual $W - P^{(3)}$ is roughly an order of
magnitude smaller than the $P^{(2)}$ residual $W - P^{(2)}$, and stable at $\le 0.4 N$
across all four $N$. This means the new formal prediction (via $\Sigma_3$ Laurent on the
$n$-band) absorbs the bulk of the prior "deep-tail residual" — the previous session's
$\sim 4.5 N$ at $N = 10^6$ was largely an artifact of using the wrong formal prediction
$P^{(2)}$.

## Strategic implications (with documented limits)

**(1) The corrected analytic question** for the topmost window:

The empirical residual $W_{K-1} - P^{(3)}$ at four $N$ in $\{10^4, 3 \cdot 10^4, 10^5,
3 \cdot 10^5\}$ is in the range $[+0.13 N, +0.36 N]$, **non-monotone** ($0.13, 0.36, 0.29,
0.14$). Across these four points $L$ varies only from $9.21$ to $12.61$ — a factor
$1.4$ in $L$ — which is **insufficient to distinguish $O(N)$ from $O(NL^{1/2})$ or
even $O(NL)$**. The conservative empirical statement is "$W_{K-1} - P^{(3)} \le 0.4 N$
across our four data points"; the asymptotic order remains undetermined. To distinguish
$O(N)$ from $O(NL)$ needs $L$ varying by a factor $\ge 4$, i.e. $N$ ranging over at
least $4$ decades — pending data at $N \in \{10^6, 10^7\}$.

**(2) "Most of the prior 0.85 $NL$ residual is $P^{(2)}$ artifact" — currently NOT
established.** This note demonstrates the $P^{(3)} \ll P^{(2)}$ residual reduction
**only** for the topmost window $W_{K-1}$. The prior session's $0.85 NL$ figure is
$\sum_k(W_k - P^{(2)}_k)$ over many high-$d$ windows. Lower windows $W_{K-2}, W_{K-3},
\ldots$ involve $r \in \{1, 2\}, r \in \{1, 2, 3\}, \ldots$ contributions, and the
clean "$r = 1$ only" simplification used here does NOT directly transfer (each $r$-slice
contributes a different partial-sum-of-$S_3$-style term, plus cross terms). **Whether
analogous $\Sigma_3$-based predictions yield comparable improvements at lower windows
is an open empirical question, not yet measured.** The eventual test is to compute
$P^{(3)}_k$ for all $k$ and compare $\sum_k(W_k - P^{(3)}_k)$ against the prior $0.85
NL$. Until that's done, the "artifact" claim is suggestive but not proven.

**(3) Sharpest defensible claim** (this session): for the topmost window specifically,
the natural formal-SD prediction is $P^{(3)}$ (via $\Sigma_3$ on $n$-band), and it is
empirically much tighter than $P^{(2)}$ (via $\Sigma_*$ on $d$-range). This sharpens
the prior session's "renaming, not reduction" status: there IS an analytic structure
specific to the $r=1$ piece, namely the $\Sigma_3 = \zeta_K^2 H_3$ Laurent. Whether
this structure extends to give a global reduction of $B_>(N)$ requires window-by-window
analysis.

**(4) Beyond the top window** (open). Lower windows $W_{K-2}, W_{K-3}, \ldots$
involve $r \in \{1, 2\}, r \in \{1, 2, 3\}, \ldots$. The $r$-th slice for fixed $r$
sums $\tau(d^2)$ over $\{(n, d): d = (n^2+1)/r, n^2+1 \in r \cdot W\}$, giving
$\sum_n \tau(((n^2+1)/r)^2) [r | n^2+1]$, which is a different partial sum requiring
its own multiplicative-function analysis. Substantially more work than this note.

## Skeptic-anticipated objections

**Q1.** "The $P^{(3)}$ residual at $N = 10^4$ is $0.13 N$, at $N = 3 \cdot 10^4$ is
$0.36 N$, at $N = 10^5$ is $0.29 N$, at $N = 3 \cdot 10^5$ is $0.14 N$. Non-monotone.
Maybe just noise."

Yes. The dyadic-edge effect makes single-$N$ residuals bouncy. The honest statement is
"residual $\le 0.4 N$ across our four data points", not "decaying to 0". Whether
$W_{K-1} - P^{(3)} = O(N)$ vs $o(NL)$ vs $O(NL)$ is not determined by these four
points; one needs $N \in \{10^6, 10^7\}$.

**Q2.** "The two-term Laurent prediction $S_3(N) \sim 2 b'_2 NL^2 + 2 b'_1 NL$ has a
2-3% empirical residual at $N = 10^5$, comparable in magnitude to $W_{K-1}$ itself.
Why should subtracting the same Laurent at two endpoints give a tighter residual?"

Because of partial cancellation — the two endpoint Laurents share the same $b'_0 N$
constant term (formal), so on subtraction this term drops out. What remains is the
$L$-dependent part where the formal prediction is more accurate. (In effect, $b'_0$
is unconstrained by my computation, so I cannot include it in $P^{(3)}$; but it
cancels in $S_3(N) - S_3(n_-)$ assuming a slowly-varying Tauberian boundary.)

This argument is heuristic, not rigorous. Empirically it works as the table shows.

**Q3.** "The asymptotic limits in $P^{(2)}_\text{leading}$ ($n_- \to N/\sqrt 2$,
$\inf/\sup \to 1/2$) hold along dyadic powers of 2. For arbitrary $N$, the dyadic
edges differ. Are you comparing apples to apples?"

In the empirical table, $P^{(2)}, P^{(3)}, W$ all use the actual dyadic $\inf$ at each
$N$ (not the asymptotic limit). Specifically $P^{(3)}$ uses $n_- = \lfloor\sqrt{\inf - 1}\rfloor$
which differs from $N/\sqrt 2$ by a factor of order $1$ depending on the dyadic offset.
The asymptotic comparison is for the leading constants; the empirical comparison uses
exact dyadic edges. Both consistent.

**Q4.** "What about the $n_-$-fluctuation between dyadic decades? At $N = 10^4$,
$n_- = 9050$ and the band has 950 values. At $N = 3 \cdot 10^4$, $n_- = 22170$, 7830 values.
The per-band-element averages differ: $W/(N - n_-)$ at $N = 10^4$ is $50046/950 = 53$,
at $N = 3 \cdot 10^4$ is $482802/7830 = 62$. Is the asymptotic per-element behavior
captured?"

Per-element: $S_3(N)/N$ at $N = 10^4, 3 \cdot 10^4, 10^5$ is $45.2, 54.5, 65.4$ (slowly
increasing as $\sim L^2$). The per-element values within the top window match this
trend at each $N$. Consistent.

## Conclusion

The prior session's identification of $W_{K-1}$ as a partial $S_2$ sum was a
**labeling error**: $W_{K-1}$ is a partial $S_3 := \sum_n \tau((n^2+1)^2)$ sum, where
$S_3$ has $L^2$ asymptotic growth (not $L^3$). The natural formal prediction is the
two-term Laurent of $S_3$ applied to the corresponding $n$-band, with coefficients
$b'_2 = (\pi/4)^2 H_3(1) \approx 0.171$ and $b'_1 = (\pi/4)^2 H_3'(1) + 2(\pi/4) \gamma_K
H_3(1) \approx 0.802$, derived from $T_3(s) = \zeta_K(s)^2 H_3(s)$ with $H_3$ analytic
on $\Re s > 1/2$ and $H_3(1) \approx 0.278$, $H_3'(1) \approx 0.842$ (Euler product).
The 2-term Laurent matches empirical $S_3(N)$ to within 2-3% at $N \in \{3 \cdot 10^4,
10^5\}$, validating the analytic structure.

For the topmost window specifically, $P^{(3)}$ tracks $W_{K-1}$ to within $0.13$–$0.36 N$
across four $N$ in $[10^4, 3 \cdot 10^5]$, vs $P^{(2)}$ residual $1.2$–$2.9 N$ — a
roughly $10\times$ reduction at this scale.

**Sharpest defensible upshot:** for the $r=1$ piece of $B_>(N)$ (the topmost dyadic
window), the natural analytic structure is $\zeta_K^2 H_3$ (not $\zeta_K^3 H$ as
implicit in $P^{(2)}$). The prior session's deep-tail residual contains substantial
$P^{(2)}$-vs-natural-$P^{(3)}$ approximation error, at least in this window.

**What's NOT yet established:**
- Asymptotic order of $W_{K-1} - P^{(3)}$ (4 data points span only factor 1.4 in $L$).
- Whether the same residual reduction occurs in lower windows $W_{K-2}, W_{K-3}, \ldots$
  (analogous $\Sigma_3$-style analysis would need to be redone for each $r$-slice).
- Whether the global $0.85 NL$ residual claim of the prior session reduces accordingly.

**Next-step diagnostics** (1 session each):
- $N = 10^6$ comparison: extends the table by one decade, tests trend.
- All-windows $P^{(3)}$ predictions at one fixed $N$ (e.g. $10^5$): tests the global
  "is the deep-tail mostly artifact" claim.
- Symbolic match for $W_{K-2}$ ($r \in \{1, 2\}$): would need partial-sum analysis
  of $\sum \tau((n^2+1)^2)[\text{condition}]$ on a different $n$-band, plus $r = 2$
  slice analysis.

## Code

`bot/scratch/W-Kminus-1-symbolic.py` (this session). Computes $H_3(1), H_3'(1)$ via
Euler product, $b'_2, b'_1$ from $\zeta_K^2 H_3$ Laurent, $W_{K-1}$ via direct sieve
at four $N$, and the comparison table.
