# Skeptical referee report on P6–P9

Author of this report: a skeptical analytic number theorist who has spent decades fighting the parity barrier and is reading P6–P9 with maximum suspicion. Findings are organized by paper, then by severity (CRITICAL / SERIOUS / NEEDS-WORK / MINOR).

---

## Cross-cutting issues (most serious)

### XC-1 (CRITICAL). The $\ell^2$-to-$\ell^\infty$ "transition" in P6 §6 is wrong.

P6 Lemma 6.1 says: "$A, B$ supported on $\{|\xi|^2 \le X\}$ with $\|A\|_\infty \le 1 \Rightarrow \|A\|_2 \le X^{1/2}$, with $X \asymp N^{1/2}$ this gives $\|A\|_2 \|B\|_2 \le N^{1/2}$."

Then claims this gets plugged into $\Sigma_\psi \ll N^{1-\eta_2} \|A\|_2 \|B\|_2$ to give $\Sigma_\psi \ll N^{1-\eta_2} \cdot N^{1/2}$, then asserts this equals $N^{1-\eta_2} \|A\|_\infty \|B\|_\infty$.

**The arithmetic is incoherent**: $N^{1-\eta_2} \cdot N^{1/2} = N^{3/2-\eta_2}$, which is **worse than the trivial bound $N \log N$** for any $\eta_2 < 1/2$. Plugging $\|A\|_\infty = 1$ does not save the factor $N^{1/2}$; the $\ell^2$-to-$\ell^\infty$ transition genuinely costs you a power.

**The conjecture as stated requires $\ell^\infty$ control, and spectral methods over $\mathbb{Q}(i)$ produce $\ell^2$ bounds.** This gap is fundamental and not addressed anywhere in P6–P9. **The entire chain may collapse here.**

### XC-2 (CRITICAL). The conditional implication "subconvexity ⇒ bilinear" is asserted, never proved end-to-end with consistent norms.

Throughout P6–P9, the bound on $\Sigma$ is repeatedly stated as
$$\Sigma \ll N^{1-\delta+\varepsilon} \|A\|_\infty \|B\|_\infty,$$
but the proof goes through $\ell^2$ norms (Bessel inequality, Cauchy–Schwarz on the spectral side). The closing step — converting the $\ell^2$ bound back to $\ell^\infty$ — never properly accounts for the support size. This is XC-1 in its more serious incarnation.

### XC-3 (SERIOUS). The "main term" identification in P7 Proposition 2.5 is dimensionally suspect.

The main term is asserted to be $\widehat\psi(0) \widetilde A(1/2) \widetilde B(1/2) \cdot N$.

(a) For generic $A \in \ell^\infty$, the Dirichlet series $\widetilde A(s) = \sum A(\xi)/|\xi|^{2s}$ converges absolutely only for $\Re(s) > 1$. Evaluating at $s = 1/2$ requires analytic continuation, which depends on more than just $\|A\|_\infty < \infty$. **For arbitrary $\ell^\infty$ sequences, $\widetilde A(1/2)$ is not even defined.**

(b) Even if we restrict to $A$ for which $\widetilde A(s)$ has analytic continuation, the value at $s=1/2$ is generically unbounded (it can be of size $X^{1/2}$ for $A$ supported on $|\xi|^2 \le X$). Plugging this in produces a main term of the wrong order.

(c) The "main term" $\widetilde A(1/2) \widetilde B(1/2) \cdot N$ should be the residue of $\widetilde A(s) \widetilde B(s)$ at $s=1$ times some kernel — but $\widetilde A(s)$ generically has no pole at $s=1$ for $A \in \ell^\infty$ (only the constant function does).

This identification of the main term needs to be redone from scratch. **P7's main reduction may be working with the wrong main term.**

### XC-4 (SERIOUS). The Eisenstein contribution is hand-waved throughout.

