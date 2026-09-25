# The Loom v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and ship a deterministic 18-second animated GitHub profile hero in which a two-state Truchet-style loom generates long routed threads, selectively lifts the strongest routes into shallow ribbons, and loops seamlessly without HUD or explanatory text.

**Architecture:** Add a small offline Python renderer under `tools/loom/`. The generator produces a deterministic 30×11 two-state tile field and a cyclic mutation schedule; path tracing converts the field into continuous routes and ranks them; the renderer draws a warm vellum composition with flat threads, selective lifted ribbons, over/under crossings, subtle material grain, and soft directional shadows. The exporter renders an optimized animated GIF plus poster PNG into `assets/`, and the README embeds only the final artwork.

**Tech Stack:** Python 3.12+, Pillow, Python standard library `random`/`math`/`dataclasses`/`unittest`; GitHub Markdown image embedding.

**Spec:** `docs/superpowers/specs/2026-09-25-the-loom-design.md`

## Global Constraints

- Canvas: exactly 1200 × 430.
- Loom field: exactly 30 columns × 11 rows.
- Tile grammar: exactly two mirrored curved tile states; each state is implemented as complementary quarter-turn route arcs so every shared cell edge remains routable.
- Three slow mutation/growth zones: primary, secondary, repair.
- Path classes: Whisper 1–4 tiles, Resident 5–10, Major 11–18, Signature 19+.
- Signature prominence: 1–3 dominant routes at a time.
- Major lift: 2–3 px apparent elevation; Signature lift: 4–7 px.
- Accent: ultramarine `#2D4FB8`, below roughly 8% of visible thread mass.
- Background range stays within the approved warm vellum family; primary route remains graphite/carbon.
- Loop target: 18 seconds.
- No text inside the artwork.
- No HUD, metadata, labels, neon, glow, particles, gradient soup, tubes, chrome, or universal 3D extrusion.
- The production asset must be deterministic: identical seed + config => identical key states and output frame hashes.
- Keep the previous README backup branch untouched.
- Target final animated asset size: <= 10 MB; prefer <= 7 MB without visible degradation.

## Review Focus

- **Seam frame:** final animation state must visually match frame 0 closely enough that the loop does not flash or jump; pinned in Task 4.
- **Degenerate route field:** unusual tile states must not produce empty/invalid path lists or crash ranking; pinned in Task 2.
- **Signature overload:** route ranking must never promote more than three Signature routes at one frame; pinned in Task 2.
- **Accent overuse:** renderer must keep ultramarine coverage below the configured 8% ceiling; pinned in Task 3.
- **Asset bloat:** export must fail its QA check if the GIF exceeds 10 MB; pinned in Task 4.

---

## File Structure

- `tools/loom/config.py` — immutable dimensions, palette, timing, seed, class thresholds.
- `tools/loom/model.py` — two-state tile field, regional bias, growth zones, reversible cyclic mutation schedule.
- `tools/loom/paths.py` — route tracing, route length/classification, signature selection, crossing ownership.
- `tools/loom/render.py` — material composition and single-frame drawing.
- `tools/loom/export.py` — frame orchestration, GIF/poster export, palette optimization, deterministic QA metadata.
- `tools/loom/__main__.py` — CLI entry point.
- `tools/loom/requirements.txt` — Pillow dependency.
- `tests/test_loom_model.py` — determinism and cyclic schedule tests.
- `tests/test_loom_paths.py` — route continuity/hierarchy/crossing tests.
- `tests/test_loom_render.py` — visual-contract pixel/statistical tests.
- `tests/test_loom_export.py` — seam, dimensions, frame count, and asset-size tests.
- `assets/loom.gif` — production animated hero.
- `assets/loom-poster.png` — representative still for review/debugging.
- `README.md` — switch hero image to `assets/loom.gif`; no new hero copy.

### Task 1: Deterministic Loom State and Cyclic Mutation Schedule

**Files:**
- Create: `tools/loom/config.py`
- Create: `tools/loom/model.py`
- Create: `tools/loom/requirements.txt`
- Create: `tests/test_loom_model.py`

**Interfaces:**
- Produces: `LoomConfig`, `GridState`, `MutationEvent`, `build_initial_grid(config) -> GridState`, `build_cycle(config, grid) -> list[MutationEvent]`, `state_at(config, initial, events, t) -> GridState`
- Consumes: nothing from later tasks.

- [ ] **Step 1: Write deterministic-grid and cycle tests**

Assert:
- grid dimensions are 30×11;
- cell values are only `0` or `1`;
- same seed produces identical initial grid and mutation schedule;
- a different seed changes at least one cell or event;
- `state_at(..., 0.0)` equals `state_at(..., 18.0)`;
- each scheduled cell flips an even number of times over the complete cycle;
- events are assigned among exactly three growth-zone IDs.

Run: `python -m unittest tests.test_loom_model -v`
Expected: FAIL because `tools.loom.model` does not exist.

- [ ] **Step 2: Implement config and deterministic initial field**

