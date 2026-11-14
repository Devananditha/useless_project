# PartsRescue PR1: Problem Prioritisation & Narrow Scope Definition

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr1-problem-prioritisation.md`  
**Phase:** PR1 — Deep Dealership Problem Discovery & Operational Validation  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Research Entity:** PartsRescue AI Innovation Research Team  
**Date:** November 14, 2026  
**Focus:** 8 Candidate Problem Definitions Evaluated Across 10 Operational Criteria  

---

## 1. Problem Narrowing Mandate

The broad statement "dealerships have parts shortages" is too diffuse to justify a viable, differentiated product. Sourcing a part is fundamentally different from preventing a bay stall or tracking an OEM backorder.

Under `.cursor/rules/research-standards.mdc`, this evaluation assesses eight specific operational problem definitions across ten rigorous criteria (each scored on a 1.0 to 5.0 scale) to isolate the **single highest-value narrow problem** for PartsRescue AI.

---

## 2. Evaluation Criteria (Equal 10% Weighting)

1. **Frequency:** How often the bottleneck occurs in daily dealership operations.
2. **Operational Impact:** Severity of friction on technician momentum, bay throughput, and customer turnaround.
3. **Business Value:** Quantifiable dollar recovery in gross profit, avoided rental fees, and labor billing.
4. **Current Workaround Severity:** Degree of pain, manual effort, and human frustration in existing workarounds.
5. **Software White Space:** Absence of effective incumbent software coverage (higher score = larger unoccupied space).
6. **Data Availability:** Accessibility of required inputs without impossible proprietary API paywalls.
7. **AI Suitability:** Degree to which the problem genuinely requires intelligent reasoning, multi-agent coordination, or optimization rather than simple database queries.
8. **Technical Feasibility:** Mathematical and architectural credibility for a high-reliability implementation.
9. **Demo Potential:** Kinetic impact, clarity, and visual comprehension in a 5-minute hackathon presentation.
10. **Novelty Potential:** Degree of unique, defensible intellectual property vs commodity legacy tools.

---

## 3. Master Problem Prioritisation Matrix

```
+=========================================================================================================================================================================+
|                                                           EIGHT CANDIDATE PROBLEM DEFINITIONS EVALUATION MATRIX                                                         |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| ID | Candidate Problem Definition           | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 |C10 | Total Avg | Evidentiary Rationale             | Operational Rank        |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P1 | **Early Shortage Detection**           | 3.8| 4.0| 3.9| 3.5| 3.2| 4.2| 3.5| 4.2| 3.8| 3.2| **3.730** | DMS line listeners detect status, | **Rank 6**              |
|    | (Pre-Teardown Anomaly Alert)           |    |    |    |    |    |    |    |    |    |    |           | but detection alone doesn't solve.| (Useful feature, not PR) |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P2 | **Alternative Sourcing Discovery**     | 4.5| 4.2| 4.3| 4.0| 2.8| 3.2| 3.8| 3.5| 4.0| 3.5| **3.780** | Sourcing across vendors is good,  | **Rank 5**              |
|    | (Multi-Supplier Catalog Scraping)      |    |    |    |    |    |    |    |    |    |    |           | but overlaps with Nexpart/OEC.    | (Vendor crowded space)  |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P3 | **OEM National Backorder Resolution**  | 3.2| 4.8| 4.6| 4.8| 3.8| 3.0| 3.8| 3.2| 4.2| 4.0| **3.940** | High pain, but OEM factory back-  | **Rank 2**              |
|    | (Critical VOR / PDC Outages)           |    |    |    |    |    |    |    |    |    |    |           | orders cannot be magically forged.| (Severe external limit) |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P4 | **Supersession Hardware Matching**     | 3.5| 4.1| 4.0| 3.8| 3.4| 3.5| 3.2| 4.0| 3.6| 3.6| **3.670** | Traversing DAGs is valuable, but  | **Rank 8**              |
|    | (Co-Dependent Hardware Validation)     |    |    |    |    |    |    |    |    |    |    |           | OEM EPCs partially show TSB notes.| (Technical feature only)|
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P5 | **Intra-Group Inventory Sharing**      | 4.0| 4.2| 4.1| 3.9| 2.5| 3.8| 3.5| 3.8| 3.9| 3.2| **3.690** | Sister-store transfers are common,| **Rank 7**              |
|    | (Multi-Location Dealer Group Transfer) |    |    |    |    |    |    |    |    |    |    |           | but DMS multi-store already tracks| (Internal hoarding issue)|
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P6 | **Urgency-Based RO Prioritization**    | 4.2| 4.0| 3.8| 3.5| 3.0| 4.2| 3.8| 4.2| 3.8| 3.4| **3.790** | Prioritizing ROs helps dispatch,  | **Rank 4**              |
|    | (Allocating Scarce Parts to Waiting RO)|    |    |    |    |    |    |    |    |    |    |           | but doesn't procure missing parts.| (Internal allocation)   |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P7 | **Multi-Objective Tradeoff & Recovery**| 4.6| 4.7| 4.8| 4.5| 4.5| 3.8| 4.6| 4.0| 4.7| 4.6| **4.480** | **Unoccupied white space: models  | **RANK 1 (DECISIVE      |
|    | **Action Recommendation Engine**       |    |    |    |    |    |    |    |    |    |    |           | **courier cost vs bay idle time vs| **WINNER)**             |
|    |                                        |    |    |    |    |    |    |    |    |    |    |           | **warranty rules for human signoff|                         |
+----+----------------------------------------+----+----+----+----+----+----+----+----+----+----+-----------+-----------------------------------+-------------------------+
| P8 | **Proactive Parts Readiness for Appts**| 4.4| 4.3| 4.4| 3.6| 2.9| 4.0| 3.6| 3.9| 4.0| 3.5| **3.860** | Pre-picking parts for appointments| **Rank 3**              |
|    | (Pre-Ordering Before Customer Arrival) |    |    |    |    |    |    |    |    |    |    |           | is valuable, but high no-show risk| (Customer flake factor) |
+=========================================================================================================================================================================+
```

---

## 4. Why Problem P7 Decisively Wins

Problem P7 achieves a commanding score of **4.480 / 5.00**, leading the runner-up (P3) by **+0.540 points**.

### The Anatomy of Problem P7:
> **"Dealerships lack an intelligent decision engine that calculates the financial trade-off between expedited sourcing costs, service bay holding costs, technician flag-hour preservation, and warranty legal constraints when an in-progress repair order encounters a parts shortage."**

### Why P7 is the Winning Narrow Product Scope:
1. **It Solves the Departmental Metric Conflict:** Parts managers refuse to pay a $25 hotshot courier fee because their KPI is parts margin and freight expense. Service managers lose $160 in dead bay labor. P7 mathematically proves to the parts manager that spending $25 recovers $135 in net dealership profit.
2. **It Respects Legal & Warranty Realities:** P7 does not naively propose aftermarket parts for warranty claims. It applies strict deterministic Boolean rules:
   * *If Warranty:* Restrict sourcing to OEM supersession DAGs, sister stores, or emergency VOR.
   * *If Customer-Pay:* Evaluate certified aftermarket equivalents, calculate customer savings, and generate an interactive mobile authorization card.
3. **It Combines Optimization and Agentic NLP:** It is not a basic database query. It solves a multi-objective Pareto curve across transit time, procurement cost, customer promise time, and bay holding cost, then synthesizes a human-readable recommendation for 1-click approval.
4. **It Has Tremendous 5-Minute Demo Punch:** In a live demonstration, showing an interactive decision card that compares *"Option A: 45-min sister-store courier ($15 fee, 0 bay delay) vs Option B: Local Aftermarket delivery ($30 lower part cost, customer SMS authorization required)"* is immediately understood by technical and business judges alike.

---

## 5. Scope Freeze for PartsRescue AI

PartsRescue AI is formally defined around **Problem P7**:
* **Product Identity:** An autonomous, multi-objective recovery recommendation engine for service parts shortages.
* **Core Action:** Connecting the parts counter, service drive, and shop dispatch to evaluate sourcing trade-offs, enforce warranty compliance, and execute 1-click recovery plans with mandatory human-in-the-loop oversight.
