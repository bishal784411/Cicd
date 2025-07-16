import { useState, useEffect, useCallback } from 'react';

interface NetworkStatus {
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
}

export const useNetworkConnectivity = () => {
  const [networkStatus, setNetworkStatus] = useState<NetworkStatus>({
    isOnline: navigator.onLine,
    latency: null,
    lastCheck: new Date(),
    endpoints: [
      { name: 'API Server', url: 'http://localhost:5000', status: 'offline', latency: null, lastCheck: new Date() },
       { name: 'Google', url: 'https://www.google.com', status: 'offline', latency: null, lastCheck: new Date() },
    //   { name: 'Docker Registry', url: 'https://registry.hub.docker.com', status: 'offline', latency: null, lastCheck: new Date() },
      { name: 'GitHub', url: 'https://api.github.com', status: 'offline', latency: null, lastCheck: new Date() },
      { name: 'NPM Registry', url: 'https://registry.npmjs.org', status: 'offline', latency: null, lastCheck: new Date() }
    ]
  });
  const [isChecking, setIsChecking] = useState(false);

  const checkEndpoint = async (endpoint: { name: string; url: string }) => {
    const startTime = Date.now();
    try {
      // For demo purposes, simulate network checks with random results
      await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 500));
      
      const latency = Date.now() - startTime;
      const isOnline = Math.random() > 0.2; // 80% success rate for demo
      
      return {
        ...endpoint,
        status: isOnline ? 'online' : 'offline' as const,
        latency: isOnline ? latency : null,
        lastCheck: new Date()
      };
    } catch (error) {
      return {
        ...endpoint,
        status: 'offline' as const,
        latency: null,
        lastCheck: new Date()
      };
    }
  };

  const checkNetworkConnectivity = useCallback(async () => {
    setIsChecking(true);
    
    try {
      // Update all endpoints to checking status
      setNetworkStatus(prev => ({
        ...prev,
        endpoints: prev.endpoints.map(endpoint => ({
          ...endpoint,
          status: 'checking'
        }))
      }));

      // Check all endpoints
      const updatedEndpoints = await Promise.all(
        networkStatus.endpoints.map(endpoint => checkEndpoint(endpoint))
      );

      const onlineEndpoints = updatedEndpoints.filter(e => e.status === 'online');
      const avgLatency = onlineEndpoints.length > 0 
        ? Math.round(onlineEndpoints.reduce((acc, e) => acc + (e.latency || 0), 0) / onlineEndpoints.length)
        : null;

      setNetworkStatus({
        isOnline: onlineEndpoints.length > 0,
        latency: avgLatency,
        lastCheck: new Date(),
        endpoints: updatedEndpoints
      });
    } catch (error) {
      console.error('Network connectivity check failed:', error);
    } finally {
      setIsChecking(false);
    }
  }, []);

  // Auto-check on mount and when online status changes
  useEffect(() => {
    checkNetworkConnectivity();
    
    const handleOnlineStatusChange = () => {
      setNetworkStatus(prev => ({
        ...prev,
        isOnline: navigator.onLine,
        lastCheck: new Date()
      }));
      if (navigator.onLine) {
        checkNetworkConnectivity();
      }
    };

    window.addEventListener('online', handleOnlineStatusChange);
    window.addEventListener('offline', handleOnlineStatusChange);

    return () => {
      window.removeEventListener('online', handleOnlineStatusChange);
      window.removeEventListener('offline', handleOnlineStatusChange);
    };
  }, [checkNetworkConnectivity]);

  return {
    networkStatus,
    isChecking,
    checkNetworkConnectivity
  };
};