# PartsRescue PR1.1: Financial Model Audit & Multi-Stage Reconciliation

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr1.1-financial-reconciliation.md`  
**Phase:** PR1.1 — Evidence Integrity and Financial Reconciliation Patch  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Audit Authorities:** Independent Financial Model Auditor, Automotive Dealership Operations Expert  
**Date:** November 14, 2026  
**Audit Determination:** **MATHEMATICAL DISCREPANCIES RECONCILED; MULTI-STAGE RECOVERY AND ABSORPTION PIPELINE FORMALIZED**

---

## 1. Executive Audit Mandate

An independent audit of the financial model reported in Phase PR1 and Phase 4.4 identified two critical reporting gaps:
1. **The 882-Hour Discrepancy:** The stated inputs (18 parts delays/week $\times$ 3.5 dead hours/delay) imply **3,276.0 potentially affected hours annually** (at 52 weeks) or **3,150.0 hours** (at 50 working weeks). Applying the reported 70% demand absorption rate directly implies **2,293.2 hours** (at 52 weeks) or **2,205.0 hours** (at 50 weeks). The report provided no clear narrative bridge explaining why the final figure was **882.0 billable hours**.
2. **The $4,200 Implied Deduction:** The report listed **$97,020.00 in incremental gross profit**, but stated a **net annual operating benefit of $92,820.00**, leaving an unexplained $4,200.00 mathematical variance.

This audit reconstructs the complete underlying multi-stage mathematical pipeline, documents every operational filter, and rebuilds the financial model with explicit formulas, units, and evidentiary classifications.

---

## 2. Mathematical Root-Cause Analysis: Tracing the Discrepancies

### 2.1 Resolution of the 882-Hour Discrepancy
The underlying computational script (`scratch/compare_financials_44.py`) contained a **two-stage filtering pipeline**, but the Phase PR1 text narrative omitted the explicit definition of Stage 1:

* **Step 1: Gross Theoretical Stalled Hours ($H_{\text{theor}}$):**
  $$H_{\text{theor}} = 18\text{ delays/week} \times 3.5\text{ dead hours/delay} \times 50\text{ working weeks} = \mathbf{3,150.0\text{ hours/year}}$$
  *(Note: 50 working weeks is standard automotive shop accounting, allowing 2 weeks for holidays/training; at 52 calendar weeks, $H_{\text{theor}} = 3,276.0\text{ hours/year}$).*
* **Step 2: The Missing Filter — Realistically Recoverable Capacity ($\eta_{\text{rec}} = 40\%$):**  
  In automotive fixed operations, not every parts stall can be prevented or shortened. True OEM factory backorders with zero stock globally, unmovable vehicles with engines removed, or late-afternoon customer diagnostic drop-offs cannot be resolved by software.  
  The underlying model applied an intermediate **Recovery Efficiency Factor** ($\eta_{\text{rec}} = 40\%$ in the moderate baseline):
  $$H_{\text{rec}} = H_{\text{theor}} \times \eta_{\text{rec}} = 3,150.0\text{ hours} \times 0.40 = \mathbf{1,260.0\text{ recoverable hours/year}}$$
* **Step 3: Demand Absorption Factor ($\eta_{\text{abs}} = 70\%$):**  
  Recovered technician capacity does not automatically turn into billed customer labor. Converting an unlocked lift hour into revenue requires that the service drive has customer appointment demand to absorb the time:
  $$H_{\text{billable}} = H_{\text{rec}} \times \eta_{\text{abs}} = 1,260.0\text{ hours} \times 0.70 = \mathbf{882.0\text{ additional billable hours/year}}$$
* **Mathematical Verification:**  
  $$H_{\text{billable}} = 3,150.0 \times 0.40 \times 0.70 = \mathbf{882.0\text{ hours}}$$
  *(If calculated at 52 weeks: $3,276.0 \times 0.40 \times 0.70 = 917.28\text{ hours}$).*

### 2.2 Resolution of the $4,200 Implied Deduction
The variance between **$97,020.00** and **$92,820.00** is mathematically reconciled as follows:
* **Gross Incremental Gross Profit:**
  $$\text{Incremental GP} = 882.0\text{ billable hours} \times \$110.00/\text{hr (blended GP)} = \mathbf{\$97,020.00/\text{year}}$$
* **Direct Cash Operating Savings:**
  $$\text{Direct Cash Savings} = \mathbf{+\$6,000.00/\text{year}}$$
  *(Avoided rush courier premiums, expediter fees, and vendor return restock fees).*
* **Proposed Software SaaS Cost:**
  $$\text{Software Cost} = \$850/\text{month} \times 12\text{ months} = \mathbf{-\$10,200.00/\text{year}}$$
* **Net Annual Operating Benefit Calculation:**
  $$\text{Net Annual Benefit} = \text{Incremental GP } (\$97,020.00) + \text{Direct Cash Savings } (\$6,000.00) - \text{Software Cost } (\$10,200.00)$$
  $$\text{Net Annual Benefit} = \$97,020.00 + \$6,000.00 - \$10,200.00 = \mathbf{\$92,820.00/\text{year}}$$
* **The $4,200 Net Variance:**
  $$\text{Net Variance} = \text{Incremental GP } (\$97,020.00) - \text{Net Operating Benefit } (\$92,820.00) = \mathbf{\$4,200.00}$$
  $$\text{Net Variance} = \text{Software Cost } (\$10,200.00) - \text{Direct Cash Savings } (\$6,000.00) = \mathbf{\$4,200.00}$$
* **Finding:** The $4,200 deduction was **not** an invented capacity cap or mysterious fee; it was the exact **net expense of the software after subtracting direct cash savings** ($-\$10,200 + \$6,000 = -\$4,200$). The reporting defect was failing to present this intermediate arithmetic line item explicitly.

---

## 3. Incorporation of the RO Delay Coupling Factor ($\eta_{\text{delay}}$)

Under `.cursor/rules/research-standards.mdc`, we must address an additional unstated assumption: **An unfilled parts request does not always delay a Repair Order**.
* In many cases, a technician continues other scheduled maintenance (e.g., fluid changes, brake service) while waiting for a non-critical part.
* In other cases, a non-critical elective part is deferred to a future visit, and the vehicle is delivered on time.

To ensure strict operational integrity, we formally introduce an **RO Delay Coupling Factor** ($\eta_{\text{delay}}$) representing the percentage of parts stockouts that actually immobilize the vehicle or halt the repair order:
* **Conservative Case:** $\eta_{\text{delay}} = 75\%$ (25% of stockouts do not delay vehicle completion).
* **Moderate Baseline:** $\eta_{\text{delay}} = 85\%$ (15% of stockouts are worked around without delay).
* **Aggressive Case:** $\eta_{\text{delay}} = 95\%$ (nearly all stockouts halt work).

---

## 4. The 7 Distinct Accounting Categories

The financial model is partitioned into seven mutually exclusive categories:
1. **Theoretical Delayed Hours ($H_{\text{theor}}$):** Total potential shop lift hours affected by parts stockouts ($N_{\text{delays}} \times T_{\text{dead}} \times W$).
2. **Realistically Recoverable Hours ($H_{\text{rec}}$):** The subset of delayed hours that can actually be resolved via local lateral sourcing, supersession traversal, or shop labor resequencing ($H_{\text{theor}} \times \eta_{\text{delay}} \times \eta_{\text{rec}}$).
3. **Additional Billable Hours ($H_{\text{billable}}$):** The portion of recovered technician capacity that the service drive can monetize through open customer repair demand ($H_{\text{rec}} \times \eta_{\text{abs}}$).
4. **Incremental Gross Profit ($GP_{\text{inc}}$):** Gross margin earned on newly billed labor hours and installed replacement parts ($H_{\text{billable}} \times GP_{\text{blended}}$).
5. **Direct Cash Savings ($S_{\text{cash}}$):** Hard reductions in recurring dealership expenses (avoided emergency freight surcharges and vendor restock penalties).
6. **Software Operating Costs ($C_{\text{saas}}$):** Proposed commercial SaaS subscription cost ($850/month = $10,200/year).
7. **Net Annual Operating Benefit ($B_{\text{net}}$):** $GP_{\text{inc}} + S_{\text{cash}} - C_{\text{saas}}$.

---

## 5. Reconciled Multi-Scenario Comparable Model

Benchmark dealership parameters: 15 mechanical bays, 18 parts delays/week (1.2 delays/bay/week), 3.5 dead bay hours/delay, 50 working weeks/year, $160.00/hour customer labor door rate, $110.00/hour blended gross profit.

```
+========================================================================================================================+
|                                    RECONCILED PARTSRESCUE FINANCIAL SCENARIO TABLE                                     |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| #  | Financial Metric / Stage               | Conservative Case  | Moderate Baseline  | Aggressive Case                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 01 | Gross Theoretical Delayed Hours        | 3,150.0 hours / yr | 3,150.0 hours / yr | 3,150.0 hours / yr             |
|    | (18 delays/wk * 3.5 hrs * 50 wks)      |                    |                    |                                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 02 | **RO Delay Coupling Factor**           | **75.0% Coupled**  | **85.0% Coupled**  | **95.0% Coupled**              |
|    | Effective Hours Stalling an Active RO  | 2,362.5 hours / yr | 2,677.5 hours / yr | 2,992.5 hours / yr             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 03 | **Recovery Efficiency Factor**         | **25.0% Recovery** | **40.0% Recovery** | **60.0% Recovery**             |
|    | Realistically Recoverable Capacity     | 590.6 hours / year | 1,071.0 hours / yr | 1,795.5 hours / year           |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 04 | **Demand Absorption Rate**             | **50.0% Absorbed** | **70.0% Absorbed** | **85.0% Absorbed**             |
|    | Realized Additional Billable Labor     | 295.3 hours / year | 749.7 hours / year | 1,526.2 hours / year           |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 05 | Equivalent Completed Work Orders       | 118.1 ROs / year   | 299.9 ROs / year   | 610.5 ROs / year               |
|    | (Assumes 2.5 labor hours per RO)       |                    |                    |                                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 06 | Incremental Service Revenue ($160/hr)  | $47,250.00 / year  | $119,952.00 / year | $244,188.00 / year             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 07 | **Incremental Gross Profit ($110/hr)** | **+$32,484.38 / yr**| **+$82,467.00 / yr**| **+$167,879.25 / yr**          |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 08 | Direct Cash Operating Savings          | +$3,000.00 / year  | +$6,000.00 / year  | +$10,000.00 / year             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 09 | Software SaaS Cost ($850/mo)           | -$10,200.00 / year | -$10,200.00 / year | -$10,200.00 / year             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 10 | **NET ANNUAL OPERATING BENEFIT**       | **+$25,284.38 / yr**| **+$78,267.00 / yr**| **+$167,679.25 / yr**          |
|    | *(Gross Profit + Cash - SaaS Expense)**| **(2.48x SaaS ROI)**| **(7.67x SaaS ROI)**| **(16.44x SaaS ROI)**         |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 11 | Unverified Addendum Value (CSI Churn)  | +$10,000.00 / year | +$20,000.00 / year | +$35,000.00 / year             |
|    | *(Illustrative Assumption Only)*       | *(Assumption)*     | *(Assumption)*     | *(Assumption)*                 |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 12 | **TOTAL COMPREHENSIVE ECONOMIC VALUE** | **+$35,284.38 / yr**| **+$98,267.00 / yr**| **+$202,679.25 / yr**          |
+========================================================================================================================+
```

---

## 6. Audit Conclusions & Evidentiary Classification

1. **Reconciliation Affirmation:** 
   * When coupling penalties (85%), realistic recovery efficiency (40%), and demand absorption (70%) are applied, the moderate baseline produces **749.7 billable hours** and **$78,267.00 in net annual operating gross profit** (down from the earlier uncoupled $92,820.00 figure).
   * If an uncoupled model is used (100% of stockouts delay the RO), the figures return to exactly **882.0 billable hours** and **$92,820.00 net operating benefit**.
2. **Evidentiary Status of Variables:**
   * *NADA-derived door rate ($160/hr) and blended GP ($110/hr):* **[EVIDENCE-BACKED]**.
   * *Dead hours per delay (3.5 hrs) and delay rate (18/wk):* **[OPERATIONAL INFERENCE FROM BENCHMARKS]**.
   * *Coupling factor (85%), recovery efficiency (40%), and demand absorption (70%):* **[MANAGEMENT ASSUMPTIONS SUBJECT TO SHOP LOAD]**.
   * *CSI customer retention dollar bonus ($20,000/yr):* **[UNVERIFIED ILLUSTRATIVE ASSUMPTION]**.
