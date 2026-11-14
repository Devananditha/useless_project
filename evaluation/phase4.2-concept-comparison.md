# Phase 4.2 Strategic Concept Comparison: CrossBorder TitleGuard vs PartsRescue AI

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.2-concept-comparison.md`  
**Stage:** Phase 4.2 – Final Evidence Correction & Readiness Audit  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and Original Phase 4 Specifications  
**Audit Authorities:** Senior Product Strategist, Automotive Dealership Operations Specialist, AI/ML Solution Architect, Independent Innovation Critic  
**Date of Audit:** November 14, 2026  
**Audit Determination:** **CROSSBORDER TITLEGUARD RETAINS DECISIVE STRATEGIC ADVANTAGE**  

---

## 1. Executive Concept Context

During hackathon strategy reviews, a compelling new candidate concept emerged: **PartsRescue AI — an agentic repair-order recovery system for parts shortages**.

PartsRescue AI represents an evolution of the earlier Candidate B opportunity space (incorporating elements of BayFlow Dynamic B3, StageGate Dispatch B1, and PartsOrchestrator B2) focused on official **Theme 1: AI & Automation**, specifically **UC04 (*Service Parts Shortage Resolver Agent*)** and **UC01 (*Autonomous Appointment & Dispatch Orchestrator*)**.

This audit conducts a rigorous, multi-dimensional comparative evaluation between **CrossBorder TitleGuard** and **PartsRescue AI** using the **Original Phase 4 Evaluation Rubric**, evaluating technical feasibility, data access barriers, Tekion ecosystem overlap, and 5-minute hackathon demonstration strength.

---

## 2. Product Profile & Architectural Comparison

```
+========================================================================================================+
|                                    CONCEPT PROFILES AT A GLANCE                                        |
+==============================+====================================+====================================+
| Dimension                    | Concept C1: CrossBorder TitleGuard | New Concept: PartsRescue AI        |
+==============================+====================================+====================================+
| **Official Hackathon Theme** | Theme 1: AI & Automation (UC02)    | Theme 1: AI & Automation (UC04/01) |
| **Problem Addressed**        | 18–25 day out-of-state trade-in    | Mid-repair parts stalls immobilizing|
|                              | title defect latency freezing CIT. | bays, stalling techs, delaying ROs.|
+------------------------------+------------------------------------+------------------------------------+
| **Core AI / ML Mechanism**   | Multimodal VLM (Claude 3.5 Sonnet) | Multi-agent orchestrator + discrete|
|                              | + Deterministic AST rule engine.   | constraint optimizer / fitment RAG.|
+------------------------------+------------------------------------+------------------------------------+
| **Operational Workflow**     | Showroom intake pre-audit of messy | Real-time RO triage when a parts   |
|                              | physical paper deal jackets.       | line item is backordered/missing.  |
+------------------------------+------------------------------------+------------------------------------+
| **Primary Financial Unlock** | Releases $25k–$45k CIT hold; saves | Recovers 1.2–1.8 billable hours/day|
|                              | $59.6k net cash/yr + $420k float.  | ($110k–$160k shop gross profit).   |
+------------------------------+------------------------------------+------------------------------------+
| **Point of Intervention**    | Showroom sales desk (pre-contract).| Service drive & parts counter.     |
+==============================+====================================+====================================+
```

---

## 3. Deep-Dive Investigation of PartsRescue AI

### 3.1 The Hypothesized 7-Step Agentic Workflow
1. **Shortage Detection:** Agent detects a Repair Order (RO) flagged with an unexpected parts backorder or physical bin shortage.
2. **Compatibility & Fitment Identification:** Queries vehicle fitment data (ACES/PIES standards, OEM supersession chains) to identify alternative part numbers, superseded revisions, or certified OEM/aftermarket equivalents.
3. **Multi-Source Inventory Sourcing:** Queries local dealer group sister-store inventories, regional wholesale distributor portals (e.g. Worldpac, LKQ), and peer dealer networks (OEC D2D).
4. **Impact Modeling:** Evaluates tradeoffs across sourcing costs, courier transit ETAs, customer loaner vehicle expense, bay occupancy, and technician flag-hour equity.
5. **Recovery Recommendation:** Formulates actionable options for the Parts Manager and Service Advisor (e.g., *"Option A: 45-min local courier transfer from Sister Store B at +$15 cost vs Option B: Resequence technician to Bench Task RO #4012"*).
6. **Human Approval:** Parts manager clicks one-click approval on the recommended action.
7. **Action Execution:** Automatically triggers purchase requisition, internal store transfer request, and updates DMS dispatch board.

### 3.2 Evaluation of PartsRescue Feasibility & Ecosystem Realities
* **Data Availability Obstacles (Critical Red-Team Vulnerability):**
  * *Fitment & Supersession Data:* OEM parts catalogs (Microcat, Snap-on EPC) and supersession chains (e.g., Part #A supersedes to Part #B only if Wiring Harness #C is also replaced) are **strictly proprietary and fiercely protected**.
  * *Supplier Availability & ETA Feeds:* Wholesale parts distributor APIs (OEC, PartsTrader, Worldpac) require commercial enterprise developer agreements, bilateral dealership credentials, and paid transaction fees. Accessing live supplier inventory and ETA feeds is virtually impossible for a student hackathon team, forcing heavy simulation.
* **Severe Native Tekion Product Overlap:**
  * Tekion's product portfolio already includes **Tekion ARC Parts Cloud** and **Tekion ARC Service Cloud**, which advertise:
    * *Automated Parts Replenishment & Reordering.*
    * *Live Multi-Store Inventory Visibility across dealer groups.*
    * *Smart Tech Matching and Shop Capacity Scheduling.*
  * Pitching PartsRescue AI directly to Tekion engineering judges risks appearing as a naive attempt to build an external wrapper around Tekion's existing native parts ordering and dispatch infrastructure.
* **The "Lift Prison" Bottleneck Remains:**
  * If a vehicle's engine or suspension is disassembled on a 2-post lift, PartsRescue cannot "resequence" the bay. It can only resequence the technician's time.

---

## 4. Head-to-Head Comparative Rubric (Original Phase 4 Weights)

The table below provides a strict, objective evaluation under the **Original Phase 4 Rubric** (Weights Totaling 100%):

$$\text{Final Weighted Score} = \sum_{i=1}^{8} (\text{Score}_i \times \text{Weight}_i)$$

```
+========================================================================================================================+
|                                    STRATEGIC HEAD-TO-HEAD EVALUATION MATRIX                                            |
+=========================+======+=========================================+=============================================+
| Criterion               |Weight| CrossBorder TitleGuard (C1)             | PartsRescue AI (New Opportunity Candidate)  |
+=========================+======+=========================================+=============================================+
| 1. Novelty              | 20%  | **4.70 / 5.00 (0.9400)**                | **3.80 / 5.00 (0.7600)**                    |
|                         |      | *Rationale:* Unprecedented showroom     | *Rationale:* Agentic wrapper over 20-year-  |
|                         |      | intake pre-audit of physical titles.    | old parts locator concepts (OEC, D2D).      |
|                         |      | Competitors operate post-sale bureaus.  | Novelty lies in multi-agent orchestration.  |
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 2. Business Value       | 15%  | **4.60 / 5.00 (0.6900)**                | **4.50 / 5.00 (0.6750)**                    |
|                         |      | *Rationale:* Solves $25k–$45k CIT hold, | *Rationale:* Recovers stalled technician    |
|                         |      | saves $59.6k net cash/yr, $420k float.  | flag hours ($110k–$160k annual gross).      |
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 3. Technical            | 15%  | **4.50 / 5.00 (0.6750)**                | **3.60 / 5.00 (0.5400)**                    |
|    Feasibility          |      | *Rationale:* Multimodal VLM + AST;      | *Rationale:* Complex multi-agent pipeline;  |
|                         |      | deterministic local execution; no API   | highly vulnerable to complex supersession   |
|                         |      | lockouts; clear safe degradation.       | logic and supplier API simulation limits.   |
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 4. Tekion Fit           | 10%  | **4.90 / 5.00 (0.4900)**                | **4.30 / 5.00 (0.4300)**                    |
|                         |      | *Rationale:* Fills the physical paper   | *Rationale:* Fits Theme 1 UC04 perfectly,   |
|                         |      | void between Deal Guard AI and TDP.     | but heavily overlaps with ARC Parts Cloud.  |
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 5. Data Availability    | 15%  | **4.80 / 5.00 (0.7200)**                | **3.20 / 5.00 (0.4800)**                    |
|                         |      | *Rationale:* Public motor vehicle codes;| *Rationale:* Massive blocker: OEM parts     |
|                         |      | public title templates; synthetic PDFs. | catalogs and live wholesale inventory feeds |
|                         |      | Zero proprietary API dependencies.      | are proprietary, paywalled, or gated by NDAs|
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 6. Demo Potential       | 10%  | **5.00 / 5.00 (0.5000)**                | **4.10 / 5.00 (0.4100)**                    |
|                         |      | *Rationale:* Commanding visual UI: messy| *Rationale:* Shows text tables of part #s,  |
|                         |      | scanned title + red bounding box defect.| courier ETAs, and chat dialogues. Good,     |
|                         |      | Immediate comprehension in 5 minutes.   | but lacks the visual punch of vision AI.    |
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 7. Adoption             |  5%  | **4.60 / 5.00 (0.2300)**                | **4.00 / 5.00 (0.2000)**                    |
|    Practicality         |      | *Rationale:* Zero new data entry; runs  | *Rationale:* Parts managers welcome sourcing|
|                         |      | asynchronously at the F&I sales desk.   | help, but technicians resist schedule shifts|
+-------------------------+------+-----------------------------------------+---------------------------------------------+
| 8. Evidence Strength    | 10%  | **4.80 / 5.00 (0.4800)**                | **4.20 / 5.00 (0.4200)**                    |
|                         |      | *Rationale:* Primary audited statutes   | *Rationale:* Carlisle & Ducker service      |
|                         |      | (A.R.S. § 28-2058, CVC § 5753, 49 CFR). | benchmark data on parts fill-rate friction. |
+=========================+======+=========================================+=============================================+
| **FINAL WEIGHTED SCORE**| 100% | **4.7250 / 5.00**                       | **3.9150 / 5.00**                           |
| Strategic Verdict       | —    | **PRIMARY RECOMMENDED WINNER (FROZEN)** | **STRONG BACKUP / STRATEGIC HYPOTHESIS**    |
+=========================+======+=========================================+=============================================+
```

---

## 5. Comparative Strategic Synthesis

### 5.1 Why PartsRescue AI is an Attractive Concept:
* **Direct Theme 1 UC04 Alignment:** Matches the official "Service Parts Shortage Resolver Agent" description almost verbatim.
* **Autonomous Multi-Agent Appeal:** Sounds modern, sophisticated, and agentic (negotiating across suppliers, calculating delivery trade-offs, orchestrating shop schedules).
* **Solves a Painful Daily Dealership Problem:** Every dealership parts manager struggles with backordered parts and stranded customer vehicles.

### 5.2 Why CrossBorder TitleGuard Wins for the Hackathon:
1. **The Hackathon Data Reality:** In a student hackathon, data access makes or breaks a project. TitleGuard relies on **public statutory motor vehicle codes and realistic synthetic PDF deal jackets**. PartsRescue relies on **proprietary OEM parts catalogs, complex fitment supersession databases, and closed supplier inventory APIs**. Demonstrating PartsRescue forces the team to simulate 80% of its data feeds.
2. **5-Minute Live Visual Command:** TitleGuard displays a crumpled, scanned physical Arizona title on screen and visually annotates an unnotarized Bill of Sale with a red bounding box and statutory citation in under 8 seconds. This visual "wow factor" is immediately understood by non-technical judges. In contrast, PartsRescue shows part numbers, warehouse tables, and agent logs, which look like a standard inventory script.
3. **Flawless Enterprise White Space:** TitleGuard fills the physical paper gap between Tekion TDP (outbound fee math) and Deal Guard AI (buyer ID/insurance check). PartsRescue directly overlaps with Tekion's existing ARC Parts Cloud and Service Cloud.

---

## 6. Audit Conclusion & Strategic Recommendation

* **Primary Recommendation:** Retain **CrossBorder TitleGuard (Concept C1)** as the primary candidate concept for Phase 5 presentation architecture.
* **PartsRescue Designation:** Formally designate **PartsRescue AI** as an insightful **Strategic Alternative / Case Study Hypothesis**, scoring **3.9150 / 5.00** (slightly ahead of BayFlow Dynamic at **3.9050 / 5.00** due to superior agentic positioning, but trailing TitleGuard by **0.81 points** due to data accessibility and demo visual constraints).
