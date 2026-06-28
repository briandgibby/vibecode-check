# Changelog

All notable changes to this skill are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); this project uses
[semantic versioning](https://semver.org/).

## [Unreleased]
### Changed
- Shortened and enriched `SKILL.md` frontmatter metadata for better validator headroom and discoverability.
- Rebuilt distributable archives with a root-level `SKILL.md` layout and deterministic timestamps.

### Added
- Release helper scripts for deterministic dist builds and package validation.
- Marketplace description for cleaner Claude Code plugin validation.

### Fixed
- Replaced placeholder GitHub URLs in plugin metadata and README install instructions.

## [2.0.0] - 2026-06-24
### Changed
- Reframed from a "minimize questions" posture to **understanding-first**: surface
  every load-bearing gap, ask only the forks where a wrong guess is likely and costly
  (each with a one-tap default), and never gate progress. Caps clarification *rounds*,
  not question count, so it can't loop.

### Added
- Always-on **"Assumptions & possible misunderstandings — are we still in sync?"**
  section that surfaces residual guesses as cheap-to-veto items.
- **Direct** terminology/convention corrections that name the standard term and where
  the user diverged (e.g. "instruction set" → "system prompt").
- **Goal vs. mechanism** check — catches implementation words like "recursive" that
  the user may not actually mean to mandate.
- **Tech-choice coaching** — brief pros/cons when recommending a stack to a learner.

## [1.0.0] - 2026-06-24
### Added
- Initial release: adaptive ambiguity sweep, clarifying questions with recommended
  defaults, a portable rewritten prompt, change notes, prompt-writing tips, and
  terminology-mismatch detection.
