# R4 — Binary quadratic forms, Gauss composition, and Shakov's four polynomials

A **binary quadratic form** is a homogeneous polynomial $Q(x,y) = ax^2 + bxy + cy^2$ with $a,b,c \in \mathbb{Z}$. Its **discriminant** is $\Delta = b^2 - 4ac$. The four norm forms attached to Shakov's enumerable polynomials (see [[../concepts/08-the-four-polynomials]]) are precisely:

| Polynomial | Norm form | $\Delta$ | Order |
|---|---|---|---|
| $\phi_0 = n^2+1$ | $a^2+b^2$ | $-4$ | $\mathbb{Z}[i]$ |
| $\phi_1 = n^2+n+1$ | $a^2+ab+b^2$ | $-3$ | $\mathbb{Z}[\zeta_3]$ |
| $\psi_2 = n^2+2n-1$ | $a^2+2ab-b^2$ | $8$ | $\mathbb{Z}[\sqrt 2]$ |
| $\phi_3 = n^2+3n+1$ | $a^2+3ab+b^2$ | $5$ | $\mathbb{Z}[(1+\sqrt 5)/2]$ |

These are not just *any* four orders: they are the **four smallest absolute fundamental discriminants among all quadratic fields with class number 1** (two imaginary, two real). This is the conjectural structural reason for Shakov's classification.

## 1. Gauss composition and the form class group

Given a discriminant $\Delta$, primitive binary quadratic forms of discriminant $\Delta$ are partitioned into $SL_2(\mathbb{Z})$-equivalence classes, where $A = \begin{pmatrix}\alpha&\beta\\\gamma&\delta\end{pmatrix} \in SL_2(\mathbb{Z})$ acts by $(Q \cdot A)(x,y) = Q(\alpha x + \beta y,\ \gamma x + \delta y)$.

