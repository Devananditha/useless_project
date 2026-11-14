import React from 'react';
import { PolicyComparisonResult } from '../types';
import { CheckCircle2, Clock, DollarSign, TrendingDown, Cpu, AlertTriangle } from './Icons';

interface Props {
  comparison: PolicyComparisonResult | null;
  loading: boolean;
}

export const PolicyComparisonPanel: React.FC<Props> = ({ comparison, loading }) => {
  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px 20px' }}>
        <Cpu size={32} style={{ color: 'var(--accent-cyan)', animation: 'spin 1s linear infinite' }} />
        <p style={{ marginTop: '12px', color: 'var(--text-secondary)' }}>
          Executing Google OR-Tools CP-SAT Solver...
        </p>
      </div>
    );
  }

  if (!comparison) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '30px' }}>
        <p style={{ color: 'var(--text-muted)' }}>Click "Run Solver" to execute CP-SAT on the current snapshot.</p>
      </div>
    );
  }

  const { baseline_a2, joint_p3, weighted_lateness_reduction_pct, downstream_lateness_savings_minutes, freight_cost_delta } = comparison;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '16px', marginBottom: '20px' }}>
      {/* Metric Highlight Summary Card */}
      <div className="card" style={{ gridColumn: '1 / -1', background: 'linear-gradient(135deg, #162032 0%, #1a2740 100%)', borderColor: '#2d3f5d' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="badge badge-optimal">LIVE CP-SAT OPTIMIZATION</span>
              <span className="badge badge-blue">Snapshot v{comparison.snapshot_version}</span>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                OR-Tools Runtime: <strong>{joint_p3.solve_time_ms} ms</strong>
              </span>
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: '700', marginTop: '6px', color: 'var(--text-primary)' }}>
              {joint_p3.approval_status === 'STALE_SNAPSHOT' ? (
                <span style={{ color: 'var(--accent-rose)' }}>⚠️ Snapshot Invalidated by Concurrency Conflict</span>
              ) : (
                <span>Joint Sourcing & Schedule Optimization (P3 vs A2)</span>
              )}
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px' }}>
              {comparison.summary_verdict}
            </p>
          </div>

          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{ background: 'rgba(6, 182, 212, 0.1)', border: '1px solid rgba(6, 182, 212, 0.3)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-cyan)', fontWeight: '600', textTransform: 'uppercase' }}>
                Lateness Reduction
              </div>
              <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--accent-cyan)' }}>
                {weighted_lateness_reduction_pct.toFixed(1)}%
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                {baseline_a2.weighted_lateness_ticks} ➔ {joint_p3.weighted_lateness_ticks} weighted ticks
              </div>
            </div>

            <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-emerald)', fontWeight: '600', textTransform: 'uppercase' }}>
                Downstream Delay Saved
              </div>
              <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--accent-emerald)' }}>
                {downstream_lateness_savings_minutes} min
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                RO-1051: 15:15 ➔ {joint_p3.ro1051_finish_clock}
              </div>
            </div>

            <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-amber)', fontWeight: '600', textTransform: 'uppercase' }}>
                Expedited Freight Delta
              </div>
              <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--accent-amber)' }}>
                +${freight_cost_delta}
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                ${baseline_a2.parts_freight_cost} ➔ ${joint_p3.parts_freight_cost}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* A2 Baseline Card */}
      <div className="card">
        <div className="card-title">
          <span>Baseline A2: Fixed-Source Sequential</span>
          <span className="badge" style={{ background: '#334155', color: '#cbd5e1' }}>Sequential</span>
        </div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
          Sequential baseline: parts clerk selects lowest freight cost (S2) first, without bay schedule visibility.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Part Source Chosen</span>
            <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>
              {baseline_a2.selected_source_name} (${baseline_a2.parts_freight_cost})
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Bay B4 Released</span>
            <span style={{ fontWeight: '600', color: 'var(--accent-amber)' }}>{baseline_a2.b4_release_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Finish Time</span>
            <span style={{ fontWeight: '600', color: 'var(--accent-rose)' }}>{baseline_a2.ro1051_finish_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Lateness (Promise: 12:30)</span>
            <span style={{ fontWeight: '600', color: 'var(--accent-rose)' }}>
              {baseline_a2.ro1051_lateness_ticks * 5} min ({baseline_a2.ro1051_lateness_ticks} ticks)
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Total Weighted Lateness (Z₁)</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-rose)' }}>
              {baseline_a2.weighted_lateness_ticks} weighted ticks
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Solver Status</span>
            <span className="badge badge-optimal">{baseline_a2.solver_status} ({baseline_a2.solve_time_ms} ms)</span>
          </div>
        </div>
      </div>

      {/* P3 Joint Optimization Card */}
      <div className="card" style={{ borderColor: 'var(--accent-cyan)' }}>
        <div className="card-title">
          <span style={{ color: 'var(--accent-cyan)' }}>StallBreaker P3: Joint Optimization</span>
          <span className="badge badge-optimal">RECOMMENDED PROPOSAL</span>
        </div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
          Simultaneous sourcing & dispatch optimization: models bay occupancy and downstream fleet schedule.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Part Source Chosen</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-cyan)' }}>
              {joint_p3.selected_source_name} (${joint_p3.parts_freight_cost})
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Bay B4 Released</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-emerald)' }}>{joint_p3.b4_release_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Finish Time</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-emerald)' }}>{joint_p3.ro1051_finish_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Lateness (Promise: 12:30)</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-emerald)' }}>
              {joint_p3.ro1051_lateness_ticks * 5} min ({joint_p3.ro1051_lateness_ticks} ticks)
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Total Weighted Lateness (Z₁)</span>
            <span style={{ fontWeight: '800', color: 'var(--accent-emerald)' }}>
              {joint_p3.weighted_lateness_ticks} weighted ticks
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Vehicle Movement</span>
            <span className="badge badge-purple">{joint_p3.selected_movement}</span>
          </div>
        </div>

        {/* Feasibility Reasons / Justification */}
        <div style={{ marginTop: '14px', background: 'rgba(0, 0, 0, 0.25)', borderRadius: '6px', padding: '10px 12px' }}>
          <div style={{ fontSize: '11px', fontWeight: '700', color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '4px' }}>
            Feasibility Explanations:
          </div>
          <ul style={{ paddingLeft: '16px', fontSize: '12px', color: 'var(--text-secondary)' }}>
            {joint_p3.feasibility_explanations.map((exp, i) => (
              <li key={i}>{exp}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Policy Scope & Comparison Disclaimer */}
      <div style={{ gridColumn: '1 / -1', padding: '10px 14px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid var(--border-color)', borderRadius: '6px', fontSize: '11px', color: 'var(--text-muted)' }}>
        <strong>Implementation Boundary:</strong> Only A2 (study-defined fixed-source baseline) and P3 (joint sourcing and scheduling policy) are implemented as active comparison policies. P0 (unrecovered stall) and P1 (manager heuristic) are not implemented as competing policies in this prototype.
      </div>
    </div>
  );
};
