# Carl Schildkraut's lemma

## Statement (Lemma `carlslemma`)

Let $f \in \mathbb{Z}[x]$ with positive leading coefficient. If $\deg f \ge 3$, **or** $\deg f = 2$ with leading coefficient $\ge 2$, then there exists $n_0 \in \mathbb{N}$ such that
$$f(n_0) = (n_0 + a)(n_0 + b)\quad\text{with}\ a, b \in \mathbb{N}.$$

## Why this kills enumerability

Such an $n_0$ violates the [[06-enumerable-polynomial|size criterion]]: both cofactors $n_0 + a$ and $n_0 + b$ are strictly *greater* than $n_0$, so $\min\{m, f(n_0)/m\} > n_0$, contradicting Prop `maincondition`.

## Proof sketch

Pick $a$ large enough that:
1. $|f(-a)| > 3a$ (possible because $|f(-a)| \to \infty$),
2. $f(n) > \frac{3}{2} n^2$ for $n > 2a$ (possible because the leading term dominates).

Set $n_0 := |f(-a)| - a > 2a > 0$.

Then $f(n_0) \equiv f(-a) \equiv 0 \pmod{|f(-a)|}$, so $|f(-a)| = n_0 + a$ divides $f(n_0)$. Write
$$f(n_0) = (n_0 + a)(n_0 + b)$$
for some integer $b$. Bound:
$$f(n_0) > \tfrac{3}{2} n_0^2 > n_0(n_0+a)$$
which forces $b > 0$. Done.

## Where this comes from

The lemma is credited in the paper to **Carl Schildkraut** (Stack Exchange answer, 2024) — it's an elegant elementary trick that does exactly the work needed: convert an asymptotic growth bound into a concrete factorization.

## Conceptual content

The lemma is really saying: **polynomials grow either too fast or too slow to be enumerable, except in a tiny window**. Specifically, $f(n) \sim n^2$ is the unique growth rate where the divisor pair $(\sqrt{f(n)}, \sqrt{f(n)}) \approx (n, n)$ sits *exactly* on the boundary of the size criterion. Any faster growth, and Schildkraut's argument finds two cofactors both $> n$. Any slower growth (degree 1), and you can find two cofactors both $\le n$.

## Generalization potential

Schildkraut's argument is robust. It would be interesting to ask:
- For what classes of $f$ can we lower-bound the number of $n_0$ with this property? (This would give *quantitative* density of "bad" $n$ in the size criterion.)
- Is there a multivariate version? E.g. for forms $F(x,y) \in \mathbb{Z}[x,y]$ — could we classify enumerable forms similarly?
- Does the argument extend to number fields — i.e. classify polynomials over $\mathcal{O}_K$ enumerable by $SL_2(\mathcal{O}_K^+)$?

These would all be reasonable next-paper directions.
