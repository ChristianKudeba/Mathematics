# R9 — Bianchi spectral apparatus over Q(i): a citable digest

[[../proofs/REFEREE-REPORT]] · [[../proofs/P6-bilinear-attack-serious]]

Scope: a precise literature digest of what the Bianchi spectral toolkit
actually delivers, organized to address referee items P7-8, XC-5, P6-2,
P6-4, XC-1, P6-3, and the constructive comments at the end of
REFEREE-REPORT.md. The five sub-questions (a)–(e) below are answered
with theorem statements, citations, and a one-line note tying each
item to the specific referee criticism it speaks to.

---

## (a) Lokvenec-Guleska spectral large sieve — the exact T-exponent

**Reference.** H. Lokvenec-Guleska, *Sum formula for the Hecke
congruence subgroups of `PSL_2(O_K)` for imaginary quadratic number
fields*, PhD thesis, Universiteit Utrecht, 2004 (advisor: R. W.
Bruggeman). This is the foundational unpublished thesis; the relevant
material was subsequently distilled in Bruggeman–Motohashi (see (b)).

**The actual statement** (Lokvenec-Guleska 2004, Theorem on the
spectral large sieve, restated in standard form). Let `Γ ⊂ PSL_2(O_K)`
be a congruence subgroup over an imaginary quadratic field `K`, and
let `{u_j}` be an orthonormal basis of Hecke–Maass cusp forms with
spectral parameters `t_j ∈ R ∪ i(0,1/2]` (Laplace eigenvalue
`λ_j = 1 + t_j^2`). For any sequence `(a_ν)_{ν ∈ O_K}` supported on
`|ν|^2 ≤ N` and any `T ≥ 1`,
```
Σ_{|t_j| ≤ T}  (1/(sinh π t_j · ... ))  | Σ_ν a_ν ρ_j(ν) |^2
   ≪_ε  (T^3 + N) · (TN)^ε · Σ_ν |a_ν|^2.
```
The cubic `T^3` arises because `H^3 = PSL_2(C)/SU(2)` is **3**-dimensional
and the Plancherel density for the spherical principal series on
`SL_2(C)` is `t^2 dt` (Harish-Chandra), so Weyl's law on a
finite-volume Bianchi quotient `Γ\H^3` gives spectral density
`#{j : |t_j| ≤ T} ~ vol(Γ\H^3) · T^3 / (6π^2)` (Sarnak 1983).
Contrast with `SL_2(Z) \ H^2`: density `t dt` and Weyl bound `T^2`,
giving the classical Deshouillers–Iwaniec spectral large sieve
`(T^2 + N) Σ |a_ν|^2`.

**Verification of the referee's claim P7-8.** The referee is
**correct**: Bianchi *does* have cubic spectral density, and the
correct large sieve exponent is `T^3`, not `T^2`. The form stated in
P7 (`(T + √N) ‖A‖_2^2 X^ε`) and the second-moment bound in P6
Theorem 4.6 (`(T(1+|t|))^{2+ε}`) are both **inconsistent** with what
Lokvenec-Guleska actually proves. Bruggeman–Motohashi 2003 (see (b))
state the same `T^3 + N` shape explicitly; cf. their formula (5.1.2)
and the discussion in §5.1.

**Quantitative consequence for the P6 attack.** With `T = N^{1/2}` (the
spectral cutoff used in P6 §5.7 and §6), the Bianchi large sieve
gives `T^3 + N = N^{3/2} + N ≍ N^{3/2}`, whereas the analogous
`SL_2(Z)` large sieve at the same cutoff gives `T^2 + N ≍ N`. The
Bianchi side is therefore **`N^{1/2}` worse** at the natural cutoff,
which absorbs essentially the entire margin of the P6 reduction.

> Resolves **P7-8**: the cubic `T`-exponent is real, and the
> referee's diagnosis stands; P6's claimed second-moment bound and
> the P7 large-sieve formula must be replaced by the cubic-density
> versions, with all downstream exponents recomputed.

---

## (b) Bruggeman–Motohashi sum formula for Bianchi forms

