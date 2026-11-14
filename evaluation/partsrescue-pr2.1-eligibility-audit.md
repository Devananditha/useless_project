# PartsRescue PR2.1: Warranty & Part Eligibility Policy Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-eligibility-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** Automotive Parts and Service Domain Expert, Technical Red-Team Reviewer  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Mandate

In Phase PR2, `architecture/partsrescue-pr2-fitment-and-eligibility-engine.md` established blanket compliance rules:
> *"Factory Warranty = OEM Genuine Only; 100% rejection of aftermarket."*  
> *"Safety Recall = Zero substitution by federal law."*

While intended to protect dealerships against OEM claim debit-backs, these blanket statements ignored established automotive industry realities documented in Phase PR1.1 (`partsrescue-pr1.1-warranty-eligibility.md`):
1. **OEM Tier-2 Product Lines:** Major vehicle manufacturers operate authorized Tier-2 parts lines (e.g., Ford Omnicraft/Motorcraft, GM ACDelco Gold/Silver, Stellantis bproauto) that are explicitly approved for certain warranty repairs, customer-satisfaction campaigns, or backorder concessions when covered by Technical Service Bulletins (TSBs).
2. **Third-Party Vehicle Service Contracts (VSC):** Extended warranty administrators (e.g., Zurich, Ally, JM&A) often *mandate* the use of CAPA-certified aftermarket or remanufactured parts if the wholesale cost is lower than OEM list price.
3. **Emergency OEM Shortage Waivers:** During acute national supply chain shortages, OEMs periodically issue administrative bulletins authorizing dealers to procure specific aftermarket alternatives with prior authorization codes.
4. **Binary Fallacy:** Treating eligibility as a simple binary (PASS/FAIL) fails in real operations when policy documentation is incomplete, outdated, or ambiguous.

---

## 2. The 6-State Policy Eligibility Model

PartsRescue PR2.1 replaces the brittle binary firewall with an auditable **Six-State Eligibility Model**:

```
+========================================================================================================================+
|                                    SIX-STATE WARRANTY & POLICY ELIGIBILITY MODEL                                       |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| #  | Eligibility State        | System Definition     | Operational System Action & UI Behavior                        |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 01 | **VERIFIED ELIGIBLE**    | Direct match against  | Candidate passes to Optimization Engine. Green badge displayed |
|    |                          | approved OEM/VSC rules| with policy citation (e.g., "GM Warranty Policy Sec. 4.2").    |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 02 | **VERIFIED INELIGIBLE**  | Explicitly prohibited | Candidate pruned from primary recommendation. Red badge with   |
|    |                          | by OEM warranty policy| explanation (e.g., "Non-OEM component prohibited under factory |
|    |                          |                       | warranty claim #RO-104928").                                   |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 03 | **CONDITIONAL            | Permitted ONLY with   | Candidate flagged in UI with mandatory prerequisite:           |
|    | ELIGIBILITY**            | supporting concession | "Requires TSB #24-081 validation" or "Requires Prior           |
|    |                          | or prior authorization| Authorization (PA) code from VSC administrator."               |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 04 | **INSUFFICIENT           | Missing vehicle option| Candidate held in pending triage. Prompts counterperson:       |
|    | INFORMATION**            | code or policy ruleset| "Verify vehicle build code (RPO J55 vs J56) to confirm fitment."|
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 05 | **CONFLICTING POLICY     | OEM manual and local  | System abstains from ranking candidate. Alerts Warranty Admin: |
|    | EVIDENCE**               | bulletin disagree     | "Conflicting guidance between OEM Core Manual and TSB 23-11."  |
+----+--------------------------+-----------------------+----------------------------------------------------------------+
| 06 | **HUMAN REVIEW           | High-dollar repair or | Locks automated procurement. Requires Warranty Administrator  |
|    | REQUIRED**               | edge-case powertrain  | or Parts Manager explicit electronic checkoff.                 |
+========================================================================================================================+
```

---

## 3. Separation of Eligibility Dimensions

To prevent logic errors, the eligibility engine evaluates seven independent criteria before assigning a state:

```
                                  +===================================+
                                  |     Eligibility Evaluation Core   |
                                  +===================================+
                                                    |
         +-----------------+-----------------+------+------------+-----------------+-----------------+
         |                 |                 |                   |                 |                 |
         v                 v                 v                   v                 v                 v
   +-----------+     +-----------+     +-----------+       +-----------+     +-----------+     +-----------+
   |   Repair  |     | Applicable|     |  Vehicle  |       |   Part    |     | Shortage  |     | Sourcing  |
   |  Category |     |OEM Policy |     | Warranty  |       | Category  |     |Concession |     | Channel   |
   | (Warr/CP) |     |  Manual   |     | Remaining |       |(OEM/Tier2)|     | (TSB/PA)  |     |  Status   |
   +-----------+     +-----------+     +-----------+       +-----------+     +-----------+     +-----------+
```

1. **Repair Category:** Distinguishes OEM Factory Bumper-to-Bumper, OEM Powertrain, Federal Safety Recall, Third-Party Extended VSC, Retail Customer-Pay, and Internal Reconditioning.
2. **Applicable OEM Policy Manual:** Specific to the vehicle brand (Ford, GM, Toyota, Stellantis); rules are not identical across manufacturers.
3. **Vehicle Warranty Term:** Compares vehicle in-service date and mileage against OEM warranty limits. If the vehicle is outside warranty, it defaults to Customer-Pay rules regardless of customer perception.
4. **Part Brand & Quality Tier:** OEM Genuine, OEM Approved Tier-2 (Omnicraft/ACDelco), Certified Aftermarket (CAPA), Commercial Jobber Standard, or Remanufactured.
5. **Shortage Concession Bulletins:** Checks whether the OEM has issued an active shortage concession authorization for that specific part terminology.
6. **Sourcing Channel Status:** Confirms the candidate supplier is an authorized dealer or approved commercial distributor.

---

## 4. Quarantining the LLM from Policy Gating

In strict adherence to `.cursor/rules/research-standards.mdc`:
* **Zero Probabilistic Policy Logic:** Large Language Models **never** evaluate warranty eligibility. LLMs are prone to assuming generic consumer warranty rights (e.g., misinterpreting the Magnuson-Moss Warranty Act to claim dealerships can freely install aftermarket parts on OEM factory warranty tickets).
* **Deterministic Rules Engine:** The eligibility engine executes purely through deterministic Python/SQL relational lookups against a verified policy matrix.
* **Traceable Audit Citations:** Every eligibility decision outputs a statutory or OEM policy document citation (e.g., `Ford Warranty & Policy Manual 2026, Section 3, Subsection B`).
* **Non-Legal Disclaimer:** The system explicitly states in the UI:
  > *"Notice: Eligibility determinations are rule-based operational guidance based on dealership policy configurations and do not constitute formal legal advice."*

---

## 5. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Mandatory Modifications Across PR2 Documents:**
  * Update `architecture/partsrescue-pr2-fitment-and-eligibility-engine.md`: Replace binary firewall language with the Six-State Policy Eligibility Model and TSB/Shortage Concession logic.
  * Update `evaluation/partsrescue-pr2-demo-blueprint.md` (Scenario 3): Accurately reflect that the system checks for TSB shortage concessions before issuing a `VERIFIED INELIGIBLE` ruling.
  * Update `architecture/partsrescue-pr2-data-model-and-schemas.md`: Update `EligibilityRule` entity schema to support the six enumerated states.
