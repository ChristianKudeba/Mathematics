# Honest assessment — what we proved, what it means for Landau IV

After four rounds of adversarial review and a fifth round on Theorem C, here is the unvarnished accounting.

## What we did, in order

### Initial session (May 2)

1. **Read the existing literature in the project** — `index.md`, B7 (research integration), B6 (open questions), B8 (spine sieve), MASTER-REPORT, P11-master, the four-polynomial concept files.
2. **Computed.** Wrote `compute-explore.py`. Generated $SL_2(\mathbb{N}_0)$ to depth, tested several spin functions, observed that the natural $S/T$-word parity has linear positive bias (matching P1's finding) and angular Hecke characters degenerate on the slice (matching P3).
3. **Discovered an empirical pattern.** A specific $\{0, \pm 1\}$-valued function on Gaussian integers, applied bilinearly to $\xi = a-bi$ and $\eta = c+di$, gave a cumulative sum that stayed bounded as $N$ grew.
4. **Mis-identified the function.** I claimed it was a multiplicative quadratic Hecke character $\sigma$ on $\mathbb{Z}[i]$. It wasn't.
5. **Pushed empirical evidence to $N = 10^7$.** $|T(N)|/\sqrt N$ stayed in $[0.06, 1.45]$ — square-root cancellation.
6. **Wrote up draft P12** claiming a multiplicative-character interpretation, an unconditional $O(\sqrt N)$ bound via "Hooley-style methods," and a "Plancherel completeness conjecture" giving Landau IV.

### Round 1 review

The skeptic found three real problems:
- **CRITICAL:** Theorem C's $O(\sqrt N)$ unconditional claim was a bluff — my "Hooley sketch" had a dimensionally wrong AP-sum bound (conflated conductor of $\chi_4$ with conductor $d$ of the AP). Citation to Iwaniec–Kowalski Ch. 14 was fictitious.
- **SERIOUS:** Theorem B had an off-by-one — identity matrix at $n=0$ contributed 1 but the sum from $n=1$ missed it.
- **SERIOUS:** Plancherel completeness was hand-waved without exhibiting a single second example.

The skeptic agreed Theorem A was correct.

### Round 1 → 2 revisions

1. Fixed Theorem B off-by-one.
2. **Retracted Theorem C's unconditional claim.** Replaced by Proposition C1 (sketch of $o(N \log N)$) plus Conjecture C (empirical $\sqrt N$).
3. **Demoted the Plancherel completeness conjecture.** Replaced by an honest open problem.
4. **Found a second linear-form identity** (Theorem A'): $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1)$. Showed it's equivalent to the first up to sign.
5. **Added Theorem D** classifying all linear-form identities at conductor 4.
6. **Acknowledged that the σ-character framing was wrong** — the actual function is $\rho(A) = \chi_4(a-b)\chi_4(c+d)$, NOT multiplicative on $\mathbb{Z}[i]$. The bilinear identity follows from the determinant constraint, not multiplicativity.

### Round 2 review

The skeptic verified all the round-1 fixes but caught one new substantive bug:
- **MAJOR:** Theorem D's proof was structurally wrong. The "exact-coefficient-matching" derivation demanded $\alpha\gamma = \beta\delta$, but my own canonical example $(a-b)(c+d) = ac - bd + 1$ has $\beta\delta = -1 \ne 1 = \alpha\gamma$. The classification statement might be true, but the proof did not establish it.

### Round 2 → 3 revisions

Rewrote Theorem D's proof. Used **mod-4 matching with the parity restriction**:
- In Case A ($a, d$ odd, $b, c$ even): $bc \in 4\mathbb{Z}$, so the $bc$-coefficient term vanishes automatically.
- In Case B ($b, c$ odd, $a, d$ even): $bc$ is odd, so the $bc$-coefficient must vanish mod 4.
- Combined: $\alpha\delta + \beta\gamma \equiv 0 \pmod 4$, plus other constraints, give the two-element classification.

### Round 3 review

The skeptic verified the rewritten proof and found one minor expository imprecision: the proof attributed the constraint $\alpha\delta + \beta\gamma \equiv 0 \pmod 4$ to "Case B alone," but Case B alone gives only the combined constraint $K_3 \cdot bc + K_4 \equiv 0 \pmod 4$ where $bc \equiv 3 \pmod 4$. To split them you need Case A first to pin down $K_4 \equiv 0$.

**Final verdict:** "YES, I now agree the proofs of Theorems A, A', B, D and Proposition C1 are correct as stated, modulo one minor expository clarification."

### Round 3 → 4 expository fix

Tightened Theorem D's proof to extract constraints in two stages: Case A first (constants and pure-monomial terms), then Case B (the $bc$-term).

### Round 4 — Theorem C from scratch

The user asked for a real proof of Theorem C, beyond the round-2 retraction. I:

1. **Computed the AP-sum split.** $T(N) = \sum_{n \equiv 0 \pmod 4} \tau(n^2+1) - \sum_{n \equiv 2 \pmod 4} \tau(n^2+1)$. Empirically these two sums differ by $O(\sqrt N)$ — main term cancellation works.
2. **Tried bilinear approach via Theorem A.** Group by $(a, b)$, sum over $(c, d)$. Inner AP-sum $\le 1$ when $\chi_4(a-b) \ne 0$. But the count of $(a, b)$ pairs with at least one matrix grows like $N \log N$, so the bilinear bound only gives $O(N \log N)$ — same as trivial. Dead end.
3. **Tried direct hyperbola decomposition.** $\tau(n^2+1) = 2 \cdot \#\{d \mid n^2+1, d \le n\}$. Swap order. Inner AP-sum bound. Get $|T(N)| \le 2 \sum_{d \in L_{\mathrm{odd}}, d \le N} 2^{\omega(d)}$.
4. **Selberg–Delange.** The multiplicative function $f(d) = 2^{\omega(d)} \mathbb{1}[d \in L_{\mathrm{odd}}]$ has $\kappa = 1$, giving $\sum f(d) \sim cN$.
5. **Key observation along the way:** even $d$ with $\rho(d) > 0$ (i.e., $d = 2d'$) force $n_0$ odd, hence $n$ odd, hence $\chi_4(n+1) = 0$. So even $d$ contribute zero, and only odd $d$ (in $L_{\mathrm{odd}}$) matter. This is what makes the proof work.

### Round 4 review

The skeptic ran 11-item verification at $N \le 5000$, confirmed every step empirically and structurally, found two cosmetic issues (spurious $+O(1)$; asymptotic-vs-uniform constant), and signed off **YES**.

### Round 4 cosmetic fixes

Removed the $+O(1)$ from the displayed bound; clarified that the explicit constant 0.637 is asymptotic and the rigorous statement is $|T(N)| = O(N)$.

## What we proved (the math content)

Five results, all refereed and signed off:

1. **Theorem A.** For every $A \in SL_2(\mathbb{N}_0)$, $\chi_4(a-b) \chi_4(c+d) = \chi_4(n+1)$ where $n = ac+bd$. Both sides 0 when $n$ is odd.

2. **Theorem A'.** Analogous with the second linear-form pair: $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1) = -\chi_4(n+1)$ for $n$ even.

3. **Theorem B.** $T(N) := \sum_{A \ne I, \chi(A) \le N} \chi_4(a-b)\chi_4(c+d) = \sum_{n=1}^N \tau(n^2+1) \chi_4(n+1)$.

4. **Theorem C (unconditional).** $|T(N)| \le 2 \sum_{d \in L_{\mathrm{odd}}, d \le N} 2^{\omega(d)} \sim 2cN$ for an explicit $c \approx 0.318$. Hence $T(N) = O(N)$ — a $\log N$ improvement over trivial.

5. **Theorem D.** At conductor 4, the only linear-form identities $\chi_q(L_1)\chi_q(L_2) = \chi_q(\text{function of } n)$ on $SL_2(\mathbb{N}_0)$ are $(a-b, c+d)$ and $(a+b, c-d)$ up to sign.

**Open:** Conjecture C, $|T(N)| \ll \sqrt N$, empirically verified to $N = 10^7$.

## Honest assessment: how far does this take us toward Landau IV?

### The short answer: not very far at all.

Here is the unvarnished accounting.

### What Landau IV requires

The Friedlander–Iwaniec asymptotic sieve, the only known route to break parity for sums of two squares, requires bilinear estimates of the form
$$\sum_{(a,b,c,d): ad-bc=1, ac+bd \le N} \alpha(a, b) \beta(c, d) = O(N^{1-\delta})$$
for arbitrary "Type-II" inputs $\alpha, \beta$ (with appropriate axioms — zero mean on residue classes, $\ell^2$-controlled, etc.).

### What we have

A bound for the *single specific* input pair $\alpha(a, b) = \chi_4(a-b)$, $\beta(c, d) = \chi_4(c+d)$, and even there our rigorous bound is $O(N)$, not $O(N^{1-\delta})$. The empirical $O(\sqrt N)$ is a Conjecture C, not a theorem.

### The four ways this falls short

1. **Specificity.** The Friedlander–Iwaniec sieve needs the bound for *every* Type-II input. We have one. Theorem D shows the linear-form-conductor-4 well is exhausted — there are essentially no other identities of this form. To handle other inputs, one needs higher conductor or different structure (quadratic forms, multiplicative characters on $\mathbb{Z}[i]$, etc.) — and our technique doesn't extend.

2. **Strength.** Even on the one input we handled, $O(N)$ is too weak. FI needs power-saving $O(N^{1-\delta})$ for some $\delta > 0$. The $\log N$ improvement over trivial is real but is not power-saving. The empirical $O(\sqrt N)$ would suffice, but it's conjectural.

3. **The Plancherel route is blocked at the entrance.** I had hoped that decomposing arbitrary $\alpha, \beta$ along Dirichlet characters of linear functionals would give a family of identities reducing to known cancellations. Theorem D rules this out: at conductor 4, only the one identity exists; at higher conductor, the determinant defect $-2bd$ no longer reduces sufficiently mod $q$. The Plancherel decomposition would have to use entirely different building blocks.

4. **The honest novelty is structural, not analytic.** What's actually new is the *pointwise determinant identity* — that the constraint $ad - bc = 1$ forces a parity on $bd$ that aligns the conductor-4 character on linear functionals with $\chi_4$ on the divisor variable $n$. This is a clean structural fact, but it sits inside the $\mathbb{Z}[i]$ machinery already known to the project (P3 made the Gaussian-factorization picture explicit). It does not overcome P3's core finding that the slice $\{n+i\}$ has degenerate analytic properties.

### Where this fits in the larger landscape

Compared to the project's other proof attempts:

| Result | What it claims | Honest status |
|---|---|---|
| P1 (bilinear attack) | Identifies the FI-style bilinear conjecture as the bottleneck | The conjecture is the bottleneck. P1 doesn't prove it. |
| P3 (Hecke / class field) | $\Phi_0$ is the Gaussian factorization; angular characters degenerate on the slice | Correct structural identification, no proof of Landau IV. |
| P5 (joint highway) | Disjunction across the four polynomials gives no logical advantage | Negative result correctly stated. |
| P11 (Bianchi extension) | Conditional reduction of Landau IV to a Bianchi cubic moment over $\mathbb{Q}(i)$ | Conditional on Petrow–Young-strength input over $\mathbb{Q}(i)$, which is itself a major open project. |
| **P12 (this work)** | One pointwise identity, sharp classification of similar identities, $T(N) = O(N)$ unconditionally | **Real but small.** Not a route to Landau IV. |

P11 is by far the closest to Landau IV — it is a *clean conditional reduction*. P12 sits well below P11 in terms of distance to the goal: it's a structural lemma, not a reduction.

### A more honest pitch for what P12 actually is

P12 is a **clean structural fact about $SL_2(\mathbb{N}_0)$ and $\chi_4$**:

> The constraint $ad - bc = 1$ with $a, b, c, d \ge 0$ forces a specific mod-4 alignment between linear functionals of the matrix entries and the divisor variable $n = ac+bd$. Among all linear forms, exactly two essential identities exist at conductor 4. The cumulative bilinear sum reduces to a twisted divisor sum $T(N) = \sum_n \tau(n^2+1)\chi_4(n+1)$, which is unconditionally $O(N)$ and empirically $O(\sqrt N)$.

This is a small but real piece of structure. It is not a step toward Landau IV by any reasonable accounting.

### What would actually move the needle

To get closer to Landau IV through this kind of analysis, one would need:

1. **A non-linear analogue** of Theorem A — perhaps $\chi(Q_1(a,b))\chi(Q_2(c,d))$ for quadratic forms $Q_1, Q_2$, with a determinant-driven cancellation that handles higher conductors.

2. **A bilinear estimate at the level of Hecke characters** — if one can show $\sum \psi_1(\xi)\psi_2(\eta) = O(N^{1-\delta})$ uniformly in the conductor of the Hecke characters $\psi_1, \psi_2$ over $\mathbb{Z}[i]$, this would feed into FI. This is essentially the Bianchi cubic moment that P11 conditioned on.

3. **A genuine new idea** that bypasses the parity barrier — something not in the FI / Hecke-L-function template at all.

P12 does none of these.

### Educational value

What this exercise demonstrated honestly:

- **Compute first.** I found the empirical pattern by computation, not by theorizing first. The methodology memo was right.
- **Beware of pattern-matching to known machinery.** My initial $\sigma$-character framing was wrong because I pattern-matched to "primary normalization in $\mathbb{Z}[i]$" before checking that what my code computed was actually that character. It wasn't.
- **Adversarial review catches real bugs.** Three of four rounds caught substantive errors (off-by-one, wrong proof of D, bluffed proof of C). One found expository imprecision. None of these would have been caught by self-review alone.
- **The honest result is smaller than the initial pitch.** The first writeup of P12 promised "first power-saving spin in the Shakov framework" with empirical $\sqrt N$ cancellation. The final, refereed result is "$O(N)$ unconditionally, with $\sqrt N$ as Conjecture C." This is a 2x weakening of the headline claim, and it is correct.

### Bottom line on Landau IV

Iwaniec (1978) proved $n^2+1$ is $P_2$ infinitely often. Grimmelt–Merikoski (2025) gave $\theta = 1.312$ for the largest-prime-factor exponent. P11 gave a clean conditional reduction modulo a major open input. **P12 does not improve any of these.** It adds a small structural fact to the toolkit. Whether that toolkit eventually reaches Landau IV is the same open question it was before this session.
