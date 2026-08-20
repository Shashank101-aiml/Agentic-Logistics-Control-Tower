import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, ArrowUpRight, CheckCircle2 } from 'lucide-react';
import { getRiskLevel } from '../types/Risk';

export default function RiskCard({ risk, onMitigate, mitigationActive }) {
  if (!risk) return null;

  const level = getRiskLevel(risk.risk_score);
  const isCritical = level === 'CRITICAL';
  const isElevated = level === 'ELEVATED';

  const color = isCritical 
    ? 'var(--accent-rose)' 
    : isElevated 
    ? 'var(--accent-amber)' 
    : 'var(--accent-emerald)';

  return (
    <div className="glass-panel" style={{ 
      borderColor: isCritical ? 'rgba(255, 51, 102, 0.4)' : 'var(--border-glow)',
      background: isCritical ? 'rgba(255, 51, 102, 0.04)' : 'var(--bg-panel)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background glow effect */}
      <div style={{
        position: 'absolute',
        top: '-40px',
        right: '-40px',
        width: '140px',
        height: '140px',
        borderRadius: '50%',
        background: color,
        filter: 'blur(70px)',
        opacity: 0.15,
        pointerEvents: 'none'
      }} />

      <div className="section-header" style={{ marginBottom: '16px' }}>
        <div className="section-title" style={{ fontSize: '1.15rem', color: '#ffffff' }}>
          {isCritical ? <ShieldAlert size={22} color={color} /> : <ShieldCheck size={22} color={color} />}
          {risk.category}
        </div>
        <span className="status-badge" style={{ 
          background: `${color}20`,
          borderColor: color,
          color: color,
          fontWeight: 700
        }}>
          {level} RISK ({risk.risk_score}/100)
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '18px' }}>
        <div style={{ background: 'rgba(0,0,0,0.25)', padding: '10px 14px', borderRadius: '8px' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Impact Severity</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginTop: '4px' }}>{risk.impact}</div>
        </div>
        <div style={{ background: 'rgba(0,0,0,0.25)', padding: '10px 14px', borderRadius: '8px' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Probability</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginTop: '4px' }}>{risk.likelihood}</div>
        </div>
      </div>

      <div style={{ 
        background: 'rgba(255,255,255,0.03)', 
        border: '1px solid rgba(255,255,255,0.06)', 
        padding: '14px', 
        borderRadius: '10px',
        marginBottom: '18px'
      }}>
        <div style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)', fontWeight: 600, marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <AlertTriangle size={14} /> AI MITIGATION PROTOCOL:
        </div>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', lineHeight: 1.4 }}>
          {risk.mitigation_plan}
        </p>
      </div>

      {onMitigate && (
        <button 
          className="btn-action" 
          style={{ 
            width: '100%', 
            justifyContent: 'center',
            background: mitigationActive 
              ? 'rgba(0, 229, 153, 0.2)' 
              : isCritical 
              ? 'linear-gradient(135deg, var(--accent-rose), #ff6b8b)' 
              : 'linear-gradient(135deg, var(--accent-teal), var(--accent-cyan))',
            color: mitigationActive ? 'var(--accent-emerald)' : '#060b14',
            border: mitigationActive ? '1px solid var(--accent-emerald)' : 'none'
          }}
          onClick={onMitigate}
          disabled={mitigationActive}
        >
          {mitigationActive ? (
            <>
              <CheckCircle2 size={18} /> Mitigation Protocol Executed
            </>
          ) : (
            <>
              Execute Reroute & Mitigation <ArrowUpRight size={18} />
            </>
          )}
        </button>
      )}
    </div>
  );
}
