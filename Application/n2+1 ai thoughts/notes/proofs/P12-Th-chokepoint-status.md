# P12 $T_h$ chokepoint: strategic status (2026-05-10)

**Purpose.** Strategic step-back requested by prev session
(`bot/sessions/2026-05-10T12-50-00Z.md`, pickup hint #4). The recent
"Halász-$h$" thread (2026-05-08 to 2026-05-10, ~13 sessions on disk) and the
preceding "Hooley-boundary" thread (2026-05-05 to 2026-05-07, ~20 sessions on
disk) **both reduce, via the Vaaler-truncation route through Lemma 3.4, to the
same analytic chokepoint**. This convergence is route-dependent: rigorizing
$c_0^T$ via a *different* route — e.g. direct Hooley §3 — would not necessarily
yield Lemma 3.4 (see `P12-B-infty-existence-equivalence.md` §5). This note
unifies the catalog of attempted and unattempted routes so the next session
can pick a direction with full information.

## 1. The chokepoint

For $h \ge 1$ define
$$
T_h(N) := \sum_{\substack{e \le N \\ e \,\mathrm{sf,\,good} \\ e \ge 2}} e^{2\pi i h N/e} \, S_h(e),
\qquad
S_h(e) := \prod_{p \mid e} S_h^{(p)}, \quad |S_h^{(p)}| \le 2.
$$
Here "sf, good" means $e$ squarefree, $\gcd(e, 2 \cdot \prod_{p \equiv 3(4)} p) = 1$ on
relevant $p$, and $S_h^{(p)}$ is the root sum mod $p$ of $x^2 + 1$. See
`P12-Lemma-3-4-reduction.md` §3 for derivation.

**Required bound.** Lemma 3.4 of the AB-decomposition framework needs
$$
\sup_{1 \le h \le H(N)} \frac{|T_h(N)|}{N} \to 0 \qquad (N \to \infty),
$$
for $H(N)$ growing slowly (the Vaaler truncation produces a $\log^{O(1)} N$
truncation in the qualitative form; $H(N) = \log N$ suffices for $E(N) = o(N)$).
See `P12-Lemma-3-4-reduction.md` §5 for the precise relation
$\epsilon(N) \log H(N) \to 0$.

**Empirical rate (2026-05-08 03:53, 2026-05-08 09:47).** At sampled points, the
data is consistent with a $\sqrt N$ rate: across 43 sampled $h \le 7560$ at
$N = 10^7$, $|T_h|/\sqrt N \le 1.222$; across vertical scans $h \in \{1, 2, 5, 100\}$,
$N \in \{10^5, 10^6, 10^7\}$, $|T_h|/\sqrt N \le 1.53$. **Caveat:** these are
single samples per $(N, h)$; they do *not* establish uniform $\sqrt N$ behavior
across all $h \le H(N)$. The required Lemma-3.4 statement is much weaker
(sub-linear, $o(N)$).

**Two threads converge here.**
- The Lemma 3.4 reduction (`P12-Lemma-3-4-reduction.md`, 2026-05-08 00:51)
  reduced the AB framework's $E(N) = o(N)$ goal to $T_h(N) = o(N)$ uniform.
- The Hooley-boundary thread's "$B^\infty$ exists $\iff c_0^T$ exists"
  equivalence (`P12-B-infty-existence-equivalence.md`, 2026-05-07 21:56)
  reduces the Hooley §3 boundary discrepancy to *the same* Erdős–Hooley
  fractional-part bound, which is the same $T_h$ statement after Vaaler
  truncation.

**Key historical observation.** Every session since 2026-05-08 has either (a)
attacked $T_h$ uniform-in-$h$ directly, or (b) computed/refined empirical
auxiliaries on $T_h, H_h, D_h, \Phi_h$ without producing rigorous progress on
the uniform bound. Both threads run through the same analytic difficulty.

## 2. Routes attempted (status table)

| # | Route | Outcome | Session(s) | Note |
|---|---|---|---|---|
| 1 | Trivial $|S_h(e)| \le \rho(e)$ | $|T_h(N)| = O(N)$ — not sub-linear | 2026-05-08 00:51 | Insufficient |
| 2 | B-process / van der Corput on unweighted $U_h$ | **CLOSED (negative)** — gives only $\ll \sqrt{hN} + N/\sqrt h$, hence $\ll N$ at fixed $h$ | 2026-05-08 03:53, 06:50 | Both analytic ceiling and empirical $|U_1|/\sqrt N \in [6, 52]$ kill it |
| 3 | $h$-Cesaro Fourier orthogonality (sum over $h$) | **RIGOROUS but at the wrong regime.** Theorem F.2: Cesaro mean $\to 1$ as $H \to \infty$; effective only at $H \gg N \log N$ | 2026-05-10 09:54, 12:50 | Useful as Markov/density tool, NOT per-$h$ uniform |
| 4 | Halász mean on $f_h(e) = \widetilde S_h(e)$ | **EMPIRICALLY OUT-OF-FRAME.** Halász's apparatus gives only $N(\log N)^{-c}$ (log-saving), but empirics show $\sqrt N$ (CLT rate) — Halász is the *wrong framework* for the observed regime. The 2026-05-08 12:52 pivot to $D_h$ was the correct response, not avoidance | 2026-05-08 09:47 (preview); 12:52 (deliberate pivot) | A non-tight Halász execution would still yield Lemma 3.4 qualitatively, but the framework gap suggests CLT/diagonal-style routes are mathematically aligned, Halász is not |
| 5 | Diagonal SD: $D_h \sim C_h N$ | Rigorous closed form for $D_h$, not for $|H_h|$ | 2026-05-08 12:52 | Per-$h$ second moment baseline; $|H_h|^2 / D_h \in \{0.022, \ldots, 0.852\}$ supports per-$h$ cancellation but doesn't prove it |
| 6 | $h$-averaged $|H_h|^2$ at small $H$ | Empirically refuted at small $H$ (the "$h$-summation cancels off-diagonal" hypothesis: $R(N, H)$ does NOT approach 1 at $H = O(N^{1.22})$ or smaller). At asymptotically large $H$ this becomes Theorem F.2 of route #3 | 2026-05-08 15:50 | Off-diagonal is *negative* at small $H$, neither zero nor positive |
| 7 | Autocorrelation $\Phi_h(d)$, FFT power spectrum | Empirical characterization only; no analytic | 2026-05-09 15:47, 18:30; 2026-05-10 00:49, 03:52, 06:51 | Useful diagnostic; no rigor |
| 8 | Hooley 1957 §3 direct citation | **BLOCKED** — sandbox returns 403 for academic-publisher URLs; never verified the cited form | 2026-05-04 16:30 (Nair); recurring | Anton local task |

## 3. Routes not yet attempted

| # | Route | Estimated cost | Plausibility |
|---|---|---|---|
| B | **Vinogradov / van der Corput in $e$-direction (multiplicative-weight version).** Apply $e$-cancellation to $\sum_{e \in [E, 2E], \mathrm{sf,\,good}} e^{2\pi i h N/e} S_h(e)$ for dyadic blocks; stationary phase at $e \asymp \sqrt{hN}$. The multiplicative weight $S_h$ is the genuine difficulty. The unweighted version was closed (route #2); the weighted version has not been attempted | 1–2 sessions | MEDIUM — open question; partial cancellation plausible, may give $\sqrt N$ on a dyadic block conditional on a Type-I/II split |
| C | **Heath-Brown identity on $\widetilde S_h$.** Decompose into Type-I + Type-II sums at level $\Delta$. Standard hybrid machinery | 2 sessions | MEDIUM — well-developed; needs careful Type-II analysis given the split-prime structure |
| C' | **CLT / diagonal second-moment route, exploiting the empirical $\sqrt N$ regime.** Compute $\sum_h |T_h(N)|^2$ for $h$ in a window, get $L^2$-mean rate; then transfer to pointwise via large-deviation / max-inequality. Mathematically aligned with the observed regime (unlike Halász) | 1 session | MEDIUM-HIGH — directly informed by the framework gap noted in route #4; would also yield Lemma 3.4 in $L^2$-mean sense |
| D | **Voronoi-type formula for $\widetilde S_h(e)$.** Convert per-$e$ root product to dual sum over Gaussian integers. CRT structure is suggestive | 1 session (exploratory) | LOW–MEDIUM — Voronoi for genuinely multiplicative weights is non-standard; risk of dead end |
| E | **Erdős–Turán applied directly to discrepancy $E(N)$.** Bypass the Vaaler/Fourier $T_h$ reformulation and bound the saw-tooth statistic $\Psi(N)$ via Erdős–Turán on the joint distribution $\{(N-r_i)/e\}_{e,i}$. This is closer to what Hooley 1957 §3 actually does | 1–2 sessions | MEDIUM — sidesteps the $T_h$ chokepoint by attacking the original target; if successful, route also unblocks the $c_<^\infty$ side independently |
| F | **Direct Hooley 1957 §3 read (Anton local).** Pull the paper, identify whether §3 establishes uniform-in-$h$ Weyl equidistribution for $\{(N - r_i)/e\}$ across sf $e \le N$. If yes, both threads dissolve to "rigorous modulo Hooley 1957 Theorem X" | 30 min Anton-local | **HIGHEST** — if §3 has it, the entire chokepoint dissolves at zero analytic cost. Sandbox has blocked this since 2026-05-04 16:30 |
| G | **Conditional results (GRH / Elliott–Halberstam).** Sanity-check the target bound and produce a conditional Lemma 3.4. Literature value: GRH gives $T_h(N) \ll N^{1-\delta}$ for some $\delta > 0$ via standard methods | 1 session | LOW priority but useful as a sanity check that the unconditional target is plausible |

## 4. Strategic recommendation

**Highest-EV (Anton-local, 30 min): route F — pull Hooley 1957 §3.**
If §3 establishes the uniform Weyl bound on $\{(N-r_i)/e\}$, **everything
downstream is unblocked** at zero analytic cost. The bot has been blocked from
this since 2026-05-04 16:30 (academic-publisher URLs return 403 in sandbox) and
the gap has propagated through ~30 subsequent bot sessions. Strict gate.

**Highest-EV bot session: route C' (CLT / diagonal second-moment) OR route E
(Erdős–Turán direct on $E(N)$).**

Reasoning:
1. **Route #4 (Halász mean, analytic execution) is NOT recommended.** The
   empirical preview (2026-05-08 09:47) flagged that the observed $\sqrt N$
   rate exceeds what Halász's apparatus can deliver ($N(\log N)^{-c}$). The
   2026-05-08 12:52 pivot was the correct response, not avoidance. Halász is
   the *wrong framework* for the regime; it would either (a) under-deliver
   relative to what's true, or (b) require a non-standard sharpening
   (uniform-in-$h$ Hooley/Weyl) that is itself the chokepoint.
2. **Route C'** is mathematically aligned with the observed regime: CLT-type
   second-moment + max-inequality is exactly what produces $\sqrt N$ rates.
   Cost: 1 session. Output: $L^2$-mean Lemma 3.4 (weaker than pointwise but
   sufficient for several downstream applications).
3. **Route E** sidesteps the $T_h$ Fourier reformulation entirely by attacking
   the saw-tooth $\Psi(N)$ via Erdős–Turán on the joint distribution. This is
   what Hooley 1957 §3 actually does (per references in our notes); even
   without access to the paper, the technique is in standard texts
   (Tenenbaum III.2, Iwaniec–Kowalski Ch. 21).
4. **Routes B, C, D, G** are reasonable secondary candidates. Route B
   (Vinogradov in $e$, multiplicative-weight) is plausibility MEDIUM; Heath-Brown
   (C) is heavier machinery; G (GRH conditional) gives a conditional result
   that sanity-checks the target.

**De-prioritize: routes #7 (autocorrelation/spectrum), further empirical
refinements of $C(N)$, additional precision work on $c_0^T$ constants.**
These are tractable but do not advance the chokepoint.

**Anti-autopilot guardrail.** The next session should *open* with the question
"does this advance the uniform-in-$h$ $T_h$ bound or sidestep it (E) or replace
it with an $L^2$-mean version (C')?" If no, redirect.

## 5. Honest framing

This note is *no new mathematics*. It is a strategic synthesis of ~30 sessions'
worth of work that have produced (a) two rigorous results bearing on the
chokepoint — Theorem F.2 (Cesaro orthogonality) and the AB integer identity /
equivalence — and (b) many empirical observations on $H_h, D_h, \Phi_h, T_h$,
but (c) **no rigorous progress on the uniform-in-$h$ $T_h$ bound itself.**

The session catalog above is honest about which routes are:
- *Closed by negative result* (route #2 = B-process on unweighted $U_h$;
  valuable);
- *Closed at the wrong regime* (route #3 = $h$-Cesaro orthogonality, route #6 =
  $h$-averaged at small $H$);
- *Out of frame* (route #4 = Halász, framework gap);
- *Genuinely unexecuted* (routes B, C, C', D, E, F, G).

The chokepoint has not moved since 2026-05-08 00:51 (Lemma 3.4 reduction
written). Subsequent work has refined the surrounding empirical
characterization but has not produced a rigorous per-$h$ or $L^2$-mean bound.

## 6. Files

This note. References (most-relevant first):

- `n2+1 ai thoughts/notes/proofs/P12-Lemma-3-4-reduction.md`
  (defines $T_h(N)$ and the chokepoint).
- `n2+1 ai thoughts/notes/proofs/P12-B-infty-existence-equivalence.md`
  (shows the Hooley-boundary thread reduces to the same Erdős–Hooley input).
- `n2+1 ai thoughts/notes/proofs/P12-Halasz-Hh-empirical.md`
  (route #4 empirical preview).
- `n2+1 ai thoughts/notes/proofs/P12-Halasz-Dh-diagonal.md`
  (route #5 diagonal closed form).
- `n2+1 ai thoughts/notes/proofs/P12-Halasz-Fourier-orthogonality.md`
  (route #3 Theorem F.2).
- `n2+1 ai thoughts/notes/proofs/P12-Halasz-CN-empirical.md`
  (route #3 effective constant).
- `n2+1 ai thoughts/notes/proofs/P12-Uh-vs-Th-empirical.md`
  (route #2 closed).
- `n2+1 ai thoughts/notes/proofs/P12-Lemma-3-4-empirical-Th.md`
  (empirical $|T_h|/\sqrt N \le 1.222$ at $N = 10^7$).

## 7. Rigor accounting (unchanged)

- Rigorous: D₀(N) = Θ(N²), D(N) = Θ(N²), $\sum \tau(n^2+1)^2 \ll N (\log N)^3$
  (modulo Nair-form citation), Theorem F.2, AB integer identity, "$B^\infty$
  exists $\iff c_0^T$ exists" (modulo Lemma 3.4).
- Conjectural: Lemma 3.4 ($T_h(N) = o(N)$ uniform in $h$); $B^\infty = 0.085704$;
  $c_{0,\infty}^T = 0.987317$; sharp constants in $D_0(N) \sim 2.347 N^2/\pi$;
  cancellation rate $|H_h|/\sqrt N$ uniformly bounded.
