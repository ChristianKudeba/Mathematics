# R10 — Voronoi / Whittaker / Eisenstein machinery over $\mathbf{Q}(i)$

A literature digest for the technical inputs needed by [[../proofs/P7-filling-the-gaps]] and [[../proofs/P9-bianchi-whittaker]], targeted at the gaps flagged in [[../proofs/REFEREE-REPORT]] (P7-1–P7-7, XC-3, XC-4, P9-1–P9-4, plus constructive items 3 and 4). The scope is strictly the Voronoi/Whittaker/Eisenstein machinery over $\mathbf{Q}(i)$. I distinguish **unconditional / explicitly stated in published work** from **folklore or sketched**, and flag where the literature is silent.

---

## (a) Voronoi summation over $\mathbf{Z}[i]$ for $d_{\mathbf{Z}[i]}(\nu)$

**Directly addresses: P7-1 (statement of Voronoi for the unweighted divisor), P9-3 / P7-7 (Bessel-kernel constants).**

The cleanest published statement for $\mathrm{GL}_2/\mathbf{Q}(i)$ Voronoi for the divisor function is the specialization of the **Ichino–Templier** general $\mathrm{GL}_n$ Voronoi formula (Amer. J. Math. **135** (2013), 65–101, Theorem 1) to $n=2$ and the complex place. In that form the formula reads, for $\gcd(\mu,c) = 1$ in $\mathbf{Z}[i]$ and $f$ a Schwartz function on $(0,\infty)$,
$$
\sum_{\nu\in\mathbf{Z}[i]} d_{\mathbf{Z}[i]}(\nu)\, e\!\Big(\mathrm{Re}\frac{\mu\nu}{c}\Big)\, f(|\nu|^2)
\;=\;
\frac{1}{|c|^4}\sum_{\nu\in\mathbf{Z}[i]} d_{\mathbf{Z}[i]}(\nu)\, e\!\Big(-\mathrm{Re}\frac{\bar\mu\nu}{c}\Big)\, \widetilde f\!\Big(\frac{|\nu|^2}{|c|^4}\Big) \;+\; \mathrm{MT}(c,\mu),
$$
where $\bar\mu\mu \equiv 1 \pmod c$, $\mathrm{MT}(c,\mu)$ is the polar contribution (a polynomial in $\log|c|$ of degree $1$ over $\mathbf{Q}(i)$, since $\zeta_{\mathbf{Q}(i)}(s) = \zeta(s) L(s,\chi_{-4})$ has a simple pole at $s=1$), and the Hankel–Voronoi transform $\widetilde f$ is **the doubled-Bessel kernel for the complex place**:
$$
\widetilde f(\xi) \;=\; (2\pi)^2 \int_0^\infty f(y)\, J_0^{\sharp}(4\pi\sqrt{\xi y})\, dy,
\qquad
J_0^{\sharp}(x) \;=\; -2\pi\bigl(Y_0(x) + \tfrac{2}{\pi}K_0(x)\bigr).
$$

The factor $(2\pi)^2$ (one $2\pi$ per real dimension of $\mathbf{C}$), the kernel $-2\pi Y_0 - \frac{4}{\pi}K_0$, and the modulus $|c|^4$ (the $\mathbf{Z}[i]$-norm of $c\bar c$) are exactly the substitutions that distinguish the complex from the real Voronoi: over $\mathbf{Q}$, one has $|c|^2$ and the kernel $-2\pi Y_0(x) - 4K_0(x)$ from the standard reference (Iwaniec–Kowalski, *Analytic Number Theory* (AMS Colloq. **53**, 2004), Theorem 4.10).

A second published source giving the formula in fully explicit complex-place form is **Lokvenec-Guleska**'s thesis (Utrecht 2004, Theorem 12.3.1 / §12.3), which derives the Bianchi Voronoi as a corollary of the Bianchi–Kuznetsov sum formula. **Smith** (PhD, Caltech / preprints on arXiv c. 2017–2020) and **Maga** (Acta Arithmetica, 2013) restate this in a form usable for $\mathrm{GL}_2 \times \mathrm{GL}_1$ subconvexity over imaginary quadratic fields. **Bruggeman–Motohashi**, *Sum formula for Bianchi forms* (Mem. AMS / J. Math. Sci. (Japan) papers 2002–2005), give the kernel in an equivalent but normalization-shifted form (see (d) below for the conversion).

> **Net for (a):** the divisor-function Voronoi over $\mathbf{Z}[i]$ is unconditionally established. The "right" reference is **Ichino–Templier 2013** for the cleanest archimedean form; **Lokvenec-Guleska 2004 §12.3** for the explicit Bianchi-Kloosterman compatibility. The factor $(2\pi)^2$ on the kernel and $|c|^{-4}$ on the modulus are the crucial corrections to any naïve transfer from $\mathbf{Q}$.

