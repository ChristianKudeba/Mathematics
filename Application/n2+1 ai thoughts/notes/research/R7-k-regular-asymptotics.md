# R7. Asymptotics of k-regular sequences (Allouche–Shallit, Heuberger–Krenn)

## 1. The Allouche–Shallit framework

A sequence f: N -> R (R a Noetherian ring) is **k-regular** iff its **k-kernel**
K_k(f) = { (f(k^e n + r))_{n>=0} : e>=0, 0<=r<k^e } generates a finitely generated R-module
(Allouche & Shallit, "The ring of k-regular sequences," *Theor. Comput. Sci.* **98** (1992) 163–197,
doi:10.1016/0304-3975(92)90001-V; sequel: *TCS* **307** (2003) 3–29).

Equivalent characterisations:

- (Linear representation.) There exist a row vector v in Q^d, a column vector w in Q^d, and matrices
  A_0,...,A_{k-1} in Q^{d x d} such that f(n) = v · A_{d_0} A_{d_1} ... A_{d_{L-1}} · w where
  d_0 d_1 ... d_{L-1} is the base-k expansion of n. This is the "matrix product" form.
- (Schutzenberger / rational power series.) The formal series sum f(n) x^n is R-recognisable in the
  free monoid on k symbols.
- (k-automatic case.) f is k-automatic iff it is k-regular and takes finitely many values
  (Allouche–Shallit, *Automatic Sequences*, CUP 2003, Thm 16.1.5).

**Closure properties.** k-regular sequences form a ring under termwise addition and termwise
multiplication; they are closed under Cauchy product, scaling by integers, and termwise application of
polynomials (Allouche–Shallit 1992, Thm 2.5–2.6). Standard examples: the ruler sequence
nu_2(n+1), Stern's diatomic sequence, the binary digit sum s_2(n), the number of nonzero entries in
row n of Pascal mod 2.

**Growth.** A k-regular integer sequence grows at most polynomially in n; the precise exponent is
governed by the joint spectral radius rho(A_0,...,A_{k-1}) (Allouche–Shallit 1992, Thm 2.10;
Wikipedia "k-regular sequence"; Coons–Spiegelhofer chapter in Berthe–Rigo, *Combinatorics, Words and
Symbolic Dynamics*, 2016).

## 2. Heuberger–Krenn asymptotics for summatory functions

**Heuberger & Krenn, "Asymptotic Analysis of Regular Sequences," *Algorithmica* **82** (2020)
429–508**, doi:10.1007/s00453-019-00631-3 (arXiv:1810.13178). The main theorem states: let
F(N) = sum_{0<=n<N} f(n). Then F(N) admits an asymptotic decomposition

  F(N) = sum_{lambda} N^{log_k|lambda|} · sum_{j} (log N)^j · Phi_{lambda,j}(log_k N) + O(N^{log_k rho + epsilon})

where the outer sum is over eigenvalues lambda of B := A_0 + ... + A_{k-1} with |lambda| > rho (the
joint spectral radius of the A_i), the inner sum is over j = 0,..., m(lambda)-1 with m(lambda) the
size of the largest Jordan block of lambda in B, and Phi_{lambda,j} are 1-periodic Holder-continuous
"fractal" functions. The Phi are obtained as Fourier series whose coefficients are residues of the
Dirichlet series sum f(n)/n^s (Mellin–Perron; pseudo-Tauberian argument needed because the series
typically only converges conditionally).

This generalises and tightens earlier work of Dumas (*Asymptotic Expansions of Linear Recurrence
Sequences*, J. Algorithms 1993; "Asymptotic analysis of the sum of digits of n!", etc.) and of
Flajolet–Grabner–Kirschenhofer–Prodinger–Tichy on digital sums. A subsequent strengthening
("Lifting restrictions on the analysis of summatory functions of regular sequences," arXiv:1808.00842)
removed previous regularity hypotheses.

