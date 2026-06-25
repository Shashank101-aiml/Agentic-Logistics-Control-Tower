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
  const res = await fetch(`${BASE_URL}/run-workflow`);
  if (!res.ok) throw new Error('Failed to run workflow');
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
