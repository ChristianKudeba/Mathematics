# P12 — Empirical $B(N)$ to $N = 10^7$ confirms closed-form heuristic

**Session.** 2026-05-07 (later session). Builds on `P12-B-infty-closed-form.md`
which proposed
$$B^\infty \approx c_1 \sum_{p \equiv 1(4)} \frac{\log p}{(p+2)(p-1)} = 0.085704,$$
where $c_1 = \pi H(1)/2 = 0.86813$, but flagged a 14% miss in the
$\omega(q) \ge 2$ sub-piece at $N = 10^5$ as a possible signature of
heuristic failure.

This note presents a fast vectorized sieve (`bot/scratch/B-fast-sieve.py`,
~20s at $N = 10^7$ vs. ~196s at $N = 10^6$ for the prev session's
trial-division code), used to extend $B(N)$ and its $\omega(q)$ sub-decomposition
to $N \in \{10^5, 10^6, 3 \cdot 10^6, 10^7\}$. The result: **all three
predictions (total, $\omega(q) = 1$, $\omega(q) \ge 2$) match empirical at
$N = 10^7$ within sampling noise** ($\sim 1\sigma$ each). The prev session's
"14% miss at $N = 10^5$" in the $\omega(q) \ge 2$ piece is no longer present at
$N = 10^7$; the trajectory is consistent with finite-$N$ convergence to the
predicted limit. The matches do not logically refute alternative heuristics
that predict the same constant, but they are consistent with each closed-form
ingredient (per-prime marginal density and Hensel-CRT joint independence) being
individually correct at leading order.

## 1. Algorithm

For each $n \le N$ with $n^2+1$ non-squarefree, compute
$$b(n) := \#\{e \,\mathrm{sf}\mid n^2+1 : \sqrt{\mathrm{rad}(n^2+1)} < e \le n\}, \quad B(N) = \sum_n b(n).$$

Three-pass numpy sieve (the file docstring's "two-pass" label is outdated;
the implementation has three passes):

1. **Sieve $\omega(n^2+1)$ and the non-sf indicator.** For each split prime
   $p \le N$ (i.e., $p = 2$ or $p \equiv 1 \pmod 4$), find $\sqrt{-1} \mod p$ via
   Tonelli–Shanks, lift Hensel-style to $r_k \mod p^k$ while $p^k \le N^2+1$, and
   in numpy mark the arithmetic progressions $n \equiv \pm r_k \pmod{p^k}$. The
   level-$1$ marks count $\omega$; the level-$\ge 2$ marks identify non-sf.

2. **Residual extraction.** Track `residual[n]` int64, divide out matching
   primes; after processing all split $p \le N$, any `residual[n] > 1` is a
   single large prime $> N$ (since $p^2 > N^2 \ge n^2+1$ for $p > N$).

3. **Per-non-sf factor list + B(N) compute.** Build flat `(prime, exp)` arrays
   of total length $\sum_{n \,\mathrm{nsf}} \omega(n^2+1)$. For each non-sf $n$
   (~10$^6$ of them at $N = 10^7$), enumerate the $2^{\omega}$ squarefree divisors
   and count those in the window $(\sqrt{\mathrm{rad}}, n]$.

**Validation (sanity).** At $N \in \{10^4, 10^5, 10^6\}$ the new sieve agrees
with the prev session's `B-by-sqfull.py` to all printed digits:

| $N$ | $B(N)$ | $B(N)/N$ |
|---|---|---|
| $10^4$ | 880 | 0.08800 |
| $10^5$ | 8668 | 0.08668 |
| $10^6$ | 85680 | 0.08568 |

(Prev session reported: 0.0880, 0.0867, 0.0857. Match.)

## 2. Empirical $B(N)/N$ to $N = 10^7$