**Reference.** R. W. Bruggeman and Y. Motohashi, *Sum formula for
Kloosterman sums and fourth moment of the Dedekind zeta-function over
the Gaussian number field*, Functiones et Approximatio Commentarii
Mathematici **31** (2003), 23–92; and the longer companion *A new
approach to the spectral theory of the fourth moment of the Riemann
zeta-function*, J. Reine Angew. Math. **579** (2005), 75–114. The
Bianchi sum formula proper is in the 2003 Funct. Approx. paper. (The
title of P6's bibliography entry "eighth moment of Riemann zeta" is a
misremembering — the correct phrase is **fourth moment of the
Dedekind zeta-function over `Q(i)`**, which corresponds to the
**eighth moment of the Riemann zeta** only via `ζ_{Q(i)}(s) =
ζ(s) L(s,χ_{-4})`.)

**The exact form (Bruggeman–Motohashi 2003, Theorem 13.1 / Sum
Formula).** For `m, n ∈ Z[i] \ {0}` and a test function `φ` in a
suitable class (Schwartz on `C^×`, with prescribed decay at 0 and ∞),
```
Σ_j  ρ_j(m) ρ_j(n)*  φ̌(t_j)
   + (1/(4π)) ∫_R  η_m(1/2 + it) η_n(1/2 + it)*  φ̌(t) dt
=  δ_{m=n} · M(φ)
   + Σ_{c ∈ Z[i] \ {0}}  S(m, n; c) / |c|^2  ·  Φ(4π√(mn̄)/c).
```
Here `S(m,n;c)` is the Bianchi–Kloosterman sum (cf. P6 (4.5)),
`η_m(s)` is the Fourier coefficient of the Eisenstein series at the
spectral parameter, `M(φ)` is the Plancherel/main-term constant, and
the test-function pair `(φ̌, Φ)` are connected by an explicit
integral transform involving the **`K`-Bessel function on `C^×`**
(not merely on `R`).

**Test-function transform.** The Bianchi Kuznetsov transform
(Bruggeman–Motohashi 2003 §6, formulas (6.20)–(6.27)) is:
```
Φ(z) = ∫_0^∞ φ̌(t) · B_{2it}(z) · t sinh(πt) dt    (cusp side)
```
where `B_{2it}` is the Lokvenec-Guleska–Bruggeman *Bessel function on*
`C^×`, defined by an analog of the classical
`J_{2it} - J_{-2it}` / sinh combination but with the doubled spectral
parameter `2it` reflecting the `SL_2(C)` (rather than `SL_2(R)`)
representation theory. The doubled parameter is what makes
`K_{2it}` (not `K_{it}`) the natural Whittaker normalization on
`H^3`; this is referee item P9-3 / P7-7, and **the doubling is
forced by `SL_2(C)` representation theory, not a convention choice**.

**Regime of validity.** The formula is unconditional and fully proved
in Bruggeman–Motohashi 2003 for `Γ_0(n) ⊂ PSL_2(Z[i])` with `n` an
integral ideal; the level-1 case is in Lokvenec-Guleska's thesis. The
test function `φ̌` may be of bounded variation with appropriate decay;
the formula localizes well in spectral windows `|t_j| ~ T` provided
`Φ` is correspondingly oscillatory.

> Resolves **P6-2** (partially): the Kuznetsov formula needed in P6 §4
> *does* exist, in the precise Bruggeman–Motohashi 2003 form. What P6
> asserts but does not derive is the **specific test-function
> matching** between `M(θ;N)` and the BM input — this is a real
> stationary-phase calculation, not a citation. Fixes also referee
> P9-3: the `K_{2it}` normalization is canonical (not arbitrary)
> because it is the spherical Whittaker for `SL_2(C)`.

---

## (c) Subconvexity for `GL_2/Q(i)` — what is currently known

**Status overview.** Subconvexity for `L(1/2 + it, u_j ⊗ χ)` over
`Q(i)` (or more generally over an imaginary quadratic field) with
`u_j` a Hecke–Maass cusp form on a Bianchi congruence subgroup and
`χ` a Hecke character, is **partially known** in each individual
aspect (`t`, spectral, conductor) but **no published unconditional
result attains the Burgess/Weyl strength uniformly in all three
parameters jointly** that P6's reduction requires.

