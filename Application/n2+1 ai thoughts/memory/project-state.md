---
name: mathAI project state — Shakov paper analysis
description: Status of the wiki-linked notes graph and research synthesis I built around Shakov's main.tex on SL₂(ℕ₀)-enumerable polynomials and Landau's 4th problem
type: project
originSessionId: 8cf0884f-055b-4942-b476-e31741aac3d6
---
The user (Anton, who IS Anton Shakov, the paper's author) has me reading his Feb 2024 paper on polynomials in ℤ[x] whose divisors are enumerated by the free monoid SL₂(ℕ₀), and trying to push it toward Landau's 4th problem (∞ many primes of form n²+1).

## What I built (lives at C:\Users\anton\OneDrive\Desktop\mathAI\notes\)

- `index.md` — top-level wiki hub
- `concepts/00-18.md` — 19 files covering the paper's internal machinery
- `research/R1-R8.md` — literature review on sieves, parity, FI, BQFs, thin groups, Zaremba/Apollonian, k-regular asymptotics, automatic sequences and primes
- `bridges/B1-B7.md` — synthesis documents connecting Shakov to conventional approaches

## Key technical findings to remember

1. **The four enumerable polynomials are exactly the four smallest-discriminant fundamental quadratic orders with class number 1**: φ₀=n²+1 (disc -4, ℤ[i]), φ₁=n²+n+1 (disc -3, ℤ[ζ₃]), ψ₂=n²+2n-1 (disc 8, ℤ[√2]), φ₃=n²+3n+1 (disc 5, ℤ[(1+√5)/2]). Confirmed structurally by R4 agent (binary-quadratic-forms research).

2. **The bilinear cross-term χ(A) = ac+bd** is the highest-impact opening. It supplies the missing second variable for Friedlander–Iwaniec-style parity breaking that doesn't exist in the original n²+1 formulation. R3 agent's bridge section made this explicit.

3. **δ = 1 boundary obstruction**: SL₂(ℕ₀)'s limit set is the full positive real boundary, the worst-case regime for Bourgain–Kontorovich/affine-sieve transfer-operator techniques. R5 agent flagged this.

4. **Rickards 2024 (Duke 2025), arXiv:2401.01860** is the closest published structural neighbor — semigroups in SL₂(ℤ) on continued fractions with reciprocity obstructions on which integers appear.

5. **Shakov has a follow-up paper**: arXiv:2510.22805 (2025) on the τ(n²+1) 2-regular sequence (OEIS A383066). Not yet read.

6. **The S-sequence has triple eigenvalue 1 in its SL₃(ℤ) generators**, giving Jordan-block-induced polylogarithmic growth S(k) = O((log k)²) — unusual regime that may admit Mauduit–Rivat methods after technical adaptation.

7. **Mauduit–Rivat-style equidistribution for S(p) would NOT resolve Landau** — codomain-sieving (fiber cardinality) ≠ value distribution. R8 agent's negative observation.

## How to apply this in future conversations

- The notes graph at `notes/` is the canonical record; index.md is the entry point.
- B7-research-integration.md is the most "current" and important bridge — it integrates all four research findings.
- B6-open-questions.md has 13 concrete sub-problems ranked by tractability.
- For new technical work, start by checking which sub-question (Q1-Q13) it touches.

The user values unconventional approaches — feedback memory note: he's chasing Landau's 4th specifically and explicitly via the SL₂(ℕ₀) framework. The paper is elementary on the surface, deep underneath. I should not retreat to conventional sieve answers when he asks about pushing forward; the whole point is finding new structural angles.
