# R3 — Friedlander–Iwaniec, parity-breaking, and why $n^2+1$ resists

The 1998 breakthrough of Friedlander and Iwaniec is the canonical example of a **parity-broken** prime-detection result for a thin polynomial sequence. Understanding what they did — and what they didn't — illuminates exactly why the same machinery does *not* yield Landau's 4th.

## Two papers, two technical pieces

1. **Asymptotic sieve for primes.** J. Friedlander, H. Iwaniec, Annals of Math. **148** (1998), 1041–1065. ([EuDML](https://eudml.org/doc/120008); [Semantic Scholar](https://www.semanticscholar.org/paper/Asymptotic-sieve-for-primes.-Friedlander-Iwaniec/54b983810bdca3ed7ad76f28330bd16699e41834))

   This paper develops an axiomatic sieve that *bypasses the parity problem* for a sequence $(a_n)$, **provided** one has both:
   - **Type I information** (level of distribution): for $D \le X^{1-\varepsilon}$ and any $d \le D$, the count of $a_n$ divisible by $d$ matches a smooth main term.
   - **Type II / bilinear information**: control of bilinear sums $\sum_{m,n} \alpha_m \beta_n a_{mn}$ for $m, n$ in suitable ranges (axiom $R(\nu)$ for some $\nu > 2/3$ — see Tao [Notes on the Bombieri asymptotic sieve, 2016](https://terrytao.wordpress.com/2016/07/17/notes-on-the-bombieri-asymptotic-sieve/)).

   When these hold, the sieve produces a **genuine asymptotic** for $\sum_n \Lambda(a_n)$ — i.e., counts primes among the $a_n$.

2. **The polynomial $X^2+Y^4$ captures its primes.** J. Friedlander, H. Iwaniec, Annals (companion paper) ([arXiv:math/9811185](https://arxiv.org/abs/math/9811185); preliminary [PNAS](https://www.pnas.org/doi/10.1073/pnas.94.4.1054)).

   They verify the bilinear axiom for $a_n = $ characteristic function of $\{a^2+b^4 \le X\}$, obtaining
   $$\sum_{a^2+b^4 \le X} \Lambda(a^2+b^4) \;=\; \frac{4\kappa}{\pi} \, X^{3/4} \big(1 + O(\log\log X / \log X)\big),$$
   with $\kappa = \int_0^1 (1-t^4)^{1/2}\,dt = \Gamma(1/4)^2/(6\sqrt{2\pi})$.

   The set $\{a^2+b^4 \le X\}$ has size $\asymp X^{3/4}$, so primes within it have natural density $\asymp X^{3/4}/\log X$.

## The technical heart — "spin"

The bilinear sum estimate hinges on the **spin** of a Gaussian integer $\alpha = a + bi$, defined via a Jacobi symbol $\mathrm{spin}(\alpha) = \left(\frac{\bar\alpha}{\alpha}\right)$ (suitably normalized). FI prove that the spin **equidistributes** in $\{\pm 1\}$ as $\alpha$ runs over Gaussian primes — a deep statement, since spin is *not* a Hecke character. This non-Hecke equidistribution is what injects information *outside* what a parity-symmetric sieve can see — formally, what is *not* captured by the smooth divisor-weighted sums of classical sieve theory. It is the parity-breaker.

Heath-Brown–Li (2015, [arXiv:1504.00531](https://arxiv.org/abs/1504.00531)) refined this to $a^2 + p^4$ ($p$ prime), exploiting Vinogradov-type major/minor-arc decomposition for the prime-restricted variable. Heath-Brown alone (Acta Math. **186** (2001)) handled $x^3 + 2y^3$ via a different cubic-form argument, again two-variable.

The most recent extension — **Green–Sawhney 2024**, [arXiv:2410.04189](https://arxiv.org/abs/2410.04189) — proves $p^2 + nq^2$ is prime infinitely often (with $p, q$ both prime, $n \equiv 0$ or $4 \pmod 6$), using the **quasipolynomial inverse theorem for Gowers norms** (Leng–Sah–Sawhney) to handle Type II sums in $\mathbb{Q}(\sqrt{-n})$. This is the first parity-breaking result that openly relies on additive-combinatorial inverse theorems rather than sieve combinatorics.

## Why this does *not* extend to $n^2+1$

The critical fact: every parity-broken polynomial result has $\ge 2$ free integer variables. For $a^2+b^4$, the parameter $b$ is the **bilinear partner** that $a$ oscillates against; the Type II sums decompose along $b$. Without it, there is nothing to decompose.

The set $\{n^2+1 : n \le N\}$ has $N$ elements in $[1, N^2]$ — density $1/\sqrt{x}$, **thinner** than $a^2+b^4$ (density $x^{-1/4}$) by half a power. More importantly, it is a **one-parameter family**, so:

- No bilinear decomposition is available — there is only one variable.
- No Gowers-norm arguments apply — the values do not contain APs of length $\ge 3$ (a quadratic sequence is "anti-AP").
- The Friedlander–Iwaniec spin equidistribution would have to be replaced by spin equidistribution **at squares of integers**, which is essentially the parity statement we are trying to prove.

Heath-Brown explicitly comments (informal lectures) that the FI machinery is "fundamentally two-variable" and that the one-variable analogue $n^2+1$ requires either:

(a) a deep new spectral input (e.g., subconvexity for the relevant $L$-function on average), or

(b) a totally different framework (e.g., automorphic / GL₂ approach via theta series), or

(c) breaking of a Siegel-zero scenario (Heath-Brown 1983, *Prime twins and Siegel zeros*).

None of these has materialized as of 2026.

## Density comparison — the "thin enemy"

| polynomial | values $\le X$ | density | proven? |
|---|---|---|---|
| $a^2 + b^2$ (sum of two squares) | $\sim X/\sqrt{\log X}$ | $X$ | YES — Fermat / Euler |
| $a^2 + b^4$ | $\sim X^{3/4}$ | $X^{3/4}$ | YES — FI 1998 |
| $a^3 + 2b^3$ | $\sim X^{2/3}$ | $X^{2/3}$ | YES — HB 2001 |
| $p^2 + nq^2$ ($p,q$ prime) | $\sim X/\log^2 X$ | thin in another sense | YES (some $n$) — GS 2024 |
| **$n^2 + 1$** | $\sim \sqrt X$ | $X^{1/2}$ | **NO — Landau's 4th** |

$n^2+1$ is thinner than every set parity-breaking has cracked. The Hardy–Littlewood prediction is
$$\#\{n \le N : n^2+1 \text{ prime}\} \sim C \cdot \frac{\sqrt N}{\log N}, \quad C = \prod_{p \text{ odd}} \left(1 - \frac{(-1/p)}{p-1}\right) \approx 1.3727\ldots$$
(Bateman–Horn 1962, [Garcia, *What is the Bateman–Horn conjecture?*, AMS Notices Oct 2024](https://www.ams.org/journals/notices/202410/rnoti-p1378.pdf); OEIS [A002496](https://oeis.org/A002496); discussion in Pintz, *Landau's problems on primes*, J. Théorie Nombres Bordeaux **21** (2009), 357–404, [Numdam](https://www.numdam.org/item/10.5802/jtnb.676.pdf).)

## Bridge to Shakov's framework

1. **The "missing variable" is supplied by the matrix.** The fundamental obstacle to applying FI to $n^2+1$ is the lack of a second integer variable for bilinear decomposition. Shakov's reformulation provides exactly this: each $n$ with $\tau(n^2+1) = k$ corresponds to $k$ matrices $A_1, \dots, A_k \in SL_2(\mathbb{N}_0)$ with cross-term $n$. The **matrix entries $(a, b, c, d)$ are four free integer variables** living on the surface $ad - bc = 1$. A bilinear sum $\sum_{a,b,c,d} \alpha_{(a,c)} \beta_{(b,d)} \mathbf{1}_{ad-bc=1, ac+bd=n}$ becomes structurally available — at the cost of working on a thin orbit. This re-opens a Type II decomposition that is invisible at the level of the polynomial $n^2+1$ alone.

2. **Spin $\leftrightarrow$ tree-position parity.** The FI spin $\left(\frac{\bar\alpha}{\alpha}\right)$ is a function on Gaussian integers that captures information outside the Hecke characters. Under the Shakov bijection, Gaussian divisors of $n^2+1$ become positions in the $\Phi_0$ tree. The natural tree analogue of spin is a **$\pm 1$-valued function on tree positions** distinguishing left/right children at each branching — i.e., the parity of the number of $S$'s in the $S/T$-word. This is *exactly* the kind of parity-twisted weight that the parity problem says sieves cannot see, and Shakov's setup makes it explicit and combinatorial.

3. **Density rescue via the boundary count.** FI succeed for $a^2+b^4$ partly because the set has density $X^{3/4}$ — comfortably above sieve thresholds. $n^2+1$ has density $\sqrt X$, below. But in tree terms the density of the **boundary** (where primality lives) is $2$ per row of the $\Phi_0$ tree (the two spines), out of $2^k$ entries — i.e., density $2^{-k+1}$, exponentially thin. So the apparent thinness of the prime set is reframed as an *exponentially-rare-but-deterministic-position* statement on a tree, where row-recursion ([[../concepts/18-row-recursions]]) gives exact algebraic control. In particular, primality is no longer a *probabilistic* event resisted by the parity problem — it is a *deterministic* boundary-of-tree event. See [[R2-parity-problem]] §"Bridge" point 3 and [[../bridges/B4-S-sequence-density]].
