# Phase 4.4 Jury-Level Concept Comparison: 10 Critical Questions

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.4-jury-level-comparison.md`  
**Stage:** Phase 4.4 – Final Concept Integrity, Comparative Validation & Decision Gate  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Audit Authorities:** Hackathon Jury Evaluator, Senior Product Strategist, Automotive Domain Analyst  
**Date of Audit:** November 14, 2026  
**Audit Finding:** **DIRECT, ADVERSARIAL JURY EVALUATION COMPLETED ACROSS ALL 10 MANDATED QUESTIONS**

---

## 1. Jury Evaluation Mandate

In a high-stakes hackathon with senior engineering directors, venture capitalists, and dealership executives on the jury, superficial marketing claims fail. This audit evaluates **Concept A (TitleGuard)** and **Concept B (PartsRescue AI)** directly against ten critical judging inquiries, stripping away hype and exposing unresolved vulnerabilities.

---

## 2. Direct Answers to the 10 Critical Jury Questions

### Question 1: Which concept solves a clearer dealership problem?
* **Verdict: Concept A (TitleGuard) solves a clearer, more binary problem.**
* **Jury Reasoning:** 
  * TitleGuard addresses a simple, painful reality: a customer trades in an out-of-state car, the title is missing an Arizona notary seal, and $35,000 in financing is frozen for 20 days. Dealership General Managers and CFOs viscerally understand "cash frozen by bad paperwork."
  * PartsRescue addresses a real problem (parts shortages stalling bays), but dealership fixed operations are messy. A stall is caused by multiple overlapping issues (technician efficiency, shop load, bay layout, customer communication delays). The problem is multifaceted and less binary.
* **Unresolved Risk for TitleGuard:** If a dealership operates in a rural single-state market with few out-of-state trade-ins, the problem feels niche.

---

### Question 2: Which concept has a stronger connection to Tekion's actual ecosystem?
* **Verdict: Concept A (TitleGuard) has a stronger non-overlapping connection; Concept B (PartsRescue) has a more direct use-case match.**
* **Jury Reasoning:**
  * TitleGuard directly complements **Tekion Deal Guard AI** and **Tekion Digital Processing (TDP)**. Deal Guard AI audits buyer IDs and retail installment contracts; TDP does digital contracting. Neither touches physical trade-in vehicle titles. TitleGuard fills the exact paper hole between them without competing with native code.
  * PartsRescue directly matches **Theme 1 UC04** (*Service Parts Shortage Resolver Agent*), but heavily intersects with **Tekion ARC Parts Cloud** (native inventory replenishment) and **Tekion ARC Service Cloud** (Smart Tech Matching). Judges from Tekion's service/parts engineering teams may view it as duplicative of internal features.
* **Unresolved Risk for PartsRescue:** Defending against the critique: *"Doesn't our ARC Parts Cloud already track multi-store inventory across dealer groups?"*

---

### Question 3: Which concept demonstrates more meaningful AI/agentic reasoning?
* **Verdict: Concept B (PartsRescue AI) demonstrates substantially more meaningful AI/agentic reasoning.**
* **Jury Reasoning:**
  * TitleGuard is fundamentally a **neuro-symbolic linear pipeline**: VLM extracts structured JSON, and an Abstract Syntax Tree (AST) runs Boolean checks against statutory rules. While robust, an AI researcher on the jury will correctly note that the "AI" is just an off-the-shelf vision model API call, while the real work is a deterministic legal ruleset.
  * PartsRescue demonstrates true **multi-agent orchestration**: it dynamically decides which tools to invoke (OEM supersession lookup vs aftermarket ACES cross-reference), evaluates a multi-objective Pareto optimization curve (cost vs time vs customer promise), plans contingencies (sister-store transfer vs labor resequencing), and drafts natural language customer SMS communications.
* **Unresolved Risk for TitleGuard:** An AI researcher dismissing TitleGuard as *"just a Claude 3.5 Sonnet prompt with a regex/AST rule on the end."*

---

### Question 4: Which concept is more technically defensible?
* **Verdict: Concept A (TitleGuard) is more technically defensible for what it claims; Concept B (PartsRescue) has a more fragile multi-system architecture.**
* **Jury Reasoning:**
  * TitleGuard's technical scope is compact and deterministic: document image $\to$ structured JSON $\to$ local statutory AST rule engine. It executes in milliseconds, has zero moving third-party APIs, and has a clear safe degradation path (escalate to human title clerk when confidence is low).
  * PartsRescue requires integrating live DMS repair orders, OEM EPC supersession trees, third-party distributor inventory feeds, and technician dispatch boards. In production, this architecture is fragile, expensive, and vulnerable to dirty catalog data.
* **Unresolved Risk for PartsRescue:** Technicians will not trust an automated algorithm that changes their scheduled flag-hour jobs unless the data is 100% perfect.

---

### Question 5: Which concept has a more credible data strategy?
* **Verdict: Concept A (TitleGuard) has a far more credible hackathon data strategy.**
* **Jury Reasoning:**
  * TitleGuard relies on **100% authentic, publicly verifiable state statutory motor vehicle codes** (A.R.S. § 28-2058, Cal. Veh. Code § 5753, 49 CFR § 580.17) and public DMV title templates. High-fidelity synthetic PDF deal jackets can be generated and audited without any gated commercial data.
  * PartsRescue relies on **proprietary, paywalled, enterprise-licensed OEM parts catalogs (Snap-on, Microcat) and commercial distributor APIs (Worldpac, OEC)** that no student hackathon team can access live. PartsRescue must rely 100% on a small curated mock dataset, which savvy judges will instantly recognize as simulated.
* **Unresolved Risk for TitleGuard:** TitleGuard still lacks access to live DMV/NMVTIS title records, meaning it cannot verify current legal ownership or undisclosed electronic liens.

---

### Question 6: Which concept can be demonstrated reliably within a hackathon?
* **Verdict: Concept A (TitleGuard) is dramatically more reliable to demonstrate live on stage.**
* **Jury Reasoning:**
  * In a 5-minute pitch, TitleGuard loads a scanned PDF title, passes it to the VLM/AST, and renders a bright red bounding box over the unnotarized Arizona bill of sale in **under 8 seconds**. It is 100% deterministic and cannot suffer multi-agent latency deadlocks.
  * PartsRescue involves multi-step agent tool calling, simulated API queries, mobile phone emulator interactions, and Gantt chart reshuffling. Live agent demonstrations frequently suffer 15–20 second API lags or unpredictable execution paths on stage.
* **Unresolved Risk for PartsRescue:** Live demonstration latency or agent timeout during a strict 5-minute hackathon presentation window.

---

### Question 7: Which concept has a stronger novelty argument?
* **Verdict: Concept B (PartsRescue AI) has a stronger technical novelty argument; Concept A (TitleGuard) has stronger workflow novelty.**
* **Jury Reasoning:**
  * TitleGuard's technical novelty was severely challenged by Yendo's published patent application (**US 2026/0038039 A1**), which explicitly claims machine learning title extraction, multimodal tensors, and downstream used-car dealer applications. TitleGuard's remaining novelty is its showroom intake workflow and state statutory ruleset.
  * PartsRescue offers genuine novelty in applying **autonomous multi-agent planning and multi-objective optimization** to the specific bottleneck of mid-repair service parts stalls.
* **Unresolved Risk for TitleGuard:** An IP-focused judge citing Yendo's published application during Q&A.

---

### Question 8: Which concept has more credible business value?
* **Verdict: Concept A (TitleGuard) for certainty and capital velocity; Concept B (PartsRescue) for nominal operating profit.**
* **Jury Reasoning:**
  * TitleGuard's business case is grounded in direct cost avoidance: avoiding $14.1k in floorplan borrowing interest, $32.4k in expediter fees, and $7.5k in unwinds ($48.1k net cash/yr), while liberating $336,000/month in circulating float. This value has **zero demand-absorption risk**—avoiding fees and borrowing interest is 100% realized immediately.
  * PartsRescue produces **$92.8k net operating gross profit/yr** (moderate baseline), but this profit is **100% dependent on demand absorption**—if the dealership cannot sell the newly unlocked 882 technician hours to customers, incremental profit is zero.
* **Unresolved Risk for PartsRescue:** Skeptical fixed ops judges pointing out that recovering idle hours in a slow service department produces zero incremental revenue.

---

### Question 9: Which concept is more likely to be challenged by judges?
* **Verdict: BOTH concepts face severe, distinct red-team challenges:**
  * **TitleGuard will be attacked on Technical Novelty & Blind Spots:**  
    *"Isn't this just OCR + if/else statements? And without live DMV access, how do you know the car isn't stolen or has a digital lien?"*
  * **PartsRescue will be attacked on Data Access & Tekion Cannibalization:**  
    *"How did you get access to proprietary OEM EPC catalogs? Isn't this all mocked data? And doesn't Tekion ARC Parts Cloud already do this?"*
* **Who Survives the Attack Better?**  
  TitleGuard survives better because its defense is honest and grounded: *"Yes, we use VLM + AST rules, and yes, we focus on surface paperwork compliance before the customer leaves the showroom; we don't pretend to be the DMV."* In contrast, defending a simulated OEM parts network against engineers who build parts software is hazardous.

---

### Question 10: Which concept has the stronger six-slide idea-submission story?
* **Verdict: Concept A (TitleGuard) has a tighter, more compelling six-slide narrative.**
* **Jury Reasoning:**
  * **Slide 1 (The Hook):** $420k in dealership capital frozen because of a missing notary stamp on an out-of-state trade-in.
  * **Slide 2 (The White Space):** Deal Guard AI checks the buyer; TDP checks the e-contract; nobody checks the paper title in the showroom.
  * **Slide 3 (The Solution):** TitleGuard: Showroom intake pre-audit in <10 seconds.
  * **Slide 4 (The Tech):** Neuro-symbolic architecture (Multimodal VLM structured JSON + Deterministic AST Statutory Engine).
  * **Slide 5 (The Economics):** $336k CIT float released, $48.1k net cash saved, 5.72x software ROI.
  * **Slide 6 (The Roadmap):** Tri-state corridor pilot (CA-NV-AZ) expanding to regional dealer networks.
  * This narrative is crisp, visually undeniable, and fits a 6-slide deck effortlessly. PartsRescue's story requires explaining fixed ops door rates, supersession chains, ACES fitment, and Gantt charts, making a 6-slide deck feel crowded.

---

## 3. Summary Scorecard Across 10 Jury Questions

```
+========================================================================================================+
|                                    JURY QUESTIONS HEAD-TO-HEAD SCORECARD                               |
+----+------------------------------------+--------------------------+-----------------------------------+
| #  | Question Dimension                 | Winning Concept          | Decisive Factor                   |
+----+------------------------------------+--------------------------+-----------------------------------+
| 01 | Clearer Dealership Problem         | **Concept A: TitleGuard**| Binary cash pain vs complex ops   |
| 02 | Tekion Ecosystem White Space       | **Concept A: TitleGuard**| Perfect gap filler; no overlap    |
| 03 | Meaningful AI/Agentic Reasoning    | **Concept B: PartsRescue**| True multi-agent planning vs VLM  |
| 04 | Technical Defensibility            | **Concept A: TitleGuard**| Compact local engine; low risk    |
| 05 | Credible Data Strategy             | **Concept A: TitleGuard**| Authentic public statutes vs mock |
| 06 | Live Demo Reliability              | **Concept A: TitleGuard**| <8 sec visual punch; 0 agent lag  |
| 07 | Stronger Novelty Argument          | **Concept B: PartsRescue**| Multi-objective agent vs prior art|
| 08 | Credible Business Value            | **Tie / Differentiated** | TG = Liquidity; PR = Gross Profit |
| 09 | Survivability Under Jury Attack    | **Concept A: TitleGuard**| Honest surface scope vs fake APIs |
| 10 | Stronger 6-Slide Pitch Story       | **Concept A: TitleGuard**| Visually arresting; zero clutter  |
+====+====================================+==========================+===================================+
| **FINAL JURY TALLY**                    | **TitleGuard: 7.5 Wins** | **PartsRescue: 2.5 Wins**         |
+========================================================================================================+
```
