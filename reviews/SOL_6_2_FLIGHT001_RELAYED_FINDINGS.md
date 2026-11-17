# GPT-6.2 Sol — Flight 001 re-review, user-relayed report

## Provenance
A user pasted a summary of GPT-6.2 Sol's independent review on 2026-11-18 (JST). The purported standalone file `Baibain_Flight001_Sol62_Rereview.md` was **not provided verbatim** to this session and is **not represented as if it were an inspected, signed artifact**.

- **Reviewed fixed code HEAD:** `6eea19fad768214fcc6076fe942409fef36444d2`
- **Verdict:** READY **only for a single-process, shared-ledger research demonstration**; High 0 / Medium 2 / Low 3
- **Reproduction reported by reviewer:** former double-grant repaired; 128 rounds of 16+16 simultaneous requests, one grant per group; replay of previously used request ID denied; 16/16 tests pass.
- **Physics reported:** five milestone crossings independently confirmed, flat `r0+ct` occupancy crossing at 12h20; an outside-launched light ray meeting inside-horizon infaller at approx 206.06 seconds in a fixed Schwarzschild example.
- **New countermodel reported:** 3D kissing number 12 implies 13th *contact-only offspring of an unmoving original parent* cannot fit, i.e. cycle 13 / 65 minutes, only with this added placement constraint.

## Remaining findings
| Severity | Summary | Disposition for Flight 001 |
| --- | --- | --- |
| Medium 1 | Mid-transition interruption can leave count/budget inconsistent; future calls stop | Open; explicitly out-of-scope for nondurable single-process research |
| Medium 2 | Rejected attempts still populate unbounded request-ID set (4,096 rejections → 4,096 remembered IDs) | Open; resource exhaustion in long-lived service |
| Low 1 | Extreme finite inputs in numerical helpers | Open with toy numeric-range limitations |
| Low 2 | Summary/table terms drift from detailed `r0+ct`, horizon-direction, attribution | Documentation alignment in finalization commit |
| Low 3 | Newtonian pressure printed at strong gravity where the formula is invalid | Warn prominently in docs; code unchanged |

## Author action
The code and tests verified by Sol at `6eea19f` are **not modified** in the final documentation update. Any doc edits after that HEAD have not themselves been independently re-reviewed. This distinction is intentional.

**Verdict for scope**: Flight 001 is research-complete with **known open limitations**, not production-ready. Future work may add crash-safe atomic state updates and bounded admission/idempotency storage under new review.
