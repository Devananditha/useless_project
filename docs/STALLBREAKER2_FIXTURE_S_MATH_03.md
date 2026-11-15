# Canonical Fixture Specification: S-MATH-03
## Immobilised Vehicle / Physical-State Safety-Critical Gating

**Workspace:** `TEKION-HACKATHON-2026`  
**Fixture ID:** `S-MATH-03`  
**Fixture Type:** Deterministic Safety-Critical Verification Fixture  
**Epistemic Status:** `[SYNTHETIC]` (Specification & Hand-Calculation; transitions to `[MEASURED-SYNTH]` upon execution)  
**Category:** Physical Feasibility & Invariant CE-1 Fail-Closed Gating  
**Date:** November 15, 2026 (Phase 0.1 Corrected)

---

## 1. Scenario Purpose & Scientific Justification

In classical Job Shop Scheduling (JSP) and Operations Research models, jobs are treated as abstract mathematical intervals that can be paused, preempted, or shifted between machines at will. In automotive fixed operations, this assumption is **catastrophically unsafe**.

A vehicle with its steering knuckle, half-shaft, or brake assemblies dismounted cannot simply be "pushed outside" to free up an alignment hoist for a high-priority customer. If an optimizer ignores physical state mechanics, it will generate a mathematically elegant schedule that cannot be executed in the physical world without dropping a vehicle off a lift or causing severe shop injury.

`S-MATH-03` is a **safety-critical counterexample fixture**. It proves that:
1. When a vehicle is physically immobilized on a specialized bay, holding capacity alone does not authorize relocation.
2. Even when an illegal relocation would yield an almost-perfect mathematical objective ($Z_1 = 1.0$ tick vs $Z_1 = 45.0$ ticks), StallBreaker's safety filter **fails closed**.
3. The downstream schedule is strictly constrained by physical reality, enforcing Invariant CE-1 ("The Vehicle-Is-Not-A-Bay").
4. The forbidden counterfactual ($Z_1 = 1.0$ tick) must **never** be counted as a feasible solver result.

---

## 2. Complete Input Specification

### 2.1 Facility & Holding Area Configuration
- **Time Horizon:** $t = 0$ (08:00 AM) to $t = 108$ (17:00 PM), 5 minutes per discrete tick ($H = 108$).
- **Disruption Discovery Time ($t_{current}$):** $t = 21$ (09:45 AM).
- **Service Facility:** Single Rooftop, Specialized Heavy-Duty Alignment Bay B4.
- **Clearance Transit Duration ($k_{clear}$):** 2 ticks (10 minutes).
- **Relocation Transit Duration ($k_{reloc}$):** 3 ticks (15 minutes outbound, 3 ticks return).
- **Holding Area H2 Capacity:**
  - Total Stalls: 2 stalls.
  - **Available Stalls:** **2 available stalls** (Abundant holding capacity!).

---

### 2.2 Vehicle & Repair Order Parameters

| Parameter | RO-1042 (Disrupted Vehicle) | RO-1051 (Queued Commercial Fleet) |
|---|---|---|
| **Vehicle Model** | Ford Explorer | Ford F-150 Commercial Fleet |
| **Current Location** | Hoist Bay B4 | Staging Lane / Queue |
| **Physical Vehicle State** | **`PARTIALLY_DISMANTLED`** | `SAFE_TO_MOVE` |
| **Wheel / Hub Assembly** | **Dismounted; on hoist arms** | Fully Assembled, Rolling |
| **Technician Safety Signoff** | **`False` (No relocation signoff recorded)** | `True` |
| **Rollable Precondition (`is_rollable`)** | **`False` (Strictly Immobilized)** | `True` |
| **Required Shop Bay** | Bay B4 (Heavy-Duty Alignment Hoist) | Bay B4 (Heavy-Duty Alignment Hoist) |
| **Service Operation** | Steering Gear Reassembly & Reinstallation | Fleet ADAS Calibration |
| **Service Duration ($d_i$)** | 12 ticks (60 minutes) | 24 ticks (120 minutes) |
| **Clearance Duration ($k_i$)** | 2 ticks (10 minutes) | 2 ticks (10 minutes) |
| **Customer Promise ($P_i$)** | $t = 66$ (13:30 PM) | **$t = 50$ (12:10 PM)** (Urgent Fleet Promise!) |
| **Priority Weight ($w_i$)** | $w_{1042} = 1.0$ (Retail Customer) | **$w_{1051} = 3.0$ (Commercial Fleet Account)** |

---

