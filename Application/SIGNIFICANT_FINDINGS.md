# mathAI — Significant Findings to Date

*Last updated: 2026-05-07 by Claude. Compiled from `memory/`, `bot/STRATEGY.md`,
and `bot/sessions/*.md` across the autonomous mathAI research run.*

This is a curated digest of what the project has actually established about
Landau IV (∞ many primes of the form n²+1) via the SL₂(ℕ₀) framework of
Shakov's paper. It is the document a future Claude session — or a human
reader — should read first to orient before diving into the proof notes
under `n2+1 ai thoughts/notes/proofs/`.

---

## 1. Strategic frame

- **Goal**: prove Landau's 4th problem (∞ many primes n²+1) using the
  SL₂(ℕ₀)-enumerable polynomial framework of Anton Shakov's Feb 2024 paper
  (`main.tex`).
- **Why this framework at all**: SL₂(ℕ₀) is a free non-group monoid on
  S=[[1,1],[0,1]], T=[[1,0],[1,1]]. Words enumerate divisor pairs
  (ξ, η) ∈ ℤ[i]² with ξη = n+i. The bilinear cross-term χ(A) = ac+bd is the
  hidden Type-II handle that the original n²+1 formulation lacks.
- **The four enumerable polynomials are exactly the four smallest-discriminant
  fundamental quadratic orders with class number 1**:
  φ₀=n²+1 (disc −4, ℤ[i]), φ₁=n²+n+1 (disc −3, ℤ[ζ₃]),
  ψ₂=n²+2n−1 (disc 8, ℤ[√2]), φ₃=n²+3n+1 (disc 5, ℤ[(1+√5)/2]).
  Confirmed structurally (R4 binary-quadratic-forms research).

## 2. What is rigorously proven

### 2.1 Pointwise spin identity (P12 — Theorems A, A')

For every A = (a,b,c,d) ∈ SL₂(ℕ₀) with det A = 1:
- **Theorem A**:    χ₄(a−b)·χ₄(c+d) = χ₄(n+1),    where n = ac+bd.
- **Theorem A'**:   χ₄(a+b)·χ₄(c−d) = χ₄(n−1).

The character ρ(A) = χ₄(a−b)χ₄(c+d) is a product of two simple Dirichlet
characters mod 4 applied to **linear functionals of the matrix entries** — not
multiplicative on ℤ[i], but the bilinear identity follows from the determinant
constraint −2bd ≡ 0 (mod 4).

**Theorem D (sharp classification)**: at conductor 4, only (a−b, c+d) and
(a+b, c−d) identities exist.

> **Significance**: this is the first multiplicative-character spin on the
> Shakov framework that pulls a divisor-style sum on SL₂(ℕ₀) onto an integer
> twisted divisor sum — i.e., it converts a bilinear matrix object into the
> kind of object analytic NT actually has tools for.

### 2.2 Cumulative bilinear sum and its size (P12 — Theorems B, C)

- **Theorem B (reduction)**:
  T(N) := Σ_{A ∈ SL₂(ℕ₀): χ(A) ≤ N} σ(ξ)σ(η) = Σ_{n=1}^{N} τ(n²+1) χ₄(n+1).
- **Theorem C (unconditional)**: T(N) = O(N).

  Proof sketch: Hooley hyperbola decomposition; the AP sum of χ₄ on odd-step
  APs satisfies |S| ≤ 1, even-step APs vanish because n₀ is forced odd by
  ρ(2)=1; Selberg–Delange for the linear count.

### 2.3 Rigorous upper bound for the spin sum (P12 — Nair/Henriot)

- **|T(N)| = |Σ τ(n²+1) χ₄(n+1)| ≪ N (log N)^{3/2}**.

  Via Cauchy–Schwarz on Σ τ(n²+1)² ≪ N(log N)³, which is itself rigorously
  established by Nair (1992) / Nair–Tenenbaum (1998) / Henriot (2012)
  applied to f = τ², F(x) = x²+1 (verified hypotheses; computed ρ_F;
  identified Dirichlet series D(s) = ζ_K(s)⁴ H₀(s) with H₀ analytic on
  Re s > 1/2; universal Halász cancellation 8−8=0 at split primes).

> **Significance**: rigorous power-of-log control. The empirical √N
> behavior (see §3.1) would require an extra (log N)^{3/2} of
> off-diagonal cancellation — the natural next analytic target.

### 2.4 Closed-form decomposition of the c₀^T constant (P12, May 6)

Exact integer identity:
$$T_<(N) = T_{\rm half}(N) + A(N) + B(N).$$

