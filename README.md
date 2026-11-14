# StallBreaker — Feasibility-Gated Service Recovery Optimiser
## Tekion Tek-Qubit Hackathon 2026 | Theme 1: AI & Automation (UC04)

StallBreaker resolves service bay immobilization in automotive dealerships caused by parts delivery disruptions through feasibility-gated, joint sourcing and bay scheduling optimization evaluated via Google OR-Tools CP-SAT.

### Quick Links
- **Interactive Demonstrator & Quickstart:** See [README_DEMO.md](README_DEMO.md) for step-by-step instructions to run the live backend and React frontend.
- **Final Hackathon Submission Deck:** [submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx](submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx)
- **Speaker Notes & Judge Defense:** [submission/StallBreaker_Pitch_Speaker_Notes.md](submission/StallBreaker_Pitch_Speaker_Notes.md)
- **Multi-Disciplinary Specialist Review:** [submission/StallBreaker_Six_Agent_Review.md](submission/StallBreaker_Six_Agent_Review.md)

---

### Core Performance Highlights (Synthetic Benchmark Fixture S-MATH-01)
> **Note on Empirical Scope:** The numerical results below belong strictly to the study-defined synthetic canonical disruption fixture `S-MATH-01` and its paired-seed distributions. They represent model-derived outcomes, not measured field results from live dealership operations.

- **Weighted Lateness Reduction:** **66.7%** relative improvement ($99.0 \to 33.0$ weighted ticks) on `S-MATH-01`.
- **Downstream Fleet Delay Recovered:** **110 minutes** ($22$ ticks) earlier completion for fleet RO-1051.
- **Optimization Runtime:** **~30.8 ms** mean solve time via Google OR-Tools CP-SAT across 100 paired seeds.
- **N=100 Synthetic Paired Benchmark:** **100.0% win/tie rate** against the study-defined fixed-source sequential baseline A2.
- **Concurrency Safety:** Optimistic snapshot versioning with automated stale-proposal abort and mandatory human re-approval gate.

---

### Implementation Scope & Honest Boundaries

**Implemented and Tested:**
- Local scenario snapshots (`S-MATH-01` and `S-MATH-01-ROLLABLE`) with 5-minute ticks ($t=0$ at 08:00, horizon $H=108$ at 17:00).
- Deterministic pre-solver eligibility gates (ATP availability, fitment catalog match, active price quotes, vehicle relocation preconditions).
- Google OR-Tools CP-SAT solver formulation optimizing sourcing choice and vehicle movement with multi-pass lexicographic objectives ($Z_1$ lateness minimization, then $Z_3$ freight cost minimization).
- A2 vs P3 policy comparison engine.
- Physical state machine transitions with explicit clearance delays ($k=2$ ticks / 10 min) and return transit ($3$ ticks / 15 min).
- Optimistic concurrency versioning (snapshot tokens) preventing stale proposal commitments during external stock-race events.
- Local prototype human-in-the-loop approval workflow (simulation of advisor authorization).
- Automated test suite (27 passing tests covering arithmetic, physical invariants, API contracts, read-only GETs, and concurrency).
- Reproducible N=100 synthetic benchmark with individual seed inspection and JSON artifact generation.

**Not Implemented / Out of Scope:**
- No live Tekion DMS integration or production API connectivity.
- No real-world inventory reservation, parts ordering, or external courier dispatch.
- No production deployment or multi-tenant hosting.
- No general-purpose multi-rooftop dealership chain optimization.
- No arbitrary multi-job job-shop interval scheduling engine; the CP-SAT formulation models combinatorial sourcing selection and movement branch optimization over milestones and lateness objectives for the bounded single-rooftop recovery problem.
- Policies P0 (wait / unrecovered stall) and P1 (generic manager heuristic) are not implemented as competing policies in the active demonstration.

---

### Repository Structure
```
├── backend/                       # Python FastAPI + Google OR-Tools CP-SAT backend
│   ├── benchmark.py               # N=100 paired seeds benchmark runner with JSON artifacts
│   ├── eligibility.py             # ATP, fitment, quote & physical precondition gates
│   ├── fixtures.py                # Canonical S-MATH-01 and S-MATH-01-ROLLABLE snapshots
│   ├── main.py                    # FastAPI application and REST endpoints
│   ├── models.py                  # Pydantic v2 domain schemas and audit events
│   ├── policies.py                # A2 vs P3 policy comparison engine
│   ├── revalidation.py            # Optimistic concurrency checks & revalidation
│   ├── solver.py                  # Lexicographic dual-objective CP-SAT formulation
│   ├── state_store.py             # In-memory versioned store with audit log
│   └── tests/                     # 27 automated acceptance and integration tests
├── frontend/                      # Vite + React + TypeScript presentation console
│   ├── src/
│   │   ├── components/            # Gantt, Physical State, Policy Comparison, Benchmark modal
│   │   ├── types.ts               # TypeScript data models matching backend schemas
│   │   ├── api.ts                 # Typed API client
│   │   └── App.tsx                # Single-page interactive demonstrator
├── generated-results/             # Generated benchmark JSON artifacts
├── submission/                    # 6-slide PowerPoint submission and defense notes
├── references/                    # Official Tekion problem statements and theme docs
└── README_DEMO.md                 # Demonstrator guide, 3-act script, and startup commands
```
