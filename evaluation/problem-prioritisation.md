# Problem Prioritisation & Opportunity Evaluation (Post Phase 2.1 Audit)

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/problem-prioritisation.md`  
**Stage:** Phase 2.1 – Problem Discovery Validation & Prioritisation Audit  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`, and Phase 2.1 Audit Standards  
**Purpose:** Rigorous, evidence-based weighted evaluation of candidate dealership problem areas to identify the highest-value, defensible domains for hackathon exploration.

---

## 1. 7-Criterion Weighted Scoring Model Architecture

The evaluation model applies seven objective criteria with fixed percentage weights totaling 100%. This includes a dedicated criterion for **Technical Feasibility & Data Accessibility within Hackathon Scope (20%)** to ensure that theoretical problem severity does not promote concepts dependent on encrypted OEM telematics, specialized electrical hardware, or restricted GLBA financial data.

$$\text{Total Score} = \sum_{i=1}^{7} (\text{Score}_i \times \text{Weight}_i)$$

| Criterion | Weight | Scoring Anchor (1 to 5 Scale) | Strategic Focus & Methodological Rationale |
| :--- | :---: | :--- | :--- |
| **1. Business Impact & Value Creation** | **20%** | **1:** Marginal convenience gain (<$1,000/mo).<br>**3:** Moderate operational savings ($1,000–$10,000/mo).<br>**5:** Transformative revenue unlock or cost recovery (>$25,000/mo; major gross profit or cash flow driver). | Dealerships operate on thin net margins (2%–4% of sales). Solutions must deliver demonstrable, quantified ROI across gross profit, fixed absorption, or holding cost reduction. Recalibrated in Phase 2.1 to prevent overstating low-volume transaction fees. |
| **2. Operational Severity & Frequency** | **15%** | **1:** Low-friction, infrequent edge case.<br>**3:** Moderate disruption occurring weekly.<br>**5:** Daily operational bottleneck paralyzing core dealership revenue streams. | Measures how acutely frontline dealership employees experience the breakdown on a day-to-day basis. |
| **3. Existing Solution Gap / White Space** | **15%** | **1:** Solved by incumbent DMS/CRM features.<br>**3:** Addressed by established point solutions.<br>**5:** Completely unaddressed gap or poorly served by clumsy, manual workarounds. | Critical for hackathon differentiation. Winning concepts must not replicate established features already standard in Tekion ARC, CDK, or Reynolds. |
| **4. Technical Feasibility & Data Accessibility** | **20%** | **1:** Requires proprietary OEM telemetry, CAN-bus hardware, or restricted GLBA credit/payoff APIs.<br>**3:** Requires third-party vendor APIs with limited public access.<br>**5:** 100% accessible text/document/relational DMS data; fully feasible for a 2–4 person hackathon team. | Ensures ideas are deliverable without external hardware or legal/licensing blockers. |
| **5. Stakeholder Importance & Adoption Readiness** | **15%** | **1:** Low adoption priority; high frontline employee resistance or incentive conflict.<br>**3:** Departmental manager interest with moderate friction.<br>**5:** Executive GM/Controller/Service Director mandate; high willingness to pay. | Evaluates whether leadership will sponsor adoption and whether frontline staff incentives align with the solution. |
| **6. Evidence Strength & Verifiability** | **10%** | **1:** Anecdotal or marketing assertion.<br>**3:** Secondary industry survey or vendor white paper.<br>**5:** Rigorous primary trade data (NADA, Cox Automotive, FTC, peer-reviewed benchmarks). | Ensures the problem is real, documented, and defensible under aggressive red-team cross-examination. |
| **7. Alignment with Hackathon Themes** | **5%** | **1:** Distant or tangential connection to hackathon scope.<br>**3:** Moderate fit with one theme.<br>**5:** Direct, verbatim alignment with official hackathon use cases from `references/tekion-themes.pdf`. | Guarantees compliance with hackathon evaluation parameters. |

---

## 2. Re-Scoring Candidate Problem Areas (Strict Mathematical Ranking)

