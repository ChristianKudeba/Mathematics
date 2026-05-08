import Mathlib.Data.Nat.Basic
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.NumberTheory.Divisors
import Mathlib.Data.Set.Card
import Mathlib.Tactic

/-!
# A 2-Regular Sequence That Counts The Divisors of n² + 1

Formalization of Anton Shakov, arXiv:2510.22805v1 (2025).

**Main result** (Theorem 4): For all m ≥ 0,
  `#{n : ℕ | 1 ≤ n ∧ s n = m} = (Nat.divisors (m² + 1)).card`
where `s : ℕ → ℤ` is the 2-regular sequence A383066 satisfying:
  - s(4k)   = 2·s(2k)   - s(k)
  - s(4k+1) = 2·s(2k)   + s(2k+1)
  - s(4k+2) = 2·s(2k+1) + s(2k)
  - s(4k+3) = 2·s(2k+1) - s(k)
with s(1) = 0, s(2) = 1, s(3) = 1.
-/

open BigOperators Nat

namespace Shakov

/-! ## Definition 1: k-regular sequences -/

/-- A sequence `f : ℕ → ℤ` is **k-regular** if there exists E such that every
subsequence `n ↦ f(kᵉ·n + r)` (with e > E, 0 ≤ r < kᵉ) is a ℤ-linear combination
of finitely many "base" subsequences. [Definition 1] -/
def IsKRegular (k : ℕ) (f : ℕ → ℤ) : Prop :=
  ∃ (E : ℕ) (basis : Finset (ℕ × ℕ)),
    ∀ (e r : ℕ), E < e → r < k ^ e →
      ∃ (coeffs : ℕ × ℕ → ℤ),
        ∀ n, f (k ^ e * n + r) = ∑ p ∈ basis, coeffs p * f (k ^ p.1 * n + p.2)

/-! ## The Shakov sequence s(n) -/

/-- The Shakov sequence A383066. Defined by four-case recursion on n mod 4.
Values live in ℤ to allow the subtractions in the recursion. [Theorem 4] -/
def s (input : ℕ) : ℤ :=
  match input with
  | 0 => 0
  | 1 => 0
  | 2 => 1
  | 3 => 1
  | n + 4 =>
    match (n + 4) % 4 with
    | 0 => 2 * s ((n + 4) / 2) - s ((n + 4) / 4)
    | 1 => 2 * s ((n + 4) / 2) + s ((n + 4) / 2 + 1)
    | 2 => 2 * s ((n + 4) / 2) + s ((n + 4) / 2 - 1)
    | _ => 2 * s ((n + 4) / 2) - s ((n + 4) / 4)
termination_by input
decreasing_by all_goals simp_wf; omega

/-! ### Initial values -/

-- Well-founded defs don't reduce in the kernel, so rfl fails; use native_decide.
@[simp] theorem s_zero  : s 0 = 0 := by native_decide
@[simp] theorem s_one   : s 1 = 0 := by native_decide
@[simp] theorem s_two   : s 2 = 1 := by native_decide
@[simp] theorem s_three : s 3 = 1 := by native_decide

/-- The sequence begins: 0, 1, 1, 2, 3, 3, 2, 3, ... -/
example : (List.range 8).map (fun n => s (n + 1)) = [0, 1, 1, 2, 3, 3, 2, 3] := by
  native_decide

/-! ### The recursion equations stated for all k -/

/-- s(4k) = 2·s(2k) - s(k). [Theorem 4] -/
theorem s_four_mul (k : ℕ) (hk : 1 ≤ k) :
    s (4 * k) = 2 * s (2 * k) - s k := by sorry

/-- s(4k+1) = 2·s(2k) + s(2k+1). [Theorem 4] -/
theorem s_four_mul_add_one (k : ℕ) (hk : 1 ≤ k) :
    s (4 * k + 1) = 2 * s (2 * k) + s (2 * k + 1) := by sorry

/-- s(4k+2) = 2·s(2k+1) + s(2k). [Theorem 4] -/
theorem s_four_mul_add_two (k : ℕ) (hk : 1 ≤ k) :
    s (4 * k + 2) = 2 * s (2 * k + 1) + s (2 * k) := by sorry

/-- s(4k+3) = 2·s(2k+1) - s(k). [Theorem 4] -/
theorem s_four_mul_add_three (k : ℕ) (hk : 1 ≤ k) :
    s (4 * k + 3) = 2 * s (2 * k + 1) - s k := by sorry

