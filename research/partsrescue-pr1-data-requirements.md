# PartsRescue PR1: Data Requirements & The ACES/PIES Technical Reality

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/partsrescue-pr1-data-requirements.md`  
**Phase:** PR1 — Deep Dealership Problem Discovery & Operational Validation  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, Auto Care Association Standards  
**Research Entity:** PartsRescue AI Innovation Research Team  
**Date:** November 14, 2026  
**Focus:** Data Requirements Matrix, Exchange Standards Deconstruction, and Licensing Realities  

---

## 1. Data Requirements Matrix

To operationalize PartsRescue AI, the system requires inputs spanning five distinct data domains: dealership internal work orders, vehicle build attributes, OEM catalog schemas, aftermarket exchange standards, and external supplier inventory feeds.

```
+========================================================================================================================+
|                                    PARTSRESCUE PRELIMINARY DATA REQUIREMENTS MATRIX                                    |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| #  | Data Element         | Operational Purpose   | Authoritative     | Production      | Commercial  | Hackathon Demo |
|    |                      |                       | Source            | Availability    | Sensitivity | Strategy       |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 01 | **Repair Order (RO)**| Identify affected car,| Dealership DMS    | High (via DMS   | HIGH        | **Synthetic**  |
|    | **Header & Lines**   | assigned tech, bay #  | (Tekion/CDK)      | API / Webhooks) | (Customer PI| JSON Fixtures  |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 02 | **Vehicle Build Data**| Decode engine, trim, | OEM Build Sheet / | High (via VIN   | Medium      | **Curated**    |
|    | **(VIN Attributes)** | transmission, options | VIN Decoder API   | decoding APIs)  |             | VIN Fixtures   |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 03 | **Required OEM Part**| Identify missing      | OEM Electronic    | Restricted (OEM | High        | **Curated**    |
|    | **Number (SKU)**     | mechanical component  | Parts Cat (EPC)   | EPC licensing)  | (IP / Trade)| 8 Archetypes   |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 04 | **OEM Supersession** | Traversal of revised  | OEM Distribution  | Restricted (OEM | High        | **Curated**    |
|    | **Lineage (DAG)**    | part numbers (Rev A/B)| Master Database   | proprietary DAG)|             | Directed Graph |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 05 | **Dealer Inventory** | Check on-hand &       | Dealership DMS    | High (Internal  | High        | **Synthetic**  |
|    | **Master (OH / AV)** | allocated stock       | Parts Module      | DMS tables)     | (Financial) | DMS Tables     |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 06 | **Supplier / Peer**  | External multi-source | Commercial EDI /  | **PAYWALLED &** | High        | **Mock REST**  |
|    | **Stock & ETA Feed** | availability & delivery| API (OEC, World) | **NDA GATED**   | (Commercial)| Endpoints      |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 07 | **Part Wholesale &** | Calculate gross profit| Supplier Price    | Restricted (Net | High        | **Curated**    |
|    | **Retail Matrix Cost**| & price variance      | Tape / DMS Matrix | wholesale fees) | (Margin)    | Matrix Pricing |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 08 | **Courier Transit &**| Model delivery ETA vs | Local Courier API | Medium (Courier | Low         | **Simulated**  |
|    | **Freight Cost**     | bay holding cost      | / Mapping Service | distance model) |             | Distance Model |
+----+----------------------+-----------------------+-------------------+-----------------+-------------+----------------+
| 09 | **Technician & Bay** | Determine if tech can | Dealership DMS    | High (Internal  | High        | **Simulated**  |
|    | **Dispatch Status**  | resequence or stage car| Service Module   | dispatch queue) | (Labor P&L) | 12-Bay State   |
+========================================================================================================================+
```

---

## 2. Deconstruction of the ACES and PIES Standards

In earlier automotive software proposals, developers frequently assert: *"We will simply query ACES to find which part fits."* Under `.cursor/rules/research-standards.mdc`, this represents a fundamental technical conflation that would be dismantled by any automotive domain judge.

### 2.1 What ACES and PIES Actually Are (Auto Care Association Standards)
The **Auto Care Association** governs standardized data exchange formats for the North American automotive aftermarket. ACES and PIES are **XML/relational data protocols**, not software applications or self-contained catalogs:

1. **ACES (Aftermarket Catalog Exchange Standard):**
   * **Definition:** Standardized XML format used strictly to communicate **vehicle application (fitment) data**.
   * **The Question It Answers:** *"What specific years, makes, models, submodels, and engine configurations does Part XYZ fit?"*
   * **Mechanism:** ACES does **not** use free-text strings (e.g. it does not say "2021 Ford F-150"). Instead, it references unique numerical identifiers pulled from supporting relational databases.
2. **PIES (Product Information Exchange Standard):**
   * **Definition:** Standardized XML format used to communicate **product descriptive data**.
   * **The Question It Answers:** *"What is the part, what are its dimensions, weight, digital images, brand name, warranty length, and packaging attributes?"*
   * **Rule:** ACES and PIES travel together as a pair; ACES tells you what it fits, PIES tells you what it is.

---

## 3. The Supporting Relational Databases & Licensing Realities

An ACES XML file is unreadable and useless without access to the Auto Care Association's proprietary reference databases:

```
+========================================================================================================================+
|                                    AUTO CARE ASSOCIATION REFERENCE DATABASES                                           |
+----+----------------------+---------------------------------+----------------------------------------------------------+
| #  | Database Acronym     | Full Name                       | Data Content & Relational Purpose                        |
+----+----------------------+---------------------------------+----------------------------------------------------------+
| 01 | **VCdb**             | Vehicle Configuration Database  | Normalized master table of Year/Make/Model/Submodel/     |
|    |                      |                                 | Engine/DriveType (`BaseVehicleID` & `VehicleID`).        |
+----+----------------------+---------------------------------+----------------------------------------------------------+
| 02 | **PCdb**             | Product Classification Database | Standardized taxonomy of part terminology (e.g.,         |
|    |                      |                                 | assigns code 1896 to "Alternator", 1684 to "Brake Pad"). |
+----+----------------------+---------------------------------+----------------------------------------------------------+
| 03 | **Qdb**              | Qualifier Database              | Standardized application qualifier notes (e.g., "Fits    |
|    |                      |                                 | 4WD models only", "Excludes Heavy Duty Towing Package"). |
+----+----------------------+---------------------------------+----------------------------------------------------------+
| 04 | **PAdb**             | Product Attribute Database      | Standardized physical attribute names (e.g., "Amperage", |
|    |                      |                                 | "Pulley Groove Quantity", "Rotor Diameter").             |
+========================================================================================================================+
```

### Critical Licensing & Legal Boundaries:
* **ACES is NOT Open Source:** The VCdb, PCdb, and Qdb are proprietary commercial databases owned by the Auto Care Association. Access requires an **annual subscription to the Auto Care Vehicle Information Portal (VIP)**, costing thousands of dollars annually.
* **ACES is NOT an Application:** Auto Care Association does *not* provide an API where you send a VIN and receive an aftermarket part number. ACES is the format that *manufacturers* (e.g. Bosch, Dorman, Gates) use to publish their catalog feeds to wholesale distributors.
* **The Fitment Mapping Reality:** ACES maps aftermarket parts to vehicles; it does **not** natively cross-reference OEM part numbers to aftermarket numbers. Cross-referencing OEM to aftermarket requires commercial interchange tables (e.g. Motor Information Systems, Epicor, WHI Solutions).

---

## 4. Strict Evidentiary Distinctions

To maintain absolute credibility, PartsRescue AI documentation strictly distinguishes between five frequently conflated concepts:

```
+========================================================================================================================+
|                                    EVIDENTIARY SEPARATION OF AUTOMOTIVE DATA DOMAINS                                   |
+--------------------------+---------------------------------------------------------------------------------------------+
| Domain Concept           | Exact Technical Definition (Do NOT Conflate)                                                |
+--------------------------+---------------------------------------------------------------------------------------------+
| **1. Data Exchange**     | XML schemas (ACES & PIES) defining how fitment and product data are formatted.              |
| **Standards**            | Contains zero part numbers or inventory on its own.                                         |
+--------------------------+---------------------------------------------------------------------------------------------+
| **2. Reference**         | Master relational tables (VCdb, PCdb) providing normalized vehicle and part-type IDs.       |
| **Databases**            | Requires paid annual subscription from Auto Care Association.                               |
+--------------------------+---------------------------------------------------------------------------------------------+
| **3. Product Fitment**   | Proprietary mapping files published by manufacturers specifying which parts fit which VCdb  |
| **Applications**         | vehicle configurations.                                                                     |
+--------------------------+---------------------------------------------------------------------------------------------+
| **4. OEM Supersession**  | Manufacturer-specific directed acyclic graphs (DAGs) tracking internal part number revisions|
| **Lineage**              | strictly within a single OEM brand (e.g. Ford engineering part changes).                    |
+--------------------------+---------------------------------------------------------------------------------------------+
| **5. Live Inventory**    | Real-time quantity-on-hand and pricing feeds at specific dealer or distributor locations     |
| **Feeds**                | accessible only via private enterprise EDIs or authenticated dealer APIs.                   |
+========================================================================================================================+
```

---

## 5. Hackathon Demonstration Feasibility Plan

Because a student hackathon team cannot purchase commercial VCdb licenses or sign bilateral EDI agreements with Worldpac or Snap-on, PartsRescue AI will utilize a **transparent curated data strategy**:
1. **Curated Archetype Database:** Pre-compile a verified, static dataset of **8 vehicle archetypes** (4 warranty scenarios, 4 customer-pay scenarios) covering ~30 OEM part supersessions and certified aftermarket cross-references.
2. **Mock Supplier REST Server:** Deploy a lightweight mock API server that returns realistic stock counts, wholesale pricing, and courier transit times with simulated network latency.
3. **Transparent Pitch Presentation:** Explicitly inform hackathon judges:  
   > *"For our 5-minute live demonstration, PartsRescue AI operates on a curated high-fidelity dataset of 8 realistic vehicle repair archetypes and simulated distributor REST endpoints, perfectly demonstrating the agentic multi-objective optimization without incurring enterprise catalog licensing fees."*