All candidates are scored on a 1.0 to 5.0 scale across the seven criteria. The table below is **strictly sorted by the calculated weighted total score** in descending order:

| Rank | Candidate Problem Area | Official Theme & Verbatim UC | Business Impact (20%) | Severity & Freq (15%) | Solution Gap (15%) | Feasibility & Data (20%) | Stakeholder Impt (15%) | Evidence Strength (10%) | Theme Align (5%) | Weighted Total (out of 5.00) | Red-Team Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Post-Warranty Customer Service Defection & Churn Analytics** | Theme 2: UC 05 (*Churn & Win Back Predictor for Service Customers*) | 5.0 (1.000) | 4.6 (0.690) | 4.2 (0.630) | **4.8 (0.960)** | 4.8 (0.720) | 5.0 (0.500) | 5.0 (0.250) | **4.750** | **PASS / TOP 3 SHORTLIST** |
| **2** | **In-Bay Parts Backorder Stalls & Shop Dispatch Pre-Gating** | Theme 1: UC 01/04 (*Autonomous Appointment & Dispatch Orchestrator* / *Service Parts Shortage Resolver Agent*) | 4.8 (0.960) | 4.7 (0.705) | 4.2 (0.630) | **4.8 (0.960)** | 4.7 (0.705) | 4.8 (0.480) | 5.0 (0.250) | **4.690** | **PASS / TOP 3 SHORTLIST** |
| **3** | **Multi-State Title & Registration Statutory OCR & Validation** | Theme 1: UC 02 (*Smart Document Extraction Agent*) | 4.0 (0.800) | 4.8 (0.720) | 4.6 (0.690) | **4.9 (0.980)** | 4.7 (0.705) | 4.8 (0.480) | 5.0 (0.250) | **4.625** | **PASS / TOP 3 SHORTLIST** |
| **4** | **Used Vehicle Reconditioning Latency (Days to Frontline) Optimization** | Theme 2: UC 07 (*Days to Sell Anomaly Explainer*) | 4.5 (0.900) | 4.7 (0.705) | 3.5 (0.525) | **4.6 (0.920)** | 4.5 (0.675) | 5.0 (0.500) | 4.8 (0.240) | **4.465** | Deprioritized (Incumbent vAuto iRecon / Rapid Recon) |
| **5** | **Used EV Battery Health Opacity & Trade-In Residual Valuation** | Theme 4: UC 17 (*EV Trade In Battery Health Estimator*) | 4.7 (0.940) | 4.4 (0.660) | 4.7 (0.705) | **1.8 (0.360)** | 4.6 (0.690) | 4.6 (0.460) | 5.0 (0.250) | **4.065** | **BLOCKED:** Proprietary OEM SGW Telemetry Lockout |
| **6** | **Dealership Mobile Service Fleet Dynamic Routing & Parts Pre-Staging** | Theme 4: UC 18 (*Green Delivery Route Optimizer*) | 4.2 (0.840) | 4.2 (0.630) | 4.1 (0.615) | **4.0 (0.800)** | 3.2 (0.480) | 4.2 (0.420) | 4.8 (0.240) | **4.025** | Niche Impact (<15% dealership fleet adoption) |
| **7** | **Showroom Waiting Dwell Time & F&I Closing Bottleneck** | Theme 2: UC 08 / Theme 3: UC 11 (*F&I Compliance & Fairness Auditor* / *Accessible Showroom Kiosk Experience*) | 4.6 (0.920) | 4.5 (0.675) | 3.6 (0.540) | **3.8 (0.760)** | 2.5 (0.375) | 4.8 (0.480) | 4.8 (0.240) | **3.990** | **INCENTIVE TRAP:** Dealers resist self-service F&I |
| **8** | **Commercial EV Fast-Charging Peak Demand Charge Management** | Theme 4: UC 14 (*Carbon Footprint Tracker for Dealer Operations*) | 4.3 (0.860) | 4.2 (0.630) | 4.9 (0.735) | **1.5 (0.300)** | 4.2 (0.630) | 4.5 (0.450) | 5.0 (0.250) | **3.855** | **OUT OF SCOPE:** Facilities/EMS electrical hardware |
| **9** | **Technician Unbilled Diagnostic Time & Comeback Prevention** | Theme 1: UC 01 (*Autonomous Appointment & Dispatch Orchestrator*) | 4.6 (0.920) | 4.8 (0.720) | 4.2 (0.630) | **2.5 (0.500)** | 2.4 (0.360) | 4.6 (0.460) | 5.0 (0.250) | **3.840** | **INCENTIVE TRAP:** Flat-rate book-time labor structure |
| **10** | **Digital Retailing to In-Store Desking Reconciliation Breakdown** | Theme 3: UC 09/12 (*AI Co-Pilot for First Time Buyers* / *Post Purchase Loyalty Journey Orchestrator*) | 4.4 (0.880) | 4.3 (0.645) | 3.5 (0.525) | **3.5 (0.700)** | 2.2 (0.330) | 4.6 (0.460) | 4.8 (0.240) | **3.780** | **TEKION OVERLAP:** Directly clashes with Tekion ARC |

