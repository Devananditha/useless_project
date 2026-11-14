# PartsRescue PR2: Failure Recovery & Human Approval Design Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `architecture/partsrescue-pr2-failure-and-human-approval-design.md`  
**Phase:** PR2 — Product Opportunity Definition & Technical Architecture Specification  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Design Authority:** Independent Technical Red-Team Reviewer, Enterprise Workflow Automation Engineer  
**Date:** November 14, 2026  

---

## 1. Architectural Philosophy: Resilient Exception Handling

Dealership parts counters operate in high-stress, physically chaotic environments. Software that assumes perfect network conditions, accurate inventory databases, or uninterrupted technician workflows invariably fails.

PartsRescue treats failure as a first-class operational state. The system incorporates:
1. **Deterministic Isolation of 14 Real-World Failure Modes.**
2. **A Decomposed Multi-Factor Confidence Metric** (strictly avoiding opaque, blended confidence percentages).
3. **A Granular, Policy-Gated Human Approval Architecture.**

---

## 2. 14 Operational Failure Modes & Mitigation Matrix

```
+========================================================================================================================+
|                                    14 OPERATIONAL FAILURE MODES MATRIX                                                 |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| #  | Failure Mode          | Detection Mechanism     | System Automated Action | Graceful Fallback & Audit Trail       |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 01 | **Phantom Stock in**  | Counterperson physically| Counterperson clicks    | System updates DMS local inventory to |
|    | **Local DMS Bin**     | checks bin; finds empty | "Bin Empty / Discrepant"| 0; auto-triggers external discovery.   |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 02 | **Connector API**     | Sourcing adapter HTTP   | Request aborts at       | Sourcing drops vendor from round; logs|
|    | **Timeout (>1500ms)** | client timeout trigger  | $t = 1,500 \text{ ms}$  | timeout event; falls back to others.  |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 03 | **Vendor Rate-Limit** | HTTP 429 Too Many Req   | Circuit breaker trips;  | Connector pauses for 60s; serves      |
|    | **(HTTP 429 Error)**  | from external API       | route marked paused     | remaining active channels.            |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 04 | **Supplier Stockout** | Supplier API rejects PO | PO submission error     | Immediate escalation alert in UI;     |
|    | **Post-Quotation**    | during order creation   | event captured          | automatically offers next Pareto rank.|
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 05 | **Fitment DAG Branch**| Multiple successor SKUs | Ambiguity detector flags| UI presents mandatory VIN submodel    |
|    | **Ambiguity**         | without option code match| option divergence       | question to counterperson.            |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 06 | **Split-Pay Order**   | RO line carries both    | Line-level pay-type     | Enforces OEM warranty rule on warranty|
|    | **Line Ambiguity**    | OEM and Customer split  | discriminator           | split; permits choices on CP balance. |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 07 | **Courier Traffic**   | Courier webhook reports | ETA re-calculation      | UI alerts dispatcher; prompts staging |
|    | **Severe Delay**      | delay > 45 minutes      | slips past promise time | of auxiliary job to keep tech billing.|
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 08 | **Freight Fee Surge** | Courier quote exceeds   | Policy threshold gate   | Requires Parts Manager secondary      |
|    | **Over Threshold**    | max dealer limit ($35)  | triggers lock           | electronic PIN authorization.         |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 09 | **Customer Rejects**  | Customer clicks "Decline| Inbound SMS webhook     | Cancels aftermarket sourcing; falls   |
|    | **Aftermarket SMS**   | OEM Alternative" on SMS | receives negative opt-in| back to OEM PDC overnight stock order.|
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 10 | **LLM Rationale**     | Pydantic schema parse   | Validation catches      | System instantly outputs hardcoded    |
|    | **Malformed Output**  | error / invalid JSON    | malformed response      | deterministic mathematical template.  |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 11 | **DMS Network**       | WebSocket keepalive     | Local browser offline   | UI queues approvals in browser IndexedDB|
|    | **Disconnection**     | ping fails              | mode activated          | and synchronizes upon reconnect.      |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 12 | **Tech Clocks Out**   | DMS labor punch event:  | Status change listener  | Courier delivery rerouted to parts    |
|    | **While In-Transit**  | Tech clocked to lunch   | catches idle bay state  | staging shelf; bay flagged for re-work|
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 13 | **Wrong Part Shipped**| Counterperson scans     | Receiving barcode check | Generates immediate courier return tag|
|    | **by Supplier**       | arriving part barcode   | fails OEM SKU match     | and triggers priority re-order.       |
+----+-----------------------+-------------------------+-------------------------+---------------------------------------+
| 14 | **Damaged Part on**   | Counterperson flags     | RMA initiation webhook  | Reverse logistics pickup scheduled;   |
|    | **Physical Delivery** | cracked casting / box   | logged to accounting    | incident logged to vendor scorecard.  |
+========================================================================================================================+
```

---

## 3. Decomposed Multi-Factor Confidence Architecture