In P7 Theorem 4.2 and P8 Lemma 2.1, the Eisenstein contribution is "treated similarly" to the cuspidal contribution. **For divisor-correlation problems over $\mathbb{Z}[i]$, the Eisenstein contribution is NOT asymptotically smaller — it contains the main divisor-asymptotic term**, and its careful evaluation is the whole game. The standard reference (e.g., Bykovsky, Templier, Blomer) handles this with substantial work.

In P8 the Eisenstein contribution becomes $W_0$ (Lemma 2.1) — but the formula given mixes Kloosterman-type sums with Dirichlet character data in a way that is **not the standard Eisenstein evaluation** for the Bianchi setup. The expression should involve incomplete Eisenstein series and their inner products with $A, B$, not just Kloosterman-twisted bilinear sums.

### XC-5 (SERIOUS). The conductor-aspect uniformity in subconvexity \eqref{eq:subconv-input} is glossed.

The hypothesis stated is "for $\chi$ of conductor $\le T$." But the Dirichlet characters arising from the moduli $c$ in our setup have conductor *equal to* $|c|^2$ or divisors thereof, ranging up to $|c|^2 \asymp N$. So we actually need uniformity for $\mathrm{cond}(\chi) \le N$, while $T = N^{1/2}$ is the spectral cutoff. **The condition $\mathrm{cond}(\chi) \le T$ is much weaker than what the proof actually needs.**

Petrow–Young give uniformity in conductor $q$ subject to certain restrictions (cube-free $q$); the Bianchi analog would need similar restrictions. **No such restriction is checked anywhere in P6–P9.**

### XC-6 (SERIOUS). The free monoid / Shakov framework plays no analytic role.

Already noted. Once the Gaussian-integer reformulation is made (P6 Lemma 1.1), the Shakov machinery vanishes. **P6–P9 are not Shakov-framework attacks.** The corresponding work could have been (and structurally has been) attempted by other authors via classical Gaussian-divisor reformulations of $n^2+1$. This doesn't make the work wrong, but it limits the novelty claim.

---

## P6 (`P6-bilinear-attack-serious.tex`)

### P6-1 (CRITICAL). §3 dispersion is anti-strategic.

Cauchy–Schwarz $|\Sigma|^2 \le N \cdot D(N)$ throws away the cancellation in $c_n$ before it can be exploited. In standard FI-style attacks, the bilinear sum is bounded *directly* via Type II (multiplicative) input, **never** through CS to a divisor sum. The proof of Theorem 4.1 in P7 effectively reverses the CS, but the entire dispersion calculation in P6 §3 then becomes vestigial.

### P6-2 (SERIOUS). §4.7 spectral expansion of $M(\theta;N)$ is asserted, not proved.

Equation (5.1) writes $M(\theta;N) = $ (main) + spectral sum + Eisenstein + error. The proof sketch (Proposition 4.7) just says: "Apply Kuznetsov in the form (5.1)." But (5.1) is what we are trying to derive. The legitimate derivation requires:
(a) Expressing $M$ in Kloosterman-sum form;
(b) Applying the Bianchi Kuznetsov dual side;
(c) Tracking the test function transform.

None of these is done in P6 §4.

### P6-3 (SERIOUS). §5.2 "smoothed bilinear sum" assumes spectral basis decomposition for $A, B$.

The claim "$\Sigma_\psi = \sum_j A_j \overline{B_j} K_j(N)$" assumes $A$ and $B$ have valid expansions in the Hecke–Maass + Eisenstein basis. **For $A, B \in \ell^\infty$ but not $L^2$, the projections $A_j$ are not even well-defined.** This is XC-1 again.

### P6-4 (NEEDS WORK). The Bianchi second-moment Theorem 4.6 is stated as Lokvenec-Guleska, but...

Lokvenec-Guleska's thesis (2004) gives the spectral large sieve for Bianchi forms, not directly the second-moment bound stated. The bound
$$\sum_{|t_j|\le T} |L(1/2+it, u_j)|^2 \ll (T(1+|t|))^{2+\varepsilon}$$
is plausible by Cauchy–Schwarz from spectral large sieve + functional equation, but **the precise reference for this exact statement should be verified.** It may be in Bruggeman–Motohashi's *Sum formula for Bianchi forms*, or it may not be — the reader is asked to take this on trust.

