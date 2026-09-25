# README v3 Typography Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recompose the GitHub profile into a mostly native-text README punctuated by three small, highly stylized typographic artworks while retaining the existing AHMAD hero and two lightweight motion strips.

**Architecture:** Extend the existing deterministic README asset workflow with a focused static-typography generator that emits three PNG section marks: CURRENT, ACADEMIC, and INTERESTS. Keep all actual profile content in Markdown/HTML, then rewrite README.md around those marks so imagery remains a minority of the page by vertical area.

**Tech Stack:** Python 3.13, Pillow, GitHub Markdown/HTML, existing GIF motion generator, unittest.

**Spec:** `docs/superpowers/specs/2026-09-26-readme-v3-typography-design.md`

## Global Constraints

- Keep `assets/editorial/00-cover.svg`, `assets/motion/ascii-interference.gif`, and `assets/motion/selected-work.gif`.
- Add exactly three new static PNG typographic artworks.
- Each new artwork is 1000px wide, 100–150px tall, and under 150 KB.
- New typography palette is limited to #F04A2A, #3157D5, #E7F04A, #F1EEE7, #0B0B0A, and #9B9993; each artwork uses at most four colors.
- README stays mostly native text and contains no badges, fake terminal prompts, pseudo-system metadata, slogans, emoji, or project-banner images.
- No new large animated assets.
- Total new static typographic assets remain below 450 KB.
- Current content: Real-time graphics · Agent orchestration · Experimental interfaces.
- Academic content: BS Computer Science — FAST-NUCES · Dean's List ×2 · 1st position — BISE Gujranwala ICS.
- Interests content: Real-time graphics · AI systems · Developer tooling · Interaction design · Systems programming.

## Review Focus

- **GitHub scaling:** At ~800px rendered width, all three section marks must remain legible and visually distinct.
- **Visual dominance:** AHMAD must remain stronger than CURRENT/ACADEMIC/INTERESTS; new art cannot become a second hero.
- **Text fallback:** If images fail, all section meaning must still exist in native Markdown text immediately below the artwork.
- **Color discipline:** Registration offsets/contours may not create muddy low-contrast text or exceed four colors per artwork.
- **Density:** There must be no more than five visual assets before the main project list, and native text must occupy more vertical space than decorative media.

---

### Task 1: Lock the v3 README contract

**Files:**
- Modify: `tests/test_readme_lean.py`
- Create: `tests/test_readme_typography.py`

**Interfaces:**
- Consumes: existing `README.md`, retained hero/GIF asset paths.
- Produces: behavioral tests that later generator/README tasks must satisfy.

- [ ] **Step 1: Write failing tests for section artwork contract**

Create tests asserting:
- `assets/typography/current.png`, `academic.png`, `interests.png` exist.
- Each image width is 1000px.
- Each height is between 100 and 150px.
- Each file is <150 KB.
- Combined size is <450 KB.

- [ ] **Step 2: Write failing tests for README structure**

Assert exact order:
1. hero
2. CURRENT art + Current text
3. ACADEMIC art + Academic text
4. INTERESTS art + Interests text
5. ASCII strip
6. SELECTED WORK strip
7. main projects
8. Other work
9. Tools
10. footer

Also assert:
- no old project-panel SVG references
- no raw car screenshot
- no badges/stats URLs
- academic achievements are present as text

- [ ] **Step 3: Run the new tests and verify RED**

Run:
`python -m unittest tests.test_readme_typography -v`

Expected: FAIL because the three typography PNGs and v3 README structure do not exist yet.

- [ ] **Step 4: Commit tests**

```bash
git add tests/test_readme_typography.py tests/test_readme_lean.py
git commit -m "test: define README v3 typography contract"
```

### Task 2: Build deterministic typography generator

**Files:**
- Create: `tools/readme_typography/generate.py`
- Create: `assets/typography/current.png`
- Create: `assets/typography/academic.png`
- Create: `assets/typography/interests.png`
- Test: `tests/test_readme_typography.py`

**Interfaces:**
- Produces:
  - `render_current() -> Image.Image`
  - `render_academic() -> Image.Image`
  - `render_interests() -> Image.Image`
  - `save_all(output_dir: Path) -> None`

- [ ] **Step 1: Implement `render_current()` minimally**

