# Phase 4.2 Hackathon Demonstration Feasibility Audit & Core Scenario Specification

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.2-demo-feasibility-audit.md`  
**Stage:** Phase 4.2 – Final Evidence Correction & Readiness Audit  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and Phase 3.2 Authoritative Corrections  
**Audit Authorities:** AI/ML Solution Architect, Senior Product Strategist, Independent Innovation Critic  
**Date of Audit:** November 14, 2026  
**Audit Determination:** **FEASIBLE FOR 2–4 PERSON TEAM (SCOPED TO 3 SCENARIOS)**  

---

## 1. Executive Feasibility Assessment

In a 5-minute hackathon presentation, demonstrating an overly broad, disconnected set of features (e.g., attempting live DMV API queries, full DMS database synchronizations, and 50-state tax calculations) guarantees execution failure.

This audit establishes a **minimal, coherent demonstration architecture** proving one complete end-to-end operational workflow:
$$\text{Scanned Deal Jacket Ingestion} \longrightarrow \text{Multimodal VLM Perception} \longrightarrow \text{Deterministic Statutory AST Evaluation} \longrightarrow \text{Visual Defect Overlays} \longrightarrow \text{Human Escalation}$$

### 1.1 Feasibility Classification for 2–4 Person Student Team
* **Perception Engine:** Readily achievable using Claude 3.5 Sonnet Vision or GPT-4o Vision API with structured JSON outputs governed by a standardized Pydantic model.
* **Deterministic AST Rule Engine:** Lightweight, highly performant Python evaluation script executing in $< 50\text{ milliseconds}$ over extracted JSON.
* **Demonstration UI:** A clean, responsive React / Vite or Streamlit split-screen interface displaying source PDF canvases on the left with SVG bounding box overlays on the right.
* **Zero WAN Dependency Fallback:** A local containerized FastAPI mock server pre-loaded with synthetic responses safeguards the presentation against conference Wi-Fi latency.

---

## 2. Feature Scope Classification

To prevent feature creep, all demonstration capabilities are strictly partitioned across three delivery tiers:

```
+========================================================================================================+
|                                  DEMO CAPABILITY PARTITIONING MATRIX                                   |
+=============================================+==========================================================+
| Feature Category                            | Technical Scope & Hackathon Role                         |
+=============================================+==========================================================+
| **TIER 1: MANDATORY CORE DEMO**             | 1. Synthetic Deal Jacket PDF Ingestion (Drag-and-drop).  |
| *(Proves the Complete Operational Workflow)*| 2. Multimodal VLM Extraction (Key fields + 2D coords).   |
|                                             | 3. Cross-Document Parity (49 CFR § 565.15 VIN Checksum). |
|                                             | 4. Deterministic AST Statutory Evaluation (CA-NV-AZ).    |
|                                             | 5. Visual Defect Annotation (Red bounding box overlays). |
|                                             | 6. Tactile Ambiguity Modal (Dry-embossed seal check).    |
+---------------------------------------------+----------------------------------------------------------+
| **TIER 2: OPTIONAL DEMO EXTENSIONS**        | 7. Local Offline Mock Fallback (`Ctrl+Shift+M`).         |
| *(Presentation Safety Harness)*             | 8. Downloadable PDF Pre-Audit Summary Report.            |
+---------------------------------------------+----------------------------------------------------------+
| **TIER 3: FUTURE PRODUCTION ROADMAP**       | 9. Tekion Deal Guard AI Webhook Dispatch.                |
| *(Explicitly Out of Live Demo Scope)*       | 10. External RFC 3161 Timestamping / WORM Storage.       |
|                                             | 11. Live State DMV Database / NMVTIS Queries.            |
|                                             | 12. Automated Electronic Lien (ELT) Bank Payoffs.        |
+=============================================+==========================================================+
```

---

## 3. The Three Core Demonstration Scenarios

The live demonstration is strictly constrained to **three standardized, synthetic test scenarios** demonstrating: (1) compliant pass, (2) planted statutory defect, and (3) safe human escalation:

```
+----------------------------------------------------------------------------------------------------+
|                                    THREE CORE DEMONSTRATION SCENARIOS                              |
|                                                                                                    |
|  [ Scenario 1: Clean Pass ]    [ Scenario 2: Planted Defect ]      [ Scenario 3: Ambiguous Seal ]  |
|  Synthetic AZ Title + BOS      Synthetic AZ Bill of Sale           Synthetic Older NV Title        |
|  Status: PRE_AUDIT_PASS        Status: CRITICAL_DEFECT_DETECTED    Status: TACTILE_ESCALATION      |
|  Result: 100% Green Badge      Result: Red Box + A.R.S. § 28-2058  Result: Modal to Title Clerk    |
+----------------------------------------------------------------------------------------------------+
```

---

### Scenario 1: Compliant Interstate Acquisition (Clean Pre-Audit Pass)
* **Synthetic Input Document:** `deal_jacket_AZ_clean.pdf` (Synthetic 2-page document containing an Arizona Certificate of Title and matching ADOT Form 48-2004 Bill of Sale, featuring clean signatures and a licensed dealer ATP witness stamp).
* **Expected Extracted Fields:**
  * VIN: `1HGCR2F83HA019482` (17 characters; Mod-11 Check-Digit valid per 49 CFR § 565.15).
  * Vehicle: 2017 Honda Accord EX-L.
  * Seller Name: "Eleanor Marie Vance".
  * Buyer Name: "Desert Sky Motors LLC" (Dealer License #AZ-D9021).
  * Odometer Reading: 68,412 miles; Status: "Actual Mileage".
  * Notary / Witness Block: `witness_type: "ATP_OFFICER"`, `witness_present: true`.
* **Deterministic Validation Rules Applied:**
  * `FED-ODO-01`: Model year 2017 subject to 20-year rolling rule ($2026 - 2017 = 9 < 20$); valid actual disclosure $\rightarrow$ **PASS**.
  * `AZ-TITLE-01`: Arizona title certificate assignment section properly executed $\rightarrow$ **PASS**.
  * `AZ-BOS-02`: Form 48-2004 witnessed by authorized ATP officer pursuant to A.R.S. § 28-370 $\rightarrow$ **PASS**.
  * `AZ-DEALER-04`: Licensed dealer endorsement recorded with valid license number $\rightarrow$ **PASS**.
* **Expected Result:** Status badge: **`PRE_AUDIT_PASS (No Detected Discrepancies)`**.
* **Human Escalation:** None required. System enables "Export Pre-Audit Summary".
* **What Judge Observes:** Rapid, frictionless processing (<8 seconds); split-screen interface displaying source PDF with green highlight overlays and an all-pass statutory checklist.
* **What is Mocked vs Live:**
  * *Live:* VLM field extraction and AST rule evaluation.
  * *Mocked / Simulated:* Upstream DMS deal creation webhook.

---

### Scenario 2: Planted Statutory Defect (Missing Notary / Witness on AZ Bill of Sale)
* **Synthetic Input Document:** `deal_jacket_AZ_defect.pdf` (Synthetic 2-page document where seller Eleanor Vance signed ADOT Form 48-2004 Bill of Sale, but the notary acknowledgment jurat is blank and no ATP witness signature is present).
* **Expected Extracted Fields:**
  * Seller Signature: `present: true`.
  * Notary Jurat Text: `present: false`.
  * Notary Seal Impression: `present: false`.
  * ATP Witness Signature: `present: false`.
* **Deterministic Validation Rules Applied:**
  * `AZ-BOS-02`: A.R.S. § 28-2058 and ADOT Form 48-2004 mandate that bill of sale signatures must be notarized OR witnessed by an authorized MVD/ATP agent pursuant to A.R.S. § 28-370. Condition not satisfied $\rightarrow$ **FATAL DEFECT DETECTED**.
* **Expected Result:** Status banner: **`CRITICAL DEFECT DETECTED: Missing Mandatory Notary or Witness Acknowledgment`**.
* **Human Escalation & Actionable Remediation:**
  * System locks deal clearance and presents the F&I Desk Remediation Panel:
    * *Option A:* Execute on-site notarization before the customer departs the showroom (Notary on duty: J. Miller, Office #104).
    * *Option B:* Have dealership licensed ATP representative witness the seller's signature pursuant to A.R.S. § 28-370.
* **What Judge Observes:** UI immediately scrolls to Page 2 Section C, draws a crisp **red bounding box** around the empty notary/witness block, cites **A.R.S. § 28-2058 / § 28-370**, and displays the calculated financial CIT freeze risk ($32,450).
* **What is Mocked vs Live:**
  * *Live:* Visual bounding box coordinate rendering and AST rule violation trigger.
  * *Mocked:* Dealership employee directory lookup for on-duty notary.

---

### Scenario 3: Physical Ambiguity Handling (Nevada Dry-Embossed Notary Seal)
* **Synthetic Input Document:** `deal_jacket_NV_emboss.pdf` (Synthetic 1-page scan of an older Nevada Certificate of Title containing printed notary jurat text and signature, but featuring a low-contrast circular artifact representing an un-inked, colorless raised dry-embossed crimp seal).
* **Expected Extracted Fields:**
  * Notary Text: `present: true`.
  * Commission Expiry: `valid (2027)`.
  * Optical Seal Confidence: `0.58` (Low contrast circular pattern detected; below $0.85$ optical certainty floor).
* **Deterministic Validation Rules Applied:**
  * System identifies physical artifact that cannot be certified optically under flatbed scanning conditions $\rightarrow$ Triggers **`AMBIGUOUS_AUDIT_CONDITION`**.
* **Expected Result:** Amber Warning Banner: **`VERIFICATION REQUIRED: Potential Dry-Embossed Seal Detected`**.
* **Human Escalation Workflow:**
  * An interactive modal prompt appears for the Title Clerk:
    > *"Optical flatbed scanning cannot reliably verify colorless raised dry-embossed notary crimp seals. Please perform tactile inspection on the original paper title. Does the physical document contain a raised embossed impression over the notary signature?"*
  * Presenter clicks **"Confirm Physical Embossed Seal Present"** and inputs Clerk ID (`TC-4091`).
  * System logs the manual override with timestamp and transitions status to **`PRE_AUDIT_PASS (Tactile Verification Confirmed)`**.
* **What Judge Observes:** Proves engineering maturity and real-world domain knowledge. Shows that the system never hallucinates compliance on physical artifacts it cannot optically prove, safely keeping a human in the loop.
* **What is Mocked vs Live:**
  * *Live:* Low-contrast detection thresholding and escalation modal trigger.
  * *Mocked:* Clerk physical paper handling.

---

## 4. Technical Feasibility & Runtime Safeguards

| Component / Risk | Student Implementation Architecture | Contingency Fallback Harness |
| :--- | :--- | :--- |
| **Model Latency (>10s API Spike)** | Asynchronous extraction queue with progressive UI rendering. | Standby local FastAPI mock server pre-loaded with synthetic responses (`Ctrl+Shift+M`). UI displays `[DEMO SIMULATION MODE ENGAGED]`. |
| **Pydantic Schema Parsing Error** | Strict JSON mode prompting with regex pre-validation. | Deterministic fixture failover; logs extraction error for immediate manual clerk review. |
| **Local Environment Compatibility** | Containerized Docker Compose or lightweight Python virtual environment running Streamlit / Vite. | Zero WAN network required; entire stack runs locally on presentation laptop. |

---

## 5. Audit Conclusion on Demo Feasibility

1. **Perfect Hackathon Fit:** Constraining the demonstration to these three tightly specified scenarios eliminates technical overreach while delivering maximum visual impact within the 5-minute presentation window.
2. **Clear Judge Takeaways:**
   * *Scenario 1 proves automated speed (<8s).*
   * *Scenario 2 proves deep statutory domain intelligence (cites A.R.S. § 28-2058).*
   * *Scenario 3 proves safety and human-in-the-loop integrity (dry-emboss handling).*
