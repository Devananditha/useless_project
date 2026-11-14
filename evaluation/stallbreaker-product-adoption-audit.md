# StallBreaker: Product Adoption & Competitive Differentiation Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-product-adoption-audit.md`  
**Phase:** StallBreaker Transition Evaluation — SR1.1 Consistency & Architecture Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Authority:** Joint Architecture Review Board (Product Strategy, Automotive Domain, Competitive Intelligence, Innovation Red-Team)  
**Primary Sources:**  
- `references/StallBreaker_Product_Validation_and_Winning_Strategy-1.pdf` [SB-PDF]  
- `references/tekion-themes.pdf` (Official UC04 Source)  
**Date:** November 14, 2026  
**Status:** AUDITED & RECONCILED (SR1.1)  

---

## 1. Executive Summary & Audit Mandate

This audit evaluates the architectural and product justification for transitioning from PartsRescue to **StallBreaker: Feasibility-Gated Service Recovery Optimiser** for the Tekion Tek-Qubit Hackathon 2026.

The audit board confirms that StallBreaker is **NOT an entirely new product**, but rather an **architecturally necessary evolution of the same fundamental problem**: an in-progress repair order stalls on an unavailable parts line, and dealership personnel must determine the optimal recovery path.

StallBreaker's core innovation is the **joint decision model**: rather than evaluating sourcing options in isolation and subsequently rescheduling technician tasks, StallBreaker jointly optimizes parts sourcing feasibility, available-to-promise (ATP) inventory reservations, physical vehicle location and dismantling state, holding space capacity, technician skills, and downstream repair order schedules within a single constrained optimization pass — protected by pre-commit revalidation.

The 35-page StallBreaker validation report ([SB-PDF], p. 1) delivered an honest verdict that this board formally endorses:
> *"The revised direction is a meaningful design improvement, but it is not yet a proven product gap. The strongest version is a feasibility-gated recovery optimiser that chooses and validates a complete plan across part source, usable arrival time, vehicle location/movability, technicians, bays and downstream customer commitments. The proof must show this joint decision beating a strong source-selection plus schedule-replanning baseline."*

---

## 2. What StallBreaker Actually Proposes

### 2.1 The Original Proposal vs. The Joint Evolution
* **Original StallBreaker Concept ([SB-PDF], pp. 4–6):** An event-driven parts shortage resolver that evaluated sourcing options sequentially: for each candidate, it ran a CP-SAT re-plan, ranked the resulting schedules, requested tiered human approval, and committed the schedule version.
* **The Revised "Joint" Evolution ([SB-PDF], pp. 7–8):** Eliminates sequential candidate evaluation by solving source selection $x_{r,s}$, physical vehicle relocation $m_v$, holding assignment $z_{v,h}$, and shop schedule intervals simultaneously. It adds authoritative VIN fitment gates, 7-state inventory lease semantics, low/central/high ETA uncertainty bounds, and atomic pre-commit token revalidation.

### 2.2 The Five Core Architectural Additions Over PartsRescue

```
+===================================================================================================================================+
|                                           STALLBREAKER CORE ARCHITECTURAL ADDITIONS                                               |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| #  | Architectural Dimension     | PartsRescue PR2.1 Baseline         | StallBreaker SR1.1 Specification                         |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| 01 | **Physical Vehicle State**  | Conflated with labor interval. Bay | Dedicated `VehicleState` machine. Bay B4 cannot release  |
|    |                             | assumed free when job is paused.   | while vehicle is `PARTIALLY_DISMANTLED`.                 |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| 02 | **ATP Inventory Gate**      | Acknowledged "Available" field,    | Deterministic gate: $\text{ATP} = \text{On-Hand} -       |
|    |                             | but did not filter candidates.     | \text{Allocated} - \text{Damaged}$. ATP=0 candidate out. |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| 03 | **Joint Decision Coupling** | Multi-objective Pareto sieve on    | Single joint CP-SAT model coupling source selection to   |
|    |                             | isolated parts candidates.         | bay release and downstream alignment jobs.               |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| 04 | **Pre-Commit Revalidation** | Non-existent; immediate PO draft   | Atomic 10-token check before commit; aborts on stale     |
|    |                             | creation upon manager click.       | lease, version mismatch, or supplier defect revocation.  |
+----+-----------------------------+------------------------------------+----------------------------------------------------------+
| 05 | **ETA Uncertainty Bounds**  | Point estimate (5-stage bench).    | Explicit Low / Central / High usable ready scenarios.    |
+===================================================================================================================================+
```

---

## 3. Official Hackathon Alignment: UC04 vs. UC01 Scope Boundaries

StallBreaker aligns directly with **Theme 1 — AI & Automation, UC04: Service Parts Shortage Resolver Agent** (`references/tekion-themes.pdf`).

### 3.1 Strict UC04 Alignment Verification
* **Triggering Event:** Real-time capture of `PART_DELAYED`, `ETA_SLIPPED`, or `WRONG_PART_RECEIVED` on an active RO.
* **Parts Evaluation:** Verifies sister-store inventory and commercial vendor expedite options.
* **Schedule Re-sequencing:** Re-plans bay and technician assignments to prevent stall downtime.
* **Human-in-the-Loop:** Risk-tiered managerial approval; zero autonomous purchase order issuance.

