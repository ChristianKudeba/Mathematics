# Business Plan — Autonomous AI Research Agents for Mathematicians

*Working draft, May 2026. Co-founders: Anton Shakov + Chrisitan Kudeba.*
*This is a strategy document, not a pitch deck. It is meant to be argued with.*

---

## 1. Executive Summary

We are building a SaaS platform on which research mathematicians configure **custom autonomous AI agents** — each one a bespoke combination of prompts, tools (Lean, computer algebra, search), and verifiers (mechanical proof-checking + human review) — to think about the problems they care about. Agents run on long horizons. Their output feeds a **public, growing, attribution-preserving knowledge graph of mathematics**. The graph is free to read for anyone in the world. The researchers, departments, and labs whose agents produce that output are the paying customers.

The business is positioned in the white space between three crowded categories:

- **Olympiad-grade prover startups** (Harmonic AI, Axiom Math, Morph Labs) — well-funded, narrowly focused on competitive proof-of-concept benchmarks.
- **Generic AI-coding platforms** (Cursor, Cognition/Devin, Lovable) — capable but not designed for research mathematics.
- **Non-profit science-agent platforms** (FutureHouse for biology, Project Numina for math) — the closest spiritual analogues, but free and donation-funded.

No commercial actor today owns the position **"verifier-pluggable autonomous research agents producing a permanent public mathematical record, with researcher attribution as a first-class feature."** That is the wedge.

The headline numbers we are underwriting:
- **Path to $10M ARR in Year 3** via a mix of academic site licenses, individual researcher subscriptions, private-lab enterprise contracts, and verified-knowledge-graph data licensing to frontier AI labs.
- **Blended gross margin: 55% Y1 → 65% Y3**, achieved through aggressive model-routing (Haiku/Flash for orchestration, Opus/o3-Deep-Research only when needed), prompt caching, and a high enterprise mix.
- **Funding plan: $1–3M non-dilutive grants (Renaissance AI for Math Fund, NSF SBIR, Schmidt Sciences, Simons) stacked with a $2–4M angel/seed round** from Conviction or Lux Capital. The grant-funded public knowledge graph is the moat the venture round pays to expand.

The single biggest risk is not technical — frontier models can already do graduate-level math when steered well — it is **trust**. Mathematicians are a market that pays dearly for instruments they trust and ignores everything else. The defensible product, the marketing strategy, and the funding sequence in this plan are all designed around that single truth.

---

## 2. The Opportunity

### 2.1 The frustration that creates the market

Mathematicians have eagerly adopted ChatGPT, Claude, and Gemini for routine assistance — Terence Tao formalized a one-page proof in Lean in 33 minutes using Copilot, and now publicly says AI is "ready for primetime in math and theoretical physics." But the same community is uniformly frustrated with the next step: **getting from "promising assistant" to "produces real, organized, citable mathematical results."** The objections are concrete and specific:

- **Hallucination.** OpenAI's own research argues hallucinations are mathematically inevitable in autoregressive LLMs. A widely-shared experiment that prompted Claude 550 times to "invent mathematics" produced zero exploitable results.
- **No persistence.** Each conversation is a sandcastle. There is no growing artifact, no graph of dead ends and live leads, no shared institutional memory.
- **No verification.** The community trusts Lean. It does not trust unchecked LLM proofs, and it is right not to.
- **No attribution.** A mathematician's career is built on citations. Output that cannot be cited cleanly to its prompter is professionally useless.

### 2.2 Why now (May 2026)

Four conditions converged in the last 18 months:

1. **Frontier models can reason mathematically** at graduate-research level when carefully steered (Gemini Deep Think IMO gold, Aristotle gold, Aletheia agentic research).
2. **Lean 4 + mathlib became the de facto verifier** — millions of lines, hundreds of contributors, the FLT formalization underway. Mechanical verification at scale is finally tractable.
3. **Prompt caching and tiered model routing collapsed agent-hour costs by ~5×** in 12 months, putting "let it think for hours" into the realm of subscription economics.
4. **The math community accepted AI as legitimate.** Tao, Buzzard, Scholze, Polymath+AI, Renaissance Philanthropy's $31.5M AI for Math Fund, DARPA expMath — the institutional permission slip is signed.

