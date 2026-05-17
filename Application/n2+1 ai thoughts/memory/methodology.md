---
name: Research methodology — theory-building, not just analogy
description: How Anton wants me to do math: build theory, compute, test, create new math, not just apply known literature
type: feedback
originSessionId: 8cf0884f-055b-4942-b476-e31741aac3d6
---
Be a **theory-builder**, not just an analogy-applier or literature-search-and-apply machine.

**Why:** The default mode of "see a problem → find an analogous published technique → translate it" produces shallow work. Anton specifically wants me creating new mathematics, building genuine understanding from the ground up.

**How to apply:**

1. **Compute first, then theorize.** When facing a question (especially about the four enumerable polynomials, the S-sequence, the spine sieve, etc.), take an aside and **actually do calculations**. Tabulate values for small $n$. Look for patterns by hand.

2. **Write Python when it helps.** For small-example exploration — checking which $f(n)$ are prime, computing fiber sizes, enumerating spine matrices, testing conjectured identities — write a small Python program and run it. Don't reason about what *should* happen; check what *does* happen.

3. **Summarize what I learned to myself before continuing.** After each computation/exploration aside, pause and write down (in a few lines) what I now understand. Then continue with the math informed by that understanding.

4. **Build new theory from the data.** When I see a numerical pattern, formulate it as a conjecture, then try to prove it from scratch — not by searching for "what literature has done analogously."

5. **Don't conflate research with creation.** Searching the literature (R1–R8 reports) is a service step. The actual research goal is **creating new math** that didn't exist before. Spend time in the create-mode.

6. **Pause cycle**: compute → observe → conjecture → test on more data → attempt proof from first principles → only then check whether existing literature applies.

This applies especially to questions like "is f(n), f(n+1), ..., f(n+k) prime for small n,k?" — where the right move is to compute, find the actual data, see what patterns emerge, *then* formulate theorems.
