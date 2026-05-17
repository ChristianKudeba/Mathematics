# Master synthesis: five proof-attempt papers on Landau's 4th via Shakov

This report consolidates findings from five independent mathematician-agents, each pursuing one of the promising directions identified in the bridges series ([[../bridges/B5-affine-sieve-attack]], [[../bridges/B7-research-integration]], [[../bridges/B8-priori-primes-and-spine-sieve]]).

The five papers:

| ID | direction | file | status |
|---|---|---|---|
| **P1** | Bilinear Type-II attack | `P1-bilinear-attack.tex` | complete (1153 ln) |
| **P2** | Spine-sieve combinatorics | `P2-spine-sieve-combinatorics.tex` | complete (620 ln) |
| **P3** | Hecke / class-field reframing | `P3-hecke-classfield.tex` | complete (918 ln) |
| **P4** | Transfer operator spectrum | `P4-transfer-operator.tex` | complete (737 ln) |
| **P5** | Joint highway quadruple density | `P5-joint-highway.tex` | complete (677 ln) |

**Headline.** None of the five proves Landau's 4th. None improves Iwaniec's $P_2$ count, Pascadi / Grimmelt–Merikoski's $\theta = 1.312$ greatest-prime-factor exponent, or any other unconditional result in the literature on $n^2+1$. **However**, several papers produce genuinely new results, new structural connections within Shakov's framework, and important *negative results* that correct conjectures from the bridges series.

---

## Ranked list of significant proven results

### Tier 1 — Genuinely new results (most significant)

#### **#1. The resultant-prime coincidence** (P5, Lemma 6.1)
The six pairwise resultants of the four enumerable polynomials $\mathcal{F} = \{\phi_0, \phi_1, \psi_2, \phi_3\}$ are *exactly* the first six primes:
$$\{\mathrm{Res}(f, g)\}_{f < g \in \mathcal{F}} = \{2, 3, 5, 7, 11, 13\}, \quad \text{each appearing once}.$$
This is the **joint counterpart of the discriminant coincidence** ([[../bridges/B2-discriminant-coincidence]]) — a small-numbers phenomenon that does not appear in the standard literature on Bunyakovsky-type problems. Consequence: the four polynomials of $\mathcal{F}$ share no common roots mod $p$ for $p > 13$, giving clean local independence at all but six primes.

#### **#2. Quantitative degeneracy of Hecke characters on the Landau slice** (P3, Theorem 5.2)
On the slice $\{n + i : n \ge 1\} \subset \mathbb{Z}[i]$ relevant to Landau's 4th, the angular Hecke characters $\chi_{4k}(\alpha) = (\alpha/|\alpha|)^{4k}$ become **asymptotically trivial** because $\arg(n+i) = \arctan(1/n) \to 0$. **Precise quantification**: Heath-Brown's narrow-cone equidistribution achieves cone width $X^{-1/4+\varepsilon}$, but Landau requires $X^{-1/2+\varepsilon}$. A clean theorem locating exactly *why* decades of Hecke L-function attacks on Landau have failed.

#### **#3. Refutation of the B7 spectral conjecture** (P4, Theorem 2.4 / Proposition 4.3)
The conjecture from [[../bridges/B7-research-integration]] that the row-sum eigenvalue $\lambda_+ = (5+\sqrt{17})/2$ corresponds to Iwaniec's half-dimensional sieve constant $\kappa = 1/2$ is **proven false**. Specifically:
- $\lambda_+$ is the dominant eigenvalue of the explicit $2 \times 2$ first-moment matrix $\begin{pmatrix}3 & 2 \\ 2 & 2\end{pmatrix}$, computed by tracking $(M_k, N_k) = (\sum_A \chi_1(A), \sum_A \chi(A))$ on row $k$.
- It is *not* a pressure value of the symbolic transfer operator $\mathcal{L}_s$.
- The numerical proximity $\log 2 / \log \lambda_+ \approx 0.4565 \approx 1/2$ is **fortuitous**.

A clean corrective. The genuine identification of $\kappa = 1/2$ is given separately (P4 Theorem 5.2): it is the order of pole of $\sqrt{D(s)}$ at $s=1$ where $D(s) = \zeta(s) L(s, \chi_4) E(s)$. P3's Theorem 4.2 makes the same correction from the L-function side.