### P6-5 (NEEDS WORK). "Power-saving error term" claim in Theorem 5.1.

The statement $D_{\text{off}}(N) \ll N^{1/2+\eta_0+\varepsilon}$ is derived under the conditional subconvexity, but the integration over $\theta$ in §5 implicitly assumes the bound in $\theta$ is integrable. The function $(1+|\theta| N)^{-1/2+\eta_0}$ is integrable on $[-1/2, 1/2]$ for any $\eta_0 < 1/2$, but the factor $N^\varepsilon$ inside the bound may depend on $\theta$ — this is not addressed.

### P6-6 (MINOR). The "boundary spine" terminology and SL₂(ℕ₀) interior count.

The interior count $\#\{A \in SL_2(\mathbb{N}) : \chi(A) \le N\}$ is asserted equal to $1 + \sum_{n \le N} \tau(n^2+1)$ minus boundary, giving $\sim (3/\pi) N \log N$. This is correct (Hooley/McKee), but the paper should distinguish between $\sum \tau(n^2+1)$ and the Hooley constant explicitly. The constant $3/\pi$ is from $\sum_{n \le N} r(n) \sim \pi N$, not $\tau(n^2+1)$ (which is $\sim N \log N$ with constant $3/\pi$). Verify the constant.

---

## P7 (`P7-filling-the-gaps.tex`)

### P7-1 (CRITICAL). Theorem 2.5 (Voronoi for bilinear weights) is wrong as stated.

The proof is: "Decompose $d_{A,B}(\nu) = \sum_{\nu_1\nu_2=\nu} A(\nu_1) B(\nu_2)$; for fixed $\nu_1$, apply standard Voronoi to inner sum." The fatal issue:

After fixing $\nu_1$, the Voronoi formula transforms a sum over $\nu_2$ against a test function $f(|\nu_2|^2)$. **In our setting, the test function is $f(|\nu_1|^2 |\nu_2|^2)$**, which depends on $\nu_1$. Voronoi gives a transformed sum over $\nu_2'$ with kernel $\widetilde f$ depending on $\nu_1$.

