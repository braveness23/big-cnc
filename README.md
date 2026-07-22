# big-cnc

A large-format, multi-tool CNC platform — 4'×8' capacity, a pivoting bed, and a gantry built to carry more than one kind of head. Router, laser, drag knife, and pen are the obvious ones. A gantry-mounted LiDAR depth camera is the interesting one.

## Why the scanner is the headline, not an accessory

Most affordable 3D scanners are handheld or turntable rigs that track position by SLAM/feature-matching — accurate for shoebox-sized objects, and drifty past that. This machine's gantry always knows exactly where its head is, in X, Y, and Z, because that's the same precision it needs to cut a straight line. Point a depth camera at that same gantry and you get **metrology-grade positioning at a physical scale (4'×8') that consumer scanners don't reach.**

That reframes the whole machine: it isn't a CNC that happens to have a camera bolted on. It's a general-purpose precision motion platform, and cutting is just one of the things you can put on the end of it. Scanning is the other.

Concretely, that opens the door to:

- **Auto stock alignment** — scan the bed before a job, detect actual position/skew of the material, and correct the toolpath instead of jigging by hand.
- **Digitize-then-carve** — scan an irregular or damaged object, build a 3D model of it, and generate a toolpath to reproduce or repair it.
- **Pre/post-cut QA** — scan before and after a pass to verify the cut matches intent.
- **A DIY coordinate-measuring machine** — check a finished part's real dimensions against its CAD model, at a scale full CMMs are usually too expensive to cover.
- **Self-calibration** — use the scanner to check the machine's own gantry squareness, rail straightness, and bed flatness.
- **Uses that have nothing to do with cutting** — large-object 3D digitizing (furniture, parts, costume pieces), shop inventory scans, a vision front end for a future pick-and-place head.

None of this is built yet — see [`design-notes.md`](./design-notes.md) for the running log of what's decided versus still open. The candidate hardware under consideration is the [Onion Tau LiDAR Camera (TA-L10)](https://onion.io/), a USB-C depth + grayscale camera.

## What's actually decided (see design-notes.md for the full log)

- 4'×8' bed, pivoting on a center axis from horizontal to vertical
- Dual-rail gantry along the 8' Y axis, belt-driven X/Y (precision over speed), 4–6" Z travel
- Welded steel tube frame, mobile "truck" base with lifting casters
- Multi-tool carriage: router, laser, drag knife, pen — tool-changing approach still open
- 220V/60A single-phase power available; target base footprint ~4'×3'
- No quantified precision target yet — this is the key open variable driving structural sizing

## Status

Design journal stage — no code, no build, no hardware purchased yet. `design-notes.md` is the source of truth and is append-only: newest entries at the bottom, firm decisions marked plainly, open items marked TBD.
