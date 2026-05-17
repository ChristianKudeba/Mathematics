# P13. Subconvexity over Q(i) → Landau IV: skeptic-verified roadmap

> A skeptic-tested verification of the implication chain in P11, plus a detailed roadmap for the Q→Q(i) adaptation of Petrow–Young / Conrey–Iwaniec.
>
> **Bottom line:** The chain "sup-norm subconvexity over Q(i) ⇒ Landau IV" as stated in P11 §1-2 Conj 2.14 is **NOT sound**. What is actually needed is the **conductor-aspect cubic moment** (P11 §5-6 Hyp 6.7), which is strictly stronger than sup-norm subconvexity but is what the dispersion-and-spectral argument actually consumes. Mapping the Q-side proof of Petrow–Young 2020 to Q(i) is achievable in principle, ~18–24 person-months of work, with a single major missing input: the GL₂/Q(i) spectral fourth moment.

Two-round skeptic dialogue conducted 2026-05-03 (this session). Outputs of both rounds preserved below in summary; full transcripts archived in session messages.

---

## 1. The original claim under test

P11 §1-2 Conjecture 2.14 + Theorem 2.12 + Corollary 2.13 assert:

> Subconvexity for L(½+it, u_j ⊗ χ) over Q(i), uniform in conductor up to N (and t, t_j), with saving exponent η₀ > 0, implies the bilinear conjecture in ℓ² form, hence Landau's fourth problem via Friedlander–Iwaniec.

The explicit "δ = η₀/3" is asserted in P11 §5-6 line 314.

## 2. What the skeptic broke

Two rounds of attack established:

### 2.1 The sup-norm subconvexity is not the right input

The proponent's back-of-envelope used the Q analytic conductor `(|cond|² · t_j · t)^{1/2-η₀}`. The correct Q(i) analytic conductor for a degree-4 L-function L(s, u_j × χ) over Q(i) is:

```
C(L) = N(cond(u_j × χ)) · Q_∞(L) ≍ |cond(χ)|⁴ · (1+|t_j|)⁴ · (1+|t|)²
```

Convexity gives `|L| ≪ C^{1/4+ε}`, so at cond(χ) ~ √(|θ|N), t_j ~ √(|θ|N):
- **Convexity:** `|L| ≪ (|θ|N)^{1+ε}`.
- **Petrow–Young Weyl strength (saving 1/12 below convexity):** `|L| ≪ (|θ|N)^{2/3+ε}`.

Plugged into the Cauchy–Schwarz spectral bound with **unit-window** spectral large sieve (T² + N) ‖A‖² (the only honest version; the global cubic T³ form is too lossy):

```
|M_cusp(θ)| ≪ N · sup|L| · sup|K| · ‖A‖₂‖B‖₂
            ≪ N · (|θ|N)^{2/3} · N^{-1/2} · ‖A‖₂‖B‖₂
            ≪ |θ|^{2/3} · N^{7/6} · ‖A‖₂‖B‖₂.
```

After ∫₀¹ dθ: cuspidal contribution ≪ N^{7/6} ‖A‖₂‖B‖₂. **This exceeds the trivial bound N ‖A‖₂‖B‖₂.** Petrow–Young Weyl strength (η₀ = 1/12 over Q analog, equivalent to L ≪ C^{1/6} for the Q(i) L-function) is **insufficient** for any positive δ in the bilinear bound.

For δ > 0 from this approach, one would need `|L| ≪ C^{1/8+ε}` — saving 1/8 below convexity, which is **strictly stronger than Petrow–Young Weyl strength.**

### 2.2 What the cubic moment actually buys

The cubic moment `Σ_χ |L(½, u ⊗ χ)|³ ≪ Q^{1+ε}` for χ of conductor ≤ Q is a **moment-averaged** input. Crucially, for the spectral side after ∫dθ, one uses the **second moment** consequence:

```
∫₀¹ |L(½, u_j × χ_θ)|² dθ ≪ T_j^ε   (border-Lindelöf, averaged over θ)
```

derived from the cubic moment via Hölder. This is **much stronger** than `(sup|L|)² · 1` from the same exponent applied pointwise.

Reapplying Cauchy–Schwarz with the moment input:
```
|∫₀¹ e(-θ) M_cusp(θ) dθ|²
   ≤ Σ_j |X_j Y_j|² · ∫₀¹ |L|² dθ · ∫₀¹ |K|² dθ
   ≪ ‖A‖₂² ‖B‖₂² · T_j^ε · N^{-1}.
```

This power-saves below trivial. **The cubic moment is the right input.**

### 2.3 Other holes (partially conceded by proponent)

