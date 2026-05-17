# P12 — Unweighted phase sum $U_h(N)$ vs rooted sum $T_h(N)$: empirical refutation of B-process route

**Date:** 2026-05-08 (session ~07 UTC).
**Goal:** Test pickup hint #1 from session 2026-05-08T03-53-40Z: "van der Corput
B-process on the unweighted $e$-sum should give $\sqrt N$." Compare empirically
the *unweighted* phase sum $U_h(N)$ against the *rooted* sum $T_h(N)$ that the
proof of Lemma 3.4 actually requires.

## 1. Definitions

For a "good" squarefree integer $e$ — i.e., $e$ squarefree with all prime
factors $p = 2$ or $p \equiv 1 \pmod 4$ — let $\rho(e) = 2^{\omega(e)}$ count
the roots of $r^2 + 1 \equiv 0 \pmod e$.  Define

$$
T_h(N) := \sum_{\substack{e \le N \\ \mathrm{sf, good}}} \sum_{\substack{r \pmod e \\ r^2 + 1 \equiv 0}} e^{2\pi i h (N - r)/e}
        = \sum_{\substack{e \le N \\ \mathrm{sf, good}}} e^{2\pi i h N/e} \cdot \widetilde S_h(e),
$$

with the multiplicative root-weight

$$
\widetilde S_h(e) = \sum_{r^2+1 \equiv 0 \pmod e} e^{-2\pi i h r/e},
\qquad |\widetilde S_h(e)| \le \rho(e).
$$

Define the *unweighted* analogue (one phase per $e$, no root expansion):

$$
U_h(N) := \sum_{\substack{e \le N \\ \mathrm{sf, good}}} e^{2\pi i h N/e}.
$$

If $U_h(N) = O(N^{1/2 + \epsilon})$ rigorously, then any morally-comparable
bound on $T_h(N)$ would follow from a routine multiplicative-aggregation
argument on the bounded weight $|\widetilde S_h(e)| \le \rho(e) \le \tau(e)$.
This is the heuristic motivation behind pickup hint #1.

## 2. B-process bound on $U_h$ (analytic)

The phase $\phi(e) = h N/e$ has $\phi''(e) = 2 h N/e^3$.  Standard
van-der-Corput Process B (e.g.\ Iwaniec–Kowalski Thm 8.16, with $\phi'' \asymp \lambda$):

$$
\Bigl|\sum_{e \in [E, 2E]} e^{2\pi i \phi(e)}\Bigr|
\;\ll\; E \lambda^{1/2} + \lambda^{-1/2}.
$$

With $\lambda = h N/E^3$ this becomes

$$
\sum_{e \in [E, 2E]} e^{2\pi i h N/e} \;\ll\; \sqrt{h N/E} \;+\; E^{3/2}/\sqrt{h N}
\qquad (E \ge \sqrt{h N}).
$$

For $E < \sqrt{h N}$ the phase oscillates rapidly and the trivial bound $\le E$
applies (or one uses Process A; the trivial bound suffices here).  Inserting
the indicator $\mathbf 1_{\mathrm{sf,good}}$ either via Möbius (cost $\log E$
in the sum, no rate change) or absorbed into a smoother weight only changes
implicit constants.

**Dyadic sum.**  Splitting $E$ into dyadic blocks $E \in \{2^k : 1 \le 2^k \le N\}$:
for $E \le \sqrt{hN}$ apply trivial bound (size $\le E \le \sqrt{hN}$); for
$E \ge \sqrt{hN}$ apply B-process.  Sum:

$$
|U_h(N)| \;\ll_\epsilon\; \sqrt{h N} \;+\; \frac{N}{\sqrt h} \cdot N^\epsilon.
$$

Both branches of the B-process bound itself, $\sqrt{hN/E}$ and $E^{3/2}/\sqrt{hN}$,
are dominated when summed dyadically by their endpoints — geometric series.
The $\sqrt{hN}$ term is the *trivial* contribution from $E \le \sqrt{hN}$
(rapid-oscillation regime where this technique gives no gain); the $N/\sqrt h$
term is the dyadic-summed B-process contribution.  Both terms balance at
$h \asymp \sqrt N$, where each is $\asymp N^{3/4}$.

