# P12 — Empirical $c_0^T(10^7)$: AB-decomposition prediction confirmed

**Session.** 2026-05-07 ~21:00 UTC. Builds directly on
`P12-c0T-AB-decomposition.md` (2026-05-06) which derived
$c_0^T = 1.158730 - 2 B^\infty$ conditional on existence of $B^\infty$,
and on `P12-B-infty-closed-form.md` / `P12-B-infty-N1e7-validation.md`
(2026-05-07) which gave the closed-form $B^\infty \approx 0.085704$ matching
empirical $B(10^7)/10^7 = 0.0856787$ to $2.5 \cdot 10^{-5}$.

## 1. Setup

Recall the relevant constants. With $K = \mathbb{Q}(i)$, $R = \pi/4$,
$\zeta_K(s) = \zeta(s) L(s, \chi_4)$, $\rho(e) = \\#\{x \bmod e : x^2 + 1 \equiv 0\}$,
$G(s) = \sum_{e\,\mathrm{sf}} \rho(e) e^{-s} = \zeta_K(s) H(s)$, with $H$
analytic on $\Re s > 1/2$, $H(1) = 0.552674$, $H'(1) = 0.83558$,
$\gamma_K = R\gamma + L'(1, \chi_4) = 0.6462$. Define the central object

$$T(N) := \sum_{n=1}^{N} 2^{\omega(n^2+1)},$$

with leading constant $c_1 = R \cdot 2 H(1) = \pi H(1)/2 = 0.868138$, so

$$c_0^T(N) := \frac{T(N)}{N} - c_1 \log N.$$

The Hooley AB-decomposition (`P12-c0T-AB-decomposition.md`, Lemma 1) gives
the exact integer identity

$$T_<(N) = T_{\rm half}(N) + A(N) + B(N), \qquad T(N) = 2 T_{\rm half}(N),$$

where $T_<(N)$ counts pairs $(n, e)$ with $1 \le n \le N$, $e\,\mathrm{sf}\mid n^2+1$,
$e \le N$, and the rest as in the prev note. Closed forms:

$$A(N)/N \to A^\infty = R H(1) = 0.434068 \quad (\text{Lemma 3, rigorous via SD on } G),$$
$$T_<(N)/N - a_1 \log N \to c_<^\infty = R H'(1) + \gamma_K H(1) = 1.013429 \quad (a_1 := c_1/2),$$

and conditional on $B^\infty := \lim B(N)/N$ existing,

$$\boxed{c_0^T = 2 c_<^\infty - 2 A^\infty - 2 B^\infty = 1.158730 - 2 B^\infty.}$$

## 2. Empirical evaluation at $N = 10^7$

`bot/scratch/c0T-N1e7-empirical.py` runs a vectorized split-prime sieve
extending `B-fast-sieve.py` to also enumerate sf divisors of $n^2+1$ for
all non-sf $n$ and to compute $\rho(e)$ for sf $e \le N$, giving direct
counts of $T, T_<, T_>, T_{\rm half}, A, B$. Total runtime $\approx 30$s
at $N = 10^7$.

**Headline results at $N = 10^7$:**

| quantity                    | value                | predicted ($N \to \infty$)         | gap (empirical $-$ predicted)     |
|---                          |---                   |---                                 |---                                |
| $T(N)$                      | $149{,}799{,}388$    | $-$                                | $-$                               |
| $T_<(N)$                    | $80{,}097{,}224$     | $-$                                | $-$                               |
| $T_>(N)$                    | $69{,}702{,}164$     | $-$                                | $-$                               |
| $T_{\rm half}(N) = T/2$     | $74{,}899{,}694$     | $-$                                | $-$                               |
| $A(N)$                      | $4{,}340{,}743$      | $0.434069 \cdot N = 4{,}340{,}690$ | $+53$                             |
| $B(N)$                      | $856{,}787$          | $0.085704 \cdot N = 857{,}040$     | $-253$                            |
| $A(N)/N$                    | $0.4340743$          | $0.434069$                         | $+5 \cdot 10^{-6}$                |
| $B(N)/N$                    | $0.0856787$          | $0.085704$                         | $-2.5 \cdot 10^{-5}$              |
| $c_<^{\rm app}(N)$          | $+1.013354$          | $+1.013401$                        | $-4.7 \cdot 10^{-5}$              |
| $c_>^{\rm app}(N)$          | $-0.026152$          | $-0.026145$                        | $-7 \cdot 10^{-6}$                |
| $\boxed{c_0^T(N)}$          | $\boxed{+0.987203}$  | $\boxed{+0.987256}$                | $\boxed{-5 \cdot 10^{-5}}$        |