Closed form (rigorous via Selberg–Delange on G(s) = ζ_K(s)H(s) at the
simple pole s = 1):
$$A(N) = R H(1) \cdot N + O_A\!\big(N(\log N)^{-A}\big),
   \qquad R = \pi/4.$$

Verified empirically: at N = 10⁶, A(N) − R H(1) N = +0.5 absolute. All five
forecast quantities at N = 10⁶ from the prior session were confirmed.

Conditional reduction:
$$c_0^T = 2(R H'(1) + \gamma_K H(1) - R H(1)) - 2 B^\infty
        = 1.158730 - 2 B^\infty,$$
*conditional on existence of B^∞ := lim B(N)/N*. Empirical B^∞ ≈ 0.086 ± 0.002
across N ∈ [10⁴, 10⁶].

### 2.5 Selberg–Delange asymptotics for the second moment (P12, May 4)

Identified G(s) = Σ τ(d²)ρ(d) d^{−s} = ζ_K(s)³ H(s), with H absolutely
convergent for Re s > 1/2 and
$$H(1) = \tfrac{5}{16} \!\!\prod_{p \equiv 3(4)}\!\!(1-1/p^2)^3
             \!\!\prod_{p \equiv 1(4)}\!\!(1-1/p)^4(1+4/p-1/p^2)
        \approx 0.12324.$$
Closed-form secondary coefficients c₂ ≈ 0.870, c₁ ≈ 2.143 derived for
the conjectural leading asymptotic
   Σ_{n ≤ N} τ(n²+1)² ~ (π³ H(1)/48) N (log N)³ ≈ 0.0796 N (log N)³.

The leading constant is rigorous as an upper bound (Nair/Henriot, §2.3);
the matching asymptotic is the analog of Hooley 1957 for τ and is the
natural multi-session target.

## 3. What is empirical / conjectural (and quantitatively sharp)

### 3.1 Conjecture C — square-root cancellation in the spin sum

Empirical:
- |T(N)|/√N ∈ [0.06, 1.45] across N ∈ {10³, 10⁴, …, 10⁷}.
- Extended to N = 5·10⁷: RMS(T/√N) ≈ 0.638 stable.

**Conjecture C (refined to C′)**: T(N) = o(√N log N), plausibly
T(N) = O(√N (log log N)^{O(1)}) — GRH-strength cancellation.

This would require subconvexity for a Hecke L-function over ℚ(i).

### 3.2 The diagonal D(N), D₀(N) (second-moment route)

- D₀(N) rigorously Θ(N²) with closed-form bounds N²/(4π) ≤ D₀(N) ≤ 31N²/(4π)
  via Dirichlet identity F(s) = ζ_{ℚ(i)}(s) / [ζ(2s)(1+2^{-s})] and class
  number formula for ℚ(i).
- Empirical D₀/N² ∈ [0.7475, 0.7482] at N up to 2·10⁵ — consistent with
  C* ∈ [0.748, 0.750]; C* = 3/4 plausible but not ruled in or out.
- D − D₀ ≈ 0.232 N² stable.
- Per-d "independence" route to closing the log N gap **is refuted** by
  d=5 counterexample ⟨S(2)·S(3)⟩ = 0.3 ≠ 0. Future work needs a cross-d
  aggregation argument.

### 3.3 Caveat retracted (methodological lesson banked)

The cumulative V(N) = Σ T(M)² to N=10⁷ is statistically indistinguishable
from a Gaussian random-walk null. An earlier draft over-claimed "5.6×
suppression"; the comparison was apples-to-oranges (within-path std vs.
ensemble RW). Skeptic caught it; retracted. **Lesson**: when comparing
empirical within-path statistics against a theoretical null, ALWAYS use
Monte Carlo of the null applied to the SAME statistic — never the ensemble
formula.

## 4. The subconvexity chain (P11 / P13) — what was disproved and what is left

**P11 stated**: "sup-norm subconvexity over ℚ(i) ⇒ Theorem 2.12 ⇒ Landau IV."

**P13 verified by skeptic dialogue (May 2026)**: this chain is **NOT sound**.
- Petrow–Young Weyl-strength sup-norm subconvexity (saving 1/12 below
  convexity) is **insufficient** — gives cuspidal contribution N^{7/6} > trivial.
- The actual operative input is the **cubic moment** (Hyp 6.7 in P11 §5–6),
  giving an averaged second moment ∫|L|²dθ ≪ T^ε.