**Heuberger, Krenn & Lipnik, "Asymptotic Analysis of q-Recursive Sequences," *Algorithmica* **84**
(2022) 2480–2532**, doi:10.1007/s00453-022-00950-y (arXiv:2105.04334). Defines q-recursive sequences
(specified by recurrences on subsequences modulo powers of q), proves they are q-regular, and produces
*exact* (no error term) summatory formulae for Stern's diatomic sequence, the count of nonzero
entries in generalised Pascal triangles, and unbordered factor counts in Thue–Morse.

**Krenn & Shallit, "Strongly k-recursive sequences," arXiv:2401.14231 (2024)**. Defines strongly
k-recursive sequences as a proper subclass of k-regular: the defining linear relations expressing
(f(k^t n + b))_n as combinations of (f(k^r n + a))_n must use only offsets 0 <= a < k^t. Every
k-automatic sequence is strongly k-recursive; the example g_{k,l}(n) = 1 + l^{floor(log_k n)} is
k-regular but not k-recursive; the Delannoy-type sequence h is 3-regular but not strongly 3-recursive.

## 3. Spectral structure when 1 is the only eigenvalue (the Shakov case)

For Shakov's S, L = [[0,1,0],[-1,2,0],[0,2,1]] has characteristic polynomial (1-lambda)^3 and is *not*
diagonalisable: it is a single Jordan block J_3(1) = I + N (up to conjugation), where N is nilpotent
with N^3 = 0. The other matrix R is similarly unipotent. Then B := L + R has eigenvalues all equal
to 2 (= sum of diagonals along the Jordan structure of each summand)—**this is the key point that
controls the leading-order asymptotics in Heuberger–Krenn**. With k = 2, log_2 |2| = 1, and the
maximal Jordan block of 2 in B = L + R can have size up to 3, giving a leading term

  F(N) ~ N · (a (log N)^2 + b log N + c) · Phi(log_2 N)

with Phi 1-periodic. The joint spectral radius of {L, R} is at least 1 (since each is unipotent with
|lambda|=1 across its spectrum) and can be computed from finite products; if rho({L,R}) < 2 then the
above is the genuine main term and the error is O(N^{log_2 rho + epsilon}). General references for
the spectral case:

- Dumas, "Joint spectral radius, dilation equations, and asymptotic behavior of radix-rational
  sequences," *Linear Algebra Appl.* **438** (2013) 2107–2126, hal-00780568.
- Heuberger–Krenn–Lipnik, "A note on the relation between recognisable series and regular sequences,"
  arXiv:2201.13446 (2022).
- Drmota, "A master theorem for discrete divide-and-conquer recurrences," J. ACM 2013.

The unipotent case (only eigenvalue 1) has been studied less than the dominant-eigenvalue case but is
covered by the general framework: it just produces poly-log corrections rather than power growth.

## 4. Stern's diatomic sequence as a parallel

Stern's a(n) (OEIS A002487) satisfies a(2n)=a(n), a(2n+1)=a(n)+a(n+1) with linear representation by
A_0 = [[1,0],[1,1]], A_1 = [[1,1],[0,1]]; it is 2-regular. Northshield's *Amer. Math. Monthly* **117**
(2010) 581–598 survey ("Stern's Diatomic Sequence 0,1,1,2,1,3,2,3,1,4,...") proves a(n+1) = number
of hyperbinary representations of n and surveys the analogues with Fibonacci, the Calkin–Wilf
enumeration of Q+, and the fractal scaling limit. The summatory function S_Stern(N) ~ (3/2) N
log_2(3/2) · Phi(log_2 N) + lower order; precise formulae appear in Coons–Spiegelhofer and in
Heuberger–Krenn–Lipnik 2022 §5. **No closed form is known for level-set cardinalities |a^{-1}(n)| of
Stern's sequence**; this is exactly the structural analogue of the open problem for Shakov's S.

## Bridge to Shakov's framework

