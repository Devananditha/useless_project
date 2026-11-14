import React from 'react';
import { PartSource, ScenarioSnapshot } from '../types';
import { Package, Truck, Zap, AlertTriangle } from './Icons';

interface Props {
  scenario: ScenarioSnapshot | null;
  onSimulateStockRace: () => void;
  loading: boolean;
}

export const SourceInventoryPanel: React.FC<Props> = ({ scenario, onSimulateStockRace, loading }) => {
  if (!scenario) return null;

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Package size={18} style={{ color: 'var(--accent-cyan)' }} />
          <span>Real-Time Parts Inventory & Sourcing Snapshot</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span className="badge badge-blue">Snapshot Version: v{scenario.snapshot_version}</span>
          <button
            onClick={onSimulateStockRace}
            disabled={loading}
            style={{
              padding: '5px 12px',
              fontSize: '11px',
              fontWeight: '700',
              background: '#e11d48',
              color: '#ffffff',
              borderRadius: '5px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Zap size={13} />
            Simulate S1 Stock Race (Act 3)
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
        {scenario.sources.map((src) => {
          const isAtpAvailable = src.atp > 0;
          const arrivalClock = src.source_id === 'S1' ? '10:15 (Usable: 10:30)' : '11:45 (Usable: 12:00)';

          return (
            <div
              key={src.source_id}
              style={{
                background: isAtpAvailable ? '#0e172a' : '#23121b',
                border: isAtpAvailable ? '1px solid var(--border-color)' : '1px solid #e11d48',
                borderRadius: '8px',
                padding: '14px',
                position: 'relative'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                <div>
                  <div style={{ fontSize: '15px', fontWeight: '700', color: isAtpAvailable ? 'var(--text-primary)' : '#fda4af' }}>
                    {src.source_id}: {src.name}
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                    Supplier Version #{src.source_version}
                  </div>
                </div>
                <span
                  className="badge"
                  style={{
                    background: isAtpAvailable ? 'var(--badge-optimal)' : '#881337',
                    color: isAtpAvailable ? 'var(--badge-optimal-text)' : '#fda4af'
                  }}
                >
                  {isAtpAvailable ? `ATP = ${src.atp} Unit` : 'ATP = 0 (DEPLETED)'}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px', marginTop: '10px' }}>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Freight Surcharge:</span>
                  <div style={{ fontWeight: '700', color: 'var(--text-primary)', fontSize: '14px' }}>
                    ${src.cost}.00
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Bay Delivery & Usable:</span>
                  <div style={{ fontWeight: '600', color: 'var(--accent-cyan)' }}>
                    {arrivalClock}
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Fitment Check:</span>
                  <div style={{ color: src.fitment_verified ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: '600' }}>
                    {src.fitment_verified ? '✓ Verified (OEM Match)' : '✗ Unverified'}
                  </div>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Price Quote:</span>
                  <div style={{ color: src.quote_valid ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: '600' }}>
                    {src.quote_valid ? '✓ Valid (Locked 60m)' : '✗ Expired'}
                  </div>
                </div>
              </div>

              {!isAtpAvailable && (
                <div style={{ marginTop: '10px', padding: '6px 10px', background: 'rgba(225, 29, 72, 0.2)', borderRadius: '4px', fontSize: '11px', color: '#fda4af', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <AlertTriangle size={14} />
                  <span>Inventory consumed by concurrent RO-1099. Not eligible for recovery.</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