Create `LoomConfig` with exact locked values:
- `width=1200`, `height=430`
- `cols=30`, `rows=11`
- `duration_s=18.0`
- `fps=12`
- fixed default seed `20260925`
- approved palette and hierarchy thresholds.

`build_initial_grid` combines a low-frequency analytic bias field with seeded randomness so broad tile-orientation regions emerge instead of white noise.

- [ ] **Step 3: Implement three-zone reversible cycle**

`build_cycle` generates a deterministic set of local mutation events for primary, secondary, and repair zones. Every mutated tile must receive a paired later mutation so the topology closes back to the initial state at 18.0s. Keep per-beat visible changes small: no event mutates more than six cells.

- [ ] **Step 4: Implement interpolated tile transition state**

`state_at` returns tile orientation plus per-cell transition progress so render code can morph a flip over several frames rather than pop topology instantly.

- [ ] **Step 5: Run model tests**

Run: `python -m unittest tests.test_loom_model -v`
Expected: PASS.

- [ ] **Step 6: Commit**

`git add tools/loom/config.py tools/loom/model.py tools/loom/requirements.txt tests/test_loom_model.py && git commit -m "feat: add deterministic loom state engine"`

---

### Task 2: Continuous Route Tracing and Hierarchy

**Files:**
- Create: `tools/loom/paths.py`
- Create: `tests/test_loom_paths.py`

**Interfaces:**
- Consumes: `GridState`, `LoomConfig` from Task 1.
- Produces: `Route`, `Crossing`, `trace_routes(grid) -> list[Route]`, `classify_routes(routes, config) -> list[Route]`, `select_signature_routes(routes, limit=3) -> list[Route]`, `assign_crossings(routes) -> list[Crossing]`.

- [ ] **Step 1: Write route topology tests**

Use small hand-authored tile grids and assert:
- every traced route is edge-continuous;
- boundary routes terminate only at outer edges;
- closed loops return to their starting half-edge;
- all valid half-edges are consumed exactly once;
- empty/degenerate small grids return a valid list rather than throwing;
- class boundaries are exactly 1–4 / 5–10 / 11–18 / 19+;
- `select_signature_routes(..., limit=3)` never returns more than three routes.

Run: `python -m unittest tests.test_loom_paths -v`
Expected: FAIL because route tracer is missing.

- [ ] **Step 2: Implement two-state Truchet topology**

Represent each cell state as the two mirrored complementary quarter-turn arc pair. Trace routes through shared edges without branching, assigning each traversed arc a stable route ID.

- [ ] **Step 3: Implement hierarchy and composition-aware ranking**

Classify by exact spec thresholds. Signature selection ranks by length first, then favors routes whose visible span crosses the center-right focus region and penalizes routes concentrated entirely in the negative-space pocket.

- [ ] **Step 4: Implement deterministic over/under ownership**

At spatially close route crossings, assign upper/lower ownership deterministically from route rank and crossing index. Signature beats Major; Major beats Resident; ties alternate using stable route IDs.

- [ ] **Step 5: Run path tests**

Run: `python -m unittest tests.test_loom_paths -v`
Expected: PASS.

- [ ] **Step 6: Commit**

`git add tools/loom/paths.py tests/test_loom_paths.py && git commit -m "feat: trace and rank loom routes"`

---

### Task 3: Material Frame Renderer

**Files:**
- Create: `tools/loom/render.py`
- Create: `tests/test_loom_render.py`

**Interfaces:**
- Consumes: `LoomConfig`, interpolated grid state, classified `Route` and `Crossing`.
- Produces: `render_frame(config, state, routes, crossings, t) -> PIL.Image.Image`.

- [ ] **Step 1: Write renderer contract tests**

Assert a rendered frame:
- is exactly 1200×430 RGB/RGBA;
- has no text layer/input dependency;
- background median color stays inside the approved vellum range;
- graphite occupies more pixels than ultramarine;
- ultramarine coverage remains < 8% of non-background route pixels;
- a frame containing a Signature route contains measurable soft-shadow pixels offset from the ribbon;
- a frame with no Major/Signature routes does not invent lifted geometry.

Run: `python -m unittest tests.test_loom_render -v`
Expected: FAIL because renderer is missing.

- [ ] **Step 2: Implement vellum surface**

Draw a matte warm mineral base with deterministic low-amplitude luminance grain. No visible vignette, gradient wash, or grunge texture.

- [ ] **Step 3: Implement flat route drawing**

Map tile edge points into the centered 30×11 composition. Draw Whisper/Resident routes with precise quarter-curves, hierarchy-specific graphite values, round joins, and the spec’s restrained stroke widths.

- [ ] **Step 4: Implement lifted ribbon spans**

For Major/Signature routes, derive only selected middle spans as lifted geometry. Render in order:
1. diffuse warm shadow;
2. narrow darker side face;
3. graphite top ribbon;
4. restrained warm edge highlight.

Elevation is 2–3 px for Major and 4–7 px for Signature. Ends remain visually anchored.

- [ ] **Step 5: Implement over/under crossings**

Use `Crossing` ownership from Task 2 to mask the lower route briefly under the upper ribbon and render the upper route shadow across it. Keep crossing treatment sparse and local.

