// src/api/fix.ts
import axios from 'axios';



const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch latest error report
export const getAllFixData = async () => {
  const response = await axios.get(`${API_BASE_URL}/fixes`);
  return response.data;
};


export const startfix = async () => {
  const response = await axios.post(`${API_BASE_URL}/start/fix`);
  return response.data;
};

export const stopfix = async () => {
  const response = await axios.post(`${API_BASE_URL}/stop/fix`);
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
