# StallBreaker: SR1.2.5.1 — Mathematical Invariance & Event Ordering Correction

**Workspace:** `TEKION-HACKATHON-2026`  
**Document:** `evaluation/stallbreaker-sr1.2.5.1-mathematical-correction.md`  
**Phase:** SR1.2.5.1 — Bounded Final Research Correction  
**Date:** November 14, 2026  
**Standard Compliance:** Fully compliant with `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Board:** Operations Research Scientist, Constraint Programming Specialist, Automotive Fixed Operations Domain Reviewer, Safety-Critical State-Machine Reviewer, Mathematical Verification Auditor, Research Integrity Reviewer  
**Classification:** ADVERSARIAL MATHEMATICAL PROOF & EVENT-SEMANTICS CORRECTION  

---

## 1. Executive Summary & Audit Mandate

An independent mathematical audit of Phase SR1.2.5 identified one bounded mathematical overclaim, one fleet contractual overgeneralization, and one temporal event-ordering ambiguity:

1. **Total Weighted-Objective Invariance Overclaim (Issue A):** Section 6.4 of `stallbreaker-sr1.2.5-final-reconciliation.md` claimed that the total weighted objective difference $\Delta Z_1 = Z_1(\text{A2}) - Z_1(\text{P3})$ is identically $66.0$ weighted ticks for *all* clearance durations $T_{\text{clear}} \ge 0$. This claim overlooked the nonnegative lateness operator on the upstream job (RO-1042): for $T_{\text{clear}} > 5$ ticks (25 minutes), RO-1042 becomes late under A2 ($C_{\text{A2}}^{1042} = 61 + T_{\text{clear}} > 66$), whereas under P3 it remains on time until $T_{\text{clear}} > 27$ ticks ($C_{\text{P3}}^{1042} = 39 + T_{\text{clear}} \le 66$). Consequently, $\Delta Z_1(T)$ is **piecewise linear**, not universally constant. The raw downstream lateness difference on RO-1051 *is* universally 110 minutes, but the total weighted objective difference $\Delta Z_1(T)$ equals 66 ticks only for $0 \le T_{\text{clear}} \le 5$.
2. **Fleet Contractual SLA Wording Overclaim (Issue B):** Section 6.2 presented commercial fleet SLA terms as universally mandating service completion on the hoist, implying an external empirical finding. This assertion lacked traceable workspace contractual evidence and must be qualified as an operational modeling convention conforming to Equation (C25).
3. **Cross-Entity Event Precedence Ambiguity (Issue C):** Section 5 represented vehicle departure, bay inspection, bay availability, and downstream vehicle entry at the exact same discrete tick ($t = 41$ in P3; $t = 63$ in A2) without explicitly formalizing their ordered zero-duration logical sequence.

This deliverable provides complete, independent mathematical proofs, boundary checks, contractual qualifications, and logical event precedence specifications resolving all three issues.

---

## 2. Issue A: Rigorous Mathematical Derivation of Invariance

### 2.1 Preserved S-MATH-01 Parameters
- Time discretization: $1\text{ tick} = 5\text{ minutes}$. Shift origin $t = 0$ (08:00 AM).
- **RO-1042 (Sarah Jenkins):** Customer-ready promise $P_1 = 66$ (13:30 PM), Priority weight $w_1 = 1.0$.
  - Installation duration: $d_{\text{install}} = 12\text{ ticks}$.
- **RO-1051 (Commercial Fleet):** Service-completion promise $P_2 = 54$ (12:30 PM), Priority weight $w_2 = 3.0$.
  - Operation duration: $d_2 = 24\text{ ticks}$. Ready at $t = 24$.
- **Sourcing candidates:**
  - $S_1$ (Hotshot Courier): Usable at $T_{\text{ready}}(S_1) = 27$ (10:15 AM), Cost \$55.00.
  - $S_2$ (Sister Store Transfer): Usable at $T_{\text{ready}}(S_2) = 49$ (12:05 PM), Cost \$18.00.
- **Clearance Parameter:** $T = T_{\text{clear}} \ge 0$ (in ticks). Actual canonical fixture: $T = 2\text{ ticks}$ (10 minutes).
- **Policy assignments:** A2 fixes $s^* = S_2$; P3 selects $s^* = S_1$. Both face identical equipment-specific Bay $B_4$ hoist requirements and saturated holding slot $H_2$.

---

### 2.2 Proposition 1: Downstream RO-1051 Lateness Difference Invariance

#### Derivation:
Bay $B_4$ release times for any $T \ge 0$:
$$t_{\text{free}}(B_4, \text{A2}) = T_{\text{ready}}(S_2) + d_{\text{install}} + T = 49 + 12 + T = 61 + T$$
$$t_{\text{free}}(B_4, \text{P3}) = T_{\text{ready}}(S_1) + d_{\text{install}} + T = 27 + 12 + T = 39 + T$$

Since $t_{\text{free}} \ge 24$ for all $T \ge 0$, downstream RO-1051 enters Bay $B_4$ immediately upon availability:
$$\text{start}_2(\text{A2}) = 61 + T, \quad \text{start}_2(\text{P3}) = 39 + T$$

Completion times for RO-1051 under Milestone 1 (Service Operation Completion):
$$C_{\text{A2}}^{1051}(T) = 61 + T + 24 = 85 + T$$
$$C_{\text{P3}}^{1051}(T) = 39 + T + 24 = 63 + T$$

Nonnegative lateness against $P_2 = 54$:
$$L_{\text{A2}}^{1051}(T) = \max(0, C_{\text{A2}}^{1051} - 54) = \max(0, 85 + T - 54) = 31 + T \quad (\text{since } 31 + T > 0\ \forall T \ge 0)$$
$$L_{\text{P3}}^{1051}(T) = \max(0, C_{\text{P3}}^{1051} - 54) = \max(0, 63 + T - 54) = 9 + T \quad (\text{since } 9 + T > 0\ \forall T \ge 0)$$

#### Difference:
$$\Delta L^{1051}(T) = L_{\text{A2}}^{1051}(T) - L_{\text{P3}}^{1051}(T) = (31 + T) - (9 + T) \equiv \mathbf{22\text{ ticks}} \equiv \mathbf{110\text{ minutes}} \quad \forall T \ge 0$$

$$\boxed{\mathbf{PROPOSITION\ 1\ VERIFIED:\ }\Delta L^{1051}(T) \equiv 110\text{ minutes for all } T \ge 0}$$

*Proposition 1 holds strictly for all nonnegative clearance durations under the declared common-clearance, fixed-source, and immediate-downstream-entry assumptions.*

---

### 2.3 Proposition 2: Piecewise Total Weighted Objective Difference

#### Derivation:
RO-1042 customer-ready staging completion times:
$$C_{\text{A2}}^{1042}(T) = T_{\text{ready}}(S_2) + d_{\text{install}} + T = 49 + 12 + T = 61 + T$$
$$C_{\text{P3}}^{1042}(T) = T_{\text{ready}}(S_1) + d_{\text{install}} + T = 27 + 12 + T = 39 + T$$

Nonnegative lateness against $P_1 = 66$:
$$L_{\text{A2}}^{1042}(T) = \max(0, 61 + T - 66) = \max(0, T - 5)$$
$$L_{\text{P3}}^{1042}(T) = \max(0, 39 + T - 66) = \max(0, T - 27)$$

Total weighted customer lateness objective $Z_1 = w_1 \cdot L^{1042} + w_2 \cdot L^{1051}$ with $w_1 = 1.0, w_2 = 3.0$:
$$Z_1(\text{A2}, T) = 1.0 \cdot \max(0, T - 5) + 3.0 \cdot (31 + T) = 93 + 3T + \max(0, T - 5)$$
$$Z_1(\text{P3}, T) = 1.0 \cdot \max(0, T - 27) + 3.0 \cdot (9 + T) = 27 + 3T + \max(0, T - 27)$$

Subtracting $Z_1(\text{P3}, T)$ from $Z_1(\text{A2}, T)$:
$$\Delta Z_1(T) = [93 + 3T + \max(0, T - 5)] - [27 + 3T + \max(0, T - 27)]$$
$$\boxed{\Delta Z_1(T) = 66 + \max(0, T - 5) - \max(0, T - 27)}$$

#### Piecewise Form:
Evaluating across the critical thresholds $T = 5$ (25 minutes) and $T = 27$ (135 minutes):

$$\Delta Z_1(T) = \begin{cases} 
66, & 0 \le T \le 5 \\ 
61 + T, & 5 < T \le 27 \\ 
88, & T > 27 
\end{cases}$$

#### Boundary Checks:
- **Left boundary $T = 0$:** $\Delta Z_1(0) = 66 + 0 - 0 = 66$.
- **Boundary $T = 5$:**
  - Left limit: $\lim_{T \to 5^-} \Delta Z_1(T) = 66$.
  - Right limit: $\lim_{T \to 5^+} (61 + T) = 61 + 5 = 66$. Continuous.
- **Interior point $T = 10$:** $\Delta Z_1(10) = 61 + 10 = 71$.
  *(Here, RO-1042 is 5 ticks late under A2 and 0 ticks late under P3, increasing the gap by $+5$ ticks).*
- **Boundary $T = 27$:**
  - Left limit: $\lim_{T \to 27^-} (61 + T) = 61 + 27 = 88$.
  - Right limit: $\lim_{T \to 27^+} 88 = 88$. Continuous.
- **Asymptotic regime $T > 27$:** Both RO-1042 and RO-1051 are late under both policies. The difference is $(T - 5) - (T - 27) + 66 = 22 + 66 = 88$ ticks (440 weighted minutes). Constant.

$$\boxed{\mathbf{PROPOSITION\ 2\ VERIFIED:\ }\Delta Z_1(T) \text{ is piecewise linear; equals } 66 \text{ ticks only for } 0 \le T \le 5}$$

---

### 2.4 Actual Canonical Fixture Verification ($T = 2$ Ticks)

At the actual modeled canonical fixture ($T = 2\text{ ticks} = 10\text{ minutes}$):
- Since $0 \le 2 \le 5$, we are strictly in Regime 1 ($0 \le T \le 5$):
  - $L_{\text{A2}}^{1042} = \max(0, 2 - 5) = \mathbf{0\text{ ticks}}$ (0 minutes).
  - $L_{\text{P3}}^{1042} = \max(0, 2 - 27) = \mathbf{0\text{ ticks}}$ (0 minutes).
  - $L_{\text{A2}}^{1051} = 31 + 2 = \mathbf{33\text{ ticks}}$ (165 minutes).
  - $L_{\text{P3}}^{1051} = 9 + 2 = \mathbf{11\text{ ticks}}$ (55 minutes).
- Weighted objectives:
  - $Z_1(\text{A2}) = 1.0(0) + 3.0(33) = \mathbf{99.0\text{ weighted ticks}}$.
  - $Z_1(\text{P3}) = 1.0(0) + 3.0(11) = \mathbf{33.0\text{ weighted ticks}}$.
  - $\Delta Z_1 = 99.0 - 33.0 = \mathbf{66.0\text{ weighted ticks}}$.
- Relative percentage improvement:
  $$\text{Relative Improvement} = \frac{99.0 - 33.0}{99.0} = \frac{66.0}{99.0} = \mathbf{66.7\%}$$

#### Verification of Secondary Staging Sensitivity Variant ($T = 2$ on both jobs):
- If RO-1051 also undergoes a 2-tick clearance transit to outbound fleet staging:
  - $C_{\text{A2}}^{1051} = 85 + 2 + 2 = 89 \implies L_{\text{A2}}^{1051} = 89 - 54 = 35\text{ ticks}$ (175 minutes).
  - $C_{\text{P3}}^{1051} = 63 + 2 + 2 = 67 \implies L_{\text{P3}}^{1051} = 67 - 54 = 13\text{ ticks}$ (65 minutes).
  - $Z_1(\text{A2}) = 3.0 \times 35 = \mathbf{105.0\text{ weighted ticks}}$.
  - $Z_1(\text{P3}) = 3.0 \times 13 = \mathbf{39.0\text{ weighted ticks}}$.
  - Relative improvement: $(105.0 - 39.0) / 105.0 = 66.0 / 105.0 = \mathbf{62.9\%}$.
  - Lateness difference: $(175 - 65) = \mathbf{110\text{ minutes}}$ (strictly invariant).

#### Finding on Headline Metrics:
> **The primary headline metric (66.7%) and secondary sensitivity metric (62.9%) for the actual fixture $T = 2$ are 100% mathematically correct and remain completely unchanged.** Only the theoretical generalization for $T > 5$ is corrected.

---

## 3. Issue B: Qualified Fleet SLA Interpretation

### 3.1 The Contractual Evidence Boundary
In SR1.2.5 Section 6.2, commercial fleet SLA obligations were described as universally written for bay completion of ADAS sensor calibration. In accordance with `.cursor/rules/research-standards.mdc`, assertions regarding real-world commercial contracts must not be presented as empirical facts unless traceable to actual customer agreements in the workspace.

### 3.2 Formal Qualified Replacement Wording
The workspace formally adopts the following qualified definition across all documents:

> **"For scenario `S-MATH-01`, service-operation completion on the hoist is selected as the primary modeled promise milestone for RO-1051, consistent with the mathematical objective function in Equation (C25). This operational modeling convention reflects the shop milestone where specialized alignment equipment is released and technician diagnostic sign-off is logged. Actual fleet-contract delivery milestones in commercial dealership operations vary (some agreements specify bay completion, while others specify outbound staging inspection) and must be calibrated against specific customer SLA agreements during field deployment."**

### 3.3 Epistemological Separation
- **Mathematical Objective Formulation (C25):** $\text{late}_r \ge \text{end}_{\text{last\_op}(r)} - P_{\text{orig}, r}$. (Design specification).
- **Milestone 1 Benchmark Selection:** Operational modeling assumption chosen for S-MATH-01. (Synthetic convention).
- **Real-World Fleet SLA Terms:** Unverified empirical domain question. (Open calibration item for PR3 pilot).

---

## 4. Issue C: Ordered Cross-Entity Logical Event Semantics

### 4.1 Resolving Discrete-Tick Boundary Collisions
In discrete-time scheduling with tick size $\Delta t = 5\text{ minutes}$, multiple state transitions occur at tick boundary $t = 41$ (P3) and $t = 63$ (A2). Representing these as physically simultaneous states creates apparent paradoxes (e.g., vehicle in bay while bay is declared available).

To eliminate ambiguity, StallBreaker formalizes transitions at discrete tick boundaries as an **ordered sequence of zero-duration logical events** with strict causal precedence:

```
+===================================================================================================================================+
|                                  ORDERED LOGICAL EVENT SEQUENCE AT TICK BOUNDARY t = 41 (P3) / t = 63 (A2)                         |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
|Seq | Event Identifier      | Vehicle Entity State (V1)   | Bay B4 Resource State (B4)    | Logical Precondition / Guard Invariant |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
| 1  | `e_transit_end`       | `IN_CUSTOMER_PICKUP_STAGING`| `CLEARANCE_PENDING`           | V1 completely crosses bay boundary     |
|    |                       |                             |                               | and enters customer delivery stall.    |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
| 2  | `e_bay_clear_confirm` | `IN_CUSTOMER_PICKUP_STAGING`| `CLEARANCE_PENDING`           | Tech inspects hoist floor, stows arms, |
|    |                       |                             |                               | verifies zero tools/fluid on floor.    |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
| 3  | `e_bay_available`     | `IN_CUSTOMER_PICKUP_STAGING`| `AVAILABLE_FOR_ALLOCATION`    | DMS / scheduler unlocks Bay B4 record; |
|    |                       |                             |                               | bay capacity transitions 0 -> 1.       |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
| 4  | `e_v2_bay_entry`      | `IN_CUSTOMER_PICKUP_STAGING`| `OCCUPIED` (by Vehicle V2)    | Downstream RO-1051 vehicle dispatched; |
|    |                       |                             |                               | crosses threshold into Bay B4.         |
+----+-----------------------+-----------------------------+-------------------------------+----------------------------------------+
```

### 4.2 Enforcing Invariants
- **Invariant CE-1 (Causal Precedence):** $e_{\text{transit\_end}} \prec e_{\text{bay\_clear\_confirm}} \prec e_{\text{bay\_available}} \prec e_{\text{v2\_bay\_entry}}$.
- **Invariant CE-2 (Zero Double-Booking):** At no logical point is Bay $B_4$ simultaneously occupied by $V_1$ and $V_2$. $V_1$ is confirmed in `IN_CUSTOMER_PICKUP_STAGING` at Seq 1; $V_2$ enters at Seq 4.
- **Invariant CE-3 (Strict Decoupling):** $V_1$ reaches customer pickup staging independently of when downstream vehicle $V_2$ enters the bay.

---

## 5. Summary of Affected Files & Corrections Applied

```
+===================================================================================================================================+
|                                              CROSS-DOCUMENT CORRECTION TRACKING MATRIX                                             |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| #  | Document Modified                            | Specific Section Updated          | Exact Correction Applied                  |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| 01 | `stallbreaker-sr1.2.5-final-reconciliation.md`| Section 6.4 (Theorem & Proof)     | Replaced universal Delta Z1 = 66 claim    |
|    |                                              |                                   | with Proposition 1 and Proposition 2.     |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| 02 | `stallbreaker-sr1.2.5-final-reconciliation.md`| Section 6.2 (Operational Meaning) | Replaced universal fleet SLA claim with   |
|    |                                              |                                   | qualified modeling convention wording.    |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| 03 | `stallbreaker-sr1.2.5-final-reconciliation.md`| Section 4.4 & 5 (Timeline)        | Formalized ordered zero-duration logical  |
|    |                                              |                                   | event sequence at tick boundaries.        |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| 04 | `stallbreaker-sr1.2.5-final-gate-report.md`  | Section 1 & Section 2             | Reconciled theorem summary to reflect     |
|    |                                              |                                   | piecewise form Delta Z1(T).               |
+----+----------------------------------------------+-----------------------------------+-------------------------------------------+
| 05 | `stallbreaker-source-of-truth-index.md`      | Domains 36-37 & Reconcil. Item 16 | Added SR1.2.5.1 ownership domains and     |
|    |                                              |                                   | reconciliation log entry.                 |
+===================================================================================================================================+
```

---

$$\mathbf{PHASE\ SR1.2.5.1\ MATHEMATICAL\ CORRECTION:\ VERIFIED\ AND\ COMPLETE}$$
