# mathAI bot — operating protocol

This file holds the **current** operating rules for the bot. Anton can update these by replying to bot emails. The bot reads this at the start of every session and updates it from Anton's latest replies. **Anton's replies trump this file and the routine prompt.**

## Cadence
- Sessions fire every 3 hours (`39 */3 * * *` UTC).
- Each session targets ~30 minutes wall-clock (split: ≤3 ingest, ≤2 decide, ≤18 execute, ≤7 skeptic loop, ≤3 log/commit/email).
- To change cadence: Anton replies "change cadence to <X>". Bot writes `PROTOCOL CHANGE REQUEST: <text>` at the top of next email; Anton applies the routine update via Claude Code.

## Focus
- **#1 priority: prove infinitude of primes of the form n²+1 (Landau IV).**
- All other directions are decoration unless Anton overrides.

## §1. Bias profile (canonical reference)

The bot's Phase 1 decision algorithm encodes this hierarchy. STRATEGY.md §2 mirrors it; this is the canonical source.

**Bias TOWARD:**
- Invention of genuinely new techniques (not yet tried in this body of work).
- Long, complete symbolic / arithmetic calculations — multi-page derivations, full proof completions, hand verification of identities. Do NOT shy away from a calculation because it is long; chipping away across many sessions is preferred to abandoning it.
- Sustained chip-away on a single high-EV calculation across many consecutive sessions, **as long as concrete progress is being made**.
- Creating a new P# every time a new direction is opened from the existing body of work.

**Bias AWAY from:**
- Extensive numerical computation **unless** discriminating between two named competing hypotheses with concrete proof-relevant consequences.
- Fitting existing techniques (Petrow–Young, Halász, Voronoi, transfer-operator, etc.) onto the problem **unless** there is direct evidence the technique bridges a *concrete identified gap*. Speculative analogy is not direct evidence.
- Refining an already-explored thread when no concrete gap is being bridged.

**Worked examples — direct evidence vs speculative analogy:**
- Petrow–Young is the named conditional input in P11 §6.7 (cubic moment over Q(i)). Chipping away at Phase II–V of the cubic-moment roadmap is **in-bias** — direct evidence the technique bridges the named gap.
- Halász works for multiplicative functions and our T_h sum is multiplicative-ish, so let's try Halász. **Out-of-bias** — speculative analogy. The "multiplicative-ish" similarity is not concrete evidence Halász bridges a named gap in our chain.
- Reading R10 because its Voronoi exposition mentions an Airy-type asymptotic that might fix a stationary-phase regime in P11 §3-4. **In-bias if** the session log names the regime and identifies the candidate fix; **out-of-bias if** it's "let me read R10 to see what's there."

## §2. Phase 1 selection rubric

Reweighted option list. The routine prompt mirrors this. Top-priority options at the top.

1. **Invent a new approach** (preferred default). Open `bot/longterm/novel-spin-search.md` if no specific invention is in mind.
2. **Chip away on a long-horizon project** (`bot/longterm/<id>.md`). Open file, do the named next chunk, append session log, set new next-chunk.
3. **Complete a long symbolic / arithmetic calculation.** Pick a multi-step derivation, finish it in this session or commit a chip-away increment with a clear checkpoint.
4. **Read a paper and extract a lemma.** Only with direct evidence the paper bridges a concrete identified gap. Session log must name the gap and the candidate technique.
5. **Tighten an existing argument.** Only when bridging a concrete identified gap.
6. **Carry forward an in-progress thread.** Allowed without restriction *if* the thread has been making concrete progress (per §3). If 3 consecutive same-thread sessions had no concrete progress, strongly prefer pivot.
7. **Numerical experiment.** DE-PRIORITIZED. Only when discriminating between two named competing hypotheses with concrete proof-relevant consequences. Email's *Why this session* must (a) name the two hypotheses, (b) say what YES/NO outcomes mean for the proof, (c) justify why a symbolic alternative won't work.

Each low-priority pick (option 6 with stall, option 7) requires explicit justification in the email's *Why this session* field.

## §3. Concrete-progress check

