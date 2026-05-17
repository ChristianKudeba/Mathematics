# P12 — Cumulative second moment $V(N) = \sum_{M\le N} T(M)^2$ — empirical extension

**Date:** 2026-05-04 03:39 UTC
**Author:** Claude (mathAI bot)
**Status:** PROGRESS / CONSENSUS-WITH-CAVEAT (after Round 1 skeptic forced retraction of a sub-claim)

## Setup

For the $\sigma$-spin sum
$$T(N) := \sum_{n=1}^{N} \tau(n^2+1)\,\chi_4(n+1),$$
define the **cumulative second moment**
$$V(N) := \sum_{M=1}^{N} T(M)^2.$$

If $T(M) = O(\sqrt{M})$ in mean square (i.e. $T(M)^2 \sim \sigma^2 M$ on average) **AND** the partial sums of $T(M)^2$ self-average along a single sequence, then
$$V(N) \sim \frac{\sigma^2}{2} N^2, \qquad \frac{V(N)}{N^2} \to \frac{\sigma^2}{2} =: C^\dagger.$$
This $C^\dagger$ is the natural cumulative analogue of the windowed constant $C^*$ studied in `P12-second-moment-empirical-extension.md` (where $\mathcal{D}_0/N^2 \to C^*$ over $M \in (N, 2N]$).

**Caveat on the limit's existence:** as the §"Theoretical RW variance" section below makes explicit, the second self-averaging hypothesis is non-trivial. Under a Gaussian RW model, $V(N)/N^2$ does **not** converge along a single path — each realization has a different limit $C_{\mathrm{path}}$ with mean $\sigma^2/2$ and std $\sigma^2/\sqrt 3$. So $C^\dagger$ as a deterministic constant is meaningful only if the deterministic spin sum has structure beyond what RW provides.

## Result

Computed $T(M)$ for all $M \le 10^7$ via tau-of-$n^2{+}1$ sieve (`bot/scratch/V-cumulative.py`, runtime $\approx 13$ s). Then $V(N)$ for all $N \le 10^7$ in $0.6$ s.

### Cumulative ratio at log-spaced $N$

| $N$ | $V(N)/N^2$ |
|---|---|
| $10^3$ | $0.2335$ |
| $10^4$ | $0.2587$ |
| $10^5$ | $0.2041$ |
| $10^6$ | $0.1662$ |
| $10^7$ | $0.1937$ |

### Dense scan in upper half $N \in [5\times 10^6, 10^7]$

$V(N)/N^2$ at $N = j \cdot 5\times 10^4$ for $j = 101, \dots, 200$ (100 sample points):

- mean $= 0.2796$
- std $= 0.0574$
- min $= 0.1934$, max $= 0.3711$
- **rel std/mean $= 0.205$**.

### Smoothed estimator (avg over 100 $N$-values in $[N_0, 2N_0]$)

| $N_0$ | smoothed $V/N^2$ | std (within-window) |
|---|---|---|
| $10^4$ | $0.197$ | $0.038$ |
| $5 \times 10^4$ | $0.226$ | $0.019$ |
| $10^5$ | $0.183$ | $0.020$ |
| $5 \times 10^5$ | $0.215$ | $0.038$ |
| $10^6$ | $0.268$ | $0.072$ |
| $2 \times 10^6$ | $0.164$ | $0.022$ |
| $5 \times 10^6$ | $0.281$ | $0.057$ |

Across-$N_0$ range: $[0.16, 0.28]$.

## Random-walk null model — within-path comparison (corrected after Round 1 skeptic)

**A first draft of this note compared the empirical "rel std/mean = $0.205$" against the *ensemble* RW prediction $2/\sqrt 3 \approx 1.155$ and concluded "$5.6\times$ suppression $\Rightarrow$ mean-reverting structure."  This comparison was wrong** — the empirical statistic is the within-path std of $V(N)/N^2$ as $N$ varies on a single deterministic sequence, not the ensemble std at fixed $N$ across realizations.  The cumulative construction of $V$ guarantees small within-path fluctuation across nearby $N$, regardless of any structural hypothesis.

