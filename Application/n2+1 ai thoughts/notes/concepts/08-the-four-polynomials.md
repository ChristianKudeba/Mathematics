# The four enumerable polynomials

A reference card.

## $\phi_0(n) = n^2 + 1$

- **Discriminant** $-4$, **field** $\mathbb{Q}(i)$, ring $\mathbb{Z}[i]$ (Gaussian integers)
- **Norm form**: $a^2 + b^2$
- **Φ₀ map**: $A \mapsto (a^2+b^2,\ ac+bd)$
- **Identity**: $(ac+bd)^2 + 1 = (a^2+b^2)(c^2+d^2)$ when $ad-bc=1$
- **Primes represented**: $\{2\} \cup \{p : p \equiv 1 \pmod 4\}$
- **Prime conjecture**: [[10-landau-fourth-problem|Landau's 4th]] (open)
- **First few primes of form**: $n=1\to 2,\ n=2\to 5,\ n=4\to 17,\ n=6\to 37,\ n=10\to 101,\ n=14\to 197,\ldots$

## $\phi_1(n) = n^2 + n + 1$

- **Discriminant** $-3$, **field** $\mathbb{Q}(\zeta_3) = \mathbb{Q}(\sqrt{-3})$, ring $\mathbb{Z}[\zeta_3]$ (Eisenstein integers)
- **Norm form**: $a^2 + ab + b^2$
- **Φ₁ map**: $A \mapsto (a^2+ab+b^2,\ ac+bc+bd)$
- **Identity**: $(ac+bc+bd)^2 + (ac+bc+bd) + 1 = (a^2+ab+b^2)(c^2+cd+d^2)$ when $ad-bc=1$
- **Primes represented**: $\{3\} \cup \{p : p \equiv 1 \pmod 3\}$
- **Prime conjecture**: open ($p = n^2+n+1$ infinitely often)

## $\psi_2(n) = n^2 + 2n - 1 = (n+1)^2 - 2$

- **Discriminant** $8$, **field** $\mathbb{Q}(\sqrt 2)$, ring $\mathbb{Z}[\sqrt 2]$
- **Norm form**: $a^2 - 2b^2$ (after substitution; the paper's form is $a^2 + 2ab - b^2$)
- **Ψ₂ map**: more complex with max/min — see [[04-equivariant-map]]
- **Primes represented**: $\{2\} \cup \{p : p \equiv \pm 1 \pmod 8\}$
- **Prime conjecture**: open. (Note: $\psi_2(n) = (n+1)^2 - 2$, so $p = m^2 - 2$ for $m = n+1$.)

## $\phi_3(n) = n^2 + 3n + 1$

- **Discriminant** $5$, **field** $\mathbb{Q}(\sqrt 5)$, ring $\mathbb{Z}[\frac{1+\sqrt 5}{2}]$ (golden integers — same as $\mathbb{Z}[\phi]$)
- **Norm form**: $a^2 + 3ab + b^2$ — closely related to Fibonacci/Lucas
- **Φ₃ map**: $A \mapsto (a^2+3ab+b^2,\ ac+3bc+bd)$
- **Primes represented**: $\{5\} \cup \{p : p \equiv \pm 1 \pmod 5\}$
- **Prime conjecture**: open. Note $\phi_3(L_k) = L_{2k+3}$ (Lucas-style identity worth checking).

## Discriminant pattern

| polynomial | discriminant | $|d|$ | class number $h(d)$ |
|---|---|---|---|
| $\phi_0$ | $-4$ | 4 | 1 |
| $\phi_1$ | $-3$ | 3 | 1 |
| $\psi_2$ | $8$ | 8 | 1 |
| $\phi_3$ | $5$ | 5 | 1 |

These are the **four smallest absolute discriminants of orders in real or imaginary quadratic fields with class number 1.** See [[../bridges/B2-discriminant-coincidence]]. The next one would be disc $-7$ (i.e. $n^2 + n + 2$), and indeed $f(0) = 2 \ne 1$, so it's *not* enumerable.

## The "highway" — coupling of divisor facts

Each $A \in SL_2(\mathbb{N}_0)$ produces *four* divisor pairs simultaneously:
$$\Phi_0(A) \in \mathcal{D}_{\phi_0},\ \Phi_1(A) \in \mathcal{D}_{\phi_1},\ \Psi_2(A) \in \mathcal{D}_{\psi_2},\ \Phi_3(A) \in \mathcal{D}_{\phi_3}.$$

Example from §3 of the paper: $A = \begin{pmatrix}3&4\\8&11\end{pmatrix}$ gives:
- $\Phi_0(A) = (25, 68)$: $68^2+1 = 4625 = 25 \cdot 185$
- $\Phi_1(A) = (37, 100)$: $10101 = 37 \cdot 273$
- $\Psi_2(A) = (31, 84)$: $7223 = 31 \cdot 233$
- $\Phi_3(A) = (61, 164)$: $27389 = 61 \cdot 449$

So a single matrix simultaneously parameterizes a factorization in *each* of the four divisor-pair sets. Density information transports across.
