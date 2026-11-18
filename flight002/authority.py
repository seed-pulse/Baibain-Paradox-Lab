"""In-process, non-durable approval counterexample/repair lab.

This is NOT a physical actuator, transaction service, fault-tolerant storage,
cryptographic token system, or distributed authorization protocol.
"""
from dataclasses import dataclass
from threading import Lock


def _nonnegative_int(value: object, field: str) -> None:
    if type(value) is not int or value < 0:  # bool is NOT accepted
        raise ValueError(f"{field} must be a nonnegative integer")


@dataclass(frozen=True)
class BudgetSnapshot:
    budget: int
    remaining: int
    grants: int
    version: int
    approved_ids: frozenset[str]


@dataclass(frozen=True)
class Decision:
    approved: bool
    reason: str
    snapshot: BudgetSnapshot


class BudgetAuthority:
    """One authoritative instance, with immutable whole-state publication.

    A single assignment publishes the complete next in-memory snapshot while
    holding a process-local Lock. It fixes the Flight 001 *partial in-memory
    multi-field update* issue for failure before publication.

    It DOES NOT promise crash durability, preservation across fork/replication,
    reliable delivery of responses, or atomic coupling to physical creation.
    A request denied for temporary resource failure may later be retried with
    the same ID and a fresh version, since only GRANTED IDs are retained.
    """

    def __init__(self, budget: int):
        _nonnegative_int(budget, "budget")
        self._guard = Lock()
        self._state = BudgetSnapshot(
            budget=budget, remaining=budget, grants=0, version=0,
            approved_ids=frozenset()
        )

    def snapshot(self) -> BudgetSnapshot:
        with self._guard:
            return self._state

    def _build_successor(self, old: BudgetSnapshot, request_id: str) -> BudgetSnapshot:
        """Overrideable only for deterministic fault-injection tests."""
        new = BudgetSnapshot(
            budget=old.budget, remaining=old.remaining - 1,
            grants=old.grants + 1, version=old.version + 1,
            approved_ids=old.approved_ids | {request_id}
        )
        assert new.remaining + new.grants == new.budget
        assert len(new.approved_ids) == new.grants
        return new

    def request_birth(self, *, expected_version: int, request_id: str,
                      feedstock_ok: bool, space_ok: bool,
                      cooling_ok: bool) -> Decision:
        _nonnegative_int(expected_version, "expected_version")
        if type(request_id) is not str or not (1 <= len(request_id) <= 128):
            raise ValueError("request_id must be a nonempty str with length <=128")
        for key, value in (("feedstock_ok", feedstock_ok), ("space_ok", space_ok),
                           ("cooling_ok", cooling_ok)):
            if type(value) is not bool:
                raise ValueError(f"{key} must be an actual bool")
        with self._guard:
            before = self._state
            if request_id in before.approved_ids:
                return Decision(False, "already_granted", before)
            if before.version != expected_version:
                return Decision(False, "stale_version", before)
            if before.remaining == 0:
                return Decision(False, "budget_exhausted", before)
            if not (feedstock_ok and space_ok and cooling_ok):
                # Only successful IDs need retention for a no-double-GRANT
                # guarantee. Denials are not guaranteed to stay denied.
                return Decision(False, "resource_unavailable", before)
            candidate = self._build_successor(before, request_id)
            # One in-memory publication rather than partial counter mutation.
            self._state = candidate
            return Decision(True, "granted", candidate)
