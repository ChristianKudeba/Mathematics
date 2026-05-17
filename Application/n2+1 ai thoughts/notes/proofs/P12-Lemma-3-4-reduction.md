# P12 — Lemma 3.4 reduction: $F(N) - \langle F\rangle = o(N)$ via Fourier + character sums

**Session.** 2026-05-08 (UTC). Builds on:
- `P12-c0T-secondary-constant.md` (Cor 3.2 invokes Lemma 3.4 implicitly).
- `P12-B-infty-existence-equivalence.md` (Lemma 3.4 stated explicitly).

**Goal.** Reduce the unrigorized "Erdős–Hooley discrepancy" step (Lemma 3.4 below)
to a precisely-stated character-sum estimate that is standard in the analytic
literature, and verify the qualitative bound empirically. This converts the
status of Lemma 3.4 from "cited as Hooley 1957 §3 / Erdős–Hooley delta-function,
not freshly written here" to "explicitly reduced to a known character-sum
estimate, verified to hold at the empirical $\sqrt N$ level".

## 1. The fluctuation $E(N)$

Recall the setup in `P12-B-infty-existence-equivalence.md`. For sf $e \ge 2$
with $\rho(e) \ge 1$, let $r_1^{(e)}, \ldots, r_{\rho(e)}^{(e)} \in [1, e-1]$
be the roots of $x^2 \equiv -1 \pmod e$. Define
$$F(N) := \sum_{\substack{e \,\mathrm{sf}\\ 2 \le e \le N}} \sum_{i=1}^{\rho(e)} \left\{\frac{N - r_i^{(e)}}{e}\right\}, \qquad A(N) := \sum_{\substack{e \,\mathrm{sf}\\ 2 \le e \le N}} \rho(e), \qquad \Sigma_*(N) := \sum_{\substack{e \,\mathrm{sf}\\ e \le N}} \frac{\rho(e)}{e}.$$

**Mean of $F$.** For each fixed $e \ge 2$, $\{(N-r_i^{(e)})/e\}$ takes each of
the $e$ values $0/e, 1/e, \ldots, (e-1)/e$ once as $N$ ranges over a complete
residue system mod $e$. The mean is $(e-1)/(2e) = 1/2 - 1/(2e)$. Summing over
$i$ and over sf $e \in [2, N]$:
$$\langle F(N) \rangle := \tfrac{1}{2} A(N) - \tfrac{1}{2}(\Sigma_*(N) - 1) = \tfrac{1}{2} A(N) - \tfrac{1}{2}\Sigma_*(N) + \tfrac{1}{2}.$$

The fluctuation we need to bound:
$$E(N) := F(N) - \langle F(N) \rangle = \sum_{e, i} \left[\left\{\tfrac{N - r_i^{(e)}}{e}\right\} - \left(\tfrac{1}{2} - \tfrac{1}{2e}\right)\right].$$

**Lemma 3.4 (target).** $E(N) = o(N)$ as $N \to \infty$.

The trivial bound is $|E(N)| \le \tfrac{1}{2} A(N) \sim \tfrac{1}{2} a_1 N$, exactly
$O(N)$ with $a_1 = R H(1) = 0.4341$. Lemma 3.4 asks for a sub-linear bound.

## 2. Fourier expansion of the saw-tooth

Use the symmetric saw-tooth $\psi(x) := \{x\} - 1/2$ for $x \notin \mathbb Z$,
extended to $\psi(x) = 0$ at $x \in \mathbb Z$ (the Bernoulli $\bar B_1$
convention). Then for $x = (N - r_i)/e$:

- If $N \not\equiv r_i \pmod e$: $\{x\} = \psi(x) + 1/2$.
- If $N \equiv r_i \pmod e$: $\{x\} = 0$ and we must add $1/2$ by hand to make
  the formula uniform: $\{x\} = \psi(x) + 1/2 - \mathbb 1[e | (N - r_i)] \cdot 1/2$.

Equivalently, with the $\bar B_1$ convention $\bar B_1(x) := \{x\} - 1/2$ for
$x \notin \mathbb Z$, $\bar B_1(x) := 0$ at $x \in \mathbb Z$:
$$\{x\} = \bar B_1(x) + 1/2 \cdot \mathbb 1[x \notin \mathbb Z].$$

