"""Baibain Flight 001: toy mathematics, not a physical simulation.

Only Python standard library. Canon: doubling every 300 seconds.
All thresholds are conditional on 50g, rho=1000 kg/m^3 and declared geometry.
"""
from dataclasses import dataclass
import argparse
import json
import math
import threading

G = 6.67430e-11
C = 299_792_458.0
AU_M = 149_597_870_700.0
EARTH_KG = 5.9722e24
SUN_KG = 1.98847e30
M0_KG = 0.05
RHO_KG_M3 = 1000.0
PERIOD_S = 300


def snapshot(cycle: int, initial_mass_kg: float = M0_KG,
             density_kg_m3: float = RHO_KG_M3) -> dict:
    """Conditional indicators; positive initial spatial radius included.

    Values that would overflow, underflow to physically meaningless zeros,
    or lose finiteness are rejected rather than returned as evidence.
    """
    if type(cycle) is not int or cycle < 0 or cycle > 200:
        raise ValueError("cycle must be an integer from 0 to 200")
    for label, value in (("initial_mass_kg", initial_mass_kg),
                         ("density_kg_m3", density_kg_m3)):
        try:
            valid = (type(value) in (int, float) and math.isfinite(value)
                     and value > 0)
        except (OverflowError, TypeError, ValueError):
            valid = False
        if not valid:
            raise ValueError(f"{label} must be positive and finite")
    try:
        n = 1 << cycle
        mass = initial_mass_kg * n
        volume = mass / density_kg_m3
        radius = (3.0 * volume / (4.0 * math.pi)) ** (1.0 / 3.0)
        initial_volume = initial_mass_kg / density_kg_m3
        initial_radius = (3.0 * initial_volume / (4.0 * math.pi)) ** (1.0 / 3.0)
        rs = 2.0 * G * mass / C**2
        elapsed = cycle * PERIOD_S
        # A non-pointlike initial bun occupies a ball of radius initial_radius.
        causal = initial_radius + C * elapsed
        pressure = 2.0 * math.pi * G * density_kg_m3**2 * radius**2 / 3.0
        compactness = rs / radius
        radius_fraction = radius / causal
    except (OverflowError, ZeroDivisionError, ValueError) as exc:
        raise ValueError("parameters out of supported numerical range") from exc
    computed = (mass, volume, radius, initial_volume, initial_radius,
                rs, causal, pressure, compactness, radius_fraction)
    if any((not math.isfinite(x) or x <= 0) for x in computed):
        raise ValueError("parameters produce nonfinite or underflowed indicators")
    return {
        "cycle": cycle,
        "minutes": cycle * 5,
        "count": n,
        "mass_kg": mass,
        "volume_m3": volume,
        "uniform_radius_m": radius,
        "initial_radius_m": initial_radius,
        "schwarzschild_radius_m": rs,
        "compactness_ratio_rs_over_r": compactness,
        "newtonian_center_pressure_pa": pressure,
        "flat_causal_radius_m": causal,
        "radius_over_flat_causal_radius": radius_fraction,
    }


def parent_locality_capacity(n: int) -> int:
    """Optimistic volume count when child centers may move one diameter per birth.

    Both parent and child centers are restricted to the parent-centered
    two-radius neighborhood per cycle, all objects remain fixed once made,
    and balls must not overlap. Ignores sphere packing inefficiencies.
    """
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    return (2 * n + 1) ** 3


def first_cycle(predicate, max_cycle: int = 200) -> int:
    """First positive completed cycle satisfying a model predicate."""
    for i in range(1, max_cycle + 1):
        if predicate(snapshot(i)):
            return i
    raise ValueError("not found through max_cycle")


def milestones() -> dict:
    """Returns first crossing cycles, not predictions of real-world events."""
    return {
        "10L_uniform_volume_exceeded": first_cycle(lambda x: x["volume_m3"] > 0.010),
        "earth_mass_exceeded": first_cycle(lambda x: x["mass_kg"] > EARTH_KG),
        "solar_mass_exceeded": first_cycle(lambda x: x["mass_kg"] > SUN_KG),
        "rs_at_least_uniform_radius": first_cycle(
            lambda x: x["schwarzschild_radius_m"] >= x["uniform_radius_m"]
        ),
        "uniform_radius_exceeds_flat_light_cone": first_cycle(
            lambda x: x["uniform_radius_m"] > x["flat_causal_radius_m"]
        ),
    }


