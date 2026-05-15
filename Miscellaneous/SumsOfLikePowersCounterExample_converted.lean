import Mathlib.Tactic

/-!
# Counterexample to Euler's Conjecture on Sums of Like Powers

Paper: L. J. Lander and T. R. Parkin, "Counterexample to Euler's Conjecture on Sums of Like Powers"
*Bulletin of the American Mathematical Society* **72** (1966), p. 1079.

## Main Result

Euler conjectured (1769) that for every integer n > 2, the equation a₁ⁿ + ⋯ + aₖⁿ = bⁿ
has no solution in positive integers when k < n. Lander and Parkin found by computer search
on the CDC 6600 that 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵, a counterexample with n = 5, k = 4.
-/

open BigOperators

namespace LanderParkin

/-! ## Statement of Euler's Conjecture (1769) -/

/-- Euler's conjecture: for every n > 2, an nth power cannot be expressed as a sum of
    fewer than n positive nth powers.
    Formally: there exist no positive integers a₁, …, aₖ, b with k < n satisfying
    a₁ⁿ + a₂ⁿ + ⋯ + aₖⁿ = bⁿ. -/
def EulersConjecture : Prop :=
  ∀ (n k : ℕ), n > 2 → k < n →
    ∀ (a : Fin k → ℕ) (b : ℕ),
      (∀ i, 0 < a i) → 0 < b →
      ∑ i, (a i) ^ n ≠ b ^ n

/-! ## The Lander-Parkin Counterexample -/

/-- The Lander-Parkin identity: 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵.
    Verified by direct computation. -/
theorem lander_parkin_identity : 27 ^ 5 + 84 ^ 5 + 110 ^ 5 + 133 ^ 5 = (144 : ℕ) ^ 5 := by
  norm_num

/-- Euler's conjecture is false: four positive fifth powers sum to a fifth power,
    contradicting the conjecture for n = 5, k = 4. -/
theorem eulers_conjecture_false : ¬EulersConjecture := by
  intro h
  have ha : ∀ i : Fin 4, 0 < (![27, 84, 110, 133] : Fin 4 → ℕ) i := by
    intro i; fin_cases i <;> norm_num
  have key : ∑ i : Fin 4, ((![27, 84, 110, 133] : Fin 4 → ℕ) i) ^ 5 = (144 : ℕ) ^ 5 := by
    decide
  exact h 5 4 (by norm_num) (by norm_num) ![27, 84, 110, 133] 144 ha (by norm_num) key

/-! ## Numerical Checks -/

-- Confirm the individual fifth powers and their sum
#eval (27 ^ 5 : ℕ)   -- 14348907
#eval (84 ^ 5 : ℕ)   -- 4182119424
#eval (110 ^ 5 : ℕ)  -- 16105100000
#eval (133 ^ 5 : ℕ)  -- 41615795893
#eval (144 ^ 5 : ℕ)  -- 61917364224

#eval (27 ^ 5 + 84 ^ 5 + 110 ^ 5 + 133 ^ 5 : ℕ)  -- 61917364224

end LanderParkin
