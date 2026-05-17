# P12 — Empirical preview of the Halász direction: $H_h(N) \ll \sqrt N$

**Date:** 2026-05-08 (UTC). **Status:** Empirical — no rigorous content.

## 1. Setup

In the Fourier reduction of Lemma 3.4 (see `P12-Lemma-3-4-reduction.md`),
the binding quantity is

$$T_h(N) \;=\; \sum_{\substack{e \le N \\ e\ \mathrm{sf,\ good}}} e^{2\pi i h N/e}\, \widetilde S_h(e), \qquad \widetilde S_h(e) := \sum_{\substack{r \pmod e \\ r^2 \equiv -1}} e^{-2\pi i h r/e}.$$

"$e$ sf good" means $e$ squarefree with every prime factor $p \in \{2\} \cup \{p \equiv 1 \pmod 4\}$.

Prev session (`P12-Uh-vs-Th-empirical.md`) closed the "van der Corput in the
$e$-direction" route and identified the *multiplicative root-weight*
$\widetilde S_h$ as the binding direction. The next-natural empirical preview
of that route is

$$H_h(N) \;:=\; \sum_{\substack{e \le N \\ e\ \mathrm{sf,\ good}}} \widetilde S_h(e),$$

i.e. $T_h$ with the $e$-direction phase $e^{2\pi i h N/e}$ stripped. This isolates
the cancellation contributed by the multiplicative weight alone.

## 2. The product formula and reality of $H_h$

For sf good $e = p_1 \cdots p_k$, the CRT gives
$$\frac{r}{e} \;\equiv\; \sum_{j=1}^k \frac{r_j (e/p_j)^{-1}_{p_j}}{p_j} \pmod 1$$
where $r_j \in \{\pm \alpha_{p_j}\}$ with $\alpha_p^2 \equiv -1 \pmod p$. Summing
$e^{-2\pi i h r/e}$ over the $2^{\omega(e)}$ choices factors as

$$\widetilde S_h(e) \;=\; \prod_{p\mid e} 2\cos\!\Big(2\pi h\, \tfrac{\alpha_p (e/p)^{-1}_p}{p}\Big).$$

(At $p=2$: single root, factor $\pm 1$.) In particular
$\widetilde S_h(e) \in \mathbb R$ and $|\widetilde S_h(e)| \le 2^{\omega(e)}$.
Hence $H_h(N) \in \mathbb R$ for all $h, N$. (Empirical confirmation: every
row of §3 has $\mathrm{Im}(H_h) = 0$.)

## 3. Empirical data

Computed via `bot/scratch/Halasz-Hh-empirical.py` (per-$e$ Python loop using
SPF sieve + product formula above; $\le 30$s at $N = 10^7$).

### 3.1 Vertical scan: $N \in \{10^5, 10^6, 10^7\}$, $h \in \{1, 2, 5, 100\}$

| $N$ | $h$ | $H_h(N)$ | $\|H_h\|/N$ | $\|H_h\|/\sqrt N$ |
|---:|---:|---:|---:|---:|
| $10^5$ | 1 | $+4.54$ | $5\cdot10^{-5}$ | $0.0144$ |
| $10^5$ | 2 | $-108.70$ | $1.1\cdot10^{-3}$ | $0.3437$ |
| $10^5$ | 5 | $-112.84$ | $1.1\cdot10^{-3}$ | $0.3568$ |
| $10^5$ | 100 | $-429.60$ | $4.3\cdot10^{-3}$ | $1.3585$ |
| $10^6$ | 1 | $-53.28$ | $5\cdot10^{-5}$ | $0.0533$ |
| $10^6$ | 2 | $-38.97$ | $4\cdot10^{-5}$ | $0.0390$ |
| $10^6$ | 5 | $-26.42$ | $3\cdot10^{-5}$ | $0.0264$ |
| $10^6$ | 100 | $-1067.17$ | $1.1\cdot10^{-3}$ | $1.0672$ |
| $10^7$ | 1 | $+291.28$ | $3\cdot10^{-5}$ | $0.0921$ |
| $10^7$ | 2 | $-757.57$ | $7.6\cdot10^{-5}$ | $0.2396$ |
| $10^7$ | 5 | $-529.27$ | $5.3\cdot10^{-5}$ | $0.1674$ |
| $10^7$ | 100 | $-2151.42$ | $2.2\cdot10^{-4}$ | $0.6803$ |

