# Round 4 — Proof of Theorem C and final sign-off

After three rounds of review settled Theorems A, A', B, and D, **Theorem C** (the cancellation bound on $T(N)$) had been retracted to an honest "Conjecture C" with only a sketch of $T(N) = o(N \log N)$. The user requested a serious push to actually prove a non-trivial unconditional bound.

## The proof I produced

**Theorem C.** $T(N) = O(N)$ unconditionally, with
$$|T(N)| \le 2 \sum_{d \in L_{\mathrm{odd}}, \, d \le N} 2^{\omega(d)} \sim 2cN, \quad 2c \approx 0.637.$$

**Six-step proof**:
1. **Hyperbola.** $\tau(n^2+1) = 2 \cdot \#\{d : d | n^2+1, 1 \le d \le n\}$ since $n^2+1$ is never a square for $n \ge 1$.
2. **Restrict $d$.** $\rho(d) := \#\{x : x^2 \equiv -1 \pmod d\} > 0$ iff $v_2(d) \le 1$ and all odd prime factors $\equiv 1 \pmod 4$.
3. **Even $d$ contribute zero.** If $d = 2d'$, every $n_0$ is odd, so $n$ is odd, so $\chi_4(n+1) = 0$.
4. **Inner AP-sum bound.** For $d$ odd with $\rho(d) > 0$: the AP-sum of $\chi_4(n+1)$ has $|S(d, n_0)| \le 1$, since $\gcd(d, 4) = 1$ and $\chi_4$ has full period-4 cancellation.
5. **Combine.** $|T(N)| \le 2 \sum_{d \in L_{\mathrm{odd}}, \, d \le N} \rho(d) \cdot 1 = 2 \sum 2^{\omega(d)}$.
6. **Selberg–Delange.** $\sum_{d \le N, d \in L_{\mathrm{odd}}} 2^{\omega(d)} \sim cN$ since the Dirichlet series has $\kappa = 1$.

## Skeptic's round-4 verdict (verbatim verification)

The skeptic verified each step:

> **Issue list:**
>
> 1. **MINOR — Step 1 hyperbola, off-by-one.** Author writes `1 ≤ d ≤ n`, not `d ≤ √(n²+1)`. Verified: for n ≥ 1, n² < n²+1 < (n+1)², so n < √(n²+1) < n+1, hence "d ≤ n" and "d < √(n²+1)" cut out the same divisor set. n²+1 is never a square for n ≥ 1. The pairing d ↔ (n²+1)/d is a strict involution (no fixed point since not a square), and (n²+1)/d ≥ n+1 iff d ≤ (n²+1)/(n+1) = n − (n−1)/(n+1) < n, with equality d = n only if n | 1. So the partition into {d ≤ n} ⊔ {d ≥ n+1} is exact and balanced, giving τ(n²+1) = 2·#{d|n²+1, d ≤ n}. **Correct.**
>
> 2. **MINOR — Summation swap.** Valid: for fixed d, the constraint "d ≤ n ≤ N and d | n²+1" exactly matches the inner condition "d | n²+1, 1 ≤ d ≤ n" once you swap order. **Correct.**
>
> 3. **MINOR — Step 2 (ρ structure).** Verified directly: ρ(2)=1, ρ(4)=0, ρ(5)=2, ρ(8)=0, ρ(10)=2, ρ(13)=2, ρ(25)=2, ρ(65)=4. The classical claim ρ(d) > 0 ⟺ v₂(d) ≤ 1 and all odd prime factors ≡ 1 mod 4, with ρ(d) = 2^ω(d_odd), is standard CRT + Hensel. **Correct.**
>
> 4. **MINOR — Step 3 (even d kill).** For d = 2d′ with d′ odd ∈ L_odd, every solution n₀ to x² ≡ −1 (mod d) has parity {1} (odd). Reason: x² ≡ −1 (mod 2) forces x ≡ 1 (mod 2). So n ≡ n₀ (mod 2d′) ⇒ n odd ⇒ n+1 even ⇒ χ₄(n+1) = 0. **Correct.**
>
> 5. **MINOR — Step 4 (AP-sum bound).** Tested for d ∈ {1,3,5,7,9,15,25,65} and all offsets n₀ mod d, all lengths up to 200: max |partial sum| = 1 in every case. Reason: gcd(d,4) = 1 since d odd, so n+1 = (n₀+1) + jd cycles through all 4 residues mod 4 with period 4 as j varies, summing to 0. The remainder of ≤ 3 terms gives partial sums in {0, ±1}. **Correct.**
>
> 6. **MINOR — Step 5 (combining).** Just |∑| ≤ ∑|·|, with ρ(d) = 2^ω(d) for d ∈ L_odd. **Correct.**
>
> 7. **SERIOUS — Step 6 (Selberg–Delange citation, but conclusion holds).** The Euler product computation is correct: at p ≡ 1 mod 4, the local factor is 1 + 2/p^s + 2/p^{2s} + … = (1 + p^{-s})/(1 − p^{-s}). The Dirichlet series F(s) = ζ(s)·L(s,χ₄) up to bounded factor: F(s)/[ζ(s)L(s,χ₄)] = ∏_{p≡1(4)} (1-p^{-2s}) · ∏_{p≡3(4)} (1-p^{-2s}) · (1-2^{-s}), which is bounded and analytic for Re(s) > 1/2. Hence F(s) ~ (residue) · 1/(s−1) near s=1 with κ = 1, and Selberg–Delange (or just Wirsing/Tenenbaum II.5 Thm 5.2) gives ∑_{d≤N} f(d) ~ cN. The author's verification of κ=1 via ∑_p f(p)/p = log log X + O(1) is correct. **The result is correct.** The citation is loose but the conclusion holds.
>
> 8. **MINOR — d=1 boundary case.** d=1 gives ρ(1)=1, n₀=0, AP is all of [1,N]; |S(1,0)| ≤ 1 holds. Contributes 2·1 = 2.
>
> 9. **MINOR — d=N edge.** AP of length 1, |S| ≤ 1 trivially.
>
> 10. **MINOR — The author claims `O(1)` correction term in `|T(N)| ≤ 2∑… + O(1)`.** Where does the O(1) come from? There is no O(1) error in Step 1 for n ≥ 1. So the `+O(1)` is harmless slack but technically unjustified — author should write `=` not `≤ … + O(1)`. **Cosmetic.**
>
> 11. **MINOR — Asymptotic vs explicit constant.** Step 6 yields `~ cN`, an asymptotic; the displayed bound `≤ cN + O(1)` with c ≈ 0.637 is then an asymptotic upper bound, not a uniform-in-N inequality. To get a true uniform inequality requires effective Selberg–Delange (which exists, but with a different constant + explicit error). The displayed table shows bound/N converging from above to 0.637, consistent with `2∑_{d≤N} 2^ω(d)/N → 2c`. So `O(N)` is rigorous, but the explicit `0.637·N` only holds asymptotically. **Author should clarify.**
>
> ## Numerical confirmation
>
> | Check | Verified |
> |---|---|
> | n²+1 never a square, n ∈ [1,1000] | Yes |
> | τ(n²+1) = 2·#{d≤n : d|n²+1}, n ∈ [1,200] | Yes |
> | ρ(d) values for d ∈ {2,4,5,8,10,13,25,65} | Match author |
> | All n₀ for d=2d′ are odd, d′ ∈ {1,5,13,25,65} | Yes |
> | Max AP-partial-sum |S(d,n₀)| over d ∈ {1,3,5,7,9,15,25,65} = 1 | Yes |
> | 2·∑_{d∈L_odd, d≤N} 2^ω(d)/N at N=5000 ≈ 0.634 | Matches author's 0.637 |
>
> ## Consensus
>
> **YES, I agree the proof of Theorem C as written is correct and unconditional**, modulo the cosmetic objections #10 (the spurious `+O(1)`) and #11 (the constant 0.637 is asymptotic, not uniform). All six steps are verified empirically and structurally.
>
> The proof represents a genuine $\log N$ improvement over trivial. It does not approach the empirical $\sqrt{N}$, as the author honestly notes — that gap requires real analytic NT (Conjecture C, line 168).

