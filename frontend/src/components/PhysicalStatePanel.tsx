import React from 'react';
import { ScenarioSnapshot, VehicleState, BayState } from '../types';
import { ShieldCheck, AlertCircle, ArrowRight, CheckCircle2, XCircle } from './Icons';

interface Props {
  scenario: ScenarioSnapshot | null;
}

export const PhysicalStatePanel: React.FC<Props> = ({ scenario }) => {
  if (!scenario) return null;

  const currentVehicleState: VehicleState = scenario.ro1042.current_vehicle_state;
  const currentBayState: BayState = scenario.bay_b4_state;
  const isImmobilized = currentVehicleState === 'PARTIALLY_DISMANTLED';
  const hasSignoff = scenario.ro1042.technician_signoff_recorded;
  const hasH2Capacity = scenario.h2_available_stalls > 0;
  const isRelocationEligible = !isImmobilized && hasSignoff && hasH2Capacity;

  const vehicleStates: { id: VehicleState; label: string }[] = [
    { id: 'PARTIALLY_DISMANTLED', label: 'Partially Dismantled' },
    { id: 'SAFE_TO_RELOCATE', label: 'Safe To Relocate' },
    { id: 'IN_HOLDING', label: 'In Holding (H2)' },
    { id: 'REPAIR_MECHANICALLY_COMPLETE', label: 'Repair Complete' },
    { id: 'IN_CLEARANCE_TRANSIT', label: 'Clearance Transit' },
    { id: 'IN_CUSTOMER_PICKUP_STAGING', label: 'Customer Staging' },
  ];

  const bayStates: { id: BayState; label: string }[] = [
    { id: 'OCCUPIED', label: 'Bay Occupied' },
    { id: 'CLEARANCE_PENDING', label: 'Clearance Pending' },
    { id: 'AVAILABLE_FOR_ALLOCATION', label: 'Available' },
  ];

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldCheck size={18} style={{ color: 'var(--accent-emerald)' }} />
          <span>Physical State Machine & Pre-Solver Feasibility Gates</span>
        </div>
        <span className="badge badge-optimal">Safety Invariants Enforced</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
        {/* Vehicle Physical State Progression */}
        <div style={{ background: '#0e1626', padding: '14px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--accent-cyan)', marginBottom: '8px' }}>
            RO-1042 Physical Vehicle State (Ford Explorer)
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
            {vehicleStates.map((st, i) => {
              const isActive = currentVehicleState === st.id;
              return (
                <React.Fragment key={st.id}>
                  <div
                    style={{
                      padding: '5px 9px',
                      borderRadius: '4px',
                      fontSize: '11px',
                      fontWeight: isActive ? '800' : '500',
                      background: isActive ? 'var(--accent-cyan)' : '#1e293b',
                      color: isActive ? '#000' : 'var(--text-muted)',
                      border: isActive ? '1px solid #ffffff' : '1px solid transparent',
                      boxShadow: isActive ? '0 0 10px rgba(6, 182, 212, 0.5)' : 'none',
                    }}
                  >
                    {st.label}
                  </div>
                  {i < vehicleStates.length - 1 && (
                    <ArrowRight size={12} style={{ color: 'var(--text-muted)' }} />
                  )}
                </React.Fragment>
              );
            })}
          </div>
          <div style={{ marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>
            Physical Condition:{' '}
            {isImmobilized ? (
              <span style={{ color: 'var(--accent-amber)', fontWeight: '700' }}>
                IMMOBILIZED (Wheels/Hub detached; vehicle cannot roll; locks hoist)
              </span>
            ) : (
              <span style={{ color: 'var(--accent-emerald)', fontWeight: '700' }}>
                ROLLABLE (Wheels remounted; certified safe to relocate to H2)
              </span>
            )}
          </div>
        </div>

        {/* Bay Physical Resource State Progression */}
        <div style={{ background: '#0e1626', padding: '14px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--accent-amber)', marginBottom: '8px' }}>
            Bay B4 Resource State (Heavy-Duty Alignment Hoist)
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
            {bayStates.map((st, i) => {
              const isActive = currentBayState === st.id;
              return (
                <React.Fragment key={st.id}>
                  <div
                    style={{
                      padding: '5px 12px',
                      borderRadius: '4px',
                      fontSize: '11px',
                      fontWeight: isActive ? '800' : '500',
                      background: isActive ? 'var(--accent-amber)' : '#1e293b',
                      color: isActive ? '#000' : 'var(--text-muted)',
                      border: isActive ? '1px solid #ffffff' : '1px solid transparent',
                      boxShadow: isActive ? '0 0 10px rgba(245, 158, 11, 0.5)' : 'none',
                    }}
                  >
                    {st.label}
                  </div>
                  {i < bayStates.length - 1 && (
                    <ArrowRight size={12} style={{ color: 'var(--text-muted)' }} />
                  )}
                </React.Fragment>
              );
            })}
          </div>
          <div style={{ marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>
            Holding Area H2 Buffer:{' '}
            <strong style={{ color: hasH2Capacity ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
              {scenario.h2_available_stalls} of {scenario.h2_capacity} stalls available
            </strong>
          </div>
        </div>
      </div>

      {/* Pre-Solver Feasibility Checklist */}
      <div
        style={{
          marginTop: '16px',
          background: 'rgba(15, 23, 42, 0.5)',
          border: '1px solid var(--border-color)',
          borderRadius: '8px',
          padding: '12px 16px'
        }}
      >
        <div style={{ fontSize: '12px', fontWeight: '800', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '8px' }}>
          Pre-Solver Feasibility Filter (Prunes Search Space Before Optimization):
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '10px', fontSize: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {!isImmobilized ? (
              <CheckCircle2 size={16} style={{ color: 'var(--accent-emerald)', flexShrink: 0 }} />
            ) : (
              <XCircle size={16} style={{ color: 'var(--accent-rose)', flexShrink: 0 }} />
            )}
            <span>
              <strong>Wheel Assembly:</strong> {!isImmobilized ? 'Mounted (Rollable)' : 'Detached (Cannot Roll)'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {hasSignoff ? (
              <CheckCircle2 size={16} style={{ color: 'var(--accent-emerald)', flexShrink: 0 }} />
            ) : (
              <XCircle size={16} style={{ color: 'var(--accent-rose)', flexShrink: 0 }} />
            )}
            <span>
              <strong>Technician Signoff:</strong> {hasSignoff ? 'Tech K1 Certified' : 'Not Recorded'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {hasH2Capacity ? (
              <CheckCircle2 size={16} style={{ color: 'var(--accent-emerald)', flexShrink: 0 }} />
            ) : (
              <XCircle size={16} style={{ color: 'var(--accent-rose)', flexShrink: 0 }} />
            )}
            <span>
              <strong>H2 Holding Capacity:</strong> {hasH2Capacity ? 'Stall Available' : 'No Free Stalls'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span
              className="badge"
              style={{
                background: isRelocationEligible ? 'var(--badge-optimal)' : '#881337',
                color: isRelocationEligible ? 'var(--badge-optimal-text)' : '#fda4af'
              }}
            >
              {isRelocationEligible ? 'RELOCATION ELIGIBLE' : 'RELOCATION PRUNED (HOLD ONLY)'}
            </span>
          </div>
        </div>
      </div>

      {/* Safety Invariants strip */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px', marginTop: '14px' }}>
        <div style={{ borderLeft: '3px solid var(--accent-cyan)', paddingLeft: '10px', fontSize: '11px', color: 'var(--text-secondary)' }}>
          <strong style={{ color: 'var(--text-primary)' }}>Invariant CE-1 (Hoist Lock):</strong> Bay B4 is strictly single-capacity. No subsequent vehicle can enter the hoist while an immobilized vehicle occupies it.
        </div>
        <div style={{ borderLeft: '3px solid var(--accent-emerald)', paddingLeft: '10px', fontSize: '11px', color: 'var(--text-secondary)' }}>
          <strong style={{ color: 'var(--text-primary)' }}>Invariant CE-3 (Non-Instant Clearance):</strong> 10-min clearance transit ($k=2$) required before Bay B4 transitions from <code>CLEARANCE_PENDING</code> to <code>AVAILABLE</code>.
        </div>
        <div style={{ borderLeft: '3px solid var(--accent-rose)', paddingLeft: '10px', fontSize: '11px', color: 'var(--text-secondary)' }}>
          <strong style={{ color: 'var(--text-primary)' }}>Invariant CE-7 (Promise Integrity):</strong> Customer promise times are immutable contractual commitments; lateness penalty cannot be masked by postponing promises.
        </div>
      </div>
    </div>
  );
};
