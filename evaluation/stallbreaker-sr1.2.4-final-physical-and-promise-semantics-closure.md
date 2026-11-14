# StallBreaker: SR1.2.4 — Final Physical State & Customer-Promise Semantics Closure

> [!NOTE]
> **[SR1.2.5 RECONCILIATION NOTICE]:**  
> Entity state separation (decoupling the vehicle entity from bay release) and the formal designation of Milestone 1 (66.7%) as the primary authoritative benchmark have been finalized in [`evaluation/stallbreaker-sr1.2.5-final-reconciliation.md`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/evaluation/stallbreaker-sr1.2.5-final-reconciliation.md). The mathematical counterexample analyzed herein is formally identified as scenario **`S-MATH-01`**.

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md`  
**Phase:** SR1.2.4 — Final Physical State and Customer-Promise Semantics Closure  
**Standard Compliance:** `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Board:** Automotive Service Operations Specialist, Operations Research Scientist, Constraint Programming Specialist, Safety-Critical State-Machine Reviewer, Independent Hackathon Research Evaluator  
**Date:** November 14, 2026  
**Classification:** MATHEMATICAL & OPERATIONAL SPECIFICATION [SYNTHETIC FIXTURE SCEN-01, HAND-WORKED]  

---

## 1. Executive Summary & Audit Mandate

Phase SR1.2.3 introduced an explicit post-repair clearance interval ($T_{\text{clear}} = 2$ ticks = 10 minutes) and recalculated canonical scenario fixture **SCEN-01**, demonstrating a 66.7% weighted customer lateness improvement for joint policy P3 over sequential baseline A2, with an algebraically invariant 110-minute lateness advantage.

However, an independent adversarial review identified two remaining modeling ambiguities:
1. **Safety-State Ordering Ambiguity (Correction A):** In SR1.2.3, the vehicle was described as transitioning to `SAFE_TO_DRIVE = TRUE` immediately upon installation completion, while its clearance interval simultaneously included torque verification and inspection sign-off. In safety-critical automotive service operations, a vehicle must **never** be declared safe to move before safety verification has formally passed.
2. **Customer-Promise Completion Semantics (Correction B):** The objective function in SR1.2.3 calculated RO-1042 customer lateness against installation completion ($t_{\text{install\_end}}$), whereas the vehicle was not confirmed in customer pickup staging until clearance completion ($t_{\text{install\_end}} + T_{\text{clear}}$). The exact operational milestone represented by a "customer promise" ($P_{\text{orig}, r}$) was not formalized across all repair order types.

This deliverable provides final closure on both issues without altering the canonical SCEN-01 inputs, source candidates, or core A2/P3 policies.

---

## 2. Correction A: Physical Vehicle State Lifecycle Model

### 2.1 The Two Operational Paths from Teardown
In automotive dealership service bays, a vehicle placed onto a hoist and partially disassembled enters physical state `PARTIALLY_DISMANTLED`. From this state, exactly two physical exit branches exist:

```
+===================================================================================================================================+
|                                        UNIFIED PHYSICAL VEHICLE LIFECYCLE MODEL                                                   |
+===================================================================================================================================+
                                            [ IN_SERVICE_BAY ]
                                                    |
                                                    | (Technician Begins Teardown)
                                                    v
                                         [ PARTIALLY_DISMANTLED ]
                                             (Locked on Hoist)
                                                    |
                       +----------------------------+----------------------------+
                       |                                                         |
         [ BRANCH 1: MID-REPAIR SHORTAGE ]                         [ BRANCH 2: POST-REPAIR DEPARTURE ]
         (Vehicle Incomplete -> Needs Staging)                     (Vehicle Repaired -> Customer Ready)
                       |                                                         |
                       | (Tech Performs Safe-Close Tie-Down)                     | (Tech Completes Parts Installation)
                       v                                                         v
              [ SAFE_TO_RELOCATE ]                                  [ REPAIR_MECHANICALLY_COMPLETE ]
             (Wheels Torqued / Dolly Mounted)                                    |
                       |                                                         | (Formal Safety & Torque Check Begins)
                       | (Manager Approval & Holding Reserved)                   v
                       v                                           [ FINAL_VERIFICATION_IN_PROGRESS ]
               [ MOVE_APPROVED ]                                                 |
                       |                                        +----------------+----------------+
                       | (Porter Begins Physical Push)          | (Checks Pass)                   | (Checks Fail)
                       v                                        v                                 v
                 [ IN_TRANSIT ]                           [ SAFE_TO_MOVE ]              [ VERIFICATION_FAILED ]
                       |                                        |                        (Rework Lock Active)
                       | (Parked in Staging Slot H2)            | (Lowered; Driven Out)
                       v                                        v
                 [ IN_HOLDING ]                       [ IN_CLEARANCE_TRANSIT ]
             (BAY B4 IS RELEASED!)                              |
                                                                | (Parked in Customer Staging Lane)
                                                                v
                                                   [ IN_CUSTOMER_PICKUP_STAGING ]
                                                                |
                                                                | (Bay Sensor / Tech Lane Clear Confirmation)
                                                                v
                                                     [ BAY_CONFIRMED_CLEAR ]
                                                      (BAY B4 IS RELEASED!)
+===================================================================================================================================+
```

