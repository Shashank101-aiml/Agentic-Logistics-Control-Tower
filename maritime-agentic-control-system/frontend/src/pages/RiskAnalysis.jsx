import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle, Activity, RefreshCw } from 'lucide-react';
import { useRisks } from '../hooks/useRisks';
import RiskCard from '../components/RiskCard';
import RiskTrendChart from '../components/Charts/RiskTrendChart';
import LoadingSpinner from '../components/LoadingSpinner';

export default function RiskAnalysis() {
  const { 
    currentRisk, 
    trends, 
    fleetSummary, 
    isHighRisk, 
    loading, 
    error, 
    mitigationActive, 
    activateMitigation, 
    refreshRisk 
  } = useRisks();

  const categories = [
    { title: 'Severe Weather Systems', count: 3, level: 'CRITICAL', score: 72, desc: 'Cyclonic activity in Sector 4B creating 4.5m swells and high wind sheer.' },
    { title: 'Piracy & Security Threats', count: 2, level: 'ELEVATED', score: 58, desc: 'Suspicious fast-skiff movements reported along Gulf of Aden Corridor B.' },
    { title: 'Port Congestion & Anchor Queues', count: 4, level: 'MODERATE', score: 35, desc: 'Strait of Malacca terminal delays averaging 8-14 hours due to heavy traffic.' },
    { title: 'Vessel Equipment & Telemetry', count: 0, level: 'NORMAL', score: 12, desc: 'All fleet propulsion, GPS navigation, and satellite communications nominal.' }
  ];

  return (
    <div className="page-wrapper">
      <div className="section-header" style={{ marginBottom: '24px' }}>
        <div>
          <h1 className="section-title" style={{ fontSize: '1.8rem', color: '#ffffff' }}>
            <ShieldAlert size={28} color="var(--accent-rose)" />
            Navigational Hazard & Risk Analysis
          </h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
            AI-assessed vulnerability scoring, probability matrices, and active mitigation protocols across global corridors.
          </p>
        </div>

        <button className="btn-action" onClick={refreshRisk}>
          <RefreshCw size={16} className={loading ? 'spin' : ''} />
          Recalculate Risk Matrix
        </button>
      </div>

      {loading && !currentRisk ? (
        <LoadingSpinner message="Calculating multi-variate hazard risk models..." />
      ) : error ? (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '40px', borderColor: 'var(--accent-rose)' }}>
          <AlertTriangle size={36} color="var(--accent-rose)" style={{ margin: '0 auto 12px' }} />
          <p style={{ color: 'var(--text-main)' }}>{error}</p>
        </div>
      ) : (
        <>
          {/* Top Row: Current Risk Card + Fleet Risk Summary */}
          <div className="content-grid" style={{ gridTemplateColumns: '1.3fr 1fr', marginBottom: '24px' }}>
            <RiskCard 
              risk={currentRisk} 
              onMitigate={activateMitigation} 
              mitigationActive={mitigationActive} 
            />

            <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div className="section-header">
                  <h3 className="section-title" style={{ fontSize: '1.15rem' }}>
                    <Activity size={20} color="var(--accent-amber)" />
                    Fleet Vulnerability Overview
                  </h3>
                </div>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  The Risk Assessment Agent continuously evaluates meteorological forecasts, geopolitical advisories, and vessel telemetry to calculate composite hazard scores.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', margin: '20px 0' }}>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>VESSELS AT CRITICAL RISK</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: isHighRisk ? 'var(--accent-rose)' : 'var(--accent-emerald)', marginTop: '4px' }}>
                    {fleetSummary.vesselsAtRisk} <span style={{ fontSize: '0.9rem', fontWeight: 400, color: 'var(--text-muted)' }}>/ {fleetSummary.totalVessels}</span>
                  </div>
                </div>

                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>ACTIVE SECURITY ALERTS</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-amber)', marginTop: '4px' }}>
                    {fleetSummary.activeAlerts}
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', color: 'var(--accent-cyan)', background: 'rgba(0, 242, 255, 0.08)', padding: '10px 14px', borderRadius: '8px' }}>
                <ShieldCheck size={16} /> Autonomous LangGraph safety guardrails active.
              </div>
            </div>
          </div>

          {/* Risk Trend Chart */}
          <div style={{ marginBottom: '24px' }}>
            <RiskTrendChart trends={trends} />
          </div>

          {/* Hazard Breakdown by Category */}
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 className="section-title" style={{ fontSize: '1.15rem', marginBottom: '18px' }}>
              Hazard Breakdown by Domain Category
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              {categories.map((cat, i) => {
                const color = cat.level === 'CRITICAL' ? 'var(--accent-rose)' : cat.level === 'ELEVATED' ? 'var(--accent-amber)' : 'var(--accent-emerald)';

                return (
                  <div key={i} style={{ background: 'rgba(0,0,0,0.25)', borderLeft: `4px solid ${color}`, padding: '16px', borderRadius: '10px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                      <h4 style={{ color: '#fff', fontSize: '1rem' }}>{cat.title}</h4>
                      <span className="status-badge" style={{ fontSize: '0.7rem', background: `${color}15`, borderColor: color, color }}>
                        {cat.level} ({cat.score}/100)
                      </span>
                    </div>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
                      {cat.desc}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
