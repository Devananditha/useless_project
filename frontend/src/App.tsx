import React, { useState, useEffect } from 'react';
import {
  ScenarioSnapshot,
  PolicyComparisonResult,
  Proposal,
  AuditEvent
} from './types';
import {
  fetchScenarios,
  fetchScenario,
  runSolve,
  triggerCompetingReservation,
  approveProposal,
  fetchAuditEvents,
  resetScenarioStore
} from './api';
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
  Layers
} from './components/Icons';

export const App: React.FC = () => {
  const [scenarios, setScenarios] = useState<ScenarioSnapshot[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>('S-MATH-01');
  const [currentScenario, setCurrentScenario] = useState<ScenarioSnapshot | null>(null);
  const [comparison, setComparison] = useState<PolicyComparisonResult | null>(null);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [successBanner, setSuccessBanner] = useState<string | null>(null);
  const [staleBanner, setStaleBanner] = useState<boolean>(false);
  const [benchmarkOpen, setBenchmarkOpen] = useState<boolean>(false);

  // Initialize
  useEffect(() => {
    loadInitialData();
  }, [selectedScenarioId]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      setErrorBanner(null);
      setStaleBanner(false);
      setSuccessBanner(null);

      const scList = await fetchScenarios();
      setScenarios(scList);

      const sc = await fetchScenario(selectedScenarioId);
      setCurrentScenario(sc);

      // Automatically solve upon initial load
      const comp = await runSolve(selectedScenarioId);
      setComparison(comp);

      const evts = await fetchAuditEvents();
      setAuditEvents(evts);
    } catch (err: any) {
      setErrorBanner(err.message || 'Failed to initialize app state');
    } finally {
      setLoading(false);
    }
  };

  const handleScenarioChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedScenarioId(e.target.value);
  };

  const handleRunSolve = async () => {
    try {
      setLoading(true);
      setErrorBanner(null);
      setStaleBanner(false);
      setSuccessBanner(null);

      const comp = await runSolve(selectedScenarioId);
      setComparison(comp);

      const sc = await fetchScenario(selectedScenarioId);
      setCurrentScenario(sc);

      const evts = await fetchAuditEvents();
      setAuditEvents(evts);
    } catch (err: any) {
      setErrorBanner(err.message || 'Solver execution failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateStockRace = async () => {
    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);

      const { scenario } = await triggerCompetingReservation(selectedScenarioId, 'S1');
      setCurrentScenario(scenario);

      const evts = await fetchAuditEvents();
      setAuditEvents(evts);
    } catch (err: any) {
      setErrorBanner(err.message || 'Failed to simulate competing reservation');
    } finally {
      setLoading(false);
    }
  };

  const handleAdvisorApprove = async () => {
    if (!comparison?.joint_p3) return;

    try {
      setLoading(true);
      setErrorBanner(null);
      setSuccessBanner(null);

      const res = await approveProposal(comparison.joint_p3, 'Service Advisor');

      if (res.status === 'APPROVED') {
        setStaleBanner(false);
        setSuccessBanner(
          `Proposal ${res.proposal.proposal_id} APPROVED by Service Advisor. Bay B4 dispatch lock acquired and part dispatched.`
        );
      }

      // Update comparison
      if (res.new_comparison) {
        setComparison(res.new_comparison);
      } else {
        setComparison({
          ...comparison,
          joint_p3: res.proposal,
        });
      }

      const sc = await fetchScenario(selectedScenarioId);
      setCurrentScenario(sc);

      const evts = await fetchAuditEvents();
      setAuditEvents(evts);
    } catch (err: any) {
      // Check if stale snapshot error occurred
      const msg = err.message || '';
      if (msg.includes('STALE_SNAPSHOT') || msg.includes('stale snapshot') || msg.includes('concurrency')) {
        setStaleBanner(true);
        // Refresh scenario and solve
        const sc = await fetchScenario(selectedScenarioId);
        setCurrentScenario(sc);
        const comp = await runSolve(selectedScenarioId);
        setComparison(comp);
        const evts = await fetchAuditEvents();
        setAuditEvents(evts);
      } else {
        setErrorBanner(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      setLoading(true);
      await resetScenarioStore(selectedScenarioId);
      await loadInitialData();
    } catch (err: any) {
      setErrorBanner(err.message || 'Reset failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* Top Header */}
      <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ background: 'var(--accent-cyan)', padding: '6px', borderRadius: '8px', color: '#000', display: 'flex' }}>
              <Wrench size={22} />
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: '800', letterSpacing: '-0.02em' }}>
              StallBreaker <span style={{ color: 'var(--accent-cyan)', fontWeight: '400', fontSize: '18px' }}>MVP</span>
            </h1>
            <span className="badge badge-optimal">Google OR-Tools CP-SAT</span>
            <span className="badge badge-blue">Tekion Hackathon 2026 UC04</span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Feasibility-Gated Service Recovery Optimiser — Resolving Shop Hoist Blocking via Joint Sourcing & Scheduling
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button
            onClick={() => setBenchmarkOpen(true)}
            style={{
              padding: '8px 14px',
              fontSize: '12px',
              fontWeight: '600',
              background: '#1e293b',
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
            style={{
              padding: '8px 14px',
              fontSize: '12px',
              fontWeight: '600',
              background: '#1e293b',
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
      <div className="card" style={{ marginBottom: '20px', background: '#0e1627', borderColor: '#2b3b55' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
          {/* Scenario Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', minWidth: '320px' }}>
            <span style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-secondary)' }}>
              Scenario:
            </span>
            <select
              value={selectedScenarioId}
              onChange={handleScenarioChange}
              style={{
                background: '#162238',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                padding: '8px 12px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: '600',
                flex: 1
              }}
            >
              <option value="S-MATH-01">Act 1: Canonical S-MATH-01 (Immobilized Vehicle on Hoist)</option>
              <option value="S-MATH-01-ROLLABLE">Act 2: S-MATH-01-ROLLABLE (Vehicle Relocatable to H2)</option>
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
                fontWeight: '700',
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
              disabled={loading || !comparison?.joint_p3}
              style={{
                padding: '9px 18px',
                background: 'var(--accent-emerald)',
                color: '#000',
                fontWeight: '700',
                fontSize: '13px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: '0 2px 8px rgba(16, 185, 129, 0.4)'
              }}
            >
              <CheckCircle size={16} />
              Advisor Approve & Commit
            </button>
          </div>
        </div>
      </div>

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
            gap: '14px'
          }}
        >
          <AlertOctagon size={24} style={{ color: '#fda4af', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <div style={{ fontSize: '15px', fontWeight: '800', color: '#fda4af' }}>
              ACT 3: STALE SNAPSHOT DETECTED — AUTOMATED COMMIT ABORTED
            </div>
            <p style={{ fontSize: '13px', color: '#ffe4e6', marginTop: '4px' }}>
              Snapshot version advanced (v14 ➔ v15) while awaiting advisor authorization because competing repair order RO-1099 claimed S1 (Metro Courier).
              In accordance with safety invariants, StallBreaker aborted commit, triggered an automated re-solve under v15 (which selected S2), and flagged that human re-approval is mandatory before dispatch.
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
        jointProposal={comparison?.joint_p3 || null}
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
