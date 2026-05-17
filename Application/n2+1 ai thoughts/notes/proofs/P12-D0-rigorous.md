# P12 follow-up: rigorous bounds on the true diagonal $\mathcal{D}_0(N)$

> **Result, this session.**  Let
> $$\mathcal{D}_0(N) \;=\; 4 \sum_{\substack{d \in L_{\mathrm{odd}}\\ d \le 2N}} \sum_{\substack{n_0 \pmod d \\ n_0^2 \equiv -1\,(d)}} \sum_{M=N+1}^{2N} S_{M,d}(n_0)^2,$$
> with $S_{M,d}(n_0) = \sum_{n \equiv n_0 \,(d),\, n \le M} \chi_4(n+1)$ and $L_{\mathrm{odd}} = \{d \ge 1 : p \mid d \Rightarrow p \equiv 1 \,(\mathrm{mod}\, 4)\}$.  Then **rigorously**
> $$\frac{1}{4\pi}\, N^2 + O\!\left(\frac{N^2}{\log N}\right) \;\le\; \mathcal{D}_0(N) \;\le\; \frac{8}{\pi}\, N^2 + O\!\left(\frac{N^2}{\log N}\right),$$
> with explicit closed-form constants.  A sharper upper bound $\mathcal{D}_0(N) \le \tfrac{31}{4\pi} N^2 + O(N^2/\log N) \approx 2.467\,N^2$ follows from a steady-state cutoff at $d = N/4$.  Empirically (previous session) $\mathcal{D}_0(N) \approx 0.747\,N^2$ lies inside the rigorous interval $[0.080\,N^2,\ 2.467\,N^2]$.
>
> **Scope.**  This is a bound on $\mathcal{D}_0$ alone — the diagonal-of-the-diagonal $(n_0 = n_0',\ d = d')$ piece of the AP decomposition.  It does **not** bound the within-$d$ cross-$n_0$ piece $\mathcal{D} - \mathcal{D}_0$ ($\approx 0.24\,N^2$ empirically) nor the cross-$d$ off-diagonal that is the actual obstruction for $\sum_M T(M)^2$.  The constant $1/\pi$ named here is the Selberg–Delange constant for $A(x) = \sum_{d \le x,\,L_{\mathrm{odd}}} 2^{\omega(d)} \sim x/\pi$; it is **not** the asymptotic constant of $\mathcal{D}_0(N)/N^2$ (which is empirically $\approx 0.747 \approx 2.347/\pi$ and is not derived).

This note discharges the next-session pickup hint of `P12-second-moment-diagonal.md` (path 1 in its "Next sessions" list): give a rigorous closed-form bound on $\mathcal{D}_0(N)$ with a named constant.

## 1. The Selberg–Delange constant for $L_{\mathrm{odd}}$

**Lemma 1.** Let $A(x) := \sum_{d \le x,\, d \in L_{\mathrm{odd}}} 2^{\omega(d)}$.  Then $A(x) = x/\pi + O(x/\log x)$, with an explicit power-saving error term of strength $O(x/(\log x)^k)$ for any $k \ge 1$ via Selberg–Delange.

*Proof.*  Form the Dirichlet series
$$F(s) \;:=\; \sum_{d \in L_{\mathrm{odd}}} \frac{2^{\omega(d)}}{d^s} \;=\; \prod_{p \equiv 1\,(4)} \left(1 + \sum_{k \ge 1} \frac{2}{p^{ks}}\right) \;=\; \prod_{p \equiv 1\,(4)} \frac{1 + p^{-s}}{1 - p^{-s}}.$$
Rewrite each Euler factor as $(1 - p^{-2s})/(1-p^{-s})^2$, which gives
$$F(s) \;=\; \prod_{p \equiv 1\,(4)} \frac{1 - p^{-2s}}{(1 - p^{-s})^2}.$$

Compare to $\zeta_K(s) = \zeta(s) L(s, \chi_4)$ for $K = \mathbb{Q}(i)$:
$$\zeta_K(s) \;=\; (1 - 2^{-s})^{-1} \prod_{p \equiv 1\,(4)} (1-p^{-s})^{-2} \prod_{p \equiv 3\,(4)} (1-p^{-2s})^{-1}.$$
Solving for the product over $p \equiv 1\,(4)$ and substituting:
$$F(s) \;=\; \zeta_K(s)\,(1 - 2^{-s}) \prod_{p \equiv 1\,(4)} (1-p^{-2s}) \prod_{p \equiv 3\,(4)} (1-p^{-2s}) \;=\; \frac{\zeta_K(s)\,(1-2^{-s})}{\zeta(2s)\,(1-2^{-2s})}.$$
Using $1 - 2^{-2s} = (1-2^{-s})(1+2^{-s})$:
$$\boxed{\,F(s) \;=\; \frac{\zeta_K(s)}{\zeta(2s)\,(1 + 2^{-s})}\,.\,}$$

