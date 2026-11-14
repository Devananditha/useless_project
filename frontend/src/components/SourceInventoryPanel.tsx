import React from 'react';
import { PartSource, ScenarioSnapshot } from '../types';
import { Package, Truck, Zap, AlertTriangle, CheckCircle2, XCircle } from './Icons';

interface Props {
  scenario: ScenarioSnapshot | null;
  onSimulateStockRace: () => void;
  loading: boolean;
}

export const SourceInventoryPanel: React.FC<Props> = ({ scenario, onSimulateStockRace, loading }) => {
  if (!scenario) return null;

  const isAct1 = scenario.scenario_id === 'S-MATH-01';
  const s1Source = scenario.sources.find((s) => s.source_id === 'S1');
  const isS1Available = (s1Source?.atp ?? 0) > 0;

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Package size={18} style={{ color: 'var(--accent-cyan)' }} />
          <span>Real-Time Parts Inventory & Vendor Sourcing Snapshot</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span className="badge badge-blue">Snapshot Version: v{scenario.snapshot_version}</span>
          <button
            onClick={onSimulateStockRace}
            disabled={loading || !isAct1 || !isS1Available}
            style={{
              padding: '6px 14px',
              fontSize: '11px',
              fontWeight: '800',
              background: !isAct1 ? '#334155' : isS1Available ? '#e11d48' : '#475569',
              color: '#ffffff',
              borderRadius: '6px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              border: isS1Available && isAct1 ? '1px solid #fda4af' : '1px solid var(--border-color)',
              boxShadow: isS1Available && isAct1 ? '0 0 12px rgba(225, 29, 72, 0.5)' : 'none',
              cursor: loading || !isAct1 || !isS1Available ? 'not-allowed' : 'pointer'
            }}
          >
            <Zap size={14} />
            {!isAct1
              ? 'Switch to Act 1 for Stock Race'
              : isS1Available
              ? 'Simulate S1 Stock Race (Act 3)'
              : 'S1 Depleted (Act 3 Simulated)'}
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
        {scenario.sources.map((src) => {
          const isAtpAvailable = src.atp > 0;
          const isEligible = isAtpAvailable && src.fitment_verified && src.quote_valid;
          const arrivalClock = src.source_id === 'S1' ? '10:00 (Usable: 10:15 AM)' : '11:50 (Usable: 12:05 PM)';

          return (
            <div
              key={src.source_id}
              style={{
                background: isAtpAvailable ? '#0e172a' : '#23121b',
                border: isAtpAvailable ? '1px solid var(--border-color)' : '2px solid #e11d48',
                borderRadius: '8px',
                padding: '16px',
                position: 'relative',
                boxShadow: isAtpAvailable ? 'none' : '0 0 16px rgba(225, 29, 72, 0.3)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                <div>
                  <div style={{ fontSize: '16px', fontWeight: '800', color: isAtpAvailable ? 'var(--text-primary)' : '#fda4af' }}>
                    {src.source_id}: {src.name}
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                    Supplier Catalog v{src.source_version} • {src.source_id === 'S1' ? 'Expedited Courier' : 'Regional Freight'}
                  </div>
                </div>
                <span
                  className="badge"
                  style={{
                    background: isAtpAvailable ? 'var(--badge-optimal)' : '#881337',
                    color: isAtpAvailable ? 'var(--badge-optimal-text)' : '#fda4af',
                    fontWeight: '800'
                  }}
                >
                  {isAtpAvailable ? `ATP = ${src.atp} UNIT` : 'ATP = 0 (DEPLETED)'}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '12px', marginTop: '12px' }}>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Freight Surcharge:</span>
                  <div style={{ fontWeight: '800', color: 'var(--text-primary)', fontSize: '15px' }}>
                    ${src.cost}.00
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Bay Delivery & Usable:</span>
                  <div style={{ fontWeight: '700', color: 'var(--accent-cyan)' }}>
                    {arrivalClock}
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Fitment Compatibility:</span>
                  <div style={{ color: src.fitment_verified ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: '700' }}>
                    {src.fitment_verified ? '✓ OEM Matched (VIN Checked)' : '✗ Fitment Mismatch'}
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Price Quote Lock:</span>
                  <div style={{ color: src.quote_valid ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: '700' }}>
                    {src.quote_valid ? '✓ Locked & Valid' : '✗ Expired'}
                  </div>
                </div>
              </div>

              {/* Eligibility Status Tag */}
              <div style={{ marginTop: '12px', paddingTop: '10px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>CP-SAT Candidate:</span>
                <span
                  className="badge"
                  style={{
                    background: isEligible ? 'rgba(6, 182, 212, 0.15)' : 'rgba(239, 68, 68, 0.2)',
                    color: isEligible ? 'var(--accent-cyan)' : '#fca5a5',
                    border: isEligible ? '1px solid rgba(6, 182, 212, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)'
                  }}
                >
                  {isEligible ? 'ELIGIBLE FOR SOLVER SELECTION' : 'INELIGIBLE — PRUNED FROM SELECTION'}
                </span>
              </div>

              {!isAtpAvailable && (
                <div style={{ marginTop: '10px', padding: '8px 12px', background: 'rgba(225, 29, 72, 0.2)', borderRadius: '6px', fontSize: '11px', color: '#ffe4e6', display: 'flex', alignItems: 'center', gap: '8px', border: '1px solid rgba(225, 29, 72, 0.4)' }}>
                  <AlertTriangle size={16} style={{ color: '#fda4af', flexShrink: 0 }} />
                  <span>Act 3 Stock Race: Inventory allocated elsewhere by competing RO-1099. State drifted to v{scenario.snapshot_version}.</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
