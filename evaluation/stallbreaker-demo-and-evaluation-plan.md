# StallBreaker: Canonical Demonstration Specification & Evaluation Protocol

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-demo-and-evaluation-plan.md`  
**Phase:** StallBreaker Transition Evaluation — SR1.1 Consistency & Architecture Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Authority:** Joint Architecture Review Board (Operations Research, Fixed Ops, SaaS Architecture, AI Systems, Red-Team)  
**Primary Source:** `references/StallBreaker_Product_Validation_and_Winning_Strategy-1.pdf` [SB-PDF]  
**Date:** November 14, 2026  
**Status:** AUDITED & RECONCILED (SR1.1)  

> [!WARNING]
> ALL scenario data, inventory counts, ETAs, costs, customer promises, and performance metrics in this document are **SYNTHETIC**. They are illustrative design fixtures for demonstration and experimental protocol definition only. They do NOT represent measured dealership data, industry averages, or Tekion production telemetry.

---

## 1. Central Demonstration Narrative (One Sentence)

When a required parts line ETA slips on an in-progress repair order while the vehicle is immobilized on a scarce alignment bay, StallBreaker rejects an unavailable on-hand candidate (ATP = 0), prevents premature bay release while the vehicle is partially dismantled, evaluates a joint recovery across reservable sources and safe physical relocation, and demonstrates transactional resilience by aborting commit when a supplier warehouse revocation makes the chosen reservation stale, cleanly re-solving to an alternative before committing.

---

## 2. Canonical Demo Scenario Specification: `S-DEMO-01` (formerly `S-CANONICAL-01`)

> **[SR1.2.5 SCENARIO DIFFERENTIATION NOTICE]:**  
> This scenario is designated **`S-DEMO-01`** (Transactional Demonstration Fixture). It defines the end-to-end operational flow, MockTekionDmsAdapter integration, the 10-token pre-commit optimistic locking protocol, and race event `EVT-RACE-012` (Ford Escape, Sarah Jenkins $P=12:30$, $w=3$, $S_1$ out-of-stock).  
> The separate mathematical counterexample evaluating A2 vs. P3 jointness (Ford Explorer, Sarah Jenkins $P=13:30$, $w=1$, $S_1$ hotshot $55, commercial fleet RO-1051 $P=12:30$, $w=3$) is designated **`S-MATH-01`** and owned by [`stallbreaker-sr1.2.5-final-reconciliation.md`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/evaluation/stallbreaker-sr1.2.5-final-reconciliation.md). Generic references to "the canonical scenario" are deprecated.

### 2.1 Dealership Operating Baseline
* **Shop Hours:** 08:00 AM – 17:00 PM (540 shop-open minutes; discretised into 108 five-minute ticks; $t=0$ at 08:00 AM).
* **Disruption Event Timestamp:** 09:15 AM ($t = 15$).
* **Labor Gross Profit Baseline:** $GP_{\text{labor}} = \$110.00/\text{hr}$ (from Phase PR1.1 / PR2.1 financial reconciliation).

### 2.2 Primary Disrupted Repair Order: RO-1042
* **Repair Order ID:** `RO-1042` (DMS RO #48921).
* **Customer:** Sarah Jenkins (Customer Wait Type: `WAITING_IN_LOUNGE`; Promise Priority Weight $w_r = 3$).
* **Vehicle ID / VIN:** `V-1042` / `1FMCU9J93LUA12042` (2021 Ford Escape 2.0L EcoBoost).
* **Original Promise Time:** 12:30 PM ($t = 54$; immutable baseline).
* **Current Communicated Promise:** 12:30 PM ($t = 54$).
* **Blocked Operation:** `OP-201` — AC Compressor & Condenser Line Replacement.
  * *Standard Labor Time:* 60 minutes (12 five-minute ticks).
  * *Required Skill:* ASE HVAC Certification (`SKILL_HVAC_MASTER`).
  * *Required Bay Type:* `BAY_ALIGN_HEAVY` (Dedicated alignment / in-ground rack required for auxiliary subframe alignment).
* **Required Part:** `P-7231` (OEM Compressor Assembly, Motorcraft YCC-498).
  * *Quantity Required:* 1 unit.
  * *VIN Fitment Reference:* `FIT-FORD-2021-ESCAPE-20L-OEM` (`VERIFIED_ELIGIBLE`).
* **Assigned Technician:** `T3` (Mark Vance; Master Tech; Certifications: `SKILL_HVAC_MASTER`, `SKILL_ALIGN_MASTER`; Shift: 08:00–17:00).
* **Occupied Bay:** `B4` (Bay #4: Dedicated Alignment Rack & Heavy Mechanical Hoist).

### 2.3 Physical Facility & Holding Zone Status (at 09:15 AM / $t = 15$)
* **Bay B4:** Occupied by vehicle `V-1042`. Physical status: `PARTIALLY_DISMANTLED`.
* **Holding Zone H1 (Main Yard Staging):** Capacity = 3 vehicles; Occupancy = 3 vehicles (`FULL`).
* **Holding Zone H2 (Quick-Service Covered Buffer Slot):** Capacity = 1 vehicle; Occupancy = 0 vehicles (`AVAILABLE`).
  * *Relocation Transit Duration:* 15 minutes (3 ticks) via powered shop dolly / vehicle pusher.
  * *Prerequisite:* Vehicle must achieve `SAFE_TO_RELOCATE` status before transit begins.

### 2.4 Downstream Repair Orders Affected
* **RO-1051 (Downstream Bay Bottleneck):**
  * *Customer:* David Chen (`DROP_OFF`; Priority Weight $w_r = 1$; Promise: 16:30 PM / $t = 102$).
  * *Vehicle:* `V-1051` (2023 Ford F-150 Lightning; requires four-wheel precision radar alignment).
  * *Operation:* `OP-105` (Radar/Camera Alignment; Duration: 120 minutes / 24 ticks; Requires Bay `B4`).
  * *Original Scheduled Start:* 11:00 AM ($t = 36$). Stalled while `V-1042` occupies `B4`.
* **RO-1063 (Downstream Technician Bottleneck):**
  * *Customer:* Linda Rodriguez (`DROP_OFF`; Priority Weight $w_r = 1$; Promise: 17:00 PM / $t = 108$).
  * *Vehicle:* `V-1063` (2020 Ford Explorer; transmission valve body overhaul).
  * *Operation:* `OP-304` (Duration: 90 minutes / 18 ticks; Requires Technician `T3`).
  * *Original Scheduled Start:* 13:00 PM ($t = 60$).

### 2.5 Candidate Parts Sourcing Menu

```
+===================================================================================================================================+
|                                           CANONICAL SOURCING CANDIDATE FIXTURES                                                   |
+----+----------------------+---------+---------+-----+--------------------+---------------+---------------------+--------+-------+
| ID | Sourcing Source      | On-Hand | Alloc.  | ATP | Fitment / Warranty | Initial State | Usable Ready Time   | Direct | Rank  |
|    | Name & Location      | Qty     | Qty     | Qty | Verification Ref   | at 09:18 AM   | Low / Central / High| Freight| Gate  |
+----+----------------------+---------+---------+-----+--------------------+---------------+---------------------+--------+-------+
| S1 | Sister Store Alpha   | 1       | 1       | 0   | VERIFIED_ELIGIBLE  | REJECTED      | N/A                 | $0.00  | GATE  |
|    | (Northside Ford, 8mi)|         |         |     | FIT-FORD-P7231     | (ATP == 0)    | (Unusable)          |        | REJECT|
+----+----------------------+---------+---------+-----+--------------------+---------------+---------------------+--------+-------+
| S2 | Sister Store Beta    | 1       | 0       | 1   | VERIFIED_ELIGIBLE  | CONFIRMED     | Low: 11:40 AM (t44) | $18.00 | TOP   |
|    | (Metro Lincoln, 14mi)|         |         |     | FIT-FORD-P7231     | (10-min lease)| Cen: 12:05 PM (t49) | Hotshot| CANDI-|
|    |                      |         |         |     |                    | exp: 09:29 AM | High:12:45 PM (t57) | Courier| DATE  |
+----+----------------------+---------+---------+-----+--------------------+---------------+---------------------+--------+-------+
| S3 | AutoZone Commercial  | Avail.  | 0       | 1   | VERIFIED_ELIGIBLE  | CONFIRMED     | Low: 12:30 PM (t54) | $40.00 | BACKUP|
|    | (Expedite Hub, 22mi) | (Hub)   |         |     | ACES-P7231-AM      | (30-min quote)| Cen: 13:00 PM (t60) | Exped. | RECOV-|
|    |                      |         |         |     | Tier-2 Commercial  | exp: 09:48 AM | High:13:45 PM (t69) | Freight| ERY   |
+----+----------------------+---------+---------+-----+--------------------+---------------+---------------------+--------+-------+
| S4 | Unverified Jobber    | 2       | 0       | 2   | UNVERIFIED_SUB     | INFEASIBLE    | Low: 10:30 AM (t30) | $12.00 | GATE  |
|    | (Local Warehouse)    |         |         |     | Fitment Unmatched  | (Fitment fail)| (Inadmissible)      | Local  | REJECT|
+===================================================================================================================================+
```

*Canonical ETA Reconciliation:* S2 usable ready time is explicitly fixed as **Low: 11:40 AM ($t=44$) / Central: 12:05 PM ($t=49$) / High: 12:45 PM ($t=57$)**. All documents adopting 11:55/12:20 or typo "12:20 AM" are superseded by this fixture.

---

## 3. Physical Vehicle State Lifecycle Model

> **[SR1.2.4 RECONCILIATION NOTE]:**  
> The diagram below represents **Branch 1 (Mid-Repair Shortage Relocation to Holding Zone H2)**. The complete unified lifecycle model—including **Branch 2 (Post-Repair Mechanical Completion, Final Verification, Clearance Transit, and Customer Pickup Staging)**—is formally specified in [`evaluation/stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/evaluation/stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md). Both branches share identical hoist exclusivity and safety verification invariants.

