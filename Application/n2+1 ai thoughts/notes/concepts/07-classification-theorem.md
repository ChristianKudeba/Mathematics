# Classification theorem (Theorem `main`)

## Statement

Let $f \in \mathbb{Z}[x]$ have positive leading coefficient. Then $f$ is [[06-enumerable-polynomial|enumerable]] iff
$$f \in \{\phi_0,\ \phi_1,\ \psi_2,\ \phi_3\} = \{n^2+1,\ n^2+n+1,\ n^2+2n-1,\ n^2+3n+1\}.$$

In each case the explicit invertible map is the corresponding $\Phi_\beta$ or $\Psi_\beta$ from the families defined in [[04-equivariant-map]]:
- $\hat F_{\phi_0} = \Phi_0$
- $\hat F_{\phi_1} = \Phi_1$
- $\hat F_{\psi_2} = \Psi_2$
- $\hat F_{\phi_3} = \Phi_3$

## Proof structure

Three lemmas:
1. **Degree ≥ 2**: degree 0 forces $f \equiv \pm 1$, fails injectivity at $S, T$. Degree 1 fails the [[06-enumerable-polynomial|size criterion]].
2. **Among monic degree-2**: only the four candidates survive (each other choice exhibits a $(m,n)$ violating $\min\le n < \max$).
3. **[[09-carl-schildkraut-lemma|Schildkraut]]**: degree ≥ 3, or leading coefficient ≥ 2 in degree 2, produces a factorization $f(n_0) = (n_0+a)(n_0+b)$ with $a,b \ge 1$, violating size on the *low* side.

Then check each of the four works using the inequalities $|f(n)| < (n+1)^2$ except at boundary, etc.

## What's secretly being proved

The classification is really saying:

> The polynomials whose values' divisor structure is "as efficiently enumerable as possible" are exactly the **norm forms of the four real or imaginary quadratic orders with smallest absolute discriminant**: $-4, -3, 5, 8$.

These are precisely the orders for which:
- ideal class group is trivial
- Gauss reduction gives a *single* reduced binary quadratic form of each discriminant up to equivalence
- the [[16-calkin-wilf-tree|continued-fraction]] enumeration of SL₂(ℤ)-orbits on lattices works "without remainder"

See [[../bridges/B2-discriminant-coincidence|the discriminant coincidence]] for why this is structurally inevitable, and [[../research/R4-binary-quadratic-forms|binary quadratic forms]] for the necessary background.

## Strategic value

The classification pins down four very specific polynomials in which divisor structure is rigid. **All four are conjectured to take prime values infinitely often** ([[11-bunyakovsky-conjecture|Bunyakovsky]]), and all four conjectures are open. Any progress on one — via the SL₂(ℕ₀) framework — would automatically give partial information about the other three through the "highway" coupling (each matrix encodes a divisor fact in all four sets simultaneously). See [[../bridges/B1-synthesis|synthesis]].
