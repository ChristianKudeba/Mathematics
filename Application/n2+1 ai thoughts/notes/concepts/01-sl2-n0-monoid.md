# SL₂(ℕ₀) — the free monoid

## Definition

$SL_2(\mathbb{N}_0) := \{A \in M_2(\mathbb{Z}) : \det A = 1,\ \text{all entries} \ge 0\}$.

This is a **monoid** under matrix multiplication (closed, has identity $I$), but *not* a group — most matrices have no nonneg inverse.

## Free generation

It is a free monoid on the two generators
$$S = \begin{pmatrix}1 & 0 \\ 1 & 1\end{pmatrix},\qquad T = \begin{pmatrix}1 & 1 \\ 0 & 1\end{pmatrix}$$
(Nathanson 2014, Cor. 1). Powers:
$$S^\alpha = \begin{pmatrix}1 & 0 \\ \alpha & 1\end{pmatrix},\quad T^\alpha = \begin{pmatrix}1 & \alpha \\ 0 & 1\end{pmatrix}.$$

So **every element has a unique factorization** as $S^{\alpha_k} T^{\alpha_{k-1}} \cdots S^{\alpha_0}$ (or starting with $T$). This unique-factorization property is the engine of the entire paper — it is what makes the equivariant maps $\hat F_f$ well-defined and invertible.

## The binary tree

Multiplying by $S$ on the left = "left child", by $T$ on the left = "right child", root = $I$.

```
                        I
              /                  \
             S                    T
          /    \                /    \
        S²      TS            ST      T²
        ...
```

## Interior vs boundary

[[12-boundary-vs-interior|Crucial dichotomy]]:
- **Boundary** of the tree = matrices that are pure powers $S^\alpha$ or $T^\alpha$. Equivalently, matrices in $SL_2(\mathbb{N}_0)$ with at least one zero entry. These correspond to *trivial factorizations* on the pair side.
- **Interior** = matrices with all entries strictly positive = the semigroup $SL_2(\mathbb{N})$. These correspond to *nontrivial factorizations* of $f(n)$.

## Connection to SL₂(ℤ)

$SL_2(\mathbb{N}_0)$ is *not* a subgroup of $SL_2(\mathbb{Z})$ (it's not closed under inverse), but it generates $SL_2(\mathbb{Z})$ (together with the involution $A \mapsto A^{-T}$ or sign changes). In particular:
- Words in $S, T$ are exactly **continued fraction matrices**: $S^{\alpha_k} \cdots T^{\alpha_0}$ corresponds to the continued fraction $[\alpha_0; \alpha_1, \ldots, \alpha_k]$.
- Compare with the [[16-calkin-wilf-tree|Calkin–Wilf tree]], which uses the same generators acting on rational pairs.
- Compare with [[../research/R5-thin-groups-affine-sieve|thin subgroup]] / [[../research/R6-zaremba-apollonian|Zaremba]] machinery, where SL₂(ℕ) semigroup orbits are studied via spectral gap.

## Why this is the right object

Two reasons the paper uses SL₂(ℕ₀) and not SL₂(ℤ):
1. **Free** monoid → unique encoding of every divisor pair.
2. The Diophantus identity ([[02-diophantus-identity]]) requires $ad-bc = 1$ *with the right sign* and produces $n^2+1$ rather than $n^2-1$ exactly when we are in the determinant-1, nonnegative regime.

## Key properties used in the paper

- Free monoid of rank 2 → every matrix has a unique S/T-word.
- The complement involution $c(A) = JAJ$ where $J = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ swaps $S \leftrightarrow T$. See [[05-complement-involution]].
- Boundary = $\{I, S, S^2, \ldots\} \cup \{T, T^2, \ldots\}$ = matrices with a zero entry.
