# Flight 002 — Replication rights, causal limits and resource throughput 🌰

## Status and provenance
GPT-6 authored an independent next-step toy model from the merged Flight 001 code. **All numerical examples below are conditional on explicitly chosen values.** This Flight does not simulate material generation, phase transitions, relativistic gravity or physical actuator commit.

Flight 001 remains unchanged; this Flight's authority model lives in \`flight002/\`. It is a separate prototype to probe Sol 6.2's remaining Medium issues, not a retroactive claim that the Flight 001 implementation was production-ready.

## 1. A necessary contradiction between exact indefinite doubling and finite permission

Suppose one bun exists at n=0; each original and descendent remains active, and every active one makes exactly one new copy each cycle. Then \`N(n)=2^n\` and **cumulative births** are \`B_required(n)=2^n-1\`.

A finite bank of \`B\` unique, noncloneable creation permits is enough for at most \`B\` successful births. To reproduce fully unrestricted doubling through n complete cycles, \`B >= 2^n-1\` is **necessary**. Thus no finite \`B\` can guarantee such doubling at every future cycle.

Examples:
- \`B=15\` permits unrestricted doubling through \`n=4\` (20 min, 16 buns), **not** through \`n=5\`.
- \`B=4095\` permits through \`n=12\` (1 h, 4,096 buns), not \`n=13\`.

**Interpretation:** A finite birth permit is a coherent *hypothetical emergency brake*, but necessarily changes the behavior of a system stipulated to double forever. No such device behavior is asserted to be canonical.

## 2. Resource throughput is another independent necessary bound

Assume each new 50-g bun requires 50 g externally supplied feedstock, an initially available reserve \`W\` grams, and a constant delivery capacity \`q\` grams/second for time \`t\`.

Then at time t, **cumulative** successful births cannot exceed
\`floor((W + q*t)/50)\`.

This bound does not imply that a schedule exists: resource arrival, spatial placement, competition among children and control latency must still be checked **at each birth**.

For **W=0** and **q=1000 g/s (1 kg/s)**, with **no permit restriction**, unrestricted doubling requires:
- n=16 (80 min): 65,535 births; 3,276,750 g total feedstock, within 4,800,000 g supplied by 80 min.
- n=17 (85 min): 131,071 births; 6,553,550 g demanded, exceeding 5,100,000 g supplied by 85 min.

Therefore, n=17 (85 min) is the **first violated cumulative supply bound**, under these input values. This is not a universal 85-minute stop; it just proves a 1 kg/s reservoir-free source is insufficient for that ideal branching schedule by then.

An external power source that creates matter from energy must still supply at least its rest-energy equivalent; 50 g corresponds to roughly \`4.4938e15 J\`. This is **not** necessarily delivered as heat. Energy conversion, transport and conservation mechanisms are separate unknowns.

## 3. Work on the remaining two Medium findings

### M1 — Interrupt between field updates
Flight 001 updated \`remaining\`, \`births\`, and \`version\` as separate writes under a thread lock. Sol 6.2 demonstrated an exception or interruption leaving the ledger half updated.

Flight 002 constructs a complete **immutable** \`BudgetSnapshot\` candidate before changing its single authoritative reference. In one Python process while all calls use the same lock, a failure **during candidate construction** leaves previous state untouched. In this model the state switch is one in-memory assignment. A fault **after** publication can still leave the caller uncertain whether authorization succeeded; same request ID replay denies a second grant.

**No crash durability, physical commit coupling or distributed consensus is claimed.** A process restart, fork, corrupted memory or partial physical creation remains outside the proof.

### M2 — Denied-ID memory growth
Flight 001 stored the IDs of *denied* attempts, so an adversary could grow memory with many unique denials even after the budget reached zero.

Flight 002 records **successful** grant IDs only. The set size can never exceed the initial finite budget. A denied request ID is not retained: if resources later become available and the client submits a matching current version, an earlier denied ID may be approved. This changes *denial idempotency*, deliberately; **grant single-spend** is the invariant being claimed.

Performance caveat: the entire frozenset is copied per grant, which is expensive for large B. No wall-clock or memory benchmark was carried out; this prototype is a correctness study. Untrusted request floods still require rate limits and admission control in any actual service.

## 4. Falsification: where the proof fails
- Two independent ledgers with the same initial B can each authorize B births. Single process and one authority are essential.
- Cloning a permit, rolling back a snapshot after restart, or treating an arbitrary copied state as authority bypasses the one-ledger budget.
- A successfully issued authorization is not the same as a completed physical birth; coupling requires a separately engineered, recoverable actuator/transaction protocol.
- A finite permit bank could fit what is shown in a finite scene and still fail to prove how the gadget behaves later.
- Unrestricted magic might move matter spacelike or construct additional space; flat Minkowski bounds cannot exclude those fictional mechanisms.
- Contact-only placement of same-size spheres yields a 65-minute bound only if each child of the original must stay touching that original and prior positions do not change. The 3D kissing number is 12, a mathematical result; it is not a universal limit on Baibain.

## 5. Astra Flight 003 target
Ask GPT-6.2 Astra to independently construct counterexamples rather than approve on faith. Primary attacks: (i) mid-commit interruption and request result ambiguity, (ii) replay after rollback/crash, (iii) denied-ID re-use semantics, (iv) exact n=17 throughput arithmetic and timing, (v) black-hole/causal/conservation premises in Flight 001, (vi) finite-permit incompatibility with indefinite exact doubling, and (vii) the scope and correct interpretation of the 65-minute kissing bound.

### Sources
- [TV Asahi synopsis for Baibain](https://www.tv-asahi.co.jp/doraemon/story/0135/) (five-minute interval)
- [MathWorld: Kissing Number](https://mathworld.wolfram.com/KissingNumber.html), 3D upper bound 12
- [Physical review of Baibain baseline](../docs/02_PHYSICS_AND_NUMERICS.md)
- [Flight 001 bounded safety-model limitations](../docs/03_SAFETY_PROTOCOL.md)

> Claim types: **CANON** for original published descriptions; **MATH** for exact integer formulas under assumptions; **MODEL** for geometry/resource comparisons; **SPECULATIVE** for permit hardware and safety mechanisms.
