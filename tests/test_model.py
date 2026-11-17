"""Flight 001 post-Sol regression tests; toy-policy scope only."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import unittest

from model import (
    C, M0_KG, SUN_KG, PermitLedger, creation_energy_j,
    fixed_schwarzschild_horizon_fall_s, milestones,
    parent_locality_capacity, snapshot,
)


class MathematicsTests(unittest.TestCase):
    def test_canon_five_minute_cycle(self):
        self.assertEqual(snapshot(12)["count"], 4096)
        self.assertEqual(snapshot(12)["minutes"], 60)
        self.assertEqual(snapshot(24)["count"], 16_777_216)

    def test_mass_at_one_hour(self):
        self.assertAlmostEqual(snapshot(12)["mass_kg"], 204.8)

    def test_ten_liter_threshold(self):
        self.assertLessEqual(snapshot(7)["volume_m3"], 0.010)
        self.assertGreater(snapshot(8)["volume_m3"], 0.010)

    def test_milestone_cycles(self):
        self.assertEqual(milestones(), {
            "10L_uniform_volume_exceeded": 8,
            "earth_mass_exceeded": 87,
            "solar_mass_exceeded": 105,
            "rs_at_least_uniform_radius": 132,
            "uniform_radius_exceeds_flat_light_cone": 148,
        })

    def test_crossings_are_first(self):
        self.assertLess(snapshot(131)["compactness_ratio_rs_over_r"], 1)
        self.assertGreaterEqual(snapshot(132)["compactness_ratio_rs_over_r"], 1)
        self.assertLess(snapshot(147)["uniform_radius_m"],
                        snapshot(147)["flat_causal_radius_m"])
        self.assertGreater(snapshot(148)["uniform_radius_m"],
                           snapshot(148)["flat_causal_radius_m"])

    def test_finite_initial_radius(self):
        s = snapshot(0)
        self.assertGreater(s["initial_radius_m"], 0.0)
        self.assertAlmostEqual(s["flat_causal_radius_m"],
                               s["initial_radius_m"])
        self.assertAlmostEqual(s["radius_over_flat_causal_radius"], 1.0)

    def test_locality_case(self):
        self.assertLessEqual(1 << 14, parent_locality_capacity(14))
        self.assertEqual(parent_locality_capacity(15), 29_791)
        self.assertGreater(1 << 15, parent_locality_capacity(15))

    def test_energy_rest_mass_only(self):
        self.assertAlmostEqual(creation_energy_j(), M0_KG * C**2)
        self.assertTrue(4e15 < creation_energy_j() < 5e15)

    def test_horizon_fall_idealized(self):
        t = fixed_schwarzschild_horizon_fall_s(100_000_000 * SUN_KG)
        self.assertTrue(650 < t < 665)
        # Timer phase 270s at horizon -> first +30, then +330, then +630.
        events = [30, 330, 630]
        self.assertEqual(sum(e < t for e in events), 3)

    def test_invalid(self):
        for n in (-1, 201, 1.5, False):
            with self.assertRaises(ValueError):
                snapshot(n)
        for kw in (
            {"initial_mass_kg": 1e308},
            {"initial_mass_kg": 1e-320},
            {"density_kg_m3": 1e308},
            {"density_kg_m3": 1e-320},
            {"initial_mass_kg": float("nan")},
            {"density_kg_m3": float("inf")},
        ):
            with self.assertRaises(ValueError):
                snapshot(200 if kw == {"initial_mass_kg": 1e308} else 0, **kw)


class PermitPolicyTests(unittest.TestCase):
    @staticmethod
    def attempt(ledger, version, request_id, **override):
        checks = dict(feedstock_ok=True, free_space_ok=True, cooling_ok=True)
        checks.update(override)
        return ledger.try_authorized_birth(
            expected_version=version, request_id=request_id, **checks
        )

    def test_budget_upper_bound(self):
        ledger = PermitLedger(15)
        births = 0
        for i in range(20):
            state, granted = self.attempt(ledger, ledger.snapshot().version,
                                          f"request-{i}")
            births += int(granted)
        self.assertEqual((births, state.permits_remaining, state.cumulative_births),
                         (15, 0, 15))
        self.assertEqual(1 + births, 16)

    def test_fail_closed(self):
        ledger = PermitLedger(3)
        for i, checks in enumerate((
            dict(feedstock_ok=False),
            dict(free_space_ok=False),
            dict(cooling_ok=False),
        )):
            state, ok = self.attempt(ledger, 0, f"deny-{i}", **checks)
            self.assertFalse(ok)
            self.assertEqual((state.permits_remaining, state.version), (3, 0))

    def test_sol_high_stale_same_state(self):
        """Same observed version must not authorize twice."""
        ledger = PermitLedger(1)
        version = ledger.snapshot().version
        first, ok1 = self.attempt(ledger, version, "independent-a")
        second, ok2 = self.attempt(ledger, version, "independent-b")
        self.assertTrue(ok1)
        self.assertFalse(ok2)
        self.assertEqual((first.permits_remaining, second.permits_remaining), (0, 0))
        self.assertEqual(ledger.snapshot().cumulative_births, 1)

    def test_sol_high_concurrent_same_version(self):
        ledger = PermitLedger(1)
        barrier = Barrier(2)
        def worker(identifier):
            barrier.wait(timeout=5)
            return self.attempt(ledger, 0, identifier)[1]
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(worker, ("concurrent-a", "concurrent-b")))
        self.assertEqual(sum(outcomes), 1)

    def test_replay_request_id(self):
        ledger = PermitLedger(2)
        first, ok = self.attempt(ledger, 0, "nonce-1")
        self.assertTrue(ok)
        second, replay_ok = self.attempt(ledger, first.version, "nonce-1")
        self.assertFalse(replay_ok)
        self.assertEqual(second, first)
        third, new_ok = self.attempt(ledger, first.version, "nonce-2")
        self.assertTrue(new_ok)
        self.assertEqual(third.cumulative_births, 2)

    def test_invalid_input_boundary(self):
        for bad in (float("nan"), float("inf"), "1", True, 1.0, -1):
            with self.assertRaises(ValueError):
                PermitLedger(bad)
        ledger = PermitLedger(1)
        for bad in (float("nan"), float("inf"), "0", True, -1):
            with self.assertRaises(ValueError):
                self.attempt(ledger, bad, "id")
        for bad in ("false", 0, None, 1):
            with self.assertRaises(ValueError):
                self.attempt(ledger, 0, f"bad-{bad}", feedstock_ok=bad)
        for bad in ("", None, 0, "x" * 129):
            with self.assertRaises(ValueError):
                self.attempt(ledger, 0, bad)
        self.assertEqual(ledger.snapshot().permits_remaining, 1)


if __name__ == "__main__":
    unittest.main()
