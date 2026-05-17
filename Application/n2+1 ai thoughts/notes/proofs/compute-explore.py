"""
Computational exploration of SL_2(N_0) tree structure for n^2+1.

Goal: find new identities and patterns not yet noticed in the existing notes.

Strategy:
1. Generate the Phi_0 tree to depth K.
2. Compute various spin/character functions on each matrix.
3. Look at cumulative sums and partial cancellation.
4. Compute moments, fiber sizes, joint statistics.
"""

import math
from collections import defaultdict, Counter
from fractions import Fraction

# Generators of SL_2(N_0)
def matmul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)

S = (1, 1, 0, 1)  # [[1,1],[0,1]]
T = (1, 0, 1, 1)  # [[1,0],[1,1]]
I_mat = (1, 0, 0, 1)

def cross_term_phi0(A):
    """For phi_0 = n^2+1: chi(A) = ac + bd."""
    a, b, c, d = A
    return a*c + b*d

def m_phi0(A):
    """Norm a^2 + b^2, the divisor of n^2+1 produced."""
    a, b, c, d = A
    return a*a + b*b

def in_interior(A):
    """A is in SL_2(N), strict interior."""
    return all(x > 0 for x in A)

def gen_tree_to_depth(K):
    """Generate all matrices with S/T words of length <= K, paired with the word."""
    # word is a tuple of 'S' and 'T' chars
    out = [(I_mat, ())]
    current = [(I_mat, ())]
    for _ in range(K):
        nxt = []
        for A, w in current:
            nxt.append((matmul(A, S), w + ('S',)))
            nxt.append((matmul(A, T), w + ('T',)))
        out.extend(nxt)
        current = nxt
    return out

def gen_tree_by_cross_bound(N):
    """Generate all A in SL_2(N_0) with chi(A) <= N. BFS by left-multiplication."""
    seen = {I_mat: ()}
    queue = [(I_mat, ())]
    out = []
    while queue:
        A, w = queue.pop()
        if cross_term_phi0(A) > N:
            continue
        out.append((A, w))
        for gen, ch in [(S, 'S'), (T, 'T')]:
            B = matmul(A, gen)
            if cross_term_phi0(B) <= N and B not in seen:
                seen[B] = w + (ch,)
                queue.append((B, w + (ch,)))
    return out

# -------------------------------------------------------------------------
# 1. Verify the trivial-bound identity #X_N = 1 + sum_{n<=N} tau(n^2+1)
# -------------------------------------------------------------------------

def tau_n2_plus_1(n):
    """Number of divisors of n^2+1."""
    v = n*n + 1
    cnt = 0
    i = 1
    while i*i <= v:
        if v % i == 0:
            cnt += 1
            if i*i != v:
                cnt += 1
        i += 1
    return cnt

print("=" * 70)
print("Test 1: Verify #{A in SL_2(N_0): chi(A) <= N} = 1 + sum_{n=1}^N tau(n^2+1)")
print("=" * 70)
for N in [10, 20, 50, 100]:
    matrices = gen_tree_by_cross_bound(N)
    expected = 1 + sum(tau_n2_plus_1(n) for n in range(1, N+1))
    print(f"  N={N:4d}: |X_N|={len(matrices):6d}, 1+sum_tau={expected:6d}, match={len(matrices)==expected}")

# -------------------------------------------------------------------------
# 2. Spin functions and cumulative sums
# -------------------------------------------------------------------------

def num_T(w):
    return sum(1 for c in w if c == 'T')

def num_S(w):
    return sum(1 for c in w if c == 'S')

def fi_spin_gaussian(a, b):
    """Friedlander-Iwaniec spin for primary Gaussian integers.
    Defined for a^2+b^2 odd, then extended.
    Standard normalization: alpha = a + bi primary if a odd, b even, a+b ≡ 1 (mod 4).
    Spin tracks the sign change under unit multiplication.

    Here we use a simpler character: the Jacobi/Kronecker symbol-like character.
    spin(alpha) = 1 if alpha is primary, -1 if its associate is primary.

    For simplicity let's use: chi(alpha) = (-1)^((a-1)/2) when a odd, b even.
    This is sign of Re(alpha)'s residue mod 4 after primary normalization.
    """
    if (a*a + b*b) % 2 == 0:
        return 0  # ramified prime case
    # Find the unique associate with a' odd, b' even, a'+b' ≡ 1 mod 4
    candidates = [(a, b), (-b, a), (-a, -b), (b, -a)]
    for ap, bp in candidates:
        if ap % 2 == 1 and bp % 2 == 0 and (ap + bp) % 4 == 1:
            return 1 if ap == a and bp == b else -1
    return 0