/-- The sequence is non-negative: s(n) ≥ 0 for all n. -/
theorem s_nonneg (n : ℕ) : 0 ≤ s n := by sorry

/-- The sequence is 2-regular. [Definition 1] -/
theorem s_is_2_regular : IsKRegular 2 s := by sorry

/-! ## The integer pair tree -/

/-- The **left child** map L(d, m) = (d, m + d). [Proof of Theorem 4] -/
def L (d m : ℕ) : ℕ × ℕ := (d, m + d)

/-- The **right child** map R(d, m) = (((m+d)²+1)/d, m + (m²+1)/d).
Valid (gives integer results) when d | m² + 1. [Proof of Theorem 4] -/
def R (d m : ℕ) : ℕ × ℕ :=
  (((m + d) ^ 2 + 1) / d, m + (m ^ 2 + 1) / d)

/-- The symmetry involution ι(d, m) = ((m²+1)/d, m).
Satisfies R = ι ∘ L ∘ ι when d | m² + 1. [Proof of Theorem 4] -/
def treeInvolution (d m : ℕ) : ℕ × ℕ := ((m ^ 2 + 1) / d, m)

/-- R equals ι applied to L(ι(d,m)). [Proof of Theorem 4] -/
theorem R_eq_inv_L_inv (d m : ℕ) (h : d ∣ m ^ 2 + 1) :
    let ι := fun p : ℕ × ℕ => treeInvolution p.1 p.2
    R d m = ι (L (ι (d, m)).1 (ι (d, m)).2) := by sorry

/-- A pair (d, m) is **valid** if d ≥ 1 and d | m² + 1. -/
def ValidPair (d m : ℕ) : Prop := 1 ≤ d ∧ d ∣ m ^ 2 + 1

/-! ## Lemma 5: Tree pairs are valid -/

/-- Every pair reachable from (1, 0) by L and R satisfies d ≥ 1 and d | m² + 1.
[Lemma 5] -/
theorem tree_pairs_valid (d m : ℕ) (h : ValidPair d m) :
    ValidPair (L d m).1 (L d m).2 ∧ ValidPair (R d m).1 (R d m).2 := by
  -- L(d,m) = (d, m+d): need d ≥ 1 (given) and d | (m+d)² + 1.
  -- Key: (m+d)² + 1 = (m²+1) + 2md + d², and d divides each summand.
  -- R validity follows from ι ∘ L ∘ ι preservation.
  sorry

/-! ## Lemma 6: Each valid pair appears exactly once -/

/-- Every valid pair (d, m) appears exactly once in the integer pair tree rooted at (1, 0).
Proved by strong induction on m. [Lemma 6] -/
theorem tree_pair_unique (d m : ℕ) (h : ValidPair d m) :
    ∃! path : List Bool,
      path.foldl (fun p b => if b then L p.1 p.2 else R p.1 p.2) (1, 0) = (d, m) := by
  sorry

/-! ## Theorem 4: The main counting theorem -/

/-- The number of indices n ≥ 1 with s(n) = m equals σ₀(m² + 1), the divisor count.
[Theorem 4] -/
theorem shakov_main (m : ℕ) :
    Set.ncard {n : ℕ | 1 ≤ n ∧ s n = (m : ℤ)} = (Nat.divisors (m ^ 2 + 1)).card := by
  sorry

/-- Generating function form of Theorem 4 (placeholder). [Theorem 4] -/
theorem shakov_generating_function : ∀ (_ : ℝ) (_ : True), True := fun _ _ => trivial

/-! ## Boundary values and row structure -/

/-- The leftmost value on row n of the second component tree is s(2ⁿ) = n. -/
theorem s_pow_two (n : ℕ) : s (2 ^ n) = n := by
  induction n with
  | zero => simp
  | succ n _ih => sorry

/-- The rightmost value on row n is s(2^{n+1} - 1) = n. -/
theorem s_pow_two_sub_one (n : ℕ) : s (2 ^ (n + 1) - 1) = n := by sorry

/-! ## Proposition 8: Primality characterization -/

