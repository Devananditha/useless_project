# Phase 4.4 Patent and Novelty Audit: Reassessment of Yendo Inc. (WO 2026/030477 A1 / US 2026/0038039 A1) vs TitleGuard

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.4-patent-and-novelty-audit.md`  
**Stage:** Phase 4.4 – Final Concept Integrity, Comparative Validation & Decision Gate  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Audit Authorities:** Patent and Competitive Intelligence Research Analyst, AI/ML Solutions Architect, Independent Innovation Red-Team Evaluator  
**Date of Audit:** November 14, 2026  
**Audit Finding:** **MATERIAL TECHNICAL OVERLAP IDENTIFIED; FREEDOM-TO-OPERATE CANNOT BE DECLARED WITHOUT QUALIFIED COUNSEL; SCOPE STRICTLY CONSTRAINED TO CA–NV–AZ CORRIDOR**

---

## 1. Bibliographic Reference & Verified Patent Scope

This audit reassesses the published patent application family held by **Yendo Inc.**, correcting prior characterizations in Phase 4.3 that prematurely dismissed patent overlap.

```
+========================================================================================================+
|                                    VERIFIED PATENT BIBLIOGRAPHIC RECORD                                |
+=========================+==============================================================================+
| **Publication Number**  | US 2026/0038039 A1 / WO 2026/030477 A1                                       |
| **Publication Date**    | February 5, 2026 (Published application; not an issued, granted patent)       |
| **Filing Date**         | July 30, 2025 (PCT / US National Application)                                 |
| **Priority Date**       | July 31, 2024 (US Provisional Application 63/677,XXX)                        |
| **Assignee / Applicant**| Yendo Inc. (Dallas, Texas, USA)                                              |
| **Title**               | Machine Learning Based Vehicle Title Validation                              |
| **Inventors**           | Jordan Miller, Aaron Sengstacken                                             |
| **CPC Classifications** | G06V 30/1916 (Text/document recognition), G06Q 40/02 (Financial underwriting)|
| **Source Citation**     | Justia Patents / USPTO Patent Center Publication US20260038039A1 [Feb 2026]  |
+=========================+==============================================================================+
```

---

## 2. Independent Reassessment of Independent Claim 1

### 2.1 Earlier Erroneous Characterization in Phase 4.3
The Phase 4.3 report characterized US 2026/0038039 A1 / WO 2026/030477 A1 as strictly an "asset-backed consumer credit underwriting method" and asserted:
* *"TitleGuard has zero infringement risk."*
* *"Independent Claim 1 is expressly limited to revolving credit lines."*
* *"Freedom to operate is established."*

**Correction:** Under rigorous re-audit of the published abstract and independent claim architecture, this characterization was **incomplete and legally premature**. 

### 2.2 Actual Published Claim 1 Structure & Scope
The core independent claims of US 2026/0038039 A1 are drawn broadly to a **computer-implemented method and system for vehicle title data extraction and validation**:
1. **Physical Title Image Capture:** Receiving, via a user interface on a client device, an image of a physical vehicle title.
2. **OCR Extraction:** Applying optical character recognition to extract text from the title image.
3. **Multimodal Input Construction:** Preprocessing to construct a multi-modal input tensor comprising the image, the OCR output, and schema-based structured data templates.
4. **Machine-Learned Extraction:** Feeding the tensor into a machine-learned model that outputs a structured data object comprising vehicle, title, and ownership information.
5. **Validation Cross-Referencing:** A validation module cross-referencing the output with external title records to generate validation metadata.
6. **Predetermined Actions:** Performing predetermined actions based on the validation (e.g., executing notifications, issuing alerts, or updating transaction workflows).

### 2.3 Downstream Applications Disclosed in Specification
Crucially, the patent specification of US 2026/0038039 A1 is **not** limited to consumer credit card underwriting. The specification expressly discloses downstream applications including:
* Automotive dealerships and used-car retailers verifying trade-in vehicles.
* Wholesale automotive auctions checking title transfer eligibility.
* Vehicle salvage and remarketing entities auditing title status.

Therefore, dismissing Yendo's patent as "irrelevant to dealerships" is factually unsupported.

---

## 3. Claim-Element Comparison Table: Yendo Disclosure vs TitleGuard

The table below contrasts each element of US 2026/0038039 A1 against TitleGuard's proposed architecture:

| Patent Claim Element | Yendo Disclosure | TitleGuard Equivalent | Difference | Residual Overlap |
|---|---|---|---|---|
| **1. Image Ingestion** | User uploads physical title image via client device interface. | Salesperson scans physical title via showroom scanner / tablet. | Form factor (mobile app vs desktop scanner). | **Direct overlap** on digital title image intake. |
| **2. OCR & Layout Extraction** | OCR module extracts text and token locations from image. | Multimodal VLM (Claude 3.5 / GPT-4o) extracts tokens & boxes. | Implementation (OCR engine vs modern VLM API). | **Direct overlap** on text/bounding box extraction. |
| **3. Multimodal Tensor Construction** | Preprocessing constructs tensor combining image, OCR, & schema templates. | Prompt pipeline feeds image + JSON schema to VLM. | Technical representation (tensor embedding vs prompt schema). | **Substantial overlap** on multimodal schema guidance. |
| **4. Structured Entity Extraction** | ML model outputs structured object: vehicle, title, owner data. | VLM outputs structured JSON: VIN, owner, title #, odometer. | Model weights (custom CNN/transformer vs frontier VLM). | **Direct overlap** on structured field extraction. |
| **5. External Title Record Retrieval** | Queries external title databases (state DMVs, NMVTIS, ELT) for metadata. | **None.** TitleGuard operates locally without live DMV APIs. | **Major architectural difference:** Yendo calls external DBs; TitleGuard is local. | **Zero overlap** on external registry queries. |
| **6. Reference Validation Rules** | Validates extracted data against external reference metadata and rules. | Deterministic AST checks data against corridor statutory rules (CA-NV-AZ). | Rule domain: Yendo checks external registry match; TitleGuard checks statutory law. | **Partial overlap** on automated rule evaluation. |
| **7. Predetermined Downstream Action** | Automated actions: lien registration, user notification, or credit limit. | Displays non-blocking UI alert and pre-fills corrective statutory forms. | Action domain (commercial credit vs dealership showroom alert). | **Functional overlap** on triggering alerts from validation. |
| **8. Multi-Document Deal Jacket** | Specification notes single title document verification. | Cross-audits packet: Title + Bill of Sale + POA + Reassignment. | Scope: TitleGuard cross-validates relational integrity across 4 documents. | **No direct overlap** in Yendo independent claims. |
| **9. Statutory Cross-Border Logic** | Specification focuses on title validity and encumbrances. | Checks corridor transfer rules (A.R.S. § 28-2058, CVC § 5753, 49 CFR § 580.17). | Scope: Domain-specific state statutory transfer compliance. | **No direct overlap** in Yendo claims. |

---

## 4. Legal Categories & Evidentiary Distinctions

Under strict research standards, we distinguish the following categories:

1. **Independent Claim Language:** Broadly covers multimodal ML ingestion, structured title extraction, reference validation, and automated actions.
2. **Dependent Claim Limitations:** Cover specific mobile capture framing, edge guide overlays, microprint/intaglio classification, and specific financial underwriting workflows.
3. **Specification Examples:** Disclose broader industry applicability across used-car retailers, auction houses, and salvage companies.
4. **TitleGuard's Proposed Features:** Showroom intake pre-audit, deal jacket cross-referencing, zero external DMV queries, and tri-state corridor transfer compliance.
5. **Actual Technical Differentiation:**
   * *Relational Deal Jacket Verification:* Cross-referencing names, VINs, and signatures across physical title, Bill of Sale, Power of Attorney, and Reassignment forms.
   * *Offline / Local AST Statutory Logic:* Evaluating transfer legality without relying on third-party DMV API connections.
6. **Legal Conclusions That Cannot Be Established:**
   * This academic/hackathon review **cannot** establish Freedom to Operate (FTO).
   * This review **cannot** make formal legal determinations of patent validity, non-infringement, or doctrine of equivalents.
   * **Mandatory Standard Language Adopted:**  
     > *"Potential technical overlap identified; claim construction and freedom-to-operate assessment require qualified patent counsel."*

---

## 5. Technical Significance of TitleGuard's Differences

We critically evaluate whether TitleGuard's differentiators represent fundamental technical innovation:

1. **Absence of External DMV/NMVTIS Calls:**
   * *Technical Reality:* While this eliminates external API dependencies and latency, it is an **architectural reduction** rather than an inventive technical leap. It also creates a severe operational blind spot: TitleGuard cannot verify current legal title status or undisclosed liens.
2. **Multi-Document Relational Cross-Verification:**
   * *Technical Reality:* Extracting fields from four documents instead of one is a **valuable workflow extension**, but technically relies on the same VLM prompting and string comparison primitives.
3. **Jurisdiction-Specific Statutory Processing:**
   * *Technical Reality:* Implementing Boolean statutory logic (e.g., if origin is AZ and sale is private, verify notary presence) is standard legal-engineering / AST evaluation. It is domain-valuable, but not a novel machine learning architecture.

---

## 6. Strict Scope Restriction: California–Nevada–Arizona Corridor

TitleGuard's scope is strictly bounded to the previously approved **tri-state corridor**:
* **California:** Cal. Veh. Code § 5753 (uncertified alterations, REG 227 requirements, REG 262 power of attorney).
* **Nevada:** NRS 482.400 / 482.415 (dry-embossed state seal handling, VP104 bill of sale requirements).
* **Arizona:** A.R.S. § 28-2058 (seller signature notarization / authorized witness mandates, MVD Form 48-1004).
* **Federal Baseline:** 49 CFR § 580.17 (20-year rolling odometer disclosure exemption).

> [!CAUTION]
> **SCOPE ENFORCEMENT:** Any claims asserting that TitleGuard possesses a "proprietary 50-state AST compilation" or "nationwide automated titling engine" are **expressly revoked**. No 50-state engine has been authored, verified, or approved. TitleGuard is strictly an initial three-state corridor proof-of-concept.

---

## 7. Re-Calibrated Novelty Evaluation

* **Prior Novelty Score (Phase 4.3):** 4.35 / 5.00
* **Phase 4.4 Re-Calibrated Score:** **3.90 / 5.00** (-0.45 adjustment)
* **Evidentiary Justification:** 
  1. Multimodal title parsing and structured extraction are directly claimed in published patent art (US 2026/0038039 A1).
  2. The application of VLM prompting to document schemas is an established industry practice.
  3. TitleGuard's genuine novelty is restricted to its **dealership showroom workflow positioning** and its **curated tri-state statutory transfer heuristics**.