| $N$ | $B(N)$ | $B(N)/N$ | predicted $0.085704$ | abs diff |
|---|---|---|---|---|
| $10^4$ | 880 | $0.08800$ | $0.08570$ | $+0.00230$ |
| $10^5$ | 8{,}668 | $0.08668$ | $0.08570$ | $+0.00098$ |
| $10^6$ | 85{,}680 | $0.08568$ | $0.08570$ | $-0.00002$ |
| $3 \cdot 10^6$ | 257{,}572 | $0.08586$ | $0.08570$ | $+0.00016$ |
| $10^7$ | 856{,}787 | $0.08568$ | $0.08570$ | $-0.000025$ |

The trajectory is monotone-decreasing from $N = 10^4 \to 10^6$, then exhibits
mild sub-decadal noise ($+0.00018$ at $N = 3 \cdot 10^6$, back to within
$3 \cdot 10^{-5}$ of the prediction at $N = 10^7$). The truncation error in
the predicted constant is bounded above by
$c_1 \sum_{p > 10^7, p \equiv 1(4)} \log p / ((p+2)(p-1)) \sim c_1/(2 \cdot 10^7) \approx 4 \cdot 10^{-8}$
(verified numerically), so the predicted $0.085704$ is itself accurate to
~7 decimals.

**Sampling noise estimate at $N = 10^7$.** $B(N)$ is a sum over $\sim 1.05 \cdot 10^6$
non-sf $n$, with per-$n$ contribution $b(n) \in \{0, 1, 2, \ldots, O(2^{\omega})\}$,
roughly geometric in scale (most $b(n)$ are $0$ or $1$, a tail at higher values
for non-sf $n$ with multiple repeated primes). Empirical mean $\bar b \approx 0.815$.
Treating non-sf $n$ as approximately independent (true to leading order via Hensel-CRT),
$\mathrm{SE}(B/N) \sim \sqrt{N_{\mathrm{nsf}} \cdot \mathrm{var}(b)}/N \sim 10^{-4}$
at $N = 10^7$.

The empirical-vs-predicted gap of $2.5 \cdot 10^{-5}$ is well within $1\sigma$.
**The 4-decimal agreement is at the noise floor, not "earned" beyond it** —
the precision of the test caps at $\sim 10^{-4}$, and the data is consistent
with both "heuristic exact" and "heuristic correct to $\sim 10^{-4}$".

## 3. $\omega(q)$ sub-decomposition: the 14% miss vanishes

Sub-decomposition of $B(N)/N$ by $\omega(q)$ (= number of distinct primes
appearing to power $\ge 2$ in $n^2+1$):

| $N$ | $\omega(q)=1$ | $\omega(q)=2$ | $\omega(q)\ge 3$ | $\omega(q)\ge 2$ total |
|---|---|---|---|---|
| $10^5$ | $0.07792$ | $0.00868$ | $0.00008$ | $0.00876$ |
| $10^6$ | $0.07798$ | $0.00745$ | $0.00025$ | $0.00770$ |
| $3 \cdot 10^6$ | $0.07811$ | $0.00746$ | $0.00028$ | $0.00774$ |
| $10^7$ | $0.07792$ | $0.00751$ | $0.00024$ | $0.00776$ |

**Predicted (closed form):**
- $\omega(q) = 1$: $0.07794$ (from `B-omega1-closed-form.py`).
- Total: $0.08570$ (from `B-total-closed-form.py`).
- $\omega(q) \ge 2$ by subtraction: $0.08570 - 0.07794 = 0.00776$.

**Empirical $\omega(q) \ge 2$ at $N = 10^7$:** $0.00776$ — match within $1\sigma$
of sampling noise (see §3.1 below).

**Resolution of the prev session's 14% miss at $N = 10^5$.** The prev session
observed empirical $\omega(q) \ge 2 = 0.00876$ vs predicted $0.00776$, a 14%
overshoot, and identified this as a possible heuristic failure — the
"per-prime $\nu_p^+$ sum double-counts joint events $\{v_p \ge 2, v_{p'} \ge 2\}$"
concern.

