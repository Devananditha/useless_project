# Phase 4.4 Candidate Feasibility and Alignment Audit: PartsRescue AI

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.4-partsrescue-alignment-and-feasibility.md`  
**Stage:** Phase 4.4 – Final Concept Integrity, Comparative Validation & Decision Gate  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`  
**Audit Authorities:** AI/ML Solutions Architect, Automotive Operations Expert, Hackathon Jury Evaluator  
**Date of Audit:** November 14, 2026  
**Audit Finding:** **OFFICIAL USE CASE ALIGNMENT CORRECTED TO UC04; 10-STEP AGENTIC WORKFLOW DECONSTRUCTED; DATA ARCHITECTURE GROUNDED IN HYBRID DETERMINISTIC/ML DESIGN**

---

## 1. Official Theme & Use-Case Correction

In Phase 4.3, PartsRescue AI was described as spanning "Theme 1 UC04 / UC01" and UC01 was mislabeled as "Automated Technician Dispatch & Bay Allocation." 

Under strict audit against `references/tekion-themes.pdf`, the official text defines:
* **Theme 1: AI & Automation – Intelligent Solutions for Operations**
  * **UC01: Autonomous Appointment & Dispatch Orchestrator:** *"A multi-agent system that re-optimizes technician assignments and bay allocation in real time as parts delays, no-shows, or urgent walk-ins occur."*
  * **UC04: Service Parts Shortage Resolver Agent:** *"An agent that detects a repair order stalled on a missing part, automatically checks sister store and vendor stock, and proposes a resequenced schedule so the bay is not idle."*

### Official Use-Case Correction:
1. **Primary Alignment:** PartsRescue AI is primarily and unequivocally aligned with **Theme 1 UC04 (Service Parts Shortage Resolver Agent)**.
2. **UC01 Clarification:** PartsRescue AI does **not** manage initial customer appointment scheduling or full-shop dispatching from scratch. It touches technician dispatch only at the point of parts exception handling. Therefore, claiming UC01 as a primary use case is **withdrawn**. UC01 is retained strictly as an upstream integration interface.

---

## 2. Technical & Operational Coherence of the 10-Step Workflow

We evaluate the proposed 10-step recovery workflow for technical realism and operational feasibility:

```
+========================================================================================================================+
|                                    10-STEP PARTSRESCUE RECOVERY WORKFLOW EVALUATION                                    |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| #  | Workflow Step                  | Technical Primitive   | Operational Feasibility & Failure Modes                  |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 01 | **Shortage Detection**         | Event Listener / Webhook| HIGH. Triggered when RO parts status transitions to     |
|    |                                | on DMS parts line item| `BACKORDER` or `OOS` (Out of Stock).                   |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 02 | **Affected RO Identification** | DMS Relational Query  | HIGH. Pulls customer promise time, assigned tech, bay #, |
|    |                                |                       | and current vehicle teardown stage.                      |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 03 | **Compatibility Analysis**     | **Deterministic Table**| HIGH (if deterministic). **NEVER rely on raw LLM!** Must |
|    |                                | (ACES/PIES schema)    | query verified catalog attributes (engine, trim, year).  |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 04 | **OEM Supersession Check**     | Directed Acyclic Graph| HIGH (if deterministic). Traverses manufacturer part     |
|    |                                | (DAG) lookup          | lineage (e.g., Rev A $\to$ Rev B $\to$ Rev C).           |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 05 | **Multi-Source Sourcing**      | Concurrency / Async   | HIGH (simulated). Queries sister store inventory, regional|
|    |                                | API queries           | OEM PDC, and local aftermarket distributors (NAPA/World).|
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 06 | **Tradeoff Modeling**          | **Discrete Multi-Obj**| HIGH. Solves Pareto curve: courier fee vs bay idle cost  |
|    |                                | **Optimization**      | vs customer promise time vs warranty constraints.        |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 07 | **Recovery Recommendation**    | LLM Synthesis & Rationale| HIGH. Synthesizes structured options with natural     |
|    |                                | Formatting            | language justifications for human decision-maker.        |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 08 | **Human-in-the-Loop Sign-off** | Interactive UI Card / | **MANDATORY GATE.** Advisor or parts manager must click  |
|    |                                | Mobile SMS Gateway    | approval before purchase order or schedule shifts fire.  |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 09 | **Workflow Execution**         | DMS API / SMS Webhook | HIGH (simulated). Updates parts requisition, dispatches  |
|    |                                |                       | hotshot courier, and shifts technician queue.            |
+----+--------------------------------+-----------------------+----------------------------------------------------------+
| 10 | **Telemetry & Outcome Log**    | Event Log / Analytics | HIGH. Logs recovery latency, cost variance, technician   |
|    |                                |                       | idle time saved, and advisor acceptance rate.            |
+========================================================================================================================+
```

---

## 3. Separation of Responsibilities: Rules vs AI vs Optimization

A critical architectural flaw in many AI hackathon concepts is treating the Large Language Model as an all-knowing oracle. In automotive fixed operations, an LLM hallucinating a mechanical part fitment can cause catastrophic engine failure or void customer warranties.

