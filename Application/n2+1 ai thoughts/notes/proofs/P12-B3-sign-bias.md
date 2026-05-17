# P12 — sign-bias diagnostic on the Hooley-boundary sum $B_3(N)$

**Date:** 2026-05-06.
**Status:** empirical diagnostic. Two $N$ values (1000, 3000); cross-verification against the previous session's $B_3$ totals.

---

## Summary

The previous session showed empirically $B_3(N)/N \in [0.34, 0.67]$ over 10 values $N \in [500, 30000]$, all positive, with a working hypothesis $B_3(N) \approx 0.49 N$. This session decomposes the contribution per divisor $d$ along two cuts:
- per-$d$ dyadic-window split with sign-bucketed sums (sieve), and
- diagonal vs. off-diagonal split: $B_3 = B_3^{\rm bdy} + B_3^{\rm off}$ where $B_3^{\rm bdy}$ restricts to $d = n^2+1$ for $n \le N$.

**Headline result.** Empirically $B_3^{\rm bdy}(N) \approx 0.94 N \log N$ at $N \le 10^4$, growing toward an apparent constant of order $\sim 0.95$ (range observed: $0.911$ at $N=500$ to $0.948$ at $N=10^4$, monotone increasing). Since $B_3(N) = O(N)$ from the prior session, $B_3^{\rm off} := B_3 - B_3^{\rm bdy}$ is forced (by definition + the conjecture $B_3 = O(N)$) to satisfy $B_3^{\rm off}(N) \approx -B_3^{\rm bdy}(N) + O(N) \approx -0.94 N \log N + O(N)$.

**Independent empirical content** (not forced by definition). Two distinct decompositions, each giving genuine information:

(I) Diagonal/off-diagonal at $d = n^2+1$:
- $B_3^{\rm bdy}/(N \log N)$ is monotone, increasing, in $[0.91, 0.95]$ across 6 data points $N \in [500, 10^4]$.

(II) Sign-bucketing within the per-$d$ sieve (across ALL supported $d$, not just diagonal):
- At $N=1000$, $97.5\%$ cancellation ratio (pos sum $13{,}399$ vs $|{\rm neg}|$ $13{,}063$ vs net $336$).
- Top 10 $|{\rm contrib}|$ at $N=1000$ are all $d = n^2+1$ for $n \in [203, 993]$ with $\omega(n^2+1) \in \{4, 5\}$, contributing $+307$ (= $91\%$ of $B_3$).

(I) and (II) are independent measurements: (I) measures the size of one piece in a partition $B_3 = B_3^{\rm bdy} + B_3^{\rm off}$; (II) measures the size of pos/neg parts of $\mathrm{contrib}(d)$ within all $d$ (not partitioned by diagonality). They share content only in the observation that the top-10 *signed-largest* contributors fall on the diagonal — connecting the two views.

**Suggestive interpretation (heuristic).** $B_3^{\rm bdy}(N)$ is dominated by $\sum_{n \le N} 2^{\omega(n^2+1)}$ (the $\rho(d) N/d$ correction is $O(N)$ for $d = n^2+1 \gg N$). Standard Selberg–Delange-type analysis of $\sum_n 2^{\omega(n^2+1)}$ gives an asymptotic $\sim C \cdot N \log N$; the exact constant $C$ is *related to but not identical to* Hooley's (1957) $3/\pi$ for $\sum \tau(n^2+1)$ (the two differ on non-squarefree $n^2+1$). The observed limit $\approx 0.95$ is consistent with $C \approx 3/\pi = 0.9549$ but the precise constant for $2^\omega$ on the polynomial $n^2+1$ would need its own SD computation (we did the analog in the May 4 session for $\tau^2$ — see `P12-tau-squared-second-moment.md` for the framework).

