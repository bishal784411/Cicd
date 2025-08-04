import React, { useState } from 'react';
import {
  Play,
  Square,
  RefreshCw,
  AlertTriangle,
  Activity,
  Terminal,
  X,
  Trash2,
  Pause,
  GitBranch,
} from 'lucide-react';

import { FixFileCard } from '../components/FixFileCard';
import { useFix } from '../hooks/useFix';
import { FileStatusFix } from '../types/monitoring';
import { createLogStream } from '../api/monitoring';
import { Breadcrumbs } from '../components/Breadcrumbs';
import {  startfix, stopfix } from '../api/fix';


export const FixPage: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [showTerminal, setShowTerminal] = useState(false);
  const [terminalContent, setTerminalContent] = useState<string[]>([]);
  const [eventSource, setEventSource] = useState<EventSource | null>(null);

  const {
    data,
    loading,
    error,
    manualRefresh,
    triggerFix
  } = useFix(isMonitoring ? 3000 : 0);



  const handleStartMonitor = async () => {
    await startfix();
    setIsMonitoring(true);
    setShowTerminal(true);
    manualRefresh();

    const stream = createLogStream('fix', (msg: string) => {
      setTerminalContent(prev => [...prev, msg]);
    });

    setEventSource(stream);
  };

  const handleStopMonitor = async () => {
    await stopfix();
    setIsMonitoring(false);

    if (eventSource) {
      eventSource.close();
      setEventSource(null);
    }

    setTerminalContent(prev => [
      ...prev,
      '',
      '[MONITOR STOPPED] Refer to the cards below in the CI/CD Pipeline Components section for detailed information.',
      ''
    ]);
  };

  

  const handleClearTerminal = () => {
    setTerminalContent([]);
    setShowTerminal(false);

    if (eventSource) {
      eventSource.close();
      setEventSource(null);
    }
  };

  const handleTriggerFix = async (filePath: string, errorIndex: number) => {
    const success = await triggerFix(filePath, errorIndex);
    console[success ? 'log' : 'error'](`Fix ${success ? 'triggered' : 'failed'} for ${filePath}`);
  };

  if (error) {
    return (
      <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-2">
          <AlertTriangle className="h-5 w-5 text-red-400" />
          <span className="text-red-300 font-medium">CI/CD Fix Service Error</span>
        </div>
        <p className="text-red-200">{error}</p>
        <button
          onClick={manualRefresh}
          className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
        >
          Retry Connection
        </button>
      </div>
    );
  }
  const currentPage = "fix";

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div className="flex items-center justify-between">
        <Breadcrumbs currentPage={currentPage} parentPage="dashboard" />
        <div className="flex items-center space-x-3">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${isMonitoring
            ? 'bg-green-500/20 text-green-400'
            : 'bg-gray-500/20 text-gray-400'
            }`}>
            <Activity className={`h-4 w-4 inline mr-2 ${isMonitoring ? 'animate-pulse' : ''}`} />
            {isMonitoring ? 'Running Fix Agent' : 'Agent STOPPED'}
          </div>
        </div>
      </div>

      {/* MONITOR CONTROL */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center">
            <Terminal className="h-5 w-5 mr-2 text-green-400" />
            Fix Monitor Control
          </h3>
          <div className="flex items-center space-x-3">
            {!isMonitoring ? (
              <button
                onClick={handleStartMonitor}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
              >
                <Play className="h-4 w-4" />
                <span>Start Monitor</span>
              </button>
            ) : (
              <button
                onClick={handleStopMonitor}
                className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
              >
                <Square className="h-4 w-4" />
                <span>Stop Monitor</span>
              </button>
            )}
            {showTerminal && (
              <button
                onClick={handleClearTerminal}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg"
              >
                <Trash2 className="h-4 w-4" />
                <span>Clear Terminal</span>
              </button>
            )}
          </div>
        </div>

        {/* TERMINAL */}
        {showTerminal && (
          <div className="bg-black rounded-lg border border-gray-600">
            <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-600">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-gray-300 text-sm ml-2">CI/CD Fix Monitor Terminal</span>
              </div>
              <button
                onClick={handleClearTerminal}
                className="text-gray-400 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div
              className="p-4 overflow-y-auto font-mono text-sm resize-y"
              style={{ minHeight: '200px', maxHeight: '80vh' }}
            >
              {terminalContent.length === 0 ? (
                <div className="text-green-400">
                  $ Starting CI/CD fix monitoring system...
                  <br />
                  $ Initializing log stream...
                  <br />
                  <span className="animate-pulse">$ Waiting for log entries...</span>
                </div>
              ) : (
                <div className="space-y-1">
                  {terminalContent.map((line, i) => (
                    <div key={i} className={
                      line.includes('ERROR') ? 'text-red-400' :
                        line.includes('WARN') ? 'text-yellow-400' :
                          line.includes('SUCCESS') ? 'text-green-400' :
                            line.includes('MONITOR STOPPED') ? 'text-cyan-400 font-bold' :
                              'text-gray-300'
                    }>
                      {line}
                    </div>
                  ))}
                  {isMonitoring && (
                    <div className="text-green-400 animate-pulse">$ Fix monitoring is Running...</div>
                  )}
                </div>
              )}
            </div>



          </div>
        )}
      </div>

      {!isMonitoring && !showTerminal && (
        <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-xl p-4">
          <div className="flex items-center space-x-2">
            <Pause className="h-5 w-5 text-yellow-400" />
            <span className="text-yellow-300 font-medium">Fix Monitoring Paused</span>
          </div>
          <p className="text-yellow-200 mt-1">Click "Start Monitor" to begin real-time monitoring of your CI/CD pipeline fixes.</p>
        </div>
      )}

      {loading && !data ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center space-x-3 text-cyan-300">
            <RefreshCw className="h-6 w-6 animate-spin" />
            <span className="text-lg">Loading CI/CD fix monitoring data...</span>
          </div>
        </div>
      ) : data ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white">CI/CD Pipeline Components</h2>
              <p className="text-gray-400 text-sm mt-1">
                Real-time fix monitoring of {data.files.length} pipeline configuration files
              </p>
            </div>
            <div className="text-sm text-gray-400">
              {data.files_with_errors} of {data.files.length} components have issues
            </div>
          </div>

          {data.files.length === 0 ? (
            <div className="text-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
              <GitBranch className="h-12 w-12 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No pipeline components are currently being monitored</p>
              <p className="text-gray-500 text-sm mt-2">
                Configure your CI/CD fix monitoring to start tracking pipeline health
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {['critical', 'warning'].flatMap(severity =>
                data.files
                  .filter(f => f.status === severity)
                  .map((file: FileStatusFix, index) => (
                    <FixFileCard
                      key={`${severity}-${index}`}
                      file={file}
                      onTriggerFix={handleTriggerFix}
                    />
                  ))
              )}
              {data.files
                .filter(f => !['critical', 'warning'].includes(f.status))
                .map((file: FileStatusFix, index) => (
                  <FixFileCard
                    key={`other-${index}`}
                    file={file}
                    onTriggerFix={handleTriggerFix}
                  />
                ))}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-400">No fix monitoring data available</p>
          <button
            onClick={handleStartMonitor}
            className="mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
          >
            Start Fix Monitoring
          </button>
        </div>
      )}
    </div>
  );
};
