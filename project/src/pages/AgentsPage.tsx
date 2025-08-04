// import React from 'react';
// import {
//   Bot,
//   RefreshCw,
//   Play,
//   Cpu,
//   Activity,
//   Clock,
//   CheckCircle,
//   AlertTriangle,
//   Wifi,
//   WifiOff,
//   Zap,
//   Container,
//   Network,
//   Shield,
//   TestTube,
//   Rocket,
//   GitBranch
// } from 'lucide-react';
// import { useAgent } from '../hooks/useAgents';
// import { StatsCard } from '../components/StatsCard';

// type AgentType = {
//   id: string;
//   name: string;
//   type: string;
//   status: string;
//   health: string;
//   uptime: number;
//   cpu_usage: number;
//   memory_usage: number;
//   tasks_completed: number;
//   tasks_failed: number;
//   queue_size: number;
//   current_task?: string;
//   docker_containers?: number;
//   version: string;
//   location: string;
//   last_heartbeat: string;
// };

// type AgentsObject = {
//   monitor: AgentType;
//   solution: AgentType;
//   fix: AgentType;
// };

// export const AgentsPage: React.FC = () => {
//   const { agents, error, refetch } = useAgent();
//   console.log('Agents data from backend:', agents);


//   const normalizeAgent = (agent: any): AgentType => ({
//     ...agent,
//     cpu_usage: agent.system?.cpu_percent ?? 0,
//     memory_usage: agent.system?.memory_percent ?? 0,
//     // you can add disk usage or any others as needed
//   });

//   // Helpers for UI colors & icons
//   const getAgentTypeIcon = (type: string) => {
//     switch (type) {
//       case 'pipeline': return GitBranch;
//       case 'docker': return Container;
//       case 'network': return Network;
//       case 'security': return Shield;
//       case 'testing': return TestTube;
//       case 'deployment': return Rocket;
//       default: return Bot;
//     }
//   };

//   const getAgentTypeColor = (type: string) => {
//     switch (type) {
//       case 'pipeline': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
//       case 'docker': return 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30';
//       case 'network': return 'bg-green-500/20 text-green-400 border-green-500/30';
//       case 'security': return 'bg-red-500/20 text-red-400 border-red-500/30';
//       case 'testing': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
//       case 'deployment': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
//       default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
//     }
//   };

//   const getStatusColor = (status: string) => {
//     switch (status) {
//       case 'running': return 'bg-green-500/20 text-green-400';
//       case 'offline': return 'bg-gray-500/20 text-gray-400';
//       case 'busy': return 'bg-yellow-500/20 text-yellow-400';
//       case 'error': return 'bg-red-500/20 text-red-400';
//       default: return 'bg-gray-500/20 text-gray-400';
//     }
//   };

//   const getHealthColor = (health: string) => {
//     switch (health) {
//       case 'healthy': return 'text-green-400';
//       case 'warning': return 'text-yellow-400';
//       case 'critical': return 'text-red-400';
//       default: return 'text-gray-400';
//     }
//   };

//   const getUsageColor = (usage: number) => {
//     if (usage >= 90) return 'bg-red-500';
//     if (usage >= 70) return 'bg-yellow-500';
//     return 'bg-green-500';
//   };

//   if (error) {
//     return (
//       <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-6">
//         <div className="flex items-center space-x-2 mb-2">
//           <AlertTriangle className="h-5 w-5 text-red-400" />
//           <span className="text-red-300 font-medium">CI/CD Agents Service Error</span>
//         </div>
//         <p className="text-red-200">{error}</p>
//         <button
//           onClick={refetch}
//           className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
//         >
//           Retry Connection
//         </button>
//       </div>
//     );
//   }

//   if (!agents) {
//     return (
//       <div className="text-center py-12">
//         <RefreshCw className="h-6 w-6 animate-spin text-cyan-300 mx-auto mb-4" />
//         <p className="text-gray-400">Loading agents...</p>
//       </div>
//     );
//   }

//   // Destructure the agents object
//   const { monitor, solution, fix } = agents as unknown as AgentsObject;

