# workbench

Interviews you one question at a time, then executes the work through your skills
in an order enforced by code rather than by instruction.

Built on the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk).

## What makes it different from a prompt

A prompt can tell Claude to run `evidence-gates` before analysis. It cannot make
it happen. This runs each stage as a separate `query()` call carrying only that
stage's `skills` list. Per the SDK: when you pass a list, "the model doesn't see
unlisted skills and the Skill tool rejects them."

So during the gates stage, the writing skills are not reachable. During the
draft stage, the research skills are not reachable. Context carries across
stages through `resume`; the allowlist does not. That is the enforcement.

## Install

```bash
cd workbench
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

Requires the `claude` CLI on your PATH (the SDK drives it) and an authenticated
Anthropic credential. `ant auth status` will tell you whether you already have one.

## Your skills have to be on disk

The SDK discovers skills from the filesystem, not from your claude.ai account.
It looks in:

- `~/.claude/skills/<name>/SKILL.md`
- `<project>/.claude/skills/<name>/SKILL.md`, and every parent up to the repo root

Check what it can actually see before trusting the enforcement:

```bash
workbench doctor
```

It reports, per pipeline, which required skills were discovered and which were
not. A stage whose skills are all missing still runs, but with no skill at all,
which is the failure mode worth catching early.

## Use

```bash
workbench pipelines                      # the stage order for each pipeline
workbench run "draft a memo on the FM tender variance"
workbench run "size the Doha grade A office market" --pipeline market
workbench run "..." --plan-only          # interview and show the plan, run nothing
workbench run "..." --yes                # skip the per-stage confirmation
```

A run writes to `runs/<timestamp>-<pipeline>/`:

- `brief.json` — everything the interview collected, plus what it inferred and what stayed open
- `NN-<stage>.md` — each stage's output
- `run.json` — which stages ran, which were skipped, and why

## Pipelines

Defined in `workbench/pipelines.yaml`. Seven of them: `writing`, `analysis`,
`market`, `research-prep`, `linkedin`, `document`, `automation`. Each has a
question bank for the interview and an ordered stage list.

Edit the YAML to change the enforced order. A stage is:

```yaml
- name: gates
  title: Intake gates
  skills: [evidence-gates]          # the only skills invokable in this stage
  allowed_tools: [Read, Grep, Glob]
  when: sources                     # optional condition against the brief
  writes: gate_findings             # optional: put the output back in the brief
  required: true                    # a failure here halts the run
  prompt: >
    ...
```

`when` takes four forms only, and is not evaluated as code: `key`, `!key`,
`key == value`, `key != value`.

## Limits worth knowing

- **Your skills now live in two places.** The repo and `~/.claude/skills/`. That
  is sync work you are taking on.
- **You lose the ability to go off-script.** The stage list is fixed once the run
  starts. In judgment-heavy work that is sometimes where the value was.
- **The interview is model-driven within a fixed frame.** It will not ask a
  question the pipeline's bank does not seed unless it judges the request needs
  one, and it may still ask something you consider obvious.
- **Classification can be wrong.** It asks you to confirm, and `--pipeline`
  overrides it.
