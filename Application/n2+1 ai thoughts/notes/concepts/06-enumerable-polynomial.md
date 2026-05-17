# Enumerable polynomials

## Definition

A polynomial $f \in \mathbb{Z}[x]$ is **enumerable** if there exists an invertible, [[04-equivariant-map|equivariant map]]
$$F : SL_2(\mathbb{N}_0) \to \mathcal{D}_f.$$
Equivalently (by uniqueness): the canonical map $\hat F_f$ (defined by $\hat F_f(I) = (1,0)$) is a bijection.

## Necessary conditions

If $f$ is enumerable then:

1. **$|f(0)| = 1$** (forced by the lemma sending $I \mapsto (1,0)$).
2. **$f$ nonvanishing on ℕ₀** (else $(0,n) \in \mathcal{D}_f$, breaking injectivity via $\bar S$).
3. **$|f(1)|, |f(2)|, |f(|f(1)|)|$ are prime** (Lemma `f(1), f(2) prime`) — they sit on the boundary, can't have nontrivial factorizations because the second-coordinate ordering forbids it.
4. **$\deg f \ge 2$** (degree-0 fails injectivity; degree-1 with given $|f(0)|=1$ fails the size bound).
5. **$\deg f \le 2$** with leading coefficient $\pm 1$ ([[09-carl-schildkraut-lemma|Carl Schildkraut's lemma]]).

These together force $f$ monic quadratic with $|f(0)|=1$, i.e. of the form $n^2 + bn \pm 1$.

## The size criterion (Prop `maincondition`)

$f$ (nonvanishing on ℕ₀) is enumerable **iff** for all $(m,n) \in \mathcal{D}_f \setminus \{(1,0)\}$:
$$\boxed{\min\{m,\ |f(n)|/m\} \le n < \max\{m,\ |f(n)|/m\}}$$

Read this as: every divisor pair $(m, n)$ has one factor $\le n$ and the other $> n$. Geometrically, $n$ sits "between" the two cofactors of $|f(n)|$.

For monic quadratic $f$ with $|f(0)|=1$, you get $f(n) \approx n^2$ near infinity; one cofactor is around $\sqrt{f(n)} \approx n$. The criterion is asking that the divisor split *strictly straddles* $n$, which is true for $n^2 \pm 1$-shape polynomials (equality only at $(1,1)$).

## Why this is rare

The criterion fails the moment the polynomial has **a square or near-square value** with both cofactors $> n$ (or both $\le n$). The argument in [[09-carl-schildkraut-lemma]] shows: degree $\ge 3$ or leading coefficient $\ge 2$ ⇒ infinitely often $f(n_0) = (n_0+a)(n_0+b)$ with $a,b \ge 1$, breaking the criterion.

## Why exactly four

Of the form $n^2 + bn \pm 1$ with $b > 0$:
- $f = n^2 - bn + 1$: $|f(b)| = 1$ ⇒ $\bar c_f$-fixed ⇒ injectivity fails.
- $f = n^2 - bn - 1$: same.
- $f = n^2 + bn + 1$, $b$ even: need $f(1) = b+2$ prime, so $b=0$ (giving $\phi_0$).
- $f = n^2 + bn + 1$, $b$ odd: need $f((b-1)^2/4 - 1)$ to be square ⇒ $b \in \{1, 3\}$ (giving $\phi_1, \phi_3$).
- $f = n^2 + bn - 1$: only $b = 2$ survives (giving $\psi_2$). Other $b$ either $f(1) = 1$ (injection fail) or size criterion fails at $n = b-1$.

Result: $\{\phi_0, \phi_1, \psi_2, \phi_3\}$. See [[07-classification-theorem]] and [[08-the-four-polynomials]].
