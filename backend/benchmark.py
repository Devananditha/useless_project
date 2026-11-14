"""
N=100 Paired-Seed Benchmark Execution Module.
Runs actual Google OR-Tools CP-SAT solver across deterministic paired disruption seeds.
Evaluates A2 (study-defined fixed-source baseline) and P3 (StallBreaker joint policy).
Derives status distributions and metrics strictly from measured solver outputs.
"""

import json
import os
import random
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.models import (
    ScenarioSnapshot,
    RepairOrder,
    PartSource,
    BayState,
    VehicleState,
    PolicyId,
    SolverStatusEnum
)
from backend.solver import solve_recovery_problem
from backend.fixtures import tick_to_clock


def generate_benchmark_seeds(n: int = 100, master_seed: int = 42) -> List[ScenarioSnapshot]:
    """
    Generates n deterministic scenario seeds using a documented pseudo-random generator.
    Variations reflect realistic dealership operational jitter around canonical S-MATH-01.
    """
    rng = random.Random(master_seed)
    seeds: List[ScenarioSnapshot] = []

    for seed_idx in range(n):
        # Operational variations around canonical disruption
        s1_ready = rng.randint(24, 32)   # 10:00 to 10:40 AM
        s1_cost = round(rng.uniform(50.0, 65.0), 2)
        
        s2_ready = rng.randint(44, 56)   # 11:40 AM to 12:40 PM
        s2_cost = round(rng.uniform(15.0, 24.0), 2)
        
        install_dur = rng.randint(10, 14)       # 50 to 70 min
        fleet_dur = rng.randint(20, 28)         # 100 to 140 min
        p1_promise = rng.randint(62, 70)        # 13:10 to 13:50 PM
        p2_promise = rng.randint(50, 58)        # 12:10 to 12:50 PM

        # 85% hoist lock (partially dismantled), 15% rollable
        is_rollable = (rng.random() < 0.15)
        veh_state = VehicleState.SAFE_TO_RELOCATE if is_rollable else VehicleState.PARTIALLY_DISMANTLED
        h2_stalls = 1 if is_rollable else 0

        ro1042 = RepairOrder(
            ro_id="RO-1042",
            customer_name=f"Customer Seed #{seed_idx+1}",
            vehicle_model="Ford Explorer",
            promise_ticks=p1_promise,
            priority_weight=1.0,
            service_duration_ticks=install_dur,
            required_bay="B4",
            current_vehicle_state=veh_state,
            technician_signoff_recorded=is_rollable
        )

        ro1051 = RepairOrder(
            ro_id="RO-1051",
            customer_name=f"Fleet Account #{seed_idx+1}",
            vehicle_model="Ford F-150 Commercial",
            is_commercial_fleet=True,
            promise_ticks=p2_promise,
            priority_weight=3.0,
            service_duration_ticks=fleet_dur,
            required_bay="B4",
            current_vehicle_state=VehicleState.SAFE_TO_MOVE,
            technician_signoff_recorded=True
        )

        sources = [
            PartSource(source_id="S1", name="Hotshot Courier Express", usable_time_ticks=s1_ready, cost=s1_cost, atp=1),
            PartSource(source_id="S2", name="Sister Store Shuttle Transfer", usable_time_ticks=s2_ready, cost=s2_cost, atp=1)
        ]

        seed_snap = ScenarioSnapshot(
            scenario_id=f"SEED-{seed_idx+1:03d}",
            scenario_name=f"Benchmark Disruption Seed #{seed_idx+1:03d}",
            description="Synthetic paired-seed dealership scenario with operational variance.",
            snapshot_version=1,
            current_tick=21,
            current_clock=tick_to_clock(21),
            ro1042=ro1042,
            ro1051=ro1051,
            sources=sources,
            bay_b4_state=BayState.OCCUPIED,
            h2_capacity=1,
            h2_available_stalls=h2_stalls,
            relocation_duration_ticks=3,
            clearance_duration_ticks=2,
            technician_k1_available=True
        )
        seeds.append(seed_snap)

    return seeds


