# The complement involution $c$

## Two parallel involutions

On matrices:
$$c\begin{pmatrix}a&b\\c&d\end{pmatrix} = \begin{pmatrix}d&c\\b&a\end{pmatrix}$$
Equivalently $c(A) = JAJ$ with $J = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ (which has det $-1$).

On pairs (depends on $f$):
$$\bar c_f(m, n) = (|f(n)|/m,\ n)$$
Sends a divisor of $f(n)$ to its **complementary divisor**.

## Compatibility

$c$ and $\bar c_f$ are intertwined by every equivariant map: $\hat F_f \circ c = \bar c_f \circ \hat F_f$.

## Properties

- **Involution**: $c^2 = \mathrm{id}$, $\bar c_f^2 = \mathrm{id}$.
- **Anti-symmetric on generators**: $c(S) = T$, $c(T) = S$. So conjugation by $J$ swaps the two generators of [[01-sl2-n0-monoid|SL₂(ℕ₀)]].
- **Reflection**: $c$ reflects the binary tree across the central axis.
- **On words**: $c(S^{\alpha_k} T^{\alpha_{k-1}} \cdots S^{\alpha_0}) = T^{\alpha_k} S^{\alpha_{k-1}} \cdots T^{\alpha_0}$ (Prop `refl`).
- **Used to derive $\bar T_f$**: $\bar T_f = \bar c_f \circ \bar S \circ \bar c_f$ (Prop `depmatrix` / definition).

## Why this matters

The complement gives you $\bar T_f$ for free from $\bar S$ and $\bar c_f$. So you only need to verify equivariance with respect to $\bar S$ and $\bar c_f$ — the $\bar T_f$ equivariance follows. This is the key technical convenience throughout §2–3 of the paper.

## Conceptual content

In the language of [[../research/R4-binary-quadratic-forms|binary quadratic forms]], the involution $c$ on matrices is the **Gauss "opposite" form**: the form $ax^2 + bxy + cy^2$ has opposite $cx^2 + bxy + ay^2$, and these represent the same primes (the form class group has $[Q]^{-1} = [\bar Q]$). The complement on divisor pairs is the **factor-pair flip** $d \leftrightarrow N/d$.

Both are order-2 symmetries that quotient down to a meaningful counting object: **classes** of forms / **factor pairs** instead of divisors. The paper exploits this symmetry pervasively.
