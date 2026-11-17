# Flight 001 — Canon, assumptions, provenance

Status: **Source-checked synopsis + conditional toy assumptions**. 2026-11-18 JST.

## Canon / published fiction
- The treated thing doubles **every 5 minutes**. TV Asahi synopsis: https://www.tv-asahi.co.jp/doraemon/story/0135/
- The story concerns chestnut manju, a warning to eat the copies, and removal to space. Later synopsis credits volume 17: https://www.tv-asahi.co.jp/doraemon/story/0497/
- The 17th manga volume and precise depiction of consumed copies were reported in Sol's independently shared preliminary review; this Flight has **not itself inspected the copyrighted manga pages**.
- **Not established in canon here:** existence of material supply reservoir; how individual replication rights are tracked; whether fragments inherit the effect; whether any safeguard activates in space; whether all copies remain active.

## Fixed assumption set A (arithmetic)
A1. At time zero exactly one 50 g object is active.
A2. Exactly once every 300 seconds, all active objects duplicate into a pair of the same 50 g mass; all children stay active.
A3. No losses, cancellations, eating, mergers or finite resources. Total number after n cycles: 2^n. This is a counterfactual rule, **not a prediction**.
A4. Effective mass density rho = 1000 kg/m^3 when illustrating contiguous storage volumes.

## Optional assumptions (do NOT silently combine)
B. Packing: available volume 10 L; using density 1000 kg/m^3 and 100% packing efficiency is an intentionally optimistic occupancy bound.
C. Spherical proxy: all mass forms a uniform-density Euclidean sphere; Newtonian pressure proxy is only meaningful in its regime of validity. A growing real gravitating sphere cannot be treated as static.
D. Causality: all births take place by local processes within the future light cone of the initial treated object, in **flat** spacetime; copies require nonzero volume, and cannot overlap. This excludes magic spacelike creation / wormholes.
E. Black-hole probe: a **fixed** stationary nonrotating hole and test particle dropped from rest at infinity, not the self-gravitating Baibain cluster.
F. Safety-budget model: each authorized birth consumes one unique, noncopyable permission from a finite initial stock. Requires trusted enforcement; **invented design, not canon**.

## Historical error and preservation
Both 2025 README versions at https://github.com/seed-pulse/baibainn and https://github.com/seed-pulse/-The-Baibain-Paradox use a **5-second** interval. Their important question is preserved, but numerical chronology must be recomputed for **5 minutes**.

## Canon vs proof boundaries
Evidence that eaten copies cease being a problem does **not** uniquely identify whether digestion, identity, destruction or a state-change disables replication. Removing the objects to space does **not** demonstrate that they subsequently disappear, survive or fill the universe. No extrapolation is labeled canonical without a cited passage.

## Post-Sol clarifications — 2026-11-18
- The initial treated object is **not a point**. A flat-spacetime causality upper bound must include its initial spherical equivalent radius \`r0=(3 m0/(4πρ))^(1/3)\`, giving outer extent at most \`r0+ct\` under assumptions D. This does not affect first threshold n=148 with the default values.
- The manga's **rocket removal at original volume 17 p.11** was reported by the independently solicited Sol review, relayed by the user. The present GPT-6 session **has not personally inspected that page**; it is *reviewer-reported source*, not author-verification.
- Being made of matter does not automatically mean that the gadget's hypothetical remote power source or information-transfer mechanism obeys the same effective propagation constraints. The flat causal volume bound explicitly assumes locality and an ordinary Minkowski background.
