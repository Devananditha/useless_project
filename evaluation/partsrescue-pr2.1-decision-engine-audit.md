# PartsRescue PR2.1: Multi-Objective Decision Engine & Optimization Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-decision-engine-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** Operations Research and Optimization Specialist, Enterprise SaaS Product Architect  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Mandate

In Phase PR2, `architecture/partsrescue-pr2-decision-engine.md` introduced a "Discrete Vector Pareto-Frontier Solver" operating over a candidate pool of $3 \le |\mathcal{K}| \le 8$ sourcing options.

This audit critically interrogates:
1. **Is "Pareto Optimization" Justified or Buzzword Overkill?** In a candidate set of 3 to 8 discrete options, is a Pareto solver mathematically necessary, or is a hard-constraint filter followed by simple ranking completely sufficient?
2. **The Danger of Arbitrary Weighted Sums:** Does blending cost, speed, and CSI into a single scalar score obscure critical trade-offs from the human operator?
3. **Preventing Operationally Toxic Choices:** How does the engine prevent recommending an option that is mathematically $\$10$ cheaper but risks a catastrophic customer CSI dispute or technician walkout?
4. **Handling Missing or Uncertain Data:** What happens when supplier pricing, transit ETAs, or core charges are partially unknown?

---

## 2. Hard Constraints vs. Optimization Preferences

The core architecture must strictly distinguish **Non-Negotiable Feasibility Gates (Hard Constraints)** from **Economic Optimization Trade-Offs (Soft Preferences)**:

```
+========================================================================================================================+
|                                    HARD CONSTRAINTS VS. SOFT PREFERENCES                                               |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Dimension                | Operational Gate Type | Evaluation Logic    | System Action if Violated                     |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Mechanical Fitment**   | **HARD CONSTRAINT**   | Deterministic DAG   | **IMMEDIATE PRUNING:** Zero ranking; candidate|
|                          |                       | / ACES Catalog      | cannot be presented as viable option.         |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Policy Eligibility**   | **HARD CONSTRAINT**   | 6-State Compliance  | **IMMEDIATE PRUNING:** Red-badged if verified |
|                          |                       | Engine              | ineligible under active RO pay-type.          |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Commercial Stock**     | **HARD CONSTRAINT**   | $Q_{\text{avail}}   | **IMMEDIATE PRUNING:** Cannot order a part    |
|                          |                       | \ge Q_{\text{req}}$ | that has 0 physical or in-transit stock.      |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Direct Landed Cost**   | **SOFT PREFERENCE**   | $C_{\text{direct}}$ | Optimization dimension: evaluated against bay |
|                          |                       | (Part + Freight)    | opportunity cost and customer margin.         |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Technician Bench ETA** | **SOFT PREFERENCE**   | $T_{\text{bench}}$  | Optimization dimension: evaluated against     |
|                          |                       | (5-stage timeline)  | bay downtime and customer delivery promise.   |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Customer Promise Slip**| **SOFT PREFERENCE**   | $\Delta T_{\text{promise}}$| Optimization dimension: penalized via loaner  |
|                          |                       |                     | cost and customer satisfaction weight.        |
+========================================================================================================================+
```

---

## 3. Demystifying Pareto Dominance: Why It Is Justified

### 3.1 The Value of Eliminating Dominated Candidates
In a candidate pool of 6 suppliers:
* **Supplier A (Local Jobber):** Landed Cost: $\$150.00$, Delivery: $45 \text{ mins}$.
* **Supplier B (Unfavored Jobber):** Landed Cost: $\$175.00$, Delivery: $60 \text{ mins}$.

Supplier B is **strictly dominated** by Supplier A: it is both more expensive AND takes longer to arrive. 
* A simple Pareto dominance filter removes Supplier B without requiring the user or algorithm to invent arbitrary weighting coefficients ($w_{\text{cost}}$ vs $w_{\text{speed}}$).
* **Verdict:** Pareto filtering is mathematically trivial to compute on small discrete sets ($O(K^2)$ or $O(K \log K)$), but it provides **tremendous user experience value** by instantly decluttering the counterperson's screen and eliminating obviously inferior choices.

