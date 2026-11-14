# StallBreaker: SR1.2.1 Transaction Failure & Adversarial Outbox Saga Review

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.1-transaction-failure-review.md`  
**Phase:** StallBreaker Transition Evaluation — Final Adversarial Closure Review SR1.2.1  
**Standard Compliance:** Fully compliant with `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Board Authority:** Distributed Systems Architect, Enterprise Software Architect, SaaS Reliability Engineer  
**Date:** November 14, 2026  
**Classification:** SYSTEM ARCHITECTURE AUDIT & RESIDUAL RISK SPECIFICATION  

---

## 1. Executive Summary: Dismantling Imaginary Distributed Atomicity

A persistent danger in hackathon architecture proposals is the conflation of **local ACID database transactions** with **distributed cross-enterprise atomicity**. 

In automotive retail, a software platform must interact with:
1. Internal Dealership Management Systems (DMS) — e.g., Tekion ARC.
2. OEM National Parts Depots — proprietary batch/REST APIs with variable response times.
3. Independent Wholesale Parts Distributors (e.g., AutoZone Pro, Worldpac) — external commerce portals with varied idempotency semantics.
4. Third-Party On-Demand Couriers (e.g., Curri, Roadie) — physical logistics dispatch with dispatch-fee irreversibility.

> **Definitive Architectural Principle:**  
> StallBreaker **CANNOT** guarantee atomic distributed transactions across these external entities. A Two-Phase Commit (2PC / XA) protocol across independent external parts jobbers does not exist and cannot be built. Any claim of "unconditional distributed safety" is mathematically and operationally false.
>
> StallBreaker's true architecture is an **event-driven, failure-aware, auditable compensating saga**. It provides **at-least-once outbox delivery with idempotent processing** internally, coupled with **deterministic timeout bounding, status reconciliation probes, and bounded human escalation** for external failures.

---

## 2. Comprehensive Adversarial Failure Scenario Matrix (T1 – T7)

```
+===================================================================================================================================+
|                                    ADVERSARIAL DISTRIBUTED FAILURE MATRIX (SCENARIOS T1 - T7)                                     |
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| ID | Failure Trigger      | External Boundary State   | StallBreaker State Transition     | Deterministic System Action & Recovery|
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T1 | Lost Response After  | Supplier processed and    | `REQUESTED` ->                    | Client-side lease query using opaque  |
|    | Sourcing Commit      | reserved part; network dropped| `AMBIGUOUS_RETRY_PENDING`     | idempotency key; status inquiry probe.|
|    |                      | response before receipt.  |                                   | If unresolvable within 30s -> ESCALATE|
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T2 | Non-Idempotent Vendor| Supplier API does NOT     | `REQUESTED` ->                    | BLIND RETRIES STRICTLY FORBIDDEN.     |
|    | Network Timeout      | accept idempotency keys;  | `REQUIRES_MANUAL_RECONCILIATION`  | Outbox halts automated POST. Alert to |
|    |                      | blind retry risks 2x order|                                   | Parts Counterperson with phone/PO info|
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T3 | Compensation Request | Reservation succeeded;    | `COMPENSATION_REQUESTED` ->       | Exponential backoff retry (3 attempts)|
|    | Network / API Failure| schedule commit aborted;  | `COMPENSATION_FAILED_DEAD_LETTER` | If exhausted: DLQ event + high-sev    |
|    |                      | release call fails (500). |                                   | alert: `CRITICAL_INVENTORY_ORPHAN`.   |
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T4 | Post-Commit Supplier | Schedule committed;       | `CONFIRMED` ->                    | Invalidate schedule version; retain   |
|    | Revocation           | vendor cancels lease or   | `INVALIDATED_SUPPLIER_REVOCATION` | vehicle bay lock; trigger CP-SAT      |
|    |                      | courier suffers breakdown.|                                   | re-solve; alert Service Dispatcher.   |
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T5 | Duplicate Outbox     | Message broker redelivers | `DUPLICATE_DETECTED_DROPPED`      | Idempotent consumer DB table with     |
|    | Message Delivery     | order event after worker  | (State remains unchanged)         | unique constraint on (outbox_id, step)|
|    |                      | crash/restart.            |                                   | Duplicate payload dropped silently.   |
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T6 | Out-of-Order Event   | Delayed `CONFIRMED` event | `EVENT_STALE_DROPPED`             | Monotonic version vector & terminal   |
|    | Arrival              | arrives AFTER `REVOKED`   | (State remains `REVOKED`)         | state lock. Terminal states cannot be |
|    |                      | or `EXPIRED` transition.  |                                   | overwritten by older event timestamps.|
+----+----------------------+---------------------------+-----------------------------------+---------------------------------------+
| T7 | Irreversible Action  | Courier already in transit| `COMPENSATION_IMPOSSIBLE` ->      | Acknowledge sunk logistics expense.   |
|    | (Shipped / In Flight)| when schedule cancels;    | `SUNK_EXPENSE_UNRECOVERABLE`      | Route arriving part to shop inventory;|
|    |                      | freight fee cannot refund.|                                   | re-release bay without waiting.       |
+===================================================================================================================================+
```

