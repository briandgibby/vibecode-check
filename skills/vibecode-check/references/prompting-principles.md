# Prompt-writing principles for coding agents

The principles vibecode-check teaches, with their grounding in primary sources. When you correct a prompt, you can draw the "why" from here. Citations are to Anthropic's published guidance (read June 2026); the terminology principle is derived from the general "be clear and direct / avoid ambiguity" guidance rather than a single quotable line.

## 1. Be specific; the agent can't read your mind
"Claude can infer intent, but it can't read your mind. Reference specific files, mention constraints, and point to example patterns." Vague prompts are useful only when you're exploring and can afford to course-correct; for a task you want done right, precision reduces corrections.
Source: Best practices for Claude Code — "Provide specific context in your prompts." https://code.claude.com/docs/en/best-practices

## 2. Scope the task — say what's in and what's out
Specify which file, which scenario, and your testing preferences. Self-contained specs "name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works." Stating what NOT to touch is as valuable as stating what to build.
Source: Best practices for Claude Code — "Scope the task" / "Let Claude interview you." https://code.claude.com/docs/en/best-practices

## 3. Give the agent a way to verify its work
"Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop." End prompts with something that returns a pass/fail signal — a test suite, a build, a linter, a screenshot to compare. And have the agent "show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot." This is the single highest-leverage habit for a novice.
Source: Best practices for Claude Code — "Give Claude a way to verify its work." https://code.claude.com/docs/en/best-practices

## 4. For anything non-trivial, separate explore/plan from implementation
"Letting Claude jump straight to coding can produce code that solves the wrong problem." For larger or unfamiliar changes, have the agent explore and plan first. But: "For tasks where the scope is clear and the fix is small... ask Claude to do it directly. If you could describe the diff in one sentence, skip the plan." Match the ceremony to the task size — this is why vibecode-check is adaptive.
Source: Best practices for Claude Code — "Explore first, then plan, then code." https://code.claude.com/docs/en/best-practices

## 5. For a real feature, let the agent interview you first
"For larger features, have Claude interview you first... Ask about technical implementation, UI/UX, edge cases, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered." vibecode-check IS this interview, sized down so a small prompt isn't over-questioned.
Source: Best practices for Claude Code — "Let Claude interview you." https://code.claude.com/docs/en/best-practices

## 6. Reference existing patterns and provide rich context
Point the agent at an example to mirror ("HotDogWidget.php is a good example. follow the pattern..."), reference files directly, paste screenshots, and give URLs for docs. Concrete anchors beat abstract description.
Source: Best practices for Claude Code — "Reference existing patterns" / "Provide rich content." https://code.claude.com/docs/en/best-practices

## 7. Use examples to pin down format
Across Anthropic's prompt-engineering guidance, providing examples (multishot) and being explicit about desired output format are core techniques for removing ambiguity. A single example of the desired output often does more than a paragraph describing it.
Sources: Prompt engineering overview, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview ; Prompting best practices (the canonical techniques reference), https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

## 8. Use the field's standard vocabulary (derived principle)
A prompt only works if a word means the same thing to the writer and the agent. Newer programmers sometimes attach a concept to a near-but-wrong term ("instruction set" for *system prompt*, "function" for a whole *script*, "database" for a single *CSV*). The agent reads the term literally and builds the wrong thing. This is the "avoid ambiguity / be clear and direct" principle applied at the level of individual words: when a term looks non-standard for the evident intent, surface the conventional term, confirm it, and teach it. (Derived from the clarity guidance above rather than a single quotable line.)
Source basis: the clarity/specificity guidance in #1 and in Anthropic's prompt-engineering best practices. https://code.claude.com/docs/en/best-practices

## 9. Describe the goal and constraints, not the implementation — unless you mean to (derived principle)
Naming a mechanism ("make it recursive," "use threads," "cache it in Redis") constrains *how* the agent works, not just *what* it produces. That's the right move when the mechanism genuinely matters — but newer programmers often name a technique they half-learned when they really just want an outcome, and the literal mechanism can be the worse choice (true recursion can overflow the call stack or fail to terminate where an iterative, stack-based scan wouldn't). Prefer stating the goal and the real constraints ("traverse all nested folders to any depth; must always terminate") and let the agent choose the implementation, pinning the technique only when there's a specific reason. (Derived from the specificity/clarity guidance above and standard software practice, not a single quotable line.)
Source basis: the specificity guidance in #1-#2. https://code.claude.com/docs/en/best-practices

## Primary sources
- Best practices for Claude Code — https://code.claude.com/docs/en/best-practices
- Prompt engineering overview — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Prompting best practices (techniques reference) — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Effective context engineering for AI agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
