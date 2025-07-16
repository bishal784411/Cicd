import React from 'react';
import { Wifi, WifiOff, RefreshCw, Globe, Server, GitBranch, SatelliteDish, Package } from 'lucide-react';
// import { FaChrome } from 'react-icons/fa'; 

interface NetworkStatusProps {
  networkStatus: {
    isOnline: boolean;
    latency: number | null;
    lastCheck: Date;
    endpoints: {
      name: string;
      url: string;
      status: 'online' | 'offline' | 'checking';
      latency: number | null;
      lastCheck: Date;
    }[];
  };
  isChecking: boolean;
  onCheck: () => void;
}

export const NetworkStatus: React.FC<NetworkStatusProps> = ({ 
  networkStatus, 
  isChecking, 
  onCheck 
}) => {
  const getEndpointIcon = (name: string) => {
    switch (name) {
      case 'API Server': return Server;
      case 'Google': return SatelliteDish;
      case 'GitHub': return GitBranch;
      case 'NPM Registry': return Package;
      default: return Globe;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-green-400 bg-green-500/20';
      case 'offline': return 'text-red-400 bg-red-500/20';
      case 'checking': return 'text-yellow-400 bg-yellow-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 sm:p-6 border border-slate-700/50">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 gap-3">
        <h3 className="text-lg font-semibold text-white flex items-center">
          {networkStatus.isOnline ? (
            <Wifi className="h-5 w-5 mr-2 text-green-400" />
          ) : (
            <WifiOff className="h-5 w-5 mr-2 text-red-400" />
          )}
          Network Connectivity
        </h3>
        <button
          onClick={onCheck}
          disabled={isChecking}
          className="flex items-center space-x-2 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-50 text-white rounded-lg transition-colors text-sm"
        >
          <RefreshCw className={`h-4 w-4 ${isChecking ? 'animate-spin' : ''}`} />
          <span>Check Now</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        {networkStatus.endpoints.map((endpoint, index) => {
          const Icon = getEndpointIcon(endpoint.name);
          return (
            <div
              key={index}
              className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30"
            >
              <div className="flex items-center space-x-2 mb-2">
                <Icon className="h-4 w-4 text-gray-400" />
                <span className="text-sm font-medium text-white truncate">{endpoint.name}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(endpoint.status)}`}>
                  {endpoint.status === 'checking' ? (
                    <RefreshCw className="h-3 w-3 animate-spin inline mr-1" />
                  ) : null}
                  {endpoint.status.toUpperCase()}
                </div>
                {endpoint.latency && (
                  <span className="text-xs text-gray-400">{endpoint.latency}ms</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between text-sm text-gray-400 gap-2">
        <div className="flex items-center space-x-4">
          <span>Overall Status: 
            <span className={networkStatus.isOnline ? 'text-green-400' : 'text-red-400'}>
              {networkStatus.isOnline ? ' Connected' : ' Disconnected'}
            </span>
          </span>
          {networkStatus.latency && (
            <span>Avg Latency: <span className="text-white">{networkStatus.latency}ms</span></span>
          )}
        </div>
        <span>Last checked: {networkStatus.lastCheck.toLocaleTimeString()}</span>
      </div>
    </div>
  );
};