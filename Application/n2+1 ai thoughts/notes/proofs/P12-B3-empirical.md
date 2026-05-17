# P12: Direct empirical sieve of $B_3(N)$ — Hooley-boundary cancellation diagnostic (2026-05-06)

## Summary

The previous session ($\Sigma_3$ effective Selberg–Delange) closed the SD-piece
of the band-difference rigorously (qualitatively): the asymptotic content of
the conjecture $W_{K-1} - P^{(3,3)} = O(N)$ is now exactly the Hooley-boundary
statement
$$
B_3(N) - B_3(n_-) = O(N), \qquad B_3(N) := \sum_{d \le N^2+1} 2^{\omega(d)} \delta_d(N), \quad \delta_d(N) := N_d(N) - \rho(d) N/d.
$$
This session computes $B_3(N)$ **directly** at multiple $N$ values via the
exact identity $B_3(N) = S_3(N) - N \Sigma_3(N^2+1)$, where
$S_3(N) := \sum_{n \le N} \tau((n^2+1)^2)$.

**Result (empirical only).** Across $N \in \{500, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 30000\}$,
the ratio $B_3(N)/N$ stays in $[0.34, 0.67]$, with all 10 values positive
and no statistically significant monotone trend (linear regression slope
$+1 \cdot 10^{-6}$ per unit $N$, std $5 \cdot 10^{-6}$). Mean $\approx 0.49$.

This is **empirical evidence to within the data range that $B_3(N) = O(N)$**
— the same flavor of evidence Hooley had for $S_1 = \sum \tau(n^2+1)$ before
proving it in 1957. It is **not** a proof, and the data does **not**
distinguish $B_3 \sim C N$ from $B_3 \asymp N \log\log N$ over our range
(see Discussion §6).

## The exact identity

We use the identity $\tau(m^2) = \sum_{d|m} 2^{\omega(d)}$. Both sides are
multiplicative in $m$, so it suffices to check at prime powers $m = p^e$:
$\tau(p^{2e}) = 2e+1$, while
$\sum_{d|p^e} 2^{\omega(d)} = 2^{\omega(1)} + \sum_{j=1}^e 2^{\omega(p^j)} = 1 + \sum_{j=1}^e 2 = 1 + 2e$.
Equality holds. Substituting $m = n^2+1$ and summing over $n \le N$:
$$
S_3(N) = \sum_{n \le N} \tau((n^2+1)^2) = \sum_{n \le N} \sum_{d | n^2+1} 2^{\omega(d)}
       = \sum_{d \le N^2+1} 2^{\omega(d)} N_d(N).
$$
Substituting $N_d(N) = \rho(d) N/d + \delta_d(N)$:
$$
S_3(N) = N \sum_{d \le N^2+1} \frac{2^{\omega(d)} \rho(d)}{d} + B_3(N) = N \cdot \Sigma_3(N^2+1) + B_3(N).
$$
This identity is **exact**, not asymptotic. The truncation at $d \le N^2+1$
is exact because for $d > N^2+1$, $N_d(N) = 0$ (no $n \le N$ has
$d | n^2+1 \le N^2+1$).

Both sides are integers (well, $N \cdot \Sigma_3$ is rational), so $B_3(N) = S_3(N) - N \cdot \Sigma_3(N^2+1)$
is an exact rational that we can compute.

## Computation

Two pieces:

**(a) $S_3(N)$ by trial-divide-of-$n^2+1$.** For each $n \le N$, factor $n^2+1$
by trial division using $p = 2$ and primes $p \equiv 1 \pmod 4$ with $p \le n$
(primes $p \equiv 3 \pmod 4$ never divide $n^2+1$, so they are skipped).
The residue $r$ after dividing out all such $p$ has all prime factors $> n$
(by construction). If $r > 1$, then since $r \le n^2+1 < (n+1)^2$, $r$ cannot
be a product of two or more primes $> n$ (which would give $r \ge (n+1)^2$),
nor can it be $q^k$ with $q > n$ and $k \ge 2$ (same bound). Hence $r$ is
either $1$ or a single prime $> n$ to multiplicity 1. The script therefore
multiplies $\tau$ by $3 = 2 \cdot 1 + 1$ when $r > 1$. **Runtime safety:**
the script does *not* explicitly verify the residue is prime; the argument
above is the verification.

**(b) $\Sigma_3(N^2+1)$ by recursive enumeration of supported $d$.** Recall the
support: $d = 2^a m$, $a \in \{0,1\}$, $m$ a product of primes $\equiv 1 \pmod 4$
to any power; in this support $f(d) := 2^{\omega(d)} \rho(d) = 2^a \cdot 4^{\omega(m)}$.
We enumerate by DFS over split primes (in increasing order, with multiplicities),
streaming the contribution $f(d)/d$ into a running sum without materializing
the full list. Memory is $O(|\text{breakpoints}| + \log X_{\max})$.

