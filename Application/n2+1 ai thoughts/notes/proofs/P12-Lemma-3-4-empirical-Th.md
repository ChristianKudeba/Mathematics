# P12 — Empirical $|T_h(N)|$ scaling for the Lemma 3.4 Fourier reduction

**Session.** 2026-05-08 (UTC). Builds directly on:
- `P12-Lemma-3-4-reduction.md` (prev session, 2026-05-08 00:51): reduced
  Lemma 3.4 ($E(N) = o(N)$) to the Fourier-side input
  $\sup_{h \le H(N)} |T_h(N)|/N \to 0$ where
  $$T_h(N) := \sum_{\substack{e \,\mathrm{sf} \\ 2 \le e \le N \\ \rho(e) \ge 1}} e^{2\pi i h N/e} \, S_h^*(e), \qquad S_h^*(e) := \sum_{i=1}^{\rho(e)} e^{-2\pi i h r_i^{(e)}/e}.$$
  The trivial bound $|S_h^*(e)| \le \rho(e)$ gives only $|T_h(N)| = O(N)$.

**Goal.** Test the analytic input itself empirically — not just its qualitative
consequence $E(N) = o(N)$. Compute $|T_h(N)|$ directly at multiple $N$ and
multiple $h$, and ask: is the trivial bound off by a $\sqrt{\log}$ factor, or
by $\sqrt N$? The answer determines whether the Fourier reduction is
"essentially tight modulo $\sqrt N$" or whether it loses a power of $N$.

## 1. Computational setup

Code: `bot/scratch/Th-discrepancy.py` (sweep over $N$, fixed $h$ list) and
`bot/scratch/Th-uniform-h-scan.py` (fixed $N = 10^7$, sweep over $h$).

For each sf $e \in [2, N]$ with $\rho(e) \ge 1$ (all prime factors $= 2$ or
$\equiv 1 \pmod 4$):
1. Factor $e$ via SPF sieve; check sf-and-good in $O(\omega(e))$.
2. Find roots of $x^2 \equiv -1 \pmod p$ for each prime $p \mid e$ via
   Tonelli (cached per prime).
3. CRT-lift to roots $\{r_i^{(e)}\}$ of $x^2 \equiv -1 \pmod e$.
4. For each root $r$, accumulate $\{(N-r)/e\}$ into $F(N)$ and the phase
   $e^{2\pi i h (N-r)/e}$ into $T_h(N)$.

Pure-Python execution; SPF sieve and sweep at $N = 10^7$ each take $\sim 5$ s.
Full sweep $N \in \{10^5, 3\!\cdot\!10^5, 10^6, 3\!\cdot\!10^6, 10^7\}$ over
$h \in \{1, 2, 3, 5, 10\}$: 28 s total. Single-$N$ scan over 30 $h$-values at
$N = 10^7$: 41 s.

**Sign / phase convention.** Note's definition uses $e^{2\pi i h(N-r_i)/e}$;
code uses $y := (N - r_i) \bmod e$ and $e^{2\pi i h y/e}$. These are equal:
$h(N-r_i)/e - h y/e = h(N-r_i-y)/e = h k$ for the integer $k = (N-r_i-y)/e$,
and $e^{2\pi i h k} = 1$ since $h$ and $k$ are integers. The script faithfully
computes $T_h(N)$ as defined in §1.

**Sanity check.** At $N = 10^3$ the script reports $E(N) = 7.6922$, matching
the prev note's $E(10^3) = +7.69$ to 3 d.p. Confirms the $E(N)$ branch is
consistent with the predecessor sieve `F-discrepancy-empirical.py`.

## 2. Forecast (F1) and (F2) confirmation

At $N = 10^7$:
- **F1.** $|E(N)|/\sqrt N = 0.2057$ — well within forecast range $[0.05, 0.5]$.
  *Confirmed.*
- **F2.** $|E(N)|/N = 6.5\!\cdot\!10^{-5}$ — well within forecast $\le 10^{-3}$.
  *Confirmed.*

Updated table of $E(N)$:

| $N$ | $E(N)$ | $|E|/N$ | $|E|/\sqrt N$ |
|---|---|---|---|
| $10^5$ | $+123.33$ | $1.2\!\cdot\!10^{-3}$ | $0.390$ |
| $3\!\cdot\!10^5$ | $-245.14$ | $8.2\!\cdot\!10^{-4}$ | $0.448$ |
| $10^6$ | $-211.85$ | $2.1\!\cdot\!10^{-4}$ | $0.212$ |
| $3\!\cdot\!10^6$ | $-254.79$ | $8.5\!\cdot\!10^{-5}$ | $0.147$ |
| $10^7$ | $+650.55$ | $6.5\!\cdot\!10^{-5}$ | $0.206$ |