### 3.2 The Limitation of Pareto Dominance
Pareto filtering only eliminates inferior options; it **cannot rank non-dominated options**:
* **Option 1:** $\$140.00$ cost, $90 \text{ min}$ arrival.
* **Option 2:** $\$180.00$ cost, $30 \text{ min}$ arrival.

Neither option dominates the other. To help the counterperson choose between Option 1 and Option 2, the system must either:
1. Force an arbitrary weighted formula (which users distrust), OR
2. **Present the Non-Dominated Frontier Classified by Operational Archetypes.**

PartsRescue PR2.1 adopts Approach 2: It exposes the non-dominated candidates classified into **three transparent operational archetypes**, accompanied by the net economic impact calculation $\Omega(k)$.

---

## 4. The 3-Archetype Transparent Presentation Model

Instead of forcing a single "black-box winner", the decision engine maps non-dominated candidates to three clear operational stances:

```
+========================================================================================================================+
|                                    THREE OPERATIONAL ARCHETYPES PRESENTATION                                           |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| Archetype Title   | Operational Priority       | Formal Mathematical Selection     | When It Should Be Chosen          |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 1:**  | **Maximum Bay Speed**      | $\arg\min_{k} T_{\text{bench}}(k)$| Stalled lift blocking service lane|
| *Fastest*         | (Minimizes shop downtime)  | subject to $k \in \mathcal{K}_f$ | or customer waiting in lounge.    |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 2:**  | **Lowest Landed Cost**     | $\arg\min_{k} C_{\text{direct}}(k)$| Vehicle staged in lot; technician |
| *Most Economical* | (Maximizes parts GP)       | subject to $k \in \mathcal{K}_f$ | has 4 other jobs in queue.        |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 3:**  | **Optimal Operational      | $\arg\min_{k} \Omega(k)$          | Standard repair drive stall where |
| *Recommended*     | Trade-Off**                | subject to $k \in \mathcal{K}_f$ | freight cost balances downtime GP.|
+========================================================================================================================+
```

---

## 5. Guardrails Against Operationally Toxic Recommendations

A naive optimization algorithm might recommend an option that is mathematically cheapest on paper but disastrous in practice (e.g., ordering from an unreliable supplier with frequent lost shipments, or selecting a low-tier aftermarket part that barely passes fitment rules).

PartsRescue PR2.1 enforces **four operational guardrails**:

1. **The Minimum Assurance Gate:** If a supplier has an unverified batch inventory status (`UNVERIFIED_BATCH_ESTIMATE`), it cannot be selected as Archetype 3 (Recommended) unless confirmed via an automated real-time ping or counterperson phone verification.
2. **The Cutoff Horizon Guardrail:** If an option's estimated arrival falls within 30 minutes of the technician's shift end (e.g., arrival at 4:30 PM, tech clocks out at 5:00 PM), the engine penalizes the option by adding an overnight holding cost ($8 \text{ hours}$ unbilled bay tie-up).
3. **The Customer Pay-Type Boundary:** The system strictly locks aftermarket parts from being recommended on Factory Warranty or Recall tickets, preventing financially ruinous warranty debit-backs.
4. **Mandatory Human Override:** The counterperson can reject all three archetypes with one click and manually enter a custom supplier requisition.

---

## 6. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Mandatory Modifications Across PR2 Documents:**
  * Update `architecture/partsrescue-pr2-decision-engine.md`: Clearly explain the relationship between Hard Constraint Pruning, Pareto Dominance, and Archetype Selection.
  * Explicitly justify why Pareto analysis is utilized (declutters screen and eliminates dominated options without arbitrary weighting).
  * Document the operational guardrails against toxic recommendations.
