# Canonical Fixture Specification: S-MATH-02
## Null-Benefit / Cheap-Source-Wins Control Scenario

**Workspace:** `TEKION-HACKATHON-2026`  
**Fixture ID:** `S-MATH-02`  
**Fixture Type:** Deterministic Synthetic Control Fixture  
**Epistemic Status:** `[SYNTHETIC]` (Specification & Hand-Calculation; transitions to `[MEASURED-SYNTH]` upon execution)  
**Category:** Null-Benefit / Bottleneck-Constrained Decision Benchmark  
**Date:** November 15, 2026 (Phase 0.1 Corrected)

---

## 1. Scenario Purpose & Scientific Justification

A common failure mode in automated service dispatch optimizers is the "expedited freight bias": the solver habitually recommends premium courier parts ($50–$150 freight surcharges) under the naive assumption that faster part arrival always improves shop throughput.

`S-MATH-02` is an indispensable **negative control scenario**. It models a realistic operational situation where:
1. Two eligible parts sources exist: a fast, expensive courier source ($S1: \$55.00$, ready at $t=26$) and a slower, cheaper logistics source ($S2: \$18.00$, ready at $t=48$).
2. Prior repair order **RO-1030** occupies Master Technician K2 from $t = 0$ to $t = 60$ (08:00 AM to 13:00 PM).
3. Downstream repair order **RO-1051** requires Master Technician K2 and has service duration 24 ticks (120 minutes) with customer promise $t = 90$ (15:30 PM).
4. Both parts (S1 at $t=26$, S2 at $t=48$) arrive and become usable **before** Technician K2 becomes available at $t=60$.
5. Therefore, paying for the faster source yields **zero customer-promise improvement** and **zero weighted-lateness reduction**.
6. The only rational, cost-effective decision under lexicographic optimization is to select the cheaper source ($S2$), saving $\$37.00$.

This scenario proves that StallBreaker's CP-SAT engine does not blindly burn dealership parts budgets when downstream bottlenecks prevent on-time gains.

---

## 2. Complete Input Specification

### 2.1 Timeline & Facility Parameters
- **Time Unit:** 5 minutes per discrete tick ($H = 108$ ticks, 08:00 AM to 17:00 PM).
- **Disruption Discovery Time ($t_{current}$):** $t = 21$ (09:45 AM).
- **Service Facility:** Rooftop 1, Bay B4.
- **Clearance Transit Duration ($k_{clear}$):** 2 ticks (10 minutes).
- **Holding Area H2:** 0 available stalls (vehicle is immobilized regardless).

---

### 2.2 Complete Preceding Technician & Repair Order Assignments

#### Preceding Commitment: RO-1030
- **RO Identifier:** `RO-1030`
- **Operation:** Engine Recall / Timing Chain Replacement
- **Assigned Technician:** Master Tech K2
- **Scheduled Time Window:** $t = 0 \to 60$ (08:00 AM – 13:00 PM, 60 ticks / 300 minutes)
- **Status:** In progress, strictly occupies Tech K2 until $t = 60$. Tech K2 earliest available tick is **$t = 60$ (13:00 PM)**.

#### Evaluated Repair Orders

| Parameter | RO-1042 (On-Hoist Vehicle) | RO-1051 (Queued Vehicle) |
|---|---|---|
| **Vehicle Model** | Ford Explorer | Ford F-150 Commercial Fleet |
| **Current Location** | Hoist Bay B4 | Staging Lane / Queue |
| **Physical Condition** | Wheels Detached (`PARTIALLY_DISMANTLED`) | Intact, Rolling (`SAFE_TO_MOVE`) |
| **Rollable Flag (`is_rollable`)** | `False` | `True` |
| **Required Shop Bay** | Bay B4 | Bay B4 |
| **Assigned Technician** | Tech K1 (Available at $t=21$) | **Master Tech K2 (Occupied until $t=60$)** |
| **Technician Earliest Start** | $t = 21$ (09:45 AM) | **$t = 60$ (13:00 PM)** (Preceding RO-1030) |
| **Service Duration ($d_i$)** | 12 ticks (60 minutes) | 24 ticks (120 minutes) |
| **Clearance Duration ($k_i$)** | 2 ticks (10 minutes) | 2 ticks (10 minutes) |
| **Customer Promise ($P_i$)** | **$t = 84$ (15:00 PM)** | **$t = 90$ (15:30 PM)** |
| **Priority Weight ($w_i$)** | $w_{1042} = 1.0$ (Retail) | $w_{1051} = 3.0$ (Commercial Fleet) |