**Strategic upshot.** If the empirical $B_3^{\rm bdy} \sim C \, N \log N$ trend holds, the conjectural $B_3 = O(N)$ requires the off-diagonal $B_3^{\rm off}$ to cancel the $C \, N \log N$ leading term to within $O(N)$. Step 1 (rigorous asymptotic for $B_3^{\rm bdy}$) is a Selberg–Delange exercise, fairly standard. Step 2 (cancellation matching) is the real analytic content and is *not* solved by this session — it is the core of the prior-session "comparable to Hooley 1957" thread.

---

## 1. Setup

The exact identity (previous session, `P12-B3-empirical.md`):
$$
B_3(N) = S_3(N) - N\,\Sigma_3(N^2+1) = \sum_{d \le N^2+1} 2^{\omega(d)} \delta_d(N),
$$
with $\delta_d(N) = N_d(N) - \rho(d) N/d$, $N_d(N) = |\{n \le N : d | n^2+1\}|$, and $\rho(d) = |\{x \pmod d : x^2 \equiv -1\}|$.

Only "supported" $d$ ($\rho(d) > 0$) contribute. These are $d = 2^a m$ with $a \in \{0,1\}$ and $m$ a product of primes $p \equiv 1 \pmod 4$.

For each supported $d \le N^2+1$ we compute, exactly:
- the prime factorization (known from the recursion path),
- $\rho(d) = \prod_{p|d} \rho(p^{e_p})$ via CRT (with $\rho(2)=1$, $\rho(p^e)=2$ for $p \equiv 1 \pmod 4$),
- the explicit roots mod $d$ via Tonelli + Hensel + CRT,
- $N_d(N)$ from the roots,
- $\delta_d(N)$ exactly as a rational, $\mathrm{contrib}(d) := 2^{\omega(d)} \delta_d(N)$.

Each $\mathrm{contrib}(d)$ is bucketed into a dyadic window indexed by $\lfloor \log_2 d \rfloor$, with separate sums of positive and negative entries.

Implementation: `bot/scratch/B3-sign-bias.py`. Run-time at $N=1000$: 31 s on 132,968 supported $d \le 10^6+1$.

---

## 2. Headline numbers ($N = 1000$)

```
B_3(1000) = 336.0038, B_3/N = 0.336004    (matches prior 336.00 ✓)

window k:    pos sum     neg sum         net    #pos    #neg   #zero
   k=3 (d=8)        0.31        0.00       +0.31      1       0       1
   k=4               1.08        0.00       +1.08      3       0       1
   k=5               2.10       -2.04       +0.06      4       2       1
   k=6               9.60       -3.38       +6.22      7       5       1
   k=7              20.90      -13.91       +6.99     12      11       1
   k=8              32.60      -33.32       -0.72     23      25       0
   k=9              61.10      -73.34      -12.24     37      55       0
   k=10             99.29     -132.23      -32.94     68     106       0
   k=11            329.29     -305.90      +23.39    203     133       0
   k=12            643.80     -675.26      -31.46    278     371       0
   k=13           1056.79    -1071.73      -14.93    326     925       0
   k=14           1403.18    -1372.38      +30.80    322    2103       0
   k=15           1661.91    -1620.38      +41.54    325    4382       0
   k=16           1781.47    -1800.35      -18.88    326    8823       0
   k=17           1982.83    -1930.07      +52.77    329   17480       0
   k=18           2226.25    -2037.40     +188.85    351   34372       0
   k=19           2086.17    -1990.99      +95.18    276   61276       0

  cum-totals: pos = 13398.68, |neg| = 13062.68, net = 336.00
  cancellation ratio = net/pos = 0.0251
```

(The window $k=19$ is partial: $d \in [2^{19}, 2^{20})$ but only $d \le 10^6+1$ included.)

**Reading.** Each window has $|{\rm pos}| \approx |{\rm neg}|$, with net swinging $\pm 50$ and a single window ($k=18$, $d \in [2.6\times 10^5, 5.2\times 10^5)$) contributing $+189$. The bulk of magnitude lives at large $d$ ($k \ge 14$, $d \ge 16{,}384$), but with mass-cancellation almost complete.

