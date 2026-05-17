# $k$-regular sequences

## Definition (Allouche–Shallit 1992)

A sequence $s : \mathbb{N} \to \mathbb{Z}$ is **$k$-regular** if there exists $E \ge 0$ such that, for every $e \ge E$ and $0 \le r < k^e$, the subsequence $s(k^e n + r)$ can be written as a $\mathbb{Z}$-linear combination
$$s(k^e n + r) = \sum_i c_i \cdot s(k^{f_i} n + b_i)$$
with $f_i \le E$ and $0 \le b_i < k^{f_i}$.

Equivalently: the **$k$-kernel** $\{(s(k^e n + r))_n : e \ge 0, 0 \le r < k^e\}$ spans a finitely generated $\mathbb{Z}$-module.

## Examples

- **Stern's diatomic** $a(n)$ is 2-regular ([[16-calkin-wilf-tree]]).
- **The $\mathcal{S}$-sequence** of [[14-S-sequence]] is 2-regular by inspection of the recursion (each $\mathcal{S}(4k+j)$ is a $\mathbb{Z}$-linear combination of $\mathcal{S}(k), \mathcal{S}(2k), \mathcal{S}(2k+1)$).
- $\sum_i \nu_2(i)$ (sum of 2-adic valuations up to $n$) is 2-regular.
- Any **automatic sequence** is $k$-regular and bounded. The two notions coincide on bounded sequences.

## Why 2-regular is the right framework

Three reasons:

1. **Closed under arithmetic**: 2-regular sequences are closed under addition, multiplication by polynomials in $n$, and convolution. So natural operations preserve regularity.

2. **Linear-algebraic structure**: a 2-regular $s$ admits a representation as a *matrix product*:
$$s(n) = u^T M_{i_1} M_{i_2} \cdots M_{i_\ell} v$$
where $i_1 i_2 \cdots i_\ell$ is the binary expansion of $n$, and $M_0, M_1$ are fixed integer matrices. This is essentially saying: 2-regular sequences are the *abelianizations* of automaton outputs over $\mathbb{Z}$.

3. **Asymptotic theory**: Heuberger, Krenn, Lipnik, Shallit have developed precise asymptotics for partial sums $S(N) = \sum_{n \le N} s(n)$. Typically:
$$S(N) = N^{\log_k \rho} \cdot \Phi(\log_k N) + O(\text{error})$$
where $\rho$ is the spectral radius of the generating matrix and $\Phi$ is a continuous, periodic, **fractal** function (often Hölder-continuous of fractional degree).

See [[../research/R7-k-regular-asymptotics]] for the technical details.

## Matrix representation for $\mathcal{S}$

The recursion lifts to:
$$\begin{pmatrix}\mathcal{S}(2k) \\ \mathcal{S}(2k+1) \\ \mathcal{S}(k)\end{pmatrix} = M_? \cdot \begin{pmatrix}\mathcal{S}(k) \\ \mathcal{S}(?) \\ \mathcal{S}(?)\end{pmatrix}$$
or more cleanly: the vector $\mathbf{v}_k = (\mathcal{S}(k), \mathcal{S}(2k), \mathcal{S}(2k+1))^T$ satisfies $\mathbf{v}_{2k} = L \mathbf{v}_k$ and $\mathbf{v}_{2k+1} = R \mathbf{v}_k$ for the matrices
$$L = \begin{pmatrix}0&1&0\\-1&2&0\\0&2&1\end{pmatrix},\quad R = \begin{pmatrix}0&0&1\\0&1&2\\-1&0&2\end{pmatrix}$$
(both in $SL_3(\mathbb{Z})$, mutual conjugates by $\mathrm{diag}(1) \oplus J$).

So **$\mathcal{S}$ is $SL_3(\mathbb{Z})$-presented**, with a 3-dimensional state. This is small — there's hope that the spectral analysis is tractable.

## Spectral data of L (and R)

The two matrices are conjugate, so same spectrum. Compute $\det(L - \lambda I)$:
$$L - \lambda I = \begin{pmatrix}-\lambda&1&0\\-1&2-\lambda&0\\0&2&1-\lambda\end{pmatrix}$$

Expand along third column:
$$\det = (1-\lambda) \cdot \det\begin{pmatrix}-\lambda&1\\-1&2-\lambda\end{pmatrix} = (1-\lambda)(-\lambda(2-\lambda) + 1) = (1-\lambda)(\lambda^2 - 2\lambda + 1) = (1-\lambda)^3.$$

So **$L$ has triple eigenvalue $1$**. (Not diagonalizable — it's a Jordan block plus.) This is a degenerate case for the standard $k$-regular asymptotic theory (which assumes generic spectral radius).

This is *interesting* — the polynomial-growth rate of $\mathcal{S}$'s partial sums is governed by the Jordan structure rather than a dominant eigenvalue. The "eigenvalue 1" reflects the fact that $\mathcal{S}$ values are *bounded in some normalized sense* on the boundary spines (where $\mathcal{S}(2^n) = n$, linear in $n$).

This degeneracy is unusual and may need a **bespoke** analysis. See [[../bridges/B4-S-sequence-density]].

## What 2-regularity unlocks

- **Computability** of $\mathcal{S}$ in $O(\log n)$ time (just factor $n$ in binary, multiply matrices).
- **Hölder-continuous asymptotic profile** — $\mathcal{S}$ has a self-similar / fractal profile as $n \to \infty$.
- **Finite-state combinatorial structure** — there is a finite automaton (with $\mathbb{Z}$-output) computing $\mathcal{S}$.

The third bullet is the key one for [[../research/R8-automatic-sequences-and-primes|prime detection in automatic sequences]] (Mauduit–Rivat).