When we then sum over $\nu_1$, we get a double sum:
$$\sum_{\nu_1} A(\nu_1) \sum_{\nu_2'} B(\widetilde\nu_2') \widetilde f(|\nu_2'|^2 / |\nu_1|^2 \cdot \text{stuff}).$$

This is **not** the form claimed in the conclusion of Theorem 2.5. The bilinear weight cannot be "passed through linearly" in this way. The actual structure of the doubly-Voronoi-transformed sum is much more complex.

**The Theorem as stated is incorrect.** A correct statement would involve a double-Voronoi formula on $\mathbb{Z}[i]^2$, which is non-trivial and requires the Bessel-type kernel for the double sum.

### P7-2 (CRITICAL). Proposition 2.4 (Mellin-Fourier of slice cutoff) has a sign/exponent error.

The proof substitutes $u = r\sin\phi/N$, giving $r = Nu/\sin\phi$ and $dr = (N/\sin\phi) du$. Then $r^{2s-1} = (Nu/\sin\phi)^{2s-1}$, and the integrand becomes
$$(Nu/\sin\phi)^{2s-1} \cdot (N/\sin\phi) = N^{2s} u^{2s-1} (\sin\phi)^{-2s}.$$

The proof writes this as $N^{2s} u^{2s-1} (\sin\phi)^{-2s}$ initially, then rewrites with $(\sin\phi)^{2s-1}$ in the integral $I_k$ — a contradiction. The exponent $-2s$ vs.\ $2s-1$ matters: it changes whether $I_k$ converges at $\phi = 0, \pi$.

### P7-3 (SERIOUS). The integral $I_k(\lambda)$ at $\Re s = 1/2$ has integrability problems at $\phi = 0, \pi$.

For $\Re s = 1/2$, the amplitude $(\sin\phi)^{-2s}$ behaves like $\phi^{-1}$ near $\phi = 0$ — **non-integrable**. The integral $I_k(\lambda)$ does not converge absolutely on the line $\Re s = 1/2$. The contour must be shifted to $\Re s < 1/2$ for convergence, picking up residues. This contour shift is not addressed.

### P7-4 (SERIOUS). Stationary phase Lemma 3.1 asymptotic constants.

The stationary phase formula gives a leading constant proportional to $|f''(\phi_0)|^{-1/2}$, then asserts (after substitution) $|I_k| \asymp \lambda^{1/4}/|k|^{3/4}$. The substitution chain is hand-waved. Verifying:
- $f''(\phi_0) = 2\lambda/\sin^3\phi_0 \cdot \cos\phi_0 = 2\lambda \cot\phi_0/\sin^2\phi_0 = 2|k|\cot\phi_0$ using $\sin^2\phi_0 = \lambda/|k|$.
- So $\sqrt{1/|f''|} = 1/\sqrt{2|k|\cot\phi_0}$, which depends on $\cot\phi_0 = \sqrt{|k|/\lambda - 1}$.
- The amplitude $(\sin\phi_0)^{-2s} = (\lambda/|k|)^{-s}$.

Combining: $|I_k| \sim (\lambda/|k|)^{-s} / \sqrt{|k|\cot\phi_0}$. At $\Re s = 1/2$: $|I_k| \sim |k|^{1/2}/\lambda^{1/2} \cdot 1/\sqrt{|k|\cot\phi_0}$. **This does not match the claimed $\lambda^{1/4}/|k|^{3/4}$.** The stated constant is wrong; recomputation is needed.

### P7-5 (SERIOUS). Proposition 3.2 (Kuznetsov transform bound) is asserted, never proved.

The proof says: "The combined estimate, after stationary-phase analysis of the Bessel kernel against the $\theta$-cosine factor, yields the stated bound; see [BHM, Lemma 4.3] for the analogous calculation over $\mathbb{Q}$."

**This is not a proof.** BHM's lemma is for a different test function in a different setting. The transfer to our setting requires:
(a) Identifying the precise correspondence between BHM's test function and ours.
(b) Verifying that the support and oscillation properties match.
(c) Carrying out the actual stationary-phase calculation for our integral.

None of (a)–(c) is done. This is the central technical step of P7 and it is not even attempted.

### P7-6 (CRITICAL). Theorem 4.1 proof is internally contradictory.

The proof first computes:
- $|\Sigma| \le |\Sigma_{\text{main}}| + \int |E(\theta;N)| d\theta \ll N + N^{1/2+\eta_0+\varepsilon}$,
giving $|\Sigma| \ll N$ — the trivial bound.

Then asserts: "Power saving requires going further. We must show $\Sigma_{\text{main}} \ll N^{1-\delta}$ for generic bilinear weights. ... Carrying out this bookkeeping (analogous to Petrow–Young), we obtain $\Sigma \ll N^{1-\delta+\varepsilon}$ with $\delta = \eta_0/3$."

**The "bookkeeping" is then not done in P7.** It is deferred to P8. So Theorem 4.1 is not actually proved in P7.

### P7-7 (SERIOUS). The Bianchi Whittaker normalization in §3 does not match standard references.

The normalization $W_{it}(n(x)a(y)) = y \cdot K_{2it}(2\pi |x| y) \cdot e(\Re x)$ is asserted but the factor of $2$ in $K_{2it}$ vs. $K_{it}$ is a matter of convention. Different references (Lokvenec-Guleska, Ichino–Templier, Bruggeman–Miatello) use different conventions. **Without fixing a reference convention, the subsequent calculations are ambiguous.**

### P7-8 (NEEDS WORK). Spectral large sieve for Bianchi over $\mathbb{Z}[i]$ — exact statement.

Equation in §4.3: "$\sum_{|t_j| \le T} |S_j(A,A)|/\cosh(\pi t_j) \ll (T + \sqrt X) \|A\|_2^2 X^\varepsilon$."

This is the Bianchi spectral large sieve. The standard form (Lokvenec-Guleska) has the form
$$\sum_{|t_j| \le T} \frac{1}{\cosh \pi t_j} |\sum_\nu a_\nu \rho_j(\nu)|^2 \le (T^3 + N) \sum |a_\nu|^2$$
for $|\nu|^2 \le N$. The cube on $T$ vs. linear in $T$ changes the resulting bound by a factor of $T^2 = N$. **The statement in P7 has the wrong exponent on $T$.**

This is fatal for the bound: with the correct $T^3$ (Bianchi has cubic spectral density, not quadratic, due to $\HH^3$ being 3-dimensional), the spectral large sieve produces a much larger bound and the claimed power saving may vanish entirely.

---

## P8 (`P8-mainterm-bookkeeping.tex`)

### P8-1 (CRITICAL). Lemma 2.3 (self-similarity) is not actually self-similar.

Claim: $W_0 = \widehat\psi(0) \sum_c |c|^{-2} \Sigma^{(|c|^2)}(N; A, \overline B)$.

The slice $\Re(\alpha\beta) = |c|^2$ is a translated/scaled version of $\Re(\alpha\beta) = 1$ only after rescaling $\alpha, \beta$. **But rescaling $\alpha, \beta$ also rescales the support of $A(\alpha), B(\beta)$**, which changes the bilinear sum. The rescaled bilinear sum is NOT $\Sigma^{(|c|^2)}(N; A, \overline B)$ but rather $\Sigma^{(1)}(N/|c|^2; \widetilde A_c, \widetilde B_c)$ for some rescaled $\widetilde A_c, \widetilde B_c$.

**The self-similarity is genuine only after careful rescaling, and the resulting sum is at scale $N/|c|^2$, not $N$.** This invalidates the bootstrap argument: each step works on a smaller-scale problem, and the cumulative error is harder to control than asserted.

### P8-2 (SERIOUS). The bootstrap iteration in Remark 2.5 is hand-waved.

"Define $\delta_0 = 0$ (trivial bound) and $\delta_{k+1} = \delta_k + \eta_0/3$ ... bounded above by $\delta_\infty \le \eta_0/2$."

For this to converge, each iteration must use the bound from the previous iteration *with the same constants*. **The constants in $\Sigma \ll N^{1-\delta_k+\varepsilon}$ implicit in the spectral large sieve and stationary phase depend on $\delta_k$**, and the iteration may not contract.

In fact, the standard Petrow–Young argument is **not** a bootstrap — it is a direct application of the cubic moment / Conrey–Iwaniec identity. There is no iteration. **The bootstrap structure invented in P8 §2.5 is not the Petrow–Young method.**

### P8-3 (SERIOUS). Bound on $W_1$ in §2.7 is asserted by analogy.

"The proof is parallel to the bound on $E(\theta;N)$ in P7 §3 with the test function adjusted by the factor $\min(1, 1/(\pi |\rho|))$, which contributes only a logarithmic loss."

But the factor $\min(1, 1/(\pi |\rho|))$ is **not** smooth: it has a discontinuity at $|\rho| = 1/\pi$, and singular behavior near $|\rho| = 0$ (where it equals $1$). Spectral methods require smooth test functions. The "logarithmic loss" claim is unsubstantiated.

### P8-4 (CRITICAL). Theorem 3.1 conclusion is non-sequitur.

From $|W_0| + |W_1| \ll N^{1-\delta+\varepsilon}$, the proof concludes $|\widehat c_0(1)| \ll N^{-\delta+\varepsilon}$ by "dividing by $N$."

But $\widehat c_0(1) = W_0 + W_1$ as defined, **not** $(W_0 + W_1)/N$. The relation between $\widehat c_0(1)$ and the contribution $\widehat c_0(1) \cdot N$ to $\Sigma$ requires understanding how $\widehat c_0(1)$ is normalized. If $\widehat c_0(1) = W_0 + W_1$ then $\widehat c_0(1) \cdot N \ne W_0 + W_1$ in any obvious way. The "dividing by $N$" step is inconsistent with the definitions.

---

## P9 (`P9-bianchi-whittaker.tex`)

### P9-1 (CRITICAL). The author admits incompleteness in Proposition 3.2.

Direct quote: "After correct accounting (which I do not repeat in full here), the stated bound holds."

This is not a proof. The actual stationary-phase calculation has two computations that don't match (the author's own notes show $N^{1/2}\theta^{-5/4}$ from the calculation vs. $N^{-1/2}\theta^{-3/4}$ from the target, off by a factor of $N \cdot \theta^{-1/2}$). The author hand-waves this away.