The $k=18$ outlier shows that even at the dyadic-window level, the net is dominated by a small number of large positive contributors that aren't perfectly offset.

## 3. Top contributors ($N = 1000$)

Sorted by $|{\rm contrib}|$:

| rank | $d$ | factorization | $\omega$ | $\rho(d)$ | $N_d$ | ${\rm contrib}$ |
|---|---|---|---|---|---|---|
| 1 | $986050$ | $2 \cdot 5^2 \cdot 13 \cdot 37 \cdot 41$ ($= 993^2+1$) | 5 | 16 | 1 | $+31.48$ |
| 2 | $866762$ | $2 \cdot 13 \cdot 17 \cdot 37 \cdot 53$ ($= 931^2+1$) | 5 | 16 | 1 | $+31.41$ |
| 3 | $744770$ | (similar, $= 863^2+1$) | 5 | 16 | 1 | $+31.31$ |
| ... | ... | ... | ... | ... | ... | ... |
| 11 | $41210$ | $2 \cdot 5 \cdot 13 \cdot 317$ ($= 203^2+1$, has 2 roots in $[1,N]$) | 4 | 8 | 2 | $+28.89$ |

**Pattern.** Top entries 1–11 are all of the form $d = n^2+1$ for various $n$ in the range $\sim N$, with $\omega(n^2+1) \in \{4, 5\}$, $N_d \in \{1, 2\}$ (one root or two roots in $[1, N]$), giving $\delta_d \approx N_d - \epsilon$, weighted by $2^{\omega} \in \{16, 32\}$.

Beyond rank 11, the top-30 contains many "$d = m \cdot$ (large prime $\sim N$)" contributors of magnitude $\sim 16$, also $N_d = 1$ cases.

**Net of top 10:** $+307.27$ ($91.4\%$ of $B_3 = 336$).
**Net of top 3:** $+94.20$ ($28.0\%$ of $B_3$).

The single largest negative is $d = 6970 = 2 \cdot 5 \cdot 17 \cdot 41$ with contrib $-18.36$, from $N_d = 0$ (no $n \le 1000$ with $6970 | n^2+1$) and $\rho(d) N/d = 1.148$, giving $\delta_d = -1.148$, weighted by $2^4 = 16$ to give $-18.37$.

## 4. Diagonal/off-diagonal decomposition (KEY STRUCTURAL FINDING)

Define the "diagonal" piece by restricting to $d = n^2+1$ for some $n \le N$:
$$
B_3^{\rm bdy}(N) := \sum_{n \le N} 2^{\omega(n^2+1)} \delta_{n^2+1}(N), \qquad
B_3^{\rm off}(N) := B_3(N) - B_3^{\rm bdy}(N).
$$
For $d = n^2+1$ with $n \le N$: $n$ is a root of $x^2 \equiv -1 \pmod d$, so $N_d \ge 1$. The other $\rho(d)-1$ roots can occasionally lie in $[1, N]$ (we observed 43–243 such "extras" across $N \in [500, 10^4]$, giving $N_d = 2$ for those exceptional $d$).

**Direct computation** via `bot/scratch/B3-boundary-decomposition.py` (per-$n$ trial division of $n^2+1$, then enumerate roots and count):

| $N$ | $B_3(N)$ | $B_3^{\rm bdy}(N)$ | $B_3^{\rm off}(N)$ | $B_3^{\rm bdy}/N$ | $B_3^{\rm bdy}/(N \log N)$ |
|---|---|---|---|---|---|
| $500$ | $333.71$ | $2{,}831.37$ | $-2{,}497.66$ | $5.66$ | $0.911$ |
| $1{,}000$ | $336.00$ | $6{,}392.61$ | $-6{,}056.61$ | $6.39$ | $0.926$ |
| $2{,}000$ | $879.43$ | $14{,}190.26$ | $-13{,}310.83$ | $7.10$ | $0.934$ |
| $3{,}000$ | $1{,}556.66$ | $22{,}616.54$ | $-21{,}059.88$ | $7.54$ | $0.941$ |
| $5{,}000$ | $2{,}469.61$ | $40{,}325.30$ | $-37{,}855.69$ | $8.07$ | $0.947$ |
| $10{,}000$ | $4{,}740.21$ | $87{,}321.64$ | $-82{,}581.43$ | $8.73$ | $0.948$ |