---

## 3. Detailed Failure Scenario Protocols

### Scenario T1: Lost Response After Supplier Processing
* **Physical Reality:** StallBreaker dispatches `POST /v1/reservations` to a parts supplier adapter. The supplier creates the reservation with a 10-minute lease token. Before the HTTP 200 response reaches StallBreaker's gateway, the connection drops or times out (HTTP 504).
* **Vulnerability:** If StallBreaker treats this as an outright failure, it will abandon the reservation while the supplier holds inventory; if StallBreaker immediately retries, it might create an unnecessary second hold.
* **Protocol & Recovery:**
  1. Transition state from `REQUESTED` to `AMBIGUOUS_RETRY_PENDING`.
  2. Outbox background worker executes a **Reconciliation Probe**: `GET /v1/reservations/status?client_request_id={uuid}` using the deterministic client-generated UUID.
  3. *Branch A (Probe succeeds, reservation exists):* Update state to `CONFIRMED`, record `lease_token` and `lease_expires_at`, resume saga.
  4. *Branch B (Probe confirms not found):* Safely issue fresh reservation request.
  5. *Branch C (Probe times out or endpoint unavailable):* After 30 seconds of ambiguity, transition to `MANUAL_RECONCILIATION_REQUIRED` and alert parts specialist.

---

### Scenario T2: Supplier Lacks Idempotency Support
* **Physical Reality:** Many legacy dealership vendors and automotive parts wholesalers maintain legacy SOAP or REST interfaces that ignore HTTP `Idempotency-Key` headers. Submitting a second `POST` with the same purchase order number results in two distinct warehouse pick tickets and duplicate financial charges.
* **Mandatory Behavioral Rule:**
  > **StallBreaker STOPS all automated network retries on mutating endpoints for non-idempotent adapters.**
* **Protocol & Recovery:**
  1. The adapter registry flags each supplier as `IdempotencySupported: TRUE | FALSE`.
  2. If a network timeout or connection reset occurs against an adapter with `IdempotencySupported == FALSE`, the outbox processor **MUST NOT RETRY**.
  3. System transitions reservation state immediately to `REQUIRES_MANUAL_RECONCILIATION`.
  4. The UI displays an actionable modal to the Parts Counterperson:
     * Supplier Name and Phone Number.
     * Timestamp of dispatched request and exact part SKU.
     * Two human action buttons: `[Confirm Order Created Externally]` (enters token manually) or `[Abort & Select Alternative]`.

---

