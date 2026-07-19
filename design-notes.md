# Design Notes

Running log of design thoughts, decisions, and ideas. Newest at bottom.

## 2026-07-19 — Initial concept

- **Bed size**: handles 4' x 8' sheet material
- **Tooling**: multi-tool — router, laser, drag knife, pen (plotter-style)
- **Frame**: welded steel tubing
- **Base frame ("truck")**: welded steel frame with lifting casters; supports the pivoting bed — not the tool carriage. Nothing fancy, just a mobile base + pivot support.
- **Bed orientation**: pivots — horizontal, vertical, and everywhere in between
- **Gantry**: dual rails along the 8' Y axis
- **Z axis travel**: 4–6"
- **Electronics**: TBD — Dave has a collection of electronics on hand already; controls/electronics design to be discussed later
- **X/Y drive**: belt drive — priority is precision over speed
- **Base frame footprint**: relatively small floor footprint
- **Bed pivot actuation**: manual at first, motorized actuator later
- **Materials to support**: wood, metal, composite, fabric, paper, vinyl
- **Additional tooling (sensing)**: lidar, camera, 3D scanner

### Q&A round 1

- **Tool changing**: likely multiple tools live on the carriage simultaneously (vs. one-at-a-time manual swap) — approach still unknown/open
- **Laser + other tools sharing the machine** (dust, fumes, reflections with router/metal work) — deferred, later problem
- **Bed pivot mechanics**: pivots on a center axis (not an edge trunnion). Material held to bed via clamps, adhesives, or plastic/blind nails (method depends on material/job)
- **"Truck" clarified**: it's the mobile base frame with lifting casters + pivot supports for the bed — not a carriage for the router. Nothing fancy — base + pivot support only
- **Precision target**: unknown/TBD so far
- **Power**: 220V, 60A, single phase available
- **Footprint target**: as small as reasonably possible — rough target ~4' x 3' floor space for the base

### Scope clarification

- Not designing around specific tools right now — the goal is a **versatile foundation/platform** for unknown future CNC tooling, not a tool-specific machine
- Precision goal: wants "high precision" capability, but no quantified target yet (no tolerance number in mind)
