# Phase 3 Concept Scorecard: Weighted Multi-Dimensional Evaluation (Post Red-Team Audit)

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase3-concept-scorecard.md`  
**Stage:** Phase 3 – Opportunity Identification & Concept Generation  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`, and Innovation Critic Red-Team Audit  
**Purpose:** Objective weighted evaluation of all 12 generated solution concepts across eight strategic criteria totaling 100%, documenting initial scores, red-team adjustments, and post-audit final rankings.

---

## 1. Evaluation Rubric & Weighted Criteria Architecture

$$\text{Total Score} = \sum_{i=1}^{8} (\text{Score}_i \times \text{Weight}_i)$$

| Criterion | Weight | Scoring Anchor (1 to 5 Scale) | Strategic Focus & Rationale |
| :--- | :---: | :--- | :--- |
| **1. Novelty & Differentiation** | **20%** | **1:** Rebranded existing DMS feature.<br>**3:** Incremental automation of point solution.<br>**5:** Unprecedented mechanism solving an unaddressed capability gap. | Concepts that replicate Tekion ARC, CDK, Reynolds, or established point solutions (AutoAlert, Xtime, Vitu, OEC) are severely penalized. High scores require clear operational white space. |
| **2. Business Value & Measurable Impact** | **20%** | **1:** Negligible convenience gain.<br>**3:** Moderate savings ($5k–$15k/yr).<br>**5:** Transformative revenue unlock or cost recovery (>$150,000/yr per rooftop). | Evaluates quantified economic recovery (billable labor recovery, absorption protection, Contracts in Transit acceleration, expediter fee elimination). |
| **3. Technical Feasibility & AI Justification** | **15%** | **1:** Zero AI or unnecessary LLM bloat.<br>**3:** Moderate multi-API pipeline.<br>**5:** Mathematically justified AI/OR pattern executing locally/sub-second with zero GPU bloat. | Penalizes boolean SQL checks masquerading as "AI" as well as hallucinating LLMs. Rewards right-sized engineering (OR-Tools CP-SAT, vision LLM extraction). |
| **4. Tekion Ecosystem Fit** | **15%** | **1:** Clashes with Tekion's architecture.<br>**3:** Standalone external integration.<br>**5:** Natural cloud-native extension directly enhancing Tekion ARC (Auto Dispatch, Deal Guard AI, DSE). | Evaluates architectural harmony with Tekion's enterprise cloud product portfolio. |
| **5. Data Availability & Integration** | **10%** | **1:** Blocked by proprietary OEM SGW or GLBA credit APIs.<br>**3:** Requires third-party B2B scraping.<br>**5:** 100% accessible DMS relational ledger or public statutory DMV codes. | Ensures the required data inputs are realistically accessible without commercial licensing blockers. |
| **6. Hackathon Demo Potential** | **10%** | **1:** Invisible backend script.<br>**3:** Standard static web charts.<br>**5:** Dynamic, visually stunning, interactive split-screen demo that commands judge attention. | Measures the visual "kinetic wow" factor achievable by a student team in a 5-minute presentation. |
| **7. Adoption & Operational Practicality** | **5%** | **1:** High employee sabotage risk / compensation conflict.<br>**3:** Moderate workflow adjustment.<br>**5:** Aligns with frontline incentives (e.g. flat-rate earnings, clerk speed). | Evaluates whether dealership staff will cooperate with or resist the workflow intervention. |
| **8. Evidence Strength** | **5%** | **1:** Anecdotal vendor assertion.<br>**3:** Secondary industry study.<br>**5:** Primary audited trade benchmark (NADA, Cox Automotive, Ducker Carlisle, NHTSA). | Ensures the underlying problem and economic impact are grounded in traceable evidence. |

---

## 2. Post Red-Team Scorecard & Adjusted Rankings

The table below contrasts **Initial Scores** against **Post-Audit Adjusted Scores** following the Innovation Critic red-team review, sorted strictly by **Absolute Mathematical Rank** (1 to 12) with Candidate Category Shortlist status explicitly designated:

| Math Rank | Concept ID & Name | Candidate Area | Initial Score | Novelty (20%) | Business Value (20%) | Tech Feas (15%) | Tekion Fit (15%) | Data Avail (10%) | Demo Pot (10%) | Adoption (5%) | Evidence (5%) | Post-Audit Score | Candidate Stratification & Audit Verdict |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **C1: CrossBorder TitleGuard** | Candidate C (Titling) | 4.765 | 4.7 (0.940) | 4.5 (0.900) | 4.4 (0.660) | 4.9 (0.735) | 4.8 (0.480) | 5.0 (0.500) | 4.6 (0.230) | 4.8 (0.240) | **4.685** | **PRIMARY RECOMMENDATION: Candidate C Flagship** (Frontrunner for Phase 4; scoped to CA-NV-AZ corridor; customer titles; absorbs C2) |
| **2** | **B3: BayFlow Dynamic** | Candidate B (Parts) | 4.635 | 4.8 (0.960) | 4.6 (0.920) | 4.6 (0.690) | 4.7 (0.705) | 4.6 (0.460) | 4.8 (0.480) | 3.6 (0.180) | 4.6 (0.230) | **4.625** | **CONSTRAINED FALLBACK: Candidate B Flagship** (Google OR-Tools CP-SAT; lift prison limits; $110k–$160k baseline; absorbs B1 & B4) |
| **3** | **C4: TitleFlow Orchestrator** | Candidate C (Titling) | 4.410 | 4.0 (0.800) | 4.2 (0.840) | 4.6 (0.690) | 4.6 (0.690) | 4.8 (0.480) | 4.6 (0.460) | 4.6 (0.230) | 4.4 (0.220) | **4.410** | Non-Shortlist: Secondary Candidate C Concept (Absorbed into C1 Title Clerk UI) |
| **4** | **CadenceRevive (Hybrid A)** | Candidate A (Retention) | 4.470 | 4.3 (0.860) | 4.4 (0.880) | 4.2 (0.630) | 4.6 (0.690) | 4.6 (0.460) | 4.4 (0.440) | 4.0 (0.200) | 4.4 (0.220) | **4.380** | **DISQUALIFIED & INELIGIBLE FOR PHASE 4** (Critic Verdict: REJECT due to TCPA statutory liability & dealer margin destruction) |
| **5** | **A1: CadenceGuard (Standalone)**| Candidate A (Retention) | 4.405 | 4.2 (0.840) | 4.2 (0.840) | 4.5 (0.675) | 4.6 (0.690) | 4.8 (0.480) | 3.8 (0.380) | 4.2 (0.210) | 4.6 (0.230) | **4.345** | Non-Shortlist: Merged into CadenceRevive Survival Core |
| **6** | **B4: FairFlag Dispatch** | Candidate B (Parts) | 4.290 | 4.2 (0.840) | 4.2 (0.840) | 4.5 (0.675) | 4.5 (0.675) | 4.6 (0.460) | 4.0 (0.400) | 3.6 (0.180) | 4.4 (0.220) | **4.290** | Non-Shortlist: Constraint absorbed into B3 CP-SAT Solver |
| **7** | **C3: DMV RiskScorer** | Candidate C (Titling) | 4.200 | 4.2 (0.840) | 4.0 (0.800) | 4.4 (0.660) | 4.4 (0.660) | 4.2 (0.420) | 4.0 (0.400) | 4.2 (0.210) | 4.2 (0.210) | **4.200** | Non-Shortlist: Absorbed into C1 Pre-Submission Triage Meter |
| **8** | **A4: RetentionOpt** | Candidate A (Retention) | 4.190 | 4.0 (0.800) | 4.2 (0.840) | 4.4 (0.660) | 4.4 (0.660) | 4.4 (0.440) | 4.0 (0.400) | 3.8 (0.190) | 4.0 (0.200) | **4.190** | Non-Shortlist: Secondary Macro BI Simulation Tool |
| **9** | **B2: PartsOrchestrator AI** | Candidate B (Parts) | 4.300 | 4.3 (0.860) | 4.2 (0.840) | 3.8 (0.570) | 4.5 (0.675) | 3.6 (0.360) | 4.2 (0.420) | 3.8 (0.190) | 4.2 (0.210) | **4.125** | Non-Shortlist: Demoted for external courier API dependency |
| **10** | **A3: FairRate AI (Standalone)** | Candidate A (Retention) | 4.130 | 4.5 (0.900) | 4.2 (0.840) | 3.8 (0.570) | 4.2 (0.630) | 3.5 (0.350) | 4.2 (0.420) | 3.0 (0.150) | 4.2 (0.210) | **4.070** | Non-Shortlist: Merged into CadenceRevive pricing sub-module |
| **11** | **C2: DealJacket Reconciler** | Candidate C (Titling) | 4.560 | **2.4 (0.480)**| **3.5 (0.700)**| **4.0 (0.600)**| 4.6 (0.690) | 4.8 (0.480) | 4.0 (0.400) | 4.4 (0.220) | 4.6 (0.230) | **3.800** | **REJECTED AS STANDALONE:** Duplicates Deal Guard AI; zero ML; merged into C1 |
| **12** | **B1: StageGate Dispatch** | Candidate B (Parts) | 4.775 | **2.2 (0.440)**| **3.8 (0.760)**| **3.2 (0.480)**| 4.8 (0.720) | 4.8 (0.480) | 4.0 (0.400) | 4.0 (0.200) | 4.8 (0.240) | **3.720** | **DEMOTED FROM RANK 1:** Zero AI/ML; basic boolean SQL gate; absorbed into B3 |

