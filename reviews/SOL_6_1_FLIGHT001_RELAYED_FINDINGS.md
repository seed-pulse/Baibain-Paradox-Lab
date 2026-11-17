# Flight 001 — Sol independent review, user-relayed summary (provenance)

**Review target:** 4005d40d128c7c79eba016cb1a9b6af26357bc3f
**Verdict reported:** CONDITIONAL; High 1 / Medium 4 / Low 3.
**Provenance:** User pasted the GPT-6.1 Sol result into ChatGPT. This file is a **faithful condensed relay**, NOT a newly executed Sol review of the fixes and not a direct transcription of the separate \`Baibain_Flight001_Sol_Review.md\` artifact, which was not present in this repository at author time.

High 1: Pure \`try_authorized_birth(PermitState(1))\` run twice from same state can grant twice. Sequential consistency proven in review over 264 cases is not a global guarantee. Fix requires authority, freshness and one-shot grant.

Medium 4: (1) non-strict NaN/infinite permit counts and string \`"false"\` resource flags; (2) nonzero initial radius in causal-ball argument; (3) gravity-vs-flat-light-cone model compatibility; (4) incoming vs outgoing signals crossing horizon.

Low 3: (1) original volume 17 p.11 attribution for rocket removal (reviewer-reported, not checked here); (2) correct “inner horizon” heading: Schwarzschild has an event horizon; (3) guard extreme finite inputs in \`snapshot\`.

Additional countermodels: 75-min parent-neighbor placement obstruction at n=15; external light meets infaller inside horizon at a sample 206s; phase 270s at crossing can fit 3 scheduled creation events within the idealized ~657s; fragmented bun can retain independent controller state; hypothetical shortcut spacetime still faces source throughput constraints.

**Status:** Remediation proposed in subsequent GPT-6 commit. New HEAD MUST be independently reviewed by Sol before declaring conditional findings closed.
