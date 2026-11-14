import React, { useState, useEffect, useRef } from 'react';
import {
  ScenarioSnapshot,
  PolicyComparisonResult,
  Proposal,
  AuditEvent,
  SolveResponse,
  CompetingReservationResponse,
  ApprovalResponse
} from './types';
import {
  fetchScenarios,
  fetchScenario,
  selectScenario,
  runSolve,
  triggerCompetingReservation,
  approveProposal,
  fetchAuditEvents,
  resetScenarioStore
} from './api';
import { OperationalSummary } from './components/OperationalSummary';
import { PolicyComparisonPanel } from './components/PolicyComparisonPanel';
import { GanttTimeline } from './components/GanttTimeline';
import { PhysicalStatePanel } from './components/PhysicalStatePanel';
import { SourceInventoryPanel } from './components/SourceInventoryPanel';
import { AuditLogPanel } from './components/AuditLogPanel';
import { BenchmarkModal } from './components/BenchmarkModal';
import {
  Wrench,
  Play,
  RotateCcw,
  CheckCircle,
  AlertOctagon,
  BarChart2,
  Cpu,
  Zap
} from './components/Icons';

export const App: React.FC = () => {
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>('S-MATH-01');
  const [currentScenario, setCurrentScenario] = useState<ScenarioSnapshot | null>(null);
  const [comparison, setComparison] = useState<PolicyComparisonResult | null>(null);
  const [activeProposal, setActiveProposal] = useState<Proposal | null>(null);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [successBanner, setSuccessBanner] = useState<string | null>(null);
  const [staleBanner, setStaleBanner] = useState<boolean>(false);
  const [staleMessage, setStaleMessage] = useState<string | null>(null);
  const [benchmarkOpen, setBenchmarkOpen] = useState<boolean>(false);

  // Request cancellation reference to prevent race conditions during scenario switching
  const requestIdRef = useRef<number>(0);

  // Load canonical initial data on application mount
  useEffect(() => {
    loadScenarioData(selectedScenarioId);
  }, []);

  const loadScenarioData = async (scenarioId: string) => {
    const reqId = ++requestIdRef.current;
    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);
      setStaleBanner(false);
      setStaleMessage(null);

      // Invalidate proposal to prevent displaying cross-scenario data
      setActiveProposal(null);
      setComparison(null);

      // 1. Activate scenario in backend state store
      await selectScenario(scenarioId);

      // 2. Fetch fresh snapshot
      const sc = await fetchScenario(scenarioId);
      if (reqId !== requestIdRef.current) return;
      setCurrentScenario(sc);

      // 3. Solve fresh scenario using live CP-SAT
      const solveRes: SolveResponse = await runSolve(scenarioId);
      if (reqId !== requestIdRef.current) return;
      setComparison(solveRes.comparison || null);
      setActiveProposal(solveRes.active_proposal);
      setCurrentScenario(solveRes.snapshot);

      // 4. Fetch audit events
      const evts = await fetchAuditEvents();
      if (reqId !== requestIdRef.current) return;
      setAuditEvents(evts);
    } catch (err: any) {
      if (reqId === requestIdRef.current) {
        setErrorBanner(err.message || `Failed to load scenario ${scenarioId}`);
      }
    } finally {
      if (reqId === requestIdRef.current) {
        setLoading(false);
      }
    }
  };

  const handleScenarioChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newId = e.target.value;
    setSelectedScenarioId(newId);
    loadScenarioData(newId);
  };

  const handleRunSolve = async () => {
    const reqId = ++requestIdRef.current;
    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);
      setStaleBanner(false);
      setStaleMessage(null);

      const solveRes: SolveResponse = await runSolve(selectedScenarioId);
      if (reqId !== requestIdRef.current) return;
      setComparison(solveRes.comparison || null);
      setActiveProposal(solveRes.active_proposal);
      setCurrentScenario(solveRes.snapshot);

      const evts = await fetchAuditEvents();
      if (reqId !== requestIdRef.current) return;
      setAuditEvents(evts);
    } catch (err: any) {
      if (reqId === requestIdRef.current) {
        setErrorBanner(err.message || 'Solver execution failed');
      }
    } finally {
      if (reqId === requestIdRef.current) {
        setLoading(false);
      }
    }
  };

  const handleSimulateStockRace = async () => {
    const reqId = ++requestIdRef.current;
    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);

      const res: CompetingReservationResponse = await triggerCompetingReservation(selectedScenarioId, 'S1');
      if (reqId !== requestIdRef.current) return;
      setCurrentScenario(res.snapshot);

      setStaleBanner(true);
      setStaleMessage(
        `Act 3 Stock-Race: S1 inventory was consumed by an external concurrent buyer (ATP 1 ➔ 0). Snapshot advanced to v${res.new_snapshot_version}. ` +
        `The current active proposal (${activeProposal?.proposal_id || 'P3'}) was formulated under v${activeProposal?.input_snapshot_version} and is now STALE. ` +
        `Attempting to commit this proposal will trigger the optimistic concurrency gate.`
      );

      const evts = await fetchAuditEvents();
      if (reqId !== requestIdRef.current) return;
      setAuditEvents(evts);
    } catch (err: any) {
      if (reqId === requestIdRef.current) {
        setErrorBanner(err.message || 'Failed to simulate competing reservation');
      }
    } finally {
      if (reqId === requestIdRef.current) {
        setLoading(false);
      }
    }
  };

  const handleAdvisorApprove = async () => {
    if (!activeProposal) return;
    const reqId = ++requestIdRef.current;

    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);

      const res: ApprovalResponse = await approveProposal(activeProposal.proposal_id);
      if (reqId !== requestIdRef.current) return;

      if (res.status === 'SCENARIO_MISMATCH') {
        setErrorBanner(`Scenario Mismatch: ${res.message} Please solve and approve within the active scenario.`);
        setStaleBanner(false);
        setSuccessBanner(null);
      } else if (res.status === 'STALE_SNAPSHOT') {
        // Optimistic concurrency gate abort
        setStaleBanner(true);
        setSuccessBanner(null);
        setStaleMessage(
          `STALE PROPOSAL DETECTED (Optimistic Concurrency Gate): Proposal ${res.old_proposal?.proposal_id} evaluated under snapshot v${res.old_proposal?.input_snapshot_version} was REJECTED because live inventory has advanced to v${res.current_snapshot?.snapshot_version}. ` +
          `StallBreaker executed an automated re-solve under v${res.current_snapshot?.snapshot_version} and generated replacement proposal ${res.new_proposal?.proposal_id} selecting ${res.new_proposal?.selected_source_name}. ` +
          `In accordance with safety invariants, human review and explicit re-approval are required before commitment.`
        );

        if (res.current_snapshot) {
          setCurrentScenario(res.current_snapshot);
        }
        if (res.new_proposal) {
          setActiveProposal(res.new_proposal);
        }
        if (res.new_comparison) {
          setComparison(res.new_comparison);
        }
      } else if (res.status === 'APPROVED') {
        // Accepted in local prototype simulation
        setStaleBanner(false);
        setStaleMessage(null);
        setSuccessBanner(
          `Proposal ${res.proposal?.proposal_id || activeProposal.proposal_id} approved and committed to local state (Prototype Simulation — No Real DMS Dispatch).`
        );

        if (res.proposal) {
          setActiveProposal(res.proposal);
          if (comparison) {
            setComparison({
              ...comparison,
              joint_p3: res.proposal,
            });
          }
        }
        if (res.current_snapshot) {
          setCurrentScenario(res.current_snapshot);
        }
      } else {
        setErrorBanner(res.message || `Approval failed with status: ${res.status}`);
      }

      const evts = await fetchAuditEvents();
      if (reqId !== requestIdRef.current) return;
      setAuditEvents(evts);
    } catch (err: any) {
      if (reqId === requestIdRef.current) {
        setErrorBanner(err.message || 'Approval request failed');
      }
    } finally {
      if (reqId === requestIdRef.current) {
        setLoading(false);
      }
    }
  };

  const handleReset = async () => {
    const reqId = ++requestIdRef.current;
    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);
      setStaleBanner(false);
      setStaleMessage(null);
      setActiveProposal(null);
      setComparison(null);

      // Reset backend state store to canonical Act 1 (S-MATH-01, v14)
      await resetScenarioStore();
      setSelectedScenarioId('S-MATH-01');

      const sc = await fetchScenario('S-MATH-01');
      if (reqId !== requestIdRef.current) return;
      setCurrentScenario(sc);

      const solveRes: SolveResponse = await runSolve('S-MATH-01');
      if (reqId !== requestIdRef.current) return;
      setComparison(solveRes.comparison || null);
      setActiveProposal(solveRes.active_proposal);
      setCurrentScenario(solveRes.snapshot);

      const evts = await fetchAuditEvents();
      if (reqId !== requestIdRef.current) return;
      setAuditEvents(evts);
      setSuccessBanner('System successfully reset to Act 1 Canonical Initial State (S-MATH-01, snapshot v14).');
    } catch (err: any) {
      if (reqId === requestIdRef.current) {
        setErrorBanner(err.message || 'Reset failed');
      }
    } finally {
      if (reqId === requestIdRef.current) {
        setLoading(false);
      }
    }
  };

  const isAct1 = selectedScenarioId === 'S-MATH-01';
  const s1Source = currentScenario?.sources.find((s) => s.source_id === 'S1');
  const isS1Available = (s1Source?.atp ?? 0) > 0;

  return (
    <div className="container">
      {/* Top Header */}
      <header style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <div style={{ background: 'var(--accent-cyan)', padding: '6px', borderRadius: '8px', color: '#000', display: 'flex' }}>
              <Wrench size={22} />
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--text-primary)' }}>
              StallBreaker <span style={{ color: 'var(--accent-cyan)', fontWeight: '400', fontSize: '18px' }}>MVP</span>
            </h1>
            <span className="badge badge-optimal">Google OR-Tools CP-SAT</span>
            <span className="badge badge-blue">Tekion Hackathon 2026 UC04</span>
            <span className="badge badge-purple">Single-Rooftop Prototype</span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Feasibility-Gated Service Recovery Optimiser — Resolving Shop Hoist Blocking via Joint Sourcing & Scheduling
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button
            onClick={() => setBenchmarkOpen(true)}
            disabled={loading}
            style={{
              padding: '8px 14px',
              fontSize: '12px',
              fontWeight: '700',
              background: '#1a2638',
              color: 'var(--text-primary)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <BarChart2 size={15} style={{ color: 'var(--accent-cyan)' }} />
            N=100 Benchmark
          </button>

          <button
            onClick={handleReset}
            disabled={loading}
            style={{
              padding: '8px 14px',
              fontSize: '12px',
              fontWeight: '700',
              background: '#1a2638',
              color: 'var(--text-secondary)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <RotateCcw size={15} />
            Reset State
          </button>
        </div>
      </header>

      {/* Control Action Bar */}
      <div className="card" style={{ marginBottom: '16px', background: '#0e1627', borderColor: '#2b3b55' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '14px' }}>
          {/* Scenario Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: '380px', flex: '1 1 380px' }}>
            <span style={{ fontSize: '13px', fontWeight: '800', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>
              Scenario:
            </span>
            <select
              value={selectedScenarioId}
              onChange={handleScenarioChange}
              disabled={loading}
              style={{
                background: '#152136',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                padding: '9px 12px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: '700',
                flex: 1,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              <option value="S-MATH-01">Act 1: Canonical S-MATH-01 (Ford Explorer Immobilized on Hoist)</option>
              <option value="S-MATH-01-ROLLABLE">Act 2: S-MATH-01-ROLLABLE (Ford Explorer Safe to Relocate to H2)</option>
            </select>
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button
              onClick={handleRunSolve}
              disabled={loading}
              style={{
                padding: '9px 18px',
                background: 'var(--accent-cyan)',
                color: '#000',
                fontWeight: '800',
                fontSize: '13px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: '0 2px 8px rgba(6, 182, 212, 0.4)'
              }}
            >
              <Play size={16} fill="#000" />
              {loading ? 'Solving...' : 'Run Solver (Live CP-SAT)'}
            </button>

            <button
              onClick={handleAdvisorApprove}
              disabled={loading || !activeProposal || activeProposal.approval_status === 'APPROVED'}
              style={{
                padding: '9px 18px',
                background: activeProposal?.approval_status === 'APPROVED' ? '#334155' : staleBanner ? 'var(--accent-amber)' : 'var(--accent-emerald)',
                color: activeProposal?.approval_status === 'APPROVED' ? 'var(--text-muted)' : '#000',
                fontWeight: '800',
                fontSize: '13px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: activeProposal?.approval_status === 'APPROVED' ? 'none' : '0 2px 8px rgba(16, 185, 129, 0.4)'
              }}
            >
              <CheckCircle size={16} />
              {activeProposal?.approval_status === 'APPROVED'
                ? 'Proposal Committed (Local Simulation)'
                : staleBanner
                ? 'Approve Replacement Proposal'
                : 'Advisor Approve & Commit'}
            </button>

            <button
              onClick={handleSimulateStockRace}
              disabled={loading || !isAct1 || !isS1Available}
              style={{
                padding: '9px 16px',
                background: !isAct1 ? '#1e293b' : isS1Available ? '#e11d48' : '#334155',
                color: !isAct1 ? '#64748b' : isS1Available ? '#ffffff' : '#94a3b8',
                fontWeight: '700',
                fontSize: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                border: isS1Available && isAct1 ? '1px solid #fda4af' : '1px solid var(--border-color)',
                boxShadow: isS1Available && isAct1 ? '0 0 10px rgba(225, 29, 72, 0.4)' : 'none'
              }}
            >
              <Zap size={14} />
              Simulate Stock Race (Act 3)
            </button>
          </div>
        </div>
      </div>

      {/* Operational Summary Cockpit Bar */}
      <OperationalSummary
        scenario={currentScenario}
        proposal={activeProposal}
        loading={loading}
      />

      {/* Alert Banners */}
      {staleBanner && (
        <div
          style={{
            background: 'rgba(225, 29, 72, 0.15)',
            border: '2px solid #e11d48',
            borderRadius: '8px',
            padding: '16px 20px',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '14px',
            boxShadow: '0 4px 14px rgba(225, 29, 72, 0.25)'
          }}
        >
          <AlertOctagon size={24} style={{ color: '#fda4af', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <div style={{ fontSize: '15px', fontWeight: '900', color: '#fda4af' }}>
              ACT 3: OPTIMISTIC CONCURRENCY GATE TRIGGERED — COMMIT ABORTED
            </div>
            <p style={{ fontSize: '13px', color: '#ffe4e6', marginTop: '4px', lineHeight: '1.45' }}>
              {staleMessage || (
                'Live inventory state advanced while awaiting advisor authorization. In accordance with safety invariants, StallBreaker rejected commitment of the stale proposal, executed an automated re-solve under the latest state, and generated a replacement recovery plan requiring explicit human approval.'
              )}
            </p>
          </div>
        </div>
      )}

      {successBanner && (
        <div
          style={{
            background: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid #10b981',
            borderRadius: '8px',
            padding: '14px 18px',
            marginBottom: '20px',
            color: '#a7f3d0',
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}
        >
          <CheckCircle size={18} style={{ color: '#10b981' }} />
          <span>{successBanner}</span>
        </div>
      )}

      {errorBanner && (
        <div
          style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid #ef4444',
            borderRadius: '8px',
            padding: '14px 18px',
            marginBottom: '20px',
            color: '#fca5a5',
            fontSize: '13px'
          }}
        >
          {errorBanner}
        </div>
      )}

      {/* Main Content Panels */}
      <PolicyComparisonPanel comparison={comparison} loading={loading} />

      <GanttTimeline
        baselineProposal={comparison?.baseline_a2 || null}
        jointProposal={activeProposal || comparison?.joint_p3 || null}
        scenario={currentScenario}
      />

      <PhysicalStatePanel scenario={currentScenario} />

      <SourceInventoryPanel
        scenario={currentScenario}
        onSimulateStockRace={handleSimulateStockRace}
        loading={loading}
      />

      <AuditLogPanel events={auditEvents} />

      {/* Benchmark Modal */}
      <BenchmarkModal isOpen={benchmarkOpen} onClose={() => setBenchmarkOpen(false)} />
    </div>
  );
};