A vehicle is a physical object that occupies space independently of technician labor intervals.

```
+----------------------------------------------------------------------------------------------------+
|                                    VEHICLE PHYSICAL STATE MACHINE                                  |
|                                                                                                    |
|   +-----------------------+         Technician Begins Teardown                                     |
|   |    IN_SERVICE_BAY     | -----------------------------------------> +-----------------------+   |
|   | (Wheels on, movable)  |                                            |  PARTIALLY_DISMANTLED |   |
|   +-----------------------+                                            |  (LOCKED ON HOIST)    |   |
|                                                                        +-----------------------+   |
|                                                                                    |               |
|                                                                                    | Tech Confirms |
|                                                                                    | Safe-Close    |
|                                                                                    v               |
|   +-----------------------+         Manager Relocation Approval        +-----------------------+   |
|   |     MOVE_APPROVED     | <----------------------------------------- |   SAFE_TO_RELOCATE    |   |
|   +-----------------------+                                            | (Wheels torqued/dolly)|   |
|               |                                                        +-----------------------+   |
|               | Porter Begins Physical Push                                                        |
|               v                                                                                    |
|   +-----------------------+         Porter Parks in Hold H2            +-----------------------+   |
|   |      IN_TRANSIT       | -----------------------------------------> |      IN_HOLDING       |   |
|   |  (15-min shop push)   |                                            | (BAY B4 IS RELEASED!) |   |
|   +-----------------------+                                            +-----------------------+   |
+----------------------------------------------------------------------------------------------------+
```