---

### 2.2 Post-Repair State & Event Definitions

To eliminate safety-ordering ambiguity, Branch 2 specifies six distinct, sequentially ordered states/events:

1. **`REPAIR_MECHANICALLY_COMPLETE` (Event / State):**
   - *Precondition:* Technician completes physical installation of all replacement parts (e.g., AC bracket bolted, compressor aligned, drive belt routed).
   - *Physical Location:* Vehicle remains elevated on the mechanical hoist in Bay $B_4$.
   - *Safety Status:* Not yet certified road-ready or roll-ready. Tools and jacks remain in active bay perimeter.

2. **`FINAL_VERIFICATION_IN_PROGRESS` (Active Interval):**
   - *Precondition:* `REPAIR_MECHANICALLY_COMPLETE == TRUE`.
   - *Activities:* Master technician executes formal quality assurance protocol:
     - Calibrated torque wrench verification on critical suspension/subframe fasteners.
     - Fluid level check (refrigerant pressure, engine coolant, power steering).
     - Electronic diagnostic scan tool clearance of pending DTCs.
     - Digital multi-point inspection (MPI) sign-off in shop terminal.
   - *Physical Location:* Vehicle remains secured in Bay $B_4$ under technician supervision.

3. **`SAFE_TO_MOVE` (Safety Gate State):**
   - *Precondition:* All mandatory inspection checklist items in `FINAL_VERIFICATION_IN_PROGRESS` pass with digital technician signature.
   - *Safety Status:* Vehicle is authenticated as structurally sound, mechanically complete, and safe for operator transit.
   - *Failure Branch:* If any check fails (e.g., stripped thread, persistent DTC, fluid leak), the vehicle transitions to `VERIFICATION_FAILED_REWORK_REQUIRED`. The vehicle is **prohibited from moving**, the bay lock is maintained, and an urgent alert is dispatched to the shop foreman.

4. **`IN_CLEARANCE_TRANSIT` (Active Physical Movement Interval):**
   - *Precondition:* `SAFE_TO_MOVE == TRUE` AND `PickupStagingLot.AvailableSpaces >= 1`.
   - *Physical Actions:* Hoist safety locks disengaged; vehicle lowered to shop floor; vehicle started and driven (or rolled) by porter along designated shop exit corridor toward the customer pickup lot.
   - *Occupancy:* Vehicle physically exits Bay $B_4$ envelope and traverses shop transit lane.

5. **`IN_CUSTOMER_PICKUP_STAGING` (Terminal Facility Location):**
   - *Precondition:* Vehicle safely parked in designated customer pickup lot stall; parking brake set; keys tagged and delivered to service cashier/advisor key locker.
   - *Customer Milestone:* Vehicle is 100% available for customer key handover and drive-away.

6. **`BAY_CONFIRMED_CLEAR` (Resource Release Event):**
   - *Precondition:* Vehicle has completely crossed the yellow boundary line of Bay $B_4$ AND technician confirms hoist arms stowed, tools cleared, and floor dry.
   - *Resource State:* Bay $B_4$ occupancy transitions from $1 \to 0$. The bay lock is officially released in the DMS / shop scheduler. Downstream vehicle $V_2$ is authorized to enter.

