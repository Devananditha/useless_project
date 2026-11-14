import React, { useState } from 'react';
import { BenchmarkResult } from '../types';
import { runBenchmark } from '../api';
import { X, Play, BarChart3, CheckCircle2 } from './Icons';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const BenchmarkModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const [result, setResult] = useState<BenchmarkResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await runBenchmark(100);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Benchmark run failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.75)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px'
      }}
    >
      <div
        className="card"
        style={{
          width: '100%',
          maxWidth: '680px',
          background: '#111927',
          borderColor: 'var(--accent-cyan)',
          maxHeight: '90vh',
          overflowY: 'auto'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <BarChart3 size={20} style={{ color: 'var(--accent-cyan)' }} />
            <h3 style={{ fontSize: '18px', fontWeight: '700', color: 'var(--text-primary)' }}>
              N=100 Paired Seeds Live Solver Benchmark
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'transparent', color: 'var(--text-muted)', padding: '4px' }}
          >
            <X size={20} />
          </button>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '18px' }}>
          Executes real Google OR-Tools CP-SAT models across 100 pseudo-randomized dealership disruption scenarios (varying carrier arrival jitter, technician availability, priority weights, and shop duration).
        </p>

        <div style={{ marginBottom: '20px', display: 'flex', gap: '12px' }}>
          <button
            onClick={handleRun}
            disabled={loading}
            style={{
              padding: '8px 18px',
              fontSize: '13px',
              fontWeight: '700',
              background: 'var(--accent-cyan)',
              color: '#000',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Play size={16} />
            {loading ? 'Running 100 Solves via CP-SAT...' : 'Execute N=100 Benchmark'}
          </button>
        </div>

        {error && (
          <div style={{ padding: '12px', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid #ef4444', borderRadius: '6px', color: '#fca5a5', marginBottom: '16px', fontSize: '13px' }}>
            {error}
          </div>
        )}

        {result && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
              <div style={{ background: '#0a0f1d', padding: '12px', borderRadius: '6px', textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>P3 WIN/TIE RATE</div>
                <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--accent-emerald)' }}>
                  {result.p3_win_or_tie_rate_pct.toFixed(1)}%
                </div>
                <div style={{ fontSize: '11px', color: 'var(--accent-emerald)' }}>
                  {result.p3_outperform_count} Wins, {result.tie_count} Ties, {result.p3_worsened_count} Losses
                </div>
              </div>

              <div style={{ background: '#0a0f1d', padding: '12px', borderRadius: '6px', textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>MEAN LATENESS REDUCTION</div>
                <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--accent-cyan)' }}>
                  {result.mean_weighted_lateness_reduction_pct.toFixed(1)}%
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                  {result.mean_a2_weighted_lateness.toFixed(1)} ➔ {result.mean_p3_weighted_lateness.toFixed(1)} ticks
                </div>
              </div>

              <div style={{ background: '#0a0f1d', padding: '12px', borderRadius: '6px', textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>MEAN DELAY SAVED</div>
                <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--accent-emerald)' }}>
                  {result.mean_downstream_delay_savings_min.toFixed(0)} min
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                  Valid Seeds: {result.valid_paired_seeds} / {result.total_seeds}
                </div>
              </div>
            </div>

            <div style={{ background: '#0a0f1d', padding: '12px', borderRadius: '6px', fontSize: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Total Seeds Tested:</span>
                <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{result.total_seeds} paired instances (Master seed: {result.master_seed})</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Total Wall-Clock Time:</span>
                <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{result.total_wall_clock_seconds.toFixed(2)} seconds</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Mean CP-SAT Solve Time:</span>
                <span style={{ fontWeight: '600', color: 'var(--accent-cyan)' }}>
                  P3: {result.mean_p3_solve_time_ms.toFixed(1)} ms | A2: {result.mean_a2_solve_time_ms.toFixed(1)} ms
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ color: 'var(--text-muted)' }}>P3 Solver Statuses:</span>
                <span style={{ fontWeight: '600', color: 'var(--badge-optimal-text)' }}>
                  {result.p3_status_distribution ? Object.entries(result.p3_status_distribution).map(([k, v]) => `${k}: ${v}`).join(', ') : 'N/A'}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>A2 Solver Statuses:</span>
                <span style={{ fontWeight: '600', color: '#93c5fd' }}>
                  {result.a2_status_distribution ? Object.entries(result.a2_status_distribution).map(([k, v]) => `${k}: ${v}`).join(', ') : 'N/A'}
                </span>
              </div>
            </div>

            <div style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
              <strong>Scope notice:</strong> P3 option set includes candidates available to A2; win-rate compares joint optimisation against fixed-source sequential baseline A2 under synthetic operational jitter, not against all human manager decisions in real dealership operations.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