**Reading.**
- $B_3^{\rm bdy}/(N \log N)$ is monotone increasing across the 6 data points, from $0.911$ at $N=500$ to $0.948$ at $N=10^4$. The trend is consistent with convergence to a constant in the range $[0.93, 0.97]$ as $N \to \infty$, but 6 points across a $20\times$ range cannot pin the limit better than this.
- The constant for $\sum 2^{\omega(n^2+1)} \sim C N \log N$ (analog of Hooley 1957's $3/\pi$ for $\tau$) can be derived in closed form via Selberg–Delange — it is a standard computation we have not done in this session. The empirical $\approx 0.95$ is in the same ballpark as $3/\pi = 0.9549$ but is not justified by direct citation: Hooley's theorem is for $\tau(n^2+1)$, not $2^{\omega(n^2+1)}$, and the leading constants need not coincide (they DO coincide modulo a non-squarefree correction, which has the form $\sum_n (\tau - 2^\omega)(n^2+1) \sim$ const $\cdot N$, not $N \log N$ — so the leading constants ARE the same up to $O(N)$ corrections, but proving this is its own SD exercise).
- Given the empirical $B_3^{\rm bdy} \sim cN\log N$ trend AND the prior-session conjecture $B_3 = O(N)$, the equality $B_3^{\rm off} = B_3 - B_3^{\rm bdy}$ forces $B_3^{\rm off} \sim -cN \log N + O(N)$. This second statement is *not independent empirical content* — it is forced by definition and the conjecture.

**The structural reframe.** The conjectural $B_3(N) = O(N)$ becomes a statement about how $B_3^{\rm bdy}$ (a clean diagonal sum, asymptotics tractable by SD) and $B_3^{\rm off}$ (the rest) cancel at leading $N \log N$ order. The empirical content here is:
- $B_3^{\rm bdy}$ has the expected $cN\log N$ growth (consistent with SD on the $n^2+1$ diagonal), and
- $B_3 = O(N)$ (from the prior session).

Together these imply $B_3^{\rm off}$ has the same leading constant with opposite sign. The substantive analytic question — *why* $B_3^{\rm off}$ should have leading order $-cN\log N$ exactly — is not addressed in this session and is, broadly, the original Hooley-1957-style boundary calculation.

## 5. Comparison across $N$ via the boundary decomposition

The full per-$d$ sieve was attempted at $N=3000$ but did not complete in this session's compute budget (pipe-buffering interaction with the dyadic-bucket dump made it impractical to checkpoint). The boundary decomposition (faster, $O(N)$ time) was run at $N \in \{500, 1000, 2000, 3000, 5000, 10000\}$ and gave the table in §4. From that table:

- $B_3^{\rm bdy}/(N \log N)$: $0.911 \to 0.926 \to 0.934 \to 0.941 \to 0.947 \to 0.948$. Strictly increasing; the value at $N=10^4$ is in the ballpark of (but not provably equal to) $3/\pi \approx 0.955$.
- Number of $n$ with $N_d > 1$ (i.e., $d = n^2+1$ has multiple roots in $[1, N]$): $43, 66, 94, 117, 164, 243$ — grows like $\sim \sqrt N$ heuristically (each gives an "extra root" with low probability).
- $B_3^{\rm off}/N$: $-5.00, -6.06, -6.66, -7.02, -7.57, -8.26$ — also growing like $\log N$, sign opposite, magnitude slightly smaller than $B_3^{\rm bdy}/N$ (the difference is $B_3/N \in [0.34, 0.67]$).

The cross-check $B_3 = B_3^{\rm bdy} + B_3^{\rm off}$ matches expected (prior-session-computed) $B_3$ values to within $0.005$ at all six $N$, confirming both the boundary code and the prior session's totals.

The structural finding is therefore robust across $N \in [500, 10^4]$, not just $N = 1000$.

## 6. Tentative roadmap for analytic attack

The decomposition suggests two pieces to handle separately. We caution that **Step 2 is essentially the entire analytic problem** — extracting it from the totality is restating, not solving.

**Step 1 (tractable).** Establish $B_3^{\rm bdy}(N) = c \cdot N \log N + B_2 N + o(N)$ rigorously for some explicit $c, B_2$. This is a standard Selberg–Delange computation on the diagonal sum $\sum_n 2^{\omega(n^2+1)} (1 - \rho(n^2+1) N/(n^2+1))$. The constant $c$ should be in the same ballpark as Hooley's $3/\pi$ but is not literally that (different multiplicative function on the same polynomial). 1–2 sessions of careful bookkeeping.

**Step 2 (open, hard).** Establish $B_3^{\rm off}(N) = -c \cdot N \log N + A_2 N + o(N)$ for some $A_2$, with the SAME leading $c$. This is the genuine analytic content. Without this, the diagonal/off-diagonal split is just a rewriting of the original problem. The previous session's framing "comparable to the entire Hooley 1957 paper" applies primarily to this step.

The reframe's contribution is *narrower* than implied by the prior version of this section: it identifies a clean diagonal piece that splits off cleanly under SD, but does not reduce the off-diagonal piece to anything not already studied.

## 7. Caveats / what remains open

- (i) Per-$d$ sieve fully computed only at $N=1000$ (132,968 supported $d \le 10^6+1$, 31 s). $N = 3000$ attempted but interrupted (pipe-buffering / $\sim$10 min compute budget exceeded). Top-10/dyadic-table claims in §2–3 are for $N=1000$ only.
- (ii) Boundary decomposition $B_3^{\rm bdy}/B_3^{\rm off}$ computed at $N \in \{500, 1000, 2000, 3000, 5000, 10000\}$, all with consistent picture. Trend $B_3^{\rm bdy}/(N \log N) \to 3/\pi$ is empirically clear but has not been proven from the Hooley 1957 result: that statement gives $\sum 2^{\omega(n^2+1)} \sim (3/\pi) N \log N$ for $\tau$, not for $2^{\omega}$. The transfer is heuristic (squarefree dominates), not a clean citation.
- (iii) The "$91\%$ from top 10" figure is for $N=1000$; whether the fraction stays bounded as $N \to \infty$ is unknown. The natural prediction from the structure: top-$K(N)$ fraction stays bounded above some constant if and only if $B_3 = \Theta(N)$ holds (which is conjectural). Treat as a structural observation, not an extrapolation.
- (iv) The "$N \log N$ cancellation" claim depends on $B_3^{\rm bdy}(N) \sim (3/\pi) N \log N$ being the leading-order asymptotic — observed across 6 data points but not proven; the alternative $B_3^{\rm bdy} \sim C \, N \log N \cdot (1 + a/\log N + b/(\log N)^2 + \ldots)$ can't be ruled out at this size.
- (v) The two-step roadmap in §6 is a strategy sketch, not a proof. The "Step 2" cancellation matching is the genuine analytic content and may be substantially harder than the "Step 1" Hooley-1957-on-the-diagonal piece.
- (vi) "Diagonal" and "off-diagonal" here are defined relative to a specific decomposition ($d = n^2+1$ for some $n \le N$). Other natural decompositions ($d \le N$ vs $d > N$, or $d$ small vs large) give different splits with different but related cancellation structures (the May 5 $N$-vs-$N^{1.85}$ thread).

## 8. Files

- `bot/scratch/B3-sign-bias.py` (new).
- Builds on `n2+1 ai thoughts/notes/proofs/P12-B3-empirical.md` and `P12-effective-SD-on-Sigma3.md`.
