# StallBreaker 2.0: Benchmark Methodology, Research Limitations & Capability Assessment

**Workspace:** `TEKION-HACKATHON-2026`  
**Milestone:** Stage 4.1 — Benchmark Validation Hardening  
**Date:** November 15, 2026  
**Governing Standard:** Strict epistemic honesty; separation of synthetic mathematical proof from production claims.

---

## 1. Executive Summary: Stage 4 Empirical Findings

The Stage 4 three-policy paired-seed comparative benchmark evaluated three distinct recovery policies across $N=100$ paired synthetic disruptions (`master_seed=42`, `bootstrap_seed=42`, $B=10{,}000$ paired resamples):

1. **Policy A2 (Fixed-Source Sequential Baseline):** Sourcing is pre-fixed to standard regional shuttle (Source S2, $17.20–$24.50 landed freight) regardless of downstream conflicts; scheduling is solved sequentially.
2. **Policy A2+ (Deterministic One-Step Lookahead Heuristic):** Sourcing evaluates immediate downstream repair order conflicts under a bounded freight budget ($\Delta_{\max} = \$50.00$). Upgrades to expedited sourcing (Source S1) if and only if weighted lateness strictly improves within budget.
3. **Policy P3 (StallBreaker Two-Tier CP-SAT Joint Optimization):** Mixed-integer constraint programming solving lexicographic multi-pass optimization over sourcing, bay assignment, and vehicle movement.

### Empirical Results Summary ($N = 100$)

| Metric | Policy A2 (Fixed S2) | Policy A2+ (Lookahead) | Policy P3 (Joint CP-SAT) |
|---|---:|---:|---:|
| **Mean Weighted Lateness ($Z_1$)** | 101.83 ticks | 34.59 ticks | 34.59 ticks |
| **Median Weighted Lateness ($Z_1$)** | 102.00 ticks | 33.00 ticks | 33.00 ticks |
| **Std. Dev. Weighted Lateness** | 15.08 ticks | 11.87 ticks | 11.87 ticks |
| **Mean Landed Freight Cost** | $19.73 | $56.69 | $56.69 |
| **Mean Downstream Delay** | 167.8 min | 57.6 min | 57.6 min |
| **Mean Solve Runtime** | 30.71 ms | 0.29 ms | 31.47 ms |
| **Independent Verifier Certification Rate** | 100.0% (100/100) | 100.0% (100/100) | 100.0% (100/100) |

### Head-to-Head Comparative Summary

| Comparison | Advanced Wins | Ties | Advanced Losses | Win Rate | Mean $\Delta Z_1$ Reduction | Mean Freight Delta | 95% Bootstrap CI for $\Delta Z_1$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| **A2 vs A2+** | 100 | 0 | 0 | 100.0% | +67.24 ticks | +$36.97 | [64.38, 70.08] **[Sig.]** |
| **A2 vs P3** | 100 | 0 | 0 | 100.0% | +67.24 ticks | +$36.97 | [64.38, 70.08] **[Sig.]** |
| **A2+ vs P3** | 0 | 100 | 0 | 0.0% | +0.00 ticks | +$0.00 | [0.00, 0.00] [Not Sig.] |

---

## 2. Seven Strict Research Limitations

To maintain epistemic integrity and adhere to Tekion hackathon evaluation standards, the following seven boundaries must be explicitly communicated:

### 1. Canonical Scenario Family Limitation
The $N=100$ seed generator (`backend/benchmark.py:generate_benchmark_seeds`) models one specific canonical operational pattern: a single bottleneck bay (`B4`), exactly two sequential repair orders (`RO-1042` on-bay and `RO-1051` downstream), and exactly two candidate part sources (`S1` hotshot courier and `S2` regional shuttle). It does not test the broader combinatorial topology of a full dealership shop floor.

### 2. Freight Surcharge Range Limitation
Across all 100 generated seeds, the landed freight difference between S1 and S2 ranged from $+\$28.50$ to $+\$44.80$, which remains strictly within the configured $\Delta_{\max} = \$50.00$ budget threshold. Consequently, the $N=100$ benchmark does not meaningfully test boundary rejection of expedited alternatives that exceed the advisor's willingness-to-pay threshold.

