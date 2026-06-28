---
name: vibecode-check
description: >-
  Use when the user wants to sharpen or rewrite a prompt for a coding agent such as Claude
  Code, Cursor, Copilot, or v0. Finds load-bearing ambiguity, vocabulary drift, and accidental
  implementation mandates; resolves them with one-tap questions or stated assumptions; returns
  a portable prompt, sync-check list, and short teaching tip.
version: 2.0.0
author: Brian Gibby
license: MIT
metadata:
  hermes:
    tags: [prompt-engineering, coding-agent, disambiguation, vibe-coding, skill]
    related_skills: []
---

# Vibecode Check

A pre-flight check for prompts headed to a coding agent. The user writes a prompt; this skill finds the places where the user's mental picture and the words on the page have drifted apart, closes that gap, and hands back a sharper prompt the user can paste straight into their tool of choice.

The user of this skill is often a **novice programmer**, so the goal is not just to fix this one prompt but to help them *learn to write better ones*. Every rewrite should teach a little.

## The core idea: ambiguity is where agents go off the rails

A coding agent does exactly what the prompt says — not what the user pictured. The danger isn't that the user is wrong; it's that they hold a vivid, detailed picture in their head and only wrote down a fraction of it. The agent then fills every gap with a guess, and a single wrong guess early (wrong framework, wrong file, wrong idea of "done") can send a whole session sideways.

Anthropic's own guidance for Claude Code puts it plainly: *"Claude can infer intent, but it can't read your mind"* — the more precise the instructions, the fewer corrections needed. So the job here is to find each spot where a *reasonable* agent could legitimately interpret the prompt two different ways, and remove that fork in the road.

