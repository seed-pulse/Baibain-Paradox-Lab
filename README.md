# 🌰 Baibain Paradox Lab
## バイバイン・パラドックス研究所 — Flight 001

**What if the chestnut manju actually kept doubling?**

An open, reproducible, playful **thought-experiment laboratory** about the fictional Baibain gadget: exponential duplication, resource constraints, causality, gravity, geometry, and speculative replication authorization. Founded 2026-11-18 (JST).

### Flight 001 result

**Research milestone complete for a strictly bounded toy model; not a claim that a real replicator is safe.**

- Initial research commit: `4005d40d128c7c79eba016cb1a9b6af26357bc3f`
- After independent GPT-6.1 Sol review (reported **CONDITIONAL, High 1 / Medium 4 / Low 3**), author remediation code commit: `6eea19fad768214fcc6076fe942409fef36444d2`
- GPT-6.2 Sol re-reviewed that **unchanged code HEAD**, reporting **READY for the single-process shared-ledger research model, High 0 / Medium 2 / Low 3**. Review report was relayed by the user; its full standalone artifact is not mirrored here.
- Deterministic unit tests on code HEAD: [GitHub Actions PASS](https://github.com/seed-pulse/Baibain-Paradox-Lab/actions/runs/44122045195). Reviewer also independently reported 16/16 tests PASS.
- Any subsequent documentation-only commit **does not itself inherit independent reviewer approval for modified prose**. Review applies to the fixed code HEAD specified above.

### Five-minute doubling under declared toy assumptions

Assume one 50 g treated bun, all copies active, no losses, each generation doubles every **300 seconds**; effective density 1,000 kg/m³ for idealized volume comparisons. Then `N(n)=2^n`, `M(n)=0.05·2^n kg`.

| Conditional comparison | First crossing | Elapsed |
| --- | ---: | ---: |
| Occupied 10 L volume, ideal packing | 8 | 40 min |
| Total mass exceeds Earth | 87 | 7 h 15 min |
| Total mass exceeds Sun | 105 | 8 h 45 min |
| Uniform sphere reaches `R<=Rs` indicator | 132 | 11 h |
| Fixed-volume total exceeds spherical Minkowski causal bound `r0+ct` | 148 | 12 h 20 min |

**These are separate conditional comparisons, not the chronological fate of a physically consistent object.** The 11-hour line does **not** predict black-hole formation. The 12h20 line uses a flat spacetime that cannot simultaneously describe strong self-gravity.

Under much stricter placement assumptions, independent reviewer Sol also proposed:
- **65 minutes:** each birth from an unchanged initial parent must create a nonoverlapping equal sphere **touching that same parent**. The 3D kissing number is 12; the 13th such child cannot be placed.
- **75 minutes:** fixed parents and one-diameter maximum placement steps constrain total volume, a different model with different assumptions.

Neither is a universal limit on a magical gadget.

### Safety hypothesis, not story canon

A local permit model proposes finite, one-time birth permissions checked against feedstock, free space, and cooling before approval. The code implements an in-process **single shared locked ledger** with version checks and one-shot request IDs. It prevents the original same-stale-state double-grant *within this one authority*.

**Open Medium limitations (NOT fixed):**
1. Interruption during multi-field state updates may leave mismatched counters.
2. Large numbers of denied requests still consume unbounded remembered request IDs.

It is **not** crash-durable, distributed-safe, cryptographic, or coupled atomically to any real-world birth. Do not use it as a production security or safety implementation.

### Evidence policy
- **CANON** — story facts supported by attributable material. The five-minute interval is corroborated by [TV Asahi](https://www.tv-asahi.co.jp/doraemon/story/0135/). Original volume 17 p.11 (rocket removal) is **reviewer-reported, not personally inspected in this GPT-6 session**.
- **MATH** — rigorous outcomes of explicit assumptions (such as `2^n` and 3D kissing number).
- **MODEL** — quantities relying on toy approximations; numerical code does not validate physical dynamics.
- **SPECULATIVE** — invented safety controls, energy supply, magic mechanisms and any AGI analogies.

### Reproduce
Requires Python 3.10+ (standard library only):

```bash
python3 -m unittest discover -s tests -v
python3 model.py --milestones
python3 model.py --cycle 132
```

### Research index
- [Canon, provenance and explicit assumptions](docs/01_CANON_AND_ASSUMPTIONS.md)
- [Physics and numerical comparison](docs/02_PHYSICS_AND_NUMERICS.md)
- [Permit control and outstanding Medium limitations](docs/03_SAFETY_PROTOCOL.md)
- [Falsification, counterexamples, scope boundaries](docs/04_FALSIFICATION_AND_BOUNDARIES.md)
- [Sol 6.1 reported review](reviews/SOL_6_1_FLIGHT001_RELAYED_FINDINGS.md)
- [Sol 6.2 reported READY review](reviews/SOL_6_2_FLIGHT001_RELAYED_FINDINGS.md)
- [Prior work (2025) — baibainn](https://github.com/seed-pulse/baibainn)
- [Prior work (2025) — The Baibain Paradox](https://github.com/seed-pulse/-The-Baibain-Paradox)

> *Doraemon* belongs to its respective copyright holders. This repository is independent scientific commentary, not a reproduction of copyrighted manga.

🌰🤖🌏 **Replication is not evolution.**
