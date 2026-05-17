# P12 — High-precision constants for the $c_0^T$ closed form

**Session.** 2026-05-07 ~21:30 UTC. Cheap, half-session refinement.
Pickup hint #4 from prev session
(`bot/sessions/2026-05-07T18-30-00Z.md`): recompute
$H(1), H'(1), \gamma_K$ at 10+ decimal digits to remove the
input-precision caveat from the closed-form prediction
$c_0^T_\infty = 2(RH'(1) + \gamma_K H(1) - RH(1)) - 2B^\infty$.

Notation as in `P12-c0T-AB-decomposition.md`:
$K = \mathbb Q(i)$, $R = \pi/4$, $\gamma_K := R\gamma + L'(1, \chi_4)$
(scaled Euler-Kronecker convention; constant term in the Laurent
expansion of $\zeta_K$ at $s = 1$),
$$H(s) = (1 - 4^{-s}) \prod_{p \equiv 1 \,(4)} (1 - 3 p^{-2s} + 2 p^{-3s})
                       \prod_{p \equiv 3 \,(4)} (1 - p^{-2s}).$$

## 1. Closed-form $L'(1, \chi_4)$

The classical Lerch–Kronecker formula gives the closed form
$$L'(1, \chi_4) \;=\; \frac{\pi}{4}\Big(\gamma + 2\log 2 + 3\log \pi - 4\log\Gamma(1/4)\Big).$$
Evaluated to 25 digits via `mpmath` at 40-digit precision:
$$L'(1, \chi_4) = 0.19290131679691242936\ldots$$
Cross-check against `mpmath.diff(beta, 1)` agrees to 9 digits (the
numerical-differentiation residual in `mpmath.diff` is the only
limit on the cross-check).

Derived constants:
- $R = \pi/4 = 0.78539816339745\ldots$
- $\gamma = 0.57721566490153\ldots$
- $\gamma_K = R\gamma + L'(1, \chi_4) = 0.64624543989481\ldots$

The prev sessions used $\gamma_K \approx 0.6462$ (4 digits); the high-precision
correction is $+4.5 \cdot 10^{-5}$.

## 2. $H(1)$ and $H'(1)$ via Euler product

$$H(1) = \frac{3}{4} \prod_{p \equiv 1(4)} (1 - 3/p^2 + 2/p^3)
                 \prod_{p \equiv 3(4)} (1 - 1/p^2),$$
and the logarithmic derivative
$$\frac{H'(1)}{H(1)} = \frac{\log 4}{3}
   + \sum_{p \equiv 1(4)} \frac{6 \log p \,(1/p^2 - 1/p^3)}{1 - 3/p^2 + 2/p^3}
   + \sum_{p \equiv 3(4)} \frac{2 \log p / p^2}{1 - 1/p^2}.$$

**Tail estimate via PNT-AP.** By partial summation against
$\theta_a(t) = \sum_{p \le t,\, p \equiv a(4)} \log p \sim t/2$,
$$\sum_{p > P} \frac{\log p}{p^2}
\;=\; -\frac{\theta(P)}{P^2} + 2\int_P^\infty \frac{\theta(t)}{t^3}\, dt
\;\sim\; \frac{1}{P}.$$
Applied to the weighted sum (coefficients $\le 6/p^2$ for split,
$\le 2/p^2$ for inert; density $\approx 1/2$ each) gives
$$\sum_{p > P} \text{(summand of } H'/H \text{)} \;\le\; \frac{4}{P}.$$
Similarly the truncation error of $\log H(1)$ past $P$ is bounded by
$\sum_{p > P} 3/p^2 \le 2/(P \log P)$ via PNT (the $\log p$ factor is
absent here, so $\int 1/(t^2 \log t)\, dt$ scales as $1/(P \log P)$;
the constant $2$ is conservative, since the average density coefficient
is $(3+1)/2 = 2$).

**Computation paths in `bot/scratch/highprec-constants.py`**:
- Path 1: `mpmath` 40-digit Euler product at $P = 10^7$ (~620k primes,
  ~27 s). Output:
  $H(1)_{|10^7} = 0.55267210050496\ldots$,
  $(H'/H)_{|10^7} = 1.51190340324778\ldots$,
  $H'(1)_{|10^7} = 0.83558682963355\ldots$.
- Path 2: `float64` Euler product at $P = 10^8$ (~5.76M primes,
  ~7 s). Output:
  $H(1)_{|10^8} = 0.5526720946007\ldots$,
  $(H'/H)_{|10^8} = 1.5119037632415\ldots$,
  $H'(1)_{|10^8} = 0.8355870196654\ldots$.

**Cross-check.** The empirical increment $10^7 \to 10^8$ is
$\Delta H(1) = -5.9 \cdot 10^{-9}$ and $\Delta H'(1) = +1.9 \cdot 10^{-7}$;
both are within the $4/P|_{P=10^7} \cdot H(1) \approx 2.2 \cdot 10^{-7}$
tail bound — a passing cross-check.

**Best estimates** (Path 1 mp value at $P = 10^7$ plus the float64-derived
$10^7\to 10^8$ increment, with tail past $10^8$):
$$H(1) = 0.552672094601 \pm 1.1 \cdot 10^{-9},$$
$$H'(1) = 0.835587019665 \pm 2.2 \cdot 10^{-8}.$$

These differ from the prev-session 6-digit values $H(1) = 0.552674$,
$H'(1) = 0.83558$ by $-1.3 \cdot 10^{-6}$ and $+7 \cdot 10^{-6}$
respectively.

(The float64 path is independent of the mp path. Float64 has ~13-digit
precision; for 5.76M sums of small bounded-magnitude terms, the rounding
error grows like $\sqrt N \cdot \epsilon \sim 5 \cdot 10^{-13}$
under independence assumptions, well below the truth-truncation.)

## 3. Sub-components and structural part (high-precision)

All values from `bot/scratch/highprec-constants.py` (mp 40-digit
arithmetic):

| Quantity | High-precision value | uncertainty |
|---|---|---|
| $R$ | $0.7853981634\ldots$ | exact |
| $\gamma_K$ | $0.6462454399\ldots$ | $< 10^{-10}$ |
| $H(1)$ | $0.5526720946007\ldots$ | $\pm 1 \cdot 10^{-9}$ |
| $H'(1)$ | $0.8355870196654\ldots$ | $\pm 2 \cdot 10^{-8}$ |
| $A^\infty = R H(1)$ | $0.4340676480604\ldots$ | $\pm 1 \cdot 10^{-9}$ |
| $R H'(1)$ | $0.6562685106039\ldots$ | $\pm 2 \cdot 10^{-8}$ |
| $\gamma_K H(1)$ | $0.3571618208928\ldots$ | $\pm 7 \cdot 10^{-10}$ |
| $c_<^\infty = R H'(1) + \gamma_K H(1)$ | $1.01343033149676\ldots$ | $\pm 2 \cdot 10^{-8}$ |
| structural $= 2(c_<^\infty - A^\infty)$ | $1.15872536687268\ldots$ | $\pm 5 \cdot 10^{-8}$ |

These are the canonical values. They supersede:
- prev session's "structural = $1.158730$" (off by $-4.6 \cdot 10^{-6}$);
- prev session's "$c_<^\infty = 1.013429$" (off by $+1.4 \cdot 10^{-6}$);
- prev session's "$\gamma_K = 0.6462$" (off by $+4.5 \cdot 10^{-5}$).

The dominant prev-session error was rounding $\gamma_K$ to 4 digits,
which on its own shifts structural by $\Delta\gamma_K \cdot 2H(1)
\approx 5 \cdot 10^{-5}$.

## 4. Headline closed-form prediction

$$\boxed{\; c_0^T_\infty \;=\; 1.158725367 \;-\; 2 B^\infty
        \;\approx\; 0.987317367 \quad \text{(using heuristic } B^\infty = 0.085704\text{).} \;}$$

Compare:
- prev-session-quoted prediction: $0.987256$ (6-digit input).
- this-session high-precision: $0.987317$ (12-digit input).
- empirical $c_0^T(10^7) = 0.987203$.

The high-precision prediction has a *larger* gap to the empirical value
($1.14 \cdot 10^{-4}$ vs the prev session's $5 \cdot 10^{-5}$). The
prev-session match was input-precision-noise-limited; the precision-induced
shift was in the direction of GROWING the residual.

## 5. Decomposition of the $1.14 \cdot 10^{-4}$ residual

Algebraic identity at $N = 10^7$ (exact):
$$c_0^T(10^7) = 2\big(c_<^{\rm app}(10^7) - A(10^7)/10^7 - B(10^7)/10^7\big),$$
where (from prev session's empirical sieve):
$c_<^{\rm app}(10^7) = 1.013354$,
$A(10^7)/10^7 = 0.4340743$,
$B(10^7)/10^7 = 0.0856787$.
Numerical: $2(1.013354 - 0.4340743 - 0.0856787) = 0.987202$, matching empirical
$0.987203$ to within rounding.

Decomposition:
- $\Delta_{c_<} := c_<^\infty - c_<^{\rm app}(10^7) = 1.013430 - 1.013354 = +7.63 \cdot 10^{-5}$.
- $\Delta_A := A^\infty - A(10^7)/10^7 = 0.434068 - 0.434074 = -6.65 \cdot 10^{-6}$.
- $\Delta_B := B^\infty - B(10^7)/10^7 = 0.085704 - 0.085679 = +2.53 \cdot 10^{-5}$.

Then
$$\text{predicted} - \text{empirical} = 2(\Delta_{c_<} - \Delta_A - \Delta_B)
= 2 \cdot (5.77 \cdot 10^{-5}) = 1.154 \cdot 10^{-4},$$
matching the directly-computed $1.14 \cdot 10^{-4}$ residual to within
$1 \cdot 10^{-6}$ (residual rounding in the per-piece numerics).

**Signed contributions (NOT proportions of the gap, since they have
opposite signs).** Each $\Delta$ contributes signed to the
gap = $2(\Delta_{c_<} - \Delta_A - \Delta_B)$:
- $+2\Delta_{c_<} = +1.527 \cdot 10^{-4}$ (SD remainder on $c_<^\infty$,
  predicted exceeds empirical, contributes to the gap).
- $-2\Delta_A = +1.33 \cdot 10^{-5}$ (SD remainder on $A^\infty$;
  $A^\infty$ is below $A(10^7)/10^7$, the negative sign in the gap
  formula makes this positive).
- $-2\Delta_B = -5.06 \cdot 10^{-5}$ (heuristic $B^\infty$ exceeds
  empirical $B(10^7)/10^7$; the negative sign makes this
  *negative* — i.e. the heuristic-$B$ overshoot is REDUCING the
  predicted-empirical gap, not contributing to it).

Net: $1.527 + 0.133 - 0.506 = 1.154 \cdot 10^{-4}$.

So the SD finite-$N$ remainder on $c_<^\infty$ alone ($+1.53 \cdot 10^{-4}$)
is LARGER than the empirical-vs-predicted gap; without the
heuristic-$B$ overshoot REDUCING the gap by $5 \cdot 10^{-5}$, the
prediction would miss the empirical by $\sim 1.7 \cdot 10^{-4}$.
This is more concerning than the previous framing suggested: the
"good agreement" between heuristic-$B^\infty$ and empirical at $N = 10^7$
is partly due to two errors of opposite sign happening to cancel a third
of the $c_<^\infty$ SD-remainder contribution.

Pinning $B^\infty$ better requires either reducing the SD remainder on
$c_<^\infty$ (extending $N$ to e.g. $10^9$) or independent rigorization
of $B^\infty$.

## 6. Status / caveats

**What this session achieves.**
1. Removes the input-precision caveat from the closed-form prediction.
   The structural part is now precise to $\sim 5 \cdot 10^{-8}$.
2. Reveals that the prev-session quoted "$0.987256$" prediction was
   off by $+6 \cdot 10^{-5}$ from the true high-precision value
   $0.987317$, due to the 4-digit truncation of $\gamma_K$.
3. Re-factors the empirical-vs-predicted gap at $N = 10^7$:
   the SD finite-$N$ remainder on $c_<^\infty$ alone is $+1.53 \cdot 10^{-4}$
   (LARGER than the gap), partially canceled by the heuristic-$B^\infty$
   overshoot ($-5 \cdot 10^{-5}$) and the SD-on-$A^\infty$ contribution
   ($+1 \cdot 10^{-5}$). The "match" at $N = 10^7$ is partially fortuitous
   sign-cancellation between three different finite-$N$ effects.

**What remains uncertain.**
1. **$B^\infty$ heuristic.** The value $0.085704$ inherits uniform-in-log
   and Hensel-CRT factorization heuristics from the prev-prev-prev
   session's per-prime $\nu_p^+$ closed form. Not rigorous.
2. **Existence of $B^\infty$.** Plausible but not proved. (Cf. pickup
   hint #3: cheap session to establish existence without computing
   the value.)
3. **SD remainder rate.** The empirical $\Delta_{c_<} \approx 7.6 \cdot 10^{-5}$
   at $N = 10^7$ is consistent with $O((\log N)^{-A})$ for any $A$,
   so we cannot pin $B^\infty$ below the $\sim 10^{-4}$ level from this
   comparison alone.

**Banked methodological lesson.** When a "match within input precision"
is reported across sessions, ALWAYS recompute at higher precision before
banking. The prev session's "match within $5 \cdot 10^{-5}$" was
input-precision-noise-limited; the precision-induced shift was such that
the high-precision gap GREW to $1.1 \cdot 10^{-4}$, becoming dominated
by SD finite-$N$ remainder rather than heuristic-$B^\infty$ uncertainty.

## 7. Files

- `bot/scratch/highprec-constants.py` (new): contains both
  Path 1 (mp 40-digit at $P = 10^7$, ~27 s) and Path 2 (float64 at
  $P = 10^8$, ~7 s).
- Builds on: `P12-c0T-AB-decomposition.md` (the AB structural identity),
  `P12-c0T-N1e7-validation.md` (empirical $c_0^T(10^7)$),
  `P12-c0T-secondary-constant.md` (the $c_<^\infty$ closed form).
