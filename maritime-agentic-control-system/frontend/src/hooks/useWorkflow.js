import { useState, useEffect, useCallback } from 'react';
<<<<<<< HEAD
import {
  executeWorkflow,
  getAgentStatus
} from '../services/workflowServices';

/**
 * Custom hook for coordinating the multi-agent workflow
=======
import { executeWorkflow, getAgentStatus } from '../services/workflowServices';

/**
 * Custom hook for coordinating the multi-agent LangGraph pipeline
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
 */
export const useWorkflow = () => {
  const [agents, setAgents] = useState([]);
  const [workflowRes, setWorkflowRes] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [loadingAgents, setLoadingAgents] = useState(true);
  const [error, setError] = useState(null);

  const loadAgents = useCallback(async () => {
    setLoadingAgents(true);
<<<<<<< HEAD

=======
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    try {
      const data = await getAgentStatus();
      setAgents(data);
    } catch (err) {
      setError('Failed to load agent fleet status.');
    } finally {
      setLoadingAgents(false);
    }
  }, []);

  useEffect(() => {
    loadAgents();
<<<<<<< HEAD

    const interval = setInterval(
      loadAgents,
      20000
    );

    return () => clearInterval(interval);
  }, [loadAgents]);

  const runPipeline = async (
    event,
    route
  ) => {
    setExecuting(true);
    setError(null);

    try {
      const res = await executeWorkflow(
        event,
        route
      );

      setWorkflowRes(res);

      await loadAgents();

      return res;

    } catch (err) {
      console.error(
        'Workflow execution error:',
        err
      );

      setError(
        err.message ||
        'Multi-agent workflow execution failed.'
      );

      throw err;

=======
    const interval = setInterval(loadAgents, 20000);
    return () => clearInterval(interval);
  }, [loadAgents]);

  const runPipeline = async () => {
    setExecuting(true);
    setError(null);
    try {
      const res = await executeWorkflow();
      setWorkflowRes(res);
      await loadAgents();
      return res;
    } catch (err) {
      setError('Multi-agent workflow execution failed.');
      throw err;
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
    } finally {
      setExecuting(false);
    }
  };

  return {
    agents,
    workflowRes,
    executing,
    loadingAgents,
    error,
    runPipeline,
    refreshAgents: loadAgents
  };
};

<<<<<<< HEAD
export default useWorkflow;
=======
export default useWorkflow;
>>>>>>> 80d16660a52137b15a5dfffa5e213328db0bf64a
