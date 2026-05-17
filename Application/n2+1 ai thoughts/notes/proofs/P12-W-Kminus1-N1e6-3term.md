# P12: $W_{K-1}$ vs three-term Laurent prediction at $N = 10^6$ (2026-05-06)

## Summary

Extended the prior session's $W_{K-1}$ vs $P^{(3)}$ comparison by one decade to
$N = 10^6$, and added the third Laurent term to the prediction. The third term
$b'_0 \cdot N$ comes from the constant Laurent coefficient of $T_3(s) = \zeta_K(s)^2
H_3(s)$ at $s = 1$. Computed $b'_0 \approx 0.939$ in closed form. Empirical residual
$(W_{K-1} - P^{(3,3)})/N$ across five $N$ from $10^4$ to $10^6$ is bounded in
$[+0.04, +0.21]$, vs the previous two-term residual range $[+0.13, +0.47]$ (mean
$0.112$ vs $0.282$, ratio $2.52\times$; max $0.213$ vs $0.471$, ratio $2.21\times$).
The 3-term residual normalized by the band size, $\rho_3 := (W_{K-1} - P^{(3,3)})/
(N - n_-)$, lies in $[0.41, 1.26]$ across the same five $N$, vs the prior 2-term
$[1.35, 2.19]$.

**Scope of the claim.** Empirically established: $(W_{K-1} - P^{(3,3)})/N$ is bounded
by $0.213$ across five $N$ spanning $L \in [9.21, 13.82]$ (factor $1.5$ range).
**NOT** established: that the residual is $O(N)$ asymptotically. Five points across
factor-$1.5$ $L$ cannot discriminate $O(N)$ from $O(N L^{0.5})$ or $O(N (\log L)^c)$.
**Conditional on Hooley boundary cancellation** (an unproved assumption discussed
in the soft-spots list), the natural reading is $O(N)$; without that, the
unconditional bound on the boundary is much worse.

## Setup recap (from 2026-05-05 session)

For $N \ge 1$, dyadically partition the $d$-tail by $K = \lceil \log_2((N^2+1)/N)
\rceil$, $\inf := N \cdot 2^{K-1}$. The topmost window of $B_>(N)$ is
$$
W_{K-1} = \sum_{n_- < n \le N} \tau((n^2+1)^2), \qquad n_- = \lfloor \sqrt{\inf - 1} \rfloor.
$$
Equivalently, $W_{K-1}$ is a partial sum of $S_3(N) := \sum_{n \le N} \tau((n^2+1)^2)$
on the band $(n_-, N]$.

By the dual identity $\tau(m^2) = \sum_{d \mid m} 2^{\omega(d)}$, $S_3(N) = \sum_d
2^{\omega(d)} N_d(N)$ where $N_d(N) = \#\{n \le N : d \mid n^2+1\}$. The relevant
generating function is
$$
T_3(s) = \sum_d \frac{2^{\omega(d)} \rho(d)}{d^s} = \zeta_K(s)^2 H_3(s),
$$
$K = \mathbb{Q}(i)$, $H_3$ analytic on $\Re s > 1/2$ with explicit Euler product.
From the prior session, $H_3(1) \approx 0.27775$, $H_3'(1) \approx 0.84241$.

## Three-term Laurent expansion of $T_3$ at $s = 1$

$T_3$ has a pole of order 2 at $s = 1$ (from $\zeta_K^2$). Write
$$
T_3(s) = \frac{c_2}{(s-1)^2} + \frac{c_1}{s-1} + c_0 + O(s-1).
$$
Using $\zeta_K(s) = R/(s-1) + \gamma_K + \beta_K (s-1) + O((s-1)^2)$ with $R = \pi/4$,
the squared expansion is $\zeta_K^2(s) = R^2/(s-1)^2 + 2 R \gamma_K/(s-1) + (\gamma_K^2
+ 2 R \beta_K) + O(s-1)$. Multiplying by $H_3(s) = H_3(1) + H_3'(1)(s-1) + H_3''(1)
(s-1)^2/2 + \ldots$:

$$
\begin{aligned}
c_2 &= R^2 \, H_3(1), \\
c_1 &= R^2 \, H_3'(1) + 2 R \gamma_K \, H_3(1), \\
c_0 &= R^2 \, \frac{H_3''(1)}{2} + 2 R \gamma_K \, H_3'(1) + (\gamma_K^2 + 2 R \beta_K) \, H_3(1).
\end{aligned}
$$

Numerical with $\gamma_K \approx 0.6462$, $\beta_K \approx 0.0915$, $H_3(1) \approx
0.27775$, $H_3'(1) \approx 0.84241$:
- $c_2 = b'_2 \approx 0.17133$
- $c_1 = b'_1 \approx 0.80157$ (matches prior session)
- For $c_0 = b'_0$, need $H_3''(1)$.

