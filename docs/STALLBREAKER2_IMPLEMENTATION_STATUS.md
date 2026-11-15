# StallBreaker 2: Implementation Status & Repository Audit

**Workspace:** `TEKION-HACKATHON-2026`  
**Phase:** Phase 0 — Repository Alignment & Capability Audit  
**Authoritative Reference:** *StallBreaker 2: Promise-Keeping Service Recovery — Complete Technical Report*  
**Date:** November 15, 2026  
**Audit Standard:** Fact-based repository inspection only. No feature is marked `TESTED` based on a test plan document. No feature is marked `IMPLEMENTED` based on an architecture diagram.

---

## 1. Executive Summary

StallBreaker 2 specifies a unified, single-engine decision architecture operating in two operational modes:
1. **Quote Mode:** Evaluates customer promises, parts delivery options, and technician/bay capacity *before* additional repair work is authorized.
2. **Recover Mode:** Re-optimizes joint sourcing and shop floor dispatch *after* an in-progress repair is disrupted by a parts shortage, technician delay, or hoist bottleneck.

The existing repository is an early **Recover-Mode Prototype (StallBreaker 1.2)**. It validates the foundational feasibility of joint sourcing and scheduling using Google OR-Tools CP-SAT on a single-bay canonical fixture (`S-MATH-01`), verifies physical state-machine gating, and enforces optimistic concurrency revalidation.

This audit establishes the baseline status of all 20 core subsystems across Tiers A through D prior to architectural migration.

```
+----------------------------------------------------------------------------------------------------+
|                                    STALLBREAKER 2 CAPABILITY STATUS                                |
+------------------------------------+-----------------------------+---------------------------------+
| TIER                               | IMPLEMENTATION STATUS       | PRODUCTION / BENCHMARK READINESS|
+------------------------------------+-----------------------------+---------------------------------+
| Tier A: Core Decision Engine       | 45% (Recover CP-SAT built)  | Benchmark verified on S-MATH-01 |
| Tier B: Multi-RO & Extended Solvers| 15% (Heuristics outlined)   | Not started                     |
| Tier C: Enterprise Integrations    | 10% (Local event log built) | Synthetic memory store only     |
| Tier D: Autonomous Multi-Rooftop   | 0%  (Conceptual target)     | Out of hackathon scope          |
+------------------------------------+-----------------------------+---------------------------------+
```

---

## 2. Component-by-Component Audit Ledger

### Status Taxonomy
- **NOT STARTED:** No production code exists in the repository.
- **IN PROGRESS:** Preliminary data structures, stubs, or partial logic exist.
- **IMPLEMENTED:** Fully executable code exists in the repository.
- **TESTED:** Executable code is covered by automated unit/integration tests in `backend/tests/`.
- **DEMONSTRATED:** End-to-end verified via interactive UI or live HTTP suite.
- **PARTNER-VALIDATED:** Validated against live external partner APIs (Tekion DMS / OEM).

---

### Component 1: Unified Quote and Recover Engine
- **Tier:** Tier A
- **Status:** **IN PROGRESS (Recover Mode Only)**
- **Existing Source Path:** [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L35-L480)
- **Existing Test Identifier:** `test_01` through `test_05`, `test_22` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Interactive UI Act 1 (`S-MATH-01`) and Act 2 (`S-MATH-01-ROLLABLE`) execution in `App.tsx`.
- **Missing Implementation Work:**
  1. Quote Mode formulation: Evaluating customer promise feasibility for proposed upsell/additional repair lines before advisor quotation.
  2. Unified entry point: `solve_engine(mode: EngineMode, snapshot: ScenarioSnapshot)` accepting both `QUOTE` and `RECOVER` payloads.
  3. Objective function adaptation: Quote mode optimizes delivery margin and promise probability subject to zero disruption to existing committed ROs.
- **Dependencies:** Component 2 (Versioned State Model), Component 13 (Quote Subset Evaluator).

---