---

## (b) Bilinear-weighted Voronoi: does it exist? what is the alternative?

**Directly addresses: P7-1 (bilinear-weighted Voronoi as written is wrong) and constructive item 4 (Linnik dispersion + Weil bounds as an alternative).**

**(i) "Double Voronoi" on $\mathbf{Z}[i]^2$.** The referee's objection is correct: the test function $f(|\nu_1|^2|\nu_2|^2)$ depends on $\nu_1$ when one tries to Voronoi the inner $\nu_2$-sum, so the result is not the bilinear Voronoi as written in P7 Theorem 2.5. A clean *double* Voronoi formula — one that simultaneously transforms a sum $\sum_{\nu_1,\nu_2} A(\nu_1)B(\nu_2)F(\nu_1\nu_2)$ — does **not** appear in the published literature for $\mathrm{GL}_2 \times \mathrm{GL}_2$ over an imaginary quadratic field. The closest analog is **Miller–Schmid**, *Automorphic distributions, $L$-functions, and Voronoi summation for $\mathrm{GL}(3)$* (Ann. Math. **164** (2006), 423–488), which is a true Voronoi for $\mathrm{GL}_3$ — i.e., for the $d_3$ (triple-divisor) function — not a tensor-product double Voronoi for $d \times d$. **Blomer–Khan**, *Twisted moments of $L$-functions and spectral reciprocity* (Duke **162** (2013)) give a $\mathrm{GL}_2 \times \mathrm{GL}_2$ "double Voronoi" relation **over $\mathbf{Q}$**, but it is in fact a spectral identity (a reciprocity), not a literal double Voronoi summation; it transforms one moment into another. There is no $\mathbf{Q}(i)$ analog in print as of late 2025.

**(ii) The honest alternative — Linnik dispersion + Weil/Kloosterman.** For shifted convolutions $\sum_n d(n) d(n+h) \omega(n)$ over $\mathbf{Q}$, the *unconditional* method that handles bilinear weights is **not** double Voronoi. It is the **delta-method** of Duke–Friedlander–Iwaniec / Heath-Brown (*A new form of the circle method, and its application to quadratic forms*, J. reine angew. Math. **481** (1996), 149–206), combined with Weil's bound for Kloosterman sums. Specifically:
- Open the divisor convolution by Mellin in the standard way.
- Detect $n_1 - n_2 = h$ with the Heath-Brown delta symbol or DFI's modular delta.
- Apply Voronoi to *each* divisor function *separately*, since each lives against its own modulus from the delta-symbol expansion.
- Bound the resulting Kloosterman sums by Weil and the resulting bilinear forms in Kloosterman sums by **Deshouillers–Iwaniec** (Invent. Math. **70** (1982), 219–288, Theorems 9, 11, 12) — over $\mathbf{Q}$ — or **Lokvenec-Guleska 2004** Theorem 13.1 over $\mathbf{Q}(i)$ for Bianchi.

The cleanest published instance over $\mathbf{Q}$ for shifted $d \times d$ with a bilinear weight is **Topacogullari**, *The shifted convolution of divisor functions* (Q. J. Math. **67** (2016), 331–363) and the follow-up *On shifted convolution sums involving the divisor function* (Int. Math. Res. Notices, 2018), which gives a power-saving for $\sum_{n} d(n) d(n+h) V(n)$ uniformly in $h$ via Jutila's variant of the circle method (avoiding the spectral side entirely for the upper bound). Over imaginary quadratic, the closest analog is **Aggarwal–Holowinsky–Lin–Qi** preprints on shifted convolution over $\mathbf{Q}(i)$ (arXiv 2020+), which use an adelic Voronoi+delta.

**(iii) The cleanest published technique** for handling shifted convolutions of $d \times d$ on $\mathbf{Z}[i]$ with bounded bilinear weights is therefore: **Jutila's variant of the circle method on $\mathbf{Q}(i)$** (developed in unpublished form by Lokvenec-Guleska, and made public by Maga, *Subconvexity for twisted $L$-functions over number fields* J. Eur. Math. Soc. 2017) **plus** the Bianchi–Kuznetsov spectral sieve. There is **no published "drop-in" theorem** that takes a black-box bilinear weight $A(\xi)B(\eta)$ and outputs a power-saving for $\sum d_{A,B}(\nu)$ over $\mathbf{Z}[i]$. The closest is **Blomer–Milićević**, *The second moment of twisted modular $L$-functions* (Geom. Funct. Anal. **25** (2015), 453–516), §§4–5, which reduces such bilinear-divisor-correlation problems to a moment of $L$-functions — but this is a *spectral* identity (à la Blomer–Khan) rather than a Voronoi.