$|E|/N$ is monotonically declining; $|E|/\sqrt N$ stays in $[0.15, 0.45]$ across
the new 5 scales (all $\ge 10^5$). Sign alternation $+,-,-,-,+$ — non-monotone,
consistent with CLT-type fluctuation.

## 3. Empirical $|T_h(N)|$ at fixed $h$, sweeping $N$

For $h \in \{1, 2, 3, 5, 10\}$ across $N \in \{10^5, \ldots, 10^7\}$:

| $N$ | $|T_1|/\sqrt N$ | $|T_2|/\sqrt N$ | $|T_3|/\sqrt N$ | $|T_5|/\sqrt N$ | $|T_{10}|/\sqrt N$ |
|---|---|---|---|---|---|
| $10^5$ | $0.671$ | $0.717$ | $0.422$ | $0.686$ | $0.261$ |
| $3\!\cdot\!10^5$ | $0.433$ | $0.198$ | $1.528$ | $0.950$ | $0.328$ |
| $10^6$ | $0.513$ | $0.840$ | $0.467$ | $0.267$ | $0.535$ |
| $3\!\cdot\!10^6$ | $0.389$ | $0.690$ | $0.586$ | $0.901$ | $0.408$ |
| $10^7$ | $0.593$ | $0.737$ | $0.177$ | $1.081$ | $1.174$ |

**Key observation.** $|T_h(N)|/\sqrt N$ is bounded across all 25 (h, N) pairs in
$[0.18, 1.53]$ — *the trivial bound $|T_h(N)| \le A(N) = O(N)$ is empirically
loose by exactly the factor $\sqrt N$ (no log corrections visible)*.

Per-$h$ and per-$N$ fluctuations are large (factor 4-8) but the supremum across
the table is bounded; no monotone trend in $N$.

## 4. Empirical $|T_h(N)|/\sqrt N$ at fixed $N = 10^7$, sweeping $h$

**Scan A** — dense low + log-spaced ($S_A = \{1,\ldots,20, 25, 30, 50, 75, 100,
150, 200, 300, 500, 1000\}$, 30 values):

| $h$ | $|T_h|/\sqrt N$ | | $h$ | $|T_h|/\sqrt N$ |
|---|---|---|---|---|
| $1$ | $0.593$ | | $20$ | $0.742$ |
| $2$ | $0.737$ | | $25$ | $0.679$ |
| $3$ | $0.177$ | | $30$ | $0.890$ |
| $4$ | $0.341$ | | $50$ | $0.283$ |
| $5$ | $1.081$ | | $75$ | $1.066$ |
| $6$ | $0.128$ | | $100$ | $0.666$ |
| $7$ | $1.222$ | | $150$ | $0.164$ |
| $8$ | $0.509$ | | $200$ | $0.491$ |
| $9$ | $0.257$ | | $300$ | $0.459$ |
| $10$ | $1.174$ | | $500$ | $0.526$ |
| $11$ | $0.891$ | | $1000$ | $0.981$ |
| $12$ | $0.492$ | | | |
| $\vdots$ | $\vdots$ | | | |
| $19$ | $0.402$ | | | |

(Selected entries from $S_A$; full data in script output.)

**Scan B** — *resonance candidates* (highly composite + factorial-like
$h \in S_B = \{12, 24, 36, 48, 60, 120, 360, 420, 720, 840, 2520, 5040, 7560\}$,
13 values). These are the $h$ where one would expect a spike via Vinogradov-style
"diagonal alignment" reasoning; if $h$ has many small divisors, the phase
$h r_i^{(e)}/e$ is non-generic for many small $e$.

| $h$ | $|T_h|/\sqrt N$ | | $h$ | $|T_h|/\sqrt N$ |
|---|---|---|---|---|
| $12$ | $0.492$ | | $720$ | $0.673$ |
| $24$ | $0.745$ | | $840$ | $0.902$ |
| $36$ | $0.805$ | | $2520$ | $0.667$ |
| $48$ | $0.463$ | | $5040$ | $0.301$ |
| $60$ | $0.213$ | | $7560$ | $0.398$ |
| $120$ | $0.909$ | | | |
| $360$ | $0.524$ | | | |
| $420$ | $1.211$ | | | |

**Key observation.** Combined supremum across $S_A \cup S_B$ (43 distinct $h$):
$$\sup_{h \in S_A \cup S_B} |T_h(10^7)|/\sqrt N = 1.222 \quad (\text{at } h = 7).$$
*No "resonant" $h$ in $S_B$ exceeds the Scan-A supremum.* Highly composite $h$
gives nothing different from generic $h$.

