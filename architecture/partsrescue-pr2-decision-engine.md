# PartsRescue PR2: Multi-Objective Decision Engine Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `architecture/partsrescue-pr2-decision-engine.md`  
**Phase:** PR2 — Product Opportunity Definition & Technical Architecture Specification  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Design Authority:** Operations Research & Optimization Specialist, Principal Automotive Product Architect  
**Date:** November 14, 2026  

---

## 1. Problem Statement & Mathematical Formulation

When an active repair order (RO) encounters an unexpected parts shortage during vehicle disassembly, dealership staff face a multi-dimensional economic trade-off. Sourcing options vary widely across purchase price, shipping/courier fees, transit time, and warranty compliance. 

The core operational dilemma is:
> *Is it economically advantageous to pay an expedited hotshot courier fee (e.g., $25) to acquire a part in 45 minutes, rather than waiting 4 hours for standard shuttle delivery, when a stalled lift costs the dealership $160/hr in lost labor capacity?*

The **Multi-Objective Decision Engine** solves this trade-off deterministically.

---

## 2. Formal Mathematical Model

Let $\mathcal{K} = \{1, 2, \dots, K\}$ be the discrete set of all discovered sourcing candidate options for a specific unfulfilled part on active Repair Order $r$.

### 2.1 The Net Operational Impact Function

For each candidate option $k \in \mathcal{K}_{\text{feasible}}$, the total operational recovery cost function $\Omega(k)$ is defined as:

$$\Omega(k) = C_{\text{direct}}(k) + \Psi_{\text{capacity}}(k) + \Theta_{\text{promise}}(k)$$

Where:
* **$C_{\text{direct}}(k) = C_{\text{part}}(k) + C_{\text{freight}}(k)$:** Landed direct procurement cost ($ USD).
  * $C_{\text{part}}(k)$: Wholesale acquisition cost of candidate part.
  * $C_{\text{freight}}(k)$: Expedited hotshot courier or freight fee ($15 - $35 local courier; $0 standard stock delivery).
* **$\Psi_{\text{capacity}}(k)$:** Capacity opportunity cost of unabsorbed technician stall:
  $$\Psi_{\text{capacity}}(k) = GP_{\text{labor}} \cdot (1 - \alpha_{\text{reassign}}) \cdot \max\left(0, T_{\text{bench}}(k) - T_{\text{buffer}}\right)$$
  * $GP_{\text{labor}}$: Dealership labor gross profit per billed hour (calibrated at $\$110.00/\text{hr}$ baseline; configurable by dealership controller).
  * $\alpha_{\text{reassign}} \in [0.0, 1.0]$: Shop Reassignment Factor (e.g. $0.85$ when vehicle blocks a specialized hoist; $0.30$ in normal shop load with alternate jobs).
  * $T_{\text{bench}}(k)$: True part availability time at the technician's workstation (5-stage logistics timeline: $t_{\text{order}} + t_{\text{transit}} + \Delta t_{\text{dock-to-bench}}$).
  * $T_{\text{buffer}}$: Remaining productive teardown/inspection work available on RO before work stoppage (typically $0.5 \text{ hr}$).
* **$\Theta_{\text{promise}}(k)$:** Customer delivery promise impact:
  $$\Theta_{\text{promise}}(k) = \begin{cases}
  0 & \text{if } T_{\text{complete}}(k) \le T_{\text{promise}} \\
  C_{\text{loaner}} \cdot \left\lceil \frac{T_{\text{complete}}(k) - T_{\text{promise}}}{8} \right\rceil + P_{\text{csi}} & \text{if } T_{\text{complete}}(k) > T_{\text{promise}}
  \end{cases}$$
  * $C_{\text{loaner}}$: Daily loaner car / alternative mobility cost ($\$45 - \$65/\text{day}$).
  * $P_{\text{csi}}$: Customer satisfaction / goodwill threshold penalty ($\$25.00$ illustrative placeholder).

---

### 2.2 Hard Feasibility Constraints

A candidate option $k$ is feasible if and only if it satisfies all four deterministic gating constraints:

$$\Phi(k) = F(k) \land A(k) \land W(k) \land S(k) = 1$$

