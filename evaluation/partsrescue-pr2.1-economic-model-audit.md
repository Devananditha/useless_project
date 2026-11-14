# PartsRescue PR2.1: Economic Model & Operational Cost Function Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-economic-model-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** Financial and Operational Modelling Analyst, Senior Automotive Dealership Operations Architect  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Purpose

In Phase PR2, the decision engine relied on an unvalidated, simplified objective function:
$$J_{\text{PR2}}(k) = C_{\text{part}}(k) + C_{\text{courier}}(k) + C_{\text{bay\_hold}} \cdot \max(0, T_{\text{eta}}(k) - T_{\text{free}}) + P_{\text{cust}}(k) \cdot \max(0, T_{\text{eta}}(k) - T_{\text{promise}})$$

This formulation contained critical economic flaws:
1. **Conflating Customer Door Rate with Opportunity Cost:** Equated $C_{\text{bay\_hold}}$ with the dealership's $\$160/\text{hr}$ posted retail door rate as if every stalled hour is pure lost cash.
2. **Double-Counting Economic Losses:** Assumed that bay holding cost, lost labor revenue, technician idle time, and customer delay penalties were independent additive losses.
3. **Ignoring Reassignment Elasticity:** Assumed the technician produces zero value while waiting for a part, ignoring real-world job resequencing and buffer tasks.
4. **Ambiguous ETA Semantics:** Failed to distinguish between supplier order acceptance, warehouse shipping, physical dealership dock arrival, parts verification, and actual bench availability for installation.

This document dismantles these unsupported assumptions, establishes an economically defensible mathematical formulation, and clarifies operational parameter classifications.

---

## 2. Challenging the Door-Rate Assumption

### 2.1 The Economic Reality of Dealership Service Labor
A dealership's posted labor rate (e.g., $\$160.00/\text{hr}$) represents the gross retail billing rate charged to customers for customer-pay mechanical labor. It is **not** equivalent to:
* **Technician Compensation:** Dealership technicians are typically compensated on a flat-rate flag-hour system ($\$32.00 - \$48.00/\text{hr}$ flagged), subject to state minimum wage guarantees or minimum attendance hours.
* **Labor Gross Profit:** Dealership labor gross margin typically ranges from $60\%$ to $70\%$. At a $\$160/\text{hr}$ door rate, the gross profit per billed hour is approximately $\$100.00 - \$112.00/\text{hr}$ (consistent with the $\$110.00/\text{hr}$ baseline reconciled in PR1.1).
* **Actual Cash Loss:** A stalled bay does not incur $\$160/\text{hr}$ in out-of-pocket cash loss. It represents an **unrealized labor capacity opportunity cost**, which only converts to an actual financial loss if the lost hours cannot be absorbed or rescheduled within the shop's operational planning horizon.

```
+========================================================================================================================+
|                                    DEALERSHIP LABOR COST COMPONENT DECOMPOSITION                                       |
+--------------------------+-----------------------+-----------------------+---------------------------------------------+
| Financial Component      | Typical Value Range   | PR2 Fallacy           | Correct Operational Treatment               |
+--------------------------+-----------------------+-----------------------+---------------------------------------------+
| **Posted Retail Door     | $\$150 - \$190/\text{hr}$| Treated as cash loss  | Top-line billing rate; only realized when   |
| Rate ($R_{\text{door}}$) | (Illustrative: $160)  | per hour of stall.    | labor is billed and collected.              |
+--------------------------+-----------------------+-----------------------+---------------------------------------------+
| **Technician Wage Cost   | $\$32 - \$48/\text{hr}$| Ignored; treated tech | Sunk cost if flat-rate; unabsorbed overhead |
| ($W_{\text{tech}}$)**    | (Illustrative: $42)   | as $0 marginal cost.  | if minimum hourly guarantee is triggered.   |
+--------------------------+-----------------------+-----------------------+---------------------------------------------+
| **Labor Gross Profit     | $\$95 - \$125/\text{hr}$| Ignored; substituted  | True economic value of an unrecoverable     |
| ($GP_{\text{labor}}$)**  | (Illustrative: $110)  | with full door rate.  | technician flag hour.                       |
+--------------------------+-----------------------+-----------------------+---------------------------------------------+
| **Unabsorbed Overhead    | $\$20 - \$35/\text{hr}$| Conflated with door   | Fixed facility overhead allocated across    |
| / Bay Cost**             | (Facility allocation) | rate.                 | bay operational hours.                      |
+========================================================================================================================+
```

### 2.2 Deferred Revenue vs. Truly Lost Capacity
When a vehicle encounters a parts shortage:
1. **Deferred Repair Revenue:** The labor on the delayed vehicle is rarely cancelled; the customer still pays for the repair once the part arrives. The revenue is *delayed*, not erased.
2. **Capacity Displacement:** The true loss occurs if the technician stands idle, or if a disassembled vehicle blocks a hoist lift so that *another scheduled vehicle* cannot be serviced, causing that second job to walk away or spill into overtime.
3. **Reassignment Elasticity ($\alpha_{\text{reassign}}$):** In real dealership shops, if a part is delayed, the technician can often:
   * Perform teardown, multi-point inspection (MPI), or auxiliary maintenance on the same RO.
   * Clock onto another waiting quick-service or recall ticket.
   * Move to an adjacent flat bay if the vehicle is immobilized on a lift.

