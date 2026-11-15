# StallBreaker 2: Scientific & Engineering Claim Ledger

**Workspace:** `TEKION-HACKATHON-2026`  
**Phase:** Phase 0 — Evidence Governance & Integrity Audit  
**Date:** November 15, 2026  
**Governing Standard:** Strict epistemic discipline. Claims without traceable evidence fail.

---

## 1. Epistemic Classification Taxonomy

Every technical, operational, and commercial statement made across the StallBreaker project is tagged with one of seven evidence categories:

| Tag | Category | Definition & Standard |
|---|---|---|
| `[PUBLIC]` | Public Verifiable Fact | Published automotive retail research, OEM standards, textbooks, or official vendor documentation. |
| `[TEAM SOURCE]` | Team-Authored Code | Source code, models, and scripts authored directly by this hackathon team in this repository. |
| `[INFERENCE]` | Logical Deduction | Mechanistic deduction derived mathematically from verified physical or operational premises. |
| `[SYNTHETIC]` | Synthetic Parameter | Deliberately designed synthetic test values, scenario configurations, and simulation distributions. |
| `[MEASURED-SYNTH]` | Empirical Measurement | Actual empirical outputs measured from executing Google OR-Tools CP-SAT on synthetic fixtures. |
| `[TARGET]` | Engineering Specification | Architecture specifications and design targets for future implementation phases (not yet built). |
| `[VALIDATE]` | Partner-Dependent Claim | Statements requiring direct verification with Tekion engineers or dealership pilot data. |

---

## 2. Comprehensive Claim Ledger

### 2.1 Problem Space & Dealership Fixed Operations

| ID | Statement / Claim | Evidence Tag | Source / Verification |
|---|---|---|---|
| **C-01** | Vehicle immobilisation on a lift during a parts shortage locks the bay, preventing subsequent scheduled repairs from accessing the hoist. | `[PUBLIC]` / `[INFERENCE]` | NADA Fixed Operations Guidelines; standard physical mechanics of two-post and alignment lifts. |
| **C-02** | Traditional dealership management systems (DMS) decouple parts ordering from shop-floor dispatch scheduling. | `[PUBLIC]` | Dealer Management System functional architectures (parts department ordering screens operate independently of service appointment dispatch). |
| **C-03** | Parts clerks routinely select the lowest freight-cost source without real-time visibility into downstream bay occupancy costs. | `[INFERENCE]` | Standard dealership procurement incentives: parts managers are evaluated on parts inventory margin and freight budget, not service bay throughput. |
| **C-04** | A vehicle with disassembled suspension or detached wheel hubs cannot be safely pushed or flat-towed to a holding yard. | `[PUBLIC]` | OSHA automotive shop safety standards; vehicle mechanical integrity requirements. |
| **C-05** | Dealership service departments suffer significant customer churn and commercial fleet penalties from uncommunicated promise breaches. | `[PUBLIC]` | J.D. Power U.S. Customer Service Index (CSI) Study. |

---

### 2.2 Mathematical Formulation & Algorithmic Mechanics