---

### 2.3 Candidate Parts Sourcing Options

| Attribute | Source S1 (Expedited Courier) | Source S2 (Standard Transfer) |
|---|---|---|
| **Supplier Name** | Hotshot Courier Express | Regional Logistics Hub |
| **Usable-Ready Tick ($A_s$)** | **$t = 26$ (10:10 AM)** | **$t = 48$ (12:00 PM)** |
| **Procurement/Freight Cost ($C_s$)** | **$\$55.00$** | **$\$18.00$** |
| **Available-To-Promise (ATP)** | 1 Unit | 1 Unit |
| **Fitment Verification** | `True` (OEM Matched) | `True` (OEM Matched) |
| **Quote Validity** | `True` (Active) | `True` (Active) |
| **Eligibility Status** | **Eligible** | **Eligible** |

---

## 3. Step-by-Step Hand-Derived Mathematical Evaluation

Both parts arrive before Technician K2 becomes available at $t = 60$:
$$A_{S1} = 26 < 60, \quad A_{S2} = 48 < 60$$

### Evaluation under Expedited Source S1 ($55.00)

1. **RO-1042 Execution (Bay B4, Tech K1):**
   - Parts ready at $A_{S1} = 26$.
   - $\text{start}_{1042} = \max(t_{current}, A_{S1}) = \max(21, 26) = 26$ (10:10 AM).
   - Install ends: $26 + 12 = 38$ (11:10 AM).
   - Clearance ends: $38 + 2 = 40$ (11:20 AM).
   - Completion: $C_{1042} = 40 \le P_{1042} = 84 \implies L_{1042} = \max(0, 40 - 84) = 0\text{ ticks}$.
   - Bay B4 released at $t = 40$.

2. **RO-1051 Execution (Bay B4, Tech K2):**
   - Bay B4 is available at $t = 40$.
   - Technician K2 is committed to RO-1030 until $t = 60$.
   - Earliest start:
     $$\text{start}_{1051}(S1) = \max(\text{Bay B4 Free}, \text{Tech K2 Free}) = \max(40, 60) = \mathbf{60}\text{ (13:00 PM)}$$
   - Completion:
     $$C_{1051}(S1) = 60 + 24 = \mathbf{84}\text{ (15:00 PM)}$$
   - Customer Promise: $P_{1051} = 90$ (15:30 PM).
   - Lateness:
     $$L_{1051}(S1) = \max(0, 84 - 90) = \mathbf{0\text{ ticks}}$$

3. **Objective Values under S1:**
   - Weighted Lateness: $Z_1(S1) = 1.0(0) + 3.0(0) = \mathbf{0.0\text{ ticks}}$
   - Operating Cost: $Z_2(S1) = \mathbf{\$55.00}$

---

### Evaluation under Standard Source S2 ($18.00)

1. **RO-1042 Execution (Bay B4, Tech K1):**
   - Parts ready at $A_{S2} = 48$.
   - $\text{start}_{1042} = \max(t_{current}, A_{S2}) = \max(21, 48) = 48$ (12:00 PM).
   - Install ends: $48 + 12 = 60$ (13:00 PM).
   - Clearance ends: $60 + 2 = 62$ (13:10 PM).
   - Completion: $C_{1042} = 62 \le P_{1042} = 84 \implies L_{1042} = \max(0, 62 - 84) = 0\text{ ticks}$.
   - Bay B4 released at $t = 62$.

