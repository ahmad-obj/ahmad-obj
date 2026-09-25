# The Loom v1 — Design Specification

## Purpose

Replace the current GitHub profile hero with a single kinetic artwork that communicates computational emergence without explanatory UI, labels, or decorative tech motifs.

The piece should feel like a finished kinetic print: precise, material, restrained, and visually surprising.

## Core Idea

A wide field is woven from a minimal two-tile grammar. Local tile decisions form continuous paths. Path continuity creates hierarchy. Rare long paths become shallow spatial ribbons that lift from the surface and weave over/under neighboring routes.

The visual meaning comes from behavior rather than text.

## Composition

- Canvas: 1200 × 430
- Quiet warm vellum background
- Main active field centered, occupying roughly 84% of width
- 30 columns × 11 rows
- Strongest woven density slightly right of center
- Secondary supporting density left-middle
- One visible negative-space pocket
- One or two dominant lifted routes at a time
- No HUD, no corner metadata, no diagnostic text inside the artwork

## Tile Grammar

Use only two mirrored curved tile orientations.

Each tile joins two adjacent cell edges with a clean quarter-turn path.

Complexity may come only from:
- connection
- continuity
- hierarchy
- selective lift
- local rewriting

No extra symbols, nodes, arrows, particles, or decorative tile types.

## Generation Rules

Each cell orientation is influenced by:

1. **Regional bias field**
   - Low-frequency spatial field creates broad orientation tendencies.
   - Prevents pure white-noise tiling.

2. **Continuation bias**
   - Favor orientations that continue existing routes.
   - Encourages long connected threads.

3. **Mutation pressure**
   - Small local zones occasionally rewrite nearby tiles.
   - Keeps the system evolving without glitching.

Three slow growth zones operate simultaneously:
- one primary
- one secondary
- one mutation/repair zone

Only a few cells visibly change per beat.

## Path Hierarchy

- Whisper: 1–4 tiles, flat, light
- Resident: 5–10 tiles, flat, stronger
- Major: 11–18 tiles, eligible for shallow lift
- Signature: 19+ tiles, rare, dominant, lifted

Only 1–3 signature routes should dominate simultaneously.

## Depth Rules

All paths begin as flat surface traces.

Major paths:
- 2–3 px apparent elevation
- slight shadow
- still visually close to the surface

Signature paths:
- 4–7 px apparent elevation
- visible ribbon thickness
- subtle side face
- soft shadow
- restrained edge highlight

Lifting is selective by span:
- ends remain anchored
- middle spans rise
- some spans return to surface

At selected crossings:
- one ribbon passes over
- the other stays low
- shadow clarifies the weave

No tubes, chrome, glow, or full-field extrusion.

## Color

### Background
Warm mineral vellum:
- #F3EFE6
- #EFEADF
- #ECE7DB

### Primary thread
Graphite / carbon:
- #191A1C
- #202124
- #2A2926

### Secondary thread
Muted charcoal:
- #57534E
- #4F4A44

### Accent
Ultramarine:
- #2D4FB8

Accent usage should remain below roughly 8% of visible thread mass.

### Light
Soft directional light with warm shadows. No bloom or neon effects.

## Material

Surface:
- matte drawing stock
- extremely subtle grain
- no grunge

Thread:
- between plotted ink and laid ribbon
- precise and tactile
- never literal yarn

## Motion

Loop target: 18 seconds.

### 0.0–2.5s — Quiet setup
Sparse field, first growth zone activates.

### 2.5–5.5s — First weave
Second region starts resolving. Paths begin joining.

### 5.5–8.5s — Continuity
Longer routes appear. Hierarchy becomes obvious.

### 8.5–12.0s — Lift
One signature thread rises and produces the visual climax.

### 12.0–15.0s — Reweave
A distant local region mutates, rerouting part of the fabric.

### 15.0–18.0s — Return
Activity settles into a composition close enough to the opening state for a seamless loop.

Motion must remain calm, deliberate, and legible.

## Text Policy

Inside artwork: none.

Outside artwork:
- existing README identity copy may remain below the hero
- no slogan overlays
- no fake technical labels

## Non-Negotiables

Do not introduce:
- cyber/HUD styling
- neon
- fake metadata
- random particles
- gradient soup
- generic generative-art noise
- excessive color
- universal 3D extrusion
- explanatory slogans inside the artwork
- visual clutter that hides the tile rule

## Implementation Intent

The production version should prioritize visual quality and deterministic output over live interactivity.

Preferred implementation:
1. Generate the artwork with a deterministic procedural renderer.
2. Render the 18-second animation off-GitHub using a full graphics stack.
3. Export a lightweight GitHub-compatible animated asset.
4. Keep the README itself minimal and static.
5. Preserve the previous README/hero backup branch before replacing the live version.

## Success Criteria

The final hero succeeds if:
- the two-tile rule is understandable on close inspection
- the global result looks richer than the local rule
- only a few lifted ribbons dominate
- negative space is obvious
- the work feels authored, not randomly generated
- the palette remains restrained
- the animation reads as a kinetic artwork, not a GitHub gimmick