Substitute and sum:
$$E(N) = \underbrace{\sum_{e, i} \bar B_1\!\left(\tfrac{N-r_i}{e}\right)}_{=: \, \Psi(N)} + \tfrac{1}{2} \sum_{e, i}\big(\mathbb 1[e \nmid (N-r_i)] - 1 + 1/e\big).$$

The second piece collapses cleanly. The number of pairs $(e, i)$ with $2 \le e \le N$,
$e\,\mathrm{sf}$, $\rho(e) \ge 1$, and $e \mid (N - r_i^{(e)})$ equals the count
of sf $e \in [2, N]$ dividing $N^2 + 1$ — equivalently, sf divisors of $N^2+1$
in $[2, N]$:
$$D_N := \#\{e \,\mathrm{sf} \mid N^2+1 : 2 \le e \le N\} \le \tau^*(N^2+1) = 2^{\omega(N^2+1)}.$$ By Erdős's
classical bound $\tau^*(m) \ll m^{\epsilon}$ for any $\epsilon > 0$ (in fact
$2^{\omega(m)} \ll \exp(c \log m / \log\log m)$, the maximal order of $\tau^*$),
we get $D_N \ll N^{\epsilon}$ for any $\epsilon > 0$. So the discrete-jump piece
contributes $O(N^\epsilon)$, which is $o(N)$.

We've reduced Lemma 3.4 to:
$$\Psi(N) := \sum_{\substack{e \,\mathrm{sf}\\ 2 \le e \le N}} \sum_{i=1}^{\rho(e)} \bar B_1\!\left(\frac{N - r_i^{(e)}}{e}\right) = o(N) \quad \text{as} \quad N \to \infty. \qquad (\star)$$

## 3. Fourier expansion of $\bar B_1$ and the resulting character sum

The standard Fourier expansion (uniformly convergent on $\mathbb R \setminus \mathbb Z$):
$$\bar B_1(x) = -\sum_{h=1}^\infty \frac{\sin(2\pi h x)}{\pi h}.$$

For any $H \ge 1$ and $x \in \mathbb R \setminus \mathbb Z$, the Vaaler
truncation gives
$$\bar B_1(x) = -\sum_{h=1}^{H} \frac{\sin(2\pi h x)}{\pi h} + O\!\left(\min\!\left(1, \frac{1}{H \|x\|}\right)\right),$$
where $\|x\|$ denotes distance to the nearest integer. (The implicit constant is
absolute; cf. Tenenbaum, *Introduction to Analytic and Probabilistic Number Theory*, I.5.4.)

Apply with $x = (N - r_i^{(e)})/e$:
$$\Psi(N) = -\sum_{h=1}^{H} \frac{1}{\pi h} \mathrm{Im}\!\left[\sum_{e, i} e^{2\pi i h (N - r_i^{(e)})/e}\right] + O\!\left(\sum_{e, i} \min\!\left(1, \frac{e}{H \|N - r_i^{(e)} \pmod e\|_e}\right)\right),$$
where $\|y\|_e := \min(y, e-y)$ for $y \in \{0, 1, \ldots, e-1\}$.

Define the "twisted root sum":
$$S_h(e) := \sum_{i=1}^{\rho(e)} e^{-2\pi i h r_i^{(e)}/e}.$$

The main term decomposes:
$$\sum_{e, i} e^{2\pi i h (N - r_i^{(e)})/e} = \sum_{e \le N, \mathrm{sf}, e \ge 2} e^{2\pi i h N/e} \cdot S_h(e) =: T_h(N).$$

So $(\star)$ reduces to two estimates:
- **(M)** *Main-term bound:* $\sum_{h=1}^{H} \frac{|T_h(N)|}{h} = o(N)$ for some choice of $H = H(N)$.
- **(R)** *Remainder bound:* $\sum_{e, i} \min(1, e/(H \|y\|_e)) = o(N)$.

## 4. Structure of the twisted root sum $S_h(e)$

The roots $r_i^{(e)}$ are the lifts via CRT of roots mod each prime $p \mid e$:
- $p = 2$: unique root $r = 1$ (no $\pm$).
- $p \equiv 1 \pmod 4$: two roots $\pm r_p$, where $r_p^2 \equiv -1 \pmod p$.

