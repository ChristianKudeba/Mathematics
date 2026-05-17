---
name: P12 sigma-spin identity finding (May 2026 session)
description: First multiplicative-character spin on SL_2(N_0) that gives empirical square-root cancellation in the bilinear sum, succeeding where P1's word-parity and P3's angular Hecke characters fail
type: project
originSessionId: 36ff7212-a3cd-4ed2-b366-ebff4b57622b
---
In a 60-min "think hard" session on 2026-05-02, I identified a NEW multiplicative spin on the Shakov SL_2(N_0) bilinear sum that achieves empirical GRH-strength square-root cancellation. Saved as `notes/proofs/P12-pointwise-spin-identity.md`.

## The character

$\sigma: \mathbb{Z}[i] \setminus (1+i)\mathbb{Z}[i] \to \{\pm 1\}$, the multiplicative *ramified quadratic* Hecke character of conductor $(1+i)^3$. Defined by $\sigma(\alpha) := u_\alpha^2$ where $\alpha = u_\alpha \cdot \alpha_0$ with $\alpha_0 \equiv 1 \pmod{(1+i)^3}$ primary and $u_\alpha \in \{\pm 1, \pm i\}$.

$\sigma$ is trivial on rational integers; it distinguishes the two split conjugates above each rational prime $p \equiv 1 \pmod 4$.

## The pointwise identity

For every $A = (a,b,c,d) \in SL_2(\mathbb{N}_0)$ with $\det A = 1$:
$$\sigma(a-bi) \cdot \sigma(c+di) = \sigma((a-bi)(c+di)) = \sigma(n+i) = \chi_4(n+1)$$
where $n = ac+bd = \chi(A)$, and the value is 0 for $n$ odd (since then $1+i \mid n+i$).

This is multiplicativity of $\sigma$ specialized to the Diophantus factorization $\xi\eta = n+i$.

## The cumulative cancellation (empirical)

$T(N) := \sum_{A \in SL_2(\mathbb{N}_0): \chi(A) \le N} \sigma(\xi)\sigma(\eta) = \sum_{n \le N} \tau(n^2+1) \chi_4(n+1)$.

Verified up to $N = 10^7$:
- $|T(N)|/\sqrt N \in [0.06, 1.45]$ across $N \in \{10^3, 10^4, ..., 10^7\}$
- Suggests $T(N) \ll \sqrt N$ — GRH-strength.

## Why this matters / why this fails to immediately give Landau

**Matters because**:
- First spin in the Shakov framework with power-saving cancellation. P1's word-parity spin has linear positive bias from boundary spines ($+N$), partial-but-not-power-saving interior cancellation. P3's angular Hecke characters degenerate on the slice (angles → 0).
- The pointwise reduction to a single twisted divisor sum, via a *ramified* (not angular) character, is the key structural innovation — slice cycles through $\bmod (1+i)^3$ residues even as angles trivialize.
- This is the natural opening to the Plancherel route: decompose Type-II inputs along Hecke characters; if each $T_{\psi_1, \psi_2}$ has $O(N^{1-\delta})$ cancellation uniformly, the FI bilinear conjecture holds.

**Fails to immediately give Landau because**:
- The FI sieve needs the bilinear bound for *arbitrary* Type-II inputs, not just $\sigma\otimes\sigma$. Other Hecke characters (especially the angular ones, despite their on-slice degeneration) need to be bounded too.
- The cross-pairings $T_{\psi_1, \psi_2}$ with $\psi_1 \ne \psi_2$ have not been computed.
- The cumulative sum likely corresponds to a known shifted convolution result; the novelty is the structural collapse, not the cancellation strength itself.

## How to apply going forward

1. Compute $T_{\psi_1, \psi_2}(N)$ for ($\sigma$, angular $\chi_{4k}$) and ($\chi_{4k_1}, \chi_{4k_2}$) cross-pairings.
2. Identify the precise $L$-function whose value gives $T(N)$. Likely a quadratic-twist of a Hecke L-function on $\mathbb{Q}(i)$.
3. Repeat the construction for $\phi_1, \psi_2, \phi_3$: each has analogous primary-normalization in its quadratic order, giving an analogous $\sigma_f$ character.
4. Plug $\sigma$-bilinear cancellation into the FI sieve: trace through which Type-II inputs reduce to $\sigma$-pairings vs which need other characters.

## Status update (after 4 rounds of adversarial review, May 2026)

**The original σ-character claim was wrong** (the function I computed wasn't the multiplicative Hecke σ). Corrected character: $\rho(A) = \chi_4(a-b)\chi_4(c+d)$ — a product of two simple Dirichlet characters mod 4 applied to LINEAR functionals of the matrix entries. NOT multiplicative on Z[i], but the bilinear identity follows from the determinant constraint $-2bd \equiv 0 \pmod 4$ (since $bd$ is even when both $\chi_4$ factors are nonzero).

**Five proven results (after referee approval):**
- Theorem A: $\chi_4(a-b)\chi_4(c+d) = \chi_4(n+1)$ pointwise.
- Theorem A': $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1)$ pointwise.
- Theorem B: $T(N) = \sum_{n=1}^N \tau(n^2+1)\chi_4(n+1)$.
- **Theorem C (unconditional): $T(N) = O(N)$.** Proof via Hooley hyperbola, key cancellation: AP-sums of $\chi_4$ on odd-step APs are $|S| \le 1$, and even-step APs contribute zero because $n_0$ is forced odd by $\rho(2)=1$. Selberg–Delange gives the linear count.
- Theorem D: at conductor 4, only $(a-b, c+d)$ and $(a+b, c-d)$ identities exist (sharp classification).

**Open: Conjecture C** — empirical $T(N) \ll \sqrt N$ over $N \le 10^7$. Would require subconvexity for a Hecke L-function over $\mathbb{Q}(i)$.

**Files**: `n2+1 ai thoughts/notes/proofs/P12-pointwise-spin-identity.md` (proofs), `notes/proofs/P12-review-transcript/` (4-round adversarial review transcript).
