import React, { useState, useEffect } from 'react';
import { Anchor, Activity, ShieldAlert, Navigation, Clock } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemStatus }) {
  const [time, setTime] = useState(new Date().toUTCString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <nav className="navbar">
      <div className="brand">
        <Anchor className="brand-icon" size={28} />
        <div>
          <span className="brand-title">Maritime Agentic Control</span>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
            Autonomous Fleet & Route Management
          </div>
        </div>
      </div>
      
      <div className="nav-links">
        <button 
          className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <Activity size={16} />
          Dashboard
        </button>
        <button 
          className={`nav-btn ${activeTab === 'risk' ? 'active' : ''}`}
          onClick={() => setActiveTab('risk')}
        >
          <ShieldAlert size={16} />
          Risk Matrix
        </button>
        <button 
          className={`nav-btn ${activeTab === 'routes' ? 'active' : ''}`}
          onClick={() => setActiveTab('routes')}
        >
          <Navigation size={16} />
          AI Corridors
        </button>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-muted)', background: 'rgba(0,0,0,0.3)', padding: '6px 12px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
          <Clock size={14} color="var(--accent-cyan)" />
          <span style={{ fontFamily: 'monospace' }}>{time}</span>
        </div>

        <div className="status-badge">
          <div className="pulse-dot"></div>
          <span>SYSTEM {systemStatus || 'ONLINE'}</span>
        </div>
      </div>
    </nav>
  );
}