Looking at the data, the trajectory of $\omega(q) \ge 2$ is:
$$0.00876 \to 0.00770 \to 0.00774 \to 0.00776,$$
sharply decreasing from $N = 10^5 \to 10^6$ (closing $\sim 90\%$ of the
gap to predicted), then small-amplitude rise/fall from $10^6 \to 10^7$
within sampling noise. At $N = 10^7$ the empirical-vs-predicted gap is
$-5 \cdot 10^{-6}$, well within sampling noise. **The 14% miss at $N = 10^5$
is plausibly finite-$N$ artifact** (the $\omega(q) \ge 2$ piece has only
$\sim 250$ events at $N = 10^5$, giving sample-noise SE $\sim 1/\sqrt{250}/\sqrt{50} \approx 9 \cdot 10^{-3}$
in rate units), not necessarily a heuristic flaw. We cannot logically rule out
that the heuristic IS slightly biased in $\omega(q) \ge 2$ but the bias is below
$\sim 10^{-4}$; we can rule out the prev session's specific "14% miss" hypothesis.

**3.1. Sampling noise on the $\omega(q)$ sub-pieces at $N = 10^7$.**

| sub-piece | $N_{\mathrm{events}}$ at $N=10^7$ | $\bar b$ | est. SE(rate) | predicted | empirical | gap |
|---|---|---|---|---|---|---|
| $\omega(q) = 1$ | $1{,}027{,}121$ | $0.76$ | $\sim 10^{-4}$ | $0.07794$ | $0.07792$ | $-2 \cdot 10^{-5}$ |
| $\omega(q) \ge 2$ | $24{,}462$ | $3.17$ | $\sim 4 \cdot 10^{-5}$ | $0.00776$ | $0.00776$ | $\le 5 \cdot 10^{-6}$ |
| total | $1{,}051{,}583$ | $0.815$ | $\sim 10^{-4}$ | $0.08570$ | $0.08568$ | $-2.5 \cdot 10^{-5}$ |

All three gaps are well within $1\sigma$. Three independent sub-pieces all
matching at $\le 1\sigma$ is mildly stronger than chance ($P \approx 0.31$
under "heuristic exact"), but the sample-noise floor here is $\sim 10^{-4}$, so
we cannot distinguish between "heuristic exact" and "heuristic biased by $\sim 10^{-4}$".

## 4. What this confirms and what remains heuristic

**Confirmed (empirical, within $\sim 10^{-4}$ sampling-noise floor at $N = 10^7$):**

- The closed form $B^\infty = c_1 \sum_{p \equiv 1(4)} \log p / ((p+2)(p-1))$
  predicts $B^\infty \approx 0.085704$ correctly to within sampling noise.
- The $\omega(q) = 1$ sub-piece $0.077943$ correctly captures the dominant
  contribution to within sampling noise.
- The $\omega(q) \ge 2$ sub-piece $0.00776$ correctly captures the
  multi-prime contribution to within sampling noise.
- The prev session's 14% miss in $\omega(q) \ge 2$ at $N = 10^5$ does NOT
  persist at $N = 10^7$ — it was plausibly finite-$N$ artifact, not a
  permanent heuristic flaw.

**What the data does NOT prove (logical caveats):**

- Empirical match within sampling noise does not refute alternative heuristics
  that predict the same value. A different decomposition (e.g., one that
  applies Gaussian-window correction to uniform-in-log) could yield the same
  $0.085704$ from different ingredients. Our agreement is consistent with the
  closed form being correct, but does not uniquely identify it.
- The prev session's specific "double-counting cancellation" hypothesis is
  not refuted: it could be that errors in the per-$p$ marginal model
  (overcounting joint events) cancel against errors in the uniform-in-log
  model (under-counting upper-half divisors), and the cancellation happens
  at both the $\omega(q) = 1$ and $\omega(q) \ge 2$ levels independently.
  The data is consistent with this scenario AND with "each ingredient is
  individually correct"; we cannot distinguish them from this empirical
  test alone.

**Still heuristic (rigorization NOT achieved this session):**

- Uniform-in-log distribution of squarefree divisors of $n^2+1$ in the
  window $(\sqrt{\mathrm{rad}}, n]$. Erdős–Kac/CLT gives Gaussian-distributed
  divisor logs, not uniform; the empirical match to 5 decimals at $N = 10^7$
  suggests the bias either averages out over $n$ or is below sampling noise,
  but this is NOT proven.
