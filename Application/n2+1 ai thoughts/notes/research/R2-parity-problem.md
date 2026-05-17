# R2 — The parity problem and the $P_2 \to P_1$ wall

The structural reason no purely sieve-theoretic argument has reached "$n^2+1$ is prime infinitely often" — only "$n^2+1$ has $\le 2$ prime factors" — is the **parity problem**, identified by Atle Selberg in 1949.

References: [Wikipedia: Parity problem (sieve theory)](https://en.wikipedia.org/wiki/Parity_problem_(sieve_theory)); Tao, *The parity problem in sieve theory* ([blog post 2007](https://terrytao.wordpress.com/2007/06/05/open-question-the-parity-problem-in-sieve-theory/)); Tao, *A general parity problem obstruction* ([blog 2014](https://terrytao.wordpress.com/2014/11/21/a-general-parity-problem-obstruction/)); Selberg, *Lectures on Sieves* (Collected Papers vol II, Springer 1991); Heath-Brown, *A parity problem from sieve theory*, Mathematika **29** (1982), 1–6.

## The Selberg construction

Let $\mathcal A_e \subset [1,x]$ be integers with no prime factor $\le x^{1/u}$ and an **even** number of prime factors; $\mathcal A_o$ likewise with **odd** number. Selberg observed that no combinatorial sieve, applied with weights $\lambda_d$ vanishing for $d > x^{1/u}$ (with $u$ small), can distinguish $\mathcal A_e$ from $\mathcal A_o$. The Möbius-inversion identity $\mathbf{1}_{n=1} = \sum_{d\mid n}\mu(d)$ that the sieve emulates is *blind to the Liouville function* $\lambda(n) = (-1)^{\Omega(n)}$ at the level of moments accessible to the sieve.

Concretely, both $|\mathcal A_e|$ and $|\mathcal A_o|$ admit upper bounds of $(2 + o(1)) x/(u \log x)$ from Brun's or Selberg's sieve. But $|\mathcal A_e|$ may be near $0$ (e.g., when $u < 2$, every element of $\mathcal A_o$ is a single prime and $\mathcal A_e$ is empty), while $|\mathcal A_o|$ matches its upper bound. The **factor of 2** is the parity loss.

## The formal obstruction (Tao, 2007)

> If $A \subset \mathbb{N}$ consists entirely of integers with $\Omega(n)$ of one fixed parity, then sieve theory alone gives no nontrivial *lower* bound on $|A \cap [1,x]|$ — and any *upper* bound is off from the truth by $\ge 2$.

The mechanism: the Liouville function $\lambda(n)$ is *orthogonal* to all "smooth" sums of the kind sieves can compute (sums over divisors weighted by Möbius-like coefficients). So perturbations $f \mapsto f \cdot (1 + \lambda)$ leave sieve outputs invariant but can take a set entirely from "all primes" to "all $P_2$'s with two distinct primes" — and the sieve can't tell.

## Why this stops $P_2 \to P_1$ for $n^2+1$

Iwaniec's [[R1-iwaniec-and-sieves|half-dim sieve]] gives $\#\{n\le N : n^2+1 \in P_2\} \gg \sqrt N/\log N$. To upgrade to $P_1$ requires sieving with level of distribution $z = N$ at dimension $\kappa = 1/2$, which forces the residual factor count to be controlled by **bilinear (Type II) sums** $\sum_{m\sim M, n \sim N} a_m b_n e(\dots)$ over the values of the polynomial. For *one-variable* polynomials of degree $\ge 2$, these bilinear sums are not accessible:

- The set $\{n^2+1 : n \le N\}$ has $N$ elements but lives in $[1, N^2]$ — density $1/\sqrt x$, very thin.
- Bilinear decomposition $n^2+1 = m \cdot k$ requires Gaussian-integer factorization, which gives **only one degree of freedom** ($n$) for the joint parameter $(m,k)$.
- There is no "second variable" to oscillate against.

This is exactly the obstruction that does **not** appear for $a^2+b^4$: in that two-variable problem the parameter $b$ supplies the oscillation needed. See [[R3-friedlander-iwaniec]].

## Heath-Brown 1982 — Equivalence formulation

Heath-Brown (Mathematika **29**, 1982, 1–6, [Cambridge Core](https://www.cambridge.org/core/journals/mathematika/article/abs/parity-problem-from-sieve-theory/A35B61ACBE82889EE5F568091D03A602)) gave the parity problem its sharpest form: the parity barrier at $P_2$ is **equivalent** to a non-correlation statement of the form
$$\sum_{n \le x} \lambda(n) \alpha_n = o\left(\sum_n |\alpha_n|\right)$$
for arbitrary "sieve-admissible" sequences $\alpha_n$. Breaking the parity barrier requires controlling such Liouville sums against the specific $\alpha_n$ from your problem.

## Known parity-breaking results

| year | result | key new ingredient | reference |
|---|---|---|---|
| 1996/98 | Friedlander–Iwaniec: $a^2+b^4$ prime ∞ often | "spin" Jacobi-symbol equidistribution over Gaussian primes; bilinear sum estimates | Annals **148** (1998), 1041–1065 |
| 2001 | Heath-Brown: $x^3 + 2y^3$ prime ∞ often | Vaughan identity + cubic-form algebra | Acta Math. **186** (2001), 1–84 |
| 2015/26 | Heath-Brown–Li: $a^2 + p^4$ ($p$ prime) | refines FI; uses GL₂ analogue / level of distribution for primes | [arXiv:1504.00531](https://arxiv.org/abs/1504.00531) |
| 2024 | Green–Sawhney: $p^2 + nq^2$ ($p,q$ prime), $n\equiv 0,4 \pmod 6$ | quasipolynomial inverse theorem for Gowers norms; concatenation theorems | [arXiv:2410.04189](https://arxiv.org/abs/2410.04189), Annals (to appear) |

Other inputs that defeat parity in different settings: **Siegel zeros** (Heath-Brown, twin primes given Siegel-Landau), **Vinogradov three-primes** (uses major-arc/minor-arc structure), **Green–Tao** (relative Szemerédi via pseudorandom majorants).

## Why none of these techniques touches $n^2+1$

Every parity-broken polynomial result so far has *at least two free integer variables*. The reason is structural — Tao's analysis (2014) shows that the parity-breaking ingredient must inject Liouville-correlation information *not* captured by the sieve. For two-variable polynomials this can be done by:

- factoring across one variable (Gaussian for $a^2+b^4$) and using oscillation in the other;
- exploiting Type II sums over a bilinear $(a,b)$-product structure;
- applying inverse-Gowers theory, which requires a "thick" set with additive-combinatorial structure.

A single-variable polynomial $f(n)$ supplies neither bilinear room nor additive-combinatorial structure (the values are in geometric progression, not an AP-rich set). $n^2+1$ is the prototypical case: even the **two-variable cousin** $a^2+1 \cdot b^0$ collapses to the same single-variable difficulty.

Tao (2007 blog) explicitly mentions $n^2+1$ as the canonical example of a problem where "one cannot hope to use plain sieve theory to just count primes."

## Bridge to Shakov's framework

1. **The Liouville obstruction in tree language.** The Liouville function on $n^2+1$ pulls back to a $\pm 1$-valued function on positions of the $\Phi_0$ tree: $\lambda(n^2+1) = (-1)^{\Omega(n^2+1)} = (-1)^{|\mathcal{S}^{-1}(n)| - 1}$ (using $\tau = 2^{\omega}$ for squarefree, and the [[../concepts/14-S-sequence|fiber-size identity]]). So the parity problem becomes: *sieves cannot distinguish even-fiber-size from odd-fiber-size $n$'s in $\mathcal{S}$*. This is a concrete combinatorial reformulation. The Shakov framework gives an **exact** count $|\mathcal{S}^{-1}(n)| = \tau(n^2+1)$, not a sieve estimate — so it is, in a precise sense, **already past the parity barrier** in terms of *counting*. The remaining question is whether one can detect when the count equals 2.

2. **Liouville sums on the tree.** The parity-breaking sum $\sum_n \lambda(n^2+1) \alpha_n$ corresponds, in tree language, to $\sum_{n} (-1)^{|\mathcal{S}^{-1}(n)|-1} \alpha_n$. The 2-regular structure of $\mathcal{S}$ ([[../concepts/15-k-regular-sequences]]) gives a **transfer matrix** whose spectrum controls this sum. If the transfer matrix has a nontrivial spectral gap on a parity-twisted subspace, that *would* break parity. This is closer to "automatic-sequence + Allouche–Shallit" technology than to sieve theory.

3. **Boundary-only $\Leftrightarrow$ prime as a deterministic statement.** Critically, the [[../concepts/12-boundary-vs-interior|boundary-vs-interior dichotomy]] does not need a sieve at all. The statement "$n^2+1$ prime $\iff n$ appears only on the spine of the $\Phi_0$ tree" is **exact**. It bypasses the parity problem because it does not approximate primes by almost-primes — it *characterizes* primes via tree position. The route forward (cf. [[../bridges/B4-S-sequence-density]]) is to estimate the cardinality of the spine-only set directly via 2-regular asymptotics, **without** invoking any sieve weights and hence without inheriting the parity loss.