def creation_energy_j(mass_kg: float = M0_KG) -> float:
    """Rest-energy equivalent; NOT heat necessarily deposited in surroundings."""
    if not math.isfinite(mass_kg) or mass_kg <= 0:
        raise ValueError("mass must be finite and positive")
    return mass_kg * C**2


def fixed_schwarzschild_horizon_fall_s(mass_kg: float) -> float:
    """Radial geodesic rest-at-infinity E=1, horizon->r=0 proper time.
    
    Ideal test particle, uncharged nonspinning stationary BH; not a calculation
    for a self-replicating mass or for an extended food object.
    """
    if not math.isfinite(mass_kg) or mass_kg <= 0:
        raise ValueError("mass must be finite and positive")
    return 4.0 * G * mass_kg / (3.0 * C**3)


@dataclass(frozen=True)
class PermitState:
    """Read-only observation; NEVER sufficient to authorize creation."""
    permits_remaining: int
    cumulative_births: int = 0
    version: int = 0


def _require_uint(value: object, field: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative int (bool excluded)")


class PermitLedger:
    """In-process serialized authorization authority (NOT distributed/durable).

    Unlike a pure state transition, old snapshots cannot be replayed to grant
    more births. Request IDs are one-shot; version checks reject stale clients.
    All instances must share ONE ledger. Forks, restarts, multi-process copies,
    real-world physical commit, sensor authenticity, power-loss atomicity and
    external replication remain UNSOLVED.
    """

    def __init__(self, initial_permits: int) -> None:
        _require_uint(initial_permits, "initial_permits")
        self._lock = threading.Lock()
        self._budget = initial_permits
        self._remaining = initial_permits
        self._births = 0
        self._version = 0
        self._attempted_ids: set[str] = set()

    def _snapshot_unlocked(self) -> PermitState:
        return PermitState(self._remaining, self._births, self._version)

    def snapshot(self) -> PermitState:
        with self._lock:
            return self._snapshot_unlocked()

    def try_authorized_birth(self, *, expected_version: int,
                             request_id: str, feedstock_ok: bool,
                             free_space_ok: bool,
                             cooling_ok: bool) -> tuple[PermitState, bool]:
        """Atomically authorize a hypothetical birth; does not create matter."""
        _require_uint(expected_version, "expected_version")
        if type(request_id) is not str or not (1 <= len(request_id) <= 128):
            raise ValueError("request_id must be nonempty str of length <= 128")
        for field, val in (("feedstock_ok", feedstock_ok),
                           ("free_space_ok", free_space_ok),
                           ("cooling_ok", cooling_ok)):
            if type(val) is not bool:
                raise ValueError(f"{field} must be bool")
        with self._lock:
            if request_id in self._attempted_ids:
                return self._snapshot_unlocked(), False
            # Even denied requests consume this request ID; retry with new ID.
            self._attempted_ids.add(request_id)
            if expected_version != self._version:
                return self._snapshot_unlocked(), False
            if self._remaining == 0 or not (
                feedstock_ok and free_space_ok and cooling_ok
            ):
                return self._snapshot_unlocked(), False
            self._remaining -= 1
            self._births += 1
            self._version += 1
            assert self._births + self._remaining == self._budget
            return self._snapshot_unlocked(), True


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cycle", type=int, help="show indicators after n doublings")
    p.add_argument("--milestones", action="store_true",
                   help="show first crossing cycles and their minutes")
    args = p.parse_args()
    if not args.milestones and args.cycle is None:
        p.print_help()
        return
    if args.milestones:
        m = milestones()
        print(json.dumps({
            k: {"cycle": v, "minutes": v * 5} for k, v in m.items()
        }, ensure_ascii=False, indent=2))
    if args.cycle is not None:
        print(json.dumps(snapshot(args.cycle), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
