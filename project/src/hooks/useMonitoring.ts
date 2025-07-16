import { useState, useEffect, useCallback } from 'react';
import { MonitoringData } from '../types/monitoring';
import { getLatestMonitoringData } from '../api/monitoring';

export const useMonitoring = (pollInterval: number = 3000) => {
  const [data, setData] = useState<MonitoringData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('connected');

  const fetchMonitoringData = useCallback(async () => {
    try {
      setError(null);
      setConnectionStatus('reconnecting');

      const response = await getLatestMonitoringData();

      // console.log("Here: ", response)

      // Normalize response: treat as array whether it's a single object or a list
      const errorEntries = Array.isArray(response?.errors)
        ? response.errors
        : Array.isArray(response)
        ? response
        : [response]; // fallback: wrap single object

      

      const transformedFiles = errorEntries.map((entry: any) => ({
        file: entry.file,
        status: entry.status ?? 'detected',
        last_checked: entry.last_checked ?? new Date().toISOString(),
        error_count: entry.errors?.length ?? 0,
        build_status: 'success',
        uptime_percentage: 92,
        last_fix_attempt: undefined,
        pipeline_stage: entry.pipeline_stage,
        errors: (entry.errors ?? []).map((msg: string, idx: number) => ({
          key: `${entry.err_id}-${idx}`, 
          err_id: entry.err_id,
          timestamp: entry.timestamp,
          file: entry.file,
          error_type: entry.error_type,
          line_number: undefined,
          message: msg,
          ai_analysis: entry.ai_analysis?.[idx]?.analysis ?? '',
          severity: entry.severity,
          fix_suggestion: entry.fix_solution?.[idx]?.correction ?? '',
          auto_fixable: true,
          fix_applied: false,
          fix_timestamp: undefined,
          pipeline_stage: entry.pipeline_stage,
          commit_hash: entry.commit_hash,
          branch: entry.branch,
        })),
      }));


      const transformed: MonitoringData = {
        last_updated: new Date().toISOString(),
        total_files: transformedFiles.length,
        files_with_errors: transformedFiles.length,
        critical_issues: transformedFiles.filter((f: { status: string; }) => f.status === 'critical').length,
        metrics: {
          cpu_usage: Math.floor(Math.random() * 30) + 50,
          memory_usage: Math.floor(Math.random() * 20) + 70,
          network_latency: Math.floor(Math.random() * 20) + 15,
          docker_containers_running: Math.floor(Math.random() * 5) + 1,
          disk_usage: 0,
          active_pipelines: 0,
          successful_deployments_today: 0,
          failed_builds_today: 0
        },
        pipeline_status: 'success',
        system_health: 'healthy',
        agent_status: 'active',
        files: transformedFiles,
        // total_solutions: ''
      };

      setData(transformed);
      setLastRefresh(new Date());
      setConnectionStatus('connected');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to connect to monitoring service';
      setError(errorMessage);
      setConnectionStatus('disconnected');
      console.error('❌ Monitoring API Error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const manualRefresh = useCallback(async () => {
    setLoading(true);
    await fetchMonitoringData();
  }, [fetchMonitoringData]);

  const triggerFix = useCallback(async (filePath: string, errorIndex: number) => {
    try {
      console.log(`Triggering fix for ${filePath}, error ${errorIndex}`);
      await new Promise(resolve => setTimeout(resolve, 1000));

      if (data) {
        const updatedData = { ...data };
        const fileIndex = updatedData.files.findIndex(f => f.file === filePath);
        if (fileIndex !== -1 && updatedData.files[fileIndex].errors[errorIndex]) {
          updatedData.files[fileIndex].errors[errorIndex].fix_applied = true;
          updatedData.files[fileIndex].errors[errorIndex].fix_timestamp = new Date().toISOString();
          updatedData.files[fileIndex].status = 'healthy';
          setData(updatedData);

          setTimeout(() => {
            const finalData = { ...updatedData };
            finalData.files[fileIndex].status = 'healthy';
            setData(finalData);
          }, 3000);
        }
      }

      return true;
    } catch (err) {
      console.error('Fix request failed:', err);
      return false;
    }
  }, [data]);

  useEffect(() => {
    fetchMonitoringData();
    // const interval = setInterval(fetchMonitoringData, pollInterval);
    // return () => clearInterval(interval);
  }, [fetchMonitoringData, pollInterval]);

  return {
    data,
    loading,
    error,
    lastRefresh,
    connectionStatus,
    manualRefresh,
    triggerFix
  };
};