Ambiguity isn't only *missing* information. It's also **words that mean different things to the two of you**. A term used loosely — or learned slightly wrong — can read as precise-but-wrong to the agent. A newer programmer who writes "instruction set" when they mean *system prompt* will get an agent that takes "instruction set" literally (it can even read as a CPU's instruction set) and builds the wrong thing. So the vocabulary itself is part of the sweep.

**A note on priority.** The aim is a genuine shared understanding between the user and the agent — and that matters more than keeping the exchange short. So this skill does **not** try to ask as few questions as possible. It tries to leave no load-bearing gap unspoken, while keeping the *cost* of getting there low. The two things to manage are **friction** (each question one-tap to answer) and **looping** (the process must always be able to finish) — and neither is solved by asking *less*. They're solved by asking *cheaply* and *never blocking*. The mental move, applied to every part of the prompt: **"Could a competent but literal-minded agent read this and build something the user didn't intend?"** If yes, that's a gap to close.

## Workflow

1. **Understand the real intent.** Read the prompt and infer what the user is actually trying to accomplish — the underlying goal, not just the literal words. Factor in any files referenced or pasted.
2. **Run the ambiguity sweep.** Walk the checklist below and note every gap an agent would have to guess at, including any term that looks non-standard and any implementation word that may not be meant as a mandate.
3. **Triage each gap by stakes** — *load-bearing* (a wrong guess would change what gets built, or reflects a real mismatch in understanding) versus *cosmetic* (any sensible convention works).
4. **Resolve every load-bearing gap.** Ask a one-tap clarifying question when a wrong guess is both likely and costly; otherwise state a sensible default and flag it for veto. Cosmetic gaps you simply decide. Never block — you can always proceed on stated assumptions.
5. **Deliver:** the rewritten prompt, what you changed and corrected, the always-on "are we still in sync?" list, and a tip.

## Step 2 in depth: the ambiguity sweep

These are the dimensions where coding prompts most often leave an agent guessing. The question to ask yourself is in italics. Sweep them all, keep what's relevant.

- **Goal & definition of done.** *What does success actually look like — how would the user know it worked?* Agents optimize for the stated target, so a fuzzy target produces a fuzzy result. The single most important thing to pin down.
- **Terminology & domain vocabulary.** *Is every technical term used the way the field uses it — and the way the agent will read it?* Newer programmers often map a concept to a close-but-not-standard word: "instruction set" for *system prompt*, "function" for a whole *script*, "database" for a single *CSV file*, "API" for any *integration*, "deploy" for "run it locally". The agent takes the word at face value and builds the wrong thing or stalls. When a term looks off, name the standard term and correct it (directly — see below).
- **Goal vs. mechanism (the "how" sneaking in).** *Has the user named a specific technique — "recursive," "multithreaded," "use a regex," "cache it in Redis" — when what they actually care about is an outcome?* Newer programmers often bake in an implementation word because it's the term they just learned, not because they need that exact mechanism. Taken literally it can hand the agent a worse or riskier approach: asking for a "recursive folder scan" can yield true function-call recursion that overflows the stack or never terminates without a base case, when an iterative, stack-based scan (push/pop) reaches the same outcome more safely. Separate the *what* from the *how* — capture the goal and constraints ("list every file in all subfolders, however deep; must always terminate") and either let the agent choose the implementation, or, if the user genuinely wants a specific technique, note its tradeoffs so the choice is deliberate.
- **Stack & environment.** *Which language, framework, and versions? Where does this run (browser, Node, a CLI, a phone, a serverless function)?* Code correct on Python 3.12 can break on 3.8; "a chart" means something different in React vs. plain HTML. Novices very often omit this.
- **Codebase context.** *New project or a change to existing code? Which files should the agent read or touch? Existing patterns to follow?* Without this an agent reinvents what exists or drops code in the wrong place. Name the files; point at an example to mirror.
- **Scope — in and out.** *What is explicitly NOT part of this task?* Stating what to leave alone prevents an agent from helpfully refactoring things the user didn't want touched.
- **Inputs & outputs.** *What does the data look like going in, and what shape should come out?* A couple of concrete example rows or a sample of the desired output removes more ambiguity than a paragraph of description.
- **Constraints.** *Libraries to use or avoid, performance limits, style rules, things that must not break?* Invisible to the agent unless stated.
- **Verification.** *How will we check it works — a test, a command to run, a screenshot to compare?* The highest-leverage thing to add and the thing novices most often miss. A prompt that ends with "then run the tests and show me the output" closes the loop so the agent catches its own mistakes. Anthropic's guidance: have the agent *show evidence rather than assert success.*
- **Edge cases & errors.** *What should happen on empty input, bad input, or failure?* Worth a clause when it matters; skip for throwaway scripts.
- **Process preferences (optional).** *For a big or risky change, should the agent plan first, or check in before anything destructive?* Useful for larger tasks; overkill for a one-line fix.

## Step 3 in depth: triage by stakes, not by count

Sort each gap by stakes — not to ration questions, but to decide *how* to resolve it. A gap is **load-bearing** if a wrong guess would change what gets built or reflects a real mismatch in understanding. It's **cosmetic** if any sensible convention works (naming, minor style).

Resolve **every** load-bearing gap — by asking when a wrong guess is both *likely* and *costly*, or by stating a default you flag for veto when a safe convention exists. Cosmetic gaps you just decide and move on. The point is not to minimize questions; it's to leave nothing load-bearing unspoken while keeping each resolution cheap.

Two failure modes, equally bad: **padding** with cosmetic questions (noise that trains the user to dread the check), and **dropping a load-bearing gap to seem terse** (the exact failure this skill exists to prevent). A stated assumption the user can veto is often better than a question — it keeps things moving while still giving them the final say — so prefer it whenever a safe default exists, and save actual questions for the forks where guessing wrong is genuinely likely and genuinely expensive.

## Step 4 in depth: asking without interrogating or looping

When questions are warranted:

- **Ask about every load-bearing fork** where a wrong guess is likely and costly — however many that is. Don't cap the *count*; cap the *friction*.
- **One-tap each.** Batch them into a single round, every question carrying a recommended default, so the user can reply "use the defaults" or answer only the ones they care about. High friction — not high quantity — is what makes questioning feel like interrogation.
- **Offered, never required — the real loop-breaker.** The user can always say "just go," and you proceed on stated assumptions. Because there is always a terminating move, the process *cannot* loop, no matter how many gaps exist.
- **Cap rounds, not questions.** Surface all the gaps in one batch. Open a second round only if the user's answers revealed genuinely new, material forks. Two rounds is plenty.
- **Break a stalemate with a draft, not more questions.** If ambiguity survives a round or two, stop asking — show a concrete rewritten prompt (or a tiny worked example) with the open points flagged. People correct a concrete thing ("no, not that") far faster than they answer an abstract question, so a draft is the quickest way to expose a hidden mismatch.
- **Use the right mechanism.** A structured multiple-choice question tool if the environment has one; otherwise plain text — but always with the defaults.

### Correcting terminology and conventions: direct and respectful

When the user uses a term in a non-standard way, or names an approach that isn't the conventional one, correct it plainly. Name the standard term or practice, say in a clause what it means and why it's the convention, and note where their wording or approach diverged. Do this **directly** — confident and matter-of-fact, the way a good colleague would: *"'Instruction set' isn't the standard term here — the convention is **system prompt**, the standing instructions the model follows every turn. I've used that."* Respect the user enough not to bury the correction in apology or "maybe possibly" hedging; a learner is here to learn the right words and the reasons behind them, and watered-down corrections don't teach. Direct is not harsh: no condescension, no implying they should already have known. Just name it, explain it, move on.

### Recommending a tech choice to a learner

When the task hinges on a technical decision the user hasn't made — which language, framework, database, or convention — and the user is new or unsure, don't just hand down a default. Pair the recommendation with a *compact* rationale and a brief pros/cons so they learn *why* it fits, not just *what* to pick. Name the two or three realistic options that matter here, give each a one-line "good because / costs you," then say which you'd recommend for their situation and why. Keep it short — a sentence or two per option, not a textbook: *"For a small personal app you run yourself, SQLite needs no setup and lives in a single file; Postgres is sturdier once you have many simultaneous users but it's a separate server to run and maintain — so I'd start with SQLite and move up only if you outgrow it."* The reasoning is the gift. Whether the recommendation lands in a question or as a stated default, carry the short "why" with it.

## Step 5 in depth: the output

Four sections, in this order. Keep it tight and scale to the task. (When clarifying questions are warranted, they come *first*, before this deliverable.)

### 1. The cleaned-up prompt

A portable, self-contained prompt the user can copy straight into their coding tool. Present it as its own block so it's obvious what to copy — wrap it in a fenced code block. (If the prompt itself contains triple-backtick code, use a labeled delimiter like `===== PROMPT =====` above and below instead, so the fences don't collide.)