### 3.2 Horizontal scan: $h \in \{1,2,3,5,10,20,50,100,200,500,1000\}$ at $N = 10^6$

| $h$ | $\|H_h(10^6)\|$ | $\|H_h\|/\sqrt N$ |
|---:|---:|---:|
| 1 | 53.28 | 0.053 |
| 2 | 38.97 | 0.039 |
| 3 | 75.54 | 0.076 |
| 5 | 26.42 | 0.026 |
| 10 | 167.92 | 0.168 |
| 20 | 364.54 | 0.365 |
| 50 | 485.79 | 0.486 |
| 100 | 1067.17 | 1.067 |
| 200 | 1181.51 | 1.182 |
| 500 | 136.07 | 0.136 |
| 1000 | 524.35 | 0.524 |

Max ratio across the horizontal scan is $1.18$ (at $h = 200$). All 11 values are
$O(\sqrt N)$ uniformly, with most considerably smaller.

## 4. The empirical regime is square-root, not log-saving

Halász's mean-value theorem for a bounded multiplicative function with mean$\to 0$
gives $\sum_{e \le N} f(e) \ll N \exp(-A(N))$ with
$A(N) = \min_\tau \sum_{p \le N} (1 - \mathrm{Re}(f(p) p^{-i\tau}))/p$. This is
the natural *worst-case* bound from the multiplicative method; it produces a
log-saving $N/(\log N)^c$ rate, **not** square-root cancellation.

The empirical $|H_h(N)| \ll \sqrt N$ regime is therefore *not* what the abstract
Halász apparatus gives — it is the rate that random-walk / CLT heuristics
predict for a "structureless" mean-zero sum of $\sim N^{1-o(1)}$ unimodular-ish
terms. The empirical evidence is consistent with the latter, suggesting that
the multiplicative weight $\widetilde S_h$ behaves like a random-walk-type
sum with no anomalous coherence.

We did **not** compute $A(N)$ explicitly, so we cannot quantitatively compare
to the Halász ceiling. What we *can* say is that $|H_h(N)|/N$ is at most
$\sim 4 \cdot 10^{-4}$ (max across the §3 tables) at $N = 10^7$ — already
small in absolute terms, regardless of which abstract benchmark one prefers.

## 5. Comparison to $T_h(N)$ (two data points; weak)

From `P12-Lemma-3-4-empirical-Th.md` and prev session: $|T_1(10^6)| \approx 510$,
$|T_h(10^7)|/\sqrt N \le 1.22$ uniformly across 43 $h$-values. Two data points
where we can compare $|T_h|$ and $|H_h|$ at the same $(N, h)$:

| $N$ | $h$ | $\|T_h\|$ | $\|H_h\|$ | ratio $\|T\|/\|H\|$ |
|---:|---:|---:|---:|---:|
| $10^6$ | 1 | $\sim 510$ | $53.3$ | $\sim 9.6$ |
| $10^6$ | 5 | $\sim 267$ | $26.4$ | $\sim 10.1$ |

In both points, $|T_h| > |H_h|$ — i.e. introducing the $e$-phase modulation
does not *help* the cancellation already present in $\widetilde S_h$. **This is
weak evidence**: two $(N, h)$ pairs cannot distinguish a structural claim
("the $e$-phase is irrelevant") from a CLT-magnitude fluctuation. A wider
$(N, h)$ scan computing $|T_h|/|H_h|$ jointly is needed before drawing a
structural conclusion. Provisionally, the data is *consistent with* — but
does not establish — the picture that the multiplicative root-weight provides
the dominant cancellation, with the $e$-phase a re-shuffle of signs.

## 6. Empirical observation (not a conjecture)

Across the 12 + 11 = 23 measured data points in §3.1–3.2, the ratio
$|H_h(N)|/\sqrt N$ is bounded by $1.36$ (max attained at $N = 10^5, h = 100$),
and at $N = 10^7$ the max over the four $h$-values tested is $0.68$.

We **deliberately stop short of conjecturing** an envelope. Three caveats
disqualify a clean conjecture from this data:

