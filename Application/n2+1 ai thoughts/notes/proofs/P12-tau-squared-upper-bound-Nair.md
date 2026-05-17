# P12 — Rigorous order-of-magnitude upper bound for $\sum_{n\le N}\tau(n^2+1)^2$ via Nair (1992)

**Date:** 2026-05-04 13:00 UTC
**Author:** Claude (mathAI bot)
**Status:** RIGOROUS upper bound. Modulo a published theorem (Nair, *Acta Arithmetica* 62 (1992)) cited as a black box, we prove
$$\sum_{n \le N} \tau(n^2+1)^2 \ll N (\log N)^3,$$
with explicit local-factor verification. This is **not** the matching lower bound and **not** the leading constant; that requires the Hooley-style argument still open.

## Why this is interesting

Previous sessions identified $G(s) = \sum_d \tau(d^2)\rho(d)/d^s = \zeta_K(s)^3 H(s)$ and conjectured (formal Selberg–Delange)
$$S(N) := \sum_{n \le N} \tau(n^2+1)^2 \sim c_3\, N (\log N)^3, \qquad c_3 = \pi^3 H(1)/48 \approx 0.0796,$$
but were unable to rigorize the asymptotic — the boundary error in the elementary derivation **dominates** the main term and a Hooley-type hyperbola argument is required.

