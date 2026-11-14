# StallBreaker — Feasibility-Gated Service Recovery Optimiser
## Tekion Tek-Qubit Hackathon 2026 | Theme 1: AI & Automation (UC04)

StallBreaker resolves service bay immobilization in automotive dealerships caused by parts delivery disruptions through feasibility-gated, joint sourcing and bay scheduling optimization.

### Quick Links
- **Interactive Demonstrator & Quickstart:** See [README_DEMO.md](README_DEMO.md) for step-by-step instructions to run the live backend and React frontend.
- **Final Hackathon Submission Deck:** [submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx](submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx)
- **Speaker Notes & Judge Defense:** [submission/StallBreaker_Pitch_Speaker_Notes.md](submission/StallBreaker_Pitch_Speaker_Notes.md)
- **Multi-Disciplinary Specialist Review:** [submission/StallBreaker_Six_Agent_Review.md](submission/StallBreaker_Six_Agent_Review.md)

---

### Core Performance Highlights (Tested on Canonical Dealership Fixture)
- **Weighted Lateness Reduction:** **66.7%** relative improvement ($99.0 \to 33.0$ weighted ticks)
- **Downstream Fleet Delay Recovered:** **110 minutes** earlier completion for fleet RO-1051
- **Optimization Runtime:** **~30.8 ms** mean solve time via Google OR-Tools CP-SAT
- **N=100 Paired-Seed Benchmark:** **100.0% win/tie rate** against the fixed-source sequential baseline A2
- **Concurrency Safety:** Optimistic snapshot versioning with automated stale-proposal abort and human re-approval gate.

---

### Repository Structure
```
├── backend/                       # Python FastAPI + Google OR-Tools CP-SAT backend
│   ├── benchmark.py               # N=100 paired seeds benchmark runner
│   ├── eligibility.py             # ATP, fitment, quote & physical precondition gates
│   ├── fixtures.py                # Canonical S-MATH-01 and S-MATH-01-ROLLABLE snapshots
│   ├── main.py                    # FastAPI application and REST endpoints
│   ├── models.py                  # Pydantic v2 domain schemas and audit events
│   ├── policies.py                # A2 vs P3 policy comparison engine
│   ├── revalidation.py            # Optimistic concurrency checks & revalidation
│   ├── solver.py                  # Lexicographic dual-objective CP-SAT formulation
│   ├── state_store.py             # In-memory versioned store with audit log
│   └── tests/                     # 16 automated acceptance test suite
├── frontend/                      # Vite + React + TypeScript presentation console
│   ├── src/
│   │   ├── components/            # Gantt, Physical State, Policy Comparison, etc.
│   │   ├── types.ts               # TypeScript data models matching backend schemas
│   │   ├── api.ts                 # Typed API client
│   │   └── App.tsx                # Single-page interactive demonstrator
├── submission/                    # 6-slide PowerPoint submission and defense notes
├── references/                    # Official Tekion problem statements and theme docs
└── README_DEMO.md                 # Demonstrator guide, 3-act script, and startup commands
```
