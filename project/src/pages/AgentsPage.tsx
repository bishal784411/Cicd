import React from 'react';
import { 
  Bot, 
  RefreshCw, 
  Play, 
  Square, 
  Cpu, 
  Activity, 
  Clock, 
  CheckCircle,
  AlertTriangle,
  Wifi,
  WifiOff,
  Zap,
  Container,
  Network,
  Shield,
  TestTube,
  Rocket,
  GitBranch
} from 'lucide-react';
import { useAgents } from '../hooks/useAgents';
import { StatsCard } from '../components/StatsCard';

export const AgentsPage: React.FC = () => {
  const { agents, loading, error, refetch, restartAgent, stopAgent } = useAgents();

  const getAgentTypeIcon = (type: string) => {
    switch (type) {
      case 'pipeline': return GitBranch;
      case 'docker': return Container;
      case 'network': return Network;
      case 'security': return Shield;
      case 'testing': return TestTube;
      case 'deployment': return Rocket;
      default: return Bot;
    }
  };

  const getAgentTypeColor = (type: string) => {
    switch (type) {
      case 'pipeline': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'docker': return 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30';
      case 'network': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'security': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'testing': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'deployment': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500/20 text-green-400';
      case 'offline': return 'bg-gray-500/20 text-gray-400';
      case 'busy': return 'bg-yellow-500/20 text-yellow-400';
      case 'error': return 'bg-red-500/20 text-red-400';
      case 'maintenance': return 'bg-blue-500/20 text-blue-400';
      default: return 'bg-gray-500/20 text-gray-400';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy': return 'text-green-400';
      case 'warning': return 'text-yellow-400';
      case 'critical': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getUsageColor = (usage: number) => {
    if (usage >= 90) return 'bg-red-500';
    if (usage >= 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (error) {
    return (
      <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-2">
          <AlertTriangle className="h-5 w-5 text-red-400" />
          <span className="text-red-300 font-medium">CI/CD Agents Service Error</span>
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

  const onlineAgents = agents.filter(a => a.status === 'online').length;
  const busyAgents = agents.filter(a => a.status === 'busy').length;
  const totalTasks = agents.reduce((acc, a) => acc + a.tasks_completed, 0);
  const avgUptime = agents.length > 0 
    ? Math.round(agents.reduce((acc, a) => acc + a.uptime, 0) / agents.length)
    : 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">CI/CD Agent Management</h1>
          <p className="text-gray-400 mt-1">Monitor and control your DevOps automation agents</p>
        </div>
        <button
          onClick={refetch}
          disabled={loading}
          className="flex items-center space-x-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-800 disabled:opacity-50 text-white rounded-lg transition-colors"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Online Agents"
          value={onlineAgents}
          icon={CheckCircle}
          color="bg-green-500/20 text-green-400"
          subtitle={`${agents.length} total agents`}
        />
        <StatsCard
          title="Busy Agents"
          value={busyAgents}
          icon={Activity}
          color="bg-yellow-500/20 text-yellow-400"
          subtitle="Currently processing tasks"
        />
        <StatsCard
          title="Tasks Completed"
          value={totalTasks}
          icon={CheckCircle}
          color="bg-blue-500/20 text-blue-400"
          subtitle="All-time task count"
        />
        <StatsCard
          title="Average Uptime"
          value={`${avgUptime}%`}
          icon={Clock}
          color="bg-purple-500/20 text-purple-400"
          subtitle="Across all agents"
        />
      </div>

      {/* Agents List */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Active CI/CD Agents</h2>
          <div className="text-sm text-gray-400">
            {agents.length} agents registered
          </div>
        </div>

        {loading && agents.length === 0 ? (
          <div className="text-center py-12">
            <RefreshCw className="h-6 w-6 animate-spin text-cyan-300 mx-auto mb-4" />
            <p className="text-gray-400">Loading agents...</p>
          </div>
        ) : agents.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
            <Bot className="h-12 w-12 text-gray-500 mx-auto mb-4" />
            <p className="text-gray-400">No CI/CD agents registered</p>
            <p className="text-gray-500 text-sm mt-2">
              Deploy agents to start automation
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {agents.map((agent) => {
              const TypeIcon = getAgentTypeIcon(agent.type);
              const StatusIcon = agent.status === 'online' ? Wifi : WifiOff;
              
              return (
                <div
                  key={agent.id}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:border-slate-600/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg border ${getAgentTypeColor(agent.type)}`}>
                        <TypeIcon className="h-5 w-5" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">{agent.name}</h3>
                        <p className="text-sm text-gray-400 capitalize">{agent.type} Agent</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(agent.status)}`}>
                        <StatusIcon className="h-3 w-3 inline mr-1" />
                        {agent.status.toUpperCase()}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-slate-900/50 rounded-lg p-3">
                      <div className="flex items-center space-x-2 mb-1">
                        <Activity className={`h-4 w-4 ${getHealthColor(agent.health)}`} />
                        <span className="text-xs text-gray-400">Health</span>
                      </div>
                      <span className={`text-lg font-bold capitalize ${getHealthColor(agent.health)}`}>
                        {agent.health}
                      </span>
                    </div>
                    <div className="bg-slate-900/50 rounded-lg p-3">
                      <div className="flex items-center space-x-2 mb-1">
                        <Clock className="h-4 w-4 text-blue-400" />
                        <span className="text-xs text-gray-400">Uptime</span>
                      </div>
                      <span className="text-lg font-bold text-blue-400">{agent.uptime}%</span>
                    </div>
                  </div>

                  {/* Resource Usage */}
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center space-x-3">
                      <Cpu className="h-4 w-4 text-blue-400" />
                      <div className="flex-1">
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-gray-300">CPU</span>
                          <span className="text-white">{agent.cpu_usage}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-1.5">
                          <div 
                            className={`h-1.5 rounded-full transition-all duration-300 ${getUsageColor(agent.cpu_usage)}`}
                            style={{ width: `${agent.cpu_usage}%` }}
                          />
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <Zap className="h-4 w-4 text-purple-400" />
                      <div className="flex-1">
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-gray-300">Memory</span>
                          <span className="text-white">{agent.memory_usage}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-1.5">
                          <div 
                            className={`h-1.5 rounded-full transition-all duration-300 ${getUsageColor(agent.memory_usage)}`}
                            style={{ width: `${agent.memory_usage}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-gray-400 mb-4">
                    <span>Tasks: {agent.tasks_completed} / {agent.tasks_failed} failed</span>
                    <span>Queue: {agent.queue_size}</span>
                  </div>

                  {agent.current_task && (
                    <div className="bg-yellow-500/10 border border-yellow-500/20 rounded p-2 mb-4">
                      <p className="text-xs text-yellow-300">
                        Current: {agent.current_task}
                      </p>
                    </div>
                  )}

                  {agent.docker_containers && (
                    <div className="bg-cyan-500/10 border border-cyan-500/20 rounded p-2 mb-4">
                      <p className="text-xs text-cyan-300">
                        Managing {agent.docker_containers} Docker containers
                      </p>
                    </div>
                  )}

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => restartAgent(agent.id)}
                      disabled={agent.status === 'offline'}
                      className="flex items-center space-x-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:opacity-50 text-white rounded text-sm font-medium transition-colors"
                    >
                      <Play className="h-3 w-3" />
                      <span>Restart</span>
                    </button>
                    <button
                      onClick={() => stopAgent(agent.id)}
                      disabled={agent.status === 'offline'}
                      className="flex items-center space-x-1 px-3 py-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:opacity-50 text-white rounded text-sm font-medium transition-colors"
                    >
                      <Square className="h-3 w-3" />
                      <span>Stop</span>
                    </button>
                  </div>

                  <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-gray-500">
                    <div className="flex justify-between">
                      <span>Version: {agent.version}</span>
                      <span>Location: {agent.location}</span>
                    </div>
                    <div className="mt-1">
                      Last heartbeat: {new Date(agent.last_heartbeat).toLocaleString()}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};