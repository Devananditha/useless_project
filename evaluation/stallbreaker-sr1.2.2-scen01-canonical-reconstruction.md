# StallBreaker: SR1.2.2 — SCEN-01 Canonical Reconstruction

> [!CAUTION]
> **[SR1.2.3 CORRECTION — IMPROVEMENT PERCENTAGE SUPERSEDED]**
> This document assumed zero post-repair bay clearance time ($T_{\text{clear}} = 0$), producing an improvement figure of **71.0%**. That physical assumption is unrealistic. The authoritative corrected canonical result uses $T_{\text{clear}} = 2$ ticks (10 min) `[SYNTHETIC FIXTURE ASSUMPTION]`, yielding:
> - A2 $Z_1 = 99.0$, RO-1051 lateness = **165 min**, $B_4$ released $t = 63$ (13:15 PM)
> - P3 $Z_1 = 33.0$, RO-1051 lateness = **55 min**, $B_4$ released $t = 41$ (11:25 AM)
> - Improvement = **(99.0 − 33.0) / 99.0 = 66.7%**
>
> See: [`evaluation/stallbreaker-sr1.2.3-physical-clearance-reconstruction.md`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/evaluation/stallbreaker-sr1.2.3-physical-clearance-reconstruction.md)

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.2-scen01-canonical-reconstruction.md`  
**Phase:** SR1.2.2 — Consistency Correction and Final Gate Audit  
**Standard Compliance:** `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Board:** Operations Research Scientist, Constraint Programming Specialist, Automotive Dealership Operations Specialist, Adversarial Hackathon Evaluator  
**Date:** November 14, 2026  
**Classification:** MATHEMATICALLY DEMONSTRATED [SYNTHETIC FIXTURE — HAND-WORKED EXAMPLE]  

> [!CAUTION]
> This document SUPERSEDES Section 6 of `stallbreaker-sr1.2.1-counterexample-reproduction.md` and Section 3.5 of `stallbreaker-mvp-feasibility.md`. Both contain internally inconsistent lateness calculations that produced the erroneous 37.5% figure. That figure is **WITHDRAWN** from all active claims. The correct result from the declared SCEN-01 inputs is **71.0%** reduction in RO-1051 lateness.

---

## 1. What Was Wrong in SR1.2.1

SR1.2.1 Section 6 ("Mathematical Verification of the 37.5% Lateness Reduction Metric") silently introduced two undeclared deviations from the SCEN-01 inputs declared in Section 3:

| Parameter | Declared in Section 3 | Used in Section 6 |
| :--- | :--- | :--- |
| RO-1051 Customer Promise ($P_2$) | $t = 54$ (12:30 PM) | $t = 61$ (13:05 PM) — **unstated change** |
| P3 RO-1051 finish time | $t = 63$ (13:15 PM) from $39 + 24 = 63$ | $t = 76$ (14:20 PM) — **unexplained** |

Under the declared inputs, the results are:

- **A2:** RO-1051 finishes at $t = 85$ (15:05 PM). Lateness $= (85 - 54) \times 5 = \mathbf{155\ \text{min}}$.  
- **P3 (branch $S_1$):** RO-1051 finishes at $t = 63$ (13:15 PM). Lateness $= (63 - 54) \times 5 = \mathbf{45\ \text{min}}$.  
- **Improvement:** $(155 - 45) / 155 = \mathbf{71.0\%}$.

The 37.5% figure ($120\text{ vs }75$ min) is not reproducible from Section 3 inputs and is hereby withdrawn. The 71.0% result is the authoritative corrected claim for SCEN-01.

---

## 2. Authoritative SCEN-01 Input Table

### 2.1 Time Axis

| Parameter | Value |
| :--- | :--- |
| Time origin | 08:00 AM $= t = 0$ |
| Time step | 5 minutes per tick |
| Shift horizon | 08:00 AM – 17:00 PM $= t \in [0, 108]$ |
| Audit timestamp | $t = 21$ (09:45 AM) |

### 2.2 Vehicle V1 — RO-1042 (Sarah Jenkins, 2022 Ford Explorer)