---

### 2.3 Strict Safety & Physical Invariants

The following formal invariants must hold across all execution traces:

- **Invariant INV-1 (No Premature Movement):** A vehicle shall not transition to `IN_CLEARANCE_TRANSIT` or initiate any physical motion until its status is `SAFE_TO_MOVE`.
- **Invariant INV-2 (Verification Precedence):** `VehicleState == SAFE_TO_MOVE` strictly requires `VerificationPassed(v) == TRUE` with authenticated technician credentials.
- **Invariant INV-3 (Conservation of Mass / Continuous Occupancy):** At all times $t \in [0, T_{\max}]$, every vehicle $v$ occupies exactly one designated spatial coordinate (Bay, Transit Corridor, Holding Zone, or Customer Staging). A vehicle can never disappear or exist in two locations simultaneously:
  $$\text{Location}(v, t) \in \{B_4, \text{Corridor}, H_2, \text{PickupStaging}\} \quad \forall t$$
- **Invariant INV-4 (Strict Hoist Exclusivity):** For single-capacity Bay $B_4$:
  $$\text{Occupancy}(B_4, t) \le 1 \quad \forall t$$
  Downstream vehicle $V_2$ cannot cross into Bay $B_4$ until event `BAY_CONFIRMED_CLEAR` has registered for vehicle $V_1$:
  $$\text{start}(I_{V2}^{B_4}) \ge t(\text{BAY\_CONFIRMED\_CLEAR}(V_1))$$
- **Invariant INV-5 (Non-Inference of Bay Release):** Bay availability shall **never** be inferred from repair completion. Repair completion triggers verification, not bay vacancy.
- **Invariant INV-6 (Destination Availability Precondition):** A vehicle shall not disengage from the hoist or enter transit unless the target destination capacity is confirmed:
  $$\text{AvailableCapacity}(\text{Destination}) \ge 1$$
- **Invariant INV-7 (Strict Domain Separation of $H_2$ vs. Pickup Staging):** Holding Zone $H_2$ is reserved exclusively for incomplete vehicles awaiting parts or bay space (`IN_HOLDING`). Fully repaired, verified vehicles move strictly to Customer Pickup Staging. The saturation of $H_2$ does not restrict access to Customer Pickup Staging.

---

### 2.4 Canonical Parameterization of $T_{\text{clear}}$ (10 Minutes)

The canonical fixture maintains:
$$T_{\text{clear}} = 2 \text{ ticks} = 10 \text{ minutes} \quad \text{[SYNTHETIC FIXTURE ASSUMPTION]}$$

To eliminate ambiguity without inventing unsupported empirical measurements, the canonical fixture models $T_{\text{clear}}$ as two discrete 5-minute operational phases:
- **Tick 1 ($\Delta t_{\text{verify}} = 1$ tick = 5 min):** Covers `FINAL_VERIFICATION_IN_PROGRESS`. Vehicle is on the hoist. Torque checks, DTC scan, and MPI digital sign-off occur. Passes at end of tick $\implies$ `SAFE_TO_MOVE`.
- **Tick 2 ($\Delta t_{\text{transit}} = 1$ tick = 5 min):** Covers `IN_CLEARANCE_TRANSIT`. Hoist lowering (2 min), vehicle transit to customer pickup lot (2 min), and bay housekeeping/lane clear sign-off (1 min). At end of tick $\implies$ `IN_CUSTOMER_PICKUP_STAGING` and `BAY_CONFIRMED_CLEAR`.

*Both sub-durations are explicitly classified as `[SYNTHETIC FIXTURE MODELLING CONVENTIONS]`. In actual dealership deployments, these intervals vary with vehicle chassis type and facility layout.*

---

## 3. Correction B: Customer-Promise Completion Semantics

### 3.1 Investigation of Existing Definitions & Industry Standards

In dealership fixed operations and DMS architectures (including Tekion ARC, CDK Drive, and Reynolds ERA):