//   // Compute some summary stats from these 3 agents:
//   const totalAgents = 3; // monitor, solution, fix
//   const onlineAgents = [monitor, solution, fix].filter(a => a.status === 'online').length;
//   const busyAgents = [monitor, solution, fix].filter(a => a.status === 'busy').length;
//   const totalTasks = [monitor, solution, fix].reduce((acc, a) => acc + a.tasks_completed, 0);
//   const avgUptime = Math.round(
//     [monitor, solution, fix].reduce((acc, a) => acc + a.uptime, 0) / totalAgents
//   );
//   const monitorNorm = normalizeAgent(monitor);
//   const solutionNorm = normalizeAgent(solution);
//   const fixNorm = normalizeAgent(fix);

//   // Agent Card component inline for reuse
//   const AgentCard: React.FC<{ agent: AgentType }> = ({ agent }) => {
//     const TypeIcon = getAgentTypeIcon(agent.type);
//     const StatusIcon = agent.status === 'online' ? Wifi : WifiOff;

//     function restartAgent(_id: string): void {
//       throw new Error('Function not implemented.');
//     }

//     return (
//       <div
//         className={`bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:border-slate-600/50 transition-colors
//         ${agent.status === 'stopped' ? 'opacity-40 grayscale pointer-events-none' : ''}`}
//       >
//         <div className="flex items-start justify-between mb-4">
//           <div className="flex items-center space-x-3">
//             <div className={`p-2 rounded-lg border ${getAgentTypeColor(agent.type)}`}>
//               <TypeIcon className="h-5 w-5" />
//             </div>
//             <div>
//               <h3 className="font-semibold text-white">{agent.name}</h3>
//               <p className="text-sm text-gray-400 capitalize">{agent.type} Agent</p>
//             </div>
//           </div>
//           <div className="flex items-center space-x-2">
//             <div className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(agent.status)}`}>
//               <StatusIcon className="h-3 w-3 inline mr-1" />
//               {agent.status.toUpperCase()}
//             </div>
//           </div>
//         </div>

//         <div className="grid grid-cols-2 gap-4 mb-4">
//           <div className="bg-slate-900/50 rounded-lg p-3">
//             <div className="flex items-center space-x-2 mb-1">
//               <Activity className={`h-4 w-4 ${getHealthColor(agent.health)}`} />
//               <span className="text-xs text-gray-400">Health</span>
//             </div>
//             <span className={`text-lg font-bold capitalize ${getHealthColor(agent.health)}`}>
//               {agent.health}
//             </span>
//           </div>
//           <div className="bg-slate-900/50 rounded-lg p-3">
//             <div className="flex items-center space-x-2 mb-1">
//               <Clock className="h-4 w-4 text-blue-400" />
//               <span className="text-xs text-gray-400">Uptime</span>
//             </div>
//             <span className="text-lg font-bold text-blue-400">{agent.uptime}No</span>
//           </div>
//         </div>

//         {/* Resource Usage: Only show if status is NOT 'stopped' */}
//         {agent.status !== 'stopped' && (
//           <div className="space-y-3 mb-4">
//             <div className="flex items-center space-x-3">
//               <Cpu className="h-4 w-4 text-blue-400" />
//               <div className="flex-1">
//                 <div className="flex justify-between text-xs mb-1">
//                   <span className="text-gray-300">CPU</span>
//                   <span className="text-white">{agent.cpu_usage}%</span>
//                 </div>
//                 <div className="w-full bg-slate-700 rounded-full h-1.5">
//                   <div
//                     className={`h-1.5 rounded-full transition-all duration-300 ${getUsageColor(agent.cpu_usage)}`}
//                     style={{ width: `${agent.cpu_usage}%` }}
//                   />
//                 </div>
//               </div>
//             </div>

//             <div className="flex items-center space-x-3">
//               <Zap className="h-4 w-4 text-purple-400" />
//               <div className="flex-1">
//                 <div className="flex justify-between text-xs mb-1">
//                   <span className="text-gray-300">Memory</span>
//                   <span className="text-white">{agent.memory_usage}%</span>
//                 </div>
//                 <div className="w-full bg-slate-700 rounded-full h-1.5">
//                   <div
//                     className={`h-1.5 rounded-full transition-all duration-300 ${getUsageColor(agent.memory_usage)}`}
//                     style={{ width: `${agent.memory_usage}%` }}
//                   />
//                 </div>
//               </div>
//             </div>
//           </div>
//         )}

//         <div className="flex items-center justify-between text-xs text-gray-400 mb-4">
//           <span>Tasks: {agent.tasks_completed} / {agent.tasks_failed} failed</span>
//           <span>Queue: {agent.queue_size}</span>
//         </div>

