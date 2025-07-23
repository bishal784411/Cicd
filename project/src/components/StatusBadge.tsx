import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Clock, Wrench, Shield } from 'lucide-react';

interface StatusBadgeProps {
  status: 'healthy' | 'detected' | 'warning' | 'critical' | 'fixing' | 'fixed' | 'unknown' | 'Solved';
  errorCount?: number;
  criticalCount?: number;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, errorCount = 0, criticalCount = 0 }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'healthy':
        return {
          icon: CheckCircle,
          text: 'Healthy',
          className: 'bg-green-500/20 text-green-400 border-green-500/30'
        };
      case 'detected':
        return {
          icon: CheckCircle,
          text: 'Healthy',
          className: 'bg-green-500/20 text-green-400 border-green-500/30'
        };
      case 'warning':
        return {
          icon: AlertTriangle,
          text: `${errorCount} Issue${errorCount !== 1 ? 's' : ''}`,
          className: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
        };
      case 'critical':
        return {
          icon: XCircle,
          text: `${criticalCount} Critical`,
          className: 'bg-red-500/20 text-red-400 border-red-500/30'
        };
      case 'fixing':
        return {
          icon: Wrench,
          text: 'Auto-Fixing',
          className: 'bg-blue-500/20 text-blue-400 border-blue-500/30 animate-pulse'
        };
      case 'fixed':
        return {
          icon: Shield,
          text: 'Fixed',
          className: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
        };
      
      case 'Solved':
        return {
          icon: Shield,
          text: 'Fixed',
          className: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
        };
      case 'unknown':
      default:
        return {
          icon: Clock,
          text: 'Detected',
          className: 'bg-gray-500/20 text-gray-400 border-gray-500/30'
        };
    }
  };

  const { icon: Icon, text, className } = getStatusConfig();

  return (
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full border text-sm font-medium ${className}`}>
      <Icon className="h-4 w-4" />
      <span>{text}</span>
    </div>
  );
};