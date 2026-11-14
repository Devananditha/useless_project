# PartsRescue PR2: Product Opportunity Definition & Scope Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/partsrescue-pr2-product-definition.md`  
**Phase:** PR2 — Product Opportunity Definition & Technical Architecture Specification  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Design Authority:** Principal Automotive Product Architect, AI/Agentic Systems Architect  
**Date:** November 14, 2026  
**Product Identity:** **PartsRescue — Multi-Objective Parts Recovery and Decision Support Agent**  

---

## 1. Product Identity & Core Positioning

### 1.1 Product Name & Classification
* **Full Product Title:** **PartsRescue — Multi-Objective Parts Recovery and Decision Support Agent**
* **Short Name:** **PartsRescue**
* **Official Hackathon Classification:** **Theme 1 — AI & Automation, UC04: Service Parts Shortage Resolver Agent**  
  *(Note: Upstream integration with UC01: Autonomous Appointment & Dispatch Orchestrator is maintained strictly as an operational interface).*

### 1.2 Refined One-Line Positioning Statement
> **"PartsRescue is an intelligent decision-support agent for dealership parts and service personnel that detects in-bay parts shortages, evaluates multi-source recovery options across cost, transit time, and warranty rules, and recommends the mathematically optimal recovery action to minimize dead bay downtime."**

---

## 2. Operational User Personas & Responsibilities

To ensure operational adoption and eliminate software bloat, PartsRescue establishes strict user boundaries:

```
+========================================================================================================================+
|                                        PARTSRESCUE USER PERSONA HIERARCHY                                              |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| #  | Persona Role         | Operational Tier   | Primary Interface           | Core Action in PartsRescue              |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| 01 | **Parts Counter-**   | **PRIMARY USER**   | DMS-embedded side-panel /   | Reviews ranked sourcing options; selects|
|    | **person**           | (Daily Operator)   | desktop triage console      | 1-click PO or inter-store transfer req. |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| 02 | **Service Advisor**  | **SECONDARY USER** | Mobile web action card /    | Approves customer-facing communications;|
|    |                      | (Collaborator)     | DMS service notification    | verifies customer promise time impact.  |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| 03 | **Parts Manager**    | Governance Admin   | Policy & threshold settings | Configures freight spending limits,     |
|    |                      |                    | dashboard                   | vendor preference weights, and margins. |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| 04 | **Service Manager**  | Operational Monitor| Shop capacity dashboard     | Monitors recovered bay hours and        |
|    |                      |                    |                             | technician flag-hour preservation.      |
+----+----------------------+--------------------+-----------------------------+-----------------------------------------+
| 05 | **Flat-Rate Tech-**  | Passive Consumer   | Bay display / mobile alert  | Receives staging notification when the  |
|    | **nician**           |                    |                             | part is physically pulled and tagged.   |
+========================================================================================================================+
```

---

## 3. Detailed Product Boundaries

```
+========================================================================================================================+
|                                    PRODUCT BOUNDARIES & SCOPE MATRIX                                                   |
+--------------------------+---------------------------------------------------------------------------------------------+
| Dimension                | Operational Specification                                                                   |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Exact Operational**    | When an in-progress Repair Order encounters an unfulfilled parts line item during vehicle   |
| **Problem Solved**       | disassembly, dealership staff lack a decision-support tool to calculate whether paying an   |
|                          | expedited courier fee (e.g. $25) is economically justified by avoiding unabsorbed technician|
|                          | stall time and lost labor gross profit ($110/hr GP benchmark), while strictly enforcing     |
|                          | manufacturer warranty and customer authorization rules.                                     |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Triggering Event**     | An active Repair Order parts line item transitions in the DMS to:                           |
|                          | `STATUS_OUT_OF_STOCK`, `STATUS_BACKORDERED`, or `STATUS_DELAYED_ETA`.                       |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Required Inputs**      | 1. DMS RO line data (RO #, VIN, assigned tech, bay #, labor operation, pay-type).           |
|                          | 2. Required OEM part number and quantity.                                                   |
|                          | 3. Local inventory position (On-Hand, Allocated, Available).                                |
|                          | 4. External candidate supplier availability, pricing, and 5-stage bench ETA estimates.      |
|                          | 5. Applicable warranty policy ruleset (OEM vs VSC vs Customer-Pay).                         |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Expected Outputs**     | 1. Ranked, explainable Recovery Action Cards displaying net operational cost trade-offs.    |
|                          | 2. Pre-filled draft purchase requisition or sister-store inventory transfer request.        |
|                          | 3. Draft customer authorization SMS card (for customer-pay substitutions/price changes).   |
|                          | 4. Standardized parts delivery ETA update event published to dealership service board/UC01. |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Core Decision Made**   | Determining the mathematically optimal recovery path across non-dominated alternatives:     |
|                          | *Option A:* Local sister-store courier transfer (fastest, moderate courier fee).            |
|                          | *Option B:* Local commercial distributor aftermarket (customer-pay only, customer-approved).|
|                          | *Option C:* OEM PDC priority emergency VOR (warranty/recall compliant, overnight air).     |
|                          | *Option D:* Hold order & publish delay ETA (when part is globally delayed or backordered).  |
+--------------------------+---------------------------------------------------------------------------------------------+
| **Business Outcome**     | Preserves 750–880 billable technician hours annually ($78k–$97k net operating gross profit  |
|                          | across illustrative dealership models), protects customer CSI, and reduces dead stall time. |
+========================================================================================================================+
```

---

## 4. Explicit Non-Goals (What PartsRescue is NOT)

To prevent architectural scope creep and protect hackathon feasibility, the following areas are **strictly excluded**:

1. **NOT an Autonomous Global Purchasing Bot:** PartsRescue will **never** automatically bind the dealership to external financial purchase orders without human-in-the-loop sign-off from the Parts Counterperson or Parts Manager.
2. **NOT an Electronic Parts Catalog (EPC) Replacement:** PartsRescue does not replace Snap-on, Microcat, or OEM microfiche. It does not identify parts from scratch; it activates *after* the technician or counterperson identifies the required OEM part number on an active work order.
3. **NOT a Predictive Demand Replenishment Engine:** PartsRescue does not manage stock inventory min/max levels or weekly stock replenishment orders (which Tekion ARC Parts Cloud already handles). It is strictly an **exception-handling recovery engine for in-progress repair stalls**.
4. **NOT a Warranty Policy Circumvention Tool:** PartsRescue will **never** recommend aftermarket or unauthorized salvage parts for factory warranty or recall repairs. It enforces a strict, deterministic compliance firewall.
5. **NOT an Autonomous Shop Re-Scheduler:** PartsRescue does not automatically reschedule the entire dealership service drive. It provides delivery ETA signals to human dispatchers or upstream dispatch tools (UC01) to enable intelligent labor resequencing.
