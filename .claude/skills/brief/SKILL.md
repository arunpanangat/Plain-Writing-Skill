---
name: brief
description: Run an intake interview, then do the work. Use when the user types /brief, or asks to be walked through setting something up, or arrives with a request too vague to act on ("help me with the tender note", "I need something on the Doha office market"). Asks one question at a time, fills what it can infer without asking, then names the skills the work needs, in the order they have to run, and executes them. Owns the routing rules between the other skills, deciding which gate runs before which analysis, which writing layer sits on which base, and which research skill owns which destination. Do not use when the request is already specific enough to act on, or when the user wants a single named skill run directly.
---

# Brief

## The problem this solves

Two failures, and they compound.

The first is starting work on a request that has not been specified. The answer comes back competent and wrong, because the objective, the audience, the sources and the deliverable were assumed rather than established. Fixing it afterwards costs more than asking would have.

The second is skill routing. There are around 25 skills here with overlapping boundaries. Which gate runs before which analysis, whether a market fact base exists before options are generated, whether the destination of a research brief is a person or a tool: these are decided every time, from memory, under time pressure, and they are decided wrongly often enough to matter. The rules exist in the individual skill descriptions but nothing holds them together.

This skill holds them together. It collects what the work needs, then names the chain and runs it.

## How the skill runs

Four steps, in order. Do not skip step 3.

1. **Classify** the work into one of the seven types below.
2. **Interview**, one question at a time, until the brief is filled.
3. **State the plan** and get it confirmed before doing anything.
4. **Run the chain**, naming the skill at each step.

## Step 1: Classify

Read the request and pick one type. Prefer the narrowest that covers the whole request. Say which one you picked and why, in one sentence.

| Type | It is this when |
|---|---|
| **Writing** | Prose with no cross-source quantitative claim behind it. Emails, memos, notes, summaries, paragraphs. |
| **Analysis** | Any argument that compares or combines figures from more than one source, or rests on cited external facts. Cost work, ratio work, benchmarking. |
| **Market** | Sizing, structure, competitive landscape, white space, entry screening, and the strategic options that follow. |
| **Research prep** | Preparing research before it runs. A brief, a deep research prompt, or an academic topic to validate. |
| **LinkedIn** | Public writing on LinkedIn. Posts, comments, screening briefing items for post potential. |
| **Document** | A formatted deliverable has to come out. Word, PowerPoint, Excel, PDF. Includes the controlled QFZ and HBS document sets. |
| **Automation** | A flow, script, scraper or pipeline that reads a data source and processes what it finds. |

If the request spans several types, run the dominant one and say which other chains it touches. If it genuinely spans several strategy stages, that is what `strategy-decision-support` is for: hand off rather than assembling the chain here.

## Step 2: Interview

### The rules

1. **One question per turn.** Never batch. A batch gets a batch answer, which is a worse answer.

2. **Do not ask what the request already answers.** Fill the field, and say you filled it: "Taking the audience as the Steering Committee, from your wording." A wrong inference stated out loud gets corrected in one line. An unstated one does not.

3. **Do not ask what you can infer with confidence** from the request, the files in play, or the workstream. Same rule: state the inference rather than asking.

4. **Do not ask a question whose answer would not change the output.** This is the main source of interview bloat. Before asking, say what you would do differently with each answer. If the answer is nothing, drop the question.

5. **Ask why it matters** when the question is not obviously load-bearing. One clause is enough.

6. **Two attempts, then move on.** If a required field is still empty, record it as an open gap and carry on. Do not stall the whole job on one field.

7. **Offer examples when the question is open.** Two or three, drawn from the request, not generic ones.

8. **Stop when the brief is filled.** Do not keep asking because there are questions left in the bank.

### The question banks

Seed questions only. Add one when the request clearly needs it. Drop any the request has answered.

**Writing**
- What does this have to achieve, and what should the reader do after reading it?
- Who reads it, and what do they already know?
- What form, and roughly how long?
- Your style, or the plain base register only?
- Which files should it be built on, if any?
- Anything that must appear, or must not?

**Analysis**
- What decision does this serve, and who makes it?
- State the question it has to answer, in one sentence.
- Which files or exports hold the figures?
- Are there terms whose definition differs between sources: cost, area, headcount, period?
- What comes out the other end?
- When is it needed, and what depth does that allow?

**Market**
- Which market: product or service, geography, segment, time horizon?
- What call does this inform: entry, investment, pricing, portfolio?
- Do you need options and a recommendation, or just the fact base?
- Any sources you already have?
- Is this GCC real estate specifically?
- What form does the output take, and for whom?

**Research prep**
- Who runs the research: an AI deep research tool in one pass, or a person or team over time?
- Is this an academic thesis, dissertation or paper whose novelty is not yet settled?
- What is the research question, as precisely as you can state it now?
- Time, budget, access or method constraints?
- What has to exist at the end?

**LinkedIn**
- A post of your own, a comment on someone else's, or a screen of briefing items?
- What is the point you want to land? If a response, paste the post.
- What is your position, and where does it depart from the consensus?
- Any specific fact, figure or first-hand experience that anchors it?

**Document**
- What file has to come out: docx, pptx, xlsx, pdf?
- Which workstream: QFZ service charge, APM operating model, QFZ-2025-005 ACM, HBS coursework, DBA articles, or none of these?
- What goes in it, and what source material exists?
- Does it need official QFZA presentation treatment?
- New production, or a review of something existing?

**Automation**
- What should it do, end to end?
- What does it read from: folder, library, drive, inbox, database, website?
- What access do you have to that source, and through which account?
- Where does the output go?
- One-off, or on a schedule?

