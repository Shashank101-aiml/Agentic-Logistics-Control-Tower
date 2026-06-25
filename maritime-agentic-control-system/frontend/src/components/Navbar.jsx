import React from 'react';
import { Anchor, ShieldAlert, Activity, Cpu } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemStatus }) {
  return (
    <nav className="navbar">
      <div className="brand">
        <Anchor className="brand-icon" size={28} />
        <span className="brand-title">Maritime Agentic Control</span>
      </div>
      
      <div className="nav-links">
        <button 
          className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <Activity size={18} />
          Fleet Overview
        </button>
        <button 
          className={`nav-btn ${activeTab === 'workflow' ? 'active' : ''}`}
          onClick={() => setActiveTab('workflow')}
        >
          <Cpu size={18} />
          Agentic AI Pipeline
        </button>
      </div>

      <div className="status-badge">
        <div className="pulse-dot"></div>
        <span>SYSTEM {systemStatus || 'ONLINE'}</span>
      </div>
    </nav>
  );
}