| Parameter | Value |
| :--- | :--- |
| Current location | Bay $B_4$ (heavy-duty alignment hoist with subframe cradle) |
| Physical state at $t = 21$ | Front subframe detached, suspension unbolted; vehicle not safe to drive |
| `SAFE_TO_DRIVE` | `FALSE` at $t = 21$ |
| Mid-repair relocation safety | Requires 6-tick (30 min) safe-close tie-down labor before rolling mid-repair |
| Parts shortage | AC Compressor Bracket, Part #BB5Z-19D850-A |
| Installation operation | Duration = 12 ticks (60 min). **Requires Bay $B_4$ exclusively** (subframe alignment jig). |
| Customer promise $P_1$ | $t = 66$ (13:30 PM) |
| Customer priority weight $w_1$ | $1.0$ |

**Post-repair vehicle state transition:** When installation completes and the subframe is retorqued, $V_1$ transitions to `SAFE_TO_DRIVE`. It then moves to the **customer staging / pickup lot** — not to $H_2$. The holding zone $H_2$ is for incomplete repairs awaiting parts; a fully repaired vehicle exits to customer delivery staging. This transition frees Bay $B_4$ immediately upon repair completion.

### 2.3 Downstream Job — RO-1051 (Fleet F-150, ADAS Calibration)

| Parameter | Value |
| :--- | :--- |
| Vehicle | $V_2$ (2023 Ford F-150 Commercial Fleet) |
| Operation | High-precision ADAS calibration + suspension alignment |
| Duration | 24 ticks (120 min) |
| **Bay requirement** | **Bay $B_4$ exclusively** (optical alignment rack + calibration targets are $B_4$-only equipment) |
| Ready to enter $B_4$ | $t = 24$ (10:00 AM) |
| Customer promise $P_2$ | **$t = 54$ (12:30 PM)** |
| Customer priority weight $w_2$ | $3.0$ (commercial SLA) |

### 2.4 Source Candidates for RO-1042

| Candidate | Type | Cost $c_s$ | Part arrival time | Usable-ready tick $T_{\text{ready}}(s)$ | ATP / Fitment / Warranty |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_1$ — Expedited Hotshot | Local courier | \$55.00 | 10:15 AM | $t = 27$ | OEM — approved |
| $S_2$ — Standard Transfer | Sister dealership | \$18.00 | 12:05 PM | $t = 49$ | OEM — approved |
| $S_3$ — Aftermarket | Local jobber | \$40.00 | 13:00 PM | $t = 60$ | Non-OEM — **warranty gate rejected** |

$S_3$ is eliminated deterministically. Feasible candidate set: $\{S_1, S_2\}$.

### 2.5 Facility and Staging Constraints

| Resource | Capacity | Occupancy at audit time |
| :--- | :--- | :--- |
| Bay $B_4$ | $C = 1$ (single-capacity, shared by RO-1042 and RO-1051) | Occupied by $V_1$ from $t = 21$ |
| Holding zone $H_2$ | $C = 1$ | Occupied by recall vehicle (RO-0988) from $t = 0$ to $t = 60$ |
| Holding zones $H_1$, $H_3$ | Blocked | EV battery isolation regulation; unavailable |

**Consequence for mid-repair relocation:** Because $H_2$ is saturated and $H_1$/$H_3$ are unavailable, $V_1$ **cannot** be moved out of $B_4$ while its repair is incomplete. The 6-tick safe-close relocation path is physically blocked.

**Consequence for completed repair:** A completed repair does not need holding space. $V_1$ moves to the customer pickup lot directly. Bay $B_4$ is released.

### 2.6 Technician Availability

| Technician | Availability |
| :--- | :--- |
| $K_1$ (Master Tech) | Continuously available from $t = 21$ onward |

---

## 3. A2 Sequential Policy — Full Calculation

### 3.1 Subproblem 1: Sourcing (Information-Bounded, Blind to Downstream Bay)

A2 evaluates sourcing in isolation using only RO-1042's local cost and promise:

$$J_{\text{source}}(s) = c_s + \lambda \cdot \max(0,\ T_{\text{ready}}(s) + d_{\text{install}} - P_1)$$

