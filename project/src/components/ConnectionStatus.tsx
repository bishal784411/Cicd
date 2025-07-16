import React from 'react';
import { Wifi, WifiOff, RotateCcw } from 'lucide-react';

interface ConnectionStatusProps {
  status: 'connected' | 'disconnected' | 'reconnecting';
  lastRefresh: Date;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ status, lastRefresh }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'connected':
        return {
          icon: Wifi,
          text: 'Connected',
          className: 'text-green-400 bg-green-500/20'
        };
      case 'reconnecting':
        return {
          icon: RotateCcw,
          text: 'Reconnecting',
          className: 'text-yellow-400 bg-yellow-500/20 animate-spin'
        };
      case 'disconnected':
      default:
        return {
          icon: WifiOff,
          text: 'Disconnected',
          className: 'text-red-400 bg-red-500/20'
        };
    }
  };

  const { icon: Icon, text, className } = getStatusConfig();

  const formatLastRefresh = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="flex items-center space-x-3">
      <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${className}`}>
        <Icon className="h-4 w-4" />
        <span className="text-sm font-medium">{text}</span>
      </div>
    </div>
  );
};