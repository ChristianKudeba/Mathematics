# Research integration — what the literature tells us

Synthesis of findings from the four research subagents. Reshapes the program in [[B1-synthesis]] in light of what's now known.

## The state of the art (consolidated)

### Where conventional methods sit on Landau's 4th

| year | result | how it relates to Landau |
|---|---|---|
| 1922 | Hardy–Littlewood prediction $\sim C\sqrt N/\log N$ | conjectural target |
| 1956 | Halberstam: Erdős–Kac for $n^2+1$ | ω(n²+1) ~ log log; doesn't bound min |
| 1978 | Iwaniec: $n^2+1 = P_2$ infinitely often | best known toward Landau |
| 2025 | Grimmelt–Merikoski: $\theta = 1.312$ in $P^+(n^2+1) \ge n^\theta$ | (Landau needs $\theta = 2$) |
| – | parity barrier | still standing |

The trajectory $\theta: 1.2182 \to 1.279 \to 1.3 \to 1.312$ over six years (de la Bretèche–Drappeau, Merikoski, Pascadi, Grimmelt–Merikoski) is real progress on the *exponent of largest prime factor*, but is asymptotically far from the goal.

### Parity-breaking landscape ([[../research/R3-friedlander-iwaniec]])

Every parity-broken polynomial result has **≥ 2 free integer variables**:
- Friedlander–Iwaniec ($a^2 + b^4$): bilinear in $a, b$
- Heath-Brown ($a^3 + 2b^3$): bilinear in $a, b$
- Heath-Brown–Li ($a^2 + p^4$): bilinear with prime auxiliary
- Green–Sawhney 2024 ($p^2 + nq^2$): Gowers-norm inverse, two prime variables

For $n^2 + 1$, there is one variable. **This is the structural reason FI does not transfer.**

## The Shakov insight that changes the picture

**The cross-term $\chi(A) = ac + bd$ exposes a bilinear partner that does not exist in the original $n^2+1$ formulation.**

When we count $n^2+1$ as a value of a polynomial, $n$ is a single variable. When we count it as $\chi(A) = ac + bd$ for $A \in SL_2(\mathbb{N}_0)$, we have *four* variables $(a, b, c, d)$ on the determinant surface $\{ad - bc = 1\}$ — a 3-dimensional algebraic variety. This is a **3-parameter family**, not a 1-parameter family.

Quoting from R3's bridge section verbatim:

> Matrix entries $(a,b,c,d)$ on the determinant surface supply the **missing second variable** for bilinear decomposition; FI spin corresponds to parity of $S$'s in the $S/T$-word.

This is **the** structural innovation. It's the insight that should drive a real attack.

## The spectral coincidence — log 2 / log λ₊ ≈ 0.456