The correct null comparison is a Monte Carlo: simulate Gaussian RWs and compute the within-path std of $V(N)/N^2$ over the same sliding-$N$ range.  Result (`bot/scratch/V-rw-simulation.py`, $\sigma^2 = 0.4$ chosen to match empirical $V/N^2 \approx 0.2$; note the *relative* std/mean is scale-invariant in $\sigma^2$, so this calibration affects the absolute scale of the simulated $V/N^2$ but not the ratio that we compare against the empirical $0.205$):

| Path length $K$ | # paths | RW within-path rel std/mean |
|---|---|---|
| $10^6$ | 50 | $0.222 \pm 0.126$ |
| $5\times 10^6$ | 10 | $0.213 \pm 0.099$ |
| Empirical (T sieve, [5×10⁶, 10⁷]) | 1 | $0.205$ |

**The empirical value $0.205$ is statistically indistinguishable from the RW null $0.21\!-\!0.22$.**  Quantitatively, the $z$-score is $z = (0.205 - 0.213)/0.099 \approx -0.08$ (using the $K=5\times 10^6$ row, where the across-path std of the within-path rel-std-mean is $0.099$).  We have **no positive evidence** that $T$ is more structured than a Gaussian random walk based on this statistic.

(For context: the *ensemble* std at fixed $K$ is also $\sim \sigma^2/\sqrt 3 \approx 0.23$ — see derivation in §"Theoretical RW variance" below.  This matches the path-to-path std observed, but is the wrong null for the empirical $0.205$.)

## Theoretical RW variance (for reference)

