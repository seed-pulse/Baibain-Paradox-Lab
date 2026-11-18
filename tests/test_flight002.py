"""Independent repeatable regressions for Flight 002 toy assumptions."""
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from flight002.authority import BudgetAuthority
from flight002.throughput import (
    demanded_births, feedstock_birth_upper_bound, first_impossible_cycle,
    snapshot_cycle
)


def request(authority, version, rid, **overrides):
    flags = dict(feedstock_ok=True, space_ok=True, cooling_ok=True)
    flags.update(overrides)
    return authority.request_birth(
        expected_version=version, request_id=rid, **flags
    )


class ReusableAuthorityTests(unittest.TestCase):
    def test_same_snapshot_double_grant_is_prevented(self):
        a = BudgetAuthority(1)
        observed = a.snapshot()
        results = [request(a, observed.version, f"id-{i}") for i in range(2)]
        self.assertEqual([x.approved for x in results], [True, False])
        self.assertEqual(a.snapshot().remaining, 0)

    def test_threaded_races_16_rounds_16_threads(self):
        for round_no in range(16):
            a = BudgetAuthority(1)
            barrier = Barrier(16)
            def worker(i):
                barrier.wait(timeout=10)
                return request(a, 0, f"r{round_no}-{i}").approved
            with ThreadPoolExecutor(max_workers=16) as pool:
                result = list(pool.map(worker, range(16)))
            self.assertEqual(sum(result), 1, round_no)
            self.assertEqual(a.snapshot().grants, 1)

    def test_immutable_state_publication_fault(self):
        class FaultyAuthority(BudgetAuthority):
            def _build_successor(self, old, request_id):
                candidate = super()._build_successor(old, request_id)
                raise RuntimeError("fault before the single state publication")
        a = FaultyAuthority(2)
        before = a.snapshot()
        with self.assertRaises(RuntimeError):
            request(a, 0, "fault")
        self.assertEqual(a.snapshot(), before)

    def test_failed_requests_do_not_grow_approved_ids(self):
        a = BudgetAuthority(0)
        for i in range(4096):
            decision = request(a, 0, f"rejected-{i}")
            self.assertFalse(decision.approved)
        self.assertEqual(len(a.snapshot().approved_ids), 0)
        self.assertEqual(a.snapshot().grants, 0)

    def test_only_success_ids_retained_and_bounded_by_budget(self):
        a = BudgetAuthority(3)
        for i in range(3):
            self.assertTrue(request(a, a.snapshot().version, f"allow-{i}").approved)
        snap = a.snapshot()
        self.assertEqual((snap.grants, snap.remaining, len(snap.approved_ids)),
                         (3, 0, 3))
        self.assertFalse(request(a, snap.version, "allow-1").approved)

    def test_retry_denied_id_can_later_succeed(self):
        a = BudgetAuthority(1)
        initial = request(a, 0, "same", feedstock_ok=False)
        self.assertFalse(initial.approved)
        self.assertEqual(initial.reason, "resource_unavailable")
        next_try = request(a, 0, "same", feedstock_ok=True)
        self.assertTrue(next_try.approved)
        self.assertFalse(request(a, 1, "same").approved)

    def test_strict_boundary(self):
        for v in (True, 1.5, -1, "1", float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                BudgetAuthority(v)
        a = BudgetAuthority(1)
        for version in (False, 0.5, "0", float("nan"), -1):
            with self.assertRaises(ValueError):
                request(a, version, "id")
        for bad in ("false", 0, 1, None):
            with self.assertRaises(ValueError):
                request(a, 0, "id", space_ok=bad)
        self.assertEqual(a.snapshot().remaining, 1)


class ResourceBoundTests(unittest.TestCase):
    def test_doubling_births(self):
        self.assertEqual(demanded_births(0), 0)
        self.assertEqual(demanded_births(4), 15)
        self.assertEqual(demanded_births(12), 4095)

    def test_permit_cap_exact_cycle(self):
        self.assertTrue(snapshot_cycle(4, finite_permits=15, reserve_g=1000,
                                       feed_rate_g_s=0)["necessary_conditions_hold"])
        self.assertFalse(snapshot_cycle(5, finite_permits=15, reserve_g=1000,
                                        feed_rate_g_s=0)["necessary_conditions_hold"])
        self.assertEqual(first_impossible_cycle(finite_permits=15,
                         reserve_g=1000, feed_rate_g_s=0), 5)

    def test_feedstock_rate_one_kg_per_second(self):
        self.assertEqual(feedstock_birth_upper_bound(
            elapsed_s=300, reserve_g=0, feed_rate_g_s=1000), 6000)
        self.assertEqual(first_impossible_cycle(
            finite_permits=10**100, reserve_g=0, feed_rate_g_s=1000), 17)
        self.assertTrue(snapshot_cycle(16, finite_permits=10**100, reserve_g=0,
                                       feed_rate_g_s=1000)["necessary_conditions_hold"])
        self.assertFalse(snapshot_cycle(17, finite_permits=10**100, reserve_g=0,
                                        feed_rate_g_s=1000)["necessary_conditions_hold"])

    def test_denied_input(self):
        with self.assertRaises(ValueError):
            demanded_births(True)
        with self.assertRaises(ValueError):
            feedstock_birth_upper_bound(elapsed_s=0, reserve_g=-1,
                                        feed_rate_g_s=1)
        with self.assertRaises(ValueError):
            feedstock_birth_upper_bound(elapsed_s=0, reserve_g=0,
                                        feed_rate_g_s=1, per_copy_g=0)


if __name__ == "__main__":
    unittest.main()
