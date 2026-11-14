# Tekion Tek-Qubit Hackathon 2026 workspace

This workspace prepares idea-submission research for the Tekion Tek-Qubit Hackathon 2026. It holds specialist agent definitions, evidence rules, and empty phase folders. It does not contain a chosen idea, a prototype, or a slide deck.

**Research first. Challenge assumptions. Evaluate alternatives. Select only after evidence-based comparison.**

## Hackathon context

- Event: Tekion Tek-Qubit Hackathon 2026.
- Stage: idea submission.
- Deliverable: a PowerPoint presentation of at most six slides.
- Team size: 2–4 members.
- Immediate objective: select the strongest defensible idea.
- Current scope: research, problem discovery, differentiation, and feasibility.
- Prototype development stays out of scope until the user explicitly asks for it.

Official themes:

1. AI & Automation – Intelligent Solutions for Operations.
2. Data Analytics – Insights from Customer Data.
3. Customer Experience – Seamless Digital Interactions.
4. Sustainability – Green Tech for Automotive Retail.

Detailed official use cases come from `references/tekion-themes.pdf`. Read that file before claiming an official requirement. If it is absent, record the gap. Do not invent use cases.

## Specialist agents

Project subagents live in `.cursor/agents/`. Each is read-only (`readonly: true`), uses `model: inherit`, and runs in the foreground. They return analysis to the parent agent. They do not edit the workspace.

| Agent | File | Responsibility |
| --- | --- | --- |
| Product Strategist | `.cursor/agents/product-strategist.md` | Find high-value automotive retail problems, map stakeholders, and recommend what to investigate across all four themes. |
| Market Researcher | `.cursor/agents/market-researcher.md` | Research Tekion's public products, competitors, and existing solutions with traceable sources. |
| Automotive Analyst | `.cursor/agents/automotive-analyst.md` | Map dealership workflows and adoption barriers across service, inventory, F&I, customer engagement, and EV operations. |
| AI Architect | `.cursor/agents/ai-architect.md` | Judge whether AI is necessary and whether a shortlisted concept is technically credible. |
| Innovation Critic | `.cursor/agents/innovation-critic.md` | Challenge novelty, overlap, and weak evidence. Default to scepticism. |
| Pitch Strategist | `.cursor/agents/pitch-strategist.md` | Shape an approved idea into a six-slide narrative. Do not create the PowerPoint during research. |

Invoke one explicitly with `/product-strategist`, `/market-researcher`, `/automotive-analyst`, `/ai-architect`, `/innovation-critic`, or `/pitch-strategist`, or ask the parent agent to use that subagent by name.

Subagents start from their own instructions and do not see earlier chat unless the parent includes it. Pass the question, the relevant notes, and the evidence standard in the delegation prompt.

The Innovation Critic must not be asked to endorse another agent's conclusion. Independent agreement is not proof.

## Project rules

Both rules use `alwaysApply: true`.

- `.cursor/rules/research-standards.mdc` — no fabricated evidence; cite URLs and dates; separate facts, findings, assumptions, hypotheses, and recommendations; state confidence and gaps; do not treat a proposal as a built or validated system.
- `.cursor/rules/tekion-context.mdc` — event, stage, six-slide limit, team size, four themes, PDF as the source of official use cases, and no prototype until the user asks.

## Reference material

`references/agency-agents/` is a shallow clone of [agency-agents](https://github.com/msitarzewski/agency-agents), kept as read-only methodology. Do not edit it. The six hackathon agents adapt only these definitions:

- `product/product-manager.md` — problem before solution, opportunity assessment.
- `product/product-trend-researcher.md` — competitive landscape and sourced market research.
- `design/design-ux-researcher.md` — workflow and journey analysis with a stated research question.
- `engineering/engineering-ai-engineer.md` — when an AI method is justified, and what data it needs.
- `engineering/engineering-multi-agent-systems-architect.md` — least privilege, failure modes, and human review.
- `engineering/engineering-data-engineer.md` — data contracts, quality, and lineage as requirements.
- `engineering/engineering-rapid-prototyper.md` — hypotheses and success criteria before any build.
- `testing/testing-reality-checker.md` and `testing/testing-evidence-collector.md` — claims without evidence fail.
- `strategy/playbooks/phase-0-discovery.md` and `strategy/playbooks/phase-1-strategy.md` — discovery before commitment. Those playbooks are not this team's phase plan.

No final idea can be selected without explicit user approval.

## Later research sequence

Do not run these phases until the user instructs it.

1. Understand Tekion's publicly documented product ecosystem.
2. Research dealership problems and industry workflows.
3. Generate a broad set of potential opportunities.
4. Investigate existing competitors and overlapping solutions.
5. Shortlist and score promising ideas.
6. Conduct independent technical feasibility analysis.
7. Conduct a rigorous novelty and red-team review.
8. Select one final idea with user approval.
9. Develop the six-slide submission.

Folders reserved for that later work: `research/`, `evaluation/`, `architecture/`, and `submission/`. They contain no findings yet.
