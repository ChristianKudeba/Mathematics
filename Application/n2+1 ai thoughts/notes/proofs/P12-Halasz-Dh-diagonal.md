# P12: Diagonal second moment $D_h(N)$ — closed-form prediction matched to data

**Status (2026-05-08 12:45 UTC):** Empirical $D_h(N)/N \to C_h$ at $h \in \{1,2,5,100\}$
across $N \in \{10^5, 10^6, 10^7\}$ matches a closed-form heuristic prediction
$C_h = (\pi/4) H_h(1)$ at gap $< 10^{-3}$ throughout, where $H_h$ is an explicit
Euler product (rigorous Selberg–Delange on a residue-averaged multiplicative function;
the identification $D_h \approx D_h^{\text{heur}}$ is heuristic — see §6). **Strategic
effect**: rules OUT the Halász framework as the binding mechanism for the prev-session
$|H_h(N)| \ll \sqrt N$ observation (Halász would give $N (\log N)^{-c}$, much weaker
than $\sqrt N$); SUGGESTS but does not prove that the right framework is diagonal /
second moment / CLT (the diagonal $D_h \sim C_h N$ gives the correct scale, but
off-diagonal cancellation is still needed and not yet established).

## 1. Setup

For squarefree $e \ge 2$ with all prime factors in $\{2\} \cup \{p : p \equiv 1 \pmod 4\}$
(call such $e$ "sf good"), the multiplicative-root weight is
$$
\widetilde S_h(e) \;:=\; \sum_{r:\, r^2 \equiv -1 \pmod e} e^{-2\pi i h r/e}
\;=\; \prod_{p \mid e} 2\cos\!\Big(2\pi h\,\alpha_p (e/p)^{-1}_p / p\Big)
$$
(with the $p=2$ factor being $(-1)^h$). Here $\alpha_p$ is a fixed root of
$x^2 + 1 \equiv 0 \pmod p$ at split $p$, and $(e/p)^{-1}_p \in (\mathbb Z/p)^*$
is the modular inverse of $e/p$.

Define the diagonal second moment
$$
D_h(N) \;:=\; \sum_{2 \le e \le N,\ \text{sf good}} \widetilde S_h(e)^2
\;=\; \sum_{e} \prod_{p \mid e} 4\cos^2\!\Big(2\pi h\,\alpha_p (e/p)^{-1}_p / p\Big).
$$

## 2. Empirical scaling: $D_h(N) \sim C_h N$ with NO log corrections

Direct computation (`bot/scratch/Halasz-Dh-empirical.py`):

| $N$ | $h=1$ | $h=2$ | $h=5$ | $h=100$ |
|---|---|---|---|---|
| $D_h(N)/N$ at $10^5$ | 0.3932 | 0.3899 | 0.5401 | 0.5402 |
| $D_h(N)/N$ at $10^6$ | 0.3942 | 0.3924 | 0.5439 | 0.5403 |
| $D_h(N)/N$ at $10^7$ | 0.3928 | 0.3919 | 0.5426 | 0.5434 |

$D_h(N)/N$ is constant to within $\pm 0.5\%$ across three decades. **No $\log N$
factor.** Sf good count $\approx 0.115\, N$; the "average $\widetilde S_h^2$ per sf good $e$"
is $\sim 3.4$ for $h \in \{1,2\}$ and $\sim 4.7$ for $h \in \{5,100\}$.

## 3. Heuristic closed form

Average the per-prime factor $4\cos^2(2\pi h \alpha_p (e/p)^{-1}/p)$ over
$(e/p)^{-1} \in (\mathbb Z/p)^*$ uniformly. Using $4\cos^2\theta = 2 + 2\cos(2\theta)$
and $\sum_{k=1}^{p-1}\cos(2\pi m k/p) = -1$ for $p \nmid m$:
$$
\overline g_h(p) \;:=\; \mathbb E_{k}\big[4\cos^2(2\pi h \alpha_p k / p)\big] \;=\; \begin{cases}
1 & p = 2, \\
2(p-2)/(p-1) & p \equiv 1 \pmod 4,\ p \nmid h, \\
4 & p \equiv 1 \pmod 4,\ p \mid h, \\
0 & \text{else.}
\end{cases}
$$
(For $p=2$: $\widetilde S_h$ factor is $(-1)^h$, square $1$.)

