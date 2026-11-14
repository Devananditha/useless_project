# StallBreaker: SR1.2.3 — Physical Clearance Reconstruction of Canonical Scenario SCEN-01

> [!NOTE]
> **[SR1.2.4 REFINEMENT NOTICE]:**  
> While the numerical calculations ($T_{\text{clear}} = 2$ ticks, 66.7% improvement, 110-minute lateness invariance) remain authoritative, the physical safety-state ordering during clearance and the customer-promise completion milestones have been formally finalized in [`evaluation/stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/evaluation/stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md). Readers should refer to SR1.2.4 for the definitive 6-state safety sequence and clarified Equation (C25-Clarified).

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.3-physical-clearance-reconstruction.md`  
**Phase:** SR1.2.3 — Physical Clearance and Claim-Scope Closure  
**Supersedes:** SR1.2.2 canonical SCEN-01 timeline (specifically the zero-clearance B4-release assumption)  
**Standard Compliance:** `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Board:** Operations Research Scientist, Constraint Programming Specialist, Automotive Dealership Operations Specialist  
**Date:** November 14, 2026  
**Classification:** MATHEMATICALLY DEMONSTRATED [SYNTHETIC FIXTURE SCEN-01, HAND-WORKED EXAMPLE]  

---

## 1. What Was Omitted in SR1.2.2

The SR1.2.2 canonical reconstruction assumed that Bay $B_4$ is released **at the instant** installation completes — zero clearance time. Specifically:

- A2: installation ends $t = 61$ → $B_4$ released $t = 61$ → RO-1051 starts $t = 61$.
- P3: installation ends $t = 39$ → $B_4$ released $t = 39$ → RO-1051 starts $t = 39$.

This models the following physical sequence as instantaneous:

1. Final torque verification and inspection sign-off.
2. Vehicle lowered from hoist / disconnected from alignment jig.
3. Vehicle driven or rolled from Bay $B_4$ to customer pickup staging.
4. Bay $B_4$ confirmed physically clear (no vehicle, no tools left in lane).
5. Next vehicle ($V_2$, RO-1051) permitted to enter.

No real dealership bay transitions this rapidly. The omission inflated both the absolute lateness values and, through the formula $22 / (31 + T_{\text{clear}})$, the improvement percentage. This document introduces an explicit clearance interval $T_{\text{clear}}$, recalculates both policies, and reports the corrected result.

---

## 2. Clearance Model Definition

### 2.1 Parameter $T_{\text{clear}}$ — Post-Repair Bay Clearance Duration

| Parameter | Symbol | Definition |
| :--- | :--- | :--- |
| Post-repair clearance duration | $T_{\text{clear}}$ | The number of time ticks required between installation completion and confirmed Bay $B_4$ availability. Encompasses verification, lowering from hoist, vehicle movement, and lane confirmation. |

**What $T_{\text{clear}}$ covers:**
- Final torque check and fluid top-up (typically 2–5 min).
- Lowering vehicle from hoist, reconnecting suspension if partially lifted (1–3 min).
- Driving or steering vehicle from hoist position to exit lane (1–3 min).
- Advisor confirming vehicle is in pickup area (1–2 min).
- Technician clearing tools and confirming lane clear (1–2 min).

**Evidence status:** `SYNTHETIC FIXTURE ASSUMPTION`. No measured dealership data for $T_{\text{clear}}$ exists in this workspace. The value used in SCEN-01 is an illustrative synthetic parameter chosen to represent a reasonable post-repair bay turnover. Actual dealership clearance times require direct operational measurement; estimates in literature vary from 5 to 20 minutes depending on lift type, vehicle size, and service workflow.

**Canonical SCEN-01 value:** $T_{\text{clear}} = 2$ ticks $= 10$ minutes `[SYNTHETIC ASSUMPTION]`.

**Rule:** $T_{\text{clear}}$ applies identically to both A2 and P3 policies. There is no operational justification for different clearance durations based on which source was selected — the same vehicle, the same bay, and the same post-repair steps apply in both cases.

### 2.2 Customer Pickup Staging Lot — Assumptions

The customer pickup lot is **distinct** from Holding Zone $H_2$.

| Property | $H_2$ (incomplete-repair holding) | Customer Pickup Lot |
| :--- | :--- | :--- |
| **Purpose** | Temporarily stage a vehicle mid-repair while awaiting parts or bay space. Vehicle may be partially disassembled. | Stage a **fully repaired, driveable** vehicle for customer collection. Vehicle is road-ready. |
| **Occupancy at $t = 21$** | Occupied by RO-0988 until $t = 60$ (13:00 PM). | Available — declared as a synthetic fixture assumption. |
| **Is it unavailable?** | Yes — saturated until $t = 60$. This is a binding constraint in SCEN-01. | No. The pickup lot is assumed to have at least one open space at all relevant times in this fixture. |
| **Does V1 need it?** | Only if relocation is needed mid-repair. Under P3-S1, V1's repair completes fully; no mid-repair staging is needed. | Yes — $V_1$ moves here after repair completion and clearance. |

**Explicit declaration:** For SCEN-01, the customer pickup staging lot is assumed to have $\ge 1$ available space at both $t = 41$ (P3 clearance completion) and $t = 63$ (A2 clearance completion). This is a synthetic fixture assumption. In a full model, the pickup lot would be a resource with explicit capacity and occupancy tracking.

---

## 3. Authoritative SCEN-01 Input Table (Unchanged from SR1.2.2 Except Clearance)

| Parameter | Value |
| :--- | :--- |
| Time origin | 08:00 AM $= t = 0$ |
| Time step | 5 min per tick |
| Shift horizon | $t \in [0, 108]$ |
| Audit timestamp | $t = 21$ (09:45 AM) |
| **Vehicle $V_1$ (RO-1042)** | In Bay $B_4$, subframe detached, not safe-to-drive |
| RO-1042 customer promise $P_1$ | $t = 66$ (13:30 PM), weight $w_1 = 1.0$ |
| Installation duration | 12 ticks (60 min), Bay $B_4$ required exclusively |
| **Post-repair clearance $T_{\text{clear}}$** | **2 ticks (10 min)** `[SYNTHETIC ASSUMPTION]` |
| **Vehicle $V_2$ (RO-1051)** | ADAS calibration + alignment, duration 24 ticks (120 min) |
| RO-1051 ready to enter $B_4$ | $t = 24$ (10:00 AM) |
| RO-1051 customer promise $P_2$ | $t = 54$ (12:30 PM), weight $w_2 = 3.0$ |
| Bay $B_4$ | Capacity 1; required exclusively by both RO-1042 and RO-1051 |
| Holding zone $H_2$ | Occupied by RO-0988 from $t = 0$ to $t = 60$; relevant only for mid-repair staging |
| Holding zones $H_1$, $H_3$ | Blocked (EV regulations) |
| Customer pickup lot | At least 1 space available from $t = 39$ onward `[SYNTHETIC ASSUMPTION]` |
| Technician $K_1$ | Available from $t = 21$ continuously |
| Source $S_1$ (Expedited Hotshot) | ETA $t = 27$ (10:15 AM), cost \$55.00, OEM approved |
| Source $S_2$ (Standard Transfer) | ETA $t = 49$ (12:05 PM), cost \$18.00, OEM approved |
| Source $S_3$ (Aftermarket) | ETA $t = 60$, non-OEM → rejected by warranty gate |

---

## 4. Explicit Vehicle State Transition Sequence

The following complete event sequence replaces the implicit zero-clearance assumption:

```
EVENT SEQUENCE — BOTH POLICIES
=============================================================
[ INSTALLATION PHASE ]
  t_install_start  = T_ready(s)              Part arrives, tech begins work
  t_install_end    = T_ready(s) + 12         Repair complete, vehicle assembled
                                              SAFE_TO_DRIVE transitions TRUE

[ CLEARANCE PHASE — T_clear = 2 ticks ]
  t_install_end    Verification & sign-off begins
  t_install_end+1  Vehicle lowered from hoist; driven toward pickup lot
  t_install_end+2  Vehicle confirmed in pickup staging; B4 physically clear
  t_B4_free        = t_install_end + T_clear  B4 available for next vehicle

[ HANDOVER PHASE ]
  t_B4_free        RO-1051 vehicle (V2) granted bay entry
  t_1051_start     = max(t_B4_free, t_1051_ready) = max(t_B4_free, 24)
  t_1051_end       = t_1051_start + 24

[ LATENESS CALCULATION ]
  late_1051        = max(0, t_1051_end - P2)    P2 = 54 (12:30 PM)
  Z1               = w1 * max(0, t_install_end - P1) + w2 * late_1051
=============================================================
```

---

## 5. A2 Sequential Policy — Corrected Calculation

**Source selected:** $S_2$ (ETA $t = 49$, cost \$18.00). Subproblem 1 selects $S_2$ because both candidates meet RO-1042's promise $P_1 = 66$ (13:30 PM), and $S_2$ costs \$37.00 less. Subproblem 1 has zero visibility into Bay $B_4$'s downstream queue.

| Event | Clock time | Tick |
| :--- | :--- | :--- |
| Part $S_2$ usable-ready | 12:05 PM | $t = 49$ |
| Installation start | 12:05 PM | $t = 49$ |
| Installation end | 13:05 PM | $t = 61$ |
| Clearance start | 13:05 PM | $t = 61$ |
| $V_1$ reaches customer staging lot | 13:15 PM | $t = 63$ |
| **Bay $B_4$ confirmed clear** | **13:15 PM** | $t = 63$ |
| RO-1051 enters $B_4$ | 13:15 PM | $t = 63$ |
| RO-1051 completes | 15:15 PM | $t = 87$ |

**Lateness calculations:**

| RO | Finish | Promise | Lateness | Weighted |
| :--- | :--- | :--- | :--- | :--- |
| RO-1042 | $t = 61$ (13:05 PM) | $P_1 = 66$ (13:30 PM) | $\max(0, 61 - 66) \times 5 = 0$ min | $1.0 \times 0 = 0$ |
| RO-1051 | $t = 87$ (15:15 PM) | $P_2 = 54$ (12:30 PM) | $\max(0, 87 - 54) \times 5 = \mathbf{165}$ **min** | $3.0 \times 33 = 99.0$ |

$$\boxed{Z_1(\text{A2}) = 99.0 \text{ weighted ticks}}$$

---

## 6. P3 Joint Policy — Corrected Calculation

**Source selected:** $S_1$ (ETA $t = 27$, cost \$55.00). P3 jointly evaluates $S_1$ and $S_2$; under $S_2$ the result equals A2's outcome ($Z_1 = 99.0$). Under $S_1$:

| Event | Clock time | Tick |
| :--- | :--- | :--- |
| Part $S_1$ usable-ready | 10:15 AM | $t = 27$ |
| Installation start | 10:15 AM | $t = 27$ |
| Installation end; $V_1$ fully repaired | 11:15 AM | $t = 39$ |
| Clearance start | 11:15 AM | $t = 39$ |
| $V_1$ reaches customer staging lot | 11:25 AM | $t = 41$ |
| **Bay $B_4$ confirmed clear** | **11:25 AM** | $t = 41$ |
| RO-1051 enters $B_4$ ($\max(41, 24) = 41$) | 11:25 AM | $t = 41$ |
| RO-1051 completes | 13:25 PM | $t = 65$ |

**Vehicle state check at clearance:** $V_1$'s installation is complete; suspension is fully retorqued; vehicle is `SAFE_TO_DRIVE = TRUE`. It moves to the customer pickup lot — not to $H_2$ (which is for incomplete repairs). $H_2$ saturation is irrelevant to a completed vehicle.

**Lateness calculations:**

| RO | Finish | Promise | Lateness | Weighted |
| :--- | :--- | :--- | :--- | :--- |
| RO-1042 | $t = 39$ (11:15 AM) | $P_1 = 66$ (13:30 PM) | 0 min | 0 |
| RO-1051 | $t = 65$ (13:25 PM) | $P_2 = 54$ (12:30 PM) | $\max(0, 65 - 54) \times 5 = \mathbf{55}$ **min** | $3.0 \times 11 = 33.0$ |

$$\boxed{Z_1(\text{P3}) = 33.0 \text{ weighted ticks}}$$

---

## 7. Authoritative Comparison Table

| Metric | A2 (source $S_2$) | P3 (source $S_1$) |
| :--- | ---: | ---: |
| Source cost | \$18.00 | \$55.00 |
| Part usable-ready | $t = 49$ (12:05 PM) | $t = 27$ (10:15 AM) |
| Installation end | $t = 61$ (13:05 PM) | $t = 39$ (11:15 AM) |
| Clearance duration $T_{\text{clear}}$ | 2 ticks (10 min) | 2 ticks (10 min) |
| **Bay $B_4$ released** | $t = 63$ (13:15 PM) | $t = 41$ (11:25 AM) |
| RO-1051 start | $t = 63$ (13:15 PM) | $t = 41$ (11:25 AM) |
| RO-1051 completion | $t = 87$ (15:15 PM) | $t = 65$ (13:25 PM) |
| RO-1042 lateness | 0 min | 0 min |
| **RO-1051 lateness** | **165 min** | **55 min** |
| **Weighted $Z_1$** | **99.0** | **33.0** |

**Corrected improvement:**
$$\frac{Z_1(\text{A2}) - Z_1(\text{P3})}{Z_1(\text{A2})} = \frac{99.0 - 33.0}{99.0} = \frac{66.0}{99.0} = \mathbf{66.7\%}$$

**Classification:** `MATHEMATICALLY DEMONSTRATED [SYNTHETIC FIXTURE SCEN-01, T_clear = 2 ticks (10 min), HAND-WORKED EXAMPLE]`

> [!IMPORTANT]
> The 71.0% figure from SR1.2.2 assumed zero clearance duration ($T_{\text{clear}} = 0$). That assumption was physically unrealistic. The correct canonical result is **66.7%** with $T_{\text{clear}} = 2$ ticks (10 min). The 71.0% figure is **superseded** by this corrected value.

---

## 8. Algebraic Structural Analysis

For any clearance duration $T_{\text{clear}} \ge 0$ ticks, the following closed-form expressions hold:

$$Z_1(\text{A2}) = w_2 \cdot (31 + T_{\text{clear}}) = 3 \cdot (31 + T_{\text{clear}})$$
$$Z_1(\text{P3}) = w_2 \cdot (9 + T_{\text{clear}}) = 3 \cdot (9 + T_{\text{clear}})$$
$$\text{Improvement} = \frac{Z_1(\text{A2}) - Z_1(\text{P3})}{Z_1(\text{A2})} = \frac{22}{31 + T_{\text{clear}}}$$

**Key mathematical property:** The absolute lateness difference in raw minutes is:

$$(Z_1(\text{A2}) - Z_1(\text{P3})) \times \frac{5}{w_2} = 22 \times 5 = \mathbf{110 \text{ minutes, invariant for all } T_{\text{clear}}}$$

$T_{\text{clear}}$ cancels identically from the difference. The P3 advantage over A2 in absolute lateness is always 110 minutes of RO-1051 lateness, regardless of clearance time. The percentage improvement decreases as clearance time increases because A2's already-large denominator grows further.

---

## 9. Sensitivity Analysis

The table below shows how the improvement percentage changes across four illustrative clearance values. All are synthetic assumptions.

| $T_{\text{clear}}$ | Duration | A2 $Z_1$ | P3 $Z_1$ | A2 RO-1051 lateness | P3 RO-1051 lateness | Abs. diff | Improvement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 ticks | 0 min (SR1.2.2 baseline — physically unrealistic) | 93.0 | 27.0 | 155 min | 45 min | 110 min | 71.0% |
| 1 tick | 5 min (minimum plausible) | 96.0 | 30.0 | 160 min | 50 min | 110 min | 68.8% |
| **2 ticks** | **10 min** `[SCEN-01 canonical]` | **99.0** | **33.0** | **165 min** | **55 min** | **110 min** | **66.7%** |
| 4 ticks | 20 min (slower workflow) | 105.0 | 39.0 | 175 min | 65 min | 110 min | 62.9% |
| 6 ticks | 30 min (congested or understaffed) | 111.0 | 45.0 | 185 min | 75 min | 110 min | 59.5% |

**Sensitivity conclusion:** The P3 advantage over the A2 baseline is **structurally robust** across all reasonable clearance values. For any $T_{\text{clear}} \in [0, 6]$ ticks (0–30 min), the improvement ranges from 59.5% to 71.0%. This robustness arises because $T_{\text{clear}}$ affects both policies equally and cancels from the absolute difference.

> [!NOTE]
> This sensitivity analysis is entirely hand-computed on synthetic inputs. It cannot be used to claim generalisation to other shop configurations, different source arrival gaps, or different downstream job parameters. It demonstrates sensitivity of the SCEN-01 percentage figure to the clearance assumption only.

---

## 10. Physical Continuity Checks

| Check | A2 path | P3 path | Status |
| :--- | :--- | :--- | :--- |
| $V_1$ in $B_4$ at audit time $t = 21$? | ✓ Yes | ✓ Yes | Declared |
| $V_1$ safe-to-drive before clearance? | ✓ $t = 61$ (install complete) | ✓ $t = 39$ (install complete) | Verified |
| Clearance destination available? | ✓ Pickup lot (assumed 1 space at $t = 63$) | ✓ Pickup lot (assumed 1 space at $t = 41$) | Synthetic assumption |
| $H_2$ required for completed vehicle? | ✗ Not needed | ✗ Not needed | Verified |
| $B_4$ released only after clearance ends? | ✓ at $t = 63$ | ✓ at $t = 41$ | Verified |
| $V_1$ and $V_2$ never simultaneously in $B_4$? | ✓ $V_2$ enters at $t = 63$ after $V_1$ leaves | ✓ $V_2$ enters at $t = 41$ after $V_1$ leaves | Verified |
| RO-1051 ready constraint satisfied? | ✓ $\max(63, 24) = 63$ | ✓ $\max(41, 24) = 41$ | Verified |
| $V_1$ never in two locations simultaneously? | ✓ Transitions: $B_4$ → transit → pickup lot | ✓ Transitions: $B_4$ → transit → pickup lot | Verified |

All physical continuity checks pass.
