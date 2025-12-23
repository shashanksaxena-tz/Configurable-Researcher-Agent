import axios from "axios";

const BASE = import.meta.env.VITE_API_URL || "/api/v1";

const api = axios.create({
  baseURL: BASE,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getModules = async () => {
  const response = await api.get("/modules");
  return response.data;
};

export const performResearch = async (data) => {
  const response = await api.post("/research", data);
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get("/health");
  return response.data;
};

export default api;
