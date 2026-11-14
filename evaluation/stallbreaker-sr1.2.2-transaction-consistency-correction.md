# StallBreaker: SR1.2.2 — Transaction Consistency Correction

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/stallbreaker-sr1.2.2-transaction-consistency-correction.md`  
**Phase:** SR1.2.2 — Consistency Correction and Final Gate Audit  
**Standard Compliance:** `AGENTS.md`, `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Board:** Distributed Systems Architect, Automotive Dealership Operations Specialist  
**Date:** November 14, 2026  

---

## 1. Fundamental Principle (Unchanged)

StallBreaker does **not** claim atomic distributed transactions across independent external systems. The correct characterisation remains:

- **Local guarantee:** Strict ACID atomicity within the PostgreSQL database boundary (reservation records, outbox entries, schedule versions, audit logs written in one local transaction).
- **External guarantee:** At-least-once outbox delivery to an external HTTP endpoint, combined with idempotent local consumer processing. This does **not** make external HTTP calls exactly-once.
- **Cross-boundary guarantee:** None. External supplier state must be queried or reconciled; it cannot be assumed to match local state.

---

## 2. Corrected Failure Scenario Matrix (T1 – T7)

### T1 — Supplier Processes Request; Response Lost

| Field | Detail |
| :--- | :--- |
| **Trigger** | StallBreaker dispatches `POST /v1/reservations` with client-generated idempotency UUID. Supplier creates reservation; network drops before response arrives. |
| **External state** | Supplier holds a confirmed reservation for the requested part. |
| **Local state** | Reservation record in `REQUESTED`; no `lease_token` stored. |
| **Guarantee** | Local database is consistent (outbox record persisted). External state is **unknown**. |
| **Recovery** | Outbox worker issues a reconciliation probe: `GET /v1/reservations/status?client_request_id={uuid}`. If supplier supports status lookup: (a) reservation confirmed → store token, advance to `CONFIRMED`; (b) not found → safe to retry the POST; (c) endpoint unavailable → transition to `AMBIGUOUS_PENDING`, alert parts specialist within 30 s. |
| **Idempotency** | Local: idempotent (UUID deduplicated). External: depends on supplier. |
| **Human action** | Required if probe timeout or probe endpoint unavailable after 30 s. |
| **Residual risk** | Supplier that does not support status lookup and silently processed the request → inventory may be held without a local lease token. Human must phone-verify. |

---

### T2 — Supplier Lacks Idempotency Support

| Field | Detail |
| :--- | :--- |
| **Trigger** | A network timeout occurs on a `POST` to a supplier whose API does not accept `Idempotency-Key` headers and cannot be probed for prior-request status. |
| **External state** | Unknown. The supplier may or may not have processed the first request. |
| **Local state** | Reservation in `REQUESTED`. |
| **Guarantee** | Local state is consistent. External state is indeterminate. Automated retries **must not** be issued; each retry risks creating a duplicate purchase order and duplicate financial charge. |
| **Recovery** | Outbox halts all further automated POSTs to this endpoint. Reservation transitions to `REQUIRES_MANUAL_RECONCILIATION`. Parts Counterperson receives an alert with supplier phone number, PO reference, part SKU, and two explicit actions: **Confirm Order Created** (enter lease token manually) or **Abort and Re-select Source**. |
| **Idempotency** | Local: guaranteed. External: **unavailable**. |
| **Human action** | **Always required.** System must not proceed without human confirmation of external state. |
| **Residual risk** | Until human confirms, the reservation state is indeterminate. Bay plan may need to hold without committing a supplier. |

---

### T3 — Compensation Failure

| Field | Detail |
| :--- | :--- |
| **Trigger** | A reservation was created at the supplier. The local schedule commit fails (e.g., concurrent bay conflict). StallBreaker attempts to release the reservation (`DELETE /v1/reservations/{token}`) but receives HTTP 500. |
| **External state** | Supplier still holds the inventory reservation. |
| **Local state** | Reservation is in `COMPENSATION_REQUESTED`. |
| **Guarantee** | Local database records the compensation attempt and all retry outcomes. The supplier-side reservation is NOT confirmed as released until the supplier responds with 2xx. |
| **Recovery** | Exponential backoff: attempt 1 at $t{+}5s$, attempt 2 at $t{+}15s$, attempt 3 at $t{+}45s$ (±20% jitter). After exhaustion: (a) outbox writes event to PostgreSQL Dead-Letter Queue (DLQ) with full context; (b) reservation local state transitions to `COMPENSATION_FAILED_DEAD_LETTER`; (c) high-severity alert `CRITICAL_INVENTORY_ORPHAN` is raised. Parts Manager must manually phone the supplier and log the outcome. |
| **Idempotency** | Local DLQ write: idempotent. External release: not confirmed. |
| **Human action** | **Required.** DLQ is a record of unresolved work, not proof of reversal. The Parts Manager must confirm external release and update the reservation record to `CANCELLED_MANUALLY_CONFIRMED` once the supplier confirms. |
| **Residual risk** | Until manual confirmation, supplier holds inventory StallBreaker is not using. Orphaned holds may incur restocking penalties. |

