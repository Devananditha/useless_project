# Phase 3 Source Register: Market Intelligence, Competitors, and Architectural Sources

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/phase3-source-register.md`  
**Stage:** Phase 3 – Opportunity Identification & Concept Generation  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, and Phase 3 Directives  
**Purpose:** Dedicated master catalog of external evidence, competitor technical documentation, product announcements, operational studies, and regulatory citations gathered during Phase 3 concept generation.

---

## 1. Master Evidence Registry

| Source ID | Title / Document | Publisher / Organization | Date / Period | Primary URL | Evidence Type | Key Technical & Market Claims |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-P3-01** | *AutoAlert CXM Platform & Predictive Propensity Scoring* | AutoAlert Inc. | Nov 2026 | https://www.autoalert.com/solutions/cxm/ | Competitor Product Documentation | AutoAlert combines DMS and CRM transaction records to compute PScore for vehicle upgrade propensity; service retention modules focus on trade equity mining rather than independent aftermarket price benchmarking. |
| **SRC-P3-02** | *Xtime Invite & Inspect Product Portfolio* | Cox Automotive (Xtime) | Nov 2026 | https://www.xtime.com/products/invite/ | Competitor Product Documentation | Xtime Invite automates maintenance marketing based on static OEM mileage/time schedules; Xtime Inspect handles digital MPI with photo/video approvals; lacks dynamic interval cadence degradation modeling. |
| **SRC-P3-03** | *DriveCentric Service Engagement Hub & Omnichannel Messaging* | DriveCentric | Nov 2026 | https://www.drivecentric.com/service | Competitor Product Documentation | Provides conversational AI texting and BDC queue management for service appointment booking; acts as a communication workflow layer without predictive component wear modeling. |
| **SRC-P3-04** | *CDK Predictive Service & CDP Insights Suite* | CDK Global | Nov 2026 | https://www.cdkglobal.com/solutions/service | Competitor Product Documentation | CDK Predictive Service uses historical make/model repair order datasets to predict component failures (e.g., water pump wear) to auto-populate recommended inspection items on electronic MPIs. |
| **SRC-P3-05** | *CDK ShopTrak Electronic Dispatch Board* | CDK Global | Nov 2026 | https://www.shoptrak.com/features | Competitor Product Documentation | Visual dispatch grid displaying technician workloads and open ROs; tracks "Waiting on Parts" (WOP) status passively without enforcing automated pre-dispatch bill-of-materials staging locks. |
| **SRC-P3-06** | *Reynolds & Reynolds ERA-IGNITE Service & Parts Integration* | Reynolds and Reynolds | Nov 2026 | https://www.reyrey.com/solutions/dealership-management/era-ignite | Competitor Product Documentation | Provides native DMS linkage between parts catalog and RO billing lines; places stalled ROs on manual "Parts Hold" queues requiring manual clerk re-notification. |
| **SRC-P3-07** | *OEConnection D2DLink Wholesale Parts Locator Network* | OEConnection (OEC) | Nov 2026 | https://oeconnection.com/solutions/dealers/d2dlink/ | Competitor Product Documentation | Industry-standard B2B parts locator network connecting dealership parts departments across franchise brands for surplus parts trading; operates outside of service bay scheduling and technician queues. |
| **SRC-P3-08** | *Tekion Acquires Five64 to Expand Digital Processing Capabilities* | Tekion Corp. | July 19, 2023 | https://www.tekion.com/news/tekion-acquires-five64 | Corporate Acquisition & Product Release | Tekion acquired Five64 to create Tekion Digital Processing (TDP), providing automated 50-state Tax, Title, and License (TT&L) fee calculation and state-specific DMV registration form population across the US and Canada. |
| **SRC-P3-09** | *Tekion Deal Guard AI & ARC Digital Deal Capabilities* | Tekion Corp. | 2024–2026 | https://www.tekion.com/products/automotive-retail-cloud | Official Product Documentation | Deal Guard AI provides automated driver's license extraction (ID verification), insurance card validity checks, lender contract completeness auditing, and pre-submission error flags. |
| **SRC-P3-10** | *Vitu Interstate Titling & RegUSA Acquisition* | Vitu / NTT DATA | Nov 2026 | https://vitu.com/interstate/ | Competitor Product Documentation | Vitu operates nationwide out-of-state vehicle registration and titling (RegUSA); software calculates fees and prints forms, but physical title document auditing and notary validation remain reliant on manual title clerks. |
| **SRC-P3-11** | *Automotive Titling Company (ATC) Out-of-State Titling APIs* | ATC (Cox Automotive) | Nov 2026 | https://www.autotitling.com/ | Competitor Product Documentation | Provides tax and fee calculation APIs across 3,143 US counties and automated DMV checklist generation; does not autonomously audit scanned trade-in title defect chains or notary jurats. |
| **SRC-P3-12** | *Parts Department Efficiency & Technician Billable Productivity Benchmarks* | Ducker Carlisle (Carlisle & Co.) | 2023–2024 | https://www.duckercarlisle.com/ | Primary Operational Benchmark | Demonstrates technician productivity in un-optimized shops hovers at 80%–92% versus top-quartile shops achieving >110% through pre-staging and automated dispatch rules. |
| **SRC-P3-13** | *Federal Odometer Disclosure Requirements & 20-Year Rolling Exemption Rule* | National Highway Traffic Safety Administration (NHTSA) | 49 CFR Part 580 (2021–2026) | https://www.nhtsa.gov/ | Federal Regulatory Mandate | Amends federal odometer disclosure exemption threshold from 10 years to 20 years for model years 2011 and newer; failure to execute compliant disclosures across title assignments triggers statutory deal rejection. |

---

## 2. Traceability & Methodological Boundaries

1. **Verification Standard:** Competitor capabilities are documented from direct product specifications and corporate press releases, distinguishing verified functionality from marketing assertions.
2. **Tekion Differentiation Standard:** Every Phase 3 concept must be evaluated against Tekion's documented baseline (Tekion ARC Service Bay, Scheduler AI, CRM One View, TDP/Five64, and Deal Guard AI) to ensure concepts do not propose functionality that Tekion has already built or acquired.
