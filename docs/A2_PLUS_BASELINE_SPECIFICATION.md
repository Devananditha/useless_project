# StallBreaker 2.0 — Baseline A2+: Deterministic One-Step Lookahead Specification

## 1. Overview and Purpose

Baseline **A2+** is an independent, pure-Python deterministic heuristic designed to serve as a rigorous, defensible baseline for automotive retail service recovery. It models an attentive service advisor who evaluates candidate part sources against immediate downstream commitments before deciding on expedited procurement.

In the StallBreaker study hierarchy:
1. **P0 (Wait / No Recovery):** Vehicle remains stalled indefinitely on the hoist; no expedited part is sourced.
2. **A2 (Fixed-Source Sequential Baseline):** Sourcing is pre-fixed to standard regional logistics (Source S2) regardless of downstream disruptions; vehicle scheduling is solved sequentially.
3. **A2+ (Deterministic One-Step Lookahead Baseline):** Sourcing is evaluated using a bounded-budget, single-downstream-RO lookahead rule. If an expedited courier strictly reduces total weighted lateness without exceeding a predefined freight surcharge budget ($\Delta_{\max} = \$50.00$), the heuristic upgrades procurement.
4. **P3 (StallBreaker Joint Optimization):** Full mixed-integer constraint programming via Google OR-Tools CP-SAT, jointly optimizing sourcing and spatial relocation across arbitrary multi-job, multi-resource horizons.

A2+ prevents strawman comparisons by providing a non-trivial heuristic competitor that easily outperforms naive fixed-source baselines on single-bay disruptions.

---

## 2. Policy Pipeline and Step-by-Step Specification

The A2+ policy operates deterministically via `solve_a2_plus_policy(snapshot, max_freight_budget_delta=50.0)`. It proceeds through five disciplined stages:

```
[Candidate Sources] ---> Step A: Eligibility Filter (ATP > 0, Fitment, Quote Valid)
                                |
[Vehicle Snapshot]  ---> Step B: Physical Relocation Gating (Rollable, Signoff, H2 Capacity)
                                |
                         Step C: Anchor on Cheapest Landed Cost Source (S_cheap)
                                |
                         Step D: One-Step Lookahead over Alternatives (Z1(alt) < Z1(cheap) & Cost Delta <= $50)
                                |
                         Step E: Candidate Selection (Lowest Z1 -> Lowest Cost -> Usable Tick -> Source ID)
```

### Step A — Source Eligibility
Candidate part sources $S$ are evaluated against three physical inventory criteria:
1. **Available-to-Promise (ATP):** $S.\text{atp} \ge 1$ (units must be physically reservable).
2. **Fitment Verification:** $S.\text{fitment\_verified} == \text{True}$ (VIN and OEM catalogue match).
3. **Quote Validity:** $S.\text{quote\_valid} == \text{True}$ (courier holding window is active).

If no candidate satisfies all three conditions, the heuristic returns an un-fabricated, non-placeholder `INFEASIBLE` decision.

### Step B — Physical Relocation Gating
Spatial vehicle movement (`RELOCATE_TO_H2`) is gated by four strict physical preconditions on primary vehicle RO-1042:
1. `ro1042.is_rollable == True` (vehicle must physically roll on shop floor).
2. `ro1042.current_vehicle_state != VehicleState.PARTIALLY_DISMANTLED` (hoist lock invariant CE-1).
3. `ro1042.technician_signoff_recorded == True` (certified technician safety signoff).
4. `snapshot.h2_available_stalls >= 1` (staging area must have free physical capacity).

If any precondition fails, the movement mode is strictly forced to `HOLD_ON_BAY`. This movement decision is held constant across all candidate evaluations to prevent joint optimization leakage.

### Step C — Cheapest Source Baseline Anchor
Eligible sources are sorted deterministically:
1. Lowest landed procurement/freight cost: $\min \text{cost}(S)$.
2. Earliest usable-ready tick: $\min \text{usable\_time\_ticks}(S)$.
3. Deterministic tie-breaker: $\min \text{source\_id}(S)$.

The first source in this ordering is designated as the cheapest baseline anchor $S_{\text{cheap}}$. The heuristic computes its complete chronological schedule and records baseline weighted lateness $Z_1(S_{\text{cheap}})$.

### Step D — One-Step Downstream Lookahead
The heuristic simulates the resulting shop schedule for each alternative source $S_{\text{alt}} \in S_{\text{eligible}} \setminus \{S_{\text{cheap}}\}$ under the same selected movement mode.

An alternative qualifies for potential upgrade if and only if **both** necessary conditions hold:
1. **Strict Lateness Improvement:**
   $$Z_1(S_{\text{alt}}) < Z_1(S_{\text{cheap}})$$
   *(Equal weighted lateness offers zero operational benefit and is strictly disqualified).*