---

## 3. The Top 3 Defensible Problem Areas (Final Shortlist)

The Top 3 shortlist matches the strictly calculated mathematical rankings:

### Rank 1: Post-Warranty Customer Service Defection & Churn Analytics (Score: 4.750 / 5.00)
- **Theme & Verbatim Official Use Case:** Theme 2: Data Analytics | Use Case 5: *Churn & Win Back Predictor for Service Customers*
- **Problem Statement:** Dealership service retention for late-model vehicles (<=2 years old) drops to 54%, and once factory warranties expire at months 36–48, defection accelerates to independent repair facilities, leaving dealerships with only a 29% overall share of all automotive service visits (`SRC-P2-04`). Losing these service clients imperils the dealership's core profitability (fixed ops = ~49.6% of total gross profit) and forfeits repeat vehicle sales, as service clients are 74% more likely to buy their next car from that store (`SRC-P2-04`).
- **Defensibility & Data Availability:**
  1. *Data Accessibility:* Dealerships own 100% of historical repair orders, vehicle sales dates, maintenance line items, and customer contact records in their native DMS. Zero GLBA barriers, zero third-party API dependencies, zero OEM telemetry lockouts.
  2. *Defensible Innovation:* Transcends generic batch CRM mailers by engineering predictive mileage-interval component wear algorithms combined with localized aftermarket pricing transparency.
  3. *Business Consequence:* A 5% improvement in service retention directly protects hundreds of thousands of dollars in high-margin fixed-ops gross profit.
- **Primary Stakeholders:** Service Director, Customer Retention Manager, General Manager, Dealership Owner.

---

### Rank 2: In-Bay Parts Backorder Stalls & Shop Dispatch Pre-Gating (Score: 4.690 / 5.00)
- **Theme & Verbatim Official Use Case:** Theme 1: AI & Automation | Use Case 1: *Autonomous Appointment & Dispatch Orchestrator* & Use Case 4: *Service Parts Shortage Resolver Agent*
- **Problem Statement:** Service technicians begin vehicle teardown in active repair bays before verifying whether 100% of required parts, fasteners, and fluids are physically present and staged, paralyzing bays at an idle capacity cost of ~$175/hour (`SRC-P2-01`) and stranding vehicles on lifts while parts counter staff make frantic manual spot-buys.
- **Defensibility & Data Availability:**
  1. *Data Accessibility:* Operates entirely within core relational DMS databases (active RO repair lines, parts catalog bills of materials, bin inventory counts, technician skill matrices).
  2. *Defensible Innovation:* Solves the major operational bottleneck between the parts counter and the service shop floor. Existing DMS tools track bin stock and dispatch boards separately; Rank 2 introduces dynamic combinatorial pre-dispatch bill-of-materials gating.
  3. *Business Consequence:* Recovers lost technician billable hours (technicians lose 20%–30% of daily time to shop stalls, `SRC-P2-06`) and eliminates costly customer loaner vehicle days.