| ID | Statement / Claim | Evidence Tag | Source / Verification |
|---|---|---|---|
| **C-06** | Service bay recovery can be formulated as a mixed-integer constraint satisfaction problem (CP-SAT) with lexicographic multi-pass optimization. | `[TEAM SOURCE]` | Implemented in [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L35-L259). |
| **C-07** | Pass 1 minimizes total weighted customer lateness ($Z_1$); Pass 2 minimizes expedited freight cost ($Z_2$) subject to $Z_1 \le Z_1^*$. | `[TEAM SOURCE]` | Implemented in [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L200-L240). |
| **C-08** | Milestone start times are strictly pinned to earliest feasible physical moments via `AddMaxEquality` constraints. | `[TEAM SOURCE]` | Implemented in [`backend/solver.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/solver.py#L118-L157); verified in `test_30` and `test_31`. |
| **C-09** | On canonical synthetic fixture `S-MATH-01`, P3 reduces weighted lateness by 66.7% (33 vs 99 ticks) compared to fixed-source baseline A2. | `[MEASURED-SYNTH]` | Verified in `test_03` and `test_04` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py); measured via live solver execution. |
| **C-10** | On canonical synthetic fixture `S-MATH-01-ROLLABLE`, P3 reduces weighted lateness by 99.0% (1 vs 99 ticks) by relocating the vehicle to H2. | `[MEASURED-SYNTH]` | Verified in `test_26` in [`backend/tests/test_acceptance.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/tests/test_acceptance.py); measured via live solver execution. |
| **C-11** | In the $N=100$ Monte Carlo benchmark under synthetic operational jitter, P3 outperforms A2 on 100/100 seeds with mean solve time ~31 ms. | `[MEASURED-SYNTH]` | Recorded in [`generated-results/benchmark_results_n100_20261115_033621.json`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/generated-results/benchmark_results_n100_20261115_033621.json); verified in `test_23`. |
| **C-12** | The 100% win-rate is evaluated against study-defined fixed-source baseline A2 on synthetic fixtures, not against human master dispatchers on real production data. | `[SYNTHETIC]` | Stated as explicit boundary in UI telemetry and test documentation. |
| **C-12a** | Synthetic fixture `S-MATH-02` proves lexicographic cost discipline (saving $37 freight) when downstream technician bottlenecks prevent on-time acceleration. | `[SYNTHETIC]` | Hand-derived in `docs/STALLBREAKER2_FIXTURE_S_MATH_02.md`; verified by Stage 1 fixture registry. |
| **C-12b** | Synthetic fixture `S-MATH-03` proves fail-closed safety gating, pruning physically unsafe vehicle relocation ($Z_1^{illegal} = 1.0$) and enforcing Invariant CE-1 ($Z_1 = 45.0$). | `[SYNTHETIC]` | Hand-derived in `docs/STALLBREAKER2_FIXTURE_S_MATH_03.md`; verified by Stage 1 fixture registry. |

---

### 2.3 Software Architecture & Transactional Concurrency