//         {agent.current_task && (
//           <div className="bg-yellow-500/10 border border-yellow-500/20 rounded p-2 mb-4">
//             <p className="text-xs text-yellow-300">
//               Current: {agent.current_task}
//             </p>
//           </div>
//         )}

//         {agent.docker_containers && (
//           <div className="bg-cyan-500/10 border border-cyan-500/20 rounded p-2 mb-4">
//             <p className="text-xs text-cyan-300">
//               Managing {agent.docker_containers} Docker containers
//             </p>
//           </div>
//         )}

//         <div className="flex items-center space-x-2">
//           <button
//             onClick={() => restartAgent(agent.id)}
//             disabled={agent.status === 'offline'}
//             className="flex items-center space-x-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:opacity-50 text-white rounded text-sm font-medium transition-colors"
//           >
//             <Play className="h-3 w-3" />
//             <span>Restart</span>
//           </button>
//         </div>

//         <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-gray-500">
//           <div className="flex justify-between">
//             <span>Version: {agent.version}</span>
//             <span>Location: {agent.location}</span>
//           </div>
//           <div className="mt-1">
//             Last heartbeat: {new Date(agent.last_heartbeat).toLocaleString()}
//           </div>
//         </div>
//       </div>
//     );
//   };


//   return (
//     <div className="space-y-8">
//       {/* Header */}
//       <div className="flex items-center justify-between">
//         <div>
//           <h1 className="text-2xl font-bold text-white">CI/CD Agent Management</h1>
//           <p className="text-gray-400 mt-1">Monitor and control your DevOps automation agents</p>
//         </div>

//       </div>

//       {/* Stats Overview */}
//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
//         <StatsCard
//           title="Online Agents"
//           value={onlineAgents}
//           icon={CheckCircle}
//           color="bg-green-500/20 text-green-400"
//           subtitle={`${totalAgents} total agents`}
//         />
//         <StatsCard
//           title="Busy Agents"
//           value={busyAgents}
//           icon={Activity}
//           color="bg-yellow-500/20 text-yellow-400"
//           subtitle="Currently processing tasks"
//         />
//         <StatsCard
//           title="Tasks Completed"
//           value={totalTasks}
//           icon={CheckCircle}
//           color="bg-blue-500/20 text-blue-400"
//           subtitle="All-time task count"
//         />
//         <StatsCard
//           title="Average Uptime"
//           value={`${avgUptime}`}
//           icon={Clock}
//           color="bg-purple-500/20 text-purple-400"
//           subtitle="Across all agents"
//         />
//       </div>

//       {/* Agents List */}
//       <div className="space-y-6">
//         <div className="flex items-center justify-between">
//           <h2 className="text-xl font-bold text-white">Active CI/CD Agents</h2>
//           <div className="text-sm text-gray-400">
//             {totalAgents} agents registered
//           </div>
//         </div>

//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//           <AgentCard agent={monitorNorm} />
//           <AgentCard agent={solutionNorm} />
//           <AgentCard agent={fixNorm} />
//         </div>
//       </div>
//     </div>
//   );
// };