### P9-2 (SERIOUS). The Bianchi vs. holomorphic-modular-form transfer is conflated.

P9 §1 asserts the transfer of BHM Lemma 4.3 from $\mathbb{Q}$ to $\mathbb{Q}(i)$ is "structural." But:
- BHM Lemma 4.3 is for HOLOMORPHIC modular forms over $\mathbb{Q}$, with weight $k$.
- Bianchi forms are MAASS forms over $\mathbb{Q}(i)$, with no analog of "weight $k$."
- The Whittaker-function calculations for these are genuinely different.

**The transfer is not structural — it requires actual work.** This is a different setup, not a reformulation.

### P9-3 (SERIOUS). The Whittaker normalization $K_{2it}$ vs. $K_{it}$ is convention-dependent.

P9 asserts $W_{it}(n(x)a(y)) = y K_{2it}(2\pi |x| y) e(\Re x)$ as if it's universal. Different references give different normalizations:
- Lokvenec-Guleska uses one convention.
- Ichino–Templier another.
- Bruggeman–Miatello a third.

The factor of $2$ in $K_{2it}$ is a normalization choice; flipping to $K_{it}$ changes the "spectral parameter doubling" claim throughout. **Without fixing the convention, the calculation is meaningless.**

### P9-4 (SERIOUS). The three-regime stationary phase in §3.2 is incomplete.