| ID | Statement / Claim | Evidence Tag | Source / Verification |
|---|---|---|---|
| **C-13** | A proposal generated on one scenario cannot be committed against another scenario even if both snapshots share the same version number. | `[TEAM SOURCE]` | Implemented in [`backend/revalidation.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/revalidation.py#L37-L64); verified in `test_28` and `test_29`. |
| **C-14** | When an external concurrent order consumes inventory (ATP $1 \to 0$), attempting to commit an earlier proposal is rejected as `STALE_SNAPSHOT`. | `[TEAM SOURCE]` | Implemented in [`backend/revalidation.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/revalidation.py#L66-L80); verified in `test_15` and Act 3 live proxy test. |
| **C-15** | Automated re-solving on stale snapshot generates a fallback proposal, but requires a second explicit human approval before commitment. | `[TEAM SOURCE]` | Implemented in [`backend/revalidation.py`](file:///c:/Users/asus/Documents/TEKION-HACKATHON-2026/backend/revalidation.py#L82-L100); verified in `test_21` and UI action bar. |
| **C-16** | Local proposal approval in the MVP updates prototype simulation state; it does not dispatch purchase orders to real supplier APIs or DMS databases. | `[TEAM SOURCE]` | Stated explicitly in UI commit banner and documentation. |

---

### 2.4 StallBreaker 2 Target Specifications (Future Phases)

| ID | Statement / Claim | Evidence Tag | Source / Verification |
|---|---|---|---|
| **C-17** | The engine can be unified to evaluate both pre-authorization repair quotes (Quote Mode) and in-flight disruptions (Recover Mode). | `[TARGET]` | Specified in *StallBreaker 2: Technical Report*; architecture defined in Phase 0 Build Plan. |
| **C-18** | A standalone independent pure-Python verifier (`backend/verifier.py`) and 7-gate commit-time revalidation pipeline (`backend/revalidation.py`) mathematically certify schedule and allocation correctness across 11 domain invariants with SHA-256 decision-payload integrity digests. | `[TEAM SOURCE]` | Implemented in `backend/verifier.py` and `backend/revalidation.py`; verified in `test_verifier.py` and `test_approval_integrity.py`. Scope: In-memory demonstration integrity; production requires isolated keystore, keyed signing (HMAC/Ed25519), and transactional persistence. |
| **C-19** | A two-layer JPS lower bound can prune combinatorial candidate spaces before CP-SAT setup. | `[TARGET]` | Algorithmic target for Tier B scaling. |
| **C-20** | A transactional outbox pattern guarantees reliable at-least-once message delivery to Tekion DMS webhooks. | `[TARGET]` | System architecture target for Tier C enterprise pilot. |

---

### 2.5 Claims Requiring Partner Validation (Mentor Scope)

| ID | Statement / Claim | Evidence Tag | Source / Verification |
|---|---|---|---|
| **C-21** | Tekion's current DMS Auto Dispatcher re-optimizes bay assignments when a parts shortage occurs on an active job. | `[VALIDATE]` | Question for Tekion Mentor (Item 1). Do not claim Tekion lacks this without direct confirmation. |
| **C-22** | Tekion parts inventory API distinguishes between physical on-hand stock and uncommitted available-to-promise (ATP). | `[VALIDATE]` | Question for Tekion Mentor (Item 2). Requires schema review. |
| **C-23** | Dealerships permit automated temporary reservation holds (30–60 min TTL) on supplier inventory via OEM D2D or parts aggregators. | `[VALIDATE]` | Question for Tekion Mentor (Item 5). Involves commercial supplier agreements. |
| **C-24** | Real dealership shop floors track physical vehicle rollability and holding stall occupancy in real-time DMS data. | `[VALIDATE]` | Question for Tekion Mentor (Item 6). Involves service advisor field adoption reality. |
| **C-25** | On the $N=100$ canonical synthetic single-bay family, deterministic lookahead baseline A2+ matches CP-SAT optimization P3 on 100% of scenarios (100 ties, 0 wins, 0 losses; $\Delta Z_1 = +0.00$ ticks, 95% CI $[0.00, 0.00]$). | `[MEASURED-SYNTH]` | Recorded in `generated-results/three_policy_benchmark_n100_seed42_20261115_191819.json`; certified by `backend/verifier.py`. |
| **C-26** | The empirical parity between A2+ and P3 on the single-bay canonical family does not prove general algorithmic equivalence; P3's structural combinatorial superiority is relevant in multi-bay, multi-technician, and buffer-contention disruptions. | `[INFERENCE]` | Documented in `docs/BENCHMARK_RESEARCH_LIMITATIONS.md`; verified by capability-support architectural audit. |

---

## 3. Disallowed Overclaims Checklist

The following claims are **strictly forbidden** in all presentation materials, pitch decks, and reports:

- ❌ *"StallBreaker is proven to increase dealership fixed operations revenue by 20% in production."* (No field deployment has occurred; claims are bounded to synthetic experiments).
- ❌ *"StallBreaker eliminates $10,000+ commercial fleet losses."* (Fleet dollar figures are synthetic illustrative context, not verified audited losses).
- ❌ *"Tekion DMS is completely blind to shop bottlenecks."* (Unfair and unverified claim about partner software).
- ❌ *"Our CP-SAT solver achieves 100% win-rate against human dispatchers."* (Win-rate is strictly measured against baseline A2 under synthetic jitter).
- ❌ *"StallBreaker provides production-grade cryptographic security against malicious state-store tampering."* (The local prototype uses an in-memory SHA-256 decision-payload digest for tamper detection within the demonstration session; production deployments require an isolated keystore, HMAC/Ed25519 keyed signing, and durable transactional state).
- ❌ *"The complete StallBreaker 2 architecture is already built."* (Only Recover-mode prototype exists today; Phase 0 documents the truthful build plan).