### Component 2: Versioned State Model
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/models.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/models.py#L103-L135), [`backend/state_store.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/state_store.py#L18-L125)
- **Existing Test Identifier:** `test_14`, `test_18`, `test_19`, `test_28`, `test_29` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Top cockpit telemetry displaying active snapshot version (`v14` advancing to `v15` during Act 3).
- **Missing Implementation Work:**
  1. Multi-bay, multi-technician entity state schema (currently single Bay B4 and single Tech K1).
  2. Transactional version branching for speculative quote exploration without dirtying the committed operational baseline.
- **Dependencies:** None.

---

### Component 3: ATP (Available-To-Promise) and Reservation Ledger
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/models.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/models.py#L20-L29), [`backend/eligibility.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/eligibility.py#L13-L41), [`backend/main.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/main.py#L142-L157)
- **Existing Test Identifier:** `test_11`, `test_20`, `test_25` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Source Inventory Panel displaying real-time ATP unit counts; Act 3 S1 ATP drop from 1 to 0 upon external allocation.
- **Missing Implementation Work:**
  1. Continuous inventory quantity tracking (currently binary scalar ATP integer: 1 or 0).
  2. Supplier lead-time variance intervals (currently point-estimate usable tick).
- **Dependencies:** Component 14 (Four-State Reservation Hold).

---

