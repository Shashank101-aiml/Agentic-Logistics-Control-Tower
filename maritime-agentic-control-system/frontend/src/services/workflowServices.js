const BASE_URL = 'http://localhost:8000/api';

const MOCK_AGENTS_LIST = [
  { agent_name: 'Coordinator Agent', role: 'Master Workflow Orchestrator', status: 'ONLINE', last_active: 'Just now' },
  { agent_name: 'Ingestion Agent', role: 'Telemetry & Weather Stream Collector', status: 'ONLINE', last_active: 'Just now' },
  { agent_name: 'Risk Assessment Agent', role: 'Navigational Hazard Evaluator', status: 'ONLINE', last_active: 'Just now' },
  { agent_name: 'Route Optimization Agent', role: 'Dynamic Waypoint & Corridor Planner', status: 'ONLINE', last_active: 'Just now' },
  { agent_name: 'Explanation Agent', role: 'Decision Transparency & NLP Synthesizer', status: 'ONLINE', last_active: 'Just now' }
];

const MOCK_WORKFLOW_RESULT = {
  status: 'SUCCESS',
  event: {
    event_type: 'Severe Storm Cell & High Swell',
    location: 'Arabian Sea (Sector 4B)',
    severity: 'HIGH'
  },
  risk_score: 68,
  route: {
    route: 'Corridor Beta (Southern Bypass)',
    reason: 'Avoids severe cyclonic weather system by shifting waypoints 120 nm south.'
  },
  explanation: 'The Ingestion Agent detected an intense cyclonic storm cell in Sector 4B. The Risk Assessment Agent evaluated fleet vulnerability at a critical score of 68/100. Consequently, the Route Optimization Agent generated a dynamic corridor shift to Corridor Beta, saving 15 tons of fuel while ensuring vessel and crew safety.'
};

/**
 * Triggers the LangGraph multi-agent collaborative workflow
 */
export const executeWorkflow = async () => {
  try {
    const res = await fetch(`${BASE_URL}/run-workflow`);
    if (!res.ok) throw new Error('Network error');
    return await res.json();
  } catch (err) {
    console.warn('Backend offline for executeWorkflow, simulating multi-agent LangGraph execution.');
    await new Promise(resolve => setTimeout(resolve, 1200)); // simulate AI processing delay
    return MOCK_WORKFLOW_RESULT;
  }
};

/**
 * Fetches active AI agent status list
 */
export const getAgentStatus = async () => {
  try {
    const res = await fetch(`${BASE_URL}/agents`);
    if (!res.ok) throw new Error('Network error');
    return await res.json();
  } catch (err) {
    console.warn('Backend offline for getAgentStatus, using simulation agents list.');
    return MOCK_AGENTS_LIST;
  }
};