Where:
1. **Mechanical Fitment Gate ($F(k) \in \{0, 1\}$):**
   $$F(k) = 1 \iff \text{Part } k \text{ is verified OEM exact match, supersession successor, or ACES-certified substitute.}$$
   *If $F(k) = 0$, candidate $k$ is immediately pruned.*

2. **Commercial Availability Gate ($A(k) \in \{0, 1\}$):**
   $$A(k) = 1 \iff Q_{\text{available}}(k) \ge Q_{\text{required}}$$
   *The vendor must have verified unallocated inventory on hand.*

3. **Warranty Policy Compliance Gate ($W(k) \in \{0, 1\}$):**
   $$W(k) = \begin{cases} 
   1 & \text{if PayType}(r) \in \{\text{Customer-Pay}\} \\
   1 & \text{if PayType}(r) \in \{\text{OEM Warranty}\} \land \text{Tier}(k) \in \{\text{OEM Original}, \text{OEM Tier-2}\} \\
   1 & \text{if PayType}(r) \in \{\text{Aftermarket VSC}\} \land \text{Tier}(k) \in \{\text{OEM}, \text{CAPA/Tier-1 Aftermarket}\} \\
   0 & \text{otherwise}
   \end{cases}$$
   *Under factory warranty, non-OEM parts strictly yield $W(k) = 0$.*

4. **Supplier Credentialing Gate ($S(k) \in \{0, 1\}$):**
   $$S(k) = 1 \iff \text{Supplier has an active accounts-payable ledger in DMS and credit limit is unblocked.}$$

The feasible candidate set is defined as:
$$\mathcal{K}_{\text{feasible}} = \{k \in \mathcal{K} \mid \Phi(k) = 1\}$$

If $\mathcal{K}_{\text{feasible}} = \emptyset$, the engine triggers the **Exhaustion Fallback Protocol** (vehicle staging to back lot and technician queue resequencing).

---

## 3. Discrete Multi-Objective Pareto-Frontier Solver

Because the candidate pool $\mathcal{K}_{\text{feasible}}$ is small and discrete (typically $3 \le |\mathcal{K}_{\text{feasible}}| \le 8$ options), solving this problem does not require non-linear heuristics or complex Mixed-Integer Linear Programming (MILP) solvers like CP-SAT. 

Instead, PartsRescue utilizes an exact, auditable **Discrete Pareto Dominance Algorithm** that computes in $< 5 \text{ ms}$.

### 3.1 Pareto Dominance Definition
Let each candidate $k$ be characterized by a 3-dimensional outcome vector:
$$\mathbf{v}(k) = \Big( \text{Direct Cost: } C_{\text{direct}}(k), \;\; \text{Downtime: } T_{\text{downtime}}(k), \;\; \text{Gross Margin: } M(k) \Big)$$
Where:
* $C_{\text{direct}}(k) = C_{\text{part}}(k) + C_{\text{courier}}(k)$
* $T_{\text{downtime}}(k) = \max\left(0, T_{\text{eta}}(k) - T_{\text{free}}\right)$
* $M(k) = \text{Price}_{\text{customer}} - C_{\text{part}}(k)$

Candidate $k_1$ **dominates** candidate $k_2$ ($k_1 \succ k_2$) if and only if:
1. $k_1$ is no worse than $k_2$ on all three dimensions ($C_{\text{direct}}(k_1) \le C_{\text{direct}}(k_2)$, $T_{\text{downtime}}(k_1) \le T_{\text{downtime}}(k_2)$, and $M(k_1) \ge M(k_2)$).
2. $k_1$ is strictly better than $k_2$ in at least one dimension.

All dominated candidates are pruned from the primary recommendation set.

---

### 3.2 Archetype Classification (Avoiding Arbitrary Weighting)

Dealership parts managers and service advisors frequently disagree on subjective weighting coefficients ($w_{\text{cost}}$ vs $w_{\text{speed}}$). To eliminate black-box friction, PartsRescue selects and displays the top options categorized by **explicit operational archetypes**:

```
+========================================================================================================================+
|                                    PARETO RECOMMENDATION ARCHETYPES                                                    |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| Archetype Tag     | Objective Prioritized      | Formal Selection Rule             | Typical Real-World Sourcing Path  |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 1:**  | **Minimum Bay Downtime**   | $\arg\min_{k} T_{\text{eta}}(k)$ | Sister-store hotshot courier      |
| *Fastest*         | (Protects lift & CSI)      | subject to $k \in \mathcal{K}_f$ | (Arrives in 45 min; +$25 courier) |
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 2:**  | **Lowest Landed Cost**     | $\arg\min_{k} C_{\text{direct}}(k)$| Commercial aftermarket jobber or |
| *Most Economical* | (Maximizes part GP)        | subject to $k \in \mathcal{K}_f$ | standard morning stock replenishment|
+-------------------+----------------------------+-----------------------------------+-----------------------------------+
| **ARCHETYPE 3:**  | **Optimal Operational**    | $\arg\min_{k} J(k)$               | Evaluates courier cost vs dead    |
| *Recommended*     | **Total Cost Trade-Off**   | subject to $k \in \mathcal{K}_f$ | bay opportunity cost ($160/hr)    |
+========================================================================================================================+
```

---

## 4. Explainable Decision Rationale & Card Generation

The output of the Decision Engine is not a raw numerical score. It is rendered into a transparent, human-readable **Action Card** presented to the Parts Counterperson:

```
+========================================================================================================================+
| [RECOMMENDED ACTION] SOURCING CARD: Brake Caliper Assembly (Part #BRK-44021)                                           |
+------------------------------------------------------------------------------------------------------------------------+
| REPAIR ORDER: #104928 | BAY: #04 (Hoist Lift) | TECH: Mike R. (Flat-Rate Master) | PAY TYPE: Customer-Pay               |
| DOWNTIME COST: $160.00/hr | BUFFER TIME: 30 mins | REMAINING PROMISE TIME: 3.5 hrs                             |
+------------------------------------------------------------------------------------------------------------------------+
| OPTION 1 (RECOMMENDED - OPTIMAL TRADEOFF):                                                                            |
|   Source: Metro Sister-Store #4 (12 miles away)                                                                       |
|   Part Cost: $142.00 | Hotshot Courier: $28.00 | Total Landed: $170.00                                                 |
|   Delivery ETA: 45 minutes (Net Dead Bay Time: 15 mins = $40.00 labor impact)                                         |
|   TOTAL OPERATIONAL IMPACT: $210.00                                                                                    |
|   >> RATIONALE: Spending $28.00 on courier saves $240.00 in dead bay labor compared to tomorrow's stock delivery.     |
+------------------------------------------------------------------------------------------------------------------------+
| OPTION 2 (FASTEST - PREMIUM EXPEDITE):                                                                                 |
|   Source: AutoZone Commercial Hub #12 (3 miles away)                                                                  |
|   Part Cost: $168.00 (Tier-1 Duralast Gold) | Delivery Fee: $12.00 | Total Landed: $180.00                                |
|   Delivery ETA: 25 minutes (Net Dead Bay Time: 0 mins = $0.00 labor impact)                                           |
|   TOTAL OPERATIONAL IMPACT: $180.00 + Customer Approval Required                                                       |
|   >> RATIONALE: Zero bay downtime; requires customer SMS authorization for aftermarket substitution.                   |
+------------------------------------------------------------------------------------------------------------------------+
| OPTION 3 (STATUS QUO - OVERNIGHT OEM PDC):                                                                             |
|   Source: OEM Regional Parts Distribution Center (PDC)                                                                 |
|   Part Cost: $138.00 | Standard Stock Freight: $0.00 | Total Landed: $138.00                                           |
|   Delivery ETA: Tomorrow 08:30 AM (Net Dead Bay Time: 4.5 hrs = $720.00 labor hold)                                   |
|   TOTAL OPERATIONAL IMPACT: $858.00                                                                                    |
|   >> WARNING: Exceeds customer promise time by 18 hours. Requires pushing vehicle out of bay.                         |
+========================================================================================================================+
```

---

## 5. Verification & Boundary Proof
- **Computational Complexity:** $O(|\mathcal{K}| \log |\mathcal{K}|)$ where $|\mathcal{K}| \le 8$. Run time is guaranteed $< 10 \text{ ms}$.
- **Zero Hallucination Guarantee:** The rankings and cost values are generated entirely by the deterministic objective function $J(k)$. The LLM is only utilized to concatenate the values into the natural-language rationale strings.
- **Traceability:** Mathematical parameters directly link to PR1.1 financial reconciliation ($160/hr door rate, 3.5 hr average bay delay, $15–$35 courier fees).
