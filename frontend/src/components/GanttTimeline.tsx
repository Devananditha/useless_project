import React, { useState } from 'react';
import { Proposal, ScheduledInterval } from '../types';

interface Props {
  baselineProposal: Proposal | null;
  jointProposal: Proposal | null;
}

export const GanttTimeline: React.FC<Props> = ({ baselineProposal, jointProposal }) => {
  const [viewMode, setViewMode] = useState<'P3' | 'A2'>('P3');
  const [hoveredInterval, setHoveredInterval] = useState<ScheduledInterval | null>(null);

  const activeProposal = viewMode === 'A2' ? baselineProposal : jointProposal;

  // Timeline geometry
  // Canonical horizon: t=0 (08:00) to t=108 (17:00), 5 min per tick = 12 ticks/hr
  const totalTicks = 108;
  const svgWidth = 1050;
  const trackHeight = 44;
  const headerHeight = 40;
  const labelWidth = 160;
  const chartWidth = svgWidth - labelWidth - 20;

  const tickToX = (tick: number) => {
    return labelWidth + (Math.min(tick, totalTicks) / totalTicks) * chartWidth;
  };

  const hours = [
    { label: '08:00', tick: 0 },
    { label: '09:00', tick: 12 },
    { label: '10:00', tick: 24 },
    { label: '11:00', tick: 36 },
    { label: '12:00', tick: 48 },
    { label: '13:00', tick: 60 },
    { label: '14:00', tick: 72 },
    { label: '15:00', tick: 84 },
    { label: '16:00', tick: 96 },
    { label: '17:00', tick: 108 },
  ];

  const getColorForOperation = (op: string) => {
    if (op.includes('Stall') || op.includes('Immobilized') || op.includes('Staged in Holding')) return '#f59e0b'; // amber
    if (op.includes('Installation') || op.includes('Active')) return '#06b6d4'; // cyan
    if (op.includes('Clearance') || op.includes('Verification')) return '#10b981'; // emerald
    if (op.includes('Service') || op.includes('Calibration') || op.includes('ADAS')) return '#3b82f6'; // blue
    if (op.includes('Relocation') || op.includes('Transit') || op.includes('Return')) return '#8b5cf6'; // purple
    return '#64748b';
  };

  const tracks = [
    { id: 'BAY_B4', label: 'Bay B4 (Hoist)', y: headerHeight },
    { id: 'HOLDING_H2', label: 'Holding Area H2', y: headerHeight + trackHeight },
    { id: 'RO_1042', label: 'RO-1042 (Ford Explorer)', y: headerHeight + trackHeight * 2 },
    { id: 'RO_1051', label: 'RO-1051 (Fleet F-150)', y: headerHeight + trackHeight * 3 },
  ];

  const totalHeight = headerHeight + trackHeight * tracks.length + 20;

  // Map intervals to tracks
  const getTrackY = (interval: ScheduledInterval) => {
    if (interval.entity_id === 'B4' || interval.entity_type === 'BAY') return tracks[0].y;
    if (interval.entity_id === 'H2' || interval.entity_type === 'HOLDING') return tracks[1].y;
    if (interval.entity_id === 'RO-1042') return tracks[2].y;
    if (interval.entity_id === 'RO-1051') return tracks[3].y;
    return tracks[0].y;
  };

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span>Gantt Operational Timeline & Hoist Scheduling (Horizon: 08:00 – 17:00)</span>
          <span className="badge badge-optimal">5-min Ticks (H=108)</span>
        </div>
        <div style={{ display: 'flex', gap: '6px' }}>
          <button
            onClick={() => setViewMode('P3')}
            style={{
              padding: '4px 10px',
              fontSize: '12px',
              background: viewMode === 'P3' ? 'var(--accent-cyan)' : '#1e293b',
              color: viewMode === 'P3' ? '#000' : 'var(--text-secondary)',
              fontWeight: '600'
            }}
          >
            P3 Joint Schedule
          </button>
          <button
            onClick={() => setViewMode('A2')}
            style={{
              padding: '4px 10px',
              fontSize: '12px',
              background: viewMode === 'A2' ? 'var(--accent-amber)' : '#1e293b',
              color: viewMode === 'A2' ? '#000' : 'var(--text-secondary)',
              fontWeight: '600'
            }}
          >
            A2 Baseline Schedule
          </button>
        </div>
      </div>

      <div style={{ position: 'relative', overflowX: 'auto', background: '#0d1527', borderRadius: '8px', padding: '12px' }}>
        <svg
          viewBox={`0 0 ${svgWidth} ${totalHeight}`}
          className="timeline-svg"
          style={{ minWidth: '820px' }}
        >
          {/* Background grid */}
          {hours.map((h, i) => {
            const x = tickToX(h.tick);
            return (
              <g key={i}>
                <line
                  x1={x}
                  y1={headerHeight}
                  x2={x}
                  y2={totalHeight - 10}
                  stroke="#1e293b"
                  strokeWidth="1"
                  strokeDasharray={h.tick === 0 ? '' : '3 3'}
                />
                <text
                  x={x}
                  y={headerHeight - 12}
                  fill="#94a3b8"
                  fontSize="11"
                  fontWeight="600"
                  textAnchor="middle"
                >
                  {h.label}
                </text>
              </g>
            );
          })}

          {/* Track rows */}
          {tracks.map((track, i) => (
            <g key={i}>
              <rect
                x={0}
                y={track.y}
                width={svgWidth}
                height={trackHeight - 6}
                fill={i % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.04)'}
                rx="4"
              />
              <text
                x={10}
                y={track.y + trackHeight / 2 - 2}
                fill="#cbd5e1"
                fontSize="12"
                fontWeight="600"
              >
                {track.label}
              </text>
            </g>
          ))}

          {/* Canonical Promise Marker Lines */}
          {/* RO-1051 Promise: t=54 (12:30) */}
          <line
            x1={tickToX(54)}
            y1={headerHeight}
            x2={tickToX(54)}
            y2={totalHeight - 10}
            stroke="var(--accent-rose)"
            strokeWidth="2"
            strokeDasharray="4 2"
          />
          <text
            x={tickToX(54)}
            y={headerHeight - 22}
            fill="var(--accent-rose)"
            fontSize="10"
            fontWeight="700"
            textAnchor="middle"
          >
            RO-1051 Promise (t=54, 12:30)
          </text>

          {/* RO-1042 Promise: t=66 (13:30) */}
          <line
            x1={tickToX(66)}
            y1={headerHeight}
            x2={tickToX(66)}
            y2={totalHeight - 10}
            stroke="var(--accent-cyan)"
            strokeWidth="1.5"
            strokeDasharray="3 3"
          />
          <text
            x={tickToX(66)}
            y={headerHeight - 22}
            fill="var(--accent-cyan)"
            fontSize="10"
            fontWeight="700"
            textAnchor="middle"
          >
            RO-1042 Promise (t=66, 13:30)
          </text>

          {/* Active Schedule Blocks */}
          {activeProposal?.scheduled_intervals.map((interval, i) => {
            const startX = tickToX(interval.start_tick);
            const endX = tickToX(interval.end_tick);
            const width = Math.max(endX - startX, 4);
            const y = getTrackY(interval) + 4;
            const height = trackHeight - 14;
            const color = getColorForOperation(interval.operation);

            return (
              <g
                key={i}
                onMouseEnter={() => setHoveredInterval(interval)}
                onMouseLeave={() => setHoveredInterval(null)}
                style={{ cursor: 'pointer' }}
              >
                <rect
                  x={startX}
                  y={y}
                  width={width}
                  height={height}
                  fill={color}
                  opacity="0.85"
                  rx="4"
                  stroke="#ffffff"
                  strokeWidth="0.5"
                />
                {width > 35 && (
                  <text
                    x={startX + width / 2}
                    y={y + height / 2 + 4}
                    fill="#0f172a"
                    fontSize="10"
                    fontWeight="700"
                    textAnchor="middle"
                  >
                    {interval.operation.length > 22 ? `${interval.operation.slice(0, 20)}...` : interval.operation}
                  </text>
                )}
              </g>
            );
          })}
        </svg>

        {/* Hover detail tooltip */}
        {hoveredInterval && (
          <div
            style={{
              position: 'absolute',
              bottom: '12px',
              right: '16px',
              background: '#0f172a',
              border: '1px solid var(--accent-cyan)',
              borderRadius: '6px',
              padding: '8px 12px',
              fontSize: '12px',
              color: 'var(--text-primary)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
              pointerEvents: 'none'
            }}
          >
            <div style={{ fontWeight: '700', color: 'var(--accent-cyan)' }}>{hoveredInterval.operation}</div>
            <div style={{ color: 'var(--text-secondary)' }}>
              Entity: <strong>{hoveredInterval.entity_id}</strong> | Window: <strong>{hoveredInterval.start_clock} (t={hoveredInterval.start_tick}) ➔ {hoveredInterval.end_clock} (t={hoveredInterval.end_tick})</strong>
            </div>
            <div style={{ color: 'var(--text-muted)' }}>
              Duration: {(hoveredInterval.end_tick - hoveredInterval.start_tick) * 5} min ({hoveredInterval.end_tick - hoveredInterval.start_tick} ticks)
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#f59e0b', borderRadius: '2px' }} />
          <span>Bay Immobilized / Staged in Holding</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#06b6d4', borderRadius: '2px' }} />
          <span>Parts Installation (RO-1042)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#10b981', borderRadius: '2px' }} />
          <span>Clearance Transit (10m)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#3b82f6', borderRadius: '2px' }} />
          <span>Fleet ADAS Calibration (RO-1051)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#8b5cf6', borderRadius: '2px' }} />
          <span>Relocation / Return Transit (15m)</span>
        </div>
      </div>
    </div>
  );
};
