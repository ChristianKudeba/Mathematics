# Round 1 — Skeptic's report

The author's draft P12 (the version before round 1 had: σ-character framing for parts of the writeup, Theorem C as an unconditional claim, full Plancherel completeness conjecture, pre-fix Theorem B). The skeptic was instructed to find errors and rank them.

## Verdict

The skeptic found **one CRITICAL issue (Theorem C overclaim), two SERIOUS issues (Theorem B off-by-one; Plancherel program hand-waving), and several MINOR issues**. Theorem A was deemed correct.

## Skeptic's full report (verbatim)

> Empirical evidence supports the small constant. Now I have enough to write the report.
>
> # Referee Report on P12-pointwise-spin-identity.md
>
> ## Theorem A — Proof is CORRECT
>
> **Verified computationally:** zero counterexamples among all matrices with entries in [0,15) (a few thousand cases). The algebraic identity (a-b)(c+d) - (n+1) = -2bd holds identically for all (a,b,c,d) with ad-bc=1 — verified symbolically over a range and re-derived by hand.
>
> The case analysis IS exhaustive: ad-bc=1 forces exactly one of {ad, bc} to be odd (an integer congruence fact), so Cases A and B cover everything. Step 4 invokes multiplicativity of χ₄ on odd arguments, which is fine since χ₄ is a Dirichlet character mod 4 and both factors are odd in the ρ ≠ 0 cases. The "mod 4" closing step is rigorous: 2bd ≡ 0 mod 4 because b or d is even (depending on case), so a-b)(c+d) ≡ n+1 mod 4 with both odd, and χ₄ depends only on residue mod 4.
>
> **Theorem A is solid.**
>
> ---
>
> ## Issue 1 — SERIOUS — Off-by-one in Theorem B (n=0 case)
>
> The LHS of Theorem B is defined as `T(N) = Σ_{A: χ(A) ≤ N} ρ(A)`. This includes the identity matrix A = I, for which χ(I) = ac+bd = 0. The RHS sums n=1..N and misses n=0.
>
> **Verified computationally:** for N=20, LHS = 1, RHS = 0. The discrepancy is exactly τ(0²+1)·χ₄(1) = 1·1 = 1, contributed by I.
>
> **Fix:** either change LHS to `χ(A) ≥ 1` (i.e., exclude I), or change RHS sum to start at n=0. This is a constant additive offset, doesn't affect the O(√N) claim, but the stated equation is literally false as written.
>
> Also: the proof says "the set {A: χ(A) = n} is in bijection with the divisor pairs (m,n), m | n²+1. There are τ(n²+1) such pairs." For n ≥ 1 this is correct via Shakov's F̂. For n=0, n²+1 = 1, τ(1) = 1, and the unique matrix is I — also fine, but it must be acknowledged.
>
> ---
>
> ## Issue 2 — CRITICAL — Theorem C is overclaimed; "Hooley-style methods" sketch is wrong
>
> The author claims `T(N) = O(N^{1/2+ε})` is "provably unconditional" via "Hooley-style methods (citation: Iwaniec–Kowalski Ch. 14)." This is **not honest**.
>
> **(a) The PV/Burgess sketch in §C is incorrect.** The author writes:
> > Σ_{n ≤ M, n ≡ n₀ mod d} χ₄(n+1) = O(d^{1/2+ε} M^ε)
>
> This conflates moduli. χ₄ has conductor 4, NOT d. The AP n ≡ n₀ mod d intersects each residue class mod 4 (when gcd(d,4)=1) with density 1/4, and the AP-sum of χ₄ over a length-M window equals (M/d)·(sum of χ₄ over a complete period mod 4) + O(1) = O(1). So the inner sum is **O(1)**, not "square-root in d." The author's stated bound `O(d^{1/2+ε} M^ε)` is meaningless dimensionally — there's no character mod d to apply Pólya–Vinogradov to.
>
> **(b) The trivial bound is O(N log N).** Using inner-sum O(1) and summing over Landau-d ≤ N (density ~ N/√(log N)) recovers exactly the trivial bound, as the author himself notes. He then waves at "square-root cancellation in the AP sums" without delivering one.
>
> **(c) The Hooley reference is dubious.** Hooley (1957/63) studied Σ_{n ≤ N} τ(n²+1) ~ cN log N (no twist). Adding a Dirichlet twist χ(n+1) does not automatically inherit a √N saving from Hooley's method. The relevant theory is Deshouillers–Iwaniec / Heath-Brown on shifted-convolution sums and divisor function in APs, which gives **power saving** but typically of the form O(N^{1-δ}) for some small δ, not O(N^{1/2+ε}). I am not aware of an unconditional O(N^{1/2+ε}) result for Σ τ(n²+1) χ(n+1) in Iwaniec–Kowalski Ch. 14 (which covers automorphic L-functions and subconvexity, not this specific sum).
>
> **(d) Mixed signals in the note itself.** The Theorem C statement says "assuming GRH ... and standard subconvexity." But §"What's actually proved" then says the bound is "**provable unconditionally** by Hooley-style methods." These contradict each other within the same document.
>
> **Verdict:** Theorem C is at best conjectural, possibly conditional on GRH + subconvexity, and the unconditional sketch is not a proof. The author should retract the unconditional claim.
>
> ---
>
> ## Issue 3 — MINOR — Empirical evidence for Theorem C is suggestive but incomplete
>
> I verified at smaller scale: N=1000 gives |T|/√N ≈ 0.506; N=10000 gives ≈ 0.060. Consistent with O(√N) and a small constant. But two data points don't distinguish O(√N) from O(N^{1/2+ε}) or even O(N^{0.6}) — the user's claim of having checked up to 10^7 is plausible but I haven't re-verified.
>
> Also: the author says "cancellation comes from χ₄(n+1) averaging over even n." But χ₄(n+1) is nonzero precisely when n is even, and on even n the average is essentially 1/2·(+1) + 1/2·(-1) = 0 over residues n ≡ 0, 2 mod 4 corresponding to χ₄(n+1) = 1, -1. This is correct framing, but the cancellation is only of the χ₄ factor; whether it survives multiplication by the spiky τ(n²+1) is exactly the hard question being punted.
>
> ---
>
> ## Issue 4 — SERIOUS — The Plancherel program is hand-waving
>
> §"What this gives toward Landau IV" claims:
> > for a generic Plancherel input (χ_q, χ_{q'}) ... the cumulative bilinear sum factors through a twisted divisor sum analogous to T(N), with cancellation O(N^{1-δ}).
>
> But the proof of Theorem A used **specific** features:
> 1. The linear functionals L₁(a,b) = a-b and L₂(c,d) = c+d were chosen so that L₁(a,b)·L₂(c,d) - (n+1) = -2bd is divisible by 2 thanks to the determinant constraint.
> 2. χ₄ has conductor 4 = 2², so divisibility-by-2 of the defect bd lifted to mod-4 equality after the ×2.
>
> For another linear pair (αa + βb, γc + δd), expansion gives (αa+βb)(γc+δd) = αγ·ac + αδ·ad + βγ·bc + βδ·bd, which equals αγ·n + αγ·bd + αδ·ad + βγ·bc + βδ·bd minus αγ·bd. With ad = 1+bc, this becomes a mess and won't generally equal n + (small mod q²) without a lucky algebraic alignment. **The author has produced one identity, then conjectured a whole family without exhibiting a second example.** Q12.2 acknowledges this but the Plancherel claim in the body section is stronger than the open question warrants.
>
> **Concrete demand:** the author should at minimum write down the constraint on (α,β,γ,δ; q,q') such that the analogue of Theorem A holds — and try the listed candidates χ₄(a+b)χ₄(c-d), χ_q(a)χ_q(c) — before claiming "Plancherel completeness" is plausible.
>
> ---
>
> ## Issue 5 — MINOR — Honesty disclaimer is mostly honest
>
> The author correctly retracts the σ multiplicative-Hecke-character claim and explicitly states ρ is NOT multiplicative on Z[i]. I scanned the rest of the document for residual multiplicativity assumptions. Step 4 of Theorem A's proof uses χ₄((a-b)(c+d)) = χ₄(a-b)χ₄(c+d) — this is multiplicativity of χ₄ on Z, not on Z[i], and is fine. **No hidden multiplicativity claim is found.** The disclaimer is honest.
>
> However: §15 says "the multiplicative path actually fails ... the non-multiplicative ρ succeeds because its non-multiplicativity defect is killed by the SL₂ determinant constraint." This is a nice intuition but the author should note that the "defect being killed" is exactly the -2bd identity, which works only because the conductor of χ₄ is 4 and the defect is divisible by 2. Different conductors will have different defect-divisibility requirements — this is the same point as Issue 4.
>
> ---
>
> ## Issue 6 — MINOR — Definitional/exposition issues
>
> (a) The definition `χ(A) = ac+bd` is used both as a notation (a single function) and conflicts notationally with χ₄ and "χ" in "χ⊗θ." The author should rename to avoid χ overload — e.g., `n(A)` or `μ(A)`.
>
> (b) §C invokes "the binary theta of x²+y²" and `L(s, χ ⊗ θ)` without defining either object precisely. This is a sketch, fine, but should be flagged as such.
>
> (c) The "diagonal term δ_□" in the hyperbola decomposition is dismissed as "rare." Strictly, n²+1 is a perfect square only when n=0 (since n²+1 = m² implies (m-n)(m+n)=1), so δ_□ contributes only at n=0 and is genuinely O(1). Worth stating.
>
> (d) The Shakov bijection F̂_{φ₀} is invoked in Theorem B without restating the map. A one-line reminder (m, n) ↔ A would help.
>
> ---
>
> ## Summary
>
> - **Theorem A: solid.** Proof is correct; case analysis exhaustive; identity verified.
> - **Theorem B: nearly correct, off-by-one for n=0.** Easy fix.
> - **Theorem C: overclaimed.** The "unconditional Hooley-style proof" is not a proof; the inner-AP-sum step is dimensionally wrong; the IK Ch. 14 citation appears to be a bluff. The conditional statement (GRH + subconvexity) might be defensible but isn't proved either.
> - **Plancherel program: speculative.** No second example, no characterization of (L₁, L₂, q, q') compatible with the determinant trick.
> - **Honesty disclaimer: honest.** No residual multiplicativity assumption found.
>
> The note's correct contribution — a clean pointwise determinant-driven character identity on SL₂(ℕ₀) — is real and worth keeping. The overclaim is in §C and the Plancherel pitch.
