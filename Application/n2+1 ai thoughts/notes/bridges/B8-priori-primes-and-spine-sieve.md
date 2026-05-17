# A-priori primes from the lemma + the spine-sieve direction

This note investigates: how far can we push the paper's `f(1), f(2) prime` lemma, and can conventional tools squeeze a non-trivial lower bound on primes among f(1), f(2), …, f(N)?

## The lemma's true strength

The paper proves: for f enumerable, |f(1)|, |f(2)|, |f(|f(1)|)| are all prime ([[../concepts/06-enumerable-polynomial|Lemma `f(1), f(2) prime`]]). But the proof mechanism — **the smallest interior second-coord is 1+|f(1)|** — actually gives:

**Generalized Lemma.** For f enumerable and every n ∈ [1, |f(1)|], |f(n)| is prime.

### Why the proof gives this

The argument (paper's proof of `f(1), f(2) prime`):
- The boundary spines of the F̂_f tree consist of (1, n) [left] and (|f(n)|, n) [right]. These are trivial divisor pairs.
- The first interior pair appears at row 2: it is $\bar S \bar T_f (1,0)$ or $\bar T_f \bar S (1,0)$, both of which have second coord = 1+|f(1)|. (For φ_0: the pair (5,3) and (2,3) at n = 3 = 1+|f(1)|.)
- Equivalently: the minimum cross-term value over $A \in SL_2(\mathbb{N})$ for the polynomial f equals 1+|f(1)|. (Direct check from the explicit formula and a,b,c,d ≥ 1 with ad-bc=1.)

Therefore: any n ∈ [1, |f(1)|] has no interior pre-image under $\hat F_f$, so |f(n)| has only trivial factorizations, so |f(n)| is prime.

### The four cases tabulated

| f | \|f(1)\| | a-priori primes | values |
|---|---|---|---|
| φ_0 = n²+1 | 2 | f(1), f(2) | 2, 5 |
| φ_1 = n²+n+1 | 3 | f(1), f(2), f(3) | 3, 7, 13 |
| ψ_2 = n²+2n-1 | 2 | f(1), f(2) | 2, 7 |
| **φ_3 = n²+3n+1** | **5** | f(1), …, f(5) | **5, 11, 19, 29, 41** |

The φ_3 case is striking — five consecutive prime values for free.

### Tightness

At n = 1+|f(1)|, the Generalized Lemma fails because the interior is non-empty. Direct check:
- φ_0: f(3) = 10 = 2·5 (interior pairs (5,3), (2,3)). ✓
- φ_1: f(4) = 21 = 3·7 (interior pairs (3,4), (7,4)). ✓
- ψ_2: f(3) = 14 = 2·7 (interior pairs). ✓
- φ_3: f(6) = 55 = 5·11 (interior pairs (11,6), (5,6)). ✓

So the bound n ≤ |f(1)| is exact.

## What about iterates f(f(n))?

The lemma gives f(|f(1)|) prime. Beyond that:

| f | f(f(1)) | f(f(2)) | f(f(3)) | f(f(4)) |
|---|---|---|---|---|
| φ_0 | f(2)=5 ✓ | f(5)=26=2·13 | f(10)=101 ✓ | f(17)=290=2·5·29 |
| φ_3 | f(5)=41 ✓ | f(11)=155=5·31 | f(19)=419 ✓ | f(29)=929 ✓ |

Sporadic. No theorem extending the iterate guarantee beyond f(f(1)) = f(|f(1)|).

The iterate question for polynomials is itself an unsolved area (e.g., conjectures about Mersenne-like primes p, 2p+1, 4p+3, …). Shakov's framework gives nothing structural here.

## Three difficulty layers

Anchoring the answer to the user's question:

**Layer A — trivial extension via the lemma.** Free. Gives |f(1)| primes.

**Layer B — modular / local obstructions.** For each f, there are residue classes mod small primes that force f(n) composite. E.g., φ_0(n) is even iff n is odd (so all odd n ≥ 3 give composite f(n)). Shakov's framework recovers these via *interior spines*:
- Leftmost interior spine of φ_0: $\bar S^k \bar T_f(1,0) = (2, 2k+1)$ for k ≥ 1. This pair has m=2 dividing f(2k+1) = (2k+1)²+1. So **every odd n ≥ 3 is composite, witnessed by divisor 2**.
- Other "spine words" give other AP exclusions.

**Layer C — density of f-primes in [1, N].** Open. Even the statement "count of f-primes in [1, N] → ∞ as N → ∞" is *equivalent to Landau's 4th* (the count is monotone). So:

> Any unconditional lower bound that grows with N implies Landau's 4th (or its analog for the relevant f).

Best known *unconditional* bounds:
- **Constant lower bound** (= |f(1)|) on primes among f(1), …, f(N).
- $\#\{n \le N : f(n) \in P_2\} \gg N/\log N$ — [[../research/R1-iwaniec-and-sieves|Iwaniec 1978]]. (Almost-primes, not primes.)
- $\#\{n \le N : P^+(f(n)) \ge n^{1.312}\} \gg N/\log N$ — Grimmelt–Merikoski 2025. (Composite f(n) with a large prime factor.)

Conditional under GRH / Elliott–Halberstam: nothing additional for f(n) of degree 2 (the density 1/√N is below the threshold of conditional sieve methods).

## The promising direction: spine-sieve reformulation

Each interior word $w \in \{\bar S, \bar T_f\}^*$ with at least one $\bar T_f$ produces, when applied to (1,0), a pair (m_w(k), n_w(k)) parameterized by some integer k (running over $\bar S^k$ in the rightmost factor of w, say). The second coord n_w(k) defines an arithmetic family of n-values, all guaranteed composite (witnessed by m_w(k) > 1 dividing f(n_w(k))).

**Examples for φ_0**:
- $w = \bar S^k \bar T_f$: family (2, 2k+1) → "every odd n" excluded with witness 2.
- $w = \bar S^k \bar T_f \bar S \bar T_f$: another arithmetic family with witness 5 (since $\bar T_f \bar S \bar T_f(1,0) = (5,3)$).
- $w = \bar S^k \bar T_f \bar S^2 \bar T_f$: family with witness 13 (since $\bar T_f \bar S^2 \bar T_f(1,0) = (13, 5)$).

In general, for each interior pair $(m_0, n_0)$ on row r, the spine $\bar S^k \cdot (\text{path to } (m_0, n_0))$ produces the family $(m_0, n_0 + k m_0)$ — n_0 + k·m_0 over k ≥ 0, with witness m_0.

So the interior of the φ_0 tree decomposes into **a countable union of APs**, each of the form $\{n_0 + k m_0 : k \ge 0\}$ for various (m_0, n_0), with each AP excluded from primality with witness m_0.

### Sundaram's sieve in disguise

This is structurally **Sundaram's sieve** (1934) for n²+1. Sundaram's classical observation: **n is the index of a sum-of-two-squares prime iff n is not of form 2(i+j+2ij)+1**. The Shakov interior gives the same kind of "AP-exclusion sieve" for n²+1 primality.

Sundaram's sieve has not yielded any improvement on Landau's 4th — the known sieve methods can produce $P_2$ via the same AP framework but cannot push to $P_1$ (parity problem).

**However**: Shakov's APs have *additional algebraic structure* not present in Sundaram. Specifically, each excluded AP has a **witness divisor** with a specific size and a specific congruence behavior dictated by the SL_2(ℕ_0) word. The (m_0, n_0) pair encodes a **Gaussian integer factorization** with explicit norms.

### Concrete sub-problem

Define the **spine-sieve indicator**:
$$\sigma(n) := \begin{cases} 0 & \text{if } n = n_w(k) \text{ for some interior word } w \text{ and some } k \\ 1 & \text{otherwise} \end{cases}$$

By the bijection F̂_{φ_0}: $\sigma(n) = 1 \iff n^2+1$ is prime.

The question: can we estimate $\sum_{n \le N} \sigma(n)$ via the algebraic structure of the interior words (i.e., via Gaussian integer L-functions, since each (m_0, n_0) is a Gaussian factorization)?

This is the "**spine-sieve attack**" — a refinement of [[B5-affine-sieve-attack|the affine-sieve attack]] that uses the SL_2(ℕ_0) word structure as the sifting parameter rather than congruence quotients. Whether it can succeed where Sundaram's sieve cannot is open. The hope is that the **bilinear cross-term** ([[B5-affine-sieve-attack#3-bilinear-cross-term-as-the-parity-breaking-lever|B5 §3]]) makes the sum tractable in a way the residue-class-based sieves can't access.

## Bottom line

Direct answers to the user's question:

1. **Yes, the lemma extends.** f(1), f(2), …, f(|f(1)|) are all prime — straightforward extension of the paper's proof. φ_3 gives 5 free primes.

2. **No further extension is possible.** At n = 1+|f(1)|, an explicit interior pair appears, breaking the "no interior" argument, and indeed f(1+|f(1)|) is composite for all four polynomials.

3. **Iterates f(f(n))** are sporadic. f(f(1)) is prime by the lemma; beyond that, no theorem.

4. **Lower bound on primes in [1, N]** that grows with N: would imply Landau's 4th. Best provable unconditional bound is constant. Best almost-prime bound is N/log N (Iwaniec, $P_2$).

5. **The productive direction** within Shakov's framework: the **interior-spine sieve** is structurally Sundaram's sieve enriched with algebraic-witness data from the SL_2(ℕ_0) words. It plugs into the [[B5-affine-sieve-attack|affine-sieve attack]] as a refinement, and it inherits the parity-problem barrier. To break parity, one would need to exploit the **bilinear** structure of the witness pairs (m_0, n_0), which is the same lever identified in B5 §3.

The honest summary: **the question opens a real avenue (the spine-sieve), but breaking parity within it remains the same wall as everywhere else**.