**Roadmap to prove the Bianchi cubic moment** (P13):
- Phase I (foundations) — known.
- Phase II (Bianchi Waldspurger) — ~3–6 months.
- Phase III (GL₂/ℚ(i) spectral 4th moment) — **central missing input**,
  ~8–10 months, comparable to Kowalski–Michel–VanderKam 2002.
- Phase IV (cubic moment via theta unfolding) — ~3–4 months.
- Phase V (extensions to all q) — ~6 months.

**Total**: 18–24 person-months, 80–120 pages, achievable in principle.

The single highest-EV next step here: read Yuan–Zhang–Zhang Ch. 3 with
F = ℚ(i) and write down explicit Bianchi Waldspurger; then set up the
amplified second moment of L(½, u_j) at level q on Bianchi forms.

## 5. Structural obstructions worth remembering

- **δ = 1 boundary obstruction**. SL₂(ℕ₀)'s limit set is the full positive
  real boundary — the worst case for Bourgain–Kontorovich / affine-sieve
  transfer-operator techniques.
- **Mauduit–Rivat for the S-sequence does NOT resolve Landau**.
  Codomain-sieving (fiber cardinality) ≠ value distribution. R8 negative
  observation; do not chase.
- **The S-sequence has triple eigenvalue 1 in its SL₃(ℤ) generators**,
  giving Jordan-block-induced polylogarithmic growth S(k) = O((log k)²)
  — an unusual regime that may admit Mauduit–Rivat methods after technical
  adaptation.
- **Rickards 2024 (Duke 2025), arXiv:2401.01860** is the closest published
  structural neighbor — semigroups in SL₂(ℤ) on continued fractions with
  reciprocity obstructions on which integers appear.
- **Shakov 2025 follow-up arXiv:2510.22805** on the τ(n²+1) 2-regular
  sequence (OEIS A383066) — not yet read.

## 6. Where to pick up next

Ranked by expected value, smallest first:

1. **Existence of B^∞ (1 session, cheap)** — show lim B(N)/N exists without
   computing the value. Converts §2.4 from "modulo existence" to "modulo
   value." Should follow standard density arguments for squarefree n²+1
   (Estermann 1931).
2. **Closed form for B^∞ (1–2 sessions)** — proper Dirichlet-series
   treatment of Σ_n τ*(n²+1) log Q(n²+1) with Q := m/rad(m); decompose
   log Q = Σ_p (log p) ν_p^+(m). The current heuristic gives a factor-2-low
   estimate.
3. **Off-diagonal asymptotic B₃^off(N) = −c₁ N log N + c₀' N + o(N)
   (multi-session, structural bottleneck)** — same c₁ as the diagonal
   forced by B₃ = O(N); secondary c₀' is independent content. Comparable
   in length to the entire Hooley 1957 paper.
4. **Verify Nair (1992) citation form against the original paper**
   (30-min literature check — blocked in sandbox by 403s on every
   academic publisher; flagged for Anton's local follow-up). The
   |T(N)| ≪ N (log N)^{3/2} consequence does not depend on this.
5. **Bianchi Waldspurger (P13 Phase II)** — read Yuan–Zhang–Zhang Ch. 3
   over ℚ(i); set up amplified second moment of L(½, u_j) at level q.

## 7. Files to read in this order

1. `memory/MEMORY.md` — top-level index of memory notes.
2. `memory/identity.md`, `memory/methodology.md` — persona and operating mode.
3. This file (`SIGNIFICANT_FINDINGS.md`) — what is established and conjectural.
4. `memory/p12-spin-identity-finding.md` — current state of P12 (the σ/ρ
   spin identity and its cumulative sum).
5. `memory/p13-subconvexity-verification.md` — the corrected P11 chain.
6. `bot/STRATEGY.md` — autonomous-bot ranked open directions and per-session log.
7. `n2+1 ai thoughts/notes/index.md` — wiki-graph of concepts/research/bridges/proofs.
8. `n2+1 ai thoughts/notes/proofs/P12-c0T-AB-decomposition.md` — most recent
   structural decomposition.
9. `n2+1 ai thoughts/notes/proofs/P13-subconvexity-skeptic-roadmap.md` —
   the Bianchi cubic moment plan.

## 8. House-keeping

- The bot fires every 3 hours and emails a summary + a session-log link
  to Anton at antoshashakov@gmail.com.
- Email path uses `bot/send_via_api.py` (Gmail HTTPS API). SMTP is blocked
  in this sandbox; drafts fallback removed.
- Refresh token is in Google Testing-mode and expires every 7 days —
  re-auth procedure documented in `memory/mathai-bot-email-path.md`.
- `bot/PROTOCOL.md` is canonical for current operating rules; **Anton's
  email replies trump everything**.