### 2.3 Candidate Parts Sourcing Options for RO-1042

| Attribute | Source S1 (Expedited Courier) | Source S2 (Regional Logistics Hub) |
|---|---|---|
| **Physical Delivery Clock** | 10:00 AM ($t = 24$) | 11:50 AM ($t = 46$) |
| **Receiving / Processing** | 3 ticks (15 minutes) | 3 ticks (15 minutes) |
| **Usable-Ready Tick ($A_s$)** | **$t = 27$ (10:15 AM)** | **$t = 49$ (12:05 PM)** |
| **Freight Surcharge ($C_s$)** | **$\$55.00$** | **$\$18.00$** |
| **Available-To-Promise (ATP)** | 1 Unit | 1 Unit |
| **Fitment Verification** | `True` (OEM Verified) | `True` (OEM Verified) |
| **Quote Validity** | `True` (Locked 60m) | `True` (Locked 60m) |
| **Eligibility Status** | **Eligible** | **Eligible** |

---

## 3. The Mathematical Temptation vs Physical Reality

### 3.1 Forbidden Counterfactual: The Physically Impossible Relocation

> [!CAUTION]
> **FORBIDDEN COUNTERFACTUAL (PHYSICALLY UNREALIZABLE)**  
> The following calculation represents what an unconstrained solver would hallucinate if physical safety gates were bypassed. It must NEVER be reported as a feasible solution or operational achievement.

Suppose an unconstrained optimizer observes that Holding Area H2 has 2 open stalls, ignores the vehicle's dismounted wheels, and authorises `RELOCATE_TO_H2`:

1. RO-1042 transits to H2 at $t = 21 \to 24$ (3 ticks).
2. Hoist Bay B4 is declared "free" at $t = 24$ (10:00 AM).
3. RO-1051 enters Bay B4 immediately at $t = 24$, running for 24 ticks until $t = 48$ (12:00 PM).
4. RO-1051 finishes at 12:00 PM $\le$ Promise 12:10 PM ($t = 50$):
   $$L_{1051}^{illegal} = \max(0, 48 - 50) = \mathbf{0\text{ ticks lateness}}$$
5. Bay B4 post-service clearance: $t = 48 \to 50$ (2 ticks).
6. RO-1042 returns at $t = \max(50, A_{S2}) = \max(50, 49) = 50$.
7. Return transit takes 3 ticks: $t = 50 \to 53$.
8. Reassembly install takes 12 ticks: $t = 53 \to 65$.
9. Final clearance takes 2 ticks: $t = 65 \to 67$ (13:35 PM).
10. RO-1042 lateness: $C_{1042} - P_{1042} = 67 - 66 = 1$ tick (5 minutes).
11. **Hallucinated Objective:**
    $$Z_1^{counterfactual} = 1.0(1) + 3.0(0) = \mathbf{1.0\text{ tick}}\quad (\text{Freight: } \$18.00)$$

**Physical Shop Consequence:** The vehicle is resting on bare brake rotors on hoist arms. Attempting to roll or drag it across the shop floor damages the vehicle, drops it from the hoist, destroys shop equipment, and poses immediate bodily risk to technicians.

---

### 3.2 The Fail-Closed Physical Feasibility Gate

StallBreaker's Pre-Solver Feasibility Filter evaluates Candidate Movement Option $M = \text{RELOCATE\_TO\_H2}$:

```python
def validate_relocation_feasibility(snapshot):
    # Rule SG-1: Rollability Precondition
    if not snapshot.ro1042.is_rollable or snapshot.ro1042.current_vehicle_state == VehicleState.PARTIALLY_DISMANTLED:
        return False, "VEHICLE_NOT_ROLLABLE"
    
    # Rule SG-2: Explicit Certified Technician Signoff
    if not snapshot.ro1042.technician_signoff_recorded:
        return False, "MISSING_TECHNICIAN_SIGNOFF"
    
    # Rule SG-3: Spatial Holding Capacity
    if snapshot.h2_available_stalls < 1:
        return False, "HOLDING_CAPACITY_EXCEEDED"
        
    return True, "FEASIBLE"
```

- **Rule SG-1 Evaluation:** State is `PARTIALLY_DISMANTLED`, `is_rollable == False` $\implies$ **FAILED**.
- **Rule SG-2 Evaluation:** `technician_signoff_recorded == False` $\implies$ **FAILED**.
- **Rule SG-3 Evaluation:** $2 \ge 1$ $\implies$ Passed, but **insufficient** because Rules SG-1 and SG-2 failed.
- **Result:** `RELOCATE_TO_H2` is **REJECTED AND PRUNED BEFORE OPTIMIZATION**.
- **Invariant CE-1 Enforced:** Bay B4 remains locked in state `OCCUPIED`.