Gauss (Disquisitiones Arithmeticae §V) defined a binary operation — **composition** — on these classes that makes them an abelian group, the **form class group** $\mathrm{Cl}(\Delta)$. Modern reformulation (Dedekind, then Bhargava): for fundamental $\Delta$,
$$\mathrm{Cl}(\Delta) \;\cong\; \mathrm{Cl}^+(\mathcal{O}_\Delta),$$
the **narrow class group** of the quadratic order $\mathcal{O}_\Delta = \mathbb{Z}[(\Delta + \sqrt\Delta)/2]$. For $\Delta < 0$ this coincides with the ordinary class group; for $\Delta > 0$ it can be twice as large unless a unit of norm $-1$ exists ([Wikipedia: Fundamental unit](https://en.wikipedia.org/wiki/Fundamental_unit_(number_theory))). Bhargava (*Higher composition laws I*, Annals 159 (2004), 217–250 — see [Bhargava cube](https://en.wikipedia.org/wiki/Bhargava_cube)) recovered Gauss composition from $2\times 2\times 2$ integer cubes: a cube produces a triple $(Q_1, Q_2, Q_3)$ of forms of common discriminant whose Gauss product is the identity in $\mathrm{Cl}^+(\mathcal{O}_\Delta) \times \mathrm{Cl}^+(\mathcal{O}_\Delta)$.

The point for us: **the β-deformed Diophantus identities of [[../concepts/02-diophantus-identity]] are precisely the multiplicativity statement $N(\alpha)N(\beta)=N(\alpha\beta)$ for the relevant order** — i.e., the principal-class case of Gauss composition.

## 2. The four discriminants $-4, -3, 5, 8$

**Imaginary side.** By Stark–Heegner ([Heegner number, Wikipedia](https://en.wikipedia.org/wiki/Heegner_number)), the imaginary quadratic fields of class number 1 have $d \in \{-1,-2,-3,-7,-11,-19,-43,-67,-163\}$. The two smallest absolute fundamental discriminants are $-3$ and $-4$.

**Real side.** Real quadratic fields of class number 1 begin at $d = 2, 3, 5, 6, 7, \dots$ ([List of number fields with class number one, Wikipedia](https://en.wikipedia.org/wiki/List_of_number_fields_with_class_number_one)). The two smallest *fundamental* discriminants are $5$ (for $\mathbb{Q}(\sqrt 5)$) and $8$ (for $\mathbb{Q}(\sqrt 2)$). Both moreover have **narrow class number 1**: $\mathbb{Q}(\sqrt 5)$ has fundamental unit $(1+\sqrt 5)/2$ of norm $-1$, and $\mathbb{Q}(\sqrt 2)$ has fundamental unit $1+\sqrt 2$ of norm $-1$, so in both cases $\mathrm{Cl}^+ = \mathrm{Cl} = 1$.

So $\{-4, -3, 5, 8\}$ are exactly the four fundamental discriminants $\Delta$ with $|\Delta| \le 8$ **and** $h^+(\Delta) = 1$. The next candidate $-7$ (for $n^2+n+2$) also has $h=1$, but $f(0)=2 \ne 1$, breaking the size criterion (see [[../concepts/07-classification-theorem]]). The next real one $\Delta = 12$ (for $n^2 - 3$) has $\mathbb{Z}[\sqrt 3]$ which is *not* maximal (and has $h^+ = 2$), failing already on a different ground.

## 3. Primes represented — the Cox / class field theory picture

Cox's *Primes of the Form $x^2+ny^2$* (Wiley 1989; AMS Chelsea 3rd ed. 2022) gives the canonical treatment. For a fundamental discriminant $\Delta$ of class number 1, **every** form of discriminant $\Delta$ is $SL_2(\mathbb{Z})$-equivalent to the unique reduced (principal) form. A prime $p \nmid \Delta$ is represented by *some* form of discriminant $\Delta$ iff $\left(\frac{\Delta}{p}\right) = 1$, i.e. iff $p$ splits in $\mathcal{O}_\Delta$. Since there is only one form-class, "some form" $=$ "the principal form":

- $p = a^2+b^2 \iff p=2$ or $p\equiv 1 \pmod 4$ (Fermat).
- $p = a^2+ab+b^2 \iff p=3$ or $p\equiv 1 \pmod 3$.
- $p = a^2 - 2b^2 \iff p=2$ or $p \equiv \pm 1 \pmod 8$.
- $p = a^2+ab-b^2$ (disc 5) $\iff p=5$ or $p\equiv \pm 1 \pmod 5$.

These four congruence characterizations match exactly the prime-representation rows in [[../concepts/08-the-four-polynomials]]. The class-field-theoretic content: $p$ splits completely in the **ring class field** of the order $\mathcal{O}_\Delta$, which for class number 1 reduces to "$p$ splits in $K$", a Frobenius / quadratic-reciprocity condition.

For details and proofs see Cox (cited above); a clean undergraduate write-up is Stevenhagen, *Primes Represented by Quadratic Forms* (Leiden lecture notes, [PDF](https://websites.math.leidenuniv.nl/algebra/Stevenhagen-Primes.pdf)) and the Chicago REU paper Skenderi, *Quadratic forms, reciprocity laws, and primes of the form $x^2+ny^2$* ([PDF](http://math.uchicago.edu/~may/REU2018/REUPapers/Skenderi.pdf)).

## 4. $SL_2(\mathbb{Z})$ reduction and the role of $SL_2(\mathbb{N}_0)$

**Reduction theory.** Every primitive form is $SL_2(\mathbb{Z})$-equivalent to a unique *reduced* form: for $\Delta < 0$ the conditions are $|b| \le a \le c$ with $b\ge 0$ if $|b|=a$ or $a=c$; for $\Delta > 0$ a periodic continued-fraction reduction yields a finite cycle of reduced forms (Buell, *Binary Quadratic Forms*, Springer 1989, Chs. 2–3; also Beshaj, *Reduction theory of binary forms*, [arXiv:1502.06289](https://arxiv.org/pdf/1502.06289); O'Sullivan, *Topographs for binary quadratic forms and class numbers*, [arXiv:2408.14405](https://arxiv.org/abs/2408.14405)). For class number 1 this reduced form is *unique* — there is exactly one reduced form per discriminant.

**The submonoid $SL_2(\mathbb{N}_0)$.** As noted in [[../concepts/01-sl2-n0-monoid]], $SL_2(\mathbb{N}_0)$ is the free monoid on $S = \begin{pmatrix}1&0\\1&1\end{pmatrix}$, $T = \begin{pmatrix}1&1\\0&1\end{pmatrix}$ (Nathanson 2014). These are exactly the matrices arising in the Stern–Brocot / Calkin–Wilf tree and in continued-fraction expansions: a word $S^{a_k} T^{a_{k-1}} \cdots$ encodes the CF $[a_0; a_1, \dots, a_k]$.

**The classical link to forms.** Markov's theorem on the Markov spectrum is exactly the statement that values of indefinite binary quadratic forms at integer points correspond to continued-fraction expansions, which are in turn $SL_2(\mathbb{N}_0)$-words (Karpenkov–Van-Son, *Generalised Markov numbers*, [PDF](https://pcwww.liv.ac.uk/~mvanson/papers/gmn.pdf); blog summary at [matheuscmss.wordpress.com](https://matheuscmss.wordpress.com/2018/12/30/continued-fractions-binary-quadratic-forms-and-markov-spectrum/)). The Markov tree itself is built from the same $S, T$ generators — so $SL_2(\mathbb{N}_0)$ is *the* combinatorial substrate connecting CFs, the Stern–Brocot tree, and form values.

## 5. Has anyone noticed the exact pattern?

A targeted search for prior work pairing the specific list $\{n^2+1, n^2+n+1, n^2+2n-1, n^2+3n+1\}$ with $SL_2(\mathbb{N}_0)$ enumeration returns **only Shakov's preprint** (*Polynomials in Z[x] whose divisors are enumerated by SL₂(ℕ₀)*, [arXiv:2405.03552](https://arxiv.org/pdf/2405.03552)). Adjacent literature exists — Markov forms, topographs, Bhargava composition — but no source explicitly singles out these four polynomials as a class. The discriminant coincidence appears genuinely novel from the combinatorial side, even though each individual polynomial is classical.

## Why this might explain Shakov's classification

**Hypothesis.** A monic positive-leading polynomial $f$ is enumerable by $SL_2(\mathbb{N}_0)$ iff it is the principal norm form of an order $\mathcal{O}$ in a quadratic field such that:

1. **(Class number 1)** $h^+(\mathcal{O}) = 1$, so every form of $\mathrm{disc}(\mathcal{O})$ is equivalent to the principal one — Gauss composition is trivial, and the multiplicative β-Diophantus identity ([[../concepts/02-diophantus-identity]]) suffices to capture *all* divisors;
2. **(Small discriminant / size)** $|\mathrm{disc}(\mathcal{O})| \le 8$, so the "principal form" $f(n) = N(n - \omega) = n^2 + \beta n \pm 1$ has constant term $\pm 1$ — this is exactly Shakov's size criterion $|f(n)| < (n+1)^2$ at the boundary;
3. **($SL_2(\mathbb{N}_0)$-reduction is unique on the nose)** The unique reduced form has the property that *every* $SL_2(\mathbb{Z})$-orbit representative in the principal class can be realized in the $\mathbb{N}_0$-cone — i.e. $SL_2(\mathbb{N}_0)$ already covers the orbit modulo the boundary involution.

Conditions (1)+(2) carve out exactly $\Delta \in \{-3,-4,5,8\}$. Condition (2) is the obstruction at $\Delta=-7$: the principal form $x^2+xy+2y^2$ has constant term $2$, so $\phi(0) = 2$ violates the size criterion; the order $\mathbb{Z}[(1+\sqrt{-7})/2]$ has class number 1 but does *not* give an enumerable polynomial. Condition (2) also excludes $\Delta = 12, 13, \dots$ on the real side either by non-maximality, $h^+ > 1$, or constant-term failure.

**Predictions.**
- **No further enumerable monic quadratics exist** — confirmed by Shakov's [[../concepts/07-classification-theorem]].
- **No higher-degree enumerable polynomials**, because the relevant norm forms in cubic/higher orders are *not* binary quadratic, so $SL_2(\mathbb{N}_0)$ cannot enumerate their divisors. This matches Schildkraut's lemma ([[../concepts/09-carl-schildkraut-lemma]]) eliminating degree $\ge 3$.
- **Generalisation to higher rank** would replace $SL_2(\mathbb{N}_0)$ by an analogous positive-cone monoid in $SL_n(\mathbb{Z})$ (e.g. $SB(n,\mathbb{N})$ from the multidimensional Stern–Brocot construction). The natural conjecture: enumerable forms over rank-$n$ orders correspond to $n$-ary norm forms over orders with trivial narrow class group and minimal discriminant.

**What might be missing / where the hypothesis could fail.** The hypothesis as stated is necessary but perhaps not quite sufficient. Two candidate extra conditions:

(a) **Norm-$-1$ unit**, ensuring $\mathrm{Cl} = \mathrm{Cl}^+$ on the real side. Both $\mathbb{Z}[\sqrt 2]$ and $\mathbb{Z}[(1+\sqrt 5)/2]$ have such a unit; the next real candidate $\mathbb{Z}[\sqrt 3]$ (disc 12) does not, and indeed $h^+(\mathbb{Q}(\sqrt 3)) = 2$.

(b) **Compatibility of $SL_2(\mathbb{N}_0)$-words with the ring's reduction algorithm.** For class number 1, reduction terminates at the principal form via a continued-fraction step, which is a sequence of $S$ and $T$ multiplications. For larger class number, reduction would need to hit *several* inequivalent reduced forms, breaking unique factorization in $SL_2(\mathbb{N}_0)$.

If the hypothesis is correct, Shakov's combinatorial classification is a genuine *shadow of class field theory*: the enumerability of divisors of a quadratic polynomial is equivalent to triviality of Gauss composition for its discriminant, packaged combinatorially through the free monoid structure of $SL_2(\mathbb{N}_0)$.

---

### Source list

- David A. Cox, *Primes of the Form $x^2 + ny^2$*, Wiley 1989; AMS Chelsea 3rd ed. 2022 — [PDF mirror](https://www.math.utoronto.ca/~ila/Cox-Primes_of_the_form_x2+ny2.pdf).
- D. Buell, *Binary Quadratic Forms*, Springer 1989.
- M. Bhargava, *Higher composition laws I: A new view on Gauss composition*, Annals of Math. 159 (2004), 217–250 — [PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n1-p03.pdf).
- M. Bhargava, *Higher composition laws II*, Annals 159 (2004), 865–886 — [PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n2-p09.pdf).
- K. Stange, *Notes on Bhargava's composition laws* — [PDF](https://math.colorado.edu/~kstange/papers/notes-on-Bhargava.pdf).
- P. Stevenhagen, *Primes Represented by Quadratic Forms* — [PDF](https://websites.math.leidenuniv.nl/algebra/Stevenhagen-Primes.pdf).
- L. Beshaj, *Reduction theory of binary forms* — [arXiv:1502.06289](https://arxiv.org/pdf/1502.06289).
- C. O'Sullivan, *Topographs for binary quadratic forms and class numbers* — [arXiv:2408.14405](https://arxiv.org/abs/2408.14405).
- O. Karpenkov, M. Van-Son, *Generalised Markov numbers* — [PDF](https://pcwww.liv.ac.uk/~mvanson/papers/gmn.pdf).
- [Wikipedia: Heegner number](https://en.wikipedia.org/wiki/Heegner_number); [Class number problem](https://en.wikipedia.org/wiki/Class_number_problem); [List of number fields with class number one](https://en.wikipedia.org/wiki/List_of_number_fields_with_class_number_one); [Bhargava cube](https://en.wikipedia.org/wiki/Bhargava_cube); [Fundamental unit](https://en.wikipedia.org/wiki/Fundamental_unit_(number_theory)); [Binary quadratic form](https://en.wikipedia.org/wiki/Binary_quadratic_form).
- A. Shakov, *Polynomials in $\mathbb{Z}[x]$ whose divisors are enumerated by $SL_2(\mathbb{N}_0)$* — [arXiv:2405.03552](https://arxiv.org/pdf/2405.03552) (the paper under study).
