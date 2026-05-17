# Bunyakovsky's conjecture

## Statement

Let $f \in \mathbb{Z}[x]$ satisfy:

1. $f$ is **irreducible** in $\mathbb{Z}[x]$,
2. $f$ has **positive leading coefficient**,
3. $\gcd\big(f(0), f(1), f(2), \ldots\big) = 1$ (no fixed prime divisor).

Then there are **infinitely many primes of the form** $p = f(n)$.

## Position in the field

- The degree-1 case is **Dirichlet's theorem** on primes in arithmetic progressions (proved 1837).
- The degree-2 case is **completely open**. The four enumerable polynomials of [[07-classification-theorem|Shakov's classification]] are all degree-2 instances.
- The degree-≥ 3 case is even more wildly out of reach.
- Multivariate generalization: **Schinzel's hypothesis H** for finite collections, and **Bateman–Horn conjecture** for asymptotic counts.

## Heuristic count (Bateman–Horn)

For $f$ satisfying Bunyakovsky's conditions:
$$\#\{n \le N : f(n) \text{ prime}\} \sim \frac{1}{\deg f} \cdot \frac{C(f)}{\log N} \cdot N$$
where
$$C(f) = \prod_p \frac{1 - \omega_f(p)/p}{1 - 1/p}$$
and $\omega_f(p)$ is the number of solutions to $f(n) \equiv 0 \pmod p$.

For $f = n^2+1$: $C(f) \approx 1.3727$, density $\sim N^{1/2}/\log N$ — see [[10-landau-fourth-problem]].

## Where the four enumerable polynomials sit

All of $\phi_0, \phi_1, \psi_2, \phi_3$ satisfy Bunyakovsky's conditions:
- $\phi_0 = n^2+1$: $\gcd = 1$ trivially. Bateman–Horn: $C \approx 1.37$.
- $\phi_1 = n^2+n+1$: $\gcd = 1$. $C \approx 2.25$.
- $\psi_2 = n^2+2n-1$: $\gcd = 1$. $C \approx 1.51$.
- $\phi_3 = n^2+3n+1$: $\gcd = 1$. $C \approx 1.66$.

So all four are conjectured to take ∞ many prime values, with **comparable densities**.

## Why this matters for Shakov

The "factorization highway" remark in the paper says: each matrix $A \in SL_2(\mathbb{N}_0)$ encodes a divisor pair simultaneously in all four $\mathcal{D}_f$. So:

> Any density theorem about absences-from-interior in *one* tree gives partial information about the others.

If we could prove Bunyakovsky for *one* of the four via the SL₂(ℕ₀) framework, we may get all four together. Conversely: lower-bounding the joint density of $n$ such that all four of $\phi_0(n), \phi_1(n), \psi_2(n), \phi_3(n)$ are simultaneously prime would be a "quadruple-prime constellation" result, also wildly open.

## Connection to other open problems

- **Twin primes** = Schinzel's H for the pair $\{n, n+2\}$.
- **Goldbach** is a different beast (additive, not value-of-polynomial).
- **Sophie Germain primes** = Schinzel's H for $\{n, 2n+1\}$.
- **Cunningham chains**, etc., are all instances of Schinzel's H.

Bunyakovsky is the **single-polynomial** case. Even this is unsolved in any nontrivial degree.
