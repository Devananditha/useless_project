# PartsRescue PR1: Existing Systems, Competitors, and Operational Gaps

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/partsrescue-pr1-existing-solutions-review.md`  
**Phase:** PR1 — Deep Dealership Problem Discovery & Operational Validation  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Research Entity:** PartsRescue AI Innovation Research Team  
**Date:** November 14, 2026  
**Focus:** Competitive Systems Review, Incumbent Solutions, and the Unresolved Orchestration Chasm  

---

## 1. Competitive Landscape Overview

Dealership parts operations are not underserved by software. Automotive retail features multi-billion-dollar incumbent platforms managing parts catalogs, dealer inventory, and wholesale ordering.

To validate whether **PartsRescue AI** addresses an authentic white space rather than duplicating existing tools, this audit dissects existing systems across six distinct functional capabilities:
1. **Inventory Visibility:** Knowing what is on the shelf.
2. **Automatic Replenishment:** Reordering stock based on sales velocity.
3. **Part Fitment & Cataloging:** Determining which part matches a VIN.
4. **Supplier Sourcing / Locating:** Finding where an out-of-stock part exists.
5. **Shortage Exception Resolution:** Selecting the best recovery path when standard channels fail.
6. **Repair-Order Recovery Orchestration:** Synchronizing parts arrival with technician labor and bay dispatch.

---

## 2. Capability Differentiation Matrix

```
+========================================================================================================================+
|                                    EXISTING SYSTEMS CAPABILITY DECONSTRUCTION MATRIX                                   |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| System / Software Entity | 1. Inven.  | 2. Auto-Re-   | 3. Part    | 4. Supplier| 5. Shortage   | 6. RO Recovery       |
|                          | Visibility | plenishment   | Fitment    | Sourcing   | Resolution    | Orchestration        |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **Core DMS Parts**       | **YES**    | **YES**       | Minimal    | Limited    | **NO**        | **NO**               |
| (CDK / Reynolds / Tekion)| (Master OH)| (Min/Max /RIM)| (Raw SKU)  | (OEM EDI)  | (Manual alert)| (Siloed from service)|
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **OEM EPC Platforms**    | Limited    | **NO**        | **YES**    | **NO**     | **NO**        | **NO**               |
| (Snap-on / Microcat)     | (PDC stock)|               | (VIN build)|            | (Text TSB only| (Blind to shop floor)|
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **OEC D2DLink**          | Peer stock | **NO**        | **NO**     | **YES**    | Partial       | **NO**               |
| (OEConnection)           | (Nationwide|               | (Requires  | (Dealer-to-| (Manual buy   | (Zero shop/bay       |
|                          | dealer net)|               | exact SKU) | dealer net)| request)      | intelligence)        |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **OEC D2D Express**      | Peer stock | **NO**        | **NO**     | **YES**    | **YES**       | **NO**               |
| (Auto-Backorder Matching)|            |               | (Requires  | (Automated | (Fulfills OEM | (Zero technician     |
|                          |            |               | exact SKU) | broker)    | backorder)    | resequencing)        |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **Aftermarket Portals**  | Local stock| **NO**        | **YES**    | **YES**    | Partial       | **NO**               |
| (Nexpart / Worldpac)     | (Local WD) |               | (Year/Make)| (Online PO)| (Buy local alt| (Isolated web tab)   |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **DMS Shop Dispatch**    | **NO**     | **NO**        | **NO**     | **NO**     | **NO**        | Partial              |
| (Smart Tech Matching)    |            |               |            |            |               | (Queues techs, but   |
|                          |            |               |            |            |               | blind to parts ETAs) |
+--------------------------+------------+---------------+------------+------------+---------------+----------------------+
| **PartsRescue AI**       | Consumes   | Consumes      | Determin-  | Multi-     | **AUTONOMOUS**| **AUTONOMOUS**       |
| (Proposed Solution)      | DMS feeds  | DMS feeds     | istic DAG  | Source     | **MULTI-OBJ.**| **CROSS-FUNCTIONAL** |
|                          |            |               | & ACES/PIES| Optimizer  | **TRADE-OFF** | **ORCHESTRATION**    |
+========================================================================================================================+
```

---

## 3. Deep-Dive Profile of Existing Incumbents

### 3.1 OEConnection (OEC) D2DLink & D2D Express
* **Documented Capability:** OEC is the premier original equipment parts locating network in North America, connecting thousands of franchised dealerships.
  * **D2DLink:** Allows parts managers to manually search peer dealership inventories across the nation for scarce or backordered OE parts.
  * **D2D Express:** An automated broker system. When an OEM PDC reports a national backorder, D2D Express scans participating dealer inventories within a geographic radius and automatically routes a fulfillment order to a stocking dealer.
* **The Unresolved Gap:**
  * OEC operates exclusively within the **OEM wholesale supply chain**. It does not know or care about the dealership's physical bay status, the customer's promised ready time, or the hourly holding cost of the service lift.
  * OEC only locates the **exact requested part number**; it does not dynamically evaluate whether an aftermarket equivalent is commercially appropriate for a customer-pay job, nor does it generate customer approval SMS cards.

### 3.2 DMS Parts Replenishment & RIM Programs
* **Documented Capability:** Dealership Management Systems (Tekion ARC Parts Cloud, CDK Global, Reynolds & Reynolds ERA-IGNITE) feature automated inventory replenishment engines:
  * Minimum/Maximum stocking thresholds based on historical sales velocity.
  * OEM-mandated inventory replenishment programs (e.g. GM RIM - Retail Inventory Management, Ford ASR - Automated Stock Replenishment).
* **The Unresolved Gap:**
  * Replenishment engines are **statistical ordering tools for future stock** (optimizing what to order on Tuesday's stock truck). They are completely useless when a technician has a car disassembled on Lift 4 right now and needs a part in 45 minutes.

### 3.3 Aftermarket Ordering Portals (Nexpart / Worldpac Speedir / PartsTrader)
* **Documented Capability:** Web-based portals allowing commercial repair shops and dealerships to query local wholesale warehouse inventory (e.g., brake pads, alternators, sensors) and order local delivery.
* **The Unresolved Gap:**
  * These portals live in **isolated browser tabs** outside the dealership DMS.
  * Counter personnel must manually re-key vehicle data into Nexpart, evaluate pricing, call the service advisor to ask if the customer will accept an aftermarket brand, and manually type an outside purchase (OP) order back into the DMS.

---

## 4. The Unresolved Orchestration Chasm

The existing software landscape suffers from a profound **architectural fragmentation**:

```mermaid
flowchart LR
    subgraph Silo1 ["Parts Sourcing Silo (OEC / Worldpac)"]
        O1["Finds Part at Sister Store"]
        O2["Finds Aftermarket at NAPA"]
    end
    subgraph Silo2 ["DMS Parts Inventory Silo"]
        D1["Local Stock Counts"]
        D2["Purchase Orders / Bins"]
    end
    subgraph Silo3 ["Service Drive Silo"]
        S1["Customer Promise Time"]
        S2["Customer SMS Authorizations"]
    end
    subgraph Silo4 ["Shop Floor Silo"]
        F1["Lift Occupancy / Bay Status"]
        F2["Technician Flag-Hour Dispatch"]
    end
    Silo1 -.->|DISCONNECTED| Silo2
    Silo2 -.->|DISCONNECTED| Silo3
    Silo3 -.->|DISCONNECTED| Silo4
```

### What No Existing System Does:
No current commercial automotive product connects the dots across these four silos:
1. It does **not** evaluate whether spending $25 on a hotshot courier is justified by avoiding $160 in dead bay time.
2. It does **not** check whether the repair is factory warranty (mandating OEM) or customer-pay (allowing certified aftermarket).
3. It does **not** generate an automated interactive mobile approval card for the customer while the parts counter is evaluating delivery options.
4. It does **not** update the shop dispatcher to pull forward an alternate maintenance job while the courier is in transit.

**This is the precise white space occupied by PartsRescue AI: Autonomous Cross-Functional Recovery Orchestration.**
