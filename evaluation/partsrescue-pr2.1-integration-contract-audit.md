# PartsRescue PR2.1: Tekion API & DMS Integration Contract Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-integration-contract-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** Integration and API Architect, Enterprise SaaS Product Architect  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Mandate

In Phase PR2, `architecture/partsrescue-pr2-integration-strategy.md` and `architecture/partsrescue-pr2-logical-architecture.md` specified concrete API endpoints and webhooks (e.g., `dealership.service.ro_line.status_changed`, `POST /parts/purchase-orders`, `PATCH /service/repair-orders/{id}/lines/{lineId}`, `POST /parts/transfers`).

This audit critically interrogates these interface definitions against official Tekion documentation and `.cursor/rules/research-standards.mdc`.

### Key Audit Findings:
1. **Unverified Proprietary Endpoints:** Tekion does not publicly document or sanction the specific URIs presented in PR2. Presenting them as verified Tekion ARC production endpoints violates research standards.
2. **Mock vs. Production Conflation:** The PR2 architecture did not clearly differentiate between:
   * Real, verified DMS vendor capabilities.
   * Proposed internal application contracts.
   * Mock test adapters designed for hackathon demonstration.
3. **Write-Safety & Permission Realities:** DMS vendors (including Tekion, CDK, and Reynolds) maintain strict security boundaries around purchase order generation and financial ledger posting. Third-party integrations typically generate **draft purchase orders** or **uncommitted requisition lines** that require an authorized DMS operator to review and post.

---

## 2. Rigorous Interface Classification Matrix

In accordance with Critical Audit Area C, every interface mentioned in the architecture is classified into one of five rigorous categories:

```
+=================================================================================================================================+
|                                            INTERFACE CLASSIFICATION MATRIX                                                      |
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| #  | Interface / Contract Name      | PR2 Presentation      | Audit Classification        | Authoritative Reality & Remedy      |
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 01 | `dealership.service.ro_line.`  | Claimed as official   | **[PROPOSED INTERNAL /      | *Reality:* Tekion ARC uses internal |
|    | `status_changed`               | Tekion webhook.       | MOCK CONTRACT]**            | event buses; public webhook payload |
|    |                                |                       |                             | format is not publicly documented.  |
|    |                                |                       |                             | *Remedy:* Reframe as Mock Adapter.  |
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 02 | `POST /parts/purchase-orders`  | Claimed as Tekion ARC | **[MOCK ADAPTER CONTRACT]** | *Reality:* Unverified URI. Tekion   |
|    |                                | PO creation endpoint. | (Assumed External Capability)| parts purchasing API is proprietary.|
|    |                                |                       |                             | *Remedy:* Label as Mock DMS Adapter.|
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 03 | `PATCH /service/repair-orders/`| Claimed as Tekion ARC | **[MOCK ADAPTER CONTRACT]** | *Reality:* Unverified URI. Live DMS |
|    | `{id}/lines/{lineId}`          | line update endpoint. | (Assumed External Capability)| line updates require partner cert.  |
|    |                                |                       |                             | *Remedy:* Label as Mock DMS Adapter.|
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 04 | `POST /parts/transfers`        | Claimed as Tekion ARC | **[MOCK ADAPTER CONTRACT]** | *Reality:* Multi-store transfer     |
|    |                                | transfer endpoint.    | (Assumed External Capability)| logic is proprietary to dealer group|
|    |                                |                       |                             | *Remedy:* Label as Mock DMS Adapter.|
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 05 | Nexpart / PartsTech B2B REST   | Presented as live     | **[ASSUMED EXTERNAL         | *Reality:* Real commercial APIs     |
|    | Endpoints                      | supplier connectors.  | CAPABILITY / MOCK]**        | exist, but credentials are unavail. |
|    |                                |                       |                             | *Remedy:* High-fidelity mock adapter|
+----+--------------------------------+-----------------------+-----------------------------+-------------------------------------+
| 06 | Curri / Roadie Hotshot Courier | Presented as live     | **[ASSUMED EXTERNAL         | *Reality:* Real courier APIs exist; |
|    | Webhooks                       | delivery dispatch.    | CAPABILITY / MOCK]**        | requires commercial developer token.|
|    |                                |                       |                             | *Remedy:* Synthetic courier adapter.|
+=================================================================================================================================+
```

---

## 3. Demarcation of Application Data Needs & Operations

To establish a defensible integration contract, PartsRescue explicitly separates what it reads from the DMS versus what it requests the DMS to write:

