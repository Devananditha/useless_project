# CrossBorder TitleGuard: Product Acceptance Criteria & Test Matrix

**Document Version:** 1.0  
**Phase:** 4 — Final Concept Selection, Product Definition & Scope Freeze  
**Concept Reference:** Concept C1 — CrossBorder TitleGuard  
**Status:** Approved Specification  
**Authority:** AI Solution Architect & Technical Review Committee  

---

## 1. Acceptance Criteria Framework

This document establishes the empirical evaluation framework, quantitative performance benchmarks, and a 12-scenario Product Acceptance Test (PAT) Benchmark Specification for **CrossBorder TitleGuard**.

> [!IMPORTANT]
> **Integrity Notice on Prototype Status:** In strict compliance with `.cursor/rules/research-standards.mdc` and hackathon governance, **no application prototype has yet been coded or executed in this workspace**. The figures below distinguish engineering target specifications from planned verification benchmarks. They must NOT be treated as empirical measurements from an already-built software system.

To ensure absolute methodological integrity under `.cursor/rules/research-standards.mdc`, metrics are categorized into three strictly separated tiers:
1. **Tier 1: Hackathon Demo Target Specification:** Required performance thresholds for the 5-minute live hackathon presentation.
2. **Tier 2: Planned Verification Benchmark (Engineering Estimates):** Target baseline performance to be measured across synthetic test fixtures when prototype coding is authorized.
3. **Tier 3: Future Commercial Production KPIs:** Operational goals targeted for multi-dealership pilot deployments integrated with Tekion Deal Guard AI.

---

## 2. Quantitative Performance Benchmarks

| Metric Dimension | Tier 1: Hackathon Demo Target | Tier 2: Planned Verification Benchmark | Tier 3: Commercial Production KPI | Verification Method |
| :--- | :---: | :---: | :---: | :--- |
| **Field Extraction Accuracy** | $\ge 92.0\%$ | $\ge 94.0\%$ (Target on test docs) | $\ge 98.5\%$ | Field-level exact match vs human ground-truth annotation. |
| **VIN Extraction & Checksum** | $100.0\%$ (Mod-11 Valid) | $100.0\%$ | $100.0\%$ | 49 CFR § 565.15 Mod-11 check-digit algorithm. |
| **Defect Detection Recall** | $\ge 95.0\%$ | $\ge 96.0\%$ (Target defect catch) | $\ge 99.0\%$ | Proportion of intentional statutory defects successfully flagged. |
| **False Positive Alarm Rate** | $< 5.0\%$ | $< 4.0\%$ (Target on clean docs) | $< 1.5\%$ | Proportion of compliant documents incorrectly flagged with fatal defects. |
| **Statutory Citation Correctness**| $100.0\%$ | $100.0\%$ | $100.0\%$ | Exact string match against frozen AST legal rule catalogue. |
| **Jacket Processing Latency** | $< 15.0\text{ sec}$ | $< 10.0\text{ sec}$ (Target on Sonnet 3.5)| $< 6.0\text{ sec}$ | End-to-end time from ingestion to visual overlay render. |
| **Tactile Ambiguity Escalation** | $100.0\%$ Route to Clerk | $100.0\%$ Routed to Modal | $100.0\%$ Escalation | Dry-emboss / low-contrast seals must never be auto-approved. |
| **Export Payload Compliance** | $100.0\%$ Valid Schema | $100.0\%$ Valid JSON | $100.0\%$ Webhook Success | Automated Pydantic model validation against Tekion API schema. |

---

## 3. The 12-Scenario Product Acceptance Test (PAT) Benchmark Specification

The following 12 test scenarios represent the planned acceptance benchmark suite covering clean transactions, planted statutory violations, multi-state discrepancies, edge-case entity variants, and human escalation workflows across California, Nevada, and Arizona. These define the exact reproducible test fixtures to be evaluated upon prototype implementation:

```
+----------------------------------------------------------------------------------------------------+
|                                    12-SCENARIO ACCEPTANCE MATRIX                                   |
|                                                                                                    |
|  [ Clean Trades ]        [ Statutory Defects ]       [ Identity / Odo Mismatch ]  [ Edge Cases ]   |
|  - PAT-01 (Clean AZ)     - PAT-04 (AZ Missing Notary)- PAT-07 (VIN Transposition) - PAT-10 (NV Seal) |
|  - PAT-02 (Clean NV)     - PAT-05 (CA Smog Expired)  - PAT-08 (Odo Rollback)      - PAT-11 (POA)   |
|  - PAT-03 (Clean CA)     - PAT-06 (AZ Over-15-Day)   - PAT-09 (Legal Name Shift)  - PAT-12 (Alter) |
+----------------------------------------------------------------------------------------------------+
```

