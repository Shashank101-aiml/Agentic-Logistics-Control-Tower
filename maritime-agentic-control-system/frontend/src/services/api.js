const BASE_URL = 'http://localhost:8000/api';

export const fetchDashboard = async () => {
  const res = await fetch(`${BASE_URL}/dashboard`);
  if (!res.ok) throw new Error('Failed to fetch dashboard');
  return res.json();
};

export const fetchEvents = async () => {
  const res = await fetch(`${BASE_URL}/events`);
  if (!res.ok) throw new Error('Failed to fetch events');
  return res.json();
};

export const fetchRisks = async () => {
  const res = await fetch(`${BASE_URL}/risks`);
  if (!res.ok) throw new Error('Failed to fetch risks');
  return res.json();
};

export const runWorkflow = async () => {
  const event = {
    event_type: "weather",
    severity: "high",
    description: "Severe weather detected",
    weather_severity: 0.8,
    congestion_score: 0.4,
    incident_score: 0.2,
    delay_hours: 24
  };

  const route = {
    origin: "SGSIN",
    destination: "NLRTM",
    status: "planned",
    distance_nm: 7950,
    estimated_cost_usd: 2440000,
    delay_hours: 236
  };

  const res = await fetch(
    `${BASE_URL}/intelligence/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event,
        route
      })
    }
  );

  if (!res.ok) {
    throw new Error("Failed to run workflow");
  }

  return res.json();
};

export const fetchAgents = async () => {
  const res = await fetch(`${BASE_URL}/agents`);
  if (!res.ok) throw new Error('Failed to fetch agents');
  return res.json();
};

export const fetchRecommendations = async () => {
  const res = await fetch(`${BASE_URL}/recommendations`);
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
};
