# Open questions and concrete sub-problems

A list of well-defined sub-problems whose resolution would advance the program. Ordered roughly by difficulty / promise.

## Tier 1 — Tractable, near-term

### Q1. Closed form for $\mathcal{S}(k)$
Stern's diatomic sequence has the closed form $a(n)$ = #hyperbinary representations of $n-1$. Does $\mathcal{S}$ admit an analogous combinatorial formula?

**Approach**: enumerate small values; conjecture; prove by induction on the recursion.

### Q2. Empirical verification of B&H heuristic
Compute $\chi(SL_2(\mathbb{N}))$ for matrices up to word-length 30. Verify:
$$\#(\chi(SL_2(\mathbb{N})) \cap [1, N]) \sim N - C\sqrt{N}/\log N$$
with $C \approx 1.37$ (the Bateman–Horn constant for $\phi_0$).

### Q3. Eigenvalue $(5+\sqrt{17})/2$ — what is it really?
The row-sum recursion has spectral radius $(5+\sqrt{17})/2$. The 17 = $4^2+1$ — the first nontrivial $\phi_0$-prime. **Conjecture (Shakov-style)**: the spectral data of the $\hat F_f$ row-sum recursions involves the smallest non-trivial prime values of $f$.

For $f = \phi_1$ (smallest nontrivial prime $\phi_1(2) = 7$), check: do the analogous row recursions have eigenvalues involving $\sqrt{p}$ for small primes related to $\phi_1$?

**Test**: derive the analogous $5x - 2y$-type recursion for $\Phi_1, \Psi_2, \Phi_3$ and tabulate.

## Tier 2 — Moderate, doable with serious work

### Q4. Spectral gap for the SL₂(ℕ₀) action on $\mathcal{D}_{\phi_0}/q$
Define the operator
$$\mathcal{L}_q f(m, n) = f(\bar S(m,n)) + f(\bar T_{\phi_0}(m,n))$$
acting on $L^2(\mathcal{D}_{\phi_0}/q)$. Prove a spectral gap uniformly in $q$.

This is the **technical heart** of any affine-sieve attack. Probably requires adapting Bourgain–Gamburd to free monoids.

### Q5. Quantitative density of $\{n : \tau(n^2+1) \le K\}$
For each fixed $K \ge 2$, lower-bound:
$$\#\{n \le N : \tau(n^2+1) \le K\} \ge ?$$

For $K = 2$ this is Landau. For $K = 3$ this is "$n^2+1$ is prime or twice prime." For larger $K$, easier. Best-known result: Iwaniec's $K = 4$ (i.e. $P_2$ + $\le 2$ small extra factors).

The Shakov approach should give this *as a corollary* of fiber-size asymptotics for $\mathcal{S}$.

### Q6. Bilinear sums over SL₂(ℕ₀)
Estimate the bilinear sum
$$\sum_{(a,b)\ \text{coprime}} \sum_{(c,d) : ad - bc = 1, ac+bd \le N} \alpha_{a,b} \beta_{c,d}$$
for arbitrary bounded sequences $\alpha, \beta$. This is the parity-breaking ingredient. See Friedlander–Iwaniec for the prototype in $a^2 + b^4$.

## Tier 3 — Major projects

### Q7. Hecke L-function reformulation of $\mathcal{S}$
Express the generating function $\sum_n \mathcal{S}(n) x^n$ in terms of Hecke $L$-functions of $\mathbb{Q}(i)$. Use the resulting Euler product to extract level-set densities via Tauberian methods.

### Q8. Joint density of the four polynomials
For all four enumerable polynomials simultaneously: lower-bound
$$\#\{n \le N : \phi_0(n), \phi_1(n), \psi_2(n), \phi_3(n)\ \text{all have } \le K\ \text{prime factors}\}.$$

This is a quadruple-prime-constellation result. Even $K = 4$ would be new.

### Q9. SL₂(ℕ₀) version of the $a^2 + b^4$ trick
Friedlander–Iwaniec broke parity for $a^2 + b^4$ by leveraging the asymmetry $a \ne b$. In the cross-term $\chi(A) = ac + bd$, the four entries are *not* symmetric — the determinant constraint couples $(a,d)$ and $(b,c)$ asymmetrically. Find an analogue of FI's bilinear estimate that exploits this asymmetry.

### Q10. Higher-rank Shakov classifications
Classify polynomials in $\mathbb{Z}[x_1, \ldots, x_n]$ enumerated by free monoids $SL_n(\mathbb{N}_0)$ or $Sp_{2n}(\mathbb{N}_0)$. By the [[B2-discriminant-coincidence|discriminant coincidence]] hypothesis, this should produce the analogous "small-discriminant + class number 1" forms in higher rank.

If the analogue of $\phi_0$ in rank 3 exists, attacking *its* Bunyakovsky conjecture might benefit from the additional symmetry of higher rank.

## Tier 4 — Speculative

### Q11. The "innumerable polynomials" idea
Shakov's title hints at polynomials whose divisor structures *resist* counting because of structural symmetries. Formulate this notion precisely:
> A polynomial $f$ is **innumerable** if no SL_n(ℕ₀) action enumerates $\mathcal{D}_f$.

Are there interesting innumerable polynomials? Do they correspond to forms with $h > 1$? Class number $> 1$ orders?

### Q12. Connection to Markov triples
The Markov equation $x^2 + y^2 + z^2 = 3xyz$ has solutions parameterized by an SL₂(ℤ) action. Markov triples sit on the **Markov spectrum**. Are there hidden Markov-style identities for the four enumerable polynomials? Might Markov-spectrum techniques apply?

### Q13. Modular-form interpretation
Each enumerable polynomial $f$ comes with a sequence $\mathcal{S}_f$. Are these sequences related to the Fourier coefficients of any modular form? CM forms over $\mathbb{Q}(\omega)$? Theta series of the norm form $N_f$?

## How to use this list

These questions are nominally *independent* and could be attacked by different collaborators. The most strategic move would be:

1. **Solve Q1, Q2, Q3** first (low-hanging fruit, sets up intuition).
2. **Attempt Q4** seriously. This is the single technical bottleneck — without spectral gap, no affine sieve.
3. In parallel, **Q6 / Q9** by FI experts.
4. **Q5** falls out of Q4+Q6.
5. **Landau** falls out of Q5 with $K = 2$, but parity will likely block.
6. **Joint Q8** with all four polynomials might break parity for at least one.

A genuine, full solution to Landau's 4th will require a synthesis of Q4-Q6-Q8-Q9, plus probably a new idea we haven't yet identified.
