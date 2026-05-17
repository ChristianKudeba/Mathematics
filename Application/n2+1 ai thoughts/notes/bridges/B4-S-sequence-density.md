# Density results via the S-sequence

## The reduction

By [[../concepts/14-S-sequence|the S-sequence theorem]], Landau's 4th is equivalent to:
$$\#\{n \le N : |\mathcal{S}^{-1}(n)| = 2\} \to \infty\ \text{as}\ N \to \infty.$$

This is a **fiber-cardinality** question for a [[../concepts/15-k-regular-sequences|2-regular sequence]].

## The state of the art on level sets of regular sequences

Surveying what is known (will be filled in by [[../research/R7-k-regular-asymptotics]]):
- **Average fiber size**: easy from counting. Total = $2^k$ entries on row $k$, distinct values typically scattered, so on average each value is hit once or twice.
- **Distribution of $\mathcal{S}$ values**: row $k$ produces $2^k$ pairs, so $2^k$ values of $\mathcal{S}$. These values reach up to ~$\lambda_+^k = ((5+\sqrt{17})/2)^k \approx 4.56^k$ in the second component (interior of row).
- **Heuberger–Krenn** asymptotics give partial sums $\sum_{n \le N} \mathcal{S}(n) \sim N^\alpha \Phi(\log_2 N)$ for periodic $\Phi$ — but partial sums don't directly give level-set sizes.

## Why level sets are hard

For a generic 2-regular sequence, the level set $\mathcal{S}^{-1}(n)$ can have wildly varying size. The "average" size is $\tau(n^2+1) \sim \log n$, but the *variance* can be large.

The question "is $|\mathcal{S}^{-1}(n)| = 2$ infinitely often" is essentially asking for a **lower-density tail bound**. This is strictly harder than partial-sum asymptotics.

## Three concrete attacks

### Attack 1 — Generating function approach

Define $F(x) = \sum_n |\mathcal{S}^{-1}(n)| \cdot x^n = \sum_n \tau(n^2+1) x^n$.

By multiplicativity of $\tau$ and the Hecke decomposition of $n^2+1$ over $\mathbb{Z}[i]$:
$$\tau(n^2+1) = \sum_{(a+bi)(a-bi) | n^2+1} 1 = (\text{Hecke divisor sum})$$

So $F(x)$ is the generating function for Hecke divisor sums over Gaussian integers. The $L$-function $L(s, \chi)$ associated with the Hecke character of $\mathbb{Q}(i)$ enters.

If we can express $F(x)$ as $\sum_k 2 x^k + (\text{higher fiber terms})$ and the "$=2$ fibers" form a positive-density subset, we're done. But this is tautological — the difficulty is showing that the "$=2$ contributions" don't all bunch up at finitely many $n$.

### Attack 2 — Spectral / Hecke approach

Decompose $\mathcal{S}$ into Hecke eigencomponents. The recursion
$$\mathcal{S}(4k+j) = a_j \mathcal{S}(2k) + b_j \mathcal{S}(2k+1) + c_j \mathcal{S}(k)$$
should respect a hidden **Hecke action** of $\mathbb{Z}[i]$ on the sequence (since $\mathcal{S}$ encodes Gaussian divisors). Write
$$\mathcal{S}(n) = \sum_\chi \widehat{\mathcal{S}}(\chi) \cdot \chi(n)$$
for some characters $\chi$. Bound the off-diagonal contributions using $L$-function zero density / convexity.

This is speculative but matches the structure of Mauduit–Rivat's approach to digit-sum-of-primes.

### Attack 3 — Direct combinatorial reduction

Use the explicit recursion to compute a *generating function* for fiber sizes:
$$G(x, y) = \sum_n |\mathcal{S}^{-1}(n)|\ x^n y^{|\mathcal{S}^{-1}(n)|}$$
or equivalently the **distribution** of fiber sizes weighted by $n$. Heuberger–Krenn type asymptotics applied to $G$ might extract level-set asymptotics.

## What we'd need that doesn't exist

The crucial missing tool is a **fiber-cardinality asymptotic** for 2-regular sequences. Specifically:

> Conjecture (paraphrasing what we'd want): For a "generic" 2-regular sequence $s$ with appropriate non-degeneracy, the fiber sizes $|s^{-1}(n)|$ have a limiting distribution as $n \to \infty$, and the support of this distribution determines which fiber sizes occur infinitely often.

For Shakov's $\mathcal{S}$, the fiber sizes are exactly $\tau(n^2+1)$, so the conjecture would say: **$\tau(n^2+1)$ has a limiting distribution** — which is essentially the **Erdős–Kac theorem for $n^2+1$** (open in this exact form, but proved for related sequences).

## Erdős–Kac for $n^2+1$

The Erdős–Kac theorem for $n^2+1$ would say:
$$\frac{\omega(n^2+1) - \log\log(n^2+1)}{\sqrt{\log\log(n^2+1)}} \xrightarrow{d} \mathcal{N}(0,1)$$
as $n \to \infty$ (where $\omega$ counts distinct prime factors). This *is* known unconditionally for $n^2+1$ — it's a result of Halberstam (1956) — and it gives the *typical* number of prime factors, but doesn't bound the *minimum* (which is what Landau wants).

## Polynomial growth via Jordan structure

The [[../concepts/15-k-regular-sequences|matrix L]] generating $\mathcal{S}$ has triple eigenvalue 1, not diagonalizable — Jordan form
$$L \sim \begin{pmatrix}1 & 1 & 0\\ 0 & 1 & 1\\ 0 & 0 & 1\end{pmatrix}.$$

This means $\mathcal{S}(2^k n + r) \sim$ polynomial-in-$k$ × $\mathcal{S}(\text{base values})$. So $\mathcal{S}$ has **polynomial growth in $\log n$** along each "subsequence" — much slower than typical 2-regular sequences (which have polynomial-in-$n$ growth).

This is exceptional. It might be the structural reason that bringing automatic-sequence prime distribution machinery to bear is feasible. (Most automatic-sequence prime results are for *bounded* sequences; ours is *almost* bounded in a precise asymptotic sense.)

## Open question to research subagent

Does the Mauduit–Rivat methodology for sums-of-digits of primes extend to 2-regular sequences with **polylogarithmic growth**? If yes, we can plug in $\mathcal{S}$ and get a Mauduit–Rivat-style theorem about $\mathcal{S}(p)$ for $p$ prime — which would be stunning, but possibly not quite what Landau needs.

What Landau needs is more like: **fiber cardinality $|\mathcal{S}^{-1}(n)| = 2$ for infinitely many $n$**. The Mauduit–Rivat methodology computes correlations $\sum_{p \le N} f(\mathcal{S}(p))$ for nice $f$; a $\delta$-function $f = 1_{\{2\}}$ on the *fiber size* is at the very edge of what these methods can handle. But it's the right neighborhood of the literature.
