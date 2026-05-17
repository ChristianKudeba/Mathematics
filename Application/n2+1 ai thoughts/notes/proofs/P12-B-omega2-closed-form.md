# P12 — Closed-form heuristic for the $\omega(q)=2$ piece of $B^\infty$

**Session.** 2026-05-07 (third session of the day). Builds on
`P12-B-infty-closed-form.md` (per-prime closed form for total $B^\infty$) and
`P12-B-infty-N1e7-validation.md` (extended empirics to $N = 10^7$).

This note derives a direct closed form for the contribution of $n$ with
$\omega(q) = 2$ (where $q = $ maximum squarefull divisor of $n^2+1$) to
$B^\infty$. It tests the per-pair Hensel–CRT independence hypothesis at the
level of the per-$\omega$ decomposition — independent of the per-prime
$\nu_p^+$ formula.

## 1. Statement

For $n$ with $n^2+1$ non-sf, let $q = $ maximum squarefull divisor (so
$n^2+1 = qk$, $\gcd(q,k)=1$, $k$ sf). The $\omega(q)=2$ piece is
$$B^{(\omega=2)}(N) := \sum_{n \le N: \omega(q)=2} b(n).$$

**FULL closed form** (with global mean correction $G$):
$$B^{(\omega=2),\infty}_{\rm full} \approx c_1 C_0 G \cdot \big[ S_\beta^\sharp \cdot S_\alpha^\sharp - S_{\rm diag}^\sharp\big],$$
where, summing over $p \equiv 1 \pmod 4$,
$$S_\beta^\sharp = \sum_p \frac{\beta(p) \log p}{(1+2/p)\,g_p}, \quad
S_\alpha^\sharp = \sum_p \frac{\alpha(p)}{(1+2/p)\,g_p}, \quad
S_{\rm diag}^\sharp = \sum_p \frac{\alpha(p)\beta(p)\log p}{(1+2/p)^2\, g_p^2},$$
with
$$\alpha(p) := \frac{2}{p^2-2}, \qquad \beta(p) := \frac{2p}{(p-1)(p^2-2)},$$
$$g_p := \frac{1 + 2/p - 4/p^2}{(1-2/p^2)(1+2/p)}, \qquad G := \prod_{p\equiv 1(4)} g_p,$$
$$C_0 := \prod_{p\equiv 1(4)}(1 - 2/p^2), \qquad c_1 := \pi H(1)/2.$$

**Numerical (truncated $p \le 10^6$)**: $B^{(\omega=2),\infty}_{\rm full} \approx 0.0075381$.

**Empirical at $N = 10^7$** (`bot/scratch/B-fast-sieve.py`):
$B^{(\omega=2)}(10^7)/10^7 = 0.0075123$.

**Empirical block-bootstrap SE** (`bot/scratch/B-omega2-variance.py`,
10 blocks of $10^6$): $\mathrm{SE} \approx 5.1 \cdot 10^{-5}$. Per-event
variance is large ($\sigma^2_b \approx 19$, $b \in [0, 57]$), giving
i.i.d. SE upper bound $6.8 \cdot 10^{-5}$ and half-split SE lower bound
$3.8 \cdot 10^{-5}$.

**FULL vs empirical**: gap $= +2.6 \cdot 10^{-5} \approx 0.5\sigma$.
**LEAD vs empirical**: gap $= +2.0 \cdot 10^{-4} \approx 4\sigma$.

The FULL prediction is consistent with empirical at $\sim 0.5\sigma$;
the leading-order LEAD approximation is empirically distinguishable
at $\sim 4\sigma$.

## 2. Derivation

Each $n$ with $\omega(q)=2$ has $q = p_1^{v_1} p_2^{v_2}$ for distinct split
primes $p_1, p_2 \equiv 1 \pmod 4$ and $v_1, v_2 \ge 2$. (Inert primes
$p \equiv 3 \pmod 4$ have $\rho(p)=0$ so cannot divide $n^2+1$. The prime $2$
has $v_2 \le 1$ deterministically since $\rho(4)=0$, so $2 \nmid q$.)

### 2.1 Density $D_q$

By Hensel + CRT independence (rigorous standard input for the leading term):
$$D_q := \mathbb P[\max\text{sqfull}(n^2+1) = q]
= C_0 \cdot a(p_1, v_1) \cdot a(p_2, v_2),$$
where
$$a(p, v) := \frac{2(p-1)}{p^{v+1}(1 - 2/p^2)} \quad\text{for } v \ge 1.$$

Closed forms (verified numerically to $10^{-17}$):
$$\sum_{v\ge 2} a(p, v) = \alpha(p) = \frac{2}{p^2-2}, \qquad
\sum_{v\ge 2}(v-1) a(p, v) = \beta(p) = \frac{2p}{(p-1)(p^2-2)}.$$