#### **#4. Mayer / GKW identification of the Shakov transfer operator** (P4, Theorem 4.1)
The symbolic transfer operator $\mathcal{L}_s$ on $\{S, T\}^{\mathbb{N}}$ with the matrix-norm potential is **conjugate** (via the alphabet-doubling $s \mapsto 2s$) to a sub-operator of Mayer's GKW continued-fraction transfer operator on $A_\infty(\mathbb{D})$. This places Shakov's combinatorics on the same analytic footing as classical continued-fraction dynamics, importing all of Mayer–Roepstorff, Wirsing, Pollicott–Vytnova, and Hensley.

Recovers spectral data: $\lambda_1(1) = 1$ (Gauss measure), $\lambda_2(1) = \lambda_{\mathrm{GKW}} \approx 0.30366$ (Wirsing constant). Critical exponent $\delta = 1$.

#### **#5. Disjunctive equivalence — joint highway gives no logical advantage** (P5, Theorem 9.1)
The "easier-looking" disjunctive statement
$$\pi^\cup(N) := \#\{n \le N : \text{at least one of } f(n) \text{ is prime, } f \in \mathcal{F}\} \to \infty$$
is **logically equivalent** to "$\pi_f(N) \to \infty$ for some specific $f \in \mathcal{F}$" — i.e., to single-polynomial Bunyakovsky for at least one of the four. The joint approach gives no logical weakening of the underlying problem. A precise negative result that **kills the optimistic "quadruple-coupling" hope** from [[../bridges/B7-research-integration]].

#### **#6. New conjecture: Iwaniec's $\kappa = 1/2$ as a limiting Hensley dimension** (P4, Conjecture 8.4)
NEW conjecture: $\kappa = 1/2$ should equal the limiting Hausdorff dimension of the bidegree-$a$ spinal sub-monoid $\langle S^a, T^a \rangle$ as $a \to 1$. Hensley's $\delta_2 \approx 0.5313$ is just above $1/2$. **Testable numerically** with Pollicott–Vytnova methods. If true, this gives a new geometric interpretation of the half-dimensional sieve.

#### **#7. Bilinear conjecture pinpointed in two equivalent forms** (P1 Conj 7.1, P3 Conj 6.4)
The single bilinear estimate that would unlock Landau via the Friedlander–Iwaniec asymptotic sieve is now precisely formulated:
$$\sum_{\substack{(a,b,c,d) \in \mathbb{N}_0^4 \\ ad-bc=1, \, ac+bd \le N}} \alpha(a,b)\, \beta(c,d) = O(N^{1-\delta}), \quad \delta > 0$$
**P3 shows this is equivalent** to a bilinear estimate on the codimension-1 slice $\{\im(\bar\gamma\delta) = 1\} \subset \mathbb{Z}[i] \times \mathbb{Z}[i]$. The two formulations are the SAME conjecture in two languages.

### Tier 2 — Substantive new structural results

#### **#8. Functional equation for the $\Phi_0$ generating function** (P2, Theorem 3.1)
Trivariate generating function $G(x, y, z)$ for the $\Phi_0$-tree satisfies an exact functional equation derived from the free-monoid structure. Specialization gives $\sum_n \tau(n^2+1) x^n = 1 + 2 G(x, x, 1)$.

#### **#9. Exact small-depth survival densities** (P2, Theorems 5.4, 5.5)
The "depth-$\le k$" surviving density of the spine sieve is computed exactly:
- $\delta_2 = 2/5$ (exact rational)
- $\delta_3 = 33/130$ (exact rational)

These are testable predictions for the truncated singular series of $\phi_0$ and constitute the first explicit computation of spine-sieve survival rates.

#### **#10. Sundaram's sieve as the depth-1 spine sieve** (P2, Theorem 4.2)
Sundaram's classical 1934 sieve is *precisely* the depth-1 spine sieve of the (non-enumerable, degenerate) polynomial $f_S(n) = 2n+1$ in the trivial enumeration of $\mathbb{N}$. This identifies Shakov's interior-spine construction as a structural generalization of the oldest combinatorial sieve.

#### **#11. Multiplicity identity** (P2, Theorem 5.6)
$$\mu^{(S)}_{\phi_0}(n) + \mu^{(T)}_{\phi_0}(n) = \tau(n^2+1) - 2$$
where the LHS counts the appearances of $n$ on the two interior spine families. Decomposes the divisor count $\tau(n^2+1)$ along the $S/T$-word structure.