print()
print("=" * 70)
print("Test 2: Various spin functions, their cumulative sums on chi(A) <= N")
print("=" * 70)

# Compute several spins
def analyze_spins(N):
    matrices = gen_tree_by_cross_bound(N)
    # Group by cross-term value
    by_n = defaultdict(list)
    for A, w in matrices:
        n = cross_term_phi0(A)
        by_n[n].append((A, w))

    # Spins to try
    results = {
        'T_parity': 0,         # (-1)^#T
        'S_parity': 0,         # (-1)^#S  -- same as T_parity mod 2 (length parity)
        'word_length': 0,      # (-1)^|w|
        'mu_word': 0,          # mu of word: 0 if any double letter, else (-1)^|w|
        'gaussian_sign': 0,    # sign of the (a-bi) Gaussian factor under unit norm
        'interior_only': 0,    # 1 on interior, 0 on boundary; counts interior matrices
    }

    for A, w in matrices:
        if A == I_mat:
            continue
        a, b, c, d = A
        # T_parity
        results['T_parity'] += (-1)**num_T(w)
        # S_parity
        results['S_parity'] += (-1)**num_S(w)
        # word length parity
        results['word_length'] += (-1)**len(w)
        # Möbius-word: 0 if word has SS or TT consecutive, else (-1)^|w|
        if any(w[i] == w[i+1] for i in range(len(w)-1)):
            mu = 0
        else:
            mu = (-1)**len(w)
        results['mu_word'] += mu
        # interior count
        if in_interior(A):
            results['interior_only'] += 1

    return results, len(matrices)

for N in [10, 50, 100, 500, 1000]:
    res, total = analyze_spins(N)
    print(f"  N={N:5d} (total={total:6d}):")
    for name, val in res.items():
        print(f"    {name:20s}: {val:8d}")

# -------------------------------------------------------------------------
# 3. Better spin candidates: FI-primary character on Gaussian factors
# -------------------------------------------------------------------------

def fi_primary_spin(a, b):
    """FI-primary spin of alpha = a + bi.
    Returns:
       0 if alpha divisible by (1+i) [i.e., a+b odd is impossible in coprime case;
                                      better: a^2+b^2 even means alpha~(1+i)k]
       +1 if alpha is primary (a odd, b even, a+b ≡ 1 (mod 4))
       -1 if -alpha is primary
       else: classify via associate. Multiplication by i takes (a,b)->(-b,a).
    """
    if (a*a + b*b) == 0:
        return 0
    # If alpha divisible by 1+i: (a+b) and (a-b) both even, i.e., a,b same parity.
    if (a + b) % 2 == 0:
        return 0  # not coprime to ramified prime
    # Now a+b is odd, so exactly one of a,b is even.
    # Find the unique associate (a',b') with a' odd, b' even.
    # Associates: (a,b), (-b,a), (-a,-b), (b,-a)
    for (ap, bp), sign in [((a, b), 1), ((-b, a), 1), ((-a, -b), 1), ((b, -a), 1)]:
        # Just pick the one with a' odd, b' even
        if ap % 2 != 0 and bp % 2 == 0:
            # Check primary condition: a' + b' ≡ 1 mod 4
            if (ap + bp) % 4 == 1:
                # +1 if (ap,bp) == (a,b) or (-a,-b), -1 otherwise
                return 1 if (ap, bp) in [(a, b), (-a, -b)] else -1
            else:
                # The opposite associate is primary
                return -1 if (ap, bp) in [(a, b), (-a, -b)] else 1
    return 0  # unreachable if a+b odd

# Test the spin
print()
print("FI primary spin on small Gaussian integers (1 + ki):")
for k in range(0, 12):
    s = fi_primary_spin(1, k)
    print(f"  alpha = 1 + {k}i, spin = {s}")