## Author's response — cosmetic fixes applied

Both cosmetic objections addressed in the final draft:

- **(#10):** Removed the spurious `+O(1)`. Now: $|T(N)| \le 2 \sum_{d \in L_{\mathrm{odd}}, d \le N} 2^{\omega(d)}$ (equality is what's proved up to swap).
- **(#11):** Clarified that the bound RHS is asymptotic to $\sim cN$ and the rigorous uniform conclusion is $|T(N)| = O(N)$. The constant $2c \approx 0.637$ is empirically verified but does not give a uniform-in-$N$ inequality without effective Selberg–Delange.

## Final status

After four rounds and four substantive revisions, **Theorems A, A', B, C, D and Proposition C1** all signed off as **correct as stated**:

- **Theorem A** — pointwise determinant identity $\chi_4(a-b)\chi_4(c+d) = \chi_4(n+1)$.
- **Theorem A'** — second linear-form identity $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1)$.
- **Theorem B** — bilinear-to-divisor reduction.
- **Theorem C (NEW, proven this round)** — $T(N) = O(N)$ unconditionally via hyperbola + Selberg–Delange.
- **Theorem D** — sharp linear-form classification.
- **Proposition C1** — supplanted by the stronger Theorem C.

Open: **Conjecture C** ($T(N) \ll \sqrt N$), would require subconvexity for an appropriate Hecke L-function over $\mathbb{Q}(i)$.

## Lessons from round 4

The previous Theorem C (round 1) was a bluff — I had pattern-matched to "$O(N^{1/2+\varepsilon})$ via Hooley" without doing the work, and the skeptic correctly called it out. The honest path was:

1. **Compute first.** Empirically check whether $T(N)$ has the structure I'm claiming.
2. **Find the right swap.** Hyperbola decomposition + arithmetic-progression splitting.
3. **Identify the correct AP-sum cancellation.** $\chi_4$ has period 4; for AP step coprime to 4, partial sums are bounded by 1. **For step divisible by 4, no cancellation** — but those $d$ have $\rho(d) = 0$, so they don't contribute.
4. **Identify the correct counting.** $\sum_{d \le N, d \in L_{\mathrm{odd}}} 2^{\omega(d)}$ — Selberg–Delange gives the linear bound.
5. **Even $d$ kill themselves.** Without this observation, the bound would face a real obstruction; with it, the proof goes through cleanly.

The result is a $\log N$ improvement over trivial — modest but real, and rigorous.
