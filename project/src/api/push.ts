import axios from "axios";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getProcessFlowData = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/agents/process/flow`);
    console.log("Process Flow Data:", response.data);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch process flow:", error);
    return [];
  }
};


export const streamGithubPushLogs = (
  onMessage: (data: string) => void,
  onError?: (error: Event) => void
): EventSource => {
  const eventSource = new EventSource(`${API_BASE_URL}/github/push/stream`);

  eventSource.onmessage = (event) => {
    onMessage(event.data);
  };

  eventSource.onerror = (error) => {
    if (onError) onError(error);
    eventSource.close();
  };

  return eventSource;
};