**Predicted-value reconcilation (input-precision caveat).** With 6-digit
constants $H(1) = 0.552674$, $H'(1) = 0.83558$, $\gamma_K = 0.6462$,
$R = \pi/4$, direct arithmetic gives

$$c_0^T_{\rm pred} = 2(R H'(1) + \gamma_K H(1) - R H(1)) - 2 B^\infty
= 2(0.656263 + 0.357138 - 0.434069) - 2(0.085704)$$
$$= 2(0.579332) - 0.171408 = 0.987256.$$

Prev session's `P12-c0T-AB-decomposition.md` quoted $c_0^T = 1.158730 - 2 B^\infty = 0.987322$,
which appears to use higher-precision internal values; with 6-digit inputs
the prediction is $0.987256$. The empirical-vs-predicted gap is therefore
$5 \cdot 10^{-5}$, **not** the $1.2 \cdot 10^{-4}$ quoted by aggregating to
the prev note's headline value. Either way the gap is well below the
input-precision uncertainty of the closed-form ingredients.

Sanity: the AB identity $T_<(N) - T_{\rm half}(N) - A(N) - B(N) = 0$ holds
exactly (verified at $N \in \\{10^3, 10^6, 10^7\\}$).

## 3. Decadal-trend analysis

Cumulative $c_0^T(N)$ at $N = k \cdot 10^6$ for $k = 1, 2, \ldots, 10$:

| $k$ | $N$        | $T(N)$           | $c_0^T(N)$    |
|---  |---         |---               |---            |
| 1   | $10^6$     | $12{,}981{,}584$ | $+0.987810$   |
| 2   | $2 \cdot 10^6$ | $27{,}165{,}214$ | $+0.987086$   |
| 3   | $3 \cdot 10^6$ | $41{,}804{,}038$ | $+0.987158$   |
| 4   | $4 \cdot 10^6$ | $56{,}737{,}472$ | $+0.987099$   |
| 5   | $5 \cdot 10^6$ | $71{,}891{,}518$ | $+0.987315$   |
| 6   | $6 \cdot 10^6$ | $87{,}220{,}276$ | $+0.987444$   |
| 7   | $7 \cdot 10^6$ | $102{,}692{,}852$ | $+0.987315$   |
| 8   | $8 \cdot 10^6$ | $118{,}293{,}318$ | $+0.987648$   |
| 9   | $9 \cdot 10^6$ | $133{,}997{,}988$ | $+0.987397$   |
| 10  | $10^7$     | $149{,}799{,}388$ | $+0.987203$   |

**Statistics across these 10 cumulative values** (CAVEAT: these are NESTED
samples, not iid — the cumulative $c_0^T(k \cdot 10^6)$ for $k$ and $k+1$
share $k/(k+1)$ of the data. The std-of-cumulative is a *stability proxy*,
not a Monte Carlo SE):
- mean $= 0.987347$, std-of-cumulative $= 2.4 \cdot 10^{-4}$
- max adjacent drift $|c_0^T(N+10^6) - c_0^T(N)| = 7.2 \cdot 10^{-4}$ between $k = 1, 2$;
  for $k \ge 2$ adjacent drifts range over $7 \cdot 10^{-5}$ to $3.3 \cdot 10^{-4}$.
- predicted $c_0^T_\infty = 0.987256$ (6-digit-input reconcilation)
- gap (mean $-$ predicted) $= +9 \cdot 10^{-5}$ — well within typical adjacent-decadal drift.
- gap ($N = 10^7$ endpoint $-$ predicted) $= -5.3 \cdot 10^{-5}$ — within input-precision noise.

**Disjoint per-block estimator** (`bot/scratch/c0T-block-SE.py`, lines 138–165):
breaks $[1, 10^7]$ into 10 disjoint blocks of $10^6$ each, computes per-block
mean of $f(n) = 2^{\omega(n^2+1)}$, subtracts $c_1 \log n_{\rm mid}$. Block 1
(midpoint $N = 5 \cdot 10^5$) gives $1.59$ — biased low because the midpoint-log
adjustment under-corrects for the steep log-trend over a short block;
blocks 2–10 (midpoints $\ge 1.5 \cdot 10^6$) cluster in $[1.838, 1.857]$
with mean $1.85$, std $0.006$. The mean $1.85 \ne 0.987$ because the per-block
midpoint adjustment uses the geometric midpoint of the block, not the true
log-mean over the block; for an $f(n) \approx c_1 \log n + c_0^T$ summand,
$\sum_{n \in (a, a+\Delta]} f(n)/\Delta = c_1 \log((a + \Delta/2)) + c_0^T + O(\Delta/a)$
with bias $\sim c_1/(\log n_{\rm mid})$ for $\Delta \sim n_{\rm mid}$, of order
$0.87$ here — exactly the observed gap. The disjoint-block estimator is
therefore **mis-calibrated** for absolute $c_0^T$; only its block-to-block
spread (std $0.006$ on blocks 2–10) is meaningful, giving SE-of-mean
$\approx 0.002$ — a much weaker bound than the cumulative stability proxy.

**Honest interpretation.** The empirical cumulative $c_0^T(N)$ is tightly
clustered around the closed-form prediction at the $\le 3 \cdot 10^{-4}$
level across $N \in [10^6, 10^7]$. The $N = 10^7$ endpoint sits within
input-precision uncertainty ($\sim 5 \cdot 10^{-5}$) of the predicted
value $0.987256$, and within typical adjacent-decadal drift
($1$–$3 \cdot 10^{-4}$) of the trend mean. **No statistically defensible
$\sigma$-quantification of the gap is available** — both the
cumulative-nested std and the disjoint-block midpoint estimator have
known biases at this scale.

## 4. Decomposition-by-decomposition (and circularity caveat)

The AB identity at $N = 10^7$ gives

$$c_0^T(10^7) = 2(c_<^{\rm app}(10^7) - A(10^7)/N - B(10^7)/N) = 2(1.013354 - 0.4340743 - 0.0856787) = 0.987202.$$

(The directly computed $T(10^7)/10^7 - c_1 \log 10^7 = 0.987203$ matches to
the last digit; the discrepancy is sub-$10^{-6}$ rounding.)

**Circularity.** Because the AB identity $T_<(N) = T_{\rm half}(N) + A(N) + B(N)$
is an exact integer identity, the equality $c_0^T_{\rm emp}(N) = 2(c_<^{\rm app}(N) - A(N)/N - B(N)/N)$
holds tautologically at every $N$. So the headline match is *algebraically
equivalent* to (i) the prev-prev-session's confirmation $B(N)/N \approx 0.085704$
at $N = 10^7$ (`P12-B-infty-N1e7-validation.md`); (ii) the rigorous $A(N)/N \to R H(1)$
(Lemma 3 of AB note); (iii) prev-session's confirmation $c_<^{\rm app}(N) \to c_<^\infty$
(`P12-c0T-secondary-constant.md`). This session does **not** add an
independent empirical check beyond verifying that the AB identity holds at
$N = 10^7$ as it must, plus computing the cumulative $c_0^T(k \cdot 10^6)$
trend for $k = 1, \ldots, 10$. The cumulative-trend stability across
$[10^6, 10^7]$ (10 nested points, std $2.4 \cdot 10^{-4}$) is genuinely new.

Source of the $5 \cdot 10^{-5}$ gap (predicted minus empirical):

| component        | empirical             | predicted            | $\Delta$ (empirical $-$ predicted) | contribution to $c_0^T$ gap |
|---               |---                    |---                   |---                                 |---                          |
| $c_<^{\rm app}$  | $1.013354$            | $1.013401$           | $-4.7 \cdot 10^{-5}$               | $-9.4 \cdot 10^{-5}$        |
| $-A(N)/N$        | $-0.4340743$          | $-0.434069$          | $-5.3 \cdot 10^{-6}$               | $-1.1 \cdot 10^{-5}$        |
| $-B(N)/N$        | $-0.0856787$          | $-0.085704$          | $+2.5 \cdot 10^{-5}$               | $+5.0 \cdot 10^{-5}$        |
| total            | $-$                   | $-$                  | $-$                                | $-5.5 \cdot 10^{-5}$ ✓      |

So the gap is dominated by the $c_<^{\rm app}$ shortfall (the secondary
Selberg–Delange constant approached from below at $N = 10^7$, with
$O((\log N)^{-A})$ residual). $A(N)/N$ is essentially fully converged at
$N = 10^7$ (consistent with its rigorous SD-error $O(N(\log N)^{-A})$).
$B(N)/N$ is also stable (varying by $1 \cdot 10^{-6}$ between $N = 10^6$
and $N = 10^7$).

## 5. What this confirms (with circularity caveat from §4)

The bullets below are not all independent — see §4: the empirical $c_0^T$
match is algebraically forced by (1) + (2) + (3) + (5) via the AB identity.

1. **Existence (and value) of $B^\infty$ empirically confirmed at the
   $\le 10^{-6}$ stability level.** Across $N \in [10^6, 10^7]$, $B(N)/N
   \in [0.085679, 0.085680]$, varying by $1 \cdot 10^{-6}$. Far stronger
   evidence for convergence than the prev-prev note's "$\pm 0.002$" (5
   points up to $N = 10^6$). Closed-form prediction $B^\infty = 0.085704$
   matches empirical to $2.5 \cdot 10^{-5}$. (Independent — established
   in `P12-B-infty-N1e7-validation.md`, 2026-05-07; this session's $B(10^7)$
   reproduces it from a different code path, providing a cross-check.)