### Scenario T3: Compensation Failure
* **Physical Reality:** A parts lease was granted, but the downstream schedule commit failed (e.g., DMS database lock conflict or conflicting technician assignment). StallBreaker attempts to roll back by sending `DELETE /v1/reservations/{token}` to release the inventory hold, but the supplier endpoint returns HTTP 500 Internal Server Error.
* **Vulnerability:** Unreleased inventory leaves the supplier holding parts unnecessarily, straining dealership relationships or incurring restocking penalties.
* **Protocol & Recovery:**
  1. Transition reservation state to `COMPENSATION_REQUESTED`.
  2. Outbox initiates exponential backoff retries: Attempt 1 at $t=5\text{s}$, Attempt 2 at $t=15\text{s}$, Attempt 3 at $t=45\text{s}$ (with $\pm 20\%$ jitter).
  3. If Attempt 3 fails, transition state to `COMPENSATION_FAILED_DEAD_LETTER`.
  4. Write compensation event to PostgreSQL Dead-Letter Queue (DLQ).
  5. Emit high-severity operational notification: `CRITICAL_INVENTORY_ORPHAN`.
  6. Parts Manager dashboard highlights orphaned PO with one-click phone dialer or direct manual release acknowledgment.

---

### Scenario T4: Supplier Revocation After Local Schedule Commit
* **Physical Reality:** StallBreaker confirmed the lease, validated the schedule, and committed the multi-bay plan to the DMS. Five minutes later, the supplier sends a webhook or status callback: `ORDER_CANCELLED_STOCKOUT` (e.g., physical bin count discrepancy, or hotshot courier vehicle broke down).
* **Vulnerability:** Naive automated systems might abruptly eject the vehicle from the bay or leave technician schedules in an invalid state, causing bay gridlock.
* **Protocol & Recovery:**
  1. Webhook handler logs event and immediately marks the active schedule version as `INVALIDATED_SUPPLIER_REVOCATION`.
  2. **Bay Protection Lock Enforced:** The physical bay assignment for the affected vehicle is **STRICTLY PRESERVED**. The vehicle is *never* automatically moved to holding or relocated without a verified replacement plan.
  3. Operation status transitions to `BLOCKED_AWAITING_RECOVERY`.
  4. **Automated Re-Solve Trigger:** The CP-SAT solver is immediately queued in background with:
     * Candidate set $\mathcal{S}_{\text{new}} = \mathcal{S} \setminus \{s_{\text{revoked}}\}$.
     * Current vehicle locations pinned to physical reality ($c_{v,b} = \text{current}$).
  5. **Anti-Thrashing Circuit Breaker:** If $\ge 2$ supplier revocations occur on the same Repair Order within 30 minutes, automated re-planning halts, and the job transitions to `MANUAL_DISPATCH_REQUIRED`.

---

### Scenario T5: Duplicate Outbox Delivery
* **Physical Reality:** The outbox worker reads an event `RESERVE_PART_REQ`, sends the HTTP request to the supplier, but crashes right before executing `UPDATE outbox_events SET status = 'PROCESSED'`. Upon daemon restart, the new worker picks up the same pending event and attempts to resend.
* **Protocol & Recovery:**
  1. Outbox table enforces an **At-Least-Once Delivery** model.
  2. Every outbox event has a deterministic UUID: `event_id`.
  3. Local event consumers log execution into a `processed_events` table within the same ACID transaction:
     ```sql
     INSERT INTO processed_events (event_id, consumer_id, processed_at)
     VALUES ($1, 'outbox_dispatcher', NOW())
     ON CONFLICT (event_id, consumer_id) DO NOTHING;
     ```
  4. If conflict detected, message processing is skipped (`DUPLICATE_DETECTED_DROPPED`).
  5. External HTTP calls inject `X-StallBreaker-Idempotency-Key: {event_id}` into headers to enable remote de-duplication on modern supplier endpoints.

---

### Scenario T6: Out-of-Order Event Delivery
* **Physical Reality:** Due to asynchronous network routing, a lease timeout event (`LEASE_EXPIRED`) is processed at $t=60\text{s}$, transitioning the state to `EXPIRED`. At $t=62\text{s}$, a severely delayed supplier confirmation packet (`200 OK`) arrives from the original request.
* **Protocol & Recovery:**
  1. Every reservation entity maintains a monotonic version sequence `state_version` and state precedence rules.
  2. **State Machine Precedence Hierarchy:**
     $$\text{TERMINAL} \in \{\text{CANCELLED}, \text{EXPIRED}, \text{REVOKED}, \text{RESTOCKED}\} \succ \text{CONFIRMED} \succ \text{REQUESTED} \succ \text{NONE}$$
  3. A state transition can *never* move backwards against the precedence hierarchy.
  4. When the delayed `CONFIRMED` packet arrives:
     * System checks `current_state`.
     * `current_state == EXPIRED` $\implies$ Event is rejected as stale (`EVENT_STALE_DROPPED`).
     * System immediately fires compensating release `DELETE /v1/reservations/{token}` to ensure the supplier does not maintain an orphan hold.

