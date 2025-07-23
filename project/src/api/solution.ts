// src/api/monitoring.ts
import axios from 'axios';



const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch latest error report
export const getLatestSolutionData = async () => {
  const response = await axios.get(`${API_BASE_URL}/solutions`);
  console.log("here: ", response.data)
  return response.data;
};




export const startSolution = async () => {
  const response = await axios.post(`${API_BASE_URL}/start/solution`);
  return response.data;
};

// Stop the monitor
export const stopSolution = async () => {
  const response = await axios.post(`${API_BASE_URL}/stop/solution`);
  return response.data;
};


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