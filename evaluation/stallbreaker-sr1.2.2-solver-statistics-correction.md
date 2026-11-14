# StallBreaker: SR1.2.2 — Solver Semantics and Statistical Claims Correction

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.2-solver-statistics-correction.md`  
**Phase:** SR1.2.2 — Consistency Correction and Final Gate Audit  
**Standard Compliance:** `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Board:** Operations Research Scientist, Constraint Programming Specialist, Statistical Evaluation Reviewer  
**Date:** November 14, 2026  

---

## 1. Workstream C — Solver Semantics Corrections

### 1.1 Authoritative Objective Architecture (Unchanged)

Sequential multi-pass lexicographic optimization remains the sole authoritative architecture. The scalar-weight formulation was rejected in SR1.2.1 and that rejection stands. This section corrects the **FEASIBLE-state bound** and **infeasible fallback** semantics.

---

### 1.2 Lexicographic Optimization: Exact vs. Approximate

The word "lexicographic optimum" has a precise meaning: each objective is solved to global optimality before the next objective is considered. When a CP-SAT pass returns `FEASIBLE` (a valid incumbent exists, but optimality is not proved within the time limit), the result is **not** a lexicographic optimum. It is an approximate lexicographic plan.

This distinction must be preserved in all documentation and system logging.

| Solver status | Meaning | Allowable claim |
| :--- | :--- | :--- |
| `OPTIMAL` | Global optimum proved for this objective within time limit | "Lexicographically optimal for Tier $k$" |
| `FEASIBLE` | Valid incumbent found; optimality not proved | "Approximately lexicographic plan (incumbent retained; gap unproven)" |
| `INFEASIBLE` | No solution exists satisfying hard constraints | No plan; escalate |
| `UNKNOWN` | Time limit reached before any feasible solution found | No plan; retain existing schedule |

---

### 1.3 Corrected FEASIBLE-State Bound: Incumbent Lock Policy

SR1.2.1 proposed the formula:
$$Z_k \le Z_k^{\text{incumbent}} \cdot (1 + \min(\epsilon, 0.05))$$

**Problems with this formula:**

1. The 5% cap is a design parameter, not a mathematically derived bound from the problem structure. It is not justified by any analysis of the objective's range or domain.
2. When the actual solver gap $\epsilon > 0.05$, the formula caps at 5% but the solver has *not* proved the incumbent is within 5% of optimum. The cap misrepresents the proven guarantee.
3. A relative tolerance on a lateness objective (measured in weighted ticks) has no inherent operational meaning. 5% of a 100-tick incumbent $= 5$ extra weighted ticks $= 25$ min of additional customer lateness — which may be unacceptable.
4. The relaxation compounds across passes: Pass 2 → Pass 3 → Pass 4 each inherit a degraded bound, potentially allowing the final plan to substantially underperform the lexicographic ideal.

**Corrected policy — Incumbent Lock (no relaxation):**

When Pass $k$ returns `FEASIBLE`:
- Fix $Z_k \le Z_k^{\text{incumbent}}$ exactly (no tolerance added).
- Proceed to Pass $k{+}1$ with this exact bound active.
- Record `APPROXIMATE_LEXICOGRAPHIC_PLAN` in the plan metadata.
- The final plan output states: "Approximately lexicographic — not all passes proved optimal."

**Rationale:** An exact incumbent lock is the most defensible policy for a priority-based system. It ensures that Pass $k{+}1$ cannot worsen the highest-priority objective by any amount in exchange for lower-priority savings. This correctly reflects the lexicographic intent without introducing an unjustified tolerance.

**What is not guaranteed:** The incumbent retained from a `FEASIBLE` pass may not be the global optimum for that tier. The final plan is a feasible plan that is locally constrained to be no worse than the best found within the time limit, with subsequent tiers optimized given that constraint.

---

### 1.4 Complete Per-Pass Status Decision Table

