# Row-sum recursions for $\Phi_0$

## Three statistics (Definition `sumsandavgsdefns`)

For row $k$ of the [[14-S-sequence|$\Phi_0$ tree]] (which has $2^k$ pairs):
$$M_k := \sum_{(m,n) \in \mathrm{row}_k} m,\quad N_k := \sum_{(m,n) \in \mathrm{row}_k} n,\quad R_k := \sum_{(m,n) \in \mathrm{row}_k} \frac{n}{m}$$

## Recursions (Theorem `phi0recursions`)

$$M_k = 5 M_{k-1} - 2 M_{k-2},\quad M_0 = 1, M_1 = 3$$
$$N_k = 5 N_{k-1} - 2 N_{k-2},\quad N_0 = 0, N_1 = 2$$
$$R_k = R_{k-1} + 3 \cdot 2^{k-2},\quad R_0 = 0$$

## Closed forms (Cor `closed_forms`)

Characteristic polynomial of the $5x - 2y$ recursion: $\lambda^2 - 5\lambda + 2 = 0$, roots $\lambda_\pm = (5 \pm \sqrt{17})/2$.

$$M_k = \frac{1}{34}\left(-\lambda_-^k(-17+\sqrt{17}) + \lambda_+^k(17+\sqrt{17})\right) \asymp \lambda_+^k$$

Note: $\lambda_+ \approx 4.5615$.

$$R_k = \tfrac{3}{2}(2^k - 1)$$

## Asymptotic ratio mean

Cor `phi0average`: $\lim_{k\to\infty} R_k / 2^k = 3/2$. Same as Calkin–Wilf ([[16-calkin-wilf-tree]]).

## Structural meaning

- The eigenvalue $\lambda_+ = (5+\sqrt{17})/2$ controls the **spectral growth** of both $M_k$ and $N_k$ — the average pair component grows like $\lambda_+^k / 2^k = (5+\sqrt{17})/4 \approx 2.28$ per row.
- This is the **right-coordinate** analogue of the Hölder exponent for the [[15-k-regular-sequences|2-regular sequence]] $\mathcal{S}$.

## What's not yet in the paper

The paper proves row-sum recursions but does *not* extract:
- **Variance** of $m$ across a row (would tell us about the spread of divisor sizes).
- **Higher moments** $\sum m^p$ (would give Hardy–Littlewood-style densities).
- **Joint distribution** of $(m, n)$ — needed for fiber-count results.

These higher-order statistics are exactly what the [[../research/R7-k-regular-asymptotics|Heuberger–Krenn]] machinery delivers for general 2-regular sequences. Applying it to $\Phi_0$ would be a natural follow-up.

## The eigenvalue $5 + \sqrt{17}$

Where does this come from? The matrix
$$M = \begin{pmatrix}5 & -2 \\ 1 & 0\end{pmatrix}$$
has characteristic polynomial $\lambda^2 - 5\lambda + 2$. Discriminant: $25 - 8 = 17$. Field: $\mathbb{Q}(\sqrt{17})$.

**Curious**: $\sqrt{17}$ shows up. Is there a structural reason involving the *real* quadratic field $\mathbb{Q}(\sqrt{17})$ in the asymptotics of a problem fundamentally about $\mathbb{Q}(i)$? Possible: $17 = 4^2 + 1$ is itself a value of $\phi_0$. The first **non-trivial** prime of the form $n^2+1$ is $17 = 4^2+1$ — and it appears as a discriminant in the asymptotic spectrum of the tree it generates. Suggestive of a self-referential structure.

This deserves more thought — see [[../bridges/B6-open-questions]].