### 2.2 Conditional mean of $\tau^*$

Given $\max\text{sqfull} = q = p_1^{v_1} p_2^{v_2}$ (i.e., $v_{p_i}=v_i$ for
$i=1,2$ AND $v_{p'} \le 1$ for all other split primes $p'$), Hensel–CRT
factorization gives heuristically:
$$\mathbb E[\tau^*(n^2+1) \mid \max\text{sqfull}=q]
\approx \tau^*(p_1^{v_1})\tau^*(p_2^{v_2}) \cdot \prod_{p'\ne p_1,p_2}\mathbb E_{p'}[\tau^* \mid v_{p'}\le 1].$$

This factorization treats $\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$ as
literally the product $\prod_p \mathbb E_p[\tau^*]$ — a heuristic identification
of a global asymptotic with an Euler product (same gloss flagged in the prev
session, see `P12-B-infty-closed-form.md` §7(3)).

The inner factor at split $p' \equiv 1 \pmod 4$ is
$$\mathbb E_{p'}[\tau^* \mid v_{p'}\le 1]
= \frac{1\cdot(1-2/p') + 2\cdot(2/p')(1-1/p')}{(1-2/p') + (2/p')(1-1/p')}
= \frac{1 + 2/p' - 4/p'^2}{1 - 2/p'^2}.$$

Defining
$$g_p := \frac{\mathbb E_p[\tau^* \mid v_p \le 1]}{\mathbb E_p[\tau^*]}
= \frac{1 + 2/p - 4/p^2}{(1-2/p^2)(1+2/p)},$$
and using $\mathbb E_p[\tau^*] = 1 + 2/p$, the chain factors as:
$$\mathbb E[\tau^*(n^2+1) \mid \max\text{sqfull}=q]
\approx 4 \cdot \mathbb E[\tau^*(n^2+1)] \cdot \frac{1}{(1+2/p_1)(1+2/p_2)} \cdot \frac{G}{g_{p_1} g_{p_2}}.$$

Inserting $\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$ and
$\log Q = (v_1-1)\log p_1 + (v_2-1)\log p_2$, plus the heuristic
$b(n) \approx \tau^*(n^2+1) \log Q/(4\log n)$ (Hooley uniform-in-log,
P12-B-infty-closed-form.md §3):
$$\mathbb E[b(n) \mid \max\text{sqfull}=q]
\approx c_1 \cdot G \cdot \prod_{i=1,2}\frac{1}{(1+2/p_i)g_{p_i}} \cdot \log Q.$$

(The factor $4$ from $\tau^*(p_1^{v_1})\tau^*(p_2^{v_2}) = 4$ exactly cancels
the $1/(4\log n)$ heuristic factor times $\log N$, leaving prefactor $1$
in front of $\log Q$.)

### 2.3 Summing over $v_1, v_2 \ge 2$

For fixed unordered pair $\{p_1, p_2\}$:
$$\sum_{v_1,v_2\ge 2} D_q \cdot \mathbb E[b\mid q]
= c_1 C_0 G \cdot \frac{\beta(p_1)\alpha(p_2)\log p_1 + \alpha(p_1)\beta(p_2)\log p_2}{(1+2/p_1)(1+2/p_2) g_{p_1} g_{p_2}}.$$

### 2.4 Summing over unordered pairs

The summand is symmetric in $\{p_1, p_2\}$, so summing over unordered pairs
converts to half the ordered sum:
$$B^{(\omega=2),\infty} = \tfrac12 c_1 C_0 G \sum_{p_1 \ne p_2} \frac{\beta(p_1)\alpha(p_2)\log p_1 + \alpha(p_1)\beta(p_2)\log p_2}{(1+2/p_1)(1+2/p_2) g_{p_1} g_{p_2}}.$$

By symmetry the two terms give the same ordered sum, so:
$$B^{(\omega=2),\infty} = c_1 C_0 G \sum_{p_1 \ne p_2} \frac{\beta(p_1)\alpha(p_2)\log p_1}{(1+2/p_1)(1+2/p_2) g_{p_1} g_{p_2}}.$$

The double sum factors via inclusion–exclusion on the diagonal $p_1 = p_2$:
$$B^{(\omega=2),\infty} = c_1 C_0 G \big[ S_\beta^\sharp\,S_\alpha^\sharp - S_{\rm diag}^\sharp\big],$$
with $S_\beta^\sharp, S_\alpha^\sharp, S_{\rm diag}^\sharp$ as in §1.

## 3. Numerical evaluation

`bot/scratch/B-omega2-closed-form.py`, summing primes $p \equiv 1 \pmod 4$
up to $10^6$:

| Quantity | Value |
|---|---|
| $C_0$ | $0.8948412$ |
| $c_1 = \pi H(1)/2$ | $0.8681354$ |
| $G$ | $0.9413205$ |
| $S_\beta$ (lead, $1/(1+2/p)$ weight) | $0.2079471$ |
| $S_\alpha$ (lead) | $0.0872428$ |
| $S_{\rm diag}$ (lead) | $0.0082118$ |
| $S_\beta^\sharp$ (full, $1/((1+2/p)g_p)$ weight) | $0.2131758$ |
| $S_\alpha^\sharp$ (full) | $0.0897824$ |
| $S_{\rm diag}^\sharp$ (full) | $0.0088311$ |
| $B^{(\omega=2),\infty}_{\rm lead}$ | $0.0077141$ |
| $B^{(\omega=2),\infty}_{\rm full}$ | $0.0075381$ |

The LEAD version drops $G/(g_{p_1} g_{p_2}) \to 1$.

## 4. Empirical comparison

`bot/scratch/B-fast-sieve.py` at $N \in \{10^6, 10^7\}$ (per-$\omega(q)$):

| $N$ | $\omega(q) = 1$ | $\omega(q) = 2$ | $\omega(q) = 3$ | $\omega(q) = 4$ |
|---|---|---|---|---|
| $10^6$ | $0.07798$ | $0.00745$ | $0.000247$ | $-$ |
| $10^7$ | $0.07792$ | $0.00751$ | $0.000238$ | $0.000006$ |

**Comparison at $N = 10^7$:**

| Quantity | Empirical | Predicted FULL | Predicted LEAD |
|---|---|---|---|
| $\omega(q)=1$ rate | $0.077923$ | $0.077943$ † | $0.080771$ † |
| $\omega(q)=2$ rate | $0.007512$ | $0.007538$ | $0.007714$ |
| $\omega(q)=3$ rate | $0.000238$ | $\sim 0.000220$ ‡ | $\sim 0.000218$ ‡ |

† From `B-omega1-closed-form.py` (prev session).
‡ Triple-prime sum truncated at $p \le 1000$; full $\omega=3$ FULL is
slightly larger (the truncation is dominated by primes $p \in \{5,13,17,29,...\}$;
adding more primes adds $\sim 10^{-5}$).

### 4.1 Sampling-noise estimate (empirical)

At $N = 10^7$, the count of $\omega=2$ events is $24{,}195$, with per-event
$b$ statistics: mean $3.10$, std $4.39$, var $19.24$, max $57$
(`bot/scratch/B-omega2-variance.py`). Three SE estimates:

- **i.i.d. assumption** ($b(n)$ treated as iid given $\omega=2$):
  SE $= \sqrt{K \cdot \mathrm{var}}/N \approx 6.8 \cdot 10^{-5}$.
- **Half-split** (compare rate on $n \in [1, N/2]$ vs $(N/2, N]$):
  SE $\approx 3.8 \cdot 10^{-5}$ (lower bound, only 1 d.o.f.).
- **10-block bootstrap** (10 blocks of $10^6$):
  SE $\approx 5.1 \cdot 10^{-5}$.

The block estimate is the most defensible — it incorporates both per-event
fluctuation and AP correlation. Quoted $\mathrm{SE} = 5.1 \cdot 10^{-5}$.

### 4.2 FULL vs empirical

$|0.0075381 - 0.0075123| = 2.58 \cdot 10^{-5} \approx 0.5\sigma$. **Within
sampling noise; FULL prediction not distinguishable from empirical.**

### 4.3 LEAD vs empirical

$|0.0077141 - 0.0075123| = 2.02 \cdot 10^{-4} \approx 4.0\sigma$. **Empirically
distinguishable.** The leading-order approximation that drops $G/(g_{p_1}g_{p_2})$
is biased high by $\sim 2\%$ at this resolution.

### 4.4 Finite-$N$ drift caveat

Empirical $\omega(q)=2$ rate at $N = 10^6$: $0.00745$; at $N = 10^7$: $0.00751$.
Drift between the two: $+6 \cdot 10^{-5}$ over a decade. This drift is
comparable to the FULL-vs-empirical gap ($2.6 \cdot 10^{-5}$); convergence to
$0.0075381$ is not yet definitively established. To pin the asymptote
within $\pm 10^{-5}$ would require $N \approx 10^9$ at the same per-decade
drift rate.

## 5. Implications

**1. Pair-level Hensel–CRT independence is empirically supported, with
caveats.** The FULL prediction matches empirical at $\sim 0.5\sigma$,
consistent with no detectable pair-correlation gap. This is the cleanest
direct test to date of pair-level independence in the heuristic.

**2. The prev-prev-session "14% miss" alarm is a finite-$N$ artifact.** At
$N=10^5$, $\omega(q) \ge 2$ was $0.0089$ vs predicted $0.0078$ — flagged as
a possible heuristic flaw. At $N=10^7$, the $\omega=2$ empirical $0.00751$
matches FULL $0.00754$ at $0.5\sigma$; no signal of a genuine cross-correlation
gap remains.

**3. The LEAD vs FULL distinction matters at $N = 10^7$.** At smaller $N$ the
LEAD/FULL gap ($\sim 2\%$) was below sampling noise. At $N = 10^7$ the FULL
prediction beats LEAD by a factor of $\sim 8$ in absolute discrepancy
($2.6 \cdot 10^{-5}$ vs $2.0 \cdot 10^{-4}$). Empirics now require the
global $G$-product correction.

## 6. Caveats

- **Block-bootstrap SE only partially captures correlation.** Events at
  related $n$ (e.g. sharing a prime $p$ via the same arithmetic progression)
  are correlated; a 10-block bootstrap only crudely estimates this. A more
  rigorous SE would require bootstrapping at the prime-AP level. The
  $0.5\sigma$ vs $4\sigma$ comparison is robust to this concern (both gaps
  scale together if the true SE differs by a constant factor).
- **Uniform-in-log heuristic for $b(n)$.** Hooley's assumption that sf
  divisors are uniform in $\log e$ may bias the $\omega=2$ piece differently
  than the $\omega=1$ piece — for $\omega(q)=2$ events, the radical $r$ has
  fewer prime factors and the divisor distribution is more discrete. The
  prev session noted this biases $b(n)$ low pointwise; whether the bias is
  differential across $\omega$ is not analytically resolved here.
- **Hensel–CRT pair independence as $N \to \infty$.** The factorization in
  §2.2 treats $\mathbb E[\tau^*(n^2+1)]$ as a literal Euler product over all
  primes. This identification is heuristic, the same gloss flagged in the
  prev session.
- **$\mathbb E[\tau^*(n^2+1)] \sim c_1 \log N$.** Lower bound rigorous
  (`P12-B3-bdy-leading-constant.md`); upper bound conjectural pending Hooley
  rigorization for $\tau^*$ at $n^2+1$.
- **$\omega = 3$ FULL truncated at $p < 1000$.** The $\sim 0.000220$ figure
  underestimates the true FULL prediction by maybe $10\%$ (smaller-prime
  triples dominate, but the long tail is non-zero). Not used in primary
  comparisons, only in §7.

## 7. Self-consistency: omega-sum vs per-prime-sum

The two heuristic decompositions of $B^\infty$ — by maximum squarefull
$\omega(q)$ vs. by per-prime $\nu_p^+$ — are derived from the same underlying
heuristic factorization (Hensel–CRT independence + Hooley uniform-in-log).
**They should therefore agree numerically up to higher-order corrections;
agreement is internal consistency, not independent evidence for the heuristic.**

Per-prime total: $B^\infty_{\rm total} = c_1 \sum_p \log p / ((p+2)(p-1))
\approx 0.0857038$.

Sum over $\omega$ pieces (FULL throughout):
- $\omega=1$ FULL: $0.077943$
- $\omega=2$ FULL: $0.0075381$
- $\omega=3$ FULL ($p<1000$ truncation): $0.0002148$
- $\omega \ge 4$: bounded by $< 10^{-5}$ (empirically $6 \cdot 10^{-6}$)

Sum $\approx 0.0856959$ vs per-prime $0.0857038$ — agreement to $8 \cdot 10^{-6}$.
(Truncation at $p < 1000$ in $\omega=3$ likely accounts for most of this gap.)

Sum over $\omega$ pieces (LEAD): $0.0807712 + 0.0077141 + 0.0002184 = 0.0887036$,
vs per-prime $0.0857038$ — gap $0.003$. The LEAD approximation breaks the
identity, consistent with the LEAD's empirical bias from §4.

## 8. Files

- `bot/scratch/B-omega2-closed-form.py` (new): closed-form sums for the
  $\omega(q) = 2$ piece, both LEAD and FULL versions; truncated $\omega = 3$
  LEAD and FULL via direct triple loop on $p < 1000$.
- `bot/scratch/B-omega2-variance.py` (new): empirical per-event variance
  and block-bootstrap SE for the $\omega(q)=2$ rate at $N = 10^7$.
- `bot/scratch/B-fast-sieve.py` (existing, prev session): vectorized sieve
  with $\omega(q)$ breakdown.
- This file: closed-form derivation and per-$\omega$ empirical comparison.
- Builds on: `P12-B-infty-closed-form.md` (per-prime total),
  `P12-B-infty-N1e7-validation.md` (sieve infrastructure and $N = 10^7$ data).
