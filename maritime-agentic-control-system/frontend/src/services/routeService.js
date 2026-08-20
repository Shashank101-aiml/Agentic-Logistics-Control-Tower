import { createRecommendation } from '../types/Recommendation';

const BASE_URL = 'http://localhost:8000/api';

const MOCK_CORRIDORS = [
  {
    id: 'COR-ALPHA',
    name: 'Corridor Alpha (Direct Route)',
    distance: '3,450 nm',
    estTime: '9.2 days',
    fuelConsumption: '420 tons',
    riskScore: 75,
    status: 'HIGH HAZARD',
    reason: 'Intersects active storm cell in Arabian Sea and piracy risk zone.',
    recommended: false
  },
  {
    id: 'COR-BETA',
    name: 'Corridor Beta (Southern Bypass) ⭐ AI RECOMMENDED',
    distance: '3,620 nm (+170 nm)',
    estTime: '9.5 days',
    fuelConsumption: '405 tons (-15 tons fuel save via favorable currents)',
    riskScore: 22,
    status: 'OPTIMAL SAFE',
    reason: 'Dynamic waypoint detour avoiding storm center by 120 nm. Favorable ocean swells reduce engine load.',
    recommended: true
  },
  {
    id: 'COR-GAMMA',
    name: 'Corridor Gamma (Coastal Transit)',
    distance: '3,890 nm (+440 nm)',
    estTime: '10.4 days',
    fuelConsumption: '480 tons',
    riskScore: 45,
    status: 'SUB-OPTIMAL',
    reason: 'Safe from deep-water weather but introduces severe port congestion delays near Malacca.',
    recommended: false
  }
];

/**
 * Fetches AI route recommendations from backend API
 */
export const getRecommendations = async () => {
  try {
    const res = await fetch(`${BASE_URL}/recommendations`);
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();
    return createRecommendation(data);
  } catch (err) {
    console.warn('Backend offline for getRecommendations, using simulation recommendation.');
    return createRecommendation({
      status: 'SUCCESS',
      timestamp: new Date().toLocaleTimeString() + ' UTC',
      action_required: true,
      primary_recommendation: 'Autonomous LangGraph coordination recommends immediate detour to Corridor Beta to evade severe storm cells in Arabian Sea.',
      suggested_route: { route: 'Corridor Beta (Southern Bypass)', reason: 'Avoids 4-meter swells and reduces fuel consumption by 15 tons via favorable currents.' },
      assessed_risk: 22
    });
  }
};

/**
 * Returns comparative corridor options for the Route Recommendations page
 */
export const getCorridorOptions = async () => {
  try {
    const rec = await getRecommendations();
    return {
      primary: rec,
      corridors: MOCK_CORRIDORS
    };
  } catch (err) {
    return {
      primary: createRecommendation(),
      corridors: MOCK_CORRIDORS
    };
  }
};