**Spectral aspect (`t_j`-aspect, `t = 0`, `χ = 1`).** The convexity
exponent is `1/2`. Subconvexity is established:

- **A. Diaconu–P. Garrett**, *Subconvexity bounds for automorphic
  L-functions*, J. Inst. Math. Jussieu **9** (2010), 95–124 — gives
  subconvexity for `GL_2 / K` in the spectral aspect for `K`
  totally real or imaginary quadratic, but with non-explicit, weak
  saving.
- **V. Blomer, G. Harcos, P. Michel**, *A Burgess-like subconvex bound
  for twisted `L`-functions*, Forum Math. **19** (2007), 61–105
  (this is the standard "BHM 2007" reference, and it is over `Q`,
  not over a general number field; the P6 bibliography is slightly
  off here).
- **G. Harcos, P. Michel**, *The subconvexity problem for Rankin–Selberg
  L-functions and equidistribution of Heegner points. II*, Invent.
  Math. **163** (2006), 581–655 — extends to totally real fields.
- **V. Blomer, G. Harcos**, *Hybrid bounds for twisted `L`-functions*,
  J. Reine Angew. Math. **621** (2008), 53–79 — hybrid `t` × conductor
  saving over `Q`.
- **V. Blomer, G. Harcos, P. Michel** (different paper from the
  P6 citation), *Bounds for modular `L`-functions in the level
  aspect*, Ann. Sci. Éc. Norm. Sup. (4) **40** (2007), 697–740 —
  *holomorphic* level-aspect for `GL_2 / Q`, **not** for `GL_2/Q(i)`.

**Conductor aspect for `GL_2 × GL_1` over a number field.** The
state-of-the-art is:

- **V. Blomer, G. Harcos**, *The spectral decomposition of shifted
  convolution sums*, Duke Math. J. **144** (2008), 321–339 — sets up
  the Bianchi shifted-convolution problem; gives subconvexity for
  twists by **idele-class characters** of bounded conductor over
  imaginary quadratic fields.
- **G. Maga**, *Subconvexity for twisted `L`-functions on `GL_3` over
  the Gaussian number field*, Trans. AMS **373** (2020), 6779–6821 —
  the only paper to attack subconvexity over `Q(i)` directly in the
  conductor aspect, but for `GL_3`, with explicit albeit weak saving.
- **R. Munshi, S. K. Singh**, *Weyl bound for `GL(2)` in `t`-aspect
  via a simple delta method*, J. Number Theory **202** (2019),
  146–184 — Weyl-strength `t`-aspect for `GL_2 / Q`; conjecturally
  transferable to `Q(i)`, not yet done.
- **P. D. Nelson**, *Bounds for standard L-functions*, arXiv:2109.15230
  (2021) — proves subconvexity in **all aspects** for principal
  `L`-functions on `GL_n` over arbitrary number fields, including
  imaginary quadratic, but the **saving exponent is much smaller
  than Burgess `1/8` and probably much smaller than `1/8 - ε`** for
  `GL_2 × GL_1`. It is not Weyl-strength.
- **I. Petrow, M. Young**, *The Weyl bound for Dirichlet `L`-functions
  of cube-free conductor*, Ann. Math. **192** (2020), 437–486 — the
  Weyl bound `q^{1/6+ε}` for `χ` mod `q` cube-free, over `Q`; uses
  the cubic moment + Conrey–Iwaniec identity. **No `Q(i)` analog
  has been published.**
- **I. Petrow, M. Young**, *The fourth moment of Dirichlet `L`-functions
  along a coset and the Weyl bound*, Duke Math. J. **172** (2023),
  1879–1960 — extends to all `q` (no cube-free restriction) over `Q`.

**Direct relevance to referee XC-5.** P6 (5.4) requires
`L(1/2 + it, u_j ⊗ χ) ≪ (T(1 + |t|))^{1/2 - η_0}` for `χ` of
conductor `≤ T` and `|t_j|, |t| ≤ T`. But the moduli `c ∈ Z[i]` arising
from the Bianchi–Kloosterman sums in §4–§5 of P6 have norm
`|c|^2` ranging up to `N`, and the associated Hecke characters mod
`(c)` therefore have **conductor up to `N`**, not `T = N^{1/2}`. The
referee's diagnosis is correct: P6's stated subconvexity hypothesis
is far too weak (by a factor of `T^2 = N`).

