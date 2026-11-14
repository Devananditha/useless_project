import React, { useState } from 'react';
import { AuditEvent } from '../types';
import { History, ChevronDown, ChevronRight, FileText } from './Icons';

interface Props {
  events: AuditEvent[];
}

export const AuditLogPanel: React.FC<Props> = ({ events }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getEventBadgeStyle = (eventType: string) => {
    switch (eventType) {
      case 'PROPOSAL_GENERATED':
        return { bg: 'rgba(6, 182, 212, 0.15)', text: 'var(--accent-cyan)', border: 'rgba(6, 182, 212, 0.3)' };
      case 'SCENARIO_SELECTED':
        return { bg: 'rgba(59, 130, 246, 0.15)', text: '#93c5fd', border: 'rgba(59, 130, 246, 0.3)' };
      case 'STOCK_ALLOCATED_ELSEWHERE':
        return { bg: 'rgba(245, 158, 11, 0.2)', text: 'var(--accent-amber)', border: 'rgba(245, 158, 11, 0.4)' };
      case 'STALE_SNAPSHOT_ABORT':
        return { bg: 'rgba(244, 63, 94, 0.2)', text: '#fda4af', border: 'rgba(244, 63, 94, 0.4)' };
      case 'SCENARIO_MISMATCH_ABORT':
        return { bg: 'rgba(225, 29, 72, 0.25)', text: '#fca5a5', border: 'rgba(225, 29, 72, 0.5)' };
      case 'REPLACEMENT_PROPOSAL_GENERATED':
        return { bg: 'rgba(139, 92, 246, 0.2)', text: '#c4b5fd', border: 'rgba(139, 92, 246, 0.4)' };
      case 'PROPOSAL_APPROVED_LOCAL':
        return { bg: 'rgba(16, 185, 129, 0.2)', text: 'var(--badge-optimal-text)', border: 'rgba(16, 185, 129, 0.4)' };
      case 'SYSTEM_RESET':
        return { bg: 'rgba(100, 116, 139, 0.2)', text: '#cbd5e1', border: 'rgba(100, 116, 139, 0.3)' };
      default:
        return { bg: 'rgba(59, 130, 246, 0.15)', text: '#93c5fd', border: 'rgba(59, 130, 246, 0.3)' };
    }
  };

  return (
    <div className="card">
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={18} style={{ color: 'var(--accent-purple)' }} />
          <span>Immutable Audit Event Stream & Concurrency State Trail</span>
        </div>
        <span className="badge badge-purple">{events.length} Events Logged</span>
      </div>

      <div style={{ maxHeight: '300px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {events.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', padding: '12px' }}>
            No audit events recorded yet.
          </p>
        ) : (
          events.map((evt) => {
            const isExpanded = expandedId === evt.event_id;
            const badgeStyle = getEventBadgeStyle(evt.event_type);
            const formattedTime = new Date(evt.timestamp).toLocaleTimeString();

            return (
              <div
                key={evt.event_id}
                style={{
                  background: '#0c1524',
                  borderRadius: '6px',
                  border: '1px solid var(--border-color)',
                  padding: '9px 14px',
                  fontSize: '12px',
                  transition: 'background 0.15s ease'
                }}
              >
                <div
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer', gap: '10px' }}
                  onClick={() => setExpandedId(isExpanded ? null : evt.event_id)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, minWidth: 0 }}>
                    {isExpanded ? (
                      <ChevronDown size={14} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                    ) : (
                      <ChevronRight size={14} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                    )}
                    <span
                      style={{
                        padding: '2px 8px',
                        borderRadius: '4px',
                        fontSize: '10px',
                        fontWeight: '800',
                        letterSpacing: '0.04em',
                        background: badgeStyle.bg,
                        color: badgeStyle.text,
                        border: `1px solid ${badgeStyle.border}`,
                        whiteSpace: 'nowrap',
                        flexShrink: 0
                      }}
                    >
                      {evt.event_type}
                    </span>
                    <span
                      style={{
                        color: 'var(--text-primary)',
                        fontWeight: '500',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis'
                      }}
                    >
                      {evt.description}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexShrink: 0 }}>
                    <span style={{ color: 'var(--accent-cyan)', fontWeight: '600', fontSize: '11px' }}>
                      v{evt.version_before} ➔ v{evt.version_after}
                    </span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>
                      {formattedTime}
                    </span>
                  </div>
                </div>

                {isExpanded && (
                  <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #1a2638' }}>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                      Event Payload (Snapshot Transition Details):
                    </div>
                    <pre
                      style={{
                        background: '#070b13',
                        padding: '10px',
                        borderRadius: '4px',
                        color: 'var(--accent-cyan)',
                        fontSize: '11px',
                        overflowX: 'auto',
                        border: '1px solid #162234'
                      }}
                    >
                      {JSON.stringify(evt.details, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