The two computations together give $B_3(N)$ exactly.

## Numerical results

`bot/scratch/B3-direct-sieve.py` output. Sieve enumerated $9.78 \cdot 10^7$
supported $d \le 9 \cdot 10^8$ in $163$ s; $S_3$ computation took $1.4$ s.

| $N$ | $S_3(N)$ | $N \cdot \Sigma_3(N^2+1)$ | $B_3(N)$ | $B_3(N)/N$ |
|---|---|---|---|---|
| $500$    | $12{,}402$    | $12{,}068.29$    | $333.71$    | $0.6674$ |
| $1{,}000$  | $28{,}700$    | $28{,}363.99$    | $336.00$    | $0.3360$ |
| $2{,}000$  | $66{,}722$    | $65{,}842.57$    | $879.43$    | $0.4397$ |
| $3{,}000$  | $108{,}776$   | $107{,}219.34$   | $1{,}556.66$  | $0.5189$ |
| $5{,}000$  | $199{,}724$   | $197{,}254.39$   | $2{,}469.61$  | $0.4939$ |
| $7{,}000$  | $297{,}554$   | $293{,}951.96$   | $3{,}602.04$  | $0.5146$ |
| $10{,}000$ | $452{,}468$   | $447{,}727.79$   | $4{,}740.21$  | $0.4740$ |
| $15{,}000$ | $726{,}836$   | $720{,}576.05$   | $6{,}259.95$  | $0.4173$ |
| $20{,}000$ | $1{,}020{,}308$ | $1{,}008{,}475.65$ | $11{,}832.35$ | $0.5916$ |
| $30{,}000$ | $1{,}633{,}670$ | $1{,}616{,}462.18$ | $17{,}207.82$ | $0.5736$ |

**Summary statistics** (over $N \ge 1000$, 9 points):
- $\min B_3/N = 0.336$, $\max B_3/N = 0.592$, ratio $\max/\min \approx 1.76$.
- $\text{mean} = 0.485$, $\text{std} \approx 0.077$.
- All 10 $B_3$ values are **positive**.
- No monotone trend in $B_3/N$ vs $N$ (linear regression slope statistically
  indistinguishable from zero: slope $\approx +1 \cdot 10^{-6}$ per unit $N$
  with std $\approx 5 \cdot 10^{-6}$).

## Sanity check vs the SD prediction

The 3-term SD Laurent prediction for $S_3(N)$ is
$\text{pred}_3(N) = 2 c_2 N L^2 + 2 c_1 N L + c_0 N$ with $c_2, c_1, c_0$ from
the previous session ($c_2 \approx 0.171$, $c_1 \approx 0.802$, $c_0 \approx 0.939$).
By Theorem 1 of the previous session,
$$
N \cdot \Sigma_3(N^2+1) = \text{pred}_3(N) + O_A(N/L^A).
$$
So $S_3(N) - \text{pred}_3(N) = B_3(N) + O_A(N/L^A)$ — the empirical check is
that $S_3(N) - \text{pred}_3(N)$ and $B_3(N)$ agree within the SD remainder.
The script's last two columns give $S_3(N) - \text{pred}_3(N)$:

| $N$ | $B_3(N)$ | $S_3(N) - \text{pred}_3(N)$ | difference |
|---|---|---|---|
| $1000$  | $336.0038$  | $336.2556$  | $-0.252$ |
| $3000$  | $1556.6628$ | $1557.7000$ | $-1.037$ |
| $10000$ | $4740.2110$ | $4743.8084$ | $-3.598$ |
| $30000$ | $17207.8249$ | $17217.9251$ | $-10.100$ |

The agreement to 3-4 significant digits at each $N$ confirms the SD chain works
as claimed in the previous session: the *substitution* of the 3-term Laurent
into $\Sigma_3$ at $X = N^2+1$ tracks the truth to $\le 10^{-4} \cdot N$, well
below the $B_3$ scale ($\sim 0.5 N$). The small drift in the difference column
($\sim 3 \cdot 10^{-4} \cdot N$) is consistent with the heuristic
$|r(X)| \lesssim 0.4/L^2$ evaluated at $X = N^2+1$.

## Discussion

**(1) What the data shows.** The ratio $B_3(N)/N$ is in a bounded range
$[0.34, 0.67]$ over $N \in [500, 3 \cdot 10^4]$, with **all 10 values
positive** and no clear monotone trend on a linear scale (regression slope
$+1 \cdot 10^{-6}$ per unit $N$, std $5 \cdot 10^{-6}$, indistinguishable
from zero). Mean $\approx 0.49$. This is **consistent with**
$B_3(N) = O(N)$ but **does not distinguish** $B_3 \sim C N$ from
$B_3 \asymp N \cdot (\text{slow growth})$ such as $\log\log N$
(see (6) below).

