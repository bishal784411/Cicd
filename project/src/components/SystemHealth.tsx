import React from 'react';
import { Activity, Cpu, HardDrive, Wifi, Zap, Container, GitBranch, CheckCircle, XCircle } from 'lucide-react';
import { SystemMetrics } from '../types/monitoring';

interface SystemHealthProps {
  metrics: SystemMetrics;
  systemHealth: 'healthy' | 'degraded' | 'critical';
  agentStatus: 'active' | 'idle' | 'error' | 'maintenance';
  pipelineStatus: 'running' | 'idle' | 'failed' | 'success';
}

export const SystemHealth: React.FC<SystemHealthProps> = ({ 
  metrics, 
  systemHealth, 
  agentStatus, 
  pipelineStatus 
}) => {
  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy': return 'text-green-400 bg-green-500/20';
      case 'degraded': return 'text-yellow-400 bg-yellow-500/20';
      case 'critical': return 'text-red-400 bg-red-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getAgentStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-500/20';
      case 'idle': return 'text-blue-400 bg-blue-500/20';
      case 'error': return 'text-red-400 bg-red-500/20';
      case 'maintenance': return 'text-orange-400 bg-orange-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getPipelineStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'text-green-400 bg-green-500/20';
      case 'running': return 'text-blue-400 bg-blue-500/20';
      case 'failed': return 'text-red-400 bg-red-500/20';
      case 'idle': return 'text-gray-400 bg-gray-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getUsageColor = (usage: number) => {
    if (usage >= 90) return 'bg-red-500';
    if (usage >= 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* System Status */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">CI/CD System Status</h3>
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${getHealthColor(systemHealth)}`}>
            <Activity className="h-4 w-4 inline mr-2" />
            {systemHealth.toUpperCase()}
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Pipeline Status</span>
            <div className={`px-2 py-1 rounded text-xs font-medium flex items-center space-x-1 ${getPipelineStatusColor(pipelineStatus)}`}>
              {pipelineStatus === 'success' ? <CheckCircle className="h-3 w-3" /> : 
               pipelineStatus === 'failed' ? <XCircle className="h-3 w-3" /> : 
               <GitBranch className="h-3 w-3" />}
              <span>{pipelineStatus.toUpperCase()}</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-300">DevOps Agents</span>
            <div className={`px-2 py-1 rounded text-xs font-medium ${getAgentStatusColor(agentStatus)}`}>
              {agentStatus.toUpperCase()}
            </div>
          </div>
          
          
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Active Agents</span>
            <span className="text-cyan-400 font-mono">{metrics.docker_containers_running}</span>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Successful Deployments Today</span>
            <span className="text-green-400 font-mono">{metrics.successful_deployments_today}</span>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Failed Builds Today</span>
            <span className="text-red-400 font-mono">{metrics.failed_builds_today}</span>
          </div>
        </div>
      </div>

      {/* Resource Usage */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-lg font-semibold text-white mb-4">Infrastructure Resources</h3>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <Cpu className="h-5 w-5 text-blue-400" />
            <div className="flex-1">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-300">CPU Usage</span>
                <span className="text-white font-mono">{metrics.cpu_usage}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${getUsageColor(metrics.cpu_usage)}`}
                  style={{ width: `${metrics.cpu_usage}%` }}
                />
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <Zap className="h-5 w-5 text-purple-400" />
            <div className="flex-1">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-300">Memory Usage</span>
                <span className="text-white font-mono">{metrics.memory_usage}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${getUsageColor(metrics.memory_usage)}`}
                  style={{ width: `${metrics.memory_usage}%` }}
                />
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <HardDrive className="h-5 w-5 text-green-400" />
            <div className="flex-1">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-300">Disk Usage</span>
                <span className="text-white font-mono">{metrics.disk_usage}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${getUsageColor(metrics.disk_usage)}`}
                  style={{ width: `${metrics.disk_usage}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};