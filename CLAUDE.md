# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Download the Mathlib build cache (do this before building to avoid recompiling Mathlib)
lake exe cache get

# Build the project
lake build

# Build a specific file
lake build Mathematics.Basic

# Update dependencies
lake update
```

## Project Overview

This is a **Lean 4** mathematical formalization project using [Mathlib](https://github.com/leanprover-community/mathlib4) (v4.30.0-rc2). The goal is to produce machine-verified proofs for research-level mathematics — specifically formalizing a 2025 paper on k-regular sequences and building ZFC foundations from scratch.

## Directory Structure

```
Mathematics/
├── Mathematics.lean              # Top-level module; imports all submodules
├── Mathematics/
│   ├── Basic.lean                # Minimal example (2 + 2 = 4); used as a template
│   ├── ShakovDivisors.lean       # Main formalization of Shakov's paper (arXiv:2510.22805v1)
│   └── ZFC.lean                  # ZFC set theory axiomatized from scratch
├── Miscellaneous/
│   ├── ShakovPaper.pdf           # Original research paper (source material)
│   └── ShakovPaper_converted.lean # Auto-converted first draft from PDF
├── Notes/                        # Markdown notes (not compiled by Lake)
│   ├── Axioms.md
│   └── Claude Info.md
├── Tools/
│   └── ProofViz/
│       └── proof_viz.exe         # Proof visualization utility
├── .claude/
│   ├── commands/paper-to-lean.md # Custom skill: PDF → Lean 4 formalization
│   └── settings.local.json       # Tool permission allowlist
├── .github/workflows/
│   ├── lean_action_ci.yml        # Build + docgen CI
│   ├── update.yml                # Automated Mathlib dependency updates
│   └── create-release.yml        # Release tagging on toolchain changes
├── lakefile.toml                 # Lake project config
└── lake-manifest.json            # Dependency lock file
```

## Source Files

### `Mathematics.lean`
Top-level entry point. Every new `.lean` file added to `Mathematics/` must be imported here.

### `Mathematics/Basic.lean`
A trivial example (`2 + 2 = 4`) used as a template and to verify the build environment works.

### `Mathematics/ShakovDivisors.lean`
The primary formalization target. Formalizes Anton Shakov's 2025 paper (arXiv:2510.22805v1):

**Main theorem (Theorem 4):** For all m ≥ 0, the count of indices n ≥ 1 where s(n) = m equals the divisor count of m² + 1.

Key definitions:
- `IsKRegular` — k-regular sequences (Definition 1): subsequences are ℤ-linear combinations of finitely many base sequences
- `s : ℕ → ℤ` — the Shakov sequence (OEIS A383066); base cases s(0)=0, s(1)=0, s(2)=1, s(3)=1, with 4-branch recursion for n ≥ 4
- `L`, `R`, `treeInvolution` — binary tree operations used to construct the bijection in Theorem 4
- `ValidPair (d, m)` — constraint d ≥ 1, d | m² + 1
- `rowSum n` — sum of s(t) over row n of the binary tree (indices 2ⁿ to 2^(n+1)−1)
- `fibPathIndex` — index sequence tracing the Fibonacci path through the tree

Proof status: base cases and structural lemmas are proved; main theorem and most supporting propositions currently use `sorry`.

### `Mathematics/ZFC.lean`
Axiomatizes ZFC set theory inside Lean 4 using abstract axioms rather than Mathlib's built-in `Set`.

- Introduces `ZFSet : Type` and `Mem : ZFSet → ZFSet → Prop` as axioms
- Defines `Subset`, `IsEmptySet`, `IsPair`, `IsSingleton`, `IsUnion`, `IsPowerSet`, `IsSeparation`, `IsReplacementImage` as predicates
- States all 9 standard ZFC axioms: Extensionality, Empty Set, Pairing, Union, Powerset, Separation, Replacement, Infinity, Foundation, and Choice

### `Miscellaneous/ShakovPaper_converted.lean`
An auto-generated first pass from the PDF using the `paper-to-lean` skill. Not imported by `Mathematics.lean`; used as a reference draft when developing `ShakovDivisors.lean`.

## Lean Options (set in `lakefile.toml`)

- `relaxedAutoImplicit = false` — implicit variables must be declared explicitly
- `pp.unicode.fun = true` — pretty-prints `fun a ↦ b` instead of `fun a => b`
- `weak.linter.mathlibStandardSet = true` — enables the Mathlib recommended linter set
- `maxSynthPendingDepth = 3` — limits typeclass synthesis depth

## Working with Mathlib

Always run `lake exe cache get` before `lake build` when the Mathlib revision changes — building Mathlib from scratch takes hours. The cached `.olean` files come from the Mathlib CI and are keyed to the exact `rev` in `lake-manifest.json`.

To use a Mathlib definition or lemma, import the relevant Mathlib module at the top of your file:

```lean
import Mathlib.Algebra.Group.Basic
```

Use `exact?`, `apply?`, `simp?`, and `#check` interactively to find and verify Mathlib lemmas.

Useful Mathlib APIs for this project:
- Divisor count: `(Nat.divisors n).card`
- Fibonacci: `Nat.fib n` (0-indexed)
- Finset sums: `∑ t ∈ Finset.Ico a b, f t`
- Set cardinality: `Set.ncard {n : ℕ | P n}`
- Well-founded recursion: `termination_by`, `decreasing_by omega`

## Adding a New Formalization

1. Create `Mathematics/<Name>.lean` with appropriate Mathlib imports
2. Add `import Mathematics.<Name>` to `Mathematics.lean`
3. Run `lake build Mathematics.<Name>` to verify

Use the `paper-to-lean` skill (`.claude/commands/paper-to-lean.md`) to auto-generate a first draft from a PDF.

## CI / GitHub Actions

- **`lean_action_ci.yml`** — runs on every push/PR; builds the project and generates documentation deployed to GitHub Pages
- **`update.yml`** — periodically checks for Mathlib updates and opens a PR/issue automatically
- **`create-release.yml`** — creates a release tag whenever `lean-toolchain` changes
