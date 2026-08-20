import React from 'react';
import { AlertTriangle, ShieldAlert, X, Navigation } from 'lucide-react';

export default function AlertBanner({ alert, onDismiss, onAction }) {
  if (!alert) return null;

  const isCritical = alert.severity === 'CRITICAL' || alert.severity === 'HIGH';

  return (
    <div 
      className="alert-banner" 
      style={{
        background: isCritical 
          ? 'linear-gradient(90deg, rgba(255, 51, 102, 0.25) 0%, rgba(13, 23, 42, 0.9) 100%)' 
          : 'linear-gradient(90deg, rgba(255, 184, 0, 0.25) 0%, rgba(13, 23, 42, 0.9) 100%)',
        border: `1px solid ${isCritical ? 'var(--accent-rose)' : 'var(--accent-amber)'}`,
        borderRadius: '12px',
        padding: '14px 20px',
        margin: '0 0 24px 0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: `0 0 24px ${isCritical ? 'rgba(255, 51, 102, 0.2)' : 'rgba(255, 184, 0, 0.2)'}`,
        animation: 'slideDown 0.3s ease-out'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{ 
          width: '38px', 
          height: '38px', 
          borderRadius: '10px', 
          background: isCritical ? 'rgba(255, 51, 102, 0.2)' : 'rgba(255, 184, 0, 0.2)',
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center' 
        }}>
          {isCritical ? (
            <ShieldAlert size={22} color="var(--accent-rose)" />
          ) : (
            <AlertTriangle size={22} color="var(--accent-amber)" />
          )}
        </div>
        <div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#ffffff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ 
              color: isCritical ? 'var(--accent-rose)' : 'var(--accent-amber)',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              fontSize: '0.85rem'
            }}>
              [{alert.severity} HAZARD ALERT]
            </span>
            {alert.event_type}
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            Location: <strong style={{ color: '#fff' }}>{alert.location}</strong> — {alert.vessel_id ? `Vessel: ${alert.vessel_id}` : 'Affecting Fleet Corridor'}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {onAction && (
          <button 
            className="btn-action" 
            style={{ 
              padding: '8px 16px', 
              fontSize: '0.85rem',
              background: isCritical ? 'var(--accent-rose)' : 'var(--accent-amber)',
              color: '#060b14'
            }}
            onClick={onAction}
          >
            <Navigation size={14} /> View Reroute Protocol
          </button>
        )}
        <button 
          onClick={onDismiss}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '4px',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center'
          }}
          title="Dismiss Alert"
        >
          <X size={20} />
        </button>
      </div>
    </div>
  );
}