PartsRescue AI must strictly partition its logic into three architectural layers:

```mermaid
flowchart TD
    subgraph Deterministic Layer ["1. Deterministic Layer (Zero Hallucination)"]
        D1["OEM Supersession DAG"]
        D2["ACES/PIES Fitment Schema"]
        D3["Warranty vs Customer-Pay Rules"]
    end
    subgraph Optimization Layer ["2. Discrete Optimization Layer"]
        O1["Cost vs ETA Tradeoff Solver"]
        O2["Bay Idle vs Courier Cost Objective Function"]
        O3["Technician Flag-Hour Re-allocator"]
    end
    subgraph Agentic / AI Layer ["3. Generative AI / Agentic Layer"]
        A1["Unstructured Tech Notes Parsing"]
        A2["Multi-Agent Dialogue & Tool Selection"]
        A3["Customer SMS Communication Drafter"]
        A4["Natural Language Rationale Formatter"]
    end
    Deterministic Layer --> Optimization Layer
    Optimization Layer --> Agentic / AI Layer
```

1. **Deterministic Layer (Rules & Relational Lookups):**
   * *Fitment & Compatibility:* An LLM is **strictly forbidden** from predicting whether an alternator fits a vehicle. Fitment must be determined via deterministic lookup against ACES/PIES attribute databases.
   * *Warranty Eligibility:* OEM warranty work strictly forbids aftermarket substitutions. This is a hard Boolean constraint.
2. **Optimization Layer (Discrete Algorithms):**
   * Evaluating whether to pay a $25 hotshot courier fee to save 2 hours of bay downtime ($170 value) is calculated via standard linear programming or greedy cost-benefit optimization, not generative text.
3. **Agentic / AI Layer (Generative Orchestration):**
   * Parsing unstructured technician diagnostic notes ("Bracket sheared off during teardown; need secondary bolt kit").
   * Orchestrating asynchronous queries across multiple tools and consolidating findings.
   * Generating clear, transparent trade-off explanations for the service advisor.
   * Drafting customer-facing SMS explanations for aftermarket substitution authorizations.

---

## 4. Hackathon Demonstration vs Production Deployment

Under `.cursor/rules/research-standards.mdc`, we transparently separate what can be demonstrated in a hackathon sprint from what requires enterprise production infrastructure:

```
+========================================================================================================+
|                               HACKATHON DEMO VS PRODUCTION DEPLOYMENT REALITY                          |
+--------------------------+---------------------------------+-------------------------------------------+
| Dimension                | Hackathon Demonstration Scope   | Enterprise Production Reality             |
+--------------------------+---------------------------------+-------------------------------------------+
| **Repair Orders (RO)**   | 15–20 high-fidelity synthetic   | Live bidirectional integration with Tekion|
|                          | JSON RO fixtures.               | ARC Service Cloud REST APIs / Webhooks.   |
+--------------------------+---------------------------------+-------------------------------------------+
| **Parts Compatibility &**| Curated dataset: **8 vehicle**  | Enterprise licensing of OEM Electronic    |
| **Supersession Data**    | **archetypes**, ~30 parts DAGs. | Parts Catalogs (Microcat, Snap-on EPC).   |
+--------------------------+---------------------------------+-------------------------------------------+
| **Wholesale Supplier**   | Mock REST API server simulating | Commercial enterprise developer agreements|
| **Inventory & ETAs**     | latency, stock, and courier fees| and EDI integrations (Worldpac, OEC, LKQ).|
+--------------------------+---------------------------------+-------------------------------------------+
| **Shop Capacity & Bays** | Simulated 12-bay shop state with| Live DMS shop floor punch-clock and       |
|                          | active lift / technician status.| technician electronic dispatch boards.    |
+--------------------------+---------------------------------+-------------------------------------------+
| **Customer Interaction** | Interactive mobile web card via | Automated carrier SMS gateway with        |
|                          | simulated smartphone simulator. | customer profile authentication.          |
+========================================================================================================+
```

### Critical Evidentiary Answers:
* **Can the problem be demonstrated convincingly without live OEM APIs?**  
  **Yes**, provided the team openly presents the curated dataset as a realistic representative sample (e.g., Ford F-150 brake caliper, Toyota RAV4 alternator, Chevy Silverado solenoid) rather than claiming fake live integrations.
* **What is the minimum credible dataset?**  
  **8 vehicle archetypes** covering 4 warranty scenarios and 4 customer-pay scenarios, with 20–30 parts relationships (OEM superseded part numbers and certified aftermarket equivalents).
* **What happens when compatibility or availability is uncertain?**  
  The system triggers **Safe Degradation**: marks the line item as "Unverified Compatibility," pauses automated routing, and alerts the Human Parts Specialist.

---

## 5. Audit Conclusion

PartsRescue AI is technically and operationally coherent when structured as a **hybrid deterministic-optimization-agentic system**. It aligns cleanly with **Theme 1 UC04**. Its primary limitation is the impossibility of connecting to live OEM parts catalogs in a hackathon, necessitating a transparent, curated synthetic scenario demonstration.