- **Scope Nuance (from Phase 2.1 Audit):** Pre-dispatch gating strictly applies to known maintenance operations, factory recalls, and customer-authorized post-diagnostic repair lines; initial diagnostic teardowns where parts requirements cannot be known in advance remain excluded from pre-gating.
- **Primary Stakeholders:** Service Director, Shop Dispatcher, Parts Manager, Flat-Rate Technicians.

---

### Rank 3: Multi-State Title & Registration Statutory Cross-Border Validation (Score: 4.625 / 5.00)
- **Theme & Verbatim Official Use Case:** Theme 1: AI & Automation | Use Case 2: *Smart Document Extraction Agent*
- **Problem Statement:** Selling vehicles across state lines results in 30 to 90 days of administrative delay, temp-tag expirations, lender funding stalls, and third-party expediter fees ($300–$600/deal) due to complex, disparate statutory DMV tax, lien, and safety regulations across 50 states (`SRC-P2-02`).
- **Defensibility & Data Availability:**
  1. *Data Accessibility:* Operates purely on scanned document images, PDF contracts, buyer address data, and publicly accessible state/county DMV statutory rules. No physical hardware or vehicle access required.
  2. *Tekion Differentiation:* Cleanly differentiates from Tekion Deal Guard AI. Deal Guard AI focuses on basic deal checklist presence and driver's license/insurance OCR (`SRC-TEK-07`, `SRC-TEK-08`). Rank 3 targets deep, 50-state statutory cross-border DMV tax, lien, and emissions compliance logic.
  3. *Business Consequence:* Directly accelerates Contracts in Transit (CIT) cash flow and eliminates $300–$600 per-deal third-party outsourcing fees (`SRC-P2-02`). Business impact is recalibrated to 4.0/5.0 to reflect true out-of-state transaction volume (3%–7% of total sales).
- **Primary Stakeholders:** Dealership Office Manager, Title Clerks, Dealership Controller, Indirect Auto Lenders.

---

## 4. Rejection and Demotion Register (Audit Findings)

The following problem areas were formally evaluated and rejected/demoted from primary contention:

1. **Used EV Battery Health Opacity (Demoted to Rank 5, Score: 4.065):**
   - *Failure Mode:* **Fatal Hardware & Telemetry Dependency.** High-voltage battery State of Health (SoH) is locked behind OEM proprietary Security Gateways (SGW) and is not exposed via standard OBD-II (SAE J1979). A student hackathon team cannot credibly access ground-truth battery diagnostics without OEM partnerships or specialized CAN-bus hardware.
2. **Technician Unbilled Diagnostic Time (Demoted to Rank 9, Score: 3.840):**
   - *Failure Mode:* **Human Compensation Trap.** Diagnostic time caps are dictated by flat-rate labor guides and manufacturer warranty reimbursement policies. Rushing and comebacks stem from pay plans, which software cannot unilaterally rewrite.
3. **Commercial EV Fast-Charging Demand Charges (Demoted to Rank 8, Score: 3.855):**
   - *Failure Mode:* **Out of Scope (Facilities Engineering).** Managing peak demand charges requires smart building electrical switchgear, physical energy management systems (EMS), and commercial battery buffers (BESS). It is not an automotive retail DMS problem.
4. **Showroom Waiting Dwell Time / F&I Bottleneck (Demoted to Rank 7, Score: 3.990):**
   - *Failure Mode:* **Human Incentive Misalignment.** Dealerships deliberately route buyers through a physical F&I office to maximize high-margin aftermarket product sales ($1,500–$2,500 backend gross). Dealers actively resist unassisted self-service digital contracting.
5. **Digital Retailing to In-Store Desking Reconciliation (Demoted to Rank 10, Score: 3.780):**
   - *Failure Mode:* **Tekion Core Product Overlap.** Directly attacks Tekion ARC's primary cloud architecture proposition. Furthermore, showroom "re-desking" is often an intentional profit tactic rather than a software failure.
6. **Mobile Service Fleet Dynamic Routing (Demoted to Rank 6, Score: 4.025):**
   - *Failure Mode:* **Niche Operational Footprint.** Fewer than 15% of US franchise dealerships operate mobile service fleets; commercial last-mile route optimization platforms (e.g. Wise Systems) already exist.
