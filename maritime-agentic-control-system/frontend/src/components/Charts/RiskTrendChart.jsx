import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function RiskTrendChart({ trends }) {
  const data = trends || [
    { time: '00:00', score: 32 },
    { time: '04:00', score: 38 },
    { time: '08:00', score: 45 },
    { time: '12:00', score: 55 },
    { time: '16:00', score: 68 },
    { time: '20:00', score: 62 },
    { time: '24:00', score: 40 }
  ];

  // SVG dimensions
  const width = 600;
  const height = 180;
  const paddingX = 40;
  const paddingY = 20;

  const points = data.map((d, i) => {
    const x = paddingX + (i / (data.length - 1)) * (width - paddingX * 2);
    const y = height - paddingY - (d.score / 100) * (height - paddingY * 2);
    return `${x},${y}`;
  }).join(' ');

  const areaPoints = `${paddingX},${height - paddingY} ${points} ${width - paddingX},${height - paddingY}`;

  return (
    <div className="glass-panel" style={{ padding: '24px', width: '100%' }}>
      <div className="section-header">
        <h3 className="section-title" style={{ fontSize: '1.15rem' }}>
          <ShieldAlert size={20} color="var(--accent-rose)" />
          Fleet Risk Score Trajectory (24h Trend)
        </h3>
        <span className="status-badge" style={{ fontSize: '0.75rem', background: 'rgba(255, 51, 102, 0.15)', borderColor: 'var(--accent-rose)', color: 'var(--accent-rose)' }}>
          PEAK HAZARD: 68/100
        </span>
      </div>

      <div style={{ width: '100%', overflowX: 'auto', marginTop: '16px' }}>
        <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: 'auto', overflow: 'visible' }}>
          <defs>
            <linearGradient id="riskGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="var(--accent-rose)" stopOpacity="0.4" />
              <stop offset="50%" stopColor="var(--accent-amber)" stopOpacity="0.2" />
              <stop offset="100%" stopColor="var(--accent-cyan)" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          <line x1={paddingX} y1={paddingY} x2={width - paddingX} y2={paddingY} stroke="rgba(255,255,255,0.08)" strokeDasharray="4 4" />
          <line x1={paddingX} y1={height / 2} x2={width - paddingX} y2={height / 2} stroke="rgba(255,255,255,0.08)" strokeDasharray="4 4" />
          <line x1={paddingX} y1={height - paddingY} x2={width - paddingX} y2={height - paddingY} stroke="rgba(255,255,255,0.2)" />

          {/* Area under curve */}
          <polygon points={areaPoints} fill="url(#riskGradient)" />

          {/* Line path */}
          <polyline fill="none" stroke="var(--accent-rose)" strokeWidth="3" points={points} strokeLinecap="round" strokeLinejoin="round" />

          {/* Data points and labels */}
          {data.map((d, i) => {
            const x = paddingX + (i / (data.length - 1)) * (width - paddingX * 2);
            const y = height - paddingY - (d.score / 100) * (height - paddingY * 2);
            const isHigh = d.score > 50;

            return (
              <g key={i}>
                <circle 
                  cx={x} 
                  cy={y} 
                  r="5" 
                  fill={isHigh ? 'var(--accent-rose)' : 'var(--accent-cyan)'} 
                  stroke="#060b14" 
                  strokeWidth="2"
                  style={{ cursor: 'pointer' }}
                >
                  <title>{`${d.time}: Risk Score ${d.score}/100`}</title>
                </circle>
                <text x={x} y={height - 4} fill="var(--text-muted)" fontSize="10" textAnchor="middle" fontFamily="var(--font-body)">
                  {d.time}
                </text>
                <text x={x} y={y - 10} fill={isHigh ? 'var(--accent-rose)' : '#fff'} fontSize="11" fontWeight="700" textAnchor="middle" fontFamily="var(--font-heading)">
                  {d.score}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}