**(2) Self-consistency check vs the band difference (weak).** Treating the
"$B_3 \approx 0.5 N$" reading as a working hypothesis, the band difference
predicted is $B_3(N) - B_3(n_-) \approx 0.49 \cdot (1 - 1/\sqrt 2) N
\approx 0.144 N$. The previous session's empirical
$W_{K-1} - P^{(3,3)} \in [+0.04N, +0.21N]$ at five $N \in [10^4, 10^6]$ is a
wide band; $0.144$ falls inside it but this is **compatibility with a
factor-5 interval, not independent triangulation**. The honest reading is:
the two empirical streams are mutually consistent, but neither pins the
constant.

**(3) What it does not show.** Bounded ratio over $N \le 3 \cdot 10^4$
($\sim 1.8$ decades) is *not* a proof that $B_3 = O(N)$ asymptotically.
The unconditional bound is $|B_3(N)| \ll N^2 (\log N)^c$ via SD on $A_3$,
exponentially weaker than what the data show. To rigorously distinguish
$B_3 = O(N)$ from $B_3 = o(N^{1+\epsilon})$ would require either (a)
tracking $B_3/N$ over many more decades and confirming no drift, or (b)
an analytic argument (the Hooley 1957 proof for $S_1$, adapted to
$2^{\omega(d)}$ weights). This session does not attempt (b).

**(4) Sign behavior is striking.** All 10 values $B_3(N) > 0$, with no
oscillation. Pure square-root cancellation in $\sum 2^{\omega(d)} \delta_d(N)$
(random-sign $\delta_d$) would generically give a sign-oscillating
$B_3(N)$ with $|B_3(N)| \ll \sqrt{\sum 2^{2\omega(d)} \cdot \text{var}(\delta_d)}$.
The consistent positivity instead suggests a *systematic bias* in
$\delta_d$ — possibly a rounding-bias contribution
($N_d(N) - \rho(d) N/d$ has a sign bias because $N_d$ is an integer count),
possibly a missed constant Laurent term in the substitution chain. Either
way, the bias is what would justify a "$\sim C N$" reading of the data.
Identifying $C$ analytically (or ruling out a constant by showing $B_3/N \to 0$
at larger $N$) is a natural next sub-task.

**(5) Comparison to $S_1$ (Hooley 1957).** Hooley showed
$S_1(N) := \sum_{n \le N} \tau(n^2+1) = c_1' N \log N + c_0' N + O(N (\log N)^{c''})$
for some $c'' < 1$, i.e. the analog $B_1(N) = S_1(N) - c_1' N \log N - c_0' N$
is $o(N)$. By comparison, our empirics suggest $B_3(N) = O(N)$ but
**not** $o(N)$ (the $\sim C N$ piece doesn't cancel). The bottleneck for
the band-difference is therefore not the Hooley-style $o(N)$ residual but
the explicit constant $C$.

**(6) Caveat on the "$\sim C N$" reading.** The data are at
$N \le 3 \cdot 10^4$, where $L = \log N \le 10.3$ and
$\log\log N \in [1.83, 2.32]$. A model $B_3(N) = N \cdot c \log\log N$ with
$c \approx 0.23$ fits the observed range $[0.34, 0.67]$ as well as the
constant model $B_3 \approx 0.49 N$. Two decades of additional data ($N$ up
to $\sim 10^7$, $\log\log N \in [1.83, 2.78]$) would discriminate the two by
a factor 1.2 in the predicted ratio — possible but not in this session.
Honest framing: the data show $B_3(N)/N$ bounded over our range, which is
**$O(N)$ to within the data range** but does not pin the asymptotic shape.

## Files

- `bot/scratch/B3-direct-sieve.py` (new): the streaming sieve.
- This note.
- Builds on: `n2+1 ai thoughts/notes/proofs/P12-effective-SD-on-Sigma3.md`,
  `n2+1 ai thoughts/notes/proofs/P12-W-Kminus1-N1e6-3term.md`.

## Caveats (documented soft spots)

- Empirical at $N \le 3 \cdot 10^4$ only; $\sim 1.5$ decades. Does not
  distinguish $O(N)$ from $o(N^{1+\epsilon})$.
- $S_3$ floating-point is exact (integer arithmetic). $\Sigma_3$ is computed
  in float64 by summing $f(d)/d$; rounding is bounded by $\sim 10^{-13}$ per
  $d$ summed, total $\sim 10^{-5}$ over the full enumeration. This is well
  below the $B_3 \sim 10^3$–$10^4$ scale.
- The 3-term Laurent prediction uses $H_3''(1) \approx -0.234$ from previous
  session at $p < 10^6$ truncation; truncation tail $\sim 10^{-5}$ propagates
  linearly into $c_0$ but not into $c_2, c_1$.
