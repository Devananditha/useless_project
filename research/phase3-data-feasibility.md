# Phase 3 Data Feasibility, Availability Classifications, and Privacy Architecture

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/phase3-data-feasibility.md`  
**Stage:** Phase 3 – Opportunity Identification & Concept Generation  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and Phase 3 Directives  
**Purpose:** Technical data feasibility assessment mapping inputs, availability categories, synthetic data requirements, API boundaries, and regulatory compliance (GLBA, FTC Safeguards) across all 12 concepts.

---

## 1. Standardized Data Availability Taxonomy

Every data input utilized across Phase 3 concepts is classified into one of six standardized availability categories:
1. **Confirmed Public Data:** Authoritative external datasets, official state statutes, public DMV vehicle code regulations, federal truth-in-mileage rules, and publicly published trade benchmarks.
2. **Confirmed Internal Tekion Capability:** Data structures natively maintained and documented in Tekion Automotive Retail Cloud (ARC), Automotive Enterprise Cloud (AEC), Tekion Digital Processing (TDP), or Deal Guard AI.
3. **Assumed Internal DMS Data:** Standard relational entities present across major commercial automotive DMS platforms (CDK Drive, Reynolds ERA-IGNITE, Tekion ARC) based on industry standards (e.g. STAR XML / VMRS standards).
4. **External Integration Required:** Data feeds requiring active third-party commercial API licenses, B2B supplier partnerships, or external web scraping (e.g. aftermarket repair pricing, live on-demand courier dispatch, regional wholesale inventory networks).
5. **Synthetic Demonstration Data:** Plausible, domain-grounded artificial data generated to model operational distributions for hackathon demonstration purposes without accessing real dealership PII.
6. **Unknown:** Data fields whose availability, frequency, or schema structure cannot be verified from public or developer documentation.

---

## 2. Concept-by-Concept Data Feasibility Mapping

| Concept ID & Name | Required Data Inputs | Data Availability Classification | Extraction Method & Latency | Synthetic Generation Feasibility | Privacy & Regulatory Constraints |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A1: CadenceGuard** | RO open/close timestamps, odometer in/out, customer ID, vehicle VIN, op-codes (VMRS), make/model baseline intervals. | **Confirmed Internal Tekion Capability** / **Assumed Internal DMS Data** | Tabular SQL / REST API query to DMS historical RO ledger (<50ms). | **High**: Gamma-distribution mileage generator + OEM service interval map. | **GLBA / PII**: Customer contact records and VINs must be anonymized or hashed (`Customer_ID_001`). |
| **A2: ReviveRO** | Electronic MPI inspection lines, technician notes (`Concern_Cause_Correction`), declined repair quote dollars, op-codes, mileage. | **Confirmed Internal Tekion Capability** (Tekion DSE eMPI tables) | NLP entity extraction from unstructured text; tabular eMPI line fetch (<100ms). | **High**: Synthetic eMPI inspection sheets with pre-built declined brake/tire lines. | **Low**: Internal dealership inspection logs; zero third-party data sharing. |
| **A3: FairRate AI** | Dealership CP labor door rate, parts menu pricing, regional aftermarket labor/parts estimates by 3-digit zip code. | **External Integration Required** (Aftermarket pricing) / **Assumed Internal DMS Data** (Menu pricing) | Web scraping / API calls to public repair estimate portals (RepairPal, AAA) (<500ms). | **High**: Static regional pricing benchmark table (e.g. 5 metro areas across 10 wear ops). | **Low**: Publicly published commercial pricing; zero consumer PII involved. |
| **A4: RetentionOpt** | Customer total historical spend (Sales + Service), gross margin per customer, monthly retention marketing budget, loaner fleet capacity. | **Confirmed Internal Tekion Capability** (Tekion Accounting & CRM One View) | Internal SQL aggregate queries against accounting ledger and loaner asset tables (<200ms). | **High**: Synthetic customer spending distribution with Pareto 80/20 LTV curves. | **Moderate**: Financial spend figures must remain internal to dealership management. |
| **B1: StageGate Dispatch** | Active RO labor lines, OEM parts catalog BOMs, shelf bin inventory counts, pick-and-scan barcode events. | **Confirmed Internal Tekion Capability** (Tekion ARC Parts & Service modules) | Real-time webhook on barcode scan; sub-second deterministic rule validation (<10ms). | **Very High**: Synthetic parts catalog with 20 repair BOMs and simulated bin stock. | **Zero**: Operational warehouse and repair order data; zero PII. |
| **B2: PartsOrchestrator AI** | Multi-store DMS inventory APIs, local parts distributor B2B catalogs, courier transit time/cost APIs, active RO promise times. | **Confirmed Internal Tekion Capability** (Multi-store view) / **External Integration Required** (Courier & B2B APIs) | REST API queries across multi-store inventory endpoints and logistics APIs (<1.5s). | **High**: Simulated 3-store dealer network with synthetic courier transit matrices. | **Zero**: B2B supply chain and logistics metadata. |
| **B3: BayFlow Dynamic** | Shop lift asset registry (lift type, capacity), technician skill roster, active RO clock status, parts arrival ETAs, vehicle mobility flag. | **Confirmed Internal Tekion Capability** (Tekion ARC Service Bay asset table) | Discrete-event simulation state fetch; sub-3-second CP-SAT solve time. | **Very High**: Simulated 25-bay shop floor with predefined technician skill profiles. | **Zero**: Shop floor operational and physical asset metadata. |
| **B4: FairFlag Dispatch** | Technician historical flag efficiency by op-code, weekly cumulative flag hours per tech, flat-rate guarantee thresholds, certified skills. | **Confirmed Internal Tekion Capability** (Tekion Payroll & Technician Performance tables) | Internal SQL query to technician payroll ledger and daily dispatch logs (<50ms). | **High**: Synthetic technician roster with varying skill tiers and historical flag counts. | **Internal HR**: Technician compensation records require role-based access control (RBAC). |
| **C1: CrossBorder TitleGuard** | Scanned PDF deal jackets (Title, Bill of Sale, Credit App, POA), destination state/county DMV statutory rule tables. | **Confirmed Public Data** (State DMV motor vehicle codes) / **Confirmed Internal Tekion Capability** (Deal jacket PDFs) | Vision-Language Model (VLM) structured extraction (3–6s) + AST rule evaluation (<5ms). | **Extremely High**: Pre-cooked synthetic scanned deal jackets with authentic DMV forms. | **FTC Safeguards Rule / GLBA**: Scanned buyer IDs, SSNs, and credit applications must be masked/redacted. |
| **C2: DealJacket Reconciler** | Scanned multi-page deal jacket PDFs, core DMS deal desking ledger numbers (selling price, down payment, trade allowance, VIN). | **Confirmed Internal Tekion Capability** (Tekion Digital Deal repository) | Multimodal VLM extraction + Levenshtein fuzzy string matching + ISO 3779 checksum (<4s). | **Extremely High**: Synthetic multi-document deal packets with intentional clerical typos. | **FTC Safeguards Rule**: Synthetic customer names and addresses used for demonstration. |
| **C3: DMV RiskScorer** | Historical dealership title submission logs, DMV rejection reason codes, transaction metadata (sale type, buyer state/county, lienholder ID). | **Assumed Internal DMS Data** / **Confirmed Public Data** (State processing turnaround times) | Tabular ML inference (LightGBM/XGBoost) running on deal metadata (<30ms). | **High**: Synthetic log of 1,000 historical title filings with authentic DMV rejection reason codes. | **Low**: Historical administrative metadata; zero credit or financial PII. |
| **C4: TitleFlow Orchestrator** | Scanned deal jacket images, document field bounding boxes, DMS customer/vehicle records, clerk audit decision logs. | **Confirmed Internal Tekion Capability** (Tekion ARC Business Office repository) | VLM visual bounding-box coordinate extraction + real-time WebSocket UI stream (<3s). | **Very High**: Scanned PDF deal jackets paired with pre-extracted bounding-box overlays. | **FTC Safeguards Rule**: Redaction overlays applied to sensitive PII before rendering in demo UI. |

---

## 3. Synthetic Demonstration Data Engineering Plan

Because a 2–4 person hackathon team cannot legally or operationally ingest live dealership production databases containing real consumer Non-Public Personal Information (NPI), all demonstration prototypes must be powered by **authoritative synthetic datasets**:

### Candidate A Synthetic Pipeline (Customer Service Churn)
* **Dataset Structure:** 2,500 synthetic customer accounts, 3,200 vehicles, and 18,000 historical repair order lines spanning a 48-month synthetic timeline.
* **Domain Grounding:**
  - Mileage progression generated via Gamma distributions ($\alpha=4.5, \beta=3000$) matching national driving averages (~13,500 miles/year).
  - VMRS op-codes mapped to authentic OEM operations: `044-001` (Front Brakes), `015-002` (Synthetic Oil Service), `022-005` (Automatic Transmission Flush), `017-003` (Tire Rotation & Balance).
  - Synthetic defection injected at Month 36 to simulate the post-warranty cliff, with a controllable subset exhibiting pre-defection interval stretching.

### Candidate B Synthetic Pipeline (In-Bay Parts Stalls & Dispatch)
* **Dataset Structure:** Simulated mid-sized dealership workshop: 25 service bays (18 2-post lifts, 4 flat bays, 2 alignment racks, 1 EV high-voltage bay) and 35 technicians across 4 skill certification tiers.
* **Domain Grounding:**
  - 80 daily repair orders with authentic flat-rate book times (sampled from standard Mitchell/ALLDATA labor times).
  - Parts catalog bill-of-materials linking op-codes to primary and secondary part numbers.
  - Discrete event shock injection: 15% probability of mid-repair secondary parts backorders to demonstrate dynamic OR-Tools CP-SAT resequencing.

### Candidate C Synthetic Pipeline (Multi-State Title Validation)
* **Dataset Structure:** Complete scanned PDF deal packets across the **California – Nevada – Arizona (CA-NV-AZ)** sales corridor.
* **Domain Grounding:**
  - Real public state DMV form templates: California Form REG 343 (*Application for Title or Registration*), Nevada Form VP-222 (*Application for Vehicle Registration*), Arizona Form 96-0236 (*Title and Registration Application*).
  - Synthetic buyer identities (e.g. "Jane Doe", "Robert J. Smith") with generated driver's licenses, standard Retail Installment Sale Contracts (RISC 553 form), and fictitious insurance binders.
  - Pre-engineered error test cases: VIN digit transposition, missing California smog certificate for an Arizona-imported vehicle, and missing Arizona notarized Power of Attorney.

---

## 4. Privacy, Security, and Regulatory Governance (GLBA & FTC Safeguards)

Dealership technology operates under strict federal regulatory frameworks governing consumer financial privacy:
1. **Gramm-Leach-Bliley Act (GLBA) & FTC Safeguards Rule (16 CFR Part 314):**
   - *Requirement:* Dealerships must protect Non-Public Personal Information (NPI), including credit scores, loan payoff balances, social security numbers, and driver's license numbers.
   - *Architectural Safeguard:* Concepts A1, A4, C1, and C2 must implement **client-side PII masking and tokenization**. Scanned document processing via Vision LLMs must execute with strict zero-data-retention (ZDR) API agreements, ensuring consumer documents are never stored or used for model training.
2. **Fair Credit Reporting Act (FCRA) Compliance:**
   - *Requirement:* Dealers cannot pull credit scores or loan balances without permissible purpose.
   - *Architectural Safeguard:* Concept A1 and A4 strictly operate on internal dealership transaction history (repair orders and sales gross), completely bypassing external credit bureau soft-pulls or per-diem loan payoff queries.
3. **Telephone Consumer Protection Act (TCPA) Compliance:**
   - *Requirement:* Automated marketing texts or win-back communications require documented consumer express written consent.
   - *Architectural Safeguard:* Concepts A1 and A2 must cross-reference DMS communication opt-in flags (`SMS_Consent == True`) before queuing automated retention messages.
