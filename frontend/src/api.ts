import {
  ScenarioSnapshot,
  PolicyComparisonResult,
  Proposal,
  AuditEvent,
  BenchmarkResult,
  PolicyId
} from './types';

const API_BASE = '/api';

export async function fetchScenarios(): Promise<ScenarioSnapshot[]> {
  const res = await fetch(`${API_BASE}/scenarios`);
  if (!res.ok) throw new Error(`Failed to fetch scenarios: ${res.statusText}`);
  return res.json();
}

export async function fetchScenario(scenarioId: string): Promise<ScenarioSnapshot> {
  const res = await fetch(`${API_BASE}/scenarios/${scenarioId}`);
  if (!res.ok) throw new Error(`Failed to fetch scenario ${scenarioId}: ${res.statusText}`);
  return res.json();
}

export async function runSolve(
  scenarioId: string,
  policyId?: PolicyId
): Promise<PolicyComparisonResult> {
  const res = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: scenarioId, policy_id: policyId }),
  });
  if (!res.ok) throw new Error(`Solve failed: ${res.statusText}`);
  return res.json();
}

export async function triggerCompetingReservation(
  scenarioId: string,
  sourceId: string = 'S1'
): Promise<{ scenario: ScenarioSnapshot; event: AuditEvent }> {
  const res = await fetch(
    `${API_BASE}/scenarios/${scenarioId}/events/competing-reservation?source_id=${sourceId}`,
    { method: 'POST' }
  );
  if (!res.ok) throw new Error(`Failed to trigger competing reservation: ${res.statusText}`);
  return res.json();
}

export async function approveProposal(
  proposal: Proposal,
  approverRole: string = 'Service Advisor'
): Promise<{
  success: boolean;
  status: string;
  reason?: string;
  proposal: Proposal;
  new_comparison?: PolicyComparisonResult;
}> {
  const res = await fetch(`${API_BASE}/proposals/${proposal.proposal_id}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ proposal, approver_role: approverRole }),
  });
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Approval request failed: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAuditEvents(): Promise<AuditEvent[]> {
  const res = await fetch(`${API_BASE}/events`);
  if (!res.ok) throw new Error(`Failed to fetch events: ${res.statusText}`);
  return res.json();
}

export async function resetScenarioStore(scenarioId?: string): Promise<{ status: string }> {
  const url = scenarioId ? `${API_BASE}/reset?scenario_id=${scenarioId}` : `${API_BASE}/reset`;
  const res = await fetch(url, { method: 'POST' });
  if (!res.ok) throw new Error(`Reset failed: ${res.statusText}`);
  return res.json();
}

export async function runBenchmark(numSeeds: number = 100): Promise<BenchmarkResult> {
  const res = await fetch(`${API_BASE}/benchmark/run?num_seeds=${numSeeds}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error(`Benchmark run failed: ${res.statusText}`);
  return res.json();
}
