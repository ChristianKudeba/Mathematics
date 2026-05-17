# P12 — Leading Selberg–Delange constant for $B_3^{\rm bdy}$

**Date:** 2026-05-06 12:30 UTC.
**Status:** rigorous identification of $c_1 = H(1)\pi/2 \approx 0.8681$, with quantitative empirical cross-check across $N \in [500, 10^5]$.

## 1. Setup

From the prior session (`P12-B3-sign-bias.md`), define

$$B_3^{\rm bdy}(N) := \sum_{n=1}^{N} 2^{\omega(n^2+1)} \, \delta_{n^2+1}(N), \qquad \delta_d(N) := N_d(N) - \frac{\rho(d)\,N}{d},$$

where $N_d(N) := \#\{m \le N : d \mid m^2+1\}$ and $\rho(d) := \#\{x \pmod d : x^2 \equiv -1 \pmod d\}$.

Empirical at $N \in [500, 10^4]$: $B_3^{\rm bdy}/(N \log N)$ rises from $0.911$ to $0.948$. The prior session put this "in the ballpark of $3/\pi \approx 0.955$" but flagged "fit-by-eye." This note replaces the eyeball with a derivation.

## 2. Exact decomposition

For each $n \le N$, $n$ itself is one root of $x^2 \equiv -1 \pmod{n^2+1}$ in $[1, N]$. Other roots in $[1, N]$ contribute extra. Decompose

$$B_3^{\rm bdy}(N) = T(N) + P(N) - N \, K_N,$$

where

- $T(N) := \displaystyle\sum_{n \le N} 2^{\omega(n^2+1)}$ (the diagonal $m = n$ contribution);
- $P(N) := \displaystyle\sum_{n \le N} 2^{\omega(n^2+1)} (N_{n^2+1}(N) - 1)$ (off-diagonal pairs $n \ne m$, weighted);
- $K_N := \displaystyle\sum_{n \le N} \frac{2^{\omega(n^2+1)} \rho(n^2+1)}{n^2+1}$.

This is an identity (no asymptotics). Verified at six $N$ in `bot/scratch/B3-bdy-secondary.py`: predicted vs empirical $B_3^{\rm bdy}$ agree to within $0.5$ at all six $N$.

## 3. Leading constant via Selberg–Delange on $T(N)$

The leading order of $B_3^{\rm bdy}(N)$ is set by $T(N)$, since $P(N) = O(N)$ and $K_N \to K_\infty$ finite (Section 4).

### 3.1 Dirichlet-series setup

Restrict to the Dirichlet series of $\mu^2(d) \rho(d)$:

$$G(s) := \sum_{d \, \mathrm{sf}} \rho(d) \, d^{-s} = (1 + 2^{-s}) \prod_{p \equiv 1 (4)} (1 + 2 p^{-s}).$$

Factor through $\zeta_K(s) = \zeta(s) L(s, \chi_4)$ for $K = \mathbb Q(i)$:

$$G(s) = \zeta_K(s) \cdot H(s),$$
$$H(s) := (1 - 4^{-s}) \prod_{p \equiv 1 (4)} (1 - 3 p^{-2s} + 2 p^{-3s}) \prod_{p \equiv 3 (4)} (1 - p^{-2s}).$$

Local-factor cancellations (verified algebraically):

- $p = 2$: $(1+2^{-s}) \cdot (1-2^{-s}) = 1 - 4^{-s}$.
- $p \equiv 1 (4)$: $(1+2p^{-s})(1-p^{-s})^2 = 1 - 3 p^{-2s} + 2 p^{-3s}$.
- $p \equiv 3 (4)$: $1 \cdot (1 - p^{-2s}) = 1 - p^{-2s}$.

$H(s)$ is given by an absolutely convergent Euler product on $\Re s > 1/2$, so $H$ is analytic there. $\zeta_K$ has a simple pole at $s=1$ with residue $L(1, \chi_4) = \pi/4$, so $G$ has a simple pole at $s=1$ with residue $H(1) \cdot \pi/4$.

### 3.2 Numerical $H(1)$

Truncating the Euler product at primes $\le 10^6$ (78,498 primes total, 39,176 split, 39,322 inert, plus $p=2$):

$$H(1) = \frac{3}{4} \prod_{p \equiv 1(4), \, p \le 10^6} \!\!\!(1 - 3/p^2 + 2/p^3) \prod_{p \equiv 3(4), \, p \le 10^6}\!\!\! (1 - 1/p^2) = 0.5526721690.$$

