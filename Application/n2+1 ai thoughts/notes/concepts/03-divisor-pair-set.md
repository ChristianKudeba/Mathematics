# Divisor pair set $\mathcal{D}_f$

## Definition

For $f \in \mathbb{Z}[x]$:
$$\mathcal{D}_f := \{(m, n) \in \mathbb{N}_0 \times \mathbb{N}_0 : m \mid f(n)\}.$$

A point $(m,n) \in \mathcal{D}_f$ records the bare fact "$m$ divides $f(n)$" with no extra structure. The set is naturally infinite, with one row per $n$ giving $\tau(|f(n)|)$ pairs.

## Lattice geometry

Picture $\mathcal{D}_f$ as a 2D point cloud in the first quadrant:
- Horizontal axis: $n$
- Vertical axis: $m$
- Above each $n$, points $(m,n)$ for each divisor $m$ of $|f(n)|$.

The "boundary" points are $(1, n)$ (always present) and $(|f(n)|, n)$ (always present). The "interior" points are nontrivial divisors.

## Three structural maps on $\mathcal{D}_f$

The paper equips $\mathcal{D}_f$ with three operations (see [[04-equivariant-map]]):

| symbol | formula | order | depends on $f$? |
|---|---|---|---|
| $\bar S$ | $(m, n) \mapsto (m, m+n)$ | $\infty$ | no |
| $\bar c_f$ | $(m, n) \mapsto (|f(n)|/m,\ n)$ | 2 | yes |
| $\bar T_f$ | $\bar c_f \bar S \bar c_f$ | $\infty$ | yes |

All three preserve the property "$m \mid f(n)$" — see Proposition `invariance`.

- $\bar S$ shifts $n$ by one period of $m$ (since $m\mid f(n) \Rightarrow m \mid f(n+m)$).
- $\bar c_f$ swaps a divisor with its complementary divisor.
- $\bar T_f$ does the analogous shift for the complementary factor.

## Why this is the natural codomain for [[01-sl2-n0-monoid|SL₂(ℕ₀)]]

The $\bar S, \bar T_f$ pair satisfies the **same monoid presentation** as the matrix generators $S, T$: free, no relations. So an SL₂(ℕ₀)-equivariant map is determined by its value at $I$, and we choose $I \mapsto (1,0)$ (the "trivial divisor of $f(0)$" base point — possible iff $|f(0)| = 1$, which the paper proves is forced).

## Forbidden points

Lemma (`lemma_(0,n)`): if $f$ is enumerable then $(0, n) \notin \mathcal{D}_f$, i.e. $f$ is **nonvanishing on ℕ₀**. This is automatic from invertibility: $\bar S(0,n) = (0,n)$ would be a fixed point, breaking injectivity.

So: enumerability ⇒ $f$ has no integer roots in ℕ₀.

## Key counting fact

For each enumerable $f$:
$$|\{A \in SL_2(\mathbb{N}_0) : (\text{cross-term})(A) = n\}| = \tau(|f(n)|).$$

For $f = \phi_0$: number of matrices with $ac+bd = n$ equals $\tau(n^2+1)$. This is **Theorem `divisorcount`**.

So **counting representations** of $n^2+1$ by the binary quadratic form $X^2 + Y^2$ becomes **counting words in the free monoid** on $S,T$ with a prescribed cross-term value. See [[13-prime-characterization]].