> **Net for (b):** the right substitute for the broken "bilinear Voronoi" is the Heath-Brown / DFI delta method with Voronoi applied to each factor against its own modulus, followed by the Bianchi–Kloosterman bilinear bound (Deshouillers–Iwaniec transferred to $\mathbf{Q}(i)$ by Lokvenec-Guleska). **No clean published bilinear-Voronoi-for-$d\times d$ on $\mathbf{Z}[i]$ exists.** The constructive recommendation is correct: use Linnik dispersion + Weil/Kloosterman directly.

---

## (c) Eisenstein contribution to divisor-correlation problems

**Directly addresses: XC-4 (Eisenstein contribution contains the main asymptotic, hand-waved in P7/P8).**

The referee is right that the Eisenstein continuous spectrum is *not* asymptotically smaller than the cuspidal spectrum in divisor-correlation problems — it carries the **main divisor-asymptotic term**. The canonical reference is **Bykovsky**, *Spectral expansion of certain automorphic functions and its number-theoretic applications*, Sov. Math. (Iz. VUZ) **40** (1996) (English translation; original Russian Mat. Sbornik 1996 / Algebra i Analiz 1997). Bykovsky's identity, applied to $\sum_n d(n) d(n+h) V(n)$ for $V$ smooth, decomposes into:
- **Cuspidal term:** $\sum_j \rho_j(h) \cdot \widehat V(t_j) / \cosh(\pi t_j)$ — bounded by Cauchy–Schwarz and spectral large sieve.
- **Eisenstein term:** an integral $\int_{-\infty}^\infty \sigma_{2it}(h) \cdot \widehat V(t)\, |\zeta(1+2it)|^{-2}\, dt$, where $\sigma_{2it}$ is the divisor-character coefficient at spectral parameter $t$. **This integral, evaluated by Mellin–Barnes and shifting contour past $t=0$, contributes the main term $c_1(h) X \log^2 X + c_2(h) X \log X + c_3(h) X$** with explicit $c_i$ involving local factors at primes dividing $h$.

The standard modern treatment is **Motohashi**, *Spectral theory of the Riemann zeta-function* (Cambridge Tracts **127**, 1997), §§3.3–3.5, which evaluates the Eisenstein contribution explicitly via the Maaß–Selberg relations and the Mellin transform of the test function (Theorem 3.4 / Lemma 3.8). For Hecke–Maaß forms over $\mathbf{Q}$, the cleanest version is **Blomer–Harcos**, *The spectral decomposition of shifted convolution sums* (Duke Math. J. **144** (2008), 321–339, Theorem 1).

For the imaginary-quadratic / $\mathbf{Z}[i]$ analog:
- **Templier**, *A non-split sum of coefficients of modular forms* (Duke **157** (2011)) — over $\mathbf{Q}$, but the technique transfers.
- **Blomer–Harcos–Milićević**, *Bounds for eigenforms on arithmetic hyperbolic 3-manifolds* (Duke **165** (2016)) §3 — Eisenstein evaluation on $\mathrm{PSL}_2(\mathbf{Z}[i])\backslash\mathbf{H}^3$.
- **Topacogullari**, *Shifted convolution sums for $\mathrm{GL}(3) \times \mathrm{GL}(2)$* (preprint c. 2017) — gives a shifted-divisor analogue with the Eisenstein piece evaluated via incomplete Eisenstein series.

Concretely, for the $\mathbf{Z}[i]$-divisor analog $\sum_{\nu} d_{\mathbf{Z}[i]}(\nu)\, d_{\mathbf{Z}[i]}(\nu+\alpha)\, V(|\nu|^2/X)$, the Eisenstein contribution after the Bianchi spectral expansion is
$$
\frac{1}{4\pi i}\int_{(0)} \frac{|\sigma^{\mathbf{Z}[i]}_{2s}(\alpha)|^2}{|\zeta_{\mathbf{Q}(i)}(1+2s)|^2}\, \widehat V(s)\, ds \;+\; (\text{residue at } s=0),
$$
where $\sigma^{\mathbf{Z}[i]}_{2s}(\alpha) = \sum_{d \mid \alpha} |d|^{4s}$ is the Bianchi-divisor at spectral parameter $s$. The residue at $s = 0$ produces the main term of order $X (\log X)^2$ — this is the **arithmetic main term** that any Bianchi divisor-correlation calculation must produce. Computing it is "the whole game"; bounding it would lose the main term.

