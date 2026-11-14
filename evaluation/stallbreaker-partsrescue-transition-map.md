# StallBreaker: PartsRescue Transition & Component Migration Map

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-partsrescue-transition-map.md`  
**Phase:** StallBreaker Transition Evaluation — SR1.1 Consistency & Architecture Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Authority:** Joint Architecture Review Board (Enterprise SaaS Architect, AI Systems Architect, Automotive Domain Specialist)  
**Primary Sources:**  
- `evaluation/partsrescue-pr2.1-final-report.md` (PR2.1 Master Baseline)  
- `references/StallBreaker_Product_Validation_and_Winning_Strategy-1.pdf` [SB-PDF]  
**Date:** November 14, 2026  
**Status:** AUDITED & REQUALIFIED (SR1.1)  

> [!IMPORTANT]
> **Audit D Finding:** The previously asserted "60% architectural reuse" is hereby **excised and replaced** with an evidence-grounded, multi-dimensional qualitative assessment. Because zero lines of production implementation code were authored during PR1, PR1.1, PR2, or PR2.1 (which were strictly research, mathematical specification, and evaluation phases), **code reuse is formally 0% (unmeasured / non-existent)**. Realized reuse is concentrated in conceptual framing, data contracts, and operational research foundations.

---

## 1. Multi-Dimensional Reuse Taxonomy

To prevent misleading claims to hackathon judges, transition utility is decoupled across five distinct dimensions:

```
+===================================================================================================================================+
|                                           PARTSRESCUE ASSET REUSE TAXONOMY                                                        |
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| #  | Reuse Dimension          | Realized Assessment | Concrete Real-World Justification                                          |
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| 01 | **Conceptual Reuse**     | **VERY HIGH**       | The problem definition (UC04 parts shortage stall), user hierarchy (Parts   |
|    |                          | (Foundational)      | Counterperson vs. Service Advisor), economic cost baselines ($110/hr labor  |
|    |                          |                     | GP, hotshot courier rates), and rejection of Account 68A carry over 100%.   |
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| 02 | **Data Model Reuse**     | **HIGH**            | Entities `RepairOrder`, `RepairOperation`, `PartRequirement`, and           |
|    |                          | (Schema Blueprint)  | `CustomerAuthorization` carry forward directly. `InventoryPosition` and     |
|    |                          |                     | `SourcingCandidate` require targeted schema extensions (ATP, lease fields). |
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| 03 | **Component & Interface**| **HIGH**            | The `MockTekionDmsAdapter` specification, 6-state deterministic warranty     |
|    | **Specification Reuse**  | (Architectural)     | engine, audit log structure, and LLM explanation boundary carry over intact.|
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| 04 | **Implementation Code**  | **ZERO (0%)**       | No application code was written in prior phases in compliance with hackathon|
|    | **Reuse**                | (Non-Existent)      | governance rules. Code reuse cannot be claimed or measured.                 |
+----+--------------------------+---------------------+-----------------------------------------------------------------------------+
| 05 | **Engineering Effort**   | **SUBSTANTIAL**     | Saves approximately 25–35 hours of architecture deliberation by reusing the |
|    | **Savings**              | (Design Velocity)   | audited financial model, decoupled human approval gates, and mock adapters. |
+===================================================================================================================================+
```

---

## 2. Granular Component-Level Migration Table

```
+===================================================================================================================================+
|                                           GRANULAR COMPONENT MIGRATION MATRIX                                                     |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| #  | Architecture Component   | Existing PR2.1 State| Required StallBreaker SR1.1 Action  | Reuse Classification  | Confidence    |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 01 | **FastAPI Event Adapter**| REST/Webhook schema | Extend event schema with vehicle    | DIRECT REUSE          | HIGH          |
|    |                          | for RO status/parts.| physical state & lease webhooks.    | (Minor Extension)     | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 02 | **MockTekionDmsAdapter** | Read/write adapter  | Extend with VehicleState read and   | DIRECT REUSE          | HIGH          |
|    |                          | contract for ROs/POs| unposted draft PO write contracts.  | (Minor Extension)     | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 03 | **Immutable Audit Log**  | Event hash ledger   | Add version token tuple (schedule,  | DIRECT REUSE          | HIGH          |
|    |                          | with snapshot IDs.  | inventory, vehicle, quote versions).| (Minor Extension)     | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 04 | **Approval Framework**   | Dual-gate (Customer | Adapt to 3-tier risk routing: Low   | DIRECT REUSE          | HIGH          |
|    |                          | Scope vs. Staff PO).| (Counter), Med (Mgr), High (Mgr+Adv)| (Minor Adaptation)    | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 05 | **Fitment / Warranty**   | 6-State determin-   | Retain 6-state firewall; add fitment| DIRECT REUSE          | HIGH          |
|    | **Compliance Engine**    | istic rules engine. | verification gate as pre-solve check| (Unchanged Core)      | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 06 | **Parts Sourcing Model** | Multi-source pricing| Replace point ETA with Low/Cen/High | MODERATE REDESIGN     | HIGH          |
|    |                          | & 5-stage bench ETA.| usable ready times; add quote TTL.  | (Parameter Upgrade)   | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 07 | **Shop Scheduling Model**| Standard flexible   | Couple operation start to physical  | MODERATE REDESIGN     | HIGH          |
|    |                          | job-shop scheduler. | bay release & vehicle occupancy.    | (Constraint Coupling) | (Documented)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 08 | **CP-SAT Variables**     | Job start, tech, and| Add binary variables x[r,s], m[v],  | MAJOR EXTENSION       | HIGH          |
|    |                          | bay assignment vars.| z[v,h], and physical vehicle interval| (New Formulations)   | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 09 | **Objective Function**   | Omega(k) per-candi- | Replace with 5-tier Lexicographic   | COMPLETE REDESIGN     | HIGH          |
|    |                          | date scalar cost.   | Multi-Objective Hierarchy.          | (New Objective)       | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 10 | **Vehicle State Model**  | Conflated with job  | Build dedicated 6-state physical    | NEW BUILD             | HIGH          |
|    |                          | interval in bay.    | VehicleState machine & safe-close.  | (New Entity)          | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 11 | **Holding Zone Model**   | Non-existent        | Build physical Location entity with | NEW BUILD             | HIGH          |
|    |                          | (infinite capacity).| discrete capacity and dolly transit.| (New Entity)          | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 12 | **ATP / Reservation**    | Acknowledged but    | Build 7-state reservation lifecycle | NEW BUILD             | HIGH          |
|    | **Lifecycle**            | not gated.          | with 10-min exclusive lease token.  | (New Lifecycle)       | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 13 | **Pre-Commit Revalid.**  | Non-existent        | Implement 10-token atomic pre-commit| NEW BUILD             | HIGH          |
|    |                          | (immediate commit). | validation algorithm & stale abort. | (New Safety Gate)     | (Formulated)  |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 14 | **Transaction Coord.**   | Simple draft PO     | Implement Saga/Outbox coordinator   | NEW BUILD             | MEDIUM        |
|    |                          | write.              | with idempotency keys and retry log.| (New Transaction Flow)| (Inferred)    |
+----+--------------------------+---------------------+-------------------------------------+-----------------------+---------------+
| 15 | **Evaluation Simulator** | Discrete-event PR1  | Expand to paired-seed protocol      | MODERATE EXTENSION    | HIGH          |
|    |                          | simulation design.  | evaluating P0, P1, A2, and P3.      | (Protocol Upgrade)    | (Documented)  |
+===================================================================================================================================+
```

---

## 3. Detailed Component Transition Analysis

### 3.1 Directly Reusable Assets (No Redesign Required)
1. **The $110/hr Labor Gross Profit Baseline:** Phase PR1.1 reconciled the dealership economic baseline, proving that labor gross margin ($110/hr) governs opportunity cost, not posted door rates ($160/hr). StallBreaker adopts this exact figure for financial reporting.
2. **Excised Account 68A Sublet Rule:** PR2.1 completely struck the fabricated "Account 68A auto-billing rule". StallBreaker retains this correction, modeling freight as a standard parts operating expense.
3. **Decoupled Two-Gate Authorization:** Customer scope authorization (SMS price approval) remains strictly segregated from staff procurement authorization (Manager PIN).
4. **Deterministic Six-State Warranty Firewall:** Sourcing candidates must pass the auditable 6-state warranty engine before entering the optimization candidate set.

### 3.2 Components Requiring Redesign
1. **From Pareto Sieve to Joint Lexicographic CP-SAT:** PartsRescue filtered candidates via an offline Pareto dominance sieve ($K \le 8$), then solved schedules sequentially. StallBreaker replaces this with a **single joint CP-SAT model** where source selection variables $x_{r,s}$ directly constrain operation start times.
2. **From Point ETA to Bounded Uncertainty Scenarios:** The 5-stage bench timeline ($T_{\text{bench}}$) is upgraded from a deterministic point estimate to low, central, and high usable bench intervals.

### 3.3 New Architectural Builds Required
1. **`VehicleState` Physical Entity:** Decouples vehicle presence from technician flag-time. Bay $B4$ cannot be freed until physical relocation to holding zone $H2$ completes.
2. **Seven-State Inventory Reservation Lifecycle:** Implements exclusive 10-minute leases, explicit ATP gating, and asynchronous supplier revocation handling.
3. **Ten-Token Pre-Commit Revalidation Gate:** Implements optimistic concurrency verification across schedule, vehicle, inventory, and quote tokens immediately prior to execution.

---

## 4. Engineering Feasibility & Resource Allocation

Under the Reduced MVP scope, the new builds are strictly delimited:
* **Vehicle State Machine:** Simple in-memory / relational state machine (~40 lines of Python).
* **Reservation Lifecycle:** State machine with TTL timer check (~60 lines of Python).
* **Pre-Commit Validation:** Ten conditional checks executed in a single atomic transaction (~50 lines of Python).
* **CP-SAT Joint Formulation:** Native Google OR-Tools model with ~250 boolean variables and ~150 interval variables (~200 lines of Python).

**Total New Implementation Burden:** Estimated at **350–500 lines of Python logic** plus synthetic data fixtures. This is completely tractable for a 2–4 person team within a hackathon timeframe.

---

**SR1.1 Audit Sign-Off:**
* Ungrounded "60% reuse" figure excised; code reuse explicitly certified as 0% (unmeasured).
* Multi-dimensional reuse taxonomy established across conceptual, data model, component, code, and design effort.
* Granular 15-component migration table specified with documented classifications.
* New architectural builds bounded to realistic hackathon scope.