---

## 3. Flagship Shortlist for Phase 4 Selection (1 Primary, 1 Fallback, 1 Disqualified)

Following the independent red-team audit and Phase 3.1 validation, only two concepts remain viable for Phase 4 selection, with CadenceRevive formally disqualified:

### #1 Primary Recommendation (Frontrunner): CrossBorder TitleGuard (Candidate C, Theme 1 UC02)
* **Adjusted Score:** **4.685 / 5.00** (Math Rank #1 Overall)
* **Core Mechanism:** Hybrid multimodal Vision-Language Model (VLM structured JSON extraction) coupled with a deterministic declarative Abstract Syntax Tree (AST) statutory rule engine validating incoming physical deal documents (scanned trade-in titles, reassignment chains, Powers of Attorney, 20-year rolling odometer disclosures) against destination-state motor vehicle codes.
* **Demonstration Scope:** Bounded to the high-volume **California – Nevada – Arizona (CA-NV-AZ)** sales corridor.
* **Why It Wins:** Solves a documented $300–$600/deal cost and 4–8 day Contracts in Transit (CIT) drag; commands the highest visual demo impact in a 5-minute hackathon pitch; directly augments Tekion Deal Guard AI and TDP (Five64) without duplicating existing features. Scoped to customer-held physical titles with asynchronous non-blocking F&I desk alerts.

### #2 Constrained Fallback: BayFlow Dynamic (Candidate B, Theme 1 UC01 & UC04)
* **Adjusted Score:** **4.625 / 5.00** (Math Rank #2 Overall)
* **Core Mechanism:** Operations research combinatorial optimization engine utilizing **Google OR-Tools CP-SAT** to solve the shop floor Flexible Job-Shop Scheduling Problem with Resource Constraints (FJSSP-RC). When unexpected mid-repair parts stalls occur, it dynamically shifts off-car diagnostic/bench tasks to stalled technicians, reallocates open flat bays, enforces pre-dispatch parts staging locks (absorbing B1), and balances technician flag-hour equity (absorbing B4).
* **Operational Limits & Value:** Explicitly constrained by the physical "lift prison" (a disabled car cannot be rolled off a lift). Recalibrated commercial baseline of **$110,000–$160,000 in annual gross profit** across a 12-bay shop at 80% demand absorption. Retained as an engineering alternative if the team favors constraint programming over computer vision.

### Disqualified & Ineligible: CadenceRevive (Candidate A, Theme 2 UC05)
* **Adjusted Score:** **4.380 / 5.00** (Math Rank #4 Overall)
* **Disqualification Verdict:** Formally **REJECTED** and eliminated from Phase 4 eligibility due to fatal TCPA class-action statutory liabilities ($500–$1,500/text), dealer fixed ops gross margin destruction from matching aftermarket rates, and competitive commoditization against 15-year-old CRM products.
