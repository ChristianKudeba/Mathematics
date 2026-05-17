# P12 — Fourier-orthogonality identity for $\sum_h(|H_h|^2 - D_h)$

## 1. Context and the prev-session hint

Session 2026-05-10 06:51 ($\rho_h$ broad scan) closed with a ranked
"Next-session pickup hint" list. Hint **#1** (highest-EV next analytic
step) read:

> **(1 session, analytic, highest-EV next): rigorize a negative cross-pair
> expectation bound.** The data now triple-confirms $E_h[H_h^2 - D_h] < 0$
> at fixed $N$ (this session) and $\sum_{h \le H}(|H_h|^2 - D_h) < 0$
> cumulative (Halasz-h-averaged). Targeted analytic question: prove
> $\sum_h (H_h^2 - D_h) \le 0$ as a Fourier identity over $h$. This is
> closely related to the orthogonality-of-additive-characters structure
> of $\widetilde S_h$ — see if it falls out cleanly.

This note resolves that question. **Short version: it does NOT fall out
cleanly in the way the hint envisions.** The Cesaro mean is $0$, not
$\le -c$. The empirical negativity at moderate $H$ is a per-$h$
phenomenon, not an $h$-orthogonality phenomenon. The session does
produce one rigorous identity ($R(N, H) \to 1$ as $H \to \infty$ for
fixed $N$), which is a vindication of an EARLIER hypothesis from
`P12-Halasz-h-averaged.md` §4 reading (b) — but that identity does
not bound $|H_h|^2$ at the regime we care about.

## 2. Setup and Fourier expansion

Recall (`Halasz-h-averaged.py`, formula confirmed with `Halasz-Fourier-cesaro.py`):
for sf-good $e$ (squarefree, all prime factors $p = 2$ or $p \equiv 1 \pmod 4$),
$$
\widetilde S_h(e) = \prod_{p \mid e} 2\cos(2\pi h \, a_p^{(e)} / p),
$$
where $a_2^{(e)} := 1/2$ contributes $(-1)^h$, and for odd $p \mid e$
$$
a_p^{(e)} = i_p \cdot (e/p)^{-1} \bmod p,
$$
with $i_p$ a chosen square root of $-1$ mod $p$.

