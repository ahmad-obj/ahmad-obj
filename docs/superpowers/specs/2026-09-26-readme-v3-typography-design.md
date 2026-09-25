# README v3 — Text-First Typographic Redesign

## Goal

Keep the GitHub profile lightweight and native while making it feel authored, colorful, and visually distinctive through a small number of highly designed typographic moments.

The README should not look like:
- a portfolio webpage pasted into GitHub
- a wall of banners
- a badge collection
- a terminal-roleplay profile
- a generic developer template

It should feel like:
- a GitHub-native document
- interrupted by a few strong pieces of experimental typography
- easy to scan
- visually memorable without being image-heavy

## References and extracted principles

### Studio Feixen
References:
- https://www.studiofeixen.ch/about/
- https://www.studiofeixen.ch/poster-pen/
- https://www.studiofeixen.ch/wired-magazine/
- https://www.studiofeixen.ch/air-max-day/

Use:
- bold color and typography as the main visual material
- technically sophisticated but simple-looking results
- playful distortions that still preserve structure
- repetition, perspective, registration, and unexpected scale

Do not copy any composition directly.

### DIA
References:
- https://dia.tv/project/mailchimp/
- https://dia.tv/project/catk/
- https://dia.tv/project/nike-statement-house/

Use:
- typography as the motion/identity system
- motion and static design from the same visual rules
- flexible expressive systems that do not overpower the content

### Dinamo
Reference:
- https://dinamopipeline.com/

Use:
- variable/deformed type as the visual event
- lettering that feels like a designed object rather than a heading

## Existing assets to retain

Keep:
- `assets/editorial/00-cover.svg` — AHMAD hero
- `assets/motion/ascii-interference.gif`
- `assets/motion/selected-work.gif`

Do not add another large hero or project screenshot.

## New typographic moments

Add exactly three narrow static typographic artworks.

All are PNG, not SVG, to keep rendering predictable on GitHub.

Target width: 1000 px.
Target height: 100–150 px.
Target size: under 150 KB each.
No gradients unless they are part of raster shading in the 3D/extrusion treatment.
No photographic texture.

### CURRENT — chromatic registration

Text:
CURRENT

Treatment:
- oversized condensed sans
- 3–4 offset copies
- coral/orange, cobalt, acid yellow, off-white
- offsets resemble imperfect print registration but remain deliberate
- one layer slightly cropped at top/bottom
- no fake glitch noise
- high legibility

Content below in normal Markdown:
- Real-time graphics
- Agent orchestration
- Experimental interfaces

### ACADEMIC — perspective / extrusion

Text:
ACADEMIC

Treatment:
- one bold face extruded backward in perspective
- repeated outlines/solid shadows create depth
- off-white front face
- muted cobalt / coral depth layers
- diagonal perspective direction
- no chrome, bevel, or fake metallic 3D
- should feel like a printed typographic sculpture

Content below in normal Markdown:
- BS Computer Science — FAST-NUCES
- Dean's List ×2
- 1st position — BISE Gujranwala ICS

### INTERESTS — contour / repetition

Text:
INTERESTS

Treatment:
- 8–12 repeated outline contours of the same letters
- contours drift slightly in depth and curve
- front word remains sharp and readable
- orange/cobalt accents only on a few contours
- visual effect should feel like a vibrating topographic object rather than a glow

Content below in normal Markdown:
- Real-time graphics
- AI systems
- Developer tooling
- Interaction design
- Systems programming

## README composition

Order:

1. AHMAD hero
2. identity + links
3. CURRENT artwork
4. Current text
5. ACADEMIC artwork
6. Academic text
7. INTERESTS artwork
8. Interests text
9. ASCII interference strip
10. SELECTED WORK kinetic strip
11. three main project entries as native Markdown
12. Other work
13. Tools
14. minimal footer links

## Text design

### General rules

Use native Markdown and HTML for actual content.

Do not use:
- fake terminal prompts
- status labels
- pseudo-system metadata
- slogans
- emojis
- tables unless needed
- nested bullets unless needed
- badges

Project entries should remain compact:
- linked title
- one sentence
- stack line

### Section spacing

Use blank lines and `<br>` sparingly.
Each typographic artwork should have enough breathing room to read as a visual pause.
Do not place two visual assets directly adjacent except the ASCII strip and SELECTED WORK animation, which may remain close as a transition into projects.

## Color system

The README itself stays GitHub-native.

Typography art palette:
- Coral: #F04A2A
- Cobalt: #3157D5
- Acid yellow: #E7F04A
- Off-white: #F1EEE7
- Near-black: #0B0B0A
- Gray: #9B9993

Each artwork should use at most four colors.

## Motion

Keep only the existing two narrow animations.

No new large animated assets.

The three new typographic pieces are static so the profile does not become visually restless.

## Performance

Total new static typographic assets under 450 KB.
Existing two GIFs remain under 1 MB each.
No new image wider than 1000 px except the retained AHMAD hero.
No full-page image.

## User-eye review gates

Before shipping:
1. AHMAD remains the first and strongest visual.
2. CURRENT, ACADEMIC, and INTERESTS each have a clearly different visual treatment.
3. The README is still mostly native text by vertical area.
4. No section looks like a banner template.
5. The colored typography looks intentional, not like a glitch effect pack.
6. Project titles and descriptions remain easier to read than the artwork.
7. The academic achievements are visible without expanding anything.
8. The whole README still feels clean at GitHub's normal desktop width.
9. The profile remains usable if images fail to load.
10. No more than five visual assets appear before the project list.

## Success definition

A viewer should remember:
- the AHMAD mark
- the unusual typographic section treatments
- the main technical work
- the academic credibility

The profile should feel designed without feeling designed *around* GitHub.
