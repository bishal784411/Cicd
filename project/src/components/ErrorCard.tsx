import React from 'react';
import { AlertTriangle, Clock, Brain, Wrench, CheckCircle, GitBranch, Hash } from 'lucide-react';
import { ErrorEntry } from '../types/monitoring';
import ReactMarkdown from 'react-markdown';
import { GlobalTerminal } from './GlobalTerminal';

interface ErrorCardProps {
  error: ErrorEntry;
  onTriggerFix?: (errorIndex: number) => void;
  errorIndex: number;
  showTerminal: boolean; 
}

export const ErrorCard: React.FC<ErrorCardProps> = ({ error, onTriggerFix, errorIndex }) => {
  
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-red-500/50 bg-red-500/10';
      case 'high':
        return 'border-orange-500/50 bg-orange-500/10';
      case 'medium':
        return 'border-yellow-500/50 bg-yellow-500/10';
      case 'low':
      default:
        return 'border-blue-500/50 bg-blue-500/10';
    }
  };


  const getErrorIdColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-red-500/50 bg-red-500/10';
      case 'high':
        return 'border-orange-500/50 bg-orange-500/10';
      case 'medium':
        return 'border-yellow-500/50 bg-yellow-500/10';
      case 'low':
      default:
        return 'border-blue-500/50 bg-blue-500/10';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'DOCKERFILE': return '🐳';
      case 'NETWORK': return '🌐';
      case 'BUILD': return '🔨';
      case 'DEPLOYMENT': return '🚀';
      case 'SECURITY': return '🔒';
      case 'PERFORMANCE': return '⚡';
      case 'CONFIG': return '⚙️';
      case 'TEST': return '🧪';
      default: return '📄';
    }
  };

  const getSeverityBadge = (severity: string) => {
    const colors = {
      critical: 'bg-red-500/20 text-red-300 border-red-500/30',
      high: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      low: 'bg-blue-500/20 text-blue-300 border-blue-500/30'
    };
    return colors[severity as keyof typeof colors] || colors.low;
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

  return (
    <div className={`rounded-lg border p-4 ${getSeverityColor(error.severity)}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          {/* <span className="text-lg">{getTypeIcon(error.error_type)}</span> */}
          <span className="text-lg text-purple-300">{error.err_id}</span>

          <div>
            <div className="flex items-center space-x-2">
              <span className="font-medium text-white">{error.error_type}</span>
              <span className={`px-2 py-1 text-xs rounded-full border ${getSeverityBadge(error.severity)}`}>
                {error.severity}
              </span>
              {error.pipeline_stage && (
                <span className={`px-2 py-1 text-xs rounded-full ${getPipelineStageColor(error.pipeline_stage)}`}>
                  {error.pipeline_stage}
                </span>
              )}
            </div>
            <div className="flex items-center space-x-3 mt-1">
              {error.line_number && (
                <span className="text-xs text-gray-400">Line {error.line_number}</span>
              )}
              {error.commit_hash && (
                <div className="flex items-center space-x-1 text-xs text-gray-400">
                  <Hash className="h-3 w-3" />
                  <span>{error.commit_hash}</span>
                </div>
              )}
              {error.branch && (
                <div className="flex items-center space-x-1 text-xs text-gray-400">
                  <GitBranch className="h-3 w-3" />
                  <span>{error.branch}</span>
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-xs text-gray-400">
            <Clock className="h-3 w-3" />
            <span>{new Date(error.timestamp).toLocaleTimeString()}</span>
          </div>
          
          {error.fix_applied ? (
            <div className="flex items-center space-x-1 text-xs text-green-400">
              <CheckCircle className="h-3 w-3" />
              <span>Fixed</span>
            </div>
          ) : error.auto_fixable && onTriggerFix && (
            <button
              onClick={() => onTriggerFix(errorIndex)}
              className="flex items-center space-x-1 px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
            >
              <Wrench className="h-3 w-3" />
              <span>Auto Fix</span>
            </button>
          )}
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <div className="flex items-center space-x-2 mb-2">
            <AlertTriangle className="h-4 w-4 text-red-400" />
            <span className="text-sm font-medium text-gray-300">Error Details</span>
          </div>
          <div className="bg-slate-900/60 rounded p-3 font-mono text-sm text-red-300 border border-red-500/20">
            {error.message}
          </div>
        </div>

        {error.ai_analysis && (
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Brain className="h-4 w-4 text-purple-400" />
              <span className="text-sm font-medium text-gray-300">AI Analysis</span>
            </div>
            <div className="bg-purple-500/10 border border-purple-500/20 rounded p-3 text-sm text-purple-200">
               <ReactMarkdown>{error.ai_analysis}</ReactMarkdown>
            </div>
          </div>
        )}

        {error.fix_suggestion && (
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Wrench className="h-4 w-4 text-green-400" />
              <span className="text-sm font-medium text-gray-300">Recommended Fix</span>
            </div>
            <div className="bg-green-500/10 border border-green-500/20 rounded p-3 text-sm text-green-200">
              
              <ReactMarkdown>{error.fix_suggestion}</ReactMarkdown>

            </div>
          </div>
        )}

        {error.fix_applied && error.fix_timestamp && (
          <div className="bg-emerald-500/10 border border-emerald-500/20 rounded p-2 text-xs text-emerald-300">
            ✅ Fix applied automatically at {new Date(error.fix_timestamp).toLocaleString()}
          </div>
        )}
      </div>

          <GlobalTerminal />
    
    </div>
  );
};