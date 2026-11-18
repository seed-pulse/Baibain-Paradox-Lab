"""Flight 003 arithmetic oracles. This module never imports Flight 001/002."""

from decimal import Decimal, localcontext
from math import comb


def supply_and_permits():
    population = 1
    demand = 0
    rows = []
    for tick in range(1, 19):
        births_this_tick = population
        demand += births_this_tick
        population += births_this_tick
        assert demand == 2**tick - 1
        rows.append({
            "tick": tick, "minutes": 5 * tick, "births_this_tick": births_this_tick,
            "cumulative_births": demand, "demand_g": 50 * demand,
            "supply_g": 300_000 * tick, "supply_cap_births": 6_000 * tick,
            "slack_g": 300_000 * tick - 50 * demand,
        })
    first = next(row["tick"] for row in rows if row["slack_g"] < 0)
    # Independent alternative: at most one interval's delivery is usable per tick.
    no_carry = next(row["tick"] for row in rows if row["births_this_tick"] > 6_000)
    assert (first, no_carry) == (17, 14)
    partial_capacity = rows[16]["supply_cap_births"] - rows[15]["cumulative_births"]
    assert partial_capacity == 36_465
    for budget in range(4097):
        n = (budget + 1).bit_length() - 1
        assert 2**n - 1 <= budget < 2**(n + 1) - 1
    return {
        "first_cumulative_failure": first, "first_no_carry_failure": no_carry,
        "max_new_buns_by_mass_at_tick_17_after_16_complete": partial_capacity,
        "prefixes_checked": len(rows), "budgets_checked": 4097,
        "boundary": rows[15:17],
    }


def placement():
    # Each existing object persists at its depth and creates one child at depth + 1.
    by_depth = [1]
    witnesses = []
    for tick in range(1, 16):
        by_depth = [a + b for a, b in zip(by_depth + [0], [0] + by_depth)]
        assert by_depth == [comb(tick, depth) for depth in range(tick + 1)]
        within = 0
        for depth, count in enumerate(by_depth):
            within += count
            capacity = (2 * depth + 1)**3
            if within > capacity:
                witnesses.append((tick, depth, within, capacity))
    assert witnesses[0] == (12, 4, 794, 729)
    # A separate enumeration counts the birth/no-birth choices in 12 ticks.
    shallow = sum(history.bit_count() <= 4 for history in range(2**12))
    assert shallow == 794
    full_volume = next(n for n in range(1, 16) if 2**n > (2*n + 1)**3)
    assert full_volume == 15
    # Moving-parent countermodel, in bun diameters. During a tick center i
    # slides from i to 2*i. Sampled gaps are exact; the interpolation is linear.
    centers = [0]
    largest_move = {}
    for tick in range(1, 16):
        largest_move[tick] = centers[-1]
        midpoint_doubled = [3*i for i in centers]
        assert all(b-a >= 2 for a, b in zip(midpoint_doubled, midpoint_doubled[1:]))
        centers = [site for i in centers for site in (2*i, 2*i + 1)]
        assert centers == list(range(2**tick))
    return {
        "first_depth_volume_witness": list(witnesses[0]),
        "histories_with_up_to_four_birth_edges_at_12": shallow,
        "first_full_population_volume_witness": full_volume,
        "full_volume_ticks_14_and_15": [[2**n, (2*n + 1)**3] for n in (14, 15)],
        "direct_child_limit_from_kissing_theorem": 12,
        "moving_line_max_parent_move_in_diameters": {
            str(n): largest_move[n] for n in (12, 13, 15)
        },
    }


def gravity_and_causality():
    D = Decimal
    with localcontext() as ctx:
        ctx.prec = 64
        pi = D("3.141592653589793238462643383279502884197169399375105820974944592")
        c, grav, au = D(299_792_458), D("6.67430e-11"), D(149_597_870_700)
        density, seed = D(1000), D("0.05")
        one_third = D(1) / 3
        r0 = (3 * seed / (4 * pi * density)) ** one_third
        thresholds = {}
        boundary = {}
        for tick in range(1, 151):
            mass = seed * 2**tick
            volume = mass / density
            radius_cubed = 3 * volume / (4 * pi)
            rs = 2 * grav * mass / c**2
            causal = r0 + c * (300 * tick)
            comparisons = {
                "10_litres": volume > D("0.010"), "earth": mass > D("5.9722e24"),
                "sun": mass > D("1.98847e30"), "compactness": rs**3 >= radius_cubed,
                "flat_volume": radius_cubed > causal**3,
            }
            for name, crossed in comparisons.items():
                if crossed:
                    thresholds.setdefault(name, tick)
            if tick in (131, 132, 147, 148):
                radius = radius_cubed ** one_third
                boundary[str(tick)] = {
                    "Rs_over_R": format(rs / radius, ".9f"),
                    "R_AU": format(radius / au, ".6f"),
                    "flat_reach_AU": format(causal / au, ".6f"),
                }
        expected = {"10_litres": 8, "earth": 87, "sun": 105,
                    "compactness": 132, "flat_volume": 148}
        assert thresholds == expected

        # E=1 inward geodesic, x=sqrt(r/rs). Integrate advanced time along it.
        rs_time = 2 * grav * D("1e8") * D("1.98847e30") / c**3
        fall = 2 * rs_time / 3
        def primitive(x):
            return x**3 / 3 - x**2 / 2 + x - (1 + x).ln()
        lo, hi = D(0), D(1)
        for _ in range(120):
            mid = (lo + hi) / 2
            advanced = 2 * rs_time * (primitive(D(1)) - primitive(mid))
            if advanced > 100:
                lo = mid
            else:
                hi = mid
        x = (lo + hi) / 2
        hit = fall * (1 - x**3)
        assert D(206) < hit < D(207)
        phases = {str(phase): [t for t in range(300 - phase, 901, 300) if t < fall]
                  for phase in (0, 270)}
        assert phases == {"0": [300, 600], "270": [30, 330, 630]}

        # A prescribed flat-slice FLRW metric. Compare only geometric capacity.
        hubble = D(2).ln() / 900
        growth = (hubble * 300 * 148).exp()
        required = r0 * D(2)**(D(148) / 3)
        proper_front = growth * r0 + c * (growth - 1) / hubble
        assert required > r0 + c * 300 * 148 and required < proper_front
        return {
            "initial_radius_m": format(r0, ".10f"), "first_ticks": thresholds,
            "boundary": boundary, "rest_energy_one_bun_J": str(seed * c**2),
            "horizon_to_zero_s": format(fall, ".6f"), "birth_times_by_phase_s": phases,
            "ingoing_pulse_advanced_delay_s": 100, "meeting_r_over_rs": format(x*x, ".7f"),
            "meeting_proper_s": format(hit, ".6f"),
            "FLRW_H_per_s": format(hubble, ".12f"),
            "FLRW_comoving_limit_AU": format((r0 + c / hubble) / au, ".6f"),
            "FLRW_required_over_proper_front_at_148": format(required / proper_front, ".8E"),
        }


def split_charge():
    # A speculative local resource split. One confirmation sequence, not canon.
    charges = [15]
    history = []
    for _ in range(6):
        history.append([len(charges), sum(charges)])
        children = []
        for q in charges:
            if q:
                left = (q - 1) // 2
                children.extend((left, q - 1 - left))
            else:
                children.append(0)
        charges = children
    assert history == [[1, 15], [2, 14], [4, 12], [8, 8], [16, 0], [16, 0]]
    return history
