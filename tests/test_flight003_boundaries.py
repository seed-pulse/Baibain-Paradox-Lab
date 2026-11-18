from unittest import TestCase

from flight002.authority import BudgetAuthority
from flight002.throughput import first_impossible_cycle


class Flight003Boundaries(TestCase):
    def test_public_snapshot_and_all_decisions_have_their_own_field_storage(self):
        bank = BudgetAuthority(1)

        def check_view(view):
            self.assertEqual(view, bank.snapshot())
            self.assertIsNot(view, bank._state)
            self.assertIsNot(vars(view), vars(bank._state))

        check_view(bank.snapshot())
        for version, rid, space, reason in (
            (1, "later", True, "stale_version"),
            (0, "one", False, "resource_unavailable"),
            (0, "one", True, "granted"),
            (1, "one", True, "already_granted"),
            (1, "another", True, "budget_exhausted"),
        ):
            answer = bank.request_birth(expected_version=version, request_id=rid,
                                        feedstock_ok=True, space_ok=space, cooling_ok=True)
            self.assertEqual(answer.reason, reason)
            check_view(answer.snapshot)

    def test_zero_horizon_validates_inputs(self):
        args = dict(finite_permits=15, reserve_g=50, feed_rate_g_s=1, max_cycle=0)
        self.assertIsNone(first_impossible_cycle(**args))
        for field in ("finite_permits", "reserve_g", "feed_rate_g_s"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                first_impossible_cycle(**(args | {field: -1}))
