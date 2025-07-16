import React, { useRef, useState } from 'react';
import {
  ChevronDown,
  ChevronRight,
  FileText,
  Clock,
  TrendingUp,
  Wrench,
  TrendingDown
} from 'lucide-react';
import { StatusBadge } from './StatusBadge';
import { ErrorCard } from './ErrorCard';
import { useTerminal } from '../components/TerminalContext';
import { FileStatus } from '../types/monitoring';
// import {  } from '../components/TerminalContext';


interface FileCardProps {
  file: FileStatus;
  onTriggerFix?: (filePath: string, errorIndex: number) => void;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const FileCard: React.FC<FileCardProps> = ({ file }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const { isOpen: showTerminal, openTerminal, closeTerminal, clearTerminal, appendLog } = useTerminal();
  const cardRef = useRef<HTMLDivElement | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const getUptimeColor = (uptime?: number) => {
    if (!uptime) return 'text-gray-400';
    if (uptime >= 99) return 'text-green-400';
    if (uptime >= 95) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getBuildStatusColor = (status?: string) => {
    switch (status) {
      case 'success': return 'text-green-400';
      case 'failed': return 'text-red-400';
      case 'running': return 'text-yellow-400';
      case 'pending': return 'text-blue-400';
      default: return 'text-gray-400';
    }
  };

  const getBuildStatusIcon = (status?: string) => {
    switch (status) {
      case 'success':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      default:
        return null;
    }
  };

  const getPipelineStageColor = (stage?: string) => {
    switch (stage) {
      case 'build': return 'bg-blue-500/20 text-blue-300';
      case 'test': return 'bg-purple-500/20 text-purple-300';
      case 'deploy': return 'bg-green-500/20 text-green-300';
      case 'post-deploy': return 'bg-cyan-500/20 text-cyan-300';
      default: return 'bg-gray-500/20 text-gray-300';
    }
  };

  const toggleTerminalAndStreamLogs = (e: React.MouseEvent) => {
    e.stopPropagation();

    if (!isExpanded) setIsExpanded(true);

    if (!showTerminal) {
      openTerminal();
      clearTerminal();

      // Use the first error's err_id to stream logs
      if (file.errors.length > 0) {
        const firstErrId = file.errors[0].err_id;
        eventSourceRef.current = new EventSource(
          `${API_BASE_URL}/solution/${firstErrId}/stream/logs`
        );

        eventSourceRef.current.onmessage = (event) => {
          appendLog(event.data);
        };

        eventSourceRef.current.onerror = () => {
          appendLog('\n--- Script finished running ---');
          eventSourceRef.current?.close();
          eventSourceRef.current = null;
        };
      }

      setTimeout(() => {
        cardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
    } else {
      closeTerminal();
      eventSourceRef.current?.close();
      eventSourceRef.current = null;
    }
  };

  return (
    <div
      ref={cardRef}
      className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 overflow-hidden hover:border-slate-600/50 transition-colors"
    >
      <div
        className="p-4 cursor-pointer hover:bg-slate-700/20 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              {file.errors.length > 0 ? (
                isExpanded ? (
                  <ChevronDown className="h-4 w-4 text-gray-400" />
                ) : (
                  <ChevronRight className="h-4 w-4 text-gray-400" />
                )
              ) : (
                <FileText className="h-4 w-4 text-gray-400" />
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-1">
                <h3 className="font-medium text-white text-sm">{file.file}</h3>
                {file.pipeline_stage && (
                  <span
                    className={`px-2 py-1 text-xs rounded-full ${getPipelineStageColor(
                      file.pipeline_stage
                    )}`}
                  >
                    {file.pipeline_stage}
                  </span>
                )}
              </div>
              <div className="flex items-center space-x-4 text-xs text-gray-400">
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>Last checked: {new Date(file.last_checked).toLocaleString()}</span>
                </div>
                {file.build_status && (
                  <div className="flex items-center space-x-1">
                    <span>{getBuildStatusIcon(file.build_status)}</span>
                    <span className={getBuildStatusColor(file.build_status)}>
                      Github Push: {file.build_status}
                    </span>
                  </div>
                )}
                {file.uptime_percentage !== undefined && (
                  <div className="flex items-center space-x-1">
                    <span className={getUptimeColor(file.uptime_percentage)}>
                      {file.uptime_percentage}%
                    </span>
                  </div>
                )}
                {file.last_fix_attempt && (
                  <div className="flex items-center space-x-1">
                    <Wrench className="h-3 w-3" />
                    <span>Last fix: {new Date(file.last_fix_attempt).toLocaleString()}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Button + Status */}
          <div className="flex items-center space-x-2">
            <button
              onClick={toggleTerminalAndStreamLogs}
              className="px-4 py-1 bg-slate-600 hover:bg-slate-700 text-white text-xs rounded"
            >
              {showTerminal ? 'Hide Terminal' : 'Give Solution'}
            </button>

            <StatusBadge status={file.status} errorCount={file.error_count} />
          </div>
        </div>
      </div>

      {/* Expanded content */}
      {isExpanded && file.errors.length > 0 && (
        <div className="border-t border-slate-700/50 p-4 space-y-4 bg-slate-900/20">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-300">
              {file.errors.length} issue{file.errors.length !== 1 ? 's' : ''} detected
            </span>
          </div>

          {file.errors.map((error, index) => (
            <ErrorCard
              key={error.err_id}
              error={error}
              errorIndex={index}
              showTerminal={showTerminal}
            />
          ))}
        </div>
      )}
    </div>
  );
};
