import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Activity,
  CheckCircle,
  AlertTriangle,
  Container,
  GitBranch,
  Zap,
  Clock,
  Users,
  Server,
  Shield,
  Rocket,
} from 'lucide-react';
import { StatsCard } from '../components/StatsCard';
import { SystemHealth } from '../components/SystemHealth';
import { ProcessFlowMap } from '../components/ProcessFlowMap';
import { Breadcrumbs } from '../components/Breadcrumbs';
import { LiveNetworkStatus } from '../components/LiveNetworkStatus';

interface Metrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_pipelines: number;
  docker_containers_running: number;
  successful_deployments_today: number;
  failed_builds_today: number;
}

export const DashboardPage: React.FC = () => {

  // Live metrics state
  const [metrics, setMetrics] = useState<Metrics>({
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
    active_pipelines: 8,
    docker_containers_running: 24,
    successful_deployments_today: 12,
    failed_builds_today: 3,
  });

  // Other system statuses (can be fetched from other APIs or mocked here)
  const [systemHealth] = useState<'healthy' | 'degraded' | 'critical'>('healthy');
  const [agentStatus] = useState<'active' | 'idle' | 'error' | 'maintenance'>('active');
  const [pipelineStatus] = useState<'running' | 'idle' | 'failed' | 'success'>('running');
  const [loading, setLoading] = useState(true);

  const currentPage = "dashboard";

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

        setLoading(false);
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




  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center space-x-3 text-cyan-300">
          <BarChart3 className="h-6 w-6 animate-pulse" />
          <span className="text-lg">Loading dashboard metrics...</span>
        </div>
      </div>
    );
  }

  // Mock agent and deployment data (or replace with real API data)
  const mockAgentData = {
    totalAgents: 6,
    activeAgents: 4,
    agentsWithIssues: 1,
  };

  const mockDeploymentData = {
    successfulDeployments: metrics.successful_deployments_today,
    failedDeployments: metrics.failed_builds_today,
    totalPipelines: metrics.active_pipelines,
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <Breadcrumbs currentPage={currentPage} parentPage="dashboard" />

      {/* System Health Overview */}
      <SystemHealth
        metrics={metrics}
        systemHealth={systemHealth}
        agentStatus={agentStatus}
        pipelineStatus={pipelineStatus}
      />

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Agents"
          value={mockAgentData.totalAgents}
          icon={Users}
          color="bg-blue-500/20 text-blue-400"
          subtitle={`${mockAgentData.activeAgents} active, ${mockAgentData.agentsWithIssues} with issues`}
          trend={{ value: 8.2, isPositive: true }}
        />

        <StatsCard
          title="Successful Deployments"
          value={mockDeploymentData.successfulDeployments}
          icon={CheckCircle}
          color="bg-green-500/20 text-green-400"
          subtitle="Today's successful deployments"
          trend={{ value: 15.3, isPositive: true }}
        />

        <StatsCard
          title="Pipeline Files Monitored"
          value={mockDeploymentData.totalPipelines}
          icon={GitBranch}
          color="bg-purple-500/20 text-purple-400"
          subtitle="Docker, K8s, CI/CD configs"
          trend={{ value: 2.1, isPositive: true }}
        />

        <StatsCard
          title="Critical Issues"
          value={4} // Replace with real critical issues count if available
          icon={AlertTriangle}
          color="bg-red-500/20 text-red-400"
          subtitle="Requiring immediate attention"
          trend={{ value: 12.5, isPositive: false }}
        />
      </div>

      {/* Secondary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Active Pipelines"
          value={mockDeploymentData.totalPipelines}
          icon={Activity}
          color="bg-cyan-500/20 text-cyan-400"
          subtitle="Currently running"
        />

        <StatsCard
          title="Docker Containers"
          value={metrics.docker_containers_running}
          icon={Container}
          color="bg-indigo-500/20 text-indigo-400"
          subtitle="Running containers"
        />

        <StatsCard
          title="Failed Builds Today"
          value={mockDeploymentData.failedDeployments}
          icon={AlertTriangle}
          color="bg-orange-500/20 text-orange-400"
          subtitle="Build failures"
        />

        <StatsCard
          title="System Uptime"
          value="99.8%"
          icon={TrendingUp}
          color="bg-emerald-500/20 text-emerald-400"
          subtitle="Last 30 days"
        />
      </div>

      {/* Quick Actions & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-yellow-400" />
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button className="flex items-center space-x-2 p-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
              <Rocket className="h-4 w-4" />
              <span className="text-sm font-medium">Deploy Pipeline</span>
            </button>
            <button className="flex items-center space-x-2 p-3 bg-green-600 hover:bg-green-700 rounded-lg transition-colors">
              <Activity className="h-4 w-4" />
              <span className="text-sm font-medium">Start Monitor</span>
            </button>
            <button className="flex items-center space-x-2 p-3 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors">
              <Shield className="h-4 w-4" />
              <span className="text-sm font-medium">Security Scan</span>
            </button>
            <button className="flex items-center space-x-2 p-3 bg-orange-600 hover:bg-orange-700 rounded-lg transition-colors">
              <Server className="h-4 w-4" />
              <span className="text-sm font-medium">Restart Agents</span>
            </button>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Clock className="h-5 w-5 mr-2 text-blue-400" />
            Recent Activity
          </h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-3 p-2 bg-slate-700/30 rounded">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Pipeline deployment completed successfully</span>
              <span className="text-xs text-gray-500 ml-auto">2m ago</span>
            </div>
            <div className="flex items-center space-x-3 p-2 bg-slate-700/30 rounded">
              <div className="w-2 h-2 bg-red-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Docker build failed in staging</span>
              <span className="text-xs text-gray-500 ml-auto">5m ago</span>
            </div>
            <div className="flex items-center space-x-3 p-2 bg-slate-700/30 rounded">
              <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Security vulnerability detected</span>
              <span className="text-xs text-gray-500 ml-auto">8m ago</span>
            </div>
            <div className="flex items-center space-x-3 p-2 bg-slate-700/30 rounded">
              <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Agent Monitor-01 restarted</span>
              <span className="text-xs text-gray-500 ml-auto">12m ago</span>
            </div>
          </div>
        </div>
      </div>

      {/* Network Status */}
      <LiveNetworkStatus />

      {/* Process Flow Map */}
      <ProcessFlowMap />
    </div>
  );
};