---

### PAT-01: Standard Clean Arizona Trade-in
- **Scenario:** Customer trades in clear-titled 2018 Ford F-150 with Arizona title and valid Form 48-2004 Bill of Sale signed before a licensed dealer witness.
- **Input Documents:** 2-page PDF (AZ Certificate of Title + ADOT Form 48-2004).
- **Expected Extraction:** VIN `1FTFW1E84JK109281`, Odometer 54,210, Owner "Marcus Aurelius Vance", Dealer Witness Stamp present.
- **Expected Statutory Evaluation:** Rules `FED-ODO-01`, `AZ-TITLE-01`, `AZ-BOS-02`, and `AZ-DEALER-04` evaluate to `PASS`.
- **Expected Exception Handling:** Zero fatal alerts. Green "Compliant Deal Jacket" status.
- **Human Review Behavior:** None required. System enables "Export to Tekion".
- **Pass/Fail Criteria:** All fields extracted correctly; 0 false positive alerts; processing time $< 10\text{ sec}$.

### PAT-02: Standard Clean Nevada-to-Arizona Interstate Acquisition
- **Scenario:** Dealership acquires 2020 Toyota RAV4 from Las Vegas private seller with clean Nevada title and secure Nevada reassignment.
- **Input Documents:** 2-page PDF (NV Certificate of Title Form VP222 + Bill of Sale VP104).
- **Expected Extraction:** VIN `2T3C1RFV8LC091823`, Odometer 38,400, Notary ink stamp detected with valid commission expiry date (2027).
- **Expected Statutory Evaluation:** Rules `FED-ODO-01`, `NV-REASSIGN-01`, and `NV-BOS-02` evaluate to `PASS`.
- **Expected Exception Handling:** Status: Green Compliant.
- **Human Review Behavior:** Automated clearance; no manual override requested.
- **Pass/Fail Criteria:** Correct interstate tax reciprocity tag generated; zero false alerts.

### PAT-03: Standard Clean California In-State Retail Trade
- **Scenario:** California dealer acquires 2019 Chevrolet Silverado trade-in with clean California title and recent smog certificate.
- **Input Documents:** 3-page PDF (CA Title Reg 227 + Reg 262 Power of Attorney + BAR Smog Certificate issued 18 days prior).
- **Expected Extraction:** VIN `1GCEYCEK9KZ198234`, Odometer 61,050, Smog Cert issue date within 90 days.
- **Expected Statutory Evaluation:** Rules `FED-ODO-01`, `CA-SMOG-01`, `CA-REASSIGN-03` evaluate to `PASS`.
- **Expected Exception Handling:** Status: Green Compliant.
- **Human Review Behavior:** Automated clearance.
- **Pass/Fail Criteria:** Smog 90-day validity window verified mathematically; 0 errors.

---

### PAT-04: Planted Defect — Arizona Bill of Sale Lacks Notary / Witness (A.R.S. § 28-2058)
- **Scenario:** Seller Eleanor Vance signs ADOT Form 48-2004 Bill of Sale in private showroom without notary present; dealer witness block is left blank.
- **Input Documents:** 2-page PDF (AZ Title + Unnotarized Form 48-2004).
- **Expected Extraction:** Seller signature detected; Notary Jurat `present: False`; Authorized Witness `present: False`.
- **Expected Statutory Evaluation:** Rule `AZ-BOS-02` evaluates to `FATAL_VIOLATION`.
- **Expected Exception Handling:** Red Critical Alert Banner: "Missing Notary or Authorized Witness Acknowledgment".
- **Human Review Behavior:** Screen locks export to Tekion; presents actionable options: (1) Execute on-site notarization, (2) Execute dealer ATP witness.
- **Pass/Fail Criteria:** 100% defect capture; red bounding box rendered over Section C; exact citation to A.R.S. § 28-2058 displayed.

### PAT-05: Planted Defect — Expired California Smog Certification (Cal. Veh. Code § 4000.1)
- **Scenario:** Customer-held California trade-in includes a smog certification inspection dated 114 days prior to sale date (exceeds statutory 90-day limit).
- **Input Documents:** 2-page PDF (CA Title + BAR Smog Vehicle Inspection Report).
- **Expected Extraction:** Smog test date: `2025-10-12`; Transaction intake date: `2026-02-03` ($\Delta = 114\text{ days}$).
- **Expected Statutory Evaluation:** Rule `CA-SMOG-01` evaluates to `FATAL_VIOLATION` ($114 > 90$).
- **Expected Exception Handling:** Red Alert: "Smog Certification Expired (>90 Days Old)".
- **Human Review Behavior:** Recommends immediate routing of trade-in to dealership service bay for re-smog before retail offering.
- **Pass/Fail Criteria:** Exact day differential calculated; prevents DMV rejection at CA DMV registration.