#### **#12. Joint a-priori prime count** (P5, Theorem 7.1)
$\pi^\cup(N) \ge 5$ for $N \ge 5$, with explicit witnesses. A **12-prime tally with multiplicity** for $n \in [1, 5]$ across all four polynomials of $\mathcal{F}$ — a clean small-numbers consequence of the generalized lemma from [[../bridges/B8-priori-primes-and-spine-sieve|B8]].

#### **#13. $\Phi_0$ as Gaussian-integer factorization, made fully explicit** (P3, Theorem 2.1)
The map $\Phi_0$ is *literally* the Gaussian factorization map: $(a - bi)(c + di) = n + i$ with $n = ac + bd$ when $ad - bc = 1$. Combined with explicit Hecke L-function dictionary (P3 Prop 3.3): $L(s, \chi_{4k})$ is the generating function of the first-row data of the $\Phi_0$-tree.

#### **#14. Three-dimensions disambiguation** (P3, Theorem 4.2)
The "half" in Iwaniec's half-dimensional sieve refers to the **value-set density** of sums of two squares (Landau's theorem, $\kappa = 1/2$), NOT to Gaussian-prime density ($\kappa = 1$) or to the rational sieve dimension of $\{n^2+1\}$ ($\kappa = 1$). Corrects an ambiguity in the existing notes ([[../research/R1-iwaniec-and-sieves]]).

#### **#15. Local joint admissibility** (P5, Proposition 6.3)
For every prime $p$, $\omega_\cup(p) < p$ where $\omega_\cup(p)$ counts the joint roots of $\mathcal{F}$ mod $p$. The conjunction $\pi^\cap$ has **no Hasse obstruction**. Extends to a Galois decomposition of the joint Bateman–Horn constant via Frobenius classes in $(\mathbb{Z}/2)^4$.

### Tier 3 — Foundational infrastructure / numerical data

#### **#16. Trivial-bound exact identity** (P1, Theorem 4.1)
$$\#\mathcal{X}_N = 1 + \sum_{n \le N} \tau(n^2+1)$$
where $\mathcal{X}_N := \{A \in SL_2(\mathbb{N}_0) : \chi(A) \le N\}$. The foundation of any bilinear-attack accounting.

#### **#17. Cauchy–Schwarz saturates the trivial bound** (P1, Proposition 5.3)
The diagonal contribution $a^2+b^2 \approx \sqrt{N}$ alone gives $\sim (3/\pi) N \log N$, exactly matching the trivial bound. Cauchy–Schwarz on the bilinear sum cannot beat this without exploiting cancellation *inside* the diagonal regime. Locates the obstacle precisely.

#### **#18. The natural $S/T$-word spin equidistributes on rows** (P1, Proposition 6.2)
The candidate spin $\mathrm{spin} : SL_2(\mathbb{N}_0) \to \{\pm 1\}$ derived from the parity of $S$'s in the $S/T$-word has zero mean on each row of the binary tree. **However**, the boundary spines contribute a *deterministic* positive bias of size $1 + 2\lfloor N/2 \rfloor$ to the cumulative spin sum (Theorem 6.5). Empirically the strict-interior cumulative spin sum carries a negative bias of order $-N/\log N$, so cancellation between boundary and interior is **partial but not power-saving**. A precise localization of why the natural spin candidate fails as a parity-breaker.

#### **#19. Spectral data on small congruence quotients** (P4, §7)
Explicit numerical computation of the Cayley graph eigenvalues:
- $SL_2(\mathbb{F}_2) \cong S_3$: spectrum $\{2, 1, 1, -1, -1, -2\}$
- $SL_2(\mathbb{F}_3)$: spectrum $\{\pm 2, \pm \sqrt{3} \times 2, \pm 1 \times 4, 0 \times 6\}$, gap $2 - \sqrt{3} \approx 0.268$

Foundation for testing the Bourgain–Gamburd-style uniform spectral gap conjecture (P4 Conjecture 7.3).

#### **#20. Bateman–Horn constants tabulated** (P5, Heuristic 8.1)
$C(\phi_0) \approx 1.37$, $C(\phi_1) \approx 2.24$, $C(\psi_2) \approx 1.85$, $C(\phi_3) \approx 3.55$. The $\phi_3$ constant — the largest — confirms quantitatively the "prime-rich" character of $n^2 + 3n + 1$ already visible in the [[../bridges/B8-priori-primes-and-spine-sieve|generalized lemma]] (5 a-priori primes).

