import React from 'react';
import { PolicyComparisonResult } from '../types';
import { CheckCircle2, Clock, DollarSign, TrendingDown, Cpu, AlertTriangle, ArrowRight } from './Icons';

interface Props {
  comparison: PolicyComparisonResult | null;
  loading: boolean;
}

export const PolicyComparisonPanel: React.FC<Props> = ({ comparison, loading }) => {
  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px 20px', marginBottom: '20px' }}>
        <Cpu size={32} style={{ color: 'var(--accent-cyan)', animation: 'spin 1s linear infinite' }} />
        <p style={{ marginTop: '12px', color: 'var(--text-secondary)', fontWeight: '600' }}>
          Formulating Mixed-Integer Constraints & Executing Google OR-Tools CP-SAT Solver...
        </p>
      </div>
    );
  }

  if (!comparison) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '30px', marginBottom: '20px' }}>
        <p style={{ color: 'var(--text-muted)' }}>Click "Run Solver (Live CP-SAT)" to execute optimization on the active snapshot.</p>
      </div>
    );
  }

  const { baseline_a2, joint_p3, weighted_lateness_reduction_pct, downstream_lateness_savings_minutes, freight_cost_delta } = comparison;
  const isAct2Rollable = comparison.scenario_id.includes('ROLLABLE');

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '16px', marginBottom: '20px' }}>
      {/* Metric Highlight Summary Card */}
      <div
        className="card"
        style={{
          gridColumn: '1 / -1',
          background: 'linear-gradient(135deg, #131d2e 0%, #17243a 100%)',
          borderColor: '#293d5c',
          boxShadow: '0 6px 18px rgba(0, 0, 0, 0.4)'
        }}
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span className="badge badge-optimal">LIVE CP-SAT SOLVER EXECUTION</span>
              <span className="badge badge-blue">Snapshot v{comparison.snapshot_version}</span>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                OR-Tools Runtime: <strong>{joint_p3.solve_time_ms.toFixed(1)} ms</strong>
              </span>
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: '800', marginTop: '6px', color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
              {joint_p3.approval_status === 'STALE_SNAPSHOT' ? (
                <span style={{ color: 'var(--accent-rose)' }}>⚠️ Snapshot Invalidated by External Inventory Race</span>
              ) : (
                <span>Joint Sourcing & Shop Schedule Optimization (P3 vs Fixed-Source A2)</span>
              )}
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px', maxWidth: '850px' }}>
              {comparison.summary_verdict}
            </p>
          </div>

          <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
            {/* KPI 1: Lateness Reduction */}
            <div style={{ background: 'rgba(6, 182, 212, 0.1)', border: '1px solid rgba(6, 182, 212, 0.35)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center', minWidth: '130px' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-cyan)', fontWeight: '700', textTransform: 'uppercase' }}>
                Lateness Reduction
              </div>
              <div style={{ fontSize: '24px', fontWeight: '900', color: 'var(--accent-cyan)' }}>
                {weighted_lateness_reduction_pct.toFixed(1)}%
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                {baseline_a2.weighted_lateness_ticks} ➔ {joint_p3.weighted_lateness_ticks} weighted ticks
              </div>
            </div>

            {/* KPI 2: Downstream Delay Saved */}
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.35)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center', minWidth: '130px' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-emerald)', fontWeight: '700', textTransform: 'uppercase' }}>
                Fleet Delay Saved
              </div>
              <div style={{ fontSize: '24px', fontWeight: '900', color: 'var(--accent-emerald)' }}>
                {downstream_lateness_savings_minutes} min
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                RO-1051: {baseline_a2.ro1051_finish_clock} ➔ {joint_p3.ro1051_finish_clock}
              </div>
            </div>

            {/* KPI 3: Freight Surcharge Delta */}
            <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.35)', padding: '10px 16px', borderRadius: '8px', textAlign: 'center', minWidth: '130px' }}>
              <div style={{ fontSize: '11px', color: 'var(--accent-amber)', fontWeight: '700', textTransform: 'uppercase' }}>
                Freight Delta
              </div>
              <div style={{ fontSize: '24px', fontWeight: '900', color: freight_cost_delta > 0 ? 'var(--accent-amber)' : 'var(--accent-emerald)' }}>
                {freight_cost_delta > 0 ? `+$${freight_cost_delta.toFixed(0)}` : `$${freight_cost_delta.toFixed(0)}`}
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                ${baseline_a2.parts_freight_cost} ➔ ${joint_p3.parts_freight_cost}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* A2 Baseline Card */}
      <div className="card" style={{ borderLeft: '4px solid #64748b' }}>
        <div className="card-title">
          <span>Baseline A2: Fixed-Source Sequential</span>
          <span className="badge" style={{ background: '#334155', color: '#cbd5e1' }}>Sequential (Greedy S2)</span>
        </div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
          Study-defined sequential baseline: parts clerk greedily orders lowest-cost part (S2: $18) first, without downstream hoist visibility.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Part Source Chosen</span>
            <span style={{ fontWeight: '700', color: 'var(--text-primary)' }}>
              {baseline_a2.selected_source_name} (${baseline_a2.parts_freight_cost}.00)
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Bay B4 Released</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-amber)' }}>{baseline_a2.b4_release_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Finish (Promise: 12:30)</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-rose)' }}>{baseline_a2.ro1051_finish_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Downstream Lateness</span>
            <span style={{ fontWeight: '700', color: 'var(--accent-rose)' }}>
              +{baseline_a2.ro1051_lateness_ticks * 5} min ({baseline_a2.ro1051_lateness_ticks} ticks)
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Total Weighted Lateness (Z₁)</span>
            <span style={{ fontWeight: '800', color: 'var(--accent-rose)' }}>
              {baseline_a2.weighted_lateness_ticks} weighted ticks
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Vehicle Movement</span>
            <span className="badge" style={{ background: '#1e293b', color: '#94a3b8' }}>{baseline_a2.selected_movement}</span>
          </div>
        </div>

        {/* A2 Verification Certificate Badge */}
        {baseline_a2.verification_result && (
          <div
            style={{
              marginTop: '12px',
              background:
                baseline_a2.verification_result.verification_status === 'VERIFIED'
                  ? 'rgba(16, 185, 129, 0.08)'
                  : baseline_a2.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                  ? 'rgba(245, 158, 11, 0.08)'
                  : 'rgba(239, 68, 68, 0.08)',
              border: `1px solid ${
                baseline_a2.verification_result.verification_status === 'VERIFIED'
                  ? 'rgba(16, 185, 129, 0.35)'
                  : baseline_a2.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                  ? 'rgba(245, 158, 11, 0.35)'
                  : 'rgba(239, 68, 68, 0.35)'
              }`,
              borderRadius: '6px',
              padding: '8px 12px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: '10px', fontWeight: '800', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
                Independent Verifier
              </div>
              <span
                className="badge"
                style={{
                  background:
                    baseline_a2.verification_result.verification_status === 'VERIFIED'
                      ? 'var(--badge-optimal)'
                      : 'rgba(239, 68, 68, 0.2)',
                  color:
                    baseline_a2.verification_result.verification_status === 'VERIFIED'
                      ? 'var(--badge-optimal-text)'
                      : 'var(--accent-rose)',
                  fontSize: '9px',
                  fontWeight: '800'
                }}
              >
                {baseline_a2.verification_result.verification_status}
              </span>
            </div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'monospace' }}>
              Cert: {baseline_a2.verification_result.certificate_id}
            </div>
          </div>
        )}
      </div>

      {/* P3 Joint Optimization Card */}
      <div className="card" style={{ borderColor: 'var(--accent-cyan)', borderLeft: '4px solid var(--accent-cyan)' }}>
        <div className="card-title">
          <span style={{ color: 'var(--accent-cyan)' }}>StallBreaker P3: Joint Optimization</span>
          <span className="badge badge-optimal">RECOMMENDED PROPOSAL</span>
        </div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
          Joint sourcing & dispatch optimization: models shop bay occupancy, parts arrival milestones, and downstream customer commitments simultaneously.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Part Source Chosen</span>
            <span style={{ fontWeight: '800', color: 'var(--accent-cyan)' }}>
              {joint_p3.selected_source_name} (${joint_p3.parts_freight_cost}.00)
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Bay B4 Released</span>
            <span style={{ fontWeight: '800', color: 'var(--accent-emerald)' }}>{joint_p3.b4_release_clock}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1051 Finish (Promise: 12:30)</span>
            <span style={{ fontWeight: '800', color: joint_p3.ro1051_lateness_ticks === 0 ? 'var(--accent-emerald)' : 'var(--accent-cyan)' }}>
              {joint_p3.ro1051_finish_clock} {joint_p3.ro1051_lateness_ticks === 0 ? '(ON TIME)' : `(+${joint_p3.ro1051_lateness_ticks * 5}m)`}
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>RO-1042 Finish (Promise: 13:30)</span>
            <span style={{ fontWeight: '800', color: joint_p3.ro1042_lateness_ticks === 0 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
              {joint_p3.ro1042_finish_clock} {joint_p3.ro1042_lateness_ticks === 0 ? '(ON TIME)' : `(+${joint_p3.ro1042_lateness_ticks * 5}m)`}
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Total Weighted Lateness (Z₁)</span>
            <span style={{ fontWeight: '900', color: 'var(--accent-emerald)' }}>
              {joint_p3.weighted_lateness_ticks} weighted ticks
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-muted)' }}>Vehicle Movement</span>
            <span className="badge badge-purple">{joint_p3.selected_movement}</span>
          </div>
        </div>

        {/* Feasibility Reasons / Justification */}
        <div style={{ marginTop: '14px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '6px', padding: '10px 14px' }}>
          <div style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '6px' }}>
            Solver Justification & Feasibility Bounds:
          </div>
          <ul style={{ paddingLeft: '16px', fontSize: '12px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '3px' }}>
            {joint_p3.feasibility_explanations.map((exp, i) => (
              <li key={i}>{exp}</li>
            ))}
          </ul>
        </div>

        {/* Verification Certificate */}
        {joint_p3.verification_result && (
          <div
            style={{
              marginTop: '12px',
              background:
                joint_p3.verification_result.verification_status === 'VERIFIED'
                  ? 'rgba(16, 185, 129, 0.08)'
                  : joint_p3.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                  ? 'rgba(245, 158, 11, 0.08)'
                  : 'rgba(239, 68, 68, 0.08)',
              border: `1px solid ${
                joint_p3.verification_result.verification_status === 'VERIFIED'
                  ? 'rgba(16, 185, 129, 0.35)'
                  : joint_p3.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                  ? 'rgba(245, 158, 11, 0.35)'
                  : 'rgba(239, 68, 68, 0.35)'
              }`,
              borderRadius: '6px',
              padding: '10px 14px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <div style={{ fontSize: '11px', fontWeight: '800', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
                Independent Verifier (Commit-Time Revalidation)
              </div>
              <span
                className="badge"
                style={{
                  background:
                    joint_p3.verification_result.verification_status === 'VERIFIED'
                      ? 'var(--badge-optimal)'
                      : joint_p3.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                      ? 'rgba(245, 158, 11, 0.2)'
                      : 'rgba(239, 68, 68, 0.2)',
                  color:
                    joint_p3.verification_result.verification_status === 'VERIFIED'
                      ? 'var(--badge-optimal-text)'
                      : joint_p3.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                      ? 'var(--accent-amber)'
                      : 'var(--accent-rose)',
                  fontSize: '10px',
                  fontWeight: '800'
                }}
              >
                {joint_p3.verification_result.verification_status}
              </span>
            </div>

            <div style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '3px' }}>
              <div>
                <strong style={{ color: 'var(--text-secondary)' }}>Cert ID:</strong>{' '}
                <span style={{ fontFamily: 'monospace', color: 'var(--accent-cyan)' }}>
                  {joint_p3.verification_result.certificate_id}
                </span>
              </div>
              <div>
                <strong style={{ color: 'var(--text-secondary)' }}>Decision-Payload Integrity Digest:</strong>{' '}
                <span style={{ fontFamily: 'monospace', color: 'var(--text-muted)' }}>
                  {joint_p3.verification_result.proposal_digest?.slice(0, 16)}... (SHA-256)
                </span>
              </div>
              <div>
                <strong style={{ color: 'var(--text-secondary)' }}>Verified Invariants:</strong>{' '}
                <span style={{ color: 'var(--accent-emerald)', fontWeight: '600' }}>
                  {joint_p3.verification_result.checked_invariants?.length || 0} passed
                </span>
                <ul style={{ paddingLeft: '16px', marginTop: '2px', marginBottom: '2px', fontSize: '10px', color: 'var(--text-secondary)' }}>
                  {joint_p3.verification_result.checked_invariants?.map((inv, i) => (
                    <li key={i}>✓ {inv}</li>
                  ))}
                </ul>
              </div>
              {joint_p3.verification_result.skipped_checks && joint_p3.verification_result.skipped_checks.length > 0 && (
                <div style={{ marginTop: '2px' }}>
                  <strong style={{ color: 'var(--text-muted)' }}>Skipped / Unconstrained Checks:</strong>
                  <ul style={{ paddingLeft: '16px', marginTop: '2px', marginBottom: '2px', fontSize: '10px', color: '#64748b' }}>
                    {joint_p3.verification_result.skipped_checks.map((chk, i) => (
                      <li key={i}>— {chk}</li>
                    ))}
                  </ul>
                </div>
              )}
              {joint_p3.verification_result.violations?.length > 0 && (
                <div style={{ marginTop: '4px', color: 'var(--accent-rose)' }}>
                  <strong>
                    {joint_p3.verification_result.verification_status === 'INSUFFICIENT_EVIDENCE'
                      ? `Missing Evidence / Gaps (${joint_p3.verification_result.violations.length}):`
                      : `Violations (${joint_p3.verification_result.violations.length}):`}
                  </strong>
                  <ul style={{ paddingLeft: '16px', marginTop: '2px' }}>
                    {joint_p3.verification_result.violations.map((v, i) => (
                      <li key={i}>
                        [{v.violation_code}] {v.description}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div style={{ fontSize: '10px', color: '#64748b', marginTop: '2px', fontStyle: 'italic' }}>
                Prototype integrity notice: SHA-256 decision digest validates payload consistency in-memory. Production deployment requires isolated certificate storage, cryptographic signing (HMAC/Ed25519), and transactional state.
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Policy Scope & Comparison Disclaimer */}
      <div
        style={{
          gridColumn: '1 / -1',
          padding: '12px 16px',
          background: 'rgba(15, 23, 42, 0.7)',
          border: '1px solid var(--border-color)',
          borderRadius: '8px',
          fontSize: '11px',
          color: 'var(--text-muted)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '8px'
        }}
      >
        <div>
          <strong style={{ color: 'var(--text-secondary)' }}>Methodology Standard:</strong>{' '}
          {isAct2Rollable
            ? 'Act 2 (S-MATH-01-ROLLABLE): Demonstrates physical relocation where wheels are mounted and H2 capacity is available. 99.0% lateness reduction achieved by freeing the hoist immediately.'
            : 'Act 1 (S-MATH-01): 66.7% weighted lateness reduction evaluated on the canonical synthetic disruption fixture against the study-defined fixed-source sequential baseline A2.'}
        </div>
        <div style={{ color: 'var(--accent-cyan)', fontWeight: '600' }}>
          Deterministic CP-SAT • Lexicographic Dual-Pass (Z₁: Lateness, Z₂: Freight)
        </div>
      </div>
    </div>
  );
};
