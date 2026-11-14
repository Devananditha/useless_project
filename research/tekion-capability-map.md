# Tekion Product Ecosystem & Capability Map

**Document Classification:** Phase 1 Master Research Deliverable  
**Project:** Tekion Tek-Qubit Hackathon 2026  
**Standards Compliance:** `.cursor/rules/research-standards.mdc` & `.cursor/rules/tekion-context.mdc`  
**Sources Referenced:** `research/source-register.md` (SRC-TEK-01 through SRC-TEK-11, SRC-TECH-01 through SRC-TECH-04)  
**Last Updated:** 2026-11-13  

---

## 1. Executive Summary

Tekion Inc. is an automotive retail technology unicorn (valued at >$4.0 Billion following a $200M growth capital round in July 2024 led by Dragoneer Investment Group) founded in 2016 by Jay Vijayan, former Chief Information Officer (CIO) of Tesla Motors. Headquartered in Pleasanton, California, with global technology centers in Bengaluru and Chennai, Tekion provides a multi-tenant, cloud-native Software-as-a-Service (SaaS) platform designed to modernize the legacy Dealer Management System (DMS) landscape.

As of late 2026, Tekion's software is deployed across **thousands of automotive retail rooftops and major dealer groups** (such as Ken Garff Automotive Group's ~70 stores and Asbury Automotive Group pilots), with secondary industry directories and Wikipedia citing deployments surpassing **3,000 locations** across the United States, Canada, the United Kingdom, France, and Germany. While this represents significant commercial momentum, Tekion remains an agile challenger in an industry where legacy duopolies (CDK Global and Reynolds and Reynolds) still control approximately 55% to 65%+ of the ~18,000 U.S. franchised dealership locations.

Tekion’s core value proposition rests on a modern cloud microservices architecture that unifies formerly fractured point solutions (DMS, CRM, Digital Retail, Fixed Operations, Parts, and Accounting) onto a synchronized, event-driven data core. In June 2026, at its inaugural *Tekion One* conference, the company accelerated its AI roadmap with the announcement of **T1 Pro** (a conversational AI interface and agent orchestrator) and its **Agentic AI Suite** (including specialized agents for sales, finance, accounts payable, and service).

This document establishes a factual, evidence-grounded baseline of Tekion’s product portfolio, operational capabilities, integration footprint, technical architecture, and documented limitations, distinguishing verified production features from recently announced marketing tiers.

---

## 2. Tekion Company and Platform Overview

### 2.1 Corporate Identity & Leadership
* **Founding:** 2016 in Pleasanton, California.
* **Founder & CEO:** Jay Vijayan. Prior to founding Tekion, Vijayan served as CIO at Tesla Motors (2012–2016), reporting directly to Elon Musk, where he led the design and build of Tesla’s end-to-end proprietary digital platform, ERP, and customer eCommerce systems. Vijayan previously held senior software engineering leadership roles at VMware and Oracle.
* **Capitalization & Valuation:** Over $635M in total funding raised. Attained unicorn status in October 2020 ($1B valuation) and achieved a **>$4.0B valuation** in July 2024 following a $200M growth financing round led by Dragoneer Investment Group. Key strategic investors include OEM venture arms (General Motors, BMW i Ventures, Hyundai Motor Company, Exor/Stellantis) alongside institutional investors (Index Ventures, Storm Ventures, Goldman Sachs).
* **Workforce & Operations:** Approximately 3,000+ employees globally. Corporate headquarters in Pleasanton, California; APAC headquarters and research centers in Bengaluru; primary software engineering campus in Chennai, India; regional sales and field operations across North America and Europe.

### 2.2 Cloud-Native Architecture & Technical Infrastructure
Contrary to oversimplified marketing claims of a "single monolithic relational database," Tekion’s underlying technical architecture is a modern, distributed microservices platform built on hyperscale cloud infrastructure, utilizing a **polyglot persistence data strategy**:

```
+----------------------------------------------------------------------------------------------------+
|                                    TEKION MULTI-CLOUD DATA TOPOLOGY                                 |
+----------------------------------------------------------------------------------------------------+
| PRESENTATION LAYER: Responsive Web (React), Mobile Apps (iOS/Android for Service & Lot Porters)   |
+----------------------------------------------------------------------------------------------------+
| ORCHESTRATION & AI: T1 Pro AI Orchestrator / Azure OpenAI Service (LLMs / Prompt Governance)       |
+----------------------------------------------------------------------------------------------------+
| MICROSERVICES COMPUTE: Azure Kubernetes Service (AKS) - Scalable Domain Microservices             |
|                        (Sales Engine, Desking Engine, Dispatch Engine, Accounting Ledger)           |
+----------------------------------------------------------------------------------------------------+
| POLYGLOT DATA PERSISTENCE:                                                                         |
| - Configuration & High-Availability NoSQL: Azure Cosmos DB (Flexible Schemas, Multi-Region Replic)|
| - Strict ACID Financial Transactions: Azure SQL (General Ledger, Invoicing, Zero Error Tolerance)  |
| - Relational Enterprise Data: Azure Database for PostgreSQL (Multi-tier Customer/Vehicle Records)  |
| - Analytics & Telemetry: ClickHouse Cloud (High-Throughput APM, Diagnostic & Operational Streaming)|
| - Event Bus / Messaging: Apache Kafka / Event Hubs (Event-Driven Real-Time Sync)                   |
+----------------------------------------------------------------------------------------------------+
| INTEGRATION LAYER: Automotive Partner Cloud (APC) RESTful APIs, Webhooks, STAR Standard XML        |
+----------------------------------------------------------------------------------------------------+
```

* **Compute & Containerization:** Deployed on **Azure Kubernetes Service (AKS)** (Microsoft Customer Story, 2024), enabling elastic scaling across multi-tenant dealer clusters with automated rolling updates and zero planned server downtime (averaging >3,000 feature updates deployed annually).
* **Transactional & Configuration Persistence:** Employs a polyglot persistence model:
  * **Azure Cosmos DB:** Used for critical system configurations, metadata, and high-availability operational services requiring flexible schemas and rapid zero-downtime upgrades.
  * **Azure SQL:** Utilized for scenarios requiring strict ACID transactional guarantees and data integrity for read/write operations with zero tolerance for errors (such as general ledger accounting, payments, and contract bookings).
  * **Azure Database for PostgreSQL:** Leveraged within the multi-tier data ecosystem to store and manage customer and enterprise relational records securely.
* **Operational Telemetry & Observability:** Leverages **ClickHouse Cloud** (ClickHouse case study, 2024) to ingest **1.2 million records per minute** (averaging ~20,000 events/second with sub-0.5s query response times) across real-time application performance monitoring (APM) metrics, customer telemetry events, and system audit logs.
* **AI & Machine Learning Infrastructure:** Integrates natively with **Microsoft Azure OpenAI Service** for secure, enterprise-governed large language model (LLM) execution, alongside proprietary computer vision models for document extraction and predictive ML pipelines for inventory pricing and maintenance forecasting.

---

## 3. Product Portfolio Overview

Tekion segments its commercial software offerings into three distinct platforms:

