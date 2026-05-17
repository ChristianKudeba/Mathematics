# P11. Bianchi Q→Q(i) extension: master document

> Clean conditional reduction of Landau IV (∞-many primes $n^2+1$) to a Bianchi cubic-moment / Petrow–Young-strength subconvexity input over $\mathbb{Q}(i)$.

This document is the index and meta-commentary for **P11**, the rewrite that supersedes the corresponding parts of [[P6-bilinear-attack-serious|P6]]–[[P9-bianchi-whittaker|P9]] in response to the [[REFEREE-REPORT|skeptical referee report]].

P11 is split into three .tex files (each fully self-contained, each compiles independently):

| Section | File | Lines | Scope |
|--------|------|-------|-------|
| §1–2 | [[P11-section-1-2.tex]] | 496 | Setup, $\ell^2$ norm convention, Shakov–Gaussian bijection, direct Type-II reduction (no CS-to-dispersion), main conditional theorem |
| §3–4 | [[P11-section-3-4.tex]] | 725 | Whittaker normalization fixed, cubic-$T^3$ spectral large sieve, Bianchi-Kuznetsov, Eisenstein-to-leading-order, three-regime stationary phase including small-$\theta$ degenerate IBP |
| §5–6 | [[P11-section-5-6.tex]] | 800 | Linnik dispersion + $\mathbb{Z}[i]$-Kloosterman (Route A, abandons broken bilinear-Voronoi), redone main-term as residue at $s=1$, corrected self-similarity, no bootstrap, residual gap (Bianchi cubic moment) |

Supporting research digests:

| File | Scope |
|------|-------|
| [[../research/R9-bianchi-spectral-apparatus.md]] | Lokvenec-Guleska large sieve (cubic $T^3$ confirmed), Bruggeman–Motohashi sum formula, GL₂/Q(i) subconvexity status, Petrow–Young analog over Q(i) (open), FI ℓ² axiom |
| [[../research/R10-voronoi-whittaker-eisenstein.md]] | Z[i]-Voronoi, no published bilinear-weighted Voronoi exists, Eisenstein evaluation template (Bykovsky/Templier), Whittaker normalizations (5 references reconciled), Airy-type transition asymptotic for $K_{2it}$ |

---

## The bottom line

> **P11 is an honest conditional reduction.** Modulo a single residual unconditional gap — the Petrow–Young-strength **Bianchi cubic moment** for Hecke–Maass forms over $\mathbb{Q}(i)$ in the conductor aspect — Landau's fourth problem follows.
>
> The cubic-moment input has not been written down in the literature. Adapting Conrey–Iwaniec to the Bianchi setting is a major open project, comparable in scope to Petrow–Young's original 2020 paper.

P11 should *not* be cited as "a proof of Landau IV." It should be cited as: a clean conditional reduction with all critical errors of P6–P9 either resolved or transparently identified; the precise residual gap is now a well-defined open problem, not a fog of vagueness.

---

## Referee criticism — resolution status

The 9 critical and 12 serious items from [[REFEREE-REPORT]] are tracked here. ✅ resolved · 🟡 partially resolved (with honest acknowledgement) · 🔴 still open · ↪ now subsumed (was an artifact of the broken structure).

### Cross-cutting (XC)

| ID | Sev. | Status | Where resolved | One-line resolution |
|----|------|--------|----------------|----------------------|
| XC-1 | 🔴 CRIT | 🟡 partial | §1.3 norm convention (P11 §1-2); Remark 2.16 §5-6 | Adopted ℓ² throughout. FI Type-II actually accepts ℓ² (R9 finding). For ℓ^∞ inputs the bound has an extra $X^{1/2}\asymp N^{1/2}$ — honestly admitted as a real loss; ℓ^∞ form is *not* what FI needs anyway. |
| XC-2 | 🔴 CRIT | ✅ | §2 throughout (P11 §1-2) | Norms tracked consistently in ℓ²; closing step does not require ℓ^∞ → ℓ² conversion. |
| XC-3 | 🟡 SERIOUS | ✅ | Prop. main-correct (P11 §5-6); §3.4 Eisenstein (P11 §3-4) | Main term is **residue at $s=1$** of $\widetilde A(s)\widetilde B(s)K(s;θ;N)$, not evaluation at $s=1/2$. Residue is well defined for $A,B \in \ell^2$. For FI Type-II inputs (zero mean), main term **vanishes**. |
| XC-4 | 🟡 SERIOUS | 🟡 partial | Lemma 3.5 (P11 §3-4); Prop. eis-bound (P11 §5-6) | Eisenstein contribution written down to leading order: $\theta$-independent main term $\widetilde\psi(1)N\widetilde A(1/2)\widetilde B(1/2)P_2(\log N)/\zeta_{\mathbb{Q}(i)}(2)$ + bounded $\theta$-dependent residual. Residual: detailed Bruggeman–Miatello calculation referenced not redone. |
| XC-5 | 🟡 SERIOUS | ✅ | Hypothesis H-PY-corrected (P11 §1-2 + §3-4 §3.6) | Subconvexity stated with full conductor range $|\mathfrak{q}| \le N$ (**not** $T = N^{1/2}$ as P6 claimed); spectral apparatus uniform in conductor; the "real" weakness now lives in the conditional input. |
| XC-6 | 🟡 SERIOUS | ✅ | Remark 1.11 (P11 §1-2) | Honestly stated: SL₂(ℕ₀) plays no analytic role after Gaussian-integer passage; its contribution is structural (pinpointed the slice $\{\Re(\xi\eta)=1\}$). |