| Milestone | Technical Identifier | Operational Meaning | Customer Perception |
| :--- | :--- | :--- | :--- |
| **Milestone 1** | `SERVICE_WORK_COMPLETE` | Technician punches off RO line; labor flags complete. Vehicle remains in shop. | Internal labor metric. Customer cannot collect car yet. |
| **Milestone 2** | `CUSTOMER_READY_STAGED` | Vehicle inspected, washed/parked in delivery stall, keys in cashier drawer, customer SMS dispatched. | **True Customer Promise Milestone.** Vehicle is ready for customer key handover. |

### 3.2 Authoritative Workspace Definition for SCEN-01

To ensure absolute consistency across all documents, the customer promise lateness formulation (Equation C25) is hereby clarified:

$$\text{late}_r = \max\left(0,\ C_r - P_{\text{orig}, r}\right) \tag{C25-Clarified}$$

where the completion milestone $C_r$ is defined as follows:

- **For Retail Customer Repair Orders (e.g., RO-1042, Sarah Jenkins):**
  The customer promise $P_1 = 13:30$ PM ($t = 66$) represents **Vehicle Ready for Customer Collection**. Therefore, completion is measured at arrival in customer pickup staging:
  $$C_{\text{RO-1042}} \equiv t(\text{IN\_CUSTOMER\_PICKUP\_STAGING}) = t_{\text{install\_end}} + T_{\text{clear}}$$

- **For Commercial Fleet Repair Orders (e.g., RO-1051, Fleet F-150):**
  We evaluate two rigorous, distinct operational interpretations:
  - **Interpretation 1 (Standard Milestone — Service Hoist Completion):** Commercial fleet SLA governs bay availability and alignment calibration completion ($C_{\text{RO-1051}} \equiv t_{\text{service\_complete}} = t_{\text{start}} + 24$). This directly preserves Equation (C25) $\text{end}_{\text{last\_op}}$.
  - **Interpretation 2 (Comprehensive Milestone — Customer Delivery Staging):** Fleet driver pickup SLA governs vehicle availability in the fleet outbound staging lot ($C_{\text{RO-1051}} \equiv t_{\text{fleet\_ready}} = t_{\text{start}} + 24 + T_{\text{clear}}$).

**Critical Finding:** As mathematically proven below, **under both interpretations, Sarah Jenkins' (RO-1042) lateness is identically 0 minutes, and P3's absolute lateness reduction over A2 is invariant at exactly 110 minutes!**

---

## 4. Recomputation of Canonical Scenario SCEN-01

### 4.1 Input Parameters (Strictly Preserved)
- Shift Origin: 08:00 AM ($t = 0$), Tick Size: 5 min.
- RO-1042 Promise $P_1$: $t = 66$ (13:30 PM), Priority Weight $w_1 = 1.0$.
- RO-1051 Promise $P_2$: $t = 54$ (12:30 PM), Priority Weight $w_2 = 3.0$.
- RO-1042 Install Duration: 12 ticks (60 min). Bay $B_4$ required exclusively.
- RO-1051 Operation Duration: 24 ticks (120 min). Bay $B_4$ required exclusively. Ready at $t = 24$.
- $T_{\text{clear}}$ Duration: 2 ticks (10 min) = 1 tick verification + 1 tick transit.
- Holding Zone $H_2$: Capacity 1, occupied until $t = 60$.
- Customer Pickup Lot: $\ge 1$ stall available at all relevant times `[SYNTHETIC ASSUMPTION]`.
- Candidate $S_1$: Usable at $t = 27$ (10:15 AM), Freight Cost \$55.00, OEM Approved.
- Candidate $S_2$: Usable at $t = 49$ (12:05 PM), Freight Cost \$18.00, OEM Approved.

---

### 4.2 Policy A2 (Sequential Optimization) Trace

1. **Subproblem 1 (Decoupled Sourcing):**
   - Evaluates $S_2$ vs $S_1$ against local RO-1042 promise $P_1 = 66$ (13:30 PM).
   - Under $S_2$: $T_{\text{ready}} + d_{\text{install}} + T_{\text{clear}} = 49 + 12 + 2 = 63$ (13:15 PM) $\le 66$. Local lateness = 0, Cost = \$18.00.
   - Under $S_1$: Ready at $t = 41$ (11:25 AM) $\le 66$. Local lateness = 0, Cost = \$55.00.
   - Sourcing subproblem selects **$s^* = S_2$**, blind to Bay $B_4$'s downstream schedule.