Note that for $p = 2$ both signs $\epsilon_2 \cdot 1/2 \equiv \pm 1/2 \equiv 1/2
\pmod 1$ collapse, so $p=2$ contributes a single character of frequency $1/2$
rather than two characters. Use $2\cos\theta = e^{i\theta} + e^{-i\theta}$ on
the odd-prime factors only:
$$
\widetilde S_h(e) = \sum_{\epsilon \in \{\pm 1\}^{\omega'(e)}}
e^{2\pi i h \, \tilde\alpha_\epsilon(e)},
\qquad
\tilde\alpha_\epsilon(e) := \frac{[2 \mid e]}{2} +
\sum_{\substack{p \mid e \\ p \text{ odd}}} \epsilon_p \, a_p^{(e)} / p
\pmod 1,
$$
where $\omega'(e) := \omega(e) - [2 \mid e]$ counts the odd prime factors.
The expansion of $\widetilde S_h(e)$ thus has $2^{\omega'(e)}$ characters,
not $2^{\omega(e)}$.

Hence
$$
\widetilde S_h(e_1)\,\widetilde S_h(e_2) =
\sum_{\epsilon_1 \in \{\pm 1\}^{\omega'(e_1)}}
\sum_{\epsilon_2 \in \{\pm 1\}^{\omega'(e_2)}}
e^{2\pi i h \, \beta_{\epsilon_1, \epsilon_2}(e_1, e_2)},
\quad
\beta = \tilde\alpha_{\epsilon_1}(e_1) + \tilde\alpha_{\epsilon_2}(e_2)
\pmod 1.
$$

## 3. Lemma F.1 (no-torsion).

**Claim.** For sf-good $e_1, e_2$ with $e_1 \ne e_2$ and any sign vectors
$\epsilon_1 \in \{\pm 1\}^{\omega(e_1)}, \epsilon_2 \in \{\pm 1\}^{\omega(e_2)}$,
$$
\beta_{\epsilon_1, \epsilon_2}(e_1, e_2) \not\equiv 0 \pmod 1.
$$

**Proof.** Write $m = \gcd(e_1, e_2)$, $u_j = e_j / m$, so $\gcd(u_1, u_2) = 1$.
Since $e_1 \ne e_2$, at least one of $u_1, u_2$ is $> 1$; WLOG $u_1 > 1$
(the case $u_2 > 1$ is symmetric).

**Case A:** $u_1$ has an *odd* prime factor $p$. Then $p \nmid e_2$, so
the $p$-component of $\beta$ comes only from $\epsilon_{1,p} a_p^{(1)}/p$,
i.e., $\beta \cdot e_1 e_2 / p \equiv \epsilon_{1,p} a_p^{(1)} \cdot
(e_1 e_2 / p^2) \cdot p \pmod p$ — more cleanly, multiply $\beta$ by the
LCM of all denominators except $p$ (which is coprime to $p$) and reduce
mod $p$: get $\epsilon_{1,p} a_p^{(1)} \cdot c \pmod p$ for some unit $c$,
which is $\not\equiv 0$ since $\epsilon \ne 0$ and $a_p^{(1)} \ne 0$.
Hence $\beta \not\equiv 0 \pmod 1$.

**Case B:** $u_1$ is a power of 2. Then $u_1 = 2$ (since squarefree),
so $2 \mid e_1$ and $2 \nmid e_2$. The $p=2$ contribution to $\beta$ is
$1/2 + 0 = 1/2$ from $\tilde\alpha(e_1)$, $\tilde\alpha(e_2)$. The remaining
contribution is $\sum_{\text{odd } p \mid e_1} \epsilon_{1,p} a_p^{(1)}/p +
\sum_{\text{odd } q \mid e_2} \epsilon_{2,q} a_q^{(2)}/q$, a rational with
ODD denominator $Q$. Thus $\beta = 1/2 + r/Q \pmod 1$ with $Q$ odd. If
$\beta \equiv 0$, then $r/Q \equiv -1/2 \pmod 1$, i.e., $2r \equiv -Q
\pmod{2Q}$, i.e., $2r + Q \equiv 0 \pmod{2Q}$. But $Q$ odd ⇒ $2r + Q$ is
odd, can't be divisible by even $2Q$. Contradiction. $\square$

**Remark.** Lemma F.1 only uses the existence of *some* prime that
appears in exactly one of $e_1, e_2$ — Case A handles odd such primes,
Case B handles $p = 2$. The fact that $a_p^{(e)}$ depends on $e$ when
$p \mid \gcd(e_1, e_2)$ is irrelevant: shared-prime contributions are
never isolated by this argument.

## 4. Theorem F.2 (Cesaro orthogonality).

**Claim.** For each fixed $N \ge 2$,
$$
R(N, H) := \frac{\sum_{h=1}^H |H_h(N)|^2}{\sum_{h=1}^H D_h(N)}
\xrightarrow[H \to \infty]{} 1,
$$
with the explicit upper-bound rate $|R(N, H) - 1| \le C(N) / H$ for an
explicit (finite, $N$-dependent) constant $C(N)$.

**Step 1 (numerator off-diagonal).**
$\sum_h |H_h|^2 - \sum_h D_h = \sum_{h=1}^H \sum_{e_1 \ne e_2}
\widetilde S_h(e_1) \widetilde S_h(e_2)$. Swap sums and expand:
$$
\sum_h \sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde S_h(e_2)
= \sum_{e_1 \ne e_2} \sum_{\epsilon_1, \epsilon_2}
\sum_{h=1}^H e^{2\pi i h \beta(\cdots)}.
$$
By Lemma F.1, every $\beta$ here is nonzero mod $1$. Geometric series:
$$
\left|\sum_{h=1}^H e^{2\pi i h \beta}\right|
\le \frac{1}{|1 - e^{2\pi i \beta}|}
= \frac{1}{2|\sin(\pi\beta)|},
$$
$H$-independent. Hence
$$
\left|\sum_h |H_h|^2 - \sum_h D_h\right|
\le C_{\mathrm{num}}(N) :=
\sum_{e_1 \ne e_2 \le N \text{ sf-good}}
\sum_{\epsilon_1, \epsilon_2}
\frac{1}{2|\sin(\pi \beta)|},
$$
finite (finite sum of finite terms, $\beta \ne 0$ for every term).

**Step 2 (denominator main term, rigorously).**
$D_h(e) = \widetilde S_h(e)^2 = \sum_{\epsilon_1, \epsilon_2}
e^{2\pi i h \gamma_{\epsilon_1, \epsilon_2}(e)}$ where
$\gamma = \tilde\alpha_{\epsilon_1}(e) + \tilde\alpha_{\epsilon_2}(e) \pmod 1$.
The $p=2$ contributions cancel ($1/2 + 1/2 \equiv 0$), so
$$
\gamma_{\epsilon_1, \epsilon_2}(e) =
\sum_{\substack{p \mid e \\ p \text{ odd}}}
(\epsilon_{1,p} + \epsilon_{2,p}) \, a_p^{(e)} / p \pmod 1.
$$
This is $\equiv 0$ iff $\epsilon_{1,p} + \epsilon_{2,p} \equiv 0 \pmod p$
for each odd $p \mid e$, which (since $\epsilon \in \{\pm 1\}$ and $p$ odd)
forces $\epsilon_{2,p} = -\epsilon_{1,p}$. Number of such pairs:
$2^{\omega'(e)}$. For all other pairs ($\gamma \ne 0$), apply the
same geometric-series bound. Hence
$$
\sum_{h=1}^H D_h = H \cdot \sum_{e \le N \text{ sf-good}} 2^{\omega'(e)}
+ R_D(H, N), \quad |R_D| \le C_{\mathrm{den}}(N),
$$
finite. Set $A(N) := \sum_e 2^{\omega'(e)} \ge 1$ (the term $e = 2$
already gives $1$, all others $\ge 1$).

**Step 3 (combine).** For $H \ge 2 C_{\mathrm{den}}(N) / A(N)$,
$\sum_h D_h \ge HA(N)/2 > 0$. Then
$$
|R(N, H) - 1| =
\frac{|\sum_h |H_h|^2 - \sum_h D_h|}{\sum_h D_h}
\le \frac{C_{\mathrm{num}}(N)}{HA(N)/2}
= \frac{2 C_{\mathrm{num}}(N)/A(N)}{H}.
$$
Set $C(N) := 2 C_{\mathrm{num}}(N) / A(N)$. $\square$

**Verification of $A(N)$ from data.** At $N = 20$: sf-good $e \in
\{2, 5, 10, 13, 17\}$ with $\omega' \in \{0, 1, 1, 1, 1\}$, so
$A(20) = 1 + 4 \cdot 2 = 9$. Empirically $\sum_h D_h$ at $H = 10^6$ is
$8.9999 \cdot 10^6 \approx 9H$. ✓ At $N = 50$: $A = 1 + 9 \cdot 2 = 19$,
matching $1.9 \cdot 10^7$. At $N = 100$: $A = 43$, matching $4.3 \cdot 10^7$.

## 5. Empirical verification

Script: `bot/scratch/Halasz-Fourier-cesaro.py`. Computes $R(N, H)$
exactly by summing $\widetilde S_h(e) = \prod 2\cos(\cdots)$ over all
sf-good $e \le N$, vectorized over $h$ in chunks.

| $N$ | sf-good count | primes | $H = 10^2$ | $H = 10^3$ | $H = 10^4$ | $H = 10^5$ | $H = 10^6$ |
|----:|--------------:|:-------|----------:|----------:|----------:|----------:|----------:|
|  10 |  3 | $\{2,5\}$ | $1.000000$ | $1.000000$ | $1.000000$ | $1.000000$ | $1.000000$ |
|  20 |  5 | $\{2,5,13,17\}$ | $0.945970$ | $0.998176$ | $0.999632$ | $0.999962$ | $0.999993$ |
|  50 | 10 | $\{2,5,13,17,29,37,41\}$ | $1.034848$ | $1.004611$ | $0.997825$ | $1.000069$ | $0.999996$ |
| 100 | 20 | $\{2,5,13,17,29,37,41,53,61,73,89,97\}$ | $0.970033$ | $1.033623$ | $1.000840$ | $0.999993$ | $0.999985$ |

(Total wall-clock: $< 1$s.)

**Observations:**
- $R(N, H) \to 1$ is clear at all four $N$ tested.
- The data is *consistent with* $|R - 1| = O_N(1/H)$ (Theorem F.2's bound),
  but does NOT establish $\Theta(1/H)$. For instance at $N = 100$,
  $|R - 1|$ at $H \in \{10^4, 10^5, 10^6\}$ is
  $\{8.4 \cdot 10^{-4}, 6.5 \cdot 10^{-6}, 1.5 \cdot 10^{-5}\}$ —
  non-monotone, with the $H = 10^5$ value below the $H = 10^6$ value.
  This is consistent with $R - 1$ being an oscillatory sum of many
  geometric-series tails, where individual cancellations can briefly
  bring $|R - 1|$ below the $C(N)/H$ envelope before returning to it.
- $R$ oscillates above and below $1$ — sign of $R - 1$ has no systematic
  preference, as the geometric-series bound is two-sided.

The $N = 10$ case ($e \in \{2, 5, 10\}$) has $R = 1$ exactly already at
$H = 100$ because $H = 100$ is a multiple of $\mathrm{lcm} = 10$
(orthogonality is exact over a complete period).

## 6. Strategic reading: hint #1 is misleading.

The prev-session hint suggested that $\sum_h(|H_h|^2 - D_h) \le 0$ might
be a "Fourier identity over $h$ . . . orthogonality of additive characters".
What §4 shows is that the Fourier-orthogonality content is:
$$
\sum_h(|H_h|^2 - D_h) = O_N(1) \quad \text{as } H \to \infty,
\quad N \text{ fixed}.
$$
The Cesaro mean of the off-diagonal is **zero**, not $\le -c$. So
Fourier-orthogonality alone does NOT give a negative bound.

**Where does the empirical negativity come from?** From the per-$h$
fact that $|H_h(N)|^2 \ll D_h(N)$ holds at each individual $h$, in
the regime $H \ll \mathrm{lcm}(\text{primes} \le N)$ — i.e., before the
Cesaro convergence kicks in. Empirically (`P12-Halasz-rho-broad.md`):
median $\rho_h \approx 0.06$, mean $\bar\rho \approx 0.55$ at
$N = 10^7$, so per-$h$ $|H_h|^2 - D_h \approx -0.4 N$, summed over $h \le H$
gives $\approx -0.4 NH$.

These two regimes are sharply different:
- **Pre-Cesaro** ($H \ll \mathrm{lcm}$): $|H_h|^2 \ll D_h$ uniformly,
  $\sum_h(|H_h|^2 - D_h) \approx -0.4 NH$, growing linearly in $H$.
- **Post-Cesaro** ($H \gg \mathrm{lcm}$): $\sum_h(|H_h|^2 - D_h) = O_N(1)$,
  bounded in $H$ at fixed $N$.

The crossover $H = H_*(N)$ is roughly $\mathrm{lcm}(\{p : p \equiv 1 \pmod 4,
p \le N\}) \cdot 2$ — superexponential in $N$ (e.g., $\mathrm{lcm}$ at
$N = 100$ is $\approx 2 \times 10^{17}$). For $H = O(N)$ or
$H = O(N^c)$ for any fixed $c$, we are deep in the pre-Cesaro regime.

**Conclusion**: the strategically-relevant negativity ($H \ll \mathrm{lcm}$)
is per-$h$, equivalent to the strategic goal $|H_h(N)| \ll \sqrt N$. There
is no Fourier-orthogonality shortcut.

## 7. What this DOES vindicate

The previous-prev-session hypothesis from `P12-Halasz-h-averaged.md` §1
was: "averaging over $h$ might cancel the off-diagonal contribution,
giving $\sum_{h=1}^H |H_h(N)|^2 \approx \sum_{h=1}^H D_h(N)$." That note
labeled the hypothesis "wrong-signed" based on data showing $R(N, H)$
decreasing with $N$ at fixed $H$.

**Correction: the hypothesis was correct, but with the wrong limit
direction.** $R(N, H) \to 1$ holds in the $H \to \infty$ limit at fixed
$N$, NOT in the $N \to \infty$ limit at fixed $H$. The earlier note's
empirics were in the wrong limit. Theorem F.2 proves the correct version.

This vindication is rigorously satisfying but strategically hollow:
the "useful" limit (large $N$, moderate $H$) is the OTHER one.

## 8. Rigor accounting

**Rigorous (this note):**
- Lemma F.1: for sf-good $e_1 \ne e_2$, no sign vector gives $\beta \equiv 0$.
- Theorem F.2: $R(N, H) \to 1$ as $H \to \infty$ for fixed $N$, at rate
  $|R - 1| = O_N(1/H)$.
- Constant $C(N)$ in §4 is finite (finite sum) but not effectively bounded
  in $N$ (could be huge; not estimated here).

**Empirical:**
- The $1/H$ rate at $N \in \{10, 20, 50, 100\}$ (5 $H$-values each).
- The "$R$ oscillates above and below 1" qualitative observation.

**Not addressed:**
- Effective bound on $C(N)$ in §4 as a function of $N$.
- Per-$h$ bound on $|H_h(N)|^2$ — the actual strategic goal.
- Anything in the pre-Cesaro regime.

## 9. Strategic implications

1. **Hint #1 from prev-session: the $h$-orthogonality route is closed
   (negative).** Orthogonality of additive characters in $h$ gives
   $\sum_h(|H_h|^2 - D_h) = O_N(1)$ asymptotically (Theorem F.2),
   *not* $\le -c$. So this specific Fourier approach does not yield the
   negative bound the hint asked for. Other Fourier routes (e.g.,
   weighted $h$-sums, Fourier in $e$ instead of $h$, characters mod $q$)
   remain untested and could in principle still give a negative bound.

2. **Per-$h$ cancellation IS the strategic goal.** The empirical
   negativity at moderate $H$ is exactly the strategic question. There
   is no known shortcut via $h$-averaging.

3. **The $H \to \infty$ limit at fixed $N$ is the "wrong" limit.** Future
   sessions should not pursue large-$H$ identities unless they apply
   uniformly in $N$.

4. **Possible spinoff (low-EV but cheap)**: bound $C(N)$ effectively. If
   $C(N) = O(N^{2-\delta})$ for some $\delta > 0$, then for $H = N$ we'd
   get a nontrivial bound on $\sum_{h=1}^N(|H_h|^2 - D_h)$. **Probably
   $C(N)$ is much larger than $N^2$** (small $|\sin(\pi\beta)|$ factors
   for pairs with $\beta$ very close to integers), so this is unlikely to
   pan out. Worth ½-session of empirical $C(N)$ measurement before any
   commitment.

## 10. Files

- `bot/scratch/Halasz-Fourier-cesaro.py` (new): exact computation of
  $R(N, H)$ at small $N$, large $H$.
- `bot/scratch/Halasz-Fourier-cesaro-output.txt` (new): raw output.
- This note (new).
- Builds on / corrects: `P12-Halasz-h-averaged.md` (which had the right
  hypothesis but tested in the wrong limit), `P12-Halasz-rho-broad.md`
  (per-$h$ scan), `P12-Halasz-Dh-diagonal.md` (closed form for $D_h$).
