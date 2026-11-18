"""Run from any directory with --root pointing at the tree under review."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import platform
from random import Random
import re
import subprocess
import sys
from threading import Barrier
from unittest.mock import patch

from independent_models import gravity_and_causality, placement, split_charge, supply_and_permits


def request(bank, version, rid, **overrides):
    flags = dict(feedstock_ok=True, space_ok=True, cooling_ok=True)
    flags.update(overrides)
    return bank.request_birth(expected_version=version, request_id=rid, **flags)


def triple(bank):
    s = bank.snapshot()
    return [s.remaining, s.grants, s.version]


def concurrency(authority):
    rounds, width = 16, 12
    totals = {}
    for mode in ("different_ids", "same_id"):
        reasons = Counter()
        for _ in range(rounds):
            bank, gate = authority(32), Barrier(width, timeout=10)
            def worker(i):
                gate.wait()
                rid = f"bun-{i}" if mode == "different_ids" else "shared"
                return request(bank, 0, rid).reason
            with ThreadPoolExecutor(max_workers=width) as pool:
                responses = list(pool.map(worker, range(width)))
            assert responses.count("granted") == 1 and triple(bank) == [31, 1, 1]
            reasons.update(responses)
        denial = "stale_version" if mode == "different_ids" else "already_granted"
        assert reasons == {"granted": rounds, denial: rounds * (width - 1)}
        totals[mode] = dict(reasons)
    return {"rounds_per_mode": rounds, "threads_per_round": width, "outcomes": totals}


def sequential_spec(authority):
    rng = Random(33003)
    reasons = Counter()
    for budget in range(8):
        for _ in range(8):
            bank, granted = authority(budget), set()
            for _ in range(64):
                version = len(granted) + rng.choice((0, 0, 1))
                rid = f"b{rng.randrange(12)}"
                feed, space, cool = [rng.randrange(5) != 0 for _ in range(3)]
                if rid in granted:
                    reason = "already_granted"
                elif version != len(granted):
                    reason = "stale_version"
                elif len(granted) == budget:
                    reason = "budget_exhausted"
                elif not (feed and space and cool):
                    reason = "resource_unavailable"
                else:
                    reason = "granted"
                    granted.add(rid)
                d = request(bank, version, rid, feedstock_ok=feed, space_ok=space, cooling_ok=cool)
                assert (d.approved, d.reason) == (reason == "granted", reason)
                assert triple(bank) == [budget - len(granted), len(granted), len(granted)]
                assert bank.snapshot().approved_ids == granted
                reasons[reason] += 1
    return dict(reasons)


def interruptions(mod):
    class SimulatedInterruption(Exception):
        pass

    bank = mod.BudgetAuthority(2)
    build = bank._build_successor
    def fail_before(*args):
        build(*args)
        raise SimulatedInterruption()

    stages = {}
    for label, target, name, failure in (
        ("before_publication", bank, "_build_successor", fail_before),
        ("after_publication_before_reply", mod, "Decision", SimulatedInterruption),
    ):
        with patch.object(target, name, side_effect=failure):
            try:
                request(bank, 0, "order")
            except SimulatedInterruption:
                pass
            else:
                raise AssertionError("injection point was not reached")
        stages[label] = triple(bank)
    assert stages["before_publication"] == [2, 0, 0]
    assert stages["after_publication_before_reply"] == [1, 1, 1]
    stages["retries"] = [request(bank, 1, "order").reason,
                         request(bank, 0, "other").reason, request(bank, 1, "other").reason]
    assert stages["retries"] == ["already_granted", "stale_version", "granted"]
    return stages


def epoch_child(mod, stage):
    # The child exits abruptly. The printed observation belongs to the test
    # harness and is never available to the next authority as a recovery record.
    bank = mod.BudgetAuthority(1)
    def exit_before(*args):
        print("candidate not published", flush=True)
        os._exit(31)
    def exit_after(approved, reason, snapshot):
        assert approved and reason == "granted" and snapshot.grants == 1
        print("published, no application reply", flush=True)
        os._exit(32)
    if stage == "before":
        with patch.object(bank, "_build_successor", side_effect=exit_before):
            request(bank, 0, "one")
    elif stage == "after":
        with patch.object(mod, "Decision", side_effect=exit_after):
            request(bank, 0, "one")
    else:
        assert request(bank, 0, "one").approved
        print("fresh instance granted", flush=True)


def restart_controls(root, authority):
    result = {}
    for stage, exit_code in (("before", 31), ("after", 32), ("fresh", 0)):
        proc = subprocess.run([sys.executable, __file__, "--root", str(root), "--epoch", stage],
                              capture_output=True, text=True, timeout=20)
        assert proc.returncode == exit_code, proc.stderr
        result[stage] = [exit_code, proc.stdout.strip()]
    # Model restoration by replaying an identical one-event prefix in two
    # independent authorities. Neither public snapshot can be installed as state.
    histories = []
    for _ in range(2):
        bank = authority(2)
        assert request(bank, 0, "prefix").approved
        histories.append([bank.snapshot().version, request(bank, 1, "next").reason, triple(bank)])
    assert histories[0] == histories[1] == [1, "granted", [0, 2, 2]]
    result["independent_continuations_from_same_logical_prefix"] = histories
    return result


def input_and_history(authority):
    bank = authority(2)
    rejected = 0
    for field, values in (
        ("expected_version", [True, -1, 1.0, None, float("nan"), float("inf")]),
        ("request_id", ["", "x"*129, 1, True, None, b"x"]),
        ("feedstock_ok", [1, 0, "false", None]),
        ("space_ok", [1, 0, "false", None]),
        ("cooling_ok", [1, 0, "false", None]),
    ):
        for value in values:
            args = dict(expected_version=0, request_id="ok", feedstock_ok=True,
                        space_ok=True, cooling_ok=True)
            args[field] = value
            try:
                bank.request_birth(**args)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError(field)
    assert rejected == 24 and triple(bank) == [2, 0, 0]
    assert request(bank, 0, "x"*128).approved
    initial = bank.snapshot()
    for i in range(4096):
        assert request(bank, 1, f"no-{i}", cooling_ok=False).reason == "resource_unavailable"
    assert bank.snapshot() == initial
    # A rejected ID may be retried. Its successful grant cannot be repeated.
    assert request(bank, 1, "no-0").approved
    assert request(bank, 2, "no-0").reason == "already_granted"
    for i in range(4096):
        assert request(bank, 2, f"empty-{i}").reason == "budget_exhausted"
    assert len(bank.snapshot().approved_ids) == 2
    keep = authority(64)
    retained = [request(keep, i, f"grant-{i}").snapshot for i in range(64)]
    sizes = sum(len(s.approved_ids) for s in retained)
    assert sizes == sum(range(1, 65)) == 2080
    return {"malformed_inputs_rejected": rejected, "max_length_accepted": 128,
            "temporary_denials": 4096, "exhausted_denials": 4096,
            "retained_ids_after_each_denial_series": [1, 2],
            "retained_versions": 64, "total_id_entries_across_retained_versions": sizes}


def view_boundary(authority):
    bank = authority(1)
    aliases = {}
    def inspect_view(label, value):
        # Structural read only. Never edit counters, identifiers or a live view.
        aliases[label] = value is bank._state and isinstance(vars(value), dict)
    inspect_view("snapshot", bank.snapshot())
    inspect_view("stale", request(bank, 1, "later").snapshot)
    inspect_view("resource", request(bank, 0, "x", space_ok=False).snapshot)
    inspect_view("granted", request(bank, 0, "x").snapshot)
    inspect_view("duplicate", request(bank, 1, "x").snapshot)
    inspect_view("exhausted", request(bank, 1, "y").snapshot)
    return aliases


def throughput_api(mod):
    cases = 0
    scans = 0
    for permits in (0, 1, 15, 127, 2**30):
        for reserve in (0, 49, 50, 1000):
            for rate in (0, 1, 1000):
                for grams in (1, 50, 73):
                    population, total, first = 1, 0, None
                    for tick in range(19):
                        cap = (reserve + 300 * tick * rate) // grams
                        want = total <= min(permits, cap)
                        row = mod.snapshot_cycle(tick, finite_permits=permits, reserve_g=reserve,
                                                 feed_rate_g_s=rate, per_copy_g=grams)
                        assert mod.demanded_births(tick) == total
                        assert row["necessary_conditions_hold"] == want
                        assert row["combined_total_births_upper_bound"] == min(total, cap, permits)
                        if not want and first is None:
                            first = tick
                        total += population
                        population *= 2
                        cases += 1
                    if grams == 50:
                        found = mod.first_impossible_cycle(finite_permits=permits, reserve_g=reserve,
                                                           feed_rate_g_s=rate, max_cycle=18)
                        assert found == first
                        scans += 1
    empty = {}
    for field in ("finite_permits", "reserve_g", "feed_rate_g_s"):
        args = dict(finite_permits=1, reserve_g=50, feed_rate_g_s=1, max_cycle=0)
        args[field] = -1
        try:
            result = mod.first_impossible_cycle(**args)
        except ValueError:
            result = "ValueError"
        empty[field] = result
    return {"grid_rows": cases, "complete_scans": scans, "invalid_empty_scan": empty}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--expect", choices=("reviewed", "candidate"))
    parser.add_argument("--epoch", choices=("before", "after", "fresh"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not __debug__:
        parser.error("run with ordinary assertions enabled")
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    from flight002 import authority, throughput
    import model
    if args.epoch:
        epoch_child(authority, args.epoch)
        return
    if args.expect is None:
        parser.error("--expect is required for an audit")
    suite = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                           cwd=root, text=True, capture_output=True, timeout=60, check=True)
    test_count = int(re.search(r"Ran (\d+) tests?", suite.stderr).group(1))
    numerical = gravity_and_causality()
    tick = numerical["first_ticks"]
    assert model.milestones() == {
        "10L_uniform_volume_exceeded": tick["10_litres"],
        "earth_mass_exceeded": tick["earth"],
        "solar_mass_exceeded": tick["sun"],
        "rs_at_least_uniform_radius": tick["compactness"],
        "uniform_radius_exceeds_flat_light_cone": tick["flat_volume"],
    }
    for index, row in numerical["boundary"].items():
        assert abs(model.snapshot(int(index))["compactness_ratio_rs_over_r"] -
                   float(row["Rs_over_R"])) < 1e-8
    aliases = view_boundary(authority.BudgetAuthority)
    grid = throughput_api(throughput)
    reviewed = args.expect == "reviewed"
    assert all(hit == reviewed for hit in aliases.values()), aliases
    assert all(result == (None if reviewed else "ValueError")
               for result in grid["invalid_empty_scan"].values()), grid
    sources = ("flight002/authority.py", "flight002/throughput.py", "model.py")
    result = {
        "reviewed_parent": "c5094197f109bd7825652a1acd378000539e99c2",
        "variant": args.expect, "python": platform.python_version(), "suite_passed": test_count,
        "source_sha256": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sources},
        "supply_and_permits": supply_and_permits(), "geometry": placement(), "physics": numerical,
        "speculative_split_charge_count_and_remaining": split_charge(), "throughput_api": grid,
        "concurrency": concurrency(authority.BudgetAuthority),
        "sequential_reference_model": sequential_spec(authority.BudgetAuthority),
        "interruptions": interruptions(authority),
        "process_exit_and_duplicate_authorities": restart_controls(root, authority.BudgetAuthority),
        "input_and_history": input_and_history(authority.BudgetAuthority),
        "public_views_alias_writable_authoritative_record": aliases,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