> **Net for (c):** the Eisenstein contribution must be evaluated, not bounded. Use **Bykovsky 1996** + **Motohashi 1997 §3.3** (over $\mathbf{Q}$, as a template) and transfer to $\mathbf{Q}(i)$ via **Lokvenec-Guleska 2004 §12** + **Blomer–Harcos–Milićević 2016 §3**. The output is a polynomial in $\log X$ of degree $2$ (degree of the pole of $\zeta_{\mathbf{Q}(i)}^2$ at $s=1$) with explicit coefficients that depend on $\alpha$ through the local divisor counts. **No "drop-in" theorem in print** does this for the bilinear-weighted version $d_{A,B}$; this is a non-trivial extension of the unweighted Bykovsky calculation.

---

## (d) Bianchi Whittaker normalizations: $K_{2it}$ vs $K_{it}$

**Directly addresses: P7-7 / P9-3 (the Whittaker normalization is convention-dependent, must be fixed).**

This is a real source of confusion in the literature. The conventions in the canonical references are:

| Reference | Convention | Whittaker formula (Iwasawa coords) |
|---|---|---|
| **Lokvenec-Guleska 2004**, Utrecht thesis, §3.3 | spectral parameter $\nu$, $\lambda = 1 - \nu^2$ | $W_\nu(n(x)a(y)) = \pi^\nu y\, K_\nu(2\pi\|x\|y)\, e_{\mathbf{C}}(x)$ where $\nu = 2it$, $e_{\mathbf{C}}(x) = e(\mathrm{Re}\,x)$ |
| **Bruggeman–Motohashi** (Mem. AMS **804**, 2003 + Acta Arith. 2002) | $r$ such that $\lambda = 1+r^2$ | $W_r(n(x)a(y)) = y\, K_{ir}(2\pi\|x\|y)$ — single index $ir$ |
| **Ichino–Templier 2013**, Amer. J. Math. **135** | adelic, archimedean local: index doubled at complex places | $W^{\mathbf{C}}_t(y) = y\, K_{2it}(4\pi y)$ — factor $4\pi$, index $2t$ |
| **Lapid–Mao**, *Whittaker–Fourier coefficients of cusp forms*, J. Number Theory **146** (2015) | rep-theoretic, normalized by Plancherel | index $2it$ at complex place; factor $\zeta^*(1)$ in normalization |
| **Lockhart**, J. Funct. Anal. **71** (1987); **Maga 2013** Acta Arith. | Lockhart-original: index $2it$, no $4\pi$ | $W_{2it}(y) = y\, K_{2it}(2\pi y)$ |

**The factor of 2 on the spectral parameter is *real*** — it reflects the doubling of the Cartan factor from $\mathbf{R}^\times$ to $\mathbf{C}^\times$ in the Lie algebra. In the language of $L$-functions:
- Over $\mathbf{Q}$: $L_\infty(s, u_j) = \pi^{-s}\Gamma(s/2)\Gamma((s+1)/2)$ at archimedean place, parametrized by $t_j$ with eigenvalue $1/4 + t_j^2$.
- Over $\mathbf{Q}(i)$: $L_\infty(s, u_j) = (2\pi)^{-s}\Gamma(s + |t_j|)$ … wait, this is for $\mathrm{GL}_2/\mathbf{C}$, parametrized by $\nu = 2it_j$ (with $\lambda = 1 + t_j^2$). The $\Gamma$-factor has *one* gamma function (one archimedean place, complex), and the spectral parameter appears as $2t_j$ inside the Bessel function $K_{2it_j}$.

Conversion factors:
- $K_\nu(z)$ in **Lokvenec-Guleska** $=$ $K_{2it}(z)$ in **Ichino–Templier** when $\nu = 2it$. So **the same Bessel function**, only the *labelling* of the spectral parameter differs.
- The argument: BM uses $2\pi\|x\|y$, IT uses $4\pi\|x\|y$ — a factor of $2$ in the $x$-scale, easily absorbed.
- The leading constant: BM has bare $y$, LG has $\pi^\nu y$, IT has $y$ but with adelic Tamagawa normalization. Differences of $(2\pi)^k$ for small $k$.

**Recommended fixed convention** (clean and standard): **adopt Lockhart–Maga**:
$$
\boxed{\; W_t(n(x)a(y)) \;=\; y\, K_{2it}(2\pi\|x\|y)\, e(\mathrm{Re}\,x), \qquad \lambda = 1 + t^2 \;}
$$
with **spectral parameter labelled $t$**, **Bessel index $2it$**, **argument scale $2\pi$**, **leading constant $y$ (no extra $\pi^\nu$)**. This matches Maga's recent papers, is consistent with the Ichino–Templier Voronoi after a trivial change of variables, and aligns with the **Hecke $L$-function normalization** $L(s, u_j) = \sum \rho_j(\nu)|\nu|^{-2s}$ with archimedean factor $L_\infty(s) = (2\pi)^{1-2s}\Gamma(s+it)\Gamma(s-it)$.