Therefore, the opportunity cost of delay must be discounted by the **Shop Reassignment Factor** $\alpha_{\text{reassign}} \in [0.0, 1.0]$:
* $\alpha_{\text{reassign}} = 1.0$: Fully blocked (single hoist, disassembled suspension, no alternative work available). Total loss of gross profit capacity.
* $\alpha_{\text{reassign}} = 0.2$: High reassignability (technician has 3 other repair orders staged in queue and an open stall). Only $20\%$ of downtime causes unrecoverable capacity loss.

---

## 3. Redesigned Economic Model & Objective Function

To eliminate double-counting and establish rigorous mathematical foundations, PartsRescue PR2.1 establishes the **Operational Recovery Evaluation Model**.

### 3.1 The Net Operational Impact Function

For each candidate sourcing option $k \in \mathcal{K}_{\text{feasible}}$, the total operational recovery cost $\Omega(k)$ is defined as:

$$\Omega(k) = C_{\text{direct}}(k) + \Psi_{\text{capacity}}(k) + \Theta_{\text{promise}}(k)$$

Where:

#### 1. Direct Landed Procurement Cost ($C_{\text{direct}}(k)$):
$$C_{\text{direct}}(k) = C_{\text{part}}(k) + C_{\text{freight}}(k) + C_{\text{core\_net}}(k)$$
* $C_{\text{part}}(k)$: Wholesale acquisition cost of the part ($ USD).
* $C_{\text{freight}}(k)$: Direct freight or hotshot courier fee ($ USD).
* $C_{\text{core\_net}}(k)$: Unreturned core deposit liability or net core processing cost ($ USD).

#### 2. Capacity Opportunity Cost ($\Psi_{\text{capacity}}(k)$):
$$\Psi_{\text{capacity}}(k) = GP_{\text{labor}} \cdot (1 - \alpha_{\text{reassign}}) \cdot \max\left(0, T_{\text{bench}}(k) - T_{\text{buffer}}\right)$$
* $GP_{\text{labor}}$: Dealership labor gross profit per hour (default baseline: $\$110.00/\text{hr}$, configurable by dealership).
* $\alpha_{\text{reassign}} \in [0.0, 1.0]$: Shop Reassignment Factor (configurable; defaults to $0.30$ in normal shop load, $0.85$ when vehicle blocks a specialized rack with no spare bay).
* $T_{\text{bench}}(k)$: True part availability time at the technician's workstation (in hours from $t_0$).
* $T_{\text{buffer}}$: Remaining productive work available on the current RO before total work stoppage (in hours; defaults to $0.5 \text{ hr}$ teardown buffer).

#### 3. Customer Promise Impact ($\Theta_{\text{promise}}(k)$):
$$\Theta_{\text{promise}}(k) = \begin{cases}
0 & \text{if } T_{\text{complete}}(k) \le T_{\text{promise}} \\
C_{\text{loaner}} \cdot \left\lceil \frac{T_{\text{complete}}(k) - T_{\text{promise}}}{8} \right\rceil + P_{\text{csi}} & \text{if } T_{\text{complete}}(k) > T_{\text{promise}}
\end{cases}$$
* $T_{\text{complete}}(k) = T_{\text{bench}}(k) + T_{\text{install}}$: Estimated repair completion time.
* $T_{\text{promise}}$: Customer promise delivery timestamp.
* $C_{\text{loaner}}$: Incremental dealership cost of providing alternative transportation / loaner vehicle per day (typically $\$45.00 - \$65.00/\text{day}$).
* $P_{\text{csi}}$: Fixed customer goodwill / CSI risk penalty threshold (illustrative: $\$25.00$ for missing same-day promise).

---

## 4. Parameter Classification: Facts vs. Placeholders

To ensure compliance with `.cursor/rules/research-standards.mdc`, every parameter in the economic model is categorized:

```
+========================================================================================================================+
|                                    ECONOMIC PARAMETER CLASSIFICATION MATRIX                                            |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Parameter Symbol         | Description           | Value Classification| Source & Calibration Methodology              |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $C_{\text{part}}(k)$     | Wholesale part cost   | **OBSERVED FACT**   | Sourced directly from vendor quote / DMS cost.|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $C_{\text{freight}}(k)$  | Courier / shipping fee| **OBSERVED FACT**   | Quoted by courier API or vendor shipping rate.|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $GP_{\text{labor}}$      | Labor gross profit/hr | **CONFIGURABLE**    | Configured by dealership controller (PR1.1    |
|                          |                       | (Dealer Input)      | benchmark: $110/hr; typical: $95–$125/hr).     |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $\alpha_{\text{reassign}}$| Reassignment factor  | **ESTIMATED**       | Shop load estimate: 0.85 for blocked hoist;   |
|                          |                       | (Dynamic Context)   | 0.30 for general flat stall with backlogged ROs|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $T_{\text{buffer}}$      | Tech buffer hours     | **ESTIMATED**       | Service advisor or technician input           |
|                          |                       | (RO Context)        | (default: 0.5 hr teardown allowance).         |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $C_{\text{loaner}}$      | Daily loaner car cost | **CONFIGURABLE**    | Dealership fleet operating cost ($45–$65/day).|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| $P_{\text{csi}}$         | Goodwill penalty      | **ILLUSTRATIVE**    | Heuristic placeholder ($25); dealership can   |
|                          |                       | (Policy Input)      | zero out if no CSI bonus is at risk.          |
+========================================================================================================================+
```

