# StallBreaker 2: Tekion Mentor Consultation & Alignment Questionnaire

**Workspace:** `TEKION-HACKATHON-2026`  
**Phase:** Phase 0 — Partner Technical Alignment  
**Target:** Tekion Product Engineering, DMS Architecture & Fixed Operations Mentors  
**Date:** November 15, 2026

---

## 1. Objectives of Mentor Consultation

StallBreaker 2 addresses Theme 1 (AI & Automation), specifically **UC04: Service Parts Shortage Resolver Agent**. 

To ensure our proposed architecture natively integrates with Tekion Automotive Retail Cloud (ARC) and respects existing production system boundaries, we have isolated nine specific technical and operational questions. We present these to Tekion mentors to validate our assumptions and eliminate unsupported claims before proceeding with Tier A implementation.

---

## 2. Nine Specific Alignment Questions

### Question 1: Existing Stalled RO Recovery Mechanics
*Context:* When a technician encounters a missing or damaged part on an active repair order, how does Tekion ARC currently handle the disrupted shop bay?
- Does the system currently trigger an automated bay re-dispatch, or is bay clearing left entirely to the manual discretion of the shop foreman / dispatcher?
- Does Tekion's current parts procurement screen have real-time visibility into the downstream appointment promises of vehicles queued for that specific bay?

---

### Question 2: ATP (Available-To-Promise) vs On-Hand Inventory Semantics
*Context:* In StallBreaker 2, available parts are filtered using Available-To-Promise (ATP) rather than nominal on-hand inventory, preventing double-allocation when multiple ROs compete for the same stock.
- What specific inventory status fields exist in Tekion Parts Master (e.g. `on_hand`, `allocated_to_ro`, `in_transit`, `reserved_quote`)?
- Does Tekion ARC expose real-time webhooks or GraphQL subscriptions when inventory allocation changes on a specific SKU?

---

### Question 3: Mid-Visit Scope Changes & Downstream Capacity Re-Planning
*Context:* In Quote Mode, a multi-point inspection (MPI) uncovers additional required repairs (e.g. brake pads, tie rods).
- How are supplementary quotes currently added to an active RO in Tekion Service?
- If accepting an upsell pushes the promised delivery time past the customer's agreed promise, does Tekion ARC alert the service advisor, or is schedule checking done manually?

---

### Question 4: In-Progress Auto Dispatch & Scheduler AI Event Triggers
*Context:* Tekion has demonstrated AI-driven scheduling and dispatch capabilities.
- What event triggers cause Tekion's Scheduler / Auto-Dispatcher to re-optimize an in-progress schedule (e.g. technician clock-off, job overrunning flat-rate hours, parts delay)?
- Is there an existing API or extension point where an external solver agent (like StallBreaker) can suggest a revised milestone sequence for a specific bay?

---

### Question 5: Temporary Supplier Reservation Holds & Partner Permissions
*Context:* StallBreaker 2 proposes a 4-state reservation hold (`UNHELD` ➔ `PROVISIONAL_HOLD` ➔ `CONFIRMED` ➔ `RELEASED`) with a 30–60 minute TTL while awaiting customer or advisor authorization.
- Do OEM parts locators (e.g. Ford D2D, GM CCA) or third-party catalog aggregators integrated with Tekion (e.g. PartsEdge, Parts Commander) support temporary API reservation holds?
- Or is parts reservation in automotive retail strictly an all-or-nothing purchase order dispatch?

---

### Question 6: Physical Bay Occupancy & Vehicle Mobility Tracking
*Context:* StallBreaker enforces Invariant CE-1 ("The Vehicle-Is-Not-A-Bay"), recognizing that an immobilized vehicle (`PARTIALLY_DISMANTLED`) physically locks the lift.
- Does Tekion ARC or Tekion Fixed Ops mobile apps currently track physical vehicle state (e.g. wheels off, on lift, staged in lot, customer pickup zone)?
- Do dealerships record holding lot / outdoor staging stall occupancy in the DMS, or is lot management tracked outside the system?

---

### Question 7: OEM Fitment, Supersession & Interchange Contracts
*Context:* A parts shortage resolver must evaluate whether an alternative part SKU is fully compatible before presenting it to an advisor.
- Does Tekion parts catalog natively resolve supersession chains and interchange part numbers via OEM data feeds?
- What schema or API contract does Tekion recommend for verifying that an alternative source SKU is a certified engineering supersession for the vehicle's VIN?

---

### Question 8: Partner Sandbox Availability & API Mock Standards
*Context:* We wish to validate StallBreaker's transactional outbox against realistic Tekion API payloads.
- Is a developer sandbox or OpenAPI specification available for Tekion ARC Service & Parts modules for hackathon participants?
- If direct sandbox access is restricted, what canonical JSON data structures does Tekion recommend for mock adapters?

---

### Question 9: Dealership Calibration & Outcome-Data Sharing Rights
*Context:* To transition from synthetic benchmarks ($N=100$) to empirical dealership validation.
- What anonymized historical fixed operations datasets (e.g. parts disruption frequency, bay dwell times, expediting freight expenditures) could Tekion provide for solver calibration?
- Under what governance or security framework can third-party optimization agents interact with dealership ARC data?

---

## 3. Anticipated Answers & Architectural Contingencies

| Question | If Feature Exists in Tekion ARC | If Feature Does Not Exist (StallBreaker Scope) |
|---|---|---|
| **Q1 (Shop Recovery)** | StallBreaker integrates as an optimization copilot feeding the existing dispatcher. | StallBreaker provides the standalone decision engine (UC04 implementation). |
| **Q2 (ATP Semantics)** | Connect directly to Tekion ATP ledger fields. | Emulate ATP via StallBreaker's internal reservation hold table. |
| **Q5 (Reservation Holds)** | Leverage native OEM/vendor hold APIs. | Fall back to local soft reservation with optimistic read-set validation (Act 3 flow). |
| **Q6 (Vehicle Mobility)** | Consume vehicle mobility tags from technician mobile inspect app. | Require explicit advisor/technician toggle before authorising relocation. |
