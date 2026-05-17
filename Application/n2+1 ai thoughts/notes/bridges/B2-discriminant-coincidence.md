# The discriminant coincidence

## The observation

The four [[../concepts/07-classification-theorem|enumerable polynomials]] have discriminants:

| polynomial | $\mathrm{disc}$ | quadratic field | class number $h$ | unit group |
|---|---|---|---|---|
| $\phi_0 = n^2+1$ | $-4$ | $\mathbb{Q}(i)$ | 1 | $\{\pm 1, \pm i\}$ |
| $\phi_1 = n^2+n+1$ | $-3$ | $\mathbb{Q}(\zeta_3)$ | 1 | $\{\pm 1, \pm \zeta_3, \pm \zeta_3^2\}$ |
| $\psi_2 = n^2+2n-1$ | $8$ | $\mathbb{Q}(\sqrt 2)$ | 1 | $\{\pm (1+\sqrt 2)^k\}$ |
| $\phi_3 = n^2+3n+1$ | $5$ | $\mathbb{Q}(\sqrt 5)$ | 1 | $\{\pm \phi^k\}$ ($\phi$ = golden) |

These are the **four smallest absolute discriminants of any quadratic field**. (The next would be $\mathrm{disc} = -7$ from $n^2+n+2$, then $-8$ from $n^2+2$, then $12$ from $n^2-3$, etc.)

All four have **class number 1**. The next class-number-1 discriminant is $-7$, but $\phi(0) = 2 \ne 1$ for $f = n^2+n+2$, so it fails Shakov's necessary condition $|f(0)| = 1$.

## Hypothesis

> **Enumerability** $\iff$ **class number 1** $+$ **$|\mathrm{disc}|$ small enough that SL₂(ℕ₀)-reduction reaches every reduced form**.

Specifically: $f$ is enumerable iff (i) $|f(0)| = 1$ (forces minimal-discriminant order), (ii) the form class group is trivial, and (iii) the principal form admits a *positive Markov-style* reduction tree.

## Why class number 1 is necessary

Each invertible equivariant map $\hat F_f$ encodes a **unique** factorization of every value $f(n)$ into a product $m \cdot (|f(n)|/m)$ via a unique matrix word. Inside the relevant ring $\mathcal{O}_K$:

- $f(n)$ corresponds to a norm $N(\alpha)$ for some $\alpha \in \mathcal{O}_K$.
- A divisor of $f(n)$ corresponds to a *factorization* $\alpha = \beta \gamma$ in $\mathcal{O}_K$ (up to units).
- For the count to match $\tau(|f(n)|)$, every ideal divisor must come from a *principal* ideal divisor — which is precisely class number 1.

If $h(K) > 1$, some ideal divisors of $\alpha$ are non-principal, so they don't correspond to a divisor of $f(n)$ in the integers — the count breaks.

## Why small discriminant is necessary

Even with class number 1, the [[../concepts/04-equivariant-map|equivariance]] requires $\hat F_f$ to send SL₂(ℕ₀) injectively into divisor pairs. Larger discriminants give *more* matrix elements with the same cross-term value (because $\sqrt{|d|}$ is bigger), and the equivariance map starts to overlap.

[[../concepts/09-carl-schildkraut-lemma|Schildkraut's lemma]] is essentially a way of saying: when growth $f(n) \gg n^2$, you find $f(n_0) = (n_0+a)(n_0+b)$ with both cofactors above $n_0$ — these are the "extra" SL₂(ℤ)-orbits that wouldn't arise from a single principal ideal in a small-disc field.

## Predictions from the hypothesis

If correct, the hypothesis predicts:

1. **No enumerable polynomial of degree > 2 exists.** ✓ (Schildkraut's lemma, proved in the paper.)

2. **Higher-rank generalizations**: there should be enumerable forms of *more variables* whose value sets are enumerated by SL₃(ℕ₀) or higher monoids, classified by SL₃ Bhargava cubes / class numbers.

3. **Number-field analogue**: replace ℤ by $\mathcal{O}_K$, look at polynomials in $\mathcal{O}_K[x]$ whose divisor pairs are enumerated by $SL_2(\mathcal{O}_K^+)$ where $\mathcal{O}_K^+$ is some "positive cone." The four enumerable polynomials should correspond to the *quartet of smallest-disc quadratic extensions of $K$ with class number 1.*

4. **No enumerable polynomial corresponds to $\mathbb{Q}(\sqrt{-7})$**: indeed $f = n^2+n+2$ has $|f(0)|=2$.

## What this gives us strategically

If enumerability is *fundamentally* a class-field-theoretic property, then:

- The Shakov framework is implicitly using **Hecke characters** of the four small quadratic orders. A direct translation between $\mathcal{D}_f$ and $\mathrm{Cl}(\mathcal{O}_K)$-equivariant data should exist.
- **Hecke L-functions of these characters** govern the prime-counting in $\mathcal{D}_f$.
- **L-function methods for $\mathbb{Q}(i)$** (Iwaniec, etc.) should be re-expressible in Shakov's language.

This is the bridge that needs to be built. See [[B5-affine-sieve-attack]] and [[B1-synthesis]].

## What's NEW from Shakov

Even though enumerability boils down to class-field-theoretic properties of the four small orders, the *combinatorial reformulation* — Landau's 4th as fiber-cardinality of a 2-regular sequence — is **new**. It opens a route via [[../research/R7-k-regular-asymptotics|Heuberger–Krenn]] / [[../research/R8-automatic-sequences-and-primes|Mauduit–Rivat]] machinery that has *never before* been brought to bear on Landau's 4th.

The key novelty:
> Landau's 4th = fiber-size estimate for a specific 2-regular sequence with degenerate (triple eigenvalue 1) spectral data.

This is *not* a sieve question. It's an automatic-sequence prime-distribution question.
