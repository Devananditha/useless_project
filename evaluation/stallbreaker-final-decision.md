# StallBreaker: Final Product Adoption & Architecture Decision

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-final-decision.md`  
**Phase:** StallBreaker Transition Evaluation — SR1.1 Consistency & Architecture Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Decision Authority:** Joint Architecture Review Board (Product Strategy, Fixed Ops, OR Science, SaaS Architecture, AI Systems, Red-Team)  
**Date:** November 14, 2026  
**Status:** AUDITED & CONSOLIDATED (SR1.1) — AWAITING EXPLICIT USER APPROVAL  

---

## FINAL DECISION

```
+===================================================================================================================================+
|                                                                                                                                   |
|                                       ADOPT STALLBREAKER WITH REDUCED MVP                                                         |
|                                                                                                                                   |
+===================================================================================================================================+
```

---

## 1. What This Decision Formally Establishes

The team adopts **StallBreaker — Feasibility-Gated Service Recovery Optimiser** as its definitive concept for the Tekion Tek-Qubit Hackathon 2026, aligned with **Theme 1 — AI & Automation, UC04: Service Parts Shortage Resolver Agent**.

This decision is conditioned on **ten binding MVP constraints** (The "Reduced MVP"):
1. **Single Simulated Dealership Rooftop:** One parts-blocked repair order evaluated at a time.
2. **Synthetic Data Fixtures Only:** All dataset records, inventory positions, quotes, and timestamps must display explicit `[SYNTHETIC]` labels.
3. **MockTekionDmsAdapter Contract:** System connects strictly via local mock adapters. No live Tekion ARC APIs or partner credentials are required or assumed.
4. **Bounded Combinatorial Scale:** Optimization bounded to $\le 50$ operations, $\le 10$ technicians, $\le 12$ service bays, and $2–3$ sourcing options.
5. **Physical Vehicle State Machine:** Implements the dedicated `VehicleState` entity (`PARTIALLY_DISMANTLED`, `SAFE_TO_RELOCATE`, `MOVE_APPROVED`, `IN_TRANSIT`, `IN_HOLDING`). Bay release requires physical relocation completion.
6. **Seven-State Inventory Lease Lifecycle:** Enforces the 7-state reservation model (`NONE`, `REQUESTED`, `CONFIRMED`, `EXPIRED`, `FAILED`, `REVOKED`, `RELEASED`) with a 10-minute exclusive lease token. Candidates with $\text{ATP} == 0$ are deterministically rejected pre-solve.
7. **Ten-Token Pre-Commit Revalidation Gate:** Optimistic concurrency verification checks schedule, vehicle, inventory, quote, and reservation tokens immediately before commit. Any mismatch aborts execution to a clean re-solve.
8. **Fair Experimental Baselines:** Evaluates against the strong **P1 Greedy Manager** baseline and the primary **A2 Sequential Optimisation** ablation across identical paired synthetic seeds.
9. **Subordinate LLM Layer:** The hosted LLM is strictly restricted to plain-language explanation and note extraction. Zero decision or write authority. Full LLM-off deterministic fallback required.
10. **Zero Autonomous Real-World Actions:** All purchase orders are generated as `UNPOSTED` draft requisitions. Zero automated real-world orders or retail customer SMS dispatches.

---

## 2. Core Decision Justification

### 2.1 The Architectural Flaw in PartsRescue PR2.1
The Phase PR2.1 audit established a sound economic cost function ($GP_{\text{labor}} = \$110/\text{hr}$) and excised Account 68A, but retained a fundamental physical modeling flaw:
* PartsRescue assumed that when an operation encounters a parts stall, the bay can be released for other work.
* In physical dealership reality, a vehicle with a dismantled subframe or detached steering rack **physically locks the hoist**, preventing any other vehicle from entering the stall regardless of technician availability.
* StallBreaker resolves this by decoupling the vehicle's physical location interval $I_v^{\text{bay}}$ from active labor intervals, modeling safe-close authorization, holding space capacity ($H2$), and dolly relocation transit.

### 2.2 Sourcing Integrity: ATP Gating and Lease Concurrency
* PartsRescue accepted raw inventory counts from supplier screens. If a supplier showed "1 on-hand", the system assumed availability.
* In reality, that single unit is frequently allocated to another repair order or damaged in the bin.
* StallBreaker adds deterministic ATP gating ($\text{ATP} = \text{On-Hand} - \text{Allocated} - \text{Damaged}$), pre-solve candidate filtering, exclusive 10-minute reservation leases, and asynchronous defect revocation handling.

### 2.3 Mathematical Jointness vs. Sequential Decomposition
* PartsRescue evaluated sourcing candidates sequentially in an outer loop, running the scheduler separately for each option.
* StallBreaker formulates a **single joint CP-SAT model** where source selection variables $x_{r,s}$, vehicle relocation $m_v$, holding assignment $z_{v,h}$, and shop intervals are solved simultaneously.
* This allows the optimizer to select a source with a slightly later arrival time if that source synchronizes with vehicle safe-close and holding space availability to save a high-value downstream alignment job.

---

## 3. Evidence-Grounded Reuse Assessment

In strict compliance with `.cursor/rules/research-standards.mdc`, the unsupported "60% architectural reuse" claim from early drafts is **formally excised**:
* **Implementation Code Reuse:** **0% (Unmeasured / Non-existent)**. No application code was written during PR1, PR1.1, PR2, or PR2.1.
* **Conceptual & Economic Reuse:** **100%**. Reuses the $110/hr labor GP baseline, hotshot courier cost models, rejection of Account 68A, and dual-gate approval principles.
* **Data Contract Reuse:** **Substantial**. Reuses the schemas for `RepairOrder`, `RepairOperation`, `PartRequirement`, and `CustomerAuthorization`, extending them with `VehicleState` and `SourceReservation`.
* **Design Velocity Savings:** Saves an estimated 25–35 hours of architecture deliberation by carrying forward validated fixed-ops concepts.

---

## 4. Primary Risks & Engineering Mitigations

```
+===================================================================================================================================+
|                                           STALLBREAKER PRIMARY RISKS & MITIGATIONS                                                |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| #  | Identified Operational Risk | Prob. | Impact | Engineering Mitigation Strategy                                               |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| 01 | **A2 vs. P3 Ablation Null   | MED   | HIGH   | If paired experiment across 30 seeds shows P3 does not outperform A2 with     |
|    | Result (No Joint Edge)**    |       |        | statistical significance, honestly report the null result and reframe novelty |
|    |                             |       |        | on data integrity (ATP gate + physical vehicle state + pre-commit safety).    |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| 02 | **CP-SAT Solver Latency     | LOW   | MED    | Bound model strictly to $\le 50$ operations and 3 candidates. Set hard solver |
|    | Tail Spikes (>2,500 ms)**   |       |        | time limit at 2,500 ms. If timeout occurs, fall back to best feasible         |
|    |                             |       |        | incumbent or deterministic greedy heuristic.                                  |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| 03 | **Tekion ARC Internal Over- | MED   | HIGH   | Execute prioritized mentor validation inquiry during hackathon. If ARC already|
|    | lap Discovered by Mentor**  |       |        | optimizes mid-day stalls, position StallBreaker as an algorithmic extension   |
|    |                             |       |        | service integrated via Automotive Partner Cloud (APC).                        |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| 04 | **Demo Race Condition       | LOW   | MED    | Use deterministic replay script `S-CANONICAL-01` with frozen timestamps and   |
|    | Flakiness During Pitch**    |       |        | seeds. Provide a pre-recorded 30-second screen capture backup in slide deck.  |
+----+-----------------------------+-------+--------+-------------------------------------------------------------------------------+
| 05 | **Scope Creep into UC01     | MED   | HIGH   | Strictly enforce negative constraints: No appointment booking, no customer    |
|    | Appointment Rescheduling**  |       |        | intake, no general dispatch. Re-sequence ONLY downstream jobs sharing B4/T3. |
+===================================================================================================================================+
```

---

## 5. What This Decision Does NOT Authorize

This adoption decision explicitly does **NOT** grant authority to:
1. Write application, solver, or frontend code.
2. Build prototypes, mock servers, or test scripts.
3. Create PowerPoint slides or pitch collateral.
4. Modify, overwrite, or delete any historical PartsRescue PR1, PR1.1, PR2, or PR2.1 files.
5. Stage, commit, or push any changes to Git.
6. Invent unverified Tekion ARC API endpoints.
7. Claim measured dealership financial ROI without explicit `[SYNTHETIC]` labels.

---

## 6. Formal Gate Determination & Next Steps

```
+===================================================================================================================================+
|                                           SR1.1 AUDIT READINESS GATE VERDICT                                                      |
+===================================================================================================================================+
|                                  READY FOR PR3 TECHNICAL SPECIFICATION                                                           |
|                                                                                                                                   |
| 1. All six StallBreaker deliverables are fully reconciled and internally consistent.                                             |
| 2. Reservation semantics, concurrency guarantees, and pre-commit checks are mathematically formalized.                            |
| 3. The canonical demo scenario S-CANONICAL-01 resolves all prior timeline and ETA discrepancies.                                 |
| 4. The CP-SAT joint optimization model is rigorously specified with physical vehicle occupancy intervals.                         |
| 5. Experimental baselines P0, P1, A2, and P3 enforce strict fairness and falsifiability.                                         |
| 6. Code reuse is honestly certified as 0%, eliminating ungrounded percentages.                                                    |
+===================================================================================================================================+
```

**Next Phase (Awaiting Explicit User Instruction):**  
Upon receiving explicit user direction, the team will proceed to **Phase PR3: Technical Architecture & System Specification**, detailing the database schemas, Pydantic data contracts, MockTekionDmsAdapter endpoints, and CP-SAT Python solver recipes for StallBreaker.

---

**SR1.1 Audit Sign-Off:**
* Final transition decision re-confirmed under the 10 binding constraints of the Reduced MVP.
* Flawed 60% reuse claim excised.
* Full alignment with Canonical Scenario S-CANONICAL-01 verified.
* All autonomous execution halted pending user review.
