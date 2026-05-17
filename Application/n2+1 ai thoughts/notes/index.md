# Shakov Paper — Concept Map

Working hub for understanding *"Polynomials in $\mathbb{Z}[x]$ whose divisors are enumerated by $SL_2(\mathbb{N}_0)$"* (Shakov, Feb 2024) and its connection to **Landau's 4th problem** (infinitude of primes of the form $n^2+1$).

## How to read this graph

Start at [[concepts/00-overview]] for the one-screen summary of what the paper does and where the n²+1 problem hides inside it. Then follow links into either the **paper's internal machinery** (concepts/) or the **external mathematical landscape** (research/) we're trying to bridge to (bridges/).

## The paper's internal machinery

### Algebraic skeleton
- [[concepts/01-sl2-n0-monoid]] — the free monoid SL₂(ℕ₀), generators S and T, binary-tree enumeration
- [[concepts/02-diophantus-identity]] — $(a^2+b^2)(c^2+d^2) = (ac+bd)^2 + (ad-bc)^2$ and its β-generalizations
- [[concepts/03-divisor-pair-set]] — $\mathcal{D}_f = \{(m,n) : m \mid f(n)\}$
- [[concepts/04-equivariant-map]] — $\bar S$, $\bar T_f$, $\bar c_f$ and the equivariance condition
- [[concepts/05-complement-involution]] — $c$ on matrices, $\bar c_f$ on pairs, why they're conjugate

### The classification
- [[concepts/06-enumerable-polynomial]] — what makes a polynomial admit an invertible equivariant map
- [[concepts/07-classification-theorem]] — exactly four polynomials work
- [[concepts/08-the-four-polynomials]] — $\phi_0, \phi_1, \psi_2, \phi_3$ and why these specifically
- [[concepts/09-carl-schildkraut-lemma]] — degree must be ≤ 2, leading coefficient ±1

### The n²+1 connection
- [[concepts/10-landau-fourth-problem]] — the conjecture itself
- [[concepts/11-bunyakovsky-conjecture]] — the broader umbrella
- [[concepts/12-boundary-vs-interior]] — primality ⇔ absence from interior
- [[concepts/13-prime-characterization]] — the four equivalent matrix-counting reformulations

### The S-sequence and asymptotics
- [[concepts/14-S-sequence]] — the 2-regular sequence reading off the Φ₀ tree
- [[concepts/15-k-regular-sequences]] — Allouche–Shallit framework
- [[concepts/16-calkin-wilf-tree]] — Stern's diatomic sequence as a parallel
- [[concepts/17-inversion-algorithm]] — continued-fraction-like reduction in $\mathcal{D}_f$
- [[concepts/18-row-recursions]] — $M_k$, $N_k$, $R_k$, the 5x-2x recursion, ratio mean → 3/2

## External landscape (research subagent territory)

- [[research/R1-iwaniec-and-sieves]] — half-dimensional sieve, Iwaniec's $n^2+1$ has $\le 2$ prime factors infinitely often
- [[research/R2-parity-problem]] — the structural barrier between P₂ and P₁
- [[research/R3-friedlander-iwaniec]] — how parity was broken for $a^2+b^4$
- [[research/R4-binary-quadratic-forms]] — Gauss composition, primes as $x^2+y^2$, class field theory of ℚ(i)
- [[research/R5-thin-groups-affine-sieve]] — Bourgain–Gamburd–Sarnak, expansion in SL₂
- [[research/R6-zaremba-apollonian]] — continued-fraction prime statistics in semigroup orbits
- [[research/R7-k-regular-asymptotics]] — Heuberger–Krenn machinery for the S-sequence
- [[research/R8-automatic-sequences-and-primes]] — Mauduit–Rivat, primes in Thue–Morse, etc.
- [[research/R9-bianchi-spectral-apparatus]] — Lokvenec-Guleska large sieve (cubic $T^3$), Bruggeman–Motohashi sum formula, GL₂/Q(i) subconvexity status, FI $\ell^2$ axiom
- [[research/R10-voronoi-whittaker-eisenstein]] — Z[i]-Voronoi, no published bilinear-weighted Voronoi, Eisenstein evaluation template, Whittaker normalizations across 5 references, Airy-type transition asymptotic for $K_{2it}$

