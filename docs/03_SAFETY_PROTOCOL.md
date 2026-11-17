# Flight 001 — Hypothetical Safety Mechanism: finite, conserved birth permits

Label: **SPECULATIVE engineering thought experiment**, NOT a feature shown in the story.

## Core invariant
Introduce B nonforgeable, unique birth permits minted before operation. Each successful creation spends exactly one permit, and **no permit is duplicated**, regardless of how many descendants or fragments exist. If the total authorized birth count is B, then cumulative births <= B and total ever created objects <= B + 1 (one initial object). For B=15, no more than 16 full objects / 800 g under 50 g per object.

This is an *accounting invariant*, not proof of physically realized finite resources. The children may still be hazardous to the environment. The fiction's household overflow suggests that a 15-permit cap is incompatible with the depicted episode; 15 is just a small demonstration budget.

## Order of operations — fail closed
1. Verify object identity and authentic permit; reject replay/double spending.
2. Reserve sufficient raw material/energy to create the new 50 g object; account separately for thermal handling.
3. Reserve an unoccupied destination of adequate volume; prevent collision with prior objects.
4. Atomically mark one permit **spent** in the authoritative ledger (or physically consume a nonduplicable token).
5. Only after the above succeed, commit a new object. On ambiguity/failure, create nothing; reconcile before retry.

The code in model.py implements ONLY the scalar, atomic ledger invariant and boolean resource gates. It does **not** implement physical conservation, cryptographic tokens, consensus, or reliable distributed transactions.

## Threat model
- Concurrent replication: two separated children spend the same permit (double-spend) unless enforcement is atomic/noncopyable.
- Fracture: inherited tag is copied into each fragment. A naive identity flag increases permissions.
- Replay: a power cycle restores an old snapshot with more unspent permits.
- Partition: stopping all children via one remote message is impossible in general if communication is blocked or delayed.
- Resource sensor spoofing: optimistic estimated feedstock/space/cooling must not become creation.
- Black-hole horizon: remote stop signal cannot be assumed to reach interior.

## No-free-lunch
An all-powerful gadget capable of inventing arbitrary mass, making duplicates at spacelike separation, or cloning permissions can trivially defeat our model. Safety requires *specified*, enforced limits and assumptions that are falsifiable. Calling this 'minimal' means fewer **logical primitives** than global surveillance, not that we proved future engineering can build it.

## Connection to Voyager research (ANALOGY only)
Consume authorized state just before mutation, preserve monotonic evidence, and never treat equality of the current world view as evidence that history has not changed (ABA). These are software safety analogies; they do not establish physical replication technology.
