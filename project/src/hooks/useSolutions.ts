import { useState, useEffect, useCallback } from 'react';
import { getLatestSolutionData } from '../api/solution';
import { SolutionStatus } from '../types/monitoring';

export const useSolutions = () => {
  const [files, setFiles] = useState<SolutionStatus[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSolutions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await getLatestSolutionData();

      // Extract the inner Solutions object
      const solutionArray = response?.Solutions;
      if (!Array.isArray(solutionArray)) {
        setFiles([]);
        return;
      }

      // Map API status to your UI statuses
      const mapStatus = (apiStatus: string): SolutionStatus['status'] => {
        switch (apiStatus) {
          case 'pending_review': return 'detected';
          case 'solving': return 'fixing';
          case 'fixed': return 'fixed';
          case 'critical': return 'critical';
          case 'healthy': return 'healthy';
          default: return 'unknown';
        }
      };

      const mapBuildStatus = (apiStatus: string): SolutionStatus['build_status'] => {
        switch (apiStatus) {
          case 'pending_review': return 'pending';
          case 'solving': return 'running';
          case 'fixed': return 'success';
          case 'failed': return 'failed';
          default: return 'pending';
        }
      };

      // Map the API data into your SolutionStatus type
      const mapped = solutionArray.map((solution) => ({
        file: solution.file,
        last_checked: new Date().toISOString(),
        status: mapStatus(solution.status),
        error_count: solution.errors?.length || 0,
        errors: solution.errors || [],
        Solution_Type: solution.Solution_Type,
        pipeline_stage: solution.pipeline_stage,
        build_status: mapBuildStatus(solution.status),
        solutions: (solution.available_solutions || []).map((s: any, index: number) => ({
          id: `${solution.solution_id}-${index}`,
          name: `Fix: ${s.error ?? 'unknown'}`,
          description: s.explanation?.text || s.description || 'No description',
          code: s.explanation?.code_example,
          category: solution.pipeline_stage || 'unknown',
          status: 'active',
          error_types: [solution.error_type || 'Unknown'],
          pipeline_stages: [solution.pipeline_stage],
          created_by: 'AI Engine',
          created_at: new Date().toISOString(),
          last_executed: new Date().toISOString(),
          execution_count: 0,
          success_rate: Math.round((solution.model_confidence ?? 0) * 100),
          avg_execution_time: 1.5,
          auto_trigger: solution.auto_apply ?? false,
        })),
        critical_count: 0,
        last_fix_attempt: null,
        uptime_percentage: 0
      }));

      // setFiles(mapped);

      setFiles(mapped);
    } catch (err) {
      console.error('Error fetching latest solution:', err);
      setError('Failed to fetch latest solution');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSolutions();
    const interval = setInterval(fetchSolutions, 10000);
    return () => clearInterval(interval);
  }, [fetchSolutions]);

  return {
    files,
    loading,
    error,
    refetch: fetchSolutions,
  };
};
