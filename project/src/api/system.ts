// api/system.ts
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getLatestSystemMetrics() {
  const res = await axios.get(`${API_BASE_URL}/system/usages`);
  console.log("Here: ", res)
  return res.data;
}