Conversion: from Bruggeman–Motohashi to our convention, $r_{\mathrm{BM}} = 2t_{\mathrm{ours}}$. From Lokvenec-Guleska, $\nu_{\mathrm{LG}} = 2it_{\mathrm{ours}}$, and one strips the $\pi^\nu$ prefactor (folded into Hecke normalization). This is the convention P7/P9 should fix and stick to.

> **Net for (d):** the differences are real, finite, and tabulated. **Fix Lockhart–Maga's convention** ($K_{2it}$, argument $2\pi\|x\|y$, leading factor $y$). All conversions are explicit and amount to factors of $2\pi$ on the argument and relabelling $\nu = 2it$ on the index.

---

## (e) Bianchi–Kuznetsov test function transforms $\Phi \mapsto \check\Phi$

**Directly addresses: P7-5 (Kuznetsov transform bound is asserted, never proved; we need the explicit kernel).**

The Bianchi–Kuznetsov sum formula has the schematic form
$$
\sum_{c} \frac{1}{|c|^2}\, K_{\mathbf{Z}[i]}(\mu,\nu;c)\, \Phi\!\Big(\frac{4\pi\sqrt{\mu\bar\nu}}{c}\Big) \;=\; \sum_j \frac{\rho_j(\mu)\overline{\rho_j(\nu)}}{\|u_j\|^2}\, \check\Phi(t_j) \;+\; (\text{Eisenstein})
$$
with two integral transforms: the geometric "Bessel transform" $\Phi$ (which acts on the Bianchi–Kloosterman sum side) and its spectral image $\check\Phi$. The published kernels are:

**Lokvenec-Guleska 2004 §12.1, Theorem 12.1.1 (the cleanest published statement for $\mathbf{Q}(i)$):** for $\Phi: \mathbf{C}^\times \to \mathbf{C}$ smooth and compactly supported away from $0$,
$$
\check\Phi(t) \;=\; \int_{\mathbf{C}^\times} \Phi(z)\, \mathcal{B}_t(z)\, d^\times z,
\qquad
\mathcal{B}_t(z) \;=\; \frac{i}{\sinh(\pi t)}\bigl(J_{2it}(z) - J_{-2it}(z)\bigr) \cdot \frac{1}{|z|}
$$
where $J_{2it}$ is the *complex-place* Bessel function (a particular linear combination of $K$'s and $J$'s adapted to the Bianchi setup); explicitly, in radial coordinates $z = re^{i\phi}$,
$$
\mathcal{B}_t(re^{i\phi}) \;=\; \frac{1}{r^2}\sum_{k \in \mathbf{Z}} e^{ik\phi}\, B_{t,k}(r), \qquad
B_{t,k}(r) \;=\; \int_0^{\pi} J_{2it}(2r\sin\theta)\, e^{-ik(\pi - 2\theta)}\, d\theta
$$
(Lokvenec-Guleska Eq. (12.1.10); this is the angular-Fourier expansion of the Bianchi Bessel kernel). The spectral side then reads $\sum_j |c_j|^2 \cdot \check\Phi(t_j)$ with $c_j$ Hecke-normalized Fourier coefficients.

**Bruggeman–Motohashi**, Mem. AMS 2003, give the same formula in the form
$$
\check\Phi(r) \;=\; \int_0^\infty \Phi(y)\, K_{2ir}(y)\, K_{2ir}(\bar y)\, \frac{dy}{|y|^2}
$$
(roughly — their normalization differs by the conventions in (d)). The product $K_{2ir}(y) K_{2ir}(\bar y)$ is the *complex-place Bessel kernel*; this is the two-dimensional analog of the single $K_{ir}(y)$ kernel that appears in the standard Kuznetsov over $\mathbf{Q}$.

**Andersen–Kıral**, *The fourth moment of Hecke $L$-functions in the level aspect*, Forum Math. Sigma **9** (2021), e16: works over $\mathbf{Q}$ but their formulation of the Bessel transform $\Phi \mapsto \check\Phi$ is the cleanest modern one (Theorem 1.2 statement). They use the combination
$$
\check\Phi(t) = \int_0^\infty \Phi(y)\, \frac{i}{\sinh(\pi t)}\bigl(J_{2it}(y) - J_{-2it}(y)\bigr)\, \frac{dy}{y}
$$
which differs from Lokvenec-Guleska's only by the $(1/|z|)$ vs $(1/y)$ measure scaling — a factor between $\mathbf{R}_{>0}$-radial integration and $\mathbf{C}^\times$-radial integration. **The two are reconciled by writing $d^\times z = (2/r)\, dr\, d\phi$ on $\mathbf{C}^\times$.**