**B-process consequence — for this *route*, not for $U_h$ itself.**  At fixed
$h$, the B-process technique applied dyadically yields only the bound $\ll N$,
i.e., no improvement over the trivial sf-count.  This is a ceiling on what
*this technique* produces; the unconditional growth rate of $U_h(N)$ is a
separate question (see §3 and §6.4).  A rigorous bound $U_h(N) \ll N^{1/2+\epsilon}$
at fixed $h$ would require *higher exponent pairs* (AB-process / Phillips /
Huxley), analogous to the divisor-problem $\Delta(N) \ll N^{0.315}$ (see §5).

## 3. Empirical comparison

Computed via `bot/scratch/Uh-vs-Th-empirical.py` and `Uh-h-sweep.py`,
`Uh-N1e7.py`. All sums over good squarefree $e \le N$.

### 3.1 $U_h$ scales linearly in $N$ at small $h$

| $N$    | $\|U_1\|$ | $\|U_1\|/N$ | $\|U_1\|/\sqrt N$ |
|-------:|-------:|-------:|-------:|
| $10^5$ | $1{,}937.8$  | $0.0193$ | $6.13$  |
| $10^6$ | $17{,}724.3$ | $0.0177$ | $17.72$ |
| $10^7$ | $165{,}374.6$ | $0.0165$ | $52.30$ |

Ratio $|U_1|/N$ is essentially constant ($\approx 0.018$, slow log-decay);
$|U_1|/\sqrt N$ grows like $\sqrt N$.  **The unweighted phase sum at $h=1$
scales as $\Theta(N)$, not as $\sqrt N$.**  This pattern persists at $h = 2, 5, 10$.

### 3.2 $U_h$ vs $T_h$ at $N = 10^6$ (one decade of $h$)

| $h$ | $\|U_h\|$ | $\|U_h\|/\sqrt N$ | $\|T_h\|$ | $\|T_h\|/\sqrt N$ | $\|U_h\|/\|T_h\|$ |
|----:|-------:|-------:|-------:|-------:|-------:|
| $1$   | $17{,}724$ | $17.72$ | $513$ | $0.51$ | $34.6$ |
| $2$   | $9{,}270$  | $9.27$  | $840$ | $0.84$ | $11.0$ |
| $5$   | $3{,}718$  | $3.72$  | $267$ | $0.27$ | $13.9$ |
| $10$  | $1{,}918$  | $1.92$  | $536$ | $0.54$ | $3.6$  |
| $100$ | $327$    | $0.33$  | $656$ | $0.66$ | $0.5$  |

The rooted sum $T_h$ stays at $\le \sqrt N$ scale uniformly; the unweighted
sum $U_h$ is $\gg \sqrt N$ for small $h$ and crosses below $T_h$ around
$h \sim 100$.

### 3.3 $U_h$ as a function of $h$, at $N = 10^6$

| $h$ | $\|U_h\|$ | $\|U_h\|/\sqrt{N/h}$ |
|----:|-------:|-------:|
| $1$   | $17{,}724$ | $17.72$ |
| $5$   | $3{,}718$  | $8.31$  |
| $20$  | $1{,}014$  | $4.54$  |
| $50$  | $385$    | $2.72$  |
| $150$ | $198$    | $2.42$  |
| $500$ | $175$    | $3.91$  |
| $1000$ | $263$   | $8.32$  |
| $3000$ | $418$   | $22.9$  |
| $10000$ | $269$  | $26.9$  |

Empirical minimum near $h \sim \sqrt N = 10^3$ (actually at $h \approx 150{-}500$).
Past $h \asymp \sqrt N$, $|U_h|$ grows again, broadly compatible with the
B-process $\sqrt{h N}$ branch.  **The data is consistent with**

$$
|U_h(N)| \asymp \min\Bigl(\frac{N}{\sqrt{h}},\,\sqrt{h N}\Bigr) \cdot \text{(slow log)},
$$

i.e., the *worse* of the two B-process branches, not better.

## 4. Implication: the dyadic B-process route is too weak

Two combined observations refute pickup hint #1 as a route to $T_h \ll \sqrt N$:

(i) **§2 analytic ceiling.**  Dyadic B-process applied to $U_h$ produces
$|U_h(N)| \ll \sqrt{hN} + N/\sqrt h$.  At fixed small $h$ this is $\ll N$,
not $\ll \sqrt N$.  This is a hard ceiling on what *this technique* gives.

