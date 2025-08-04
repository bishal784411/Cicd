import { useEffect, useState, useCallback } from 'react';

export interface SystemStats {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
}

export interface AgentInfo {
  name: string;
  status: string;
  last_heartbeat: string | null;
  uptime: string | null;
  total_detections: number;
  health: string;
  system: SystemStats;
  solutions_provided?: number;
  solutions_pending?: number;
  fixes_applied?: number;
  fixes_pending?: number;
}

export interface SummaryStats {
  total_errors: number;
  total_solutions: number;
  total_fixes: number;
  pending_solutions: number;
  pending_fixes: number;
  online_agents: number;
  tasks_completed: number;
  average_uptime: number | null;
}

export interface CombinedStats {
  timestamp: string;
  agents: {
    monitor: AgentInfo;
    solution: AgentInfo;
    fix: AgentInfo;
  };
  summary: SummaryStats;
}



export const useAgent = () => {
  const [data, setData] = useState<CombinedStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
  const API_EVENT_URL = import.meta.env.VITE_API_BASE_URL;
  useEffect(() => {
    const eventSource = new EventSource(`${API_EVENT_URL}/system/combined-stats`);

    eventSource.onopen = () => {
      setConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsed: CombinedStats = JSON.parse(event.data);

        // Normalize missing fields
        ['monitor', 'solution', 'fix'].forEach((agentKey) => {
          const agent = parsed.agents[agentKey as keyof CombinedStats['agents']];
          if (agent) {
            agent.system = agent.system ?? {
              cpu_percent: 0,
              memory_percent: 0,
              disk_percent: 0,
            };
            agent.health = agent.health ?? 'unknown';
            agent.solutions_provided ??= 0;
            agent.solutions_pending ??= 0;
            agent.fixes_applied ??= 0;
            agent.fixes_pending ??= 0;
          }
        });

        parsed.summary.online_agents ??= 0;
        parsed.summary.tasks_completed ??= 0;
        parsed.summary.average_uptime ??= null;

        setData(parsed);
      } catch (err) {
        console.error('Failed to parse SSE event data:', err);
        setError('Failed to parse data');
      } finally {
        setLoading(false);
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE connection error:', err);
      setError('Connection lost');
      setConnected(false);
      eventSource.close();
      setLoading(false);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const refetch = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(true);
  }, []);

  return {
    data,
    agents: data?.agents ?? null,
    summary: data?.summary ?? null,
    timestamp: data?.timestamp ?? null,
    loading,
    error,
    connected,
    refetch,
  };
};
