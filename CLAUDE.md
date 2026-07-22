# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a design journal for a large-format multi-tool CNC machine (working name "big-cnc") — a pivoting-bed CNC that handles 4'x8' sheet material with a tool carriage that can host a router, laser, drag knife, and pen/plotter. There is currently no code, build system, or tests in this repo — it is a single markdown file, `design-notes.md`, tracking design decisions as the machine concept develops. Do not invent build/lint/test commands; none exist yet.

## Repo convention

`design-notes.md` is a running log, **newest entries at the bottom**, structured as dated `##` sections (e.g. `## 2026-07-19 — Initial concept`) with `###` subsections for follow-ups (Q&A rounds, scope clarifications, estimates). When adding new design notes:

- Append — don't rewrite or reorder existing entries.
- Distinguish firm decisions from open/rough items. The existing pattern uses bold labels (`**Bed size**: ...`) for settled points and explicit disclaimers like `(NOT a decision — ...)` in section headers for rough estimates that are still pending real inputs (load calcs, precision targets, etc.).
- When a value is genuinely undecided, say so explicitly (e.g. "TBD", "unknown/open") rather than picking a default.

## Current design state (as of the latest entry)

Key parameters already settled — check `design-notes.md` directly before relying on these, as they will change as the design evolves:

- 4'x8' bed, pivots on a center axis from horizontal to vertical (manual actuation first, motorized later)
- Dual-rail gantry along the 8' Y axis, belt-driven X/Y (precision prioritized over speed), 4–6" Z travel
- Welded steel tube frame (mobile "truck" base with lifting casters, separate from the gantry/carriage)
- Multi-tool carriage (router, laser, drag knife, pen) — tool-changing approach still open
- 220V/60A single-phase power available; target base footprint ~4'x3'
- No quantified precision target yet — this is called out as the key open variable driving structural sizing
