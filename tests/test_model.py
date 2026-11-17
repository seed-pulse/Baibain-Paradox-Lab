"""Flight 001 regression checks: formulas and toy-policy invariants only."""
import math
import unittest

from model import (
    C, M0_KG, SUN_KG, PermitState, creation_energy_j,
    first_cycle, fixed_schwarzschild_horizon_fall_s, milestones,
    snapshot, try_authorized_birth,
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

    def test_energy_rest_mass_only(self):
        self.assertAlmostEqual(creation_energy_j(), M0_KG * C**2)
        self.assertTrue(4e15 < creation_energy_j() < 5e15)

    def test_horizon_fall_idealized(self):
        t = fixed_schwarzschild_horizon_fall_s(100_000_000 * SUN_KG)
        self.assertTrue(650 < t < 665)

    def test_invalid(self):
        for n in (-1, 201, 1.5):
            with self.assertRaises(ValueError):
                snapshot(n)


class PermitPolicyTests(unittest.TestCase):
    def test_budget_upper_bound(self):
        state = PermitState(15)
        births = 0
        for _ in range(20):
            state, granted = try_authorized_birth(
                state, feedstock_ok=True, free_space_ok=True, cooling_ok=True
            )
            births += int(granted)
        self.assertEqual((births, state.permits_remaining, state.cumulative_births),
                         (15, 0, 15))
        self.assertEqual(1 + births, 16)  # Initial object + births

    def test_fail_closed(self):
        initial = PermitState(3)
        for checks in (
            dict(feedstock_ok=False, free_space_ok=True, cooling_ok=True),
            dict(feedstock_ok=True, free_space_ok=False, cooling_ok=True),
            dict(feedstock_ok=True, free_space_ok=True, cooling_ok=False),
        ):
            actual, ok = try_authorized_birth(initial, **checks)
            self.assertFalse(ok)
            self.assertEqual(actual, initial)


if __name__ == "__main__":
    unittest.main()