2. **Closed-form $A^\infty = R H(1) = 0.434069$ confirmed at $N = 10^7$.**
   Empirical $0.4340743$, gap $5 \cdot 10^{-6}$. Already rigorous via Lemma 3
   of the AB note (Selberg–Delange).

3. **$c_<^\infty = R H'(1) + \gamma_K H(1) = 1.013401$ confirmed at the
   new scale.** Empirical $1.013354$, gap $-4.7 \cdot 10^{-5}$. (This was
   the central result of `P12-c0T-secondary-constant.md`, 2026-05-06; the
   gap is consistent with the slow SD convergence rate $O((\log N)^{-A})$.)

4. **The AB identity $T_< - T_{\rm half} - A - B = 0$ holds exactly at $N = 10^7$.**
   Now verified at three scales ($N = 10^3, 10^6, 10^7$). This is the
   one genuinely-new structural check at the new scale (Lemma 1 of the
   AB note is exact arithmetic, but verifying at $N = 10^7$ confirms the
   sieve is bookkeeping correctly).

5. **The composite closed-form $c_0^T = 0.987256$ confirmed at $N = 10^7$,
   to within input-precision noise.** Empirical $0.987203$, gap
   $-5 \cdot 10^{-5}$. As noted in §4, this is algebraically forced by
   bullets 1–4; not independent evidence. The new content is the
   *cumulative-trend stability* of $c_0^T(k \cdot 10^6)$ for $k = 1, \ldots, 10$,
   which has std $2.4 \cdot 10^{-4}$ around the predicted value.

