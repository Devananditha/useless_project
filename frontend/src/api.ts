import {
  ScenarioSnapshot,
  SolveResponse,
  CompetingReservationResponse,
  ApprovalResponse,
  AuditEvent,
  BenchmarkResult,
  PolicyId
} from './types';

const API_BASE = '/api';

export async function fetchScenarios(): Promise<ScenarioSnapshot[]> {
  const res = await fetch(`${API_BASE}/scenarios`);
  if (!res.ok) throw new Error(`Failed to fetch scenarios: ${res.statusText}`);
  const data = await res.json();
  return data.scenarios || [];
}

export async function fetchScenario(scenarioId: string): Promise<ScenarioSnapshot> {
  const res = await fetch(`${API_BASE}/scenarios/${scenarioId}`);
  if (!res.ok) throw new Error(`Failed to fetch scenario ${scenarioId}: ${res.statusText}`);
  return res.json();
}

export async function selectScenario(scenarioId: string): Promise<{ snapshot: ScenarioSnapshot }> {
  const res = await fetch(`${API_BASE}/scenarios/${scenarioId}/select`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error(`Failed to select scenario ${scenarioId}: ${res.statusText}`);
  return res.json();
}

export async function runSolve(
  scenarioId: string,
  policyId?: PolicyId
): Promise<SolveResponse> {
  const res = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: scenarioId, policy_id: policyId, compare_a2_p3: true }),
  });
  if (!res.ok) throw new Error(`Solve failed: ${res.statusText}`);
  return res.json();
}

export async function triggerCompetingReservation(
  scenarioId: string,
  sourceId: string = 'S1'
): Promise<CompetingReservationResponse> {
  const res = await fetch(
    `${API_BASE}/scenarios/${scenarioId}/events/competing-reservation?source_id=${sourceId}`,
    { method: 'POST' }
  );
  if (!res.ok) throw new Error(`Failed to trigger competing reservation: ${res.statusText}`);
  return res.json();
}

export async function approveProposal(
  proposalId: string
): Promise<ApprovalResponse> {
  const res = await fetch(`${API_BASE}/proposals/${proposalId}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ proposal_id: proposalId }),
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
  const data = await res.json();
  return data.events || [];
}

export async function resetScenarioStore(scenarioId?: string): Promise<{ status: string }> {
  const url = scenarioId ? `${API_BASE}/reset?scenario_id=${scenarioId}` : `${API_BASE}/reset`;
  const res = await fetch(url, { method: 'POST' });
  if (!res.ok) throw new Error(`Reset failed: ${res.statusText}`);
  return res.json();
}

export async function runBenchmark(numSeeds: number = 100): Promise<BenchmarkResult> {
  const res = await fetch(`${API_BASE}/benchmark/run?n=${numSeeds}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error(`Benchmark run failed: ${res.statusText}`);
  return res.json();
}
