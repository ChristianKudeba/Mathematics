---
name: P13 — subconvexity over Q(i) chain verified (with critical correction)
description: 2026-05-03 skeptic dialogue verified P11's "subconvexity ⇒ Landau IV" chain. Finding — sup-norm subconvexity (Conj 2.14) is INSUFFICIENT; cubic moment (Hyp 6.7) is what's actually needed. Q→Q(i) adaptation roadmap written as P13.md.
type: project
originSessionId: e6fc4493-b0d6-45fc-a5f6-686d6e102daa
---
May 2026: User asked to verify the implication chain in P11 ("subconvexity over Q(i) implies Landau IV") and adapt the Q-side proof of Petrow-Young to give Q(i) subconvexity.

## Key finding (skeptic-confirmed)

**The chain "Conj 2.14 (sup-norm subconvexity over Q(i)) ⇒ Theorem 2.12 ⇒ Landau IV" is NOT sound.** The cubic spectral density T³ on H³ combined with the Q(i) analytic conductor (degree 4 over Q) means:
- Petrow-Young Weyl-strength subconvexity (saving 1/12 below convexity) is **insufficient** — gives cuspidal contribution N^{7/6}, exceeds trivial.
- Need saving > 1/8 below convexity, strictly stronger than Weyl-strength sup-norm.
- The cubic moment (Hyp 6.7 in P11 §5-6) is the actual operative hypothesis. It gives an averaged second moment ∫|L|²dθ ≪ T^ε which IS sufficient.

**P11 §1-2 Conj 2.14 is misleadingly stated** — sup-norm subconvexity is a corollary of Hyp 6.7 via Hölder, not the load-bearing input.

## Roadmap to prove Bianchi cubic moment

Written up as `n2+1 ai thoughts/notes/proofs/P13-subconvexity-skeptic-roadmap.md`. Five phases:
- Phase I: foundations (all known: BM sum formula, T³ large sieve, AFE, Voronoi).
- Phase II: Bianchi Waldspurger formula (~3-6 months; Yuan-Zhang-Zhang precursor).
- Phase III: **GL₂/Q(i) spectral fourth moment** — the central missing input, ~8-10 months, comparable to Kowalski-Michel-VanderKam 2002.
- Phase IV: cubic moment from theta unfolding + (★) (~3-4 months).
- Phase V: extensions to all q (~6 months).

**Total: 18-24 person-months, 80-120 pages, achievable in principle, not yet written.**

## How to apply

If user asks about pushing P11 forward, the SINGLE most useful next step is:
1. Read Yuan-Zhang-Zhang Ch. 3 with F = Q(i) and write down the explicit Bianchi Waldspurger.
2. Set up the amplified second moment of L(½, u_j) at level q on Bianchi forms (entry to Phase III).

The off-the-shelf "subconvexity from Michel-Venkatesh 2010" approach gives subconvexity over Q(i) but with too-small saving — does NOT suffice for the bilinear bound. Need cubic moment for the moment-averaged input.

## Open questions raised by the analysis

- Is (★) (GL_2/Q(i) spectral 4th moment) in unpublished form somewhere? Check Frolenkov, Balkanova, Bruggeman/Motohashi students post-2003.
- The self-dual Hecke character family over Q(i) is thin (cardinality ~ 2^{ω(q)} vs |q| over Q). Need to handle either by sum-over-all-primitive-χ-in-coset (Petrow-Young 2023 trick) or by a different family.
- Could Munshi-δ-method over Q(i) bypass the cubic moment? Probably not — sup-norm subconvexity isn't enough; would need a moment-form δ-method.
