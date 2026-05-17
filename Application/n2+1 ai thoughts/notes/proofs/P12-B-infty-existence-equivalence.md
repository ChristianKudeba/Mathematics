# P12 — Existence of $B^\infty$ ⇔ existence of $c_0^T$: rigorous equivalence via $B(N) = U(N) - T(N)/2$

**Session.** 2026-05-08 (UTC). Builds on:
- `P12-c0T-AB-decomposition.md` — the structural identity
  $T_<(N) = T_{\rm half}(N) + A(N) + B(N)$ and the closed form
  $A(N) = R H(1)\cdot N + O_A(N(\log N)^{-A})$.
- `P12-c0T-secondary-constant.md` — Cor 3.2:
  $T_<(N) = R H(1)\cdot N\log N + (R H'(1) + \gamma_K H(1))\,N + o(N)$.

Goal: convert the conditional "$c_0^T = 1.158725 - 2 B^\infty$ modulo existence
*and* value of $B^\infty$" to "**$B^\infty$ exists iff $c_0^T$ exists**", with
an explicit relationship between the two limits.

Notation: $K = \mathbb Q(i)$, $R = \pi/4$, $a_1 := R H(1) = 0.434068$;
$c_<^\infty := R H'(1) + \gamma_K H(1) = 1.013430$ (rigorous via SD).
$\rho(d) := \#\{x \in \mathbb Z/d\mathbb Z : x^2 \equiv -1 \pmod d\}$.
$r(n) := \mathrm{rad}(n^2+1)$, $\omega(n) := \omega(n^2+1)$.

## 1. A pointwise complementary-divisor identity for $b(n)$

Recall the per-$n$ summand of $B(N)$:
$$b(n) := \#\{e \,\mathrm{sf}\mid n^2+1 : \sqrt{r(n)} < e \le n\},\qquad B(N) = \sum_{n=1}^N b(n).$$

(For squarefree $n^2+1$ the set is empty — $\sqrt{r} \in (n,n+1)$ — so $b$ is
automatically zero on sf $n^2+1$ without needing to spell out the indicator.)

**Lemma 1.1 (complementary-divisor identity).** *For every $n \ge 1$,*
$$b(n) = \#\{e \,\mathrm{sf}\mid n^2+1 : e \le n\} - 2^{\omega(n^2+1) - 1}.$$

*Proof.* Squarefree divisors of $n^2+1$ are exactly divisors of $r := r(n)$. As
$r$ is squarefree and $r \ge 2$ for $n \ge 1$, $r$ is not a perfect square, so
$\#\{e \mid r\} = 2^{\omega}$ partitions into the disjoint halves
$\{e \le \sqrt r\}$ and $\{e > \sqrt r\}$, each of size $2^{\omega-1}$ (no fixed
point $e = \sqrt r$).

*Case 1: $n^2+1$ squarefree.* Then $r = n^2+1$, $\sqrt r \in (n, n+1)$, so the
divisors $e \le n$ are exactly the divisors $e \le \sqrt r$ (cardinality
$2^{\omega-1}$). RHS $= 2^{\omega-1} - 2^{\omega-1} = 0 = b(n)$. ✓

*Case 2: $n^2+1$ not squarefree.* Then $r \le (n^2+1)/4 < n^2$, hence
$\sqrt r < n$. Partition $\{e \mid r\}$ by the threshold $\sqrt r$:
$\{e \mid r : e \le n\} = \{e \mid r : e \le \sqrt r\}\,\sqcup\,\{e \mid r : \sqrt r < e \le n\}$,
giving $\#\{e\mid r : e \le n\} = 2^{\omega-1} + b(n)$. ✓ $\square$

Numerical check (Python, $n \le 5000$): the identity holds with zero
mismatches; cumulative sums agree exactly.

## 2. The $B = U - T/2$ identity

Define
$$U(N) := \sum_{n=1}^N \#\{e \,\mathrm{sf}\mid n^2+1 : e \le n\}.$$

Summing Lemma 1.1 and using Hooley's identity
$\sum_n 2^{\omega-1} = T_{\rm half}(N) = T(N)/2$:

**Theorem 2.1.** *For every $N \ge 1$,*
$$\boxed{\,B(N) = U(N) - \tfrac{1}{2}\,T(N).\,}$$

This is an exact integer identity (the prefactor $1/2$ on $T$ is benign:
$T(N)$ is automatically even as $T = 2\,T_{\rm half}$).

Verified exactly at $N \in \{10^3, 3\!\cdot\!10^3, 10^4, 3\!\cdot\!10^4\}$:
$U - T/2 - B = 0$ in each case.

Cross-check at $N = 10^4$: $U(10^4) = 45763$, $T(10^4) = 89766$,
$U - T/2 = 45763 - 44883 = 880 = B(10^4)$ ✓ (matching the table in
`P12-c0T-AB-decomposition.md`).

## 3. Rigorous SD asymptotic for $U(N)$

**Lemma 3.1 (exact form, up to $O(1)$).** *For every $N \ge 1$,*
$$U(N) = N \cdot \Sigma_*(N) - \tfrac{1}{2}\,A(N) - F(N) + R_1,\qquad |R_1| \le 1,$$
*where*
$$\Sigma_*(N) := \sum_{e \,\mathrm{sf}, e \le N}\frac{\rho(e)}{e},\qquad A(N) := \sum_{e \,\mathrm{sf}, 2 \le e \le N}\rho(e),\qquad F(N) := \sum_{\substack{e \,\mathrm{sf}, e \ge 2\\ e \le N}}\sum_{i=1}^{\rho(e)}\!\Big\{\tfrac{N - r_i^{(e)}}{e}\Big\},$$
*and $\{r_1^{(e)}, \ldots, r_{\rho(e)}^{(e)}\}$ are the roots of $x^2 \equiv -1 \pmod e$ in $[1, e-1]$ (well-defined and nonzero for $e \ge 2$ with $\rho(e) \ge 1$).*

*Proof.* Exchange $\sum_n \sum_e$: $U(N) = \sum_{e \,\mathrm{sf}, e \le N} \#\{n : e \le n \le N,\, e\mid n^2+1\}.$

*Contribution from $e = 1$.* $\rho(1) = 1$ (trivial residue class), $e \le n$ holds for all $n \ge 1$, and $1 \mid n^2+1$ always — count $= N$.

*Contribution from $e \ge 2$.* The roots $r_i \in [1, e-1]$ all satisfy $r_i < e$, so they lie *outside* $[e, N]$. Solutions to $e \mid n^2+1$ in $[e, N]$ are $\{r_i + ke\}_{k \ge 1}$, count $= \sum_{i=1}^{\rho(e)} \lfloor (N - r_i)/e \rfloor$. Using $\lfloor x \rfloor = x - \{x\}$ and the pairing identity $\sum_i r_i = \rho(e)\,e/2$ (valid for all $e \ge 2$; cf. Cor 3.2 of `P12-c0T-secondary-constant.md`, which checks $e = 2$ separately):
$$\sum_i \lfloor (N - r_i)/e \rfloor = \rho(e)\,N/e - \rho(e)/2 - \sum_i \{(N-r_i)/e\}.$$

Sum over all sf $e \le N$:
$$U(N) = N + \sum_{e \,\mathrm{sf}, 2 \le e \le N}\Big[\rho(e)\,N/e - \rho(e)/2 - \sum_i\{\cdot\}\Big] = N + N\,\big(\Sigma_*(N) - 1\big) - \tfrac{1}{2} A(N) - F(N) = N\,\Sigma_*(N) - \tfrac{1}{2}A(N) - F(N).$$

The $e=1$ contribution $N$ is identified with the $e=1$ summand of $N\,\Sigma_*(N)$ (which is $N \cdot \rho(1)/1 = N$). No remainder. So actually $R_1 = 0$ exactly. $\square$

**Remark.** The earlier draft of this lemma carried a fudgy "$\tfrac{1}{2}(A(N)+1)$" trying to absorb a phantom $e=1$ correction; the skeptic correctly flagged this. The correct version separates the $e=1$ contribution from the start (it produces the leading "$N$"), and only the $e \ge 2$ part contributes to $A(N)$, $F(N)$, and the "$-\rho(e)/2$" pairing-identity correction. No "$+1$" is needed.

**Lemma 3.2 (Tauberian for $\Sigma_*$).** *Rigorous via SD with $\kappa = 1$ on
$G(s+1) = \zeta_K(s+1) H(s+1)$, simple pole at $s = 0$:*
$$\Sigma_*(N) = a_1\,\log N + c_<^\infty + O((\log N)^{-A})\qquad\text{for any }A \ge 1.$$
(Lemma 3.1 of `P12-c0T-secondary-constant.md`.)

**Lemma 3.3 (SD for $A$).** *Rigorous via SD with $\kappa = 1$ on $G(s) = \zeta_K(s) H(s)$:*
$$A(N) = a_1\,N + O_A(N(\log N)^{-A}).$$
(Lemma 3 of `P12-c0T-AB-decomposition.md`.)

**Lemma 3.4 (fractional-part on-average bound).** *Modulo the same Erdős–Hooley
discrepancy bound assumed in Cor 3.2 of the secondary-constant note (and used by
Hooley 1957 §3 for $\tau$), as $N \to \infty$:*
$$F(N) = \tfrac{1}{2}\,A(N) - \tfrac{1}{2}\Sigma_*(N) + \tfrac{1}{2} + o(N).$$

(The "$+\tfrac{1}{2}$" is the $e = 1$ exclusion correction: the sum $F$ excludes
$e = 1$, whose "expected" $\{N/1\} = 0$ vs $\langle\cdot\rangle = 1/2$ contributes
$+1/2$ to the difference $F - \langle F \rangle$. It is $O(1)$ and absorbed in
$o(N)$.)

*Proof sketch.* For each $e \ge 2$, the expectation of $\sum_i \{(N - r_i)/e\}$
over $N \pmod e$ uniform is $\rho(e)\cdot\tfrac{1}{2}(1 - 1/e) = \rho(e)/2 - \rho(e)/(2e)$;
summing over sf $e \in [2, N]$ gives $\tfrac{1}{2}A(N) - \tfrac{1}{2}(\Sigma_*(N) - 1) = \tfrac{1}{2}A(N) - \tfrac{1}{2}\Sigma_*(N) + \tfrac{1}{2}$.
Pointwise deviation from this expectation — the joint discrepancy of
$\rho$-many fractional parts $\{(N - r_i^{(e)})/e\}$ across sf $e \le N$ — is
at most $O(\sqrt N (\log N)^c)$ by a large-sieve / mean-value argument
(Hooley 1957 §3 establishes the analogue for the $\tau$ sum; Erdős–Hooley
delta-function methods give the $\tau^*$ analog). For our purposes, the
qualitative bound $o(N)$ suffices and is the *exact same input* used in
`P12-c0T-secondary-constant.md` Cor 3.2 to establish $T_<(N) = a_1 N\log N + c_<^\infty N + o(N)$.

**Honest framing.** Rigorizing Lemma 3.4 is the unfinished step in the
predecessor's Cor 3.2; it is unfinished here too. This note does NOT advance
the rigorization of that bound. What this note DOES achieve is showing that
the *same* unfinished step — and no additional unfinished step — is what
stands between current rigor and "$B^\infty$ exists in closed form modulo
the value of $B^\infty$". $\square$

**Theorem 3.5 (asymptotic for $U(N)$).** *Modulo the fractional-part bound in
Lemma 3.4, as $N \to \infty$:*
$$U(N) = a_1\,N\log N + (c_<^\infty - a_1)\,N + o(N).$$

*Proof.* From Lemma 3.1, $U(N) = N\,\Sigma_*(N) - \tfrac{1}{2}A(N) - F(N)$.
Substitute Lemma 3.4 ($F = \tfrac{1}{2}A - \tfrac{1}{2}\Sigma_* + o(N)$):
$$U(N) = N\,\Sigma_*(N) - \tfrac{1}{2}A(N) - \tfrac{1}{2}A(N) + \tfrac{1}{2}\Sigma_*(N) + o(N) = N\,\Sigma_*(N) - A(N) + \tfrac{1}{2}\Sigma_*(N) + o(N).$$
Substitute Lemmas 3.2, 3.3:
$$U(N) = N(a_1\log N + c_<^\infty) - a_1 N + \tfrac{1}{2}(a_1\log N + c_<^\infty) + o(N) = a_1 N\log N + (c_<^\infty - a_1) N + O(\log N) + o(N).$$
$O(\log N)$ is $o(N)$, so $U(N) = a_1 N\log N + (c_<^\infty - a_1)N + o(N)$. $\square$

**Numerical confirmation:** $U(N)/N - a_1\log N$ should approach $c_<^\infty - a_1 = 0.579362$:

| $N$ | $U(N)/N - a_1\log N$ | gap to $0.579362$ |
|---|---|---|
| $10^3$ | $0.576567$ | $-2.8\cdot10^{-3}$ |
| $3\cdot 10^3$ | $0.581695$ | $+2.3\cdot10^{-3}$ |
| $10^4$ | $0.578389$ | $-1.0\cdot10^{-3}$ |
| $3\cdot10^4$ | $0.578350$ | $-1.0\cdot10^{-3}$ |

Empirical convergence is consistent with $o(N)$ remainder. Sub-percent gap at
$N = 3\cdot10^4$ is fully consistent with the heuristic $O(N^{-1/2})$ rate of the
fractional-part discrepancy — and matches the analogous gap pattern of the
$T_<$ asymptotic (which uses the same Lemma 3.4).

## 4. Equivalence theorem and the value formula

Combining Theorem 2.1 with Theorem 3.5:

$$\frac{B(N)}{N} = \frac{U(N)}{N} - \frac{T(N)}{2N} = a_1 \log N + (c_<^\infty - a_1) + o(1) - \frac{1}{2}\cdot\frac{T(N)}{N}.$$

Equivalently:
$$\frac{T(N)}{N} - 2\,a_1\log N = 2(c_<^\infty - a_1) - \frac{2\,B(N)}{N} + o(1).$$

Since $c_1 = 2 a_1$, the LHS is $T(N)/N - c_1 \log N$, whose limit (if it exists) is
$c_0^T$.

**Theorem 4.1 (equivalence and value).** *Modulo Lemmas 3.2–3.4,*

(a) $B^\infty := \lim_{N\to\infty} B(N)/N$ *exists* $\iff c_0^T := \lim_{N\to\infty} (T(N)/N - c_1\log N)$ *exists*.

(b) *When either limit exists, both do, and they are linked by*
$$c_0^T = 2(c_<^\infty - a_1) - 2 B^\infty,\qquad B^\infty = (c_<^\infty - a_1) - c_0^T/2.$$

*Numerically* $2(c_<^\infty - a_1) = 2 \cdot 0.579362 = 1.158725$, recovering the
boxed formula of `P12-c0T-AB-decomposition.md` §4 unconditionally on $B^\infty$.

(c) *In particular, with the empirical $B^\infty \approx 0.085704$ (heuristic
closed form, validated to $\pm 5\cdot 10^{-6}$ at $N = 3\cdot 10^7$ in
`P12-c0T-N3e7-rate.md`), the predicted $c_0^T = 1.158725 - 2\cdot 0.085704 = 0.987317$.*

*Proof.* Direct from Theorem 2.1 and Theorem 3.5. The forward direction "$B^\infty$
exists $\Rightarrow c_0^T$ exists" follows because $T(N)/N - c_1\log N = 2(U(N)/N - a_1\log N) - 2 B(N)/N$, both terms convergent. The reverse direction is the same identity. $\square$

## 5. Strategic significance: what's left

Theorem 4.1 reduces "existence of $B^\infty$" to "existence of secondary
asymptotic for $\sum_{n \le N} 2^{\omega(n^2+1)}$".

The latter is the **Hooley-1957-analog question for $\tau^*$**: Hooley proved
$\sum \tau(n^2+1) = c\, N \log N + O(N\log\log N)$ for an explicit $c$. The
secondary $O(N\log\log N)$ was Hooley's bound; the existence of a true linear
secondary $c_0\, N + o(N)$ asymptotic for the $\tau$ sum is established (e.g.,
Friedlander–Iwaniec for related sums, Tenenbaum's comprehensive treatment).
For $\tau^*(n^2+1) = 2^{\omega(n^2+1)}$, the same Selberg–Delange chain on
$\zeta_K(s)^\kappa H(s)$ should give the secondary asymptotic; this is the
direct analog and is "morally" rigorous via the same machinery as Cor 3.2.

**What this session achieves:** the existence of $B^\infty$ no longer requires a
*new* unrigorized step. It rests on the *same* Erdős–Hooley discrepancy bound
(Lemma 3.4) that the prior session's Cor 3.2 already invokes — literally the same
$F(N)$ object, with the same target asymptotic $F(N) = \langle F \rangle + o(N)$.

**Restricted claim:** *if* the rigorization of $c_0^T$ proceeds via the same
$T_<(N) - T_{\rm half}(N)$ structural identity used here (i.e., via Lemma 3.4),
then it automatically rigorizes $B^\infty$ existence and vice versa. A
rigorization of $c_0^T$ via a *different* route (e.g., direct
$\zeta_K(s)^\kappa H_\kappa(s)$ Selberg–Delange on the Dirichlet series of
$2^{\omega(n^2+1)}$ at $s = 1$, treating $T(N)$ as a level-3 sieve sum)
would not necessarily yield Lemma 3.4 — the equivalence $B^\infty \leftrightarrow c_0^T$
is *equivalence of their existence as limits*, not equivalence of all proof routes.

**What is genuinely collapsed:** the "two unknowns $B^\infty$ existence and
$B^\infty$ value" become "one unknown $B^\infty$ value modulo whatever rigorizes
$c_0^T$". Until last session, $B^\infty$ was both unknown-to-exist and
unknown-in-value (modulo heuristics); now exact-existence is paired with
exact-existence of $c_0^T$ — itself a Hooley-1957-analog question whose proof
is in reach for the $\tau$ case and morally the same for $\tau^*$.

## 6. Skeptic dialogue summary

(See the session log for full skeptic correspondence.)

**Known soft spots in the proof chain:**
- Lemma 3.4 cites Hooley 1957 §3 / Erdős–Hooley delta-function, which is
  standard in the divisor literature but not freshly verified in this
  repository. The rigorization is "modulo standard Halász–Tenenbaum sieve
  analytics".
- Lemma 3.3 (existence of $A^\infty$, value $a_1$) is rigorous from SD on
  $G(s) = \zeta_K(s) H(s)$ — no Hooley boundary needed, since $G$ is integrated
  against unweighted $e \le N$ (cf. AB-decomposition note Lemma 3).
- Lemma 3.2 ($\Sigma_*$ Tauberian) is fully rigorous from SD on $G(s+1)$.

The Cesaro / on-average existence of $B^\infty$ is essentially as rigorous as
$T_<$'s secondary asymptotic. The pointwise $\sqrt N$ rate is conjectural in
both cases.

## 7. Files

- This note: `n2+1 ai thoughts/notes/proofs/P12-B-infty-existence-equivalence.md`.
- Verification: `bot/scratch/B-equivalence-check.py` (cf. session log).
- Builds on: `P12-c0T-AB-decomposition.md`, `P12-c0T-secondary-constant.md`,
  `P12-c0T-highprecision-constants.md`.