---

## Cross-paper triangulation: what we now know with certainty

The five papers, taken together, **converge** on a single sharp picture:

1. **The bilinear conjecture (P1 Conj 7.1 = P3 Conj 6.4) is the precise bottleneck.** Whether stated as a Type-II estimate over $SL_2(\mathbb{N}_0)$-words or as a slice estimate in $\mathbb{Z}[i] \times \mathbb{Z}[i]$, it is the missing ingredient. Proving it would yield Landau via the Friedlander–Iwaniec asymptotic sieve.

2. **The natural candidates for parity-breaking spin/character do not work.** P1's $S/T$-word spin has unbalanced boundary contribution. P3's angular Hecke characters degenerate on the slice. Any successful spin must be more cleverly constructed.

3. **The "highway" coupling does not give a logical shortcut.** P5's disjunctive equivalence theorem (#5) shows that a joint disjunction is no easier than the underlying single-polynomial conjecture.

4. **Shakov's framework IS class field theory of the small quadratic orders, made combinatorial.** P3 makes the dictionary explicit. The combinatorial reformulation does not produce information that is *logically* invisible to classical methods, but it does **expose bilinear structure** (the four-variable $(a,b,c,d)$ parametrization) that is not naturally present in the one-variable $n^2+1$ formulation. This is the single most promising structural feature.

5. **The transfer-operator spectrum of $\mathcal{L}_s$ is now known** (P4) to be the GKW spectrum, with $\lambda_2 = \lambda_{\mathrm{GKW}}$ as the spectral gap. Iwaniec's $\kappa = 1/2$ is **not** in this spectrum — it lives on the L-function side as a pole order.

6. **New small-numbers coincidences in Shakov's classification** (P5 #1, P4 #6) — both the resultant pattern $\{2,3,5,7,11,13\}$ and the conjectural Hensley-dimension/$\kappa$ identification suggest there is *more structure* in the four-polynomial classification than has been exploited.

## What was honestly NOT achieved

- **Landau's 4th**: not proved.
- **Iwaniec's $P_2$ result** ($\#\{n \le N : n^2+1 \in P_2\} \gg \sqrt{N}/\log N$): not improved.
- **Pascadi / Grimmelt–Merikoski $\theta = 1.312$** greatest-prime-factor exponent: not improved.
- **No $f(N) \to \infty$ lower bound** on $\pi_{\phi_0}(N)$ obtained.
- **Friedlander–Iwaniec bilinear estimate** not adapted to $SL_2(\mathbb{N}_0)$.
- **The natural spin** identified in P1 does *not* break parity.

The bilinear conjecture (#7) remains open. Its proof — or refutation — is the single most important next step.

## Open questions emerging from the synthesis

1. **(P1 / P3)** Construct a spin function on $SL_2(\mathbb{N}_0)$ whose cumulative sum has both balanced boundary and power-saving interior cancellation. The natural candidate fails (#18). What additional structure must such a spin carry?

2. **(P4 #6)** Numerically compute the Hensley dimensions $\delta_a$ for the bidegree-$a$ spinal sub-monoid $\langle S^a, T^a \rangle$ for $a = 2, 3, 5, 10$ using Pollicott–Vytnova, and check whether they extrapolate to $1/2$ as $a \to 1$.

3. **(P2 #9)** Compute exact survival densities $\delta_k$ for higher $k$. Is there a closed form?

4. **(P5 #1)** Is the resultant-prime coincidence $\{2,3,5,7,11,13\}$ a structural consequence of the discriminant coincidence, or is it independent? If structural, generalize.

5. **(P3, P4)** Is the bilinear conjecture provable on a smooth/smoothed version of the slice (e.g., with Schwartz cutoffs in place of indicator functions)? If so, can the smoothing be removed?

## Bottom line

The five papers achieved Goal 2a (new connections in Shakov's framework) and Goal 2b is partially achieved through corrections of the bridges series (#3, #5) and new conjectures with concrete numerical content (#6). Goal 1 (Landau's 4th) is not achieved and is **localized precisely** to the bilinear conjecture #7 plus the construction of a working spin (#18 obstruction).

The Shakov framework remains, after this analysis, the most structurally promising fresh angle on Landau's 4th in 50 years — but the parity barrier remains exactly where it was, now visible through a clearer lens.