print()
print("Spin on (k + 1*i) [for T^k case]:")
for k in range(0, 12):
    s = fi_primary_spin(k, 1)
    print(f"  alpha = {k} + i, spin = {s}")

# Now apply FI spin to all matrices and look at cumulative sums
print()
print("=" * 70)
print("Test 3: FI primary spin on Gaussian factor xi = a - bi (or a + bi)")
print("=" * 70)

def fi_spin_sums(N):
    matrices = gen_tree_by_cross_bound(N)
    total = 0
    s_xi = 0    # spin(a - bi) = spin(a, -b) = spin(a, b) since b -> -b just changes sign of i
    s_eta = 0   # spin(c + di) = spin(c, d)
    s_prod = 0  # spin(xi) * spin(eta)
    s_xi_int = 0  # interior only
    s_prod_int = 0
    for A, w in matrices:
        if A == I_mat:
            continue
        a, b, c, d = A
        # Note: alpha = a - bi ~ (a, -b) for spin; but spin only depends on (|a|, |b|, parity, mod 4)
        # spin is invariant under unit multiplication; (a, -b) and (a, b) related by complex conjugation
        # which is NOT unit multiplication, so spin can differ. Let's compute both.
        s1 = fi_primary_spin(a, -b)  # for xi = a - bi
        s2 = fi_primary_spin(c, d)   # for eta = c + di
        s_xi += s1
        s_eta += s2
        s_prod += s1 * s2
        if in_interior(A):
            s_xi_int += s1
            s_prod_int += s1 * s2
        total += 1
    return total, s_xi, s_eta, s_prod, s_xi_int, s_prod_int

for N in [10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]:
    total, s_xi, s_eta, s_prod, s_xi_int, s_prod_int = fi_spin_sums(N)
    print(f"  N={N:5d} (total={total:7d}):")
    print(f"    sum spin(xi)*spin(eta): {s_prod:8d}")

# Test hypothesis: inner sum at fixed n equals tau(n^2+1) * chi_4(n+1)?
print()
print("=" * 70)
print("Test 4: Does inner sum at fixed n equal tau(n^2+1) * chi_4(n+1)?")
print("=" * 70)

def chi4(n):
    n = n % 4
    if n == 1: return 1
    if n == 3: return -1
    return 0

N_test = 200
matrices = gen_tree_by_cross_bound(N_test)
inner_sum = defaultdict(int)
for A, w in matrices:
    if A == I_mat:
        continue
    a, b, c, d = A
    n = cross_term_phi0(A)
    inner_sum[n] += fi_primary_spin(a, -b) * fi_primary_spin(c, d)

print(f"  n  tau(n^2+1)  chi_4(n+1)  predicted  observed  match")
mismatches = 0
for n in range(1, N_test+1):
    predicted = tau_n2_plus_1(n) * chi4(n+1)
    observed = inner_sum[n]
    match = "OK" if predicted == observed else "FAIL"
    if predicted != observed:
        mismatches += 1
    if n <= 30 or predicted != observed:
        print(f"  {n:3d}  {tau_n2_plus_1(n):8d}    {chi4(n+1):4d}      {predicted:6d}    {observed:6d}   {match}")
print(f"\n  Total mismatches in n=1..{N_test}: {mismatches}")

# Now compute the closed-form cumulative sum T(N) = sum tau(n^2+1) chi_4(n+1)
# directly and compare to our bilinear spin sum
print()
print("=" * 70)
print("Test 5: Cumulative T(N) = sum_{n<=N} tau(n^2+1) * chi_4(n+1)")
print("Verify it matches the bilinear spin sum, and look at growth")
print("=" * 70)

def T_direct(N):
    return sum(tau_n2_plus_1(n) * chi4(n+1) for n in range(1, N+1))

print(f"  N      T(N) direct    s_prod from matrix sum")
for N in [10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]:
    T = T_direct(N)
    print(f"  {N:5d}    {T:8d}")

# extend with direct computation to much higher N
print()
print("Push T(N) to larger N (direct computation, no matrix enum):")
for N in [50000, 100000, 200000, 500000, 1000000]:
    T = T_direct(N)
    print(f"  N = {N:8d}: T(N) = {T:8d}, |T(N)|/sqrt(N) = {abs(T)/math.sqrt(N):.4f}, |T(N)|/log(N) = {abs(T)/math.log(N):.4f}")