---

## 5. Precise ETA Semantics Pipeline

In PR2, $T_{\text{eta}}$ was used loosely as "delivery time." In dealership operations, a part sitting on the receiving dock is useless to a technician until it is checked in, tagged, and delivered to the bay.

PartsRescue PR2.1 formally decomposes part arrival into a **5-Stage Logistics Timeline**:

```
+-------------------+      +-------------------+      +-------------------+      +-------------------+      +-------------------+
|     STAGE 1:      |      |     STAGE 2:      |      |     STAGE 3:      |      |     STAGE 4:      |      |     STAGE 5:      |
|  Order Placed &   | ---> | Vendor Dispatch & | ---> | Dealership Dock   | ---> | Parts Check-In &  | ---> | Technician Bench  |
|  Vendor Accepted  |      | Courier Transit   |      | Physical Arrival  |      | Tagging (Receiving|      | Availability      |
|     (t_order)     |      |    (t_transit)    |      |     (t_dock)      |      |     (t_checkin)   |      |     (t_bench)     |
+-------------------+      +-------------------+      +-------------------+      +-------------------+      +-------------------+
```

### 5.1 Formal Mathematical Definitions
1. **$t_{\text{order}}$:** Timestamp when dealership counterperson approves and releases the PO.
2. **$t_{\text{transit}}$:** Elapsed duration for supplier pick, pack, and courier transit.
3. **$t_{\text{dock}} = t_{\text{order}} + t_{\text{transit}}$:** Physical delivery to dealership receiving door.
4. **$t_{\text{checkin}} = t_{\text{dock}} + \Delta t_{\text{receive}}$:** Verification of packing slip, barcode scan, and damage inspection ($\Delta t_{\text{receive}} \approx 10 - 15 \text{ mins}$).
5. **$t_{\text{bench}} = t_{\text{checkin}} + \Delta t_{\text{stage}}$:** Physical transfer to technician tool cart or parts counter pickup shelf ($\Delta t_{\text{stage}} \approx 5 - 10 \text{ mins}$).

**Mandate:** The decision engine **must use $t_{\text{bench}}$ (True Installation Availability)** when calculating capacity holding cost and customer promise impact, adding an operational receiving buffer $\Delta t_{\text{dock-to-bench}} \approx 20 \text{ minutes}$ to raw courier arrival estimates.

---

## 6. Uncertainty & Sensitivity Modeling

The decision engine must not present point estimates as absolute certainty. Sourcing decisions operate under real-world operational variance:
1. **Courier Transit Jitter:** Traffic congestion can cause delivery variance of $\pm 15 - 30$ minutes.
2. **Supplier Stock Accuracy:** Sourcing channels carry inventory risk ($\Gamma_{\text{inv}} < 1.0$).
3. **Technician Reassignment Ambiguity:** Reassignment capacity depends on unpredictable shop flow.

### 6.1 Range-Based Evaluation Protocol
When candidate options are evaluated, the system computes both:
* **Expected Cost:** $\Omega_{\text{expected}}(k)$ using nominal parameters.
* **Adverse Scenario (Worst-Case):** $\Omega_{\text{adverse}}(k)$ injecting $+30 \text{ mins}$ traffic delay and zero technician reassignment ($\alpha_{\text{reassign}} = 1.0$).

If a candidate remains dominant under both expected and adverse scenarios, it is tagged as **HIGH-CONFIDENCE DOMINANT**. If dominance flips under the adverse scenario, the decision card explicitly surfaces this sensitivity to the counterperson:
> *"Option 1 is optimal if courier arrives within 45 mins. If traffic delays exceed 75 mins, Option 2 (Stock Shuttle) carries lower net cost risk."*

---

## 7. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Impacted Documents:**
  * `architecture/partsrescue-pr2-decision-engine.md`: Must be updated to replace $J_{\text{PR2}}(k)$ with the redesigned $\Omega(k)$ formulation and 5-stage ETA pipeline.
  * `evaluation/partsrescue-pr2-demo-blueprint.md`: Financial calculations must use $GP_{\text{labor}} = \$110/\text{hr}$ and explicit reassignment factor $\alpha_{\text{reassign}}$ instead of raw $\$160/\text{hr}$ door rate.
  * `evaluation/partsrescue-pr2-final-report.md`: Section D must reflect the corrected economic definitions.