Use a condensed/bold sans available in the runner environment. Render CURRENT with 3–4 deliberately offset layers using coral, cobalt, acid yellow, and off-white. Crop one layer slightly while keeping the front word fully legible.

- [ ] **Step 2: Run CURRENT-specific tests**

Run:
`python -m unittest tests.test_readme_typography.ReadmeTypographyTests.test_current_asset -v`

Expected: PASS.

- [ ] **Step 3: Implement `render_academic()` minimally**

Render ACADEMIC with repeated back-projected copies to create a diagonal extrusion/perspective stack. Use off-white front face and cobalt/coral depth layers; no bevel/chrome.

- [ ] **Step 4: Run ACADEMIC-specific tests**

Run:
`python -m unittest tests.test_readme_typography.ReadmeTypographyTests.test_academic_asset -v`

Expected: PASS.

- [ ] **Step 5: Implement `render_interests()` minimally**

Render INTERESTS with 8–12 repeated outline contours drifting in depth, then a crisp front face. Accent only selected contours with coral/cobalt.

- [ ] **Step 6: Run INTERESTS-specific tests**

Run:
`python -m unittest tests.test_readme_typography.ReadmeTypographyTests.test_interests_asset -v`

Expected: PASS.

- [ ] **Step 7: Implement `save_all(output_dir: Path) -> None` and size optimization**

Save PNGs with deterministic compression and palette reduction only if necessary to remain under the 150 KB per-file limit without visible banding.

- [ ] **Step 8: Run full typography test file**

Run:
`python -m unittest tests.test_readme_typography -v`

Expected: PASS.

- [ ] **Step 9: Commit generator and images**

```bash
git add tools/readme_typography/generate.py assets/typography tests/test_readme_typography.py
git commit -m "feat: add experimental typography section marks"
```

### Task 3: Recompose README around native text

**Files:**
- Modify: `README.md`
- Test: `tests/test_readme_typography.py`
- Test: `tests/test_readme_lean.py`

**Interfaces:**
- Consumes: all retained and new asset paths.
- Produces: final GitHub-native document structure.

- [ ] **Step 1: Rewrite README in the spec order**

Keep hero + identity links first.

Insert:
- CURRENT image, then one compact native-text line/list
- ACADEMIC image, then the three academic lines
- INTERESTS image, then compact interest terms

Then keep:
- ASCII interference
- SELECTED WORK motion
- three selected projects as native Markdown
- Other work
- Tools
- footer links

- [ ] **Step 2: Keep project copy compact**

Each selected project remains:
- linked heading
- one sentence
- one stack line

Do not introduce cards, tables, badges, screenshots, or extra art.

- [ ] **Step 3: Run README structure tests**

Run:
`python -m unittest tests.test_readme_typography tests.test_readme_lean -v`

Expected: PASS.

- [ ] **Step 4: Commit README composition**

```bash
git add README.md
git commit -m "feat: recompose profile around experimental typography"
```

### Task 4: Visual and performance verification

**Files:**
- Modify only if review finds defects.

**Interfaces:**
- Consumes: final README and generated images.
- Produces: reviewed branch ready for integration.

- [ ] **Step 1: Render or inspect each typography PNG at 1000px**

Verify:
- CURRENT reads instantly despite registration offsets.
- ACADEMIC reads instantly despite perspective depth.
- INTERESTS reads instantly despite contours.

- [ ] **Step 2: Inspect all three at simulated ~800px GitHub width**

Reject any treatment whose front word becomes ambiguous.

- [ ] **Step 3: Check palette and file sizes**

Run a script/test that reports:
- dimensions
- file sizes
- unique dominant palette entries

Expected:
- each <150 KB
- total <450 KB
- no out-of-palette colors beyond anti-aliasing blends

- [ ] **Step 4: Run full project test suite**

Run:
`python -m unittest discover -s tests -v`

Expected: 0 failures.

- [ ] **Step 5: Compare branch against main**

Confirm diff contains only:
- README changes
- retained AHMAD hero from earlier branch work
- retained two motion assets/source/tests
- three new typography PNGs
- typography generator/tests
- design/plan docs

No discarded image-heavy project panels should remain.

- [ ] **Step 6: Commit any visual fixes**

If review required changes, commit them with:
`git commit -m "fix: refine README typography composition"`