def run_benchmark(n: int = 100, master_seed: int = 42) -> Dict[str, Any]:
    """
    Executes actual CP-SAT solves across n deterministic paired seeds for A2 and P3.
    Derives status distributions from actual solver outcomes.
    Excludes any infeasible sentinel values from lateness averages.
    Saves results as a JSON artifact under generated-results/.
    """
    t_bench_start = time.perf_counter()
    seeds = generate_benchmark_seeds(n=n, master_seed=master_seed)

    records: List[Dict[str, Any]] = []
    
    # Track status distributions separately from actual solver statuses
    a2_status_dist = {"OPTIMAL": 0, "FEASIBLE": 0, "INFEASIBLE": 0, "UNKNOWN": 0}
    p3_status_dist = {"OPTIMAL": 0, "FEASIBLE": 0, "INFEASIBLE": 0, "UNKNOWN": 0}

    valid_a2_weighted: List[float] = []
    valid_p3_weighted: List[float] = []
    valid_delay_savings: List[int] = []
    p3_runtimes_ms: List[float] = []
    a2_runtimes_ms: List[float] = []

    p3_wins = 0
    ties = 0
    p3_worsened = 0

    for idx, snap in enumerate(seeds):
        # Solve Baseline A2
        prop_a2 = solve_recovery_problem(snap, PolicyId.A2)
        # Solve Joint P3
        prop_p3 = solve_recovery_problem(snap, PolicyId.P3)

        # Update actual status distributions
        a2_st = prop_a2.solver_status.value
        p3_st = prop_p3.solver_status.value
        a2_status_dist[a2_st] = a2_status_dist.get(a2_st, 0) + 1
        p3_status_dist[p3_st] = p3_status_dist.get(p3_st, 0) + 1

        p3_runtimes_ms.append(prop_p3.solve_time_ms)
        a2_runtimes_ms.append(prop_a2.solve_time_ms)

        # Check if both are valid feasible/optimal runs
        is_paired_valid = (
            prop_a2.solver_status in (SolverStatusEnum.OPTIMAL, SolverStatusEnum.FEASIBLE) and
            prop_p3.solver_status in (SolverStatusEnum.OPTIMAL, SolverStatusEnum.FEASIBLE) and
            prop_a2.weighted_lateness_ticks < 900.0 and
            prop_p3.weighted_lateness_ticks < 900.0
        )

        delay_diff_min = 0
        outcome = "UNKNOWN"

        if is_paired_valid:
            valid_a2_weighted.append(prop_a2.weighted_lateness_ticks)
            valid_p3_weighted.append(prop_p3.weighted_lateness_ticks)
            
            delay_diff_min = prop_a2.downstream_delay_minutes - prop_p3.downstream_delay_minutes
            valid_delay_savings.append(delay_diff_min)

            if prop_p3.weighted_lateness_ticks < prop_a2.weighted_lateness_ticks:
                p3_wins += 1
                outcome = "IMPROVED"
            elif prop_p3.weighted_lateness_ticks == prop_a2.weighted_lateness_ticks:
                ties += 1
                outcome = "TIED"
            else:
                p3_worsened += 1
                outcome = "WORSENED"
        else:
            outcome = "INFEASIBLE_RUN"

        records.append({
            "seed_id": snap.scenario_id,
            "a2_status": a2_st,
            "p3_status": p3_st,
            "a2_pass1_status": prop_a2.pass1_status.value if prop_a2.pass1_status else None,
            "a2_pass2_status": prop_a2.pass2_status.value if prop_a2.pass2_status else None,
            "p3_pass1_status": prop_p3.pass1_status.value if prop_p3.pass1_status else None,
            "p3_pass2_status": prop_p3.pass2_status.value if prop_p3.pass2_status else None,
            "a2_weighted_lateness": prop_a2.weighted_lateness_ticks,
            "p3_weighted_lateness": prop_p3.weighted_lateness_ticks,
            "a2_freight_cost": prop_a2.parts_freight_cost,
            "p3_freight_cost": prop_p3.parts_freight_cost,
            "relocation_selected": prop_p3.selected_movement == "RELOCATE_TO_H2",
            "p3_outcome": outcome,
            "delay_savings_min": delay_diff_min,
            "p3_solve_time_ms": round(prop_p3.solve_time_ms, 2),
            "a2_solve_time_ms": round(prop_a2.solve_time_ms, 2)
        })

    total_bench_time = time.perf_counter() - t_bench_start
    valid_count = len(valid_a2_weighted)

    mean_a2_z1 = (sum(valid_a2_weighted) / valid_count) if valid_count > 0 else 0.0
    mean_p3_z1 = (sum(valid_p3_weighted) / valid_count) if valid_count > 0 else 0.0
    mean_savings_min = (sum(valid_delay_savings) / valid_count) if valid_count > 0 else 0.0
    mean_p3_runtime_ms = (sum(p3_runtimes_ms) / len(p3_runtimes_ms)) if p3_runtimes_ms else 0.0
    mean_a2_runtime_ms = (sum(a2_runtimes_ms) / len(a2_runtimes_ms)) if a2_runtimes_ms else 0.0

    overall_reduction_pct = (
        ((mean_a2_z1 - mean_p3_z1) / mean_a2_z1) * 100.0 if mean_a2_z1 > 0 else 0.0
    )

    win_or_tie_rate = (
        ((p3_wins + ties) / valid_count) * 100.0 if valid_count > 0 else 0.0
    )

    # Persist benchmark artifact in generated-results/
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated-results")
    os.makedirs(out_dir, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_filename = f"benchmark_results_n{n}_{timestamp_str}.json"
    artifact_path = os.path.join(out_dir, artifact_filename)
    latest_path = os.path.join(out_dir, "benchmark_latest.json")

    result_data = {
        "benchmark_id": f"BENCH-{master_seed}-{n}",
        "total_seeds": n,
        "valid_paired_seeds": valid_count,
        "master_seed": master_seed,
        "total_wall_clock_seconds": round(total_bench_time, 2),
        "mean_p3_solve_time_ms": round(mean_p3_runtime_ms, 2),
        "mean_a2_solve_time_ms": round(mean_a2_runtime_ms, 2),
        "mean_a2_weighted_lateness": round(mean_a2_z1, 1),
        "mean_p3_weighted_lateness": round(mean_p3_z1, 1),
        "mean_downstream_delay_savings_min": round(mean_savings_min, 1),
        "mean_weighted_lateness_reduction_pct": round(overall_reduction_pct, 1),
        "p3_outperform_count": p3_wins,
        "tie_count": ties,
        "p3_worsened_count": p3_worsened,
        "p3_win_or_tie_rate_pct": round(win_or_tie_rate, 1),
        "a2_status_distribution": a2_status_dist,
        "p3_status_distribution": p3_status_dist,
        "status_distribution": p3_status_dist,  # backwards-compatible alias
        "artifact_path": artifact_path,
        "scope_notice": (
            "P3 option set includes candidates available to A2; win-rate compares joint "
            "optimisation against fixed-source sequential baseline A2 under synthetic operational jitter, "
            "not against all human manager decisions in real dealership operations."
        ),
        "records": records
    }

    try:
        with open(artifact_path, "w") as f:
            json.dump(result_data, f, indent=2)
        with open(latest_path, "w") as f:
            json.dump(result_data, f, indent=2)
    except Exception as e:
        # Non-fatal file write error
        pass

    return result_data