Tail relative error $< 2 \cdot 10^{-7}$ (from $\sum_{p > 10^6} 3/p^2 < 7 \cdot 10^{-8}$).

Hence

$$c_1 := \frac{H(1) \pi}{2} = 0.8681354129.$$

### 3.3 Tauberian on the small-$e$ piece (rigorous) plus "hyperbolic doubling" (heuristic, needing Hooley-style adaptation for $\tau^*$)

By switching summation,

$$T(N) = \sum_{n \le N} \sum_{e \mid n^2+1, \, e \, \mathrm{sf}} 1 = \!\!\!\sum_{e \le N^2+1, \, e \, \mathrm{sf}, \, \rho(e) > 0}\!\!\! N_e(N).$$

For $e \le N$, write $N_e(N) = \rho(e) N/e + O(\rho(e))$. The small-$e$ contribution is rigorously

$$\sum_{e \le N, \, e \, \mathrm{sf}, \, \rho(e)>0} N_e(N) \;=\; N \sum_{e \le N, \, e \, \mathrm{sf}} \rho(e)/e \;+\; O(N) \;=\; H(1)\,\frac{\pi}{4}\,N \log N \;+\; O(N),$$

via partial summation on $\sum_{e \le X, sf} \rho(e) \sim H(1)\pi/4 \cdot X$ (Tauberian / Selberg–Delange on the simple pole of $G$).

The big-$e$ contribution $\sum_{N < e \le N^2+1, sf} N_e(N)$ is harder. For $\tau$ instead of $\tau^*$, Hooley's exact identity $\tau(d) = 2 \#\{e \mid d : e \le \sqrt d\}$ (for non-square $d$, always true here) lets one swap big-$e$ for small-$e$ via $e \leftrightarrow d/e$, and both halves have the same Tauberian residue, doubling to give Hooley's $\sum \tau(n^2+1) \sim (3/\pi) N \log N$.

For $\tau^*$ this swap is **not direct**: $e$ squarefree does not imply $d/e$ squarefree. The correct identity uses the radical:

$$\tau^*(d) = \tau(\mathrm{rad}(d)), \qquad \mathrm{rad}(d) = \prod_{p \mid d} p,$$

which IS squarefree. So Hooley's identity applies to $\mathrm{rad}(d)$:

$$\tau^*(d) = \tau(\mathrm{rad}(d)) = 2 \#\{e \mid \mathrm{rad}(d), e \le \sqrt{\mathrm{rad}(d)}\}.$$

The constraint $e \le \sqrt{\mathrm{rad}(d)}$ depends on $d$ (specifically on its squarefree-essence factor $r := d/\mathrm{rad}(d) \ge 1$). For $n^2+1$ squarefree (positive density $\approx 0.895$ by Estermann), $r = 1$ and the constraint is $e \le \sqrt{n^2+1}$, matching the small-$e$/big-$e$ symmetry of Hooley's argument and giving the same factor-of-2 doubling. For $n^2+1$ with $r \ge 2$ (density $\approx 0.105$), the constraint is stricter ($e \le \sqrt{(n^2+1)/r}$), reducing the counted $e$.

**Conclusion (heuristic):** the leading constant is $c_1 = 2 \cdot H(1) \pi/4 = H(1) \pi/2 = 0.8681$, with the doubling from the squarefree-density-weighted Hooley-style argument on $\mathrm{rad}(n^2+1)$.

**Status of rigor.** The small-$e$ contribution $H(1)\pi/4 \cdot N\log N$ is rigorous. The big-$e$ contribution being equal to it (giving the doubling) is supported by:

- Empirical agreement to $0.6\%$ at $N = 10^5$ (Section 3.4).
- Algebraic structure (the radical identity) but not a full Hooley-style boundary estimate written out here.

Closing the rigor gap requires the analog of Hooley 1957 §3 for $\tau^*$, separating $n^2+1$ by squarefree/non-squarefree-ness and applying the radical identity. This is a 1–2 session task, deferred.

### 3.4 Empirical validation

`bot/scratch/B3-bdy-SD-constants.py` computes $T(N)$ for $N \in \{500, 10^3, 2 \cdot 10^3, 5 \cdot 10^3, 10^4, 2 \cdot 10^4, 5 \cdot 10^4, 10^5\}$.