2. **RO-1051 Execution (Bay B4, Tech K2):**
   - Bay B4 is available at $t = 62$.
   - Technician K2 is available at $t = 60$.
   - Earliest start:
     $$\text{start}_{1051}(S2) = \max(\text{Bay B4 Free}, \text{Tech K2 Free}) = \max(62, 60) = \mathbf{62}\text{ (13:10 PM)}$$
   - Completion:
     $$C_{1051}(S2) = 62 + 24 = \mathbf{86}\text{ (15:10 PM)}$$
   - Customer Promise: $P_{1051} = 90$ (15:30 PM).
   - Lateness:
     $$L_{1051}(S2) = \max(0, 86 - 90) = \mathbf{0\text{ ticks}}$$

3. **Alternative Direct Sourcing on Disrupted RO-1051:**
   - Even if RO-1051 itself required the part:
     $$\text{start}_{1051}(S1) = \max(26, 60) = 60 \implies C_{1051} = 60 + 24 = 84 \le 90 \implies L_{1051} = 0$$
     $$\text{start}_{1051}(S2) = \max(48, 60) = 60 \implies C_{1051} = 60 + 24 = 84 \le 90 \implies L_{1051} = 0$$
   - In both formulations, both complete at or before $t = 86 \le 90$ with zero lateness.

4. **Objective Values under S2:**
   - Weighted Lateness: $Z_1(S2) = 1.0(0) + 3.0(0) = \mathbf{0.0\text{ ticks}}$
   - Operating Cost: $Z_2(S2) = \mathbf{\$18.00}$

---

## 4. Lexicographic Solver Optimization Outcome

### Pass 1: Primary Objective $Z_1$ (Weighted Lateness)
$$\min Z_1 \quad \implies \quad Z_1(S1) = 0.0, \quad Z_1(S2) = 0.0 \implies Z_1^* = \mathbf{0.0\text{ ticks}}$$

### Pass 2: Secondary Objective $Z_2$ (Freight Cost)
$$\min Z_2 \quad \text{subject to } Z_1 \le 0.0$$
- Candidate S1 cost: $\$55.00$
- Candidate S2 cost: $\$18.00$
- Cost delta: $\$55.00 - \$18.00 = \mathbf{+\$37.00\text{ savings}}$
- **Solver Selection:** **Source S2 is selected**, saving $\$37.00$ with zero customer lateness impact.

---

### Evaluation of Candidate 2: Selecting Cheaper Source S2 ($18.00)

1. **RO-1042 Parts Readiness:** $A_{S2} = 49$ (12:05 PM).
2. **RO-1042 Installation Start:**
   $$\text{start}_{1042} = \max(t_{current}, A_{S2}) = \max(21, 49) = 49\text{ (12:05 PM)}$$
3. **RO-1042 Installation Complete:**
   $$\text{install\_end}_{1042} = 49 + 12 = 61\text{ (13:05 PM)}$$
4. **RO-1042 Clearance & Bay B4 Release:**
   $$\text{clear\_end}_{1042} = 61 + 2 = 63\text{ (13:15 PM)} \implies \text{Bay B4 released at } t = 63$$
5. **RO-1042 Lateness:**
   $$C_{1042} = 63 \le P_{1042} = 84 \implies L_{1042} = \max(0, 63 - 84) = 0\text{ ticks}$$
6. **RO-1051 Scheduling on Bay B4:**
   - Technician K2 is available at $t = 60$ (13:00 PM).
   - Hoist Bay B4 is cleared and available at $t = 63$ (13:15 PM).
   - Earliest feasible start:
     $$\text{start}_{1051} = \max(\text{Bay B4 Available}, \text{Tech K2 Available}) = \max(63, 60) = 63\text{ (13:15 PM)}$$
   - Hoist Bay B4 was productively occupied until 13:15 PM; idle hoist time is reduced to 0 minutes!