### 3.2 Guarding Against UC01 Scope Creep
UC01 defines the *Autonomous Appointment & Dispatch Orchestrator* (customer booking, initial shop loading, and advisor dispatch).
* **The Scope Boundary:** StallBreaker is an **in-progress disruption recovery engine**, NOT a general appointment booking or daily shop dispatch platform.
* **Downstream Scope Boundary:** StallBreaker re-sequences ONLY those downstream repair orders that share physical resources (the occupied alignment bay `B4` or the certified technician `T3`) with the disrupted vehicle. It does NOT reschedule the entire dealership appointment ledger.

---

## 4. Competitive Differentiation & Novelty Assessment

### 4.1 What Incumbents Actually Provide
As established in `references/StallBreaker_Product_Validation_and_Winning_Strategy-1.pdf` (pp. 8–10):
* **Tekion Live Service Control Center:** Real-time WIP tracking, advisor/technician performance, bottlenecks, and exception monitoring. StallBreaker CANNOT claim novelty merely by displaying a service bay board.
* **Tekion Automatic RO & Tech Scheduling / Scheduler AI:** Automated appointment booking and technician job matching. StallBreaker CANNOT claim novelty by assigning qualified technicians to operations.
* **Tekion OEM Integrations Catalogue:** Integrated parts catalog, parts inventory, parts order, and parts locator across 35 OEMs. StallBreaker CANNOT claim that Tekion has "no parts visibility."
* **Dealer-FX / CDK / Reynolds & Reynolds:** Live parts availability on RO lines, in-service queues, and dispatch prioritization.

### 4.2 The Four-Tier Differentiation Classification

```
+===================================================================================================================================+
|                                           FOUR-TIER DIFFERENTIATION CLASSIFICATION                                                |
+----+-----------------------------+----------------------------------------------------+------------------------------------------+
| Tier Category                     | Specific Functional Capabilities                   | Defensible Competitive Posture           |
+----+-----------------------------+----------------------------------------------------+------------------------------------------+
| **TIER 1:**                       | 1. Joint Feasibility-Gated Optimization across     | Genuine operational whitespace. No known |
| **CORE NOVEL CONTRIBUTION**       |    reservable supply, physical vehicle location,   | DMS or shop management platform solves   |
| (Defensible Blue Ocean)           |    holding space, and downstream bay bottlenecks.  | this joint combinatorial problem in one  |
|                                   | 2. Physical vehicle occupancy interval modeled as  | mathematical model.                      |
|                                   |    independent constraint from labor hours.        |                                          |
+----+-----------------------------+----------------------------------------------------+------------------------------------------+
| **TIER 2:**                       | 1. Seven-state exclusive lease reservation model.  | Essential production safety engineering. |
| **SUPPORTING MECHANISM**          | 2. Pre-commit 10-token atomic revalidation gate.   | Proves transaction reliability and stops |
| (Production Robustness)           | 3. Saga/outbox pattern with idempotency tracking.  | race conditions before PO release.       |
+----+-----------------------------+----------------------------------------------------+------------------------------------------+
| **TIER 3:**                       | 1. Cross-store inventory queries and EDI orders.   | Established automotive software features.|
| **EXISTING INDUSTRY CAPABILITY**  | 2. Technician certification matching to jobs.      | Present in Tekion ARC, CDK, Dealer-FX.   |
| (Baseline Mechanics)              | 3. Service bay WIP status boards and timers.       | Must be treated as baseline assumptions. |
+----+-----------------------------+----------------------------------------------------+------------------------------------------+
| **TIER 4:**                       | 1. Extent of Tekion's internal mid-repair parts-   | Unconfirmed from public sources. Must be |
| **UNVERIFIED PRODUCT-GAP**        |    stall re-planning capabilities in ARC/T1.       | framed as a testable hypothesis to       |
| **HYPOTHESIS**                    | 2. Live write permissions for reservation locks.   | validate with Tekion mentors.            |
+===================================================================================================================================+
```

---

## 5. Over-Engineering Risk & Hackathon Feasibility

The board red-teams the complexity of StallBreaker against the hackathon constraints:
* **The Danger:** Building a multi-agent framework, distributed message brokers, IoT vehicle trackers, or predictive ML ETA estimators would guarantee project failure within a hackathon window.
* **The Architectural Remedy (The Reduced MVP):**
  * Reject multi-agent architectures in favor of **one single Python CP-SAT service**.
  * Use local relational PostgreSQL state rather than distributed microservices.
  * Model vehicle physical states with a simple deterministic 6-state machine.
  * Restrict external systems to local `MockTekionDmsAdapter` contracts.
  * Ground all demo scenarios in the sealed canonical fixture `S-CANONICAL-01`.

---

## 6. Audit Verdict

```
+===================================================================================================================================+
|                                           PRODUCT ADOPTION AUDIT VERDICT                                                          |
+===================================================================================================================================+
| 1. Product Direction: APPROVED — Transition to StallBreaker: Feasibility-Gated Service Recovery Optimiser is sound.             |
| 2. UC Alignment: FULLY COMPLIANT — Strictly adheres to Theme 1, UC04 without invading UC01 appointment territory.                 |
| 3. Novelty Stance: DEFUSED & GROUNDED — Excised exaggerated claims of competitor absence; framed as joint decision novelty.       |
| 4. Architecture Scope: BOUNDED — Enforces the 10 binding constraints of the Reduced MVP.                                          |
+===================================================================================================================================+
```

---

**SR1.1 Audit Sign-Off:**
* Product scope strictly bounded to UC04 mid-repair recovery.
* Four-tier differentiation matrix incorporated; false claims of Tekion capability absence eliminated.
* Five core architectural additions over PartsRescue validated.
