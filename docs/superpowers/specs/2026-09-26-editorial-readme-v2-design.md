# Editorial README v2 — Design Specification

## Intent

Rebuild the GitHub profile as a single editorial identity system rather than a conventional developer README.

The profile should read like a compact digital monograph:
- one strong visual idea
- disciplined typography
- large project-led compositions
- very little copy
- no badge walls, card grids, fake dashboards, or generic developer-profile motifs
- motion only where it is native to the identity and remains smooth on GitHub

The design must still work as a static composition if animation is unavailable.

## Reference Principles

### Muriel Cooper / MIT
Reference:
- https://www.media.mit.edu/posts/muriel-cooper-lasting-imprint/
- https://mitpress.mit.edu/9780262036504/muriel-cooper/
- https://acg.media.mit.edu/projects/thesis/DSThesis.pdf

Extracted principles:
- crisp typographic structure before effects
- simple forms and clean lines
- spatial typography used to communicate hierarchy, not decorate it
- technology serves meaning rather than becoming the subject
- motion may introduce depth, simultaneity, and transformation without destroying legibility

### DIA Studio
Reference:
- https://dia.tv/project/mailchimp/
- https://dia.tv/project/catk/
- https://dia.tv/project/a-trak-identity/

Extracted principles:
- motion comes from the identity system itself
- remove decorative layers that do not scale
- identity should function in both motion and static form
- flexible rules create variation while preserving recognition
- the identity supports the work rather than overpowering it

### Karel Martens
Visual reference:
- Design Museum Gent, Karel Martens: Motion

Extracted principles:
- aggressive scale contrast can coexist with restraint
- typography may overlap structured color/form without becoming noisy
- print-like rhythm and cropping can make a page feel authored rather than templated

## Core Visual Identity

### Hero concept: AHMAD as movable architecture

The hero is built around the word:

AHMAD

The letters are custom modular forms, divided into a limited set of geometric pieces:
- stems
- counters
- diagonals
- horizontal bars
- cropped planes

The resting state is immediately legible.

During motion, the pieces:
- translate
- rotate
- scale
- pass behind masks
- briefly form abstract spatial compositions
- resolve back into AHMAD

The motion is not a morphing gimmick and not continuous chaos.

The identity should remain recognizable throughout most of the cycle.

### Motion requirements

Preferred delivery:
- lightweight SVG using transform animation only
- no JavaScript
- no particles
- no hundreds of animated nodes
- no raster frame sequence

Motion should be smooth because the browser interpolates vector transforms.

Fallback:
- the first frame is a complete, intentional static cover
- if GitHub does not animate a given client, the profile still looks finished

Target cycle:
- approximately 9–12 seconds
- slow overlapping motion
- no abrupt resets
- no “loading animation” feel

## Palette

Theme: dark.

- Background: #0B0B0A
- Primary: #F1EEE7
- Secondary gray: #9B9993
- Hairline: #343432
- Accent: #F04A2A

Rules:
- accent never exceeds roughly 8–10% of any composition
- no gradients unless physically necessary for a project image
- no purple, cyan, neon, glow, glass, or metallic UI treatment

## Typography

The visual system should feel editorial rather than product-UI.

Use:
- custom/path-based display lettering for AHMAD
- large editorial display type for project titles
- restrained sans-serif for metadata and descriptions

Avoid:
- monospace-as-personality
- tech badges
- uppercase micro-label spam
- tiny pseudo-system text
- fake coordinates / version strings / terminal language

If exact custom display fonts are used inside rendered panels, convert the display text to outlines/paths so GitHub rendering does not depend on local font availability.

## README Structure

### 1. Kinetic Cover

Visual:
- full-width dark panel
- giant modular AHMAD occupies most of the width
- single orange-red intervention
- strong negative space
- no slogan

Visible text:
- AHMAD

Below the artwork in normal README markup:
- Muhammad Ahmad
- Computer Science · FAST-NUCES
- Portfolio · LinkedIn · Email

Do not place explanatory copy inside the artwork.

### 2. Selected Work

No conventional heading card.

A simple editorial transition introduces the work.

Primary projects:

#### 3D Automotive Experience
Repository:
https://github.com/ahmad-obj/3dcarweb

Title:
3D Automotive Experience

Copy:
Cinematic real-time automotive experience focused on WebGL, camera choreography, lighting, materials, and motion.

Stack:
Next.js · Three.js · React Three Fiber · WebGL

Visual treatment:
- largest project spread
- one strong automotive crop
- image occupies 45–60% of composition
- typography overlaps/crops against the image only where legibility remains strong
- no dashboard/UI framing around the screenshot

#### Multimodel Orchestration
Repository:
https://github.com/ahmad-obj/multimodel-orchestration