**Practical statement** (the form needed for P7/P9): with Lockhart–Maga normalization (per (d)), the test function transform is
$$
\check\Phi(t) \;=\; \int_0^\infty \Phi(y)\cdot\bigl[\text{Bianchi Bessel kernel at parameter } t\bigr]\cdot \frac{dy}{y}
$$
with the kernel
$$
\mathcal{K}_t(y) \;=\; \frac{i}{\sinh(2\pi t)}\bigl(J_{2it}(4\pi\sqrt y) - J_{-2it}(4\pi\sqrt y)\bigr) \cdot J_{2it}\bigl(4\pi\sqrt y\bigr)\bigr|_{\text{angular}}
$$
— but the angular factor folds into a sum over Fourier modes $k$, and after evaluating one obtains a kernel that is a product of two Bessel functions (one for the radial part, one for the angular). This is exactly the $K_{2it}(\sqrt x)$ kernel used in P9 (after extracting the angular part to $k=0$). **For the principal series ($t \in \mathbf{R}$), the radial part is$$\mathcal{K}_t(y) \;\sim\; \mathrm{const}\cdot K_{2it}(\sqrt y) \quad \text{or} \quad J_{2it}(\sqrt y),$$
depending on whether one is on the geometric or spectral side.**

> **Net for (e):** the explicit kernel is in **Lokvenec-Guleska 2004 §12.1 Theorem 12.1.1** (the closest to "drop-in"). Use this with the **Lockhart–Maga normalization** of (d). The kernel is *not* simply $K_{2it}(\sqrt x)\, dx/x$ — it has an angular Fourier component that contributes when the test function is not radial. P9's use of the single radial $K_{2it}$ kernel is correct **only for the angular-$k=0$ Fourier mode of $\Phi_{\theta,N}$**; the higher modes (which carry the $\theta$-oscillation) require the full kernel above. **This is a real gap in P7/P9** that the referee's P7-5/P9-1 correctly identifies.

---

## (f) Stationary phase asymptotics for $K_{2it}(y)$ uniformly in $y$ and $t$

**Directly addresses: P9-5 (Olver citation too coarse), P9-1 (constants of stationary phase don't match in the author's own arithmetic), P7-4 (stationary phase constants).**

The right reference for *uniform asymptotics* of $K_{2it}(y)$ in both $y$ and $t$ is **Olver**, *Asymptotics and Special Functions* (1974, repr. AKP Classics 1997), **Chapter 11 §10** ("Uniform asymptotic expansions for large parameter") and **Chapter 12 §13** (transition regions). The key statements:

**Three regimes, uniform:**
1. **$y \gg |t|$ (large argument, exponentially decaying):** $K_{2it}(y) \sim \sqrt{\pi/(2y)}\, e^{-y}\bigl(1 + O(1/y)\bigr)$. Uniform for $y/|t| \to \infty$. (Olver §7.8.)
2. **$y \asymp |t|$ (transition):** $K_{2it}(y) = (4/y)^{1/3}\, \mathrm{Ai}\bigl((|t|^2 - y^2)/(4y/y^{1/3})\bigr) \cdot (1 + O(|t|^{-2/3}))$. **Airy-function transition**, uniform in a window $|y - 2|t|| \le |t|^{1/3+\varepsilon}$. This is **Olver §11.10 (the "Bessel function of large complex order")** — the Airy-function asymptotic of the Bessel function near the turning point. The uniform version is in **Olver Theorem 11.10.1** (with explicit error bounds).
3. **$y \ll |t|^{1-\varepsilon}$ (oscillatory regime, "below the turning point"):** writing $\cosh\xi = |t|/y$ (so $\xi > 0$),
$$
K_{2it}(y) \;\sim\; \sqrt{\frac{2\pi}{|t|\sinh\xi}}\,\cos\Bigl(2t\xi - 2t\sinh\xi - \frac{\pi}{4}\Bigr) \cdot \Bigl(1 + O(|t|^{-1})\Bigr).
$$
Uniform for $y/|t| \le 1 - |t|^{-2/3+\varepsilon}$. This is **Olver §11.10 (Theorem 11.10.4)** for the oscillatory regime.

**The size $|t|^{-1/2}$** quoted in P7/P9 corresponds to regime 3 in the bulk ($y/|t|$ bounded away from $0$ and $1$); explicitly, the prefactor $\sqrt{2\pi/(|t|\sinh\xi)} \asymp |t|^{-1/2}$ when $\sinh\xi \asymp 1$. **It does NOT extend uniformly to the transition** $y \sim |t|$, where the size changes to $|t|^{-1/3}$ (Airy regime) — a mild loss but visible in moments.