Follow the principles in `references/prompting-principles.md`. The essentials:

- **Scale the structure to the task.** A small fix gets a tightened sentence or two — no headers. A real feature gets light structure: objective, relevant context (named files/stack), specific requirements, what's out of scope, and a verification step. Anthropic's note on self-contained specs: the most useful ones *name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works.*
- **Stay faithful to intent.** Tighten and clarify; don't silently expand scope or invent requirements. Anything you add to fill a gap is an assumption — surface it in section 3.
- **Bake in the answers and decisions.** Fold the user's answers, your stated defaults, and corrected terms directly into the prompt so it stands on its own.
- **End with verification when the task warrants it** — "then run the tests and show the output," "take a screenshot and compare to this design."

### 2. What I changed & corrected — and the convention behind it

The confident edits: things you're sure about and are teaching.
- **Changes** — what you sharpened and why ("Named the file `expenses.csv` so the agent doesn't have to hunt for it").
- **Corrections** — any term or approach where the user diverged from standard practice: name the convention, the deviation, and a one-line why ("'instruction set' → 'system prompt': the standing instructions the model follows every turn; 'instruction set' usually means CPU opcodes"). Direct, taught, done.

### 3. Assumptions & possible misunderstandings — are we still in sync?

**Always include this, even if it's one line.** This is the loop-safe way to surface every remaining rift: make it explicit and cheap to veto instead of gating the work on another round of questions. List every gap you filled with a default or a guess, and anywhere the two of you might still be out of alignment, each framed so it's trivial to correct: *"I took X to mean Y — correct me if not."* Where it helps the user learn, add a clause on what the convention is and where they may have drifted from it, so a wrong assumption is both visible and educational. For an already-clear prompt this collapses to a single line ("Nothing significant assumed — your prompt was specific."). The honesty of this section *is* the safety mechanism: it guarantees no guess stays hidden, which is what lets the skill resolve ambiguity confidently without endless back-and-forth.

### 4. Prompt tips for next time

One or two — never a lecture — tips drawn from *this specific prompt*. Teach the principle through the edit just made: "Notice I added the Python version. Agents otherwise guess, and code that runs on 3.12 can fail on 3.8 — naming the version up front saves a round-trip." If a term or convention was corrected, reinforce it here. A concrete tip tied to the user's own prompt sticks far better than "be more specific," and compounds over time.

## Guardrails