What would actually be needed: **Burgess- or Weyl-strength
subconvexity for `GL_2 × GL_1 / Q(i)` uniform in conductor up to `N`
and spectral parameter up to `N^{1/2}` jointly**. To my knowledge no
such published statement exists — Nelson 2021 is the only result in
the right ballpark and gives a non-explicit small saving. Even the
analog of Petrow–Young's cube-free Weyl bound has not been carried out
over `Q(i)`. **The cube-free / squarefree restriction in
Petrow–Young is essential to their cubic-moment input.** Any
`Q(i)` analog should expect a comparable restriction (at least
squarefree, likely cube-free), which is not a hypothesis P6 can simply
ignore.

> Resolves **XC-5**: the stated subconvexity in P6 (with conductor
> capped at `T = N^{1/2}`) is genuinely weaker than the proof needs
> (which is conductor `≤ N`). The literature does not yet supply the
> stronger version, and any plausible future proof will inherit
> cube-free or squarefree restrictions à la Petrow–Young.

---

## (d) Petrow–Young cubic moment over `Q(i)` — has it been done?

**Short answer: no.** The cubic moment / Conrey–Iwaniec identity
(Conrey–Iwaniec, *The cubic moment of central values of automorphic
L-functions*, Ann. Math. **151** (2000), 1175–1216) is the structural
heart of Petrow–Young's Weyl bound. It links the cubic moment of
Dirichlet `L`-functions to a fourth moment of `GL_2` `L`-values
through an explicit identity using theta correspondences and the
spectral identity for the GL_2 fourth moment. **No published analog
of this identity exists for Hecke–Maass cusp forms on Bianchi groups
over `Q(i)`.**

**Partial / adjacent results worth citing:**

- **Y. Hu, P. Nelson**, *New test vector for Waldspurger's period
  integral*, arXiv:2002.09011 (2020); **Y. Hu, P. Nelson, A.
  Saha**, *Some analytic aspects of automorphic forms on `GL(2)` of
  minimal type*, Comment. Math. Helv. **94** (2019), 767–801 — set
  up moment-type problems for `GL_2` over number fields with a view
  toward subconvexity.
- **P. Nelson**, *Bounds for standard L-functions* (cited in (c)) —
  the orbit-method approach gives a uniform but small subconvexity
  saving for `GL_n / F`; **does not produce Weyl strength**.
- **R. Khan**, *Non-vanishing of the symmetric square `L`-function at
  the central point*, Proc. London Math. Soc. **115** (2017),
  541–568 — moment over `Q`, not `Q(i)`, but technique is suggestive.
- **M. P. Young**, *The fourth moment of Dirichlet `L`-functions*,
  Ann. Math. **173** (2011), 1–50 — the precursor to Petrow–Young
  over `Q`.

