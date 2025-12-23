import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getModules = async () => {
  const response = await api.get('/api/v1/modules');
  return response.data;
};

export const performResearch = async (data) => {
  const response = await api.post('/api/v1/research', data);
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/api/v1/health');
  return response.data;
};