| Pass | Objective | `OPTIMAL` | `FEASIBLE` | `INFEASIBLE` | `UNKNOWN` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pass 1** (Feasibility) | Satisfy all hard constraints (C1–C24) | Hard constraints feasible; proceed to Pass 2 | N/A (Pass 1 is feasibility; first feasible solution IS the result) | **Abort.** No plan possible under current shop state. → Emergency fallback. Alert dispatcher. | **Abort.** No feasible solution found within time limit. Retain existing DMS schedule as-is. Alert dispatcher. |
| **Pass 2** ($Z_1$: Customer Lateness) | $\min \sum_r w_r \cdot \text{late}_r$ | Lock $Z_1 \le Z_1^*$. Proceed to Pass 3. | Lock $Z_1 \le Z_1^{\text{inc}}$ (exact). Log `APPROX_LEX`. Proceed to Pass 3. | Infeasible with current $Z_1$ bound (should not occur if Pass 1 succeeded). Relax $Z_1$ bound by incremental step; re-attempt or escalate. | Retain $Z_1^{\text{inc}}$ from any partial search, if available. If no incumbent, treat as INFEASIBLE. |
| **Pass 3** ($Z_2$: Bay Disruption) | $\min \sum_v m_v + \text{idle}$ | Lock $Z_2 \le Z_2^*$. Proceed to Pass 4. | Lock $Z_2 \le Z_2^{\text{inc}}$ (exact). Log `APPROX_LEX`. Proceed to Pass 4. | Unexpected: Pass 2 set $Z_1$ bound that is not achievable with any bay assignment. Report `INFEASIBLE_TIER3`; human review. | Retain best $Z_2^{\text{inc}}$; if none, retain Pass 2 incumbent as complete plan and skip Pass 4–5. |
| **Pass 4** ($Z_3$: Sourcing Spend) | $\min \sum_{r,s} c_s \cdot x_{r,s}$ | Lock $Z_3 \le Z_3^*$. Proceed to Pass 5. | Lock $Z_3 \le Z_3^{\text{inc}}$ (exact). Log `APPROX_LEX`. Proceed to Pass 5. | Unexpected; human review. | Retain best $Z_3^{\text{inc}}$; if none, skip Pass 5 and return current plan. |
| **Pass 5** ($Z_4$: Schedule Churn) | $\min \sum_o \|\text{start}_o - \text{prior}_o\|$ | Final plan is complete. | Accept incumbent; mark plan `APPROX_LEX`. Commit. | Unexpected; human review. | Accept best incumbent from Pass 4 as final plan. |

**Hard constraint protection across all passes:** Constraints C1–C24 (hoist non-overlap, holding capacity, safe-to-relocate, warranty fitment, technician working hours) are enforced in every pass. They are **never** converted into soft penalties. A plan that violates a hard constraint is not committed regardless of its objective value.

---

### 1.5 Corrected Emergency Fallback Semantics

SR1.2.1 stated that an `INFEASIBLE` result "triggers Deterministic Emergency Relocation Fallback." This is too broad. Consider scenarios where relocation is itself infeasible (no holding space, vehicle unsafe to move, no qualified technician). An infeasible optimization result must not be treated as permission to violate the constraints that produced the infeasibility.

**Corrected fallback, in strict priority order:**

1. **No new commitment:** StallBreaker does not issue any external supplier reservation or modify the DMS schedule.
2. **Preserve current physical state:** Vehicle positions, bay assignments, and in-progress technician work remain exactly as they are. No automated vehicle move is triggered.
3. **Retain existing valid schedule:** Any previously committed schedule segments that remain feasible (not affected by the shortage) continue as-is.
4. **Escalate to dispatcher or service manager:** A structured alert is raised with the specific infeasibility reason (e.g., "No holding slot available," "No eligible supplier for part SKU X," "Bay B4 required by two simultaneous operations").
5. **Request explicit human intervention:** No automated action proceeds until a human confirms the physical state and approves a course of action.

The word "deterministic" is retained only in the sense that the fallback procedure itself is deterministic (steps 1–5 execute in fixed order). The *outcome* of the fallback is not guaranteed to resolve the shop conflict; that depends on physical conditions.

---

## 2. Workstream D — Statistical and Evidence Claims Corrections

### 2.1 Corrected Claim: 30 Paired Seeds and Statistical Power

SR1.2.1 stated: "sufficient to detect large synthetic effect sizes (Cohen's $d > 0.8$)."

**Problem:** This statement requires a statistical power analysis to support it. Power depends on:
- The variance of the paired difference $\Delta_i = Y_i^{\text{A2}} - Y_i^{\text{P3}}$ (unknown until an experiment is run).
- The significance level $\alpha$ (typically 0.05).
- The desired power $1 - \beta$ (typically 0.80).
- The distribution of shop-day outcomes (not known from synthetic analysis alone).
- The number of truly independent experimental units.

Without a power analysis using estimated variance, the claim that 30 seeds "detects Cohen's $d > 0.8$" is unsupported. The correct statement is:

> **"30 paired shop-day seeds constitute an exploratory initial protocol. No power analysis has been performed. The sample size is an engineering starting point, not a statistically justified number. Results should be interpreted as exploratory, not confirmatory."**

### 2.2 Experimental Unit and Paired Analysis (Retained Correctly)

The full **shop-day** remains the correct experimental unit because repair orders within the same simulated day share bays, technicians, and holding capacity — they are not independent. Individual ROs within a seed must not be treated as independent observations.

Paired design: on each seed $i$, the identical shop-day is simulated under A2 and P3 (Common Random Numbers, same random realizations). Primary paired difference: $\Delta_i = Z_1^{(i, \text{A2})} - Z_1^{(i, \text{P3})}$.

