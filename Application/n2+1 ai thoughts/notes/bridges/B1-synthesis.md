# Synthesis — bridging Shakov to conventional approaches

This is the **master document**. Everything else in `notes/` feeds into it.

## What Shakov gives us — the new vocabulary

Shakov's paper does three things at once:

1. **Classifies** the polynomials whose divisor structure is "free-monoid-enumerable": $\{\phi_0, \phi_1, \psi_2, \phi_3\}$ ([[../concepts/07-classification-theorem]]).
2. **Reformulates** Landau's 4th as a combinatorial statement: $n^2+1$ is prime iff $n$ does not appear in the interior of a specific binary tree, equivalently iff the [[../concepts/14-S-sequence|2-regular sequence $\mathcal{S}$]] has fiber size 2 at $n$ ([[../concepts/12-boundary-vs-interior]]).
3. **Reformulates** divisor counting as semigroup-orbit counting: $\tau(n^2+1) = \#\{A \in SL_2(\mathbb{N}_0): ac+bd = n\}$ ([[../concepts/13-prime-characterization]]).

Together: **Landau's 4th becomes a question about a 2-regular sequence whose underlying spectral data is a Jordan block of eigenvalue 1, and equivalently a thin-orbit complement question for a free monoid of integer 2×2 matrices.**

This is genuinely new vocabulary for an old problem.

## What was already known — the conventional toolbox

The status of conventional attacks (see [[../research/R1-iwaniec-and-sieves]] for sources):