**Inference (with caveat).** The empirical bound $|T_h(N)| \le c \sqrt N$
holds with $c \approx 1.22$ uniformly across the 43 sampled $h$ values up to
$h = 7560$ at $N = 10^7$. This is consistent with — *but does not prove* —
the proof-needed bound $\sup_{h \le H(N)} |T_h(N)|/N \to 0$ for any
$H(N) \to \infty$ slower than $e^{\sqrt N}$. The data does not rule out
*spike-$h$ values* outside the scanned set.

## 5. Implication for the Fourier reduction

Recall from `P12-Lemma-3-4-reduction.md` §5:
$$\Psi(N) = -\sum_{h=1}^H \frac{\mathrm{Im}[T_h(N)]}{\pi h} + O\!\left(\sum_{e, i}\min\!\left(1, \frac{e}{H \|y\|_e}\right)\right).$$

**(M) Main term, given $|T_h(N)| \le c \sqrt N$ uniform in $h \le H$:**
$$\left|\sum_{h=1}^H \frac{\mathrm{Im}[T_h]}{\pi h}\right| \le \frac{c\sqrt N}{\pi} \sum_{h=1}^H \frac{1}{h} \le \frac{c\sqrt N}{\pi}(\log H + 1).$$
For this to be $o(N)$: $\sqrt N \log H = o(N)$ ⇔ $\log H = o(\sqrt N)$.
*Any* $H \to \infty$ with $\log H = o(\sqrt N)$ works; e.g. $H = \log N$,
$H = N^{1/4}$, $H = N^{0.4}$ all fine.

**(R) Remainder term.** For sf $e \in [2, N]$ with $\rho(e) \ge 1$, the count
of $(e, i)$ with $\|(N - r_i)/e\| \le 1/H$ — equivalently
$\|y\|_e/e \le 1/H$ — is on average $A(N)/H \asymp N/H$ (uniform-distribution
heuristic, also rigorous via classical equidistribution mod $e$). Hence
$$\sum_{e, i} \min\!\left(1, \frac{e}{H \|y\|_e}\right) \ll \frac{A(N)}{H} \cdot \log H + \frac{A(N)}{H} \asymp \frac{N \log H}{H},$$
which is $o(N)$ for $H \to \infty$.

**Combined conclusion (modulo empirical extrapolation).** *If* $|T_h(N)| \le
c\sqrt N$ uniformly in $h \le H$ for some $H = H(N) \to \infty$ with
$\log H = o(\sqrt N)$, *then* $\Psi(N) = o(N)$ and hence Lemma 3.4 holds.

The empirical data of §4 supports the hypothesis with $H \le 1000$ at $N = 10^7$
and $c \approx 1.22$. This is far stronger than what the proof needs (qualitative
$|T_h(N)| = o(N)$); the data suggests the Fourier reduction is "tight at the
$\sqrt N$ rate", with very substantial headroom.

## 6. What is rigorous and what is conjectural

**Rigorous.**
- The reduction Lemma 3.4 ⟺ $\Psi(N) = o(N)$ from prev session §2-§3
  (modulo discrete jumps $O(N^\epsilon)$).
- The Vaaler / Fourier decomposition $\Psi = \text{(main)} + \text{(remainder)}$
  with the remainder bound $O(N \log H/H)$ (standard).
- The script-computed values of $E(N)$ and $T_h(N)$ at the tabulated $N$, $h$.

**Conjectural / empirical.**
- The bound $|T_h(N)| \le c \sqrt N$ uniform in $h \le H(N)$ for *all* $N$
  large and any $H(N) \to \infty$. We have evidence at $N = 10^7$ for
  $h \le 7560$ (43 sampled values); uniformity at larger $N$, and at
  un-sampled $h$ (which could include "spike" $h$ outside our scans), is
  open.
- **Cross-quantification gap.** §3 tests $|T_h|/\sqrt N$ at $h \in \{1,2,3,5,10\}$
  across 5 $N$-values; §4 tests at $N = 10^7$ across 43 $h$-values. The truly
  needed statement — *uniform in $h$ as $N \to \infty$* — is not directly
  tested. A slowly-growing $\sqrt{\log\log N}$ creep in the constant would
  be invisible at this scale.

## 7. Comparison to the natural iid CLT prediction

Treat each per-$(e,i)$ phase $e^{2\pi i h(N - r_i^{(e)})/e}$ as iid uniform on
the unit circle. There are
$$A(N) = \sum_{e \le N, \mathrm{sf, good}} \rho(e) \sim R H(1) \cdot N \approx 0.434\,N$$
such pairs (the constant $R H(1) = 0.4341$ is rigorous via SD on $\zeta_K(s) H(s)$
at the simple pole $s = 1$, see `P12-c0T-AB-decomposition.md` §3). A sum of
$A(N)$ iid unit phases has expected magnitude $\sqrt{A(N)} \sim
\sqrt{0.434\,N} \approx 0.66 \sqrt N$ (Rayleigh distribution $L^2$-norm).