The right-hand side is meromorphic on $\Re s > 1/2$.  The pole at $s = 1$ is simple, inherited from $\zeta_K$; by the class-number formula for $K = \mathbb{Q}(i)$ (discriminant $-4$, class number $h_K = 1$, $w_K = 4$ units),
$$\mathrm{Res}_{s=1}\zeta_K(s) \;=\; \frac{2\pi h_K}{w_K \sqrt{|d_K|}} \;=\; \frac{2\pi}{4\cdot 2} \;=\; \frac{\pi}{4}.$$
Substituting $\zeta(2) = \pi^2/6$ and $1 + 2^{-1} = 3/2$:
$$\mathrm{Res}_{s=1} F(s) \;=\; \frac{\pi/4}{(\pi^2/6)(3/2)} \;=\; \frac{\pi/4}{\pi^2/4} \;=\; \frac{1}{\pi}.$$
Furthermore, $\zeta_K(s)$ is non-vanishing on $\Re s = 1$ (Hecke), $\zeta(2s)$ is non-vanishing on $\Re s \ge 1/2$ ($\Re(2s) \ge 1$ is in $\zeta$'s zero-free region), and $1 + 2^{-s}$ has zeros only on $\Re s = 0$.  Hence $F(s) - (1/\pi)/(s-1)$ extends continuously to $\Re s \ge 1$.  By Selberg–Delange (Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory*, Thm.\,II.5.2) with $\kappa = 1$, this gives the *effective* asymptotic
$$A(x) \;=\; \frac{x}{\pi} \;+\; O\!\left(\frac{x}{\log x}\right),$$
and indeed $A(x) = x/\pi + O(x/(\log x)^k)$ for any $k \ge 1$.  $\square$

**Numerical confirmation** (`bot/scratch/verify-selberg-delange.py`):

| $x$ | $A(x)$ | $A(x)/x$ | $1/\pi$ | rel.\,err. |
|---|---|---|---|---|
| $10^3$ | $317$ | $0.3170$ | $0.31831$ | $-0.41\%$ |
| $10^4$ | $3187$ | $0.3187$ | $0.31831$ | $+0.12\%$ |
| $10^5$ | $31\,839$ | $0.31839$ | $0.31831$ | $+0.025\%$ |
| $10^6$ | $318\,279$ | $0.318279$ | $0.31831$ | $-0.010\%$ |

The empirical "0.319" in `P12-second-moment-diagonal.md` is now identified as $1/\pi$ in closed form.

**Corollary 1.** $B(x) := \sum_{d \le x,\, L_{\mathrm{odd}}} d \cdot 2^{\omega(d)} = x^2/(2\pi) + O(x^2/\log x)$.

*Proof.*  Abel summation: $B(x) = x A(x) - \int_1^x A(t)\,dt$.  Substituting $A(t) = t/\pi + r(t)$ with $r(t) = O(t/\log t)$ for $t \ge 2$ (Lemma 1) yields $B(x) = x \cdot (x/\pi + O(x/\log x)) - \int_1^x (t/\pi + O(t/\log t))\,dt = x^2/(2\pi) + O(x^2/\log x)$ using $\int_2^x (t/\log t)\,dt = O(x^2/\log x)$ (standard).  $\square$

## 2. Closed-form $4d$-period count of $S_{M,d}(n_0)^2$

**Lemma 2** (period-4d structure).  Fix $d \in L_{\mathrm{odd}}$ and $n_0$ with $n_0^2 \equiv -1\,(d)$, $1 \le n_0 \le d$.  Set $a_k = n_0 + kd$ for $k \ge 0$.  Then:

(a) $\chi_4(a_k + 1)$ is $4$-periodic in $k$ as a cyclic shift of $(1, 0, -1, 0)$.

(b) $S_{M,d}(n_0)$ is constant on $[a_k, a_{k+1})$ for $k \ge 0$ (and equal to $0$ on $[1, a_0)$).

(c) For $k \ge 0$, $S_{a_k, d}(n_0) \in \{-1, 0, +1\}$, and the multiset $\{S_{a_{4j}, d}, S_{a_{4j+1}, d}, S_{a_{4j+2}, d}, S_{a_{4j+3}, d}\}$ equals $\{0, 0, +1, +1\}$ or $\{0, 0, -1, -1\}$ (depending on the phase set by $n_0 + 1 \bmod 4$).

(d) Consequently, for any integer $A$ with $A \ge n_0 - 1$ (equivalently $A + 1 \ge n_0 = a_0$, so the window $[A+1, A+4d]$ is past the warm-up region $M < n_0$ where $S \equiv 0$),
$$\sum_{M = A+1}^{A + 4d} S_{M,d}(n_0)^2 \;=\; 2d.$$

*Proof.*  Since $d \in L_{\mathrm{odd}}$ is odd, the residues $a_k + 1 = n_0 + 1 + kd \pmod 4$ for $k = 0, 1, 2, 3$ run through all four residue classes mod $4$ (because $\gcd(d, 4) = 1$).  Hence $\chi_4(a_k + 1)$ for $k = 0, 1, 2, 3$ is a permutation of $(1, 0, -1, 0)$, giving (a) and the period-$4$ recurrence $\sum_{k=4j}^{4j+3} \chi_4(a_k+1) = 0$.  Statement (b) is immediate from the definition of $S_{M,d}(n_0)$ as a step function jumping at $M = a_k$.  For (c): using (a), the running partial sum $S_{a_k, d}(n_0) = \sum_{i=0}^{k} \chi_4(a_i + 1)$ takes values that depend on the cyclic shift of $(1, 0, -1, 0)$; the four shifts give running-partial-sums multisets $\{1, 1, 0, 0\}$, $\{0, -1, -1, 0\}$, $\{-1, -1, 0, 0\}$, $\{0, 1, 1, 0\}$, all of which are $\{0, 0, \pm 1, \pm 1\}$ as in (c).

For (d): the function $M \mapsto S_{M,d}(n_0)^2$ is $4d$-periodic on $M \ge n_0$ (by (a)–(c) and the fact that each $4d$-block of $\chi_4(a_k+1)$ sums to $0$, so $s_{4j+i} = s_i$ for all $j \ge 0$).  Hence on $\{M \ge n_0\}$, $S^2$ takes the value $1$ on a set of integer-density exactly $1/2$ (namely, the union of two of every four sub-intervals of length $d$).  For any $A \ge n_0 - 1$ (so $A+1 \ge n_0$), the $4d$ integers in $[A+1, A+4d]$ are entirely past the warm-up; each integer $M$ with $S^2(M) = 1$ contributes $1$.  The total count over a full period $4d$ is exactly $2d$, giving $\sum = 2d$.  $\square$

**Lemma 3** (window bound).  For all $d \in L_{\mathrm{odd}}$, all $n_0$ with $n_0^2 \equiv -1\,(d)$, $1 \le n_0 \le d$, and all $A \ge n_0 - 1$ with $B \ge A$,
$$\sum_{M=A+1}^{B} S_{M,d}(n_0)^2 \;\le\; \frac{B - A}{2} + 2d.$$
Moreover, if $A \ge n_0 - 1$ and $B - A \ge 4d$,
$$\sum_{M=A+1}^{B} S_{M,d}(n_0)^2 \;\ge\; \frac{B - A}{2} - 2d.$$

In particular, both bounds hold uniformly for $A \ge d$ (and trivially the upper bound holds for any $A \ge 0$ since the warm-up region $M < n_0$ contributes $0 \le (B-A)/2 + 2d$).

*Proof.*  Set $q = \lfloor (B-A)/(4d) \rfloor$, $r = (B-A) - 4dq \in [0, 4d)$.  By Lemma 2(d), since $A+1 \ge n_0$, the squared signal $S_{M,d}(n_0)^2$ is $4d$-periodic in $M$ over the entire window $[A+1, B]$, and within each full $4d$-period the count of $M$ with $S^2 = 1$ is exactly $2d$.

*Upper bound.*  The window decomposes into $q$ full $4d$-periods plus a residual of length $r$.  In any consecutive sub-interval of $r < 4d$ integers, the count of $M$ with $S^2 = 1$ is at most $\min(r, 2d)$ (since the full period has $2d$ such positions, and the residual contains at most $\min(r, 2d)$ of them).  Hence
$$\sum_{M=A+1}^{B} S^2 \;\le\; 2dq + \min(r, 2d).$$
Combine with $2dq \le (B-A)/2$ and $\min(r, 2d) \le 2d$:
$$\sum \;\le\; \tfrac{B-A}{2} + 2d.$$

*Lower bound.*  If $B - A \ge 4d$, then $q \ge 1$.  The residual contributes $\ge 0$, so
$$\sum \;\ge\; 2dq \;=\; \tfrac{B-A-r}{2} \;\ge\; \tfrac{B-A}{2} - 2d. \qquad \square$$

## 3. The upper bound on $\mathcal{D}_0(N)$

Write $\rho(d) := 2^{\omega(d)}$ for $d \in L_{\mathrm{odd}}$; this is exactly the number of $n_0 \pmod d$ with $n_0^2 \equiv -1 \pmod d$ (Hensel + CRT, since each prime $p \equiv 1\,(4)$ has 2 lifts and $\rho(p^k) = 2$ for $k \ge 1$).

**Theorem 4** (clean upper bound).  $\mathcal{D}_0(N) \le \dfrac{8}{\pi} N^2 + O(N^2/\log N)$.

*Proof.*  For any $(d, n_0)$ pair with $1 \le n_0 \le d$ and $d \le 2N$, the window $(N, 2N]$ has length $N$ and $|S_{M,d}(n_0)| \le 1$ pointwise (Lemma 2(c) and the warm-up region $S \equiv 0$), so
$$\sum_{M=N+1}^{2N} S_{M,d}(n_0)^2 \;\le\; N.$$
Therefore
$$\mathcal{D}_0(N) \;\le\; 4 \sum_{\substack{d \le 2N \\ d \in L_{\mathrm{odd}}}} \rho(d) \cdot N \;=\; 4N \cdot A(2N) \;=\; 4N \left(\frac{2N}{\pi} + O\!\left(\frac{N}{\log N}\right)\right) \;=\; \frac{8 N^2}{\pi} + O\!\left(\frac{N^2}{\log N}\right). \quad \square$$

**Theorem 5** (sharper upper bound via cutoff).  $\mathcal{D}_0(N) \le \dfrac{31}{4\pi} N^2 + O(N^2/\log N)$.

*Proof.*  Split at $d_* := \lfloor N/4 \rfloor$.

For $d \le d_*$: $n_0 \le d \le N/4 \le N$, so Lemma 3 applies and gives $\sum_{M=N+1}^{2N} S^2 \le N/2 + 2d$.

For $d_* < d \le 2N$: use the trivial bound $\sum_{M=N+1}^{2N} S^2 \le N$.

Hence
$$\frac{\mathcal{D}_0(N)}{4} \;\le\; \sum_{\substack{d \le d_* \\ L_{\mathrm{odd}}}} \rho(d) \left(\tfrac{N}{2} + 2d\right) \;+\; N \!\!\!\!\sum_{\substack{d_* < d \le 2N \\ L_{\mathrm{odd}}}}\!\!\!\! \rho(d) \;=\; \tfrac{N}{2} A(d_*) + 2 B(d_*) + N(A(2N) - A(d_*)).$$
By Lemma 1, Cor.\,1: $A(d_*) = N/(4\pi) + O(N/\log N)$, $B(d_*) = N^2/(32\pi) + O(N^2/\log N)$, $A(2N) = 2N/\pi + O(N/\log N)$.  Substituting:
$$\frac{\mathcal{D}_0(N)}{4} \;\le\; \frac{N^2}{8\pi} + \frac{N^2}{16\pi} + \frac{7 N^2}{4\pi} + O\!\left(\frac{N^2}{\log N}\right).$$
Adding the three rational coefficients with common denominator $16$ gives $31/(16\pi)$, hence $\mathcal{D}_0(N) \le \dfrac{31}{4\pi} N^2 + O(N^2/\log N)$.  $\square$

The cutoff $d_* = N/4$ is optimal in the family $\{N \alpha\}$ for $\alpha \in [0, 1/2]$: the objective $2\alpha^2 - \alpha + 4$ (after factoring out $2N^2/\pi$) is minimised at $\alpha = 1/4$ with value $31/8$.

## 4. The lower bound on $\mathcal{D}_0(N)$

**Theorem 6.**  $\mathcal{D}_0(N) \ge \dfrac{1}{4\pi} N^2 + O(N^2/\log N)$.

*Proof.*  Use only the contribution from $d \le d_* := \lfloor N/4 \rfloor$.  For these $d$: $n_0 \le d \le N/4$, $A = N \ge n_0 - 1$, and $B - A = N \ge 4 d_* \ge 4d$, so Lemma 3's lower bound applies and gives $\sum_{M=N+1}^{2N} S^2 \ge N/2 - 2d$.  All terms in $\mathcal{D}_0$ are $\ge 0$, so dropping $d > d_*$ is legitimate:
$$\frac{\mathcal{D}_0(N)}{4} \;\ge\; \sum_{\substack{d \le d_* \\ L_{\mathrm{odd}}}} \rho(d) \left(\tfrac{N}{2} - 2d\right) \;=\; \tfrac{N}{2} A(d_*) - 2 B(d_*) \;=\; \frac{N^2}{8\pi} - \frac{N^2}{16\pi} + O\!\left(\frac{N^2}{\log N}\right).$$
Hence $\mathcal{D}_0(N) \ge N^2/(4\pi) + O(N^2/\log N)$.  $\square$

## 5. Numerical summary

| quantity | value as $N \to \infty$ | numerical | empirical at $N = 10^4$ |
|---|---|---|---|
| LB (Thm 6) | $N^2/(4\pi)$ | $0.0796\,N^2$ | — |
| **empirical $\mathcal{D}_0(N)/N^2$** | (unknown closed form) | — | $\mathbf{0.7475}$ |
| Sharper UB (Thm 5) | $31\,N^2/(4\pi)$ | $2.4669\,N^2$ | — |
| Clean UB (Thm 4) | $8\,N^2/\pi$ | $2.5465\,N^2$ | — |

So $\mathcal{D}_0(N) = \Theta(N^2)$ is **proved** with explicit constants $1/(4\pi) \le \mathcal{D}_0(N)/N^2 \le 31/(4\pi)$.  The exact asymptotic constant is not derived; empirically it is $\approx 0.747 = 2.347/\pi$.

## 6. What this discharges

* The pickup-hint task in `P12-second-moment-diagonal.md` (path 1).  $\mathcal{D}_0(N)$ now has a **rigorous closed-form upper bound** $\le (8/\pi) N^2 + O(N^2/\log N)$ (or sharper $\le 31\,N^2/(4\pi) + O(N^2/\log N)$), with the named constant $1/\pi$ identified via $\mathrm{Res}_{s=1}\zeta_{\mathbb{Q}(i)}$ and matching lower bound $\ge N^2/(4\pi) + O(N^2/\log N)$.  Error term is effective via Selberg–Delange.
* The strategy hint "diagonal sizes correctly to $\Theta(N^2)$" — for the *true* diagonal $\mathcal{D}_0$, this is now rigorously $\Theta(N^2)$ with both bounds explicit.  The asymptotic constant remains an open empirical refinement.

## 7. What remains open

* **Sharp asymptotic constant** $C^* := \lim_{N\to\infty} \mathcal{D}_0(N)/N^2$ if the limit exists.  Empirically $C^* \approx 0.747 \approx 2.347/\pi$.  Closing the gap from the rigorous interval $[1/(4\pi),\ 31/(4\pi)] \approx [0.080, 2.467]$ requires either a careful averaging over alignments in the regime $d \in (N/4, 2N]$ or a different decomposition (e.g.\ summing over $n_0$ inside and using a Poisson-summation-style identity).
* **The full diagonal $\mathcal{D}(N)$**: the cross-$n_0$ within-$d$ piece $\mathcal{D}(N) - \mathcal{D}_0(N) \approx 0.24\,N^2$ empirically.  To bound this rigorously, need to control $\sum_{n_0 \ne n_0'} \langle S_{\cdot,d}(n_0), S_{\cdot,d}(n_0')\rangle$ — an in-$d$ correlation problem.
* **The cross-$d$ off-diagonal** (the actual obstacle for the second-moment route).  No progress this session; remains the bottleneck.

## 8. Reproducibility

```bash
python bot/scratch/verify-selberg-delange.py 1000000
```
prints $A(x)/x$ for $x \in \{10^3, 10^4, \ldots, 10^6\}$, matching $1/\pi$ to within $0.01\%$ at $x = 10^6$.
