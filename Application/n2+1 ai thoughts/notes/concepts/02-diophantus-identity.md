# Diophantus' identity (and its β-deformations)

## Classical form

$$(a^2 + b^2)(c^2 + d^2) = (ac+bd)^2 + (ad-bc)^2$$

Holds in any commutative ring. Means: **sums of two squares are closed under multiplication**. This is the prototype of all the multiplicative-norm identities — Brahmagupta, Lagrange, Euler four-square, Cayley/octonions, [[../research/R4-binary-quadratic-forms|Gauss composition of binary quadratic forms]].

## With determinant constraint

If $\begin{pmatrix}a&b\\c&d\end{pmatrix} \in [[01-sl2-n0-monoid|SL_2(\mathbb{N}_0)]]$ then $ad-bc = 1$, so:
$$(ac+bd)^2 + 1 = (a^2+b^2)(c^2+d^2)$$

This is **a factorization of $n^2+1$** with $n = ac+bd$. Each factor is itself a sum of two squares.

This single identity is the entire motivation for the paper: it sets up the map $\Phi_0(A) := (a^2+b^2,\ ac+bd) \in \mathcal{D}_{\phi_0}$.

## Three β-generalizations

For $\beta \in \mathbb{Z}$:

$$(a^2 + \beta ab + b^2)(c^2 + \beta cd + d^2) = (ac + \beta bc + bd)^2 + \beta(ac+\beta bc+bd)(ad-bc) + (ad-bc)^2$$

$$(a^2 + \beta ab - b^2)(c^2 + \beta cd - d^2) = (ac + \beta bc - bd)^2 + \beta(ac+\beta bc-bd)(ad-bc) - (ad-bc)^2$$

Setting $ad-bc = 1$ collapses the right side to $\phi_\beta(n) := n^2 + \beta n + 1$ or $\psi_\beta(n) := n^2 + \beta n - 1$ respectively, with $n$ the cross-term.

## Where this lives in algebra

These are exactly the **norm forms** for the order $\mathbb{Z}[\omega] \subset \mathbb{Q}(\omega)$ where $\omega$ satisfies $\omega^2 + \beta\omega \pm 1 = 0$:

- $\phi_0$: $\omega = i$, norm $a^2+b^2$, ring $\mathbb{Z}[i]$ (Gaussian)
- $\phi_1$: $\omega = \zeta_3$, norm $a^2+ab+b^2$, ring $\mathbb{Z}[\zeta_3]$ (Eisenstein)
- $\psi_2$: $\omega = 1+\sqrt 2$, norm $a^2+2ab-b^2$, ring $\mathbb{Z}[\sqrt 2]$
- $\phi_3$: $\omega = \frac{3+\sqrt 5}{2}$, norm $a^2+3ab+b^2$, ring $\mathbb{Z}[\frac{1+\sqrt 5}{2}]$

The β-identities are exactly **multiplicativity of the norm**: $N(\alpha)N(\beta) = N(\alpha\beta)$ in these rings. See [[../bridges/B2-discriminant-coincidence]].

## What's special about SL₂(ℕ₀) here

The constraint $ad-bc=1$ with all entries in ℕ₀ is what:
1. Makes the cross-term $ac+\beta bc + bd$ a nonneg integer (so we have a divisor pair).
2. Forces uniqueness of factorization (free monoid → unique decomposition).
3. Cuts down the eligible polynomials to just **four** — see [[07-classification-theorem]].