7. **RO-1051 Completion & Lateness:**
   $$\text{finish}_{1051} = 63 + 24 = 87\text{ (15:15 PM)}$$
   $$C_{1051} = 87 \le P_{1051} = 90 \implies L_{1051} = \max(0, 87 - 90) = 0\text{ ticks}$$
8. **Objective Values under S2:**
   - Total Weighted Lateness:
     $$Z_1(S2) = w_{1042} \cdot L_{1042} + w_{1051} \cdot L_{1051} = 1.0(0) + 3.0(0) = \mathbf{0.0\text{ ticks}}$$
   - Total Freight Cost:
     $$Z_2(S2) = \mathbf{\$18.00}$$

---

## 4. Lexicographic Solver Optimization Outcome

StallBreaker executes a deterministic two-pass lexicographic optimization:

### Pass 1: Primary Objective $Z_1$ (Weighted Lateness)
$$\min Z_1 \quad \text{subject to operational constraints}$$
- With Source S1: $Z_1 = 0.0$ ticks.
- With Source S2: $Z_1 = 0.0$ ticks.
- Optimal Pass 1 Objective: $Z_1^* = 0.0$ ticks.

### Pass 2: Secondary Objective $Z_2$ (Freight Cost)
$$\min Z_2 \quad \text{subject to } Z_1 \le Z_1^* = 0$$
- Candidate S1 cost: $\$55.00$.
- Candidate S2 cost: $\$18.00$.
- Cost delta: $\$55.00 - \$18.00 = +\$37.00$ waste under S1.
- Optimal Pass 2 Solution: **Source S2 is selected.**

---

## 5. Expected Output Schedule Summary

| Metric | Source S1 (Expedited) | Source S2 (Selected by Solver) | Outcome / Delta |
|---|---|---|---|
| **Selected Source** | S1 | **S2** | Cheaper Source Selected |
| **Selected Movement** | `HOLD_ON_BAY` | `HOLD_ON_BAY` | Feasible (Immobilized) |
| **RO-1042 Install Window** | 10:15 – 11:15 ($t = 27 \to 39$) | 12:05 – 13:05 ($t = 49 \to 61$) | Later, but on-time |
| **Bay B4 First Release** | 11:25 ($t = 41$) | 13:15 ($t = 63$) | +110 min occupancy |
| **RO-1042 Completion** | 11:25 ($t = 41$) | 13:15 ($t = 63$) | On-time ($P=15:00$) |
| **RO-1051 Calibration Window** | 13:00 – 15:00 ($t = 60 \to 84$) | 13:15 – 15:15 ($t = 63 \to 87$) | Delayed by only 15 min |
| **RO-1051 Completion** | 15:00 ($t = 84$) | 15:15 ($t = 87$) | **On-time ($P=15:30$)** |
| **RO-1051 Lateness** | 0 min (0 ticks) | 0 min (0 ticks) | **Zero Penalty** |
| **Total Weighted Lateness ($Z_1$)** | 0.0 ticks | 0.0 ticks | **Tied at 0.0 ticks** |
| **Parts Freight Cost ($Z_2$)** | $\$55.00$ | **$\$18.00$** | **$\$37.00$ Cost Savings** |

---

## 6. Scientific Significance for Benchmarking

1. **Proof of Cost Rationality:** S-MATH-02 proves that StallBreaker does not spend dealership funds on expedited couriers when the faster arrival cannot be monetized into improved delivery promises.
2. **Identification of Artificial Improvement Claims:** In this scenario, any algorithm that claims a "lateness reduction" is mathematically broken, because lateness is already zero under both choices. The true optimization gain is a **$\$37.00$ operating cost reduction**.
3. **Ablation Baseline Differentiation:** In A2 (sequential baseline), if A2 selects S2, A2 and P3 tie in both $Z_1$ ($0.0$) and $Z_2$ ($\$18.00$). This scenario correctly identifies a **tie condition** in the benchmark suite, confirming that the benchmark suite contains legitimate zero-difference scenarios rather than artificially contrived 100% win margins.
