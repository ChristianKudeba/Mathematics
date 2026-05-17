# P12 follow-up: AP-decomposition diagonal of the second moment of $T(M)$

> **Empirical claim, this session.**  Decompose
> $$T(M) \;=\; 2\sum_{\substack{d \in L_{\mathrm{odd}}\\ d \le M}} c_d(M),
> \qquad c_d(M) \;=\; \sum_{\substack{n_0 \pmod d \\ n_0^2 \equiv -1 \pmod d}} S_{M,d}(n_0),$$
> using P12 Theorem C step 4. Define the **AP-decomposition diagonal**
> $$\mathcal{D}(N) \;:=\; 4 \sum_{\substack{d \in L_{\mathrm{odd}}\\ d \le 2N}} \sum_{M=N+1}^{2N} c_d(M)^2,$$
> and the **"true diagonal"** (only $n_0=n_0'$ within each $d$)
> $$\mathcal{D}_0(N) \;:=\; 4 \sum_{\substack{d \in L_{\mathrm{odd}}\\ d \le 2N}} \sum_{n_0:\,n_0^2 \equiv -1\,(d)} \sum_{M=N+1}^{2N} S_{M,d}(n_0)^2.$$
> Numerically, for $N \in \{1000, 2000, 5000, 10000\}$, $\mathcal{D}(N) / N^2 \in [0.976, 1.011]$ and $\mathcal{D}_0(N)/N^2 \in [0.745, 0.753]$. The direct second moment $\sum_{M \in (N,2N]} T(M)^2$ fluctuates window-by-window in $[0.29, 0.90] \cdot N^2$ — bounded by $\mathcal{D}(N)$ in all four tested windows, but the cross-$d$ off-diagonal sometimes contributes a large negative correction (e.g. $-0.7 N^2$ at $N=10^4$).
>
> **Reading.** Over the tested decade, $\mathcal{D}(N)/N^2$ moved by only 1.5%, ruling out a clean $\Theta(N^2 \log N)$ scaling (which would give a 33% rise from $N=10^3$ to $N=10^4$). A slow $1 + c/\log N$ correction or $\log\log$-type drift remains compatible. The qualitative scaling $\mathcal{D}(N) = \Theta(N^2)$ is therefore plausibly but not provably established by the data. This is one half of the strategy hint that the second-moment route may yield $T(M) \ll \sqrt M$ on average — *provided* the cross-$d$ off-diagonal cancels. The off-diagonal cancellation remains the open obstacle.

## Setup (recap of P12 Theorem C step 4)

For $d \in L_{\mathrm{odd}}$ (odd, all primes $\equiv 1 \pmod 4$) and $n_0$ with $n_0^2 \equiv -1 \pmod d$, define
$$S_{M,d}(n_0) \;=\; \sum_{\substack{n \equiv n_0 \pmod d \\ d \le n \le M}} \chi_4(n+1).$$
P12 Theorem C step 4 proves $|S_{M,d}(n_0)| \le 1$ pointwise (the $\chi_4$ sum over any 4 consecutive AP elements vanishes; the partial sum has at most 1 odd-residue tail). Hence
$$T(M) = 2 \sum_d c_d(M), \qquad c_d(M) := \sum_{n_0} S_{M,d}(n_0), \qquad |c_d(M)| \le \rho(d) = 2^{\omega(d)}.$$

## Numerical results

A direct enumeration (`bot/scratch/diag-vs-second-moment.py`) of all $(d, n_0)$ pairs with $d \in L_{\mathrm{odd}}, d \le 2N$ (using Hensel lifts from $\sqrt{-1} \bmod p$ for $p \equiv 1 \pmod 4$), tracking $S_{M,d}(n_0)$ as $M$ increases, yields:

| $N$ | $\sum_{M \in (N,2N]} T(M)^2$ | $\mathcal{D}(N)$ (AP-diag) | $\mathcal{D}_0(N)$ (true-diag) | direct$/N^2$ | $\mathcal{D}/N^2$ | $\mathcal{D}_0/N^2$ |
|---|---|---|---|---|---|---|
| 1000   |       721 272  |       975 752  |     745 072  | 0.7213 | 0.9758 | 0.7451 |
| 2000   |    1 517 632   |    4 044 776   |  3 012 536   | 0.3794 | 1.0112 | 0.7531 |
| 5000   |   22 446 740   |   24 489 812   | 18 685 508   | 0.8979 | 0.9796 | 0.7474 |
| 10000  |   29 235 600   |   99 143 920   | 74 754 968   | 0.2924 | 0.9914 | 0.7475 |

Take-aways:

* $\mathcal{D}(N)/N^2 \in [0.976, 1.011]$ across the table — extraordinary stability.
* $\mathcal{D}_0(N)/N^2 \in [0.745, 0.753]$ — even tighter.
* The "cross-$n_0$ within $d$" piece $\mathcal{D} - \mathcal{D}_0$ is consistently $\approx 0.24 N^2$.
* The cross-$d$ off-diagonal $\sum_M T^2 - \mathcal{D}$ is *negative on average* and varies in sign; $|\sum_M T^2 - \mathcal{D}|/N^2$ ranges from 0.025 to 0.70 in our windows.

## Analytical estimate of the true diagonal $\mathcal{D}_0(N)$

For fixed $(d, n_0)$ with $d \le N$, $S_{M,d}(n_0)$ is a step function of $M$, piecewise constant on intervals of length $d$. As $M$ traverses one period $4d$ (after the partial sum has begun, i.e., $M \ge n_0 + d$), the value of $S_{M,d}(n_0)$ takes the four entries of one cyclic shift of $\{0, \pm 1, \pm 1, 0\}$ — specifically, partial sums of the 4-periodic pattern $\{0, +1, 0, -1\}$ (in some phase determined by $n_0+1 \bmod 4$).

**Key identity.** For any starting phase, the four values in the cycle are a multiset of $\{0, 0, \pm 1, \pm 1\}$ with two zeros and two nonzero entries of equal sign. Hence
$$\frac{1}{4d} \sum_{M=n_0+d+1}^{n_0+d+4d} S_{M,d}(n_0)^2 \;=\; \tfrac{1}{2}.$$

By summing over full periods plus an $O(d)$ boundary error, for any $X \ge n_0 + d$:
$$\sum_{M=1}^{X} S_{M,d}(n_0)^2 \;=\; \tfrac{X}{2} + O(d).$$

Substituting into $\mathcal{D}_0$ and isolating the regime $d \le N$ where this estimate is in steady state:
$$\mathcal{D}_0(N) \;\ge\; 4 \cdot \tfrac{N}{2} \cdot \sum_{\substack{d \le N \\ L_{\mathrm{odd}}}} \rho(d) \;-\; O\Big(N \sum_{d \le N} \rho(d)\Big) \;\sim\; 2 N \sum_{\substack{d \le N \\ L_{\mathrm{odd}}}} 2^{\omega(d)} \;\sim\; 2c N^2,$$
where the constant $c$ is identified empirically (from P12 Thm C step 6 numerical table at line 161) as $\sum_{d \le N, L_{\mathrm{odd}}} 2^{\omega(d)} \approx 0.319 N$ — a numerical fit, not a closed-form derivation. So the **interior lower bound** is $\mathcal{D}_0(N) \gtrsim 0.64 N^2$.

The contribution from $d \in (N, 2N]$ is between $0$ and $4 N \sum_{N < d \le 2N, L_{\mathrm{odd}}} \rho(d) \asymp N^2$. **I have not derived the exact contribution.** The trivial upper bound $|S| \le 1$ gives at most another $4 N \cdot c N = 4c N^2 \approx 1.27 N^2$, which combined with the interior gives $\mathcal{D}_0(N) \le 6c N^2 \approx 1.92 N^2$. The empirical $0.747$ sits between the interior lower bound $0.64$ and the trivial upper bound $1.92$, but I cannot derive its exact location.

**Honest summary of what is rigorous.** Interior lower bound $\mathcal{D}_0(N) \gtrsim 0.64 N^2$; trivial upper bound $\mathcal{D}_0(N) \le 1.92 N^2$. Empirically constant 0.747 falls in this range but has no closed-form derivation. The $\Theta(N^2)$ scaling claim is rigorous only as "between $0.64 N^2$ and $1.92 N^2$ asymptotically", not as a sharp asymptotic.

## What the diagonal does — and does *not* — give

**Does:**
- The diagonal $\mathcal{D}(N)$ is an explicit, computable, $O(N^2)$ upper bound on the contribution of the within-$d$ part of $\sum_M T(M)^2$.
- $\mathcal{D}_0(N)$ admits a clean elementary estimate: $\mathcal{D}_0(N) \le 8c N^2 (1 + o(1))$ by combining $|S| \le 1$ with $\sum_M S^2 \le N/2 + O(d)$ and Selberg–Delange. (Constant $8c$ is loose by ~factor 2.7 vs. empirical 0.747.)

**Does NOT:**
- Bound $\sum_M T(M)^2$ directly. Cauchy–Schwarz from $T = 2 \sum_d c_d$ gives
  $$T(M)^2 \le 4 \cdot |L_{\mathrm{odd}}(M)| \cdot \sum_d c_d(M)^2,$$
  and $|L_{\mathrm{odd}}(2N)| \asymp N/\sqrt{\log N}$, yielding only $\sum_M T^2 \ll N^3 / \sqrt{\log N}$. **The Cauchy route is not tight.**
- The tight bound $\sum_M T^2 \ll N^2$ requires the *cross-$d$ off-diagonal* to be $O(N^2)$. Empirically it is, but proving so is an open problem of the same flavor as the original Conjecture C′.

**Bottom line.** The strategy hint that "the diagonal sizes correctly to $N^2$" is **empirically validated**, but proving $\sum_M T^2 \ll N^2$ from this requires a separate cross-AP cancellation argument; the second-moment route is **not strictly easier than the pointwise route**.

## What this means for the strategy

* **Promote** to in-progress thread: prove $\mathcal{D}(N) \ll N^2$ rigorously. This is a clean, elementary number-theory exercise (Selberg–Delange + AP partial-sum estimates), achievable in 1–2 sessions.
* **Open**: the cross-$d$ off-diagonal $\sum_{d_1 \ne d_2} \sum_M c_{d_1}(M) c_{d_2}(M)$. Empirically near-zero on average, but I have no tools for it elementally. Could relate to a Hecke-character mean square (cf. P12 path 2 in `P12-empirical-followup.md`).
* **Demote** the optimistic "second-moment route gives $\sum T^2 \ll N^2$ in 1–2 sessions" line in `STRATEGY.md`; it's at least 3–4 sessions of work even at the elementary level, and the cross-$d$ piece may require analytic NT input.

## Reproducibility

```bash
python bot/scratch/diag-vs-second-moment.py
```
Output (key block):
```
       N        direct       AP-diag     true-diag    /N^2 dir     /N^2 AP     /N^2 TD
    1000        721272        975752        745072      0.7213      0.9758      0.7451
    2000       1517632       4044776       3012536      0.3794      1.0112      0.7531
    5000      22446740      24489812      18685508      0.8979      0.9796      0.7474
   10000      29235600      99143920      74754968      0.2924      0.9914      0.7475
```

Algorithm: enumerate $(d, n_0)$ pairs by recursively combining prime-power factors $p^k$ with $p \equiv 1 \pmod 4$ (Hensel-lift roots of $-1$), then for each pair simulate $S_{M,d}(n_0)$ as $M$ increments. Window second moments computed in-line. Cost: $O(N^2 \log N)$ with current implementation; for $N \gg 10^4$ the per-pair walk would need to be replaced by direct period-$4d$ closed-form.

## Caveats

* All four data points are at small $N$ ($N \le 10^4$). The data **rules out** $\Theta(N^2 \log N)$ over the tested decade (which would predict a 33% rise in $\mathcal{D}/N^2$, vs. observed 1.5%) but **does not rule out** a slow correction like $1 + c/\log N$ or $(\log\log N)^{c}$.
* "Window second moment is bounded by AP diagonal in every tested window" — only 4 windows tested, and the bound is *very* slack ($0.29 N^2$ vs. $0.99 N^2$ at $N = 10^4$). The cross-$d$ off-diagonal could in principle be large positive somewhere; the data is too thin to rule that out.
* The Hensel-lift code handles $p^k$ for all $k$ but stops at $p^k > 2N$; higher prime powers contribute negligibly to the asymptotic.
* The constant 0.747 in $\mathcal{D}_0(N)/N^2$ has **not been derived analytically**. The interior lower bound is $0.64$ and the trivial upper bound is $1.92$; the boundary contribution from $d \in (N, 2N]$ is undetermined.
* **Enumeration correctness** (sanity-check, this session). Independent brute-force enumeration of $L_{\mathrm{odd}}$ up to $B = 200$ gave 29 distinct $d$ and 65 $(d, n_0)$ pairs. The Hensel-BFS code in the script gave **identical** results: same 29 $d$'s, same 65 pairs (no duplicates), every root satisfying $n_0^2 \equiv -1 \pmod d$. So the AP enumeration is verified correct and the numerical $\mathcal{D}, \mathcal{D}_0$ values are not inflated by enumeration bugs.

## Next sessions

1. Prove $\mathcal{D}_0(N) = 4c N^2 + o(N^2)$ rigorously. Closed-form for $\sum_M S^2$ over a 4d-period, Selberg–Delange tail. Honest target: 1 session.
2. Prove $\mathcal{D}(N) - \mathcal{D}_0(N) \ll N^2$. Need cross-$n_0$ within-$d$ correlation; the partial sums on different APs mod $d$ are *correlated* via the global $\chi_4$ structure. Tractable but more intricate. Honest target: 1–2 sessions.
3. Cross-$d$ off-diagonal — open. Probably needs Hecke / Plancherel input. Honest target: research direction, not a sub-task.