### PAT-06: Planted Defect — Arizona Application Timeline Exceeded (A.R.S. § 28-2051)
- **Scenario:** Dealership intake clerk processes title signed by previous individual seller 22 days ago without prior dealer transfer recording.
- **Input Documents:** 1-page PDF (AZ Certificate of Title with seller release date signed 22 days prior).
- **Expected Extraction:** Seller signature date: `Day T - 22`. Current date: `Day T`. Elapsed: 22 days.
- **Expected Statutory Evaluation:** Rule `AZ-TITLE-01` flags statutory timeline penalty warning under A.R.S. § 28-2051 ($22 > 15\text{ days}$).
- **Expected Exception Handling:** Amber Operational Warning: "Statutory 15-Day Title Transfer Window Exceeded — Mandatory Late Penalty Fee ($8.00) Applicable".
- **Human Review Behavior:** Title clerk must acknowledge fee adjustment in deal accounting jacket.
- **Pass/Fail Criteria:** Warning triggered accurately without misidentifying rule as an outright refusal to transfer.

---

### PAT-07: Cross-Document Discrepancy — VIN Transposition Error
- **Scenario:** Dealer salesperson manually entered VIN into DMS deal file with single-character typo (`1HGCR2F83HA019482` on Title vs `1HGCR2F83HA019428` in DMS).
- **Input Documents:** 1-page PDF Title + DMS Deal Metadata JSON payload.
- **Expected Extraction:** Title VIN extracted and ISO 3779 checksum verified as mathematically valid.
- **Expected Statutory Evaluation:** Cross-Document Parity Engine flags exact character mismatch at positions 16–17.
- **Expected Exception Handling:** Red Critical Alert: "VIN Mismatch Between Scanned Physical Title and DMS Deal Record".
- **Human Review Behavior:** Visual split-screen displays side-by-side comparison; allows one-click update to sync DMS record to verified physical title.
- **Pass/Fail Criteria:** Flags discrepancy instantly; prevents funding rejection from automotive floorplan lender.

### PAT-08: Cross-Document Discrepancy — Odometer Rollback / Inversion
- **Scenario:** Previous state title record displays 84,200 miles; current trade-in odometer declaration lists 72,100 miles without "Exceeds Mechanical Limits" box checked.
- **Input Documents:** 2-page PDF (Title with historical mileage + Current Odometer Disclosure Statement).
- **Expected Extraction:** Historical mileage: 84,200; Disclosed mileage: 72,100; Status: "Actual Mileage".
- **Expected Statutory Evaluation:** Rule `FED-ODO-02` flags `CRITICAL_FRAUD_RISK` (Monotonic progression violated: $\Delta = -12,100\text{ miles}$).
- **Expected Exception Handling:** Flashing Red Alert: "Federal Odometer Discrepancy: Declared Mileage Lower Than Prior Historical Title Record".
- **Human Review Behavior:** Deal automatically escalated to General Sales Manager / Compliance Officer; deal funding hold instituted.
- **Pass/Fail Criteria:** Zero tolerance for mileage reversal; flags 100% of negative delta disclosures.

### PAT-09: Entity Discrepancy — Legal Name Variation & Married Name Shift
- **Scenario:** Arizona Title is registered to "Eleanor Marie Vance", but Bill of Sale and Driver's License list "Eleanor Vance-Castillo".
- **Input Documents:** 2-page PDF (Title + Form 48-2004 Bill of Sale).
- **Expected Extraction:** Title Name: `ELEANOR MARIE VANCE`; Bill of Sale Name: `ELEANOR VANCE-CASTILLO`.
- **Expected Statutory Evaluation:** Parity Engine calculates Jaro-Winkler distance ($0.81$); identifies non-identical surname.
- **Expected Exception Handling:** Amber Warning: "Entity Name Discrepancy: Additional Supporting Documentation Required".
- **Human Review Behavior:** System triggers prompt: "Attach Marriage Certificate, Court Decree, or ADOT One-and-the-Same Affidavit (Form 48-2004 Sec. D)".
- **Pass/Fail Criteria:** Distinguishes minor typo (auto-cleared) from substantive surname change requiring legal affidavit.

