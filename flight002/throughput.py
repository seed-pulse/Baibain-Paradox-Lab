"""Pure mathematical upper bounds for a deliberately fictional replicator.

Integers in grams/seconds avoid floating-point threshold artifacts.
The sources are cumulative upper limits, NOT sufficient physical schedules.
"""


def _uint(value: object, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative int")


def demanded_births(completed_cycles: int) -> int:
    """Exact number of additional full 50g copies under unrestricted doubling."""
    _uint(completed_cycles, "completed_cycles")
    if completed_cycles > 10000:
        raise ValueError("research model caps requested cycles at 10000")
    return (1 << completed_cycles) - 1


def feedstock_birth_upper_bound(*, elapsed_s: int, reserve_g: int,
                                feed_rate_g_s: int, per_copy_g: int = 50) -> int:
    """Max total births affordable at time t, no losses, one initial copy excluded.

    This is a necessary resource bound; a sufficient online schedule needs
    supplies to arrive before EVERY particular birth decision.
    """
    _uint(elapsed_s, "elapsed_s")
    _uint(reserve_g, "reserve_g")
    _uint(feed_rate_g_s, "feed_rate_g_s")
    _uint(per_copy_g, "per_copy_g")
    if per_copy_g == 0:
        raise ValueError("per_copy_g must be positive")
    return (reserve_g + feed_rate_g_s * elapsed_s) // per_copy_g


def snapshot_cycle(cycle: int, *, finite_permits: int,
                   reserve_g: int, feed_rate_g_s: int,
                   per_copy_g: int = 50) -> dict:
    """Count only *upper bounds* on cumulative successful births."""
    _uint(cycle, "cycle")
    _uint(finite_permits, "finite_permits")
    elapsed_s = cycle * 300
    demand = demanded_births(cycle)
    supply_cap = feedstock_birth_upper_bound(
        elapsed_s=elapsed_s, reserve_g=reserve_g,
        feed_rate_g_s=feed_rate_g_s, per_copy_g=per_copy_g
    )
    can_match = demand <= finite_permits and demand <= supply_cap
    return {
        "cycle": cycle, "elapsed_s": elapsed_s,
        "unrestricted_required_births": demand,
        "authorized_birth_upper_bound": finite_permits,
        "feedstock_birth_upper_bound": supply_cap,
        "combined_total_births_upper_bound": min(demand, finite_permits, supply_cap),
        "necessary_conditions_hold": can_match
    }


def first_impossible_cycle(*, finite_permits: int, reserve_g: int,
                           feed_rate_g_s: int, max_cycle: int = 512) -> int | None:
    """First clock tick when global budget or cumulative supply cannot meet 2^n."""
    _uint(max_cycle, "max_cycle")
    if max_cycle > 10000:
        raise ValueError("max_cycle exceeds model cap")
    for n in range(1, max_cycle + 1):
        if not snapshot_cycle(n, finite_permits=finite_permits,
                              reserve_g=reserve_g,
                              feed_rate_g_s=feed_rate_g_s)["necessary_conditions_hold"]:
            return n
    return None
