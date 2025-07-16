// src/api/monitoring.ts
import axios from 'axios';



const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch latest error report
export const getLatestMonitoringData = async () => {
  const response = await axios.get(`${API_BASE_URL}/errors`);
  return response.data;
};



// Start the monitor
export const startMonitor = async () => {
  const response = await axios.post(`${API_BASE_URL}/start/monitor`);
  return response.data;
};

// Stop the monitor
export const stopMonitor = async () => {
  const response = await axios.post(`${API_BASE_URL}/stop/monitor`);
  return response.data;
};

// Create an EventSource stream for logs
export const createLogStream = (
  agentName: string,
  onMessage: (msg: string) => void
): EventSource => {
  const eventSource = new EventSource(`${API_BASE_URL}/agent/${agentName}/logs/stream`);

  eventSource.onmessage = (event) => {
    onMessage(event.data);
  };

  eventSource.onerror = (event) => {
    console.error('EventSource error:', event);
    eventSource.close();
  };

  return eventSource;
};


export const resolveErrorById = (errId: string, onMessage: (log: string) => void) => {
  const eventSource = new EventSource(`${API_BASE_URL}/solution/${errId}/stream/logs`);

  eventSource.onmessage = (event) => {
    onMessage(event.data);
  };

  eventSource.onerror = () => {
    eventSource.close();
  };

  return eventSource;
};
