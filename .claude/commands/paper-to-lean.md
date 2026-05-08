# Convert Math Paper PDF to Lean 4

Formalize a mathematical research paper (given as a PDF path in `$ARGUMENTS`) into Lean 4 code using Mathlib.

## Steps

### 1. Extract text
```bash
pdftotext "$ARGUMENTS" -
```
If `pdftotext` is unavailable, try:
```bash
python3 -c "import fitz; doc=fitz.open('$ARGUMENTS'); print('\n'.join(p.get_text() for p in doc))"
```

### 2. Analyze the paper
Identify and list, in dependency order:
- All **definitions** (including recursive definitions and data structures)
- All **examples** (as `#eval` checks or `example` blocks)
- All **lemmas**, **theorems**, **propositions**, and **corollaries** (with their hypotheses)
- The **proof strategy** for each result (tree induction, generating functions, bijection, etc.)
- Which results are already in **Mathlib** (skip or `exact` them)
- Which **Mathlib modules** to import

### 3. Create the Lean 4 file
Create `Mathematics/<PaperName>.lean` where `<PaperName>` is derived from the paper title or author+topic (e.g., `ShakovDivisors`).

The file must:
- Start with a `/-! ... -/` module docstring naming the paper, arXiv ID if present, and main result
- Import all needed Mathlib modules
- Open a `namespace` matching the file name
- Define all mathematical objects in dependency order
- State every theorem/lemma/proposition/corollary with exact hypotheses
- Provide **complete proofs** for:
  - Base case computations (use `native_decide` or `decide`)
  - Simple algebraic identities (use `ring`, `omega`, `norm_num`)
  - Direct consequences of Mathlib lemmas
- Use `sorry` for complex proofs, with a comment explaining the proof strategy
- Add a `/-! ... -/` section docstring before each logical group
- Reference paper statement numbers in docstrings (e.g., `[Theorem 4]`)
- Follow Lean 4 / Mathlib naming: `camelCase` for defs, `lowerCamelCase_of_X` for lemmas about X

### 4. Update imports
Add `import Mathematics.<PaperName>` to `Mathematics.lean`.

### 5. Verify
Run `lake build Mathematics.<PaperName>` and fix any errors (the file must at least elaborate without type errors, even if proofs use `sorry`).

## Lean 4 / Mathlib tips
- Divisor count: `(Nat.divisors n).card` or `Nat.sigma 0 n`
- Fibonacci: `Nat.fib n` (0-indexed: `Nat.fib 0 = 0`, `Nat.fib 1 = 1`)
- Finset sum: `∑ t ∈ Finset.Ico a b, f t` (needs `open BigOperators`)
- Set cardinality: `Set.ncard {n : ℕ | P n}`
- Well-founded recursion on ℕ: use `termination_by n` with `decreasing_by omega`
- Nat subtraction floors at 0; use `ℤ` when subtraction appears in a recursive definition
- For exact Nat division (when divisibility is known), add a hypothesis or use `Nat.div_eq_of_eq_mul_left`