2. **Freight Budget Bound:**
   $$\text{cost}(S_{\text{alt}}) - \text{cost}(S_{\text{cheap}}) \le \Delta_{\max}$$
   where default $\Delta_{\max} = \$50.00$.

### Step E — Candidate Selection and Deterministic Tie-Breaking
If one or more alternatives qualify:
1. Select the candidate with the lowest weighted lateness $\min Z_1(S_{\text{alt}})$.
2. Break lateness ties by lowest landed cost $\min \text{cost}(S_{\text{alt}})$.
3. Break cost ties by earliest usable-ready time $\min \text{usable\_time\_ticks}(S_{\text{alt}})$.
4. Break remaining ties by lexicographical source ID $\min \text{source\_id}(S_{\text{alt}})$.

If no alternative qualifies, $S_{\text{cheap}}$ is strictly retained.

---

## 3. Deterministic Schedule Simulation Equations

All operations are modeled in discrete 5-minute ticks from origin 08:00 ($t=0$).

### 3.1 Mode 1: HOLD_ON_BAY
Primary vehicle RO-1042 remains immobilized on specialized Bay B4:
1. Installation start:
   $$t_{\text{inst\_start}} = \max(t_{\text{current}}, S.\text{usable\_time\_ticks})$$
2. Installation end:
   $$t_{\text{inst\_end}} = t_{\text{inst\_start}} + D_{1042}$$
3. Bay clearance end and primary vehicle finish:
   $$t_{\text{clear\_end}} = t_{\text{inst\_end}} + D_{\text{clearance}}$$
   $$t_{\text{B4\_release}} = t_{\text{clear\_end}}, \quad t_{\text{finish}, 1042} = t_{\text{clear\_end}}$$
4. Technician K2 availability resolution:
   $$\text{tech\_avail} = \begin{cases} 
   \text{technician\_k2\_available\_tick} & \text{if not None} \\ 
   \text{ro1051.technician\_available\_tick} & \text{otherwise} 
   \end{cases}$$
5. Downstream fleet job RO-1051 execution:
   $$t_{\text{start}, 1051} = \begin{cases} 
   \max(t_{\text{B4\_release}}, \text{tech\_avail}) & \text{if tech\_avail is not None} \\ 
   t_{\text{B4\_release}} & \text{otherwise} 
   \end{cases}$$
   $$t_{\text{finish}, 1051} = t_{\text{start}, 1051} + D_{1051}$$

### 3.2 Mode 2: RELOCATE_TO_H2
Primary vehicle RO-1042 relocates to Holding Location H2, freeing Bay B4:
1. Outbound transit to H2:
   $$t_{\text{H2\_arr}} = t_{\text{current}} + D_{\text{reloc}}$$
   $$t_{\text{B4\_release}} = t_{\text{H2\_arr}}$$
2. Downstream fleet job RO-1051 enters Bay B4:
   $$t_{\text{start}, 1051} = \begin{cases} 
   \max(t_{\text{B4\_release}}, \text{tech\_avail}) & \text{if tech\_avail is not None} \\ 
   t_{\text{B4\_release}} & \text{otherwise} 
   \end{cases}$$
   $$t_{\text{finish}, 1051} = t_{\text{start}, 1051} + D_{1051}$$
3. Post-service clearance of Bay B4:
   $$t_{\text{B4\_free\_after\_1051}} = t_{\text{finish}, 1051} + D_{\text{clearance}}$$
4. RO-1042 return transit from H2 to B4:
   $$t_{\text{return\_start}} = \max(t_{\text{B4\_free\_after\_1051}}, S.\text{usable\_time\_ticks})$$
   $$t_{\text{return\_arr}} = t_{\text{return\_start}} + D_{\text{reloc}}$$
5. Reassembly and clearance on Bay B4:
   $$t_{\text{inst\_end}} = t_{\text{return\_arr}} + D_{1042}$$
   $$t_{\text{finish}, 1042} = t_{\text{inst\_end}} + D_{\text{clearance}}$$

---

## 4. Objective Calculations

Lateness against customer promise targets ($P_1, P_2$) is computed without intermediate rounding:
$$L_{1042} = \max(0, t_{\text{finish}, 1042} - P_{1042})$$
$$L_{1051} = \max(0, t_{\text{finish}, 1051} - P_{1051})$$

Weighted lateness objective $Z_1$:
$$Z_1 = w_{1042} \cdot L_{1042} + w_{1051} \cdot L_{1051}$$
where $w_{1042} = 1.0$ (retail priority) and $w_{1051} = 3.0$ (commercial fleet SLA priority).