Three numerical coincidences worth recording (from R1's bridge):

1. The dominant eigenvalue of the row-sum recursion is $\lambda_+ = (5+\sqrt{17})/2 \approx 4.5616$.
2. $\log 2 / \log \lambda_+ \approx 0.456$.
3. The **half-dimensional sieve dimension** (the $\kappa = 1/2$ that defines Iwaniec's framework) is $0.5$.

These are close but not equal. **Conjecture**: the *correct* spectral exponent for the $\Phi_0$-tree transfer operator (not the row-sum operator, but the full transfer operator on $L^2(\mathcal{D}_{\phi_0})$) is exactly $1/2$, recovering Iwaniec's dimension. The row-sum operator gives a slightly perturbed value because it averages over an arithmetic-mean rather than measure-theoretic sense.

If true: **Iwaniec's half-dimensional sieve and the $\Phi_0$-tree transfer operator are the same spectral object in two different languages.** The Shakov reformulation makes the half-dimensionality *combinatorial*.

## Critical caveats from R5/R6 (thin groups)

### Caveat 1 — δ = 1 boundary regime

The limit set of $SL_2(\mathbb{N}_0)$ has Hausdorff dimension $\delta = 1$ (it's the full positive boundary $\partial \mathbb{H} = [0, \infty]$). Bourgain–Kontorovich-style affine sieves work best at $\delta < 1$ (thin orbits) and are *weakest* at $\delta = 1$.

This is bad news for naive transfer-operator attacks: the spectral gap shrinks at the boundary $\delta \to 1$, and the Dolgopyat-style estimates degenerate. **The free monoid SL₂(ℕ₀) is precisely on the worst-case boundary** for current technology.

This caveat should be reflected in [[B5-affine-sieve-attack]]: the program there is more aspirational than I initially indicated.

### Caveat 2 — semigroup vs. group

BGS expansion proofs use inversion. The substitute for free monoids is **Dolgopyat-type transfer-operator estimates** (Naud, Stoyanov, Magee–Oh–Winter). These work but lose constants — the spectral gap is non-effective for $\delta = 1$.

Magee–Oh–Winter's Schottky-semigroup counting (mentioned in R5) is the closest existing technology. Adapting it to SL₂(ℕ₀) is real research.

### The Rickards parallel

**Rickards 2024 (Duke 2025), arXiv:2401.01860**, proves reciprocity-based obstructions on which integers appear as continued-fraction-style orbit values for sub-semigroups of $\Gamma_1(4) \subset SL_2(\mathbb{Z})$. This is **the closest published structural neighbor** to Shakov.

Cross-referencing: Rickards uses Kronecker symbol obstructions to show certain integers **cannot** appear in semigroup orbits. Shakov's Diophantus identity is a **positive** structural fact: certain matrix products **always** produce values of the form $\chi(A)^2 + 1$. The two perspectives are duals — Rickards finds when orbits *miss* targets; Shakov characterizes when orbits *cover* a divisor structure.

**Action item**: read Rickards carefully; his techniques may transfer.

### The HKRS warning

**Haag–Kertzer–Rickards–Stange 2024 (Annals 2024 / arXiv:2307.02749)** disproved the Apollonian local-global conjecture by finding similar structural obstructions. Where they found these obstructions painful (a counterexample), Shakov uses them as positive characterization tools. This is unusual and possibly pioneering.

## The k-regular sequences caveat (from R7/R8)

### The negative result that hurts

R8's bridge section contains a **critical negative observation**:

> Even a full equidistribution theorem for $\mathcal{S}(p)$ (over primes $p$) à la Mauduit–Rivat would NOT resolve Landau IV.

What's needed is **codomain-sieving** — fiber cardinality $|\mathcal{S}^{-1}(n)| = 2$ — not value distribution. Mauduit–Rivat methodology computes $\sum_{p \le N} f(\mathcal{S}(p))$ for nice $f$. We need $\sum_{n \le N} 1_{|\mathcal{S}^{-1}(n)| = 2}$. These are different problems.

The carry-property / Gowers-uniformity machinery of Mauduit–Rivat is built for **bounded** sequences. Shakov's $\mathcal{S}$ is unbounded but grows like $O((\log n)^2)$ thanks to the Jordan block structure. There's a hope that "carry property with polynomial loss" could bring it within reach — but this is real research.

### What Heuberger–Krenn DOES give

For partial sums $\sum_{n \le N} \mathcal{S}(n)$, Heuberger–Krenn applies. The result (combined with the Jordan-block-1 spectral data):
$$\sum_{n \le N} \mathcal{S}(n) = N \cdot P(\log_2 N) \cdot \Phi(\log_2 N) + O(N^{1-\delta})$$
where $P$ is a polynomial of degree $\le 2$ and $\Phi$ is Hölder-continuous, periodic. This is **a useful auxiliary result** but does not directly bear on Landau.

## Updated program

The five-step program in [[B1-synthesis]] needs revision:

### Steps that survive
- Step 1 (transfer operator characterization)
- Step 2 (orbit counting): the $\sim N \log N$ heuristic is consistent with what's expected
- Step 5 (bilinear breaking): now backed by R3's explicit observation

### Steps that need rethinking
- Step 3 (spectral gap on congruence quotients): δ = 1 boundary is hostile. May need entirely new technology.
- Step 4 (sieve for primes among matrices): inherits step 3's difficulty.

### A new step that emerges from R3

**Step 0 (Pre-condition)**: Make the FI spin / matrix-word-parity correspondence (from R3's bridge) **explicit and computable**. Specifically:
- Define spin($A$) for $A \in SL_2(\mathbb{N}_0)$ (or rather: identify the invariant on $A$ that corresponds to the spin of the Gaussian integer $a + bi$ with $\Phi_0(A) = (a^2+b^2, ?)$).
- Verify equidistribution numerically.
- Identify the Type II sum that this would let you bound.

This is concrete, doable, and unblocks the bilinear attack.

## Newly identified follow-up paper

**Shakov 2025: arXiv:2510.22805** — a follow-up paper on the τ(n²+1) 2-regular sequence (OEIS A383066). This should be read.

Action item: read this paper. It may already address some of [[B6-open-questions|the open sub-problems]] in B6.

## Bottom-line summary

The Shakov framework offers three concrete *new* technical openings:

1. **The bilinear cross-term $\chi(A)$ supplies the missing second variable** for FI-style parity breaking on $n^2+1$. This is the highest-impact observation.
2. **The half-dimensional sieve dimension may equal the spectral exponent of the $\Phi_0$ transfer operator**, providing a combinatorial reformulation of the κ=1/2 framework.
3. **The Jordan-block-1 spectrum of L makes $\mathcal{S}$ polylogarithmically slow-growing**, an unusual regime that may admit Mauduit–Rivat-style methods after technical adaptation.

These openings have to fight against:
- The $\delta = 1$ boundary obstruction for the affine sieve
- The semigroup-vs-group gap in expansion proofs
- The fundamental fact that codomain-sieving differs from value-distribution

Net: **the program is not immediately tractable, but it is the first genuinely new framework for Landau's 4th in 50 years.**