By multiplicativity (CRT), for sf $e = \prod_{p \mid e} p$ with all $p \mid e$
either $= 2$ or $\equiv 1 \pmod 4$:
$$S_h(e) = \prod_{p \mid e} S_h^{(p)}(e), \qquad S_h^{(p)}(e) := \sum_{r : r^2 \equiv -1 \pmod p} e^{-2\pi i h r \cdot (e/p)^{-1}_p / p}$$
where $(e/p)^{-1}_p$ is the inverse of $e/p$ mod $p$. (Substituting the CRT lift.)
Equivalently, since $h r/e$ mod 1 depends on $h, r, e$ only via the system of
roots mod each $p$, write $h_p := h \cdot (e/p)^{-1}_p \pmod p$ and:
$$S_h(e) = \prod_{p \mid e} \bigg(\sum_{r_p^2 \equiv -1 \pmod p} e^{-2\pi i h_p r_p / p}\bigg).$$

For $p = 2$: $S_h^{(2)} = e^{-\pi i h_2} = (-1)^{h_2}$, $|\cdot| = 1$.

For $p \equiv 1 \pmod 4$ with two roots $\pm r_p$: $S_h^{(p)} = 2\cos(2\pi h_p r_p/p)$,
$|\cdot| \le 2$.

Hence $|S_h(e)| \le 2^{\omega(e)} = \rho(e)$, with the trivial bound saturated only
when $h \cdot r_i^{(e)}/e$ is "near" an integer for all $i$ simultaneously.

**Trivial bound.** $|S_h^{(p)}| \le \rho(p)$ at each prime, hence
$|S_h(e)| \le \rho(e) = 2^{\omega(e)}$ for sf $e$ with all primes
$\equiv 1 \pmod 4$ (or $= 2$). This trivial bound is the only one we *use*
below; non-trivial Salié / Weil bounds at individual primes (which would give
$|S_h^{(p)}| \le 2$ unconditionally and via cancellation in the
$h \pmod p$ direction $\ll \sqrt p$ on average) are NOT used here, and are
the genuine analytic input that a rigorization at the level of §5 would have
to invoke.

## 5. The analytic input needed (and what it is NOT in this note)

**Target form.** *We need: there exist $H = H(N) \to \infty$ and
$\epsilon(N) \to 0$ with*
$$\sup_{1 \le h \le H(N)} \frac{|T_h(N)|}{N} \le \epsilon(N), \qquad \sum_{h=1}^{H(N)} \frac{1}{h} \le 2\log H(N).$$

*If both hold with $\epsilon(N) \log H(N) \to 0$, then the main-term part of (M)*
$$\sum_{h=1}^{H(N)} \frac{|T_h(N)|}{\pi h} \le \epsilon(N) \cdot N \cdot \frac{2\log H(N)}{\pi} = o(N).$$

*Combined with the remainder bound (R) for the same choice of $H$, we get $\Psi(N) = o(N)$
and hence Lemma 3.4.*

**Honest framing of the gap.** This note does NOT carry the bound on $T_h(N)$.
The trivial bound $|S_h(e)| \le \rho(e)$ alone gives $|T_h(N)| \le \sum_e \rho(e) = O(N)$,
which fails to give $o(N)$. To get sub-linear bounds on $T_h(N)$ one of:

- **(i)** A non-trivial bound on $|S_h(e)|$ for typical $e$ (Salié/Weil at
  prime $p$, then multiplicative aggregation), giving $|S_h(e)| \ll \rho(e)/\sqrt{p_{\min}}$
  on average; or
- **(ii)** Cancellation in the $e$-sum $\sum_{e \le N, \mathrm{sf}} e^{2\pi i h N/e} S_h(e)$,
  via Vinogradov-type estimates exploiting that $h N/e$ varies with $e$; or
- **(iii)** A direct hyperbola-method analysis as in Hooley (1957), §3 —
  the analog for $\tau^*$ rather than $\tau$.

is needed. Routes (i)-(iii) each require their own multi-session effort.

**Citation status.** *The author has not verified specific theorem numbers in
Hooley 1957* against the original paper (URL access blocked in the runtime).
What is known from secondary sources:

