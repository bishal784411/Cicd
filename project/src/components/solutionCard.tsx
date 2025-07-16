
// components/SolutionCard.tsx
import React from 'react';
import {
  Clock,
  Brain,
  Wrench,
  ShieldAlert,
  TrendingUp,
  AlertTriangle,
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { SolutionMeta } from '../types/monitoring';

interface SolutionCardProps {
  solution: SolutionMeta;
  onTriggerExecute?: (solutionId: string) => void;
}

export const SolutionCard: React.FC<SolutionCardProps> = ({ solution, onTriggerExecute }) => {

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'border-green-500/50 bg-green-500/10';
      case 'inactive': return 'border-gray-500/50 bg-gray-500/10';
      case 'pending': return 'border-yellow-500/50 bg-yellow-500/10';
      case 'failed': return 'border-red-500/50 bg-red-500/10';
      default: return 'border-slate-500/50 bg-slate-500/10';
    }
  };

  const getStatusBadge = (status: string) => {
    const colors = {
      active: 'bg-green-500/20 text-green-300 border-green-500/30',
      inactive: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
      pending: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
      failed: 'bg-red-500/20 text-red-300 border-red-500/30',
    };
    return colors[status as keyof typeof colors] || colors.inactive;
  };

  return (
    <div className={`rounded-lg border p-4 ${getStatusColor(solution.status)}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          <span className="text-lg text-[#adff2f]">{solution.id}</span>

          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-medium text-white">{solution.error_types}</span>
              <span className={`px-2 py-1 text-xs rounded-full border ${getStatusBadge(solution.status)}`}>
                {solution.status.toUpperCase()}
              </span>
            </div>
            <div className="flex items-center space-x-3 mt-1 text-xs text-gray-400">
              <span>Exec Count: {solution.execution_count}</span>
              {/* <span>Success: {solution.success_rate}%</span> */}
              <span>Avg Time: {solution.avg_execution_time}s</span>
              <span>Model Confidence: {solution.success_rate}%</span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-xs text-gray-400">
            <Clock className="h-3 w-3" />
            <span>{new Date(solution.last_executed).toLocaleTimeString()}</span>
          </div>

          {solution.status === 'active' && onTriggerExecute && (
            <button
              onClick={() => onTriggerExecute(solution.id)}
              className="flex items-center space-x-1 px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
            >
              <Wrench className="h-3 w-3" />
              <span>Run</span>
            </button>
          )}
        </div>
      </div>

      <div>
        <div className="flex items-center space-x-2 mb-2">
          <AlertTriangle className="h-4 w-4 text-red-400" />
          <span className="text-sm font-medium text-gray-300">Error Details</span>
        </div>
        <div className="bg-slate-900/60 rounded p-3 font-mono text-sm text-red-300 border border-red-500/20">
          {solution.name}
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <div className="flex items-center space-x-2 mb-2">
            <Brain className="h-4 w-4 text-purple-400" />
            <span className="text-sm font-medium text-gray-300">Description</span>
          </div>
          <div className="bg-slate-900/60 rounded p-3 text-sm text-purple-200 border border-purple-500/20">
            <ReactMarkdown>{solution.description}</ReactMarkdown>
          </div>
        </div>

        <div>
          <div className="flex items-center space-x-2 mb-2">
            <Wrench className="h-4 w-4 text-green-400" />
            <span className="text-sm font-medium text-gray-300">Solution pass to Fix Agent</span>
          </div>
          <div className="bg-green-500/10 border border-green-500/20 rounded p-3 text-sm text-green-200">

            <ReactMarkdown>{solution.code}</ReactMarkdown>

          </div>
        </div>


        <div>
          <div className="flex items-center space-x-2 mb-2">
            <TrendingUp className="h-4 w-4 text-green-400" />
            <span className="text-sm font-medium text-gray-300">Pipeline Stages</span>
          </div>
          <div className="flex flex-wrap gap-2 text-xs text-green-300">
            {solution.pipeline_stages.map((stage) => (
              <span key={stage} className="bg-green-500/10 px-2 py-1 rounded border border-green-500/30">
                {stage}
              </span>
            ))}
          </div>
        </div>

        <div className="text-xs text-gray-400">
          <div>Created by: <span className="text-white">{solution.created_by}</span></div>
          <div>Created at: {new Date(solution.created_at).toLocaleString()}</div>
          <div>Auto-trigger: {solution.auto_trigger ? 'Yes' : 'No'}</div>
        </div>
      </div>
    </div>
  );
};
