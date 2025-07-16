import { Key, ReactNode } from "react";

export interface ErrorEntry {
  fix_id: Key | null | undefined;
  err_id: string;
  timestamp: string;
  file: string;
  error_type: 'DOCKERFILE' | 'NETWORK' | 'BUILD' | 'DEPLOYMENT' | 'SECURITY' | 'PERFORMANCE' | 'CONFIG' | 'TEST';
  line_number?: number;
  message: string;
  ai_analysis?: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  fix_suggestion?: string;
  auto_fixable?: boolean;
  fix_applied?: boolean;
  fix_timestamp?: string;
  pipeline_stage?: 'build' | 'test' | 'deploy' | 'post-deploy';
  commit_hash?: string;
  branch?: string;
}



export interface FixEntry {
  auto_fixable: ((fixIndex: number) => void) | undefined;
  fix_applied: any;
  commit_hash: ReactNode;
  branch: ReactNode;
  fix_id: string;
  solution_id: string;
  err_id: string;
  timestamp: string;
  file: string;
  language: string;
  errors: string[];
  status: 'fixed' | 'healthy' | 'detected' | 'warning' | 'critical' | 'fixing' | 'unknown';
  applied_at?: string;
  ai_analysis?: {
    decision: string;
    risk_level: string;
    confidence: number;
    reasoning: string;
    safety_notes: string;
    related_error: string;
  }[];
  error_type: string;
  recommendations?: string;
  isPushed: boolean;
  error_push: string | null;
}

export interface FileStatusFix {
  file: string;
  status: string;
  build_status?: string;
  uptime_percentage?: number;
  last_checked: string;
  last_fix_attempt?: string;
  pipeline_stage?: string;
  error_count: number;
  critical_count: number | undefined;
  errors: FixEntry[];
  fixes: any; // optional: can be typed if needed
}

export interface FixMonitorData {
  total_files: number;
  files_with_errors: number;
  critical_issues: number;
  metrics: {
    docker_containers_running: number;
    [key: string]: number;
  };
  system_health: string;
  agent_status: string;
  pipeline_status: string;
  files: FileStatusFix[];
}

export interface FileStatus {
  file: string;
  status: 'healthy' | 'warning' | 'critical' | 'fixing' | 'fixed' | 'unknown';
  last_checked: string;
  error_count: number;
  critical_count: number;
  errors: ErrorEntry[];
  uptime_percentage?: number;
  last_fix_attempt?: string;
  pipeline_stage?: string;
  build_status?: 'success' | 'failed' | 'running' | 'pending';
}

export type PipelineStage = 'build' | 'test' | 'deploy' | 'solving' | 'unknown';

export interface SolutionMeta {
  code: string | null | undefined;
  Solution_Type: ReactNode;
  id: string;
  name: string;
  description: string;
  category: string;
  status: 'active' | 'failed' | 'pending' | 'inactive';
  error_types: string[];
  pipeline_stages: PipelineStage[];
  created_by: string;
  created_at: string;      // ISO date string
  last_executed: string;   // ISO date string
  execution_count: number;
  success_rate: number;    // 0-100
  avg_execution_time: number; // seconds
  auto_trigger: boolean;
}

export interface SolutionStatus {
  last_fix_attempt: string | null;   // ISO date string or null if never
  file: string;
  last_checked: string;    // ISO date string
  status: 'detected' | 'fixing' | 'fixed' | 'critical' | 'healthy' | 'unknown';
  error_count: number;
  errors: string[];
  uptime_percentage: number;
  pipeline_stage: PipelineStage;
  build_status: 'success' | 'running' | 'failed' | 'pending';
  critical_count: number;
  Solution_Type: string;
  solutions: SolutionMeta[];
}

export interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_latency?: number;
  active_pipelines: number;
  successful_deployments_today: number;
  failed_builds_today: number;
  docker_containers_running: number;
}

export interface MonitoringData {
  last_updated: string;
  total_files: number;
  files_with_errors: number;
  critical_issues: number;
  system_health: 'healthy' | 'degraded' | 'critical';
  files: FileStatus[];
  metrics: SystemMetrics;
  agent_status: 'active' | 'idle' | 'error' | 'maintenance';
  pipeline_status: 'running' | 'idle' | 'failed' | 'success';
}

export interface Solutions {
  id: string;
  name: string;
  description: string;
  category: 'docker' | 'network' | 'build' | 'deployment' | 'security' | 'testing';
  status: 'active' | 'inactive' | 'pending' | 'failed';
  success_rate: number;
  last_executed: string;
  execution_count: number;
  avg_execution_time: number;
  error_types: string[];
  auto_trigger: boolean;
  created_by: string;
  created_at: string;
  pipeline_stages: string[];
}



export interface Solution {
  solution_id: string;
  timestamp: string;
  file: string;
  backup_path: string;
  errors: string[];
  available_solutions: {
    error: string;
    explanation: {
      text: string;
      code_example: string;
    };
  }[];
  model_confidence: number;
  time_estimate_fix: string;
  status: 'pending_review' | 'fixed' | 'failed';
  auto_apply: boolean;
  requires_manual_review: boolean;
  error_type: string;
  pipeline_stage: string;
  commit_hash: string;
  branch: string;
  solutions: SolutionMeta[];
}


export interface Agent {
  id: string;
  name: string;
  type: 'pipeline' | 'docker' | 'network' | 'security' | 'testing' | 'deployment';
  status: 'online' | 'offline' | 'busy' | 'error' | 'maintenance';
  health: 'healthy' | 'warning' | 'critical';
  last_heartbeat: string;
  uptime: number;
  cpu_usage: number;
  memory_usage: number;
  tasks_completed: number;
  tasks_failed: number;
  version: string;
  location: string;
  capabilities: string[];
  current_task?: string;
  queue_size: number;
  pipeline_stage?: string;
  docker_containers?: number;
}