### Component 4: Fitment and Supersession Engine
- **Tier:** Tier A
- **Status:** **TESTED**
- **Existing Source Path:** [`backend/models.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/models.py#L26), [`backend/eligibility.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/eligibility.py#L29-L32)
- **Existing Test Identifier:** `test_12` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Visual "OEM Matched (VIN Checked)" compatibility indicator on Part Source cards.
- **Missing Implementation Work:**
  1. Part supersession chain resolution (e.g., Part A superseded by Part B, interchangeable with Part C).
  2. VIN decode and build-sheet attribute verification rules.
- **Dependencies:** OEM parts catalog or Tekion parts master integration.

---

### Component 5: Vehicle State and Relocation Feasibility Machine
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/models.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/models.py#L3-L12), [`backend/eligibility.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/eligibility.py#L44-L63)
- **Existing Test Identifier:** `test_06`, `test_07`, `test_26` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Physical State Panel in UI displaying vehicle state node progression, technician signoff verification, and H2 stall availability.
- **Missing Implementation Work:**
  1. Dynamic tow-truck / dolly equipment availability checks for non-rollable movements.
  2. Weather / outdoor staging condition constraints.
- **Dependencies:** Shop floor facility configuration.

---

### Component 6: Usable-Ready ETA Intervals
- **Tier:** Tier A
- **Status:** **TESTED**
- **Existing Source Path:** [`backend/fixtures.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/fixtures.py#L38-L47), [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L112)
- **Existing Test Identifier:** `test_27` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Gantt timeline displaying arrival vs usable milestones (e.g. S1 arrives 10:00, usable 10:15 after 15m receiving quarantine).
- **Missing Implementation Work:**
  1. Stochastic transit interval distributions $[ETA_{min}, ETA_{max}]$.
  2. Receiving dock backlog and parts binning time modeling.
- **Dependencies:** Logistics provider tracking integration.

---

### Component 7: Labour-Duration Intervals
- **Tier:** Tier A
- **Status:** **TESTED**
- **Existing Source Path:** [`backend/models.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/models.py#L38), [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L120-L157)
- **Existing Test Identifier:** `test_08`, `test_09` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py)
- **Existing Demonstration Evidence:** Timeline intervals showing 60-min installation and 10-min clearance transit.
- **Missing Implementation Work:**
  1. Technician skill-tier qualification matrices (Tech Level A vs B vs C).
  2. Multi-step labour operations with interrupted work resumption penalties.
- **Dependencies:** Tekion technician scheduling master.

---

### Component 8: Tier 1 Bitset Evaluator (Pre-Solver Feasibility Filter)
- **Tier:** Tier A
- **Status:** **IN PROGRESS (Sequential Python Implementation)**
- **Existing Source Path:** [`backend/eligibility.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/eligibility.py#L13-L63)
- **Existing Test Identifier:** `test_11`, `test_12`, `test_13`, `test_06`, `test_07` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Pre-Solver Feasibility Checklist in UI Physical State Panel.
- **Missing Implementation Work:**
  1. Fast low-level bitset / mask representations for microsecond candidate pruning across large option spaces ($N > 100$).
  2. Batch pruning of mutually incompatible sourcing and movement pairs.
- **Dependencies:** Component 1.

---

### Component 9: Tier 2 CP-SAT (Constraint Programming Engine)
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L35-L480)
- **Existing Test Identifier:** `test_01` through `test_05`, `test_22`, `test_30`, `test_31` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Real-time OR-Tools solver execution in ~30 ms returning optimal status and exact milestone schedules.
- **Missing Implementation Work:**
  1. Multi-bay disjunctive scheduling via `AddNoOverlap` across multiple shared shop assets.
  2. Quote mode constraint formulation.
- **Dependencies:** Google OR-Tools CP-SAT library.

---

### Component 10: Decision-Coupled Source Search
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L100-L165)
- **Existing Test Identifier:** `test_03`, `test_04`, `test_26` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Policy Comparison Panel proving P3 couples source selection (S1 vs S2) with bay movement (`HOLD_ON_BAY` vs `RELOCATE_TO_H2`).
- **Missing Implementation Work:**
  1. Combinatorial multi-part BOM (Bill of Materials) bundling where a repair requires multiple distinct part items simultaneously.
- **Dependencies:** Component 9.

---

### Component 11: Two-Layer JPS (Job Shop Scheduling) Lower Bound
- **Tier:** Tier B
- **Status:** **NOT STARTED**
- **Existing Source Path:** None.
- **Existing Test Identifier:** None.
- **Existing Demonstration Evidence:** None.
- **Missing Implementation Work:**
  1. Analytical lower-bound derivation engine ($L_{JPS}$) for rapid pruning prior to invoking CP-SAT.
  2. Machine-load and critical-path relaxation algorithms.
- **Dependencies:** Component 9.

---

### Component 12: Independent Verifier
- **Tier:** Tier A
- **Status:** **NOT STARTED**
- **Existing Source Path:** None (verification is currently embedded in unit tests, not as an isolated runtime validation module).
- **Existing Test Identifier:** None.
- **Existing Demonstration Evidence:** None.
- **Missing Implementation Work:**
  1. Standalone `verify_proposal_feasibility(proposal, snapshot)` module independent of Google OR-Tools.
  2. Mathematical invariant validation: no bay overlap, non-negative lateness, resource capacity conservation, milestone time monotonicity.
- **Dependencies:** Component 1.

---

### Component 13: Quote Subset Evaluation
- **Tier:** Tier B
- **Status:** **NOT STARTED**
- **Existing Source Path:** None.
- **Existing Test Identifier:** None.
- **Existing Demonstration Evidence:** None.
- **Missing Implementation Work:**
  1. Combinatorial subset search evaluating which subsets of recommended repair lines can be guaranteed on-time given current parts lead times.
  2. Customer quote proposal generation showing delivery-promise tradeoffs per upsell combination.
- **Dependencies:** Component 1, Component 9.

---

### Component 14: Four-State Reservation Hold
- **Tier:** Tier A
- **Status:** **IN PROGRESS (Binary ATP + Stale State Only)**
- **Existing Source Path:** [`backend/revalidation.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/revalidation.py#L66-L80), [`backend/main.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/main.py#L142-L173)
- **Existing Test Identifier:** `test_15`, `test_20`, `test_21` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Stale proposal rejection and automated fallback generation during Act 3.
- **Missing Implementation Work:**
  1. Explicit four-state state machine: `UNHELD` ➔ `PROVISIONAL_HOLD` ➔ `CONFIRMED_RESERVATION` ➔ `EXPIRED` / `RELEASED`.
  2. Time-to-live (TTL) countdown timer for provisional holds awaiting service advisor commitment.
- **Dependencies:** Parts supplier API capabilities.

---

### Component 15: Read-Set Revalidation (Optimistic Concurrency)
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/revalidation.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/revalidation.py#L18-L100)
- **Existing Test Identifier:** `test_14`, `test_15`, `test_16`, `test_28`, `test_29` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Act 3 UI flow: commit of obsolete proposal fails closed with clear red alert; fresh proposal requires explicit re-approval.
- **Missing Implementation Work:**
  1. Fine-grained entity-level read-set validation (e.g. checking whether changed version actually impacts the specific part/bay used by the proposal, rather than coarse rooftop snapshot increment).
- **Dependencies:** Component 2.

---

### Component 16: Transactional Outbox
- **Tier:** Tier C
- **Status:** **NOT STARTED**
- **Existing Source Path:** None ([`backend/state_store.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/state_store.py#L42-L68) appends to an in-memory list).
- **Existing Test Identifier:** None.
- **Existing Demonstration Evidence:** None.
- **Missing Implementation Work:**
  1. Persistent transactional outbox table for reliable webhook/event delivery to external DMS.
  2. At-least-once message delivery with idempotency keys.
- **Dependencies:** Database persistence layer (PostgreSQL / SQLite).

---

### Component 17: Simulator (Monte Carlo Benchmark)
- **Tier:** Tier A
- **Status:** **TESTED & DEMONSTRATED**
- **Existing Source Path:** [`backend/benchmark.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/benchmark.py#L25-L165)
- **Existing Test Identifier:** `test_23`, `test_24` in `test_acceptance.py`
- **Existing Demonstration Evidence:** N=100 paired-seeds benchmark artifact (`generated-results/benchmark_results_n100_20261115_033621.json`) and Benchmark Modal in UI.
- **Missing Implementation Work:**
  1. Continuous synthetic arrival processes (Poisson repair arrivals).
  2. Multi-day longitudinal shop simulator evaluating rolling WIP (Work in Progress).
- **Dependencies:** Component 9.

---

### Component 18: A2, A2+, P3 and P3-mono Baselines
- **Tier:** Tier A / Tier B
- **Status:** **IN PROGRESS (A2 and P3 Tested; A2+ and P3-mono Not Started)**
- **Existing Source Path:** [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L35-L480), [`backend/policies.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/policies.py#L12-L48)
- **Existing Test Identifier:** `test_01`, `test_02`, `test_03`, `test_22` in `test_acceptance.py`
- **Existing Demonstration Evidence:** Policy Comparison Panel comparing A2 vs P3.
- **Missing Implementation Work:**
  1. **A2+ Baseline:** Bay-aware tie-breaking and 1-step lookahead heuristic.
  2. **P3-mono Baseline:** Monolithic single-stage CP-SAT ablation without decision coupling decomposition.
- **Dependencies:** Component 1.

---

### Component 19: LLM-Off Parity
- **Tier:** Tier A
- **Status:** **IMPLEMENTED & TESTED**
- **Existing Source Path:** Entire `backend/` codebase.
- **Existing Test Identifier:** Full acceptance suite `backend/tests/test_acceptance.py` (31/31 pass with 0 LLM calls).
- **Existing Demonstration Evidence:** 100% deterministic local CP-SAT execution without external generative API dependencies.
- **Missing Implementation Work:** None for Core Tier A. (Any future generative explanation layer must remain strictly non-blocking).
- **Dependencies:** None.

---

### Component 20: Quote and Recover Interfaces
- **Tier:** Tier A
- **Status:** **IN PROGRESS (Recover Interface Built; Quote Interface Not Started)**
- **Existing Source Path:** [`frontend/src/App.tsx`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/frontend/src/App.tsx), [`frontend/src/components/`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/frontend/src/components/)
- **Existing Test Identifier:** [`backend/tests/test_frontend_proxy.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_frontend_proxy.py)
- **Existing Demonstration Evidence:** Live web application on `http://localhost:5173/` exercising Acts 1, 2, and 3.
- **Missing Implementation Work:**
  1. Quote Mode interface: Service advisor interactive quotation workbench displaying upsell feasibility and promise trade-offs.
  2. Mode toggle switch between Quote Mode and Recover Mode.
- **Dependencies:** Component 1, Component 13.

---

## 3. Comprehensive Status Summary Matrix

| # | Subsystem / Feature | Tier | Status | Source Location | Test ID |
|---|---|---|---|---|---|
| 1 | Unified Quote & Recover Engine | Tier A | **IN PROGRESS** | `backend/solver.py` | `test_01-05` |
| 2 | Versioned State Model | Tier A | **TESTED** | `backend/state_store.py` | `test_14, 18, 28` |
| 3 | ATP & Reservation Ledger | Tier A | **TESTED** | `backend/eligibility.py` | `test_11, 20` |
| 4 | Fitment & Supersession | Tier A | **TESTED** | `backend/eligibility.py` | `test_12` |
| 5 | Vehicle Physical State Machine | Tier A | **TESTED** | `backend/eligibility.py` | `test_06, 07, 26` |
| 6 | Usable-Ready ETA Intervals | Tier A | **TESTED** | `backend/solver.py` | `test_27` |
| 7 | Labour-Duration Intervals | Tier A | **TESTED** | `backend/solver.py` | `test_08, 09` |
| 8 | Tier 1 Bitset Evaluator | Tier A | **IN PROGRESS** | `backend/eligibility.py` | `test_11-13` |
| 9 | Tier 2 CP-SAT Formulation | Tier A | **TESTED** | `backend/solver.py` | `test_01-05, 30, 31` |
| 10 | Decision-Coupled Source Search | Tier A | **TESTED** | `backend/solver.py` | `test_03, 04, 26` |
| 11 | Two-Layer JPS Lower Bound | Tier B | **NOT STARTED** | None | None |
| 12 | Independent Verifier | Tier A | **NOT STARTED** | None | None |
| 13 | Quote Subset Evaluation | Tier B | **NOT STARTED** | None | None |
| 14 | Four-State Reservation Hold | Tier A | **IN PROGRESS** | `backend/revalidation.py` | `test_15, 20` |
| 15 | Read-Set Revalidation | Tier A | **TESTED** | `backend/revalidation.py` | `test_14-16, 28` |
| 16 | Transactional Outbox | Tier C | **NOT STARTED** | None | None |
| 17 | Deterministic Simulator | Tier A | **TESTED** | `backend/benchmark.py` | `test_23, 24` |
| 18 | A2, A2+, P3, P3-mono Baselines | Tier A/B | **IN PROGRESS** | `backend/policies.py` | `test_01-04` |
| 19 | LLM-Off Parity | Tier A | **IMPLEMENTED**| `backend/` | `All 31 Tests` |
| 20 | Quote and Recover UI | Tier A | **IN PROGRESS** | `frontend/src/` | `test_frontend_proxy` |

---

## 4. Gap Assessment for StallBreaker 2 Migration

To transition cleanly from the current StallBreaker 1.2 prototype to the complete StallBreaker 2 technical report specification, the following architectural gaps must be systematically closed in Phase 1:

1. **Quote Mode Engine:** Implement the missing Quote mode mathematical objective and endpoint, allowing service advisors to test new repair scopes before customer commitment.
2. **Independent Verifier:** Decouple verification into an isolated mathematical checker to guarantee zero false positives from solver edge cases.
3. **A2+ Baseline:** Implement the stronger sequential baseline with 1-step lookahead to provide rigorous benchmark comparisons.
4. **Four-State Reservation Hold Lifecycle:** Formalize the provisional hold lifecycle with TTL expiration.
5. **Multi-Bay / Multi-RO Scope Expansion:** Generalize resource constraints beyond single Bay B4 to multi-bay disjunctive scheduling.