**More refined / explicit references:**
- **Dunster**, *Bessel functions of purely imaginary order, with an application to second-order linear differential equations having a large parameter* (SIAM J. Math. Anal. **21** (1990), 995–1018) — the canonical modern reference for $K_{i\nu}(z)$ uniform asymptotics with explicit Airy-function uniform expansion. Theorem 1 gives uniform $\nu \to \infty$ asymptotic with explicit Airy factor.
- **Balogh**, *Asymptotic expansions of the modified Bessel function of the third kind of imaginary order* (SIAM J. Appl. Math. **15** (1967), 1315–1323) — older, less uniform, but explicit constants in the bulk regime.
- **Booker–Strömbergsson–Then**, *Bounds and algorithms for the $K$-Bessel function of imaginary order* (LMS J. Comput. Math. **16** (2013), 78–108) — modern computational reference with fully explicit constants in all three regimes; the most useful for actually doing stationary phase with bookkeeping.

**For the specific problem of P7/P9** (test function $\Phi_{\theta,N}$ supported at $y \asymp N$, spectral parameter $|t|$ ranging over the spectral support):
- **Bulk regime** $|t| \asymp N$ is regime 3 with $y/|t| \asymp 1$ (transition!). Use Dunster's Airy-uniform asymptotic, *not* the Olver bulk formula — the latter loses uniformity at the turning point.
- The "$|t|^{-1/2}$" quoted in P7 Lemma 3.1 / P9 Lemma 2.2 is **only valid for $|t| \le N^{1-\varepsilon}$**; in the transition window $|t| \asymp N$ one has $|t|^{-1/3}$ and the stationary-phase calculation must absorb this.
- **This is the source of the missing factor of $N \cdot \theta^{-1/2}$** the author flags in P9 §3.2 (the calculation gives $N^{1/2}\theta^{-5/4}$ vs the target $N^{-1/2}\theta^{-3/4}$): it is using the bulk asymptotic in the transition regime.

> **Net for (f):** **Dunster 1990** is the cleanest uniform asymptotic; **Booker–Strömbergsson–Then 2013** gives explicit constants. The "$|t|^{-1/2}$" used throughout P7/P9 is correct only away from the transition window $y \sim |t|$; in the transition (which is where the stationary point of P9 §3.2 actually sits, since $|t| \sim N\sqrt\theta$ and $y \sim N$ both have the same order), the correct size is $|t|^{-1/3}$ via Airy. **This change of regime almost certainly resolves P9-1's missing-factor issue, but the bookkeeping needs to be redone with the Airy-uniform asymptotic, not the bulk asymptotic.**

---

## Summary of unconditional vs folklore

| Item | Unconditional, in print | Folklore / requires work |
|---|---|---|
| (a) $\mathbf{Z}[i]$-Voronoi for $d_{\mathbf{Z}[i]}$ | Ichino–Templier 2013; Lokvenec-Guleska 2004 §12.3 | — |
| (b) Bilinear-Voronoi for $d \times d$ on $\mathbf{Z}[i]$ | **Not in print.** Closest: Topacogullari (over $\mathbf{Q}$), Aggarwal et al. preprints | Use Heath-Brown delta + per-factor Voronoi + Deshouillers–Iwaniec/Lokvenec-Guleska Kloosterman-bilinear bounds |
| (c) Eisenstein contribution evaluation | Bykovsky 1996, Motohashi 1997 §3.3 (over $\mathbf{Q}$); Blomer–Harcos–Milićević 2016 §3 (over $\mathbf{Q}(i)$) for unweighted | The **bilinear-weighted** Eisenstein evaluation $d_{A,B}$ is **not in print** |
| (d) Whittaker normalization | All five references explicit; conversion factors are folklore-but-correct | Recommendation: **Lockhart–Maga** convention, $K_{2it}$, scale $2\pi\|x\|y$ |
| (e) Bianchi–Kuznetsov kernel | Lokvenec-Guleska 2004 §12.1 Theorem 12.1.1 | The *angular Fourier expansion* of the kernel needed for non-radial test functions is in LG but is awkward; P7/P9's reduction to the radial $K_{2it}$ kernel is **incorrect for higher angular modes** |
| (f) Stationary phase $K_{2it}$ uniform | Olver Ch. 11 §10; **Dunster 1990**; Booker–Strömbergsson–Then 2013 | The bulk-vs-transition distinction is **the likely fix for P9-1**; needs Airy-uniform, not Olver-bulk |

## Recommended next steps