| approach | best result on $\phi_0$ | obstruction |
|---|---|---|
| Half-dimensional sieve (Iwaniec '78) | $\phi_0(n) = P_2$ infinitely often | parity problem |
| Friedlander–Iwaniec bilinear method | breaks parity for $a^2+b^4$ | only one variable in $n^2+1$ |
| Heath-Brown $a^2+p^4$ | breaks parity for thinner family | requires $p$ prime as auxiliary |
| Bateman–Horn / Hardy–Littlewood | precise heuristic count | no proof technology |
| Class field theory of $\mathbb{Q}(i)$ | counts representations of $\phi_0(n)$ | doesn't detect primality |

The wall is **the parity problem**. Sieves see almost-primes $P_2$ but cannot distinguish prime from product-of-two-primes when both factors fall in the same regime.

## The structural connection — the discriminant coincidence

The four enumerable polynomials are exactly the **smallest-discriminant fundamental quadratic orders with class number 1**:
$$\mathrm{disc}(\phi_0,\phi_1,\psi_2,\phi_3) = (-4, -3, 5, 8).$$

This is **not** an accident — see [[B2-discriminant-coincidence]]. The β-Diophantus identities are *literally* Gauss composition in the principal class. Enumerability ⇔ (class number 1) + (small enough discriminant for SL₂(ℕ₀)-reduction to cover everything).

**Implication**: the Shakov framework is implicitly using class field theory of these four orders. Anything we can prove combinatorially with $\mathcal{D}_{\phi_0}$ has a class-field-theoretic shadow over $\mathbb{Z}[i]$, and vice versa.

## Three places where Shakov genuinely opens new ground

### 1. Bilinear cross-term ($\chi(A) = ac+bd$)

The cross-term $\chi(A) = ac + bd$ is **literally bilinear** in the row vectors $(a,b)$ and $(c,d)$. The det constraint $ad-bc=1$ couples them, but the bilinearity is structurally present.

Friedlander–Iwaniec broke parity for $a^2+b^4$ via a bilinear sum that could exhibit cancellation in one variable. **For $\phi_0$, the analogous bilinear sum is a sum over SL₂(ℕ₀) matrices, with the bilinearity coming from the row-vector decomposition.**

This is the **single most promising parity-breaking observation** in the Shakov framework. See [[B5-affine-sieve-attack]] §"Why this might actually work."

### 2. Free monoid → exact sums become tractable

Most thin-group problems suffer from non-uniqueness of word representations. SL₂(ℕ₀) is a *free* monoid — every matrix has a unique S/T-word. So sums over SL₂(ℕ₀) with prescribed cross-term values reduce to **sums over S/T-words with a Diophantine condition** — a very clean object.

This is much better than typical thin-orbit settings. Transfer-operator techniques apply naturally. See [[../research/R7-k-regular-asymptotics]].

### 3. Quadruple coupling ("highway")

A single matrix $A \in SL_2(\mathbb{N}_0)$ encodes a divisor pair in **all four** of $\mathcal{D}_{\phi_0}, \mathcal{D}_{\phi_1}, \mathcal{D}_{\psi_2}, \mathcal{D}_{\phi_3}$. So density information in any one transports to information about the others.

Strategically: even if Landau's 4th itself is hard, the **joint** prime distribution of $\phi_0, \phi_1, \psi_2, \phi_3$ on the same matrix index might be tractable. Sieving "any one of these is prime" might break the parity barrier for *some* of them simultaneously.

## The program — five steps

I'll outline the most coherent attack I can see.

### Step 1 — Characterize the spectrum

Develop the spectral theory of the **transfer operator** $\mathcal{L} f(m,n) = f(\bar S(m,n)) + f(\bar T_{\phi_0}(m,n))$ acting on a suitable function space on $\mathcal{D}_{\phi_0}$. Determine its dominant eigenvalue (conjecturally $(5+\sqrt{17})/2$ from row-sum recursion), spectral gap, and Hölder regularity of the leading eigenfunction.

This is doable now with current methods. It's the foundation for everything.

### Step 2 — Quantitative orbit counting

Use Step 1's spectral data to prove
$$\#\{A \in SL_2(\mathbb{N}_0) : \chi(A) \le N\} \asymp N \cdot (\log N) \cdot G(N)$$
where $G(N)$ is a slowly varying / bounded fluctuation. Compare with $\sum_{n \le N} \tau(n^2+1) \sim N \log N$ (classical for $\mathbb{Z}[i]$).

### Step 3 — Congruence quotient and spectral gap

Define the **congruence transfer operator** $\mathcal{L}_q$ on $\mathcal{D}_{\phi_0} \otimes (\mathbb{Z}/q)$. Prove a uniform spectral gap. This is the heart — it's where the affine sieve usually applies. The semigroup vs. group obstruction is real but possibly bypassable via Selberg's spectral gap for SL₂(ℤ) projected to SL₂(ℕ₀).

### Step 4 — Sieve for primes among matrices

Apply Bourgain–Kontorovich-style sieve to count
$$\#\{A \in SL_2(\mathbb{N}) : \chi(A) = p,\ p\ \text{prime}\}.$$
This is "primes among interior cross-terms." By [[../concepts/13-prime-characterization|the equivalence]], counting these primes counts the *non-Landau* primes of suitable form. The Landau primes are the **complement**.

### Step 5 — Bilinear breaking of parity

Use the bilinear structure of $\chi$ ([[B5-affine-sieve-attack]] §1) to bound a parity-breaking Type II sum:
$$\sum_{(a,b) \in \mathbb{Z}^2} \alpha_{a,b} \sum_{(c,d) : \det = 1, \chi \le N} \beta_{c,d} \cdot (\text{Liouville function}).$$

If this sum has cancellation beyond the trivial bound, parity is broken and one transitions from $P_2$ to $P_1$ statements about $\phi_0$.

## What this would prove

Steps 1–3: would give a quantitative version of Iwaniec's $P_2$ theorem (probably with sharper constants). Step 4: would give density results for "interior primes." Step 5 (the moonshot): would either give Landau's 4th outright, or a strong partial result like "$\phi_0(n)$ has at most 2 prime factors with one of them in a specified small range, infinitely often."

## What's missing

- A precise enough bilinear estimate for SL₂(ℕ₀) cross-terms — this is real research, not yet done.
- Spectral gap for the transfer operator on congruence quotients of $\mathcal{D}_{\phi_0}$ — needs adapting BGS technology to free monoids.
- A Mauduit–Rivat-style argument for level sets of $\mathcal{S}$ (rather than partial sums) — a *new theorem* in automatic-sequence theory would be required. See [[B4-S-sequence-density]].

## Conclusion — the Shakov contribution

Shakov's paper does NOT itself prove Landau. But it gives a **new combinatorial/algebraic encoding** of the problem in which:

- The bilinear structure is exposed.
- The free monoid gives clean sums.
- The quadruple coupling gives auxiliary structure.
- The 2-regular sequence gives access to fractal asymptotic theory.

It is the combination of these features that I believe represents a genuinely new angle. **The conventional toolbox (sieves, automorphic forms) plus the Shakov framework is greater than either alone.**

The next step is to actually do the technical work in steps 1-3 above, while in parallel pushing on the [[B6-open-questions|sub-problems]]. Even the *Tier 1* questions (Q1: combinatorial closed form for $\mathcal{S}$; Q2: numerical Bateman–Horn check; Q3: significance of the eigenvalue $(5+\sqrt{17})/2$) would be informative immediately.