---

### T4 — Supplier Revocation After Local Schedule Commit

| Field | Detail |
| :--- | :--- |
| **Trigger** | A supplier posts a webhook or status callback `ORDER_CANCELLED_STOCKOUT` or similar after StallBreaker has committed the shop schedule to the DMS. |
| **External state** | Supplier has cancelled the reservation; they no longer hold the part. |
| **Local state** | Active schedule version exists; reservation was `CONFIRMED`. |
| **Guarantee** | Local schedule version is marked `INVALIDATED`. The vehicle's current physical bay assignment is **preserved** in the local record (see below). No automatic vehicle move is triggered. |
| **Recovery — explicit steps:** | |
| 1. Vehicle bay | Physical bay assignment record is **not changed**. The vehicle remains where it physically is. No automatic ejection from bay. |
| 2. Existing technician work | Any in-progress work (e.g., disassembly already performed) is noted in the RO status; no automated reversal. |
| 3. Supplier reservation | Marked `REVOKED` locally. A compensating release is **not** issued (supplier already revoked). |
| 4. Recovery plan | CP-SAT solver re-queued with the revoked source removed from the candidate set. Bay lock for the affected vehicle is retained during re-solve. |
| 5. Human approval | Re-plan is a **proposed** plan. Human dispatcher must approve before any new external commitments are made. |
| 6. Anti-thrashing | If $\ge 2$ revocations on the same RO within 30 minutes, automated re-planning halts; job transitions to `MANUAL_DISPATCH_REQUIRED`. |
| **Human action** | Required to approve new plan and confirm vehicle can proceed safely given current physical state. Preserving a bay lock does **not** restore supplier inventory; a new source must be found and reserved. |
| **Residual risk** | No new part may be available. Vehicle may remain in bay without a part for an extended period. Customer SLA breach is possible regardless of recovery plan. |

---

### T5 — Duplicate Outbox Message Delivery

| Field | Detail |
| :--- | :--- |
| **Trigger** | Outbox worker dispatches `POST` to supplier, receives 200, crashes before marking the outbox event processed. Worker restarts and re-delivers the same event. |
| **External state** | The supplier has already processed the first POST. |
| **Local state** | Outbox event record is still `PENDING` (not yet marked processed). |
| **What the local `processed_events` table guarantees:** | It prevents the **local consumer** from performing duplicate local side-effects (e.g., re-writing the schedule, re-recording the lease). It does **not** prevent the duplicate external HTTP POST from being issued. |
| **What it does NOT guarantee:** | External idempotency. The second HTTP POST is transmitted to the supplier before the local consumer uniqueness check runs. If the supplier does not support `Idempotency-Key`, a duplicate purchase order may be created externally. |
| **Correct semantics:** | (a) Modern supplier adapters (`IdempotencySupported: TRUE`): inject `X-StallBreaker-Idempotency-Key: {event_id}` in every POST; supplier de-duplicates on its side. Result: at-most-one external side-effect. (b) Legacy supplier adapters (`IdempotencySupported: FALSE`): duplicate external POST is a real risk. The outbox must implement **at-most-once** semantics for these adapters: mark the event processed *before* sending (using local DB lock), accept that if the send fails the event is permanently lost (not retried), and require human confirmation. |
| **Idempotency** | Local consumer: guaranteed by `processed_events` unique constraint. External: depends on supplier adapter class. |
| **Human action** | Required for legacy adapters on any network failure after a first successful dispatch. |
| **Residual risk** | For legacy adapters, duplicate external POs remain a risk on worker crash-between-send-and-commit. This is a known limitation of at-least-once outbox patterns with non-idempotent endpoints. |

---

### T6 — Out-of-Order or Delayed Event Arrival

**Sub-case A: Delayed supplier confirmation arriving after local lease expiry**

| Field | Detail |
| :--- | :--- |
| **Trigger** | StallBreaker marks a reservation `EXPIRED` (local lease timer fired at $t{=}600s$). At $t{=}620s$, a delayed 200 OK with a lease token arrives from the supplier. |
| **External state** | Supplier created a reservation; it may still be valid on the supplier's side (supplier lease may not have expired). |
| **Local state** | Reservation is `EXPIRED`. |
| **Correct behavior** | Local `EXPIRED` does **not** automatically mean the supplier has released inventory. If the supplier has a valid reservation, StallBreaker must issue a compensating release (`DELETE /v1/reservations/{token}`) using the token now received, to prevent orphaned inventory at the supplier. Transition: `EXPIRED` → `COMPENSATION_IN_PROGRESS` → `CANCELLED`. |
| **Terminal state dominance** | The local state machine does not allow `EXPIRED → CONFIRMED`. A delayed confirmation cannot re-activate a reservation. |
| **Human action** | If the compensating release fails, the scenario falls into the T3 failure path. |

**Sub-case B: Delayed confirmation arriving after explicit revocation**

