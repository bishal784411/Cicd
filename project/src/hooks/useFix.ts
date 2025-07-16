import { useState, useEffect, useCallback } from 'react';
import { getAllFixData } from '../api/fix';
import { FileStatusFix, FixEntry, FixMonitorData } from '../types/monitoring';

export const useFix = (pollInterval: number = 3000) => {
  const [data, setData] = useState<FixMonitorData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('connected');

  const triggerFix = async (filePath: string, errorIndex: number): Promise<boolean> => {
    try {
      console.log(`Triggering fix for ${filePath} at index ${errorIndex}`);
      // TODO: connect to backend fix trigger if needed
      return true;
    } catch (e) {
      console.error('Fix trigger failed:', e);
      return false;
    }
  };

  const fetchFixData = useCallback(async () => {
    try {
      setError(null);
      setConnectionStatus('reconnecting');

      const response = await getAllFixData();

      const allFixEntries: FixEntry[] = (response.fixes ?? []).map((entry: any) => ({
        fix_id: entry.fix_id,
        solution_id: entry.solution_id,
        err_id: entry.err_id,
        timestamp: entry.timestamp,
        file: entry.file,
        language: entry.language,
        status: entry.status,
        fix_applied: entry.status === 'applied',
        applied_at: entry.applied_at,
        auto_fixable: true,
        commit_hash: 'abc123', // temp
        branch: 'main',        // temp
        errors: entry.errors,
        ai_analysis: Array.isArray(entry.ai_analysis)
          ? entry.ai_analysis.map((a: any) => ({
              decision: a.decision,
              risk_level: a.risk_level,
              confidence: a.confidence,
              reasoning: a.reasoning,
              safety_notes: a.safety_notes,
              related_error: a.related_error,
            }))
          : [],
        error_type: entry.error_type,
        recommendations: entry.recommendations,
        isPushed: entry.isPushed,
        error_push: entry.error_push,
      }));

      const groupedByFile: Record<string, FileStatusFix> = {};

      for (const fix of allFixEntries) {
        if (!groupedByFile[fix.file]) {
          groupedByFile[fix.file] = {
            file: fix.file,
            status: fix.status,
            build_status: 'success',
            uptime_percentage: 99,
            last_checked: fix.timestamp,
            last_fix_attempt: fix.applied_at,
            pipeline_stage: 'build',
            error_count: 0,
            critical_count: 0,
            errors: [],
            fixes: [],
          };
        }

        groupedByFile[fix.file].errors.push(fix);
        groupedByFile[fix.file].error_count += 1;

        if (
          fix.ai_analysis?.some((a) => a.risk_level === 'critical')
        ) {
          groupedByFile[fix.file].critical_count! += 1;
        }
      }

      const fileList = Object.values(groupedByFile);

      setData({
        total_files: fileList.length,
        files_with_errors: fileList.filter(f => f.error_count > 0).length,
        critical_issues: fileList.filter(f => f.status === 'critical').length,
        metrics: {
          docker_containers_running: 4,
        },
        system_health: 'Healthy',
        agent_status: 'Running',
        pipeline_status: 'Stable',
        files: fileList
      });

      setLastRefresh(new Date());
      setConnectionStatus('connected');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to connect to fix service';
      setError(errorMessage);
      setConnectionStatus('disconnected');
      console.error('❌ Fix API Error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFixData();
    // const interval = setInterval(fetchFixData, pollInterval);
    // return () => clearInterval(interval);
  }, [fetchFixData, pollInterval]);

  return {
    data,
    loading,
    error,
    lastRefresh,
    connectionStatus,
    manualRefresh: fetchFixData,
    triggerFix,
  };
};
