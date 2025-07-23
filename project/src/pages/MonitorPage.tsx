import React, { useState, useRef, useEffect } from 'react';
import {
  Play,
  Square,
  RefreshCw,
  FileText,
  AlertTriangle,
  CheckCircle,
  Activity,
  Container,
  GitBranch,
  Pause,
  Terminal,
  Trash2
} from 'lucide-react';

import { useMonitoring } from '../hooks/useMonitoring';
import { FileCard } from '../components/FileCard';
import { StatsCard } from '../components/StatsCard';
import { SystemHealth } from '../components/SystemHealth';
import { Breadcrumbs } from '../components/Breadcrumbs';

import { startMonitor, stopMonitor, createLogStream } from '../api/monitoring';

export const MonitorPage: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [showTerminal, setShowTerminal] = useState(false);
  const [terminalContent, setTerminalContent] = useState<string[]>([]);
  const logStreamRef = useRef<EventSource | null>(null);
  const currentPage = "monitor";

  const {
    data,
    loading,
    triggerFix
  } = useMonitoring(isMonitoring ? 3000 : 0); // Poll only when monitoring

  console.log("Here: ", data)
  // Priority map for sorting
  const priority: Record<string, number> = {
    detected: 1,
    fixing: 2,
    critical: 3,
    warning: 4,
    healthy: 5,
    fixed: 6,
    unknown: 7,
    resolved: 8,
  };

  // Start monitoring: call API, open SSE log stream
  const handleStartMonitor = async () => {
    try {
      await startMonitor();
      setIsMonitoring(true);
      setShowTerminal(true);

      // Clear terminal before streaming new logs
      setTerminalContent([]);

      // Open SSE stream for logs
      logStreamRef.current = createLogStream('monitor', (log) => {
        setTerminalContent(prev => [...prev, log]);
      });
    } catch (err) {
      console.error('Failed to start monitor:', err);
    }
  };

  // Stop monitoring: call API, close SSE log stream
  const handleStopMonitor = async () => {
    try {
      await stopMonitor();
      setIsMonitoring(false);

      // Close SSE stream if open
      if (logStreamRef.current) {
        logStreamRef.current.close();
        logStreamRef.current = null;
      }

      setTerminalContent(prev => [
        ...prev,
        '',
        '[MONITOR STOPPED] Refer to the cards below in the CI/CD Pipeline Components section for detailed information.',
        ''
      ]);
    } catch (err) {
      console.error('Failed to stop monitor:', err);
    }
  };

  // Clear terminal and close stream if open
  const handleClearTerminal = async () => {
    setTerminalContent([]);
    await stopMonitor();
    setIsMonitoring(false);
    setShowTerminal(false);

    if (logStreamRef.current) {
      logStreamRef.current.close();
      logStreamRef.current = null;
    }
  };

  // Trigger a fix via your hook
  const handleTriggerFix = async (filePath: string, errorIndex: number) => {
    const success = await triggerFix(filePath, errorIndex);
    if (success) {
      console.log(`Fix triggered for ${filePath}, error ${errorIndex}`);
    } else {
      console.error(`Failed to trigger fix for ${filePath}`);
    }
  };

  // Clean up SSE on component unmount
  useEffect(() => {
    return () => {
      if (logStreamRef.current) {
        logStreamRef.current.close();
        logStreamRef.current = null;
      }
    };
  }, []);



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

      {/* Monitor Control Section */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center">
            <Terminal className="h-5 w-5 mr-2 text-green-400" />
            Monitor Control
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

        {/* Terminal Window */}
        {showTerminal && (
          <div className="bg-black rounded-lg border border-gray-600 overflow-hidden resize-y min-h-[200px] max-h-[80vh] mt-3">
            {/* Terminal Header */}
            <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-600 cursor-default">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-gray-300 text-sm ml-2">CI/CD Monitor Terminal</span>
              </div>
            </div>

            {/* Terminal Content (scrollable inside) */}
            <div
              className="p-4 font-mono text-sm overflow-y-auto"
              style={{ height: 'calc(100% - 40px)' }} // subtract header height (40px)
              ref={(el) => {
                if (el) el.scrollTop = el.scrollHeight;
              }}
            >
              {terminalContent.length === 0 ? (
                <div className="text-green-400">
                  $ Starting CI/CD monitoring system...
                  <br />
                  $ Initializing log stream...
                  <br />
                  <span className="animate-pulse">$ Waiting for log entries...</span>
                </div>
              ) : (
                <div className="space-y-1">
                  {(() => {
                    const elements: JSX.Element[] = [];
                    let insideCodeBlock = false;
                    let codeBlockLang = '';
                    let codeLines: string[] = [];

                    terminalContent.forEach((line, index) => {
                      if (line.trim().startsWith('```')) {
                        if (!insideCodeBlock) {
                          insideCodeBlock = true;
                          codeBlockLang = line.trim().slice(3).trim();
                          codeLines = [];
                        } else {
                          insideCodeBlock = false;
                          elements.push(
                            <pre
                              key={`code-${index}`}
                              className="bg-gray-900 text-green-300 text-sm p-3 rounded-md overflow-x-auto"
                            >
                              <code className={`language-${codeBlockLang}`}>
                                {codeLines.join('\n')}
                              </code>
                            </pre>
                          );
                        }
                      } else if (insideCodeBlock) {
                        codeLines.push(line.replace(/^OUT:\s?/, ''));
                      } else {
                        const content = line.replace(/^OUT:\s?/, '');
                        let colorClass = 'text-gray-300';
                        if (line.includes('ERROR')) colorClass = 'text-red-400';
                        else if (line.includes('WARN')) colorClass = 'text-yellow-400';
                        else if (line.includes('SUCCESS')) colorClass = 'text-green-400';
                        else if (line.includes('MONITOR STOPPED')) colorClass = 'text-cyan-400 font-bold';

                        elements.push(
                          <div key={index} className={colorClass}>
                            {content}
                          </div>
                        );
                      }
                    });

                    if (isMonitoring) {
                      elements.push(
                        <div key="active-monitor" className="text-green-400 animate-pulse">
                          $ Monitoring active...
                        </div>
                      );
                    }

                    return elements;
                  })()}
                </div>
              )}
            </div>
          </div>
        )}



      </div>

      {loading && !data ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center space-x-3 text-cyan-300">
            <RefreshCw className="h-6 w-6 animate-spin" />
            <span className="text-lg">Loading CI/CD monitoring data...</span>
          </div>
        </div>
      ) : data ? (
        <>
          {/* System Health */}
          <SystemHealth
            metrics={data.metrics}
            systemHealth={data.system_health}
            agentStatus={data.agent_status}
            pipelineStatus={data.pipeline_status}
          />

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              title="Pipeline Files Monitored"
              value={data.total_files}
              icon={FileText}
              color="bg-blue-500/20 text-blue-400"
              subtitle="Docker, K8s, CI/CD configs"
            />
            <StatsCard
              title="Critical Pipeline Issues"
              value={data.critical_issues}
              icon={AlertTriangle}
              color="bg-red-500/20 text-red-400"
              subtitle="Blocking deployments"
            />
            <StatsCard
              title="Healthy Components"
              value={data.total_files - data.files_with_errors}
              icon={CheckCircle}
              color="bg-green-500/20 text-green-400"
              subtitle="Ready for deployment"
            />
            <StatsCard
              title="Docker Containers"
              value={data.metrics.docker_containers_running}
              icon={Container}
              color="bg-cyan-500/20 text-cyan-400"
              subtitle="Currently running"
            />
          </div>

          {/* Files List */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white">CI/CD Pipeline Components</h2>
                <p className="text-gray-400 text-sm mt-1">
                  Real-time monitoring of {data.files.length} pipeline configuration files
                </p>
              </div>
            </div>

            {data.files.length === 0 ? (
              <div className="text-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
                <GitBranch className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                <p className="text-gray-400">No pipeline components are currently being monitored</p>
                <p className="text-gray-500 text-sm mt-2">
                  Configure your CI/CD monitoring to start tracking pipeline health
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {data.files
                  .sort((a, b) => {
                    return (priority[a.status] ?? 99) - (priority[b.status] ?? 99);
                  })
                  .map((file, index) => (
                    <FileCard
                      key={`file-${index}`}
                      file={file}
                      onTriggerFix={handleTriggerFix}
                    />
                  ))}
              </div>
            )}
          </div>
        </>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-400">No monitoring data available</p>
          <button
            onClick={handleStartMonitor}
            className="mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
          >
            Start Monitoring
          </button>
        </div>
      )}
    </div>
  );
};
