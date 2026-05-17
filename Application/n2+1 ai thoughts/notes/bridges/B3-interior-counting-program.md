# Interior-counting program

## The goal

Recast Landau's 4th problem as a quantitative density question on the [[../concepts/12-boundary-vs-interior|interior of the $\Phi_0$ tree]], and identify the smallest sub-question whose resolution would give a result.

## The reformulation chain

[[../concepts/10-landau-fourth-problem|Landau's 4th]] reformulates as:

**(L1)** $\#\{n \le N : n^2 + 1\ \text{prime}\} \to \infty$ as $N \to \infty$.

**(L2)** $\#\{n \le N : \tau(n^2+1) = 2\} \to \infty$.

**(L3)** $\#\{n \le N : |\mathcal{S}^{-1}(n)| = 2\} \to \infty$, where $\mathcal{S}$ is the [[../concepts/14-S-sequence|S-sequence]].

**(L4)** $\#\{n \le N : \nexists\ A \in SL_2(\mathbb{N})\ \text{with}\ ac+bd = n\} \to \infty$.

**(L5)** Define the **cross-term map**
$$\chi : SL_2(\mathbb{N}) \to \mathbb{N},\qquad \chi(A) = ac + bd.$$
Then: the **complement** of $\chi(SL_2(\mathbb{N}))$ in $\mathbb{N}$ is **infinite**.

## Counting the image

$\chi$ sends matrices to natural numbers. By [[../concepts/13-prime-characterization|the divisor count theorem]]:
$$\#\chi^{-1}(n) = \tau(n^2+1) - 2$$
(subtract 2 for the boundary matrices $S^n$ and $T^n$).

So the *total weight* of $\chi$ on values $\le N$ is
$$\sum_{n \le N} (\tau(n^2+1) - 2) = \sum_{n \le N} \tau(n^2+1) - 2N \approx 4N \log N - 2N + O(\text{lower})$$
(by classical results on average $\tau(n^2+1)$).

So $\sim 4 \log N$ matrices in $SL_2(\mathbb{N})$ map to a typical $n$. **Most $n$ are hit, but lopsidedly.**

## Reformulation as a covering problem

We want to show:
$$\mathbb{N} \setminus \chi(SL_2(\mathbb{N}))\ \text{is infinite.}$$

The image $\chi(SL_2(\mathbb{N}))$ is a *set* — a subset of ℕ. Its **density** (if it exists) measures how often a random $n$ is the cross-term of some interior matrix. By Bateman–Horn:
$$\#\{n \le N : \tau(n^2+1) > 2\} = N - \pi_{\phi_0}(N) \sim N - C\sqrt N / \log N$$

So the image has density 1 (asymptotically full). The *complement* — Landau primes — has density 0 but conjecturally infinite cardinality.

This is the **density 0 + infinite cardinality** regime, where neither pure measure-theoretic nor pure counting arguments suffice. We need a **structural** reason that the complement is infinite.

## Sub-program: structural obstructions to being in the image

For each *prime* $p$:

- $p \in \chi(SL_2(\mathbb{N}))$ iff $p^2 + 1$ is composite (i.e. $\tau(p^2+1) > 2$).
- $p \in \mathbb{N} \setminus \chi(SL_2(\mathbb{N}))$ iff $p^2 + 1$ is prime.

Restated: we want to show that for ∞ many primes $p$, the value $p^2 + 1$ is also prime. (This is equivalent to Landau by reduction.)

A subprogram: study the **map $p \mapsto \tau(p^2+1)$ over primes $p$**.
- Average $\tau(p^2+1)$ over primes up to $N$?
- Variance?
- Does $\tau(p^2+1) = 2$ have positive density among primes?

These are themselves open, but **partial results exist** — see Iwaniec, Friedlander, etc. ([[../research/R1-iwaniec-and-sieves]]).

## Sub-program: parameterize the interior

Length of an SL₂(ℕ₀) word as $S/T$-string — call it $\ell(A)$. Then:

$$|SL_2(\mathbb{N}_0)|_{\ell \le k} = 2^{k+1} - 1 \quad (\text{nodes in a depth-}k\ \text{binary tree})$$

The cross-term values $\chi(A)$ for $A$ of word-length $k$ sit roughly in the range $[k, F_{2k}]$ where $F$ is Fibonacci-like — consistent with the matrix entry growth.

So:
$$\#\{A \in SL_2(\mathbb{N}_0) : \chi(A) \le N\} \asymp ?$$

This needs the [[../research/R5-thin-groups-affine-sieve|thin-group counting]] machinery. Schmidt-style "counting matrices in thin sets" theorems should apply.

**Concrete subproblem**: prove that
$$\#\{A \in SL_2(\mathbb{N}) : \chi(A) \le N\} = N \log N \cdot G(\log\log N) + O(\text{error})$$
for some explicit $G$ (related to the spectral gap of the SL₂(ℕ₀) action). Once this is known, **fluctuations** can be analyzed.

## Local-global heuristic

For each prime $q$, ask: does $\chi(A) \equiv n \pmod q$ have solutions $A \in SL_2(\mathbb{N}/q)$?

If "yes for all $q$" but "no for $\mathbb{Z}$", that's a local-global failure. By analogy with Bourgain–Kontorovich's work on Zaremba's conjecture, the **local-global principle** typically holds for thin orbits (via expander estimates).

But our situation is different: the integers $n$ where $\chi$ does NOT take the value $n$ are exactly the Landau primes. Local-global SHOULD say: $n$ is locally a value of $\chi$ for every prime $q$, *but* globally it's not. **The obstruction is precisely $n^2 + 1$ being prime.**

This is unusual — the obstruction is itself the conjecture we want to prove.

## Where to push next

The most promising sub-question, in order of feasibility:

1. **(Easy)** Compute $\chi(SL_2(\mathbb{N}))$ explicitly for $n \le 10^4$ and check Hardy–Littlewood prediction.
2. **(Medium)** Prove a lower bound for the density of $\{n : |\mathcal{S}^{-1}(n)| \le K\}$ for any fixed $K$, using regularity of $\mathcal{S}$. This would give $\tau(n^2+1) \le K$ for ∞ many $n$ — a result on small divisor counts.
3. **(Hard)** Translate Iwaniec's $P_2$ theorem into the language of $\chi(SL_2(\mathbb{N}))$ — count interior matrices with $\chi(A) = n$ for $n$ such that $n^2+1$ is "almost prime."
4. **(Open frontier)** Develop a transfer operator / spectral gap on the $\Phi_0$ tree and prove a spectral inequality forcing a positive density of primes. See [[B5-affine-sieve-attack]].