## Step 3: State the plan

Before doing any work, write out:

- **The brief.** Every field, filled.
- **What you inferred without asking**, and from where.
- **What is still open**, and why it did not stop the job.
- **The chain**, as a numbered list, each step naming its skill.

Then ask for confirmation. Wait for it.

This step exists so a wrong inference gets caught before it is built on, not after. It costs one exchange.

## Step 4: Run the chain

Work the steps in order. At each one, say which skill you are invoking and invoke it. Do not merge two steps into one pass because it seems faster. The order is the point.

A gate that fails stops the chain. Say so and stop, rather than working around it.

## The routing table

This is the part memory gets wrong. It is authoritative here.

### Gates, and what they gate

| Gate | Runs before | Rule |
|---|---|---|
| `source-discipline` | Anything built on supplied documents | Always first. Read the source directly, even for a single-figure lookup. Retrieval is not review. |
| `evidence-gates` | Any cross-source quantitative analysis | Runs after `source-discipline`, before analysis begins. Objective lock, source triage, circularity check, definition lock, claim verification, thesis hierarchy. Run it even when the data looks clean. |
| `complete-document-review` | Any verdict on a document itself | Use when the document is the object of evaluation, not a source to read. Coverage matrix and completeness statement are its output, not `source-discipline`'s. |
| `automation-feasibility-gate` | Any automation build | Before a tool is opened, not after. Establishes whether the task is possible at all. |
| `research-topic-validation` | An unvalidated academic topic | Before any brief is written for it. If the topic does not survive, nothing downstream matters. |

### Writing layers

`plain-writing` is the base and is always in force for prose. The others layer on top; they do not replace it.

- **Emails, reports, memos, summaries in the user's own voice**: add `arun-writing-style`. Trigger on "my style", "Arun's style", or an explicit personal-style request.
- **Anything public on LinkedIn**: `linkedin-writing` governs instead of `arun-writing-style`. Not both.
- **Internal comms in a company format** (status reports, leadership updates, FAQs, incident reports): `internal-comms`.
- **A controlled workstream document**: the workstream skill governs register and settled positions. See the table below. `plain-writing` still applies underneath.

### The strategy chain

Order matters and the boundaries are one-directional.

1. `market-research` owns sizing, structure, segments, white space and where-to-play. It builds the fact base. `market-mapping` is absorbed into it: do not run both.
2. `strategic-options` **consumes** that fact base. It does not build one. If the fact base does not exist, run `market-research` first.
3. `strategy-decision-support` routes work spanning several strategy stages and calls the two above as its market and options stages. Use it for the multi-stage chain, not for a single-job request.
4. `gcc-real-estate-intelligence` leads for GCC real estate, with `market-research` underneath it.
5. `financial-analysis` for ratio, valuation, forecasting, M&A and transformation work. Downstream of `evidence-gates` whenever the figures come from more than one source.

### The research fork

Who executes the research decides the skill. Nothing else does.

| Destination | Skill |
|---|---|
| An AI deep research tool, run in one pass | `deep-research-prep` |
| A person, a team, or a multi-method programme | `research-brief-builder` |
| An academic topic whose novelty is not settled | `research-topic-validation` first, then `research-brief-builder` |

If the destination becomes clear mid-interview and it is not the one assumed, switch.

### Workstream skills

Pick one. They are mutually exclusive, and each encodes settled positions that must not be re-litigated.

| Workstream | Skill |
|---|---|
| QFZ service charge methodology and its supporting set | `qfz-service-charge-writing` |
| APM operating model, function remits, activities and KRIs | `apm-operating-model-writing` |
| QFZ-2025-005 asset cost mapping | `qfz-acm-project` |
| Dr Ali Al-Khalifa's DBA article suite | `al-khalifa-dba-articles` |
| HBS Financial Accounting content | `hbs-course-reference` to locate it, `hbs-document-production` to build the file |

### Production, last

File production runs after the content is settled, never alongside it.

`docx`, `pptx`, `xlsx`, `pdf` for the general case. `qfza-presentations` when official QFZA identity is required. `hbs-document-production` for the HBS format.

## Worked example

Request: *"I need a note on why the FM costs came out higher than the budget."*

Classified as **Analysis**: the claim compares figures from at least two sources.

Interview, one at a time, arriving at: the decision is whether to revise the tariff; the reader is the Steering Committee; the sources are the FM contract schedule and the 2025 actuals export; "cost" is defined differently in the two; the deliverable is a two-page memo.

Plan stated and confirmed. Chain run:

1. `source-discipline`: read both files directly, record what each says, note the definition conflict without resolving it.
2. `evidence-gates`: objective lock, triage both sources, definition lock on "cost", verify the claims. A failure here stops the chain.
3. `financial-analysis`: the variance work on what survived, with confidence and gaps on every figure.
4. `plain-writing` plus `arun-writing-style`: the memo. Conclusion first, then evidence, then gaps.

## Self-check before finishing

- Was every question asked one at a time?
- Was any question asked whose answer did not change the output?
- Was every inference stated rather than assumed silently?
- Was the plan confirmed before work began?
- Did each gate run before the thing it gates?
- Was each skill named at the step it ran?
- Are the open gaps stated in the output, not quietly dropped?

## When this skill does not apply

- The request is already specific enough to act on. Act on it.
- The user asked for one named skill. Run that skill.
- The user is thinking out loud, brainstorming, or asking a factual question. Answer it.
- The work spans several strategy stages end to end. Hand off to `strategy-decision-support` rather than assembling the chain here.
