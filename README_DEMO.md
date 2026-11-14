# StallBreaker — Live CP-SAT Service Recovery Demonstrator
## Tekion Tek-Qubit Hackathon 2026 | Theme 1: AI & Automation (UC04)

> **Core Thesis:** In automotive dealerships, service bay immobilization caused by parts shortages is an intractable operational bottleneck. Selecting part sources purely on freight cost without considering downstream hoist schedules triggers severe fleet delays. StallBreaker jointly solves parts sourcing and bay scheduling via **Google OR-Tools CP-SAT**, eliminating **66.7% of weighted lateness** and recovering **110 minutes of downstream delay** on the canonical dealership disruption fixture.

---

## 1. Quickstart — Running the Live Demonstrator

### Prerequisites
- Python 3.10+ (with `ortools` and `fastapi` / `uvicorn`)
- Node.js 18+ (with `npm`)

### Step 1: Start Backend (FastAPI + CP-SAT Solver)
From the repository root (`TEKION-HACKATHON-2026`):

```bash
# Terminal 1: Start the backend API service (Port 8000)
uvicorn backend.main:app --reload --port 8000
```
*Health check:* [http://localhost:8000/api/health](http://localhost:8000/api/health)

### Step 2: Start Frontend (Vite + React + TypeScript)
In a second terminal:

```bash
# Terminal 2: Start the interactive presentation console (Port 5173)
cd frontend
npm run dev
```
*Open in browser:* [http://localhost:5173](http://localhost:5173)

---

## 2. Automated Test Verification (16/16 Acceptance Tests)

Execute the full suite of deterministic mathematical, state-machine, physical safety, and optimistic concurrency tests:

```bash
python -m pytest backend/tests/test_acceptance.py -v
```

### Verified Acceptance Gates:
1. `test_01_canonical_s_math_01_a2_arithmetic`: Baseline A2 selects S2; B4 free at 13:15 ($t=63$), RO-1051 finish 15:15 ($t=87$), 33 ticks lateness.
2. `test_02_canonical_s_math_01_p3_arithmetic`: Joint P3 selects S1; B4 free at 11:25 ($t=41$), RO-1051 finish 13:25 ($t=65$), 11 ticks lateness.
3. `test_03_ninety_nine_versus_thirty_three_weighted_ticks`: Exact $99.0$ vs $33.0$ weighted ticks ($w=3.0$).
4. `test_04_sixty_six_point_seven_percent_reduction`: $(99 - 33) / 99 = 66.7\%$ relative reduction in weighted lateness.
5. `test_05_one_hundred_ten_minute_delay_difference`: Exactly 22 ticks (110 minutes) downstream finish delta for fleet RO-1051.
6. `test_06_unsafe_movement_rejection`: Unassembled/partially dismantled vehicle cannot transition to holding without wheel remount signoff.
7. `test_07_h2_capacity_reservation_before_movement`: Staging movements blocked when holding capacity $= 0$.
8. `test_08_bay_no_overlap`: Hoist exclusivity strictly enforced; no simultaneous bay occupancy.
9. `test_09_technician_no_overlap`: Technician K1 cannot execute concurrent operations.
10. `test_10_return_to_bay_precedence`: Return transit to Bay B4 cannot start before the bay is vacated and available.
11. `test_11_source_atp_eligibility`: Supplier source with ATP $= 0$ rejected by eligibility filter.
12. `test_12_invalid_fitment_rejection`: Unverified parts fitment rejected prior to solver inclusion.
13. `test_13_expired_quote_rejection`: Expired supplier quote rejected before solver inclusion.
14. `test_14_inventory_version_conflict`: External reservation increments snapshot version (v14 ➔ v15).
15. `test_15_stale_proposal_cannot_be_committed`: Outdated proposal rejected with `STALE_SNAPSHOT` (HTTP 409).
16. `test_16_new_proposal_requires_new_human_approval`: Automatic re-solve requires explicit human advisor authorization; no auto-commit.

---

## 3. The 3-Act Live Demonstration Script

The demonstrator is structured into three acts that prove the technical necessity, operational validity, and production robustness of StallBreaker:

### Act 1: The Canonical Stall (Immobilized Vehicle on Scarce Bay)
- **Scenario:** `Act 1: Canonical S-MATH-01`
- **Physical Situation:**
  - RO-1042 (BMW X5) is partially dismantled on Bay B4 (the shop's only heavy-duty alignment hoist).
  - Wheels and hub assembly are detached; the vehicle **cannot roll** and holding area H2 is saturated.
  - S1 (Metro Courier): $55 freight, arrives 10:15 (usable 10:30).
  - S2 (Local Dealer): $18 freight, arrives 11:45 (usable 12:00).
- **Execution:** Click **Run Solver (Live CP-SAT)**.
- **What Happens:**
  - The backend formulates and executes Google OR-Tools CP-SAT in real-time (~30 ms).
  - **A2 Sequential Baseline:** Sourcing selects S2 to save $37 in freight. Bay B4 is held hostage until 13:15 ($t=63$). Fleet customer RO-1051 is bumped to 15:15 ($t=87$), accumulating **165 minutes of lateness** (99.0 weighted ticks).
  - **StallBreaker P3:** Joint solver recognizes hoist scarcity and chooses S1 ($55). Bay B4 is released at 11:25 ($t=41$). RO-1051 finishes at 13:25 ($t=65$).
  - **Result:** **66.7% reduction in weighted lateness**, saving **110 minutes of downstream delay** for a net freight difference of only +$37.

---

### Act 2: Physical State Sensitivity (Rollable Vehicle Relocation)
- **Scenario:** Select `Act 2: S-MATH-01-ROLLABLE` from the dropdown.
- **Physical Situation:**
  - Technician K1 completes emergency wheel remount. RO-1042 transitions to `SAFE_TO_RELOCATE`.
  - Holding area H2 has 1 available stall; transit duration is 3 ticks (15 min) each way.
- **Execution:** Click **Run Solver (Live CP-SAT)**.
- **What Happens:**
  - The CP-SAT solver dynamically discovers that the vehicle can be evacuated to holding area H2.
  - Bay B4 is evacuated at 10:00 ($t=24$).
  - Fleet RO-1051 enters Bay B4 immediately and completes on-hoist service at 12:00 ($t=48$) with **0 minutes of lateness**!
  - RO-1042 returns to B4 at 12:10 ($t=50$), installs the lower-cost S2 part ($18), and finishes with only 5 minutes lateness.
  - **Result:** Proves that StallBreaker responds dynamically to physical mechanics rather than hard-coded heuristics.

---

### Act 3: Optimistic Concurrency & The Stale-Snapshot Race
- **Scenario:** Return to `Act 1: Canonical S-MATH-01`.
- **Physical Situation:**
  - Advisor reviews P3 proposal (based on snapshot v14 with S1 allocated).
  - While the advisor is reviewing, an external warranty job (RO-1099) claims the last unit of S1 at the metro hub.
- **Execution:**
  1. Click **Simulate S1 Stock Race (Act 3)**.
     - Observe: S1 ATP drops to 0; snapshot advances from **v14 ➔ v15**.
  2. Click **Advisor Approve & Commit**.
- **What Happens:**
  - The backend detects that the proposal was calculated against v14 while the store is now v15.
  - **Commit is ABORTED.** A prominent alert displays: `STALE SNAPSHOT DETECTED`.
  - StallBreaker automatically re-solves under snapshot v15 (which now selects S2 due to S1 unavailability).
  - Crucially: **No automated commit occurs**. The new proposal is placed in `PENDING_APPROVAL` status, enforcing mandatory human advisor authorization before any parts are ordered.

---

## 4. Multi-Seed CP-SAT Benchmark (N=100 Paired Seeds)

Click **N=100 Benchmark** in the top navigation bar to execute 100 paired CP-SAT instances in under 7 seconds.

### Summary Metrics Across 100 Real Solver Runs:
- **Total Instances Solved:** 100 paired seeds (Random seed 42)
- **Mean P3 CP-SAT Solve Time:** **30.8 ms**
- **Mean A2 Baseline Solve Time:** **31.2 ms**
- **P3 Win/Tie Rate:** **100.0%** (95 Wins, 5 Ties, 0 Losses)
- **Mean Weighted Lateness Reduction:** **71.2%**
- **Mean Downstream Delay Savings:** **119.4 minutes** per disruption incident
- **Solver Status Distribution:** 100% `OPTIMAL` (0 `INFEASIBLE`, 0 `TIMEOUT`)

---

## 5. Architectural Alignment with Tekion Ecosystem

| Component | Responsibility in StallBreaker | Tekion Platform Counterpart |
|---|---|---|
| **Feasibility Guard** | Rejects unverified fitment, expired quotes, and immobilized movements | Tekion DMS Parts Catalog & Shop Safety Rules |
| **OR-Tools CP-SAT Engine** | Dual-objective lexicographic constraint programming ($Z_1 \gg Z_3$) | Tekion Automations & Service Dispatch Core |
| **Optimistic Concurrency** | Version-token validation ($v_{proposal} == v_{snapshot}$) prevents stock races | Tekion Multi-Tenant Cloud Data Platform |
| **Advisor Console** | Visual Gantt, hoist occupancy, and human-in-the-loop authorization | Tekion Service Advisor Dashboard |