Title:
Multimodel Orchestration

Copy:
AI coding-worker orchestration through shared state, task routing, persistence, and verification.

Stack:
Python · LangGraph · SQLite

Visual treatment:
- more architectural and abstract than the car project
- use structure, routing, or state as visual inspiration
- avoid fake node-network diagrams
- composition should feel editorial, not like architecture documentation

#### AI Digit Recognizer
Repository:
https://github.com/ahmad-obj/AI-digit-recognizer

Title:
AI Digit Recognizer

Copy:
Interactive handwritten-digit recognition with confidence feedback and network visualization.

Stack:
Python · PyTorch · Pygame

Visual treatment:
- tighter, more experimental spread
- use a real digit/stroke/recognition visual from the project
- avoid generic AI brain/neural imagery

### 3. Secondary Work

Use smaller editorial specimens rather than a second card grid.

Projects:

#### Sixty-Four
https://github.com/ahmad-obj/Chess

Copy:
Customizable chess system with Stockfish, variants, clocks, persistence, and desktop build support.

Stack:
C++17 · SFML · Stockfish

#### WEBERAISE
https://github.com/ahmad-obj/Weberaise

Copy:
Motion-led web work, custom interaction, and WebGL experiments.

Stack:
Next.js · Motion · WebGL

#### Scout Email
https://github.com/ahmad-obj/scout-email

Copy:
Structured prospect discovery and personalized outreach automation.

Stack:
Python · Automation · LLM workflows

Secondary work should occupy substantially less vertical space than the three primary projects.

## Tools / Stack

No logos and no badge wall.

Use a typographic composition with large, spaced words:

PYTHON   C++   TYPESCRIPT   THREE.JS
REACT   NEXT.JS   PYTORCH   WEBGL
LANGGRAPH   OPENCV   SQLITE   LINUX

The stack block should look like part of the publication, not a résumé appendix.

## Ending

Minimal.

Content:
Muhammad Ahmad

Links:
Portfolio · LinkedIn · Email · GitHub

Optional:
A small static fragment derived from the AHMAD modular hero.

No quote, slogan, visitor counter, stats card, streak card, contribution chart duplication, or generated metrics.

## Layout System

Overall:
- one coherent visual system from top to bottom
- no repeated card component
- no equal-width three-card row
- full-width visual panels alternate with sparse text-led sections
- aggressive scale contrast
- high negative-space discipline

Width:
- primary visual panels should use nearly the full README width
- text content should remain narrower and visually quiet

Rhythm:
1. strong cover
2. quiet identity strip
3. large project
4. large project with changed composition
5. tighter project spread
6. compressed secondary work
7. oversized stack typography
8. sparse ending

Every major section must use a different composition while retaining the same typography, palette, grid, and spacing logic.

## Interaction / Links

GitHub README cannot behave like a custom webpage.

Therefore:
- project panels may be wrapped in repository links
- identity/contact links remain ordinary accessible Markdown/HTML links
- do not fake hover states
- do not add UI controls that cannot actually function

## Asset Strategy

Hero:
- animated SVG if GitHub rendering proves smooth and reliable
- static SVG fallback state is complete on its own

Project spreads:
- static SVG or PNG, chosen per composition
- use real project imagery rather than generic stock or generated “tech” decoration
- display typography may be outlined inside SVG for consistency

Do not use one giant full-README image. The page must remain:
- linkable
- reasonably accessible
- easy to update
- performant

## User-Eye Review Gates

Before shipping, inspect the README at actual GitHub width and ask:

1. Does the hero read as AHMAD immediately before the motion is noticed?
2. Does the accent guide the eye rather than dominate it?
3. Is there an obvious visual hierarchy within the first two seconds?
4. Can each project be identified without reading a paragraph?
5. Does every project composition feel intentionally different?
6. Is there enough negative space to recover between dense sections?
7. Does any section resemble a GitHub README template?
8. Does any element exist only because it “looks techy”?
9. Would the static version still look designed?
10. Does motion remain smooth on a normal desktop browser at GitHub scale?

Any “no” to 1–6 or “yes” to 7–8 blocks release.

## Explicitly Rejected

Do not reintroduce:
- The Loom
- procedural maze / cellular systems
- animated GIF hero as primary delivery
- fake HUDs
- particles
- random geometric wallpaper
- neon/cyberpunk styling
- badge walls
- GitHub stats widgets
- generic “builder / creator / dreamer” copy
- “simple rules → complex systems” slogans
- giant amounts of explanatory text

## Success Definition

The finished profile should feel like an authored design object that happens to live on GitHub.

It should communicate:
- strong visual judgment
- real technical work
- range across graphics, AI, and software systems
- restraint

The design must be recognizable even without animation.
The animation must enhance the identity, not carry it.
