# PartsRescue PR2: Fitment & Warranty Eligibility Engine Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `architecture/partsrescue-pr2-fitment-and-eligibility-engine.md`  
**Phase:** PR2 — Product Opportunity Definition & Technical Architecture Specification  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Design Authority:** Automotive Parts Catalogue & Fitment Specialist, Senior Dealership DMS Integration Architect  
**Date:** November 14, 2026  

---

## 1. Architectural Mandate: Deterministic Fitment vs. AI Hallucination

In automotive repair operations, an incorrect part number results in vehicle damage, warranty claim debit-backs, or an immobilized vehicle on a hydraulic lift. Therefore, **Large Language Models (LLMs) are strictly prohibited from predicting or validating mechanical fitment**. 

Fitment, supersession, and warranty eligibility are enforced by a **100% deterministic, rule-based verification pipeline**.

---

## 2. Separation of Nine Distinct Validation Concepts

To prevent architectural ambiguity, PartsRescue explicitly distinguishes nine distinct validation dimensions:

```
+========================================================================================================================+
|                                    NINE DISTINCT VALIDATION CONCEPTS MATRIX                                            |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| #  | Validation Concept          | Technical Definition & Verification Mechanism                                       |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 01 | **Mechanical Fitment**      | Verifies that the candidate part physically bolts onto and functions within the     |
|    |                             | specific VIN application (Year, Make, Model, Submodel, Engine, Drivetrain).        |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 02 | **OEM Supersession Chain**  | Traverses the OEM directed acyclic graph (DAG) from obsolete part numbers to the    |
|    |                             | latest approved successor part number (e.g., Part A -> Part B -> Part C).          |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 03 | **Mandatory Co-Requisites** | Identifies mandatory companion hardware required for the repair operation that      |
|    |                             | cannot be reused (e.g., torque-to-yield bolts, crush washers, manifold gaskets).   |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 04 | **Work-Order Pay-Type**     | Identifies the financial entity funding the repair (OEM Factory Warranty, Third-    |
|    |                             | Party Vehicle Service Contract [VSC], Retail Customer-Pay, Internal Reconditioning)|
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 05 | **Brand & Tier Eligibility**| Categorizes part quality tiers (OEM Genuine, OEM Tier-2 [Omnicraft/ACDelco Gold],   |
|    |                             | Certified Tier-1 Aftermarket [CAPA], Standard Commercial Aftermarket, Salvage).    |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 06 | **Commercial Availability** | Confirms physically verified, unallocated stock quantity ($Q_{\text{avail}} \ge Q_{\text{req}}$)|
|    |                             | at the sourcing depot or sister-store.                                              |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 07 | **Core Deposit & Exchange** | Tracks refundable core deposits on remanufactured components (calipers, alternators)|
|    |                             | and establishes reverse-logistics courier return procedures.                       |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 08 | **Pricing & Margin Limits** | Applies dealership parts pricing matrix, calculates gross margin dollars/percent,  |
|    |                             | and checks against warranty reimbursement rate schedules.                           |
+----+-----------------------------+-------------------------------------------------------------------------------------+
| 09 | **Channel Feasibility**     | Verifies supplier account standing, credit limits, daily ordering cutoff times,    |
|    |                             | and hotshot courier delivery radius.                                                |
+========================================================================================================================+
```

---

## 3. Catalog Standards: ACES/PIES Architecture & Commercial Realities

### 3.1 Industry Standards Definition
* **ACES (Aftermarket Catalog Exchange Standard):** The North American automotive industry standard XML format for exchanging vehicle application data. It maps part numbers to specific vehicle attributes using standard database identifiers:
  * **VCdb (Vehicle Configuration Database):** Standardized Year, Make, Model, Engine, Transmission configs.
  * **PCdb (Part Terminology Database):** Standardized part taxonomy and categorization.
  * **Qdb (Qualifier Database):** Application-specific qualifiers (e.g., "with 4-wheel disc brakes", "without towing package").