(ii) **§3 empirical.**  $|U_1(N)|/\sqrt N$ grows like $\sqrt N$ across two
decades, ruling out empirically that $U_1(N) \ll \sqrt N \log^c N$ for any
fixed $c$.  ($|U_1(N)|/(\sqrt N \log N)$ at $N = 10^5, 10^6, 10^7$ is
$0.53, 1.28, 3.24$ — *increasing*, not bounded.)  However, the data does
*not* rule out $|U_1(N)| = o(N)$; e.g. $|U_1(N)|/N$ drifts from
$0.0193 \to 0.0165$ across two decades, consistent with a slow $1/(\log N)^c$
or even a transient pre-asymptotic regime.  All that the empirical data
firmly establishes is

$$
|U_1(N)| \gtrsim 0.016 \,N \text{ across the tested range};
\qquad \text{any bound } |U_1| \ll N^{1/2+\epsilon} \text{ is false on this range.}
$$

Combining (i) and (ii): **the dyadic-B-process-on-$U_h$ approach does not
yield $T_h(N) \ll \sqrt N$, neither analytically nor empirically.**  The
narrower claim "$U_h(N) = \Theta(N)$ asymptotically" is *not* established —
sub-linear decay remains possible.  The relevant fact for Lemma 3.4 is that
*even if* $U_h \ll N^{1/3+\epsilon}$ rigorously (the AB/Huxley target),
this *still* does not transfer to $T_h \ll N^{1/2}$ — see §5.

## 5. Cauchy–Schwarz obstruction: even the strongest exponent-pair bound on $U_h$ does not give $T_h \ll \sqrt N$

Suppose, hypothetically, the strongest known exponent-pair bound on
$U_h(N) \ll N^{\theta + \epsilon}$ holds for some $\theta < 1/2$ (the
divisor-problem analogue gives $\theta = 131/416 \approx 0.315$, Huxley).
Even granting this, the natural transfer to $T_h$ goes via a multiplicative
convolution / Cauchy–Schwarz on the bounded weight $\widetilde S_h(e)$.

The honest unconditional bound from such a transfer is

$$
|T_h(N)|^2 \;\le\; \Bigl|\sum_{\substack{e \le N \\ \mathrm{sf, good}}} e^{2\pi i h N/e}\Bigr|^2
              \;\cdot\; \frac{\sum_{\substack{e \le N \\ \mathrm{sf, good}}} |\widetilde S_h(e)|^2}{1}
$$

(when applied through a smooth-projection / partial-summation argument that
loses the second-moment of $\widetilde S_h$).  The second-moment factor is

$$
\sum_{\substack{e \le N \\ \mathrm{sf, good}}} |\widetilde S_h(e)|^2
   \;\asymp\; N (\log N)^c \qquad (c > 0 \text{ explicit, e.g. } c=1)
$$

since $|\widetilde S_h(e)|^2$ is multiplicative, integrating to a Selberg–Delange
class mean.  Hence even with $U_h \ll N^{\theta + \epsilon}$,

$$
|T_h(N)| \;\ll\; N^{\theta/2 + 1/2 + \epsilon} \cdot (\log N)^{c/2}.
$$

For $\theta = 1/3$ (Huxley): $|T_h(N)| \ll N^{2/3 + \epsilon}$.  For
$\theta = 0$ (counterfactual ideal): $|T_h(N)| \ll N^{1/2 + \epsilon}$.
**Even the counterfactual ideal exponent-pair bound on $U_h$ produces a
rigorous $T_h \ll N^{1/2+\epsilon}$ only — it does not match the empirical
$|T_h| \le 1.22 \sqrt N$ rate.**

Conclusion: any rigorous proof of $T_h(N) \ll N^{1/2+\epsilon}$ uniform in $h$
must avoid the Cauchy–Schwarz transfer entirely and exploit the structure of
$\widetilde S_h(e)$ directly — i.e., a Halász-type argument on the
multiplicative function $e \mapsto \widetilde S_h(e)$ twisted by the phase
$e^{2\pi i h N/e}$.

Concretely: at $h = 1$, $N = 10^7$, the $e$-sum has empirical absolute mass
$\sim 0.018 \, N \approx 1.6 \cdot 10^5$; the rooted version is
$\sim 1.5 \, \sqrt N \approx 4.7 \cdot 10^3$.  The $\widetilde S_h$
multiplicative weight provides an additional factor $\sim 35$ of cancellation
beyond what the unweighted $e$-direction provides.  This is the analytic
content the proof of Lemma 3.4 needs.

