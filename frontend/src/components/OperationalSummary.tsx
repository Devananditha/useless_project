import React from 'react';
import { ScenarioSnapshot, Proposal } from '../types';
import { tickToClock } from '../utils';
import { Activity, Clock, ShieldCheck, Wrench, Layers } from './Icons';

interface Props {
  scenario: ScenarioSnapshot | null;
  proposal: Proposal | null;
  loading: boolean;
}

export const OperationalSummary: React.FC<Props> = ({ scenario, proposal, loading }) => {
  if (!scenario) return null;

  const isRelocated = proposal?.selected_movement === 'RELOCATE_TO_H2';
  const ro1042PromiseClock = tickToClock(scenario.ro1042.promise_ticks);
  const ro1051PromiseClock = tickToClock(scenario.ro1051.promise_ticks);

  return (
    <div
      style={{
        background: 'linear-gradient(180deg, #131c2d 0%, #0e1625 100%)',
        border: '1px solid #23344d',
        borderRadius: '10px',
        padding: '14px 18px',
        marginBottom: '20px',
        boxShadow: '0 4px 14px rgba(0, 0, 0, 0.35)'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', flexWrap: 'wrap', gap: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={16} style={{ color: 'var(--accent-cyan)' }} />
          <span style={{ fontSize: '12px', fontWeight: '800', letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
            Shop Floor Operational Cockpit & Real-Time Solver Telemetry
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-blue">
            Snapshot Version: v{scenario.snapshot_version}
          </span>
          <span
            className="badge"
            style={{
              background: proposal?.solver_status === 'OPTIMAL' ? 'var(--badge-optimal)' : '#334155',
              color: proposal?.solver_status === 'OPTIMAL' ? 'var(--badge-optimal-text)' : '#94a3b8'
            }}
          >
            {proposal ? `CP-SAT: ${proposal.solver_status}` : 'Awaiting Solver'}
          </span>
          {proposal?.verification_result && (
            <span
              className="badge"
              style={{
                background:
                  proposal.verification_result.verification_status === 'VERIFIED'
                    ? 'rgba(16, 185, 129, 0.2)'
                    : 'rgba(239, 68, 68, 0.2)',
                color:
                  proposal.verification_result.verification_status === 'VERIFIED'
                    ? 'var(--accent-emerald)'
                    : 'var(--accent-rose)',
                border: `1px solid ${
                  proposal.verification_result.verification_status === 'VERIFIED'
                    ? 'rgba(16, 185, 129, 0.4)'
                    : 'rgba(239, 68, 68, 0.4)'
                }`,
                fontSize: '11px',
                fontWeight: '700'
              }}
            >
              Cert: {proposal.verification_result.verification_status}
            </span>
          )}
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '10px'
        }}
      >
        {/* Metric 1: Scenario Identity */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Active Scenario
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--text-primary)', marginTop: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {scenario.scenario_id}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            {scenario.ro1042.current_vehicle_state === 'PARTIALLY_DISMANTLED' ? 'Immobilized on Hoist' : 'Safe to Relocate'}
          </div>
        </div>

        {/* Metric 2: Selected Parts Source */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Selected Source
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--accent-cyan)', marginTop: '2px' }}>
            {proposal?.selected_source_id ? `${proposal.selected_source_id} ($${proposal.parts_freight_cost})` : '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            {proposal?.selected_source_id === 'S1' ? 'Local Dealer (10:15)' : proposal?.selected_source_id === 'S2' ? 'Regional PDC (12:05)' : 'Unassigned'}
          </div>
        </div>

        {/* Metric 3: Movement Option */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Movement Option
          </div>
          <div style={{ fontSize: '12px', fontWeight: '800', color: isRelocated ? 'var(--accent-purple)' : 'var(--accent-amber)', marginTop: '2px' }}>
            {proposal ? proposal.selected_movement : '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            {isRelocated ? 'Relocated to Holding H2' : 'Locks Bay B4 Hoist'}
          </div>
        </div>

        {/* Metric 4: Bay B4 Release */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Bay B4 Release
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--accent-emerald)', marginTop: '2px' }}>
            {proposal?.b4_release_clock || '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            {isRelocated ? 'Released at t=24 (10:00)' : `Released at t=${proposal?.b4_release_tick}`}
          </div>
        </div>

        {/* Metric 5: RO-1042 Completion */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            RO-1042 Finish
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--text-primary)', marginTop: '2px' }}>
            {proposal?.ro1042_finish_clock || '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Promise: {ro1042PromiseClock}
          </div>
        </div>

        {/* Metric 6: RO-1051 Completion */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            RO-1051 Finish
          </div>
          <div
            style={{
              fontSize: '13px',
              fontWeight: '800',
              color: proposal && proposal.ro1051_finish_tick <= scenario.ro1051.promise_ticks ? 'var(--accent-emerald)' : 'var(--accent-rose)',
              marginTop: '2px'
            }}
          >
            {proposal?.ro1051_finish_clock || '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Promise: {ro1051PromiseClock} (Fleet)
          </div>
        </div>

        {/* Metric 7: Weighted Lateness Z1 */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Weighted Lateness (Z₁)
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--accent-cyan)', marginTop: '2px' }}>
            {proposal ? `${proposal.weighted_lateness_ticks} ticks` : '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            {proposal ? `${proposal.weighted_lateness_ticks * 5} penalty min` : '--'}
          </div>
        </div>

        {/* Metric 8: Optimization Latency */}
        <div style={{ background: 'rgba(15, 23, 42, 0.65)', border: '1px solid #1e293b', borderRadius: '6px', padding: '8px 12px' }}>
          <div style={{ fontSize: '10px', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Solver Runtime
          </div>
          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--accent-emerald)', marginTop: '2px' }}>
            {proposal ? `${proposal.solve_time_ms.toFixed(1)} ms` : '--'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>
            Dual-Pass CP-SAT
          </div>
        </div>
      </div>
    </div>
  );
};