## Bridges (where the paper meets the broader program)

- [[bridges/B1-synthesis]] — the master document: how Shakov's framework could plug into conventional attacks
- [[bridges/B2-discriminant-coincidence]] — disc(φ₀,φ₁,ψ₂,φ₃) = -4,-3,8,5: the class-number-1 quadratic fields
- [[bridges/B3-interior-counting-program]] — restate Landau as an upper bound on interior multiplicities
- [[bridges/B4-S-sequence-density]] — can k-regular asymptotics give density results for fibers?
- [[bridges/B5-affine-sieve-attack]] — recasting Φ₀⁻¹(prime, ·) as a thin-orbit prime-counting problem
- [[bridges/B6-open-questions]] — concrete sub-problems whose resolution would move the needle
- [[bridges/B7-research-integration]] — **READ FIRST after B1**: integrates findings from all four research subagents; identifies the bilinear cross-term as the highest-impact opening, flags δ=1 boundary obstruction, and lists revised program
- [[bridges/B8-priori-primes-and-spine-sieve]] — extending Lemma `f(1), f(2) prime` (φ_3 gives 5 free primes!), the three difficulty layers, and the spine-sieve as a Sundaram-style reformulation of Landau's 4th

## Top-level takeaways (for quickly orienting a collaborator)

1. **The bilinear hook** ([[bridges/B7-research-integration]] §"The Shakov insight"): $\chi(A) = ac+bd$ gives the missing second variable for FI-style parity breaking on $n^2+1$. This is the single most promising lead.

2. **The discriminant coincidence** ([[bridges/B2-discriminant-coincidence]]): the four enumerable polynomials are exactly the smallest-discriminant fundamental quadratic orders with class number 1. Confirmed structurally — not a coincidence.

3. **The structural neighbor** in literature: **Rickards 2024 (Duke 2025), arXiv:2401.01860** — semigroups of SL₂(ℤ) acting on continued fractions with reciprocity obstructions. Closest published analogue.

4. **Shakov's follow-up paper**: arXiv:2510.22805 (2025) on the τ(n²+1) 2-regular sequence. Worth reading next.

## Proof-attempt papers

- [[proofs/MASTER-REPORT]] — Synthesis of P1–P5 (bilinear, spine sieve, Hecke/class field, transfer operator, joint highway). Headline: 6 Tier-1 new results, none proves Landau IV but several correct earlier conjectures.
- [[proofs/REFEREE-REPORT]] — Skeptical referee on P6–P9 (Bianchi-spectral attack chain): 9 critical, 12 serious, 5 needs-work issues catalogued.
- [[proofs/P11-master]] — **P11 (Bianchi Q→Q(i) extension): clean conditional reduction.** Three-section rewrite of P6–P9 addressing the referee report. 21 of 26 referee items now resolved; 3 partial; 1 subsumed; single residual gap is the Bianchi cubic moment over Q(i). Conditional on Petrow–Young-strength subconvexity → Landau IV.
- [[proofs/P10-tier-primality-and-windows]] — Tier-$k$ primality and window primality for the four enumerable polynomials.
- [[proofs/P12-pointwise-spin-identity]] — **P12 (pointwise spin identity, refereed proofs).** Five proven results in the Shakov framework: (A) pointwise determinant identity $\chi_4(a-b)\chi_4(c+d) = \chi_4(n+1)$; (A') second identity $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1)$; (B) bilinear-to-divisor reduction $T(N) = \sum_{n=1}^N \tau(n^2+1)\chi_4(n+1)$; **(C) unconditional bound $T(N) = O(N)$** via hyperbola + Selberg–Delange (genuine $\log N$ improvement over trivial); (D) sharp classification: at conductor 4, only the two linear-form identities exist. Empirically $T(N) \ll \sqrt N$ over $N \le 10^7$ (Conjecture C, would need subconvexity). All proofs verified by 4 rounds of adversarial review. See [[proofs/P12-review-transcript/README]].