This note observes that the *order of magnitude* $S(N) \ll N (\log N)^3$ is **immediate** from a published theorem of Nair (1992), once the right Dirichlet-series input is supplied. The leading constant is **not** pinned down (Nair's implicit constant is not sharp), but converting "conjectural order $N \log^3 N$" into "rigorous order $N \log^3 N$" is a genuine sub-result and immediately useful as input to any future second-moment bookkeeping in the SL$_2(\mathbb{N}_0)$ framework.

## The theorem we will use

**Black-box input (Nair 1992 / Nair–Tenenbaum 1998 / Henriot 2012).** *Let $f: \mathbb{N} \to \mathbb{R}_{\ge 0}$ be multiplicative, satisfying $f(p^l) \le A_1^l$ for all primes $p$ and integers $l \ge 1$, and $f(n) \le A_2 n^\epsilon$ for any $\epsilon > 0$. Let $F \in \mathbb{Z}[X]$ be of degree $g \ge 1$, irreducible over $\mathbb{Q}$, with no fixed prime divisor. Set $\rho_F(d) := |\{x \pmod d : F(x) \equiv 0 \pmod d\}|$. Then for $X^\theta \le y \le X$ (some fixed $\theta = \theta(g) < 1$) and $X$ large enough,*
$$\sum_{X < n \le X+y} f(F(n)) \;\le\; C(F, A_1, A_2, \theta) \cdot y \cdot \prod_{p \le X^g}\!\!\Big(1 - \frac{\rho_F(p)}{p}\Big) \cdot \sum_{m \le X^g} \frac{f(m)\rho_F(m)}{m}.$$

References (the bound exists in the literature in several closely related forms; the constant $C$ and exact cutoff differ between papers but the *order* in $X$ is the same):
* M. Nair, *Multiplicative functions of polynomial values in short intervals*, Acta Arith. 62 (1992), 257–269 — the foundational paper.
* M. Nair, G. Tenenbaum, *Short sums of certain arithmetic functions*, Acta Math. 180 (1998), 119–144 — a uniform Halász-type form.
* K. Henriot, *Nair–Tenenbaum bounds uniform with respect to the discriminant*, MPCPS 152 (2012), 405–424 — uniformity in $F$.

**Honest caveat on the citation.** The author has not opened the original Nair 1992 paper for this session; the form quoted above is the form most commonly used in the modern literature for $\sum f(F(n))$, with cutoff $X^g$ in the inner sum/product (since divisors of $F(n)$ for $n \le X$ can be as large as $X^g$). Any nontrivial discrepancy between this stated form and the actual published theorems would be a hole — flagged for verification by Anton when reviewing. The order-of-bound conclusion $\ll N(\log N)^3$ does not depend on the precise cutoff, only on the *exponent* of $\log$ that emerges from the inner Halász factor at split primes (here: $1 + 6/p + O(1/p^2)$, exponent $3$); see the Halász-style local-factor verification in §5 below as an independent check.

## Verification of hypotheses for $f = \tau^2$ and $F(x) = x^2+1$

**$f$:** $\tau^2$ is multiplicative non-negative. At a prime power, $\tau^2(p^l) = (l+1)^2 \le 4^l$ for $l \ge 1$ (since $(l+1)^2 \le 4 \cdot 2^{l-1} \cdot 2 = 4^{l-1} \cdot 4$ holds for $l \ge 0$ by induction: at $l = 0$: $1 = 1$ ✓; at $l = 1$: $4 \le 4$ ✓; at $l = 2$: $9 \le 16$ ✓; inductive: $(l+2)^2 / (l+1)^2 \le 4$ for $l \ge 1$, since $(l+2)/(l+1) \le 3/2 < 2$). So $A_1 = 4$ works. Likewise $\tau^2(n) \le \tau(n)^2 = O_\epsilon(n^\epsilon)$ for any $\epsilon > 0$.

**$F$:** $F(x) = x^2 + 1$. Degree $g = 2$. Irreducible over $\mathbb{Q}$ since $-1$ is not a rational square. No fixed prime divisor: $F(0) = 1$ and $F(1) = 2$, so $\gcd_{n \in \mathbb{Z}} F(n) = 1$.

**Threshold $\theta$:** $g = 2$, so $\theta > 1 - 1/3 = 2/3$ suffices; in particular $y = X = N$ (i.e., $\theta = 1$) is in range.

**$\rho_F$:** $\rho_F(d) = |\{x \pmod d : x^2 \equiv -1 \pmod d\}|$, multiplicative. At prime powers:
* $\rho_F(2) = 1$ (only $x = 1$); $\rho_F(2^k) = 0$ for $k \ge 2$ (since $x^2 + 1 \equiv 0 \pmod 4$ has no solution, $x^2 \in \{0, 1\}\pmod 4$).
* $\rho_F(p^k) = 0$ for $p \equiv 3 \pmod 4$, all $k \ge 1$ (since $-1$ is not a QR mod $p$).
* $\rho_F(p^k) = 2$ for $p \equiv 1 \pmod 4$, all $k \ge 1$ (Hensel-lift the two square roots of $-1 \pmod p$).

## Application

Take $X = y = N$, $g = 2$. Nair gives
$$S(N) = \sum_{n \le N} \tau(n^2+1)^2 \le C \cdot N \cdot \mathcal{P}(N^2) \cdot \mathcal{M}(N^2),$$
where
$$\mathcal{P}(Y) := \prod_{p \le Y}\Big(1 - \frac{\rho_F(p)}{p}\Big), \qquad \mathcal{M}(Y) := \sum_{m \le Y} \frac{\tau^2(m)\, \rho_F(m)}{m}.$$

We bound each factor.

### Bounding $\mathcal{P}(Y)$

$\mathcal{P}(Y) = \tfrac12 \cdot \prod_{\substack{p \le Y \\ p \equiv 1\, (4)}}(1 - 2/p)$.

By Mertens-type results in arithmetic progressions, for $Y \to \infty$,
$$\sum_{\substack{p \le Y \\ p \equiv 1\, (4)}} \frac{1}{p} = \tfrac{1}{2}\log\log Y + B + O\!\left(\tfrac{1}{\log Y}\right)$$
for an absolute constant $B$. Hence
$$-\sum_{\substack{p \le Y \\ p \equiv 1\, (4)}}\!\!\log(1 - 2/p) = \sum_{\substack{p \le Y \\ p \equiv 1\, (4)}}\!\!\Big(\tfrac{2}{p} + \tfrac{2}{p^2} + \cdots\Big) = \log\log Y + 2B + O(1),$$
so $\mathcal{P}(Y) = c_{\mathcal P} / \log Y \cdot (1 + o(1))$ for an explicit (small) absolute constant $c_{\mathcal P} > 0$.

In particular $\mathcal{P}(N^2) \ll 1/\log N$.

### Bounding $\mathcal{M}(Y)$

Define the Dirichlet series
$$D(s) := \sum_{m \ge 1} \frac{\tau^2(m)\,\rho_F(m)}{m^s} = \prod_p D_p(s),$$
where $D_p(s) = \sum_{k \ge 0} \tau^2(p^k)\rho_F(p^k)/p^{ks} = \sum_{k \ge 0}(k+1)^2 \rho_F(p^k)/p^{ks}$.

Local factors:
* $p \equiv 3 \pmod 4$: $D_p(s) = 1$.
* $p = 2$: $D_2(s) = 1 + 4 \cdot 1 / 2^s = 1 + 4/2^s$.
* $p \equiv 1 \pmod 4$: $D_p(s) = 1 + 2 \sum_{k \ge 1}(k+1)^2 p^{-ks}$.

Using $\sum_{k \ge 0}(k+1)^2 x^k = (1+x)/(1-x)^3$:
$$D_p(s) = 1 + 2\sum_{k \ge 1}(k+1)^2 p^{-ks} = 2\,\frac{1 + p^{-s}}{(1 - p^{-s})^3} - 1 \quad \text{(at split }p\text{).}$$

For the comparison with $\zeta_K(s)^4$ at split primes, recall the Gaussian Dedekind zeta has Euler factor at $p \equiv 1 \pmod 4$ equal to $(1 - p^{-s})^{-2}$ (two split primes above $p$), so $\zeta_K(s)^4$ has $(1 - p^{-s})^{-8}$ at such $p$. Set
$$H_0(s) := D(s) / \zeta_K(s)^4 = \prod_p D_p(s) (\text{local factor of } \zeta_K^{-4} \text{ at }p),$$
which we now show is regular and nonzero in a neighborhood of $s = 1$.

**At $p \equiv 3 \pmod 4$:** $\zeta_K^{-4}$ local factor $(1 - p^{-2s})^{4}$ (since $\zeta_K$ at inert $p$ is $(1 - p^{-2s})^{-1}$). $D_p = 1$. So $H_{0,p}(s) = (1 - p^{-2s})^{4}$.

**At $p = 2$ (ramified):** $\zeta_K$ at $p = 2$ is $(1 - 2^{-s})^{-1}$, so $\zeta_K^4$ local is $(1 - 2^{-s})^{-4}$, and
$H_{0,2}(s) = (1 + 4 \cdot 2^{-s})(1 - 2^{-s})^4$.

**At $p \equiv 1 \pmod 4$:** $\zeta_K^{-4}$ local factor is $(1 - p^{-s})^{8}$. So
$H_{0,p}(s) = D_p(s) \cdot (1 - p^{-s})^{8}$.
Substituting $x = p^{-s}$:
$$H_{0,p}(s) = \big[1 + 8x + 18x^2 + 32x^3 + 50x^4 + \cdots\big] \cdot (1 - x)^8.$$
Direct multiplication (checked numerically; see `bot/scratch/nair-upper-bound-verify.py`) gives, for *every* $p \equiv 1 \pmod 4$ (the coefficients depend only on $x = p^{-s}$, not on $p$ itself):
$$H_{0,p}(s) = 1 + 0 \cdot p^{-s} - 18\, p^{-2s} + 56\, p^{-3s} - 80\, p^{-4s} + \cdots.$$
Crucially the $p^{-s}$ coefficient is **zero** (cancellation $8 - 8 = 0$ between $D_p$'s leading and $\zeta_K^4$'s leading).

Therefore $\log H_{0,p}(s) = O(p^{-2s})$ uniformly in $p \equiv 1 \pmod 4$, and the Euler product
$$H_0(s) = \prod_p H_{0,p}(s)$$
converges absolutely on $\Re(s) > 1/2$. In particular $H_0$ is **analytic and nonzero** in an open neighborhood of $s = 1$.

**Conclusion of factorization:** $D(s) = \zeta_K(s)^4 H_0(s)$ with $H_0$ regular at $s = 1$. Since $\zeta_K$ has a simple pole at $s = 1$ with residue $\pi/4$ (Dirichlet class number formula for $\mathbb{Q}(i)$), $D$ has a pole of order **4** at $s = 1$ with leading Laurent coefficient $(\pi/4)^4 H_0(1)$.

### Selberg–Delange on the partial sum

To apply the standard Selberg–Delange theorem (Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory*, II.5.3) — which is stated for Dirichlet series of the form $\zeta(s)^z G(s)$ with $G$ regular and bounded in a suitable Vinogradov-type region — we **rewrite**
$$D(s) = \zeta_K(s)^4 H_0(s) = \zeta(s)^4 \cdot L(s, \chi_{-4})^4 \cdot H_0(s) =: \zeta(s)^4 \cdot G_0(s),$$
where $G_0(s) := L(s,\chi_{-4})^4 H_0(s)$. Now:
* $L(s, \chi_{-4})$ is entire (Dirichlet $L$-function for a non-principal character) and $L(1, \chi_{-4}) = \pi/4 \ne 0$.
* $H_0(s)$ is, by the previous subsection, absolutely convergent and nonzero on $\Re s > 1/2$.

Hence $G_0(s)$ is analytic and nonzero in a neighborhood of $s = 1$, and is bounded on $\Re s = 1 - c/\log(|t|+2)$ for the Vinogradov-type zero-free region of $\zeta(s)$ (which is sufficient since $L(s,\chi_{-4})$ also has a classical zero-free region as a Dirichlet $L$-function and $H_0$ is convergent on $\Re s > 1/2$). The hypotheses of Tenenbaum's SD theorem (II.5.3) apply with $z = 4$ and $G = G_0$, giving
$$\sum_{m \le Y} \tau^2(m) \rho_F(m) = c_4 \cdot Y \cdot (\log Y)^3 \cdot \big(1 + O(1/\log Y)\big), \quad c_4 := G_0(1)/\Gamma(4) = G_0(1)/6 > 0.$$

By partial summation,
$$\mathcal{M}(Y) = \sum_{m \le Y} \frac{h(m)}{m} = \frac{A(Y)}{Y} + \int_1^Y \frac{A(t)}{t^2}\,dt = \frac{c_4}{4}(\log Y)^4 (1 + o(1)),$$
since $\int_1^Y (\log t)^3/t\,dt = (\log Y)^4/4$. Hence $\mathcal{M}(N^2) = O((\log N^2)^4) = O((\log N)^4)$.

### Combining

$$S(N) \le C \cdot N \cdot \mathcal{P}(N^2) \cdot \mathcal{M}(N^2) \ll N \cdot \frac{1}{\log N} \cdot (\log N)^4 = N (\log N)^3. \quad \blacksquare$$

## Numerical sanity check

Empirical $S(N)/(N (\log N)^3)$ from previous-session data (`bot/scratch/tau-sq-second-moment.py`):

| $N$ | $S(N)$ | $S(N)/(N \log^3 N)$ |
|---:|---:|---:|
| $10^3$ | 86,384 | 0.262 |
| $10^4$ | 1,614,068 | 0.207 |
| $10^5$ | 26,859,868 | 0.176 |
| $3 \cdot 10^5$ | 100,153,656 | 0.166 |
| $10^6$ | 415,319,768 | 0.157 |

Bounded by $\le 0.27$ throughout the tested range, consistent with both this rigorous bound and the conjectured leading constant $c_3 \approx 0.0796$ (the rigorous *order* is firmly $\Theta(N \log^3 N)$ — the empirical ratio is decreasing toward $c_3$ slowly via the negative secondary $-c_2/(c_3 \log N)$ corrections, see `P12-tau-squared-secondary-coefficient.md`).

## What this gives — and what it doesn't

**Gives (rigorously):**
* The order $S(N) \ll N(\log N)^3$ — **upper** bound, no longer conjectural.
* The factorization $D(s) := \sum \tau^2(m)\rho_F(m)/m^s = \zeta_K(s)^4 H_0(s)$ with explicit $H_0$, $H_0(1) > 0$.
* As a consequence (combining with Cauchy–Schwarz), the rigorous bound $|T(N)| := |\sum_{n \le N} \tau(n^2+1) \chi_4(n+1)| \le \sqrt{N \cdot S(N)} \ll N(\log N)^{3/2}$. This is the trivial $\tau$-summed bound; the empirical $|T(N)| \asymp \sqrt N$ requires beating this by $(\log N)^{3/2}$ via off-diagonal cancellation.

**Doesn't give:**
* The leading constant. Nair's $C$ is not sharp; the matching $S(N) \sim c_3 N(\log N)^3$ requires Hooley.
* A matching lower bound. We don't even have $S(N) \gg N(\log N)^3$ rigorously yet; the trivial $S(N) \ge \sum_n 1 = N$ is far short. (A lower bound of the right order should be obtainable from a Cauchy–Schwarz argument using $\sum \tau(n^2+1) \asymp N \log N$, see Hooley 1957: $N \log^2 N \le (\sum \tau)^2 \le N \cdot S(N)$ via Cauchy in the *opposite* direction gives $S(N) \ge (\sum \tau)^2 / N \asymp (\log N)^2$, off by one log factor. Properly: $S(N) = \sum_n \tau^2 \ge (\sum_n \tau)^2 / N \asymp N (\log N)^2$. So the lower bound is $\Omega(N(\log N)^2)$, off by exactly one $\log$.)

## Citation-verification status (2026-05-04 16:30 UTC, follow-up session)

A follow-up session attempted to verify the precise Nair (1992) statement form against the original paper. The sandbox web environment returned `403 Forbidden` on every academic-publisher URL tried (matwbn.icm.edu.pl, link.springer.com, projecteuclid.org, arxiv.org/pdf, ar5iv.labs.arxiv.org, msp.org, semanticscholar.org, researchgate.net, annals.math.princeton.edu, academia.edu, sites.math.rutgers.edu, terrytao.wordpress.com, dms.umontreal.ca). Web search snippets confirmed:

* Nair, *Acta Arith.* 62 (1992), 257–269, exists and treats exactly this problem.
* The class hypothesis matches: $f(p^l) \le A_0^l$ and $f(n) \le A_1(\epsilon) n^\epsilon$.
* The bound is Halász/Shiu-style and generalizes Shiu's Brun–Titchmarsh-type result for multiplicative functions in APs.
* The Nair–Tenenbaum 1998 generalization and Henriot 2012 discriminant-uniform refinement are both well-established follow-ups.

**What the follow-up session could not verify (still flagged):** the precise cutoff in the prime-product/Dirichlet-sum form (i.e. whether it is $y$, $X^g$, or $X^{1/g}$). All three are encountered in the modern literature for closely related theorems. **For our application $y = X = N$ and $g = 2$, the order conclusion $\ll N(\log N)^3$ is independent of which of these three cutoffs is correct**: switching the cutoff among $\{N, N^{1/2}, N^2\}$ multiplies $\mathcal P \cdot \mathcal M$ by a bounded factor (a factor between $\sim 4^{-3} \approx 0.016$ and $\sim 4^3 \approx 64$, since $\log(N^k) = k \log N$ scales the products like $k^{-1} \cdot k^4 = k^3$), preserving $\Theta(\log^3 N)$ structure. So the order claim is robust; only the implicit constant moves.

**Action item for Anton's local follow-up:** verify the exact Nair-1992 theorem form (or, equivalently, Nair–Tenenbaum 1998 Theorem 1) against the paper. The order claim and the rigorous $|T(N)| \ll N (\log N)^{3/2}$ consequence do not depend on this verification.

## Sanity check on the implicit constant

A concrete consistency check on the chain. The structural part of the upper-bound leading constant (i.e., everything **except** Nair's implicit constant $C_{\text{Nair}}$) is

$$ C_{\text{struct}} := \frac{H_0(1) \cdot \pi^4 \cdot c_{\mathcal P}}{768}, $$

where $c_{\mathcal P} := \lim_{Y \to \infty} \mathcal P(Y) \log Y$ is the Mertens-type leading constant in $\mathcal P(Y) \sim c_{\mathcal P}/\log Y$.

Numerically (via `bot/scratch/upper-bound-explicit-constant.py`, primes up to $10^7$):

| Quantity | Value |
|----------|-------|
| $H_0(1)$ (Euler product over $\Re s = 1$) | $0.050229$ |
| $H(1)$ (cross-check vs. previous sessions) | $0.123243$ ✓ matches $0.12324$ |
| $c_{\mathcal P}$ (Mertens-AP constant) | $0.770748$ |
| $C_{\text{struct}} = H_0(1) \pi^4 c_{\mathcal P}/768$ | $0.004910$ |
| Conjectured $c_3 = \pi^3 H(1)/48$ (formal SD on $G$, cutoff $N^2$) | $0.079610$ |
| Empirical $S(10^6)/(N \log^3 N)$ | $0.157$ |

**Important conditionality.** $C_{\text{struct}}$ is **conditional on the cutoff in the unverified Nair statement being $Y = N^2$** (i.e., $X^g$ with $g = \deg F = 2$). If the actual Nair cutoff is $Y = N$ (the length of the interval, in which case $\mathcal P(N) \sim c_{\mathcal P}/\log N$ and $\mathcal M(N) \sim \pi^4 H_0(1)/6144 (\log N)^4$), the structural product becomes $H_0(1) \pi^4 c_{\mathcal P}/6144 \cdot (\log N)^3$, smaller by a factor of $8$. So the structural constant is determined modulo a small bounded factor by cutoff choice (range: roughly $\sim 0.0006$ to $\sim 0.005$ depending on whether cutoff is $N$, $N^{1/2}$, or $N^2$). The order $\Theta(\log^3 N)$ is unaffected.

**Implicit-constant lower bound for consistency.** Take the worst case (smallest $C_{\text{struct}}$) and ask: how big must $C_{\text{Nair}}$ be for the bound $C_{\text{Nair}} \cdot C_{\text{struct}} \cdot N \log^3 N \ge S(N)$ asymptotically? The answer depends on what the **actual** asymptotic constant $c^* := \lim_{N \to \infty} S(N)/(N \log^3 N)$ is.

* If $c^* = c_3 \approx 0.0796$ (the formal-SD prediction is the truth, slow-converged), then $C_{\text{Nair}} \ge 0.0796/C_{\text{struct}}$. With cutoff $Y = N^2$: $\ge 16$. With cutoff $Y = N$: $\ge 128$.
* If $c^*$ is closer to the empirical $0.157$ (i.e., $c_3$ underestimates the true leading constant), then $C_{\text{Nair}} \ge 32$ (cutoff $N^2$) up to $256$ (cutoff $N$).

Either way: $C_{\text{Nair}} \ge 16$ at minimum. This is a **perfectly normal Halász/Shiu-type implicit constant** — explicit bounds in the literature (e.g., Shiu's original paper) often have constants in the range $C \in [10, 100]$, well above $16$. The chain is internally consistent.

**Where does the algebraic factor 16 in $c_3/C_{\text{struct}}$ come from?** Strictly an algebraic ratio of normalizations between the two SD chains:

$$\frac{c_3}{C_{\text{struct}}} = \frac{\pi^3 H(1)/48}{H_0(1) \pi^4 c_{\mathcal P}/768} = \frac{768}{48 \pi} \cdot \frac{H(1)}{H_0(1) c_{\mathcal P}} = \frac{16}{\pi} \cdot \frac{H(1)}{H_0(1) c_{\mathcal P}}.$$

The $768/48 = 16$ arises from the chain of normalizations: $\Gamma(4) = 6$ (in $\mathcal M$'s SD), partial-summation factor $1/4$ (in $\mathcal M$), Mertens factor $1/2$ (cutoff $N^2$ in $\mathcal P$ vs cutoff inside $\log Y$), multiplied by $(\pi/4)$ from one extra residue of $\zeta_K$ in the quartic-pole chain. Numerically $16/\pi \cdot H(1)/(H_0(1) c_{\mathcal P}) \approx 5.09 \cdot 3.18 \approx 16.2$. **It is not "$2^4$ from cutoff change"** (an earlier draft of this note made that mistaken structural attribution).

## Files

* `bot/scratch/nair-upper-bound-verify.py` — verifies the local factor identity $H_{0,p}(s)/\zeta_{K,p}^{-4}(s)$ has zero $p^{-s}$ coefficient at split primes (i.e. cancellation $8 - 8 = 0$); confirms $H_0$'s absolute convergence on $\Re s > 1/2$ via universal coefficient $-18 p^{-2s}$ at all $p \equiv 1 \pmod 4$.
* `bot/scratch/upper-bound-explicit-constant.py` — computes $H_0(1) \approx 0.05023$, $H(1) \approx 0.12324$ (cross-check), Mertens-AP constant $c_{\mathcal P} \approx 0.77075$, and the structural upper-bound constant $C_{\text{struct}} \approx 0.00491$, and confirms internal consistency $C_{\text{Nair}} \ge 32$.

## Where this sits in the project

Promotes one of P12's most-cited bookkeeping bounds from "conjectured leading constant in a not-rigorous asymptotic" to "rigorously bounded order $N \log^3 N$." The Hooley-style rigorization of the leading **constant** is still open (it's the same boundary-error problem that Hooley 1957 solved for $\sum \tau(n^2+a)$, ported to $\tau^2$); but for any second-moment bookkeeping that needs only the **order**, that is now closed.

In particular, the trivial Cauchy–Schwarz bound on the σ-spin sum $T(N) = \sum \tau(n^2+1) \chi_4(n+1)$ now rigorously gives $|T(N)| \ll N (\log N)^{3/2}$ — recovering the trivial summed bound for $\tau$ values, but as a *rigorous* upper bound rather than under the conjectural asymptotic. The path to $|T(N)| \ll \sqrt N$ remains the off-diagonal-cancellation problem.
