# The $\mathcal{S}$-sequence

## Definition

$\mathcal{S}(k)$ is the integer sequence obtained by reading the **second components** of the [[03-divisor-pair-set|$\Phi_0$ tree]] row by row, left to right, starting at the root with index $k=1$:

$$\{\mathcal{S}(k)\}_{k\in\mathbb{N}} = \{0, 1, 1, 2, 3, 3, 2, 3, 7, 8, 5, 5, 8, 7, 3, \ldots\}$$

(indices: $k = 1,2,\ldots$ corresponding to root, then row 1 left-to-right, then row 2, etc.)

## Recursion

For $k \in \mathbb{N}$:
$$\begin{cases}
\mathcal{S}(4k) = 2\mathcal{S}(2k) - \mathcal{S}(k) \\
\mathcal{S}(4k+1) = 2\mathcal{S}(2k) + \mathcal{S}(2k+1) \\
\mathcal{S}(4k+2) = 2\mathcal{S}(2k+1) + \mathcal{S}(2k) \\
\mathcal{S}(4k+3) = 2\mathcal{S}(2k+1) - \mathcal{S}(k)
\end{cases}$$

Initial: $\mathcal{S}(1) = 0,\ \mathcal{S}(2) = 1,\ \mathcal{S}(3) = 1$.

This recursion expresses each $\mathcal{S}(4k+j)$ in terms of $\mathcal{S}(k), \mathcal{S}(2k), \mathcal{S}(2k+1)$ — i.e. a $4 \to 2$-step "doubling" rule. This is the defining property of [[15-k-regular-sequences|2-regular sequences]].

## Three properties of $\mathcal{S}$

1. **Boundary values**: $\mathcal{S}(2^n) = \mathcal{S}(2^{n+1} - 1) = n$ for all $n \in \mathbb{N}_0$.
2. **Fiber size = divisor count**: $|\mathcal{S}^{-1}(n)| = \tau(n^2 + 1)$.
3. **Primality criterion**: $n^2+1$ is prime iff $\mathcal{S}^{-1}(n) = \{2^n,\ 2^{n+1}-1\}$ — i.e. $n$ appears only on the two boundary positions.
4. **2-regularity** (Allouche–Shallit).

## Why this is the right reformulation

Landau's 4th becomes:

> $\mathcal{S}^{-1}(n) = \{2^n, 2^{n+1}-1\}$ for **infinitely many** $n$.

This is an **inverse-image cardinality** statement about a 2-regular sequence. Now ask: what does the asymptotic theory say about the typical fiber size?

Average fiber size: row $k$ of the tree has $2^k$ entries; the values populated in row $k$ go up to $\mathcal{S}(2^{k+1}-1) = k$ (boundary) but extend much further than $k$ in the middle of the row. By Bateman–Horn, average $\tau(n^2+1) \sim \log(n^2+1) \sim 2\log n$, so on row $k$ of the tree the typical $n$-value is around $\exp(O(k))$, no wait — let me be careful.

Row $k$ of the $\Phi_0$ tree has $2^k$ pairs. The second components vary; the boundary spines give $n = k$ on each side. The interior $n$-values can be large (up to of order $\sim$ $((1+\sqrt 5)/2)^{2k}$ or so by the matrix entry growth).

This means the sequence $\mathcal{S}$ is **growing exponentially in $k$ on most of its support**, but the *value $n$ is repeated $\tau(n^2+1)$ times across all rows* — fibers are scattered through the sequence.

## Connection to Stern's diatomic sequence

The sequence playing the analogous role for the [[16-calkin-wilf-tree|Calkin–Wilf tree]] is **Stern's diatomic sequence** (OEIS A002487):

$$a(2n) = a(n),\qquad a(2n+1) = a(n) + a(n+1)$$

Stern's sequence is also 2-regular. It has rich asymptotics (Allouche–Shallit, others). $\mathcal{S}$ is the analogue for the *divisor* tree of $n^2+1$ instead of the *positive rationals*.

## What's known asymptotically

The paper itself proves only a few asymptotic facts:
- Row sums of first components: $M_k = 5M_{k-1} - 2M_{k-2}$ (Theorem `phi0recursions`)
- Row sums of second components: $N_k = 5N_{k-1} - 2N_{k-2}$
- Row ratio sums: $R_k = R_{k-1} + 3 \cdot 2^{k-2}$, hence ratio-mean $\to 3/2$ as $k \to \infty$

(Same limiting ratio mean as Calkin–Wilf!)

## What we want

To approach Landau's 4th via $\mathcal{S}$, we'd want a **lower bound on the cardinality**:
$$\#\{n \le N : |\mathcal{S}^{-1}(n)| = 2\} \ge ??$$

The conjectured lower bound (from Hardy–Littlewood) is $\sim \sqrt N / \log N$. Even *any* lower bound going to infinity would be a major breakthrough.

The [[../research/R7-k-regular-asymptotics|Heuberger–Krenn theory]] gives precise asymptotics for *partial sums* of 2-regular sequences. We need *level-set* or *fiber* asymptotics — a different (and harder) regime. See [[../bridges/B4-S-sequence-density]].