| Field | Detail |
| :--- | :--- |
| **Trigger** | Supplier sent a `REVOKED` webhook at $t{=}0$; the local state is `REVOKED`. At $t{=}30s$, a delayed `CONFIRMED` packet from an earlier request arrives. |
| **Local state** | `REVOKED` (terminal). |
| **Correct behavior** | Delayed `CONFIRMED` is dropped as stale. The monotonic state hierarchy prevents any `REVOKED → CONFIRMED` transition. No action is taken on the delayed packet. |

---

### T7 — Irreversible External Action (Shipment Already In Transit)

| Field | Detail |
| :--- | :--- |
| **Trigger** | A hotshot courier has physically collected the part and is in transit. Customer cancels the repair. StallBreaker initiates cancellation. |
| **External state** | Courier is in transit; the freight fee (e.g., \$55.00) is non-refundable. The part will arrive regardless. |
| **Local state** | Reservation `CONFIRMED`; compensation requested. |
| **Guarantee** | The compensation saga acknowledges the irreversibility. The courier cannot be recalled via API. |
| **Recovery** | (a) Financial: freight cost recorded as a sunk loss under the dealership's configurable **Policy / Dispatch Loss** account (account code is a **dealership-specific configuration parameter**, not a universal constant; "Account 6840" was a placeholder and is withdrawn). (b) Physical: when the part arrives, the receiving clerk scans it; the DMS directs it to general shelf stock or cross-docks it to another RO requiring the same SKU. (c) Bay: Bay $B_4$ is released only after a **physical state check** confirms the vehicle is safe to move and a destination (staging lot or $H_2$ if available) is confirmed. Bay release is **not** automatic on cancellation if the vehicle is currently dismantled. |
| **Human action** | Parts receiving clerk must action the arriving part. Service advisor must inform the customer and confirm bay release. |
| **Residual risk** | Freight cost is unrecoverable. Vehicle bay remains occupied until physical reassembly permits safe movement. |

---

## 3. Corrected Guarantee Table Summary

| ID | Trigger | External state | Local state | Actual guarantee | Recovery | Idempotency | Human required | Residual risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | Lost response | Possibly confirmed | REQUESTED | External state unknown | Probe → retry or escalate | Local: yes; External: depends | If probe fails | Orphaned inventory without lease token |
| **T2** | Non-idempotent timeout | Unknown | REQUIRES_MANUAL | None for external | Halt auto-retry; human confirms | Local: yes; External: **unavailable** | **Always** | Duplicate PO possible |
| **T3** | Compensation failure | Reservation held | COMPENSATION_FAILED_DLQ | Local DLQ written; external not released | DLQ + alert; human phones supplier | Local: yes; External: unconfirmed | **Always** | Orphaned supplier hold; potential penalty |
| **T4** | Post-commit revocation | Part cancelled | INVALIDATED | Bay lock preserved; no auto-move | Re-solve (proposed); human approves | Local: yes; External: revoked | **Always (approve re-plan)** | No new source may exist |
| **T5** | Duplicate outbox delivery | May have duplicate PO | Depends | Local consumer dedup; external dedup: **supplier-dependent** | Modern: safe; Legacy: at-most-once | Local: yes; External: adapter-dependent | Legacy adapters | Duplicate PO for legacy adapters |
| **T6** | Out-of-order event | Active or expired | EXPIRED / REVOKED | Terminal state cannot regress | Issue release on delayed token; drop stale confirm | Local: yes | If release fails (→ T3) | Supplier may hold inventory briefly |
| **T7** | Irreversible dispatch | In transit | CANCELLED | Freight cost sunk; part arriving | Receive to stock or cross-dock; physical state check before bay release | N/A (physical) | Parts clerk + advisor | Freight cost unrecoverable |

---

## 4. Explicit Corrections to SR1.2.1 Transaction Review

| Prior claim | Correction |
| :--- | :--- |
| "Local `processed_events` table makes external HTTP actions exactly-once" | **Corrected.** The table prevents local duplicate side-effects only. External idempotency requires supplier-side `Idempotency-Key` support. For legacy adapters, at-most-once requires marking processed *before* sending with accepted loss on failure. |
| "Account 6840 — Shop Policy / Dispatch Loss" | **Withdrawn.** Account codes are dealership-specific configuration parameters. A universal code cannot be asserted. |
| "Bay $B_4$ is immediately freed for downstream alignment work without waiting for courier arrival" (T7) | **Corrected.** Bay release requires a physical state check. If the vehicle is currently dismantled, it cannot be moved until a safe staging destination is available and reassembly is sufficient. |
| Local terminal-state precedence alone resolves T6 | **Supplemented.** When a delayed confirmation carries a valid token, StallBreaker must additionally issue a compensating release to prevent an orphaned supplier hold, even if the local state remains `EXPIRED`. |

---

## 5. Summary Verdict

The transaction architecture is **failure-aware and defensible** within clearly bounded limitations. No claim of distributed atomicity, exactly-once external delivery, or unconditional distributed safety is made. The bounded failure modes (T1–T7) are explicitly handled with deterministic recovery steps, manual escalation gates, and documented residual risks.

> [!IMPORTANT]
> The correct system property to claim is: **"failure-aware, auditable compensating saga with at-least-once internal delivery, manual reconciliation gates for non-idempotent endpoints, and explicitly documented irreversible boundary conditions."**