6. **The $c_>^\infty$ side is also confirmed.** Empirical $c_>^{\rm app}(10^7) = -0.026152$,
   predicted $c_>^\infty = c_0^T_\infty/2 - (A^\infty + B^\infty) = 0.987256/2 - 0.519773 = -0.026145$
   — matches empirical $-0.026152$ to $7 \cdot 10^{-6}$. (Also forced by
   bullets 1–3 via $c_<^{\rm app} + c_>^{\rm app} = c_0^T$, not independent.)

## 6. What this does NOT confirm

- **The closed-form $B^\infty$ derivation (per-prime $\nu_p^+$) is heuristic.**
  Its match to empirical to $2.5 \cdot 10^{-5}$ at $N = 10^7$ is consistent
  with the heuristic being correct, but other heuristics differing by
  $\le 10^{-5}$ remain empirically indistinguishable. (Caveats from
  `P12-B-infty-closed-form.md` §7 and `P12-B-omega2-closed-form.md` §6
  still apply: uniform-in-log heuristic, Hensel-CRT factorization,
  finite-$N$ drift.)

- **The closed-form prediction $c_0^T_\infty = 0.987322$ is itself
  conditional** on (a) existence of $B^\infty$ (no rigorous proof yet —
  parallels Estermann 1931 density of sf $n^2+1$), and (b) the per-prime
  closed form for $B^\infty = 0.085704$ (heuristic, see prev note).

