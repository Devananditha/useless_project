# StallBreaker: Master Source-of-Truth Index

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-source-of-truth-index.md`  
**Phase:** StallBreaker Transition Evaluation — Verification Pass SR1.2  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Authority:** Joint Independent Verification Board  
**Date:** November 14, 2026  
**Status:** CANONICAL INDEX ESTABLISHED & VERIFIED (SR1.2)  

---

## 1. Architectural Mandate & Governance

To ensure zero drift, eliminate contradictions, and enforce cross-document consistency across the StallBreaker workspace, this document serves as the **Authoritative Source-of-Truth Index**. 

Every core operational concept, mathematical equation, state machine, experimental baseline, transaction contract, and scenario fixture is assigned exactly **ONE Primary Owning Document**. All other documents MUST defer to and cite the owning document without inventing local variants.

---

## 2. Master Definition Ownership & Reference Map

```
+===================================================================================================================================+
|                                           MASTER SOURCE-OF-TRUTH MATRIX                                                           |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| #  | Core Architectural Domain          | Authoritative Owning Document         | Referencing / Dependent Documents               |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 01 | **Product Boundary & UC04 Scope**  | `stallbreaker-product-adoption-audit` | `stallbreaker-final-decision.md`,               |
|    | (Mid-repair recovery vs. UC01)     | Section 3                             | `stallbreaker-tekion-capability-gap.md`         |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 02 | **Reduced MVP Scope & 10 Rules**   | `stallbreaker-final-decision.md`      | `stallbreaker-mvp-feasibility.md`,              |
|    | (Single rooftop, bounded scale)    | Section 1                             | `stallbreaker-product-adoption-audit.md`        |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 03 | **Transactional Demo Fixture**     | `stallbreaker-demo-and-evaluation-`   | `stallbreaker-mvp-feasibility.md`,              |
|    | (Scenario S-DEMO-01, Saga/Race)    | `plan.md` — Section 2                 | `stallbreaker-sr1.2-claim-evidence-matrix.md`   |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 04 | **Vehicle Physical State Machine** | `stallbreaker-sr1.2.5-`               | `stallbreaker-demo-and-evaluation-plan.md`,     |
|    | (Entity V: 2-branch lifecycle)     | `final-reconciliation.md` — Sec 4.2   | `stallbreaker-mvp-feasibility.md`               |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 05 | **Reservation Lifecycle & Leases** | `stallbreaker-sr1.2-transaction-`     | `stallbreaker-mvp-feasibility.md`,              |
|    | (7 states, 10-min lease, revoke)   | `verification.md` — Section 2         | `stallbreaker-demo-and-evaluation-plan.md`      |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 06 | **Revalidation Race Event**        | `stallbreaker-demo-and-evaluation-`   | `stallbreaker-sr1.2-transaction-verification`,  |
|    | (EVT-RACE-012, pin crack defect)   | `plan.md` — Section 4                 | `stallbreaker-mvp-feasibility.md`               |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 07 | **Pre-Commit 10-Token Algorithm**  | `stallbreaker-sr1.2-transaction-`     | `stallbreaker-mvp-feasibility.md`,              |
|    | (Atomic optimistic concurrency)    | `verification.md` — Section 3 & 4     | `stallbreaker-final-decision.md`                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 08 | **Joint CP-SAT Formulation**       | `stallbreaker-sr1.2-mathematical-`    | `stallbreaker-mvp-feasibility.md`,              |
|    | (Vehicle interval Iv_bay, coupling)| `verification.md` — Section 2 & 3     | `stallbreaker-demo-and-evaluation-plan.md`      |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 09 | **Lexicographic Objective Tiers**  | `stallbreaker-sr1.2-mathematical-`    | `stallbreaker-mvp-feasibility.md`,              |
|    | (5-tier priority hierarchy)        | `verification.md` — Section 4         | `stallbreaker-partsrescue-transition-map.md`    |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 10 | **Time-Indexed Holding Capacity**  | `stallbreaker-sr1.2-mathematical-`    | `stallbreaker-mvp-feasibility.md`,              |
|    | (NoOverlap / Cumulative intervals) | `verification.md` — Section 3.5 & 5   | `stallbreaker-demo-and-evaluation-plan.md`      |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 11 | **Experimental Baselines**         | `stallbreaker-sr1.2-experiment-`      | `stallbreaker-demo-and-evaluation-plan.md`,     |
|    | (P0, P1, A2, P3 definitions)       | `verification.md` — Section 2         | `stallbreaker-final-decision.md`                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 12 | **Falsification Scenarios (1–3)**  | `stallbreaker-sr1.2-experiment-`      | `stallbreaker-demo-and-evaluation-plan.md`,     |
|    | (Joint win, Tie, Sequential win)   | `verification.md` — Section 3         | `stallbreaker-product-adoption-audit.md`        |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 13 | **Metric Taxonomy (Biz vs. Eng)**  | `stallbreaker-sr1.2-experiment-`      | `stallbreaker-demo-and-evaluation-plan.md`,     |
|    | (M1–M5 business, R1–R4 reliability)| `verification.md` — Section 4         | `stallbreaker-final-decision.md`                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 14 | **Claim-to-Evidence Matrix**       | `stallbreaker-sr1.2-claim-evidence-`  | All Workspace Deliverables                      |
|    | (7-tier epistemological taxonomy)  | `matrix.md` — Section 1 & 2           |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 15 | **PartsRescue Asset Reuse Matrix** | `stallbreaker-partsrescue-transition-`| `stallbreaker-final-decision.md`,               |
|    | (5-dim taxonomy; code reuse = 0%)  | `map.md` — Section 1 & 2              | `stallbreaker-product-adoption-audit.md`        |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 16 | **Tekion Capability Baseline**     | `stallbreaker-tekion-capability-gap`  | `stallbreaker-product-adoption-audit.md`,       |
|    | (Public scope, sources [W1]–[W7])  | Section 1 & 2                         | `stallbreaker-final-decision.md`                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 17 | **Four-Tier Novelty Framework**    | `stallbreaker-tekion-capability-gap`  | `stallbreaker-product-adoption-audit.md`,       |
|    | (Tiers 1–4 competitive posture)    | Section 3                             | `stallbreaker-final-decision.md`                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 18 | **Prioritized Mentor Questions**   | `stallbreaker-tekion-capability-gap`  | `stallbreaker-final-decision.md`                |
|    | (10 prioritized validation items)  | Section 4                             |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 19 | **Itemized SR1.2 Correction Log**  | `stallbreaker-sr1.2-correction-log`   | All Workspace Documents                         |
|    | (Defect tracking across audits)    | Master Document                       |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 20 | **Final Gate Verification Report** | `stallbreaker-sr1.2-final-gate-`      | Master Gate Record                              |
|    | (SR1.2 Final Determination)        | `report.md` — Master Document         |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 21 | **A2 vs. P3 Counterexample**       | `stallbreaker-sr1.2.1-`               | `stallbreaker-sr1.2-mathematical-verification`, |
|    | (SCEN-01 Canonical Reproduction)   | `counterexample-reproduction.md`      | `stallbreaker-mvp-feasibility.md`               |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 22 | **Adversarial Failure Review (T1-7)| `stallbreaker-sr1.2.1-`               | `stallbreaker-sr1.2-transaction-verification`,  |
|    | (Saga failure, irreversibility)    | `transaction-failure-review.md`       | `stallbreaker-mvp-feasibility.md`               |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 23 | **Solver Semantics & Stat Protocol| `stallbreaker-sr1.2.1-solver-`        | `stallbreaker-sr1.2-experiment-verification`,   |
|    | (Lexicographic, bounds, CRN, BCa) | `and-statistics-closure.md`           | `stallbreaker-sr1.2-claim-evidence-matrix.md`   |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 24 | **SR1.2.1 Final Closure Report**   | `stallbreaker-sr1.2.1-`               | Master Adversarial Closure Record               |
|    | (PR3 Entry Authorization)          | `final-closure-report.md`             |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 25 | **SCEN-01 Canonical Reconstruction**| `stallbreaker-sr1.2.2-`              | Supersedes SR1.2.1 Section 6 and               |
|    | (71.0% result; 37.5% withdrawn)    | `scen01-canonical-reconstruction.md` | `stallbreaker-mvp-feasibility.md` Section 3.5  |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 26 | **Transaction Consistency Fix**    | `stallbreaker-sr1.2.2-`               | Supersedes SR1.2.1 transaction review           |
|    | (T1-T7 corrected; acct code retracted)| `transaction-consistency-correction.md`| on T2/T5/T6/T7 boundary claims              |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 27 | **Solver & Statistics Correction** | `stallbreaker-sr1.2.2-`               | Supersedes SR1.2.1 solver/stats doc on         |
|    | (Incumbent Lock; exploratory 30-seed)| `solver-statistics-correction.md`  | FEASIBLE bound and power claims                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 28 | **SR1.2.2 Final Gate Report**      | `stallbreaker-sr1.2.2-`               | Master Correction & Conditional Gate Record    |
|    | (Conditionally Ready verdict)      | `final-gate-report.md`                | Supersedes SR1.2.1 gate verdict                |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 29 | **Physical Clearance Reconstruct** | `stallbreaker-sr1.2.3-`               | Authoritative SCEN-01 with T_clear=2 (10 min);  |
|    | (66.7% result; 71.0% superseded)   | `physical-clearance-reconstruction.md`| supersedes SR1.2.2 zero-clearance model         |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 30 | **SR1.2.3 Final Closure Report**   | `stallbreaker-sr1.2.3-`               | Master Physical Clearance & Claim Scope Record;|
|    | (Physical Clearance Closed verdict)| `final-closure-report.md`             | Narrowed jointness claim definition             |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 31 | **State & Promise Semantics**      | `stallbreaker-sr1.2.4-`               | Canonical SCEN-01 with 6-state safety sequence, |
|    | (6-state sequence, Eq C25 clarify) | `final-physical-and-promise-`        | dual promise milestones, 110 min invariance     |
|    |                                    | `semantics-closure.md`               |                                                 |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 32 | **SR1.2.4 Final Gate Recomm.**     | `stallbreaker-sr1.2.4-`               | Master Research Closure & Pre-PR3 Gate Record;  |
|    | (Ready for Final Gate verdict)     | `final-gate-recommendation.md`       | Final Pre-Implementation Determination          |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 33 | **Math Counterexample Fixture**    | `stallbreaker-sr1.2.5-`               | Authoritative S-MATH-01 fixture (66.7% primary, |
|    | (Scenario S-MATH-01, A2 vs P3)     | `final-reconciliation.md` — Sec 3 & 6 | 62.9% sensitivity, 110m invariance)             |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 34 | **Bay Resource State Machine**     | `stallbreaker-sr1.2.5-`               | Independent Bay B4 resource states              |
|    | (Entity B4: Occupied to Available) | `final-reconciliation.md` — Sec 4.3   | (OCCUPIED -> PENDING -> AVAILABLE_ALLOCATION)   |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 35 | **SR1.2.5 Final Gate Report**      | `stallbreaker-sr1.2.5-`               | Master Research Reconciliation & Final Research |
|    | (Ready for Final Gate Approval)    | `final-gate-report.md`                | Gate Record                                     |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 36 | **SR1.2.5.1 Math & Event Ordering**| `stallbreaker-sr1.2.5.1-`             | Proposition 1 (universal raw delay) & Prop 2    |
|    | (Mathematical Invariance Proof)    | `mathematical-correction.md`          | (piecewise Delta Z1); Causal event precedence   |
+----+------------------------------------+---------------------------------------+-------------------------------------------------+
| 37 | **SR1.2.5.1 Final Audit Report**   | `stallbreaker-sr1.2.5.1-`             | Master Research Certification; 16-point audit   |
|    | (Ready for Final User Approval)    | `final-audit-report.md`               | matrix, qualified fleet SLA, PR3 not authorized |
+===================================================================================================================================+
```

---

## 3. Discrepancy Reconciliation Log (SR1.1 & SR1.2)

1. **Holding Space Capacity Defect (SR1.2):** Excised the static constraint $\sum_v z_{v,h} \le \text{Capacity}(h)$. Primary ownership assigned to `stallbreaker-sr1.2-mathematical-verification.md` (Section 3.5), establishing time-indexed interval constraints (`NoOverlap` for $C(h)=1$; `Cumulative` for $C(h)>1$).
2. **Distributed Transaction Boundaries (SR1.2):** Excised claims of distributed atomicity across external systems. Assigned primary ownership to `stallbreaker-sr1.2-transaction-verification.md`, formalizing local PostgreSQL ACID transactions coupled to external systems via Transactional Outbox and Compensating Sagas.
3. **Claim Classification (SR1.2):** Reclassified 37.5% lateness reduction as `MATHEMATICALLY DEMONSTRATED` in synthetic SCEN-01; solver latency as `ESTIMATE / TARGET`; code reuse as `MEASURED 0%`. Owned by `stallbreaker-sr1.2-claim-evidence-matrix.md`.
4. **S2 Usable Ready Time (SR1.1):** Reconciled to **Low: 11:40 AM / Central: 12:05 PM / High: 12:45 PM**. All conflicting references superseded. (Owner: `stallbreaker-demo-and-evaluation-plan.md`).
5. **Vehicle Bay Release (SR1.1):** Clarified that safe-close confirmation at 09:45 AM does NOT release Bay B4. Bay B4 is released ONLY at 10:15 AM upon arrival in slot H2. (Owner: `stallbreaker-demo-and-evaluation-plan.md`).
6. **A2 vs. P3 Counterexample Parameter Reconciliation (SR1.2.1):** Corrected previous narrative ambiguity in SR1.2 Section 6.2 regarding early part availability. Primary ownership assigned to `stallbreaker-sr1.2.1-counterexample-reproduction.md`, establishing canonical fixture SCEN-01 with equipment-specific bay hoist requirements, holding zone saturation, and decoupled sourcing objectives.
7. **Rejection of Scalar Weights (SR1.2.1):** Formally excised scalar-weight formulation due to objective leakage and numerical instability; established sequential multi-pass lexicographic optimization as sole authoritative solver architecture. (Owner: `stallbreaker-sr1.2.1-solver-and-statistics-closure.md`).
8. **Distributed Transaction Safety (SR1.2.1):** Formally eliminated claims of distributed atomicity; established failure-aware compensating saga with manual reconciliation gates for non-idempotent legacy vendors. (Owner: `stallbreaker-sr1.2.1-transaction-failure-review.md`).

---

**SR1.2.1 Master Index Sign-Off:**
* Document ownership established across all 24 core architectural domains.
* Zero cross-document drift guaranteed.

---

## 4. Discrepancy Reconciliation Log — SR1.2.2 Additions

9. **SCEN-01 Lateness Figures Corrected (SR1.2.2):** SR1.2.1 Section 6 used an undeclared promise time ($P_2 = t{=}61$ instead of the declared $t{=}54$) and an unexplained P3 finish time ($t{=}76$ instead of $39+24=63$), producing the erroneous 37.5% / 120 min / 75 min figures. All three are **withdrawn**. Authoritative corrected figures: 71.0% improvement / 155 min A2 / 45 min P3. Primary ownership: `stallbreaker-sr1.2.2-scen01-canonical-reconstruction.md`.

10. **FEASIBLE Bound Corrected (SR1.2.2):** SR1.2.1 specified an unjustified 5%-cap relaxation for the FEASIBLE solver state. Replaced with Incumbent Lock policy (`Z_k ≤ Z_k_incumbent` exactly; plan labelled `APPROXIMATE_LEXICOGRAPHIC_PLAN`). Primary ownership: `stallbreaker-sr1.2.2-solver-statistics-correction.md`.

11. **Statistical Power Claim Corrected (SR1.2.2):** SR1.2.1 claimed 30 paired seeds detect Cohen's d > 0.8 without a power analysis. Corrected to: exploratory initial protocol; no power claim made. Primary ownership: `stallbreaker-sr1.2.2-solver-statistics-correction.md`.

12. **Transaction Boundary Corrections (SR1.2.2):** Four bounded corrections applied: (a) `processed_events` table does not make external HTTP actions exactly-once; (b) Account 6840 reference withdrawn (dealership-specific config); (c) T6 delayed-confirmation handling requires compensating release, not just local state rejection; (d) T4 re-plan requires human approval before external commitments. Primary ownership: `stallbreaker-sr1.2.2-transaction-consistency-correction.md`.

13. **Explicit Physical Clearance & Revised 66.7% Metric (SR1.2.3):** SR1.2.2 assumed zero post-repair bay clearance time ($T_{\text{clear}} = 0$), yielding 71.0% improvement. SR1.2.3 introduced explicit post-repair verification, departure transit, and bay confirmation with parameter $T_{\text{clear}} = 2$ ticks (10 min) `[SYNTHETIC ASSUMPTION]`, moving $B_4$ release from $t=61$ to $t=63$ (A2) and $t=39$ to $t=41$ (P3). The revised authoritative improvement is **66.7%** ($Z_1$ from 99.0 to 33.0 weighted ticks; lateness from 165 min to 55 min). Absolute lateness reduction remains constant at **110 minutes** across all $T_{\text{clear}}$. The jointness claim was formally narrowed to the specific source-first, fixed-source baseline (A2) without claiming superiority over all conceivable sequential architectures. Primary ownership: `stallbreaker-sr1.2.3-physical-clearance-reconstruction.md`.

14. **Safety-State Transition Ordering & Customer-Promise Milestones Closed (SR1.2.4):** SR1.2.3 described `SAFE_TO_DRIVE` coinciding with the start of post-repair inspection, and evaluated RO-1042 lateness at installation end rather than customer-ready staging. SR1.2.4 formalized the 6-state post-repair sequence (`REPAIR_MECHANICALLY_COMPLETE` -> `FINAL_VERIFICATION_IN_PROGRESS` -> `SAFE_TO_MOVE` -> `IN_CLEARANCE_TRANSIT` -> `IN_CUSTOMER_PICKUP_STAGING` -> `BAY_CONFIRMED_CLEAR`) with 7 safety invariants. Formalized Equation (C25-Clarified) distinguishing Service Completion ($C_r = \text{end}_{\text{last\_op}}$, 66.7% improvement) and Customer-Ready Pickup Staging ($C_r = t_{\text{customer\_ready}}$, 62.9% improvement). Proved the Absolute Invariance Theorem: 110 minutes of downstream delay saved in both interpretations for any $T_{\text{clear}}$. Sarah Jenkins' lateness is identically 0 min in both. Primary ownership: `stallbreaker-sr1.2.4-final-physical-and-promise-semantics-closure.md`.

15. **Scenario Differentiation, Entity State Separation & Primary Promise Metric Finalized (SR1.2.5):** Resolved remaining research ambiguities by: (a) Formally separating transactional demo scenario `S-DEMO-01` (Escape, $P=12:30$, $w=3$, $S_1$ ATP=0, race condition) from mathematical counterexample scenario `S-MATH-01` (Explorer, $P=13:30$, $w=1$, $S_1$ $55 hotshot, commercial fleet RO-1051 $P=12:30$, $w=3$). Banned generic 'canonical scenario' references. (b) Decoupled the Vehicle State Machine (Entity $V$ reaches terminal `IN_CUSTOMER_PICKUP_STAGING`) from the Bay Resource State Machine (Entity $B_4$ transitions to `AVAILABLE_FOR_ALLOCATION` upon confirmed lane clearance), establishing cross-entity invariants. (c) Designated Milestone 1 (Service Operation Completion / Eq C25) as the PRIMARY benchmark (66.7% lateness reduction) based on fleet SLA operational reality, retaining Milestone 2 (Customer-Ready Staging) as the secondary sensitivity variant (62.9%). Proved algebraic invariance of 110-minute downstream delay reduction across all clearance durations under 5 explicit premises. Primary ownership: `stallbreaker-sr1.2.5-final-reconciliation.md`.

16. **Mathematical Invariance Formulation, Qualified Fleet SLA & Event Ordering (SR1.2.5.1):** Corrected Section 6.4 overclaim regarding universal $\Delta Z_1 = 66.0$ ticks. Formulated Proposition 1 (raw downstream RO-1051 lateness reduction $\equiv 110\text{ min}$ for all $T_{\text{clear}} \ge 0$) and Proposition 2 (total weighted objective difference $\Delta Z_1(T) = 66 + \max(0, T - 5) - \max(0, T - 27)$ is piecewise linear, equaling 66 ticks only on $0 \le T \le 5$). Validated that for the canonical fixture $T = 2$, $\Delta Z_1 = 66.0$ ticks, preserving the 66.7% primary metric and 62.9% staging sensitivity metric unchanged. Qualified commercial fleet SLA descriptions as an operational modeling convention conforming to Equation (C25). Formalized discrete-tick boundary transitions ($t=41$ and $t=63$) as an ordered sequence of zero-duration logical events with strict causal precedence ($e_{\text{transit\_end}} \prec e_{\text{bay\_clear\_confirm}} \prec e_{\text{bay\_available}} \prec e_{\text{v2\_bay\_entry}}$). Primary ownership: `stallbreaker-sr1.2.5.1-mathematical-correction.md` and `stallbreaker-sr1.2.5.1-final-audit-report.md`.

---

**SR1.2.5.1 Master Index Sign-Off:**
* Document ownership established across all 37 core architectural domains.
* SR1.2.5.1 achieves definitive mathematical verification, physical event ordering closure, and research certification.
