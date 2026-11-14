# PartsRescue PR2.1: Performance Target & Confidence Metric Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-performance-confidence-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** AI Systems Architect, Technical Red-Team Reviewer  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Mandate

In Phase PR2, specifications across `architecture/partsrescue-pr2-failure-and-human-approval-design.md` and `evaluation/partsrescue-pr2-acceptance-criteria.md` introduced precise numerical figures for latency, throughput, and confidence:
* *"Solver executes in $< 5 \text{ ms}$."*
* *"End-to-end triage card latency $p_{95} < 250 \text{ ms}$."*
* *"Orchestrator timeout $\le 1,500 \text{ ms}$."*
* *"Inventory confidence $\Gamma_{\text{inv}} \in [0.70, 0.99]$."*
* *"Logistics confidence $\Gamma_{\text{log}} \in [0.60, 0.95]$."*
* *"Binary Fitment Certainty $\Gamma_{\text{fit}} \in \{0, 1\}$."*

In accordance with `.cursor/rules/research-standards.mdc`, this audit confronts these numbers. **None of these values represent measured production empirical data.** Presenting design aspirations or mathematical upper bounds as validated operational truths damages the technical credibility of the hackathon submission.

---

## 2. Rigorous Performance Claim Classification

```
+=================================================================================================================================+
|                                            PERFORMANCE CLAIM AUDIT MATRIX                                                       |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| #  | Metric & Stated Value | PR2 Description     | Audit Class       | Technical Reality & Defensible Status                    |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 01 | **Pareto Solver**     | Executed in         | **PROPOSED        | *Reality:* In-memory vector comparison on $K \le 8$ takes|
|    | **$< 5 \text{ ms}$**  | $< 5 \text{ ms}$    | **TARGET**        | microseconds in Python/C, but has not been benchmarked  |
|    |                       | (Stated as fact)    |                   | under concurrent server load. Classify as Target.        |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 02 | **End-to-End Latency**| $p_{95} < 250 \text{ ms}$| **UNSUPPORTED | *Reality:* Outbound HTTP queries to 3 external vendors   |
|    | **$< 250 \text{ ms}$**| (Webhook to UI)     | **CLAIM**         | and an LLM NLP call cannot physically complete in 250ms  |
|    |                       |                     |                   | over the public Internet. Strike and correct to realistic.|
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 03 | **LLM Orchestrator**  | 1,500 ms hard limit | **PROPOSED        | *Reality:* Commercial LLM API p95 latencies range from   |
|    | **1,500 ms Timeout**  | before fallback     | **TARGET**        | 800ms to 2,200ms. 1,500ms is a reasonable SLA budget     |
|    |                       |                     |                   | trigger for fallback, but must be labeled as a Target.   |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 04 | **Inventory Confidence**| Scaled 0.70 to 0.99 | **ILLUSTRATIVE    | *Reality:* The numerical bounds (0.70, 0.85, 0.99) were  |
|    | **0.70 – 0.99**       | based on channel    | **ASSUMPTION**    | subjective heuristics without statistical calibration.   |
|    |                       |                     |                   | Reframe as discrete qualitative states.                  |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 05 | **Logistics Confidence**| Scaled 0.60 to 0.95 | **ILLUSTRATIVE    | *Reality:* Traffic and courier telematics were not       |
|    | **0.60 – 0.95**       | based on distance   | **ASSUMPTION**    | empirically trained on municipal GPS datasets.          |
|    |                       |                     |                   | Reframe as discrete qualitative states.                  |
+----+-----------------------+---------------------+-------------------+----------------------------------------------------------+
| 06 | **100% Deterministic**| 0% Hallucination in | **REQUIREMENT     | *Reality:* Code logic is deterministic, but catalog data |
|    | **Fitment Match**     | mechanical fitment  | **TARGET**        | itself can contain errors, missing RPOs, or bad mapping. |
|    |                       |                     |                   | Reframe around explicit catalog evidence completeness.   |
+=================================================================================================================================+
```

---

## 3. Dissecting the Latency Stack (Realistic Budgeting)

Claiming a $250 \text{ ms}$ end-to-end response time while orchestrating external commercial suppliers and an LLM is technically impossible. Below is the **Realistic Latency Budget Breakdown**:

```
+========================================================================================================================+
|                                    REALISTIC LATENCY BUDGET BREAKDOWN                                                  |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| #  | Pipeline Stage Component             | Realistic Latency Range | Engineering Mitigation Strategy                  |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 01 | Ingress Webhook & Auth Verification  | $20 - 50 \text{ ms}$    | Local JWT HMAC-SHA256 verification.              |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 02 | Local DMS Inventory & RO Context Read| $30 - 80 \text{ ms}$    | Indexed PostgreSQL / Redis cache query.          |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 03 | Deterministic DAG & Warranty Filter  | $10 - 25 \text{ ms}$    | In-memory graph traversal.                       |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 04 | Parallel Sourcing Fan-Out (3 Vendors)| $400 - 1,200 \text{ ms}$| Asynchronous HTTP client with 1,500ms cutoff.    |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 05 | Discrete Vector Pareto Solver        | $< 5 \text{ ms}$        | In-memory pure mathematical calculation.         |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 06 | LLM Trade-Off Rationale Synthesizer  | $600 - 1,800 \text{ ms}$| Gemini 2.5 Flash / Fast LLM API call.            |
|    | *(Or Deterministic Template Fallback)*| ($< 1 \text{ ms}$)      | (Bypassed if timeout exceeds 1,500ms budget).    |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| 07 | WebSocket Action Card Push to UI     | $20 - 50 \text{ ms}$    | Secure WebSocket broadcast to active client.     |
+----+--------------------------------------+-------------------------+--------------------------------------------------+
| **TOTAL** | **Realistic End-to-End Latency** | **$1.2 - 2.5 \text{ s}$**| **Honest, defensible operational UX budget.**    |
+========================================================================================================================+
```

**Architectural Correction:** The end-to-end triage card SLA target is formally corrected from $250 \text{ ms}$ to **$< 2.5 \text{ seconds}$** (or $< 1.2 \text{ seconds}$ when using deterministic rationale templates).

---

## 4. Reassessing the Confidence Model: Qualitative Transparency vs. Arbitrary Numbers

### 4.1 The Danger of Pseudo-Mathematical Confidence
Assigning arbitrary floating-point numbers like `confidence = 0.87` gives dealership users a false sense of scientific precision without empirical training. In automotive operations, a counterperson does not know what an "87% confident part" means.

### 4.2 The Six-Factor Transparent Status Model
PartsRescue PR2.1 eliminates arbitrary numerical scores and establishes the **Six-Factor Operational Status Model**:

```
+========================================================================================================================+
|                                    SIX-FACTOR OPERATIONAL STATUS MODEL                                                 |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| #  | Operational Factor          | Discrete Status Values      | Definitive Operational Meaning                       |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 01 | **Evidence Completeness**   | `COMPLETE_SPEC`             | All vehicle RPOs, engine codes, and trim options are |
|    |                             | `MISSING_RPO_OPTION`        | matched; or vehicle options are partially ambiguous. |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 02 | **Fitment Verification**    | `VERIFIED_EXACT_MATCH`      | Direct match against OEM catalog; or valid successor |
|    |                             | `SUPERSEDED_SUCCESSOR`      | in DAG; or requires VIN option clarification.        |
|    |                             | `UNVERIFIED_FITMENT`        |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 03 | **Catalog Source Freshness**| `LIVE_REALTIME_SYNC`        | Master catalog updated today; or batch cache older   |
|    |                             | `CACHED_CATALOG_STALE`      | than 7 days.                                         |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 04 | **Inventory Verification**  | `PHYSICALLY_VERIFIED`       | Counterperson confirmed bin; or live API quote;      |
|    |                             | `REALTIME_API_CONFIRMED`    | or unverified overnight batch feed.                  |
|    |                             | `UNVERIFIED_BATCH_ESTIMATE` |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 05 | **Logistics Reliability**   | `DEDICATED_SHUTTLE_HIGH`    | In-house driver; or hotshot courier off-peak;        |
|    |                             | `HOTSHOT_COURIER_NORMAL`    | or severe traffic congestion / adverse weather risk. |
|    |                             | `TRAFFIC_CONGESTION_RISK`   |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 06 | **Policy Eligibility**      | `VERIFIED_ELIGIBLE`         | Direct policy match; or conditional on TSB waiver;   |
|    |                             | `CONDITIONAL_TSB_WAIVER`    | or human warranty review required.                   |
|    |                             | `HUMAN_REVIEW_REQUIRED`     |                                                      |
+========================================================================================================================+
```

---

## 5. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Mandatory Modifications Across PR2 Documents:**
  * Update `architecture/partsrescue-pr2-failure-and-human-approval-design.md`: Replace floating-point confidence multipliers ($\Gamma$) with the Six-Factor Operational Status Model.
  * Update `evaluation/partsrescue-pr2-acceptance-criteria.md`: Revise unrealistic latency targets from $p_{95} < 250 \text{ ms}$ to an honest end-to-end target of $< 2.5 \text{ seconds}$.
  * Update `evaluation/partsrescue-pr2-final-report.md`: Reflect the realistic latency stack and transparent status architecture.