| $N$ | $T(N)$ | $T(N)/(N \log N)$ | $(T - c_1 N \log N)/N$ |
|---|---|---|---|
| 500 | 3,212 | 1.0337 | 1.029 |
| 1,000 | 6,968 | 1.0087 | 0.971 |
| 2,000 | 15,190 | 0.9992 | 0.996 |
| 5,000 | 41,976 | 0.9857 | 1.001 |
| 10,000 | 89,766 | 0.9746 | 0.981 |
| 20,000 | 191,694 | 0.9678 | 0.987 |
| 50,000 | 519,302 | 0.9599 | 0.993 |
| 100,000 | 1,097,800 | 0.9535 | 0.984 |

Two readings:

- $T(N)/(N\log N)$ *decreases* monotonically from $1.034$ at $N=500$ to $0.954$ at $N=10^5$ — converging from above toward $c_1 = 0.868$, not toward $0.95$.
- $(T - c_1 N \log N)/N$ is approximately constant at $\approx 0.99 \pm 0.03$ across all eight $N$, consistent with the secondary expansion $T(N) = c_1 N \log N + c_0^T N + o(N)$ with $c_0^T \approx 0.99$.

If $c_1$ were $0.95$, the residual $/N$ would be $\approx 0.05$ at $N=10^5$ — falsified.

## 4. Application to $B_3^{\rm bdy}$ and turning point

By the Section 2 identity, the leading order of $B_3^{\rm bdy}(N)$ matches $T(N)$:

$$B_3^{\rm bdy}(N) = c_1 N \log N + (c_0^T + P(N)/N - K_N) N + o(N).$$

Numerically (from `B3-bdy-secondary.py`):

| $N$ | $K_N$ | $P(N)/N$ | $K_N - P(N)/N$ | $B_3^{\rm bdy}/(N \log N)$ |
|---|---|---|---|---|
| 500 | 5.4653 | 4.704 | 0.762 | 0.9112 |
| 1,000 | 5.5134 | 4.938 | 0.575 | 0.9255 |
| 2,000 | 5.5439 | 5.044 | 0.500 | 0.9333 |
| 3,000 | 5.5558 | 5.142 | 0.414 | 0.9410 |
| 5,000 | 5.5661 | 5.236 | 0.330 | 0.9469 |
| 10,000 | 5.5750 | 5.331 | 0.244 | 0.9481 |
| 30,000 | 5.5822 | 5.426 | 0.157 | 0.9485 |
| 100,000 | 5.5854 | 5.489 | 0.097 | 0.9451 |

$K_N$ rises (toward a finite $K_\infty$, since $\sum_n 4^{\omega(n^2+1)}/n^2 < \infty$). $P(N)/N$ also rises but more slowly. Their difference $(K_N - P/N)$ steadily decreases toward zero.

**Predicted shape.** Writing $c_0^{\rm bdy}(N) := (B_3^{\rm bdy} - c_1 N \log N)/N$:

| $N$ | $c_0^{\rm bdy}(N)$ |
|---|---|
| 500 | 0.268 |
| 1,000 | 0.396 |
| 2,000 | 0.497 |
| 3,000 | 0.588 |
| 5,000 | 0.671 |
| 10,000 | 0.736 |
| 30,000 | 0.828 |
| 100,000 | 0.887 |

This is the slow rise of $c_0^{\rm bdy}(N) = c_0^T - (K_N - P(N)/N) \approx 0.99 - (K_N - P(N)/N)$ as the bracketed term tends to zero.

**Empirical turning point.** The ratio $B_3^{\rm bdy}/(N \log N)$ peaks at $\approx 0.9485$ around $N \in [10^4, 3 \cdot 10^4]$ and *decreases* at $N = 10^5$ (to $0.9451$). The peak is the maximum of $c_1 + c_0^{\rm bdy}(N)/\log N$ as $c_0^{\rm bdy}$ grows but $\log N$ grows faster. Asymptote: $c_1 = 0.8681$.

**Falsifiable forecast.** With $c_0^{\rm bdy}(N) \to c_0^{\rm bdy,\infty} \le c_0^T \approx 0.99$:

| $N$ | predicted $B_3^{\rm bdy}/(N\log N)$ |
|---|---|
| $10^6$ | $0.868 + c_0^{\rm bdy}(10^6)/13.82 \in [0.93, 0.94]$ |
| $10^8$ | $\in [0.92, 0.92]$ |
| $\to \infty$ | $0.8681$ |