**Empirical observation: $|T_h(N)|/\sqrt N$ is in the range $[0.13, 1.22]$ over
the 43 sampled $h$.** The sample mean across Scan A is $\approx 0.62$, with
sample maximum $1.22$.

**Interpretation.** The empirical spread is exactly what one would expect from
the natural iid CLT model: mean $\approx \sqrt{0.43} \approx 0.66$. *If* the
$|T_h(N)|$ for distinct $h$ were also iid (an additional assumption — the
underlying $(e, r_i)$ are shared across $h$, so this is *not* automatic), then
the max-over-43-samples Rayleigh extreme-value heuristic gives
$\approx \sqrt{2 \log 43} \cdot 0.66 \approx 1.30$. Our $1.22$ matches; the
match should be read as "consistent with" rather than "predicted by" the model.

**Implication.** $|T_h(N)|$ is asymptotically the same as a sum of $A(N)$
iid random phases. There is no "extra cancellation" beyond CLT, but also
no "extra correlation" inflating the variance by $\log^c N$ factors. The
phase-pseudorandomness of $h(N-r_i^{(e)})/e$ on $(e, i)$ pairs is sharp.

**Caveat.** This is only at $N = 10^7$ and only for the sampled $h$. A latent
$\sqrt{\log N}$ factor would inflate the constant from $\approx 1$ at
$N = 10^7$ to $\approx \sqrt{\log 10^9 / \log 10^7} \cdot 1 = 1.13$ at
$N = 10^9$ — undetectable from this data. The claim "no log corrections"
is thus *consistent with* but not *proven by* the data.

## 8. Status

This session's contribution to Lemma 3.4 rigorization:
- *Confirms* the qualitative forecast $|E(N)|/\sqrt N$ remains in $[0.05, 0.5]$
  at $N = 10^7$.
- *New positive evidence:* the Fourier-side input the proof needs
  ($T_h(N) = o(N)$ uniform in $h$) is empirically met at the much stronger
  rate $|T_h(N)| \le c \sqrt N$, with $c \approx 1.22$ uniform across
  $h \le 1000$ at $N = 10^7$.
- *Rigor accounting unchanged:* Lemma 3.4 still depends on the un-rigorized
  uniform bound $\sup_{h \le H(N)} |T_h(N)|/N \to 0$. This session does not
  prove that bound; it only provides empirical evidence at a single $N$.

**Next steps (analytic).**
1. Try van der Corput's B-process on $\sum_{e \in [E, 2E], \mathrm{sf, good}}
   e^{2\pi i h N/e}$ (the unweighted phase sum, no $S_h^*$); the empirical
   data of §4 suggests this should give the right $\sqrt N$ rate. Single
   session.
2. Multiplicative aggregation: use the fact that $S_h^*(e) = \prod_{p \mid e}
   S_h^{*(p)}$ is multiplicative to convert the $e$-sum to an Euler product
   (Mellin transform) and apply Perron / contour shift. 1-2 sessions.
3. Consult Hooley 1957 §3 directly (Anton local task) — may already give
   uniform $T_h(N) \ll N^{1-\delta}$ with explicit $\delta$.

## 9. Falsifiable forecasts (new)

**(G1)** At $N = 3 \cdot 10^7$, $\sup_{h \le 1000} |T_h(N)|/\sqrt N \le 2$.
Refutation: any value $\ge 2$ would suggest a hidden $\log^c N$ factor
not visible at $N = 10^7$ (where the corresponding sup is $1.22$). The
forecast is on the *supremum over $h$*; individual small values like
$|T_3|/\sqrt N = 0.18$ are consistent with the sup-bound.

**(G2)** At $N = 10^8$ (Anton local), $|E(N)|/\sqrt N \le 0.6$ AND
$|T_1(N)|/\sqrt N \le 1.5$. Both are upper-bound predictions, single-sided.
Refutation: either statistic violating its upper bound.

**(G3)** Variance scaling: across $N \in [10^4, 10^7]$, the *average* over
$h \in \{1, \ldots, 100\}$ of $|T_h(N)|^2$ scales as $N$ (not $N \log^k N$)
to within a factor of 2. Equivalently, the iid-CLT identification of §7
is robust as $N$ grows.

## 10. Files

- This note: `n2+1 ai thoughts/notes/proofs/P12-Lemma-3-4-empirical-Th.md`.
- New scripts: `bot/scratch/Th-discrepancy.py`,
  `bot/scratch/Th-uniform-h-scan.py`.
- Prev session: `n2+1 ai thoughts/notes/proofs/P12-Lemma-3-4-reduction.md`.
- Underlying empirical script (from prev session):
  `bot/scratch/F-discrepancy-empirical.py`.
