# big-cnc

A large-format, multi-tool CNC platform — 4'×8' capacity, a pivoting bed, and a gantry built to carry more than one kind of head. Router, laser, drag knife, and pen are the obvious ones. **A gantry-mounted multi-spectral vision system, driven by AI, is the one that turns this from a cutting machine into a machine that sees, thinks, and reacts.**

## Why the scanner is the headline, not an accessory

Most affordable 3D scanners are handheld or turntable rigs that track position by SLAM/feature-matching — accurate for shoebox-sized objects, and drifty past that. This machine's gantry always knows exactly where its head is, in X, Y, and Z, because that's the same precision it needs to cut a straight line. Point a depth camera at that same gantry and you get **metrology-grade positioning at a physical scale (4'×8') that consumer scanners don't reach.**

That reframes the whole machine: it isn't a CNC that happens to have a camera bolted on. It's a general-purpose precision motion platform, and cutting is just one of the things you can put on the end of it. Sensing is the other — and it doesn't stop at shape.

### Five channels, not one

Pair the LiDAR (depth + grayscale) with a **regular RGB camera**, a **near-IR camera**, and a **thermal camera**, and the scan head stops seeing just geometry — it sees shape, texture, color, hidden material properties, *and heat*. That's a sensing stack most hobbyist machines don't have any part of, let alone all five:

- **Shape (depth)** — precise 3D geometry of whatever's on the bed.
- **Texture (grayscale)** — surface detail, edges, markings.
- **Color (RGB)** — true color for finish/material identification and normal documentation photos.
- **Hidden detail (near-IR)** — sees material differences invisible to the eye, and cuts through smoke, dust, and laser/spark glare that would blind a regular camera.
- **Heat (thermal)** — material state and internal condition invisible to all four of the others.

### The brain on top: AI vision and control

Sensors that only log data are a photo album. The plan is to feed all five channels into a vision model and close the loop back into the machine controller — in real time, not "review the scan later":

- **See it, classify it** — identify material type, defects, and part ID automatically, instead of a human eyeballing a scan.
- **React to it** — auto-adjust feed rate or toolpath the moment a defect or stock shift is detected; auto-stop on a thermal safety anomaly, before smoke becomes fire.
- **Set the job up itself** — interpret a stock scan (boundaries, material, defects) and generate or adjust the toolpath without a human reviewing the data first.

This is the difference between "a CNC with a camera" and a machine that actually watches what it's doing.

### What that combination unlocks

- **Auto stock alignment** — scan the bed before a job, detect actual position/skew of the material, and correct the toolpath instead of jigging by hand.
- **Digitize-then-carve** — scan an irregular or damaged object, build a 3D model of it, and generate a toolpath to reproduce or repair it.
- **Pre/post-cut QA** — scan before and after a pass to verify the cut matches intent.
- **Thermal safety monitoring** — catch scorching/char risk during laser work, or bearing/spindle overheating during routing, before it's visible to the eye — a real-time early-warning layer during any cutting job.
- **Defect detection invisible to the eye** — thermal signatures can expose delamination, voids, or moisture pockets inside plywood and composites that depth/RGB alone would miss.
- **A DIY coordinate-measuring machine** — check a finished part's real dimensions against its CAD model, at a scale full CMMs are usually too expensive to cover.
- **Self-calibration** — use the scanner to check the machine's own gantry squareness, rail straightness, and bed flatness.
- **Uses that have nothing to do with cutting** — large-object 3D digitizing (furniture, parts, costume pieces), shop inventory scans, a vision front end for a future pick-and-place head.

None of this is built yet — see [`design-notes.md`](./design-notes.md) for the running log of what's decided versus still open. The candidate depth hardware is the [Onion Tau LiDAR Camera (TA-L10)](https://onion.io/), a USB-C depth + grayscale camera; RGB, near-IR, and thermal modules haven't been selected yet, and no vision model or compute platform has been chosen for the AI layer.

## What's actually decided (see design-notes.md for the full log)

- 4'×8' bed, pivoting on a center axis from horizontal to vertical
- Dual-rail gantry along the 8' Y axis, belt-driven X/Y (precision over speed), 4–6" Z travel
- Welded steel tube frame, mobile "truck" base with lifting casters
- Multi-tool carriage: router, laser, drag knife, pen — tool-changing approach still open
- 220V/60A single-phase power available; target base footprint ~4'×3'
- No quantified precision target yet — this is the key open variable driving structural sizing

## Status

Design journal stage — no code, no build, no hardware purchased yet. `design-notes.md` is the source of truth and is append-only: newest entries at the bottom, firm decisions marked plainly, open items marked TBD.