### P6 (`P6-bilinear-attack-serious.tex`)

| ID | Sev. | Status | Where resolved | One-line resolution |
|----|------|--------|----------------|----------------------|
| P6-1 | 🔴 CRIT | ✅ | §2 (P11 §1-2) | **No Cauchy–Schwarz to dispersion**. Direct Type-II via Fourier inversion in $\theta\in[0,1]$: $\Sigma_\psi = \int_0^1 e(-\theta) M(\theta;N)\,d\theta$. The dispersion *is* used in §5 for off-diagonal control, but only after spectral reduction, not as a primary tool. |
| P6-2 | 🟡 SERIOUS | ✅ | §3.3 (P11 §3-4) | Bianchi-Kuznetsov sum formula stated explicitly with both cuspidal and Eisenstein contributions, not asserted. |
| P6-3 | 🟡 SERIOUS | ✅ | §1 ℓ² convention | Spectral projections $\langle A, u_j\rangle$ are well defined for $A \in \ell^2$. The original conflict was a phantom of the wrong norm choice. |
| P6-4 | NEEDS-WORK | ✅ | R9 (a) + Theorem 3.2 (P11 §3-4) | Lokvenec-Guleska's actual statement is $T^3 + N$ (not $T^{2+\varepsilon}$ as P6 claimed). **Confirms referee's correction.** |
| P6-5 | NEEDS-WORK | ✅ | §6 (P11 §5-6) | Power-saving error term derivation now explicit; $\theta$-uniformity of constants tracked. |
| P6-6 | MINOR | — | (untouched) | Boundary spine constant identification; not load-bearing. |

### P7 (`P7-filling-the-gaps.tex`)

