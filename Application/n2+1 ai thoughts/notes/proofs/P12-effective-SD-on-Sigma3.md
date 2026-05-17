# P12: Effective Selberg–Delange on $\Sigma_3$, applied to the $W_{K-1}$ band-difference (2026-05-06)

## Summary

The previous session ($N = 10^6$ comparison) left the soft-spot caveat (i):
the empirical residual $W_{K-1} - P^{(3,3)} \in [+0.04 N, +0.21 N]$ across five
$N$ from $10^4$ to $10^6$ was conjectured to be $O(N)$, but the rigorous content
was unclear because TWO error sources were lumped together:

- (i) the **Selberg–Delange remainder** in $\Sigma_3(X) - (\text{3-term Laurent})$;
- (ii) the **Hooley-boundary remainder** $B_3(N) = S_3(N) - N \Sigma_3(N^2+1)$.

This session executes (i) rigorously. The conclusion is

$$
\boxed{\, W_{K-1} - P^{(3,3)} \;=\; \big[B_3(N) - B_3(n_-)\big] \;+\; O_A\!\left(\frac{N}{(\log N)^A}\right) \quad \text{for any fixed } A > 0,\,}
$$

with the implicit constant depending qualitatively on $A$ via Tenenbaum II.5.2.
This *qualitatively* sharpens the attack surface: for any $A > 0$, the SD-piece
is $o(N/L^{A-1})$, so the rigorous content of the conjecture
$W_{K-1} - P^{(3,3)} = O(N)$ is the Hooley-boundary statement
$B_3(N) - B_3(n_-) = O(N)$. **Conjecturally** (using a heuristic effective
constant $|r(X)| \le 0.4/L^2$ extracted from 5 numerical points in
$X \in [10^3, 10^7]$), the SD-piece at $N = 10^6$ is $\le 10^3$, three orders
below the empirical residual $\approx 2.13 \cdot 10^5$ — supporting the reading
that the empirical residual is **dominated by the Hooley boundary**, although
this $0.4/L^2$ shape is not part of the rigorous theorem.

## Setup recap

For $d \ge 1$ let $\rho(d) = \#\{x \bmod d : x^2 \equiv -1 \pmod d\}$. Define

$$
\Sigma_3(X) := \sum_{d \le X} \frac{2^{\omega(d)}\rho(d)}{d}, \qquad
T_3(s) := \sum_d \frac{2^{\omega(d)}\rho(d)}{d^s} = \zeta_K(s)^2 H_3(s),
$$

with $K = \mathbb{Q}(i)$, $\zeta_K(s) = \zeta(s) L(s, \chi_4)$, and $H_3$ analytic
on $\Re s > 1/2$. From the previous two sessions the leading Laurent
coefficients of $T_3$ at $s = 1$ are

$$
c_2 = R^2 H_3(1) \approx 0.17133, \quad c_1 = R^2 H_3'(1) + 2 R \gamma_K H_3(1) \approx 0.80157,
$$
$$
c_0 = R^2 H_3''(1)/2 + 2 R \gamma_K H_3'(1) + (\gamma_K^2 + 2 R \beta_K) H_3(1) \approx 0.93878,
$$

with $R = \pi/4$.

$S_3(N) := \sum_{n \le N} \tau((n^2+1)^2)$ has the **exact identity**

$$
S_3(N) = N \cdot \Sigma_3(N^2+1) + B_3(N), \qquad B_3(N) := \sum_{d \le N^2+1} 2^{\omega(d)} \delta_d(N),
$$

