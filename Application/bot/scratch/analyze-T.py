"""
Analyze the saved T(N) cumulative array.
Look for structure in T(N)/sqrt(N): is it bounded? Oscillatory? Mean zero?
What's the empirical RMS?  What is the histogram?
"""
import pickle
import math
import statistics

with open('/home/user/mathAI/bot/scratch/Tcum.pkl', 'rb') as f:
    data = pickle.load(f)  # list of (N, T(N)) for sparse N

# Filter to N >= 1000 (small N has too much noise from initial transients)
data = [(N, T) for (N, T) in data if N >= 1000]
print(f"{len(data)} sample points, N range [{data[0][0]}, {data[-1][0]}]")

# Compute T/sqrt(N) and T/(sqrt(N)*log(N))
ratios_sqrt = [T / math.sqrt(N) for (N, T) in data]
ratios_sqrtlog = [T / (math.sqrt(N) * math.log(N)) for (N, T) in data]

def stats(name, xs):
    m = statistics.mean(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0
    mn, mx = min(xs), max(xs)
    rms = math.sqrt(sum(x*x for x in xs) / len(xs))
    print(f"  {name}: mean={m:+.4f}  rms={rms:.4f}  std={sd:.4f}  range=[{mn:+.3f}, {mx:+.3f}]")

print("\nFull range:")
stats("T/sqrt(N)", ratios_sqrt)
stats("T/(sqrt(N)*log(N))", ratios_sqrtlog)

# Decade-by-decade
print("\nBy decade:")
for lo, hi in [(1e3, 1e4), (1e4, 1e5), (1e5, 1e6), (1e6, 1e7), (1e7, 5e7)]:
    sub = [(N, T) for (N, T) in data if lo <= N < hi]
    if not sub:
        continue
    rs = [T / math.sqrt(N) for (N, T) in sub]
    print(f"\n  N in [{lo:.0e}, {hi:.0e}], {len(sub)} samples:")
    stats("    T/sqrt(N)", rs)
    rsl = [T / (math.sqrt(N) * math.log(N)) for (N, T) in sub]
    stats("    T/(sqrt(N)*log(N))", rsl)

# Sign distribution
pos = sum(1 for r in ratios_sqrt if r > 0)
neg = sum(1 for r in ratios_sqrt if r < 0)
zero = sum(1 for r in ratios_sqrt if r == 0)
print(f"\nSign: +{pos}, -{neg}, 0:{zero}")

# Largest |T(N)/sqrt(N)| values
sorted_by_mag = sorted(data, key=lambda x: -abs(x[1])/math.sqrt(x[0]))[:10]
print("\nTop 10 |T/sqrt(N)|:")
for N, T in sorted_by_mag:
    print(f"  N={N:>10d}  T={T:>+8d}  T/sqrt(N)={T/math.sqrt(N):+.4f}")

# Look for asymptotic average  T(N)/sqrt(N) over [N/2, N] — does the AVERAGE
# of T(M)/sqrt(M) for M in [N/2, N] approach a limit?
print("\nWindowed average of T(M)/sqrt(M) for M in [N/2, N]:")
N_max = data[-1][0]
for N in [1e5, 1e6, 1e7, 5e7]:
    if N > N_max: continue
    sub = [(M, T) for (M, T) in data if N/2 <= M <= N]
    rs = [T/math.sqrt(M) for (M, T) in sub]
    if rs:
        print(f"  N={int(N):>10d}  window [{int(N/2)}, {int(N)}], n={len(rs)}: mean={statistics.mean(rs):+.4f}  rms={math.sqrt(sum(r*r for r in rs)/len(rs)):.4f}")

# Plot crude ASCII of T(N)/sqrt(N) vs log(N) to spot oscillation
print("\nASCII trajectory (T/sqrt(N) vs log10(N)):")
import bisect
buckets = []
log_N_vals = [math.log10(N) for (N, T) in data]
for i, (N, T) in enumerate(data):
    if i % max(1, len(data)//40) == 0:
        r = T / math.sqrt(N)
        buckets.append((log_N_vals[i], r))
WIDTH = 60
mx = max(abs(r) for _, r in buckets)
for lN, r in buckets:
    pos = int(WIDTH/2 + (r/mx) * (WIDTH/2))
    pos = max(0, min(WIDTH, pos))
    line = [' '] * (WIDTH+1)
    line[WIDTH//2] = '|'
    line[pos] = '*'
    print(f"  logN={lN:5.2f}  r={r:+6.3f} |{''.join(line)}|")