- Hooley (1957) "On the number of divisors of $n^2+1$ and $n^4+1$",
  *Acta Mathematica* 97, 189-210, established
  $\sum_{n \le N} \tau(n^2+1) \sim cN\log N$ via a hyperbola decomposition.
- The internal lemma controlling fractional-part fluctuations of
  $\{(N - r_i^{(e)})/e\}$ is built into Hooley's hyperbola argument; it gives
  what is essentially the $\tau$-version of $T_h(N) = o(N)$ uniformly in
  $h \le N^\eta$ (for some $\eta > 0$), via large-sieve / Erdős–Turán
  combined with arithmetic-progression equidistribution of $r_i \pmod e$.
- The $\tau^*$ analog (which is what we need: same fractional parts, but
  sf $e$ instead of all $e$) follows by the same machinery — sf $e$ is a
  *sub*set of all $e$, and the relevant character sums are multiplicatively
  cleaner.

**What to do for full rigor.** Anton's local follow-up: pull Hooley 1957 from
a non-sandbox machine and verify the precise $T_h(N)$ bound (or Erdős–Hooley
delta-function consequence in Tenenbaum III.4). A 30-minute literature session
should confirm or refute the citation.

## 6. Empirical validation

We computed $E(N)$ directly via Python sieve at $N \in \{10^3, 3 \cdot 10^3,$
$10^4, 3 \cdot 10^4, 10^5, 3 \cdot 10^5, 10^6\}$, exact integer/float computation
of $F(N)$ vs. closed-form $\langle F(N) \rangle$. Code:
`bot/scratch/F-discrepancy-empirical.py`.

| $N$ | $A(N)$ | $\Sigma_*(N)$ | $F(N)$ | $\langle F \rangle$ | $E(N)$ | $|E|/N$ | $|E|/\sqrt N$ |
|---|---|---|---|---|---|---|---|
| $10^3$ | $429$ | $4.0102$ | $220.687$ | $212.995$ | $+7.69$ | $7.7\!\cdot\!10^{-3}$ | $0.243$ |
| $3\!\cdot\!10^3$ | $1295$ | $4.4874$ | $643.550$ | $645.756$ | $-2.21$ | $7.4\!\cdot\!10^{-4}$ | $0.040$ |
| $10^4$ | $4337$ | $5.0115$ | $2183.611$ | $2166.494$ | $+17.12$ | $1.7\!\cdot\!10^{-3}$ | $0.171$ |
| $3\!\cdot\!10^4$ | $13019$ | $5.4885$ | $6550.146$ | $6507.256$ | $+42.89$ | $1.4\!\cdot\!10^{-3}$ | $0.248$ |
| $10^5$ | $43405$ | $6.0109$ | $21823.32$ | $21699.99$ | $+123.33$ | $1.2\!\cdot\!10^{-3}$ | $0.390$ |
| $3\!\cdot\!10^5$ | $130221$ | $6.4877$ | $64862.62$ | $65107.76$ | $-245.14$ | $8.2\!\cdot\!10^{-4}$ | $0.448$ |
| $10^6$ | $434069$ | $7.0103$ | $216819.65$ | $217031.49$ | $-211.85$ | $2.1\!\cdot\!10^{-4}$ | $0.212$ |

**Interpretation.**
- $|E(N)|/N$ is approaching zero with a single dip at $N = 3\!\cdot\!10^3$,
  consistent with **Lemma 3.4 ($E = o(N)$)**.
- $|E(N)|/\sqrt N \in [0.17, 0.45]$ excluding the single dip at $N = 3\!\cdot\!10^3$
  (where the value is $0.040$, an outlier from the small-$E$ sign change). Bounded
  across the remaining 6 scales, consistent with $|E(N)| = O(\sqrt N (\log N)^c)$ —
  the classical heuristic rate (cf. `P12-c0T-secondary-constant.md` Cor 3.2 caveat).
  *The lower bound of the cited range depends on which dip points are included;
  with only 7 data points, the range itself has fluctuation comparable to its width.*
- The signs of $E$ are not monotone — $E$ is genuinely fluctuating, not
  systematically biased. This is consistent with the "central limit"-type
  fluctuation expected from $\sqrt N$ scaling.