Treating $\overline g_h$ as a strictly multiplicative function on sf good $e$:
$$
D_h^{\text{heur}}(N) \;:=\; \sum_{e \le N,\,\text{sf good}} \overline g_h(e),
\qquad
G_h(s) \;:=\; \sum_e \overline g_h(e)\, e^{-s} \;=\; (1 + 2^{-s}) \prod_{p \equiv 1\,(4)}(1 + \overline g_h(p) p^{-s}).
$$

**Pole structure.** At $s = 1$,
$$
\sum_p \overline g_h(p)/p^s \;=\; 2\!\!\sum_{p \equiv 1\,(4)}\!\! p^{-s} + O(1) \;=\; \log \zeta_K(s) + O(1)
$$
(using $\zeta_K = \zeta \cdot L(\chi_4)$ and $\sum_{p \equiv 1(4)} p^{-s} = \frac12(\log\zeta + \log L(\chi_4)) + O(1)$).
Hence $G_h(s) \cdot \zeta_K(s)^{-1}$ extends holomorphically to a neighborhood of $s=1$, with
$$
H_h(s) \;:=\; G_h(s)/\zeta_K(s)
\;=\; (1 - 4^{-s})
\prod_{p \equiv 1\,(4)} (1 + \overline g_h(p)/p^s)(1-p^{-s})^2
\prod_{p \equiv 3\,(4)} (1 - p^{-2s}).
$$
Selberg–Delange / Wiener–Ikehara gives
$$
D_h^{\text{heur}}(N) \;\sim\; \mathrm{res}_{s=1} G_h(s) \cdot N \;=\; \tfrac{\pi}{4}\, H_h(1) \cdot N.
$$
Define $C_h := (\pi/4) H_h(1)$.

## 4. Explicit Euler product

$$
H_h(1) = \frac{3}{4} \prod_{p \equiv 3\,(4)} \!\Big(1 - \frac{1}{p^2}\Big)
\prod_{\substack{p \equiv 1\,(4) \\ p \nmid h}} \frac{(p^2+p-4)(p-1)}{p^3}
\prod_{\substack{p \equiv 1\,(4) \\ p \mid h}} \frac{(p+4)(p-1)^2}{p^3}.
$$

Each factor at $p \equiv 1(4)$ equals $1 - 5/p^2 + 4/p^3$ for $p \nmid h$
(expanding $(p^3+0\cdot p^2-5p+4)/p^3$), and $1 + 3/p - 4/p^2 + O(1/p^3)$ for $p \mid h$;
the $p \nmid h$ product converges absolutely. (There are finitely many primes dividing $h$,
so the $p \mid h$ correction is a finite product.)

## 5. Empirical match (3-digit precision)

Computed via truncation $P = 10^6$ (`bot/scratch/Halasz-Dh-analytic.py`):

| $h$ | predicted $C_h$ | empirical $C_h(10^7)$ | gap |
|---|---|---|---|
| 1   | 0.392532 | 0.392770 | $-2.4 \cdot 10^{-4}$ |
| 2   | 0.392532 | 0.391930 | $+6.0 \cdot 10^{-4}$ |
| 5   | 0.543506 | 0.542590 | $+9.2 \cdot 10^{-4}$ |
| 100 | 0.543506 | 0.543370 | $+1.4 \cdot 10^{-4}$ |

For $h = 1, 2$ the prediction is identical (no split prime divides $h$). For
$h = 5, 100$ the prediction is identical because $\{p \equiv 1(4): p \mid h\} = \{5\}$
in both cases.

