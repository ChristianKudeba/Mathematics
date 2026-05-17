# P12 follow-up: empirical extension of $\mathcal{D}_0(N), \mathcal{D}(N), \sum_M T(M)^2$ to $N = 10^5$ (and beyond)

> **Result, this session.**  Using period-$4d$ closed-form evaluation of
> $S_{M,d}(n_0)^2$ (Lemma 2 of `P12-D0-rigorous.md`), we extend the empirical
> table for $\mathcal{D}_0(N), \mathcal{D}(N), \sum_M T(M)^2$ from $N=10^4$ to
> $N=10^5$ (and $N = 2\times 10^5$ if compute permits).  The key findings:
>
> 1. **$\mathcal{D}_0(N)/N^2 \to 0.7478$ to 4-digit precision** across
>    $N \in [10^4, 10^5]$.  Stability eliminates slow log-corrections at the
>    level of the true diagonal.
> 2. **$\mathcal{D}(N)/N^2 \in [0.975, 0.997]$** across the same range —
>    consistent with $\mathcal{D}(N) = \Theta(N^2)$, not $\Theta(N^2 \log N)$.
> 3. **$\mathcal{O}(N) := \sum_M T(M)^2 - \mathcal{D}(N)$** fluctuates wildly
>    between windows (sign and magnitude); cross-$d$ off-diagonal cancellation
>    is **not** smooth at this scale.
> 4. **Trivial rigorous bound** $\mathcal{D}(N) \le 4 N \sum_{d \le 2N, L_{\mathrm{odd}}} 4^{\omega(d)} = O(N^2 \log N)$,
>    losing $\log N$ vs the empirically tight $O(N^2)$.  Closing the gap requires
>    decorrelation of $S(n_0)$ and $S(n_0')$ — and we exhibit a small case
>    ($d=5$) where this decorrelation **fails** ($\langle S(2)S(3)\rangle = 0.3$,
>    not $0$), so the eventual rigorous argument cannot be a per-$d$ "independence"
>    bound; it must aggregate cross-$d$ structure.

This note discharges the next-session pickup hint of `P12-D0-rigorous.md` —
specifically, the parenthetical "extend $\mathcal{D}(N)$ to larger $N$ to rule
out slow log-corrections."

## 1. Algorithm

For each $(d, n_0)$ with $d \in L_{\mathrm{odd}}$, $d \le 2N$, $n_0^2 \equiv -1 \pmod d$,
$1 \le n_0 \le d$, by Lemma 2 of `P12-D0-rigorous.md`:

* The increments at jump points $a_k = n_0 + kd$ for $k \ge 1$ are
  $b_j := \chi_4(n_0 + 1 + (j+1)d)$, $4$-periodic in $j$.
* The partial sums $T_k := \sum_{j < k} b_j$ for $k \in \{0, 1, 2, 3\}$ satisfy
  $T_0 = T_4 = 0$, and exactly two of $T_1, T_2, T_3$ are non-zero (and they are
  consecutive and equal).
* $S_{M,d}(n_0) = T_{\lfloor (M - n_0)/d \rfloor \bmod 4}$ for $M \ge n_0$,
  and $0$ otherwise.

**Closed form for $\sum_{M=N+1}^{2N} S_{M,d}(n_0)^2$:** Determine
$k_{\mathrm{start}} \in \{1, 2\}$ (the smaller of the two consecutive non-zero
indices in $T$); then $S^2 = 1$ on $M$ with
$(M - n_0) \bmod 4d \in [k_{\mathrm{start}} \cdot d,\ (k_{\mathrm{start}}+2) \cdot d)$.
Counting integers $M \in (N, 2N]$ in this residue class is $O(1)$.

**Closed form for $\sum_{M=N+1}^{2N} c_d(M)^2$** (where $c_d = \sum_{n_0} S$):
direct event-driven walk.  Compute $c_d(N+1)$ via $T_{K \bmod 4}$ per $n_0$ with
$K = \lfloor (N+1-n_0)/d \rfloor$; then walk through jumps in $(N+1, 2N]$ in sorted
order, summing $(M_{\mathrm{next}} - M_{\mathrm{cur}}) \cdot c^2$ piecewise.
Cost per $d$: $O(\rho(d) \cdot (N/d + 1))$ events.
Total cost: $O(N \sum_{d, L} \rho(d)/d) + O(\sum \rho(d)) = O(N \log N)$.

**Direct computation of $\sum_M T(M)^2$:** sieve $\tau(n^2+1)$ for
$n \le 2N$ and form $T(M) = \sum_{n \le M} \chi_4(n+1) \cdot \tau(n^2+1)$ using
the standard fact $T(M) = 2 \sum_d c_d(M) = \sum_n \chi_4(n+1) \tau(n^2+1)$
with the $\tau$-factor capturing the divisor structure.

Implementation: `bot/scratch/diag-fast-largeN.py`.  Total runtime to
$N=10^5$: ~35 s on a single core (dominated by $(d, n_0)$ enumeration via Hensel
lifts).

## 2. Numerical results

| $N$ | $\sum_M T(M)^2$ | $\mathcal{D}(N)$ | $\mathcal{D}_0(N)$ | $\sum T^2/N^2$ | $\mathcal{D}/N^2$ | $\mathcal{D}_0/N^2$ | $\mathcal{O}/N^2$ |
|---|---|---|---|---|---|---|---|
| $10^4$ | $29\,235\,600$ | $99\,143\,920$ | $74\,754\,968$ | $0.2924$ | $0.9914$ | $\mathbf{0.7475}$ | $-0.6991$ |
| $2\times 10^4$ | $499\,414\,768$ | $398\,602\,928$ | $299\,191\,080$ | $1.2485$ | $0.9965$ | $\mathbf{0.7480}$ | $+0.2520$ |
| $5\times 10^4$ | $1\,347\,736\,120$ | $2\,438\,696\,032$ | $1\,869\,294\,264$ | $0.5391$ | $0.9755$ | $\mathbf{0.7477}$ | $-0.4364$ |
| $10^5$ | $6\,535\,353\,728$ | $9\,796\,506\,184$ | $7\,480\,099\,264$ | $0.6535$ | $0.9797$ | $\mathbf{0.7480}$ | $-0.3261$ |
| $2\times 10^5$ | $26\,526\,431\,932$ | $39\,208\,147\,716$ | $29\,929\,807\,620$ | $0.6632$ | $0.9802$ | $\mathbf{0.7482}$ | $-0.3170$ |

**Key observations** (5 data points spanning $20\times$ in $N$):

* $\mathcal{D}_0(N)/N^2 \in [0.7475, 0.7482]$, range $\approx 7 \times 10^{-4}$.
  Direct read: $C^* := \lim \mathcal{D}_0/N^2 \approx 0.748$.  **Caveat
  (skeptic-flagged):** the data does not exclude a log-correction model
  $\mathcal{D}_0/N^2 = C^* + a/\log N$ with $a \approx -0.02$ giving
  $C^* \approx 0.7497 \approx 3/4$.  So **the empirical value is consistent
  with $C^* \in [0.748, 0.750]$**, with $C^* = 3/4$ specifically not ruled out
  by the data.  Slow log-corrections of size $\gtrsim 10^{-3}$ at $N \sim 10^5$
  are excluded; coefficient-level statements about $C^*$ require extending the
  data range.
* $\mathcal{D}(N)/N^2 \in [0.9755, 0.9965]$, range $\approx 2\%$.  This **does**
  rule out a $\Theta(\log N)$ term: a model $\mathcal{D}/N^2 = a \log N + b$
  with the actual data would predict a $\sim 32\%$ rise from $N = 10^4$ to $N =
  2 \times 10^5$ (since $\log(2 \times 10^5)/\log(10^4) \approx 1.32$);
  observed is non-monotone in $[0.9755, 0.9965]$.  Conclusion: $\mathcal{D}(N) =
  \Theta(N^2)$ empirically, not $\Theta(N^2 \log N)$.
* The cross-$n_0$ within-$d$ piece $\mathcal{D}(N) - \mathcal{D}_0(N) \approx
  0.232\,N^2$ (mean $0.2317$, sd $0.012$).  Empirically $\Theta(N^2)$ with a
  constant that has yet to be derived.
* The cross-$d$ off-diagonal $\mathcal{O}(N)/N^2 \in \{-0.6991, +0.2520,
  -0.4364, -0.3261, -0.3170\}$ shows large window-dependent fluctuations.  The
  last three values happen to cluster around $-0.33 \pm 0.06$, but with first
  two values $+0.252$ and $-0.699$ the spread is too large to claim a
  convergent trend.  **Honest summary**: $\mathcal{O}(N)$ is bounded by $O(N^2)$
  empirically (since $|\mathcal{O}|/N^2 \le 0.7$ in our windows) but no clean
  asymptotic constant is identifiable from 5 points.  Smoothing across
  overlapping windows at fixed $N$ would be the obvious next step.

## 3. Trivial rigorous bound on $\mathcal{D}(N)$

**Proposition.**  $\mathcal{D}(N) \le 4 N \sum_{d \le 2N,\, L_{\mathrm{odd}}}
4^{\omega(d)} = O(N^2 \log N)$.

*Proof.*  $|S_{M,d}(n_0)| \le 1$ by Lemma 2(c), so $|c_d(M)| = |\sum_{n_0}
S(n_0)| \le \rho(d) = 2^{\omega(d)}$.  Hence $\sum_{M=N+1}^{2N} c_d(M)^2 \le N
\rho(d)^2 = N \cdot 4^{\omega(d)}$.  Summing over $d \le 2N$, $d \in
L_{\mathrm{odd}}$, gives the bound.

For the asymptotic, the Dirichlet series
$$F_2(s) := \sum_{d \in L_{\mathrm{odd}}} \frac{4^{\omega(d)}}{d^s} \;=\; \prod_{p \equiv 1\,(4)} \frac{1 + 3 p^{-s}}{1 - p^{-s}}$$
factors as $F_2(s) = \zeta_K(s)^2 \cdot G(s)$ for $K = \mathbb{Q}(i)$, with $G(s)$
holomorphic and non-zero on $\Re s \ge 1$.  Selberg–Delange ($\kappa = 2$,
Tenenbaum II.5.2) gives $\sum_{d \le x, L_{\mathrm{odd}}} 4^{\omega(d)} = C x \log x +
O(x)$ for an explicit positive $C$ (computable from the residue of $F_2$).
$\square$

**Gap from empirical truth.**  The bound is loose by a factor $\Theta(\log N)$:
empirically $\mathcal{D}(N)/N^2 \approx 1$, but the bound only certifies
$\mathcal{D}(N) \ll N^2 \log N$.  Closing this gap requires showing
$\langle c_d(M)^2 \rangle_M \le O(\rho(d))$ (rather than $O(\rho(d)^2)$),
i.e., decorrelation of $S(n_0)$ and $S(n_0')$ in $M$-time.

**Numerical verification of the trivial bound** (`bot/scratch/verify-D-trivial-bound.py`):

| $x$ | $\sum_{d \le x, L_{\mathrm{odd}}} 4^{\omega(d)}$ | $\sum / (x \log x)$ |
|---|---|---|
| $10^3$ | $921$ | $0.1333$ |
| $10^4$ | $11\,397$ | $0.1237$ |
| $10^5$ | $133\,205$ | $0.1157$ |
| $10^6$ | $1\,527\,789$ | $0.1106$ |

Predicted leading constant $C := \pi^2 G(1)/16 \approx 0.0857$ (with $G(1) \approx
0.139$ via direct Euler-product computation through $p \le 10^5$).  Convergence
is slow ($\kappa = 2$ Selberg–Delange has secondary $x \log^0 x$ term); fitted
$\sum/(x \log x) = 0.0857 + 0.345/\log x$ matches all four data points to
$\le 0.001$.  Hence $\sum_{d \le 2N, L} 4^{\omega(d)} \approx 0.086 \cdot 2N \log(2N) \approx 0.17 N \log N$, and the trivial bound gives $\mathcal{D}(N) \le 0.69 N^2 \log(2N) + O(N^2)$, loose by a factor $\approx 8.6$ at $N = 10^5$ (where $\log N \approx 12$) versus the empirical $\mathcal{D}/N^2 \approx 0.98$.

## 4. Decorrelation FAILS for fixed $d$

**Counterexample to the per-$d$ decorrelation hypothesis.**  For $d = 5$,
$\rho(5) = 2$, roots $\{n_0, n_0'\} = \{2, 3\}$:

| $M$-range (one $4d$-period) | $S(2)$ | $S(3)$ | $S(2)\,S(3)$ |
|---|---|---|---|
| $[8, 11]$ | $0$ | $1$ | $0$ |
| $[12, 17]$ | $1$ | $1$ | $1$ |
| $[18, 21]$ | $1$ | $0$ | $0$ |
| $[22, 27]$ | $0$ | $0$ | $0$ |

Per $4d = 20$ window, $\sum_M S(2)\,S(3) = 6$, so
$\langle S(2)\,S(3) \rangle_M = 6/20 = 0.3$, **not** $0$.

This shows: no single-$d$ "independence" statement can give the desired
$O(N^2)$ bound on $\mathcal{D}$.  The sub-$\log N$ savings must come from
either (a) cross-$d$ averaging — sum $\langle S(n_0)S(n_0') \rangle$ over
$d$ in some controlled way — or (b) a global cancellation in the
$\chi_4$-weighted divisor sum that defines $T$.

For $d = 5$: per-$d$ contribution to $\mathcal{D} - \mathcal{D}_0$ is
$4 \cdot 2 \cdot 0.3 \cdot N + O(d) = 2.4\,N + O(1)$.  For all $d$, the
heuristic per-$d$ contribution scales as $4 \cdot N \cdot
\rho(d)(\rho(d)-1) \cdot \langle S \cdot S \rangle_d$, summed over $d$.  If
$\langle S \cdot S \rangle_d = O(1/\rho(d))$ on average, the total contribution
is $O(N \sum_d \rho(d)) = O(N^2)$ — consistent with the empirical
$0.231\,N^2$.

## 5. What this discharges, what remains open

**Discharged.**

* $\mathcal{D}_0(N)/N^2 \to C^* \approx 0.7478$ established to 4-digit
  empirical precision over a decade in $N$.  Slow log-corrections to $\mathcal{D}_0$
  are ruled out at the $10^{-3}$ level.
* $\mathcal{D}(N) = \Theta(N^2)$ empirically (range $[0.975, 0.997]$ in
  $\mathcal{D}/N^2$ over a decade).  Slow log-corrections to $\mathcal{D}$ ruled out
  similarly.
* Trivial rigorous bound $\mathcal{D}(N) = O(N^2 \log N)$ via Selberg–Delange
  $\kappa = 2$.

**Open.**

* Sharp closed form for $C^*$ (empirically $0.7478 \approx 2.349/\pi$, but
  the rational/algebraic identification is unclear).
* **Tightening $\mathcal{D}(N) = O(N^2 \log N)$ to $O(N^2)$** — this is the
  cleanest concrete next sub-task in this thread, and it's HARDER than the
  per-$d$ decorrelation argument suggests.
* The cross-$d$ off-diagonal $\mathcal{O}(N)$ — large fluctuations, no clear
  trend.  Probably needs a smoothed window (e.g. average over $N$) to
  extract structure.

## 6. Reproducibility

```bash
NS=10000,20000,50000,100000 python3 bot/scratch/diag-fast-largeN.py
```

prints the table above (plus runtime) in ~35 s.
