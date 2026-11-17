"""Baibain Flight 001: toy mathematics, not a physical simulation.

Only Python standard library. Canon: doubling every 300 seconds.
All thresholds are conditional on 50g, rho=1000 kg/m^3 and declared geometry.
"""
from dataclasses import dataclass
import argparse
import json
import math

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
    """Total mass and uniform-density/flat-spacetime proxy indicators."""
    if not isinstance(cycle, int) or cycle < 0 or cycle > 200:
        raise ValueError("cycle must be an integer from 0 to 200")
    if not (math.isfinite(initial_mass_kg) and initial_mass_kg > 0):
        raise ValueError("initial_mass_kg must be positive and finite")
    if not (math.isfinite(density_kg_m3) and density_kg_m3 > 0):
        raise ValueError("density_kg_m3 must be positive and finite")
    n = 1 << cycle
    mass = initial_mass_kg * n
    volume = mass / density_kg_m3
    radius = (3.0 * volume / (4.0 * math.pi)) ** (1.0 / 3.0)
    rs = 2.0 * G * mass / C**2
    elapsed = cycle * PERIOD_S
    causal = C * elapsed
    pressure = 2.0 * math.pi * G * density_kg_m3**2 * radius**2 / 3.0
    return {
        "cycle": cycle,
        "minutes": cycle * 5,
        "count": n,
        "mass_kg": mass,
        "volume_m3": volume,
        "uniform_radius_m": radius,
        "schwarzschild_radius_m": rs,
        "compactness_ratio_rs_over_r": rs / radius,
        "newtonian_center_pressure_pa": pressure,
        "flat_causal_radius_m": causal,
        "radius_over_flat_causal_radius": radius / causal if elapsed else None,
    }


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
    """Toy *single atomic ledger* model; not a distributed implementation."""
    permits_remaining: int
    cumulative_births: int = 0


def try_authorized_birth(state: PermitState, *,
                         feedstock_ok: bool, free_space_ok: bool,
                         cooling_ok: bool) -> tuple[PermitState, bool]:
    """Fail closed. The three environmental checks are assumed trustworthy."""
    if state.permits_remaining < 0 or state.cumulative_births < 0:
        raise ValueError("negative ledger state")
    if not (state.permits_remaining and feedstock_ok
            and free_space_ok and cooling_ok):
        return state, False
    return PermitState(state.permits_remaining - 1,
                       state.cumulative_births + 1), True


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
