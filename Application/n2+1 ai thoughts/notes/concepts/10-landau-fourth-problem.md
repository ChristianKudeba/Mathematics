# Landau's 4th problem

## Statement

> There are infinitely many primes of the form $p = n^2 + 1$.

Posed by Edmund Landau at the 1912 ICM (Cambridge) as one of four "unattackable" problems. The other three:
- **Goldbach** (every even $n \ge 4$ is a sum of two primes)
- **Twin primes** (∞ many $p$ with $p+2$ prime)
- **Legendre** (always a prime between $n^2$ and $(n+1)^2$)

Landau's 4th is the **only one** of the four that is purely about primes in a specific *polynomial* sequence — and it is the prototypical case of [[11-bunyakovsky-conjecture|Bunyakovsky]] in degree 2.

## What's known

| year | result | who |
|---|---|---|
| ~1900 | $n^2+1$ has ∞ many *square-free* values | classical |
| 1922 | Hardy–Littlewood conjecture: $\pi_{n^2+1}(N) \sim C \cdot \sqrt{N}/\log N$ with explicit $C$ | Hardy–Littlewood |
| 1978 | $n^2+1 = P_2$ (product of ≤ 2 primes) infinitely often | [[../research/R1-iwaniec-and-sieves|Iwaniec]], half-dim sieve |
| 1998 | $a^2 + b^4$ prime infinitely often (analogous result for a thinner set) | [[../research/R3-friedlander-iwaniec|Friedlander–Iwaniec]] |
| 2012 | $a^2 + p^4$ prime ($p$ prime), via $L$-functions of GL₂ | Heath-Brown, Li |

The barrier between $P_2$ and $P_1$ is the [[../research/R2-parity-problem|parity problem]] of sieve theory. **Landau's 4th remains open.**

## Heuristic count

Hardy–Littlewood predicts:
$$\#\{n \le N : n^2+1 \text{ prime}\} \sim C \cdot \frac{\sqrt N}{\log N},\qquad C = \prod_{p\ \text{odd}} \left(1 - \frac{(-1/p)}{p-1}\right) \approx 1.3727\ldots$$

The set has density $\sim 1/(2\sqrt N \log N)$ — **thin** even compared to twin primes. This thinness is what makes sieve methods struggle.

## The Shakov reformulation

The crucial Remark labelled `landauremark` in §4 of the paper:

> $n^2 + 1$ is **prime** $\iff n$ does not appear as the second component of any pair on the **interior** of the [[14-S-sequence|$\Phi_0$ tree]] $\iff \mathcal{S}^{-1}(n) = \{2^n,\ 2^{n+1}-1\}$.

So Landau's 4th becomes:

> Show that infinitely many $n \in \mathbb{N}$ satisfy $|\mathcal{S}^{-1}(n)| = 2$, where $\mathcal{S}$ is the 2-regular sequence defined by the recursion in [[14-S-sequence]].

This is a statement *about a 2-regular sequence*. There is now a theory ([[../research/R7-k-regular-asymptotics|Heuberger–Krenn]]) for asymptotics of 2-regular sequences. The route forward: see [[../bridges/B4-S-sequence-density]].

## Equivalent matrix-counting form ([[13-prime-characterization|Corollary]])

$n^2+1$ is prime iff there is **no** $\begin{pmatrix}a&b\\c&d\end{pmatrix} \in SL_2(\mathbb{N})$ (interior — strictly positive entries) with $ac + bd = n$.

This is a **Diophantine non-existence statement**. Using duality:
$$\#\{A \in SL_2(\mathbb{N}_0): ac+bd=n\} = \tau(n^2+1).$$
So $n^2+1$ prime ⇔ $\tau(n^2+1) = 2$ ⇔ exactly the two boundary matrices ($S^n$ and $T^n$, giving cross-term $n$ in trivial way) realize the value.

Counting $\tau(n^2+1) = 2$ is equivalent to counting **representations of $n^2+1$ as $X^2+Y^2$** by exactly the trivial way. This connects directly to the classical theory of [[../research/R4-binary-quadratic-forms|Gaussian primes]].

## Status

Open. Best toward: Iwaniec ($P_2$). The Shakov framework offers a genuinely new angle: instead of sieving, count via the recursive sequence and apply automatic-sequence asymptotics.
