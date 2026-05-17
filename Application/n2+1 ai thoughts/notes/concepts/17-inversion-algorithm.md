# The inversion algorithm $\hat F_f^{-1}$

## What it does

Given $(m, n) \in \mathcal{D}_f$ (i.e. $m \mid f(n)$), compute the unique matrix $A \in SL_2(\mathbb{N}_0)$ with $\hat F_f(A) = (m, n)$.

## Algorithm (paper §3, Algorithm `algorithm`)

1. While $(m, n) \ne (1, 0)$, replace
$$(m, n) \mapsto \bar c_f \bar S^{-\lfloor n/m \rfloor}(m, n)$$
2. Record the sequence of $-\lfloor n/m \rfloor$ values.
3. Convert the resulting word in $\bar S, \bar c_f$ to a word in $\bar S, \bar T_f$ using $\bar T_f = \bar c_f \bar S \bar c_f$.
4. Convert to $S, T$.
5. Multiply.

## Worked example (paper §3)

Reduce $(37, 100) \in \mathcal{D}_{\phi_1}$ (since $37 \mid 100^2+100+1 = 10101$):

$(37, 100) \xrightarrow{\bar S^{-2}} (37, 26) \xrightarrow{\bar c_f} (19, 26) \xrightarrow{\bar S^{-1}} (19, 7) \xrightarrow{\bar c_f} (3, 7) \xrightarrow{\bar S^{-2}} (3, 1) \xrightarrow{\bar c_f} (1, 1) \xrightarrow{\bar S^{-1}} (1, 0)$.

Record: $\bar S^{-1}, \bar c_f, \bar S^{-2}, \bar c_f, \bar S^{-1}, \bar c_f, \bar S^{-2}$.

Reverse and substitute $\bar T = \bar c_f \bar S \bar c_f$ giving the matrix $S^2 T S^2 T = \begin{pmatrix}3&4\\8&11\end{pmatrix}$.

## Interpretation: this is the Euclidean algorithm

Each $\bar S^{-1}$ subtracts $m$ from $n$ — a "subtractive Euclidean step." The $\lfloor n/m \rfloor$ tells you how many times. Then $\bar c_f$ swaps $m$ with the complementary divisor $|f(n)|/m$. So:

> **Reducing in $\mathcal{D}_f$ via $\bar S^{-1}, \bar c_f$ = computing the [[16-calkin-wilf-tree|continued-fraction]] expansion of $n/m$ subject to the divisor constraint.**

The $\bar c_f$ alternation is forced by which side of the inequality $\min < n < \max$ you are on after each $\bar S$ subtraction.

This is structurally identical to the **Stern–Brocot / continued-fraction algorithm**, with the divisor constraint serving as a *guidance* for which step (subtractive or complementary) to take.

## Length of the algorithm

For random $(m, n)$ with $m \approx \sqrt{f(n)} \approx n$, the algorithm runs in $\sim \log n$ steps (like the Euclidean algorithm). Worst case may be longer; tied to the continued-fraction expansion length of $n/m$.

## "Rational expression" for primes (Example `fraction`)

Tracing the $m$-values during the reduction gives a *telescoping product* representation of any prime $p \in \mathcal{P}(f)$:
$$p = \prod_{i=0}^k |f(n_{k-i})|^{(-1)^i}$$
where $n_0 < n_1 < \cdots < n_k < p$.

Examples for $p = 113 \equiv 1 \pmod 4$ (so $113 \mid n^2 + 1$ has solutions $n = 15, 98$):
$$113 = \frac{15^2 + 1}{1^2 + 1},\qquad 113 = \frac{(98^2+1)(1^2+1)}{13^2+1}$$

So **every** prime $\equiv 1 \pmod 4$ has a (non-unique) representation as an alternating product/quotient of $n^2+1$ values.

## Why this is interesting

This is essentially a "**prime factorization in disguise**" via the Gaussian integers, but written purely in terms of *integer* operations (no $i$ visible). It would be very interesting to ask:

- What is the **minimum length** $k$ over all such representations of $p$?
- Is there a **canonical** choice (shortest, smallest $n_i$)?
- Can the lengths be related to the *congruence class* of $p$ mod higher powers, or to $L$-function data?
- Are there primes with only "long" representations?

These questions could be approached numerically and might suggest analytic structure.

## Connection to dynamics

The reduction algorithm is a dynamical system on $\mathcal{D}_f$ with two attractors: $\bar S^{-1}$ and $\bar c_f \bar S^{-1} \bar c_f = \bar T_f^{-1}$. The orbit of $(m, n)$ under repeated application converges to $(1, 0)$ in finitely many steps. This is the **deterministic Gauss-like map** for $\Phi_0$.

The corresponding *invariant measure*, *entropy*, and *spectrum* of this Gauss-like map would encode density information about the $\Phi_0$ tree — and may be where the analytic content of Landau's 4th really lives.

See [[../research/R6-zaremba-apollonian]] for parallel ideas in the continued-fraction setting.