## 6. Revised next-step assessment

Pickup hint #1 from prev session is **demoted** (was: "1 session,
analytic-tractable"; now: "blocked at small $h$; the analytic burden is
multiplicative cancellation in $\widetilde S_h$").

The actually-binding direction:

- **At $h = O(1)$:** $\widetilde S_h(e) = \prod_{p|e} 2\cos(2\pi h r_p/p)$ has
  mean zero across primes $p \equiv 1 \pmod 4$ where $r_p$ varies with $p$.
  For $h = 1$, $r_p$ is a fixed root of $-1 \pmod p$.  The cancellation in
  $\widetilde S_h$ comes from this $r_p$-equidistribution, which is
  Hooley §3 / Erdős–Hooley territory (uniform discrepancy of $\{r_p/p\}$
  across split primes $p \le N^{1/2}$).

- **At $h \gtrsim \sqrt N$:** the unweighted $e$-direction phase already
  oscillates fast, B-process gains, and the rooted sum is dominated by the
  unweighted analysis.  Trivial.

The hard regime is $1 \le h \le \sqrt N$, and the rigorous tool there is
*not* van der Corput on $e$ — it is **multiplicative cancellation in
$\widetilde S_h(e)$ averaged over $e$**, equivalently a Halász-type bound
on $\sum_{e \le N, \mathrm{sf, good}} \widetilde S_h(e)$ for fixed $h$.

This is structurally similar to Hooley 1957 §3 for the $\sum_n d(n^2+1)$
problem, and it remains the open analytic content.

## 7. Caveats

1. **Range of $h$ tested.**  Sweep up to $h = 10^4$ at $N = 10^6, 10^7$.
   Beyond that the asymptotic balance $|U_h| \asymp \sqrt{hN}$ should kick
   in even more cleanly.  Did not test $h$ super-polynomial in $N$.

2. **Indicator $\mathbf 1_{\mathrm{sf, good}}$.**  Restricting to "good" sf
   $e$ (no $p \equiv 3 \pmod 4$ factors) is a natural-density restriction
   with $|\{\text{sf, good }e \le N\}| \sim c N$ for an explicit $c \in (0, 1)$.
   The B-process derivation in §2 implicitly uses this restriction; the
   constants change but the *rate* $\min(\sqrt{hN}, N/\sqrt h)$ does not.

3. **B-process is not the only available process** — but the issue with
   transferring back to $T_h$ is structural, not just about $U_h$.  See §5
   for the explicit Cauchy–Schwarz calculation showing that even the
   counterfactual ideal $U_h \ll 1$ would only give $T_h \ll \sqrt N \log^{c/2} N$,
   not the desired uniform bound.

4. **Empirical rate is not asymptotic.**  $|U_1(N)|/N$ drifts from
   $0.0193$ at $N = 10^5$ to $0.0165$ at $N = 10^7$ — slow but persistent
   decay.  Could be $1/\log N$, $1/(\log N)^c$, or just transient.  The
   data does not rule out $|U_1(N)| = o(N)$ asymptotically; it does rule
   out $|U_1(N)| = O(N^{1/2+\epsilon})$ over the empirical range.

## 8. Status

- **Verdict:** PROGRESS (negative, ruling out a route is useful).
- **Rigor accounting unchanged.** No new rigorous content; what changes is
  the *roadmap* for closing Lemma 3.4.
- **Demoted thread:** B-process on unweighted $e$-sum (pickup hint #1).
- **Re-confirmed thread (highest EV):** Halász / Hooley-§3 cancellation
  in $\widetilde S_h(e)$ uniform in $h$.

## 9. Files

- `bot/scratch/Uh-vs-Th-empirical.py` — paired computation $(U_h, T_h)$.
- `bot/scratch/Uh-h-sweep.py` — $U_h$ across 18 values of $h$ at fixed $N$.
- `bot/scratch/Uh-N1e7.py` — $|U_h|$ at $N = 10^7$ for a few $h$.
- Builds on: `P12-Lemma-3-4-empirical-Th.md` (prev session, $T_h$ scan),
  `P12-Lemma-3-4-reduction.md` (the Fourier reduction).