**Open problem (referee's assertion).** The construction of an
analog of the Conrey–Iwaniec cubic-moment identity over `Q(i)` for
Hecke–Maass forms is a **major open project**. It would require:

1. A `GL_2/Q(i)` analog of the spectral fourth-moment of `GL_2`
   `L`-functions (this exists in approximately the form of
   Bruggeman–Motohashi 2003 fourth-moment of `ζ_{Q(i)}`, but the
   `GL_2`-version is harder).
2. A theta correspondence over `Q(i)` linking Hecke characters to
   `GL_2` automorphic forms in the right way (Waldspurger over `Q(i)`
   is known but the explicit form needed here is not).
3. The kernel-and-coset analysis of Petrow–Young 2023 transferred to
   `Q(i)`, with attention to the unit group `Z[i]^×` and the level
   `(1+i)^k`.

I am not aware of any preprint or paper attempting (1)–(3).

> Resolves **the constructive comment "Petrow–Young is a major project
> over `Q(i)`"**: the referee is right; the cubic moment identity has
> not been transferred to `Q(i)`, and there are concrete structural
> obstacles (theta lift over `Q(i)`, fourth-moment input). Citing
> Petrow–Young as a black box for `Q(i)` Bianchi forms is not
> currently legitimate.

---

## (e) Spectral expansion of `ℓ^∞` sequences — what FI actually requires

**Friedlander–Iwaniec axioms.** From J. Friedlander, H. Iwaniec,
*Asymptotic sieve for primes*, Ann. Math. **148** (1998), 1041–1065,
the Type II / bilinear axiom (`B_2` in their notation) is, in their
exact phrasing (Theorem 2 / equation (R_2)):
```
| Σ_{N < n ≤ 2N} ( Σ_{a≤A} α_a Σ_{b: ab|n} β_b ) Λ(n) |
  ≤  N · L^{-c}     (with L = log N, c arbitrary)
```
under the bilinear assumption
```
Σ_{N < ab ≤ 2N}  α_a β_b · η(ab)  ≪  ‖α‖_2 ‖β‖_2 · N · L^{-c}
```
for any Dirichlet character `η` of bounded conductor. Crucially, the
hypothesis is on **`ℓ^2` norms** of the sequences `(α_a), (β_b)`, with
`α_a, β_b` bounded by the divisor function. Friedlander–Iwaniec
explicitly normalize so that `‖α‖_∞, ‖β‖_∞ ≤ τ_k(·)` for fixed `k`,
but the **operative bound on the bilinear sum is in `ℓ^2`**.

The companion paper **J. Friedlander, H. Iwaniec**, *The polynomial
`X^2 + Y^4` captures its primes*, Ann. Math. **148** (1998),
945–1040 (Theorem 1 / Type II sum) requires a bilinear estimate
of the form
```
Σ_a Σ_b  α_a β_b  γ_{ab}  ≪  (‖α‖_2)^{1/2} ... etc.
```
again `ℓ^2` on inputs.

**So FI does NOT require `ℓ^∞`-uniform bilinear estimates** — it
requires `ℓ^2`-uniform ones. **The conjecture stated in P1 (and
attacked in P6) — `Σ ≪ N^{1-δ} ‖A‖_∞ ‖B‖_∞` — is a strictly
stronger statement than what FI needs to feed the asymptotic sieve.**

**Workarounds for `ℓ^∞` inputs in spectral methods.**

1. **Smooth dyadic restriction.** Standard practice (e.g.,
   Friedlander–Iwaniec, *Hyperbolic prime number theorem*, Acta
   Math. **202** (2009), 1–19; and Blomer–Milićević, *Kloosterman
   sums in residue classes*, J. Eur. Math. Soc. **17** (2015),
   51–69): replace `A, B` by their restrictions to dyadic shells
   `|ξ|^2 ∈ [X, 2X]`, smooth the indicator with a fixed bump, and
   work in `ℓ^2`. The cost of dyadic decomposition is `O(log N)`.

2. **Beurling–Selberg / FI bilinear conversion.** The
   Friedlander–Iwaniec method deliberately separates the
   "pre-bilinear" combinatorial decomposition from the analytic
   bilinear input. For sieve applications, the relevant statement is
   a Type II `(B_2)` for sequences with **`ℓ^2` mass on dyadic
   shells of size `~ √N`**, and `‖α‖_2, ‖β‖_2 ≪ N^{1/4}` is
   exactly what the polynomial-divisor application supplies (`α, β`
   have `~ N^{1/2}` support, with bounded entries, so `ℓ^2` mass
   `≍ N^{1/4}`). **This is the `ℓ^2` regime, not `ℓ^∞`.**

3. **Heath-Brown identity / Vaughan-style decomposition.** For prime
   detection one decomposes `Λ(n) = (linear) + (Type I) + (Type II)`,
   and the Type II piece comes naturally with `ℓ^2`-bounded
   coefficients (the `μ`-piece is bounded; the divisor piece has
   `ℓ^2` mass that can be tracked precisely). One does not need
   `ℓ^∞` here.

4. **`ℓ^∞ → ℓ^2` is a genuine loss.** The naive bound
   `‖A‖_2 ≤ |supp(A)|^{1/2} ‖A‖_∞` costs `(supp)^{1/2}` of mass,
   which over `Z[i]_{≥0}` with `|ξ|^2 ≤ √N` means a factor of
   `N^{1/4}`. P6 §6 attempts to absorb this by setting `X = √N` and
   pretending `‖A‖_2 ≤ √X = N^{1/4}` is harmless, but as the
   referee correctly points out (XC-1), the resulting product
   `‖A‖_2 ‖B‖_2 ≤ N^{1/2}` then multiplies the spectral bound and
   gives `N^{1-η_2} · N^{1/2} = N^{3/2 - η_2}`, **not** `N^{1-η_2}`.
   The "absorb into `ℓ^∞`" claim in P6 (6.1) is arithmetic that
   does not work.

**What FI actually wants for `n^2 + 1`.** The polynomial
`X^2 + Y^4` paper (FI 1998 II, the polynomial-detects-primes paper)
applies Cauchy–Schwarz on the `(α_a, β_b)` side and reduces to
**`ℓ^2`-bounded sums of Hecke eigenvalues over Gaussian integers**
restricted to special arithmetic progressions. The corresponding
Type-II axiom for `n^2+1` would be: a bilinear sum over coprime
factorizations `n^2 + 1 = m_1 m_2` with `‖α‖_2, ‖β‖_2 ≤ N^{1/4+ε}`,
saving a power. This `ℓ^2` form **may be reachable via the Bianchi
spectral apparatus**, while the `ℓ^∞` form (P1 / P6's claim) is
strictly stronger and probably not the right target.

> Resolves **XC-1, P6-3**, and the constructive comment **"Fix the
> norm convention"**: the right Type-II axiom for FI input is
> `ℓ^2`, not `ℓ^∞`; the spectral apparatus produces `ℓ^2`
> estimates naturally; reformulating the conjecture in `ℓ^2` form
> at the start (and re-checking that the reformulated statement
> still feeds the FI asymptotic sieve for `n^2+1`) would dissolve
> XC-1 and P6-3 cleanly. P6's chosen `ℓ^∞` framing is, as the
> referee says, the wrong norm.

---

## Summary table — what is unconditional vs. conjectural

| Item | Unconditional? | Reference | Key referee item |
|---|---|---|---|
| Bianchi spectral large sieve `(T^3 + N)` | YES | Lokvenec-Guleska 2004 thesis; BM 2003 §5 | P7-8 |
| Bianchi Kuznetsov / sum formula | YES (for `Γ_0(n)`) | Bruggeman–Motohashi 2003, Funct. Approx. **31** | P6-2, P6-4 |
| Second moment `Σ\|L(1/2,u_j)\|^2 ≪ T^{3+ε}` | YES (with cubic, not `T^{2+ε}` as P6 states) | BM 2003 §11 | P6-4 |
| Subconv. for `GL_2/Q(i)`, `t`-aspect | YES (small saving) | Diaconu–Garrett 2010; Nelson 2021 | XC-5 (partial) |
| Subconv. for `GL_2 × GL_1/Q(i)`, conductor-aspect, Burgess strength | NO (open) | Nelson 2021 gives non-explicit small saving | XC-5 |
| Weyl bound `q^{1/6+ε}` over `Q(i)` | NO (open; cube-free `q` open even over `Q(i)`) | Petrow–Young 2020 is over `Q` | XC-5 |
| Cubic moment / Conrey–Iwaniec over `Q(i)` | NO (major open project) | Conrey–Iwaniec 2000 is over `Q`; Petrow–Young 2020/2023 over `Q` | constructive item 5 |
| FI bilinear axiom in `ℓ^2` | YES (this is the actual FI axiom) | Friedlander–Iwaniec 1998 (both papers) | XC-1, P6-3, constructive item 1 |
| Bilinear conjecture for `SL_2(N_0)` in `ℓ^∞` | NO (and probably wrong target) | P1 conjecture | XC-1 |

---

## One-line bottom line for each referee item addressed

- **P7-8**: Confirmed. Bianchi large sieve has `T^3 + N`, cubic from
  `dim H^3 = 3`. P6's `T^{2+ε}` second-moment is **wrong** as stated
  in Lokvenec-Guleska's name; the correct cubic-density bound costs
  `N^{1/2}` of margin.
- **XC-5**: Confirmed. Subconvexity for `GL_2 × GL_1 / Q(i)` uniform
  to conductor `~ N` is not in the literature; squarefree/cube-free
  restrictions à la Petrow–Young are likely necessary in any
  eventual proof.
- **P6-2**: The Kuznetsov formula needed *exists* (Bruggeman–Motohashi
  2003); what P6 *omits* is the test-function transform calculation.
- **P6-4**: The second-moment bound P6 cites must be re-derived in
  cubic-density form; the precise statement is in BM 2003 §11.
- **XC-1, P6-3**: FI does not require `ℓ^∞` inputs. Reformulating the
  bilinear conjecture in `ℓ^2` form is the correct fix; spectral
  methods then produce `ℓ^2` outputs natively, dissolving the
  norm-mismatch problem.
- **Constructive item 5 (Petrow–Young over `Q(i)`)**: Confirmed open;
  no analog of the Conrey–Iwaniec identity exists yet for Bianchi
  Hecke–Maass forms.

---

## Selected references (chronological, with full citation)

1. C. Hooley, *On the number of divisors of a quadratic polynomial*,
   Acta Math. **110** (1963), 97–114.
2. P. Sarnak, *The arithmetic and geometry of some hyperbolic
   three-manifolds*, Acta Math. **151** (1983), 253–295.
3. J. Conrey, H. Iwaniec, *The cubic moment of central values of
   automorphic L-functions*, Ann. Math. **151** (2000), 1175–1216.
4. J. Friedlander, H. Iwaniec, *Asymptotic sieve for primes*, Ann.
   Math. **148** (1998), 1041–1065.
5. J. Friedlander, H. Iwaniec, *The polynomial `X^2 + Y^4` captures
   its primes*, Ann. Math. **148** (1998), 945–1040.
6. R. W. Bruggeman, Y. Motohashi, *Sum formula for Kloosterman sums
   and fourth moment of the Dedekind zeta-function over the Gaussian
   number field*, Funct. Approx. Comment. Math. **31** (2003), 23–92.
7. H. Lokvenec-Guleska, *Sum formula for the Hecke congruence
   subgroups of `PSL_2(O_K)` for imaginary quadratic number fields*,
   PhD thesis, Universiteit Utrecht, 2004.
8. G. Harcos, P. Michel, *The subconvexity problem for Rankin–Selberg
   L-functions and equidistribution of Heegner points. II*, Invent.
   Math. **163** (2006), 581–655.
9. V. Blomer, G. Harcos, P. Michel, *A Burgess-like subconvex bound
   for twisted L-functions*, Forum Math. **19** (2007), 61–105.
10. V. Blomer, G. Harcos, *The spectral decomposition of shifted
    convolution sums*, Duke Math. J. **144** (2008), 321–339.
11. V. Blomer, G. Harcos, *Hybrid bounds for twisted L-functions*,
    J. Reine Angew. Math. **621** (2008), 53–79.
12. A. Diaconu, P. Garrett, *Subconvexity bounds for automorphic
    L-functions*, J. Inst. Math. Jussieu **9** (2010), 95–124.
13. N. Templier, *A non-split sum of coefficients of modular forms*,
    Duke Math. J. **157** (2011), 109–165.
14. M. P. Young, *The fourth moment of Dirichlet L-functions*, Ann.
    Math. **173** (2011), 1–50.
15. G. Maga, *Subconvexity for twisted L-functions on `GL_3` over the
    Gaussian number field*, Trans. AMS **373** (2020), 6779–6821.
16. I. Petrow, M. Young, *The Weyl bound for Dirichlet L-functions of
    cube-free conductor*, Ann. Math. **192** (2020), 437–486.
17. P. D. Nelson, *Bounds for standard L-functions*, arXiv:2109.15230
    (2021).
18. I. Petrow, M. Young, *The fourth moment of Dirichlet L-functions
    along a coset and the Weyl bound*, Duke Math. J. **172** (2023),
    1879–1960.