### 3. Fixed Technician Availability Timing
Technician availability is held fixed across the generator logic (`technician_k1_available = True`, `technician_k2_available_tick = None` or fixed arrival). The generator does not simulate variable technician shifts, lunch breaks, unexpected mechanic absences, or dynamic technician queueing.

### 4. Single-Bay Boundary
The experiment does not evaluate multi-bay routing or parallel bay dispatch. Consequently, it does not demonstrate CP-SAT superiority over heuristics in multi-resource assignment problems where disjunctive bay coupling creates NP-hard scheduling bottlenecks.

### 5. Algorithmic Equivalence Disclaimer
The fact that A2+ and P3 produced identical decisions across all 100 synthetic scenarios is **not proof of general algorithmic equivalence**. A single-bay, single-downstream-RO disruption with two part options has a small discrete decision tree:
$$\text{Decisions} = \{(\text{S1}, \text{HOLD}), (\text{S1}, \text{RELOCATE}), (\text{S2}, \text{HOLD}), (\text{S2}, \text{RELOCATE})\}$$
Because vehicle disassembly physically blocks relocation (`is_rollable = False`), the decision space collapses to choosing between S1 and S2. In that restricted domain, a greedy 1-step lookahead heuristic naturally identifies the exact same Pareto-optimal choice as a mixed-integer constraint solver.

### 6. Synthetic Statistical Population Boundary
The reported bootstrap 95% confidence intervals ($[64.38, 70.08]$ for lateness savings) describe only the synthetic scenario generator's parameter distribution. They cannot be cited as representative of real dealership operations, nor do they reflect empirical customer service index (CSI) distributions.

### 7. Simulation vs Production Boundary
All inputs and outputs are simulated in-memory mathematical models. The system does not claim live DMS integration, real-time supplier API integration, or physical shop-floor tracking.

---

## 3. Architecture Capability-Support Matrix

The following assessment distinguishes between **data model representation** and **solver/verifier optimization implementation**:

| Capability | Assessment | Model Fields | Solver Implementation | Verifier Constraints | Limitations & Missing Logic |
|---|---|---|---|---|---|
| **Multiple service bays** | **NOT SUPPORTED** | `RepairOrder.required_bay: str = "B4"`<br>`ScenarioSnapshot.bay_b4_state: BayState` | Hardcoded B4 variables (`b4_release_hold`, `b4_free_reloc`, `b4_avail_after_ro1051`) in `backend/solver.py:128-185`. | Checks only B4 intervals in `backend/verifier.py:270-310`. | No `List[Bay]` in model; solver cannot dispatch to alternative bays; verifier assumes single bay. |
| **Multiple downstream repair orders** | **NOT SUPPORTED** | `ScenarioSnapshot.ro1042: RepairOrder`<br>`ScenarioSnapshot.ro1051: RepairOrder` | Hardcoded decision variables specifically for `ro1042` and `ro1051` in `backend/solver.py:118-204`. | Specifically validates RO-1042 and RO-1051 in `backend/verifier.py:220-260`. | No queue or `List[RepairOrder]`; cannot evaluate 3+ cascading jobs; A2+ only evaluates single downstream RO. |
| **Multiple technicians** | **PARTIALLY SUPPORTED** | `technician_k1_available: bool`<br>`technician_k2_available_tick: Optional[int]`<br>`technician_assignments: Optional[Dict]` | Reads `tech_avail` bottleneck for RO-1051 only in `backend/solver.py:131-155`. | Checks `ro1051_start >= tech_avail` in `backend/verifier.py:320-335`. | No technician assignment/dispatch optimization; technicians cannot be dynamically reassigned across bays. |
| **Technician availability constraints** | **SUPPORTED** | `technician_k2_available_tick: Optional[int]`<br>`ro1051.technician_available_tick: Optional[int]` | Explicit `AddMaxEquality` in both HOLD and RELOCATE modes in `backend/solver.py:138, 153`. | Validates start tick vs availability tick with 0-tick explicit handling in `backend/verifier.py:325-335`. | Fully supported and certified for RO-1051. Explicit 0-tick handling verified in test suite. |
| **Holding-area contention** | **PARTIALLY SUPPORTED** | `h2_capacity: int = 1`<br>`h2_available_stalls: int = 0` | Pre-solver feasibility check in `backend/eligibility.py:50-65`; disables relocation if `stalls < 1`. | Validates `h2_available_stalls >= 1` before accepting relocation in `backend/verifier.py:135-142`. | Static capacity check only; no time-indexed holding intervals or multi-vehicle holding contention. |
| **Additional part-source candidates** | **SUPPORTED** | `ScenarioSnapshot.sources: List[PartSource]` | Dynamically constructs boolean variables `src_vars` and sums ready time and freight over all eligible sources in `backend/solver.py:85-116`. | Dynamically validates chosen source against `snapshot.sources` in `backend/verifier.py:100-125`. | Fully supports $M \ge 2$ candidate sources (S1, S2, S3, S4, ...). A2+ evaluates all candidates against anchor. |
| **Freight-budget boundary cases** | **SUPPORTED (A2+ heuristic)**<br>*Lexicographic in P3* | `PartSource.cost: float`<br>`max_freight_budget_delta: float` | P3 optimizes lexicographically (Pass 1 minimizes lateness; Pass 2 minimizes freight) without a hard budget cap. | Validates source cost integrity against snapshot. | A2+ strictly enforces `freight_delta <= max_budget + 1e-6`. P3 does not reject expensive sources if they reduce lateness. |