/-- n² + 1 is prime iff the only indices mapping to n are the boundary indices 2ⁿ and 2^{n+1}-1.
[Proposition 8] -/
theorem prime_iff_boundary (n : ℕ) :
    Nat.Prime (n ^ 2 + 1) ↔
      {m : ℕ | 1 ≤ m ∧ s m = (n : ℤ)} = {2 ^ n, 2 ^ (n + 1) - 1} := by sorry

/-! ## Row sums and average values (Proposition 7) -/

/-- Sum of s(t) over the n-th row {2ⁿ, ..., 2^{n+1}-1} of the second component tree. -/
def rowSum (n : ℕ) : ℤ :=
  ∑ t ∈ Finset.Ico (2 ^ n) (2 ^ (n + 1)), s t

@[simp] theorem rowSum_zero : rowSum 0 = 0 := by native_decide
@[simp] theorem rowSum_one  : rowSum 1 = 2 := by native_decide

/-- Row sums satisfy the recurrence rₙ = 5·rₙ₋₁ - 2·rₙ₋₂, r₀ = 0, r₁ = 2. [Proposition 7] -/
theorem rowSum_recurrence (n : ℕ) (hn : 2 ≤ n) :
    rowSum n = 5 * rowSum (n - 1) - 2 * rowSum (n - 2) := by sorry

/-- Average value on row n equals ((5+√17)ⁿ - (5-√17)ⁿ) / (2^{2n-1} · √17). [Proposition 7] -/
theorem rowSum_average (n : ℕ) :
    (rowSum n : ℝ) / 2 ^ n =
      ((5 + Real.sqrt 17) ^ n - (5 - Real.sqrt 17) ^ n) /
      (2 ^ (2 * n - 1) * Real.sqrt 17) := by sorry

/-! ## Proposition 9 and Corollaries 10-11: Fibonacci numbers in the sequence -/

/-- Index sequence a(n) tracing the Fibonacci path in the second component tree.
  a(1) = 1; a(4k) = 2·a(n-1); a(4k+1) = a(n-1)+1; a(4k+2) = 2·a(n-1)+1; a(4k+3) = a(n-1)-1.
[Proposition 9] -/
def fibPathIndex (input : ℕ) : ℕ :=
  match input with
  | 0 => 0
  | 1 => 1
  | n + 2 =>
    let prev := fibPathIndex (n + 1)
    match (n + 2) % 4 with
    | 0 => 2 * prev
    | 1 => prev + 1
    | 2 => 2 * prev + 1
    | _ => prev - 1  -- safe: fibPathIndex_pos shows prev ≥ 1 for n ≥ 1
termination_by input
decreasing_by simp_wf

/-- a(n) ≥ 1 for all n ≥ 1. -/
theorem fibPathIndex_pos (n : ℕ) (hn : 1 ≤ n) : 1 ≤ fibPathIndex n := by sorry

/-- s(a(n)) = Fib(n) for all n ≥ 1 (paper indexing: F₁ = 0, F₂ = 1).
Corresponds to Nat.fib (n-1) in Lean's 0-indexed Fibonacci. [Proposition 9] -/
theorem fibonacci_in_sequence (n : ℕ) (hn : 1 ≤ n) :
    s (fibPathIndex n) = (Nat.fib (n - 1) : ℤ) := by sorry

/-- Fₙ² + 1 is composite for n > 4.
Proof via Cassini's identity: Fₙ₋₁·Fₙ₊₁ - Fₙ² = (-1)ⁿ gives a non-trivial divisor. [Corollary 10] -/
theorem fibonacci_sq_plus_one_composite (n : ℕ) (hn : 4 < n) :
    ¬ Nat.Prime (Nat.fib n ^ 2 + 1) := by sorry

/-- The largest value on row n ≥ 1 of the second component tree equals F_{2n} (Lean: Nat.fib (2*n)).
[Corollary 11] -/
theorem largest_on_row (n : ℕ) (hn : 1 ≤ n) :
    ∀ k ∈ Finset.Ico (2 ^ n) (2 ^ (n + 1)), s k ≤ (Nat.fib (2 * n) : ℤ) := by sorry

/-- The maximum F_{2n} is achieved on row n. -/
theorem largest_on_row_achieved (n : ℕ) (hn : 1 ≤ n) :
    ∃ k ∈ Finset.Ico (2 ^ n) (2 ^ (n + 1)), s k = (Nat.fib (2 * n) : ℤ) := by sorry

end Shakov
