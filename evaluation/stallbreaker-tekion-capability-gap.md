# StallBreaker: Tekion Capability Gap & Competitive Intelligence Matrix

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-tekion-capability-gap.md`  
**Phase:** StallBreaker Transition Evaluation — SR1.1 Consistency & Architecture Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Authority:** Joint Architecture Review Board (Competitive Intelligence Analyst, AI Solution Architect, Fixed Ops Specialist)  
**Primary Sources:**  
- `references/StallBreaker_Product_Validation_and_Winning_Strategy-1.pdf` [SB-PDF] (Vendor Sources [W1]–[W13])  
- `references/tekion-themes.pdf` (Official UC04 Hackathon Source)  
**Date:** November 14, 2026  
**Status:** AUDITED & RECONCILED (SR1.1)  

> [!WARNING]
> Public vendor product pages and press releases demonstrate advertised capability, not the presence or absence of specific internal workflows. Absence of public documentation is **NOT** proof of product absence. All capability comparisons in this document are framed as **testable hypotheses for Tekion mentor validation**, not definitive market gap assertions.

---

## 1. Verified Public Tekion Capability Baseline

Based on public product disclosures accessed as documented in [SB-PDF, Appendix C], Tekion possesses an extensive, modern cloud footprint across automotive retail:

```
+===================================================================================================================================+
|                                           TEKION PUBLIC PRODUCT SURFACE ANALYSIS                                                  |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| #  | Public Platform Area | Documented Public Scope ([W1]–[W7])                    | Direct Implication for StallBreaker          |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 01 | **Tekion ARC** [W1]  | Unified cloud architecture spanning CRM, DMS, Service, | StallBreaker cannot claim to "unify data     |
|    |                      | Parts, Accounting, and Analytics.                      | silos"; ARC already unifies dealership data. |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 02 | **Live Service       | Real-time WIP tracking, advisor/tech throughput,       | StallBreaker cannot claim novelty merely by  |
|    | Control Center** [W2]| bottlenecks, deferred work, and active exceptions.     | building a service bay monitoring board.     |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 03 | **Automatic RO & Tech| Algorithmic matching of repair orders to certified     | StallBreaker cannot claim novelty by simply  |
|    | Scheduling** [W2]    | technicians based on skills and shop capacity.         | matching technician certifications to jobs.  |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 04 | **Scheduler AI** [W3]| 24/7 conversational booking and rescheduling; checks   | General appointment scheduling is existing;  |
|    | (Nov 3, 2026 update) | advisor capacity, certifications, transport options.   | StallBreaker must stay within mid-day stalls.|
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 05 | **Tekion T1 Pro**    | Unified AI agent interface and orchestration layer     | StallBreaker must position as a specialist   |
|    | (June 16, 2026) [W4] | embedded across ARC workflows.                         | decision engine that T1 Pro can orchestrate. |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 06 | **OEM Integrations   | 35 OEMs, 430 certified integrations (Parts Master,     | Parts catalogue and ordering exist; scope of |
|    | Catalogue** [W5]     | Inventory, Availability, PDC VOR, Parts Locator).      | reservation write permissions is unverified. |
+----+----------------------+--------------------------------------------------------+----------------------------------------------+
| 07 | **Automotive Partner | REST APIs, webhooks, and partner tiers.                | Realistic architectural integration path for |
|    | Cloud (APC)** [W6]   |                                                        | StallBreaker adapter contracts.              |
+===================================================================================================================================+
```

---

## 2. Granular Capability Overlap & Gap Assessment

```
+===================================================================================================================================+
|                                           GRANULAR CAPABILITY OVERLAP MATRIX                                                      |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| #  | Functional Capability       | Public Assessment | Detailed Operational Comparison                   | Evidence Standard     |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 01 | Appointment Rescheduling    | CLEARLY EXISTING  | Scheduler AI handles customer cancellations and   | DOCUMENTED            |
|    |                             |                   | appointment moves. (Out of StallBreaker scope).   | ([W3])                |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 02 | Technician Skill Matching   | CLEARLY EXISTING  | Auto RO Scheduling matches jobs to certified tech | DOCUMENTED            |
|    |                             |                   | proficiencies. (Baseline feature in StallBreaker).| ([W2])                |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 03 | Shop Bottleneck Monitoring  | CLEARLY EXISTING  | Live Service Control Center visualizes active     | DOCUMENTED            |
|    |                             |                   | stall exceptions. (StallBreaker consumes this).   | ([W2])                |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 04 | Parts Catalog & Locator     | CLEARLY EXISTING  | OEM integrations query national parts locators.   | DOCUMENTED            |
|    |                             | (Selected OEMs)   | (StallBreaker adds ATP & lease gating).           | ([W5])                |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 05 | In-RO Parts Pricing/Stock   | PARTIALLY         | Dealer-FX & Tekion display live RO parts pricing. | DOCUMENTED / INFERRED |
|    |                             | SUPPORTED         | Universal cross-store ATP write-through unproven. | ([W5], [W9])          |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 06 | Mid-Repair Parts Disruption | PUBLICLY UNCLEAR  | Hackathon brief specifies UC04 use case; exact    | UNVERIFIED HYPOTHESIS |
|    | Event Capture               |                   | real-time webhook payload in ARC is unconfirmed.  | (Mentor Validation)   |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 07 | ATP vs. On-Hand Inventory   | PUBLICLY UNCLEAR  | Public pages show inventory availability; whether | UNVERIFIED HYPOTHESIS |
|    | Gating Pre-Solve            |                   | unallocated ATP is exposed to third parties is unk| (Mentor Validation)   |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 08 | Time-Bounded Exclusive      | PUBLICLY UNCLEAR  | DMS APIs support ordering; whether cross-store    | UNVERIFIED HYPOTHESIS |
|    | Reservation Lease Lifecycle |                   | 10-minute hold leases can be written is unproven. | (Mentor Validation)   |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 09 | Physical Vehicle Bay        | PUBLICLY UNCLEAR  | ARC tracks RO repair status; whether it models    | UNVERIFIED HYPOTHESIS |
|    | Occupancy State Machine     |                   | hoist locks, dismantling, and safe-to-move is unk.| (Mentor Validation)   |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 10 | Joint Source × Vehicle ×    | POTENTIALLY       | No reviewed source demonstrates a joint model     | POTENTIALLY           |
|    | Schedule Optimization       | DIFFERENTIATED    | co-optimizing parts, hoists, holds, and jobs.     | DIFFERENTIATED        |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 11 | Atomic Pre-Commit           | POTENTIALLY       | Necessary for production concurrency; no public   | POTENTIALLY           |
|    | Revalidation Gate           | DIFFERENTIATED    | integration doc describes this transaction check. | DIFFERENTIATED        |
+----+-----------------------------+-------------------+---------------------------------------------------+-----------------------+
| 12 | Usable Part-Ready Bounded   | POTENTIALLY       | Replaces single quoted ETA with dock-to-bench     | POTENTIALLY           |
|    | Uncertainty Scenarios       | DIFFERENTIATED    | low/central/high scenario intervals.              | DIFFERENTIATED        |
+===================================================================================================================================+
```

---

## 3. Four-Tier Classification of StallBreaker Novelty

To maintain absolute credibility before hackathon evaluators, StallBreaker categorizes its features into four strict tiers:

```
+===================================================================================================================================+
|                                           STALLBREAKER FOUR-TIER NOVELTY MATRIX                                                   |
+----+--------------------------------+---------------------------------------------------------------------------------------------+
| #  | Tier Category                  | Functional Features & Strategic Boundary                                                    |
+----+--------------------------------+---------------------------------------------------------------------------------------------+
| 01 | **TIER 1:**                    | 1. **Joint Combinatorial Formulation:** Coupling parts source availability directly to      |
|    | **CORE NOVEL CONTRIBUTION**    |    physical bay hoist occupancy, holding zone capacity, and downstream alignment jobs.     |
|    | (Defensible Innovation)        | 2. **Physical Vehicle Decoupling:** Modeling the vehicle as a physical occupant that blocks |
|    |                                |    a bay independently of technician labor flag-time.                                       |
+----+--------------------------------+---------------------------------------------------------------------------------------------+
| 02 | **TIER 2:**                    | 1. **Seven-State Reservation Lifecycle:** Time-bounded exclusive leases ($T_{\text{lease}}$|
|    | **SUPPORTING MECHANISM**       |    $= 10\text{m}$) and asynchronous supplier defect revocation handling.                    |
|    | (Production Reliability)       | 2. **Pre-Commit 10-Token Revalidation:** Atomic optimistic concurrency verification.       |
|    |                                | 3. **Usable Ready Time Interval Scenarios:** Low/Central/High dock-to-bench timelines.      |
+----+--------------------------------+---------------------------------------------------------------------------------------------+
| 03 | **TIER 3:**                    | 1. **Technician Skill Matching:** Standard ASE certification eligibility filters.           |
|    | **EXISTING INDUSTRY CAPABILITY**| 2. **WIP Service Bay Board:** Visual display of bay occupancy and countdown timers.         |
|    | (Non-Differentiating Hygiene)  | 3. **Cross-Store Catalog Lookup:** Standard VIN decoding and parts lookup queries.          |
+----+--------------------------------+---------------------------------------------------------------------------------------------+
| 04 | **TIER 4:**                    | 1. **Internal Tekion ARC Recovery Coverage:** Whether ARC already executes automated parts-|
|    | **UNVERIFIED PRODUCT-GAP**     |    stall rescheduling internally. (Framed as mentor validation hypothesis).                 |
|    | **HYPOTHESIS**                 | 2. **APC Write Endpoints:** Whether partner tiers permit inventory reservation writes.      |
+===================================================================================================================================+
```

---

## 4. Prioritized Mentor Validation Protocol

During the hackathon mentor sessions, the team will execute this structured 10-question inquiry:

```
+===================================================================================================================================+
|                                           TEKION MENTOR VALIDATION INQUIRY PROTOCOL                                               |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| #  | Pri | Specific Question for Tekion Technical Mentor                   | Architectural Purpose & Impact                      |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 01 | P1  | When a parts delay occurs on an active RO today, does ARC        | Validates whether StallBreaker's joint model solves |
|    |     | recommend only a source, only a schedule change, or a joint plan?| an unaddressed workflow gap in ARC.                 |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 02 | P1  | Does inventory data in ARC expose unallocated ATP, reserved qty, | Confirms whether StallBreaker's ATP pre-solve gate  |
|    |     | and an active reservation lease token?                           | can bind to native ARC fields in production.        |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 03 | P1  | Can third-party apps write temporary inventory reservation holds | Determines whether the 10-minute lease model can be |
|    |     | via Automotive Partner Cloud (APC) partner APIs?                 | implemented natively or requires partner extension. |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 04 | P1  | Does ARC track vehicle physical location at bay/hoist level with | Validates whether the `VehicleState` machine is a   |
|    |     | disassembly state and technician safe-close confirmation?        | genuine data extension or duplicates existing state.|
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 05 | P2  | Does Scheduler AI or Automatic RO Scheduling re-optimize active  | Clarifies boundary between UC01 dispatch and UC04   |
|    |     | in-progress bay work, or only future booking appointments?       | mid-day disruption recovery.                        |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 06 | P2  | What are the guaranteed webhook delivery latencies for parts line| Calibrates the disruption detector's event polling  |
|    |     | status change events in APC?                                     | vs. webhook ingestion thresholds.                   |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 07 | P2  | Does ARC capture receiving dock-to-bench transit milestones, or  | Validates StallBreaker's 5-stage usable ready time  |
|    |     | is ETA strictly supplier dock arrival?                           | model vs. native DMS ETA semantics.                 |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 08 | P3  | What are the sanctioned extension points for embedding decision  | Confirms UI sidecar architecture for embedding      |
|    |     | cards inside T1 Pro or the Live Service Control Center?          | StallBreaker action cards in the advisor console.   |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 09 | P3  | Across Tekion dealerships, what is the standard expense account  | Validates economic assumptions regarding parts      |
|    |     | allocation for expedited hotshot courier fees?                   | manager freight budget absorption.                  |
+----+-----+------------------------------------------------------------------+-----------------------------------------------------+
| 10 | P3  | Is there an unreleased 2026/2027 roadmap initiative addressing   | Prevents building a redundant solution against an   |
|    |     | service parts shortage recovery optimization?                    | imminent native Tekion core feature.                |
+===================================================================================================================================+
```

---

**SR1.1 Audit Sign-Off:**
* Tekion public capability baseline grounded strictly in verified sources [W1]–[W7].
* False claims of competitor capability absence eliminated; replaced with documented gap classifications.
* Four-tier novelty classification formalized.
* Ten-question mentor inquiry protocol established for hackathon validation.