- **Leave no load-bearing gap unspoken — but don't pad with cosmetic ones.** Surfacing a real gap is the job; inventing a non-issue to look thorough is noise. Both matter.
- **Never gate progress.** Questions are offered; the user can always say "just go" and get output with assumptions flagged. This is what keeps the process from looping, no matter how thorough it is.
- **Correct directly and respectfully.** Name the convention, note the deviation, don't drown it in hedging — and don't condescend. A learner wants the real word and the real reason.
- **Don't bulldoze the user's voice or intent.** The rewritten prompt should still sound like their task, just clearer. You're a sharp copy-editor, not a co-author rewriting the brief.
- **Match structure to size.** A typo fix doesn't get an "Acceptance Criteria" header; sections 2 and 3 can be a single line each on a clean prompt.
- **Don't manufacture problems.** If a prompt is genuinely clear and complete, say so — don't "improve" it for its own sake. (Surfacing a real gap is not manufacturing; inventing a fake one to seem busy is.)

## Worked examples

**Example 1 — vague one-liner, several load-bearing gaps**

User's prompt: *"make a script that takes my csv of expenses and tells me how much I spent"*

The sweep finds load-bearing gaps: the CSV's columns are unknown (the agent can't sum a column it can't identify), and "how much I spent" could mean a grand total, a per-category breakdown, or per-month. Language and output format are cosmetic (default Python; printed summary). Ask the two questions that genuinely fork the outcome, each with a default:
> 1. What columns does your CSV have, and which one holds the amount? (If unsure, paste two example rows.)
> 2. Just the grand total, or a breakdown by category and/or month? *(Default: grand total, plus by-category if there's a category column.)*

Then deliver a prompt that names the file, the columns, the breakdown, defaults to Python, and ends with "print the result and show me a sample of the parsed rows so I can confirm it read the file correctly." Section 3 lists the Python and output-format assumptions ("correct me if not"). Tip: how naming the columns up front is what makes the task unambiguous.

**Example 2 — already-clear prompt, no questions needed**

User's prompt: *"In `src/utils/date.ts`, add a `formatRelative(date: Date): string` that returns '3 days ago' style strings. Use the existing `Intl` setup, no new dependencies. Add Jest tests in the sibling `date.test.ts` and run them."*

Clean: file, signature, behavior, constraint, and verification all present, no load-bearing gaps — so no questions. Make at most a tiny tightening (perhaps add one example output to nail the format). Section 3 is a single line ("Nothing significant assumed — only added an example output string, since '3 days ago style' still leaves room for 'last week' vs '7 days ago'."). One affirming tip about how complete the original already was.

**Example 3 — misused terminology**

User's prompt: *"write the instruction set for my chatbot so it always talks like a pirate, and make it a function I can reuse"*

Two vocabulary gaps. "Instruction set" means the **system prompt**; taken literally it's a CPU concept and would baffle the agent. "Make it a function" most likely means a reusable **wrapper** that sends the system prompt with each request, not a single language function. Correct both directly in section 2 (name the convention + the deviation), rewrite into a prompt asking for a system prompt plus a small reusable wrapper, end with "show me an example call and its output so I can confirm it sounds right." Tip: "system prompt" is the word every tool and tutorial uses, so learning it now pays off everywhere.

**Example 4 — an implementation word the user didn't mean as a mandate**

User's prompt: *"write me a javascript function for an n8n code node that does a recursive folder scan of a google drive folder and returns every file path, through all the subfolders no matter how deep"*

"Recursive" names a *technique*, but the *goal* is "every file path in every nested subfolder, to any depth." Those aren't the same: literal recursion can blow the call stack on a deep tree or loop forever if the stop condition is wrong, while an iterative scan using an explicit stack (push/pop) reaches the identical outcome more safely — which is why a coding agent will often produce the iterative version. Reflect the goal back and separate it from the mechanism: *"'Recursive folder scan' reads as a goal — visit every nested subfolder, however deep. I'll write the prompt around that outcome and let the agent pick the implementation, since a loop-with-a-stack approach is usually safer than literal recursion. Say the word if you specifically want true recursion."* Rewrite around the outcome plus the real constraints (arbitrary depth, always terminate, return full paths, runs in an n8n Code node). Section 2 records the recursion → iterative correction with its one-line why; section 3 flags any environment assumptions (auth, folder ID). Tip: describe *what* you want and the constraints, and pin the *how* only when you have a concrete reason.

## References

- `references/prompting-principles.md` — the prompt-writing principles this skill teaches, with citations to Anthropic's primary guidance. Read it for the "why" behind a tip or to ground the rewrite in established practice.
