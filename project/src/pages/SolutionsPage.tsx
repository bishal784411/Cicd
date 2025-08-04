import React, { useEffect, useRef, useState } from 'react';
import {
  Play,
  Square,
  RefreshCw,
  AlertTriangle,
  Activity,
  GitBranch,
  Terminal,
  Pause,
  Trash2,
} from 'lucide-react';
import { useSolutions } from '../hooks/useSolutions';
import { FileCard } from '../components/SolutionFileCard';
import { SystemHealth } from '../components/SystemHealth';
import { SolutionStatus } from '../types/monitoring';
import { Breadcrumbs } from '../components/Breadcrumbs';
import { startSolution, stopSolution, createLogStream } from '../api/solution';
import { useTerminal } from '../components/TerminalContext';
import { GlobalTerminal } from '../components/GlobalTerminal';


interface Metrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_pipelines: number;
  docker_containers_running: number;
  successful_deployments_today: number;
  failed_builds_today: number;
}


export const SolutionsPage: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const {
    isOpen: showTerminal,
    openTerminal,
    closeTerminal,
    clearTerminal,
    appendLog,
  } = useTerminal();

  const logStreamRef = useRef<EventSource | null>(null);
  const currentPage = "solutions";

  const {
    files,
    loading,
    error,
    refetch,
  } = useSolutions();

  const [metrics, setMetrics] = useState<Metrics>({
      cpu_usage: 0,
      memory_usage: 0,
      disk_usage: 0,
      active_pipelines: 8,
      docker_containers_running: 24,
      successful_deployments_today: 12,
      failed_builds_today: 3,
    });


    useEffect(() => {
    const eventSource = new EventSource(`${import.meta.env.VITE_API_BASE_URL}/system/usages`);

    eventSource.onmessage = (event) => {
      try {
        let raw = event.data.trim();
        if (raw.startsWith("data: ")) raw = raw.slice(6);
        const fixed = raw.replace(/'/g, '"');
        const data = JSON.parse(fixed);

        setMetrics((prev) => ({
          ...prev,
          cpu_usage: data.cpu_percent,
          memory_usage: data.memory_percent,
          disk_usage: data.disk_percent,
          active_pipelines: prev.active_pipelines,
          docker_containers_running: prev.docker_containers_running,
          successful_deployments_today: prev.successful_deployments_today,
          failed_builds_today: prev.failed_builds_today,
        }));

      } catch (err) {
        console.error("Error parsing SSE data:", err, event.data);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE connection error:", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const handleStartMonitor = async () => {
    try {
      await startSolution();
      setIsMonitoring(true);
      openTerminal();
      clearTerminal();

      logStreamRef.current = createLogStream('solution', (log) => {
        appendLog(log);
      });
    } catch (err) {
      console.error('Failed to start monitor:', err);
    }
  };


  const handleStopMonitor = async () => {
    try {
      await stopSolution();
      setIsMonitoring(false);

      if (logStreamRef.current) {
        logStreamRef.current.close();
        logStreamRef.current = null;
      }

      appendLog('');
      appendLog('[MONITOR STOPPED] Refer to the cards below in the CI/CD Pipeline Components section for detailed information.');
      appendLog('');
    } catch (err) {
      console.error('Failed to stop monitor:', err);
    }
  };


  // Clear terminal and close stream if open
  const handleClearTerminal = async () => {
    clearTerminal();
    await stopSolution();
    setIsMonitoring(false);
    closeTerminal();

    if (logStreamRef.current) {
      logStreamRef.current.close();
      logStreamRef.current = null;
    }
  };
  useEffect(() => {
    return () => {
      if (logStreamRef.current) {
        logStreamRef.current.close();
        logStreamRef.current = null;
      }
    };
  }, []);

  const handleExecuteSolution = (solutionId: string) => {
    console.log(`Execute solution with ID: ${solutionId}`);
  };

  if (error) {
    return (
      <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-2">
          <AlertTriangle className="h-5 w-5 text-red-400" />
          <span className="text-red-300 font-medium">Solution Monitor Error</span>
        </div>
        <p className="text-red-200">{error}</p>
        <button
          onClick={refetch}
          className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  const dataToRender: {
    metrics: any;
    system_health: "healthy" | "degraded" | "critical";
    agent_status: "active" | "error" | "idle" | "maintenance";
    pipeline_status: "success" | "running" | "idle" | "failed";
    files: SolutionStatus[];
  } = {
    metrics: {},
    system_health: "healthy",
    agent_status: "active",
    pipeline_status: "running",
    files: files.length > 0 ? files : [],
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-row justify-between">
        <Breadcrumbs currentPage={currentPage} parentPage="dashboard" />

        <div className="flex items-center space-x-3">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${isMonitoring
            ? 'bg-green-500/20 text-green-400'
            : 'bg-gray-500/20 text-gray-400'
            }`}>
            <Activity className={`h-4 w-4 inline mr-2 ${isMonitoring ? 'animate-pulse' : ''}`} />
            {isMonitoring ? 'MONITORING' : 'STOPPED'}
          </div>
        </div>
      </div>


      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center">
            <Terminal className="h-5 w-5 mr-2 text-green-400" />
            Solution Control
          </h3>
          <div className="flex items-center space-x-3">
            {!isMonitoring ? (
              <button
                onClick={handleStartMonitor}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              >
                <Play className="h-4 w-4" />
                <span>Start Monitor</span>
              </button>
            ) : (
              <button
                onClick={handleStopMonitor}
                className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              >
                <Square className="h-4 w-4" />
                <span>Stop Monitor</span>
              </button>
            )}

            {showTerminal && (
              <button
                onClick={handleClearTerminal}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
              >
                <Trash2 className="h-4 w-4" />
                <span>Close Terminal</span>
              </button>
            )}
          </div>
        </div>

        {!isMonitoring && !showTerminal && (
          <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-xl p-4">
            <div className="flex items-center space-x-2">
              <Pause className="h-5 w-5 text-yellow-400" />
              <span className="text-yellow-300 font-medium">Monitoring Paused</span>
            </div>
            <p className="text-yellow-200 mt-1">
              Click ‘Start Monitor’ to initiate monitoring of your workflow.
            </p>
          </div>
        )}

        {showTerminal && <GlobalTerminal />}

      </div>

      {loading && files.length === 0 ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center space-x-3 text-cyan-300">
            <RefreshCw className="h-6 w-6 animate-spin" />
            <span className="text-lg">Loading AI-generated solutions...</span>
          </div>
        </div>
      ) : files.length === 0 ? (
        <div className="text-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
          <GitBranch className="h-12 w-12 text-gray-500 mx-auto mb-4" />
          <p className="text-gray-400">No solutions available yet</p>
          <p className="text-gray-500 text-sm mt-2">Wait for the monitoring agent to detect issues and generate fixes.</p>
        </div>
      ) : (
        <>
          <SystemHealth
            metrics={metrics}
            systemHealth={dataToRender.system_health}
            agentStatus={dataToRender.agent_status}
            pipelineStatus={dataToRender.pipeline_status}
          />
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white">AI-Generated Fixes</h2>
                <p className="text-gray-400 text-sm mt-1">
                  Suggested improvements for {files.length} monitored file{files.length !== 1 ? 's' : ''}
                </p>
              </div>
            </div>

            <div className="space-y-3">
              {files.map((file, index) => (
                <FileCard
                  key={`solution-file-${index}`}
                  file={file}
                  onTriggerFix={handleExecuteSolution}
                />
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};


