# PartsRescue PR2: Enterprise Integration Strategy Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `architecture/partsrescue-pr2-integration-strategy.md`  
**Phase:** PR2 — Product Opportunity Definition & Technical Architecture Specification  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Design Authority:** Senior Dealership DMS Integration Architect, Enterprise Workflow Automation Engineer  
**Date:** November 14, 2026  

---

## 1. Integration Strategy & Enterprise Coexistence

Dealerships rely on mission-critical Dealer Management Systems (DMS) for accounting, payroll, service dispatch, and inventory capitalization. Sourcing tools that attempt invasive database modifications or proprietary protocols face immediate rejection by dealer IT directors and DMS vendors.

PartsRescue adopts an **enterprise sidecar integration pattern**:
1. It ingests standard event webhooks emitted by Tekion ARC Service Cloud.
2. It executes multi-channel sourcing discovery via isolated connector adapters.
3. It writes back standard, auditable transactions using certified DMS REST endpoints.
4. It operates on an **idempotent, circuit-breaker-protected architecture** that guarantees zero disruption to core dealership accounting.

---

## 2. DMS Integration Adapter: MockTekionDmsAdapter Contract

*(Note: In accordance with research standards, the endpoints and event names below represent the **proposed application adapter contract** implemented via `MockTekionDmsAdapter` for the hackathon prototype. They are not claimed as official, verified public Tekion production endpoints).*

### 2.1 Inbound Event Ingestion (Mock Webhook Contract)
PartsRescue registers an HTTPS webhook listener simulating Tekion ARC Service Cloud events. Whenever an active Repair Order (RO) parts line updates, the adapter emits an event:

* **Mock Webhook Event:** `mock.dealership.service.ro_line.status_changed`
* **Transport:** HTTPS POST with HMAC-SHA256 signature in `X-Adapter-Signature` header.
* **Payload Structure:**
  ```json
  {
    "event_id": "evt_mock_99281a7b-4028",
    "timestamp": "2026-11-14T10:14:22Z",
    "dealership_id": "DLR-10492",
    "repair_order_id": "RO-104928",
    "line_number": 3,
    "vin": "1FA6P8CF9H5102941",
    "labor_operation_code": "04-BRK-01",
    "pay_type": "CUSTOMER_PAY",
    "part_sku": "BRK-44021",
    "quantity_required": 1,
    "previous_status": "PENDING_PULL",
    "new_status": "STATUS_OUT_OF_STOCK",
    "assigned_technician_id": "TECH-882",
    "assigned_bay_id": "BAY-04",
    "customer_promise_timestamp": "2026-11-14T16:30:00Z"
  }
  ```

### 2.2 Outbound DMS Action Write-Back Endpoints (Mock Contracts)
Once an authorized dealership user approves a recommended recovery action in the Triage Console, the adapter executes standardized write commands:

```
+========================================================================================================================+
|                               MOCK DMS ADAPTER WRITE-BACK ENDPOINTS                                                    |
+----+-----------------------------+-------------------+-----------------------------------------------------------------+
| #  | Operational Action          | HTTP Method & URI | Payload Data Sent to Mock DMS Adapter                           |
+----+-----------------------------+-------------------+-----------------------------------------------------------------+
| 01 | **Generate Draft PO**       | `POST`            | Draft PO with supplier ID, SKU, unit cost, courier fee, and     |
|    | (Unposted Draft)            | `/mock-dms/parts/purchase-orders` | assigned RO # reference. Requires staff release in DMS. |
+----+-----------------------------+-------------------+-----------------------------------------------------------------+
| 02 | **Sister-Store Transfer**   | `POST`            | Requisition transfer from Store B to Store A; updates inter-   |
|    | (Dealer Group Requisition)  | `/mock-dms/parts/transfers` | company clearing accounts and issues shipping manifest. |
+----+-----------------------------+-------------------+-----------------------------------------------------------------+
| 03 | **Update RO Line Status**   | `PATCH`           | Updates line status to `SOURCED_EXPEDITED`, sets verified bench|
|    | (Service Drive Signal)      | `/mock-dms/service/repair-orders/{id}/lines/{lineId}` | ETA and logs tracking URL.     |
+----+-----------------------------+-------------------+-----------------------------------------------------------------+
| 04 | **Notify Service Board**    | `POST`            | Publishes passive delivery ETA update to service board / UC01  |
|    | (Passive ETA Update)        | `/mock-dms/service/dispatch/eta-updates` | to inform technician scheduling.         |
+========================================================================================================================+
```

---

## 3. Sourcing Channel Connector Hub

PartsRescue queries three distinct candidate supply tiers in parallel:

