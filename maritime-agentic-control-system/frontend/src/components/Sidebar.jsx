import React from 'react';
import { 
  Activity, Ship, ShieldAlert, Navigation, Cpu, Settings as SettingsIcon, 
  Anchor, Radio, ShieldCheck 
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Fleet Overview', icon: <Activity size={20} /> },
    { id: 'tracking', label: 'Vessel Tracking', icon: <Ship size={20} /> },
    { id: 'monitor', label: 'Event Monitor', icon: <Radio size={20} /> },
    { id: 'risk', label: 'Risk Analysis', icon: <ShieldAlert size={20} /> },
    { id: 'routes', label: 'Route Planning', icon: <Navigation size={20} /> },
    { id: 'workflow', label: 'AI LangGraph Pipeline', icon: <Cpu size={20} /> },
    { id: 'governance', label: 'Agent Governance', icon: <ShieldAlert size={20} /> },
    { id: 'settings', label: 'System Settings', icon: <SettingsIcon size={20} /> }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand" style={{ padding: '0 8px' }}>
          <Anchor className="brand-icon" size={26} />
          <span className="brand-title" style={{ fontSize: '1.25rem' }}>Maritime AI</span>
        </div>
        <div style={{ 
          fontSize: '0.75rem', 
          color: 'var(--text-muted)', 
          margin: '4px 0 0 38px',
          letterSpacing: '0.08em',
          textTransform: 'uppercase'
        }}>
          Agentic Control v2.4
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`sidebar-btn ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <span className="icon-wrap" style={{ color: isActive ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
                {item.icon}
              </span>
              <span className="btn-label">{item.label}</span>
              {isActive && <div className="active-indicator" />}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="security-box">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-emerald)', fontWeight: 600, fontSize: '0.85rem' }}>
            <ShieldCheck size={16} /> ENCRYPTED LINK
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            FastAPI Backend: Connected
          </div>
        </div>
      </div>
    </aside>
  );
}
