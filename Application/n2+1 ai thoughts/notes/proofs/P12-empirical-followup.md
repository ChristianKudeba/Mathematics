# P12 follow-up: empirical scaling of T(N) past N=10⁷

> **Empirical refinement of Conjecture C (P12).** Computing $T(N) = \sum_{n \le N} \tau(n^2+1)\,\chi_4(n+1)$ with a single full Eratosthenes/Tonelli sieve through $N_{\max} = 5 \times 10^7$ (50 000 sparse sample points) shows that $T(N) / \sqrt N$ has stable RMS $\approx 0.638$ across four orders of magnitude in $N$, with **no $\log N$-trend detectable** at this range.
>
> The natural sharper guess: $T(N) = o(\sqrt N \log N)$, and very plausibly $T(N) = O(\sqrt N \cdot (\log\log N)^{O(1)})$ — i.e., the explicit $\log N$ in P12 Conjecture C looks slack but a $\log\log$-style growth (e.g., LIL-type) is **not** ruled out by 4 decades of data.

## Numerical evidence

Decade-by-decade RMS of $T(N)/\sqrt N$ over 50 000 sparse $N$ in $[10^3, 5\!\times\!10^7]$:

| Decade           | $\#$ samples | RMS$(T/\sqrt N)$ | RMS$(T/(\sqrt N \log N))$ |
|------------------|-----|----|----|
| $[10^3, 10^4]$   |   9 | 0.760 | 0.093 |
| $[10^4, 10^5]$   |  90 | 0.679 | 0.064 |
| $[10^5, 10^6]$   | 900 | 0.610 | 0.047 |
| $[10^6, 10^7]$   | 9 000 | 0.667 | 0.044 |
| $[10^7, 5\!\times\!10^7]$ | 40 000 | 0.632 | 0.037 |

* RMS$(T/\sqrt N)$ stays within **$0.61$–$0.76$**, well within statistical noise of a constant. No log-trend.
* RMS$(T/(\sqrt N \log N))$ **monotonically decays** from $0.093$ to $0.037$ — i.e., dividing by $\log N$ over-corrects, confirming the polylog is *not* present.
* Sign distribution: 47.95 % positive, 52.04 % negative — symmetric around zero.
* Worst-case excursion observed: $|T/\sqrt N| \le 2.13$ across the full range; the maximum is in a localized cluster near $N \approx 1.27 \times 10^6$ (eight nearby sample points all at $|T/\sqrt N| \in [1.83, 2.13]$).
* Mean $T/\sqrt N$ over full range: $-0.039$ (consistent with zero).

These statistics are produced by `bot/scratch/compute-T-fast.py` + `bot/scratch/analyze-T.py` (saved sparse data in `bot/scratch/Tcum.pkl`).

## Refined conjecture

**Conjecture C′ (sharpened).**  $\;T(N) = o\!\bigl(\sqrt N \, \log N\bigr)$, unconditionally; plausibly $T(N) = O(\sqrt N \, (\log\log N)^{O(1)})$.

Note: a finite-$\limsup$ statement $\limsup |T(N)|/\sqrt N \le \kappa$ is **not** justified by sparse sampling at stride 1000 in $N$ — the true maxima between sample points may be substantially larger than the observed 2.13. Within the sampled grid the empirical RMS is stable at $\approx 0.638$, but a slow $(\log\log N)^{1/2}$-type growth is statistically indistinguishable from a constant over 4 decades (predicted ratio $\approx 1.22$ vs. observed scatter $1.25$). To rule out $(\log\log)^{1/2}$ growth one would need $\sim$ 10 decades of $N$.

This is still strictly stronger than P12's Conjecture C as written ($O(\sqrt N (\log N)^{O(1)})$ with $O(1)$ unspecified): we are saying the polylog exponent is 0 (or at most $\log\log$), not just bounded.

## Why the log appears to be absent — heuristic (cautious)

The summand $\tau(n^2+1)\chi_4(n+1)$ has average magnitude $\sim (3/\pi)\log n$ on $n$ even (the sum runs only over even $n$ since $\chi_4(n+1) = 0$ for $n$ odd; Hooley 1957: $\sum_{n \le N} \tau(n^2+1) \sim \tfrac{3}{\pi} N \log N$). Its second moment is folklore: $\sum_{n \le N} \tau(n^2+1)^2 \asymp N (\log N)^3$. So a naïve independent-sign model on the summand gives partial-sum RMS $\sim \sqrt{N (\log N)^3} = \sqrt N (\log N)^{3/2}$.

Empirically, the RMS is $\approx 0.64 \sqrt N$. Compared to the naïve $\sqrt N (\log N)^{3/2}$, the observed cancellation is a **factor of $(\log N)^{3/2}$**, not just a factor of $\log N$. The naïve model is clearly inadequate; some structural mechanism is suppressing the polylog.