For Regime II ($|t| \sim N$), the stationary phase analysis claims $y_0 \sim |t|^2/(\theta N)$. But this requires $|t|^2/(\theta N) \in $ support of $\Phi$, which is $y \asymp N$. So $|t|^2 \asymp \theta N^2$, i.e., $|t| \asymp N\sqrt\theta$. **For $\theta \to 0$, this regime degenerates** — the stationary point goes to $0$, outside the support. The regime analysis fails for small $\theta$.

This affects Theorem 4.1 because the integration over $\theta$ includes $\theta$ near $0$.

### P9-5 (NEEDS WORK). Olver's Bessel asymptotic citation is too coarse.

P9 cites "standard uniform asymptotic of $K_{2it}$, see Olver." But Olver gives several different uniform asymptotics depending on the regime (large $\nu$, large $z$, transition). The specific asymptotic needed for our calculation is not identified.

---

## Summary of severity

| Item | Severity | Description |
|---|---|---|
| XC-1 | CRITICAL | $\ell^2$-to-$\ell^\infty$ transition wrong |
| XC-2 | CRITICAL | Norm-tracking inconsistent throughout |
| XC-3 | SERIOUS | Main-term identification dimensionally wrong |
| XC-4 | SERIOUS | Eisenstein contribution hand-waved |
| XC-5 | SERIOUS | Conductor uniformity glossed |
| P6-1 | CRITICAL | Dispersion is anti-strategic |
| P6-2 | SERIOUS | Spectral expansion asserted, not proved |
| P6-3 | SERIOUS | Spectral basis decomposition for $A,B \in \ell^\infty$ ill-defined |
| P7-1 | CRITICAL | Voronoi for bilinear weights wrong |
| P7-2 | CRITICAL | Mellin-Fourier sign/exponent error |
| P7-3 | SERIOUS | $I_k(\lambda)$ non-convergent at $\Re s = 1/2$ |
| P7-4 | SERIOUS | Stationary phase constants wrong |
| P7-5 | SERIOUS | Proposition 3.2 not actually proved |
| P7-6 | CRITICAL | Theorem 4.1 internally contradictory |
| P7-8 | SERIOUS | Spectral large sieve has wrong $T$ exponent (cubic in $\HH^3$, not quadratic) |
| P8-1 | CRITICAL | Self-similarity claim incorrect |
| P8-2 | SERIOUS | Bootstrap is not the Petrow–Young method |
| P8-3 | SERIOUS | Bound on $W_1$ asserted by false analogy |
| P8-4 | CRITICAL | Theorem 3.1 dimensional non-sequitur |
| P9-1 | CRITICAL | Author admits incompleteness; calculations don't match |
| P9-2 | SERIOUS | Holomorphic-vs-Maass transfer conflated |
| P9-3 | SERIOUS | Whittaker normalization unfixed |
| P9-4 | SERIOUS | Regime analysis fails for small $\theta$ |