2. **Subproblem 2 (CP-SAT Scheduling with $S_2$ Fixed):**
   - $t = 21 \to 49$ (09:45–12:05 PM): Vehicle $V_1$ locked in Bay $B_4$ awaiting parts. $H_2$ saturated $\implies$ cannot relocate.
   - $t = 49$ (12:05 PM): Part arrives. Installation commences.
   - $t = 61$ (13:05 PM): Installation finishes $\implies$ `REPAIR_MECHANICALLY_COMPLETE`.
   - $t = 61 \to 62$ (13:05–13:10 PM): `FINAL_VERIFICATION_IN_PROGRESS`. Fasteners torqued, DTCs cleared.
   - $t = 62$ (13:10 PM): Quality checks pass $\implies$ `SAFE_TO_MOVE`.
   - $t = 62 \to 63$ (13:10–13:15 PM): `IN_CLEARANCE_TRANSIT`. Lowered, driven to pickup staging.
   - $t = 63$ (13:15 PM): Vehicle logged `IN_CUSTOMER_PICKUP_STAGING`. Bay sensor confirms `BAY_CONFIRMED_CLEAR`.
   - $t = 63$ (13:15 PM): Vehicle $V_2$ (RO-1051) enters Bay $B_4$ and begins ADAS calibration.
   - $t = 87$ (15:15 PM): RO-1051 service operation complete ($63 + 24 = 87$).
   - *(If fleet clearance modeled: $t = 89$ / 15:25 PM in fleet staging).*

**A2 Lateness Evaluation:**
- RO-1042 Customer Ready: $C_1 = 63$ (13:15 PM) vs $P_1 = 66$ (13:30 PM) $\implies \mathbf{\text{late}_1 = 0\text{ min}}$.
- RO-1051 Service Complete: $C_2 = 87$ (15:15 PM) vs $P_2 = 54$ (12:30 PM) $\implies \mathbf{\text{late}_2 = 33\text{ ticks} = 165\text{ min}}$.
- *(If fleet staging: $C_2 = 89 \implies \text{late}_2 = 35\text{ ticks} = 175\text{ min}$).*

---

### 4.3 Policy P3 (Joint Source-and-Schedule Optimization) Trace

1. **Joint CP-SAT Evaluation:**
   - Evaluates sourcing, vehicle states, bay occupancy, and downstream promise jointly.
   - Selects **$s^* = S_1$** (\$55.00), recognizing that earlier part arrival clears Bay $B_4$ before commercial SLA collapse.
2. **Shop Execution:**
   - $t = 27$ (10:15 AM): Part $S_1$ arrives via hotshot courier. Installation begins immediately.
   - $t = 39$ (11:15 AM): Installation finishes $\implies$ `REPAIR_MECHANICALLY_COMPLETE`.
   - $t = 39 \to 40$ (11:15–11:20 AM): `FINAL_VERIFICATION_IN_PROGRESS`. Fasteners torqued, DTCs cleared.
   - $t = 40$ (11:20 AM): Quality checks pass $\implies$ `SAFE_TO_MOVE`.
   - $t = 40 \to 41$ (11:20–11:25 AM): `IN_CLEARANCE_TRANSIT`. Lowered, driven to pickup lot.
   - $t = 41$ (11:25 AM): Vehicle logged `IN_CUSTOMER_PICKUP_STAGING`. Bay sensor confirms `BAY_CONFIRMED_CLEAR`.
   - $t = 41$ (11:25 AM): Vehicle $V_2$ (RO-1051) enters Bay $B_4$ and begins ADAS calibration.
   - $t = 65$ (13:25 PM): RO-1051 service operation complete ($41 + 24 = 65$).
   - *(If fleet clearance modeled: $t = 67$ / 13:35 PM in fleet staging).*