import React from 'react';
import {
  Bot,
  RefreshCw,
  Play,
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
import { useAgent } from '../hooks/useAgents';
import { StatsCard } from '../components/StatsCard';

type AgentType = {
  id: string;
  name: string;
  type: string;
  status: string;
  health: string;
  uptime: number;
  cpu_usage: number;
  memory_usage: number;
  tasks_completed: number;
  tasks_failed: number;
  queue_size: number;
  current_task?: string;
  docker_containers?: number;
  version: string;
  location: string;
  last_heartbeat: string;
};

type AgentsObject = {
  monitor: AgentType;
  solution: AgentType;
  fix: AgentType;
};

export const AgentsPage: React.FC = () => {
  const { agents, error, refetch, summary } = useAgent();
  console.log('Agents data from backend:', agents);

  const normalizeAgent = (agent: any): AgentType => ({
    ...agent,
    cpu_usage: agent.system?.cpu_percent ?? 0,
    memory_usage: agent.system?.memory_percent ?? 0,
  });

  // Helpers for UI colors & icons
  const getAgentTypeIcon = (type: string) => {
    switch (type) {
      case 'pipeline':
        return GitBranch;
      case 'docker':
        return Container;
      case 'network':
        return Network;
      case 'security':
        return Shield;
      case 'testing':
        return TestTube;
      case 'deployment':
        return Rocket;
      default:
        return Bot;
    }
  };

  const getAgentTypeColor = (type: string) => {
    switch (type) {
      case 'pipeline':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'docker':
        return 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30';
      case 'network':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'security':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'testing':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'deployment':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-500/20 text-green-400';
      case 'offline':
        return 'bg-gray-500/20 text-gray-400';
      case 'busy':
        return 'bg-yellow-500/20 text-yellow-400';
      case 'error':
        return 'bg-red-500/20 text-red-400';
      default:
        return 'bg-gray-500/20 text-gray-400';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy':
        return 'text-green-400';
      case 'warning':
        return 'text-yellow-400';
      case 'critical':
        return 'text-red-400';
      default:
        return 'text-gray-400';
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

  if (!agents) {
    return (
      <div className="text-center py-12">
        <RefreshCw className="h-6 w-6 animate-spin text-cyan-300 mx-auto mb-4" />
        <p className="text-gray-400">Loading agents...</p>
      </div>
    );
  }

  const { monitor, solution, fix } = agents as unknown as AgentsObject;

  // Use summary fields from backend or fallback defaults
  const totalAgents = 3; // monitor, solution, fix
  const onlineAgents = summary?.online_agents ?? 0;
  const totalTasks = summary?.tasks_completed ?? 0;
  const avgUptime = summary?.average_uptime ?? null;

  const monitorNorm = normalizeAgent(monitor);
  const solutionNorm = normalizeAgent(solution);
  const fixNorm = normalizeAgent(fix);

  // Agent Card component inline for reuse
  const AgentCard: React.FC<{ agent: AgentType }> = ({ agent }) => {
    const TypeIcon = getAgentTypeIcon(agent.type);
    const StatusIcon = agent.status === 'online' ? Wifi : WifiOff;

    function restartAgent(_id: string): void {
      throw new Error('Function not implemented.');
    }

    return (
      <div
        className={`bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:border-slate-600/50 transition-colors
        ${agent.status === 'stopped' ? 'opacity-40 grayscale pointer-events-none' : ''}`}
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
            <span className="text-lg font-bold text-blue-400">{agent.uptime ?? 'N/A'}</span>
          </div>
        </div>

        {/* Resource Usage: Only show if status is NOT 'stopped' */}
        {agent.status !== 'stopped' && (
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
        )}

        <div className="flex items-center justify-between text-xs text-gray-400 mb-4">
          <span>
            Tasks: {agent.tasks_completed} / {agent.tasks_failed} failed
          </span>
          <span>Queue: {agent.queue_size}</span>
        </div>

        {agent.current_task && (
          <div className="bg-yellow-500/10 border border-yellow-500/20 rounded p-2 mb-4">
            <p className="text-xs text-yellow-300">Current: {agent.current_task}</p>
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
        </div>

        <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-gray-500">
          <div className="flex justify-between">
            <span>Version: {agent.version}</span>
            <span>Location: {agent.location}</span>
          </div>
          <div className="mt-1">
            Last heartbeat: {agent.last_heartbeat ? new Date(agent.last_heartbeat).toLocaleString() : 'N/A'}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">CI/CD Agent Management</h1>
          <p className="text-gray-400 mt-1">Monitor and control your DevOps automation agents</p>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatsCard
          title="Online Agents"
          value={onlineAgents}
          icon={CheckCircle}
          color="bg-green-500/20 text-green-400"
          subtitle={`${totalAgents} total agents`}
        />
        {/* Busy Agents removed */}

        <StatsCard
          title="Tasks Completed"
          value={totalTasks}
          icon={CheckCircle}
          color="bg-blue-500/20 text-blue-400"
          subtitle="All-time task count"
        />
        <StatsCard
          title="Average Uptime"
          value={avgUptime !== null ? `${avgUptime}` : 'N/A'}
          icon={Clock}
          color="bg-purple-500/20 text-purple-400"
          subtitle="Across all agents"
        />
      </div>

      {/* Agents List */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Active CI/CD Agents</h2>
          <div className="text-sm text-gray-400">{totalAgents} agents registered</div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <AgentCard agent={monitorNorm} />
          <AgentCard agent={solutionNorm} />
          <AgentCard agent={fixNorm} />
        </div>
      </div>
    </div>
  );
};