### Physical State Invariants
1. **Bay Occupancy Invariant:** Bay `B4` remains physically occupied until `VehicleState(V-1042) == IN_HOLDING`.
2. **Safe-Close Precondition:** `VehicleState` cannot transition to `SAFE_TO_RELOCATE` without authenticated technician confirmation (`T3` sign-off: fluid caps torqued, steering column locked, dolly mounted).
3. **Capacity Invariant:** `VehicleState` cannot transition to `IN_TRANSIT` unless target holding slot capacity (`Capacity(H2) - Occupancy(H2) \ge 1`) is strictly verified and reserved.

---

## 4. Revalidation Race Event Specification

* **Race Event ID:** `EVT-RACE-012`
* **Trigger Mechanism:** At 09:28:15 AM ($t = 15 + 13\text{m}15\text{s}$), a warehouse picker at Sister Store Beta (Metro Lincoln) pulls bin #B-14 to package part `P-7231` for courier pickup. The picker discovers that the compressor's electrical pin connector is cracked and terminal seals are broken.
* **Source System Action:** Sister Store Beta inventory controller marks unit condition as `DAMAGED_UNSERVICEABLE`.
* **Asynchronous Webhook:** Sister Store Beta emits webhook `inventory.reservation.revoked` with payload:
  `{"reservation_id": "RES-S2-8821", "status": "REVOKED", "reason_code": "PHYSICAL_DEFECT_DISCOVERED", "timestamp": "09:28:30"}`.