1. **Heuberger–Krenn (Algorithmica 2020) gives the partial sum**
   sum_{k<N} S(k) immediately: write down the linear representation v, w, A_0, A_1, A_2, A_3 (for the
   4-regular form of Shakov's recursion, which collapses to a 2-regular one of dimension 3), compute
   B = A_0 + A_1 + A_2 + A_3, find its Jordan form. Triple eigenvalue 1 in L (and similar for R)
   suggests Spec(B) is concentrated near small integers; with 4 summing matrices the leading term will
   be N · (poly in log N) · Phi(log_2 N). **The missing piece for Landau is that we need fiber
   cardinalities |S^{-1}(n)|, not the summatory function.** The Heuberger–Krenn machinery gives
   sum_{k<N} 1_{S(k)=n} only after composing with characteristic functions, which destroys regularity.

2. **The triple Jordan block at lambda = 1 implies S(k) grows polynomially in log k**, not as any
   power k^alpha with alpha > 0. Concretely, ||L^m|| and ||R^m|| grow like m^2 since
   (I+N)^m = I + m N + binom(m,2) N^2. So S(k) = O((log k)^2). This matches the empirical values
   0,1,1,2,3,3,2,3,7,8,5,5,8,7,3,...: extremely slow growth. The fiber |S^{-1}(n)| = tau(n^2+1)
   identity is then consistent with each value n being hit ~ tau(n^2+1) times among k <= 2^{c sqrt n}.

3. **Krenn–Shallit's strongly k-recursive class (arXiv:2401.14231) is a natural target**: check
   whether Shakov's S is strongly 4-recursive. The recursion S(4k+r) involves S(2k), S(2k+1), S(k)—
   the appearance of S(k) (offset 0, but at scale k = 4k/4 with r' = k mod 4 varying) is the suspicious
   part; the strongly-recursive condition demands that the right-hand subsequences live at a uniform
   smaller scale. If S fails to be strongly k-recursive, that already places it in the harder regime
   where Heuberger–Krenn's "exact formula" results (their Stern-style theorems) do not directly apply.

4. **Stern is the analogue.** Both sequences are 2-regular, both have unipotent linear
   representations, both have closed-form fiber sizes (Stern: hyperbinary representations; Shakov:
   tau(n^2+1)). For Stern the fiber-size question is essentially trivial (combinatorial bijection); for
   Shakov it is Landau IV. The contrast highlights that Shakov's recursion encodes arithmetic
   information (the divisor function of n^2+1) that Stern's does not. Identifying *which* feature of
   Shakov's matrices L, R produces this arithmetic content—presumably the determinant-1, SL_3(Z)
   structure not present in Stern's GL_2 matrices—is the natural research direction.

## References

- Allouche & Shallit, "The ring of k-regular sequences," *Theor. Comput. Sci.* 98 (1992) 163–197.
- Allouche & Shallit, *Automatic Sequences*, Cambridge UP, 2003.
- Heuberger & Krenn, "Asymptotic Analysis of Regular Sequences," *Algorithmica* 82 (2020) 429–508.
  arXiv:1810.13178; doi:10.1007/s00453-019-00631-3.
- Heuberger, Krenn & Lipnik, "Asymptotic Analysis of q-Recursive Sequences," *Algorithmica* 84
  (2022) 2480–2532. arXiv:2105.04334; doi:10.1007/s00453-022-00950-y.
- Krenn & Shallit, "Strongly k-recursive sequences," arXiv:2401.14231 (2024).
- Dumas, "Joint spectral radius, dilation equations, and asymptotic behavior of radix-rational
  sequences," *Lin. Alg. Appl.* 438 (2013) 2107–2126.
- Northshield, "Stern's Diatomic Sequence 0,1,1,2,1,3,2,3,1,4,...," *Amer. Math. Monthly* 117
  (2010) 581–598.
- Coons & Spiegelhofer, ch. on regular sequences in *Combinatorics, Words and Symbolic Dynamics*
  (Berthe–Rigo eds.), CUP 2016.
- Drmota, "A master theorem for discrete divide-and-conquer recurrences," J. ACM 60 (2013) Art. 16.