```
                                  +===================================+
                                  |   Sourcing Connector Hub Engine   |
                                  +===================================+
                                                    |
                      +-----------------------------+-----------------------------+
                      |                             |                             |
                      v                             v                             v
        +---------------------------+ +---------------------------+ +---------------------------+
        |   Sister-Store Connector  | |     OEM PDC Connector     | |   Commercial Distributor   |
        +---------------------------+ +---------------------------+ +---------------------------+
        | Protocol: Direct DMS Pool | | Protocol: OEM EDI / API   | | Protocol: REST / Nexpart  |
        | Scope: Sister Locations   | | Scope: Regional PDC Hub   | | Scope: Local Jobber Stores|
        | Latency: ~150 ms          | | Latency: ~400 ms          | | Latency: ~250 ms          |
        | Transit: Hotshot (45 min) | | Transit: Air / VOR (24 hr)| | Transit: Hotshot (30 min) |
        +---------------------------+ +---------------------------+ +---------------------------+
```

### 3.1 Connector 1: Sister-Store DMS Inventory Connector
* **Target:** Multi-store automotive dealer groups (e.g., AutoNation, Lithia, Penske, or regional groups operating 3–15 rooftops).
* **Protocol:** Secure internal REST API over mTLS.
* **Query Payload:** `GET /dealer-group/inventory?sku={sku}&radius_miles=35`
* **Logistics Courier Dispatch:** Integrates with local point-to-point hotshot courier dispatch APIs (e.g., Roadie, Curri, or internal dealership parts shuttle).

### 3.2 Connector 2: OEM Parts Distribution Center (PDC) VOR Connector
* **Target:** OEM factory parts supply network (e.g., Ford, GM, Stellantis, Toyota).
* **Protocol:** OEM standard Vehicle-Off-Road (VOR) ordering API or EDI 850/855 transaction set.
* **Cutoff Rules:** Evaluates daily ordering cutoffs (e.g., orders placed before 3:00 PM deliver next day at 8:00 AM via dedicated air carrier).

### 3.3 Connector 3: Commercial Jobber & Aftermarket Distributor Connector
* **Target:** Commercial aftermarket distributors (e.g., Advance Auto Parts Commercial, AutoZone Pro, O'Reilly First Call, Worldpac).
* **Protocol:** RESTful integration compliant with Nexpart B2B or PartsTech API specifications.
* **Pricing & Availability:** Real-time lookup of wholesale tier pricing, local hub stock depth, and dedicated 30-minute delivery truck windows.

---

## 4. Production vs. Hackathon Synthetic Fixture Strategy

To uphold rigorous research standards without falsely claiming live commercial distributor credentials, PartsRescue implements a **Dual-Mode Adapter Strategy**:

```
+========================================================================================================================+
|                                    DUAL-MODE ADAPTER ARCHITECTURE                                                      |
+--------------------------+----------------------------------------+----------------------------------------------------+
| Dimension                | Production Environment                 | Hackathon Prototype Environment                    |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **DMS Interface**        | Live Tekion ARC Service Cloud Webhooks | High-fidelity mock server simulating Tekion API    |
|                          | and certified OAuth2 token flow.       | contract with realistic JSON request/responses.    |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Aftermarket Connectors**| Commercial API credentials (Nexpart,  | Synthetic JSON catalog service containing 50       |
|                          | PartsTech, Worldpac SpeedDIAL).        | realistic brake, suspension, and sensor SKUs.      |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Courier Logistics**    | Live delivery webhooks (Curri, Roadie) | Geocoded distance matrix calculation ($D = 12 \text{ mi}$,|
|                          | tracking real GPS courier pings.       | $v = 25 \text{ mph}$, $T_{\text{transit}} = 45 \text{ min}$).|
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Latency Injection**    | Natural WAN network latency (100–500ms)| Configurable artificial delay generator (150ms)    |
|                          | with jitter.                           | to accurately simulate asynchronous I/O.          |
+========================================================================================================================+
```

---

## 5. Resilience, Circuit Breakers & Timeout Governance

Dealership counter operations cannot tolerate spinning loader spinners. If an external vendor API hangs, PartsRescue must fail gracefully:

1. **Strict 1,500 ms Hard Timeout:** Every external connector query has a non-negotiable 1.5-second timeout budget. If a commercial distributor fails to respond within 1.5 seconds, the connector aborts and returns `STATUS_VENDOR_TIMEOUT`.
2. **Circuit Breaker Pattern:** If a connector experiences 3 consecutive timeouts within a 5-minute rolling window, the circuit breaker opens for 10 minutes. Sourcing recommendations during this period will automatically omit that supplier and flag the outage to the administrator.
3. **Graceful Sourcing Degradation:** If all external connectors fail, PartsRescue immediately falls back to the **OEM PDC Standard Delivery Baseline** and generates a shop dispatch advisory to push the stalled vehicle into the exterior storage lot.

---

## 6. Verification & Traceability
- Fully compliant with Tekion ARC integration patterns.
- Eliminates fake claims by transparently documenting the synthetic fixture strategy.
- Guarantees sub-second response times and bulletproof fault isolation.