* **Simultaneous Expiration:** In addition, S2's 10-minute lease (issued at 09:19:00 AM) reaches expiry at 09:29:00 AM.
* **Manager Interaction:** Dealership Service Manager completes review and clicks **"Approve Plan S2"** at **09:30:00 AM**.
* **Pre-Commit Gate Execution:** Pre-commit validation runs at 09:30:02 AM, detects `status == REVOKED` and `now() > T_lease_expires`.
* **System Response:** Commit is **ABORTED**. System flags state as `STALE_REPLAN_REQUIRED`, releases tentative locks, notifies manager with plain-language cause, and automatically initiates CP-SAT re-solve with remaining candidate `S3`.

---

## 5. End-to-End Demonstration Storyboard & Master Timeline

```
+====================================================================================================================================+
|                                          CANONICAL DEMO MASTER EVENT TIMELINE                                                      |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| #  | Clock   | User / Shop Event      | StallBreaker System Action    | Physical / DMS State Changes     | Invariant Verified      |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 01 | 09:15 AM| DMS emits PART_DELAYED | Disruption Detector captures  | RO-1042 flagged PART_DELAYED;    | Disruption record logged|
|    | (t=15)  | on RO-1042 (P-7231).   | EVT-001; creates snapshot v12.| V-1042 PARTIALLY_DISMANTLED (B4).| with immutable hash.    |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 02 | 09:16 AM| Automated Candidate    | Candidate Generator queries   | S1: ATP=0 (Allocated to RO-881). | Candidate Gate: S1 is   |
|    | (t=15)  | Discovery queries.     | sources; runs Fitment & ATP.  | S2: ATP=1, Fitment Verified.     | REJECTED prior to solve.|
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 03 | 09:18 AM| Tentative Sourcing     | Adapter requests 10-min lease | S2 Reservation: REQUESTED ->     | Lease granted; exclusive|
|    | (t=15)  | Reservation on S2.     | token from Sister Store Beta. | CONFIRMED (Expires 09:29 AM).    | token held (RES-S2-8821)|
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 04 | 09:20 AM| Initial Joint CP-SAT   | Model evaluates S2 stay vs.   | Plan 1: S2 + Stay in B4.         | B4 release blocked      |
|    | (t=16)  | Solve (pre-safe-close).| S2 + Move. Move is INFEASIBLE | Plan 2: S2 + Move (DISABLED:     | because V-1042 cannot   |
|    |         |                        | because V-1042 safe_close=F.  | safe_to_move=False, H2 unresvd). | safely move yet.        |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 05 | 09:45 AM| Tech T3 finishes sub-  | Adapter accepts authenticated | VehicleState(V-1042) transitions | Safe-close invariant    |
|    | (t=21)  | frame tie-down; clicks | safe-close; updates vehicle   | to SAFE_TO_RELOCATE.             | verified; relocation is |
|    |         | "Safe-Close Confirmed".| state version to v4.          | Bay B4 STILL OCCUPIED by V-1042! | now legally eligible.   |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 06 | 09:46 AM| Event-triggered Re-plan| CP-SAT re-solves. Evaluates   | Recommended Plan S2-Relocate:    | Relocation feasible; H2 |
|    | (t=21)  | with vehicle movable.  | joint move to H2 vs hold B4.  | S2 courier (ETA 12:05), move to  | capacity (1) reserved.  |
|    |         |                        | Move selected: frees B4 early.| H2, frees B4 at 10:15 for RO1051.| No double-booking.      |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 07 | 09:48 AM| Plan presented to      | UI surfaces joint trade-off:  | Plan Status: PROPOSED ->         | Human governance:       |
|    | (t=21)  | Service Manager.       | $18 freight, RO-1042 on time, | APPROVAL_PENDING.                | Zero autonomous PO      |
|    |         |                        | RO-1051 saved from 2-hr stall.| Manager reviewing card.          | dispatch permitted.     |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 08 | 09:28 AM| External warehouse bin | Sister Store Beta marks unit  | Reservation RES-S2-8821 marked   | Asynchronous supplier   |
|    | (t=21)  | pick discovers crack.  | DAMAGED; emits REVOKED event. | REVOKED in background adapter.   | defect captured safely. |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 09 | 09:30 AM| Manager clicks         | Pre-commit Revalidation Gate  | Check Fails: Status == REVOKED;  | STALE-STATE ABORT:      |
|    | (t=22)  | "Approve Plan S2".     | executes atomic verification. | Lease expired at 09:29 AM.       | Plan rejected; zero bad |
|    |         |                        | ABORTS COMMIT.                | Live schedule remains v12.       | POs or moves committed. |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 10 | 09:30 AM| Automated Emergency    | CP-SAT instantly re-solves    | Plan S3-Relocate Generated:      | System survives supplier|
|    | (t=22)  | Re-plan with S3.       | excluding S2. Candidate S3    | S3 AutoZone Expedite ($40),      | failure gracefully      |
|    |         |                        | (AutoZone Expedite) selected. | ETA 13:00, RO-1042 late 35 min.  | without deadlock.       |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 11 | 09:32 AM| Manager approves Plan  | Pre-commit Revalidation Gate  | Revalidation PASSES: S3 quote    | Atomic commit validated |
|    | (t=22)  | S3.                    | executes; all tokens match.   | valid, H2 capacity open, V safe. | across all 10 tokens.   |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 12 | 09:33 AM| Transaction Commit     | MockAdapter creates draft PO; | VehicleState: MOVE_APPROVED;     | Schedule v13 committed. |
|    | (t=22)  | Coordinator executes.  | generates porter move ticket. | Schedule version updated to v13. | Porter notified.        |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 13 | 10:00 AM| Porter begins move     | Porter scans vehicle barcode. | VehicleState(V-1042) transitions | Bay B4 STILL NOT FREE   |
|    | (t=24)  | from B4 to H2.         | Move interval begins.         | to IN_TRANSIT.                   | during physical push!   |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 14 | 10:15 AM| Porter parks V-1042 in | Porter scans H2 slot barcode. | VehicleState: IN_HOLDING.        | Physical Relocation     |
|    | (t=27)  | H2 buffer slot.        | Bay B4 officially freed!      | B4 Occupancy: RELEASED (EMPTY).  | Complete. Bay freed.    |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 15 | 10:20 AM| Downstream RO-1051     | Tech pulls F-150 into B4;     | RO-1051 OP-105 Setup begins;     | Downstream alignment RO |
|    | (t=28)  | staged into Bay B4.    | commences radar alignment.    | finishes at 12:25 PM ($t=53$).   | completely recovered!   |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 16 | 13:00 PM| AutoZone courier docks;| Parts counter receives, tags; | Part P-7231 usable on bench;     | Part usable time match; |
|    | (t=60)  | part delivered.        | delivers to tech bench.       | OP-201 start enabled.            | no premature teardown.  |
+----+---------+------------------------+-------------------------------+----------------------------------+-------------------------+
| 17 | 13:05 PM| Tech T3 installs part  | Vehicle brought to open flat  | OP-201 active (13:05–14:05 PM);  | RO-1042 completed safely|
|    | (t=61)  | in open service stall. | bay; compressor installed.    | RO-1042 closes at 14:05 ($t=73$).| at shop contribution GP.|
+====================================================================================================================================+
```

