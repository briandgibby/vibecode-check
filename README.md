# Vibecode Check

A pre-flight check for the prompts you send to coding agents (Claude Code, Cursor, v0, Copilot…). It catches the ambiguities an agent would otherwise *guess* at, asks only the questions that actually matter, and hands back a sharper, copy‑pasteable prompt — plus a short note on what it changed and where you two might still be out of sync.

Built with newer programmers in mind: every rewrite teaches a little, so you get better at writing prompts over time.

> "Claude can infer intent, but it can't read your mind." — the whole reason this skill exists.

## Why

You hold a vivid, detailed picture of what you want in your head — and you write down a fraction of it. The agent fills every gap with a guess, and one wrong guess early (wrong framework, wrong file, wrong idea of "done") can derail a whole session. Vibecode Check closes that gap *before* you hit enter.

## What it does

- **Sweeps for ambiguity** an agent would have to guess at: goal & definition of "done", stack & versions, which files to touch, scope, inputs/outputs, how to verify, and more.
- **Catches vocabulary drift** — non‑standard terms ("instruction set" when you mean *system prompt*) and implementation words you may not mean to mandate ("recursive" when you just want "scan every nested folder, however deep").
- **Asks only the load‑bearing questions**, each with a recommended default so you can reply "use the defaults" — and it never blocks, so it can't loop.
- **Returns a portable prompt** you can paste into any agent, plus a "what I changed & corrected" note and an always‑on **"are we still in sync?"** list of assumptions.

## Example (before → after)

**You typed:**
> *i need to write the instruction set for a customer service chatbot… also can you make it into an api so our website can call it*

**A plain agent** starts building — treating "instruction set" as if it were the system prompt and quietly picking a stack and provider for you.

**Vibecode Check** instead replies:
> *"'Instruction set' isn't the standard term here — the convention is **system prompt**: the standing instructions the model follows every turn. ('Instruction set' usually refers to CPU opcodes.) I've used that term."*

…then asks which AI provider and framework (each with a default), and returns a clean, copy‑pasteable prompt followed by an **"are we still in sync?"** list so no guess stays hidden.

See [`examples/`](./examples) for full before/after transcripts.

## Install

Skills are the same content everywhere — a `SKILL.md` and its resources. Each Claude surface just takes it in a slightly different wrapper, so grab the row that matches how you use Claude:

| If you use…                     | Install with                                   | File / path |
| :------------------------------ | :--------------------------------------------- | :---------- |
| **Claude Code** (CLI)           | the plugin marketplace, or drop in the folder  | plugin, or [`skills/vibecode-check/`](./skills/vibecode-check) |
| **Claude desktop / Cowork**     | the one‑click **"Save skill"** button          | [`dist/vibecode-check.skill`](./dist/vibecode-check.skill) |
| **Claude.ai** (web/desktop)     | upload under **Settings → Capabilities**       | [`dist/vibecode-check.zip`](./dist/vibecode-check.zip) |

> `dist/vibecode-check.skill` and `dist/vibecode-check.zip` are the **same archive** with different extensions — Cowork looks for the `.skill` extension; claude.ai's uploader expects a `.zip`.

### Claude Code — plugin (one‑click)

```text
/plugin marketplace add your-username/vibecode-check
/plugin install vibecode-check@gibby-skills
```

Then invoke it with `/vibecode-check` followed by your prompt — or just let it trigger automatically when a request is fuzzy.

### Claude Code — drop‑in folder

Copy the `skills/vibecode-check/` folder into either `~/.claude/skills/` (every project) or `<your-project>/.claude/skills/` (shared with the repo).

### Claude desktop / Cowork — `.skill`

Download [`dist/vibecode-check.skill`](./dist/vibecode-check.skill) and open it in the Claude desktop app, then click **Save skill**.

### Claude.ai — `.zip` upload

Download [`dist/vibecode-check.zip`](./dist/vibecode-check.zip), then in claude.ai go to **Settings → Capabilities** and add it under Skills. Requires a plan with code execution enabled (Pro, Max, Team, or Enterprise).

## Usage

Paste (or describe) the prompt you're about to send an agent, optionally prefixed with `/vibecode-check`. You'll get back, in this order:

1. **Clarifying questions** — only if needed, each with a recommended default.
2. **The cleaned‑up prompt** — portable and ready to paste.
3. **What I changed & corrected** — with the convention behind each correction.
4. **Are we still in sync?** — assumptions and possible misunderstandings, framed so they're cheap to veto.
5. **A prompt‑writing tip** — drawn from your actual prompt.

## How it works (the philosophy)

- **Understanding first.** The goal is shared understanding, not brevity. It surfaces *every* load‑bearing gap — but keeps each one one‑tap to resolve.
- **Never loops.** Questions are offered, never required; it can always proceed on stated assumptions. Rounds are capped, and a stalemate is broken with a concrete draft, not another round of questions.
- **Teaches as it goes.** Corrections name the standard term *and* where you diverged, so the vocabulary sticks for next time.

## What's inside

```text
vibecode-check/
├── skills/vibecode-check/
│   ├── SKILL.md                       # the skill itself
│   └── references/
│       └── prompting-principles.md    # principles it teaches, with citations
├── dist/
│   ├── vibecode-check.skill           # one-click install (Claude desktop / Cowork)
│   └── vibecode-check.zip             # upload to claude.ai (same archive)
├── examples/                          # real before/after transcripts
├── .claude-plugin/
│   ├── plugin.json                    # plugin manifest
│   └── marketplace.json               # marketplace listing (one-click install)
├── CHANGELOG.md
└── LICENSE
```

> The `dist/` files are rebuilt from `skills/vibecode-check/`. If you change the skill, regenerate them so all three install paths stay in sync.

## How it was built

Developed and validated with an eval harness: each test prompt was run **with and without** the skill, graded against explicit assertions, and reviewed across two iterations. Against a no‑skill baseline the lift was **+0.73** pass‑rate (100% vs ~27%); the v2 "understanding‑first" revision passes 24/24 assertions vs the prior version's 20/24.

## Credits & sources

The coaching is grounded in Anthropic's published guidance — [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) and the [prompt engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview). Full citations are in [`skills/vibecode-check/references/prompting-principles.md`](./skills/vibecode-check/references/prompting-principles.md).

## License

[MIT](./LICENSE) © 2026 Brian Gibby
