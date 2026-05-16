# lean-to-latex

Convert the Lean 4 source in the file at `$ARGUMENTS` to LaTeX mathematical
notation.

Read the file at `$ARGUMENTS`, then convert its mathematical content to LaTeX.

Output ONLY the LaTeX content — no `\documentclass`, no preamble, no markdown
code fences. Use standard math environments (`align*`, `equation*`, etc.) and
symbols (`\forall`, `\exists`, `\to`, `\land`, `\lor`, `\neg`, `\mathbb`,
`\mathcal`, `\Rightarrow`, `\iff`, `\subseteq`, `\in`, `\mid`, etc.) to
faithfully represent the mathematical statement.

For a `theorem` or `lemma`, write the statement as a displayed equation.
For a `def`, write the defining equation or function signature.
For an `axiom`, write it as a logical formula.
Omit proof bodies — only translate the type/statement.

Write the LaTeX output to the file `$ARGUMENTS.tex` using the Write tool.