---

## 6. Experimental Protocol & Policy Comparison Framework

To ensure scientific defensibility, StallBreaker evaluates **four strictly controlled policies** and **one primary ablation** across identical synthetic scenarios.

### 6.1 Formal Policy Definitions

```
+===================================================================================================================================+
|                                           CANONICAL EXPERIMENTAL POLICIES                                                         |
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| ID | Policy Label         | Sourcing Decision Logic                            | Shop Scheduling & Vehicle Movement Logic         |
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| P0 | Do Nothing (Static)  | No external recovery sourcing. Waits for OEM PDC   | Original static schedule remains frozen. Stalled |
|    |                      | weekly stock replenishment order.                  | vehicle sits in bay B4. Downstream work blocked. |
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| P1 | Strong Greedy        | Deterministic greedy heuristic: Filters fitment &  | Sequential heuristic: Upon part ETA resolution,  |
|    | Manager Baseline     | ATP > 0; selects candidate with earliest ETA; if   | assigns waiting work by Earliest Due Date (EDD); |
|    |                      | tied, lowest cost. Rejects unreservable options.   | moves vehicle only if bay is immediately blocked.|
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| A2 | Sequential           | Step 1: Evaluates sourcing candidates using multi- | Step 2: Fixes chosen source s* and passes part   |
|    | Optimisation         | criteria score (landed cost + local delay penalty);| ready time into the EXACT SAME CP-SAT scheduler  |
|    | (Primary Ablation)   | selects single "best" source candidate s*.         | as P3 to optimize vehicle, tech, and bay plan.   |
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| P3 | Joint Optimisation   | Solves sourcing selection x[r,s], vehicle movement m[v], holding space z[v,h], technician        |
|    | (StallBreaker)       | assignment a[o,t], and bay schedule c[o,b] SIMULTANEOUSLY in one joint CP-SAT model.             |
+----+----------------------+----------------------------------------------------+--------------------------------------------------+
| P2 | Historical PR2       | Evaluates sourcing candidates in an outer loop; runs CP-SAT schedule for each option.            |
|    | (Reference Only)     | NOTE: Assumes bay is freed upon job pause (ignores physical vehicle dismantling state).          |
+===================================================================================================================================+
```