* **PIES (Product Information Exchange Standard):** The standard XML format for exchanging product attribute data (dimensions, weight, hazardous material flags, country of origin, warranty terms, and high-resolution images).

### 3.2 Hackathon Feasibility & Synthetic Data Strategy
* **Commercial Reality:** Access to live ACES/PIES master tables (VCdb/PCdb) requires an active subscription to the Auto Care Association VIP portal ($3,500+ annually) or commercial catalog APIs (PartsTech, WHI Nexpart).
* **Defensible Hackathon Strategy:** For the hackathon prototype, PartsRescue utilizes a **normalized relational SQL schema that mirrors ACES/PIES specifications**. Synthetic fixture datasets represent 10 common vehicle platforms and 50 repair operations, ensuring full compliance without pretending to possess a licensed live Auto Care Association subscription.

```sql
-- Relational representation of ACES / Supersession Schema
CREATE TABLE part_master (
    part_sku VARCHAR(64) PRIMARY KEY,
    brand_code VARCHAR(32) NOT NULL,
    part_terminology_id INT NOT NULL, -- PCdb standard
    description TEXT NOT NULL,
    part_tier VARCHAR(32) NOT NULL -- OEM_GENUINE, OEM_TIER2, AFTERMARKET_CAPA, AFTERMARKET_STD
);

CREATE TABLE oem_supersession_graph (
    predecessor_sku VARCHAR(64) REFERENCES part_master(part_sku),
    successor_sku VARCHAR(64) REFERENCES part_master(part_sku),
    supersession_type VARCHAR(16) NOT NULL, -- ONE_WAY, TWO_WAY
    effective_date DATE NOT NULL,
    PRIMARY KEY (predecessor_sku, successor_sku)
);

CREATE TABLE mandatory_companion_parts (
    primary_part_sku VARCHAR(64) REFERENCES part_master(part_sku),
    companion_part_sku VARCHAR(64) REFERENCES part_master(part_sku),
    required_quantity INT DEFAULT 1,
    is_mandatory BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (primary_part_sku, companion_part_sku)
);
```

---

## 4. Six Work-Order Categories & Warranty Policy Firewall

Warranty audits by automotive OEMs are notoriously strict. If an aftermarket part or uncertified substitute is billed to an OEM warranty repair order, the OEM will issue a **100% debit-back of parts and labor**, plus administrative penalty fines.

PartsRescue enforces a strict **Warranty Compliance Firewall** across six distinct work-order categories:

```
+========================================================================================================================+
|                                  SIX WORK-ORDER CATEGORIES & SOURCING RULES                                            |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| #  | Work-Order Category      | Funding Entity        | Permitted Part Tiers             | Compliance Enforcement      |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 01 | **Factory Warranty**     | Vehicle Manufacturer  | * OEM Genuine (Original)         | **STRICT OEM FIREWALL:**    |
|    |                          | (OEM)                 | * OEM Tier-2 (Omnicraft/bproauto)| Aftermarket parts strictly  |
|    |                          |                       |   *only if authorized by TSB*    | locked and hidden in UI.    |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 02 | **Safety Recall / Cam-** | OEM / Federal Highway | * OEM Genuine ONLY               | **ZERO SUBSTITUTION:** Even |
|    | **paign (NHTSA-gated)**  | Administration        |                                  | OEM Tier-2 prohibited.      |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 03 | **Extended Warranty /**  | Third-Party Warranty  | * OEM Genuine                    | Checks specific VSC policy: |
|    | **VSC Service Contract** | Administrator         | * CAPA Certified Aftermarket     | CAPA allowed if savings     |
|    |                          | (e.g. Zurich, Ally)   | * Certified Remanufactured       | exceed administrator rule.  |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 04 | **Customer-Pay (CP):**   | Vehicle Owner         | * OEM Genuine                    | Multi-tier presentation:    |
|    | **Maintenance / Wear**   | (Retail)              | * OEM Tier-2                     | Advisor can present OEM vs  |
|    |                          |                       | * Premium Tier-1 Aftermarket     | Aftermarket savings to cust.|
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 05 | **Customer-Pay (CP):**   | Vehicle Owner         | * OEM Genuine                    | Recommends OEM for critical |
|    | **Heavy Powertrain**     | (Retail)              | * OEM Remanufactured             | internals (timing, turbos)  |
|    |                          |                       | * Premium Tier-1 Aftermarket     | to protect dealer warranty. |
+----+--------------------------+-----------------------+----------------------------------+-----------------------------+
| 06 | **Internal / Used Car**  | Dealership Sales Dept | * Quality Certified Aftermarket  | Prioritizes speed and gross |
|    | **Reconditioning**       | (Internal RO)         | * Sister-Store OEM Transfer      | margin to ready vehicle for |
|    |                          |                       | * OEM Genuine                    | frontline retail sale.      |
+========================================================================================================================+
```

