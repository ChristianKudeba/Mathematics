# Round 3 → Final — Author's response

The skeptic issued **YES** on the final consensus, modulo a one-sentence expository fix to make the case-A-then-case-B logic in Theorem D's proof fully rigorous.

## The expository fix applied

Old (round 2 / round 3 draft):

> Each of these terms must vanish mod 4 separately, since the terms involve algebraically independent variables (specifically: a generic matrix in Case A has $ac, bd, bc$ with $ac \in \{0, 2\} \pmod 4$, $bd \in \{0, 2\} \pmod 4$, $bc \in 4\mathbb{Z}$; in Case B, $bc$ is odd; varying these freely shows each term must vanish mod 4 alone).
>
> - $(*)$: $ac$ ranges over even integers including $\equiv 2 \pmod 4$. Hence $(\alpha\gamma - c_1) \cdot 2 \equiv 0 \pmod 4$ ⟹ $\alpha\gamma \equiv c_1 \pmod 2$.
> - $(**)$: same argument, $\beta\delta \equiv c_1 \pmod 2$.
> - $(\dagger)$: in Case B, $bc$ is odd, so $(\alpha\delta + \beta\gamma) \cdot 1 \equiv 0 \pmod 4$ ⟹ $\alpha\delta + \beta\gamma \equiv 0 \pmod 4$.
> - $(\ddagger)$: $\alpha\delta \equiv c_0 \pmod 4$.

Replaced with the explicit case-A-then-case-B sequence:

> Each of these terms is extracted in two stages — first using Case A, where $bc \in 4\mathbb{Z}$ kills the $(\dagger)$ contribution, then using Case B, where $bc$ is odd. Within each case the variables $ac, bd, bc$ vary freely over their allowed residues mod 4 as $A$ ranges over $SL_2(\mathbb{N}_0)$ matrices in that case (computationally verified: e.g., $S^2 T = (3,2,1,1)$ has $ac=3, bd=2$; $T^2 S = (1,1,2,3)$ has $ac=2, bd=3$; etc.).
>
> **Case A first** (where $bc \in 4\mathbb{Z}$, so $(\dagger) \equiv 0 \pmod 4$ automatically):
> - $(*)$: $ac$ takes both values mod 4 in $\{0, 2\}$ (e.g., $a=1, c=2$ gives $ac=2$; $a=1, c=4$ gives $ac=4 \equiv 0$). Hence $(\alpha\gamma - c_1) \cdot 2 \equiv 0 \pmod 4$ ⟹ $\alpha\gamma \equiv c_1 \pmod 2$.
> - $(**)$: same argument, $\beta\delta \equiv c_1 \pmod 2$.
> - $(\ddagger)$: $\alpha\delta \equiv c_0 \pmod 4$ (extracted as the constant after $(*), (**), (\dagger)$ are accounted for).
>
> **Then Case B** (where $bc$ is odd): now $(*)$ and $(**)$ already hold, so the residual constraint is $(\dagger) + (\ddagger) \equiv 0 \pmod 4$, i.e., $(\alpha\delta + \beta\gamma) \cdot bc + (\alpha\delta - c_0) \equiv 0 \pmod 4$. Subtracting the already-established $(\ddagger)$ ($\alpha\delta - c_0 \equiv 0$) leaves $(\alpha\delta + \beta\gamma) \cdot bc \equiv 0 \pmod 4$ for $bc$ ranging over odd integers. Since odd $\times k \equiv 0 \pmod 4$ forces $k \equiv 0 \pmod 4$:
> - $(\dagger)$: $\alpha\delta + \beta\gamma \equiv 0 \pmod 4$.

## Final state

After three rounds of adversarial review and three substantive revisions, the following are signed off as **correct as stated**:

1. **Theorem A** — pointwise determinant-driven identity $\chi_4(a-b)\chi_4(c+d) = \chi_4(n+1)$.
2. **Theorem A'** — analogous identity $\chi_4(a+b)\chi_4(c-d) = \chi_4(n-1)$.
3. **Theorem B** — collapse of bilinear sum to twisted divisor sum $T(N) = \sum_{n=1}^N \tau(n^2+1)\chi_4(n+1)$ (with the $n = 0$ term contributed separately by the identity matrix).
4. **Theorem D** — sharp classification: at conductor 4, the only linear-form identities of the type $\chi_4(L_1)\chi_4(L_2) = \chi_4(c_1 n + c_0)$ are $(L_1, L_2) \in \{(a-b, c+d), (a+b, c-d)\}$ up to sign. Higher-conductor extension is blocked because $bd \not\equiv 0 \pmod 4$ in $SL_2(\mathbb{N}_0)$.
5. **Proposition C1** — unconditional bound $T(N) = o(N \log N)$ via elementary AP-cancellation, with sketch targeting $O(N(\log N)^c/\sqrt{\log N})$.

What remains conjectural / open:

- **Conjecture C** ($T(N) \ll \sqrt N$): empirically verified to $N = 10^7$, would follow from subconvexity for an appropriate Hecke L-function over $\mathbb{Q}(i)$.
- **Plancherel route to FI bilinear bound**: needs a genuinely new ingredient beyond linear-form characters at conductor 4 (Theorem D shows the linear-form well is exhausted at this conductor).

## Lessons from the iteration

1. **Round 1 caught two real overclaims** (Theorem C unconditional, Plancherel completeness) and one off-by-one. The skeptic's framing — "is the author actually honest?" — was exactly right.
2. **Round 2 caught a structural proof error** (Theorem D's exact-coefficient-matching). Without the skeptic, this would have shipped as wrong-but-true: the classification statement is correct, but my round-2 proof did not establish it.
3. **Round 3 caught a small expository imprecision** (case-A vs case-B ordering for extracting constraints). Not a math error, but the proof was harder to read than it needed to be.

The result that survived: **one identity, sharply classified, with honest empirical and conditional claims about the cumulative cancellation.** Modest but solid.