| Candidate | $c_s$ | $T_{\text{ready}} + d_{\text{install}}$ | Finish time | Against $P_1 = t{=}66$ | $J_{\text{source}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_2$ | \$18.00 | $49 + 12 = 61$ (13:05 PM) | 13:05 PM | 0 min late | **\$18.00** ✓ |
| $S_1$ | \$55.00 | $27 + 12 = 39$ (11:15 AM) | 11:15 AM | 0 min late | \$55.00 |

**A2 decision:** $s^* = S_2$. Subproblem 1 has **zero visibility** into Bay $B_4$'s downstream queue and RO-1051's 12:30 PM promise.

### 3.2 Subproblem 2: Scheduling with $S_2$ Fixed

The CP-SAT scheduler receives $x_{\text{RO-1042}, S_2} = 1$ as a fixed (immutable) parameter.

| Event | Time | Tick |
| :--- | :--- | :--- |
| Part $S_2$ arrives | 12:05 PM | $t = 49$ |
| RO-1042 install **start** (earliest allowed by part availability) | 12:05 PM | $t = 49$ |
| RO-1042 install **end** (duration = 12 ticks) | 13:05 PM | $t = 61$ |
| $V_1$ moves to customer pickup lot; $B_4$ **released** | 13:05 PM | $t = 61$ |
| RO-1051 enters $B_4$ (earliest after $B_4$ release) | 13:05 PM | $t = 61$ |
| RO-1051 **completes** (duration = 24 ticks) | 15:05 PM | $t = 85$ |

**Note on $V_1$ staying in $B_4$:** Between $t = 21$ and $t = 49$, the part has not arrived. $V_1$ is dismantled in $B_4$. $H_2$ is full; no relocation is possible. $V_1$ physically blocks $B_4$ until repair is complete at $t = 61$.

**Degrees of freedom for A2 Subproblem 2:** None. Given $s^* = S_2$:
- Cannot start RO-1042 before $t = 49$ (part not available).
- Cannot move $V_1$ out of $B_4$ before repair completes ($H_2$ full).
- Cannot schedule RO-1051 in $B_4$ before $V_1$ departs (physical occupancy conflict).
- Minimum end for RO-1051 is $61 + 24 = 85$.

**A2 Lateness Calculations:**

| RO | Finish | Promise | Lateness (ticks) | Lateness (min) |
| :--- | :--- | :--- | :--- | :--- |
| RO-1042 | $t = 61$ (13:05 PM) | $P_1 = t{=}66$ (13:30 PM) | $\max(0, 61-66) = 0$ | **0 min** |
| RO-1051 | $t = 85$ (15:05 PM) | $P_2 = t{=}54$ (12:30 PM) | $\max(0, 85-54) = 31$ | **155 min** |

$$Z_1(\text{A2}) = w_1 \cdot 0 + w_2 \cdot 31 = 1.0 \times 0 + 3.0 \times 31 = \mathbf{93.0\ \text{weighted ticks}}$$

---

## 4. P3 Joint Policy — Full Calculation

P3 solves a single CP-SAT program with sourcing variable $x_{r,s}$, bay interval variables $I_v^{B_4}$, and scheduling variables $\text{start}_o$, $\text{end}_o$ jointly.

### 4.1 Branch $s = S_2$ (Evaluated Internally by P3)

Same constraint chain as A2 Subproblem 2: $Z_1 = 93.0$ weighted ticks.

### 4.2 Branch $s = S_1$

| Event | Time | Tick |
| :--- | :--- | :--- |
| Part $S_1$ arrives | 10:15 AM | $t = 27$ |
| RO-1042 install **start** | 10:15 AM | $t = 27$ |
| RO-1042 install **end** (duration = 12 ticks) | 11:15 AM | $t = 39$ |
| $V_1$ transitions: `SAFE_TO_DRIVE = TRUE` | 11:15 AM | $t = 39$ |
| $V_1$ moves to **customer staging lot** (not $H_2$) | 11:15 AM | $t = 39$ |
| $B_4$ **released** | 11:15 AM | $t = 39$ |
| RO-1051 enters $B_4$ (after $B_4$ release and RO-1051 readiness $t = 24$) | 11:15 AM | $t = 39$ |
| RO-1051 **completes** (duration = 24 ticks) | 13:15 PM | $t = 63$ |

**Physical state check:** $V_1$'s installation completes the reassembly. No holding zone is needed; a fully repaired vehicle exits to the customer pickup lot. $H_2$ saturation is irrelevant to a completed repair.

**P3 (Branch $S_1$) Lateness Calculations:**

| RO | Finish | Promise | Lateness (ticks) | Lateness (min) |
| :--- | :--- | :--- | :--- | :--- |
| RO-1042 | $t = 39$ (11:15 AM) | $P_1 = t{=}66$ (13:30 PM) | 0 | **0 min** |
| RO-1051 | $t = 63$ (13:15 PM) | $P_2 = t{=}54$ (12:30 PM) | $\max(0, 63-54) = 9$ | **45 min** |

$$Z_1(S_1) = 1.0 \times 0 + 3.0 \times 9 = \mathbf{27.0\ \text{weighted ticks}}$$

### 4.3 P3 Selection

Under the lexicographic Tier-2 objective (minimize $Z_1$):

| Branch | $Z_1$ (weighted ticks) | Sourcing cost |
| :--- | :--- | :--- |
| $s = S_2$ | 93.0 | \$18.00 |
| $s = S_1$ | **27.0 ← selected** | \$55.00 |

P3 selects $S_1$. The \$37.00 additional freight cost (Tier-4 objective) is correctly subordinate to the 66-weighted-tick lateness saving (Tier-2 objective). This subordination is structurally guaranteed by the sequential multi-pass hierarchy: Tier 2 is optimized before Tier 4 is considered.

---

## 5. Authoritative Improvement Calculation

| Metric | A2 | P3 | Improvement |
| :--- | :--- | :--- | :--- |
| RO-1051 raw lateness | **155 min** | **45 min** | **$(155-45)/155 = 71.0\%$** |
| Weighted $Z_1$ (ticks) | **93.0** | **27.0** | **$(93-27)/93 = 71.0\%$** |
| RO-1042 lateness | 0 min | 0 min | — |
| Sourcing cost | \$18.00 | \$55.00 | +\$37.00 (acceptable trade-off) |

**Classification:** `MATHEMATICALLY DEMONSTRATED [SYNTHETIC FIXTURE SCEN-01, HAND-WORKED EXAMPLE]`

> [!IMPORTANT]
> The 71.0% figure is the **sole authoritative improvement claim** for SCEN-01. The 37.5% figure from SR1.2.1 Section 6 is **withdrawn**. It arose from using an undeclared promise time ($P_2 = t{=}61$ instead of $t{=}54$) and an unexplained P3 schedule ($t{=}76$ finish instead of $t{=}63$). Those values are inconsistent with the declared scenario inputs and are removed from all active documents.

---

## 6. Proof of Genuine Jointness

### 6.1 Why A2 Subproblem 2 Has Zero Recovery Degrees of Freedom

After A2 fixes $s^* = S_2$, Subproblem 2 faces a fully determined constraint chain:

$$x_{\text{RO-1042}, S_2} = 1 \implies \text{start}_{\text{RO-1042}} \ge 49 \implies \text{end}_{\text{RO-1042}} \ge 61 \implies \text{start}_{\text{RO-1051}} \ge 61 \implies \text{end}_{\text{RO-1051}} \ge 85$$

The binding constraints that prevent any Subproblem 2 improvement:

| Constraint | Binding condition | Why A2 cannot escape |
| :--- | :--- | :--- |
| Part availability lower bound | $\text{start}_{\text{RO-1042}} \ge T_{\text{ready}}(S_2) = 49$ | Part physically not present before $t = 49$; cannot be relaxed. |
| Bay $B_4$ specialization | Both RO-1042 and RO-1051 require $B_4$ exclusively | No alternate bay; constraint is a physical property of shop equipment. |
| $V_1$ physical occupancy | $V_1$ blocks $B_4$ while repair is incomplete | Cannot move $V_1$ mid-repair because $H_2$ is saturated; no other staging exists. |
| Non-overlap | $\text{NoOverlap}(I_{V1}^{B_4}, I_{V2}^{B_4})$ | $V_2$ cannot enter $B_4$ while $V_1$ occupies it. |

A2 Subproblem 2 has **no decision variable that can break this chain**. Source selection has already been made. The solver may only choose to start RO-1051 as early as $t = 61$, which it correctly does. The 155-minute lateness is structurally forced by the source choice.

### 6.2 Why P3 Escapes This Chain

P3's joint formulation allows the sourcing variable $x_{r,s}$ to participate in the global objective evaluation before being fixed. The solver discovers that the branch $x_{\text{RO-1042}, S_1} = 1$ yields $\text{end}_{\text{RO-1051}} = 63$ and $Z_1 = 27$, versus $\text{end}_{\text{RO-1051}} = 85$ and $Z_1 = 93$ under $S_2$. Because Tier-2 dominates Tier-4, $S_1$ is selected even at higher freight cost.

No decoupled architecture can replicate this, because Subproblem 1 has no mechanism to evaluate how the source choice propagates through bay occupancy into downstream lateness. That propagation is non-local: it requires visibility across both sourcing and scheduling decision spaces simultaneously.

### 6.3 Formal Jointness Verdict

$$\mathbf{GENUINE\ JOINTNESS\ DEMONSTRATED\ [SYNTHETIC\ FIXTURE\ SCEN-01,\ HAND-WORKED\ EXAMPLE]}$$

The result is derived without any solver execution. It is a hand-traced analytical calculation. It must be presented as such in all documents.

---

## 7. Vehicle Physical State Continuity Check

The following checks confirm that every location transition in the scenario is physically feasible:

| Check | A2 path | P3 path |
| :--- | :--- | :--- |
| $V_1$ in $B_4$ at $t = 21$? | ✓ Yes (stated) | ✓ Yes (stated) |
| Can $V_1$ be moved mid-repair before $t = 60$? | ✗ No ($H_2$ full, no alternative) | ✗ No ($H_2$ full — but irrelevant: P3 completes the repair before needing to move) |
| After repair completes, can $V_1$ exit $B_4$? | ✓ Yes — to customer pickup lot (13:05 PM) | ✓ Yes — to customer pickup lot (11:15 AM) |
| Does $V_1$ need $H_2$ after repair? | ✗ No | ✗ No |
| Is $B_4$ physically clear for RO-1051 entry? | ✓ at $t = 61$ | ✓ at $t = 39$ |

No location transition requires an unavailable resource. The physical vehicle state model is internally consistent.

---

## 8. Correction Log

| Prior Document | Prior Claim | Error | Correction |
| :--- | :--- | :--- | :--- |
| SR1.2.1 Section 6 | 37.5% improvement (120 vs 75 min) | Used $P_2 = t{=}61$ (13:05 PM) instead of declared $P_2 = t{=}54$ (12:30 PM); P3 finish at $t{=}76$ is unexplained | **Withdrawn.** Correct result = 71.0% (155 vs 45 min) using declared inputs |
| SR1.2.1 Section 6 | "P3 schedule: RO-1042 staged; technician begins partial work at $t=27$, bay transition occurs, RO-1051 finishes at 14:20 PM ($t=76$)" | Timing ($t=76$) contradicts the directly calculated $39 + 24 = 63$ | Corrected: P3 RO-1051 completes at $t = 63$ (13:15 PM) |
| SR1.2.1 Section 4.2 Note | "In the unweighted case with $w_2 = 1.0$ and RO-1051 deadline at 13:05 PM, lateness = exactly 120 min" | Introduces a third, undeclared variant promise time | Removed. SCEN-01 has one promise time: $P_2 = t{=}54$ (12:30 PM) |
| `stallbreaker-mvp-feasibility.md` Section 3.5 | "Total Weighted Lateness = 120 min / 75 min (37.5% reduction)" | Same inconsistency as above | Superseded by this document's calculations |

> [!NOTE]
> `stallbreaker-mvp-feasibility.md` Section 3.5 originally compared different source candidates (S2 vs S3). That document was updated during SR1.1 / SR1.2 to reference a combined scenario. The authoritative scenario fixture going forward is this document (SCEN-01 canonical reconstruction). The old 37.5% claim in `stallbreaker-mvp-feasibility.md` Section 3.5 is marked superseded in that document.