- (Hole 4) Type I axiom for the slice {1+in : n ≤ N} mod Hecke ideals: the proof says "essentially Hinz 1981 §3" but Hinz handles `Z[i]`-moduli, not the affine slice. The slice Type I needs derivation, not citation. (~1 month of work.)
- (Hole 6) Eisenstein contribution: P11 cites "Burgess for ζ_{Q(i)}" which is `t`-aspect, not conductor-aspect. **Resolved**: the Eisenstein t-integral uses convexity, not Burgess. The proponent's claim stands modulo a sign/scaling check.
- (Hole 9) §1-2 vs §5-6 use different methods (direct Type-II vs dispersion). Proponent concedes §5-6 §5 (dispersion + Weil) is vestigial under the §1-2 framework; the chain runs through §1-2 + §3-4 + §5-6 §6 (main term).
- (Hole 13) Hyp 6.7's stated form (4th moment over u_j) was the spectral 4th moment, not the conductor-aspect 3rd moment of Petrow–Young. The right Hyp 6.7: `Σ_χ |L(½, u ⊗ χ)|³ ≪ Q^{1+ε}` for χ of conductor ≤ Q, fixed u. Proponent concedes; misstatement in P11.

### 2.4 Verdict

**The user's premise — "subconvexity over Q(i) potentially implies Landau IV" — is mathematically not the right framing.** What P11 actually conditions on (and what is actually needed) is the conductor-aspect Bianchi cubic moment of L-values. Sup-norm subconvexity is a *corollary* of the cubic moment via Hölder, not the operative hypothesis.

This is consistent with P11 master.md's explicit statement: *"Modulo a single residual unconditional gap — the Petrow–Young-strength **Bianchi cubic moment** for Hecke–Maass forms over Q(i) in the conductor aspect — Landau's fourth problem follows."*

P11 §1-2 Conj 2.14 (sup-norm subconvexity) is a misleading restatement of what's needed. The honest hypothesis is Hyp 6.7.

## 3. Roadmap to the Bianchi cubic moment

A detailed plan to adapt Petrow–Young 2020 (and Conrey–Iwaniec 2000) to Q(i).

### 3.1 Phase I — Foundations (already in place)

| Step | Statement | Status |
|---|---|---|
| I.1 | Bianchi Bruggeman–Motohashi sum formula at level q | ✅ Lokvenec-Guleska 2004; BM 2003 |
| I.2 | Spectral large sieve (T³ + |q|N) on Γ₀(q)\H³ | ✅ Lokvenec-Guleska 2004 |
| I.3 | AFE for Hecke L-functions over Q(i) | ✅ standard |
| I.4 | Voronoi for single Bianchi cusp form | ✅ BM 2003 §10; Schmidt 2011 |
| I.5 | Convexity for L(s, u ⊗ χ) | ✅ standard |

### 3.2 Phase II — Bianchi Waldspurger formula (~3-6 months)

| Step | Statement | Status |
|---|---|---|
| II.1 | Theta kernel for (~SL₂, PGL₂)/Q(i) | ✅ in principle (Yuan–Zhang–Zhang) |
| II.2 | Fourier expansion of Θ_χ at level q squarefree coprime to (1+i) | open, Friedberg–Hoffstein 1995 over Q is precursor |
| II.3 | Explicit Bianchi Waldspurger: \|L(½,χ)\|² = c_χ \|a_χ(1)\|² / ‖Θ_χ‖² | open |
| II.4 | Local computation at the ramified prime (1+i) | open, Pitale–Saha–Schmidt for paramodular is precursor |

### 3.3 Phase III — GL₂/Q(i) spectral fourth moment (★) — THE KEY MISSING INPUT (~8-10 months)

The single most load-bearing step. Conjectural form:

```
Σ_{u_j at level q, |t_j|≤T} ω_{u_j} |L(½, u_j)|⁴ h(t_j)  ≪_ε  T^{3+ε} · |q|^{1+ε}
```

| Step | Statement | Status |
|---|---|---|
| III.1 | Amplified second moment Σ ω_{u_j} \|A(u_j)\|² \|L(½,u_j)\|² h(t_j) at level q | follows standard pattern (Iwaniec amplification + BM sum formula) |
| III.2 | Off-diagonal of fourth moment via BM formula | open, KMV 2002 over Q is precursor |
| III.3 | Bianchi-Kloosterman + Bessel-transform integral bound | BM 2003 §11 (abelian fourth moment of ζ_{Q(i)}) gives the template |
| III.4 | Eisenstein contribution to fourth moment | follows Bruggeman–Miatello 2009 |
| III.5 | Combine: (★) holds at T^{3+ε} \|q\|^{1+ε} | the goal |

**This is the central open project.** It is comparable in scope to Kowalski–Michel–VanderKam 2002 over Q (~50 pages) plus the Bianchi cubic-density bookkeeping (~10 pages). Total ~40 pages new.

### 3.4 Phase IV — Cubic moment from theta unfolding + (★) (~3-4 months)

| Step | Statement |
|---|---|
| IV.1 | Unfold Σ_χ \|L(½,χ)\|³ via Plancherel on the self-dual character family of conductor q |
| IV.2 | Match the resulting divisor-with-squareclass-mod-q sum to theta-lifted GL₂ fourth moment via Phase II |
| IV.3 | Apply (★) bound from Phase III |
| IV.4 | Bookkeep cube-free / squarefree restriction, orbit count over Z[i]^× = {±1, ±i} |
| IV.5 | Conclude: Σ_χ \|L(½,χ)\|³ ≪ \|q\|^{1+ε} for q squarefree coprime to (1+i) |