where $\delta_d(N) := N_d(N) - \rho(d) N/d$ is the lattice discrepancy
($N_d(N) = \#\{n \le N : d \mid n^2+1\}$). For $d > N^2+1$, $N_d(N) = 0$, so
the truncation at $N^2+1$ is exact (not asymptotic).

The 3-term Laurent prediction is

$$
\text{pred}_3(N) := 2 b'_2 N L^2 + 2 b'_1 N L + b'_0 N
\quad \text{with } b'_j = c_j, \; L = \log N.
$$

The topmost dyadic window is $W_{K-1} = S_3(N) - S_3(n_-)$ where
$n_- = \lfloor \sqrt{N \cdot 2^{K-1} - 1}\rfloor$, $K = \lceil \log_2((N^2+1)/N)\rceil$.
The window prediction is $P^{(3,3)} = \text{pred}_3(N) - \text{pred}_3(n_-)$.

## Theorem (effective SD on $\Sigma_3$)

**Theorem 1.** *For any fixed $A > 0$, there exists an effective constant $C_A > 0$
such that for all $X \ge 3$,*

$$
\left| \Sigma_3(X) - \left(\frac{c_2}{2}(\log X)^2 + c_1 \log X + c_0\right) \right| \le \frac{C_A}{(\log X)^A}.
$$

### Proof sketch (Tenenbaum II.5.2 + partial summation).

Write $T_3(s) = \zeta(s)^2 \cdot \tilde H(s)$ with $\tilde H(s) := L(s, \chi_4)^2 H_3(s)$.

**Hypothesis check for Tenenbaum II.5.2 with $\kappa = 2$:**

1. *Analyticity in a Selberg–Delange region.* $L(s, \chi_4)$ is entire; $H_3$ is
   analytic on $\Re s > 1/2$. Hence $\tilde H$ is analytic on $\Re s > 1/2$, in
   particular in the Vinogradov–Korobov region
   $\Re s \ge 1 - c_0/(\log(|t|+2))^{2/3}(\log\log(|t|+3))^{1/3}$ (subset of
   $\Re s > 1/2$).

2. *Polynomial growth on the SD boundary.* The SD theorem requires polynomial
   bound on a fixed contour inside the VK region, **not** on $\Re s = 1/2 + \epsilon$
   for arbitrary $\epsilon$. The VK region is contained in $\Re s \ge 1 - c_{VK}$
   for some absolute $c_{VK} < 1/2$ (e.g. $c_{VK} \le 0.4$ for standard parameters),
   so it lies in $\Re s \ge 0.6$, well inside $\Re s > 1/2$. On this region:
   - $|L(s, \chi_4)| \ll (1+|t|)^{1/4}$ (convexity bound for $L$-functions on the
     critical strip; convexity is sufficient — subconvexity not needed).
   - $|H_3(s)| \le C$ for some absolute $C$. *Reason:* the Euler product of $H_3$
     factors as $\prod_p L_p(s)$, where at split $p \equiv 1\pmod 4$, the local
     factor is $L_p(s) = (1 + 3 p^{-s})(1 - p^{-s})^3$ which expands as
     $1 - 6 p^{-2s} + 8 p^{-3s} - 3 p^{-4s}$ — the $p^{-s}$ coefficient cancels
     by design ($3 - 3 = 0$)
     (this is the universal cancellation discovered in P12-tau-squared work).
     At inert primes $p \equiv 3 \pmod 4$, $L_p(s) = (1 - p^{-2s})^2 = 1 - 2p^{-2s} + p^{-4s}$.
     At $p = 2$, $L_2(s)$ is the explicit local factor, bounded for $\Re s \ge 0.6$.
     Hence $\prod_p L_p(s)$ converges absolutely and uniformly on $\Re s \ge 0.6$
     (since each factor is $1 + O(p^{-2 \cdot 0.6}) = 1 + O(p^{-1.2})$ and
     $\sum p^{-1.2}$ converges). The bound $C = \prod_p \sup_{\Re s \ge 0.6} |L_p(s)|$
     is finite.
   
   Hence $|\tilde H(s)| \ll (1+|t|)^{1/2}$ on the VK region, polynomially bounded.

3. *Non-vanishing at $s = 1$.* $\tilde H(1) = (\pi/4)^2 H_3(1) = c_2 \approx 0.171 \ne 0$.

These verify the hypotheses of the Selberg–Delange theorem
(Tenenbaum, *Introduction to analytic and probabilistic number theory*, Theorem II.5.2)
applied to the multiplicative function $f(d) = 2^{\omega(d)} \rho(d) \ge 0$ with
$F(s) = T_3(s) = \zeta(s)^2 \tilde H(s)$ and $z = 2$. The conclusion is: for any
integer $N \ge 0$,

$$
A_3(X) := \sum_{d \le X} f(d) = X \sum_{j=0}^{N} \frac{\lambda_j}{(\log X)^{j-1}} + O_N\!\left(\frac{X}{(\log X)^N}\right),
$$

with $\lambda_0 = \tilde H(1)$ and $\lambda_j$ explicit in $\tilde H, \tilde H', \ldots$.
The leading term is $\lambda_0 X \log X = c_2 X \log X$.

**Direct Perron derivation of the constant term $c_0$.** Rather than relying on
partial summation to identify the constant term, we use Perron's formula directly
on $\sum_{d \le X} b_d$ with $b_d := f(d)/d$. The Dirichlet series of $b_d$ is
$\hat F(\sigma) := \sum_d b_d/d^\sigma = T_3(\sigma + 1)$, which has a pole of
**order 2** at $\sigma = 0$ (inherited from $T_3$'s pole at $s=1$). The
shifted Laurent expansion is

$$
T_3(\sigma + 1) = \frac{c_2}{\sigma^2} + \frac{c_1}{\sigma} + c_0 + O(\sigma) \quad (\sigma \to 0).
$$

By Perron's formula (Tenenbaum II.2),

$$
\sum_{d \le X}{}^{\!*}\, b_d = \frac{1}{2\pi i}\int_{c - iT}^{c + iT} \hat F(\sigma) \frac{X^\sigma}{\sigma}\, d\sigma + (\text{Perron tail error}),
$$

where $c > 0$ is to the right of the pole. Shifting the contour past $\sigma = 0$
to a contour inside the VK region (transformed by $\sigma = s - 1$), we pick up
the residue at $\sigma = 0$:

$$
\text{Res}_{\sigma = 0}\left[\hat F(\sigma) \frac{X^\sigma}{\sigma}\right]
= [\sigma^0]\;\hat F(\sigma)\,X^\sigma
= [\sigma^0]\;\big(c_2/\sigma^2 + c_1/\sigma + c_0 + O(\sigma)\big)\,\big(1 + \sigma L + \sigma^2 L^2/2 + \cdots\big)
= \frac{c_2}{2} L^2 + c_1 L + c_0.
$$

Therefore the residue is **exactly** $c_2 L^2/2 + c_1 L + c_0$, identifying the
constant term as the $\sigma^0$ coefficient of $T_3(\sigma+1)$ at $\sigma = 0$,
i.e. the Laurent constant of $T_3$ at $s = 1$. **No partial summation is needed
to identify the constant term.**

The remaining shifted contour integral is bounded by the standard
SD/VK argument: along the shifted contour inside the VK region,
$|\hat F(\sigma)| \cdot |X^\sigma|/|\sigma|$ contributes
$O_A(1/(\log X)^A)$ for any $A > 0$, with implicit constant depending on $A$
through the SD parameters. The Perron-tail error is also $O_A(1/(\log X)^A)$
(by choosing $T = X$ or larger; standard).

Hence $\Sigma_3(X) - (c_2 L^2/2 + c_1 L + c_0) = O_A(1/(\log X)^A)$ for any
$A > 0$. $\square$

*Remark on the qualitative nature of the bound.* The "any $A > 0$" character
reflects that the implicit constant $C_A$ in $|r(X)| \le C_A/L^A$ grows with $A$,
both through Tenenbaum II.5.2's $C_N$ and through the contour-shift bookkeeping.
For fixed $A$, $C_A$ is finite and effective in principle (it can be computed
from VK constants and bounds on $\tilde H$ in the VK region), but we do not
track it explicitly here.

### Effective constant from numerics

Computing $\Sigma_3(X)$ by direct sieve at $X \in \{10^3, 10^4, 10^5, 10^6, 10^7\}$
(`bot/scratch/sigma3-effective-SD-validate.py`):

| $X$ | $\Sigma_3(X)$ | 3-term Laurent | residual $r(X)$ | $L^2 \cdot r$ | $L^3 \cdot r$ |
|---|---|---|---|---|---|
| $10^3$ | $10.5709$ | $10.5636$ | $+0.0074$ | $+0.35$ | $+2.43$ |
| $10^4$ | $15.5845$ | $15.5886$ | $-0.0041$ | $-0.34$ | $-3.17$ |
| $10^5$ | $21.5237$ | $21.5220$ | $+0.0018$ | $+0.23$ | $+2.67$ |
| $10^6$ | $28.3640$ | $28.3637$ | $+0.00024$ | $+0.05$ | $+0.62$ |
| $10^7$ | $36.1141$ | $36.1139$ | $+0.00020$ | $+0.05$ | $+0.85$ |

The residual flips sign and decays to $\sim 2 \cdot 10^{-4}$ at $X = 10^7$.
$L^2 \cdot r$ is bounded by $0.35$ across all five $X$; consistent (not proof) with
$|r(X)| \le 0.4/L^2$ in the regime tested. For the rigorous bound at any $A > 0$,
one would need a Tenenbaum-style explicit-constant computation (we do not need
that here — the qualitative bound $O_A(1/L^A)$ suffices for the band-difference
application).

## Application to the band-difference

Substitute $X = N^2+1$ in Theorem 1; using $\log(N^2+1) = 2L + O(1/N^2)$:

$$
\Sigma_3(N^2+1) = 2 c_2 L^2 + 2 c_1 L + c_0 + O(L/N^2) + O_A(1/L^A) = \frac{\text{pred}_3(N)}{N} + O_A(1/L^A),
$$

since the $O(L/N^2)$ term is utterly negligible (e.g., $\le 10^{-11}$ at $N = 10^6$),
and $\log(N^2+1) \asymp 2L$ so $1/(\log(N^2+1))^A \asymp 1/(2L)^A = O_A(1/L^A)$.
Multiplying by $N$:

$$
N \cdot \Sigma_3(N^2+1) = \text{pred}_3(N) + O_A(N/L^A).
$$

Combined with $S_3(N) = N \Sigma_3(N^2+1) + B_3(N)$:

$$
S_3(N) - \text{pred}_3(N) = B_3(N) + O_A(N/L^A).
$$

For the band $W_{K-1} = S_3(N) - S_3(n_-)$, $P^{(3,3)} = \text{pred}_3(N) - \text{pred}_3(n_-)$.
**Sanity check on $n_-$:** with $K = \lceil \log_2((N^2+1)/N)\rceil = \lceil \log_2(N + 1/N)\rceil$,
we have $2^{K-1} \in [(N + 1/N)/2,\; N + 1/N)$. Hence $\inf - 1 = N \cdot 2^{K-1} - 1
\ge N(N + 1/N)/2 - 1 = (N^2 + 1)/2 - 1$, giving $n_- = \lfloor\sqrt{\inf - 1}\rfloor
\ge \lfloor N/\sqrt 2 \cdot (1 + o(1)) \rfloor$. So $n_-/N \in [1/\sqrt 2 - o(1),\; 1]$
and consequently $L_{n_-} = L + O(1) \ge L/2$ for $N \ge 4$. Thus:

$$
W_{K-1} - P^{(3,3)} = \big[B_3(N) - B_3(n_-)\big] + O_A(N/L^A) + O_A(n_-/L_{n_-}^A) = \big[B_3(N) - B_3(n_-)\big] + O_A(N/L^A).
$$

This is the boxed conclusion above.

### Heuristic quantitative estimate at $N = 10^6$ (NOT rigorous)

The five data points in the table above suggest, **as an empirical fit only**,
$|r(X)| \lesssim 0.4/(\log X)^2$ for $X \in [10^3, 10^7]$. (As the skeptic
correctly noted, the same data are also consistent with $|r(X)| \lesssim 3.2/L^3$
or other shapes; the table cannot discriminate among these on 5 points.) If we
take the $0.4/L^2$ shape as a working hypothesis and extrapolate to $X = N^2+1$,
$\log X \approx 27.63$, then $|r(N^2+1)| \lesssim 5.2 \cdot 10^{-4}$ and the
SD-piece of $W_{K-1} - P^{(3,3)}$ is $\lesssim 10^3$, i.e. $\sim 0.5\%$ of the
empirical residual $2.13 \cdot 10^5$.

**This $0.5\%$ figure is heuristic.** It depends on (a) extrapolation of the
$0.4/L^2$ shape from $X \le 10^7$ to $X = 10^{12}$ (factor $\sim 1.5$ in $L$,
moderate), and (b) the choice of fit shape, which is not determined by 5 data
points. The rigorous statement is only that the SD-piece is $o(N/L^{A-1})$
for any $A > 0$, with effective but un-tracked constant.

The qualitative reading — *"the empirical residual is dominantly Hooley boundary,
not SD remainder"* — is supported but not rigorously proved by this argument.

## Strategic implications

1. **The SD chain is rigorously closed for $W_{K-1}$, qualitatively.** Theorem 1,
   applied as above, gives a clean rigorous *qualitative* bound on the SD-piece
   for any $A > 0$. The two-step decomposition flagged in the previous session
   is now executed for step (i) at the qualitative level. (Effective constants
   would require explicit tracking through Tenenbaum II.5.2 and the VK region
   parameters — not done here.)

2. **Asymptotic reduction to Hooley-boundary.** The conjecture
   $W_{K-1} - P^{(3,3)} = O(N)$ asymptotically reduces to
   $B_3(N) - B_3(n_-) = O(N)$ — a statement comparable in difficulty to the
   entire Hooley 1957 paper for $S_1 = \sum \tau(n^2+1)$. Unconditionally we
   only have $|B_3(N)| \le \sum_{d \le N^2+1} 2^{\omega(d)} \rho(d) = A_3(N^2+1)
   = O(N^2 (\log N)^c)$ via SD applied to $A_3$, far worse than $O(N)$.
   (Caveat: at fixed $N$, the SD remainder is bounded $O_A(N/L^A)$ for any $A$,
   but with no rigorous effective constant — so the reduction is asymptotic,
   not pointwise.)

3. **The empirical evidence gets a heuristic interpretation.** The 5-point
   $W_{K-1} - P^{(3,3)} \in [+0.04 N, +0.21 N]$ data is plausibly *evidence
   for Hooley-boundary cancellation* under the heuristic $|r(X)| \lesssim 0.4/L^2$:
   the SD-piece would be $\sim 0.5\%$ of the empirical residual at $N = 10^6$.
   This reading is heuristic, not rigorous — see the disclaimer above.

4. **Order-of-magnitude separator.** Without Theorem 1, the unconditional bound
   on the same residual would be $O(N^2 (\log N)^c)$; with it, the bound is
   $O(N^2(\log N)^c) + O_A(N/L^A)$ where the second term is provably
   sub-polynomial in $N$ for any $A$. So the SD piece is rigorously known to
   be sub-polylogarithmically smaller than any putative $N$ scaling, even at
   fixed $N$ where the explicit constant is unknown — a meaningful separation
   when ($O(N)$ is conjectured but $O(N^2 \cdot L^c)$ is unconditional).

## Documented soft spots (caveats)

- **The effective constant $C_A$ in Theorem 1 is qualitative.** The proof
  cites Tenenbaum II.5.2 with $z = 2$; the explicit constant depends on
  the Vinogradov–Korobov region for $\zeta$ (which is effective but
  un-clean) and on bounds for $\tilde H = L(\cdot, \chi_4)^2 H_3$ in that
  region. A careful track-through could give an explicit $C_A$, but is
  not needed for the qualitative separation here.

- **The $0.4/L^2$ empirical bound on $|r(X)|$ is from 5 data points across
  $X \in [10^3, 10^7]$ ($L \in [6.91, 16.12]$).** This is a heuristic
  effective constant. The rigorous statement is $r(X) = O_A(1/L^A)$ for
  any $A$; the $0.4/L^2$ shape is what the data supports but is not part
  of the theorem.

- **The boundedness check $|H_3(s)| \le C$ on the VK region was strengthened
  in this revision.** The argument uses the $p^{-s}$-coefficient cancellation at
  split primes ($1 - 3 + 3 = ?$ — actually, expanding $L_p(s) = (1+3p^{-s})(1-p^{-s})^3 = 1 - 3p^{-2s} + ...$, the linear-in-$p^{-s}$ coefficient is $3 - 3 = 0$,
  the universal cancellation), which makes each local factor $1 + O(p^{-2\Re s})$
  and the product convergent for $\Re s > 1/2$. On the VK region $\Re s \ge 0.6$,
  $\sum p^{-1.2}$ converges, so $\prod (1 + O(p^{-1.2}))$ is bounded; constant
  depends on the VK parameter but is $O(1)$. The literal $\epsilon$-uniform
  bound is not written out further.

- **$H_3''(1) \approx -0.234$ inherited from prior session at $p < 10^6$ truncation.**
  Truncation tail of order $10^{-5}$. Any error propagates linearly into $c_0$
  (and into the table residuals). Per the prior session, fourth-decimal
  accuracy on $b'_0 = c_0 \approx 0.939$ is fine for the conclusion drawn here.

- **$B_3(N)$ as defined here uses signed discrepancy $\delta_d = N_d - \rho(d)N/d$.**
  This is standard but the sign matters in summation. Cancellation in $\sum 2^{\omega(d)} \delta_d$ is the source of the conjectural $O(N)$ bound; without it, the trivial bound is $O(N^2 (\log N)^c)$.

## Connection to prior strategy

This continues from 2026-05-06 00:54 UTC ($P^{(3,3)}$ at $N = 10^6$). It
executes the highest-priority pickup hint #1: "**Effective Selberg-Delange
application**." The previous session listed "1 session, mostly bookkeeping" —
that estimate was correct.

The remaining open thread is the Hooley-boundary $B_3(N) - B_3(n_-) = O(N)$,
which is the same kind of cancellation that Hooley exploited in 1957 for
$S_1 = \sum \tau(n^2+1)$.

## Files

- `bot/scratch/sigma3-effective-SD-validate.py` (new — direct sieve and Laurent comparison).
- This note: `n2+1 ai thoughts/notes/proofs/P12-effective-SD-on-Sigma3.md`.
- Builds on: `n2+1 ai thoughts/notes/proofs/P12-W-Kminus1-N1e6-3term.md`,
  `n2+1 ai thoughts/notes/proofs/P12-W-Kminus1-symbolic-match.md`.