I do **not** have a derivation of the $\approx 0.638$ constant. The closeness to $2/\pi \approx 0.6366$ may be a coincidence with the unconditional bound's leading constant (P12 Theorem C step 6: $|T(N)| \le 2c N$ with $2c \approx 0.637$), but converting that $L^\infty$ bound into a "natural $L^2$ scaling" $0.637 \sqrt N$ requires a second-moment argument I have not done. **Treat the constant as numerology pending a derivation.**

What this suggests for next steps:
1. **Second-moment route.** Compute $\sum_{M \in [N, 2N]} |T(M)|^2$ and try to bound it by $N^2$ (which would give $T \ll \sqrt N$ on average). The AP decomposition of step 4 plus an off-diagonal estimate may suffice; this is independent of any $L$-function input.
2. **Hecke L-function route.** Identify $T(N)$ with a partial sum of coefficients of a specific $L$-function over $\mathbb{Q}(i)$ (likely $L(s, \chi_4 \otimes \theta_4)$ where $\theta_4$ is the binary theta of $x^2+y^2$); apply known mean-square bounds (Selberg, Iwaniec). Heavier machinery.

Path 1 is the lighter-weight next step.

## Caveats and what is not claimed

* This is **empirical only**. RMS being constant across 4 decades is suggestive, not proof.
* **Cross-check performed (this session).** Ran the existing `n2+1 ai thoughts/notes/proofs/compute-T-large.py` directly and diffed all 7 of its sample points against `compute-T-fast.py`'s output: exact agreement.

  | $N$ | `compute-T-large.py` | `compute-T-fast.py` |
  |---|---|---|
  | $10^3$ | $-16$ | $-16$ |
  | $5 \cdot 10^3$ | $-16$ | $-16$ |
  | $10^4$ | $-6$ | $-6$ |
  | $5 \cdot 10^4$ | $-112$ | $-112$ |
  | $10^5$ | $-108$ | $-108$ |
  | $5 \cdot 10^5$ | $+746$ | $+746$ |
  | $10^6$ | $+468$ | $+468$ |

  This rules out implementation drift between the two sieves through $N \le 10^6$. It does **not** rule out a shared bug at $N > 10^6$ (e.g., a Tonelli edge case at large primes) — both sieves use Tonelli–Shanks and could share such a bug. A third independent computation at $N = 10^7$ would further harden the empirical claim.
* The fact that RMS fits a constant does NOT imply $\limsup |T|/\sqrt N$ is finite — a slow $\log\log$-type LIL growth is consistent with the data.
* The structural cancellation is a $(\log N)^{3/2}$ factor (not $\log N$, as an earlier draft of this note misclaimed). Mechanism unclear; not derivable from P12 Theorem C's $L^\infty$ bound without additional work.
* **Sample sparsity caveat.** Sample stride is $\approx 1000$ in $N$. The empirical maximum $|T/\sqrt N| \le 2.13$ is on this grid; true off-grid maxima may be larger and a $\limsup \le 3$ statement is **not** justified by this data.

## Where this should slot in

* Update `n2+1 ai thoughts/notes/proofs/P12-pointwise-spin-identity.md` Conjecture C to note the sharper empirical conjecture C′. (Not yet done — pending Anton review.)
* `bot/STRATEGY.md` should promote "prove second-moment $\sum_{M \in [N,2N]} |T(M)|^2 \ll N^{3/2}$" as a discrete sub-task that, if successful, would yield $T(N) \ll \sqrt N$ on average and likely (with extra work) pointwise.
* The bigger ($\!18\!$–$\!24$ month) Bianchi cubic moment program (P13) is unaffected; this is an orthogonal refinement of the P12 empirical thread.

## Reproducibility

```bash
python bot/scratch/compute-T-fast.py 50000000   # produces Tcum.pkl in ~75s
python bot/scratch/analyze-T.py                  # statistics on the sparse pickle
```

Algorithm: full Eratosthenes sieve to $N_{\max}$, Tonelli–Shanks to find $\sqrt{-1} \pmod p$ for $p \equiv 1 \pmod 4$, then for each such $p$ mark APs $k \equiv \pm m_0/2 \pmod p$ where $4k^2+1 \equiv 0 \pmod p$ and divide out powers; at the end, residual $R[k] > 1$ is a single large prime contributing factor 2 to $\tau(4k^2+1)$ (uniqueness check: $R[k] \le 4K^2 < N_{\max}^2$, so two large primes don't fit). Cumulative sum uses $T(N) = \sum_{k \le N/2} (-1)^k \tau(4k^2+1)$, which follows from the substitution $n = 2k$ (the only contributing $n$).