---

### PAT-10: Ambiguity & Human Escalation — Nevada Colorless Dry-Embossed Notary Seal
- **Scenario:** Older Nevada Certificate of Title contains authentic raised dry-embossed circular notary seal, appearing on a 300 DPI flatbed scanner as a faint shadow with unreadable lettering.
- **Input Documents:** 1-page high-resolution scan of older Nevada title.
- **Expected Extraction:** Notary signature present; VLM circular seal detection confidence $= 0.58$ (below $0.85$ automated confidence floor).
- **Expected Statutory Evaluation:** System classifies information state as `AMBIGUOUS_AUDIT_CONDITION`.
- **Expected Exception Handling:** Amber Escalation Modal: "Potential Raised Dry-Embossed Seal Detected — Digital Certification Prohibited".
- **Human Review Behavior:** Interactive prompt instructs Title Clerk to perform physical tactile verification on the original paper title; Clerk enters Clerk ID and clicks "Confirm Embossed Seal Present".
- **Pass/Fail Criteria:** System NEVER auto-approves or auto-fails low-contrast embossed seals; routes 100% to verified tactile workflow.

### PAT-11: Edge Case — Secure Vehicle Power of Attorney (CA Reg 262)
- **Scenario:** Customer trade-in executed via California Reg 262 Power of Attorney because physical paper title is stored in safe deposit box.
- **Input Documents:** 1-page PDF (CA Reg 262 Secure POA and Odometer Disclosure).
- **Expected Extraction:** Attorney-in-Fact appointment, customer signature, odometer reading, and secure paper serial number.
- **Expected Statutory Evaluation:** Rule `CA-REASSIGN-03` verifies Reg 262 compliance; confirms buyer and seller are not signed by the same individual in violating capacities.
- **Expected Exception Handling:** Status: Green Compliant (with tag: "Pending Original Paper Title Receipt").
- **Human Review Behavior:** Automated validation of POA clauses.
- **Pass/Fail Criteria:** Validates dual-purpose POA/Odometer disclosure without requiring duplicate disclosures.

### PAT-12: Defect — Uncertified Alteration / White-Out Erasure on Title
- **Scenario:** Seller accidentally wrote incorrect purchase price, crossed it out with pen, and wrote correct price above without obtaining state-approved notary affidavit of correction.
- **Input Documents:** 1-page PDF Title with visible strike-through in assignment box.
- **Expected Extraction:** VLM detects visual alteration/strike-through bounding box in Assignment Block 1; `alteration_detected: True`.
- **Expected Statutory Evaluation:** Rule `CA-ALTER-02` / `AZ-TITLE-01` flags `FATAL_ALTERATION_DEFECT` (Uncertified alteration voids title assignment).
- **Expected Exception Handling:** Red Critical Alert: "Title Assignment Voided by Uncertified Alteration / Strike-Through".
- **Human Review Behavior:** Directs F&I desk to execute State Statement of Error / Affidavit of Correction signed by seller before departure.
- **Pass/Fail Criteria:** Captures strike-throughs and correction fluid marks; cites exact state voiding statute.

---

## 4. Test Suite Summary & Acceptance Criteria Benchmark Governance

To achieve formal validation upon prototype implementation, the CrossBorder TitleGuard system will be evaluated against the following benchmark thresholds across the 12-scenario specification:

| Validation Category | Scenarios Specified | Target Benchmark Threshold | Verification Governance Status | Prototype Gate Requirement |
| :--- | :---: | :---: | :---: | :---: |
| **Clean Transactions** | PAT-01, PAT-02, PAT-03 | $100\%$ Pass, 0 False Alerts | Benchmark Defined | Mandatory Gate 1 |
| **Fatal Statutory Defects** | PAT-04, PAT-05, PAT-06, PAT-12 | $100\%$ Detection Rate | Benchmark Defined | Mandatory Gate 2 |
| **Parity & Fraud Discrepancies** | PAT-07, PAT-08, PAT-09 | $100\%$ Discrepancies Flagged | Benchmark Defined | Mandatory Gate 3 |
| **Edge Cases & Ambiguity** | PAT-10, PAT-11 | $100\%$ Escalated to Human | Benchmark Defined | Mandatory Gate 4 |

**Conclusion:** The 12-scenario benchmark specification provides an objective, reproducible evaluation standard. CrossBorder TitleGuard satisfies all conceptual acceptance requirements and is ready for Phase 5 Six-Slide Presentation narrative architecture.