---

### Scenario T7: Irreversible External Actions
* **Physical Reality:** An expedited third-party courier ($S_1$) was dispatched at 10:15 AM (fee: \$55.00). At 10:30 AM, customer Sarah Jenkins calls and cancels the repair. 
* **The Irreversibility Truth:**
  > **A moving courier van cannot be rolled back via an API call.** The \$55.00 courier fee is sunk and non-refundable.
* **Protocol & Recovery:**
  1. The saga marks the cancellation compensation as `COMPENSATION_IMPOSSIBLE_ACTION_IRREVERSIBLE`.
  2. Financial state transitions to `SUNK_EXPENSE_UNRECOVERABLE` with an accounting ledger debit to Account 6840 (Shop Policy / Dispatch Loss).
  3. Physical workflow: When the courier arrives at the dealership, the receiving parts clerk scans the barcode. The DMS directs the part to:
     * General Shelf Stocking (`RESTOCKED_TO_INVENTORY`), or
     * Direct Cross-Dock to another active RO requiring the same SKU.
  4. Bay $B_4$ is immediately freed for downstream alignment work without waiting for courier arrival.

---

## 4. Architectural Boundaries & Guarantees

```
+===================================================================================================================================+
|                                             SYSTEM BOUNDARY GUARANTEE SPECIFICATION                                              |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Architectural Layer               | True Technical Guarantee              | Explicit Limitation (What is NOT Guaranteed)          |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Local PostgreSQL Database         | Strict ACID Atomicity                 | Does not extend beyond the local database boundary.   |
|                                   | (Serializable isolation level)        |                                                       |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Transactional Outbox              | At-Least-Once Delivery                | Does NOT provide exactly-once delivery without        |
|                                   | (Guaranteed local persist before send)| idempotent consumer de-duplication.                   |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Modern Supplier Adapters          | Idempotent Request Processing         | Relies on external vendor adhering to standard        |
|                                   | (via Idempotency-Key headers)         | token caching specs; vendor downtime breaks contract. |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Legacy Wholesale Adapters         | Non-Idempotent (At-Most-Once Attempt) | Blind retries strictly prohibited. Automatic retry    |
|                                   |                                       | safety is impossible; human escalation required.      |
+-----------------------------------+---------------------------------------+-------------------------------------------------------+
| Physical Courier Dispatch         | Irreversible Real-World Action        | Cannot be rolled back. Sunk freight expenses cannot   |
|                                   |                                       | be recovered via compensation sagas.                  |
+===================================================================================================================================+
```

---

## 5. Residual Risks That Cannot Be Eliminated

1. **Unilateral Supplier Phantom Delays:** A supplier confirms an ETA of 11:30 AM, but internal courier traffic causes arrival at 13:30 PM without API warning. *Residual Risk: Bay blockage occurs despite optimal mathematical planning.*
2. **Dealer Network Part Mislabeling:** A physical bin contains the wrong part variant despite 100% catalog match. *Residual Risk: Part arrives on time but fails physical bench check.*
3. **External Jobber API Total Outage:** Wholesaler system crashes mid-transaction without status lookup capability. *Residual Risk: Requires manual phone call by parts counterperson.*

---

## 6. Audit Conclusion & Sign-Off

The transactional protocol of StallBreaker is **rigorously defined, failure-aware, and defensible**. By eliminating false claims of distributed atomicity and substituting a battle-hardened outbox saga with explicit manual reconciliation gates, the architecture meets enterprise SaaS standards.

$$\mathbf{WORKSTREAM\ 2\ VERDICT:\ TRANSACTIONALLY\ DEFENSIBLE\ —\ RESIDUAL\ RISKS\ BOUNDED}$$
