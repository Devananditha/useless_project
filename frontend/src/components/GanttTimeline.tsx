import React, { useState } from 'react';
import { Proposal, ScheduledInterval, ScenarioSnapshot } from '../types';
import { tickToClock } from '../utils';
import { Calendar, Clock, Layers } from './Icons';

interface Props {
  baselineProposal: Proposal | null;
  jointProposal: Proposal | null;
  scenario?: ScenarioSnapshot | null;
}

export const GanttTimeline: React.FC<Props> = ({ baselineProposal, jointProposal, scenario }) => {
  const [viewMode, setViewMode] = useState<'P3' | 'A2'>('P3');
  const [hoveredInterval, setHoveredInterval] = useState<ScheduledInterval | null>(null);

  const activeProposal = viewMode === 'A2' ? baselineProposal : jointProposal;

  // Timeline geometry
  // Canonical horizon: t=0 (08:00) to t=108 (17:00), 5 min per tick = 12 ticks/hr
  const totalTicks = 108;
  const svgWidth = 1050;
  const trackHeight = 44;
  const headerHeight = 44;
  const labelWidth = 180;
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
    if (op.includes('Stalled') || op.includes('Immobilized') || op.includes('Staged in Holding')) return '#f59e0b'; // amber
    if (op.includes('Installation') || op.includes('Part Installation')) return '#06b6d4'; // cyan
    if (op.includes('Clearance') || op.includes('Verification')) return '#10b981'; // emerald
    if (op.includes('Service') || op.includes('Calibration') || op.includes('ADAS')) return '#3b82f6'; // blue
    if (op.includes('Relocation') || op.includes('Transit') || op.includes('Return')) return '#8b5cf6'; // purple
    return '#64748b';
  };

  const tracks = [
    { id: 'BAY_B4', label: 'Bay B4 (Alignment Hoist)', y: headerHeight },
    { id: 'HOLDING_H2', label: 'Holding Area H2 (Buffer)', y: headerHeight + trackHeight },
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

  // Promise markers
  const ro1051PromiseTick = scenario?.ro1051.promise_ticks ?? 54;
  const ro1042PromiseTick = scenario?.ro1042.promise_ticks ?? 66;
  const ro1051PromiseClock = scenario?.ro1051 ? tickToClock(scenario.ro1051.promise_ticks) : '12:30';
  const ro1042PromiseClock = scenario?.ro1042 ? tickToClock(scenario.ro1042.promise_ticks) : '13:30';

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <div className="card-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Calendar size={18} style={{ color: 'var(--accent-cyan)' }} />
          <span>Gantt Operational Timeline & Hoist Scheduling (Horizon: 08:00 – 17:00)</span>
          <span className="badge badge-optimal">5-min Ticks (H=108)</span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setViewMode('P3')}
            style={{
              padding: '5px 12px',
              fontSize: '12px',
              background: viewMode === 'P3' ? 'var(--accent-cyan)' : '#1e293b',
              color: viewMode === 'P3' ? '#000' : 'var(--text-secondary)',
              fontWeight: '700',
              border: viewMode === 'P3' ? '1px solid var(--accent-cyan)' : '1px solid var(--border-color)',
              boxShadow: viewMode === 'P3' ? '0 0 10px rgba(6, 182, 212, 0.4)' : 'none'
            }}
          >
            P3 Joint Schedule {viewMode === 'P3' ? '(Active)' : ''}
          </button>
          <button
            onClick={() => setViewMode('A2')}
            style={{
              padding: '5px 12px',
              fontSize: '12px',
              background: viewMode === 'A2' ? 'var(--accent-amber)' : '#1e293b',
              color: viewMode === 'A2' ? '#000' : 'var(--text-secondary)',
              fontWeight: '700',
              border: viewMode === 'A2' ? '1px solid var(--accent-amber)' : '1px solid var(--border-color)',
              boxShadow: viewMode === 'A2' ? '0 0 10px rgba(245, 158, 11, 0.4)' : 'none'
            }}
          >
            A2 Baseline Schedule {viewMode === 'A2' ? '(Active)' : ''}
          </button>
        </div>
      </div>

      <div style={{ position: 'relative', overflowX: 'auto', background: '#0a0f1d', borderRadius: '8px', padding: '14px', border: '1px solid var(--border-color)' }}>
        <svg
          viewBox={`0 0 ${svgWidth} ${totalHeight}`}
          className="timeline-svg"
          style={{ minWidth: '880px' }}
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
                  stroke="#1c2738"
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
                x={12}
                y={track.y + trackHeight / 2 - 2}
                fill="#cbd5e1"
                fontSize="12"
                fontWeight="700"
              >
                {track.label}
              </text>
            </g>
          ))}

          {/* Promise Marker Lines */}
          {/* RO-1051 Commercial Fleet Promise */}
          <line
            x1={tickToX(ro1051PromiseTick)}
            y1={headerHeight}
            x2={tickToX(ro1051PromiseTick)}
            y2={totalHeight - 10}
            stroke="var(--accent-rose)"
            strokeWidth="2"
            strokeDasharray="4 2"
          />
          <text
            x={tickToX(ro1051PromiseTick)}
            y={headerHeight - 24}
            fill="var(--accent-rose)"
            fontSize="10"
            fontWeight="800"
            textAnchor="middle"
          >
            RO-1051 Promise (t={ro1051PromiseTick}, {ro1051PromiseClock})
          </text>

          {/* RO-1042 Ford Explorer Promise */}
          <line
            x1={tickToX(ro1042PromiseTick)}
            y1={headerHeight}
            x2={tickToX(ro1042PromiseTick)}
            y2={totalHeight - 10}
            stroke="var(--accent-cyan)"
            strokeWidth="1.5"
            strokeDasharray="3 3"
          />
          <text
            x={tickToX(ro1042PromiseTick)}
            y={headerHeight - 24}
            fill="var(--accent-cyan)"
            fontSize="10"
            fontWeight="800"
            textAnchor="middle"
          >
            RO-1042 Promise (t={ro1042PromiseTick}, {ro1042PromiseClock})
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
                  opacity="0.88"
                  rx="4"
                  stroke="#ffffff"
                  strokeWidth="0.75"
                />
                {width > 36 && (
                  <text
                    x={startX + width / 2}
                    y={y + height / 2 + 4}
                    fill="#0a0f1d"
                    fontSize="10"
                    fontWeight="800"
                    textAnchor="middle"
                  >
                    {interval.operation.length > 24 ? `${interval.operation.slice(0, 22)}...` : interval.operation}
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
              bottom: '14px',
              right: '18px',
              background: '#0e1726',
              border: '1px solid var(--accent-cyan)',
              borderRadius: '6px',
              padding: '10px 14px',
              fontSize: '12px',
              color: 'var(--text-primary)',
              boxShadow: '0 6px 16px rgba(0,0,0,0.5)',
              pointerEvents: 'none',
              zIndex: 10
            }}
          >
            <div style={{ fontWeight: '800', color: 'var(--accent-cyan)', fontSize: '13px' }}>
              {hoveredInterval.operation}
            </div>
            <div style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
              Entity: <strong>{hoveredInterval.entity_id}</strong> | Window: <strong>{hoveredInterval.start_clock} (t={hoveredInterval.start_tick}) ➔ {hoveredInterval.end_clock} (t={hoveredInterval.end_tick})</strong>
            </div>
            <div style={{ color: 'var(--text-muted)', marginTop: '2px' }}>
              Duration: {(hoveredInterval.end_tick - hoveredInterval.start_tick) * 5} min ({hoveredInterval.end_tick - hoveredInterval.start_tick} ticks)
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginTop: '14px', fontSize: '12px', color: 'var(--text-secondary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#f59e0b', borderRadius: '3px' }} />
          <span>Immobilized on Hoist / Staged in Holding</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#06b6d4', borderRadius: '3px' }} />
          <span>Part Installation (RO-1042)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#10b981', borderRadius: '3px' }} />
          <span>Clearance Transit (10 min)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#3b82f6', borderRadius: '3px' }} />
          <span>Commercial ADAS Calibration (RO-1051)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '12px', height: '12px', background: '#8b5cf6', borderRadius: '3px' }} />
          <span>Relocation & Return Transit (15 min each)</span>
        </div>
      </div>
    </div>
  );
};