### 6.2 Strict Fairness Rules Across All Policies
1. **Information Parity:** All policies receive identical event feeds, identical candidate quotes, identical fitment tables, and identical ATP timestamps.
2. **Constraint Parity:** All policies must obey the identical hard safety constraints (no vehicle moved while `PARTIALLY_DISMANTLED`, holding zone capacity $\le 1$, zero technician overlaps, zero bay overlaps).
3. **No Strawman P1:** P1 is NOT given invalid parts or permitted to violate safety. It represents an experienced, competent fixed operations manager following standard dealership best practices.
4. **The Core Ablation Test (A2 vs. P3):** The **only** difference between A2 and P3 is the coupling of source choice and schedule. A2 picks the best part first, then optimizes the schedule. P3 optimizes both jointly.

---

## 7. The Three Synthetic Falsification Scenarios

```
+===================================================================================================================================+
|                                           PRIMARY FALSIFICATION SCENARIOS                                                         |
+----+-----------------------------+----------------------------------------------+-------------------------------------------------+
| #  | Scenario Archetype          | Operational Setup & Constraint Topology      | Expected Theoretical Outcome                    |
+----+-----------------------------+----------------------------------------------+-------------------------------------------------+
| 01 | SCEN-01: Joint Dominance    | Specialized alignment bay B4 blocked. S1 has | P3 WINS over A2: A2 greedily picks S1 (arrives  |
|    | (Downstream Bottleneck)     | earlier ETA (11:30) but vehicle dismantling  | at 11:30), but vehicle cannot move until 12:00, |
|    |                             | prevents bay release. S2 arrives at 12:15,   | holding bay B4 hostage. P3 selects S2 with move |
|    |                             | perfectly synchronizing with hold slot H2    | to H2, allowing RO-1051 to run and saving $275  |
|    |                             | availability to save downstream RO-1051.     | in labor gross profit opportunity cost.         |
+----+-----------------------------+----------------------------------------------+-------------------------------------------------+
| 02 | SCEN-02: Method Equivalence | Standard mechanical bay. Ample open holding  | P3 TIES A2: Because no specialized bay or       |
|    | (Symmetric Unconstrained)   | space. Downstream jobs have flexible buffers.| technician constraint is binding, the locally   |
|    |                             | Single dominant supplier (fastest & cheapest)| earliest part is also globally optimal. Both    |
|    |                             | clearly dominates all dimensions.            | policies select S2 and produce identical plans. |
+----+-----------------------------+----------------------------------------------+-------------------------------------------------+
| 03 | SCEN-03: Sequential Parity /| High shop congestion (95% utilization).      | A2 TIES or OUTPERFORMS P3: Sequential subproblem|
|    | Compute Bounded             | Solver time limit capped at 1,500 ms. Large  | decomposes cleanly and finds optimal schedule in|
|    |                             | combinatorial search space (80 operations).  | 350 ms. P3 joint search hits timeout with 4.2%  |
|    |                             | Candidate S1 clearly dominates costs.        | optimality gap, producing equal or slightly     |
|    |                             |                                              | higher lateness due to search truncation.       |
+===================================================================================================================================+
```

---

## 8. Metric Taxonomy: Business vs. Engineering Reliability