```
+========================================================================================================================+
|                                    DMS READ VS. WRITE BOUNDARY CONTRACT                                                |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| DMS Interaction          | Data Elements         | Operation Mode      | Authorization & User Gate                     |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Read: RO Header**      | RO #, Customer Key,   | **READ-ONLY**       | Automated ingestion via mock listener or      |
|                          | Promise Time, PayType |                     | periodic polling query. Zero user gate needed.|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Read: Parts Line**     | Line #, Part SKU,     | **READ-ONLY**       | Automated ingestion when status transitions to|
|                          | Quantity, Status      |                     | `OUT_OF_STOCK` or `BACKORDERED`.              |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Read: Service Context**| Assigned Tech ID,     | **READ-ONLY**       | Automated ingestion; used strictly to compute |
|                          | Bay ID, Labor Op Code |                     | opportunity cost and buffer time.             |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Read: Local Inventory**| On-Hand, Allocated,   | **READ-ONLY**       | Automated ingestion; verifies local stock is  |
|                          | Available, Bin Loc    |                     | genuinely exhausted before sourcing externally|
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Write: Draft PO**      | Vendor ID, Part SKU,  | **WRITE-CAPABLE**   | **MANDATORY HUMAN GATE:** Requires authorized |
|                          | Cost, Freight Surchg  | (Pre-filled Draft)  | Counterperson click. Creates UNPOSTED draft.  |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Write: Line ETA & Log**| Sourced Part SKU,     | **WRITE-CAPABLE**   | **MANDATORY HUMAN GATE:** Updates line status |
|                          | ETA timestamp, URL    | (Audit Tracking)    | to `SOURCED_EXPEDITED` upon PO creation.      |
+--------------------------+-----------------------+---------------------+-----------------------------------------------+
| **Write: Inter-Store Req**| Source Store, SKU,   | **WRITE-CAPABLE**   | **MANDATORY HUMAN GATE:** Generates sister-   |
|                          | Quantity, Courier Ref | (Requisition Draft) | store stock transfer requisition draft.       |
+========================================================================================================================+
```

---

## 4. Hackathon Mock Adapter Strategy vs. Production Reality

```
+========================================================================================================================+
|                                    MOCK ADAPTER VS. PRODUCTION FEASIBILITY                                             |
+--------------------------+----------------------------------------+----------------------------------------------------+
| Dimension                | Hackathon Mock Adapter Contract        | Production Integration Reality                     |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Implementation**      | `MockTekionDmsAdapter`                 | Formal Tekion Partner Integration Program          |
|                          | (In-memory Python/TypeScript harness)  | (mTLS, OAuth2 Client Credentials, Partner Sandbox)|
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Event Triggers**       | Synthetic JSON webhook events injected | Tekion ARC Webhook Event Bus or Change-Data-       |
|                          | via test script or Postman collection. | Capture (CDC) polling interface.                   |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Write Behavior**       | Returns simulated HTTP 201 Created with| Generates unposted draft PO in Tekion Parts Cloud; |
|                          | mock PO number `PO-MOCK-99182`.        | counterperson posts PO within standard DMS UI.     |
+--------------------------+----------------------------------------+----------------------------------------------------+
| **Feasibility Proof**    | **DOES NOT PROVE PRODUCTION ACCESS.**  | Requires formal technical agreement and API access |
|                          | Proves data model compatibility only.  | granted by Tekion enterprise engineering.          |
+========================================================================================================================+
```

---

## 5. Graceful Degradation: What Happens When Integration is Unavailable?

In dealership environments, external network disruptions and DMS maintenance windows are routine. PartsRescue incorporates three degradation tiers:

1. **Tier 1: Webhook Ingestion Offline (Polling Fallback):**
   * If the DMS webhook listener fails, PartsRescue polls the DMS RO line endpoint every 60 seconds for newly flagged shortage lines.
2. **Tier 2: DMS Write API Offline (Clipboard / Action Card Fallback):**
   * If the DMS rejects PO write commands (`HTTP 500` or network unreachable), PartsRescue **does not crash**.
   * It displays a **Pre-Populated Sourcing Slip** directly in the browser console.
   * The counterperson clicks *"Copy PO Details to Clipboard"* and pastes the vendor, SKU, price, and courier reference directly into the standard DMS purchase order screen.
3. **Tier 3: Complete Network Isolation (Standalone Manual Triage):**
   * If all DMS connectivity is lost, the counterperson can manually enter: Part SKU, Vehicle VIN, and Labor Op.
   * PartsRescue executes local fitment and trade-off calculations completely offline using local cached tables.

---

## 6. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Mandatory Modifications Across PR2 Documents:**
  * In `architecture/partsrescue-pr2-integration-strategy.md` and `architecture/partsrescue-pr2-logical-architecture.md`, explicitly rebrand all Tekion API paths as **`MockTekionDmsAdapter` contract endpoints**.
  * Remove any claim that Tekion ARC officially provides these exact webhook names or REST URIs.
  * Clearly document that mock adapters prove **logical contract viability**, not commercial integration certification.
