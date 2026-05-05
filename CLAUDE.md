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

## Architecture

This is a **Lean 4** formalization project using [Mathlib](https://github.com/leanprover-community/mathlib4) (v4.30.0-rc2).

- `Mathematics.lean` — top-level entry point; re-exports all modules via `import`
- `Mathematics/` — Lean source files; add new `.lean` files here and import them in `Mathematics.lean`
- `Notes/` — Markdown notes (not compiled by Lake)
- `lakefile.toml` — Lake build config; defines the `Mathematics` library and Mathlib dependency

### Lean Options (set in `lakefile.toml`)

- `relaxedAutoImplicit = false` — implicit variables must be declared explicitly
- `pp.unicode.fun = true` — pretty-prints `fun a ↦ b` instead of `fun a => b`
- `weak.linter.mathlibStandardSet = true` — enables the Mathlib recommended linter set

### Working with Mathlib

Always run `lake exe cache get` before `lake build` when the Mathlib revision changes — building Mathlib from scratch takes hours. The cached `.olean` files come from the Mathlib CI and are keyed to the exact `rev` in `lake-manifest.json`.

To use a Mathlib definition or lemma, import the relevant Mathlib module at the top of your file:

```lean
import Mathlib.Algebra.Group.Basic
```

Use `exact?`, `apply?`, `simp?`, and `#check` interactively to find and verify Mathlib lemmas.