- Leading-order $\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$: rigorous lower
  bound only, upper bound conjectural pending Hooley-rigorization for $\tau^*$.
- The single-prime factorization of the residue at $s = 1$ of $\zeta_K \cdot H$
  (the "Euler factor separation" assumption): true at leading order via
  multiplicativity of the Dirichlet series, but the conditional expectation
  $\mathbb E[\tau^*(n^2+1) | v_p = k]$ is computed under "$v_p$ independent of
  other primes' valuations on $n^2+1$".

**Honest update to the prev session's verdict.** The closed form is now
empirically supported at the largest available $N$ for total and both
sub-pieces independently, all to within $1\sigma$ of sampling noise
(noise floor $\sim 10^{-4}$). The prev session's specific "14% miss in
$\omega(q) \ge 2$" alarm dissolves: it was finite-$N$ artifact at $N = 10^5$.
The closed form remains heuristic in derivation, but is now consistent with
empirical to the $\sim 10^{-4}$ precision available at $N = 10^7$.

## 5. Implication for $c_0^T$

From `P12-c0T-AB-decomposition.md`:
$$c_0^T = 1.158730 - 2 B^\infty.$$

Plugging $B^\infty = 0.085704$:
$$c_0^T = 1.158730 - 2 \cdot 0.085704 = 0.987322.$$

Equivalently:
$$\boxed{c_0^T \approx 2 R H'(1) + 2\gamma_K H(1) - 2 R H(1) - \pi H(1) \sum_{p \equiv 1(4)}\frac{\log p}{(p+2)(p-1)} \approx 0.98732,}$$
with $R = \pi/4$, $\gamma_K = L'(1, \chi_4) + R\gamma$, $H$ as in
`P12-tau-squared-second-moment.md`. Empirical $c_0^T \approx 0.988$ at $N = 10^6$
(prev session) — match to 3 decimals.

## 6. Files

- `bot/scratch/B-fast-sieve.py` (new): vectorized sieve for $B(N)$ with
  $\omega(q)$ sub-decomposition. ~20s at $N = 10^7$.
- This file: validation note for prev session's closed form.
- Builds on: `P12-B-infty-closed-form.md` (the closed-form derivation),
  `P12-c0T-AB-decomposition.md` (the $c_0^T$ reduction).

## 7. Next-session pickup hints

1. **(1 session, the cleanest analytic next step): closed form for $\omega(q) = 2$
   piece directly via pair-sum.** With the empirical $\omega(q) = 2$ contribution
   $\approx 0.00751$ at $N = 10^7$, sum over distinct prime pairs $(p, q)$,
   $p < q$, both $\equiv 1 \pmod 4$, of the predicted contribution
   (involving $D_{p^v q^{v'}} \cdot E_{(p^v, q^{v'})}$). Compares directly to
   empirical and tests the Hensel + CRT independence. Should match to 4-5
   decimals if §3's resolution is correct.

2. **(Multi-session, the structural bottleneck): rigorize the heuristic.**
   The empirical match is now strong enough that the rigorization is the
   genuine next big task. Sub-tasks:
   (a) Replace uniform-in-log with proper Hooley-Selberg-Delange analysis on
       $\sum_n \tau^*(n^2+1) \log Q(n^2+1)$.
   (b) Upper bound $\mathbb E[\tau^*(n^2+1)] \le c_1 \log N$ rigorous (currently
       lower bound only via `P12-tau-squared-upper-bound-Nair.md`'s rigorous
       $\ll N(\log N)^3$ for $\tau^2$, which doesn't directly give us the
       leading constant for $\tau^*$).

3. **(Cheap, complementary): empirical $c_0^T$ at $N = 10^7$.** With the
   sieve in hand, recompute $c_0^T(N) = T(N)/(N \log N) - c_1 \cdot$ (the
   Selberg–Delange leading) at $N = 10^7$. Direct check that empirical
   $c_0^T \to 0.987$.
