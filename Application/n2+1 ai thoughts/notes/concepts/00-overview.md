# Overview — One-screen summary

Shakov classifies the polynomials $f \in \mathbb{Z}[x]$ for which the divisor structure
$$\mathcal{D}_f = \{(m,n) \in \mathbb{N}_0^2 : m \mid f(n)\}$$
is *enumerated* by the free monoid [[01-sl2-n0-monoid|$SL_2(\mathbb{N}_0)$]] — meaning there is a bijection
$$\hat F_f : SL_2(\mathbb{N}_0) \xrightarrow{\sim} \mathcal{D}_f$$
that intertwines left-multiplication by the generators $S,T$ with explicit pair operations $\bar S, \bar T_f$ on $\mathcal{D}_f$ ([[04-equivariant-map]]).

## The one theorem

[[07-classification-theorem|**Theorem.**]] $f$ is enumerable (and has positive leading coefficient) iff $f \in \{\phi_0, \phi_1, \psi_2, \phi_3\}$, where:

| polynomial | formula | discriminant | quadratic field |
|---|---|---|---|
| $\phi_0$ | $n^2+1$ | $-4$ | $\mathbb{Q}(i)$ |
| $\phi_1$ | $n^2+n+1$ | $-3$ | $\mathbb{Q}(\zeta_3)$ |
| $\psi_2$ | $n^2+2n-1$ | $8$ | $\mathbb{Q}(\sqrt 2)$ |
| $\phi_3$ | $n^2+3n+1$ | $5$ | $\mathbb{Q}(\sqrt 5)$ |

These are exactly the four quadratic orders with the smallest absolute discriminant — see [[../bridges/B2-discriminant-coincidence|the discriminant coincidence]]. **This is not a coincidence.** The Diophantus-style multiplicative identity is the *form composition* of [[../research/R4-binary-quadratic-forms|binary quadratic forms]]; enumerability picks out the fields where reduction is unique enough to embed into the free monoid.

## Where Landau hides

[[10-landau-fourth-problem|Landau's 4th problem]] (∞ many primes $p = n^2+1$) is *equivalent* (Remark labelled `landauremark` in §4) to the statement:

> Infinitely many $n \in \mathbb{N}$ never appear as a second component of any pair on the **interior** of the $\Phi_0$ divisor tree.

The interior of the SL₂(ℕ₀) tree is the strict semigroup $SL_2(\mathbb{N})$ (all four entries ≥ 1). Equivalently:

> There is no matrix $\begin{pmatrix}a&b\\c&d\end{pmatrix} \in SL_2(\mathbb{N})$ with $ac+bd = n$.

So Landau's 4th becomes a **counting problem on a thin subset of the integers**: count $n$ such that the Diophantine system $(ad-bc=1,\ ac+bd=n)$ has no solution in strictly positive integers.

See [[12-boundary-vs-interior]] and [[13-prime-characterization]].

## The S-sequence

The second components of the Φ₀ tree, read row-by-row, give an integer sequence $\mathcal{S}$ ([[14-S-sequence]]) with:

1. $|\mathcal{S}^{-1}(n)| = \tau(n^2+1)$
2. $n^2+1$ prime $\iff \mathcal{S}^{-1}(n) = \{2^n, 2^{n+1}-1\}$ (only the two boundary indices)
3. $\mathcal{S}$ is **2-regular** ([[15-k-regular-sequences]]) in the sense of Allouche–Shallit

Property 3 is the crucial one: 2-regular sequences have a developed [[../research/R7-k-regular-asymptotics|asymptotic theory]] (Heuberger–Krenn). If we can prove a *density* theorem — that the fiber sizes $|\mathcal{S}^{-1}(n)|$ hit the value 2 infinitely often — Landau's 4th falls.

## The "factorization highway" remark

Each matrix $A \in SL_2(\mathbb{N}_0)$ generates **four** divisor facts at once — one in each of $\mathcal{D}_{\phi_0}, \mathcal{D}_{\phi_1}, \mathcal{D}_{\psi_2}, \mathcal{D}_{\phi_3}$. So information about the divisor structure of $n^2+1$ is *coupled* to the divisor structure of $n^2+n+1$, $n^2+2n-1$, $n^2+3n+1$. Any density progress for one transports to the others. See [[../bridges/B1-synthesis]] §3.
