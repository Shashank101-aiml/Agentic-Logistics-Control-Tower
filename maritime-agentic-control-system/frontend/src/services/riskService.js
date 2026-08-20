import { createRiskAssessment } from '../types/Risk';

const BASE_URL = 'http://localhost:8000/api';

const MOCK_RISK_ASSESSMENT = {
  risk_score: 68,
  category: 'Severe Weather & Piracy Convergence',
  impact: 'HIGH',
  likelihood: 'HIGH',
  mitigation_plan: 'Activate autonomous waypoint adjustment via Southern Maritime Corridor. Increase vessel speed by 3 knots and enforce anti-piracy protocol level 2.',
  status: 'ACTION REQUIRED'
};

const MOCK_RISK_TRENDS = [
  { time: '00:00', score: 32, label: 'Normal Navigation' },
  { time: '04:00', score: 38, label: 'Minor Squall' },
  { time: '08:00', score: 45, label: 'Swell Building' },
  { time: '12:00', score: 55, label: 'Storm Approach' },
  { time: '16:00', score: 68, label: 'Hazard Warning' },
  { time: '20:00', score: 62, label: 'Rerouted (Mitigating)' },
  { time: '24:00', score: 40, label: 'Clear Waters' }
];

/**
 * Fetches current risk score from backend API
 */
export const getRisks = async () => {
  try {
    const res = await fetch(`${BASE_URL}/risks`);
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();
    return createRiskAssessment(data);
  } catch (err) {
    console.warn('Backend offline for getRisks, using simulation assessment.');
    return createRiskAssessment(MOCK_RISK_ASSESSMENT);
  }
};

/**
 * Fetches comprehensive risk assessment and trend history
 */
export const getFleetRiskAssessment = async () => {
  try {
    const [riskData, dashboardData] = await Promise.all([
      fetch(`${BASE_URL}/risks`).then(r => r.ok ? r.json() : null),
      fetch(`${BASE_URL}/dashboard`).then(r => r.ok ? r.json() : null)
    ]);

    const score = riskData?.risk_score ?? dashboardData?.average_fleet_risk ?? MOCK_RISK_ASSESSMENT.risk_score;
    
    return {
      currentRisk: createRiskAssessment({ risk_score: score }),
      trends: MOCK_RISK_TRENDS,
      fleetSummary: {
        totalVessels: dashboardData?.active_vessels ?? 42,
        vesselsAtRisk: score > 50 ? 6 : 1,
        activeAlerts: dashboardData?.active_alerts ?? (score > 50 ? 3 : 1)
      }
    };
  } catch (err) {
    console.warn('Backend offline for getFleetRiskAssessment, using simulation trends.');
    return {
      currentRisk: createRiskAssessment(MOCK_RISK_ASSESSMENT),
      trends: MOCK_RISK_TRENDS,
      fleetSummary: { totalVessels: 42, vesselsAtRisk: 6, activeAlerts: 3 }
    };
  }
};
