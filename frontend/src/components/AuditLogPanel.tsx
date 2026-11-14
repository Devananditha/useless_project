import React, { useState } from 'react';
import { AuditEvent } from '../types';
import { History, FileText, ChevronDown, ChevronRight } from './Icons';

interface Props {
  events: AuditEvent[];
}

export const AuditLogPanel: React.FC<Props> = ({ events }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getEventBadgeClass = (eventType: string) => {
    if (eventType.includes('STALE') || eventType.includes('REJECTED') || eventType.includes('COMPETING')) {
      return 'badge-stale';
    }
    if (eventType.includes('APPROVED')) {
      return 'badge-optimal';
    }
    return 'badge-blue';
  };

  return (
    <div className="card">
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={18} style={{ color: 'var(--accent-purple)' }} />
          <span>Immutable Audit Event Stream & Optimistic Concurrency Trail</span>
        </div>
        <span className="badge badge-purple">{events.length} Events Logged</span>
      </div>

      <div style={{ maxHeight: '280px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {events.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>No audit events recorded yet.</p>
        ) : (
          events.map((evt) => {
            const isExpanded = expandedId === evt.event_id;
            return (
              <div
                key={evt.event_id}
                style={{
                  background: '#0d1626',
                  borderRadius: '6px',
                  border: '1px solid var(--border-color)',
                  padding: '8px 12px',
                  fontSize: '12px'
                }}
              >
                <div
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
                  onClick={() => setExpandedId(isExpanded ? null : evt.event_id)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    <span className={`badge ${getEventBadgeClass(evt.event_type)}`}>
                      {evt.event_type}
                    </span>
                    <span style={{ color: 'var(--text-primary)', fontWeight: '500' }}>
                      {evt.description}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>
                      v{evt.version_before} ➔ v{evt.version_after}
                    </span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>
                      {new Date(evt.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>

                {isExpanded && (
                  <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #1e293b' }}>
                    <pre
                      style={{
                        background: '#070b13',
                        padding: '8px',
                        borderRadius: '4px',
                        color: 'var(--accent-cyan)',
                        fontSize: '11px',
                        overflowX: 'auto'
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
