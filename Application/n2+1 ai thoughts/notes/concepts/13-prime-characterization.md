# Prime characterizations via $SL_2(\mathbb{N})$

## The four corollaries (from §3 of the paper)

For $A = \begin{pmatrix}a&b\\c&d\end{pmatrix} \in SL_2(\mathbb{N})$ (strict interior):

| polynomial | $f(n)$ is prime $\iff$ no $A \in SL_2(\mathbb{N})$ with: |
|---|---|
| $\phi_0(n) = n^2 + 1$ | $ac + bd = n$ |
| $\phi_1(n) = n^2 + n + 1$ | $ac + bc + bd = n$ |
| $\psi_2(n) = n^2 + 2n - 1$ | $\max\{ac, bd\} + 2bc - \min\{ac, bd\} = n$ |
| $\phi_3(n) = n^2 + 3n + 1$ | $ac + 3bc + bd = n$ |

Each of these is a Diophantine system: one equation $ad - bc = 1$ + one linear-in-products equation = $n$.

## What kind of statement is this?

Restated: each prime characterization is

> $f(n)$ is prime $\iff$ a particular **system of two polynomial equations in 4 nonneg-integer unknowns has no positive solution**.

The system has degree 2 (one quadratic — $ad-bc=1$ — and one quadratic-in-products), and 4 variables. Solutions live on a *4-dimensional affine variety* (det surface) intersected with a *3-dimensional hypersurface* (cross-term condition). The intersection is generically a *curve*.

## Geometric content

The det surface $\{ad - bc = 1\}$ is a smooth affine quadric in $\mathbb{A}^4$. The cross-term condition cuts it with another quadric. The result is a (possibly reducible) curve $C_n \subset \mathbb{A}^4$. The question becomes:

> Does $C_n$ have any **strictly positive integer points**?

For $\phi_0$: $C_n = \{ad - bc = 1, ac + bd = n\}$, a degree-4 surface (intersection of two quadrics) — actually a curve in $\mathbb{A}^4$. By eliminating: parameterize by $(a, b)$, then $c, d$ are forced (if they exist) to be $c = (an - b)/(a^2+b^2)$, $d = (bn + a)/(a^2+b^2)$, requiring $(a^2+b^2) \mid (an-b)$ and $(a^2+b^2) \mid (bn+a)$.

So integer points on $C_n$ correspond to **Gaussian integer factorizations** of $n + i$:

$$n + i = (a + bi)(d - ci) \quad\text{in } \mathbb{Z}[i]$$

That is, $\Phi_0$ is **literally the Gaussian integer factorization map**, in disguise. See [[../research/R4-binary-quadratic-forms]] for the deep content.

## Implication: $n^2+1$ prime $\iff$ $n+i$ is a Gaussian prime

This is a classical fact! It's simply restating that an element of norm $n^2+1$ is prime iff it has only the trivial unit-factorization. The Shakov reformulation makes this **explicit** at the level of free monoid words.

## Where this leads — the prime-counting function

Let $\pi_{n^2+1}(N) = \#\{n \le N : n^2+1\ \text{prime}\}$. Then:
$$\pi_{n^2+1}(N) = N - \#\{n \le N : \exists A \in SL_2(\mathbb{N})\ \text{with}\ ac+bd = n\}.$$

So the question is: how does $\#\{n \le N : n \in \mathrm{cross}_2(SL_2(\mathbb{N}))\}$ grow? Almost all $n$ are in this set (since $\tau(n^2+1) > 2$ for most $n$). The question is the *complement*.

## Connection to [[../research/R5-thin-groups-affine-sieve|affine sieve]]

The set
$$\mathcal{O}_{\mathrm{int}} := \{ac + bd : A \in SL_2(\mathbb{N})\}$$
is a "thin orbit count" in the sense of Bourgain–Kontorovich. The complement $\mathbb{N} \setminus \mathcal{O}_{\mathrm{int}}$ is exactly the indices of $\phi_0$-primes. This recasts Landau's 4th as a **density question for a thin set defined by a semigroup** — exactly the regime where Bourgain–Gamburd–Sarnak and Bourgain–Kontorovich made breakthrough progress.

See [[../bridges/B5-affine-sieve-attack]].
