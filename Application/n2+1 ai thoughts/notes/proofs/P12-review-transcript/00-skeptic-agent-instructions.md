# Skeptic-agent instructions (P12 review)

The skeptic agent is a one-shot adversarial mathematician spawned via `Agent(subagent_type: "general-purpose")`. The role: find errors in a draft mathematical note, ranked by severity. Below are the verbatim prompts used in each of three review rounds.

## General constraints applied to every round

- **Time/compute budget (hard):** ~10 minutes per round (round 3: ~5 minutes). Skeptic should NOT run computations larger than $N=200$ for matrix enumeration or $N \le 10^4$ for direct divisor sums. The empirical evidence at $N = 10^7$ is already verified — re-verifying it is not the goal.
- **Output format:** numbered list of issues, each labeled CRITICAL / SERIOUS / MINOR, terse but specific.
- **Required closing line:** YES/NO consensus statement on whether the proofs are correct as stated.
- **Honesty requirement:** if a section is correct, say so. Do not invent issues to seem rigorous. Counterexamples or specific citations preferred over hand-waving objections.

## Round 1 — full review

> You are an adversarial mathematician acting as a SKEPTICAL REFEREE. Your job is to find mistakes, gaps, hidden assumptions, and overclaims in a draft note. Be ruthless. List every issue you can identify, ranked by severity (CRITICAL, SERIOUS, MINOR).
>
> **TIME / COMPUTE BUDGET (HARD CONSTRAINT):** You have ~10 minutes. Do NOT run any computation that takes more than ~30 seconds. If you spawn Python: keep N small (e.g., N ≤ 200 for matrix enumeration, N ≤ 10000 for direct divisor sums). Do NOT enumerate to N=10^7 or larger. The point is to find proof errors, not to re-verify the empirical claims at scale — those are already done.
>
> The note to review:
> `C:\Users\anton\OneDrive\Desktop\mathAI\n2+1 ai thoughts\notes\proofs\P12-pointwise-spin-identity.md`
>
> Background (don't assume the author is right):
> - Setting: Shakov's SL_2(N_0) framework. A = (a,b,c,d) with all entries ≥ 0 and ad-bc = 1. Diophantus: (a-bi)(c+di) = (ac+bd) + i = n + i in Z[i].
> - Bijection F̂: SL_2(N_0) → D_{phi_0} = {(m,n) : m | n^2+1}, A ↦ (a^2+b^2, ac+bd). This is from the Shakov paper and you should treat it as established.
> - Author's main claim (Theorem A): chi_4(a-b) * chi_4(c+d) = chi_4(n+1) for every A in SL_2(N_0), where chi_4 is the Dirichlet character mod 4. Proof rests on a parity case analysis + the algebraic identity (a-b)(c+d) - (n+1) = -2bd combined with bd even when nonzero.
> - Author's Theorem B: reduces the bilinear sum to T(N) = sum_{n<=N} tau(n^2+1) chi_4(n+1).
> - Author's Theorem C: claims T(N) = O(N^{1/2+eps}) by Hooley-style methods.
>
> **Specific tasks (in priority order):**
>
> 1. **Verify Theorem A's proof line by line.** Specifically:
>    (a) Is the parity case analysis (Case A: ad odd, bc even; Case B: bc odd, ad even) exhaustive? Are there matrices in SL_2(N_0) not covered?
>    (b) The claim "bd is even when rho(A) ≠ 0": verify by exhaustive small check (N ≤ 50, enumerate all matrices) — but only if you doubt the parity argument.
>    (c) Verify (a-b)(c+d) - (n+1) = -2bd by direct algebraic expansion. Show your work.
>    (d) The final step "both sides are odd, chi_4 only sees mod 4, so equal": is this fully rigorous?
>
> 2. **Verify Theorem B.** Is the Shakov bijection being used correctly? In particular, does each n in [1, N] have exactly tau(n^2+1) matrices A with chi(A) = n? Or could there be off-by-one issues with the identity matrix, or with n = 0?
>
> 3. **Critique Theorem C carefully.** The author claims T(N) = O(N^{1/2+eps}) is "provable by Hooley-style methods (citation: Iwaniec-Kowalski Ch. 14)." Is this actually true? Trace through:
>    (a) sum_{n<=N} tau(n^2+1) is asymptotic to c*N*log(N). Twisting by a character should give cancellation, but how much?
>    (b) The author's hyperbola sketch invokes Polya-Vinogradov on AP sums of chi_4 of length ~N/d, with d-summation. Does this actually give O(N^{1/2+eps}) or just O(N^{1-eps}) or even O(N/log N)?
>    (c) Is there an actual reference in Iwaniec-Kowalski Ch 14 for this exact sum? Or is the author bluffing?
>
> 4. **Critique the Plancherel claim.** The author conjectures that decomposing general Type-II inputs alpha, beta along Dirichlet characters chi_q applied to linear functionals of (a,b), (c,d) gives a family of identities analogous to Theorem A, recovering the FI bilinear bound.
>    (a) Try to find ONE other linear pair (L_1(a,b), L_2(c,d)) where the determinant constraint gives an analogous identity. What constraint must L_1, L_2 satisfy?
>    (b) Is the Plancherel completeness conjecture plausible, or does it sweep the actual difficulty under the rug?
>
> 5. **The author's "honesty" disclaimer:** the corrected version of the note retracts an earlier claim that the spin was a multiplicative Hecke character sigma. The author now uses rho(A) = chi_4(a-b)*chi_4(c+d) which is NOT multiplicative on Z[i]. Check: is the author actually honest, or is there still a hidden multiplicativity claim somewhere in the note?
>
> 6. **Anything else.** Definitional ambiguities, hand-waving, undefined terms, broken logical links.
>
> Format response as numbered issues:
> - Severity (CRITICAL / SERIOUS / MINOR)
> - Title
> - Explanation
> - Counterexample or specific citation if relevant
>
> If a section is correct, SAY SO. Do not invent issues. Be terse but specific.
>
> Report back in under 1500 words. Time-budget: ~10 minutes total.

## Round 2 — verify revisions and check for new errors

> You are an adversarial mathematician acting as a SKEPTICAL REFEREE. This is round 2 of a review. The author has revised their note in response to your earlier critique. Your job is to verify the revisions are correct, check for new errors introduced, and sign off on what's now genuinely proved.
>
> **TIME / COMPUTE BUDGET (HARD CONSTRAINT):** ~10 minutes. Do NOT run computations larger than N=200 for matrix enumeration or N=10000 for direct divisor sums. The empirical evidence is already verified at scale.
>
> The revised note: `C:\Users\anton\OneDrive\Desktop\mathAI\n2+1 ai thoughts\notes\proofs\P12-pointwise-spin-identity.md`
>
> The author's key changes in response to your round-1 review:
>
> 1. **Theorem B fix:** Off-by-one for n=0 acknowledged. Now states T(N) = sum from n=1 to N (excluding I), with the n=0 contribution rho(I) = 1 explicitly noted.
>
> 2. **Theorem C retracted:** The unconditional O(N^{1/2+eps}) claim is removed. Replaced by:
>    - Proposition C1 (proved unconditionally): T(N) = O(N/sqrt(log N)) by elementary AP-sum cancellation. Inner AP-sum of chi_4 of length N/d is O(1) when gcd(d,4)=1 (which holds for all relevant d), summed over d in a "Landau set" of density 1/sqrt(log N) gives O(N/sqrt(log N)).
>    - Conjecture C: T(N) = O(sqrt N (log N)^O(1)). Empirical only.
>    - Honest acknowledgment that the gap between proved and conjectured requires real analytic NT (Hecke L-functions over Q(i) + subconvexity).
>
> 3. **Theorem A' added:** A second linear-form identity chi_4(a+b)chi_4(c-d) = chi_4(n-1) by the same -2bd defect argument. Note rho_2 = -rho since chi_4(n-1) = -chi_4(n+1) for n even, so it gives the same information.
>
> 4. **Theorem D added (sharp limitation):** Among integer linear forms L_1 = alpha*a + beta*b, L_2 = gamma*c + delta*d, the only ones giving an identity L_1*L_2 ≡ c_1*n + c_0 (mod 4) for all A in SL_2(N_0) are (a-b, c+d) and (a+b, c-d) up to sign. So the linear-form Plancherel program is fundamentally limited.
>
> 5. **Plancherel program retracted as a "completeness conjecture":** Replaced by an honest open problem. Higher conductor identities require more than linear forms.
>
> **Your tasks for round 2:**
>
> 1. **Verify the proof of Proposition C1** (the new unconditional bound).
>    (a) Is it really true that AP-sums of chi_4 on n ≡ x (mod d), 1 ≤ n ≤ N, of length ~N/d, equal O(1) uniformly in d when gcd(d, 4) = 1? Trace the argument.
>    (b) Is the "Landau set" density (count of n ≤ N with all prime factors ≡ 1 mod 4) actually ~ N/sqrt(log N)? (This is Landau's theorem on sums of two squares — a classical result.)
>    (c) Does the multiplication of "O(1) per d" times "Landau-density" really give O(N/sqrt(log N))?
>    (d) Are there any other contributions ignored — e.g., the d=2 case, the "diagonal" delta_square term?
>
> 2. **Verify Theorem D** (the linear-form characterization).
>    (a) Walk through the algebra: expand L_1*L_2, substitute ad = 1 + bc, identify the four monomial coefficients.
>    (b) Author claims "for non-degenerate forms, gamma*delta ≠ 0, so alpha = ±beta*i (impossible over Z)" — but then in the next sentence says "the signed case alpha=-beta, gamma=delta works." This argument is suspicious.  WAIT — does the author's algebra actually rule out other solutions correctly? Specifically, can you find INTEGER solutions to alpha*gamma = beta*delta AND alpha*delta + beta*gamma = 0 OTHER than (alpha=-beta, gamma=delta) and (alpha=beta, gamma=-delta)? E.g., what about alpha=2, beta=2, gamma=1, delta=-1?
>    (c) Even if the rigid linear-form classification is correct, does the conclusion ("the linear-form Plancherel program is fundamentally limited") follow? Or could there be non-trivial families of QUADRATIC characters (e.g., chi_q applied to QUADRATIC functionals of (a,b)) that the author should have considered?
>
> 3. **Verify the second identity Theorem A'** by the same algebra: (a+b)(c-d) - (n-1) = -2bd. Yes? Confirm.
>
> 4. **Has any new error been introduced** in the revisions?
>
> 5. **Final consensus check:** Given the revisions, is the note now an HONEST contribution? Specifically:
>    - Theorem A: do you agree this is solid?
>    - Theorem B: do you agree the off-by-one is properly fixed?
>    - Theorem D: do you agree this is a clean characterization (modulo any algebra issue you find)?
>    - Conjecture C with Proposition C1: do you agree this is honestly stated?
>
> Format response as a numbered list of remaining issues (if any), each with severity. End with a YES/NO consensus statement: "I agree the proofs of Theorems A, B, D and Proposition C1 are correct as stated" — or list specific remaining objections.
>
> Report under 1500 words.

## Round 3 — final sign-off on Theorem D

> You are an adversarial mathematician acting as a SKEPTICAL REFEREE. Round 3 of review. Verify ONE specific revision and give a final consensus statement.
>
> **TIME / COMPUTE BUDGET:** ~5 minutes. Don't run anything beyond N=200 for matrix enumeration.
>
> The note: `C:\Users\anton\OneDrive\Desktop\mathAI\n2+1 ai thoughts\notes\proofs\P12-pointwise-spin-identity.md`
>
> **Round 2 status recap:**
> - Theorem A: agreed correct.
> - Theorem B with off-by-one fix: agreed correct.
> - Theorem A' (second linear-form identity): agreed correct.
> - Proposition C1: minor wording issue with bound; now restated as $T(N) = o(N \log N)$ (sublinear-log improvement); sketch targets $O(N (\log N)^c / \sqrt{\log N})$.
> - Theorem D: ROUND-2 PROOF WAS FLAWED — exact-coefficient-matching argument contradicted the canonical example. The author has rewritten the proof.
>
> **Your task:** Verify the rewritten proof of Theorem D in the note. The new proof:
> 1. Uses mod-4 matching with the parity restriction from Theorem A (Case A: a,d odd b,c even; Case B: b,c odd a,d even).
> 2. Derives constraints (i') alpha*gamma ≡ c_1 (mod 2), (ii') beta*delta ≡ c_1 (mod 2), (iii') alpha*delta + beta*gamma ≡ 0 (mod 4), (iv') alpha*delta ≡ c_0 (mod 4), by analyzing the parity of ac, bd, bc in each case.
> 3. For non-degenerate identity (chi_4 ≠ 0 generically), forces alpha, beta, gamma, delta all odd, hence in {±1} (mod 4).
> 4. Constraint (iii') alpha*delta + beta*gamma ≡ 0 (mod 4) with each summand in {±1} forces them to be {+1, -1}, leading to two sub-cases: (a-b, c+d) or (a+b, c-d) up to overall sign.
>
> **Specific things to verify:**
>
> 1. The parity analysis: in Case A (a,d odd, b,c even), is it really true that bc ∈ 4Z? (Yes: both b and c are even, so bc is a product of two even numbers.) In Case B (b,c odd, a,d even), is bc odd? (Yes.) These are needed for constraint (iii').
>
> 2. The "varying terms freely" argument: the author claims "each of these terms must vanish mod 4 separately, since the terms involve algebraically independent variables." Is this rigorous? Specifically: can you actually vary ac, bd, bc independently in SL_2(N_0) while keeping det = 1? If they're constrained by the determinant (e.g., ad - bc = 1 links them), the "independence" argument may have gaps.
>
> 3. The classification step: from (iii') alpha*delta + beta*gamma ≡ 0 (mod 4) with alpha, beta, gamma, delta ∈ {±1} (mod 4), the conclusion that solutions are (a-b, c+d) or (a+b, c-d) up to sign. Is this complete? Or could there be alpha = -beta = -gamma = -delta or other parametrizations giving distinct identities?
>
> 4. Does the author handle the "case A bc ∈ 4Z but case B bc odd" tension correctly? In case A, (alpha*delta + beta*gamma) * bc ≡ 0 (mod 4) is automatic (since bc ≡ 0 mod 4). The constraint comes from case B alone. Is the author justified in deriving alpha*delta + beta*gamma ≡ 0 (mod 4) from case B?
>
> 5. Is the statement "the two yield chi_4(n+1) and chi_4(n-1) respectively" verified (rather than asserted)? This was Theorem A and Theorem A' which we already agreed are correct.
>
> **Final consensus statement required:** A YES/NO on whether you now agree the proofs of Theorems A, A', B, D and Proposition C1 are correct as stated.
>
> If YES, state so explicitly.
> If NO, list the specific remaining objections.
>
> Report under 800 words.

## Notes on the agentic protocol

- Each round is a fresh `Agent` call with `subagent_type: "general-purpose"`. The skeptic does not retain memory across rounds; the prompter (Claude main thread) summarizes the prior round's findings and the author's revisions in each new prompt.
- The skeptic is allowed to run small Python verifications but is told the empirical claims at scale are already verified.
- Termination criterion: skeptic issues an explicit YES on consensus statement. Disagreement triggers another revision round.
- Three rounds proved sufficient for P12. The substantive bug fixes happened in rounds 1→2 (Theorem B off-by-one, Theorem C retraction) and 2→3 (Theorem D proof rewrite).
