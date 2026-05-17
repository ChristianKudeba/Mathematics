# R1 — Iwaniec, the half-dimensional sieve, and almost-primes for $n^2+1$

The cornerstone unconditional result toward [[../concepts/10-landau-fourth-problem|Landau's 4th]] is

> **Iwaniec (1978).** $n^2+1$ has at most two prime factors infinitely often; equivalently $\#\{n\le N : n^2+1 \in P_2\} \gg \sqrt{N}/\log N$.

Reference: H. Iwaniec, *Almost-primes represented by quadratic polynomials*, Inventiones Math. **47** (1978), 171–188 ([SpringerLink](https://link.springer.com/article/10.1007/BF01578070)). The proof uses Iwaniec's own **half-dimensional sieve**, developed in *The half dimensional sieve*, Acta Arithmetica **29** (1976), 69–95 ([EuDML](https://eudml.org/doc/205410); [PDF](https://bibliotekanauki.pl/articles/1393491.pdf)). A clean modern exposition (Master's thesis level) is Karatsuba-style writeup *Almost-Primes Represented by Quadratic Polynomials* ([arXiv:1910.02885](https://arxiv.org/abs/1910.02885)).

## What "half-dimensional" means

The **dimension** $\kappa$ of a sieve problem is the average number of residue classes sifted per prime:
$$\sum_{p\le z} \frac{\nu(p) \log p}{p} = \kappa \log z + O(1).$$
For sifting an arithmetic progression $\kappa = 1$. For sifting $\{a^2+b^2 \le x\}$ — i.e., Gaussian-norm values — one has $\kappa = 1/2$ because primes split in $\mathbb{Z}[i]$ with density $1/2$ (those $p \equiv 1 \pmod 4$).

For the polynomial sequence $a_n = n^2+1$ the relevant quantity is the number of residues $n \pmod p$ with $p \mid n^2+1$, i.e.
$$\nu(p) = 1 + \left(\frac{-1}{p}\right) = \begin{cases} 2 & p \equiv 1 \pmod 4\\ 0 & p \equiv 3 \pmod 4 \end{cases}$$
By Dirichlet, $\sum_{p\le z} \nu(p)/p \sim \tfrac12 \log\log z$, hence $\kappa = 1/2$. **This is the "half" in half-dimensional.** It is the same as Selberg's $\kappa$ for sums of two squares, because $n^2+1$ is itself a (degenerate) norm form (cf. [[R4-binary-quadratic-forms]] — $\Delta=-4$, ring $\mathbb{Z}[i]$).

The technical innovation of Iwaniec 1976 is an **optimal Rosser-type construction** at $\kappa=1/2$: he shows the Buchstab/Jurkat–Richert system at this dimension admits an exact solution where Rosser's $\beta=1$ truncation is sharp — yielding *both* upper and lower bounds with the right constants. (Notes: [Joni's notes on Rosser–Iwaniec](http://jonismathnotes.blogspot.com/2015/02/the-rosser-iwaniec-sieve.html); Ford, *Basic sieve methods*, [PDF](https://ford126.web.illinois.edu/sieve2023.pdf).)

## Why $P_2$, not $P_1$

The sifting limit at dimension $\kappa$ is a number $\beta(\kappa)$ such that one can sift up to $z = N^{1/\beta}$ and still get a non-trivial lower bound. For $\kappa=1/2$ one has $\beta(1/2)=1$, so $z = N$, but combinatorics forces *at least two* unsifted prime factors in the lower-bound regime. To reach $P_1$ (genuine primes) one would need $z = N^{1/2-\varepsilon}$ at this dimension, which violates the [[R2-parity-problem|parity barrier]] — Selberg's example shows no purely combinatorial sieve can do better than $P_2$ at any $\kappa$.

## The chain of improvements toward Landau via "greatest prime factor"

A weaker but still illuminating proxy is the **greatest prime factor** $P^+(n^2+1)$. Landau's conjecture is equivalent to $P^+(n^2+1) \ge n^2/\log^A n$ infinitely often. The best unconditional exponents:

| Year | Author(s) | Exponent $\theta$ s.t. $P^+(n^2+1) \ge n^\theta$ i.o. | Reference |
|---|---|---|---|
| 1934 | Chebyshev / Markov | trivial $\theta = 1$ | classical |
| ... | (long history) | ... | ... |
| 2019 | de la Bretèche–Drappeau | $\theta = 1.2182$ | — |
| 2022 | Merikoski | $\theta = 1.279$ | [arXiv:1908.08816](https://arxiv.org/abs/1908.08816) |
| 2024/26 | Pascadi | $\theta = 1.3$ via large sieve for exceptional Maass forms | [arXiv:2404.04239](https://arxiv.org/abs/2404.04239), Forum of Math Pi (2026) |
| 2025 | Grimmelt–Merikoski | $\theta = 1.312$ unconditionally (was conditional on Selberg eigenvalue conjecture) | [arXiv:2505.00493](https://arxiv.org/abs/2505.00493) |

Landau requires $\theta = 2$. The current ceiling around $\theta \approx 4/3$ is set by the level of distribution available for the relevant Kloosterman / Maass-form spectral inputs (Deshouillers–Iwaniec). Pushing past it appears to require new spectral inputs — Selberg eigenvalue conjecture would yield $\sim 1.312$ but still falls far short of 2.

These "greatest prime factor" results are *parallel* to, but distinct from, the $P_2$ result: they bound the **size** of the largest prime factor while $P_2$ bounds the **number** of prime factors. Both stop well short of "is prime" ($P_1$).

## Bridge to Shakov's framework

1. **Sieve weights vs. tree-counts.** The half-dimensional sieve weights $\sum_{d\mid n^2+1} \lambda_d$ count divisors of $n^2+1$ with sieve coefficients. In Shakov's setup, divisors of $n^2+1$ are *bijectively* enumerated by matrices $A \in SL_2(\mathbb{N}_0)$ with cross-term $ac+bd = n$ (cf. [[../concepts/13-prime-characterization]]). The Iwaniec weights $\lambda_d$ become weights on **tree positions** in the $\Phi_0$ tree. The combinatorial constraint "$d \mid n^2+1$" becomes "$A$ lies above $n$ in the tree". This is more rigid than a sieve weight: it carries the full $S/T$-word data, not just the divisor.

2. **The dimension $\kappa = 1/2$ as a tree statistic.** The reason $\kappa = 1/2$ for $n^2+1$ is that primes split in $\mathbb{Z}[i]$ with density $1/2$. Translated to the tree: each row $k$ of $\Phi_0$ has $2^k$ entries, and the typical second component grows like $\lambda_+^k$ with $\lambda_+ = (5+\sqrt{17})/2 \approx 4.56$. The ratio $\log 2 / \log \lambda_+ \approx 0.456$ is suggestively close to $1/2$ — a possible **transfer-operator interpretation** of the half-dimension. Concretely: the reason sieves cap at $P_2$ might be reformulated as a spectral-radius statement for the tree's row-recursion ([[../concepts/18-row-recursions]]).

3. **Greatest-prime-factor as boundary statistic.** $P^+(n^2+1) \ge n^\theta$ means that, in the divisor pair $(d, n^2+1/d)$, the larger factor is $\ge n^\theta$. In tree terms: the matrix $A \in SL_2(\mathbb{N}_0)$ realizing the divisor lies *close to the boundary spine* (the boundary corresponds to the trivial factorization $1 \cdot (n^2+1)$, which has $P^+ = n^2+1$, the maximum). So Pascadi/Grimmelt–Merikoski's results are statements about how often $A$ is "near boundary." The Shakov reformulation suggests these should follow from estimates on **boundary-mass concentration** in the [[../concepts/14-S-sequence|$\mathcal{S}$-sequence]].

See [[../bridges/B5-affine-sieve-attack]] for related machinery and [[../bridges/B4-S-sequence-density]] for the level-set program.
