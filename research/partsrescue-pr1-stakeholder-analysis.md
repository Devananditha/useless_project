# PartsRescue PR1: Dealership Stakeholder Analysis & Human-Agent Boundaries

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/partsrescue-pr1-stakeholder-analysis.md`  
**Phase:** PR1 — Deep Dealership Problem Discovery & Operational Validation  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Research Entity:** PartsRescue AI Innovation Research Team  
**Date:** November 14, 2026  
**Focus:** 8 Dealership Personas, Decision Rights, Trust Boundaries, and Primary User Designation  

---

## 1. Stakeholder Architecture

A common failure mode in enterprise software design is attempting to please every stakeholder equally, resulting in bloated, un-adopted software. Dealerships operate as an intense ecosystem of competing departmental priorities, divergent pay plans, and fragmented computer interfaces.

This analysis maps the eight key stakeholders in dealership fixed operations, establishing their responsibilities, information needs, trust boundaries, and **designates the single primary user persona** for PartsRescue AI.

---

## 2. Comprehensive Stakeholder Matrix

```
+========================================================================================================================+
|                                        DEALERSHIP STAKEHOLDER PROFILES & TRUST GATES                                   |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| #  | Stakeholder Role     | Primary KPI / Goal | Core Information   | What Agent CAN Do  | What Agent MUST NOT Do      |
|    |                      |                    | Required           | (Useful Rec.)      | (Zero Trust Boundary)       |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 01 | **Parts Manager**    | Parts Gross Margin | Vendor pricing,    | Ranked sourcing options| Auto-issue POs to external|
|    |                      | %, Inventory Turn, | freight surcharges,| (sister store vs   | vendors without human price |
|    |                      | Obsolescence <5%   | return policies    | vendor) with costs | confirmation.               |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 02 | **Parts Counter-**   | Quick line lookup, | VIN option codes,  | Automatic supersess- | Change inventory allocations|
|    | **person**           | picking speed,     | bin locations, EPC | ion traversal and  | without physical bin pick   |
|    |                      | accurate billing   | diagrams           | co-part hardware checklist| verification.           |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 03 | **Service Advisor**  | Customer CSI score,| Realistic arrival  | Automated customer | Send unauthorized price or  |
|    |                      | Hours billed/RO,   | ETA, vehicle ready | SMS approval card  | part-type change to customer|
|    |                      | Promise time perf. | time, loaner costs | for aftermarket alt| without advisor approval.   |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 04 | **Service Manager**  | Shop labor sales,  | Bay occupancy, tech| Alert when dead bay| Automatically reassign tech |
|    |                      | effective labor    | flag hours, stalled| holding cost exceeds| jobs without dispatcher or  |
|    |                      | rate, shop throughput| RO count         | courier freight fee| manager sign-off.           |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 05 | **Flat-Rate Tech-**  | Billable flag      | Parts ETA, staging | Fast notification  | Resequence tech to low-flag |
|    | **nician**           | hours/day, bay     | location, correct  | when parts arrive; | lube/tire work while engine |
|    |                      | teardown speed     | hardware fitment   | prep staging bin   | is half-disassembled.       |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 06 | **Procurement /**    | PO accuracy, bulk  | Open order status, | Automated tracking | Auto-commit dealership to   |
|    | **Receiving Clerk**  | discounts, check-in| backorder release  | of PDC delivery    | non-returnable special-     |
|    |                      | speed              | dates, freight bills| trucks & packing slips| order parts.              |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 07 | **Dealer General**   | Total net profit,  | Floorplan cost,    | Executive summary  | Direct day-to-day operations|
|    | **Manager / CFO**    | working capital,   | loaner vehicle fleet| of avoided bay hours| (C-suite persona; not a     |
|    |                      | CSI compliance     | burn, total margin | and recovered margin| daily software user).       |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| 08 | **Wholesale Parts**  | Order volume,      | Part number, VIN,  | Structured digital | Blind electronic order dump |
|    | **Supplier (Vendor)**| low return rate,   | commercial credit  | PO via EDI / API   | without billing line or     |
|    |                      | prompt payment     | account status     |                    | delivery address perfection.|
+========================================================================================================================+
```

---

## 3. Deep-Dive Stakeholder Profiles

### 3.1 Persona 1: The Parts Counterperson (Daily Operational User)
* **Operational Reality:** The parts counterperson stands behind the physical counter, wearing a headset, handling phone calls from wholesale collision shops while technicians lean over the counter demanding parts. They live in the DMS parts catalog and OEM EPC screens.
* **Core Frustration:** When a technician asks for an out-of-stock oil seal, the counterperson must open 3 separate distributor websites, remember passwords, and manually re-enter the vehicle year, make, model, and engine size.
* **What They Value:** A clean, 1-click side-panel that surfaces immediate availability across sister stores and local vendors without re-typing VIN data.
* **Trust Boundary:** They will **never** allow an AI to automatically bill an inventory item to an RO without physical verification, because phantom inventory discrepancies will ruin their year-end physical inventory audit.

### 3.2 Persona 2: The Service Advisor (Customer & Promise Time Guardian)
* **Operational Reality:** The service advisor manages 15–25 customer interactions daily on the service drive, facing direct customer anger when vehicle promise times are broken. Advisors are paid commission on total gross sales and penalized heavily on their monthly Customer Service Index (CSI) manufacturer bonuses.
* **Core Frustration:** Discovering at 4:30 PM that a customer's vehicle promised for 5:00 PM is missing a $12 coolant hose that was backordered at 9:00 AM.
* **What They Value:** Real-time proactive alerts when a parts order is delayed, coupled with an automated, pre-formatted customer text message offering clear options (e.g. "We located the approved replacement 4 miles away; your vehicle will still be ready at 5:15 PM").
* **Trust Boundary:** The advisor will **never** allow an autonomous agent to message a customer directly with price increases or non-OEM part proposals without the advisor clicking "Approve and Send."

### 3.3 Persona 3: The Flat-Rate Technician (Labor Momentum & Pay Plan)
* **Operational Reality:** Dealership technicians are compensated on a **flat-rate pay system** (e.g. paid 4.5 flag hours for an intake manifold gasket repair, regardless of whether it takes 3 hours or 6 hours). If a missing part halts work mid-repair, their hourly earning power drops to zero.
* **Core Frustration:** Being pushed off a high-paying diagnostic or heavy mechanical repair job to do a low-flag maintenance task because the parts department forgot to order an exhaust clamp.
* **What They Value:** Accurate, complete parts staging so they never have to walk back to the parts counter twice for the same job.
* **Trust Boundary:** Technicians will vehemently reject automated dispatch algorithms that shift them off a stalled vehicle if that vehicle is sitting half-disassembled in their primary bay.

---

## 4. Primary User Designation: Who is PartsRescue AI Actually Built For?

To prevent product diffusion, PartsRescue AI must have **one primary operator**:

```
+========================================================================================================+
|                                    PRIMARY USER DESIGNATION VERDICT                                    |
+========================================================================================================+
| **PRIMARY OPERATIONAL USER:** THE PARTS COUNTERPERSON / PARTS SPECIALIST                               |
| **SECONDARY COLLABORATIVE USER:** THE SERVICE ADVISOR (VIA ACTION CARDS)                              |
+========================================================================================================+
```

### Justification for Primary User Designation:
1. **The Parts Counterperson holds the catalog authority:** Service advisors cannot legally or technically select replacement part numbers. The parts counterperson owns inventory lookup, supersession validation, and vendor purchase requisition.
2. **The Point of Intervention:** The shortage is born at the parts counter (Step 06 of the workflow). Sourcing alternatives must be evaluated and triggered by the parts department before the service department can plan bay recovery.
3. **The User Interface Strategy:**
   * **Primary UI (Parts Specialist):** A dense, fast, keyboard-friendly sourcing optimization console embedded directly into the DMS parts requisition workflow.
   * **Secondary UI (Service Advisor):** Lightweight mobile/web "Decision Cards" (e.g., *"Option A approved by parts: Courier arriving in 35 mins; tap to notify customer"*).
   * **Passive UI (Technician):** Digital bay notification when parts are physically staged.
