# Flight 001 — Adversarial counterexamples and test design

Purpose: separate a theorem about a declared model from a prediction about the fictional gadget.

| Claim | Counterexample / challenge | What observation would resolve it? |
|---|---|---|
| Destruction stops duplication | Each fragment keeps a replication tag and rebuilds a full 50 g bun; 10 fragments may yield 10 new objects next cycle. | Define whether tags can split, whether whole-object integrity matters, and whether the tag consumes permits. |
| Cooling/combustion prevents growth | A tag survives chemical breakdown; energy/heat is removed elsewhere. | Establish coupling between composition/temperature and replication trigger. |
| Total count must double | Only one active mother produces one inert copy every five minutes; cumulative total grows linearly. | Establish whether all children retain the effect. |
| Apparent sameness means no state change | ABA: counter/permit is spent, state reset, same visible object. | Monotonic historical nonce and consumed token checks. |
| A global STOP will work | A remote copy is outside signal reach or inside a black-hole horizon. | Local finite permits and fail-closed triggers; test lost communications. |
| 11 hours is exact black hole formation | Expanding nonuniform clouds, collapsing regions, compactness early, heat, stress-energy changes. | Self-consistent time-dependent GR simulation with explicit mass source. |
| 12h20 is 'filling the universe' | FRW spacetime, relocation by wormholes, space creation, overlaps, shrinking objects. | State spacetime, locality and excluded mechanisms. |
| The fictional tool must respect ordinary conservation | An assumed external reservoir, unknown field, or explicit exotic physics can change accounting. | Provide operational source-and-sink theory or label unsupported. |
| Finite permits automatically equal safe | A permitted birth can still crush a person or release dangerous heat. | Define safety property independent of numerical cap. |

## Three independent tests
**T1 — arithmetic:** exact counts (12, 24 cycles), mass and first-cycle threshold regression tests. A failure invalidates reported table values.

**T2 — local safety proof:** exercise the single shared in-memory ledger for 20 distinct authorized requests with B=15, then stale-version replay, request-ID replay and two concurrent same-version calls. This proves only the locked single-process invariant; a distributed, copied or persisted ledger is outside scope.

**T3 — critical external review:** ask reviewer to construct a fully consistent world in which thermal destruction occurs but a tag survives, and one in which heat never destroys tags. Also challenge gravity, causal bound, source interpretation, and any claimed novelty.

## Known limitations
No real-world reproduction; no thermal transport solver; no dynamics; no real EOS; no Einstein-field-equation numerical solution; no cosmic-scale FRW calculation; no magic's internal specification; no actual Sol model invocation by this repository. Independent reviewer must sign off separately before claiming review complete.


## Additional post-Sol reviewer counterexamples
- **Same-state double grant (High):** Pure transition functions are only proposals; they must not be used as production authorizers. A caller may reuse an old snapshot. Addressed by serializing one shared authority and rejecting stale versions; not addressed across isolated authorities.
- **Initial radius:** A spatially extended initial bun needs `r0+ct`, not `ct`; numerical crossing remains n=148 for default parameters.
- **Ingoing horizon communications:** An external signal can enter a future event horizon and reach an interior infaller. “Outside cannot stop inside” was too strong; communication back to infinity remains impossible from within.
- **Local birth-placement limit:** One-diameter child-center jumps with fixed parents make a much earlier 75-minute volume obstruction.
- **Nonphysical inputs:** non-integer budgets, string values such as `"false"`, and derived nonfinite numbers must be rejected, not silently accepted.

## Sol 6.2 final re-review follow-up (user-relayed, conditional scope)
- **READY, High 0 / Medium 2 / Low 3** on the *unchanged* 6eea19f code HEAD, within the declared in-process shared-ledger research model.
- A reproduction of the original double-authorization now grants only once. Reviewer reported 128 rounds of two groups of 16 concurrent requests: exactly one approval per group, and replays denied. Existing 16 tests passed.
- Remaining medium: nontransactional interruption of a multi-field update; unbounded attempted-ID accumulation on denials. Explicitly deferred to future persistence / resource-safety work.
- Remaining low: extreme numerical helper boundaries, overview vs body label consistency, and Newtonian pressure output outside its regime. The published prose now aligns labels; numerical helper is still bounded toy code.
- **New geometry counterexample:** 12-sphere kissing-number limit around a fixed original means an added *contact-only, no-motion* assumption blocks the 13th child of that original at **65 minutes** (see docs/02 §10). The broader one-diameter-placement bound is **75 minutes**, a different assumption set.
- Original manga vol.17 p.11 rocket-removal pointer remains reviewer-reported; not personally inspected in this GPT-6 work session.
- Not an all-environments AGI safety assurance; no spacetime or conservation physics has been validated by running this toy code.