Downstream delay savings or lateness in minutes:
$$\text{delay\_min} = L_{1051} \times 5$$

---

## 5. Acceptance Scenario Benchmark Results

| Scenario | Mode | Cheapest Anchor | Alternative Evaluated | Lookahead Decision | Final Source | Weighted Lateness $Z_1$ | Freight Cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S-MATH-01** (Canonical Hoist Lock) | `HOLD_ON_BAY` | S2 ($18.00, $Z_1 = 99.0$) | S1 ($55.00, $Z_1 = 33.0$, $\Delta = \$37$) | **UPGRADE** | **S1** | **33.0 ticks** | **$55.00** |
| **S-MATH-02** (Null-Benefit Restraint) | `HOLD_ON_BAY` | S2 ($18.00, $Z_1 = 0.0$) | S1 ($55.00, $Z_1 = 0.0$, $\Delta = \$37$) | **RETAIN** | **S2** | **0.0 ticks** | **$18.00** |
| **S-MATH-03** (Safety Invariant Gate) | `HOLD_ON_BAY` | S2 ($18.00, $Z_1 = 111.0$) | S1 ($55.00, $Z_1 = 45.0$, $\Delta = \$37$) | **UPGRADE** | **S1** | **45.0 ticks** | **$55.00** |

### Key Observations
1. **S-MATH-01 (Lookahead Upgrade):** A2+ successfully matches P3 on this single-bay hoist lock instance by paying \$37.00 to reduce fleet delay by 110 minutes (66.7% weighted lateness reduction).
2. **S-MATH-02 (Null-Benefit Restraint):** Because Tech K2 is unavailable until tick 60, both S1 and S2 yield zero weighted lateness. A2+ avoids wasting \$37.00 on an unnecessary courier, saving procurement costs.
3. **S-MATH-03 (Physical Safety Gate):** Even though Holding Area H2 has 2 open stalls, RO-1042 is immobilized (`is_rollable = False`). A2+ strictly enforces `HOLD_ON_BAY` and upgrades to S1.

---

## 6. Structural Limitations of One-Step Lookahead (Why A2+ is a Heuristic)

While A2+ is an effective single-step heuristic, it has fundamental algorithmic limitations that distinguish it from the globally optimal CP-SAT formulation (Policy P3):

1. **Horizon Myopia (Single Downstream Job Horizon):**
   A2+ only considers the immediate downstream vehicle ($J_{k+1}$) on the target bay. If subsequent jobs ($J_{k+2}, J_{k+3}$) have conflicting promise windows or technician requirements, A2+ cannot anticipate upstream ripple effects.
2. **Decoupled Movement and Sourcing Decisions:**
   A2+ decides vehicle movement (`HOLD_ON_BAY` vs `RELOCATE_TO_H2`) prior to evaluating candidate part sources. In complex multi-bay facilities, optimal recovery may require joint decisions where movement selection depends directly on which part source is selected.
3. **No Dynamic Stall Re-Allocation:**
   If holding capacity becomes contested across multiple bays, A2+ cannot solve the resulting multi-commodity assignment problem.
4. **Fixed Surcharge Heuristic Threshold:**
   The \$50.00 freight budget delta is a fixed heuristic cutoff. If a \$52.00 courier would prevent a \$2,500 fleet SLA contractual penalty, A2+ rejects the option due to rigid budget truncation. CP-SAT solves lexicographic multi-objective optimization without arbitrary budget ceilings.

---

## 7. Verifier and Implementation Boundaries

- Primary implementation lives in `backend/v2/baseline_a2_plus.py`.
- No dependencies on OR-Tools or CP-SAT.
- Status is clearly labeled as `HEURISTIC` rather than `OPTIMAL`.
- **Verifier Identity Preservation:** Verified via a dedicated verifier projection `A2PlusVerifierView` (and `a2_plus_to_verifier_view` / `a2_plus_to_proposal_adapter`). It preserves `policy_id = "A2_PLUS"` without altering the production `PolicyId` enum or the `Proposal` model. The resulting SHA-256 decision digest cryptographically reflects the `"A2_PLUS"` policy identity.
- **Fail-Closed on Infeasibility:** Infeasible `A2PlusDecision` objects preserve unpopulated milestones (`None`). `a2_plus_to_verifier_view()` strictly raises `ValueError` if invoked on an infeasible decision, rejecting the fabrication of synthetic milestone or lateness values (e.g. 0 or 999).
- Isolated from the production advisor approval/commit pipeline (`backend/revalidation.py`).
- Synthetic and benchmark results reflect modeled mathematical fixtures and do not claim real dealership field performance.