The gap $\le 10^{-3}$ is consistent with: (i) finite-$N$ Selberg–Delange remainder
$O(1/\log N) \sim 0.06$ at $N = 10^7$, but our gap is much smaller — suggesting the
remainder decays faster on this multiplicative function; (ii) heuristic-averaging
error from non-strict multiplicativity (treating $(e/p)^{-1}$ as uniform — see §6).

## 6. Caveat on the heuristic — the $D_h \approx D_h^{\text{heur}}$ step is unrigorous

The function $\widetilde S_h(e)^2 = \prod_{p \mid e} 4\cos^2(2\pi h \alpha_p (e/p)^{-1}/p)$
is **not** strictly multiplicative, because the per-prime factor depends on
$(e/p)^{-1} \pmod p$, which depends on the OTHER primes in the factorization of $e$.

Replacing $\widetilde S_h(e)^2$ by the residue-averaged $\overline g_h(e) :=
\prod_{p \mid e} \overline g_h(p)$ is **not a benign Selberg–Delange-style smoothing**:
it changes the underlying summand pointwise (not just smooths a remainder). The fact
that for fixed $p$ the residue $(e/p)^{-1} \bmod p$ is approximately equidistributed
across squarefree $e$ coprime to $p$ is necessary but not sufficient — what one needs
is that the **joint** distribution of $((e/p_1)^{-1} \bmod p_1, \ldots, (e/p_k)^{-1} \bmod p_k)$
across the $\omega(e) = k$ prime divisors is close to product-uniform on
$\prod (\mathbb Z/p_i)^*$. This decorrelation is plausible (cf. Hooley/Erdős–Hooley
equidistribution arguments) but is NOT proved here.

**Therefore $D_h(N) \sim C_h N$ with $C_h = (\pi/4) H_h(1)$ is HEURISTIC**, not
"rigorous modulo SD". What §3–§4 prove rigorously is only that the heuristic sum
$D_h^{\text{heur}}(N) := \sum_{e \le N, \mathrm{sf\ good}} \overline g_h(e)$ has
this asymptotic. The identification $D_h(N) \approx D_h^{\text{heur}}(N)$ is empirical-only.

The empirical $\le 10^{-3}$ gap in §5 is consistent with this approximation holding
to ~3 digits at $N = 10^7$, but the gap could in principle drift slowly with $N$
(e.g., as a $1/\log N$ correction); 3 decades of data is too short to rule that out.

## 7. Strategic implication: a candidate framework for $|H_h(N)| \ll \sqrt N$

Prev session (`P12-Halasz-Hh-empirical.md`) showed $|H_h(N)|/\sqrt N \le 1.36$
across 23 $(N, h)$ data points up to $N = 10^7$. The candidate framework was
**Halász on $\widetilde S_h$**, which would give $|H_h| \ll N \exp(-c \log\log N)
= N (\log N)^{-c}$ — much **weaker** than $\sqrt N$ by a factor of $\sqrt{N/(\log N)^c}$.

The diagonal $D_h(N) \sim C_h N$ (heuristic — see §6) **suggests** but does NOT
prove that the right framework is second moment / CLT:

- $|H_h(N)|^2 = D_h(N) + (\text{cross terms})$.
- IF cross terms vanish in expectation under some natural averaging, $|H_h|^2 \sim D_h \sim C_h N$,
  giving $|H_h| \asymp \sqrt N$.

The empirical ratios $|H_h(10^7)|^2 / D_h(10^7)$ across $h \in \{1,2,5,100\}$ are
$\{0.022, 0.146, 0.052, 0.852\}$. These are **NOT close to 1**, so they do not provide
direct evidence for $|H_h|^2 \sim D_h$ as a pointwise statement; under a CLT-fluctuation
heuristic the ratio has mean 1 with large variance, but with only 4 data points we
cannot distinguish CLT-fluctuation from pure happenstance.