---

## 4. Legitimate Solver Optimization under Physical Invariant

Because `RELOCATE_TO_H2` is pruned, the solver is strictly restricted to `HOLD_ON_BAY`.

### Option A: Selecting Expedited Source S1 ($55.00)
1. RO-1042 parts usable at $A_{S1} = 27$ (10:15 AM).
2. Install runs $t = 27 \to 39$ (11:15 AM, 12 ticks).
3. Clearance transit runs $t = 39 \to 41$ (11:25 AM, 2 ticks).
4. **Bay B4 First Release:** $t = 41$ (11:25 AM).
5. RO-1042 finish tick = 41. Promise = 66.
   $$L_{1042} = \max(0, 41 - 66) = 0\text{ ticks}$$
6. **RO-1051 Execution on Bay B4:**
   - Starts immediately upon Bay B4 release: $t = 41$ (11:25 AM).
   - Service runs for 24 ticks: $t = 41 + 24 = 65$ (13:25 PM).
   - RO-1051 finish tick = 65. Promise = 50 (12:10 PM).
   - Lateness $L_{1051} = 65 - 50 = 15$ ticks (75 minutes late).
7. **Objective Values under S1:**
   $$Z_1(S1) = 1.0(0) + 3.0(15) = \mathbf{45.0\text{ weighted ticks}}$$
   $$Z_2(S1) = \mathbf{\$55.00}$$

---

### Option B: Selecting Cheaper Source S2 ($18.00)
1. RO-1042 parts usable at $A_{S2} = 49$ (12:05 PM).
2. Install runs $t = 49 \to 61$ (13:05 PM, 12 ticks).
3. Clearance transit runs $t = 61 \to 63$ (13:15 PM, 2 ticks).
4. **Bay B4 First Release:** $t = 63$ (13:15 PM).
5. RO-1042 finish tick = 63. Promise = 66.
   $$L_{1042} = \max(0, 63 - 66) = 0\text{ ticks}$$
6. **RO-1051 Execution on Bay B4:**
   - Starts at Bay B4 release: $t = 63$ (13:15 PM).
   - Service runs for 24 ticks: $t = 63 + 24 = 87$ (15:15 PM).
   - RO-1051 finish tick = 87. Promise = 50 (12:10 PM).
   - Lateness $L_{1051} = 87 - 50 = 37$ ticks (185 minutes late).
7. **Objective Values under S2:**
   $$Z_1(S2) = 1.0(0) + 3.0(37) = \mathbf{111.0\text{ weighted ticks}}$$
   $$Z_2(S2) = \mathbf{\$18.00}$$

---

## 5. Lexicographic Decision Outcome

1. **Pass 1 ($Z_1$ Minimization):**
   $$\min(Z_1(S1)=45.0, Z_1(S2)=111.0) \implies Z_1^* = 45.0\text{ ticks}$$
2. **Pass 2 ($Z_2$ Minimization subject to $Z_1 \le 45.0$):**
   - Only Source S1 meets the primary bound.
3. **Approved Plan:**
   - Source: **S1 ($55.00)**.
   - Movement: **`HOLD_ON_BAY`**.
   - Weighted Lateness: **45.0 ticks** (RO-1051 finishes at 13:25 PM).

---

## 6. The "Vehicle-Is-Not-A-Bay" Invariant

```
+----------------------------------------------------------------------------------------------------+
|                                    INVARIANT CE-1: HOIST LOCKING                                   |
+----------------------------------------------------------------------------------------------------+
| A service bay is a spatial asset whose operational availability is strictly bounded by the        |
| physical mobility of the vehicle placed upon it.                                                   |
|                                                                                                    |
| 1. Pausing labour does NOT clear the hoist.                                                       |
| 2. An immobilized vehicle transforms the bay from a productive workstation into an unallocatable   |
|    storage space until parts arrive and reassembly is completed.                                  |
| 3. Available buffer capacity in holding zones (H2) has ZERO utility if the vehicle cannot roll.    |
| 4. The solver MUST accept higher lateness (45.0 ticks) rather than violate physical safety.        |
+----------------------------------------------------------------------------------------------------+
```

### Scientific Verification Rule
Any optimizer that reports $Z_1 < 45.0$ ticks on fixture `S-MATH-03` is mathematically defective and violates safety invariant CE-1.
