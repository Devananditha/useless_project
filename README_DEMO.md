# StallBreaker — Live CP-SAT Service Recovery Demonstrator
## Tekion Tek-Qubit Hackathon 2026 | Theme 1: AI & Automation (UC04)

> **Core Research Concept:** In automotive service operations, bay immobilization triggered by sudden parts delivery disruptions creates severe downstream dispatch bottlenecks. Selecting candidate part sources sequentially on landed freight cost without visibility into hoist schedules triggers downstream commercial fleet delays. StallBreaker jointly evaluates eligible parts sources and bay schedules via **Google OR-Tools CP-SAT**, eliminating **66.7% of weighted lateness** and recovering **110 minutes of downstream delay** on the canonical `S-MATH-01` disruption fixture.

---

## 1. Quickstart — Running the Live Demonstrator

### Prerequisites
- Python 3.10+ (with `ortools`, `fastapi`, `uvicorn`, `pydantic`, `pytest`)
- Node.js 18+ (with `npm`)

### Step 1: Start Backend (FastAPI + CP-SAT Solver)
From repository root (`TEKION-HACKATHON-2026`):

```bash
# Terminal 1: Start the backend API service (Port 8000)
uvicorn backend.main:app --reload --port 8000
```
- Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)
- Swagger / OpenAPI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 2: Start Frontend (Vite + React + TypeScript)
In a second terminal:

```bash
# Terminal 2: Start the interactive presentation console (Port 5173)
cd frontend
npm run dev
```
- Open in browser: [http://localhost:5173](http://localhost:5173)

---

## 2. Automated Test Verification (27/27 Acceptance & Integration Tests)

Execute the full automated test suite verifying mathematical consistency, physical invariants, read-only GET requests, optimistic concurrency, and benchmark output:

```bash
python -m pytest backend/tests/test_acceptance.py -v
```

### Verified Test Gates:
1. `test_01_canonical_s_math_01_a2_arithmetic`: Baseline A2 selects S2; B4 free at 13:15 ($t=63$), RO-1051 finish 15:15 ($t=87$), 33 ticks lateness.
2. `test_02_canonical_s_math_01_p3_arithmetic`: Joint P3 selects S1; B4 free at 11:25 ($t=41$), RO-1051 finish 13:25 ($t=65$), 11 ticks lateness.
3. `test_03_ninety_nine_versus_thirty_three_weighted_ticks`: Exact $99.0$ vs $33.0$ weighted ticks ($w=3.0$).
4. `test_04_sixty_six_point_seven_percent_reduction`: $(99.0 - 33.0) / 99.0 = 66.7\%$ relative reduction in weighted lateness.
5. `test_05_one_hundred_ten_minute_delay_difference`: Exactly 22 ticks (110 minutes) downstream finish delta for fleet RO-1051.
6. `test_06_unsafe_movement_rejection`: Partially dismantled vehicle without wheel remount signoff rejected for relocation.
7. `test_07_h2_capacity_reservation_before_movement`: Movement rejected when holding area capacity $= 0$.
8. `test_08_bay_no_overlap`: Hoist exclusivity strictly enforced; no simultaneous bay occupancy.
9. `test_09_technician_no_overlap`: Technician K1 cannot execute concurrent operations.
10. `test_10_return_to_bay_precedence`: Return transit requires B4 clearance and part readiness.
11. `test_11_source_atp_eligibility`: Supplier source with ATP $= 0$ rejected by pre-check.
12. `test_12_invalid_fitment_rejection`: Unverified fitment rejected prior to solver inclusion.
13. `test_13_expired_quote_rejection`: Expired supplier quote rejected before solver inclusion.
14. `test_14_inventory_version_conflict`: Competing reservation advances snapshot version (v14 ➔ v15).
15. `test_15_stale_proposal_cannot_be_committed`: Outdated proposal rejected with `STALE_SNAPSHOT`.
16. `test_16_new_proposal_requires_new_human_approval`: Automatic re-solve requires explicit human advisor authorization; no auto-commit.
17. `test_17_solve_api_response_shape`: Solve endpoint returns exact `SolveResponse` contract (`comparison`, `active_proposal`, `snapshot`).
18. `test_18_scenario_get_is_read_only`: `GET /api/scenarios/{id}` is strictly read-only and does not mutate version.
19. `test_19_repeated_get_does_not_invalidate_proposal`: Repeated GET calls do not change version or invalidate pending proposals.
20. `test_20_act_3_competing_reservation_structure_and_stale_rejection`: Act 3 competing reservation structure validated and triggers stale rejection.
21. `test_21_replacement_proposal_requires_explicit_human_approval`: Replacement proposal explicitly authorized in subsequent call.
22. `test_22_a2_and_p3_solver_statuses_and_lexicographic_passes`: Lexicographic passes (Pass 1 lateness, Pass 2 freight) tracked and verified OPTIMAL.
23. `test_23_benchmark_status_counts_derived_from_actual_outputs`: Benchmark status counts derived from actual solver outcomes and written to artifact JSON.
24. `test_24_infeasible_runs_do_not_contaminate_lateness_averages`: Infeasible runs excluded from mean lateness statistics.
25. `test_25_ineligible_inventory_cannot_be_selected_by_solver`: Pre-solver gating blocks ineligible inventory from solver inclusion.
26. `test_26_act_2_relocation_timeline_full_sequence`: Full 7-interval relocation timeline verified with return transit and final clearance.
27. `test_27_canonical_fixture_promise_times_and_models`: Ford Explorer, F-150 Commercial, promise times ($t=66$, $t=54$), and usable times verified.

---

## 3. The 3-Act Live Demonstration Script

The demonstrator is structured into three acts proving the feasibility gating, physical state sensitivity, and optimistic concurrency of StallBreaker:

### Act 1: The Canonical Stall (Immobilized Vehicle on Scarce Bay)
- **Scenario:** Select `Act 1: Canonical S-MATH-01 (Ford Explorer on Hoist)`
- **Physical Situation:**
  - RO-1042 (Ford Explorer, Sarah Jenkins) is partially dismantled on Bay B4 (specialized alignment hoist).
  - Wheels/hub assembly detached; vehicle **cannot roll**; holding area H2 saturated ($0$ stalls available).
  - S1 (Hotshot Courier Express): $55.00 freight, usable at $t=27$ (10:15 AM).
  - S2 (Sister Store Shuttle Transfer): $18.00 freight, usable at $t=49$ (12:05 PM).
  - RO-1051 (Ford F-150 Commercial Fleet): Promised ready at $t=54$ (12:30 PM), weight $w=3.0$.
- **Action:** Click **Run Solver (Live CP-SAT)**.
- **What Happens:**
  - Google OR-Tools CP-SAT executes live (~30 ms).
  - **A2 Sequential Baseline:** Sourcing selects lowest freight S2 ($18). Bay B4 is locked until $t=63$ (13:15). RO-1051 is delayed to $t=87$ (15:15), accumulating **165 minutes lateness** (99.0 weighted ticks).
  - **StallBreaker P3:** Joint solver recognizes hoist scarcity and chooses S1 ($55). Bay B4 released at $t=41$ (11:25). RO-1051 completes at $t=65$ (13:25), accumulating only **55 minutes lateness** (33.0 weighted ticks).
  - **Result:** **66.7% reduction in weighted lateness**, saving **110 minutes of downstream delay** for +$37 freight.

---

### Act 2: Physical State Sensitivity (Relocatable Vehicle)
- **Scenario:** Select `Act 2: S-MATH-01-ROLLABLE (Vehicle Relocatable to H2)` from the dropdown.
- **Physical Situation:**
  - Technician K1 completes emergency temporary wheel remount; RO-1042 certified `SAFE_TO_RELOCATE`.
  - Holding area H2 has 1 available stall; transit takes 3 ticks (15 min) each way.
- **Action:** Click **Run Solver (Live CP-SAT)**.
- **What Happens:**
  - The CP-SAT solver dynamically selects movement option `RELOCATE_TO_H2`.
  - Chronological 7-interval sequence:
    1. RO-1042 transit to H2: $t=21 \to 24$ (09:45 to 10:00).
    2. RO-1051 on Bay B4: $t=24 \to 48$ (10:00 to 12:00) — **completes with 0 min lateness** against 12:30 promise!
    3. Bay B4 clearance: $t=48 \to 50$ (12:00 to 12:10).
    4. RO-1042 staged in H2: $t=24 \to 50$ (10:00 to 12:10).
    5. RO-1042 return transit: $t=50 \to 53$ (12:10 to 12:25).
    6. RO-1042 installation on B4: $t=53 \to 65$ (12:25 to 13:25).
    7. Final clearance: $t=65 \to 67$ (13:25 to 13:35).
  - RO-1042 finishes with only 1 tick (5 min) lateness, using the low-cost S2 part ($18).
  - **Result:** Weighted lateness drops to **1.0 weighted tick**, saving **165 minutes of fleet delay** and $37 in freight.

---

### Act 3: Optimistic Concurrency & The Stale-Snapshot Race
- **Scenario:** Return to `Act 1: Canonical S-MATH-01`.
- **Physical Situation:**
  - Proposal is generated under snapshot v14 (with S1 allocated).
  - While awaiting advisor signoff, an external job consumes the last unit of S1.
- **Action:**
  1. Click **Simulate S1 Stock Race (Act 3)**.
     - Observe: S1 ATP drops to 0; snapshot advances from **v14 ➔ v15**.
  2. Click **Advisor Approve & Commit**.
- **What Happens:**
  - The backend detects version mismatch (proposal v14 vs live v15).
  - **Commit is ABORTED.** Prominent alert: `STALE SNAPSHOT DETECTED`.
  - Automated re-solve executes under v15 (which now selects S2 due to S1 unavailability).
  - Crucially: **No automated commit occurs**. The new proposal is placed in `PENDING_APPROVAL` status.
  - The presenter can now click **Advisor Approve & Commit** a second time to explicitly authorize the replacement proposal under v15.

---

## 4. Multi-Seed CP-SAT Benchmark ($N=100$ Paired Seeds)

Click **N=100 Benchmark** in the console to execute 100 paired CP-SAT instances:

- **Master Seed:** 42 (`Random(42)`)
- **Valid Paired Seeds:** 100 / 100
- **Mean P3 CP-SAT Solve Time:** **~30.9 ms**
- **Mean A2 Baseline Solve Time:** **~31.4 ms**
- **P3 Win Rate:** **100.0%** (100 Wins, 0 Ties, 0 Losses against fixed S2 baseline)
- **Mean Downstream Delay Savings:** **119.4 minutes** per disruption incident
- **Mean Weighted Lateness Reduction:** **71.2%**
- **Status Distribution:**
  - P3: `OPTIMAL: 100, FEASIBLE: 0, INFEASIBLE: 0, UNKNOWN: 0`
  - A2: `OPTIMAL: 100, FEASIBLE: 0, INFEASIBLE: 0, UNKNOWN: 0`
- **Artifact:** Saved to `generated-results/benchmark_results_n100_<timestamp>.json`.

---

## 5. Architectural Alignment & Boundaries

| Component | Responsibility in StallBreaker | Tekion Platform Counterpart | Implementation Status |
|---|---|---|---|
| **Feasibility Guard** | Rejects unverified fitment, expired quotes, and immobilized movements | Tekion DMS Parts Catalog & Shop Safety Rules | Implemented (Local Pre-Check) |
| **OR-Tools CP-SAT Engine** | Multi-pass lexicographic optimization ($Z_1 \gg Z_3$) | Tekion Automations Core | Implemented (Live CP-SAT) |
| **Optimistic Concurrency** | Version-token check ($v_{proposal} == v_{snapshot}$) | Tekion Cloud Data Platform | Implemented (Local Store) |
| **Advisor Console** | Visual Gantt, hoist occupancy, explicit authorization | Tekion Service Advisor Dashboard | Implemented (React UI) |
| **DMS Integration** | Actual parts PO generation and technician dispatch | Tekion Production DMS | **Not Implemented (Prototype)** |