A major flaw in naive AI systems is displaying a single blended confidence metric (e.g., *"Confidence: 87%"*). In dealership operations, blending fitment certainty with delivery reliability is unacceptable — a part that is 100% physically fitting but has a 50% delivery chance must not be averaged into a deceptive 75% score.

## 3. Six-Factor Operational Status Architecture (Zero Pseudo-Precision)

A major flaw in naive AI systems is displaying arbitrary floating-point confidence scores (e.g. `confidence = 0.87`). In dealership operations, an arbitrary percentage obscures critical failure risks.

PartsRescue PR2.1 eliminates arbitrary numbers and establishes the **Six-Factor Operational Status Model**:

```
+========================================================================================================================+
|                                    SIX-FACTOR OPERATIONAL STATUS MODEL                                                 |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| #  | Operational Dimension       | Discrete Status Enum        | Concrete Operational Meaning                         |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 01 | **Evidence Completeness**   | `COMPLETE_SPEC`             | All vehicle RPOs, engine codes, and trim options are |
|    |                             | `MISSING_RPO_OPTION`        | matched; or vehicle options are partially ambiguous. |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 02 | **Fitment Verification**    | `VERIFIED_EXACT_MATCH`      | Direct match in OEM catalog; or valid successor in   |
|    |                             | `SUPERSEDED_SUCCESSOR`      | DAG; or requires VIN option clarification.           |
|    |                             | `UNVERIFIED_FITMENT`        |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 03 | **Catalog Source Freshness**| `LIVE_REALTIME_SYNC`        | Master catalog updated today; or batch cache older   |
|    |                             | `CACHED_CATALOG_STALE`      | than 7 days.                                         |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 04 | **Inventory Verification**  | `PHYSICALLY_VERIFIED`       | Counterperson physically pulled bin; or confirmed via|
|    |                             | `REALTIME_API_CONFIRMED`    | real-time API; or unverified overnight batch feed.   |
|    |                             | `UNVERIFIED_BATCH_ESTIMATE` |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 05 | **Logistics Reliability**   | `DEDICATED_SHUTTLE_HIGH`    | In-house parts shuttle; or hotshot courier off-peak; |
|    |                             | `HOTSHOT_COURIER_NORMAL`    | or severe traffic congestion / weather delay risk.   |
|    |                             | `TRAFFIC_CONGESTION_RISK`   |                                                      |
+----+-----------------------------+-----------------------------+------------------------------------------------------+
| 06 | **Policy Eligibility**      | `VERIFIED_ELIGIBLE`         | Direct policy match; or conditional on TSB waiver;   |
|    |                             | `CONDITIONAL_TSB_WAIVER`    | or human warranty review required.                   |
|    |                             | `HUMAN_REVIEW_REQUIRED`     |                                                      |
+========================================================================================================================+
```

---

## 4. Human Approval Workflow & Spending Thresholds

PartsRescue operates on a **Zero-Execution Agency** model. No financial purchase order is transmitted to an external supplier without explicit human sign-off.

### 4.1 Policy-Based Approval Thresholds
```
+========================================================================================================================+
|                                    POLICY-BASED APPROVAL THRESHOLDS                                                    |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Transaction Scope        | Expense Range         | Authorized Persona  | UI Approval Mechanism                         |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Standard Local Sourcing  | Freight $\le \$35.00$  | Parts Counterperson | 1-Click "Approve & Dispatch" button           |
|                          | Part Price $\le$ List |                     |                                               |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Premium Expedited Freight| Freight $> \$35.00$   | Parts Manager       | Requires Manager 4-Digit Security PIN         |
|                          | or Distance $> 25$ mi |                     |                                               |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Aftermarket Substitution | Any Cost              | Service Advisor     | Checkbox confirming: "Customer approved via   |
| on Customer-Pay RO       |                       |                     | SMS / Phone call."                            |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| Emergency VOR PDC Air    | Freight $> \$75.00$   | Fixed Operations    | Dual sign-off: Parts Manager + Service Mgr    |
| Order (OEM Factory)      |                       | Director            |                                               |
+========================================================================================================================+
```

### 4.2 Immutable Audit Trail
Every approval is captured with an unalterable audit log entry:
```json
{
  "audit_event_id": "aud_10842-882b",
  "timestamp": "2026-11-14T10:18:04Z",
  "repair_order_id": "RO-104928",
  "part_sku": "BRK-44021",
  "selected_source": "Metro Sister-Store #4",
  "approved_by_user_id": "USR-COUNTER-04",
  "user_ip_address": "192.168.4.112",
  "freight_approved": 28.00,
  "net_labor_hours_preserved": 3.0,
  "manager_override_pin_used": false,
  "cryptographic_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

## 5. Verification & Traceability
- Addresses real-world dealership failure points documented in Phase PR1 field interviews.
- Guarantees complete warranty and accounting compliance via clear human-in-the-loop gates.
- Prevents misleading probabilistic confidence scores through factor decomposition.