| ID | Sev. | Status | Where resolved | One-line resolution |
|----|------|--------|----------------|----------------------|
| P7-1 | 🔴 CRIT | ✅ | §5 Route A (P11 §5-6) | **Bilinear-weighted Voronoi abandoned wholesale.** R10 confirmed no published "double Voronoi" for $d \times d$ on $\mathbb{Z}[i]$ exists. Replaced by Linnik dispersion + Estermann/Weil $\mathbb{Z}[i]$-Kloosterman bound (referee's constructive item #4). |
| P7-2 | 🔴 CRIT | ✅ | §5 Mellin-fix (P11 §5-6) | Polar substitution exponent corrected: $r^{2s-1} \cdot (1/\sin\phi) \to (\sin\phi)^{-2s}$, not $(\sin\phi)^{2s-1}$. Convergence at $\phi=0,\pi$ via contour shift to $\Re s = 1/2 - \eta$. |
| P7-3 | 🟡 SERIOUS | ✅ | §5 (P11 §5-6) | Non-convergence at $\Re s = 1/2$ resolved by contour shift; residues from poles in the strip tracked. |
| P7-4 | 🟡 SERIOUS | ✅ | §5 (P11 §5-6) | **Honestly recomputed**: at $\Re s = 1/2 - \eta$ in bulk, amplitude is $\lambda^{-1/4+\eta} |k|^{-3/4+\eta}$, off by $\lambda^{1/2}$ from P7's claim. Documented that this error fortuitously partially compensates the cubic-vs-quadratic large-sieve error of P7-8. |
| P7-5 | 🟡 SERIOUS | ✅ | §4 (P11 §3-4) | Stationary-phase done explicitly (3 regimes + small-$\theta$ IBP). No more "see [BHM, Lemma 4.3]" hand-wave. |
| P7-6 | 🔴 CRIT | ✅ | §6 (P11 §5-6) | Theorem 4.1 internal contradiction resolved: trivial bound + spectral error $\not\Rightarrow$ power saving without separate main-term argument. The new main-term argument is in §6 (residue, vanishing for FI inputs). |
| P7-7 | 🟡 SERIOUS | ✅ | §3.1 + R10(d) | Whittaker convention **fixed once**: Lokvenec-Guleska normalization $W_{it}(n(x)a(y)) = y \cdot K_{2it}(2\pi|x|y) \cdot e(\Re x)$. Conversion factors to four other references documented. |
| P7-8 | 🟡 SERIOUS | ✅ | §3.2 + R9(a) | **Cubic $T^3$-exponent confirmed**, not $T + \sqrt{N}$. R9 verified this from Lokvenec-Guleska 2004 directly; P6's bound was wrong. The cost: $N^{1/2}$ worse than the SL₂/Q analog when $T \asymp N^{1/2}$. |

### P8 (`P8-mainterm-bookkeeping.tex`)

| ID | Sev. | Status | Where resolved | One-line resolution |
|----|------|--------|----------------|----------------------|
| P8-1 | 🔴 CRIT | ✅ | Lemma 6.5 (P11 §5-6) | Self-similarity corrected: rescaling by $c$ rescales **both** slice and support, giving scale-$N/|c|^2$ subproblems with rescaled $\widetilde A_c, \widetilde B_c$. |
| P8-2 | 🟡 SERIOUS | ✅ | Remark bootstrap-fails (P11 §5-6) | **Bootstrap repudiated.** At smaller scale, applying the conditional bound gives the same exponent — no contraction. Petrow–Young is one-shot, not iterative. P11 invokes no bootstrap. |
| P8-3 | 🟡 SERIOUS | ↪ | (subsumed) | The $W_0/W_1$ decomposition is gone; the new dispersion-based proof never makes this split, so the smoothing issue with $\min(1, 1/|\rho|)$ does not arise. |
| P8-4 | 🔴 CRIT | ✅ | Lemma c0-Sigma (P11 §5-6) | Dimensional non-sequitur resolved: the $\theta$-independent main term contributes zero by FI Type-II input axiom; for non-FI inputs, residue formula replaces "divide by $N$." |

### P9 (`P9-bianchi-whittaker.tex`)

| ID | Sev. | Status | Where resolved | One-line resolution |
|----|------|--------|----------------|----------------------|
| P9-1 | 🔴 CRIT | ✅ | §4.3, Remark vs-P9 (P11 §3-4) | **Direct diagnosis of the missing factor:** P9's $|t|^{-1/2}$ Hessian-decay claim was a conflation of $dx/x$ vs $dy/y$ Jacobian (factor $1/(2y) \asymp 1/N$, contributing $N$) with boundary-of-stationary-phase decay (factor $\theta^{-1/2}$, now in the IBP $A=1$ term). No stationary-phase saving in the bulk; the rapid-decay bound comes from IBP in the small-$\theta$ regime. **Note:** R10 independently observed that the bulk $|K_{2it}(y)| \asymp |t|^{-1/2}$ is itself wrong in the transition window $y\sim |t|$ (Airy-type, $|t|^{-1/3}$). The two diagnoses are consistent; both reroute the saving away from the bulk Hessian. |
| P9-2 | 🟡 SERIOUS | ✅ | §3 (P11 §3-4) | Holomorphic vs. Maass conflation no longer present: Bianchi forms are Maass forms over $\mathbb{Q}(i)$, treated as such. BHM citation corrected (R9 finding: P6's BHM cite was for $\mathbb{Q}$, not $\mathbb{Q}(i)$). |
| P9-3 | 🟡 SERIOUS | ✅ | §3.1 + R10(d) | Whittaker normalization fixed (see P7-7). R10 finding: the $K_{2it}$ vs $K_{it}$ doubling is **forced by SL₂(C) representation theory**, not a convention; it's the test-function transform's *coefficients* that are convention-dependent. |
| P9-4 | 🟡 SERIOUS | ✅ | §4.4 small-theta (P11 §3-4) | Small-$\theta$ regime treated separately by IBP; stationary-point degeneration handled. |
| P9-5 | NEEDS-WORK | ✅ | §4.2 + R10(f) | Olver citation refined; the relevant uniform asymptotic regime is the Dunster 1990 / Booker–Strömbergsson–Then transitional Bessel asymptotic. |

### Tally

| Severity | Total | ✅ resolved | 🟡 partial | 🔴 open | ↪ subsumed |
|----------|------:|:-----------:|:----------:|:-------:|:----------:|
| Critical | 9 | 8 | 1 (XC-1) | 0 | 0 |
| Serious  | 12 | 9 | 2 (XC-4, XC-1↗) | 0 | 1 (P8-3) |
| Needs-work | 5 | 4 | 0 | 0 | 0 |
| **Total** | **26** | **21** | **3** | **0** | **1 + 1 minor** |

---

## What is genuinely new in P11 (vs. P6–P9)

1. **ℓ² formulation** of the bilinear conjecture, properly aligned with Friedlander–Iwaniec's actual $B_2$ axiom (R9 finding: FI accepts ℓ², not ℓ^∞).
2. **Direct Type-II via Fourier in $\theta$** — no Cauchy–Schwarz to dispersion as the primary tool. Dispersion appears in §5 only for off-diagonal Kloosterman bookkeeping.
3. **Conductor range $|\mathfrak{q}| \le N$** in the subconvexity input, correctly stated for the first time. Previous P6 used $|\mathfrak{q}| \le \sqrt{N}$, which the referee (XC-5) and R9 confirmed is too weak.
4. **The slice $\{\Re(\xi\eta)=1\} \subset \mathbb{Z}[i]$** as the geometric heart of Landau IV, and its analytic translation through the slice-Fourier identity.
5. **Lokvenec-Guleska Whittaker convention pinned down**, with a 5-reference conversion table (R10 finding).
6. **Cubic $T^3$ honestly accounted** in the spectral large sieve, with the resulting $N^{1/2}$ cost vs. the $\mathbb{Q}$ analog flagged (R9 finding).
7. **Linnik dispersion + Weil $\mathbb{Z}[i]$-Kloosterman** as the off-diagonal frame, replacing the wholesale-broken bilinear-Voronoi (R10 finding: no published double-Voronoi for $d\times d$ on $\mathbb{Z}[i]$).
8. **Honest diagnosis of the P9 missing factor** as a $dx/x$ vs $dy/y$ Jacobian conflation; rapid-decay saving moved to the small-$\theta$ IBP regime.
9. **Main term as residue at $s=1$**, not evaluation at $s=1/2$ (resolves XC-3); vanishing for FI Type-II inputs (zero-mean).
10. **Single residual gap explicitly stated** as Hypothesis 6.7 (Bianchi cubic moment, Petrow–Young strength, conductor aspect, cube-free uniformity). Proposed as the next major project of the program.

## What is NOT shown

- Landau's fourth problem itself (P11 is conditional).
- The Bianchi cubic moment over $\mathbb{Q}(i)$ (the residual gap).
- An ℓ^∞-form bilinear bound (the FI sieve doesn't need one).
- An improvement on Iwaniec $P_2$ or Pascadi–Grimmelt–Merikoski $\theta = 1.312$ unconditionally.

## Honest structural note (referee XC-6 territory)

The Shakov / SL₂(ℕ₀) framework gave us the slice $\{\Re(\xi\eta)=1\}$ as the geometric heart of $n^2+1$ — that is its real contribution. Beyond that point, the analytic argument is "shifted convolution + spectral on $\mathrm{PSL}_2(\mathbb{Z}[i])\backslash \mathbb{H}^3$" and could in principle have been written by someone who started directly from the Gaussian-integer reformulation of $n^2+1$ without ever seeing Shakov's paper. We do not pretend otherwise.

---

## Pointers forward

**P12 (proposed):** Adapt Conrey–Iwaniec cubic moment to Hecke–Maass forms over $\mathbb{Q}(i)$ in the conductor aspect, with cube-free or squarefree uniformity. This is the residual gap; it is a substantial project on its own (R9 estimate: comparable in scope to Petrow–Young 2020).

**P13 (alternative):** Investigate whether the $T^3$ spectral density loss can be partially recovered by exploiting the Plancherel decomposition along Hecke characters, splitting the spectrum and applying Burgess-quality bounds in cross-sections. Speculative; not yet attempted.

**Open structural question:** is there a route to Landau IV via P11 that avoids the cubic-moment input entirely — for instance, via $\delta$-symbol methods on $\mathbb{Q}(i)$, or via the Vinogradov–Korobov circle / arc decomposition adapted to the slice? Worth exploring.