**Strategic upshot (more cautious)**: the diagonal $D_h \sim C_h N$ rules out the
Halász framework as the binding mechanism (the bound it gives is $\sqrt{D_h} \ll \sqrt N$,
not $N/\log^c N$). The next analytic step is to **either**:
(a) Compute $\mathbb E_h |H_h|^2$ averaged over $h \in [1, H]$ to test whether cross
    terms vanish under $h$-averaging; this is a clean computation (the inner sum over
    $h$ gives a $\delta$-like restriction to $r_1/e_1 + r_2/e_2 \in \mathbb Z$).
(b) Confirm or refute the off-diagonal at fixed $h$ empirically by computing
    $\sum_{e_1 \ne e_2} \widetilde S_h(e_1) \widetilde S_h(e_2)$ at a few $(N, h)$.

## 8. What's rigorous vs. heuristic

**Rigorous (modulo standard SD on multiplicative function)**:
- The Dirichlet series identity $G_h(s) = \zeta_K(s) H_h(s)$ with $H_h$
  holomorphic on $\Re s > 1/2$, $H_h(1) > 0$ explicit Euler product.
- Selberg–Delange asymptotic for the **heuristic** sum $D_h^{\text{heur}}(N) \sim C_h N$,
  $C_h = (\pi/4) H_h(1)$.

**Heuristic (NOT rigorous)**:
- The identification $D_h(N) \approx D_h^{\text{heur}}(N)$. Empirical gap $\le 10^{-3}$
  at $N = 10^7$ across 4 $h$-values, but no rigorous bound on the "averaging-over-residues"
  error. **The asymptotic $D_h(N) \sim C_h N$ for $D_h$ itself (as opposed to
  $D_h^{\text{heur}}$) is heuristic**; making it rigorous requires the joint
  decorrelation of $((e/p_i)^{-1} \bmod p_i)_{i}$ across the prime divisors of $e$.

**Empirical only**:
- The $\sqrt N$ rate of $H_h(N)$ itself. The diagonal $D_h \sim C_h N$
  rules out the Halász framework, but does not prove $|H_h| \ll \sqrt N$ — off-diagonal
  cancellation is needed and not yet established.

## 9. Files

- `bot/scratch/Halasz-Dh-empirical.py`: per-$e$ direct sieve computing both
  $H_h(N)$ and $D_h(N)$. Runtime $\sim 10$s at $N=10^7$ for 4 $h$-values.
- `bot/scratch/Halasz-Dh-analytic.py`: Euler-product evaluation of $H_h(1)$
  via truncation at $P$, comparing $C_h^{\text{pred}}$ vs $C_h^{\text{emp}}$.
- Builds on: `P12-Halasz-Hh-empirical.md` (prev session, $H_h$ itself);
  `P12-Uh-vs-Th-empirical.md` (route closure).

## 10. Next steps

1. **(1 session, analytic)**: Compute $\mathbb E_h[|H_h(N)|^2]$ averaged over
   $h \in [1, H]$ for some growth rate $H = H(N)$. Could decouple the cross
   terms via $h$-orthogonality, giving a cleaner "average" version of the
   diagonal $D_h$.
2. **(½ session, empirical)**: Extend $D_h$ table to $h \in \{3, 7, 13, 17, 1000, 10^4\}$
   to test the ($p \mid h$ vs $p \nmid h$) prediction for primes $p \in \{13, 17\}$
   and large $h$ where prediction is identical to $h = 1$.
3. **(½ session, empirical)**: Compute the off-diagonal sum
   $\sum_{e_1 < e_2} \widetilde S_h(e_1) \widetilde S_h(e_2)$ directly at a
   couple of $(N, h)$ points to measure how much it cancels the cross terms.
4. **(Banked methodological lesson)**: The 30-second empirical preview lesson from
   prev session generalizes: when an empirical rate appears to violate the
   "natural" analytic framework's prediction (here, $\sqrt N$ vs Halász's $N/(\log N)^c$),
   compute the next-order quantity (here, the diagonal $D_h$) — the right framework
   often becomes obvious from a 5-minute calculation.
