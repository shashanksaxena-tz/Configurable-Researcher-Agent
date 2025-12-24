/**
 * API Service - Axios client for backend communication
 */

import axios from 'axios';

// API base URL - defaults to localhost in development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with defaults
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 180000, // 3 minute timeout (SC-010: under 3 minutes)
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for logging
api.interceptors.request.use(
    (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        const errorMessage = error.response?.data?.detail || error.message || 'Unknown error';
        console.error('[API] Response error:', errorMessage);
        return Promise.reject(error);
    }
);

export default api;

// Convenience methods
export const researchApi = {
    /**
     * Generate a research plan (preview only)
     */
    async createPlan(query, depthLevel = 'standard') {
        const response = await api.post('/api/research/plan', null, {
            params: { query, depth_level: depthLevel }
        });
        return response.data;
    },

    /**
     * Execute full research workflow
     */
    async executeResearch(query, depthLevel = 'standard') {
        const response = await api.post('/api/research/execute', {
            id: crypto.randomUUID?.() || Date.now().toString(),
            query,
            depth_level: depthLevel
        });
        return response.data;
    },

    /**
     * Get research status
     */
    async getStatus(requestId) {
        const response = await api.get(`/api/research/${requestId}/status`);
        return response.data;
    },

    /**
     * Get completed report
     */
    async getReport(requestId) {
        const response = await api.get(`/api/research/${requestId}/report`);
        return response.data;
    },

    /**
     * Get citations for a report
     */
    async getCitations(requestId) {
        const response = await api.get(`/api/research/${requestId}/citations`);
        return response.data;
    }
};