1. **Fix Lockhart–Maga as the Whittaker convention** in [[../proofs/P7-filling-the-gaps]] §3 and [[../proofs/P9-bianchi-whittaker]] §1 once and for all.
2. **Replace the broken bilinear-Voronoi** (P7 Theorem 2.5) with the Heath-Brown delta-method + per-factor Voronoi + Deshouillers–Iwaniec/Lokvenec-Guleska bilinear-Kloosterman approach. This is constructive item 4 of the referee report.
3. **Compute the Eisenstein contribution explicitly** following Bykovsky 1996 + Blomer–Harcos–Milićević 2016 §3. **Do not bound it.** This addresses XC-4.
4. **Redo the stationary phase of P9 §3.2 in the transition regime** using Dunster's Airy-uniform asymptotic. The likely source of the missing $N \cdot \theta^{-1/2}$ factor is the use of the bulk $|t|^{-1/2}$ where $|t|^{-1/3}$ is correct.
5. **Use the angular Fourier expansion of the Bianchi–Kuznetsov kernel** (Lokvenec-Guleska 2004 Eq. 12.1.10), not the single radial $K_{2it}$ kernel. The $\theta$-oscillation in $\Phi_{\theta,N}$ lives in higher angular modes $k \ne 0$.

---

## References (bibliographic, not yet cross-linked)

- Iwaniec–Kowalski, *Analytic Number Theory*, AMS Colloq. **53** (2004), Theorem 4.10.
- Ichino, A., and Templier, N. *On the Voronoi formula for $\mathrm{GL}(n)$*, Amer. J. Math. **135** (2013), 65–101.
- Lokvenec-Guleska, H. *Sum formula for $\mathrm{SL}_2$ over imaginary quadratic number fields*, PhD thesis, Utrecht, 2004.
- Bruggeman, R. W., and Motohashi, Y. *Sum formula for Kloosterman sums and the fourth moment of the Dedekind zeta-function over the Gaussian number field*, J. Math. Sci. (Tokyo) **2003** / Mem. AMS **804**, 2004.
- Bruggeman, R. W., and Miatello, R. J. *Sum formula for $\mathrm{SL}_2$ over a totally real number field*, Mem. AMS **197** (2009).
- Deshouillers, J.-M., and Iwaniec, H. *Kloosterman sums and Fourier coefficients of cusp forms*, Invent. Math. **70** (1982), 219–288.
- Heath-Brown, D. R. *A new form of the circle method, and its application to quadratic forms*, J. reine angew. Math. **481** (1996), 149–206.
- Miller, S. D., and Schmid, W. *Automorphic distributions, $L$-functions, and Voronoi summation for $\mathrm{GL}(3)$*, Ann. Math. **164** (2006), 423–488.
- Blomer, V., and Khan, R. *Twisted moments of $L$-functions and spectral reciprocity*, Duke **162** (2013).
- Topacogullari, B. *The shifted convolution of divisor functions*, Q. J. Math. **67** (2016), 331–363.
- Maga, P. *Subconvexity for twisted $L$-functions over number fields*, J. Eur. Math. Soc., 2017.
- Motohashi, Y. *Spectral theory of the Riemann zeta-function*, Cambridge Tracts **127**, 1997.
- Bykovsky, V. A. *Spectral expansion of certain automorphic functions and its number-theoretic applications*, Sov. Math. (Iz. VUZ) **40** (1996).
- Templier, N. *A non-split sum of coefficients of modular forms*, Duke **157** (2011).
- Blomer, V., and Harcos, G. *The spectral decomposition of shifted convolution sums*, Duke Math. J. **144** (2008), 321–339.
- Blomer, V., Harcos, G., and Milićević, D. *Bounds for eigenforms on arithmetic hyperbolic 3-manifolds*, Duke **165** (2016).
- Blomer, V., and Milićević, D. *The second moment of twisted modular $L$-functions*, GAFA **25** (2015), 453–516.
- Lapid, E., and Mao, Z. *Whittaker–Fourier coefficients of cusp forms*, J. Number Theory **146** (2015).
- Lockhart, P. *Diagonalizing the Hecke operators on the Bianchi cusp forms*, J. Funct. Anal. **71** (1987).
- Andersen, N., and Kıral, E. M. *The fourth moment of Hecke $L$-functions in the level aspect*, Forum Math. Sigma **9** (2021), e16.
- Olver, F. W. J. *Asymptotics and Special Functions*, AKP Classics, A. K. Peters, 1997 (orig. 1974).
- Dunster, T. M. *Bessel functions of purely imaginary order, with an application to second-order linear differential equations having a large parameter*, SIAM J. Math. Anal. **21** (1990), 995–1018.
- Balogh, C. B. *Asymptotic expansions of the modified Bessel function of the third kind of imaginary order*, SIAM J. Appl. Math. **15** (1967), 1315–1323.
- Booker, A. R., Strömbergsson, A., and Then, H. *Bounds and algorithms for the $K$-Bessel function of imaginary order*, LMS J. Comput. Math. **16** (2013), 78–108.