**Critical errors: 9.** **Serious errors: 12.** **Needs-work: 5.**

## Honest verdict from this referee

P6–P9 contain a **plausible-looking outline** for a Bianchi-spectral attack on Landau IV, but the outline has **multiple critical errors** that would each independently kill the proof. The most damaging are:

1. **XC-1 / P7-8**: the $\ell^2$ vs. $\ell^\infty$ mismatch combined with the cubic spectral density of Bianchi forms (vs. quadratic for $\mathrm{SL}_2/\Q$) suggests the entire spectral approach gives bounds in the *wrong* direction.

2. **P7-1**: the bilinear-weighted Voronoi as stated is wrong; the correct double-Voronoi is much harder.

3. **P8-1, P8-4**: the Petrow–Young analog in P8 mis-identifies the self-similarity structure.

4. **P9-1**: the central technical step (stationary phase for the Bianchi Whittaker transform) is admittedly incomplete and the author's own arithmetic doesn't match.

In the honest assessment of this skeptical referee:

> P6–P9 should not be cited as "an attack on Landau IV" or even as "a conditional reduction of Landau IV to subconvexity." They are a sketch of how such a reduction *might* go, with serious unresolved technical issues at multiple points. To turn this into a real conditional theorem, all 9 critical issues would need to be addressed, and that may require fundamentally different techniques than those sketched.

The Shakov-bijection entry point (P6 Lemma 1.1) is correct. Everything after it requires substantial repair before it constitutes a real argument.

## Constructive comments

If one wanted to actually attempt this program, the right starting moves would be:

1. **Fix the norm convention** at the start: decide whether you are bounding $\Sigma$ for $\ell^2$ or $\ell^\infty$ inputs, and stick to it. The Friedlander–Iwaniec asymptotic sieve actually uses *Type II* axioms in $\ell^2$ form (Bombieri–Vinogradov-style), so $\ell^2$ may be the right choice — but then check that the $\ell^2$ bilinear bound suffices for FI.

2. **Use the correct Bianchi spectral large sieve** (Lokvenec-Guleska's actual statement), which has cubic density in $T$.

3. **Eisenstein contribution** must be evaluated, not hand-waved. The standard reference is Bykovsky 1996 or Templier 2011.

4. **Bilinear-weighted Voronoi** requires a double-Voronoi formula, which has been studied in the $\mathrm{GL}_3$ setting (Miller–Schmid) but may not have a clean analog for our setup. Alternative: avoid Voronoi entirely and use Linnik dispersion plus Kloosterman sum bounds (Weil) directly.

5. **Petrow–Young** is a specific structural identity (cubic moment of $L$-functions), not a bootstrap. To use it over $\mathbb{Q}(i)$, one needs the analog cubic moment formula for Hecke–Maass forms over $\mathbb{Q}(i)$ — this is a major project that has not been done.

These are the realistic items to fix before claiming a theorem.
