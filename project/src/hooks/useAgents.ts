import { useState, useEffect, useCallback } from 'react';
import { Agent } from '../types/monitoring';
import { dummyAgents } from '../data/dummyData';

export const useAgents = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAgents = useCallback(async () => {
    try {
      setError(null);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 400));
      
      // Add some randomness to CPU/Memory usage for realism
      const updatedAgents = dummyAgents.map(agent => ({
        ...agent,
        cpu_usage: agent.status === 'online' || agent.status === 'busy' 
          ? Math.max(0, agent.cpu_usage + Math.floor(Math.random() * 10) - 5)
          : 0,
        memory_usage: agent.status === 'online' || agent.status === 'busy'
          ? Math.max(0, Math.min(100, agent.memory_usage + Math.floor(Math.random() * 6) - 3))
          : 0,
        last_heartbeat: agent.status === 'online' || agent.status === 'busy'
          ? new Date().toISOString()
          : agent.last_heartbeat
      }));
      
      setAgents(updatedAgents);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch agents';
      setError(errorMessage);
      console.error('Agents API Error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const restartAgent = useCallback(async (agentId: string) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setAgents(prev => prev.map(agent => 
        agent.id === agentId 
          ? { 
              ...agent, 
              status: 'online' as any,
              health: 'healthy' as any,
              last_heartbeat: new Date().toISOString(),
              uptime: Math.min(100, agent.uptime + 1)
            }
          : agent
      ));
      
      return true;
    } catch (err) {
      console.error('Restart agent failed:', err);
      return false;
    }
  }, []);

  const stopAgent = useCallback(async (agentId: string) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAgents(prev => prev.map(agent => 
        agent.id === agentId 
          ? { 
              ...agent, 
              status: 'offline' as any,
              cpu_usage: 0,
              memory_usage: 0,
              current_task: undefined,
              queue_size: 0
            }
          : agent
      ));
      
      return true;
    } catch (err) {
      console.error('Stop agent failed:', err);
      return false;
    }
  }, []);

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, [fetchAgents]);

  return {
    agents,
    loading,
    error,
    refetch: fetchAgents,
    restartAgent,
    stopAgent
  };
};