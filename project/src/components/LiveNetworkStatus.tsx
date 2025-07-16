import { useEffect, useState } from 'react';
import { NetworkStatus } from './NetworkStatus';

export const LiveNetworkStatus = () => {
  const [networkStatus, setNetworkStatus] = useState<any>({
    isOnline: false,
    latency: null,
    lastCheck: new Date(),
    endpoints: [],
  });
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5000/api/network/status');

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      const endpoints = [
        {
          name: 'API Server',
          url: `http://${data.backend.host}:${data.backend.port}`,
          status: data.backend.reachable ? 'online' : 'offline',
          latency: data.wifi_latency_ms,
          lastCheck: new Date(),
        },
        {
          name: 'Google',
          url: 'https://www.google.com',
          status: data.external_services["google.com"] ? 'online' : 'offline',
          latency: null,
          lastCheck: new Date(),
        },
        {
          name: 'GitHub',
          url: 'https://github.com',
          status: data.external_services["github.com"] ? 'online' : 'offline',
          latency: null,
          lastCheck: new Date(),
        },
        {
          name: 'NPM Registry',
          url: 'https://registry.npmjs.org',
          status: data.external_services["npm_registry"] ? 'online' : 'offline',
          latency: null,
          lastCheck: new Date(),
        },
      ];

      setNetworkStatus({
        isOnline: endpoints.every(e => e.status === 'online'),
        latency: data.wifi_latency_ms,
        lastCheck: new Date(),
        endpoints,
      });
    };

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const checkNetworkConnectivity = () => {
    setIsChecking(true);
    // Optionally trigger a manual check (noop in your current backend)
    setTimeout(() => setIsChecking(false), 1000);
  };

  return (
    <NetworkStatus
      networkStatus={networkStatus}
      isChecking={isChecking}
      onCheck={checkNetworkConnectivity}
    />
  );
};