```
+----------------------------------------------------------------------------------------------------+
|                                      TEKION PRODUCT PLATFORMS                                      |
+----------------------------------------------------------------------------------------------------+
| 1. AUTOMOTIVE RETAIL CLOUD (ARC)                                                                    |
|    - The comprehensive Dealer Management System (DMS) for single and multi-rooftop dealerships.     |
|    - Natively integrates Sales, F&I, CRM, Fixed Operations, Parts, Inventory, and Accounting.      |
+----------------------------------------------------------------------------------------------------+
| 2. AUTOMOTIVE ENTERPRISE CLOUD (AEC)                                                                |
|    - Enterprise platform tailored for vehicle manufacturers (OEMs) and national mega-dealer groups.|
|    - Centralizes brand-wide inventory visibility, omnichannel online buying, and customer data.    |
+----------------------------------------------------------------------------------------------------+
| 3. AUTOMOTIVE PARTNER CLOUD (APC)                                                                   |
|    - The open API ecosystem and developer integration hub.                                         |
|    - Connects vetted third-party automotive software vendors, lenders, and hardware peripherals.    |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Product-by-Product Analysis

### 4.1 ARC Customer Relationship Management (CRM)
* **Core Functionality:** Natively embedded CRM sharing identical data records with the DMS. Replaces standalone dealership CRMs (e.g., VinSolutions, Elead).
* **Documented Capabilities:**
  * *Unified Customer Profile ("One View"):* Combines showroom sales history, digital shopping carts, service lane repair history, customer equity status, and accounting ledger records into a single live record.
  * *Intelligent Lead Routing:* Omnichannel lead ingestion (OEM leads, TrueCar, website forms) with rule-based routing, intent scoring, and response-time SLA tracking.
  * *Smart Communication & Summarization:* Built-in Azure OpenAI tools that analyze customer email/SMS threads, generate concise customer snapshots, and draft personalized email replies for BDC agents.
* **Target Stakeholders:** BDC Representatives, Internet Sales Directors, Sales Consultants, General Managers.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.2 ARC Digital Retail
* **Core Functionality:** Omnichannel consumer shopping engine designed for dealership and OEM brand websites.
* **Documented Capabilities:**
  * *Online-to-In-Store Deal Continuity:* Consumers configure trim, calculate monthly payments, value trade-ins, and apply for financing online. When visiting the dealership, showroom staff retrieve the exact session state on mobile tablets without re-keying data.
  * *Dynamic Payment Calculation:* Integrates vehicle price, OEM incentives, regional tax calculations, title fees, and lender credit tier rates.
  * *OEM Digital Storefront Integration:* Powers automaker direct-to-consumer digital desking initiatives, notably GM EV digital shopping portals and Toyota/Lexus SmartPath/MONOGRAM programs.
* **Target Stakeholders:** Car Buyers, Digital Marketing Directors, Sales Consultants.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.3 ARC Sales & Desking
* **Core Functionality:** Deal structuring, pricing negotiation, and gross profit optimization tool used at the dealership "sales desk."
* **Documented Capabilities:**
  * *Multi-Option Desking Matrix:* Generates side-by-side transaction comparisons (Cash, Finance, Lease) across multiple down payments and term durations.
  * *Inventory & Incentive Matching:* Real-time matching of active OEM customer cash rebates, dealer cash, and lease subsidies directly from factory data feeds.
  * *Mobile Showroom Desking:* Allows sales representatives to desk deals collaboratively with customers on tablets on the showroom floor, eliminating trips back and forth to the elevated sales desk.
* **Target Stakeholders:** Desk Managers, General Sales Managers (GSM), Sales Consultants.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.4 ARC Finance & Insurance (F&I)
* **Core Functionality:** Credit underwriting submission, protection product menu presentation, compliance enforcement, and digital deal jacket completion.
* **Documented Capabilities:**
  * *Lender Portal Connectivity:* Bi-directional data exchange with RouteOne and Dealertrack, submitting credit applications to captive and indirect auto lenders.
  * *Dynamic Interactive Menu:* Digital presentation of vehicle service contracts (VSC), GAP insurance, tire and wheel protection, and maintenance packages with transparent monthly payment recalculations.
  * *e-Contracting & Digital Signatures:* Remote and in-person electronic signature capture, eliminating physical paper signature pads.
  * *Automated Compliance Rules:* OFAC terrorist watch-list verification, Red Flags Rule identity checks, and Truth in Lending Act (TILA) disclosure audit trails.
* **Target Stakeholders:** F&I Managers, Finance Directors, Compliance Officers.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.5 ARC Digital Service Experience (DSE / Fixed Operations)
* **Core Functionality:** End-to-end service lane operational suite spanning online booking, service drive check-in, workshop dispatch, digital inspections, and customer payment.
* **Documented Capabilities:**
  * *Online & Mobile Scheduling:* 24/7 consumer appointment booking integrating transportation preferences (loaner, shuttle, waiting).
  * *Tablet & RFID Lane Check-In:* Service advisors conduct 360-degree vehicle walkarounds on iPads, capture photo/video documentation of pre-existing cosmetic damage, scan tire tread depths, and capture customer signatures. Compatible with RFID vehicle identification tags.
  * *Mobile Multi-Point Inspection (MPI):* Technicians document mechanical defects using photo and high-definition video, tagging inspection items as red (immediate attention), yellow (future attention), or green (pass).
  * *Two-Way Customer Approval & Messaging:* System automatically texts digital MPI reports with embedded technician video clips to the customer’s smartphone. Customers approve or decline individual repair lines with real-time pricing updates.
* **Target Stakeholders:** Service Advisors, Shop Foremen, Service Technicians, Service Directors.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.6 ARC Parts & Inventory Management
* **Core Functionality:** Vehicle inventory tracking (Variable Ops) and automotive replacement parts catalog and warehouse inventory management (Fixed Ops).
* **Documented Capabilities:**
  * *Vehicle Inventory Lifecycle:* Ingests trade-in acquisitions and auction purchases, tracks mechanical reconditioning milestones (Internal ROs), applies market pricing rules, generates window stickers, and syndicates listings to third-party portals (Autotrader, CarGurus, Cars.com).
  * *Parts Inventory Control:* Real-time parts inventory tracking across multiple warehouse bins, automated OEM stock reorder point calculations, emergency special order tracking (SOP), and core return management.
  * *Live Repair Order (RO) Allocation:* Seamlessly links parts billing directly to open technician RO lines; counter personnel or technicians assign parts without screen switching.
* **Target Stakeholders:** Used Car Managers, Inventory Merchandisers, Parts Managers, Back-Counter Personnel.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.7 ARC Accounting & Financial Management
* **Core Functionality:** Comprehensive general ledger, automotive chart of accounts, and financial statement generation.
* **Documented Capabilities:**
  * *Real-Time Continuous General Ledger:* Every closed transaction (vehicle deal funded, repair order paid, parts invoice billed) posts immediately to the general ledger, eliminating batch posting delays.
  * *Multi-Rooftop Enterprise Consolidation:* Provides consolidated balance sheets and profit-and-loss statements across multi-store dealer groups with drill-down audit trails.
  * *Automotive Payroll:* Native payroll calculation engine supporting complex automotive pay plans (technician flat-rate flagged hours, commission draw tiers, department gross profit splits).
  * *Factory Financial Statement Generation:* Formats and maps trial balance data into standardized OEM monthly financial statements for automated factory submission.
* **Target Stakeholders:** Dealership Controllers, Chief Financial Officers (CFO), Office Managers, Title Clerks.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

### 4.8 Ecosystem Extensions: Tekion Pay, Spend, and Analytics
* **Tekion Pay:** Fully embedded, PCI-compliant payment gateway supporting contactless in-store credit card terminals, text-to-pay SMS links, online portal payments, and integrated Point-of-Sale (POS) ledger reconciliation.
* **Tekion Spend:** Internal corporate card and expense management tool automating employee expense reimbursements and vendor payment approvals.
* **Tekion Analytics / Enterprise Dashboards:** Real-time business intelligence suite visualizing gross profit trends, sales closing ratios, customer retention metrics, technician labor efficiency, and dealership absorption rates across departments.
* **Commercial Status:** **FULLY DOCUMENTED & GENERALLY AVAILABLE (GA)**.

---

## 5. AI and Automation Capabilities: Current Reality vs. Announcements

Tekion brands its platform as "AI-Native." To maintain rigorous research integrity, this analysis strictly categorizes capabilities into **Field-Proven (Production GA)** vs. **Recently Announced / Commercial Rollout (June 2026)**:

```
+----------------------------------------------------------------------------------------------------+
|                                    TEKION AI CAPABILITY STATUS MATRIX                               |
+--------------------------------------+---------------------------------+---------------------------+
| AI CAPABILITY / AGENT                | FUNCTIONAL SCOPE                | VERIFIED STATUS           |
+--------------------------------------+---------------------------------+---------------------------+
| Smart Communication / Lead Snapshot  | LLM email/SMS summarization     | PRODUCTION GA (Azure OAI) |
| Digital MPI Note Translation         | Tech notes to customer text     | PRODUCTION GA             |
| Rule-Based Lead Scoring              | CRM lead prioritization         | PRODUCTION GA             |
| OCR Document Check                   | Basic file upload verification  | PRODUCTION GA             |
+--------------------------------------+---------------------------------+---------------------------+
| T1 Pro (Conversational Orchestrator) | Natural language system agent   | ANNOUNCED (June 2026)     |
| Salesperson AI                       | 24/7 autonomous BDC agent       | ANNOUNCED (June 2026)     |
| Deal Guard AI                        | Automated F&I compliance audit  | ANNOUNCED (June 2026)     |
| Accounts Payable AI (AP AI)          | Autonomous invoice coding to GL | ANNOUNCED (June 2026)     |
| Service Advisor AI                   | Proactive estimate voice agent  | ANNOUNCED (June 2026)     |
| Scheduler AI                         | Dynamic multi-variable booking  | ANNOUNCED (NADA 2025/26)  |
+--------------------------------------+---------------------------------+---------------------------+
```

### 5.1 Field-Proven Production AI Capabilities (GA)
* **Generative Communication Summaries:** Integrated directly into ARC CRM, leveraging Azure OpenAI Service to synthesize multi-message customer chat logs into a 3-bullet "Lead Snapshot," drafting suggested email responses based on vehicle specs and financing terms.
* **MPI Plain-Language Translation:** Converts cryptic technician acronyms (e.g., "R&R RF LCA bushing torn") into clear, consumer-friendly explanations with attached educational diagrams in the digital estimate.
* **Automated Lead Scoring:** Evaluates inbound leads across behavioral parameters (page visits, vehicle price tier, credit score soft pull) to route hot leads immediately to senior sales personnel.

### 5.2 Recently Announced Agentic AI Suite (June 16, 2026 – Tekion One)
Unveiled at the inaugural *Tekion One* conference in Las Vegas, these capabilities represent Tekion's current technological frontier. While demonstrated in live keynotes and entering phased customer deployment, independent third-party audit data verifying store-wide autonomous adoption rates remains limited:
* **T1 Pro (Agent Orchestrator):** Operates as an overarching conversational interface across ARC. Employees issue cross-departmental prompts (e.g., *"Show me all used SUVs in recon for more than 7 days and check if parts are pending"*), and T1 synthesizes the data and presents one-click execution actions.
* **Salesperson AI:** An autonomous agent capable of conducting multi-turn customer conversations over SMS and email, answering specific technical questions about vehicle trims, validating lot availability, and booking showroom test drives.
* **Deal Guard AI (part of the F&I AI suite):** Screens deal jackets prior to lender submission, automatically validates driver's licenses and insurance cards, cross-references buyer signatures and proof-of-income stipulations, and flags state compliance gaps to prevent contract funding rejections.
* **Accounts Payable AI (AP AI):** Scans vendor parts invoices via computer vision, matches invoice totals against DMS purchase orders, suggests appropriate chart-of-accounts GL coding, and routes invoices for approval.
* **Service Advisor AI & Scheduler AI:** Uses shop labor capacity models, technician skill matrices, and parts availability to schedule service visits and assist advisors in structuring upsell repair estimates.

> [!NOTE]
> **FUNCTIONAL BOUNDARY & DIFFERENTIATION ASSESSMENT (DEAL GUARD AI):**
> Comparing Deal Guard AI with official Theme 1 Use Case 2 (*Smart Document Extraction Agent: A tool that reads scanned title, registration, and insurance documents, validates the fields against state rules, and flags mismatches before deal finalization*) establishes an important functional boundary:
> - *Documented Overlap:* Deal Guard AI covers F&I checklist compliance, driver's license ID extraction, and insurance card presence checks.
> - *Differentiation Frontier:* Deep semantic OCR extraction on complex vehicle titles and registration certificates, automated field-level validation against 50 state statutory DMV titling rules, and multi-document discrepancy detection across titles and contracts are **not documented in Deal Guard AI**. Concepts in this use case must focus on these advanced document extraction and statutory DMV validation capabilities rather than basic deal checklist verification.

---

## 6. Integration Ecosystem & OEM Footprint

### 6.1 OEM Certifications
Dealership Management Systems require official factory certifications from Original Equipment Manufacturers (OEMs) to transmit warranty claims, order factory parts, receive vehicle allocations, and process factory financial statements. Tekion has achieved formal certified provider status across **more than 50 global OEM automotive brands**, including:
* **General Motors:** Chevrolet, Buick, GMC, Cadillac (includes GM EV Digital Retailing integration).
* **Toyota Motor North America:** Toyota and Lexus (powers the digital integration for Toyota SmartPath and Lexus Monogram).
* **Ford Motor Company:** Ford and Lincoln.
* **Stellantis:** Jeep, RAM, Dodge, Chrysler, Alfa Romeo, Fiat.
* **Hyundai Motor Group:** Hyundai, Kia (including Kia Canada certification), Genesis.
* **Nissan North America:** Nissan and Infiniti.
* **European Luxury Brands:** BMW, MINI, Mercedes-Benz, Audi, Porsche, Volkswagen, Volvo.

### 6.2 Automotive Partner Cloud (APC)
Unlike legacy DMS providers that have historically imposed steep certification fees and restrictive access programs on independent software vendors (ISVs), Tekion operates the **Automotive Partner Cloud (APC)**. APC provides modern RESTful APIs, webhook subscription architecture, and standardized data exchange (aligned with Standards for Technology in Automotive Retail - STAR) covering:
* Vehicle Inventory (read/write syndication).
* Customer & Lead Objects (bi-directional CRM sync).
* Repair Orders & Appointments (read/write service data).
* Financial Transactions & Invoicing (accounting integration).

---

## 7. Publicly Documented Limitations and Research Unknowns

Applying rigorous evidentiary standards, several operational boundaries and informational gaps are identified:

1. **Market Penetration vs. Legacy Incumbents:** Tekion's ~3,000 retail rooftops constitute single-digit market share (~3% to 5%) in North America. Long-term 3- to 5-year enterprise contracts, legacy IT inertia, and high migration switching costs at multi-rooftop groups mean CDK and Reynolds retain deep operational moats.
2. **Third-Party API Rate Limits and Egress Policies:** Public technical documentation does not disclose specific API rate limits, latency SLAs, or data egress fees for high-volume third-party software developers on APC.
3. **Internal Production Rollout Depth of Agentic AI:** While the capabilities of T1 Pro, Deal Guard AI, and Salesperson AI are thoroughly documented in official June 2026 launch materials, the percentage of active stores running these tools in full autonomous mode (vs. human-supervised pilot mode) is not publicly disclosed.
4. **Dedicated Sustainability Telemetry Gaps:** While Tekion provides comprehensive paperless operations (e-contracting, digital deal jackets, mobile MPI), public product documentation reveals **no dedicated operational carbon footprint accounting engine**, no native dealership energy/facility telemetry, and no standalone used EV battery health diagnostic pricing tool.
5. **Cross-Border DMV Direct Integration Feasibility:** Real-time programmatic title verification across all 50 U.S. state DMVs remains fragmented due to public government infrastructure limitations, meaning document validation still encounters manual verification checkpoints.

---

## 8. Capability Mapping Matrix

This matrix applies the required Phase 1 evaluation framework across core dealership business areas:

*Classifications:*
- **FULLY DOCUMENTED:** Direct public evidence of general availability and production deployment.
- **PARTIALLY DOCUMENTED:** Documented in product architecture, but key operational parameters are unverified.
- **ANNOUNCED:** Publicly unveiled and actively marketed (e.g., June 2026 Tekion One), but production maturity unverified.
- **NOT ESTABLISHED:** Insufficient public technical evidence to establish existence.
- **NOT APPLICABLE:** No logical relationship to the product domain.

| Business Area | Dealership Problem | Tekion Product | Documented Capability | Evidence Status | Confidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sales & CRM** | Inbound leads sit uncontacted after hours; slow response times cause lost sales. | ARC CRM / Salesperson AI | 24/7 automated lead response, context-aware vehicle specs, appointment booking via text/email. | **ANNOUNCED** (T1 Suite 2026); Basic automated email/SMS is **FULLY DOCUMENTED**. | High |
| **Sales & CRM** | Re-interviewing customers in showroom because online cart does not sync with store. | ARC Digital Retail + CRM | Single customer profile ("One View"); seamless cart transfer from web to mobile sales tablet. | **FULLY DOCUMENTED** (SRC-TEK-05, SRC-TEK-06) | High |
| **F&I** | Contract funding delays (CIT) due to missing signatures, incorrect fees, or bad stips. | ARC F&I / Deal Guard AI | Automated deal jacket pre-audit, signature completeness validation, compliance rule checks. | **ANNOUNCED** (Deal Guard AI, 2026); eSign/eContracting is **FULLY DOCUMENTED**. | High |
| **F&I** | First-time buyers overwhelmed by complex lease vs finance calculations and disclosures. | ARC Digital Retail / F&I | Interactive payment sliders, basic payment term disclosures. (Conversational plain-language buyer co-pilot is not native). | **PARTIALLY DOCUMENTED** | Medium |
| **Fixed Operations** | Morning drive congestion; long advisor queues typing paper repair orders. | ARC Service (DSE) | Mobile tablet check-in, 360-degree walkaround photos, RFID lane vehicle recognition. | **FULLY DOCUMENTED** (SRC-TEK-04) | High |
| **Fixed Operations** | Technicians idle waiting 1–3 hours for phone approval on discovered MPI repair items. | ARC Service (DSE) | Digital MPI with technician video clips texted directly to customer; one-click mobile approval. | **FULLY DOCUMENTED** (SRC-TEK-04, SRC-TEK-09) | High |
| **Fixed Operations** | RO stalls on a missing part; bay sits idle while foreman manually reassigns work. | ARC Service / Scheduler AI | Basic technician skill dispatching and shop capacity scheduling. Dynamic multi-agent resequencing on parts failure is unestablished. | **PARTIALLY DOCUMENTED** | Medium |
| **Parts Management** | Disconnected parts inventory; technicians walking to back counter to check shelf stock. | ARC Parts Management | Real-time parts inventory tracking linked directly to active RO lines on advisor/technician screens. | **FULLY DOCUMENTED** (SRC-TEK-01) | High |
| **Accounting** | 5 to 10-day month-end accounting close; manual batch posting of daily transactions. | ARC Accounting | Real-time continuous general ledger posting; instant financial statement trial balance generation. | **FULLY DOCUMENTED** (SRC-TEK-07) | High |
| **Back Office** | Clerks manually keying hundreds of vendor parts invoices and matching PO numbers. | ARC Accounting / AP AI | Computer vision scanning of paper/PDF invoices, automated PO matching, GL code recommendations. | **ANNOUNCED** (AP AI, June 2026) | High |
| **Inventory** | Used vehicles aging on lot beyond predicted turn; manual price discounting erodes gross. | ARC Inventory Management | Dynamic market pricing rules, inventory syndication. Automated causal diagnostic explainer is absent. | **PARTIALLY DOCUMENTED** | High |
| **Sustainability** | Dealership paper and toner waste from massive 40-page physical deal jackets. | ARC Paperless Deal Jacket | 100% digital e-contracting, document vaulting, paperless deal jacket storage. | **FULLY DOCUMENTED** (SRC-TEK-01) | High |
| **Sustainability / EV** | Used EV trade-in appraisal opacity; fear of battery degradation causing mispricing. | ARC Inventory / Appraisal | Standard vehicle valuation (VIN decode, mileage, cosmetic recon). Native battery health diagnostic integration is not established. | **NOT ESTABLISHED** | High |
| **Sustainability / Ops**| Tracking Scope 1 & 2 carbon emissions from dealership facilities, loaners, and logistics. | None documented | No dedicated dealership carbon accounting or ESG tracking product exists in Tekion’s public suite. | **NOT ESTABLISHED** | High |

---

## 9. Evidence-Backed Conclusions

1. **Tekion is an Established Cloud Leader with Agile Scale:** Tekion has successfully proven the viability of a cloud-native, microservices-driven DMS architecture across >3,000 retail dealerships and >50 OEM brands. It is no longer an unproven startup, but a scaled platform with verified commercial presence.
2. **True Structural Differentiation vs. Legacy Incumbents:** Tekion’s primary competitive moat against CDK Global and Reynolds and Reynolds is its single, synchronized data core. By eliminating the need for separate CRMs, standalone desking tools, and third-party fixed ops point solutions, Tekion reduces data friction, eliminates batch sync delays, and removes third-party integration access taxes.
3. **AI Leadership Balanced by Phased Commercial Maturation:** Tekion’s June 2026 announcement of T1 Pro and its Agentic AI Suite positions the company at the vanguard of automotive retail AI. However, research integrity requires treating these specialized agents as cutting-edge additions currently scaling across the customer base, rather than commoditized, long-standing production tools.
4. **Potential Opportunities Aligned with Hackathon Themes (Not Yet Verified in Mainstream DMS):** Tekion's existing product coverage reveals operational territory representing potential opportunities that directly match the official hackathon use cases in `references/tekion-themes.pdf`:
   * *Fixed Operations Autonomous Resequencing:* Extending static scheduling into dynamic, multi-agent shop re-dispatching when parts delays occur (Theme 1, Potential Opportunity — Not Yet Verified).
   * *Used EV Battery Valuation Intelligence:* Bridging high-voltage battery diagnostic telemetry into trade-in valuation (Theme 4, Potential Opportunity — Not Yet Verified in Native DMS).
   * *Operational ESG & Carbon Telemetry:* Quantifying facility and fleet carbon emissions within the dealership management layer (Theme 4, Potential Opportunity — Not Yet Verified).
   * *Explainable Used Inventory Analytics:* Diagnosing root causes for vehicle aging beyond crude price slashes (Theme 2, Potential Opportunity — Not Yet Verified).

---
*End of Tekion Capability Map.*
