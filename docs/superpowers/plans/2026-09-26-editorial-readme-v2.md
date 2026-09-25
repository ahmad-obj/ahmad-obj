# Editorial README v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the current profile README with a scroll-driven editorial monograph made from a sequence of high-fidelity static visual panels and minimal accessible Markdown links.

**Architecture:** Generate seven deterministic SVG panels from one shared visual system. Each panel is a static “frame” in a larger kinetic identity sequence, so browser scrolling supplies the motion while GitHub only renders ordinary SVG/PNG assets. Use one real automotive screenshot where project imagery exists; keep the other project visuals typographic/diagrammatic and grounded in actual project content.

**Tech Stack:** SVG 1.1, Python 3 standard library for deterministic panel generation/tests, GitHub Markdown/HTML, repository images.

**Spec:** docs/superpowers/specs/2026-09-26-editorial-readme-v2-design.md

## Global Constraints

- GitHub does not support inline SVG animation; all shipped SVGs must be static.
- Theme: #0B0B0A background, #F1EEE7 primary, #9B9993 secondary, #343432 hairline, #F04A2A accent.
- Accent ≤ 10% of each panel.
- No badges, GitHub stats, HUDs, fake metadata, neon, gradient soup, card grids, generic tech decoration, or explanatory hero slogan.
- Major panels are 1200px wide and use strong negative space.
- Three primary projects: 3D Automotive Experience, Multimodel Orchestration, AI Digit Recognizer.
- Secondary work: Sixty-Four, WEBERAISE, Scout Email.
- README copy stays short and links remain real HTML/Markdown links.
- Every SVG must remain readable as a static image and contain an accessible <title>.

## Review Focus

- Dark/light GitHub themes: panels must remain self-contained and not depend on page background.
- Small laptop width: critical text must remain legible when a 1200px SVG is scaled to ~800px.
- Repetition: no two adjacent major panels may share the same composition.
- Fake technical imagery: orchestration/digit visuals must come from real project concepts, not invented dashboards.
- Asset weight: total new README assets should stay below 4 MB.

### Task 1: Shared panel generator and visual contract
**Files:** create tools/readme_v2/generate.py, tests/test_readme_v2.py
- [ ] Write tests for exact palette, panel width, accessible title, no animation/script tags, and required copy.
- [ ] Run tests and observe RED.
- [ ] Implement shared SVG helpers and cover/identity panel generation.
- [ ] Run tests GREEN.

### Task 2: Primary project panels
**Files:** modify tools/readme_v2/generate.py; create assets/editorial/01-automotive.svg, 02-orchestration.svg, 03-digit.svg
- [ ] Add tests pinning titles, stacks, unique composition markers, and real project-derived visual motifs.
- [ ] Run RED.
- [ ] Implement three deliberately different spreads.
- [ ] Run GREEN.

### Task 3: Secondary work, stack, ending
**Files:** create assets/editorial/04-secondary.svg, 05-stack.svg, 06-end.svg
- [ ] Add tests for the three secondary projects, exact stack terms, and minimal ending.
- [ ] Run RED.
- [ ] Implement panels with reduced density relative to primary work.
- [ ] Run GREEN.

### Task 4: README composition
**Files:** modify README.md
- [ ] Add tests asserting the exact panel order, primary project links, no old geometric-system.svg reference, no badge/stat widgets, and concise identity/contact block.
- [ ] Run RED.
- [ ] Replace README with the editorial sequence and linked project panels.
- [ ] Run GREEN.

### Task 5: Final visual/technical gate
- [ ] Generate every panel from scratch.
- [ ] Run full test suite.
- [ ] Verify every SVG parses as XML, has viewBox 0 0 1200 <height>, and total new asset size < 4 MB.
- [ ] Review cover + all major panels at 1200px and simulated 800px width.
- [ ] Reject if any panel reads like a dashboard/card template or if AHMAD is not immediately legible in the cover.