For Gaussian $T(M) = \sum_{n \le M} \epsilon_n$ with iid $\epsilon_n \sim N(0,\sigma^2)$, writing $T(M') = T(M) + S$ with $S \perp T(M)$:

$$\mathbb{E}[T(M)^2 T(M')^2] = \mathbb{E}[T(M)^4] + \mathbb{E}[T(M)^2]\mathbb{E}[S^2] = 3\sigma^4 M^2 + \sigma^2 M \cdot \sigma^2(M'-M)$$

so $\mathrm{cov}(T(M)^2, T(M')^2) = 2\sigma^4 \min(M,M')^2$. Then
$$\mathrm{var}(V(N)) = \sum_{M,M'} 2\sigma^4 \min(M,M')^2 = 2\sigma^4 \sum_{M=1}^{N} M^2 (2N - 2M + 1).$$
Leading order: $\sum M^2 \cdot 2N = 2N \cdot N^3/3 = 2N^4/3$ and $\sum M^2 \cdot 2M = 2 N^4/4 = N^4/2$. So
$$\mathrm{var}(V(N)) \sim 2\sigma^4 (2N^4/3 - N^4/2) = 2\sigma^4 \cdot N^4/6 = \sigma^4 N^4/3.$$
Hence $\mathrm{std}(V(N)/N^2) \to \sigma^2/\sqrt 3$ across an ensemble of paths at fixed $N$, while $\mathbb{E}[V(N)/N^2] \to \sigma^2/2$. Numerically the simulation confirms this: across 50 paths of length $10^6$ with $\sigma^2 = 0.4$, std$(V(K)/K^2) = 0.234$ vs theoretical $0.231$.

**Key point:** under the RW model, $V(N)/N^2$ does NOT converge to $\sigma^2/2$ along any single path — each path has its own random limit $C_{\mathrm{path}}$ with mean $\sigma^2/2$ and std $\sigma^2/\sqrt 3$. The "constant $C^\dagger$" is undefined unless one assumes more structure than RW.

## Honest descriptive statistics for $V$

- $V(10^7)/10^{14} = 0.1937$.
- Across $N \in [10^5, 10^7]$, $V(N)/N^2$ takes values in $\approx [0.15, 0.34]$ (range $2.3\times$).
- Across $N \in [5\times 10^6, 10^7]$ (densely sampled), mean $0.28$, std $0.06$.
- These ranges are consistent with a Gaussian RW null with $\sigma^2 \in [0.3, 0.6]$.
- Equivalently RMS $T(M)/\sqrt M \in [0.55, 0.78]$, consistent with the previous session's sparse-sample estimate $0.638$.

## Implications for strategy

### Net positive findings

1. **Refutes the previous session's claim that "smoothed-window estimates can pin $c_O$ to 2 digits in 1 session."** Even the most-smoothed natural estimator (cumulative $V/N^2$) shows $\sim 20\%$ within-range fluctuation at $N = 10^7$. The fluctuation is consistent with RW null; either way, it does not shrink fast enough at reachable $N$ to pin a constant to 2 digits.

2. **Establishes the empirical envelope** $V(N)/N^2 \in [0.15, 0.34]$ for $N$ up to $10^7$. This places $\mathrm{RMS}(T(M)/\sqrt M)$ in $[0.55, 0.78]$.

3. **Methodologically:** for any future empirical analysis of constants in the spin sum, one MUST compare to a within-path null (e.g. Monte Carlo on RW), not to ensemble-std formulas. This was an error in the first draft of this note.

### What is NOT established (retracted from first draft)

- Any positive evidence for "mean-reverting structure" of $T$ beyond what a Gaussian RW would produce. The corrected Monte Carlo shows the empirical fluctuation matches RW null to within statistical noise.

### Open and re-prioritized

1. **Pin $C^\dagger$ (if it exists) to $\le 0.05$:** requires $N \ge 10^9$ (memory/runtime infeasible at current setup) OR theoretical analysis. The latter would compute $\sum_{n \le N} \tau(n^2+1)^2$ (a Selberg–Delange-type evaluation) and compare to the spin-cancellation factor.

2. **Distinguish $T$ from RW:** A within-path study needs a statistic that DOES separate them. Candidates:
   - Higher-moment ratios $\mathbb{E}[V^2]/\mathbb{E}[V]^2$ at multiple $N$.
   - The autocorrelation of $T(M)$ at lag $h$: under RW, $\mathrm{cov}(T(M), T(M+h)) = \sigma^2 \min(M, M+h) \sim \sigma^2 M$ (no $h$-dependence). Under our spin sum, $\chi_4$ structure should produce $h$-dependent behavior.
   - The 4th moment $\sum T(M)^4$ — $\mathbb{E}[T^4] = 3\sigma^4 M^2$ for Gaussian; departures would be informative.

3. The original plan to bound the within-$d$ cross-$n_0$ piece $\mathcal{D} - \mathcal{D}_0 \approx 0.232 N^2$ is unaffected.

## Files

- `bot/scratch/V-cumulative.py` — full $T$ sieve to $N=10^7$, computes $V(N)$.
- `bot/scratch/V-fluctuation.py` — dense $V/N^2$ scan and (initial, flawed) RW null comparison.
- `bot/scratch/V-rw-simulation.py` — Monte Carlo within-path RW null (the corrected comparison).
- `bot/scratch/Tcum-V.pkl` — sparse $(M, T(M), V(M))$ samples for downstream work.

## Caveats

- $N_{\max} = 10^7$ is a 5× extension over the prior session's exact-window data; the previous sparse-sample run reached $N = 5 \times 10^7$ but only sampled $T$ at every $1000$-th $M$, insufficient for $V$.
- The Gaussian RW null is one specific null; other nulls (e.g. heavy-tailed increments) would give different but qualitatively similar within-path fluctuation. The point stands: cumulative $V/N^2$ is a heavily-filtered statistic that does not separate "structured" $T$ from "noise" $T$.
- The retracted claim from the first draft of this note was not propagated to other documents (caught at Round 1 skeptic before commit).