```
+===================================================================================================================================+
|                                           METRIC SPECIFICATION & MEASUREMENT STANDARDS                                            |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| #  | Metric Name              | Cat. | Mathematical Definition & Units                  | Operational / Measurement Guardrails    |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| M1 | Weighted RO Lateness     | BIZ  | $\sum_{r} w_r \cdot \max(0, C_r - P_{\text{orig},r})$| Measured against IMMUTABLE original     |
|    |                          |      | (Minutes-Weighted).                              | promise. Never reset after delay.       |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| M2 | Promise Miss Count       | BIZ  | $\sum_{r} \mathbb{I}(C_r > P_{\text{orig},r})$   | Count of promised customer commitments  |
|    |                          |      | (Integer Count).                                 | broken across the operating day.        |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| M3 | Unabsorbed Stall Idle    | BIZ  | $\sum_{t} \text{IdleMinutes}(t) \cdot \mathbb{I}(\text{Stalled})$| Unproductive wait time while technician |
|    |                          |      | (Technician-Hours).                              | has no alternative dispatchable job.    |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| M4 | Incremental Sourcing Exp.| BIZ  | $\sum_{k} (C_{\text{freight}}(k) + \Delta C_{\text{part}}(k))$| Realized expedited courier and transfer |
|    |                          |      | (Synthetic Cost Units / Dollars).                | spend above standard OEM stock orders.  |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| M5 | Same-Day Completion Rate | BIZ  | $\frac{\text{ROs Completed before 17:00}}{\text{Total Eligible Disrupted ROs}}$ (%)| Fixed cohort definition. No post-hoc    |
|    |                          |      |                                                  | exclusion of complex repairs.           |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| R1 | Hard Constraint Viols.   | ENG  | Count of safety, fitment, overlap, or            | MUST BE ZERO in all policies. Any run   |
|    |                          |      | capacity violations (Integer).                   | with $R_1 > 0$ is disqualified.         |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| R2 | Stale-Commit Abort Rate  | ENG  | $\frac{\text{Aborted Commits}}{\text{Total Commit Attempts}}$ (%)| Verifies pre-commit revalidation gate   |
|    |                          |      |                                                  | catches race conditions reliably.       |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| R3 | Invalid Rejection Rate   | ENG  | $\frac{\text{Pre-Solve Rejected Candidates}}{\text{Total Sourcing Candidates}}$ (%)| Validates ATP=0 and fitment firewalls   |
|    |                          |      |                                                  | filter dangerous candidates pre-solve.  |
+----+--------------------------+------+--------------------------------------------------+-----------------------------------------+
| R4 | Solver Latency & Gap     | ENG  | p50, p95 solve latency (ms) and CP-SAT relative  | Evaluates computational feasibility on  |
|    |                          |      | optimality gap percentage.                       | standard hackathon developer hardware.  |
+===================================================================================================================================+
```

---

## 9. Statistical Experimental Protocol

1. **Experimental Unit:** One simulated dealership operating day (540 shop-open minutes, 50 jobs, 10 technicians, 12 bays, 3 parts disruptions).
2. **Paired Seeds (Common Random Numbers):** Experiments run across **30 independent pseudo-random seeds** (Seeds 101–130). All policies on Seed $S_i$ experience the exact same arrival sequence, initial shop layout, disruption timings, and true supplier transit realizations.
3. **Hypothesis Test (A2 vs. P3):**
   * *Null Hypothesis ($H_0$):* Mean paired difference in Weighted RO Lateness $\Delta M_1(P_3 - A_2) = 0$.
   * *Alternative Hypothesis ($H_1$):* Mean paired difference $\Delta M_1(P_3 - A_2) < 0$ (Joint achieves lower lateness).
4. **Statistical Significance & Uncertainty:** Report paired differences with **bootstrap 95% confidence intervals** (10,000 resamples).
5. **Statistical Power Caveat:** If evaluated on fewer than 15 seeds due to hackathon time constraints, results MUST be explicitly classified as **"EXPLORATORY SYNTHETIC SIMULATION — INSUFFICIENT STATISTICAL POWER TO REJECT NULL HYPOTHESIS"**.

---

**SR1.1 Audit Sign-Off:**
* Canonical scenario S-CANONICAL-01 established.
* S2 ETA ambiguity resolved (11:40 / 12:05 / 12:45). Typo 12:20 AM eliminated.
* Vehicle physical state lifecycle with safe-close preconditions formalized.
* Revalidation race condition grounded in physical supplier defect revocation.
* Baseline policies P0, P1, A2, P3 strictly defined; fairness rules enforced.