### Computing $H_3''(1)$

Use $(\log H_3)'' = H_3''/H_3 - (H_3'/H_3)^2$, i.e.
$$
H_3''(1) = H_3(1) \cdot \big[((\log H_3)'(1))^2 + (\log H_3)''(1)\big].
$$
$(\log H_3)'(1) = H_3'(1)/H_3(1) \approx 3.0330$ (independently checked from
prior Euler-product sum).

For $(\log H_3)''(1)$, sum the second derivatives of the local logs $f_p =
\log L_p$ over primes:

- **At $p = 2$**: $f_2(s) = \log(1 + 2^{1-s}) + 2 \log(1 - 2^{-s})$. Direct
  differentiation gives $f_2''(1) = -(15/4)(\log 2)^2 \approx -1.801$.

- **At $p \equiv 1 \pmod 4$**: $f_p(s) = \log(1 + 3 p^{-s}) + 3 \log(1 - p^{-s})$.
  Computed numerically via central finite difference of the explicit $f_p'(s)
  = 12 p^{-2s} \log p / [(1 - p^{-s})(1 + 3 p^{-s})]$ at $s = 1$, summed over
  split primes up to $10^6$.

- **At $p \equiv 3 \pmod 4$**: $f_p(s) = 2 \log(1 - p^{-2s})$. Direct
  $f_p''(1) = -8 (\log p)^2 / [p^2 (1 - 1/p^2)^2]$.

Result: $(\log H_3)''(1) \approx -10.042$ (Euler-product sum to $p < 10^6$).

Hence $H_3''(1) \approx 0.27775 \cdot (3.0330^2 + (-10.042)) = 0.27775 \cdot
(-0.843) \approx -0.234$.

### Plugging in

$$
\begin{aligned}
R^2 \cdot H_3''(1)/2 &\approx (\pi/4)^2 \cdot (-0.234)/2 \approx -0.0722, \\
2 R \gamma_K H_3'(1) &\approx 2 \cdot (\pi/4) \cdot 0.6462 \cdot 0.84241 \approx +0.8551, \\
(\gamma_K^2 + 2 R \beta_K) H_3(1) &\approx (0.4176 + 0.1437) \cdot 0.27775 \approx +0.1559.
\end{aligned}
$$
$$
\boxed{b'_0 = c_0 \approx 0.9388}.
$$

## Three-term partial-sum prediction

By the standard Perron-residue calculation, for $\Sigma_3(X) := \sum_{d \le X}
2^{\omega(d)} \rho(d)/d$:
$$
\Sigma_3(X) = \frac{c_2}{2} (\log X)^2 + c_1 \log X + c_0 + (\text{Tauberian error}).
$$

Substituting $X \mapsto N^2 + 1$ (with $\log(N^2+1) = 2L + O(N^{-2})$):
$$
S_3(N) = N \cdot \Sigma_3(N^2+1) + (\text{boundary}) = 2 b'_2 N L^2 + 2 b'_1 N L + b'_0 N + \text{(error)}.
$$

For the topmost-window partial sum $W_{K-1}$ on the band $(n_-, N]$, the
3-term prediction is the difference of the full-$S_3$ predictions:
$$
P^{(3,3)} := \big[2 b'_2 N L_N^2 + 2 b'_1 N L_N + b'_0 N\big] - \big[2 b'_2 n_- L_{n_-}^2 + 2 b'_1 n_- L_{n_-} + b'_0 n_-\big].
$$
Since $b'_0 (N - n_-) = b'_0 \cdot \text{band}$, this differs from the 2-term
prediction $P^{(3)}$ by $b'_0 \cdot (N - n_-)$.

## Empirical comparison at five $N$

Direct sieve-and-factor computation in `bot/scratch/W-Kminus-1-symbolic.py` at
$N \in \{10^4, 3 \cdot 10^4, 10^5, 3 \cdot 10^5, 10^6\}$ yields

| $N$ | $L$ | band $= N - n_-$ | $W/N$ | $P^{(3)}/N$ | $P^{(3,3)}/N$ | $(W-P^{(3)})/N$ | $(W-P^{(3,3)})/N$ | $(W-P^{(3,3)})/$band | $S_3/\text{pred}_{2\text{-term}}$ |
|---|---|---|---|---|---|---|---|---|---|
| $10^4$ | 9.210 | 950 | 5.0046 | 4.876 | 4.965 | $+0.129$ | $+0.039$ | $0.414$ | $1.0322$ |
| $3 \cdot 10^4$ | 10.309 | 7830 | 16.0934 | 15.732 | 15.978 | $+0.361$ | $+0.116$ | $0.444$ | $1.0286$ |
| $10^5$ | 11.513 | 19046 | 14.0636 | 13.777 | 13.956 | $+0.286$ | $+0.108$ | $0.565$ | $1.0235$ |
| $3 \cdot 10^5$ | 12.612 | 19567 | 5.6610 | 5.518 | 5.579 | $+0.143$ | $+0.082$ | $1.255$ | $1.0219$ |
| $10^6$ | 13.816 | 275923 | 27.1912 | 26.720 | 26.979 | $+0.471$ | $+0.213$ | $0.770$ | $1.0191$ |

**Key reads:**

1. **3-term residual $/N$ is uniformly smaller**: $(W - P^{(3,3)})/N \in [0.04, 0.21]$,
   vs 2-term residual $[0.13, 0.47]$. Mean drops from $0.282$ to $0.112$ — about
   $2.5\times$ reduction.

2. **3-term residual scales like the band, on average**: $(W - P^{(3,3)})/\text{band}
   \in [0.41, 1.26]$, mean $0.69$, vs 2-term $[1.35, 2.19]$, mean $1.63$.
   **Spread caveat (skeptic-flagged):** the per-band spread INCREASED after
   adding the 3rd term (max/min ratio $1.62 \to 3.06$), even as the absolute
   spread $|max-min|$ shrank ($0.84 \to 0.85$, essentially unchanged). The
   honest reading is: the 3-term Laurent corrects the AVERAGE residual scale
   from $\sim 1.6$ per band to $\sim 0.7$ per band, but introduces (or fails to
   absorb) sensitivity to band-geometry. The residuals at the 5 points
   $\{0.41, 0.44, 0.57, 1.26, 0.77\}$ are non-monotone in $N$ and dominated by
   geometric position effects, not by a clean asymptotic.

3. **The full-$S_3$ ratio confirms convergence**: $S_3/\text{pred}_{2\text{-term}}$
   monotonically descends from $1.0322$ at $N = 10^4$ to $1.0191$ at $N = 10^6$,
   consistent with a $b'_0 N$ + sub-$N$ residual sequence.

## Cross-check: full $S_3$ residual at $N = 10^6$

The 3-term prediction for full $S_3(10^6)$ is
$$
2 \cdot 0.17133 \cdot 10^6 \cdot 190.88 + 2 \cdot 0.80157 \cdot 10^6 \cdot 13.82 + 0.939 \cdot 10^6 \approx 88.5 \text{ million}.
$$
Empirical $S_3(10^6) \approx 89.2$ million. Residual $\approx 0.7 \cdot 10^6$, i.e.,
$\approx 0.7 N$. This is in the same ballpark as the WINDOW residual constant
$(W - P^{(3,3)})/\text{band}$ averaged over the four highest-$N$ points, supporting
the interpretation that the missing piece is a uniform-in-$X$ Tauberian remainder
of size $\Theta(N)$, common to both the full sum and the partial.

## Strategic implications

1. **The $r = 1$ formal-SD chain on $T_3$ is now empirically pinned to three
   leading Laurent coefficients.** With $c_2, c_1, c_0$ all explicit, predicting
   $S_3(N)$ to within $\le 0.8\%$ at $N = 10^6$ ($S_3$ residual after 3-term
   Laurent: $\approx 0.7 N$, vs $S_3 \approx 89 \cdot 10^6$).

2. **The residual is empirically bounded by $0.213 N$ across $L \in [9.21,
   13.82]$**. **NOT yet established as $O(N)$ asymptotically:** five data
   points across factor-$1.5$ $L$ cannot discriminate $O(N)$ from $O(N L^{0.5})$
   or even $O(N L)$ with a small constant. The 2-to-3-term Laurent reduction
   is real, but extrapolation to all $N$ is not warranted from this data alone.

3. **What's needed to prove $W_{K-1} = O(N)$ rigorously — TWO independent steps,
   not one.**
   - **(i) Effective Selberg-Delange for $\Sigma_3$.** Tenenbaum II.5.2 with
     $\kappa = 2$ and $H = H_3$ (regular on $\Re s > 1/2$) gives, for any $A > 0$,
     $\Sigma_3(X) - (\text{3-term}) = O(1/(\log X)^A)$. Applied to a band
     gives $O(N/(\log N)^A)$ on the SD side. **Standard tools, 1 session of
     bookkeeping.**
   - **(ii) Hooley-boundary cancellation for the $S_3 = N\Sigma_3(N^2+1) +
     B_3(N)$ remainder term.** The unconditional bound on $B_3(N)$ via $\delta_d
     := N_d - \rho(d)N/d = O(\rho(d))$ summed against $2^{\omega(d)}$ over
     $d \le N^2+1$ is $O(N^2 (\log N)^c)$ — far worse than $O(N)$. To get
     $O(N)$ requires the same kind of cancellation that Hooley exploited in
     1957 for $S_1 = \sum \tau(n^2+1)$. **This is the actual bottleneck**,
     and is comparable in difficulty to the entire Hooley 1957 paper. The
     prior strategy file's framing of "Hooley boundary as the next analytic
     target" is correct here.

   In particular: the empirical $O(N)$ reading is **conditional on (ii)**.
   Without (ii), even an executed (i) leaves the residual at the unconditional
   $O(N^2 (\log N)^c)$ bound. The 5-point empirical evidence supports the
   $O(N)$ hypothesis but does not by itself reduce the rigorous problem.

## Documented soft spots (caveats)

- **Five data points only.** $L$ varies by factor $1.5$. The asymptotic order
  claim $O(N)$ is empirically supported but not proved.

- **$N = 3 \cdot 10^5$ anomaly persists and is symptomatic.** $(W - P^{(3,3)})/
  \text{band} = 1.26$ there, vs $0.41$–$0.77$ at the other four — a factor-of-3
  spread. Skeptic's read (accepted): this is precisely the regime where the
  $b'_0 \cdot \text{band}$ correction should be cleanest (small band$/N = 6.5\%$
  means the band is a small slice; constant correction should saturate); the
  fact that the per-band residual GREW after adding the third term indicates
  $P^{(3,3)}$ has fixed the per-$N$ scale but introduced (or failed to absorb)
  band-geometry sensitivity. Concretely, $\inf - 1 = N \cdot 2^{K-1} - 1$
  varies discontinuously with $K = \lceil \log_2 N \rceil$, and the band
  position $n_-/N = \sqrt{\inf/N^2}$ jumps when $\log_2 N$ crosses an integer.
  This jump is a real effect not captured by the smooth Laurent expansion of
  $\Sigma_3$. To check whether the anomaly is band-position-fraction or some
  deeper issue, the natural next test is $N \in \{2 \cdot 10^5, 5 \cdot 10^5\}$
  (different jump-positions within the same dyadic block).

- **$b'_0$ uses Euler-product partial sums to $p < 10^6$.** Truncation tail
  for $(\log H_3)''(1)$: at split $p \equiv 1 \pmod 4$, $f_p''(1) = O((\log p)^2/p^2)$,
  so the tail is $\sum_{p > 10^6, p \equiv 1(4)} O((\log p)^2/p^2) \sim
  O((\log X)^2/(X \log X)) \cdot (1/2) = O(\log X / X)$ at $X = 10^6$, giving
  $\sim 10^{-5}$ (skeptic-corrected; prior estimate $10^{-6}$ ignored the
  $(\log p)^2$ factor). At fourth decimal of $b'_0$. Cross-check (independent):
  $H_3'(1) = H_3(1) \cdot (\log H_3)'(1) = 0.27775 \cdot 3.0330 = 0.84241$ matches
  the prior independently-computed value to 5 decimal places — confirms the
  first-derivative sum is converged at $p < 10^6$, supporting that the
  second-derivative sum is too.

- **$\beta_K$ used $\approx 0.0915$ from prior P12-c0 work.** Inherits the prior
  session's accuracy ($\approx 4$ decimal places, not separately re-derived here).
  Sensitivity: the term $(\gamma_K^2 + 2 R \beta_K) H_3(1)$ in $b'_0$ has
  $\partial / \partial \beta_K = 2 R H_3(1) \approx 0.436$. Perturbing $\beta_K$
  by $0.001$ shifts $b'_0$ by $\approx 4.4 \cdot 10^{-4}$, well below the
  4-decimal precision of the headline $b'_0 = 0.939$.

- **No rigorous theorem yet.** The $O(N)$ residual is empirical; the effective
  Selberg-Delange application is sketched not executed.

## Connection to prior strategy

This continues the thread "$W_{K-1}$ vs $P^{(3)}$" from 2026-05-05 19:30 UTC.
That session showed $\sim 10\times$ reduction from $P^{(2)}$ to $P^{(3)}$
(2-term Laurent on the correct $S_3$ moment) at four $N$. This session adds
$N = 10^6$ and a third Laurent term, getting another $\sim 2.5\times$
reduction in the residual. The residual is now visually consistent with $O(N)$
across $L \in [9.21, 13.82]$ — the asymptotic-order question that the prior
session had to leave open is sharpened to "consistent with $O(N)$".

## Files

- `bot/scratch/W-Kminus-1-symbolic.py` (extended to include $N = 10^6$ and full
  $S_3$ output)
- `bot/scratch/W-Kminus-1-bprime0.py` (new — computes $b'_0$ and post-processes)
- This note: `n2+1 ai thoughts/notes/proofs/P12-W-Kminus1-N1e6-3term.md`