**P3 Lateness Evaluation:**
- RO-1042 Customer Ready: $C_1 = 41$ (11:25 AM) vs $P_1 = 66$ (13:30 PM) $\implies \mathbf{\text{late}_1 = 0\text{ min}}$.
- RO-1051 Service Complete: $C_2 = 65$ (13:25 PM) vs $P_2 = 54$ (12:30 PM) $\implies \mathbf{\text{late}_2 = 11\text{ ticks} = 55\text{ min}}$.
- *(If fleet staging: $C_2 = 67 \implies \text{late}_2 = 13\text{ ticks} = 65\text{ min}$).*

---

### 4.4 Objective Function & Metric Comparison

```
+===================================================================================================================================+
|                                              CANONICAL SCEN-01 FINAL COMPARISON TABLE                                             |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Operational Metric                | Sequential Baseline Policy (A2)       | Joint Optimization Policy (P3)                        |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Sourcing Candidate Selected       | $S_2$ (Sister Dealership Transfer)    | $S_1$ (Local Hotshot Expedited Courier)               |
| Direct Freight Expenditure        | $18.00                                | $55.00 (+$37.00 Tier-4 premium)                       |
| Part Usable-Ready Time            | t = 49 (12:05 PM)                     | t = 27 (10:15 AM) [110 min earlier]                   |
| RO-1042 Installation Window       | t = 49 -> 61 (12:05 - 13:05 PM)       | t = 27 -> 39 (10:15 - 11:15 AM)                       |
| Post-Repair Verification Window   | t = 61 -> 62 (13:05 - 13:10 PM)       | t = 39 -> 40 (11:15 - 11:20 AM)                       |
| Clearance Transit Window          | t = 62 -> 63 (13:10 - 13:15 PM)       | t = 40 -> 41 (11:20 - 11:25 AM)                       |
| V1 Confirmed in Pickup Staging    | t = 63 (13:15 PM)                     | t = 41 (11:25 AM)                                     |
| Bay B4 Confirmed Clear            | t = 63 (13:15 PM)                     | t = 41 (11:25 AM) [110 min earlier]                   |
| RO-1051 Service Window            | t = 63 -> 87 (13:15 - 15:15 PM)       | t = 41 -> 65 (11:25 - 13:25 PM)                       |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Sarah Jenkins (RO-1042) Lateness  | 0 minutes (Staged 15m before promise) | 0 minutes (Staged 125m before promise)                |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| INTERPRETATION 1: SERVICE COMPLETE|                                       |                                                       |
| RO-1051 Lateness (vs P2 = 54)     | 165 minutes (33 ticks)                | 55 minutes (11 ticks) [SAVED: 110 MINUTES]            |
| Weighted Objective Z1             | 1.0(0) + 3.0(33) = 99.0 weighted ticks| 1.0(0) + 3.0(11) = 33.0 weighted ticks                |
| Relative Improvement              | BASELINE                              | 66.7% REDUCTION ((99.0 - 33.0) / 99.0)                |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| INTERPRETATION 2: FLEET STAGING   |                                       |                                                       |
| RO-1051 Lateness (vs P2 = 54)     | 175 minutes (35 ticks)                | 65 minutes (13 ticks) [SAVED: 110 MINUTES]            |
| Weighted Objective Z1             | 1.0(0) + 3.0(35) = 105.0 ticks        | 1.0(0) + 3.0(13) = 39.0 ticks                         |
| Relative Improvement              | BASELINE                              | 62.9% REDUCTION ((105.0 - 39.0) / 105.0)              |
+===================================================================================================================================+
```

### 4.5 The Absolute Invariance Theorem
Under both promise interpretations, and for **any** clearance duration $T_{\text{clear}} \ge 0$:
$$\Delta \text{Lateness} = \text{Lateness}(A2) - \text{Lateness}(P3) = 110 \text{ minutes (invariant)}$$
$$\Delta Z_1 = Z_1(A2) - Z_1(P3) = 3.0 \times 22 \text{ ticks} = 66.0 \text{ weighted ticks (invariant)}$$

**Conclusion:** The **66.7%** figure (Interpretation 1) is confirmed as the authoritative canonical result matching Equation (C25). Interpretation 2 is documented as a comprehensive sensitivity variant yielding **62.9%**. Both confirm the identical underlying reality: joint optimization recovers exactly 110 minutes of downstream delay by spending \$37.00 on expedited freight.

