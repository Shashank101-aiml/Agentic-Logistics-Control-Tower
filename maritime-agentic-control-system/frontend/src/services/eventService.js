import { createEvent } from '../types/Event';

const BASE_URL = 'http://localhost:8000/api';

const MOCK_EVENTS_HISTORY = [
  {
    id: 'EVT-1001',
    event_type: 'Severe Storm Cell & High Swell',
    location: 'Arabian Sea (Sector 4B)',
    severity: 'HIGH',
    timestamp: 'Just now',
    coordinates: { lat: 15.2, lng: 64.5 },
    vessel_id: 'MV-OCEAN-STAR'
  },
  {
    id: 'EVT-1002',
    event_type: 'Piracy Activity Reported',
    location: 'Gulf of Aden (Corridor B)',
    severity: 'HIGH',
    timestamp: '12 mins ago',
    coordinates: { lat: 12.5, lng: 45.3 },
    vessel_id: 'MV-TITAN-EXPRESS'
  },
  {
    id: 'EVT-1003',
    event_type: 'Port Congestion & Anchor Delay',
    location: 'Strait of Malacca (Port Singapore)',
    severity: 'MEDIUM',
    timestamp: '35 mins ago',
    coordinates: { lat: 1.35, lng: 103.8 },
    vessel_id: 'MV-PACIFIC-CARRIER'
  },
  {
    id: 'EVT-1004',
    event_type: 'GPS Spoofing / Interference Anomaly',
    location: 'Strait of Hormuz',
    severity: 'HIGH',
    timestamp: '1 hour ago',
    coordinates: { lat: 26.5, lng: 56.4 },
    vessel_id: 'MV-NEPTUNE-VOYAGER'
  },
  {
    id: 'EVT-1005',
    event_type: 'Routine Weather Clearing',
    location: 'South China Sea',
    severity: 'LOW',
    timestamp: '2 hours ago',
    coordinates: { lat: 12.0, lng: 114.0 },
    vessel_id: 'MV-EASTERN-HORIZON'
  }
];

/**
 * Fetches current telemetry event from backend API or returns mock fallback
 */
export const getEvents = async () => {
  try {
    const res = await fetch(`${BASE_URL}/events`);
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();
    return Array.isArray(data) ? data.map(createEvent) : [createEvent(data)];
  } catch (err) {
    console.warn('Backend offline or unreachable for getEvents, using simulation feed.');
    return MOCK_EVENTS_HISTORY.map(createEvent);
  }
};

/**
 * Fetches expanded event history for the Event Monitor page
 */
export const getEventHistory = async () => {
  try {
    const res = await fetch(`${BASE_URL}/dashboard`);
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();
    if (data.recent_events && data.recent_events.length > 0) {
      return data.recent_events.map(createEvent);
    }
    return MOCK_EVENTS_HISTORY.map(createEvent);
  } catch (err) {
    console.warn('Backend offline for getEventHistory, using simulation history.');
    return MOCK_EVENTS_HISTORY.map(createEvent);
  }
};