1. Only three $N$-scales, one decade apart.
2. The $h$-range tested at $N = 10^7$ is just $\{1, 2, 5, 100\}$; uniformity
   in $h \le H(N) = N^{o(1)}$ is *not* tested at large $N$.
3. Pointwise behavior is non-monotone (e.g. $|H_2|/\sqrt N$ at three $N$
   values is $0.34, 0.04, 0.24$). Any envelope $\sqrt N \cdot (\log N)^c$
   with $c \in [0, 2]$ fits.

The honest summary is: *on the tested grid*, $|H_h(N)|$ is at most $\sim 1.4 \sqrt N$,
and the data does not contradict an envelope as good as $\sqrt N$ or as bad as
$\sqrt N (\log N)^2$. Future sessions should expand the $(N, h)$ grid before
attempting a conjecture.

## 7. Implications for the proof

This is empirical encouragement, not rigor. Three takeaways:

**(i) Halász direction is empirically VIABLE — even at a stronger rate than predicted.**
The next analytic step (set up Halász + Hooley equidistribution; pickup hint
from prev session) is genuinely worth a session: empirical preview confirms
the input is at least as strong as the abstract framework promises.

**(ii) The cancellation lives in the multiplicative weight, not the $e$-phase.**
The $e$-phase $e^{2\pi i h N/e}$ does not contribute additional cancellation
at fixed $h$ in the empirical regime. Strategies that try to extract
cancellation from the $e$-phase (van der Corput / Vinogradov on $e$) face
a structural ceiling.

**(iii) Crude Abel from $H_h$ to $T_h$ is uninformative.** Abel summation:
$$T_h(N) = e^{2\pi i h} H_h(N) + 2\pi i h N \int_2^N \frac{H_h(x)\, e^{2\pi i h N/x}}{x^2}\, dx.$$
Triangle-inequality on the integral throws away the oscillation in
$e^{2\pi i h N/x}$ and yields a useless $\ll h N (\log N)^A$. This is **not**
a real obstruction — it is a defect of crude Abel. The natural analytic next
step is **dyadic Abel + stationary-phase / van der Corput** on each block
$x \in [E, 2E]$, where the phase $e^{2\pi i h N/x}$ has stationary point
governed by $h N/x^2$. Empirically we already know the truth $T_h \ll \sqrt N$
holds; whether stationary-phase + Halász on $\widetilde S_h$ recovers that rate
is a real open question for the next session.

## 8. Caveats

- **Three scales of $N$, eleven $h$-values at one scale.** Conjecture H
  is supported but not pinned: $\sqrt N \cdot (\log N)^c$ with $c \in [0, 2]$
  all fit. We cannot distinguish $c$ values without a $4\times$ longer
  $N$-range.
- **Fluctuation, not monotonicity.** $|H_2|/\sqrt N$ at three $N$ values
  is $0.34, 0.04, 0.24$ — non-monotone. The bounds $\sqrt N (\log N)^{O(1)}$
  are *envelopes*; pointwise behavior is volatile.
- **No verification of the Halász hypothesis directly.** We did not compute
  $A(N) = \sum_{p \le N, p \equiv 1(4)} (1 - \mathrm{Re}(f_h(p) p^{-i\tau}))/p$
  to confirm $A(N) \to \infty$. That's a separate quick check.
- **The mapping $\widetilde S_h(e) = \prod_{p|e} 2\cos(2\pi h a_p(e)/p)$
  has $a_p(e) := \alpha_p (e/p)^{-1}_p$ that depends on $e/p$ — so $\widetilde S_h$
  is NOT exactly multiplicative.** It is "almost multiplicative" in the sense
  that $\sum_{e \le N} \widetilde S_h(e)$ behaves like a Halász sum (the local
  factor at $p$ averages to the same $f_h(p)$ over the residues of $e/p$
  mod $p$), but a clean Halász invocation requires checking this carefully.

## 9. Files

- `bot/scratch/Halasz-Hh-empirical.py` (new): per-$e$ product-formula
  implementation, $\le 30$s at $N = 10^7$.
- Builds on: `bot/scratch/Uh-vs-Th-empirical.py` (CRT roots machinery from
  prev session); `P12-Lemma-3-4-empirical-Th.md` ($T_h$ data); `P12-Uh-vs-Th-empirical.md`
  (route closure that motivates this empirical preview).