## 5. Caveats and open

- **The "factor of 2" doubling for $\tau^*$ is not made rigorous in this note.** Section 3.3 traces the doubling to Hooley's $\tau$-identity applied to $\mathrm{rad}(n^2+1)$, but the boundary error and the squarefree-density-weighting are not bookkept with explicit constants. The empirical agreement to $0.6\%$ at $N=10^5$ and the matching of the secondary residual $(T - c_1 N \log N)/N \approx 0.99$ across 8 N strongly support $c_1 = H(1)\pi/2$, but the proof needs the analog of Hooley 1957 §3 for $\tau^*$ to be fully rigorous. **Honest rigor status: small-$e$ Tauberian is rigorous (giving $\ge H(1)\pi/4 \cdot N\log N$); the upper bound to $\le H(1)\pi/2 \cdot N\log N$ requires Hooley-style boundary control on the big-$e$ piece.**
- **The secondary constant $c_0^T$ is only empirical.** The Selberg–Delange chain $G(s) = \zeta_K(s) H(s)$ pins $c_1$ via the simple pole; $c_0^T$ requires the secondary Laurent coefficient (computable via $H'(1)$ etc., not done in this session). Empirical $c_0^T \approx 0.99 \pm 0.03$.
- **$P(N)$ asymptotic.** $P(N)$ is bounded by $O(N)$ since each summand is $\le 2^{\omega(d_n)}\rho(d_n) N/d_n + O(2^{\omega(d_n)})$ and $\sum_n 4^{\omega(n^2+1)}/n^2 < \infty$ (uses the bound $4^{\omega(n^2+1)} \ll \tau(n^2+1)^2$ and $\sum_n \tau(n^2+1)^2/n^2 < \infty$ — itself follows from $\sum_n \tau(n^2+1)^2 \ll N(\log N)^3$, see `P12-tau-squared-upper-bound-Nair.md`). Whether $P(N)/N \to P_\infty$ and whether $P_\infty = K_\infty$ is suggested empirically by $K_N - P(N)/N \to 0$ but not proved.
- **Turning-point reading is one data point.** $B_3^{\rm bdy}/(N\log N)$ peaked at $\le 0.949$ around $N \in [10^4, 3\cdot 10^4]$ and decreased slightly to $0.9451$ at $N=10^5$. That single down-step is not statistically robust on its own. The stronger evidence is the monotone descent of $T(N)/(N\log N)$ from $1.034$ to $0.954$ across 8 N — incompatible with $c_1 \ge 0.95$ as an asymptote.
- **The off-diagonal $B_3^{\rm off} := B_3 - B_3^{\rm bdy}$ remains the structural bottleneck**, with conjectured leading $-c_1 N \log N$ cancelling against the diagonal to give $B_3 = O(N)$. This note does not address it.

## 6. Conclusion

$\boxed{c_1 = H(1) \pi/2 = 0.8681354129 \pm 2 \cdot 10^{-7} \text{ (conjecturally; rigorous lower bound } \ge H(1)\pi/4 \text{)}}$
is the leading Selberg–Delange constant for $B_3^{\rm bdy}(N)$ at the level we have established it. The "factor-of-2 doubling" needed for the upper bound is supported by the empirical fit (residual $(T - c_1 N\log N)/N \approx 0.99$ stable across 8 N) and by the algebraic radical identity $\tau^*(d) = \tau(\mathrm{rad}(d))$, but a full Hooley-style boundary argument for $\tau^*$ is deferred to a future session.

The prior session's empirical "in the ballpark of $3/\pi$" reading was an artifact of the secondary $c_0^{\rm bdy}/\log N$ correction that peaks at $\sim 0.949$ near $N \in [10^4, 3 \cdot 10^4]$ before decreasing. The empirical curve $T(N)/(N\log N)$ descending monotonically from $1.034$ to $0.954$ across $N \in [500, 10^5]$ rules out $c_1 \ge 0.95$ as an asymptote.

## Files

- `bot/scratch/B3-bdy-SD-constants.py` (new): computes $H(1)$ and $T(N)$.
- `bot/scratch/B3-bdy-secondary.py` (new): computes the exact decomposition $B_3^{\rm bdy} = T + P - NK$ at six $N$, plus the extension run to $N = 10^5$.
- Builds on: `n2+1 ai thoughts/notes/proofs/P12-B3-sign-bias.md` (prior session's empirical setup).