### 2.3 Total addressable market (rough)

- **Active research mathematicians worldwide:** ~80,000 (AMS + global). A few thousand are early adopters.
- **Math/CS departments at universities:** ~5,000 globally; top 500 are realistic site-license targets.
- **Quant funds, pharma R&D, defense labs, frontier AI labs hiring pure mathematicians:** dozens to low hundreds; check sizes start at six figures.
- **The Wolfram comparison anchor:** privately held but reliably estimated at $200M+ revenue. Maple, Magma, Overleaf each in the $10M–$100M range. We are not aiming for Wolfram-scale; we are aiming to be the agent-era complement to it.

A credible **bull-case Year-5 ARR is $50–100M**. A reasonable Year-3 target is $10M. A "the academic market is too frugal and DeepMind gives Aletheia away free" downside is **$2–4M ARR concentrated in private labs** — still a viable lifestyle business, not a venture-scale outcome.

---

## 3. Product

### 3.1 What it is

A web platform on which a researcher does four things:

1. **Configures an agent.** Picks a base model (or routing policy across models), writes a system prompt or starts from a template (theory-builder, problem-solver, paper-reader, conjecture-generator), attaches tools (Lean, SymPy/SageMath, web search, arXiv lookup, mathlib search via Loogle/Moogle).
2. **Points the agent at a problem or topic.** Could be a formal statement, an open question, a paper, a half-finished argument.
3. **Lets the agent run** for minutes, hours, or days. The agent's reasoning is logged transparently (Granville's objection to outsourced rigor: addressed). When the agent produces a candidate result, **Lean verifies what is mechanically verifiable** and queues the rest for **expert human review**.
4. **Receives notifications** when the agent makes meaningful progress or a verified breakthrough. Verified results are added to the **public knowledge graph** with permanent attribution to the prompter.

### 3.2 The public knowledge graph

This is the strategic centerpiece. Every verified output — theorem, lemma, counterexample, conjecture with evidence — is a node. Edges are dependencies, generalizations, refutations, references. The graph is:

- **CC-BY-SA licensed**, exportable in bulk, mirror-able. We do not own mathematics.
- **Stewarded by a non-profit foundation** modeled on the Mathlib Initiative and the Lean FRO. The for-profit operates the platform; the foundation governs the graph. This separation is the only thing that prevents an Elsevier-style backlash.
- **Anyone can read; only paying users can write directly via agents.** Free users can submit conjectures, edits, and counterexamples through community PR-style review.

### 3.3 Template agents (the marketplace seed)

Out of the box: theory-builder, problem-solver, computational-experimentalist, paper-summarizer, lemma-finder, counterexample-hunter, formalization-translator. Power users publish their own templates; we take a 30% revenue share when others use them. This is a moat-builder, not a margin-driver, and we should not over-invest in it pre-PMF.

### 3.4 What we will not build (initially)