---

## 5. Adversarial Self-Review

The board audited the corrected model against all ten mandatory adversarial criteria:

```
+===================================================================================================================================+
|                                                  ADVERSARIAL SELF-REVIEW MATRIX                                                   |
+----+----------------------------------------------+--------+----------------------------------------------------------------------+
| #  | Challenge Question                           | Status | Evidence & Enforcing Mechanism                                       |
+----+----------------------------------------------+--------+----------------------------------------------------------------------+
| 01 | Can vehicle move before verification passes? | PASS   | Invariant INV-1 & INV-2: Movement strictly gated by SAFE_TO_MOVE.    |
| 02 | Can vehicle occupy bay & lot simultaneously? | PASS   | Invariant INV-3: Mutually exclusive location mapping across ticks.   |
| 03 | Can B4 release while vehicle is inside it?   | PASS   | Invariant INV-4 & INV-5: Release strictly gated by BAY_CONFIRMED_CLR |
| 04 | Can next vehicle enter before confirmation?  | PASS   | Invariant INV-4: start(I_v2) >= t(BAY_CONFIRMED_CLEAR(v1)).          |
| 05 | Can vehicle leave without available stall?   | PASS   | Invariant INV-6: Departure requires AvailableCapacity(Lot) >= 1.     |
| 06 | Does equation measure exact promise point?   | PASS   | Equation C25-Clarified explicitly distinguishes C_r milestones.      |
| 07 | Are A2 and P3 evaluated under identical rules| PASS   | Exact same 6-state sequence, T_clear=2, and safety rules applied.    |
| 08 | Are synthetic assumptions separated?         | PASS   | T_clear=2 and lot capacity explicitly labeled [SYNTHETIC ASSUMPTION].|
| 09 | Do all dependent docs use authoritative defs?| PASS   | Unified index points to this document as sole owning authority.      |
| 10 | Does 66.7% claim follow from corrected inputs| PASS   | Fully traced arithmetic: (99.0 - 33.0)/99.0 = 66.7% (66.0/99.0).     |
+===================================================================================================================================+
```

---

## 6. Narrowed Jointness Claim & Evidence Scope

### 6.1 Permitted Claim Formulation
The workspace strictly adopts the following narrowed claim:

> **"SCEN-01 demonstrates that joint source-and-schedule optimization (P3) can outperform the specified source-first, fixed-source sequential baseline (A2) under the fixture's physical and operational constraints. The demonstration is a hand-worked mathematical derivation on a synthetic scenario and does not establish that every conceivable sequential architecture (such as those incorporating shadow prices, iterative re-bidding, or downstream feedback) is inferior to joint optimization."**

### 6.2 Explicit Hierarchy of Evidence
1. **Hand-Worked Mathematical Demonstration:** `ESTABLISHED` via SCEN-01 in this document.
2. **Computational Solver Benchmark:** `NOT ESTABLISHED`. No OR-Tools or CP-SAT code has been compiled or run.
3. **Empirical Dealership Measurement:** `NOT ESTABLISHED`. No field telemetry or production DMS data has been collected.

---

## 7. Cross-Document Correction & Supersession Index

| Document | Previous Defect | Applied Correction in SR1.2.4 |
| :--- | :--- | :--- |
| `stallbreaker-sr1.2.3-physical-clearance-reconstruction.md` | `SAFE_TO_DRIVE = TRUE` coincided with start of clearance verification. | Superseded by Section 2: 6-state sequence with explicit safety gate. |
| `stallbreaker-sr1.2.3-final-closure-report.md` | Customer promise milestone conflated service complete with pickup ready. | Superseded by Section 3: Equation C25-Clarified with dual interpretation. |
| `stallbreaker-demo-and-evaluation-plan.md` (Sec 3) | State machine covered only mid-repair relocation (Branch 1). | Integrated with Branch 2 (post-repair completion and departure). |
| `stallbreaker-source-of-truth-index.md` | Owned domains 04 and 29 required alignment. | Updated to designate SR1.2.4 as canonical owning document. |

---

$$\mathbf{PHASE\ SR1.2.4\ STATUS:\ COMPLETED\ —\ FULLY\ CLOSED}$$
