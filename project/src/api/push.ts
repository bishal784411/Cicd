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
