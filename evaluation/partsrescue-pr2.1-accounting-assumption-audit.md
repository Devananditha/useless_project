# PartsRescue PR2.1: Interdepartmental Accounting Assumption Audit

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr2.1-accounting-assumption-audit.md`  
**Phase:** PR2.1 — Architecture Integrity, Economic Model Correction & Technical Consistency Audit  
**Standard Compliance:** Fully compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and `references/tekion-themes.pdf`  
**Audit Team:** Financial and Operational Modelling Analyst, Technical Red-Team Reviewer  
**Date:** November 14, 2026  
**Audit Status:** CRITICAL REVISION COMPLETE  

---

## 1. Executive Summary & Audit Mandate

In Phase PR2, `evaluation/partsrescue-pr2-red-team-review.md` and `evaluation/partsrescue-pr2-final-report.md` introduced an architectural construct termed:
> **"Automated DMS Sublet Billing Rule — Account 68A"**

The narrative claimed that PartsRescue automatically resolves the interdepartmental friction between the Parts Department and Service Department by reallocating expedited hotshot freight fees directly to the Repair Order labor operation as an internal sublet expense.

This audit critically investigates this claim and finds that:
1. **Account 68A is NOT a Standard Industry Account:** Dealership charts of accounts (COA) vary across OEM dealer networks (Ford, GM, Stellantis, Toyota) and dealer management systems (CDK, Reynolds, Tekion). There is no universal "Account 68A" for internal parts freight sublet.
2. **Account 68A is NOT a Documented Tekion ARC Feature:** Tekion ARC does not possess an out-of-the-box automated sublet cross-allocation rule triggered by an external parts recommendation agent.
3. **Internal Accounting Requires Human Controller Approval:** Dealership software cannot unilaterally reallocate financial liabilities between department financial statements without General Manager or Controller sign-off.
4. **Product Value Decoupling:** PartsRescue's core economic value **must not depend on an internal accounting trick**. The dealership-level financial recovery ($78k–$97k annual operating benefit) exists regardless of how the controller books the $25 freight fee.

---

## 2. Granular Audit of PR2 Accounting Claims

```
+========================================================================================================================+
|                                    ACCOUNTING ASSUMPTION AUDIT MATRIX                                                  |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| #  | PR2 Document & Claim           | Audit Severity        | Audit Finding & Mandatory Remedy                         |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 01 | `red-team-review.md` (Q12):    | **CRITICAL**          | *Claim:* "DMS adapter automatically codes courier freight|
|    | "Automated DMS Sublet Billing  | (Unsupported Claim /  | as Internal Labor Sublet (Account 68A)."                 |
|    | Rule (Account 68A)"            | False Standardization)| *Finding:* Fabricated specific account number and assumed|
|    |                                |                       | automated DMS ledger mutation without controller consent.|
|    |                                |                       | *Remedy:* Strike Account 68A. Reframe as an optional,    |
|    |                                |                       | configurable policy recommendation.                      |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 02 | `corrections-log.md` (Item 07):| **HIGH**              | *Claim:* "Freight charged to internal labor sublet,      |
|    | "Inter-Departmental Silo Fixed | (Premature Scope      | preserving parts department gross margin."               |
|    | via Sublet Billing Rule"       | Settlement)           | *Finding:* Presented an unvalidated management policy    |
|    |                                |                       | as a completed architectural fix.                        |
|    |                                |                       | *Remedy:* Label as an operational management hypothesis  |
|    |                                |                       | subject to dealership accounting setup.                  |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 03 | `final-report.md` (Section M): | **HIGH**              | *Claim:* "The Fatal Objection Resolved... turns Parts    |
|    | Resolved interdepartmental     | (Overstated Red-Team  | Manager from opponent to champion via Account 68A."      |
|    | friction completely.           | Resolution)           | *Finding:* Overstated. Departmental politics cannot be   |
|    |                                |                       | magically solved by hardcoding an arbitrary account key. |
|    |                                |                       | *Remedy:* Reframe around total rooftop profitability.    |
+========================================================================================================================+
```

---

## 3. Real-World Dealership Financial Mechanics

To understand why "Account 68A" was flawed, we examine how dealership financial statements actually work:

### 3.1 The Departmental Silo Dilemma
* **Parts Financial Statement:** Evaluated on Parts Gross Profit ($GP_{\text{parts}}$) and Department Operating Expense. Freight charges are typically booked under **Freight & Express (Expense Account)** or added to Cost of Goods Sold ($COGS_{\text{parts}}$). A parts manager whose monthly bonus depends on parts net profit resists spending $\$28$ on a courier if that $\$28$ reduces their department statement.
* **Service Financial Statement:** Evaluated on Service Gross Profit ($GP_{\text{service}}$) and Effective Labor Rate ($ELR$). When a bay is kept active, the service department books $\$110 - \$160/\text{hr}$ in labor revenue and profit.
* **The Rooftop Perspective (General Manager / Dealer Principal):** The owner of the dealership cares about **Total Dealership Operating Net Profit**. From the rooftop perspective, spending $\$28$ to preserve $\$110$ of gross profit yields a **net gain of $\$82$**.

### 3.2 Real-World Expense Allocation Methods
In actual dealership practice, handling expedited freight falls under one of four real-world controller policies:

```
+========================================================================================================================+
|                                    REAL-WORLD EXPENSE ALLOCATION ALTERNATIVES                                          |
+----+--------------------------+---------------------------------+------------------------------------------------------+
| #  | Accounting Policy Model  | How It Operates in DMS          | Practical Implementation Feasibility                 |
+----+--------------------------+---------------------------------+------------------------------------------------------+
| 01 | **Service Internal Sublet| Freight is entered as an        | Common in progressive dealerships; requires Service   |
|    | Allocation**             | internal sublet labor line on RO| Manager agreement and Controller setup in DMS.       |
+----+--------------------------+---------------------------------+------------------------------------------------------+
| 02 | **Parts Freight Expense  | Freight is booked to normal     | Standard default; acceptable if Parts Manager has a  |
|    | Absorption**             | Parts Department freight expense| monthly expedited freight allowance configured in RO. |
+----+--------------------------+---------------------------------+------------------------------------------------------+
| 03 | **Retail Customer Pass-  | Freight is billed directly to   | Standard on customer-pay emergency orders where      |
|    | Through**                | customer on Repair Order        | customer authorizes expedited shipping for same-day. |
+----+--------------------------+---------------------------------+------------------------------------------------------+
| 04 | **Warranty Concession    | Freight is claimed on OEM claim | Allowed by certain OEMs (e.g. GM, Ford) under        |
|    | Surcharge**              | or booked to warranty adjustment| emergency VOR freight allowances with prior approval.|
+========================================================================================================================+
```

---

## 4. Refactoring the Architecture: Decoupling Product Value from Accounting Workarounds

PartsRescue PR2.1 strictly refactors this dependency:

### 4.1 What PartsRescue Does (Core Architectural Boundary)
PartsRescue is a **decision-support tool**, not a general ledger accounting automation bot:
1. It computes the **Rooftop Net Operational Benefit** ($\Delta = \Psi_{\text{capacity}} - C_{\text{freight}}$).
2. It surfaces the transparent trade-off to the counterperson and advisor.
3. When creating a draft Purchase Order or updating the Repair Order line, it records the freight fee in standard DMS fields (`freight_amount`, `freight_carrier`).
4. It **does NOT** invent account codes or force internal journal entries.

### 4.2 Handling Interdepartmental Policy via Configuration
If a dealership group has established an internal cost-allocation policy, PartsRescue accommodates it via a **Configurable Expense Assignment Setting**:
```json
{
  "dealership_id": "DLR-10492",
  "freight_allocation_policy": {
    "policy_type": "SERVICE_SUBLET", // Options: SERVICE_SUBLET, PARTS_EXPENSE, CUSTOMER_PASS_THROUGH
    "requires_service_manager_signoff": true,
    "internal_account_code": "CONFIGURED_BY_CONTROLLER",
    "spending_cap_per_ro": 35.00
  }
}
```

### 4.3 Why the Product Succeeds Without Accounting Tricks
Even if a dealership uses standard Policy Model 02 (Parts Department absorbs freight):
* The Parts Manager and Service Manager report to the **Fixed Operations Director** or **General Manager**.
* PartsRescue provides the Fixed Operations Director with a monthly dashboard proving that $\$1,200$ in parts department freight expenses directly enabled $\$8,500$ in incremental service department gross profit.
* Management alignment is achieved through **transparent operational reporting**, not deceptive software accounting tricks.

---

## 5. Audit Verdict & Required PR2 File Modifications
* **Status:** PASS WITH CORRECTIONS.
* **Mandatory Text Modifications Across PR2 Documents:**
  * Strike all references to "Account 68A" in `evaluation/partsrescue-pr2-red-team-review.md`, `evaluation/partsrescue-pr2-corrections-log.md`, and `evaluation/partsrescue-pr2-final-report.md`.
  * Replace claims of "automated sublet billing rule" with "Configurable Interdepartmental Expense Policy".
  * Explicitly note that actual chart-of-accounts mapping requires dealership controller configuration.
