# P12 — Closed-form heuristic for $B^\infty$ via per-prime $\nu_p^+$ decomposition

**Session.** 2026-05-07. Builds on `P12-c0T-AB-decomposition.md` (prev session)
which reduced $c_0^T$ to a single empirical input $B^\infty \approx 0.086$:
$$c_0^T = 1.158730 - 2 B^\infty \quad \text{(rigorous modulo existence of $B^\infty$)}.$$

This note derives a heuristic closed form
$$B^\infty \approx c_1 \sum_{p \equiv 1 \pmod 4} \frac{\log p}{(p+2)(p-1)} \approx 0.08570,$$
where $c_1 = \pi H(1)/2 = 0.86813$. The total agrees with empirical
$B(10^6)/10^6 = 0.0857$ to 4 decimals, but this single-point coincidence is
within the finite-$N$ drift envelope: $B(N)/N$ moves from $0.0880$ at $N = 10^4$
to $0.0857$ at $N = 10^6$, an $O(1/\log N)$-sized residual that exceeds the
4-decimal "match" by an order of magnitude.

**Honest sub-decomposition discrepancy.** The agreement is partly cancellation:
the heuristic's $\omega(q) = 1$ piece matches its empirical analog to 4 decimals
($0.07794$ vs empirical $0.07795$ at $N=10^5$), but the $\omega(q) \ge 2$ piece
shows a $\sim 14\%$ miss ($0.0078$ predicted vs $0.0089$ empirical). The total
reconciles only because the per-$p$ $\nu_p^+$ decomposition double-counts the
joint events $\{v_p \ge 2, v_{p'} \ge 2\}$ in a way that compensates the
$\omega(q) \ge 2$ shortfall. This is the strongest signal that the heuristic
is asymptotically correct in form but currently uncontrolled in error.

The derivation rests on three heuristic inputs (uniform-in-log Hooley
distribution of squarefree divisors; leading-order $\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$;
conditional independence of local prime patterns), so the result is a
suggested asymptotic identity, not a rigorous one.

## 1. The decomposition by maximal squarefull divisor

Recall (prev session):
$$B(N) = \sum_{n \le N,\, n^2+1 \,\mathrm{not\,sf}} \#\{e \,\mathrm{sf}\mid n^2+1 : \sqrt{\mathrm{rad}(n^2+1)} < e \le n\}.$$

Each $n$ with $n^2+1$ non-sf has a unique decomposition $n^2+1 = qk$ where $q$
is squarefull (every $p|q$ has $v_p(q) \ge 2$), $k$ sf, $\gcd(q,k) = 1$.
Equivalently, $q$ is the maximal squarefull divisor of $n^2+1$.

Since $\rho(2^v) = 0$ for $v \ge 2$ ($-1$ is not a QR mod 4), every prime of
$q$ must split in $\mathbb Z[i]$, i.e., be $\equiv 1 \pmod 4$. So the squarefull
parts $q$ that arise have $\mathrm{supp}(q) \subseteq \{p : p \equiv 1 \pmod 4\}$.

**Density of $\{n^2+1 : \max\text{sqfull} = q\}$.** Hensel's lemma gives the
density of $n$ with $v_p(n^2+1) = v$ at fixed split prime $p$ as $(\rho(p)/p^v)(1-1/p) = (2/p^v)(1-1/p)$
for $v \ge 1$, and $1 - 2/p$ for $v = 0$. CRT/independence across distinct primes
$p, p'$ then gives joint distributions. Hence
$$D_q := \mathbb P[\max\text{sqfull}(n^2+1) = q] = C_0 \prod_{p\mid q} \frac{2(1-1/p)}{p^{v_p(q)} (1 - 2/p^2)},$$
where
$$C_0 := \prod_{p\equiv 1(4)} (1 - 2/p^2) \approx 0.89484.$$

The density of non-sf $n^2+1$ is
$$1 - C_0 \approx 0.10516,$$
matching empirical $0.10517$ at $N = 10^5$ (5-decimal agreement).

## 2. Empirical decomposition: aggregate by $\omega(q)$ and per-$q$ contributions

Direct sieve at $N \in \{10^5, 3\cdot 10^5\}$ (`bot/scratch/B-by-sqfull.py`):

**Aggregate by $\omega(q)$ at $N = 3 \cdot 10^5$:**
| $\omega(q)$ | count$/N$ (density) | $\sum b(n)/N$ (contribution to $B^\infty$) |
|---|---|---|
| 1 | $0.10268$ | $0.07795$ |
| 2 | $0.00245$ | $0.00811$ |
| 3 | $0.00004$ | $0.00021$ |
| **Total** | $0.10517$ | $0.08626$ |

**Top per-$q$ contributions at $N = 3 \cdot 10^5$:**
| $q$ | $D_q$ (empirical) | $D_q$ (predicted $\S 1$) | $E_q := B_q/(N D_q)$ |
|---|---|---|---|
| $5^2$ | $0.06220$ | $0.06225$ | $0.484$ |
| $5^3$ | $0.01247$ | $0.01245$ | $1.002$ |
| $13^2$ | $0.00990$ | $0.00989$ | $0.936$ |
| $17^2$ | $0.00587$ | $0.00587$ | $1.046$ |
| $5^4$ | $0.00248$ | $0.00249$ | $1.454$ |
| $29^2$ | $0.00205$ | $0.00206$ | $1.339$ |

**Density agreement.** Empirical $D_q$ matches the analytic formula to 4-5
decimals across all observed $q$.

**Conditional means $E_q$.** These do NOT match a single uniform value;
instead they depend on $q$ in a structured way. The per-$p^v$ values cluster
around $0.5(v-1) M_p \log p$ for an effective $M_p \to 2p/(p+2)$ (see §3).

## 3. Heuristic for $b(n)$ via uniform-in-log

For non-sf $n^2+1$ with radical $r = \mathrm{rad}(n^2+1)$ and squarefull excess
$Q = (n^2+1)/r$:

$b(n) = \#\{\text{sf divisors of } r \text{ in } (\sqrt r, n]\}$ where
$n \approx \sqrt{rQ}$, so the window has log-width $\frac{1}{2}\log Q$.

**Hooley uniform-in-log assumption.** Among the $\tau^*(m) = 2^{\omega(m)}$ sf
divisors of $m$, the ones in a log-interval of width $w$ centered anywhere
in $[0, \log m]$ count (asymptotically, after averaging in $n$) like
$\tau^*(m) w/\log m$.

Hence
$$b(n) \approx \tau^*(n^2+1) \cdot \frac{(1/2)\log Q(n^2+1)}{\log(n^2+1)} = \frac{\tau^*(n^2+1) \log Q(n^2+1)}{4 \log n}.$$

Summing over $n \le N$ and averaging $\log n \approx \log N$:
$$B(N) \approx \frac{1}{4 \log N} \sum_{n \le N} \tau^*(n^2+1) \log Q(n^2+1).$$

## 4. Per-prime decomposition of the inner sum

Decompose $\log Q(m) = \sum_p \nu_p^+(m) \log p$, where
$\nu_p^+(m) := \max(v_p(m) - 1, 0)$. Then
$$\sum_{n \le N} \tau^*(n^2+1) \log Q(n^2+1) = \sum_p \log p \sum_{n\le N} \tau^*(n^2+1) \nu_p^+(n^2+1).$$

**Inner sum at fixed split prime $p \equiv 1 \pmod 4$.** Using:
- $\mathbb P[v_p(n^2+1) = k] = (2/p^k)(1 - 1/p)$ for $k \ge 1$ (Hensel + independence),
- $\mathbb E[\tau^*(n^2+1) \mid v_p = k] = \tau^*(p^k) \prod_{p'\ne p}\mathbb E[\tau^*(p'^{v_{p'}})] = 2 \cdot \mathbb E[\tau^*(n^2+1)]/(1+2/p)$ for $k\ge 1$
  (since the local mean $\mathbb E_{p}[\tau^*] = 1 + 2/p$ at split $p$),
- $\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$ (rigorous lower bound, conjectural upper bound — see prev sessions),

we get:
$$\sum_n \tau^*(n^2+1) \nu_p^+(n^2+1) \sim N c_1 \log N \cdot \frac{2p}{p+2} \cdot \sum_{k \ge 2} (k-1) \cdot \frac{2(1-1/p)}{p^k}.$$

The sum $\sum_{k\ge 2}(k-1)/p^k = (1/p^2)/(1-1/p)^2 = 1/(p-1)^2$.

So the per-$p$ contribution is
$$N c_1 \log N \cdot \frac{2p}{p+2} \cdot \frac{2(p-1)/p}{(p-1)^2} = N c_1 \log N \cdot \frac{4}{(p+2)(p-1)}.$$

## 5. Closed form for $B^\infty$

Summing over $p \equiv 1 \pmod 4$:
$$\sum_n \tau^*(n^2+1) \log Q(n^2+1) \sim 4 N c_1 \log N \sum_{p \equiv 1(4)} \frac{\log p}{(p+2)(p-1)}.$$

Plugging into §3:
$$\boxed{B^\infty \approx c_1 \sum_{p \equiv 1 \pmod 4} \frac{\log p}{(p+2)(p-1)}.}$$

**Numerical.** Computing the sum to $p \le 10^7$ (`bot/scratch/B-total-closed-form.py`):
$$\sum_{p \equiv 1(4)} \frac{\log p}{(p+2)(p-1)} = 0.098722,$$
giving $B^\infty \approx 0.86813 \cdot 0.098722 = 0.085704$.

**Empirical comparison:**
| $N$ | $B(N)/N$ | predicted $0.08570$ | abs diff |
|---|---|---|---|
| $10^4$ | $0.0880$ | $0.0857$ | $+0.0023$ |
| $3\cdot 10^4$ | $0.0859$ | $0.0857$ | $+0.0002$ |
| $10^5$ | $0.0867$ | $0.0857$ | $+0.0010$ |
| $3 \cdot 10^5$ | $0.0863$ | $0.0857$ | $+0.0006$ |
| $10^6$ | $0.0857$ | $0.0857$ | $0.0000$ |

Match at $N = 10^6$ is to 4 decimals (3 zeros after decimal). The drift from
$0.0880$ at $N = 10^4$ to $0.0857$ at $N = 10^6$ is consistent with a
decreasing approach to the predicted limit.

## 6. Combined: closed-form $c_0^T$

From `P12-c0T-AB-decomposition.md`:
$$c_0^T = 2(c_<^\infty - A^\infty - B^\infty) = 1.158730 - 2 B^\infty.$$

Plugging the heuristic closed form:
$$c_0^T \approx 1.158730 - 2 \cdot 0.085704 = 0.987322.$$

Empirical at $N = 10^6$: $c_0^T \approx 0.988$. **Closed-form prediction matches
empirical to 3 decimals.**

Equivalently, in symbolic form:
$$c_0^T \approx 2 R H'(1) + 2\gamma_K H(1) - 2 R H(1) - \pi H(1) \sum_{p \equiv 1(4)}\frac{\log p}{(p+2)(p-1)}.$$

## 7. Rigor status and skeptical assessment

**What is rigorous.**
- Density formula for $D_q$: rigorous given Hensel + CRT (standard, no
  approximation).
- Identification $\log Q(m) = \sum_p \nu_p^+(m) \log p$: exact identity.
- Algebraic identity $\sum_{k \ge 2}(k-1)/p^k = 1/(p-1)^2$: verified.

**Heuristic ingredients.**

1. **Uniform-in-log distribution of sf divisors.** The Hooley assumption
   "sf divisors of $r$ are uniform in $\log e/\log r$" is the dominant
   uncontrolled error. Erdős–Kac/CLT says the divisor logs are
   *Gaussian*-distributed with mean $\frac{1}{2}\log r$ and variance
   $\frac{1}{4}\sum_{p|r}(\log p)^2$, NOT uniform. The window of interest
   $(\sqrt r, n] = (\sqrt r, \sqrt{rQ}]$ sits in the *upper half*, with its
   lower endpoint exactly at the Gaussian mean — the densest part of the
   distribution, where uniform-in-log under-counts. So the heuristic biases
   $b(n)$ low pointwise; the average over $n$ may compensate, but this is
   not justified here.

2. **Leading-order $\mathbb E[\tau^*(n^2+1)] = c_1 \log N$.** Rigorous lower
   bound only (`P12-B3-bdy-leading-constant.md`); upper bound conjectural
   pending the Hooley-rigorization for $\tau^*$.

3. **Pulling out a single $p$-factor from $\mathbb E[\tau^*]$.**
   The identity $\mathbb E[\tau^*(n^2+1) | v_p = k] = 2 \mathbb E[\tau^*(n^2+1)]/(1+2/p)$
   (for $k \ge 1$) treats $\tau^*$ as a multiplicative product over primes
   with independent local distributions. While this is morally correct in
   the Hensel/CRT model, $\mathbb E[\tau^*(n^2+1)]$ itself is a *global*
   asymptotic governed by $\zeta_K$'s simple pole; the single-prime
   factorization assumes the residue at $s = 1$ separates cleanly across
   Euler factors — true to leading order but glossed.

4. **Cross-correlation between primes (the $\omega(q) \ge 2$ piece).**
   The $\nu_p^+$ decomposition is an exact identity at the level of
   $\log Q(m)$, but the inner sum $\sum_n \tau^*(n^2+1) \nu_p^+(n^2+1)$ is
   evaluated under "$v_p$ is independent of other primes" — which produces
   the leading-order $4/((p+2)(p-1))$ factor. The empirical check at $N = 10^5$
   shows: $\omega(q) = 1$ matches predicted to 4 decimals ($0.07794$ vs
   $0.07795$), but $\omega(q) \ge 2$ shows $0.0089$ empirical vs $0.0078$
   predicted — a $\sim 14\%$ miss. The total $0.0857$ matches because the
   per-$p$ sum ALSO over-counts joint events $\{v_p \ge 2, v_{p'} \ge 2\}$
   (each such event contributes to BOTH the $p$-sum and the $p'$-sum),
   and the over-count happens to cancel the under-count from the $\omega \ge 2$
   miss. This is a non-trivial reconciliation that is not analytically
   verified here.

5. **Finite-$N$ drift in empirical $B(N)/N$.** The drift
   $0.0880 \to 0.0857$ across $N \in [10^4, 10^6]$ is of size $0.0023$,
   roughly 5x the predicted-vs-empirical gap at $N = 10^6$. With finite-$N$
   correction estimated as $O(1/\log N) \approx 0.005$, the 4-decimal match
   at $N = 10^6$ is *within finite-$N$ noise*, not strong evidence for the
   closed form being exact.

**Empirical evidence for the heuristic, sober assessment.**
- $\omega(q) = 1$: predicted $0.07794$ matches empirical $0.07795$ at $N=10^5$
  to 4 decimals — strong.
- $\omega(q) \ge 2$: predicted $0.0078$ vs empirical $0.0089$ at $N = 10^5$
  — 14% miss.
- Total: predicted $0.0857$ vs empirical $0.0857$ at $N = 10^6$ —
  apparent 4-decimal match, but partly via cancellation between (3) and (4)
  and partly via favorable finite-$N$ alignment.
- Per-$q$ density formula matches empirical to 4-5 decimals — strong.

**Honest verdict.** The closed form is the *natural leading-order* prediction
under standard heuristic assumptions. It is qualitatively correct and
quantitatively close (within $\sim 5\%$), but the coincidental 4-decimal
total agreement at $N = 10^6$ does NOT rigorously justify the heuristic.
The $\omega(q) \ge 2$ 14% miss is the cleanest signal that the heuristic is
not exact. The next session should:
(a) Compute the $\omega(q) \ge 2$ piece more carefully — analytically or
    by extending empirical $B$ to $N = 10^7$ to test whether the residual is
    finite-$N$ artifact or genuine constant.
(b) Replace uniform-in-log with proper Hooley-Selberg-Delange asymptotics
    on $\sum_n \tau^*(n^2+1) \log Q(n^2+1)$.
(c) Rigorize the upper bound of $\mathbb E[\tau^*(n^2+1)] \le c_1 \log N$.

## 8. Files

- `bot/scratch/B-by-sqfull.py` (new): empirical decomposition of $B(N)$ by
  maximal squarefull divisor $q$, with predicted $D_q$ comparison.
- `bot/scratch/B-omega1-closed-form.py` (new): closed-form sum for
  $B^\infty_{\omega(q)=1}$, matches empirical $0.0779$.
- `bot/scratch/B-total-closed-form.py` (new): closed-form sum for full
  $B^\infty$ via $\nu_p^+$ decomposition, matches empirical $0.0857$.
- This file: full proof note with derivation and rigor analysis.
- Builds on: `P12-c0T-AB-decomposition.md` (prev session reduction of $c_0^T$).