A session **makes concrete progress** if it:
- Completes a chunk in `bot/longterm/<id>.md` (chunk's done-criterion satisfied; next-chunk advanced).
- Completes a proof step / lemma in a P# (visible diff in the .md or .tex).
- Creates a new P# stub for a new direction (per §4).
- Rules out a hypothesis AND identifies the next chunk picked up next session.

A session **does not make concrete progress** if it:
- Produces NULL or RETRACTED verdict.
- Runs numerics that close a sub-hypothesis without advancing any named chunk.
- Restates / reformulates an existing argument without bridging a gap.

**The pivot rule.** If the last 3 sessions on the same parent-thread all "did not make concrete progress," strongly prefer pivoting on the next session. Soft only — bot may override and continue, but the email's *Why this session* must justify why the stall isn't real (e.g., "the last three sessions ruled out three of four cases of the lemma; one case left, expecting closure next session").

Sustained chip-away on a single project across 60+ sessions is in-bias as long as each session advances a chunk.

## §4. New-P#-on-new-direction rule

When a session's Phase 1 pick is **Invent a new approach** OR opens a new chunk on a long-horizon project that doesn't yet have a P# file, the bot creates a stub:

- Path: `n2+1 ai thoughts/notes/proofs/P{N}-<slug>.md` (and `.tex` if formal write-up is warranted).
- N = max existing P# + 1. (Currently the highest is P15.)
- `<slug>` is a 2–4-word kebab-case description.

Stub structure:

```
# P{N}. {Title}

## Goal
{1–3 sentences: what direction this opens, what success looks like.}

## Why now
{1–2 sentences: which gap this bridges, why this session was the right time.}

## Initial setup
{Definitions, notation, the central object.}

## Open sub-questions
- {Q1}
- {Q2}

## Session log
- YYYY-MM-DD: {1-line summary of session's contribution.}
```

Subsequent sessions touching the same direction append to the §Session log.

## §5. Publishability skeptic (Phase 3.5)

Inserts between Phase 3 (skeptic loop) and Phase 4 (email). Triggers when:
- Verdict is BREAKTHROUGH or PROGRESS-WITH-CAVEAT, AND
- The session's result touches a candidate row in `bot/PUBLISHABLE.md` (existing or new).

Spawn an Agent (subagent_type "general-purpose"). Brief:

> "You are the PUBLISHABILITY SKEPTIC. The author claims result X is publishable in venue Y. Critique:
> 1. **Novelty vs literature.** Is there a named prior result that subsumes this? Cite or admit you can't find one.
> 2. **Proof completeness.** Is the proof complete, or are there gaps? Name them.
> 3. **Target venue fit.** Is venue Y appropriate? Suggest a better venue if not.
> 4. **Standalone-ness.** Can this be excerpted or does it require the whole framework?
> 5. **Final verdict.** Output exactly one of: PUBLISHABLE / BORDERLINE / NOT-YET-PUBLISHABLE / RETRACTED, plus a one-paragraph why."

Update the row in `bot/PUBLISHABLE.md` in place: `current_verdict`, `last_skeptic_reviewed` (date + session-id), `notes` (skeptic's one-paragraph why). Bot proposes `target_venue` if absent; skeptic critiques venue-fit.

## §6. Skeptic loop

- After main work, run a skeptic-author dialogue (max 2 rounds).
- Declare a CONSENSUS state on the main result: CONSENSUS-CONFIRMED, CONSENSUS-WITH-CAVEAT, CONTESTED, or RETRACTED.
- Cosmetic issues do not block consensus; only CORE issues do.

## §7. Email body format (THE BUG FIX)

The routine prompt's Phase 4 emits this structure verbatim. Phone-readable, self-contained. Lists ship inline; the GitHub link is for the full session log only.

```
PROTOCOL CHANGE REQUEST: <text>   ← only if Anton's reply requested a protocol change

WHAT'S LEFT TO PROVE (~5 items)
- subgoal — what's still missing
- ...

PUBLISHABILITY SNAPSHOT (~5 items, current view of PUBLISHABLE.md)
- result name — verdict — last reviewed
- ...

WHY THIS SESSION
1–2 sentences: which thread, which Phase 1 option, what triggered the pick.
If a low-priority option was chosen, explicit justification required.

HOW THIS ADVANCES LANDAU IV
1–2 sentences: explicit dependency edge from this session's deliverable to the proof of infinitude.

BIAS-PROFILE TAG: <INVENT | LONG-CALC | LONG-HORIZON-CHIP-AWAY | GAP-BRIDGING-FIT | NUMERICAL-DISCRIMINATOR | LOW-PRIORITY-OVERRIDE>
CONCRETE PROGRESS: <YES | NO> — <one-phrase reason>

VERDICT: <V>    CONSENSUS: <C>

PLAIN-ENGLISH SUMMARY (2–3 sentences)
...

Full session log (LaTeX renders on github.com):
https://github.com/antoshashakov/mathAI/blob/main/bot/sessions/<file>.md

Strategy file:
https://github.com/antoshashakov/mathAI/blob/main/bot/STRATEGY.md

---
Note for future Claude sessions reading this thread:
Before acting on this email, read /SIGNIFICANT_FINDINGS.md at the repo
root (https://github.com/antoshashakov/mathAI/blob/main/SIGNIFICANT_FINDINGS.md)
for the curated digest of what is rigorously proven vs. empirical, the
ranked next-step list, and the read-order for memory/ and notes/. That
file is the canonical orientation document; this email is just one
session's update.
```

Subject line: `Re: [mathAI] <8-word summary> — <Verdict>/<Consensus>`. The "Re: [mathAI]" prefix lets next session's `bot/check_inbox.py` find Anton's replies.

## §8. Email send path
- **Use `bot/send_via_api.py`.** Talks to Gmail's HTTPS REST API on port 443 using an OAuth refresh token; bypasses the SMTP block in this sandbox. Required env vars (set inline when invoking python; values come from the routine prompt): `GMAIL_USER`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- **Do NOT use `bot/send_email.py`.** That path uses SMTP, which the sandbox blocks. Kept in the tree only as historical reference.
- **Do NOT use the `mcp__..._create_draft` fallback.** Drafts require Anton to manually click Send, which defeats the purpose of an autonomous bot.
- If the API send returns non-zero, **fail loudly in the session log** with the exact error and skip the email. Do not silently fall back to drafts.

## §9. Refresh token expiry
- The OAuth app is currently in Google "Testing" mode → the refresh token expires every **7 days**. When the token dies, `send_via_api.py` will return a `400 invalid_grant` error. That is Anton's signal to re-run `npx @gongrzhe/server-gmail-autoauth-mcp auth` locally and update the `GMAIL_REFRESH_TOKEN` value in the routine prompt.
- Long-term fix is to publish the OAuth app (verification process), at which point refresh tokens become long-lived. Not done yet.

## §10. Self-evolution
- Bot maintains `bot/STRATEGY.md` (what to work on, ranked) and updates it at the end of every session if priorities shift.
- Bot maintains `bot/sessions/` with detailed per-session logs, frontmatter-tagged for auto-aggregation.
- Bot maintains `bot/inbox/` with Anton's reply history.
- Bot maintains `bot/PUBLISHABLE.md` (canonical candidate-publishable list).
- Bot maintains `bot/longterm/<id>.md` (chip-away trackers).

## §11. Bootstrap

Read by the bot at first run under the new rules. After bootstrap, this section is skipped (it sits at the bottom).

### 11.1. `bot/PUBLISHABLE.md`

If missing, create with the following row IDs, all marked `current_verdict: NOT-YET-PUBLISHABLE — needs first publishability review`:

| id | result | where_written_up |
|----|--------|------------------|
| MR-T1-1 | Resultant-prime coincidence ({Res(f,g)} = {2,3,5,7,11,13}) | `n2+1 ai thoughts/notes/proofs/P5-joint-highway.tex` Lemma 6.1 |
| MR-T1-2 | Quantitative degeneracy of Hecke characters on Landau slice | `n2+1 ai thoughts/notes/proofs/P3-hecke-classfield.tex` Theorem 5.2 |
| MR-T1-3 | Refutation of B7 spectral conjecture | `n2+1 ai thoughts/notes/proofs/P4-transfer-operator.tex` Theorem 2.4 / Proposition 4.3 |
| MR-T1-4 | Mayer / GKW identification of Shakov transfer operator | `n2+1 ai thoughts/notes/proofs/P4-transfer-operator.tex` Theorem 4.1 |
| MR-T1-5 | Disjunctive equivalence (joint highway gives no logical advantage) | `n2+1 ai thoughts/notes/proofs/P5-joint-highway.tex` Theorem 9.1 |
| MR-T1-6 | New conjecture: κ=1/2 as limiting Hensley dimension | `n2+1 ai thoughts/notes/proofs/P4-transfer-operator.tex` Conjecture 8.4 |
| MR-T1-7 | Bilinear conjecture pinpointed (two equivalent forms) | `n2+1 ai thoughts/notes/proofs/P1-bilinear-attack.tex` Conj 7.1 + P3 Conj 6.4 |
| P11-CONDITIONAL | Conditional reduction: Bianchi cubic moment over Q(i) ⇒ Landau IV | `n2+1 ai thoughts/notes/proofs/P11-master.md` (with P13 caveat) |
| P12-A | Pointwise χ₄ identity on SL₂(ℕ₀) | `n2+1 ai thoughts/notes/proofs/P12-pointwise-spin-identity.md` Theorem A |
| P12-B | Bilinear-to-twisted-divisor collapse | `n2+1 ai thoughts/notes/proofs/P12-pointwise-spin-identity.md` Theorem B |
| P12-C | Unconditional T(N) = O(N) bound | `n2+1 ai thoughts/notes/proofs/P12-pointwise-spin-identity.md` Theorem C |

Bot fills `target_venue`, `novelty_vs_literature`, `notes` organically as Phase 3.5 fires across subsequent sessions.

### 11.2. `bot/longterm/cubic-moment.md`

If missing, create with the following structure (transcribed once from P13 §3 so the bot doesn't need to re-read P13):

**Goal.** Adapt Petrow–Young 2020 (and Conrey–Iwaniec 2000) to the Bianchi setting over Q(i), to produce the conductor-aspect cubic moment for Hecke–Maass forms — the residual unconditional gap in P11. P13 §3.6 estimates 18–24 person-months; ~80–120 pages of new mathematics; chunked into ~60 30-min sessions.

**Phase decomposition.**

- **Phase I — Foundations** (already in place, no chunks needed).
- **Phase II — Bianchi Waldspurger formula** (~3–6 months estimated):
  - II.1: Theta kernel for (~SL₂, PGL₂)/Q(i) — write down following Yuan–Zhang–Zhang Ch. 3 §3.1, no normalization yet.
  - II.2: Fourier expansion of Θ_χ at level q squarefree coprime to (1+i); Friedberg–Hoffstein 1995 over Q as precursor.
  - II.3: Explicit Bianchi Waldspurger: |L(½,χ)|² = c_χ |a_χ(1)|² / ‖Θ_χ‖² — derive c_χ.
  - II.4: Local computation at the ramified prime (1+i); Pitale–Saha–Schmidt for paramodular as precursor.
- **Phase III ★ — GL₂/Q(i) spectral fourth moment** (~8–10 months, the load-bearing step):
  - III.1: Amplified second moment Σ ω_{u_j} |A(u_j)|² |L(½,u_j)|² h(t_j) at level q.
  - III.2: Off-diagonal of fourth moment via Bruggeman–Motohashi sum formula; KMV 2002 over Q as precursor.
  - III.3: Bianchi-Kloosterman + Bessel-transform integral bound. BM 2003 §11 (abelian case) as template.
  - III.4: Eisenstein contribution to fourth moment; Bruggeman–Miatello 2009.
  - III.5: Combine: (★) holds at T^{3+ε} |q|^{1+ε}.
- **Phase IV — Cubic moment via theta unfolding + (★)** (~3–4 months):
  - IV.1: Unfold Σ_χ |L(½,χ)|³ via Plancherel on self-dual character family of conductor q.
  - IV.2: Match resulting divisor-with-squareclass-mod-q sum to theta-lifted GL₂ fourth moment via Phase II.
  - IV.3: Apply (★) bound from Phase III.
  - IV.4: Bookkeep cube-free / squarefree restriction, orbit count over Z[i]^×.
  - IV.5: Conclude: Σ_χ |L(½,χ)|³ ≪ |q|^{1+ε}.
- **Phase V — Extensions:**
  - V.1: Extend to cube-free q (e_p ∈ {1,2}) — local at squared primes.
  - V.2: Extend to all q via Petrow–Young 2023 coset trick — orbit analysis over (Z[i]/q)^× / Z[i]^×.
  - V.3: Extend from L(½,χ) to L(½, u ⊗ χ) — amplification by u.
  - V.4: Uniformity in spectral parameter of u — bookkeeping.

**30-min chunks within each phase step.** A "chunk" is one self-contained 30-min increment. Each phase step decomposes into 5–15 chunks. The bot creates the next chunk title in the file's `Next chunk` field at the end of each session. Chunk format: `{phase}.{step}.{letter}: {one-sentence task}`. Examples (the bot extends this list as it works):

- II.1.a: Write down theta kernel as a function on (~SL₂ × PGL₂)(A_F) for F = Q(i), following YZZ Ch. 3 §3.1 verbatim. State definition only, no convergence check.
- II.1.b: Verify the kernel is automorphic on the right factor (PGL₂(F)\PGL₂(A_F)) — quote YZZ proof, no original work.
- III.1.a: State the amplified second moment with explicit amplifier ψ = sum over Hecke eigenvalues at small primes. No estimates.
- III.1.b: Open the amplifier square: cross-terms over (p, q) prime pairs.

**Next chunk:** II.1.a (set explicitly so the bot picks it up cleanly on first chip-away session).

**Session log.** Append-only, one line per session: `YYYY-MM-DD session-id: chunk-attempted | outcome | next-chunk`.

### 11.3. `bot/longterm/novel-spin-search.md`

If missing, create with:

**Goal.** Find conductor-level identities beyond χ₄ on SL₂(ℕ₀). P12 Theorem A gave the conductor-4 identity χ₄(a-b)·χ₄(c+d) = χ₄(n+1); P12 Theorem D shows the natural extension to higher conductors fails (the parity defect 2bd is only mod-4-killable). New ideas needed.

**Initial chunks:**
- NS.1: Enumerate small SL₂(N₀) matrices A with χ(A) ≤ 100, tabulate (a,b,c,d) mod 8 distribution, look for non-trivial mod-8 patterns the conductor-4 identity misses.
- NS.2: Enumerate Hecke characters of conductor (1+i)^k for k = 2,3,4 over Z[i]; for each, compute χ(ξ)χ(η) restricted to {ξη = n+i} slice and look for cancellation.
- NS.3: Try parity tricks analogous to P12 Theorem A's determinant trick but for *quadratic* forms in (a,b,c,d), e.g., (a²-b²)(c²+d²) or (a+b)(c+d)(a-b)(c-d).
- NS.4: Investigate the second-row identity. P12 deals with the first-row Diophantus factorization; the second-row analogue might give an independent identity.

**Next chunk:** NS.1.

**Session log.** Append-only.

## Last updated
- 2026-05-03 by Claude (initial setup).
- 2026-05-05 by Claude (added required header lists — but the routine prompt was never updated to honor this; lists never shipped — this overhaul fixes the bug).
- 2026-05-05 04:00 UTC by Claude (switched email path from SMTP to Gmail HTTPS API; documented 7-day refresh-token expiry).
- 2026-05-07 by Claude (added mandatory AI footer pointing to /SIGNIFICANT_FINDINGS.md).
- 2026-05-10 by Claude (overhaul: bias profile §1, Phase 1 rubric §2, concrete-progress check §3, new-P# rule §4, publishability skeptic §5, email body §7 — the bug fix that makes lists actually ship —, bootstrap spec §11. Old STRATEGY.md content moved to bot/STRATEGY-archive.md.).