---

## 5. Six-State Deterministic Eligibility Decision Table

PartsRescue replaces brittle binary pass/fail logic with an auditable **Six-State Policy Eligibility Engine**. The engine evaluates explicit rules and traceable evidence, abstaining when documentation is incomplete:

```
+========================================================================================================================+
|                                    SIX-STATE FITMENT & ELIGIBILITY DECISION TABLE                                      |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| #  | Work-Order PayType | Candidate Part Tier  | Fitment & Evidence| Sourcing Channel      | Engine Decision & Action  |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 01 | FACTORY_WARRANTY   | OEM Genuine          | PASS (Exact/Succ) | Sister Store / PDC    | **VERIFIED ELIGIBLE:**    |
|    |                    |                      |                   |                       | Passed to decision engine.|
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 02 | FACTORY_WARRANTY   | OEM Tier-2           | PASS (TSB Waiver  | Sister / Commercial   | **CONDITIONAL ELIGIBILITY:**|
|    |                    | (Omnicraft/bproauto) | Documented)       |                       | Flagged with TSB waiver.  |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 03 | FACTORY_WARRANTY   | Aftermarket (CAPA)   | PASS (ACES Match) | Commercial Jobber     | **VERIFIED INELIGIBLE:**  |
|    |                    |                      | (No TSB Waiver)   |                       | Blocked to prevent audit. |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 04 | SAFETY_RECALL      | OEM Tier-2 / Aftermk | ANY               | ANY                   | **VERIFIED INELIGIBLE:**  |
|    |                    |                      |                   |                       | Mandatory OEM Genuine only|
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 05 | EXTENDED_VSC       | Aftermarket (CAPA)   | PASS (ACES Match) | Commercial Jobber     | **CONDITIONAL ELIGIBILITY:**|
|    |                    |                      |                   |                       | Requires Prior Auth (PA). |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 06 | CUSTOMER_PAY       | Premium Aftermarket  | PASS (ACES Match) | Commercial Jobber     | **VERIFIED ELIGIBLE:**    |
|    |                    |                      |                   |                       | (Requires customer SMS).  |
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 07 | ANY                | ANY                  | Missing Option RPO| ANY                   | **INSUFFICIENT INFO:**    |
|    |                    |                      |                   |                       | Prompts staff for RPO code|
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 08 | ANY                | ANY                  | Conflicting TSBs  | ANY                   | **CONFLICTING EVIDENCE:** |
|    |                    |                      |                   |                       | Escalates to Warranty Mgr.|
+----+--------------------+----------------------+-------------------+-----------------------+---------------------------+
| 09 | INTERNAL_RECON     | Quality Aftermarket  | PASS (ACES Match) | Commercial Jobber     | **VERIFIED ELIGIBLE:**    |
|    |                    |                      |                   |                       | Fast-track procurement.   |
+========================================================================================================================+
```

---

## 6. Verification & Traceability
- Eliminates legal and financial audit risks by enforcing hard warranty rules.
- Fully compatible with Tekion Parts Cloud data structures.
- Provides realistic synthetic grounding for ACES/PIES without commercial subscription dependencies.
