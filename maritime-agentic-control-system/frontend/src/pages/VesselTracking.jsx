import React, { useState } from 'react';
import { getVessels } from '../services/vesselService';
import { Ship, Navigation, Compass, MapPin, Search, ShieldCheck, AlertTriangle } from 'lucide-react';

export default function VesselTracking() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedVessel, setSelectedVessel] = useState(null);

  const [fleet, setFleet] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  const fetchVessels = async () => {
    try {
      setLoading(true);
      const data = await getVessels();
      setFleet(data);
    } catch (err) {
      setError('Failed to load vessel telemetry.');
    } finally {
      setLoading(false);
    }
  };

  fetchVessels();

  const interval = setInterval(fetchVessels, 15000);

  return () => clearInterval(interval);
}, []);

  const filteredFleet = fleet.filter(v => 
    v.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    v.corridor.toLowerCase().includes(searchTerm.toLowerCase()) ||
    v.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="page-wrapper">
      <div className="section-header" style={{ marginBottom: '24px' }}>
        <div>
          <h1 className="section-title" style={{ fontSize: '1.8rem', color: '#ffffff' }}>
            <Ship size={28} color="var(--accent-cyan)" />
            Real-Time Fleet & Corridor Tracking
          </h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
            Monitor active vessel positions, heading vectors, and AI-assigned maritime transport corridors.
          </p>
        </div>

        <div style={{ position: 'relative', width: '320px' }}>
          <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
          <input 
            type="text"
            placeholder="Search vessels, corridors, types..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              background: 'rgba(0,0,0,0.4)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '10px',
              padding: '10px 14px 10px 40px',
              color: '#fff',
              fontFamily: 'var(--font-body)',
              outline: 'none'
            }}
          />
        </div>
      </div>

      <div className="content-grid" style={{ gridTemplateColumns: '1.4fr 1fr' }}>
        {/* Simulated Radar / Map View */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', minHeight: '520px' }}>
          <div className="section-header">
            <h3 className="section-title" style={{ fontSize: '1.15rem' }}>
              <Compass size={20} color="var(--accent-teal)" />
              Global Telemetry & Waypoint Radar
            </h3>
            <span className="status-badge" style={{ fontSize: '0.75rem' }}>
              <span className="pulse-dot"></span> LIVE SATELLITE LINK
            </span>
          </div>

          <div style={{
            flex: 1,
            background: 'radial-gradient(circle at 50% 50%, rgba(0, 184, 255, 0.1) 0%, rgba(6, 11, 20, 0.95) 80%)',
            border: '1px solid rgba(0, 242, 255, 0.2)',
            borderRadius: '12px',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            {/* Radar circles */}
            <div style={{ position: 'absolute', width: '380px', height: '380px', border: '1px solid rgba(0, 242, 255, 0.12)', borderRadius: '50%' }} />
            <div style={{ position: 'absolute', width: '260px', height: '260px', border: '1px solid rgba(0, 242, 255, 0.18)', borderRadius: '50%' }} />
            <div style={{ position: 'absolute', width: '140px', height: '140px', border: '1px solid rgba(0, 242, 255, 0.25)', borderRadius: '50%' }} />
            <div style={{ position: 'absolute', width: '100%', height: '1px', background: 'rgba(0, 242, 255, 0.15)' }} />
            <div style={{ position: 'absolute', height: '100%', width: '1px', background: 'rgba(0, 242, 255, 0.15)' }} />

            {/* Radar sweep animation */}
            <div style={{
              position: 'absolute',
              width: '200px',
              height: '200px',
              background: 'linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, transparent 80%)',
              borderRadius: '100% 0 0 0',
              transformOrigin: 'bottom right',
              top: '50%',
              left: '50%',
              marginTop: '-200px',
              marginLeft: '-200px',
              animation: 'radarSweep 6s infinite linear'
            }} />

            {/* Vessel blips */}
            {filteredFleet.map((v, i) => {
              // Map lat/lng roughly to box
              const top = 50 - (v.lat - 10) * 1.5;
              const left = 50 + (v.lng - 70) * 1.2;
              const isSelected = selectedVessel?.id === v.id;
              const isCritical = v.risk === 'CRITICAL';

              return (
                <div 
                  key={v.id}
                  onClick={() => setSelectedVessel(v)}
                  style={{
                    position: 'absolute',
                    top: `${Math.min(85, Math.max(15, top))}%`,
                    left: `${Math.min(85, Math.max(15, left))}%`,
                    transform: 'translate(-50%, -50%)',
                    cursor: 'pointer',
                    zIndex: isSelected ? 20 : 10
                  }}
                >
                  <div style={{
                    width: isSelected ? '18px' : '12px',
                    height: isSelected ? '18px' : '12px',
                    backgroundColor: isCritical ? 'var(--accent-rose)' : v.risk === 'ELEVATED' ? 'var(--accent-amber)' : 'var(--accent-cyan)',
                    borderRadius: '50%',
                    boxShadow: `0 0 12px ${isCritical ? 'var(--accent-rose)' : 'var(--accent-cyan)'}`,
                    border: '2px solid #060b14',
                    transition: 'all 0.2s ease'
                  }} />
                  
                  <div style={{
                    position: 'absolute',
                    top: '14px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    background: 'rgba(6, 11, 20, 0.9)',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontSize: '0.65rem',
                    color: '#fff',
                    whiteSpace: 'nowrap',
                    border: isSelected ? '1px solid var(--accent-cyan)' : 'none'
                  }}>
                    {v.name}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Vessel Details & List */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 className="section-title" style={{ fontSize: '1.15rem' }}>
            <Navigation size={20} color="var(--accent-amber)" />
            Active Fleet Status ({filteredFleet.length})
          </h3>

          {selectedVessel && (
            <div style={{ background: 'rgba(0, 242, 255, 0.08)', border: '1px solid var(--accent-cyan)', padding: '16px', borderRadius: '12px', marginBottom: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h4 style={{ color: 'var(--accent-cyan)', fontSize: '1.1rem' }}>{selectedVessel.name}</h4>
                <span className="status-badge" style={{ fontSize: '0.7rem', padding: '2px 8px' }}>{selectedVessel.status}</span>
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                <div>Type: <strong style={{ color: '#fff' }}>{selectedVessel.type}</strong></div>
                <div>Speed: <strong style={{ color: '#fff' }}>{selectedVessel.speed}</strong></div>
                <div>Heading: <strong style={{ color: '#fff' }}>{selectedVessel.heading}</strong></div>
                <div>Coords: <strong style={{ color: '#fff' }}>{selectedVessel.lat}°N, {selectedVessel.lng}°E</strong></div>
              </div>
              <div style={{ marginTop: '8px', fontSize: '0.85rem', color: 'var(--text-main)' }}>
                Assigned Corridor: <strong style={{ color: 'var(--accent-teal)' }}>{selectedVessel.corridor}</strong>
              </div>
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', maxHeight: '400px', paddingRight: '4px' }}>
            {filteredFleet.map(v => {
              const isSelected = selectedVessel?.id === v.id;
              const isCritical = v.risk === 'CRITICAL';

              return (
                <div 
                  key={v.id}
                  onClick={() => setSelectedVessel(v)}
                  className="agent-item"
                  style={{
                    cursor: 'pointer',
                    background: isSelected ? 'rgba(0, 242, 255, 0.1)' : 'rgba(255, 255, 255, 0.03)',
                    borderColor: isSelected ? 'var(--accent-cyan)' : 'rgba(255, 255, 255, 0.06)'
                  }}
                >
                  <div className="agent-info">
                    <div className="agent-avatar" style={{ background: isCritical ? 'rgba(255, 51, 102, 0.15)' : 'rgba(0, 242, 255, 0.1)' }}>
                      <Ship size={18} color={isCritical ? 'var(--accent-rose)' : 'var(--accent-cyan)'} />
                    </div>
                    <div>
                      <div className="agent-name">{v.name}</div>
                      <div className="agent-role">{v.type} — {v.speed} ({v.heading})</div>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span className="status-badge" style={{ 
                      fontSize: '0.65rem', 
                      padding: '2px 8px',
                      background: isCritical ? 'rgba(255, 51, 102, 0.15)' : 'rgba(0, 229, 153, 0.15)',
                      color: isCritical ? 'var(--accent-rose)' : 'var(--accent-emerald)',
                      borderColor: isCritical ? 'var(--accent-rose)' : 'var(--accent-emerald)'
                    }}>
                      {v.status}
                    </span>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      <MapPin size={10} style={{ display: 'inline' }} /> {v.corridor.split('(')[0]}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