- [ ] **Step 6: Implement ultramarine lifecycle**

Ultramarine `#2D4FB8` appears only on recently woven portions of selected Major/Signature routes and decays back toward graphite. Enforce the 8% pixel budget in render logic.

- [ ] **Step 7: Run renderer tests and save manual poster**

Run: `python -m unittest tests.test_loom_render -v`
Expected: PASS.

Generate: `python -m tools.loom --poster assets/loom-poster.png`
Expected: 1200×430 poster with no text/HUD and visible selective depth.

- [ ] **Step 8: Commit**

`git add tools/loom/render.py tests/test_loom_render.py assets/loom-poster.png && git commit -m "feat: render material loom artwork"`

---

### Task 4: 18-Second Animation Export and Seam QA

**Files:**
- Create: `tools/loom/export.py`
- Create: `tools/loom/__main__.py`
- Create: `tests/test_loom_export.py`
- Create: `assets/loom.gif`

**Interfaces:**
- Consumes: all Task 1–3 APIs.
- Produces: CLI `python -m tools.loom --output assets/loom.gif --poster assets/loom-poster.png`; production GIF and deterministic frame metadata.

- [ ] **Step 1: Write export tests**

Assert:
- frame count is exactly `18 × 12 = 216`;
- every frame is 1200×430;
- frame 0 and the computed t=18.0 seam reference have identical logical state;
- rendered first/last seam difference stays below a fixed low pixel-difference threshold;
- generated GIF loops infinitely;
- output file is <= 10 MB;
- two test renders with same seed produce identical SHA-256.

Run: `python -m unittest tests.test_loom_export -v`
Expected: FAIL because exporter is missing.

- [ ] **Step 2: Implement choreography mapping**

Map the spec phases exactly:
- 0.0–2.5 Quiet setup
- 2.5–5.5 First weave
- 5.5–8.5 Continuity
- 8.5–12.0 Lift
- 12.0–15.0 Reweave
- 15.0–18.0 Return

Use easing only to control mutation visibility, ribbon lift, shadow depth, and accent decay; never add independent decorative motion.

- [ ] **Step 3: Implement GIF export**

Render 216 frames at 12 fps. Quantize with a stable shared palette biased toward vellum, graphite, shadow, highlight, and ultramarine. Enable loop forever and optimization. Do not dither if it produces noisy paper texture.

- [ ] **Step 4: Enforce asset-size QA**

After export, fail the command with a clear message if `assets/loom.gif` exceeds 10 MB. If the initial export is > 7 MB, first reduce palette complexity and frame delta before considering lower dimensions or lower FPS.

- [ ] **Step 5: Run complete tests and inspect representative frames**

Run:
- `python -m unittest discover -s tests -p "test_loom_*.py" -v`
- `python -m tools.loom --output assets/loom.gif --poster assets/loom-poster.png`

Expected:
- all tests PASS;
- output <= 10 MB;
- no seam flash;
- representative frames at 0s / 6s / 10s / 14s show setup / continuity / lifted climax / reweave distinctly.

- [ ] **Step 6: Commit**

`git add tools/loom/export.py tools/loom/__main__.py tests/test_loom_export.py assets/loom.gif assets/loom-poster.png && git commit -m "feat: export seamless Loom animation"`

---

### Task 5: README Integration and Final Visual Gate

**Files:**
- Modify: `README.md`
- Keep: existing backup branch `backup/readme-2026-09-25` unchanged.
- Remove from active README reference: `assets/geometric-system.svg`
- Use: `assets/loom.gif`

**Interfaces:**
- Consumes: final `assets/loom.gif`.
- Produces: live profile README with The Loom as the sole hero artwork.

- [ ] **Step 1: Write/read the README integration assertion**

Verify the README:
- references exactly one hero image at `./assets/loom.gif`;
- does not reference `geometric-system.svg`;
- adds no slogan, technical metadata, or explanatory copy inside/above the artwork.

- [ ] **Step 2: Replace hero reference only**

Change the top image source to `./assets/loom.gif` and alt text to a plain descriptive phrase such as `Muhammad Ahmad — The Loom`. Do not add new headings or hero labels.

- [ ] **Step 3: Verify repository and asset**

Run:
- `python -m unittest discover -s tests -p "test_loom_*.py" -v`
- inspect `assets/loom.gif` dimensions, frame count, loop flag, file size, and SHA-256;
- fetch `README.md` after commit and confirm its hero reference.

Expected: all automated checks pass and README contains only the intended hero swap.

- [ ] **Step 4: Visual review gate**

Review at least four rendered moments: start, continuity build, lifted climax, reweave. Reject and iterate if any of these are true:
- the tile rule is unreadable;
- the whole field has equal visual density;
- more than three routes dominate;
- lifted geometry resembles pipes/tubes;
- ultramarine becomes a general color wash;
- movement reads as glitching rather than weaving;
- the result resembles a dashboard, screensaver, or generic generative-art demo.

- [ ] **Step 5: Commit**

`git add README.md assets/loom.gif && git commit -m "feat: ship The Loom profile hero"`

