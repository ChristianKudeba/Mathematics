# Boundary vs. interior — the central dichotomy

## On the matrix side

[[01-sl2-n0-monoid|$SL_2(\mathbb{N}_0)$]] decomposes:
- **Boundary**: matrices with at least one zero entry. These are exactly the powers $S^\alpha$ and $T^\alpha$ (and $I$). Sit on the two "spines" of the binary tree.
- **Interior**: matrices with all four entries strictly positive = the **semigroup** $SL_2(\mathbb{N})$.

Equivalently: a matrix is in the interior iff its $S/T$-word contains *both* an $S$ and a $T$.

## On the divisor-pair side (under $\hat F_f$)

[[03-divisor-pair-set|$\mathcal{D}_f$]] decomposes:
- **Boundary pairs**: $(1, n)$ and $(|f(n)|, n)$ — **trivial divisors**.
- **Interior pairs**: $(m, n)$ with $1 < m < |f(n)|$ — **nontrivial divisors**.

Under $\hat F_f$, the matrix boundary maps onto the pair boundary and the matrix interior onto the pair interior. So:

$$f(n)\ \text{prime} \iff\ \text{the only pairs above } n \text{ are }(1,n) \text{ and }(|f(n)|, n) \iff\ n\ \text{appears only on the boundary of the tree.}$$

## Why this is the right reformulation

The classical question "is $f(n)$ prime?" gets translated into a **purely combinatorial** question about positions in a 2-regular sequence:

> Does $n$ appear in a non-spine position of the $\hat F_f$ tree?

Equivalently:

> Does $n$ have a representation $n = (\text{cross-term})(A)$ with $A \in SL_2(\mathbb{N})$ (interior)?

For $\hat F_{\phi_0} = \Phi_0$ this is: does $n = ac+bd$ with $A = \begin{pmatrix}a&b\\c&d\end{pmatrix} \in SL_2(\mathbb{N})$?

## Two distinct counting problems

The reformulation gives us **two complementary** counting problems:

| count | what it computes | for $\phi_0$ |
|---|---|---|
| **All matrices with cross-term $=n$** | $\tau(\|f(n)\|)$ | $\tau(n^2+1)$ |
| **Interior matrices with cross-term $=n$** | $\tau(\|f(n)\|) - 2$ | $\tau(n^2+1) - 2$ |

**$f(n)$ is prime iff the second count is zero.**

## Strategic implication

Two routes to Landau's 4th:

**Route A — Lower-bound the boundary fraction.** Show that for ∞ many $n$, the *fraction* of matrices with cross-term $n$ that are interior is exactly 0. This is the direct combinatorial route.

**Route B — Upper-bound interior representation count.** Show that for ∞ many $n$, the number of interior matrices with cross-term $n$ is 0. By inclusion–exclusion this is essentially the same, but framed for sieve-style arguments.

The interior of $SL_2(\mathbb{N}_0)$ is a **thin semigroup** in the sense of the [[../research/R5-thin-groups-affine-sieve|affine sieve]] / Bourgain–Gamburd–Sarnak. Counting orbit elements satisfying a polynomial condition (cross-term $= n$) is exactly the kind of problem the affine sieve was designed for.

See [[../bridges/B5-affine-sieve-attack]] for the program.