- **Our own foundation model.** Wrapper risk is real, but at <$10M ARR the cap-ex of training is suicidal. We route across Anthropic/OpenAI/Google and watch closely for the moment a small fine-tuned domain model becomes obviously needed (Cursor's Composer was that moment for them in late 2025).
- **Domains beyond math, before traction.** Physics and chemistry are real expansions. They are not Year-1 priorities. The math community is opinionated, well-defined, and small enough to dominate first. Generalization comes after.

---

## 4. Competitive Landscape

### 4.1 The crowded center: olympiad-grade prover startups

| Company | Funding | Position | Threat to us |
|---|---|---|---|
| **Harmonic AI / Aristotle** | $295M total ($1.45B val), Sequoia/Kleiner/Ribbit/NVentures | Lean-backed reasoning engine, free API, IMO gold, $1M student grants | Highest-profile competitor; brand and capital advantage |
| **Axiom Math (Carina Hong, Ken Ono)** | $200M Series A ($1.6B val) | AxiomProver + Axplorer; pivoting to chip design and finance | Less direct overlap once they go enterprise-vertical |
| **Morph Labs** | Smaller, undisclosed | Personal AI proof engineer, Moogle, Lean PNT formalization | Strong on prover infra; weak on research-mathematician UX |
| **Open-source provers** (DeepSeek-Prover-V2, Goedel-Prover-V2, Kimina-Prover) | n/a | 88–90% miniF2F; free | Commodifies the prover layer |

These competitors are racing on **prover capability benchmarks**. We are not racing on benchmarks. We are competing on **what a working mathematician does on a Tuesday afternoon**, which is a different and less crowded contest.

### 4.2 The closest spiritual analogue: FutureHouse (biology)

[FutureHouse](https://www.futurehouse.org/) is a non-profit running a **public platform of named scientific agents** (Crow, Falcon, Phoenix, Finch, Owl) for literature search, synthesis, and experiment design in biology and chemistry. They have already discovered a candidate dAMD therapeutic. The architecture is essentially what we are proposing — *a platform of specialized agents producing a public output corpus* — except (a) they're biology, (b) they're non-profit, (c) they're philanthropically funded.

**Implication:** The pattern works. The for-profit, math-first version of it is uncontested.

### 4.3 The existential threat: Google DeepMind's AI for Math Initiative

DeepMind unveiled **Aletheia** (April 2026), an autonomous *professional research* agent, and is giving it free to Imperial, IAS, IHES, Simons Institute, TIFR through the AI for Math Initiative. The most prestigious institutions in our TAM may already get DeepMind tooling at zero cost.

**Mitigations:**
- **Verifiable trust + attribution + persistence are not what Aletheia sells.** DeepMind sells reasoning capability; we sell the workflow around it.
- **The middle 4,500 universities and the entire private-lab segment are not on DeepMind's free list.** That is most of the revenue.
- **DeepMind cannot ship a community-governed knowledge graph.** Antitrust, perception, and corporate inertia all forbid it.
- **We can route to Gemini Deep Think.** Their capability advantage becomes our raw material.

### 4.4 The encroachment risk: Cursor

In April 2026 a generic Cursor coding harness solved a research-grade spectral graph theory problem autonomously over four days. Mathematicians could, in principle, wire up Lean + GPT-5 + a paper reader inside Cursor and DIY us.

**Mitigation:** They will not. Mathematicians are not software engineers. The setup, observability, prompt-engineering, verification queueing, attribution, and public-graph publishing we provide are exactly the friction Cursor leaves on the user. We are the opinionated path.

### 4.5 The frugality competition: free knowledge graphs and open provers

mathlib, OEIS, ProofWiki, Stacks Project, nLab — all free, all loved. We do not compete with them. We **integrate** with them and make them more discoverable from inside agents. The graph we build is meta-level: it indexes results across these sources, plus net-new agent output, with a uniform verification status.

### 4.6 Honest verdict on positioning

The crowded part of the space is "Lean-backed olympiad-level prover." The open part is **"autonomous research-mathematician workflow producing a permanent attributed verified public corpus."** No funded for-profit owns this. The non-profit FutureHouse owns the analogous position in biology. We can be its math-first commercial counterpart.

---

## 5. Differentiation & Positioning

### 5.1 The differentiator stack, ranked by audience

**For working researchers** (the buyer of the Researcher tier):
1. **Lean verification on every public claim** — answers the universal hallucination objection
2. **Attribution to the prompter, permanent** — career-aligned
3. **Cheap exploration of crazy ideas** — Tao's own framing
4. **Custom agents owned by the researcher** — workflow autonomy
5. **Optional platform credit** — soft adoption

**For department procurement:**
1. **Open-access narrative** — graph is CC-BY-SA, foundation-governed
2. **FERPA / data residency / audit logs**
3. **Lean verification** — defensible to provost
4. **Site license priced predictably**

**For private labs:**
1. **Private knowledge-graph instances** with optional partial publication
2. **Dedicated agents, on-prem Lean, custom integrations**
3. **Six-figure check sizes are normal** here, not unusual

### 5.2 Tagline candidates to test in interviews

| Tagline | Test audience |
|---|---|
| "Your research, automated. Your name on the proof." | Individual mathematicians |
| "Lean-verified. Human-attributed. Always public." | Skeptics |
| "Cheap exploration for crazy ideas." | Enthusiasts |
| "Proof-grade AI agents for serious mathematics." | Industrial labs |

A good interview signal is to drop a tagline mid-conversation and watch the face. We will commit to one only after 30+ interviews.

### 5.3 What we will *not* claim

- We will not claim our agents produce breakthroughs on demand. Sakana's AI Scientist passed peer review once in 2026, with 42% experiment failure rates en route. We promise infrastructure, not miracles.
- We will not auto-publish unverified results. Lean-verified results are publishable; informal results are private to the prompter unless they explicitly elect to publish with a clear "informal" label.
- We will not call ourselves "ChatGPT for math." That framing has lost the elite-mathematician cohort already; Tim Gowers has explicitly rejected it.

---

## 6. Go-to-Market Strategy

### 6.1 Phase 0 (now → month 3): Founder discovery

**One hundred interviews before scaling.** This is the YC benchmark and it is right. Targets, in priority order:

1. **Lean-curious early-career researchers** (postdocs, 2nd–4th-year grad students at top-30 departments). Found on Lean Zulip, mathlib contributor list, recent arXiv preprints citing Lean.
2. **Mathlib contributors** — already opt-in to tooling.
3. **Mid-career researchers in formalization-active subfields**: number theory (FLT crowd), homotopy/condensed (Scholze ecosystem), combinatorics (PFR/Gowers).
4. **Senior advocates last** (Tao, Buzzard, Granville, Scholze). They are not interview subjects — they are potential design partners after we have a working demo. Their time costs more than ours.
5. **Industrial labs in parallel**: Jane Street ML research, Renaissance Technologies, DeepMind/Anthropic theory teams, Hudson River Trading. They will pay enterprise prices the academy will not.

**Interview script (Mom Test discipline):**
- "Walk me through the last research problem where you got stuck. What did you do in the next 24 hours?"
- "Show me the last ChatGPT/Claude conversation you had about math."
- "Have you tried Lean? What stopped you / what made you keep going?"
- "How do you currently track half-formed conjectures and dead ends?"
- Never pitch. Never ask "would you pay for…". Always ask: "How are you solving this today, and what does it cost you?"

**Expected outputs by end of Phase 0:**
- Validated wedge (which sub-persona pays first)
- Three to five committed design partners
- Concrete agent template the first design partners want
- Public-build presence on Mathstodon and X with the founder personally posting

**Cost:** founder time + ~$3K travel.

### 6.2 Phase 1 (months 3–9): Public alpha + community seed

- **Free public access to the knowledge graph** from day one. No login required to read.
- **Free Researcher tier for any `.edu` email** — replicates Overleaf Commons and JetBrains Student Pack mechanics. Grad students bring it in from below until libraries license it.
- **Build in public on Mathstodon, X, and Lean Zulip.** Show the agents at work. Show the dead ends. Be a contributor first, a vendor second.
- **First Lean-verified result published with attribution.** Coordinate with one design partner to make this a small public moment.
- **First three department design partners signed at $20K each** for Phase-2-launch site licenses. These are not real revenue; they are anchor commitments.

### 6.3 Phase 2 (months 9–18): Paid launch

- **Researcher tier launches at $29/mo or $290/yr** (free for verified students/postdocs).
- **JMM 2027 booth** — Joint Mathematics Meetings, January 2027. ~$1,250–$2,750 for the booth, $2,500–$15,000 for sponsor-tier visibility. Total budget ~$10K. Single highest-leverage live event in the world for math sales.
- **MathFest** (MAA, August) for educator reach.
- **First case study with a Tao-tier advocate.** This requires the prior 12 months of patient relationship-building.
- **First three department site licenses converted to paid** at $25–40K/yr.
- **First industrial-lab pilot** — pharma quant or fintech HFT — at $150–250K.

### 6.4 Phase 3 (months 18–24): Enterprise & community scale

- **Overleaf Commons-style auto-enrollment program** for partner institutions.
- **Foundation launched** to govern the public graph (Mathlib Initiative model). Get Tao, Buzzard, or equivalent on the advisory board. This is the academic-backlash insurance policy.
- **First $500K+ enterprise contract** in private R&D.
- **First data-licensing conversation** with a frontier lab (Anthropic, Google DeepMind, OpenAI) — a verified, attributed, frontier-research-quality math corpus is differentiated training data.

### 6.5 Channel ranking summary

| Rank | Channel | Why |
|---|---|---|
| 1 | JMM 2027 booth + sponsored session | Whole-market presence in 4 days |
| 2 | `.edu` freemium | 5-year sales cycle (JetBrains-proven) |
| 3 | Founder presence on Mathstodon / X / Zulip | Authority + recruiting + design partners |
| 4 | Agent-generated arXiv preprints with attribution | Native to mathematician discovery flow |
| 5 | Targeted top-30 department visits | High-touch, high-conversion |
| 6 | MathFest, regional AMS meetings | Reach, lower priority than JMM |
| 7 | Quanta Magazine / Mathstodon coverage of milestone results | Earned, not bought |

### 6.6 What we will not do

- **No paid display ads** — wrong audience, wrong medium.
- **No SEO content marketing farm** — the math community has high taste and low tolerance.
- **No "AI for everyone" generic outreach** — sharpening to mathematicians is the entire point.
- **No conferences outside math** in Year 1 (no NeurIPS, no AAAI). We are not selling to the AI community.

---

## 7. Pricing & Packaging

Anchored against Mathematica academic ($1,410/yr), Overleaf Pro ($399/yr), GitHub Copilot Pro ($10–39/mo), Devin ($20/mo + $2.25/ACU). Mathematicians associate cheap with unserious; we should charge professional-tool prices.

| Tier | Pricing | Included compute | Overage | Target ARR/account |
|---|---|---|---|---|
| **Free / Public Graph** | $0 | Read-only graph, 1 capped agent (~$5/mo inference) | n/a | $0 — community moat |
| **Student / Postdoc (verified .edu)** | $0 | 5 ACU/mo (~75 min agent-time) | $3/ACU | $0 — funnel |
| **Researcher (Pro)** | $29/mo or $290/yr | 30 ACU/mo, priority Lean queue, arXiv integration, attribution badges, 5 custom agents | $2.50/ACU | $300–800/yr |
| **Department Site License** | $25K/yr base + $30/seat/mo | Pooled 3,000 ACU/mo, SSO, audit logs, FERPA, branded graph subspace | $2/ACU bulk | $40–80K/yr |
| **Enterprise (private R&D)** | $150K/yr base + $200/seat/mo + private deployment | Pooled 30,000 ACU/mo, dedicated agents, on-prem Lean, custom integrations | $1.50/ACU | $300K–1.2M/yr |
| **Data Licensing (frontier labs)** | Custom annual contract | Verified attributed graph as training corpus | n/a | $1–10M/yr; 2–4 customers by Y3 |
| **Nonprofit Research Foundation** | $5K/yr near-cost | For poorer institutions and global south | n/a | PR upside; analogue of GitHub Nonprofit |

**ACU = "Agent Compute Unit" ≈ 15 minutes of agent-hour ≈ $6.25 fully-loaded internal cost** at our routed average of $25/agent-hour. Selling at $2–3/ACU bulk and $3/ACU retail subsidizes individual tiers (acceptable acquisition cost) and clears 60%+ GM on enterprise pooled compute.

**Two packaging principles to defend:**

1. **The free tier must be generously useful in perpetuity.** The graph is the moat; the free tier feeds the graph and seeds the funnel.
2. **Department and enterprise prices are quoted, not listed.** Wolfram and Overleaf both deliberately hide site-license pricing. Negotiation room is real money.

---

## 8. Business Model & Unit Economics

### 8.1 Cost structure (May 2026 reality)

Frontier API pricing (per 1M input/output tokens):

| Model | Input | Output | Best use |
|---|---|---|---|
| Claude Opus 4.7 | $5 | $25 | Hard sub-problems, final synthesis |
| Claude Sonnet 4.6 | $3 | $15 | Typical agent step |
| Claude Haiku 4.5 | $1 | $5 | Orchestration, retrieval |
| OpenAI o3 | $2 | $8 | Reasoning-heavy steps |
| OpenAI o3 Deep Research | $10 | $40 | Multi-hour exploration tasks |
| Gemini 2.5 Pro | $1.25 | $10 | Long-context paper reading |

**Realistic agent-hour cost at frontier quality: $30–$150 unmanaged.** With prompt caching (90% off cached input), batching (50% off), aggressive routing to Haiku/Flash for orchestration, and Opus/o3 only for hard sub-problems, the **disciplined floor is $15–$40/hr**. We will internally call this $25/hr and hold ourselves to it.

### 8.2 The honest gross-margin reality

ICONIQ's State of AI (January 2026) puts scaling-stage AI B2B GM at **52% (up from 41% in 2024) with inference at 23% of revenue**. Cursor had **zero gross margin in early 2025** with every dollar passing through to model APIs; positive GM came only after their proprietary Composer model (Nov 2025). Lovable ($200M ARR) is unprofitable. Cognition is disciplined ($20M total burn) but pre-profit at $150M ARR.

We will plan for 50–60% blended GM, not the 80%+ classic SaaS. Anyone who tells a board they will hit 80% GM in agent SaaS without their own model is either lying or about to be fired.

### 8.3 Profitability levers, ranked

1. **Enterprise contracts with private labs.** The only segment where per-seat pricing of $5K–$50K/yr is acceptable, compute overage is invisible relative to research budgets, and 60%+ GM is easily clearable. **This is the path to profitability.** Cursor's experience proves it.
2. **Tiered subscriptions with metered agent compute** (Devin's $20/mo base + $2.25/ACU model). Flat-rate at frontier-model pricing is suicidal. Subscription pays for the platform, persistence, UI; metered compute pays for the agents.
3. **Grant-based revenue funding the public knowledge graph as scientific infrastructure.** Renaissance AI for Math Fund disbursed $31.5M across 29 projects ($100K–$1M each); DARPA expMath ($5M to UCLA's ALPHA team); NSF SBIR Phase I ($275K) → Phase II ($1M); Schmidt Sciences Trustworthy AI ($1M–$5M); Simons Targeted Grants ($250K/yr × 3yr). **Realistic non-dilutive ceiling Y1–Y2: $2–5M.** This money funds the graph as community infrastructure — defusing the academic-backlash risk and creating the moat the Series A pays to expand.
4. **Data / training-set licensing of the verified knowledge graph** to frontier labs. Lean/Mathlib datasets are already being commercialized; a *verified, attributed, frontier-research-quality* graph is differentiated. Plausibly **$1–10M/yr per major lab, 2–4 customers by Year 3.**
5. **Premium verification SLAs** — priority Lean checking and expert human review at $50–$500 per result or as enterprise tier feature. Modest, high-margin.
6. **Custom-agent template marketplace** with 70/30 split. Stickiness, not margin.

### 8.4 Unit-economics targets

| Metric | Y1 | Y3 |
|---|---|---|
| Blended GM | 55% | 65% |
| Compute as % of revenue | ≤30% | ≤22% |
| ARR | $1.5M | $10M |
| Headcount | 5–7 | 12–15 |
| Net burn | $2–3M | break-even |

**Path to $10M ARR in Year 3:**
- 2,000 paid Researcher tier @ $290 ≈ $580K
- 50 departments @ $50K ≈ $2.5M
- 10 enterprises @ $500K ≈ $5M
- 1 frontier-lab data-licensing contract @ $2M ≈ $2M
- **Total ≈ $10M**

At 60% GM that is $6M gross profit; with $4M opex on a 12–15 person team, we are at break-even — the realistic profitability inflection.

### 8.5 The decision that determines the company's character

The single highest-leverage strategic call: **enterprise-first on revenue, academic tier at-cost as the credibility and recruiting funnel.** This is the Overleaf, JetBrains, Wolfram playbook adapted for the agent-compute era. The opposite — leading with consumer pricing for individual mathematicians — is the path to a charming product and a closed-down company.

---

## 9. Funding Strategy

### 9.1 Recommended sequence

**Stage 1 (months 0–6): Bootstrap with non-dilutive capital while running interviews.**
- Submit to Renaissance Philanthropy AI for Math Fund (next deadline April 2026). 280 applicants, ~10% selection. $100K–$1M for 12–24 months.
- File NSF SBIR Phase I AI topic ($275K, 6–12 months).
- Apply to Schmidt Sciences Trustworthy AI track ($1M–$5M, deadline May 17, 2026).
- Approach Simons Foundation for Targeted Grant to Institutes ($250K/yr × 3).
- Targeted DARPA expMath subcontract conversation via existing university teams.
- **Realistic stack: $1–3M non-dilutive in 12 months.** Fund 2–3 engineers + the founder full-time.

**Stage 2 (months 6–12): $2–4M angel/seed.**
- **Conviction (Sarah Guo)**: $1–25M checks, first-investor preference, academic-AI portfolio (Mistral, Harvey, OpenEvidence). Natural fit.
- **Lux Capital**: Fund IX closed $1.5B in January 2026 on an explicit "AI tools for scientists" thesis; already invested in Cognition. Math is in the strike zone.
- **Compound, Bloomberg Beta, Conviction-adjacent angels.**
- **Trigger:** signed design partners + working alpha + early Researcher-tier conversion data.

**Stage 3 (months 18–24): $15–30M Series A.**
- Triggered by $1–3M committed enterprise pipeline + active institutional pilots.
- Sequoia / Kleiner / Ribbit (the Harmonic stack) are warm to the math thesis.

### 9.2 The strategic argument for grants-first

The grant-funded public knowledge graph is the **academic-legitimacy artifact that allows everything else**. A Series A pitch where you can say "Renaissance, NSF, Schmidt, and Simons all back the graph as community infrastructure, and we operate the platform on top" is qualitatively different from "we are a startup hoping mathematicians like us." It defuses the corporate-enclosure objection structurally, not rhetorically.

### 9.3 Comparable funding signals (for VC conversations)

- Harmonic AI: $295M total ($1.45B valuation), Sequoia/Kleiner/Ribbit/NVentures.
- Axiom Math: $200M Series A ($1.6B valuation), March 2026.
- Lila Sciences (biology analogue): $550M total funding.
- Cognition: $400M at $10.2B (Sept 2025); rumored at $25B in 2026.
- Cursor: in talks for $2B at $50B (April 2026).

VCs have already underwritten the math-AI thesis at scale. Our job is to convince them that the missing position is the workflow + graph + foundation, not another prover.

---

## 10. Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **Hallucinated "breakthrough" goes public** | Catastrophic | Lean verification gate on every public claim; informal results clearly marked and private by default |
| **Academic-community backlash on corporate ownership of math** | High | CC-BY-SA graph; non-profit foundation governs; researcher attribution non-negotiable; bulk export always available |
| **DeepMind Aletheia free at top-tier institutions** | High | Compete on workflow/persistence/attribution, not raw capability; route to Gemini Deep Think when useful |
| **Frontier-API margin compression** | High | Aggressive model routing; prompt caching; reservation pricing; small fine-tuned domain model when ARR justifies (~$10M+) |
| **Cursor / generic agent encroachment** | Medium | Opinionated UX, Lean integration, attribution, public graph — all friction Cursor leaves on user |
| **Mathematicians don't pay individually (the frugality problem)** | Medium | Underwrite revenue on enterprise + departments, not individual subs; consumer tier is funnel, not engine |
| **Co-founder conflict** | Low (so far) but high impact | Document equity, decision rights, vesting cliff, conflict process now, not later |
| **Liability for false breakthrough claims used in industry** | Medium | Explicit ToS disclaim of fitness for specific decisions; Lean-verified vs informal labeling enforced in UI |
| **Open-source provers commoditize prover layer** | Low (we already plan for this) | Moat is graph + workflow + community, not the prover |

---

## 11. 24-Month Execution Roadmap

**Month 0–3: Discovery**
- 100 founder interviews (Mom Test discipline)
- Three signed design partners
- Submit Renaissance, NSF SBIR, Schmidt grant applications
- Public Mathstodon presence; first agent demos shared

**Month 3–6: Alpha**
- Working alpha: agent configurator + Lean verification + minimum graph
- First public Lean-verified result with attribution, coordinated with design partner
- `.edu` free Researcher tier opens
- Foundation entity formed (Delaware non-profit + non-profit board candidates)

**Month 6–9: Public beta + community seed**
- Open community PR flow on graph
- Five formalization-active subfields onboarded (number theory, combinatorics, condensed, homotopy, algebraic geometry)
- $1–3M non-dilutive grants closed
- $2–4M angel/seed closed (Conviction or Lux + named angels)

**Month 9–12: Paid launch**
- Researcher tier $29/mo paid launch
- First department site license converted to paid
- JMM 2027 booth (January)
- First industrial-lab pilot conversation

**Month 12–18: Revenue scale**
- Three departments paid
- First industrial-lab contract signed ($150–250K)
- Foundation governance fully operational; Tao/Buzzard/Granville-tier advisor on board
- Template marketplace soft-launch

**Month 18–24: Enterprise scale**
- 10 departments paid
- Two to three enterprise contracts
- First data-licensing conversation with a frontier lab
- Series A close ($15–30M) on $3M+ ARR signal

**Hiring sequence:**
- Month 0: founder + co-founder
- Month 3: 1 senior engineer (Lean + agent infra)
- Month 6: 1 ML/agent engineer; 1 frontend
- Month 12: 1 enterprise sales lead; 1 community/DevRel
- Month 18: 1 mathematician-in-residence; 2 more engineers
- Month 24: 12–15 people total

---

## 12. Open Strategic Questions

These are unresolved and need to be answered, in order, in the next 90 days:

1. **Who is the co-founder, and what is their wedge?** Equity split, decision rights, vesting cliff, conflict process — document before product.
2. **Product name?** Currently unnamed. Should evoke "map of mathematics" or "verified record" without sounding sterile. Propose 5–10 candidates and test them in interviews.
3. **First subfield to dominate.** Number theory (FLT crowd) is the strongest candidate given Lean coverage. Combinatorics (PFR) is second. Pick one for Phase 1 and dogfood it ourselves.
4. **Lean integration depth.** Do agents *write* Lean, *check* Lean, or both? "Both" is the right answer eventually; "check" is the cheaper Y1 answer.
5. **Hosting / compute strategy.** Pure API reseller initially; private deployments for enterprise eventually. When do we add reserved capacity contracts with Anthropic / OpenAI / Google?
6. **Privacy of agent runs.** Are paying users' agent runs visible to others before publication? Default: private until the user elects to publish a verified result. But explicit policy needed.
7. **Liability framing.** Industrial-lab contracts will demand specific indemnities. We need a defensible ToS before the first enterprise pilot.

---

## 13. The Single Most Important Sentence

If we ship a single output that the math community decides is **slop**, we are dead. Lean verification on every public claim, conservative messaging about what the agents do, and Buzzard-tier advocates as design partners are how we avoid it. Everything else in this document is downstream of getting that one thing right.

---

*Last revised 2026-05-02. Comments welcome — argue with this; that is what it's for.*
