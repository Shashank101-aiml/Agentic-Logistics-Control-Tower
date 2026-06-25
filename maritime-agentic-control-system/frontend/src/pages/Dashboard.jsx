import React, { useState, useEffect } from 'react';
import { 
  Ship, AlertTriangle, ShieldCheck, Cpu, Play, CheckCircle2, 
  MapPin, Wind, Navigation, Sparkles, RefreshCw 
} from 'lucide-react';
import { 
  fetchDashboard, fetchAgents, runWorkflow, fetchRecommendations 
} from '../services/api';

export default function Dashboard({ activeTab }) {
  const [stats, setStats] = useState(null);
  const [agents, setAgents] = useState([]);
  const [workflowRes, setWorkflowRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashboardData, agentsData] = await Promise.all([
        fetchDashboard(),
        fetchAgents()
      ]);
      setStats(dashboardData);
      setAgents(agentsData);
    } catch (err) {
      setError('Could not connect to FastAPI Backend. Make sure server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleRunWorkflow = async () => {
    setExecuting(true);
    try {
      const res = await runWorkflow();
      setWorkflowRes(res);
      await loadData();
    } catch (err) {
      setError('Workflow execution failed.');
    } finally {
      setExecuting(false);
    }
  };

  if (error) {
    return (
      <main className="main-content">
        <div className="glass-panel" style={{ borderColor: 'var(--accent-rose)', textAlign: 'center', padding: '40px' }}>
          <AlertTriangle size={48} color="var(--accent-rose)" style={{ margin: '0 auto 16px' }} />
          <h2 style={{ color: 'var(--accent-rose)', marginBottom: '12px' }}>Connection Error</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '24px' }}>{error}</p>
          <button className="btn-action" onClick={loadData} style={{ margin: '0 auto' }}>
            <RefreshCw size={18} /> Retry Connection
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="main-content">
      {/* KPI Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div>
            <div className="kpi-label">Active Vessels</div>
            <div className="kpi-val">{stats?.active_vessels ?? '--'}</div>
          </div>
          <div className="kpi-icon-box" style={{ color: 'var(--accent-teal)' }}>
            <Ship size={28} />
          </div>
        </div>

        <div className="kpi-card">
          <div>
            <div className="kpi-label">Weather Alerts</div>
            <div className="kpi-val" style={{ color: stats?.active_alerts > 1 ? 'var(--accent-amber)' : 'var(--accent-emerald)' }}>
              {stats?.active_alerts ?? '--'}
            </div>
          </div>
          <div className="kpi-icon-box" style={{ color: 'var(--accent-amber)' }}>
            <Wind size={28} />
          </div>
        </div>

        <div className="kpi-card">
          <div>
            <div className="kpi-label">Fleet Hazard Risk</div>
            <div className="kpi-val" style={{ color: stats?.average_fleet_risk > 50 ? 'var(--accent-rose)' : 'var(--accent-emerald)' }}>
              {stats?.average_fleet_risk ? `${stats.average_fleet_risk}/100` : '--'}
            </div>
          </div>
          <div className="kpi-icon-box" style={{ color: 'var(--accent-rose)' }}>
            <ShieldCheck size={28} />
          </div>
        </div>

        <div className="kpi-card">
          <div>
            <div className="kpi-label">Active AI Agents</div>
            <div className="kpi-val">{agents.length || 5}</div>
          </div>
          <div className="kpi-icon-box" style={{ color: 'var(--accent-cyan)' }}>
            <Cpu size={28} />
          </div>
        </div>
      </div>

      {activeTab === 'dashboard' ? (
        <div className="content-grid">
          {/* Telemetry Feed */}
          <div className="glass-panel">
            <div className="section-header">
              <h2 className="section-title">
                <Navigation size={22} color="var(--accent-cyan)" />
                Live Telemetry & Hazard Feed
              </h2>
              <button className="nav-btn" onClick={loadData}>
                <RefreshCw size={16} className={loading ? 'spin' : ''} />
              </button>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {stats?.recent_events?.map((evt, idx) => (
                <div key={evt.id || idx} className="agent-item">
                  <div className="agent-info">
                    <div className="agent-avatar" style={{ background: evt.severity === 'HIGH' ? 'rgba(255, 51, 102, 0.15)' : 'rgba(0, 242, 255, 0.1)' }}>
                      <AlertTriangle size={20} color={evt.severity === 'HIGH' ? 'var(--accent-rose)' : 'var(--accent-cyan)'} />
                    </div>
                    <div>
                      <div className="agent-name">{evt.event_type}</div>
                      <div className="agent-role" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                        <MapPin size={12} /> {evt.location}
                      </div>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span className="status-badge" style={{ 
                      background: evt.severity === 'HIGH' ? 'rgba(255, 51, 102, 0.12)' : 'rgba(0, 242, 255, 0.1)',
                      borderColor: evt.severity === 'HIGH' ? 'var(--accent-rose)' : 'var(--accent-cyan)',
                      color: evt.severity === 'HIGH' ? 'var(--accent-rose)' : 'var(--accent-cyan)'
                    }}>
                      {evt.severity} HAZARD
                    </span>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      {evt.timestamp}
                    </div>
                  </div>
                </div>
              )) || <p style={{ color: 'var(--text-muted)' }}>No recent telemetry events recorded.</p>}
            </div>
          </div>

          {/* Active Agents Panel */}
          <div className="glass-panel">
            <div className="section-header">
              <h2 className="section-title">
                <Sparkles size={22} color="var(--accent-amber)" />
                Autonomous Agent Fleet
              </h2>
            </div>
            
            <div className="agents-list">
              {agents.map((ag, i) => (
                <div key={ag.agent_name || i} className="agent-item">
                  <div className="agent-info">
                    <div className="agent-avatar">
                      <Cpu size={20} />
                    </div>
                    <div>
                      <div className="agent-name">{ag.agent_name}</div>
                      <div className="agent-role">{ag.role}</div>
                    </div>
                  </div>
                  <div className="status-badge" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
                    <div className="pulse-dot" style={{ width: '6px', height: '6px' }}></div>
                    {ag.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* Agentic AI Pipeline Tab */
        <div className="glass-panel">
          <div className="section-header">
            <div>
              <h2 className="section-title" style={{ fontSize: '1.5rem', marginBottom: '6px' }}>
                <Cpu size={26} color="var(--accent-cyan)" />
                Multi-Agent LangGraph Collaboration
              </h2>
              <p style={{ color: 'var(--text-muted)' }}>
                Trigger the autonomous coordination cycle: Ingestion Agent → Risk Assessment Agent → Route Planner → NLP Explainer.
              </p>
            </div>
            <button className="btn-action" onClick={handleRunWorkflow} disabled={executing}>
              {executing ? <RefreshCw size={18} className="spin" /> : <Play size={18} fill="#060b14" />}
              {executing ? 'Orchestrating Agents...' : 'Execute AI Pipeline'}
            </button>
          </div>

          {workflowRes ? (
            <div className="workflow-box">
              <div className="workflow-header">
                <CheckCircle2 size={24} color="var(--accent-emerald)" />
                Collaborative Pipeline Execution Completed Successfully
              </div>
              <p style={{ fontSize: '1.1rem', color: '#ffffff', margin: '12px 0', lineHeight: 1.5 }}>
                <strong style={{ color: 'var(--accent-cyan)' }}>AI Reasoning Summary: </strong>
                {workflowRes.explanation}
              </p>

              <div className="workflow-data">
                <div className="data-chunk">
                  <div className="chunk-label">Ingested Telemetry Event</div>
                  <div className="chunk-val">{workflowRes.event?.event_type} at {workflowRes.event?.location} ({workflowRes.event?.severity})</div>
                </div>

                <div className="data-chunk">
                  <div className="chunk-label">Assessed Hazard Score</div>
                  <div className={`chunk-val ${workflowRes.risk_score > 50 ? 'risk-high' : 'risk-low'}`}>
                    {workflowRes.risk_score} / 100 ({workflowRes.risk_score > 50 ? 'CRITICAL RISK' : 'NORMAL RISK'})
                  </div>
                </div>

                <div className="data-chunk">
                  <div className="chunk-label">Suggested Corridor</div>
                  <div className="chunk-val" style={{ color: 'var(--accent-cyan)' }}>{workflowRes.route?.route}</div>
                </div>

                <div className="data-chunk">
                  <div className="chunk-label">Routing Justification</div>
                  <div className="chunk-val">{workflowRes.route?.reason}</div>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '60px 20px', border: '1px dashed var(--border-subtle)', borderRadius: '12px', marginTop: '20px' }}>
              <Cpu size={48} color="var(--text-muted)" style={{ margin: '0 auto 16px', opacity: 0.5 }} />
              <h3 style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>Pipeline Idle</h3>
              <p style={{ color: 'var(--text-muted)', maxWidth: '500px', margin: '0 auto' }}>
                Click "Execute AI Pipeline" above to simulate real-time maritime telemetry analysis and multi-agent waypoint routing.
              </p>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