Empirical evidence strongly supports both Lemma 3.4 and the stronger pointwise
$O(\sqrt N \log^c N)$ claim. (Pointwise bound is *not* needed for any current
limit-statement; only the qualitative $o(N)$ is needed.)

## 7. Status and what's left

**Achieved this session.**
1. Reduced Lemma 3.4 to the saw-tooth bound $\Psi(N) = o(N)$ where
   $\Psi(N) := \sum_{e \le N, \mathrm{sf}, e \ge 2}\sum_i \bar B_1((N - r_i^{(e)})/e)$,
   modulo a discrete-jump correction of size $O(2^{\omega(N^2+1)}) = O(N^\epsilon)$.
   *(This reduction step is rigorous: §2 derivation is elementary.)*
2. Fourier-expanded $\Psi(N)$ to obtain a Vaaler decomposition
   $\Psi = \text{(main)} + \text{(remainder)}$, with main term controlled by
   $|T_h(N)|/h$ for $h \le H$ and remainder by $\sum \min(1, e/(H \|y\|))$.
   *(Decomposition is rigorous; the bounds on the two pieces are NOT carried
   in this note.)*
3. Identified the multiplicative structure $S_h(e) = \prod_{p \mid e} S_h^{(p)}$
   with $|S_h^{(p)}| \le \rho(p) = 2$ at split $p$ (and $1$ at $p = 2$),
   giving the trivial bound $|S_h(e)| \le \rho(e)$.
4. Empirically verified $|E(N)|/N \to 0$ at $N \le 10^6$, with rate consistent
   with $|E(N)| = O(\sqrt N \log^c N)$.

**Not achieved this session.**
- The bound $T_h(N) = o(N)$ uniformly in $h$. Without it, the Fourier reduction
  in §3 does not yield a sub-linear estimate on $\Psi(N)$. The trivial bound
  on $|S_h(e)|$ gives $|T_h(N)| \le A(N) = O(N)$, exactly $O(N)$ not $o(N)$.
- A verified citation. Route (iii) of §5 — Hooley 1957's hyperbola method for
  $\tau$ — is *plausibly* the right reference for the $\tau^*$ analog, but
  the author has not pulled the original paper to verify.

**Honest framing of progress.** This note delivers two verifiable items:
- **(a)** A clean, rigorous identification: Lemma 3.4 is equivalent (modulo
  $O(N^\epsilon)$ jumps) to $\Psi(N) = o(N)$, where $\Psi$ is a sum of $\bar B_1$
  evaluated at fractions $(N - r_i^{(e)})/e$ over sf $e \le N$ with $\rho(e) \ge 1$.
- **(b)** Strong empirical evidence ($|E|/\sqrt N$ bounded across 6/7 scales) that
  $E(N) = o(N)$ with the heuristic $\sqrt N$ rate.

What this note does NOT deliver:
- A self-contained sub-linear bound on $T_h(N)$ — that is the actual analytic
  content and remains tied to a specific Tenenbaum/Hooley citation that has
  not been freshly verified.
- A reduction in the SET of unrigorized analytic steps invoked by
  `P12-B-infty-existence-equivalence.md`. The unrigorized step there was
  exactly Lemma 3.4 = "$E(N) = o(N)$"; the unrigorized step here is
  "$T_h(N) = o(N)$". This is a *re-statement* in cleaner Fourier form,
  not a *reduction* in difficulty. The cleaner form should make literature
  search easier; the analytic difficulty is unchanged.

## 8. Files

- This note: `n2+1 ai thoughts/notes/proofs/P12-Lemma-3-4-reduction.md`.
- Empirical script: `bot/scratch/F-discrepancy-empirical.py` (runs $N = 10^6$
  in $\sim 30$ s).
- Builds on: `P12-c0T-secondary-constant.md` (Cor 3.2),
  `P12-B-infty-existence-equivalence.md` (Lemma 3.4).

## 9. Falsifiable forecast

**(F1)** At $N = 10^7$, $|E(N)|/\sqrt N$ remains in $[0.05, 0.5]$. Any value
$\ge 1$ would refute the $O(\sqrt N)$ heuristic; any value $\le 0.01$ would
suggest a hidden cancellation faster than $\sqrt N$.

**(F2)** $E(N)/N \to 0$ uniformly: at $N = 10^7$, $|E|/N \le 10^{-3}$.