### 2.3 Timeout and Infeasibility Treatment in Experiments

The experimental protocol must specify:

| Scenario | Treatment |
| :--- | :--- |
| A2 times out (no solution) | Record `TIMEOUT_A2`; seed is excluded from primary analysis unless a sensitivity analysis is performed. Report the number of exclusions. |
| P3 times out (no solution) | Record `TIMEOUT_P3`; same exclusion rule. |
| Both time out | Record `TIMEOUT_BOTH`; excluded from all comparisons. |
| Only one policy is feasible | The feasible policy wins that seed. Report separately. Do not silently discard. |
| Feasible but unproven incumbent | Report with optimality gap. Include in analysis but note potential over-reporting of P3 advantage if P3 found a tighter bound. |
| Missing / crashed simulation run | Reported explicitly; not silently dropped. |

**Critical rule:** Do not compute improvement percentages using only favorable completed runs without declaring the selection rule and reporting exclusion rates.

### 2.4 Bootstrap Language Correction

BCa bootstrap resampling does not create additional independent experimental units. 10,000 bootstrap replicates resample the same 30 paired differences. The bootstrap quantifies the sampling uncertainty of the mean (or other statistic) given those 30 observations. It does not substitute for a larger sample.

**Correct claim:** "BCa bootstrap 95% confidence interval provides an interval estimate of the mean paired difference under the assumption that the 30 shop-day seeds are representative of the target population of dealership days. This assumption is unverified."

Hypothesis testing: retain the two-sided Wilcoxon signed-rank test. Report the test statistic, $p$-value, and paired median difference alongside the mean and CI. Do not claim statistical superiority until an actual experiment has been run.

### 2.5 Corrected Evidence Classification Table

| Claim | Classification | Required wording |
| :--- | :--- | :--- |
| 71.0% reduction in RO-1051 lateness (SCEN-01) | `MATHEMATICALLY DEMONSTRATED [SYNTHETIC]` | "71.0% reduction in RO-1051 lateness in hand-worked synthetic worked example SCEN-01. Not a dealership experiment or simulation result." |
| 37.5% improvement figure (SR1.2.1 Section 6) | **WITHDRAWN** | Do not use. The figure was derived from inconsistent scenario parameters. |
| 120-minute A2 promise miss | **WITHDRAWN** (incorrect promise time used) | Correct figure: 155-minute A2 promise miss under SCEN-01 declared inputs. |
| 75-minute P3 promise miss | **WITHDRAWN** (incorrect finish time used) | Correct figure: 45-minute P3 promise miss under SCEN-01 declared inputs. |
| Solver runtime < 800 ms | `DESIGN SPECIFICATION` | "Target design parameter. No solver has been implemented or benchmarked." |
| 2,500 ms solver timeout | `DESIGN SPECIFICATION` | "Proposed configuration threshold. Subject to change during implementation." |
| 25–35 hours dead bay time per week | `ESTIMATE` | "Operational heuristic estimate from automotive dealership domain knowledge. Not measured." |
| 30 paired seeds | `PROPOSED EXPERIMENT` | "Exploratory initial protocol. No power analysis performed. No experiment has been run." |
| BCa bootstrap 95% CI | `PROPOSED EXPERIMENT` | "Proposed statistical method for a future experiment. No results exist." |
| Weighted lateness $Z_1$ formula | `DESIGN SPECIFICATION` | "Mathematical formulation of the proposed objective function." |
| Sequential multi-pass lexicographic solver | `DESIGN SPECIFICATION` | "Proposed solver architecture. Not implemented or benchmarked." |

---

## 3. Summary of Corrections

| SR1.2.1 error | Correction in SR1.2.2 |
| :--- | :--- |
| FEASIBLE bound formula `Z_k <= Z_k_inc * (1 + min(eps, 0.05))` — arbitrary cap misrepresented as justified | Replaced with **Incumbent Lock** policy: `Z_k <= Z_k_inc` exactly. Final plan is marked `APPROXIMATE_LEXICOGRAPHIC_PLAN`. |
| Per-pass status table was incomplete (only Pass 1 was partially defined) | **Full 5-pass × 4-status table** provided. |
| Infeasible → "Deterministic Emergency Relocation Fallback" — overstated capability | Corrected to 5-step escalation that cannot violate hard constraints; no automatic vehicle move. |
| "30 seeds detect Cohen's d > 0.8" — unsupported power claim | Corrected to "exploratory protocol; no power analysis performed." |
| BCa bootstrap language implied added statistical power | Corrected: bootstrap quantifies uncertainty of existing 30 samples; does not add independent observations. |
| 37.5% / 120 min / 75 min lateness figures | **All withdrawn.** Correct SCEN-01 figures: 71.0% / 155 min / 45 min. |