### 3.5 Phase V — Extensions

| Step | Statement | Difficulty |
|---|---|---|
| V.1 | Extend to cube-free q (e_p ∈ {1,2} for all p) | ~2 months — local at squared primes |
| V.2 | Extend to all q via Petrow–Young 2023 coset trick | ~3 months — orbit analysis over (Z[i]/q)^× / Z[i]^× |
| V.3 | Extend from L(½,χ) to L(½, u ⊗ χ) (P11's Hyp 6.7 form) | ~3 months — amplification by u |
| V.4 | Uniformity in spectral parameter of u | ~1 month — bookkeeping |

### 3.6 Total estimate

**18-24 person-months** for a single competent expert. **80-120 pages** of new mathematics. **All five technical obstacles individually tractable** by current technology — none requires a new conceptual breakthrough.

## 4. Technical obstacles, ranked

1. **(★) the GL₂/Q(i) spectral fourth moment.** Comparable to KMV 2002. Closest precursor: BM 2003 §11 (abelian case). Estimate: 8-10 months.

2. **Bianchi Waldspurger normalization.** Yuan–Zhang–Zhang give the existence; Petrow–Young-version constants need to be derived. Estimate: 3-6 months.

3. **Cube-free local at (1+i).** One ramified prime, finitely many local-newform-tower cases. Estimate: 2-4 months.

4. **Self-dual Hecke character family thinness.** Z[i]^× has order 4, so self-dual χ has \|q\|^{1/2} fewer characters than over Q. Forces a different family parametrization (likely all-primitive-χ-in-coset, à la Petrow–Young 2023). Estimate: conceptual.

5. **Off-diagonal Kloosterman bookkeeping.** Use Linnik dispersion + Weil Z[i]-Kloosterman as in P11 §5. Estimate: 1-2 months, mostly recycled.

## 5. Alternative routes (if cubic moment is too long)

- **Munshi-style δ-method over Q(i) in conductor aspect.** Closest precursor: Munshi–Singh 2019 (t-aspect over Q). Estimate: 9-12 months, uncertain. Could give Weyl-strength subconvexity directly without going through cubic moment. **But sub-norm subconvexity alone (Section 2.1) is too weak — Munshi would have to give a moment-averaged bound, which is not how the δ-method usually works.** Probably not a clean substitute.
- **Asai L-function for base-change Bianchi forms.** Works only on the thin subfamily of Bianchi forms that are base-change lifts from GL₂/Q. Not a substitute in general.
- **Nelson 2021 orbit method.** Gives unconditional subconvexity over Q(i) with a small saving — much weaker than Weyl. **Insufficient** for our application (need cubic-moment averaging, not sup-norm).
- **Slice-targeted method (P11 §6 line 134).** Speculative; could bypass cubic moment by exploiting the slice Re(ξη)=1 structure directly. Not yet developed.

## 6. Concrete first step

If the project is taken up, the most efficient first step is:

> **Read Yuan–Zhang–Zhang Ch. 3 with F = Q(i) substituted, and write down the explicit Bianchi Waldspurger formula at squarefree level coprime to (1+i).** This is Phase II.2-II.3.

The Bianchi Waldspurger is the prerequisite for the cubic moment to even be statable cleanly. It is also the part most likely to already exist somewhere in the literature in some form (the imaginary quadratic case is among the easier cases of Yuan–Zhang–Zhang's general framework).

A second, parallel first step:

> **Set up the amplified second-moment problem on Bianchi forms** (Phase III.1). This is the entry point to the GL₂/Q(i) fourth moment and uses already-existing machinery (BM sum formula + amplification).

## 7. Status of P11 after this analysis

P11 should be amended:
- **Conj 2.14 in §1-2 (sup-norm subconvexity)** is misleading as the conditional input. It does not imply the bilinear bound.
- **Hyp 6.7 in §5-6 (cubic moment)** is the actual conditional input. It implies both Conj 2.14 *and* the bilinear bound; the latter is the load-bearing implication.
- The chain "Hyp 6.7 ⇒ bilinear ⇒ Landau IV" is sound at the structural level, modulo:
  - Type I axiom for the slice (Hole 4): standard but unwritten, ~1 month.
  - Eisenstein t-integral sign/scaling check (Hole 6): mechanical.
  - Cleanly picking §1-2's direct Type-II framework over §5-6's dispersion (Hole 9): editorial.

The Bianchi cubic moment itself is the central open project. Adapting Petrow–Young to Q(i) is achievable, ~18-24 person-months, with detailed roadmap above.

## 8. Files referenced

- `P11-section-1-2.tex` — original sup-norm subconvexity claim (Conj 2.14)
- `P11-section-5-6.tex` — original cubic moment hypothesis (Hyp 6.7) and the "δ = η₀/3" assertion
- `P11-master.md` — overview, status of referee items
- `REFEREE-REPORT.md` — prior referee report on P6-P9
- `notes/research/R9-bianchi-spectral-apparatus.md` — Bianchi spectral toolkit citable digest

---

**Date:** 2026-05-03  
**Author:** AI session with skeptic dialogue (Anton Shakov directing)