---

## 4. Statistical Interpretation of Bootstrap Confidence Intervals

The benchmark executes paired bootstrap resampling with $B=10{,}000$ iterations and a deterministic seed (`bootstrap_seed=42`). 

### Paired Metric Formulations
For each valid scenario $i \in \{1, \dots, M\}$:
- **Lateness Reduction:** $\Delta Z_{1, i} = Z_1(\text{Baseline}, i) - Z_1(\text{Advanced}, i)$. Positive values indicate delay reduction.
- **Freight Surcharge Delta:** $\Delta \text{Cost}_i = \text{Cost}(\text{Advanced}, i) - \text{Cost}(\text{Baseline}, i)$. Positive values indicate capital expenditure.

### Statistical Significance Threshold
A comparison is defined as statistically significant at $\alpha = 0.05$ if and only if the two-sided 95% bootstrap confidence interval strictly excludes $0.0$:
$$\text{Significance} \iff [CI_{0.025}, CI_{0.975}] \cap \{0.0\} = \emptyset$$

On the $N=100$ canonical family:
- **A2 vs A2+:** $95\%\text{ CI} = [64.38, 70.08]$ ticks $\implies$ **Statistically Significant**.
- **A2 vs P3:** $95\%\text{ CI} = [64.38, 70.08]$ ticks $\implies$ **Statistically Significant**.
- **A2+ vs P3:** $95\%\text{ CI} = [0.00, 0.00]$ ticks $\implies$ **Not Statistically Significant (Exact Parity)**.

---

## 5. Requirements for Future Stress-Test Datasets

Before claiming mathematical divergence or superiority of CP-SAT (P3) over local heuristics (A2+), future research datasets must legitimately introduce combinatorial complexity:

1. **Multi-Source Expansion ($M = 4–6$):** Sourcing sets must include courier options that exceed $\Delta_{\max} = \$50.00$ (e.g. $\$120$ same-day flight courier) to prove heuristic budget discipline vs unconstrained optimization.
2. **Technician Arrival Jitter:** Introduce variable technician arrival ticks ($t_{\text{avail}} \in [20, 60]$) to create scenarios where fast parts arrive but sit idle waiting for technicians.
3. **Multi-Bay Extension (Phase 2):** Introduce Bay B5 and parallel technician pools to require disjunctive interval assignment across bays.
4. **Buffer Contention:** Model dynamic holding capacity where multiple bays compete for limited holding stalls.