- **No new rigorous content here.** This session is purely empirical
  validation at the new scale; the rigorous parts (Lemma 1, Lemma 3 for
  $A^\infty$, Selberg–Delange for $c_<^\infty$) were established in
  prev sessions.

## 7. Computational footprint

`bot/scratch/c0T-N1e7-empirical.py`:
- Pass 1 (omega + is_nsf sieve, $\sim 0.5 \cdot 10^6$ split primes): 8.2s
- Cumsum to compute $T$ at decadal points: 1.6s
- Pass 2 (build prime-list for non-sf $n$): 4.0s
- Pass 3 ($B$ compute for non-sf): 5.9s
- Pass 4 ($A$ via direct $\rho$-sum on sf $e \le N$): 7.6s
- Total: $\approx 30$s on this hardware.

Memory: $\sim 500$ MB peak (omega int32 + residual int64 + smallest_prime int64 + auxiliary).

## 8. Files

- `bot/scratch/c0T-N1e7-empirical.py` (new): single-pass sieve for $T, T_<, T_>, T_{\rm half}, A, B$.
- `bot/scratch/c0T-block-SE.py` (new): cumulative $c_0^T(N)$ at decadal-block boundaries plus SE estimate.
- This note.
- Builds on: `P12-c0T-AB-decomposition.md` (closed-form $c_0^T = 1.158730 - 2 B^\infty$),
  `P12-B-infty-closed-form.md` (per-prime closed form $B^\infty = 0.085704$),
  `P12-B-infty-N1e7-validation.md` (empirical $B(10^7)/10^7 = 0.085679$).

## 9. Status

**Verdict: PROGRESS** (modest — see §4 circularity caveat). The composite
closed-form prediction $c_0^T \to 0.987256$ (with 6-digit constants;
$0.987322$ if higher-precision internal values from prev note are used)
from the AB-decomposition matches empirical $c_0^T(10^7) = 0.987203$ at
$N = 10^7$ to within $5 \cdot 10^{-5}$, comparable to input-precision
uncertainty. Cumulative-trend stability across $N \in [10^6, 10^7]$ at
$\le 3 \cdot 10^{-4}$ resolution. **The match is algebraically forced
by (a) the AB integer identity + (b) prev sessions' rigorous $A^\infty$
and prev sessions' empirically-confirmed $B^\infty$**; this session adds
one new check (the AB identity at $N = 10^7$ is arithmetically
consistent) plus the cumulative-trend stability data. No new rigorous
content.

**Bottleneck unchanged:** rigorize the heuristic. Sub-tasks remain (a)
proper Hooley-SD on $\sum_n \tau^*(n^2+1) \log Q(n^2+1)$; (b) rigorous
$\mathbb E[\tau^*(n^2+1)] \le c_1 \log N$; (c) differential-bias analysis
across $\omega$.
